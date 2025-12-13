"""Algorithm for calculating the GA area."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Optional

import pandas as pd

from bitfount.data.datasources.base_source import (
    BaseSource,
)
from bitfount.data.datasources.dicom_source import (
    DICOM_ACQUISISTION_DATE_TIME_ATTRIBUTE,
)
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ophthalmology.dataframe_generation_extensions import (  # noqa: E501
    generate_bitfount_patient_id,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    _BITFOUNT_PATIENT_ID_KEY,
    DOB_COL,
    LATERALITY_COL,
    NAME_COL,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ProtocolContext
from bitfount.utils.pandas_utils import find_dob_column, find_full_name_column

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig
    from bitfount.types import T_FIELDS_DICT


logger = _get_federated_logger("bitfount.federated")


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algorithm."""

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

    def initialise(
        self,
        *,
        datasource: BaseSource,
        task_id: str,
        data_splitter: Optional[DatasetSplitter] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        self.initialise_data(datasource=datasource, data_splitter=data_splitter)

    def run(
        self,
        predictions: pd.DataFrame,
        metric_columns: list[str],
        grouping_keys: Optional[list[str]] = None,
        date_column: str = DICOM_ACQUISISTION_DATE_TIME_ATTRIBUTE,
        detail_cols_to_add: Optional[list[str]] = None,
    ) -> Optional[pd.DataFrame]:
        """Groups metrics by patient over a period of time.

        Args:
            predictions: The predictions from model inference with metric calculations.
            metric_columns: List of metric column names to summarise.
            grouping_keys: Columns names to group the df by. If None, will default to
                BF Patient ID + Eye Laterality. (Rows will be per-patient-per-eye)
            date_column: Column name for the scan date.
            detail_cols_to_add: Additional patient detail columns to include in the
                grouped output eg. Patient DOB/Sex

        Returns:
            Optional Dataframe with grouping_keys as index, and one column
            per longitudinal metric, containing list of tuples [(metric, date), ...].
            Returns None if predictions are empty or file data/predictions are None
            or missing expected columns.
        """
        if grouping_keys is None:
            grouping_keys = [_BITFOUNT_PATIENT_ID_KEY, LATERALITY_COL]

        # Fail fast if there are no predictions
        if predictions.empty:
            return None

        # Retrieve the data for this run

        # When using yield data in the algorithm context, only the files in
        # selected_filenames are used so we should only have a maximum of
        # len(selected_filenames) in memory.
        dfs: list[pd.DataFrame] = list(self.datasource.yield_data(use_cache=True))

        if all(df.empty for df in dfs):
            logger.warning("No data yielded in current batch.")
            return None

        file_data: pd.DataFrame = pd.concat(dfs, axis="index")
        file_data_with_patient_id = generate_bitfount_patient_id(
            file_data,
            name_col=(
                found_name_col
                if (found_name_col := find_full_name_column(file_data)) is not None
                else NAME_COL
            ),
            dob_col=(
                found_dob_col
                if (found_dob_col := find_dob_column(file_data)) is not None
                else DOB_COL
            ),
        )
        del file_data
        if found_name_col is not None:
            file_data_with_patient_id = file_data_with_patient_id.rename(
                {found_name_col: NAME_COL}, axis=1
            )
        if found_dob_col is not None:
            file_data_with_patient_id = file_data_with_patient_id.rename(
                {found_dob_col: DOB_COL}, axis=1
            )

        required_columns = grouping_keys + [
            ORIGINAL_FILENAME_METADATA_COLUMN,
        ]
        any_missing_cols = [
            col
            for col in required_columns
            if col not in file_data_with_patient_id.columns
        ]
        if any_missing_cols:
            logger.warning(
                f"Required columns {any_missing_cols} not found in datasource."
            )
            return None

        # Join with previous predicted values
        if self.cached_data is not None:
            # Expect all the required metrics to be present in cached_data
            # If not, skip the use of cached data
            missing_columns_in_cache = [
                col for col in metric_columns if col not in self.cached_data.columns
            ]
            if missing_columns_in_cache:
                logger.warning(
                    f"Required columns {missing_columns_in_cache} missing "
                    f"from cached data, skipping the use of cache."
                )
            else:
                predictions = pd.concat([predictions, self.cached_data])

        # Join predictions/calculations with file_data_with_patient_id
        # We use an inner join instead of left because we may have files for
        # which the cached predictions were not successfully retrieved.
        # In this case we want to drop those rows (files) instead of showing
        # a NaN value.
        merged_data_df = file_data_with_patient_id.merge(
            predictions,
            on=ORIGINAL_FILENAME_METADATA_COLUMN,
            how="inner",
        )

        # Sort by scan date
        sorted_merged_df = merged_data_df.sort_values(date_column)

        # Group by patient (grouping keys) and get metric values over time
        all_series = []
        for metric_column in metric_columns:
            all_series.append(
                self.get_metric_over_time(
                    sorted_merged_df=sorted_merged_df,
                    metric_column=metric_column,
                    date_column=date_column,
                    grouping_keys=grouping_keys,
                )
            )

        all_metrics = pd.concat(all_series, axis=1)

        # Additional details such as birthdate are required
        # for Trial Inclusion calculation
        if detail_cols_to_add is None:
            output_df = all_metrics
        else:
            avail_cols = [col for col in detail_cols_to_add if col in merged_data_df]
            patient_details = merged_data_df[
                grouping_keys + avail_cols
            ].drop_duplicates(grouping_keys)
            # Note: If there were discrepancies in name/DOB etc. for a given patient
            # in their dicoms, the one that shows up in the eligibility results
            # would be chosen at random – due to dropping of duplicates based on
            # grouping_keys (usually bitfount patient ID + laterality)

            output_df = pd.merge(all_metrics, patient_details, on=grouping_keys)

        return output_df

    def get_metric_over_time(
        self,
        sorted_merged_df: pd.DataFrame,
        metric_column: str,
        date_column: str,
        grouping_keys: list[str],
    ) -> pd.Series:
        """Groups and aggregates data by grouping_keys, usually by patient.

        Returns:
            A pandas Series with grouping_keys as index and a list of tuples
            eg. [(metric value, datetime),...] as values
        """
        # Zip metric column with date column
        sorted_merged_df[f"{metric_column}_longitudinal"] = list(
            zip(sorted_merged_df[metric_column], sorted_merged_df[date_column])
        )

        # Group data by patient per eye
        # output eg.
        # patient  laterality                     {metric}_longitudinal
        # jane              L                        [(51, 2022-01-01)]
        # john              R    [(224, 2020-01-01), (345, 2021-01-01)]
        # john              L    [(224, 2021-01-01), (345, 2022-01-01)]

        output = sorted_merged_df.groupby(grouping_keys)[
            f"{metric_column}_longitudinal"
        ].agg(list)

        return output


class LongitudinalAlgorithm(
    BaseNonModelAlgorithmFactory[NoResultsModellerAlgorithm, _WorkerSide]
):
    """Algorithm for calculating the changes in metrics over time."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {}

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> NoResultsModellerAlgorithm:
        """Modeller-side of the algorithm."""
        return NoResultsModellerAlgorithm(
            log_message="Running Longitudinal Algorithm",
            **kwargs,
        )

    def worker(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the algorithm."""
        return _WorkerSide(
            **kwargs,
        )
