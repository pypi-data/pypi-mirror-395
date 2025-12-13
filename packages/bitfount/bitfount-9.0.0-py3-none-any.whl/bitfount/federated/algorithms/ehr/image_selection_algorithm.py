"""For selection of images related to patients for upload."""

from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any, ClassVar, Optional

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    PATIENT_ID_COL,
)
from bitfount.federated.exceptions import AlgorithmError
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.types import ProtocolContext
from bitfount.types import T_FIELDS_DICT

_logger = _get_federated_logger(__name__)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algo for selecting images related to a patient."""

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        """Initialize the worker-side algorithm.

        Args:
            patient_ids: List of patient IDs to get images for.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

    def initialise(
        self,
        *,
        datasource: BaseSource,
        data_splitter: Optional[DatasetSplitter] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        self.initialise_data(datasource=datasource, data_splitter=data_splitter)

    def run(
        self,
        patient_ids: Iterable[str],
    ) -> dict[str, list[Path]]:
        """Returns list of file paths related to patient IDs.

        Args:
            patient_ids: List or set of patient ids to identify files for.

        Returns:
            Dictionary mapping patient ID to list of file paths (Path objects).
        """
        # Convert to set for faster lookup if it's a list
        patient_ids_set = (
            patient_ids if isinstance(patient_ids, set) else set(patient_ids)
        )
        # Filter out empty and whitespace-only patient IDs
        patient_ids_set = {pid for pid in patient_ids_set if pid and pid.strip()}

        files_to_upload: dict[str, list[Path]] = defaultdict(list)

        patient_id_column = None

        for data in self.datasource.yield_data(use_cache=True):
            if ORIGINAL_FILENAME_METADATA_COLUMN not in data.columns:
                raise AlgorithmError(
                    f"Missing {ORIGINAL_FILENAME_METADATA_COLUMN}"
                    f" column in data to determine which images"
                    f" to upload."
                )

            if patient_id_column is None:
                if PATIENT_ID_COL in data.columns:
                    patient_id_column = PATIENT_ID_COL
                elif "patient_key" in data.columns:
                    patient_id_column = (
                        "patient_key"  # Heidelberg would use patient_key
                    )
                else:
                    _logger.error(
                        f"Unable to find patient ID column in data:"
                        f" tried {PATIENT_ID_COL} and 'patient_key'"
                    )
                    raise AlgorithmError(
                        "Unable to find matching records as "
                        "patient ID is not present in data"
                    )

            # Check all rows for empty patient IDs and log warnings
            # Then filter to matching rows for processing
            for _, row in data.iterrows():
                patient_id = row[patient_id_column]
                # Convert to string first to handle None values
                patient_id_str = str(patient_id) if patient_id is not None else ""
                if not patient_id_str.strip():
                    _logger.warning("Skipping row with empty patient ID")
                    continue

            # Use .isin() for better performance with sets
            matching_patient_rows = data[data[patient_id_column].isin(patient_ids_set)]

            if len(matching_patient_rows) == 0:
                continue

            # Collect matching files, skipping empty patient IDs (defensive check)
            for _, row in matching_patient_rows.iterrows():
                patient_id = row[patient_id_column]

                # Skip empty or whitespace-only patient IDs
                # Convert to string first to handle None values
                patient_id_str = str(patient_id) if patient_id is not None else ""
                if not patient_id_str.strip():
                    continue  # Already logged above

                file_path = Path(row[ORIGINAL_FILENAME_METADATA_COLUMN])
                files_to_upload[patient_id].append(file_path)

        return files_to_upload


class ImageSelectionAlgorithm(
    BaseNonModelAlgorithmFactory[NoResultsModellerAlgorithm, _WorkerSide]
):
    """Algorithm for selecting images related to a patient."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {}

    def __init__(
        self,
        datastructure: DataStructure,
        **kwargs: Any,
    ) -> None:
        """Initialize the algorithm.

        Args:
            datastructure: The data structure definition
            patient_ids: The patients for whom to identify a list of images.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(datastructure=datastructure, **kwargs)

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> NoResultsModellerAlgorithm:
        """Modeller-side of the algorithm."""
        return NoResultsModellerAlgorithm(
            log_message="Running Image Selection Algorithm",
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
