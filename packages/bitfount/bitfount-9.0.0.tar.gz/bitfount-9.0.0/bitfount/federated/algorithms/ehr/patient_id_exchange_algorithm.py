"""Patient ID Exchange algorithm for initial setup.

This algorithm handles the exchange of patient IDs from modeller to worker
during the initial setup phase, before any batching occurs.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, ClassVar, Optional, cast

from bitfount.data.datasources.base_source import (
    BaseSource,
)
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.types import ProtocolContext
from bitfount.types import T_FIELDS_DICT

_logger = _get_federated_logger(__name__)


class _ModellerSide(NoResultsModellerAlgorithm):
    """Modeller side of the patient ID exchange algorithm.

    This class implements InitialSetupModellerAlgorithm protocol by providing
    the required methods (remote_modeller property and values_to_send_to_worker
    method).
    """

    def __init__(
        self,
        patient_ids: Optional[list[str]] = None,
        patient_ids_file: Optional[os.PathLike | str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the modeller-side algorithm.

        Args:
            patient_ids: List of patient ID strings to send to workers.
                Mutually exclusive with `patient_ids_file`.
            patient_ids_file: Path to file containing patient ID strings, one per
                line. Mutually exclusive with `patient_ids`.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(log_message="Patient ID Exchange", **kwargs)

        # Check that we have only one of `patient_ids` and `patient_ids_file`
        if patient_ids is not None and patient_ids_file is not None:
            _logger.error(
                "Cannot have both `patient_ids` and `patient_ids_file`,"
                " please supply only one option."
            )
            raise ValueError(
                "Cannot have both `patient_ids` and `patient_ids_file`"
                " in PatientIDExchangeAlgorithm modeller side,"
                " please supply only one option."
            )
        if patient_ids is None and patient_ids_file is None:
            _logger.error(
                "Must have one of `patient_ids` and `patient_ids_file`,"
                " please supply one option."
            )
            raise ValueError(
                "Must have one of `patient_ids` and `patient_ids_file`"
                " in PatientIDExchangeAlgorithm modeller side,"
                " please supply one option."
            )

        # Extract and validate patient IDs
        if patient_ids is not None:
            # Filter out empty strings from provided list
            self._patient_ids = [pid for pid in patient_ids if pid]
        else:  # patient_ids_file is not None
            # Checks above should ensure, but check again
            if patient_ids_file is None:
                raise ValueError(f"{patient_ids_file=}. Previous checks have failed.")
            self._patient_ids = self._extract_patient_ids_from_file(patient_ids_file)
        # Remove any duplicates and empty strings
        self._patient_ids = [pid for pid in set(self._patient_ids) if pid]
        if not self._patient_ids:
            _logger.error("No valid (non-empty) patient IDs found")
            raise ValueError(
                "No valid (non-empty) patient IDs found. "
                "Please provide at least one non-empty patient ID."
            )

    @staticmethod
    def _extract_patient_ids_from_file(
        patient_ids_file: os.PathLike | str,
    ) -> list[str]:
        """Extract patient IDs from file.

        Expected format is one patient ID per line. Empty lines are skipped.

        Args:
            patient_ids_file: Path to file containing patient ID strings.

        Returns:
            List of patient ID strings extracted from the file.
        """
        _logger.debug(f"Extracting patient IDs from {str(patient_ids_file)}")
        with open(patient_ids_file) as f:
            patient_ids = [line.strip() for line in f.read().splitlines()]
            # Filter out empty strings
            return [pid for pid in patient_ids if pid]

    @property
    def remote_modeller(self) -> bool:
        """Whether the algorithm needs to accommodate a remote modeller.

        Always True for this algorithm as patient IDs are always sent from
        modeller to worker.
        """
        return True

    def values_to_send_to_worker(self) -> dict[str, Any]:
        """Get the patient IDs to send to the worker side."""
        return {"patient_ids": self._patient_ids}


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the patient ID exchange algorithm.

    This class implements InitialSetupWorkerAlgorithm protocol by providing
    the required methods (remote_modeller property, setup_run method, and
    update_values_from_modeller method).
    """

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        """Initialize the worker-side algorithm.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self._patient_ids: Optional[list[str]] = None

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
        """Does nothing for this algorithm."""
        pass

    @property
    def remote_modeller(self) -> bool:
        """Whether the algorithm needs to accommodate a remote modeller.

        Always True for this algorithm as patient IDs are always sent from
        modeller to worker.
        """
        return True

    def setup_run(self, **kwargs: Any) -> None:
        """Run setup operations before batching begins.

        This method is called by protocols tagged with InitialSetupWorkerProtocol
        before any batching occurs. For this algorithm, it's a no-op as the
        patient IDs are received via update_values_from_modeller().
        """
        # No setup needed - patient IDs are received via update_values_from_modeller
        pass

    @property
    def should_output_data(self) -> bool:
        """Indicates whether the initial setup algorithm should output data.

        For the most part initial setup algorithms will set up data, filtering it,
        grouping it, etc., and so this property should return True. However, there are
        some algorithms that don't produce any data (e.g., algorithms that use the
        initial setup phase to exchange runtime information) and so this property
        should return False.'
        """
        # This algorithm doesn't produce/set any data, is just used to exchange the
        # patient IDs before running. Return False.
        return False

    def update_values_from_modeller(self, values: dict[str, Any]) -> None:
        """Update the patient IDs sent from the modeller side."""
        if "patient_ids" not in values:
            _logger.error(
                "No patient_ids found in values from modeller. "
                "This may cause issues downstream."
            )
            self._patient_ids = []
        else:
            self._patient_ids = cast(list[str], values["patient_ids"])
            _logger.info(
                f"Received {len(self._patient_ids)} patient ID(s) from modeller"
            )

    def run(self, *args: Any, **kwargs: Any) -> None:
        """Regular run method - does nothing as this is only for initial setup."""
        pass

    @property
    def patient_ids(self) -> Optional[list[str]]:
        """Get the patient IDs received from the modeller."""
        return self._patient_ids


class PatientIDExchangeAlgorithm(
    BaseNonModelAlgorithmFactory[_ModellerSide, _WorkerSide]
):
    """Algorithm for exchanging patient IDs during initial setup.

    This algorithm handles the exchange of patient IDs from modeller to worker
    during the initial setup phase, before any batching occurs. It should be
    used as the first algorithm in protocols that need to send patient IDs to
    workers.

    Patient IDs can either be supplied as an explicit list of patient IDs or as a
    path to a file which contains one patient ID per line. These two options are
    mutually exclusive from each other.

    Args:
        datastructure: The data structure definition.
        patient_ids: List of patient ID strings to send to workers. Mutually
            exclusive with `patient_ids_file`.
        patient_ids_file: Path to file containing patient ID strings, one per line.
            Mutually exclusive with `patient_ids`.
        **kwargs: Additional keyword arguments.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        # Note: patient_ids and patient_ids_file are intentionally NOT in fields_dict
        # to prevent them from being serialized in the task definition.
        # They are only used on the modeller side and sent via initial setup exchange.
    }

    def __init__(
        self,
        datastructure: DataStructure,
        patient_ids: Optional[list[str]] = None,
        patient_ids_file: Optional[os.PathLike | str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the algorithm.

        Args:
            datastructure: The data structure definition.
            patient_ids: List of patient ID strings to send to workers. Mutually
                exclusive with `patient_ids_file`.
            patient_ids_file: Path to file containing patient ID strings, one per
                line. Mutually exclusive with `patient_ids`.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(datastructure=datastructure, **kwargs)
        self.patient_ids = patient_ids
        self.patient_ids_file = patient_ids_file

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _ModellerSide:
        """Modeller-side of the algorithm."""
        return _ModellerSide(
            patient_ids=self.patient_ids,
            patient_ids_file=self.patient_ids_file,
            **kwargs,
        )

    def worker(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the algorithm."""
        return _WorkerSide(**kwargs)


if TYPE_CHECKING:
    # Type checking to verify that the classes correctly implement the Protocol
    # interfaces. These assertions will be checked by type checkers like mypy.
    from bitfount.federated.algorithms.base import (
        InitialSetupModellerAlgorithm,
        InitialSetupWorkerAlgorithm,
    )

    # Verify _ModellerSide implements InitialSetupModellerAlgorithm
    _modeller_side_check: InitialSetupModellerAlgorithm = _ModellerSide(
        patient_ids=["test"], log_message="test"
    )

    # Verify _WorkerSide implements InitialSetupWorkerAlgorithm
    _worker_side_check: InitialSetupWorkerAlgorithm = _WorkerSide()
