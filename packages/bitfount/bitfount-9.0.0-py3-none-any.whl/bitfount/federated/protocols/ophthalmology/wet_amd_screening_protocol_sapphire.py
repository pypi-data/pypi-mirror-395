"""Wet AMD multi-algorithm protocol for Sapphire trial."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import time
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union, cast

import desert
from marshmallow import fields
import pandas as pd

from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.federated.algorithms.base import NoResultsModellerAlgorithm
from bitfount.federated.algorithms.ehr.ehr_patient_query_algorithm import (
    EHRPatientQueryAlgorithm,
    _WorkerSide as _EHRQueryWorkerSide,
)
from bitfount.federated.algorithms.model_algorithms.inference import (
    ModelInference,
    _ModellerSide as _InferenceModellerSide,
    _WorkerSide as _InferenceWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.cst_calculation_algorithm import (
    CSTCalculationAlgorithm,
    _WorkerSide as _CSTWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.csv_report_generation_ophth_algorithm import (  # noqa: E501
    CSVReportGeneratorOphthalmologyAlgorithm,
    _WorkerSide as _CSVWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.fluid_volume_calculation_algorithm import (  # noqa: E501
    FluidVolumeCalculationAlgorithm,
    _WorkerSide as _FVCalcWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.ga_trial_inclusion_criteria_match_algorithm_sapphire import (  # noqa: E501
    TrialInclusionCriteriaMatchAlgorithmSapphire,
    _WorkerSide as _TrialInclWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.longitudinal_algorithm import (
    LongitudinalAlgorithm,
    _WorkerSide as _LongitudinalWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    _BITFOUNT_PATIENT_ID_KEY,
    _BITFOUNT_PATIENT_ID_RENAMED,
    AGE_COL,
    DEFAULT_COLUMNS_TO_RENAME,
    DICOM_COLUMNS_TO_RENAME,
    DOB_COL,
    FILTER_FAILED_REASON_COLUMN,
    FILTER_MATCHING_COLUMN,
    HEIDELBERG_COLUMNS_TO_RENAME,
    LATERALITY_COL,
    NAME_COL,
    SEX_COL,
    CSTMetrics,
    FluidVolumeMetrics,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_utils import (
    _convert_predict_return_type_to_dataframe,
)
from bitfount.federated.algorithms.ophthalmology.simple_csv_algorithm import (
    _SimpleCSVAlgorithm,
    _WorkerSide as _SimpleCSVWorkerSide,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseProtocolFactory,
    BaseWorkerProtocol,
    ModelInferenceProtocolMixin,
    ProtocolState,
)
from bitfount.federated.protocols.ophthalmology.utils import (
    GenericOphthalmologyModellerSide,
)
from bitfount.federated.protocols.types import GroupingConfig
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.opentelemetry import get_task_meter
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import ProtocolContext
from bitfount.types import T_FIELDS_DICT

if TYPE_CHECKING:
    from bitfount.federated.pod_vitals import _PodVitals
    from bitfount.hub.api import BitfountHub

_logger = _get_federated_logger(f"bitfount.federated.protocols.{__name__}")


# These are the columns we'll need to aggregate over time
SAPPHIRE_LONGITUDINAL_COLUMNS = [
    "srf_total_fluid_volume",
    "irf_total_fluid_volume",
    "cst_mean_um",
]


SAPPHIRE_CSV_RENAME_COLS = {
    "cst_mean_um": "CST (µm)",
    "irf_total_fluid_volume": "IRF volume (nL)",
    "srf_total_fluid_volume": "SRF volume (nL)",
    "srf_largest_lesion_volume": "Largest SRF lesion (nL)",
    "measurement_type": "CST Measurement Layers",
}
SAPPHIRE_METRICS_COLS = list(SAPPHIRE_CSV_RENAME_COLS.keys())

ELIGIBILITY_COLUMN_ORDER = [
    "Study name",
    _BITFOUNT_PATIENT_ID_KEY,
    NAME_COL,
    DOB_COL,
    SEX_COL,
    AGE_COL,
    LATERALITY_COL,
    FILTER_MATCHING_COLUMN,
    "Context for Aflibercept Response Criteria",
    "srf_total_fluid_volume_longitudinal",
    "irf_total_fluid_volume_longitudinal",
    "cst_mean_um_longitudinal",
]


class _ModellerSide(GenericOphthalmologyModellerSide):
    """Modeller side of the protocol.

    Args:
        algorithm: The sequence of GA modeller algorithms to be used.
        mailbox: The mailbox to use for communication with the Workers.
        ehr_enabled: Whether to enable EHR processing.
        **kwargs: Additional keyword arguments.

    """

    def __init__(
        self,
        *,
        algorithm: Sequence[Union[_InferenceModellerSide, NoResultsModellerAlgorithm]],  # noqa: E501
        mailbox: _ModellerMailbox,
        ehr_enabled: bool = False,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)
        self.ehr_enabled = ehr_enabled

    async def run(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> Union[list[Any], Any]:
        """Runs Modeller side of the protocol.

        This just sends the model parameters to the workers sequentially and then tells
        the workers when the protocol is finished.

        Args:
            context: Optional. Run-time context for the protocol.
            **kwargs: Additional keyword arguments.
        """
        # Check if EHR algorithm is present (always first position if present)
        has_ehr_algo = (
            len(self.algorithm) > 0
            and hasattr(self.algorithm[0], "class_name")
            and self.algorithm[0].class_name == "bitfount.EHRPatientQueryAlgorithm"
        )

        # Filter algorithms based on ehr_enabled flag
        # If EHR is present but disabled, skip it; otherwise process all algorithms
        if has_ehr_algo and not self.ehr_enabled:
            # Skip the first algorithm (EHR) if it's present but disabled
            algorithms_to_process = self.algorithm[1:]
        else:
            # Process all algorithms (either no EHR or EHR is enabled)
            algorithms_to_process = self.algorithm

        results = []

        for algo in algorithms_to_process:
            _logger.info(f"Running algorithm {algo.class_name}")
            result = await self.mailbox.get_evaluation_results_from_workers()
            results.append(result)
            _logger.info("Received results from Pods.")
            _logger.info(f"Algorithm {algo.class_name} completed.")

        final_results = [
            algo.run(result_) for algo, result_ in zip(algorithms_to_process, results)
        ]

        return final_results


class _WorkerSide(BaseWorkerProtocol, ModelInferenceProtocolMixin):
    """Worker side of the Wet-AMD Sapphire protocol.

    Args:
        algorithm: The sequence of model inference algorithms and CSV report generator
            to be used.
        mailbox: The mailbox to use for communication with the Modeller.
        **kwargs: Additional keyword arguments.
    """

    algorithm: Sequence[
        Union[
            _EHRQueryWorkerSide,
            _InferenceWorkerSide,
            _FVCalcWorkerSide,
            _CSTWorkerSide,
            _LongitudinalWorkerSide,
            _TrialInclWorkerSide,
            _CSVWorkerSide,
            _SimpleCSVWorkerSide,
        ]
    ]

    def __init__(
        self,
        *,
        algorithm: Sequence[
            Union[
                _EHRQueryWorkerSide,
                _InferenceWorkerSide,
                _FVCalcWorkerSide,
                _CSTWorkerSide,
                _LongitudinalWorkerSide,
                _TrialInclWorkerSide,
                _CSVWorkerSide,
                _SimpleCSVWorkerSide,
            ]
        ],
        mailbox: _WorkerMailbox,
        results_notification_email: bool = False,
        rename_columns: Optional[Mapping[str, str]] = None,
        trial_name: Optional[str] = None,
        batch_grouping: Optional[Mapping[str, Any]] = None,
        ehr_enabled: bool = False,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)
        self.batch_grouping = batch_grouping
        self.results_notification_email = results_notification_email
        self.rename_columns = rename_columns
        self.trial_name = trial_name
        self._task_meter = get_task_meter()
        self._task_id: str = mailbox._task_id
        self.ehr_enabled = ehr_enabled

    def define_csv_output_rename_columns(self) -> dict[str, str]:
        """Define the columns that will be renamed in the CSV output."""
        rename_columns = {}
        # Start with common default columns
        rename_columns.update(DEFAULT_COLUMNS_TO_RENAME)
        # Add datasource-specific columns (DICOM and Heidelberg)
        rename_columns.update(DICOM_COLUMNS_TO_RENAME)
        rename_columns.update(HEIDELBERG_COLUMNS_TO_RENAME)
        rename_columns.update(SAPPHIRE_CSV_RENAME_COLS)
        # Allow custom overrides from protocol arguments
        if self.rename_columns:
            rename_columns.update(self.rename_columns)
        return rename_columns

    async def run(
        self,
        *,
        pod_vitals: Optional[_PodVitals] = None,
        context: ProtocolContext,
        batch_num: Optional[int] = None,
        protocol_state: Optional[ProtocolState] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Runs Wet-AMD inference algorithms on worker side followed by CSV algorithm.

        Args:
            pod_vitals: Optional. Pod vitals instance for recording run-time details
                from the protocol run.
            context: Run-time context for the protocol. Optional, defaults to None.
            batch_num: The number of the batch being run.
            protocol_state: State of the protocol, used to signal final reduce.
            **kwargs: Additional keyword arguments.
        """
        self.rename_columns = self.define_csv_output_rename_columns()

        # Check if EHR algorithm is present (always first position if present)
        has_ehr_algo = (
            len(self.algorithm) > 0
            and hasattr(self.algorithm[0], "class_name")
            and self.algorithm[0].class_name == "bitfount.EHRPatientQueryAlgorithm"
        )

        # Validate ehr_enabled flag
        if self.ehr_enabled and not has_ehr_algo:
            _logger.warning(
                "ehr_enabled=True but EHRPatientQueryAlgorithm not found in "
                "algorithm sequence. Skipping EHR processing."
            )

        # Unpack the algorithms from the list
        # If EHR is present and enabled, include it; otherwise skip it
        if has_ehr_algo and self.ehr_enabled:
            # EHR present and enabled - unpack all 11 algorithms
            (
                ehr_query_algo,
                fovea_landmark_algo,
                pathology_model_algo,
                retinal_layers_algo,
                irf_fluid_volume_calc_algo,
                srf_fluid_volume_calc_algo,
                cst_calculation_algo,
                longitudinal_algo,
                trial_incl_algo,
                csv_report_algo,
                simple_csv_algo,
            ) = self.algorithm
            ehr_query_algo = cast(_EHRQueryWorkerSide, ehr_query_algo)
        else:
            # EHR not present or disabled - skip first element if EHR is present
            start_idx = 1 if has_ehr_algo else 0
            (
                fovea_landmark_algo,
                pathology_model_algo,
                retinal_layers_algo,
                irf_fluid_volume_calc_algo,
                srf_fluid_volume_calc_algo,
                cst_calculation_algo,
                longitudinal_algo,
                trial_incl_algo,
                csv_report_algo,
                simple_csv_algo,
            ) = self.algorithm[start_idx:]
            ehr_query_algo = None

        # Cast to appropriate types for type checking
        fovea_landmark_algo = cast(_InferenceWorkerSide, fovea_landmark_algo)
        pathology_model_algo = cast(_InferenceWorkerSide, pathology_model_algo)
        retinal_layers_algo = cast(_InferenceWorkerSide, retinal_layers_algo)
        irf_fluid_volume_calc_algo = cast(_FVCalcWorkerSide, irf_fluid_volume_calc_algo)
        srf_fluid_volume_calc_algo = cast(_FVCalcWorkerSide, srf_fluid_volume_calc_algo)
        cst_calc_algo = cast(_CSTWorkerSide, cst_calculation_algo)
        longitudinal_algo = cast(_LongitudinalWorkerSide, longitudinal_algo)
        trial_incl_algo = cast(_TrialInclWorkerSide, trial_incl_algo)
        csv_report_algo = cast(_CSVWorkerSide, csv_report_algo)
        simple_csv_algo = cast(_SimpleCSVWorkerSide, simple_csv_algo)

        if pod_vitals:
            pod_vitals.last_task_execution_time = time.time()
        data_with_ehr: Optional[pd.DataFrame]

        if self.ehr_enabled and ehr_query_algo is not None:
            _logger.info("Running EHR Query Algo")
            # Retrieve the data for this run
            # This should only read the current batch into memory (roughly 16 rows)
            dfs: list[pd.DataFrame] = list(self.datasource.yield_data(use_cache=True))
            if any(not df.empty for df in dfs):
                file_data = pd.concat(dfs, axis="index")
                # Run EHR Query Algorithm
                _logger.info("Running EHR Patient Query Algorithm")
                query_results = ehr_query_algo.run(
                    file_data,
                    get_appointments=True,
                    get_conditions_and_procedures=True,
                    get_practitioner=False,
                    get_visual_acuity=True,
                )
                data_with_ehr = ehr_query_algo.merge_results_with_dataframe(
                    query_results,
                    file_data,
                )
                # Remove full dataframe from memory once necessary info is used
                del file_data
                _logger.info(
                    f"EHR query algorithm completed: {len(query_results)} records found"
                )
                await self.mailbox.send_evaluation_results({})
            else:
                _logger.warning(
                    "No file data was extracted. No queries to EHR will be made."
                )
                data_with_ehr = None
        else:
            data_with_ehr = None
            if not self.ehr_enabled:
                _logger.info("Skipping EHR Query Algo as ehr_enabled is set to False.")

        # Run model inference algorithms in specific order
        all_predictions_df = pd.DataFrame()

        # Run Fovea Center Landmark Detection Model
        _logger.info("Running Fovea Center Landmark Detection Model")
        fovea_predictions = fovea_landmark_algo.run(return_data_keys=True)
        fovea_predictions_df = _convert_predict_return_type_to_dataframe(
            fovea_predictions
        )
        _logger.info(
            f"Fovea landmark detection completed: "
            f"{len(fovea_predictions_df)} predictions generated"
        )

        # Apply usage limits for fovea landmark model
        (
            fovea_predictions_df,
            fovea_limits_exceeded_info,
            _,
        ) = self.apply_usage_limits(context, fovea_predictions_df, fovea_landmark_algo)

        # Signal final step if fovea limits were exceeded
        if fovea_limits_exceeded_info:
            self._signal_final_step_for_limits_exceeded(protocol_state)

        # Send fovea results to modeller
        await self.mailbox.send_evaluation_results(
            eval_results={},
            resources_consumed=self.apply_actual_usage_to_resources_consumed(
                fovea_landmark_algo,
                fovea_limits_exceeded_info,
            ),
        )
        # Try to get data keys from the predictions, if present
        try:
            fovea_filenames: list[str] = fovea_predictions_df[
                ORIGINAL_FILENAME_METADATA_COLUMN
            ].tolist()
        except KeyError as ke:
            # `filenames` is needed below, fail out if we cannot find them for this
            # protocol
            msg = (
                "Unable to find data keys/filenames in "
                "FoveaLandmarkModel; unable to continue. "
            )
            _logger.critical(msg)
            raise ValueError(msg) from ke
        #
        # Run Altris Configurable Pathology Model
        _logger.info("Running Altris Configurable Pathology Model")
        pathology_predictions = pathology_model_algo.run(return_data_keys=True)
        pathology_predictions_df = _convert_predict_return_type_to_dataframe(
            pathology_predictions
        )
        _logger.info(
            f"Pathology model completed: "
            f"{len(pathology_predictions_df)} predictions generated"
        )

        # Apply usage limits for pathology model
        (
            pathology_predictions_df,
            pathology_limits_exceeded_info,
            _,
        ) = self.apply_usage_limits(
            context, pathology_predictions_df, pathology_model_algo
        )

        # Try to get data keys from the predictions, if present
        try:
            pathology_filenames: list[str] = pathology_predictions_df[
                ORIGINAL_FILENAME_METADATA_COLUMN
            ].tolist()
        except KeyError as ke:
            # `filenames` is needed below, fail out if we cannot find them for this
            # protocol
            msg = (
                "Unable to find data keys/filenames in "
                "PathologyModel; unable to continue. "
            )
            _logger.critical(msg)
            raise ValueError(msg) from ke

        # Signal final step if pathology limits were exceeded
        if pathology_limits_exceeded_info:
            self._signal_final_step_for_limits_exceeded(protocol_state)

        # Send pathology results to modeller
        await self.mailbox.send_evaluation_results(
            eval_results={},
            resources_consumed=self.apply_actual_usage_to_resources_consumed(
                pathology_model_algo,
                pathology_limits_exceeded_info,
            ),
        )

        # Run Altris Retinal Layers Model
        _logger.info("Running Altris Retinal Layers Model")
        retinal_layers_predictions = retinal_layers_algo.run(return_data_keys=True)
        retinal_layers_predictions_df = _convert_predict_return_type_to_dataframe(
            retinal_layers_predictions
        )
        _logger.info(
            f"Retinal layers model completed: "
            f"{len(retinal_layers_predictions_df)} predictions generated"
        )

        # Apply usage limits for retinal layers model
        (
            retinal_layers_predictions_df,
            retinal_limits_exceeded_info,
            _,
        ) = self.apply_usage_limits(
            context, retinal_layers_predictions_df, retinal_layers_algo
        )

        # Try to get data keys from the predictions, if present
        try:
            retinal_layers_filenames: list[str] = retinal_layers_predictions_df[
                ORIGINAL_FILENAME_METADATA_COLUMN
            ].tolist()
        except KeyError as ke:
            # `filenames` is needed below, fail out if we cannot find them for this
            # protocol
            msg = (
                "Unable to find data keys/filenames in RetinalLayersModel "
                "predictions dataframe; unable to continue"
            )
            _logger.critical(msg)
            raise ValueError(msg) from ke

        # Signal final step if retinal layers limits were exceeded
        if retinal_limits_exceeded_info:
            self._signal_final_step_for_limits_exceeded(protocol_state)

        # Send retinal layers results to modeller
        await self.mailbox.send_evaluation_results(
            eval_results={},
            resources_consumed=self.apply_actual_usage_to_resources_consumed(
                retinal_layers_algo,
                retinal_limits_exceeded_info,
            ),
        )
        filenames = list(
            set(fovea_filenames).intersection(set(retinal_layers_filenames))
        )

        # Combine all model predictions
        prediction_dfs = [
            fovea_predictions_df,
            pathology_predictions_df,
            retinal_layers_predictions_df,
        ]
        non_empty_dfs = [df for df in prediction_dfs if not df.empty]

        if non_empty_dfs:
            # Start with the first non-empty dataframe
            all_predictions_df = non_empty_dfs[0]
            # Merge remaining dataframes
            for i, df in enumerate(non_empty_dfs[1:], 1):
                merge_cols = ["BitfountPatientID", ORIGINAL_FILENAME_METADATA_COLUMN]
                common_cols = [
                    col
                    for col in merge_cols
                    if col in all_predictions_df.columns and col in df.columns
                ]

                if common_cols:
                    all_predictions_df = all_predictions_df.merge(
                        df,
                        on=common_cols,
                        how="outer",
                        suffixes=("", f"_model_{i}"),
                    )
                else:
                    # If no common columns, concatenate
                    all_predictions_df = pd.concat([all_predictions_df, df], axis=1)

        # Run Fluid Volume Calculation Algorithms
        _logger.info("Running intraretinal cystoid fluid volume calculation algorithm")
        irf_fluid_volume_results: Mapping[str, Optional[FluidVolumeMetrics]] = (
            irf_fluid_volume_calc_algo.run(
                predictions=pathology_predictions_df,
                filenames=pathology_filenames,
            )
        )
        _logger.info(
            f"Intraretinal cystoid fluid volume calculation completed: "
            f"{len(irf_fluid_volume_results) if irf_fluid_volume_results else 0} "
            f"results generated"
        )

        # Process IRF fluid volume results
        irf_data = []
        for filename, metrics in irf_fluid_volume_results.items():
            irf_row_data: dict[str, Any] = {ORIGINAL_FILENAME_METADATA_COLUMN: filename}
            # metrics will always be a FluidVolumeMetrics object (with zeros
            # if no fluid) or None only on error (which we still need to handle)
            if metrics is not None:
                # Add IRF results with prefix
                for key, value in metrics.to_record().items():
                    irf_row_data[f"irf_{key}"] = value
            else:
                # Only happens on processing errors - add NA values
                for key in FluidVolumeMetrics.expected_cols():
                    irf_row_data[f"irf_{key}"] = pd.NA
            irf_data.append(irf_row_data)

        if irf_data:
            irf_df = pd.DataFrame(irf_data)
            # Merge IRF results with existing model predictions
            if not all_predictions_df.empty:
                all_predictions_df = all_predictions_df.merge(
                    irf_df,
                    on=ORIGINAL_FILENAME_METADATA_COLUMN,
                    how="outer",
                    suffixes=("", "_irf"),
                )
            else:
                all_predictions_df = irf_df

        # Send empty results to modeller after IRF fluid volume calculation
        await self.mailbox.send_evaluation_results({})

        _logger.info("Running subretinal fluid volume calculation algorithm")
        srf_fluid_volume_results: Mapping[str, Optional[FluidVolumeMetrics]] = (
            srf_fluid_volume_calc_algo.run(
                predictions=pathology_predictions_df,
                filenames=pathology_filenames,
            )
        )
        _logger.info(
            f"Subretinal fluid volume calculation completed: "
            f"{len(srf_fluid_volume_results) if srf_fluid_volume_results else 0} "
            f"results generated"
        )

        # Process SRF fluid volume results
        srf_data = []
        for filename, metrics in srf_fluid_volume_results.items():
            srf_row_data: dict[str, Any] = {ORIGINAL_FILENAME_METADATA_COLUMN: filename}
            # metrics will always be a FluidVolumeMetrics object (with zeros
            # if no fluid) or None only on error (which we still need to handle)
            if metrics is not None:
                # Add SRF results with prefix
                for key, value in metrics.to_record().items():
                    srf_row_data[f"srf_{key}"] = value
            else:
                # Only happens on processing errors - add NA values
                for key in FluidVolumeMetrics.expected_cols():
                    srf_row_data[f"srf_{key}"] = pd.NA
            srf_data.append(srf_row_data)

        if srf_data:
            srf_df = pd.DataFrame(srf_data)
            # Merge SRF results with existing model predictions
            if not all_predictions_df.empty:
                all_predictions_df = all_predictions_df.merge(
                    srf_df,
                    on=ORIGINAL_FILENAME_METADATA_COLUMN,
                    how="outer",
                    suffixes=("", "_srf"),
                )
            else:
                all_predictions_df = srf_df

        # Send empty results to modeller after SRF fluid volume calculation
        await self.mailbox.send_evaluation_results({})

        # Run CST Calculation Algorithm
        _logger.info("Running CST calculation algorithm")
        cst_metrics: Mapping[str, Optional[CSTMetrics]] = cst_calc_algo.run(
            layer_predictions=retinal_layers_predictions_df,
            fovea_predictions=fovea_predictions_df,
            filenames=filenames,
        )
        _logger.info(
            f"CST calculation completed: metrics for {len(cst_metrics)} files calculated."  # noqa: E501
        )
        # convert to df
        cst_metrics_df = cst_calc_algo.convert_cst_metrics_to_df(cst_metrics)

        # Merge fluid volume results (IRF and SRF) into cst_metrics_df
        # Extract only fluid volume columns from all_predictions_df
        fluid_volume_cols = [ORIGINAL_FILENAME_METADATA_COLUMN]
        for col in all_predictions_df.columns:
            if col.startswith("irf_") or col.startswith("srf_"):
                fluid_volume_cols.append(col)

        if len(fluid_volume_cols) > 1 and not all_predictions_df.empty:
            fluid_volume_df = all_predictions_df[fluid_volume_cols].copy()
            # Merge fluid volume results with CST metrics
            if not cst_metrics_df.empty:
                all_metrics_df = cst_metrics_df.merge(
                    fluid_volume_df,
                    on=ORIGINAL_FILENAME_METADATA_COLUMN,
                    how="outer",
                    suffixes=("", "_fluid"),
                )
            else:
                all_metrics_df = fluid_volume_df
        else:
            all_metrics_df = cst_metrics_df

        # Send empty results to modeller after CST calculation

        await self.mailbox.send_evaluation_results({})

        _logger.info("Running Longitudinal Algorithm")
        per_patient_eye_df = longitudinal_algo.run(
            all_metrics_df,
            metric_columns=SAPPHIRE_LONGITUDINAL_COLUMNS,
            detail_cols_to_add=[
                NAME_COL,
                DOB_COL,
                "Patient's Sex",
            ],
        )

        await self.mailbox.send_evaluation_results({})

        _logger.info("Running Trial Inclusion Algorithm")
        if per_patient_eye_df is None:
            results = None
        else:
            results = trial_incl_algo.run_and_return_dataframe(
                dataframe=per_patient_eye_df, ehr_dataframe=data_with_ehr
            )

        await self.mailbox.send_evaluation_results({})

        # Run CSV Report Generation Algorithm
        _logger.info("Running Eligibility CSV report generation algorithm")
        if results is not None:
            simple_csv_algo.rename_columns = {
                "srf_total_fluid_volume_longitudinal": "SRF Fluid Volume over time",
                "irf_total_fluid_volume_longitudinal": "IRF Fluid Volume over time",
                "cst_mean_um_longitudinal": "CST over time",
                _BITFOUNT_PATIENT_ID_KEY: _BITFOUNT_PATIENT_ID_RENAMED,
            }
            output_filename = (
                f"{self.trial_name}-eligible-patients-{csv_report_algo.task_start_date}.csv"
                if self.trial_name
                else "eligibility_results.csv"
            )
            simple_csv_algo.run(
                df=self._format_eligibility_results(results),
                task_id=self._task_id,
                output_filename=output_filename,
            )
        _logger.info("Eligibility CSV report generation algorithm completed. ")

        # Send empty results to modeller after CSV report generation
        await self.mailbox.send_evaluation_results({})

        # Run CSV Report Generation Algorithm for per-scan results
        _logger.info("Running per-scan CSV report generation algorithm")
        csv_report_algo.trial_name = self.trial_name
        csv_report_algo.filename_mid_segment = "per-scan-details"
        csv_report_algo.rename_columns = self.define_csv_output_rename_columns()

        csv_report_algo.original_cols = (
            [
                "Study name",
                "BitfountPatientID",
                "Patient's Name",
                "Patient's Birth Date",
                "Patient's Sex",
                "Scan Laterality",
                "Acquisition DateTime",
                "Number of Frames",
            ]
            + SAPPHIRE_METRICS_COLS
            + ["Modality", "_original_filename"]
        )
        # need to set aux_cols to empty list to avoid all columns being output
        csv_report_algo.aux_cols = []

        csv_report_algo.run(
            results_df=all_metrics_df,
            task_id=self._task_id,
            filenames=filenames,
        )
        _logger.info("Per-scan CSV report generation algorithm completed. ")

        # Send empty results to modeller after CSV report generation
        await self.mailbox.send_evaluation_results({})
        return all_metrics_df

    def _format_eligibility_results(self, eligibility_df: pd.DataFrame) -> pd.DataFrame:
        """Formats eligibility dataframe to a reader friendly version for CSV output.

        1. Removes unwanted columns.
        2. Formats dates in longitudinal columns.
        3. Drop ineligible patients.
        """
        eligibility_df = eligibility_df.drop(
            [
                "Age (yrs) >= 49",
                "Age (yrs) <= 90",
                "Aflibercept Response Criteria",
                FILTER_FAILED_REASON_COLUMN,
            ],
            errors="ignore",
            axis=1,
        )

        longitudinal_cols = [
            col for col in eligibility_df.columns if col.endswith("_longitudinal")
        ]
        units_map = {
            "srf_total_fluid_volume_longitudinal": "nL",
            "irf_total_fluid_volume_longitudinal": "nL",
            "cst_mean_um_longitudinal": "µm",
        }
        for long_col in longitudinal_cols:
            units = units_map.get(long_col, "")
            eligibility_df[long_col] = eligibility_df[long_col].apply(
                lambda lst, u=units: self._format_longitudinal_output(lst, units=u)
            )

        eligibility_df = eligibility_df[eligibility_df[FILTER_MATCHING_COLUMN]]
        eligibility_df["Study name"] = self.trial_name or ""
        existing_cols_in_order = [
            col for col in ELIGIBILITY_COLUMN_ORDER if col in eligibility_df
        ]
        eligibility_df = eligibility_df[existing_cols_in_order]

        return eligibility_df

    def _format_longitudinal_output(
        self, metric_list: list[tuple[Optional[float], datetime]], units: str = ""
    ) -> str:
        """Format longitudinal column output to a printable version."""
        lines = []
        for value, scan_date in metric_list:
            val_str = (
                "N/A"
                if (value is None or pd.isna(value))
                else f"{round(float(value), 2)}{(' ' + units) if units else ''}"
            )
            lines.append(f"{val_str} | Date={scan_date.strftime('%Y-%m-%d')}")
        return "\n".join(lines)

    def results_columns_save_to_db_cache(self) -> list[str]:
        """Columns of results to save to project database.

        These results will be saved alongside columns from the datasource
        get_project_db_sqlite_columns method. These cached results will get
        picked up in future runs by the Longitudinal Algorithm.
        """
        return SAPPHIRE_LONGITUDINAL_COLUMNS


