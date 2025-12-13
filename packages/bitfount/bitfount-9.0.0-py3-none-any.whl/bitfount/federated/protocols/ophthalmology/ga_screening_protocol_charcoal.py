"""GA custom multi-algorithm protocol.

First runs a model inference on the GA model, then
the GA algorithm to compute the area affected by GA.
Then CSV and PDF Reports get generated.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date
from pathlib import Path
import time
from typing import TYPE_CHECKING, Any, ClassVar, Optional, cast

from marshmallow import fields
import pandas as pd
import torch

from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.federated.algorithms.base import NoResultsModellerAlgorithm
from bitfount.federated.algorithms.ehr.ehr_patient_query_algorithm import (
    EHR_QUERY_COLUMNS,
    EHRPatientQueryAlgorithm,
    _WorkerSide as _EHRQueryWorkerSide,
)
from bitfount.federated.algorithms.filtering_algorithm import (
    RecordFilterAlgorithm,
    _ModellerSide as _RecordFilterModellerSide,
    _WorkerSide as _RecordFilterWorkerSide,
)
from bitfount.federated.algorithms.model_algorithms.inference import (
    ModelInference,
    _ModellerSide as _InferenceModellerSide,
    _WorkerSide as _InferenceWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.dataframe_generation_extensions import (  # noqa: E501
    generate_subfoveal_indicator,
)
from bitfount.federated.algorithms.ophthalmology.ga_trial_calculation_algorithm_base import (  # noqa: E501
    _BaseWorkerSideWithFovea as _GACalcWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.ga_trial_calculation_algorithm_charcoal import (  # noqa: E501
    GATrialCalculationAlgorithmCharcoal,
)
from bitfount.federated.algorithms.ophthalmology.ga_trial_inclusion_criteria_match_algorithm_charcoal import (  # noqa: E501
    TrialInclusionCriteriaMatchAlgorithmCharcoal,
    _WorkerSide as _TrialInclWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    AGE_COL,
    DISTANCE_FROM_FOVEA_CENTRE_COL,
    FILTER_FAILED_REASON_COLUMN,
    FILTER_MATCHING_COLUMN,
    LARGEST_LEGION_SIZE_COL_PREFIX,
    MAX_CNV_PROBABILITY_COL_PREFIX,
    SMALLEST_LEGION_SIZE_COL,
    SUBFOVEAL_COL,
    TOTAL_GA_AREA_COL_PREFIX,
    GAMetricsWithFovea,
    max_pathology_prob_col_name,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_utils import (
    _convert_ga_metrics_to_df,
    _convert_predict_return_type_to_dataframe,
    use_default_rename_columns,
)
from bitfount.federated.algorithms.ophthalmology.reduce_csv_algorithm_charcoal import (
    ReduceCSVAlgorithmCharcoal,
    _WorkerSide as _ReduceCSVWorkerSide,
)
from bitfount.federated.algorithms.ophthalmology.simple_csv_algorithm import (
    _SimpleCSVAlgorithm,
    _WorkerSide as _CSVWorkerSide,
)
from bitfount.federated.algorithms.s3_upload_algorithm import (
    S3UploadAlgorithm,
    _ModellerSide as _S3UploadModellerSide,
    _WorkerSide as _S3UploadWorkerSide,
)
from bitfount.federated.exceptions import ProtocolError
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseModellerProtocol,
    BaseProtocolFactory,
    BaseWorkerProtocol,
    FinalStepReduceProtocol,
    InitialSetupModellerProtocol,
    InitialSetupWorkerProtocol,
    ModelInferenceProtocolMixin,
    ProtocolState,
)
from bitfount.federated.transport.message_service import TaskNotification
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.opentelemetry import get_task_meter
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import ProtocolContext
from bitfount.types import T_FIELDS_DICT
from bitfount.utils.aws_utils import (
    AWSError,
    check_aws_credentials_are_valid,
    get_boto_session,
)

if TYPE_CHECKING:
    from bitfount.federated.pod_vitals import _PodVitals
    from bitfount.hub.api import BitfountHub

_logger = _get_federated_logger(__name__)

# TODO: [NO_TICKET: Imported from ophthalmology] Change these?
_CRITERIA_MATCH_YES_KEY = "Yes"
_CRITERIA_MATCH_NO_KEY = "No"

DRUSEN_COLS = ["hard_drusen", "soft_drusen", "confluent_drusen"]
EXCLUSION_COLS = [
    "diffuse_edema",
    "epiretinal_fibrosis",
    "hard_exudates",
    "intraretinal_cystoid_fluid",
    "serous_rpe_detachment",
    "subretinal_fluid",
    "subretinal_hyperreflective_material__shrm_",
    "choroidal_neovascularization",
    "diabetic_macular_edema",
    "wet_amd",
]
CHARCOAL_INTERMEDIATE_CSV_COLUMNS = EHR_QUERY_COLUMNS + [
    # Patient details
    AGE_COL,
    # Model metrics
    TOTAL_GA_AREA_COL_PREFIX,
    LARGEST_LEGION_SIZE_COL_PREFIX,
    SMALLEST_LEGION_SIZE_COL,
    SUBFOVEAL_COL,
    DISTANCE_FROM_FOVEA_CENTRE_COL,
    MAX_CNV_PROBABILITY_COL_PREFIX,
    *[max_pathology_prob_col_name(col) for col in DRUSEN_COLS],
    "max_drusen_probability",  # Combined drusen probabilities
    *[max_pathology_prob_col_name(col) for col in EXCLUSION_COLS],
    # Eligibility
    FILTER_MATCHING_COLUMN,
    FILTER_FAILED_REASON_COLUMN,
]

_S3_PRESCREENING_SUBDIRECTORY = "prescreening"
_CSV_ALGO_OUTPUT_FILENAME = "results.csv"


class _ModellerSide(
    BaseModellerProtocol,
    InitialSetupModellerProtocol[_RecordFilterModellerSide],
):
    """Modeller side of the Charcoal pre-screening protocol.

    Args:
        algorithm: The sequence of GA modeller algorithms to be used.
        mailbox: The mailbox to use for communication with the Workers.
        **kwargs: Additional keyword arguments.
    """

    algorithm: Sequence[
        _InferenceModellerSide
        | _S3UploadModellerSide
        | NoResultsModellerAlgorithm
        | _RecordFilterModellerSide
    ]

    def __init__(
        self,
        *,
        algorithm: Sequence[
            _InferenceModellerSide
            | _S3UploadModellerSide
            | NoResultsModellerAlgorithm
            | _RecordFilterModellerSide
        ],
        mailbox: _ModellerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    def initialise(
        self,
        task_id: str,
        **kwargs: Any,
    ) -> None:
        """Initialises the component algorithms."""
        # Modeller is not performing any inference, training, etc., of models,
        # so use CPU rather than taking up GPU resources.
        for algo in self.algorithms:
            updated_kwargs = kwargs.copy()
            if hasattr(algo, "model"):
                updated_kwargs.update(map_location=torch.device("cpu"))
            algo.initialise(
                task_id=task_id,
                **updated_kwargs,
            )

        # Register a handler from the S3 upload algorithm to handle S3 URL generation
        # requests from the Worker
        # Note: The modeller side doesn't have direct access to data owner username
        # and dataset name, so we use a generic subdirectory that the worker will
        # complete with the actual values.
        s3_upload_algo: _S3UploadModellerSide = cast(
            _S3UploadModellerSide, self.algorithm[-1]
        )
        _logger.info(
            f"Registering handler from {s3_upload_algo.class_name}"
            f" for generating S3 upload URLs"
        )
        s3_upload_algo.register_s3_upload_url_request_handler(
            mailbox=self.mailbox,
            subdirectory_for_upload=_S3_PRESCREENING_SUBDIRECTORY,
        )

        # Perform fail-fast checks that we can actually get an S3 upload location
        # and that AWS credentials are valid. We perform these checks here in
        # initialise() to fail early before the protocol starts running, avoiding
        # a state where the modeller-side errors out but the worker-side isn't
        # aware until it would be waiting on a message from the modeller.
        _logger.info("Acquiring test S3 upload URL")
        try:
            self.get_test_S3_url()
        except Exception as e:
            _logger.error(f"Error acquiring test S3 upload URL: {e}")
            raise
        _logger.info("Test S3 upload URL successfully acquired")

        # The above check only checks that the necessary details for generating an S3
        # URL are available, we additionally need to check that the credentials are
        # actually valid.
        _logger.info("Testing S3 credentials")
        try:
            self.check_AWS_credentials_valid()
        except Exception as e:
            _logger.error(f"Error testing S3 credentials: {e}")
            raise
        _logger.info("S3 credentials successfully tested")

    async def run(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> list[Any] | Any:
        """Runs Modeller side of the protocol.

        This just sends the model parameters to the workers sequentially and then tells
        the workers when the protocol is finished.

        Args:
            context: Optional. Run-time context for the protocol.
            **kwargs: Additional keyword arguments.
        """
        results = []

        # Unpack the algorithms
        # mypy: Some nasty type-casting needed here as mypy doesn't know that it's
        #       the _last_ element that's _S3UploadModellerSide
        result_run_algos: Sequence[
            _InferenceModellerSide
            | NoResultsModellerAlgorithm
            | _RecordFilterModellerSide
        ] = cast(
            Sequence[
                _InferenceModellerSide
                | NoResultsModellerAlgorithm
                | _RecordFilterModellerSide
            ],
            self.algorithm[:-1],
        )

        # Run the algorithms that rely on the evaluation results in sequence
        for algo in result_run_algos:
            _logger.info(f"Running algorithm {algo.class_name}")
            result = await self.mailbox.get_evaluation_results_from_workers()
            results.append(result)
            _logger.info("Received results from Pods.")
            _logger.info(f"Algorithm {algo.class_name} completed.")

        # Run the modeller-side algorithms that rely on the evaluation results in
        # sequence
        final_results = [
            algo.run(result_) for algo, result_ in zip(result_run_algos, results)
        ]

        return final_results

    def get_test_S3_url(self) -> None:
        """Get a test S3 upload URL from the upload algorithm, to ensure that we can."""
        s3_upload_algo: _S3UploadModellerSide = cast(
            _S3UploadModellerSide, self.algorithm[-1]
        )

        test_s3_post_url, test_s3_post_fields = s3_upload_algo.run(
            subdirectory_for_upload="test"
        )

        no_test_s3_url: bool = test_s3_post_url is None
        no_test_s3_fields: bool = test_s3_post_fields is None
        if no_test_s3_url or no_test_s3_fields:
            err_msg = ""
            if no_test_s3_url:
                err_msg += "Could not acquire a test S3 upload URL"
                if no_test_s3_fields:
                    err_msg += " or test S3 upload fields"
            else:
                err_msg += (
                    "Test S3 upload URL acquired,"
                    " but test S3 upload fields not acquired"
                )
            raise ProtocolError(err_msg)

    def check_AWS_credentials_valid(self) -> None:
        """Test that the AWS credentials are valid."""
        s3_upload_algo: _S3UploadModellerSide = cast(
            _S3UploadModellerSide, self.algorithm[-1]
        )

        try:
            session = get_boto_session(s3_upload_algo.aws_profile)
            check_aws_credentials_are_valid(session)
        except AWSError as e:
            raise ProtocolError(f"AWS credentials are not valid. Error: {e}") from e


class _WorkerSide(
    BaseWorkerProtocol,
    InitialSetupWorkerProtocol[_RecordFilterWorkerSide],
    FinalStepReduceProtocol,
    ModelInferenceProtocolMixin,
):
    """Worker side of the GA protocol.

    Args:
        algorithm: The sequence of GA inference and additional algorithms to be used.
        mailbox: The mailbox to use for communication with the Modeller.
        **kwargs: Additional keyword arguments.
    """

    algorithm: Sequence[
        _RecordFilterWorkerSide
        | _EHRQueryWorkerSide
        | _InferenceWorkerSide
        | _GACalcWorkerSide
        | _TrialInclWorkerSide
        | _CSVWorkerSide
        | _ReduceCSVWorkerSide
        | _S3UploadWorkerSide
    ]

    def __init__(
        self,
        *,
        algorithm: Sequence[
            _RecordFilterWorkerSide
            | _EHRQueryWorkerSide
            | _InferenceWorkerSide
            | _GACalcWorkerSide
            | _TrialInclWorkerSide
            | _CSVWorkerSide
            | _ReduceCSVWorkerSide
            | _S3UploadWorkerSide
        ],
        mailbox: _WorkerMailbox,
        results_notification_email: bool = False,
        rename_columns: Optional[Mapping[str, str]] = None,
        trial_name: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)
        self.results_notification_email = results_notification_email
        self.rename_columns = rename_columns
        self.trial_name = trial_name
        self._task_meter = get_task_meter()
        self._task_id: str = mailbox._task_id
        self.new_data_available: bool = False

        # Store today's date at instantiation time (as tasks may run over several
        # days) as a prefix string
        self._today_date_str = date.today().strftime("%Y-%m-%d")

    async def run(
        self,
        *,
        pod_vitals: Optional[_PodVitals] = None,
        context: ProtocolContext,
        batch_num: Optional[int] = None,
        final_batch: bool = False,
        protocol_state: Optional[ProtocolState] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Runs GA algorithm on worker side followed by metrics and csv algorithms.

        Args:
            pod_vitals: Optional. Pod vitals instance for recording run-time details
                from the protocol run.
            context: Optional. Run-time context for the protocol.
            batch_num: The number of the batch being run.
            final_batch: If this run of the protocol represents the final run within
                a task.
            protocol_state: The state of the protocol, used to signal final step.
            **kwargs: Additional keyword arguments.
        """
        # Use datasource-default column renamings if none provided
        self.rename_columns = use_default_rename_columns(
            self.datasource, self.rename_columns
        )

        # Unpack the algorithms
        (
            record_filter_algo,
            ehr_query_algo,
            fovea_algo,
            ga_algo,
            ga_calc_algo,
            criteria_match_algo,
            csv_report_algo,
            _reduce_csv_algo,
            s3_upload_algo,
        ) = self._extract_algorithms()

        if pod_vitals:
            pod_vitals.last_task_execution_time = time.time()

        # Run record filter algo (noop)
        record_filter_algo.run()
        # Send empty results to modeller to move to next algorithm
        await self.mailbox.send_evaluation_results({})

        # Retrieve the data for this run
        # This should only read the current batch into memory (roughly 16 rows)
        dfs: list[pd.DataFrame] = list(self.datasource.yield_data(use_cache=True))
        file_data: pd.DataFrame
        if any(not df.empty for df in dfs):
            file_data = pd.concat(dfs, axis="index")
            # Run EHR Query Algorithm
            _logger.info("Running EHR Patient Query Algorithm")
            data_with_ehr: pd.DataFrame
            query_results = ehr_query_algo.run(
                file_data,
                get_appointments=True,
                get_conditions_and_procedures=True,
                get_practitioner=True,
                get_visual_acuity=False,
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
        else:
            _logger.warning(
                "No file data was extracted. No queries to EHR will be made."
            )
            data_with_ehr = pd.DataFrame()

        # Send empty results to modeller to move to next algorithm
        await self.mailbox.send_evaluation_results({})

        # Run Fovea Algorithm
        # fovea_predictions should be a dataframe
        _logger.info("Running fovea inference algorithm")
        fovea_predictions = fovea_algo.run(return_data_keys=True)
        # Output will either be a dataframe (if ga_algo.class_outputs is set),
        # or a PredictReturnType, which we will need to convert into a dataframe.
        fovea_predictions_df = _convert_predict_return_type_to_dataframe(
            fovea_predictions
        )

        _logger.info(
            f"Fovea inference algorithm completed:"
            f" {len(fovea_predictions_df)} predictions made."
        )

        # If limits were exceeded, reduce the predictions dataframe and proceed as
        # though this were the last batch
        fovea_predictions_df, fovea_limits_exceeded_info, final_batch = (
            self.apply_usage_limits(
                context, fovea_predictions_df, fovea_algo, final_batch
            )
        )

        # Sends empty results to modeller just to inform it to move on to the
        # next algorithm
        await self.mailbox.send_evaluation_results(
            eval_results={},
            resources_consumed=self.apply_actual_usage_to_resources_consumed(
                fovea_algo,
                fovea_limits_exceeded_info,
            ),
        )

        # Run GA Algorithm
        _logger.info("Running GA inference algorithm")
        ga_predictions = ga_algo.run(return_data_keys=True)

        # Output will either be a dataframe (if ga_algo.class_outputs is set),
        # or a PredictReturnType, which we will need to convert into a dataframe.
        ga_predictions_df = _convert_predict_return_type_to_dataframe(ga_predictions)

        _logger.info(
            f"GA inference algorithm completed:"
            f" {len(ga_predictions_df)} predictions made."
        )

        ga_predictions_df, ga_limits_exceeded_info, final_batch = (
            self.apply_usage_limits(context, ga_predictions_df, ga_algo, final_batch)
        )

        # Try to get data keys from the predictions, if present
        try:
            if ga_predictions_df.empty:
                filenames: list[str] = []
            else:
                filenames = ga_predictions_df[
                    ORIGINAL_FILENAME_METADATA_COLUMN
                ].tolist()
        except KeyError as ke:
            # `filenames` is needed below, fail out if we cannot find them for this
            # protocol
            _logger.critical(
                "Unable to find data keys/filenames in GA predictions dataframe;"
                " unable to continue"
            )
            raise ValueError(
                "Unable to find data keys/filenames in GA predictions dataframe;"
                " unable to continue"
            ) from ke

        # Upload metrics to task meter
        _logger.info("Uploading metrics to task meter")
        self._task_meter.submit_algorithm_records_returned(
            records_count=len(ga_predictions_df),
            task_id=str(self._task_id),
            algorithm=ga_algo,
            protocol_batch_num=batch_num,
            project_id=self.project_id,
        )
        _logger.info("Metrics uploaded to task meter")

        # Sends empty results to modeller just to inform it to move on to the
        # next algorithm
        await self.mailbox.send_evaluation_results(
            eval_results={},
            resources_consumed=self.apply_actual_usage_to_resources_consumed(
                ga_algo,
                ga_limits_exceeded_info,
            ),
        )

        # Trial Calculations (GA Metrics) from the predictions
        _logger.info("Running GA calculation algorithm")
        # This dict maps filenames -> metrics
        # Note: order will be correct as dict is sorted by insertion order,
        # and we only do clean/new insertions into this dict.
        ga_metrics: Mapping[str, Optional[GAMetricsWithFovea]] = ga_calc_algo.run(
            predictions=ga_predictions_df,
            fovea_predictions=fovea_predictions_df,
            filenames=filenames,
        )
        _logger.info(
            f"GA calculation algorithm completed:"
            f" metrics for {len(ga_metrics)} files calculated."
        )

        # Sends empty results to modeller just to inform it to move on to the
        # next algorithm
        await self.mailbox.send_evaluation_results({})

        # Combine GA Metrics with existing dataframe
        metrics_df = _convert_ga_metrics_to_df(
            ga_metrics, additional_pathology_prob_cols=DRUSEN_COLS + EXCLUSION_COLS
        )

        # Get the max probability columns for the drusen columns
        drusen_prob_cols = [
            max_pathology_prob_col_name(drusen_col) for drusen_col in DRUSEN_COLS
        ]
        # Combine drusen columns into max_drusen_probability column
        metrics_df["max_drusen_probability"] = metrics_df[drusen_prob_cols].max(axis=1)

        # Join the metrics_df with the test_data_df just based on filename
        if not ga_predictions_df.empty:
            # Merge EHR data with ga_predictions
            # DEV: We merge on ga_predictions_df rather than fovea_predictions_df as
            #      we only need one df to contain the EHR data and the
            #      ga_predictions_df is used in downstream algos whereas the
            #      fovea_predictions_df is not.
            ga_predictions_with_ehr_df = data_with_ehr.merge(
                ga_predictions_df, on=ORIGINAL_FILENAME_METADATA_COLUMN
            )
            test_data_df = ga_predictions_with_ehr_df.merge(
                metrics_df, on=ORIGINAL_FILENAME_METADATA_COLUMN
            )
        else:
            test_data_df = pd.DataFrame()

        # Trial Inclusion Algo - Criteria matching
        _logger.info("Applying clinical criteria")
        # Apply clinical criteria to output dataframe and notify task meter
        _logger.debug("Finding outputs that match the clinical criteria")

        matched_df = criteria_match_algo.run_and_return_dataframe(test_data_df)

        if matched_df.empty:
            criteria_yes_count, criteria_no_count = 0, 0
        else:
            criteria_yes_count = int(matched_df[FILTER_MATCHING_COLUMN].sum())
            criteria_no_count = int((~matched_df[FILTER_MATCHING_COLUMN]).sum())

        task_notification: Optional[TaskNotification] = None
        if criteria_yes_count > 0:
            plurarized_scans = "scan" if criteria_yes_count == 1 else "scans"
            task_notification = TaskNotification(
                message=f"{criteria_yes_count} eligible {plurarized_scans} found",
                email=self.results_notification_email,
            )

        # Upload metrics to task meter
        _logger.info("Uploading metrics to task meter")
        self._task_meter.submit_algorithm_records_per_class_returned(
            records_count_per_class={
                _CRITERIA_MATCH_YES_KEY: criteria_yes_count,
                _CRITERIA_MATCH_NO_KEY: criteria_no_count,
            },
            task_id=str(self._task_id),
            algorithm=criteria_match_algo,
            protocol_batch_num=batch_num,
            project_id=self.project_id,
        )
        _logger.info("Metrics uploaded to task meter")

        # Sends result count to modeller
        await self.mailbox.send_evaluation_results(
            {
                _CRITERIA_MATCH_YES_KEY: criteria_yes_count,
                _CRITERIA_MATCH_NO_KEY: criteria_no_count,
            },
            task_notification,
        )

        # Generate Intermediate CSV Reports
        _logger.info("Generating (Intermediate) CSV report")
        if not matched_df.empty:
            # Add subfoveal indicator column
            _logger.debug("Adding subfoveal indicator column to CSV")
            matched_df = generate_subfoveal_indicator(matched_df)

            csv_report_algo.run(
                df=matched_df,
                task_id=self._task_id,
                output_columns=CHARCOAL_INTERMEDIATE_CSV_COLUMNS,
                output_filename=_CSV_ALGO_OUTPUT_FILENAME,
            )

            try:
                await self._upload_partial_csv_reports_to_s3(
                    csv_report_algo, s3_upload_algo
                )
            except Exception as e:
                # We don't _mind_ if this fails, so just log an error and continue
                _logger.error(f"Error uploading partial CSV reports to S3: {e}")
        else:
            _logger.warning(
                "No new data was extracted. Nothing will be written to CSV."
            )
        _logger.info("Intermediate CSV report generation completed")

        # Sends empty results to modeller just to inform it to move on to the
        # next algorithm
        await self.mailbox.send_evaluation_results({})
        if not matched_df.empty:
            self.new_data_available = True
        else:
            self.new_data_available = False

        # Sends empty results to modeller just to inform it to move on to the
        # next algorithm
        await self.mailbox.send_evaluation_results({})

        _logger.info("Worker side of the protocol completed")

        # Check if limits were exceeded and if so
        # we abort any remaining protocol batches
        if ga_limits_exceeded_info:
            limits = context.inference_limits
            # limits_exceeded_info is not None if and only if limits is not None
            assert limits is not None  # nosec[assert_used]
            if protocol_state is not None:
                self._signal_final_step_for_limits_exceeded(protocol_state)
            await self.handle_limits_exceeded(
                ga_algo,
                ga_limits_exceeded_info,
                limits,
                self.mailbox,
            )

        else:
            return matched_df

    def _extract_algorithms(
        self,
    ) -> tuple[
        _RecordFilterWorkerSide,
        _EHRQueryWorkerSide,
        _InferenceWorkerSide,
        _InferenceWorkerSide,
        _GACalcWorkerSide,
        _TrialInclWorkerSide,
        _CSVWorkerSide,
        _ReduceCSVWorkerSide,
        _S3UploadWorkerSide,
    ]:
        """Utility method to unpack and type the algorithm instances."""
        (
            record_filter_algo,
            ehr_query_algo,
            fovea_algo,
            ga_algo,
            ga_calc_algo,
            criteria_match_algo,
            csv_report_algo,
            reduce_csv_algo,
            s3_upload_algo,
        ) = self.algorithm
        # Correct typing
        record_filter_algo = cast(_RecordFilterWorkerSide, record_filter_algo)
        ehr_query_algo = cast(_EHRQueryWorkerSide, ehr_query_algo)
        fovea_algo = cast(_InferenceWorkerSide, fovea_algo)
        ga_algo = cast(_InferenceWorkerSide, ga_algo)
        ga_calc_algo = cast(_GACalcWorkerSide, ga_calc_algo)
        criteria_match_algo = cast(_TrialInclWorkerSide, criteria_match_algo)
        csv_report_algo = cast(_CSVWorkerSide, csv_report_algo)
        reduce_csv_algo = cast(_ReduceCSVWorkerSide, reduce_csv_algo)
        s3_upload_algo = cast(_S3UploadWorkerSide, s3_upload_algo)
        return (
            record_filter_algo,
            ehr_query_algo,
            fovea_algo,
            ga_algo,
            ga_calc_algo,
            criteria_match_algo,
            csv_report_algo,
            reduce_csv_algo,
            s3_upload_algo,
        )

    async def _upload_partial_csv_reports_to_s3(
        self, csv_report_algo: _CSVWorkerSide, s3_upload_algo: _S3UploadWorkerSide
    ) -> None:
        """Upload the partial CSV report(s) to S3.

        Handles if there are multiple partial CSV reports (due to safe-writing file
        names for instance).
        """
        csv_output_files = csv_report_algo.output_files
        if not csv_output_files:
            _logger.warning("No partial CSV reports to upload to S3. Skipping upload.")
            return

        _logger.info("Retrieving S3 upload URL")
        (
            s3_upload_url,
            s3_upload_fields,
        ) = await s3_upload_algo.get_S3_presigned_upload_url(self.mailbox)

        _logger.info("Uploading partial results to S3")
        data_owner_username, dataset_name = (
            self._extract_dataset_owner_and_dataset_name()
        )

        # Create upload keys for each of the partial results files
        # Need to extract the actual file names (and any additional appended
        # elements) from the supplied paths
        # i.e. convert paths like "/path/to/results.csv" and "/path/to/results_1.csv"
        # to "scan_level_results.csv" and "scan_level_results_1.csv" respectively.
        element_to_replace: str = Path(_CSV_ALGO_OUTPUT_FILENAME).stem
        scan_level_csv_upload_file_names: dict[Path, str] = {
            file_path: (
                file_path.stem.replace(element_to_replace, "scan_level_results")
                + file_path.suffix
            )
            for file_path in csv_output_files
        }

        # Construct the S3 upload keys for each of the partial results files
        # Note: The keys need to be typed as str|Path (even though we know they are
        #       all paths here) due to the invariance of mapping-types on the keys.
        files_to_s3_keys: dict[str | Path, str] = {
            file_path: (
                f"{data_owner_username}"
                f"/{dataset_name}"
                f"/{self._today_date_str}_{self._task_id}"
                f"/{scan_level_csv_upload_file_names[file_path]}"
            )
            for file_path in csv_output_files
        }

        s3_upload_algo.run(
            # Upload the partial results CSV(s) to S3 in a
            # "prescreening"/<data_owner_username>/<dataset_name>/<date>_<task_id>/
            # subdirectory. "prescreening" is already supplied in the path by
            # the URL supplied by the Modeller.
            # Files will be named as "scan_level_results.csv",
            # "scan_level_results_1.csv", etc.
            files_to_upload=files_to_s3_keys,
            presigned_url=s3_upload_url,
            presigned_fields=s3_upload_fields,
        )
        _logger.info(
            "Partial results uploaded to S3: "
            + ", ".join(
                f'"{_S3_PRESCREENING_SUBDIRECTORY}/{s3_upload_key}"'
                for s3_upload_key in files_to_s3_keys.values()
            )
        )

    async def run_final_step(self, *, context: ProtocolContext, **kwargs: Any) -> None:
        """Runs the final reduce step for the protocol."""
        if self.new_data_available:
            # Unpack the algorithms
            (
                _record_filter_algo,
                _ehr_query_algo,
                _fovea_algo,
                _ga_algo,
                _ga_calc_algo,
                _criteria_match_algo,
                csv_report_algo,
                reduce_csv_algo,
                s3_upload_algo,
            ) = self._extract_algorithms()

            # Run the final reduce step CSV algo
            _logger.info("Running final reduce step for the protocol")
            reduce_csv_algo.run(
                task_id=self._task_id, csv_output_files=csv_report_algo.output_files
            )
            _logger.info("Final reduce step completed")

            # Upload the final results CSV to S3
            await self._final_results_s3_upload(reduce_csv_algo, s3_upload_algo)
        else:
            _logger.info(
                "No new data was available for the final reduce step; skipping."
            )

    async def _final_results_s3_upload(
        self, reduce_csv_algo: _ReduceCSVWorkerSide, s3_upload_algo: _S3UploadWorkerSide
    ) -> None:
        """Upload the final CSV report(s) to S3.

        Handles if there are multiple final CSV reports (due to safe-writing file
        names for instance).
        """
        # Fail fast if there are no final results files to upload
        final_results_files = reduce_csv_algo.output_files
        if not final_results_files:
            _logger.warning(
                "No final results files found to upload. Aborting S3Upload Algorithm"
            )
            return

        # Uploading final results CSV to S3
        _logger.info("Retrieving S3 upload URL")
        (
            s3_upload_url,
            s3_upload_fields,
        ) = await s3_upload_algo.get_S3_presigned_upload_url(self.mailbox)

        _logger.info("Uploading final results to S3")
        data_owner_username, dataset_name = (
            self._extract_dataset_owner_and_dataset_name()
        )

        # Create upload keys for each of the final results files
        # Need to extract the actual file names (and any additional appended
        # elements) from the final results file paths
        # i.e. convert paths like "/path/to/final_results.csv" and
        # "/path/to/final_results_1.csv" to "eligible_patients.csv" and
        # "eligible_patients_1.csv" respectively.
        element_to_replace: str = reduce_csv_algo.get_output_csv_results_path(
            task_id=self._task_id
        ).stem
        final_results_csv_upload_file_names: dict[Path, str] = {
            file_path: (
                file_path.stem.replace(element_to_replace, "eligible_patients")
                + file_path.suffix
            )
            for file_path in final_results_files
        }

        # Construct the S3 upload keys for each of the partial results files
        # Note: The keys need to be typed as str|Path (even though we know they are
        #       all paths here) due to the invariance of mapping-types on the keys.
        files_to_s3_keys: dict[str | Path, str] = {
            file_path: (
                f"{data_owner_username}"
                f"/{dataset_name}"
                f"/{self._today_date_str}_{self._task_id}"
                f"/{final_results_csv_upload_file_names[file_path]}"
            )
            for file_path in final_results_files
        }

        s3_upload_algo.run(
            # Upload the final results CSV to S3 in a
            # "prescreening"/<data_owner_username>/<dataset_name>/<date>_<task_id>/
            # subdirectory. "prescreening" is already supplied in the path by
            # the URL supplied by the Modeller.
            # Files will be named as "eligible_patients.csv",
            # "eligible_patients_1.csv", etc.
            files_to_upload=files_to_s3_keys,
            presigned_url=s3_upload_url,
            presigned_fields=s3_upload_fields,
        )
        _logger.info(
            "Final results uploaded to S3: "
            + ", ".join(
                f'"{_S3_PRESCREENING_SUBDIRECTORY}/{s3_upload_key}"'
                for s3_upload_key in files_to_s3_keys.values()
            )
        )


class GAScreeningProtocolCharcoal(BaseProtocolFactory):
    """Protocol for running GA Algorithms sequentially."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "results_notification_email": fields.Boolean(allow_none=True),
        "rename_columns": fields.Dict(
            keys=fields.Str(), values=fields.Str(), allow_none=True
        ),
        "trial_name": fields.Str(allow_none=True),
    }

    def __init__(
        self,
        *,
        algorithm: Sequence[
            RecordFilterAlgorithm
            | EHRPatientQueryAlgorithm
            | ModelInference
            | GATrialCalculationAlgorithmCharcoal
            | TrialInclusionCriteriaMatchAlgorithmCharcoal
            | _SimpleCSVAlgorithm
            | ReduceCSVAlgorithmCharcoal
            | S3UploadAlgorithm
        ],
        results_notification_email: Optional[bool] = False,
        trial_name: Optional[str] = None,
        rename_columns: Optional[Mapping[str, str]] = None,
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

    @classmethod
    def _validate_algorithm(cls, algorithm: BaseCompatibleAlgoFactory) -> None:
        """Validates the algorithms by ensuring they are either GA or Fovea."""
        if (
            algorithm.class_name
            not in (
                "bitfount.RecordFilterAlgorithm",
                "bitfount.EHRPatientQueryAlgorithm",
                "bitfount.ModelInference",
                "bitfount.GATrialCalculationAlgorithmCharcoal",
                "bitfount.TrialInclusionCriteriaMatchAlgorithmCharcoal",
                "bitfount._SimpleCSVAlgorithm",
                "bitfount.ReduceCSVAlgorithmCharcoal",
                "bitfount.S3UploadAlgorithm",
                "bitfount.CSVReportGeneratorAlgorithm",  # Kept for backwards compatibility # noqa: E501
            )
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
        """Returns the Modeller side of the protocol."""
        algorithms = cast(
            Sequence[
                RecordFilterAlgorithm
                | EHRPatientQueryAlgorithm
                | ModelInference
                | GATrialCalculationAlgorithmCharcoal
                | TrialInclusionCriteriaMatchAlgorithmCharcoal
                | _SimpleCSVAlgorithm
                | ReduceCSVAlgorithmCharcoal
                | S3UploadAlgorithm
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
        """Returns worker side of the GAScreeningProtocolCharcoal protocol.

        Args:
            mailbox: Worker mailbox instance to allow communication to the modeller.
            hub: `BitfountHub` object to use for communication with the hub.
            context: Optional. Run-time protocol context details for running.
            **kwargs: Additional keyword arguments.
        """
        algorithms = cast(
            Sequence[
                RecordFilterAlgorithm
                | EHRPatientQueryAlgorithm
                | ModelInference
                | GATrialCalculationAlgorithmCharcoal
                | TrialInclusionCriteriaMatchAlgorithmCharcoal
                | _SimpleCSVAlgorithm
                | ReduceCSVAlgorithmCharcoal
                | S3UploadAlgorithm
            ],
            self.algorithms,
        )
        return _WorkerSide(
            algorithm=[algo.worker(hub=hub, context=context) for algo in algorithms],
            mailbox=mailbox,
            results_notification_email=self.results_notification_email,
            trial_name=self.trial_name,
            rename_columns=self.rename_columns,
            **kwargs,
        )
