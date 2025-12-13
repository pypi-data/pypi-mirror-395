"""Algorithms and related functionality for simply outputting data to CSV."""

from __future__ import annotations

from functools import partial
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Collection, Optional

from marshmallow import fields
import pandas as pd

from bitfount.data.datasources.base_source import (
    BaseSource,
)
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ehr.ehr_patient_query_algorithm import GENDER_COL_EHR
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    _BITFOUNT_PATIENT_ID_KEY,
    ADDRESS_COL,
    AGE_COL,
    CELL_NUMBER_COL,
    CPT4_COLUMN,
    DISTANCE_FROM_FOVEA_CENTRE_COL,
    DOB_COL,
    EMAIL_COL,
    FILTER_FAILED_REASON_COLUMN,
    FILTER_MATCHING_COLUMN,
    HOME_NUMBER_COL,
    ICD10_COLUMN,
    LARGEST_LEGION_SIZE_COL_PREFIX,
    LATERALITY_COL,
    LATEST_PRACTITIONER_NAME_COL,
    MRN_COL,
    NAME_COL,
    NEXT_APPOINTMENT_COL,
    PREV_APPOINTMENTS_COL,
    SMALLEST_LEGION_SIZE_COL,
    SUBFOVEAL_COL,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ProtocolContext, get_task_results_directory
from bitfount.types import T_FIELDS_DICT
from bitfount.utils.fs_utils import safe_write_to_file
from bitfount.utils.pandas_utils import combine_csv_files

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig


_logger = _get_federated_logger(__name__)