class WetAMDScreeningProtocolSapphire(BaseProtocolFactory):
    """Protocol for Wet-AMD model inference algorithms for Sapphire trial."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "results_notification_email": fields.Boolean(allow_none=True),
        "rename_columns": fields.Dict(
            keys=fields.Str(), values=fields.Str(), allow_none=True
        ),
        "trial_name": fields.Str(allow_none=True),
        "batch_grouping": fields.Nested(
            desert.schema_class(GroupingConfig), allow_none=True
        ),
        "ehr_enabled": fields.Boolean(allow_none=True),
    }

    def __init__(
        self,
        *,
        algorithm: Sequence[
            Union[
                EHRPatientQueryAlgorithm,
                ModelInference,
                FluidVolumeCalculationAlgorithm,
                CSTCalculationAlgorithm,
                LongitudinalAlgorithm,
                TrialInclusionCriteriaMatchAlgorithmSapphire,
                CSVReportGeneratorOphthalmologyAlgorithm,
                _SimpleCSVAlgorithm,
            ]
        ],
        results_notification_email: Optional[bool] = False,
        trial_name: Optional[str] = None,
        rename_columns: Optional[Mapping[str, str]] = None,
        batch_grouping: Optional[Mapping[str, Any]] = None,
        ehr_enabled: Optional[bool] = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(algorithm=algorithm, **kwargs)
        self.results_notification_email = (
            results_notification_email
            if results_notification_email is not None
            else False
        )
        self.rename_columns = rename_columns
        self.trial_name = trial_name
        self.batch_grouping = batch_grouping
        self.ehr_enabled = ehr_enabled if ehr_enabled is not None else False

    @classmethod
    def _validate_algorithm(cls, algorithm: BaseCompatibleAlgoFactory) -> None:
        """Validates by ensuring algorithms are of expected types."""
        if algorithm.class_name not in (
            "bitfount.ModelInference",
            "bitfount.FluidVolumeCalculationAlgorithm",
            "bitfount.CSVReportGeneratorOphthalmologyAlgorithm",
            "bitfount.CSTCalculationAlgorithm",
            "bitfount.LongitudinalAlgorithm",
            "bitfount.TrialInclusionCriteriaMatchAlgorithmSapphire",
            "bitfount._SimpleCSVAlgorithm",
            "bitfount.EHRPatientQueryAlgorithm",
        ):
            raise TypeError(
                f"The {cls.__name__} protocol does not support "
                + f"the {type(algorithm).__name__} algorithm.",
            )

    def modeller(
        self,
        *,
        mailbox: _ModellerMailbox,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _ModellerSide:
        """Create the modeller side of the protocol."""
        algorithms = cast(
            Sequence[
                Union[
                    EHRPatientQueryAlgorithm,
                    ModelInference,
                    FluidVolumeCalculationAlgorithm,
                    CSTCalculationAlgorithm,
                    LongitudinalAlgorithm,
                    TrialInclusionCriteriaMatchAlgorithmSapphire,
                    CSVReportGeneratorOphthalmologyAlgorithm,
                    _SimpleCSVAlgorithm,
                ]
            ],
            self.algorithms,
        )
        modeller_algos = []
        for algo in algorithms:
            if hasattr(algo, "pretrained_file"):
                modeller_algos.append(
                    algo.modeller(pretrained_file=algo.pretrained_file, context=context)
                )
            else:
                modeller_algos.append(algo.modeller(context=context))
        return _ModellerSide(
            algorithm=modeller_algos,
            mailbox=mailbox,
            ehr_enabled=self.ehr_enabled,
            **kwargs,
        )

    def worker(
        self,
        *,
        mailbox: _WorkerMailbox,
        hub: BitfountHub,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Create the worker side of the protocol."""
        algorithms = cast(
            Sequence[
                Union[
                    EHRPatientQueryAlgorithm,
                    ModelInference,
                    FluidVolumeCalculationAlgorithm,
                    CSTCalculationAlgorithm,
                    LongitudinalAlgorithm,
                    TrialInclusionCriteriaMatchAlgorithmSapphire,
                    CSVReportGeneratorOphthalmologyAlgorithm,
                    _SimpleCSVAlgorithm,
                ]
            ],
            self.algorithms,
        )
        return _WorkerSide(
            algorithm=[algo.worker(hub=hub, context=context) for algo in algorithms],
            mailbox=mailbox,
            results_notification_email=self.results_notification_email,
            trial_name=self.trial_name,
            rename_columns=self.rename_columns,
            batch_grouping=self.batch_grouping,
            ehr_enabled=self.ehr_enabled,
            **kwargs,
        )
