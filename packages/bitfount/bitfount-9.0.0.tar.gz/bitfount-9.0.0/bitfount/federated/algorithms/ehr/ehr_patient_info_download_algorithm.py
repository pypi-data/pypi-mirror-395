"""EHR Patient Info download algorithm to access patient data.

This module implements an algorithm for downloading all patient information
from EHR systems. It provides functionality to:
- Authenticate with NextGen's FHIR, Enterprise, and SMART on FHIR APIs
- Authenticate with FHIR R4 compatible systems
- Look up and download relevant info and documents for a given list of
  patient_ids
"""

from collections import defaultdict
from pathlib import Path
from typing import Any, ClassVar, Optional

from bitfount.data.datastructure import DataStructure
from bitfount.externals.ehr.fhir_r4.exceptions import (
    NoFHIRR4PatientIDError,
    NoMatchingFHIRR4PatientError,
    NonSpecificFHIRR4PatientError,
)
from bitfount.externals.ehr.fhir_r4.querier import FHIRR4PatientQuerier
from bitfount.externals.ehr.nextgen.authentication import NextGenAuthSession
from bitfount.externals.ehr.nextgen.exceptions import (
    NoMatchingNextGenPatientError,
    NoNextGenPatientIDError,
)
from bitfount.externals.ehr.nextgen.querier import (
    FromPatientQueryError,
    NextGenPatientQuerier,
)
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ehr.ehr_base_algorithm import (
    BaseEHRWorkerAlgorithm,
    QuerierType,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ProtocolContext
from bitfount.hub.api import (
    BitfountHub,
    SMARTOnFHIR,
)
from bitfount.hub.authentication_flow import (
    BitfountSession,
)
from bitfount.types import T_FIELDS_DICT

_logger = _get_federated_logger(__name__)


class _WorkerSide(BaseEHRWorkerAlgorithm):
    """Worker side of the algorithm for downloading patient info from EHR.

    Supports both NextGen and FHIR R4 compatible EHR systems.
    """

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        """Initialize the worker-side algorithm.

        Args:
            session: BitfountSession object for use with SMARTOnFHIR service. Will be
                created if not provided.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

    def run(
        self,
        patient_ids: list[str],
        download_path: Path,
        run_document_download: bool = True,
        run_json_dump: bool = True,
    ) -> dict[str, list[Path]]:
        """Download relevant info and documents for supplied list of patients.

        Args:
            patient_ids: List of patient ids to download data for.
            download_path: Local path to save the downloaded patient info.
            run_document_download: Boolean flag to turn on/off document downloads,
                downloads documents by default.
            run_json_dump: Boolean flag to turn on/off patient info JSON dump,
                does the JSON dump by default.

        Returns:
            Dictionary of patient_id string to list of paths of downloaded
            files related to that patient. Note: patient_ids may be MRNs,
            which will be resolved to actual EHR patient IDs.
        """
        if self.querier_type == QuerierType.NEXTGEN:
            files_to_upload = self._run_for_nextgen(
                patient_ids,
                download_path,
                run_document_download,
                run_json_dump,
            )
        elif self.querier_type == QuerierType.FHIR_R4:
            files_to_upload = self._run_for_fhir_r4(
                patient_ids,
                download_path,
                run_document_download,
                run_json_dump,
            )
        else:
            raise NotImplementedError(
                f"Download mechanism has not been implemented yet for this "
                f"EHR system, {self.querier_type.value}."
            )

        return files_to_upload

    def _run_for_nextgen(
        self,
        patient_ids: list[str],
        download_path: Path,
        run_document_download: bool = True,
        run_json_dump: bool = True,
    ) -> dict[str, list[Path]]:
        """Download files with NextGen EHR."""
        if not run_document_download and not run_json_dump:
            _logger.warning(
                "Neither document download nor JSON dump requested, skipping."
            )
            return {}

        # Filter out empty and whitespace-only patient IDs
        valid_patient_ids = [pid for pid in patient_ids if pid and pid.strip()]
        if len(valid_patient_ids) < len(patient_ids):
            skipped = len(patient_ids) - len(valid_patient_ids)
            _logger.warning(f"Skipped {skipped} empty patient ID(s) from provided list")

        if not valid_patient_ids:
            _logger.warning("No valid patient IDs to process")
            return {}

        # Get SMART on FHIR bearer token
        smart_auth = SMARTOnFHIR(
            session=self.session,
            smart_on_fhir_url=self.smart_on_fhir_url,
            resource_server_url=self.smart_on_fhir_resource_server_url,
        )
        nextgen_session = NextGenAuthSession(smart_auth)

        files_to_upload: dict[str, list[Path]] = defaultdict(list)

        # Process each patient
        num_patient_ids = len(valid_patient_ids)
        for i, patient_id_or_mrn in enumerate(valid_patient_ids, start=1):
            # Defensive check: skip empty or whitespace-only patient IDs
            # (shouldn't happen after filtering)
            if not patient_id_or_mrn or not patient_id_or_mrn.strip():
                _logger.warning(
                    f"Skipping empty patient ID at position {i} of {num_patient_ids}"
                )
                continue

            _logger.info(f"Running EHR extraction for patient {i} of {num_patient_ids}")
            try:
                # Try to use as MRN first, then fall back to direct patient ID
                nextgen_querier: NextGenPatientQuerier
                try:
                    nextgen_querier = NextGenPatientQuerier.from_mrn(
                        mrn=patient_id_or_mrn,
                        nextgen_session=nextgen_session,
                        fhir_url=self.fhir_url,
                        enterprise_url=self.enterprise_url,  # type:ignore[arg-type] # Reason: would have been set during initialise #noqa:E501
                    )
                    _logger.debug(
                        f"Found patient using MRN lookup: {patient_id_or_mrn}"
                    )
                except (
                    FromPatientQueryError,
                    NoMatchingNextGenPatientError,
                    NoNextGenPatientIDError,
                ) as e:
                    _logger.debug(
                        f"MRN lookup failed for {patient_id_or_mrn}, "
                        f"trying as direct patient ID: {str(e)}"
                    )
                    # Fall back to using as direct patient ID
                    nextgen_querier = NextGenPatientQuerier.from_nextgen_session(
                        patient_id=patient_id_or_mrn,
                        nextgen_session=nextgen_session,
                        fhir_url=self.fhir_url,
                        enterprise_url=self.enterprise_url,  # type:ignore[arg-type] # Reason: would have been set during initialise #noqa:E501
                    )

                # Create directory for patient document download
                # Use original input for folder name to maintain consistency
                patient_folder_path = download_path / patient_id_or_mrn
                patient_folder_path.mkdir(parents=True, exist_ok=True)
                _logger.debug(
                    f"Created output dir for patient {patient_id_or_mrn}"
                    f" at {str(patient_folder_path)}"
                )

                if run_document_download:
                    _logger.info(
                        f"Downloading documents for patient {i} of {num_patient_ids}"
                    )
                    downloaded_docs = nextgen_querier.download_all_documents(
                        save_path=patient_folder_path
                    )

                    files_to_upload[patient_id_or_mrn].extend(downloaded_docs)

                if run_json_dump:
                    _logger.info(
                        f"Downloading JSON entries for patient {i} of {num_patient_ids}"
                    )
                    nextgen_querier.produce_json_dump(
                        save_path=patient_folder_path / "patient_info.json"
                    )
                    files_to_upload[patient_id_or_mrn].append(
                        patient_folder_path / "patient_info.json",
                    )
            except Exception as e:
                err_msg = (
                    f"Failed to process patient {patient_id_or_mrn}"
                    f" ({i} of {num_patient_ids}): {str(e)}"
                )
                _logger.error(err_msg)
                _logger.debug(err_msg, exc_info=True)
                # Continue processing remaining patients
                continue

        return files_to_upload

    def _run_for_fhir_r4(
        self,
        patient_ids: list[str],
        download_path: Path,
        run_document_download: bool = True,
        run_json_dump: bool = True,
    ) -> dict[str, list[Path]]:
        """Download files with FHIR R4 compatible EHR systems."""
        if not run_document_download and not run_json_dump:
            _logger.warning(
                "Neither document download nor JSON dump requested, skipping."
            )
            return {}

        if self.fhir_client is None:
            raise ValueError(
                "Worker should not have been initialized without fhir_client"
            )

        # Filter out empty and whitespace-only patient IDs
        valid_patient_ids = [pid for pid in patient_ids if pid and pid.strip()]
        if len(valid_patient_ids) < len(patient_ids):
            skipped = len(patient_ids) - len(valid_patient_ids)
            _logger.warning(f"Skipped {skipped} empty patient ID(s) from provided list")

        if not valid_patient_ids:
            _logger.warning("No valid patient IDs to process")
            return {}

        # Refresh the FHIR client token before use
        self._refresh_fhir_client_token()

        files_to_upload: dict[str, list[Path]] = defaultdict(list)

        # Process each patient
        num_patient_ids = len(valid_patient_ids)
        for i, patient_id_or_mrn in enumerate(valid_patient_ids, start=1):
            # Defensive check: skip empty or whitespace-only patient IDs
            # (shouldn't happen after filtering)
            if not patient_id_or_mrn or not patient_id_or_mrn.strip():
                _logger.warning(
                    f"Skipping empty patient ID at position {i} of {num_patient_ids}"
                )
                continue

            _logger.info(f"Running EHR extraction for patient {i} of {num_patient_ids}")
            try:
                # Try to use as MRN first, then fall back to direct patient ID
                fhir_querier: FHIRR4PatientQuerier
                try:
                    fhir_querier = FHIRR4PatientQuerier.from_mrn(
                        mrn=patient_id_or_mrn,
                        fhir_client=self.fhir_client,
                        ehr_provider=self.ehr_config.provider,
                    )
                    _logger.debug(
                        f"Found patient using MRN lookup: {patient_id_or_mrn}"
                    )
                except (
                    NoMatchingFHIRR4PatientError,
                    NoFHIRR4PatientIDError,
                    NonSpecificFHIRR4PatientError,
                ) as e:
                    _logger.debug(
                        f"MRN lookup failed for {patient_id_or_mrn}, "
                        f"trying as direct patient ID: {str(e)}"
                    )
                    # Fall back to using as direct patient ID
                    fhir_querier = FHIRR4PatientQuerier(
                        patient_id=patient_id_or_mrn,
                        fhir_client=self.fhir_client,
                        ehr_provider=self.ehr_config.provider,
                    )
                    # Get patient info by ID to populate patient_dict for
                    # JSON dump
                    patient_dict = fhir_querier.get_patient_response_by_id()
                    if patient_dict:
                        fhir_querier.patient_dict = patient_dict

                # Create directory for patient document download
                # Use original input for folder name to maintain consistency
                patient_folder_path = download_path / patient_id_or_mrn
                patient_folder_path.mkdir(parents=True, exist_ok=True)
                _logger.debug(
                    f"Created output dir for patient {patient_id_or_mrn}"
                    f" at {str(patient_folder_path)}"
                )

                if run_document_download:
                    _logger.info(
                        f"Downloading documents for patient {i} of {num_patient_ids}"
                    )
                    downloaded_docs = fhir_querier.download_all_documents(
                        save_path=patient_folder_path
                    )

                    files_to_upload[patient_id_or_mrn].extend(downloaded_docs)

                if run_json_dump:
                    _logger.info(
                        f"Downloading JSON entries for patient {i} of {num_patient_ids}"
                    )
                    fhir_querier.produce_json_dump(
                        save_path=patient_folder_path / "patient_info.json"
                    )
                    files_to_upload[patient_id_or_mrn].append(
                        patient_folder_path / "patient_info.json",
                    )
            except Exception as e:
                err_msg = (
                    f"Failed to process patient {patient_id_or_mrn}"
                    f" ({i} of {num_patient_ids}): {str(e)}"
                )
                _logger.error(err_msg)
                _logger.debug(err_msg, exc_info=True)
                # Continue processing remaining patients
                continue

        return files_to_upload


class EHRPatientInfoDownloadAlgorithm(
    BaseNonModelAlgorithmFactory[NoResultsModellerAlgorithm, _WorkerSide]
):
    """Algorithm for downloading patient info and documents from EHR."""

    # DEV: This is set so that the algorithm/encapsulating protocol won't try to use
    #      the `processed_files_cache` as the context for this algorithm is that it
    #      will be running in a protocol that just receives a list of patient IDs,
    #      doesn't interact with the datasource.
    _inference_algorithm = False

    fields_dict: ClassVar[T_FIELDS_DICT] = {}

    def __init__(
        self,
        datastructure: DataStructure,
        **kwargs: Any,
    ) -> None:
        """Initialize the algorithm.

        Args:
            datastructure: The data structure definition
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
            log_message="Running EHR Patient Info Download Algorithm",
            **kwargs,
        )

    def worker(
        self,
        *,
        hub: Optional[BitfountHub] = None,
        session: Optional[BitfountSession] = None,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the algorithm.

        Note: hub and session are only required for NextGen EHR systems.
        For FHIR R4 systems, these are not needed.
        """
        # For NextGen systems, hub or session is required
        # For FHIR R4 systems, they are not needed
        # We'll allow None here and let the base class handle validation
        # during initialise based on the EHR provider type

        session_: Optional[BitfountSession] = None
        if hub is not None and session is not None:
            _logger.warning(
                "Both hub and session were provided;"
                " using provided session in preference to hub session."
            )
            session_ = session
        elif hub is not None:
            session_ = hub.session
        elif session is not None:
            session_ = session

        return _WorkerSide(
            hub=hub,
            session=session_,
            **kwargs,
        )