REDUCE_CSV_ALGORITHM_CHARCOAL_COLUMNS = [
    "Left Eye Scan Details",
    "Right Eye Scan Details",
    "Latest Left Scan Filename",
    "Latest Right Scan Filename",
    "Latest Left Scan Exclusion Reason",
    "Latest Right Scan Exclusion Reason",
    "Scanned Files",
    "Number of scans",
    "Patient Eligible",
]


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the ReduceCSVAlgorithmCharcoal algorithm."""

    def __init__(
        self,
        save_path: Path,
        eligible_only: bool = True,
        delete_intermediate: bool = True,
        **kwargs: Any,
    ) -> None:
        """Create a new worker side of the _SimpleCSVAlgorithm algorithm.

        Args:
            save_path: The path to a directory to output the CSV to from the worker.
            eligible_only: Final CSV to output only eligible patients.
            delete_intermediate: Delete the intermediate results after use.
            **kwargs: Passed to parent.
        """
        super().__init__(**kwargs)
        self.save_path = save_path
        self.eligible_only = eligible_only
        self.delete_intermediate = delete_intermediate
        self.output_files: set[Path] = set()

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
        task_id: str,
        csv_output_files: set[Path],
    ) -> None:
        """Reads previous CSV output and reduces it to one-row-per-patient."""
        output_csv_path = self.get_output_csv_results_path(task_id)

        if not csv_output_files:
            _logger.warning(
                "No intermediate CSV files supplied,"
                " aborting ReduceCSVAlgorithmCharcoal"
            )
            return

        # Combine the (potentially multiple) intermediate CSVs into a single dataframe
        df = self._combine_results_csvs(csv_output_files)
        if df.empty:
            _logger.warning(
                "No data after combining CSV files, aborting ReduceCSVAlgorithmCharcoal"
            )
            return

        df = self._reduce_df(df)
        if df.empty:
            _logger.warning(
                "No data after reducing CSV files, results file will be empty"
            )

        # Write the final dataframe to CSV
        _, output_csv_path = safe_write_to_file(
            partial(
                df.to_csv,
                mode="w",
                header=True,
                # The index of the reduced dataframe is the BitfountPatientID and we
                # _do_ want to write this out as the index to the CSV
                index=True,
                na_rep="N/A",
            ),
            output_csv_path,
        )
        _logger.info(f"Reduced (final) CSV output to {output_csv_path}")

        # Save the actually output file path(s)
        self.output_files.add(output_csv_path)

        if self.delete_intermediate:
            # Delete intermediate csv results
            for csv_path in csv_output_files:
                try:
                    os.remove(csv_path)
                except OSError as e:
                    _logger.warning(
                        f"Error deleting intermediate CSV file at {csv_path}: {str(e)}"
                    )

    def _combine_results_csvs(self, csv_output_files: Collection[Path]) -> pd.DataFrame:
        """Combine the (potentially multiple) intermediate CSV(s) into a dataframe."""
        csv_output_files_list = list(csv_output_files)

        # Fast-load if there's only one CSV file as there's nothing to combine
        if len(csv_output_files_list) == 1:
            csv_path = csv_output_files_list[0]
            _logger.info(f"Reading intermediate results CSV at {csv_path}.")
            return pd.read_csv(csv_path, index_col=False)

        # Otherwise, work through and combine them all
        _logger.info(
            f"Combining {len(csv_output_files_list)} intermediate results CSVs:"
            f" {', '.join(str(i) for i in csv_output_files_list[:5])}, ..."
        )
        return combine_csv_files(csv_output_files_list)

    def _reduce_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Reduces dataframe from one-row-per-scan to one-row-per-patient.

        Sets the index of the resulting dataframe to the BitfountPatientID.
        """
        date_sorted_df = df.sort_values("Acquisition DateTime")
        grouped = date_sorted_df.groupby(_BITFOUNT_PATIENT_ID_KEY)

        results_df = pd.DataFrame()
        results_df["Number of scans"] = grouped[NAME_COL].count()

        # All EHR columns would have the same value for all rows of a patient
        EHR_COLS = [
            NAME_COL,
            DOB_COL,
            AGE_COL,
            GENDER_COL_EHR,
            HOME_NUMBER_COL,
            CELL_NUMBER_COL,
            EMAIL_COL,
            ADDRESS_COL,
            MRN_COL,
            ICD10_COLUMN,
            CPT4_COLUMN,
            NEXT_APPOINTMENT_COL,
            PREV_APPOINTMENTS_COL,
            LATEST_PRACTITIONER_NAME_COL,
        ]
        results_df = results_df.join(grouped.first()[EHR_COLS])

        # Display the names of files we've looked at
        results_df["Scanned Files"] = grouped[ORIGINAL_FILENAME_METADATA_COLUMN].apply(
            ", ".join
        )

        most_recent_scan_per_patient_lat = (
            date_sorted_df.groupby([_BITFOUNT_PATIENT_ID_KEY, LATERALITY_COL])
            .tail(1)
            .set_index("BitfountPatientID")
        )

        # Provide details about most recent Left scan
        left_results = most_recent_scan_per_patient_lat[
            most_recent_scan_per_patient_lat[LATERALITY_COL].apply(
                lambda lat: lat.lower() in ("l", "left")
            )
        ]
        left_results["Left Eye Scan Details"] = left_results.apply(
            self._format_scan_details,
            axis=1,
        )
        # Provide details about most recent Right scan
        right_results = most_recent_scan_per_patient_lat[
            most_recent_scan_per_patient_lat[LATERALITY_COL].apply(
                lambda lat: lat.lower() in ("r", "right")
            )
        ]

        right_results["Right Eye Scan Details"] = right_results.apply(
            self._format_scan_details,
            axis=1,
        )

        results_df = results_df.join(left_results["Left Eye Scan Details"])
        results_df["Latest Left Scan Filename"] = left_results["_original_filename"]
        results_df["Latest Left Scan Exclusion Reason"] = left_results[
            FILTER_FAILED_REASON_COLUMN
        ]

        results_df = results_df.join(right_results["Right Eye Scan Details"])
        results_df["Latest Right Scan Filename"] = right_results["_original_filename"]
        results_df["Latest Right Scan Exclusion Reason"] = right_results[
            FILTER_FAILED_REASON_COLUMN
        ]

        # Eligibility column - Patient is only eligible if most recent scan says so
        results_df["Patient Eligible"] = most_recent_scan_per_patient_lat.groupby(
            _BITFOUNT_PATIENT_ID_KEY
        )[FILTER_MATCHING_COLUMN].any()

        if self.eligible_only:
            results_df = results_df[results_df["Patient Eligible"]]

        return results_df.fillna("Not Applicable")

    def _format_scan_details(self, row: pd.Series) -> str:
        """Formats GA metrics into a readable string."""
        # Get lesion size values, handling potential NaN or missing values
        largest_lesion_val = row.get(LARGEST_LEGION_SIZE_COL_PREFIX)
        largest_lesion = (
            f"{largest_lesion_val:.2f}" if pd.notna(largest_lesion_val) else "N/A"
        )
        smallest_lesion_val = row.get(SMALLEST_LEGION_SIZE_COL)
        smallest_lesion = (
            f"{smallest_lesion_val:.2f}" if pd.notna(smallest_lesion_val) else "N/A"
        )

        # Generate string for subfoveal lesion detection reason
        # The spacing and comma are included in this string so that (if it's not
        # actually set), the final scan_details string will not be malformed with
        # extra spaces or commas
        subfov_str = ""
        if row[SUBFOVEAL_COL] == "N":
            subfov_str = " Subfoveal lesion not detected,"
        elif row[SUBFOVEAL_COL] == "Y":
            subfov_str = " Subfoveal lesion detected,"
        elif row[SUBFOVEAL_COL] == "Fovea not detected":
            subfov_str = " Fovea not detected,"

        # Get distance from fovea, handling potential NaN or missing values
        distance_from_fovea_val = row.get(DISTANCE_FROM_FOVEA_CENTRE_COL)
        distance_from_fovea = (
            f"{distance_from_fovea_val:.2f}"
            if pd.notna(distance_from_fovea_val)
            else "N/A"
        )

        scan_details = (
            f"Latest Scan on {row['Acquisition DateTime']}"
            f" detected {row['total_ga_area']} mm2 area of GA,"
            f" largest lesion size: {largest_lesion} mm2,"
            f" smallest lesion size: {smallest_lesion} mm2,"
            # The spacing and comma are included in subfov_str so that (if it's not
            # actually set), the final scan_details string will not be malformed with
            # extra spaces or commas
            f"{subfov_str}"
            f" distance from fovea: {distance_from_fovea} mm,"
            f" max cnv probability: {row['max_cnv_probability']},"
            f" max hard drusen probability: {row['max_hard_drusen_probability']},"
            f" max soft drusen probability: {row['max_soft_drusen_probability']},"
            f" max confluent drusen probability:"
            f" {row['max_confluent_drusen_probability']}"
        )

        return scan_details

    def _get_expected_csv_results_path(self, task_id: str) -> Path:
        """Get the expected path for the CSV results from a previous step."""
        # Only append task ID subdirectory if the path doesn't already have the task
        # ID at the end
        if self.save_path.name != task_id:
            return self.save_path / task_id / "results.csv"
        else:
            self.save_path.mkdir(parents=True, exist_ok=True)
            return self.save_path / "results.csv"

    def get_output_csv_results_path(self, task_id: str) -> Path:
        """Get the path that the final CSV results should be output to."""
        # Only append task ID subdirectory if the path doesn't already have the task
        # ID at the end
        if self.save_path.name != task_id:
            return self.save_path / task_id / "final_results.csv"
        else:
            self.save_path.mkdir(parents=True, exist_ok=True)
            return self.save_path / "final_results.csv"


class ReduceCSVAlgorithmCharcoal(
    BaseNonModelAlgorithmFactory[NoResultsModellerAlgorithm, _WorkerSide]
):
    """Algorithm that reduces Charcoal CSV results to one-row-per-patient.

    Args:
        datastructure: The datastructure to use.
        eligible_only: Final CSV to output only eligible patients.
        delete_intermediate: Delete the intermediate results after use.
        **kwargs: Passed to parent.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "eligible_only": fields.Boolean(),
        "delete_intermediate": fields.Boolean(),
    }

    def __init__(
        self,
        datastructure: DataStructure,
        eligible_only: bool = True,
        delete_intermediate: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(datastructure=datastructure, **kwargs)
        self.eligible_only = eligible_only
        self.delete_intermediate = delete_intermediate

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> NoResultsModellerAlgorithm:
        """Modeller-side of the ReduceCSVAlgorithmCharcoal algorithm."""
        return NoResultsModellerAlgorithm(
            log_message="Running Reduce CSV Algorithm",
            **kwargs,
        )

    def worker(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the ReduceCSVAlgorithmCharcoal algorithm."""
        task_results_dir = get_task_results_directory(context)

        return _WorkerSide(
            save_path=task_results_dir,
            eligible_only=self.eligible_only,
            delete_intermediate=self.delete_intermediate,
            **kwargs,
        )
