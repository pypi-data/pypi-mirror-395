"""EHR Data Extraction protocol for Charcoal project.

Retrieves EHR JSON data and documents to dump to a location.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, cast

from marshmallow import fields
import torch

from bitfount.data.datasources.base_source import FileSystemIterableSource
from bitfount.data.datasources.null_source import NullSource
from bitfount.federated.algorithms.base import (
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ehr.ehr_patient_info_download_algorithm import (  # noqa: E501
    EHRPatientInfoDownloadAlgorithm,
    _WorkerSide as _DownloadAlgoWorkerSide,
)
from bitfount.federated.algorithms.ehr.image_selection_algorithm import (
    ImageSelectionAlgorithm,
    _WorkerSide as _ImageSelectionWorkerSide,
)
from bitfount.federated.algorithms.ehr.patient_id_exchange_algorithm import (
    PatientIDExchangeAlgorithm,
    _ModellerSide as _PatientIDExchangeModellerSide,
    _WorkerSide as _PatientIDExchangeWorkerSide,
)
from bitfount.federated.algorithms.s3_upload_algorithm import (
    S3UploadAlgorithm,
    _ModellerSide as _S3UploadModellerSide,
    _WorkerSide as _S3UploadWorkerSide,
)
from bitfount.federated.exceptions import AlgorithmError, ProtocolError
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.protocols.base import (
    BaseCompatibleAlgoFactory,
    BaseModellerProtocol,
    BaseProtocolFactory,
    BaseWorkerProtocol,
    InitialSetupModellerProtocol,
    InitialSetupWorkerProtocol,
    ModelInferenceProtocolMixin,
)
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import (
    ProtocolContext,
    get_task_results_directory,
)
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

_DATA_TRANSFER_SUBDIRECTORY = "data_extraction"


class _ModellerSide(
    BaseModellerProtocol,
    InitialSetupModellerProtocol[_PatientIDExchangeModellerSide],
):
    """Modeller side of the data extraction protocol for Charcoal project.

    Args:
        algorithm: The sequence of algorithms to be used.
        mailbox: The mailbox to use for communication with the Workers.
        **kwargs: Additional keyword arguments.
    """

    algorithm: Sequence[
        _PatientIDExchangeModellerSide
        | NoResultsModellerAlgorithm
        | _S3UploadModellerSide
    ]

    def __init__(
        self,
        *,
        algorithm: Sequence[
            _PatientIDExchangeModellerSide
            | NoResultsModellerAlgorithm
            | _S3UploadModellerSide
        ],
        mailbox: _ModellerMailbox,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

    def _extract_algorithms(
        self,
    ) -> tuple[
        _PatientIDExchangeModellerSide,
        NoResultsModellerAlgorithm,
        NoResultsModellerAlgorithm,
        _S3UploadModellerSide,
    ]:
        """Utility method to unpack and type the algorithm instances."""
        (
            patient_id_exchange_algo,
            download_info_algo,
            image_selection_algo,
            s3_upload_algo,
        ) = self.algorithm
        # Correct typing
        patient_id_exchange_algo = cast(
            _PatientIDExchangeModellerSide, patient_id_exchange_algo
        )
        download_info_algo = cast(NoResultsModellerAlgorithm, download_info_algo)
        image_selection_algo = cast(NoResultsModellerAlgorithm, image_selection_algo)
        s3_upload_algo = cast(_S3UploadModellerSide, s3_upload_algo)
        return (
            patient_id_exchange_algo,
            download_info_algo,
            image_selection_algo,
            s3_upload_algo,
        )

    def initialise(
        self,
        task_id: str,
        **kwargs: Any,
    ) -> None:
        """Initialises the component algorithms."""
        # DEV: Not currently used in this protocol (as no model algos) but protects
        #      for future case

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

        # Register S3 upload URL request handler
        # Default subdirectory structure for S3 uploads
        _, _, _, s3_upload_algo = self._extract_algorithms()
        _logger.info(
            f"Registering handler from {s3_upload_algo.class_name}"
            f" for generating S3 upload URLs"
        )
        s3_upload_algo.register_s3_upload_url_request_handler(
            mailbox=self.mailbox,
            subdirectory_for_upload=_DATA_TRANSFER_SUBDIRECTORY,
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

        This just sends the patient IDs to the workers and then tells the workers
        when the protocol is finished.

        Args:
            context: Optional. Run-time context for the protocol.
            **kwargs: Additional keyword arguments.
        """
        # Unpack the algorithms
        (
            _patient_id_exchange_algo,
            download_info_algo,
            image_selection_algo,
            s3_upload_algo,
        ) = self._extract_algorithms()
        result_run_algos: Sequence[NoResultsModellerAlgorithm] = [
            download_info_algo,
            image_selection_algo,
        ]

        _logger.info("Waiting on worker(s) to process")
        # Worker sends eval results for download/selection and S3 upload separately
        # First result: download/selection completion
        download_result = await self.mailbox.get_evaluation_results_from_workers()
        _logger.info("Received download/selection results from Pods.")

        # Second result: S3 upload completion
        # Note: S3 upload modeller side doesn't process results (it only generates URLs
        # via handlers), so we await the result but don't use it
        await self.mailbox.get_evaluation_results_from_workers()
        _logger.info("Received S3 upload results from Pods.")

        # Both algorithms are NoResultsModellerAlgorithm and don't use the result,
        # but we run both with the download result since the worker uses either
        # download_info_algo OR image_selection_algo depending on datasource type,
        # but both modeller-side algorithms should be run
        # Note: S3 upload modeller side doesn't process results (it only generates URLs
        # via handlers), so we don't run it here
        final_results = [
            algo.run(download_result)  # type: ignore[func-returns-value] # Reason: algos return None by design # noqa: E501
            for algo in result_run_algos
        ]

        return final_results

    def get_test_S3_url(self) -> None:
        """Get a test S3 upload URL from the upload algorithm, to ensure that we can."""
        # Unpack the algorithms
        _, _, _, s3_upload_algo = self._extract_algorithms()

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
        # Unpack the algorithms
        _, _, _, s3_upload_algo = self._extract_algorithms()

        try:
            session = get_boto_session(s3_upload_algo.aws_profile)
            check_aws_credentials_are_valid(session)
        except AWSError as e:
            raise ProtocolError(f"AWS credentials are not valid. Error: {e}") from e


class _WorkerSide(
    BaseWorkerProtocol,
    InitialSetupWorkerProtocol[_PatientIDExchangeWorkerSide],
    ModelInferenceProtocolMixin,
):
    """Worker side of the data extraction protocol for Charcoal project.

    Args:
        algorithm: The sequence of data extraction algorithms to be used.
        mailbox: The mailbox to use for communication with the Modeller.
        **kwargs: Additional keyword arguments.
    """

    algorithm: Sequence[
        _PatientIDExchangeWorkerSide
        | _DownloadAlgoWorkerSide
        | _ImageSelectionWorkerSide
        | _S3UploadWorkerSide
    ]

    def __init__(
        self,
        *,
        algorithm: Sequence[
            _PatientIDExchangeWorkerSide
            | _DownloadAlgoWorkerSide
            | _ImageSelectionWorkerSide
            | _S3UploadWorkerSide
        ],
        mailbox: _WorkerMailbox,
        output_dir: Path,
        trial_name: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)

        self._task_id: str = mailbox._task_id

        # Append task_id as a subdirectory if it's not already present at the end of
        # the path
        if output_dir.name != self._task_id:
            self.task_output_dir = output_dir / self._task_id
        else:
            self.task_output_dir = output_dir
        self.task_output_dir.mkdir(parents=True, exist_ok=True)
        _logger.info(
            f"Created output directory for this algorithm run"
            f" as {str(self.task_output_dir)}"
        )

        self.trial_name = trial_name

    async def run(
        self,
        *,
        pod_vitals: Optional[_PodVitals] = None,
        context: ProtocolContext,
        batch_num: Optional[int] = None,
        final_batch: bool = False,
        **kwargs: Any,
    ) -> None:
        """Runs worker side of data extraction protocol.

        Args:
            pod_vitals: Optional. Pod vitals instance for recording run-time details
                from the protocol run.
            context: Optional. Run-time context for the protocol.
            batch_num: The number of the batch being run.
            final_batch: If this run of the protocol represents the final run within
                a task.
            **kwargs: Additional keyword arguments.
        """
        # Unpack the algorithms
        (
            patient_id_exchange_algo,
            download_info_algo,
            image_selection_algo,
            s3_upload_algo,
        ) = self._extract_algorithms()

        # Get patient IDs from the exchange algorithm
        patient_ids_list = patient_id_exchange_algo.patient_ids
        if patient_ids_list is None:
            raise ProtocolError(
                "Patient IDs not received during initial setup. "
                "This should not happen if the protocol is properly "
                "configured."
            )
        # Filter out empty and whitespace-only strings and convert to set
        # for faster lookup
        patient_ids = {pid for pid in patient_ids_list if pid and pid.strip()}
        if len(patient_ids) < len(patient_ids_list):
            skipped = len(patient_ids_list) - len(patient_ids)
            _logger.warning(f"Skipped {skipped} empty patient ID(s) from received list")

        num_patient_ids = len(patient_ids)
        _logger.info(f"Processing {num_patient_ids} patients")

        # Check datasource type
        # NullSource (i.e. EHR source)
        if isinstance(self.datasource, NullSource):
            _logger.info("Datasource is NullSource - downloading EHR data")

            # Download EHR data for all patients
            patient_files = await self._download_ehr_data_for_all_patients(
                patient_ids,
                download_info_algo,
            )

            # Send eval result after download completes
            await self.mailbox.send_evaluation_results({})
            _logger.info("EHR data download completed")

            # Upload all downloaded files to S3 using the returned file list
            await self._upload_ehr_data_to_s3(
                patient_files,
                s3_upload_algo,
            )

            # Send eval result after S3 upload completes
            await self.mailbox.send_evaluation_results({})
            _logger.info("S3 upload completed")
        # FilesystemIterableSource (i.e. image source)
        elif isinstance(self.datasource, FileSystemIterableSource):
            _logger.info("Datasource is file-based - finding and uploading images")

            # Use ImageSelectionAlgorithm to find matching images
            files_to_upload = image_selection_algo.run(patient_ids=patient_ids)

            # Send eval result after image selection completes
            await self.mailbox.send_evaluation_results({})
            _logger.info("Image selection completed")

            # Upload files to S3
            await self._upload_image_files_to_s3(
                files_to_upload,
                s3_upload_algo,
            )

            # Send eval result after S3 upload completes
            await self.mailbox.send_evaluation_results({})
            _logger.info("S3 upload completed")
        # Unknown datasource type
        else:
            _logger.error(
                f"Unknown datasource type {type(self.datasource).__name__}"
                f" - expected NullSource or FileSystemIterableSource."
                " Unable to perform data transfer."
            )
            raise AlgorithmError(
                f"Unknown datasource type; got {type(self.datasource).__name__},"
                f" expected NullSource (for EHR)"
                f" or FileSystemIterableSource (for images)"
            )

        _logger.info("Data extraction protocol completed.")

    def _extract_algorithms(
        self,
    ) -> tuple[
        _PatientIDExchangeWorkerSide,
        _DownloadAlgoWorkerSide,
        _ImageSelectionWorkerSide,
        _S3UploadWorkerSide,
    ]:
        """Utility method to unpack and type the algorithm instances."""
        (
            patient_id_exchange_algo,
            download_info_algo,
            image_selection_algo,
            s3_upload_algo,
        ) = self.algorithm

        # Correct typing
        patient_id_exchange_algo = cast(
            _PatientIDExchangeWorkerSide, patient_id_exchange_algo
        )
        download_info_algo = cast(_DownloadAlgoWorkerSide, download_info_algo)
        image_selection_algo = cast(_ImageSelectionWorkerSide, image_selection_algo)
        s3_upload_algo = cast(_S3UploadWorkerSide, s3_upload_algo)

        return (
            patient_id_exchange_algo,
            download_info_algo,
            image_selection_algo,
            s3_upload_algo,
        )

    async def _download_ehr_data_for_all_patients(
        self,
        patient_ids: set[str],
        download_info_algo: _DownloadAlgoWorkerSide,
    ) -> dict[str, list[Path]]:
        """Download EHR data for all patients.

        Args:
            patient_ids: Set of patient IDs to process.
            download_info_algo: EHRPatientInfoDownloadAlgorithm worker side instance.

        Returns:
            Dictionary mapping patient ID to list of downloaded file paths.
        """
        _logger.info("Downloading EHR data for all patients")

        # Convert set to list, filtering out empty and whitespace-only strings
        patient_ids_list = [pid for pid in patient_ids if pid and pid.strip()]
        num_patient_ids = len(patient_ids_list)

        if num_patient_ids == 0:
            _logger.error("No valid patient IDs to process")
            raise AlgorithmError("No valid patient IDs provided")

        _logger.info(f"Processing {num_patient_ids} patient(s)")

        # Delegate enumeration and processing to the algorithm
        try:
            patient_files = download_info_algo.run(
                patient_ids=patient_ids_list,
                download_path=self.task_output_dir,
                run_document_download=True,
                run_json_dump=True,
            )
        except Exception as e:
            _logger.error(f"Error downloading EHR data: {e}")
            _logger.debug(f"Error downloading EHR data: {e}", exc_info=True)
            raise AlgorithmError(f"Failed to download EHR data: {e}") from e

        # Process results
        downloaded_count = 0
        patients_with_files = 0
        for _patient_id, files in patient_files.items():
            if files:
                downloaded_count += len(files)
                patients_with_files += 1

        if downloaded_count > 0:
            _logger.info(
                f"Downloaded {downloaded_count} file(s)"
                f" for {patients_with_files} of {num_patient_ids} patient(s)"
            )
        else:
            _logger.error("No files downloaded for any patient(s)")
            raise AlgorithmError("No files downloaded for any patient(s)")

        return patient_files

    async def _upload_ehr_data_to_s3(
        self,
        patient_files: dict[str, list[Path]],
        s3_upload_algo: _S3UploadWorkerSide,
    ) -> None:
        """Upload downloaded EHR data files to S3.

        Args:
            patient_files: Dictionary mapping patient ID to list of downloaded
                file paths.
            s3_upload_algo: S3UploadAlgorithm worker side instance.
        """
        _logger.info("Uploading downloaded EHR data files to S3")

        # Extract data owner username and dataset name for S3 key construction
        data_owner_username, dataset_name = (
            self._extract_dataset_owner_and_dataset_name()
        )

        uploaded_count = 0
        num_patients = len(patient_files)

        for i, (patient_id, files) in enumerate(patient_files.items(), start=1):
            if not patient_id:
                _logger.warning("Skipping empty patient ID")
                continue

            if not files:
                _logger.warning(
                    f"No files to upload for patient {patient_id}, skipping"
                )
                continue

            _logger.info(
                f"Uploading {len(files)} file(s) for patient {i} of"
                f" {num_patients}: {patient_id}"
            )

            try:
                files_uploaded = await self._upload_patient_ehr_files_to_s3(
                    patient_id=patient_id,
                    files=files,
                    s3_upload_algo=s3_upload_algo,
                    data_owner_username=data_owner_username,
                    dataset_name=dataset_name,
                )
                uploaded_count += files_uploaded
            except Exception as e:
                _logger.error(
                    f"Error uploading files for patient {patient_id}: {e}",
                )
                _logger.debug(
                    f"Error uploading files for patient {patient_id}: {e}",
                    exc_info=True,
                )
                _logger.warning("Continuing with next patient after error")
                continue

        if uploaded_count > 0:
            _logger.info(
                f"Uploaded {uploaded_count} file(s) to S3 for {num_patients} patient(s)"
            )
        else:
            _logger.error("No files uploaded to S3")
            raise AlgorithmError("No files uploaded to S3 for any patient(s)")

    async def _upload_patient_ehr_files_to_s3(
        self,
        patient_id: str,
        files: list[Path],
        s3_upload_algo: _S3UploadWorkerSide,
        data_owner_username: str,
        dataset_name: str,
    ) -> int:
        """Upload EHR data files for a single patient to S3.

        Args:
            patient_id: Patient ID to process.
            files: List of file paths to upload for this patient.
            s3_upload_algo: S3UploadAlgorithm worker side instance.
            data_owner_username: Data owner username for S3 key construction.
            dataset_name: Dataset name for S3 key construction.

        Returns:
            Number of files uploaded for this patient.

        Raises:
            Exception: If any error occurs during upload.
        """
        if not files:
            _logger.warning(f"No files provided for patient {patient_id}")
            return 0

        # Verify files exist and filter out any that don't
        existing_files: list[Path] = []
        for file_path in files:
            if not file_path.exists():
                _logger.warning(
                    f"File {file_path} does not exist for patient"
                    f" {patient_id}, skipping"
                )
                continue
            existing_files.append(file_path)

        if not existing_files:
            _logger.warning(f"No existing files found for patient {patient_id}")
            return 0

        # Determine patient directory for relative path calculation
        # Files are typically under task_output_dir / patient_id / ...
        patient_dir = self.task_output_dir / patient_id

        files_to_s3_keys: dict[Path, str] = {}
        for file_path in existing_files:
            # Construct S3 key:
            # <data_owner_username>/<dataset_name>/<patient_id>/<relative_path>
            # Calculate relative path from patient directory
            try:
                relative_path = file_path.relative_to(patient_dir)
            except ValueError:
                # If file is not under patient_dir, use just the filename
                # This handles edge cases where file structure might differ
                relative_path = Path(file_path.name)
                _logger.debug(
                    f"File {file_path} is not under patient directory {patient_dir}, "
                    f"using filename only for S3 key"
                )

            s3_key = (
                f"{data_owner_username}"
                f"/{dataset_name}"
                f"/{patient_id}"
                f"/{relative_path.as_posix()}"
            )
            files_to_s3_keys[file_path] = s3_key

        if files_to_s3_keys:
            _logger.info("Retrieving S3 upload URL")
            (
                s3_upload_url,
                s3_upload_fields,
            ) = await s3_upload_algo.get_S3_presigned_upload_url(self.mailbox)

            s3_upload_algo.run(
                files_to_upload=cast(dict[str | Path, str], files_to_s3_keys),
                presigned_url=s3_upload_url,
                presigned_fields=s3_upload_fields,
            )

            files_uploaded = len(files_to_s3_keys)
            _logger.info(f"Uploaded {files_uploaded} file(s) for patient {patient_id}")
            return files_uploaded

        return 0

    async def _upload_image_files_to_s3(
        self,
        files_to_upload: dict[str, list[Path]],
        s3_upload_algo: _S3UploadWorkerSide,
    ) -> None:
        """Upload image files to S3.

        Args:
            files_to_upload: Dictionary mapping patient ID to list of file
                paths.
            s3_upload_algo: S3UploadAlgorithm worker side instance.
        """
        if not files_to_upload:
            _logger.warning("No image files to upload to S3. Skipping upload.")
            return

        _logger.info("Uploading image files to S3")

        # Extract data owner username and dataset name for S3 key construction
        data_owner_username, dataset_name = (
            self._extract_dataset_owner_and_dataset_name()
        )

        uploaded_count = 0
        patient_upload_counts: dict[str, int] = defaultdict(int)

        # Process files iteratively in batches
        for patient_id, file_paths in files_to_upload.items():
            if not patient_id:
                _logger.warning("Skipping files with empty patient ID")
                continue

            if not file_paths:
                continue

            # Collect files for this patient
            files_to_s3_keys: dict[Path, str] = {}
            for file_path in file_paths:
                if not file_path.exists():
                    _logger.warning(f"File {file_path} does not exist, skipping.")
                    continue

                # Generate a short hash of the file path to ensure uniqueness when
                # multiple files have the same filename in different directories.
                #
                # Using 8 hex characters (32 bits) provides strong collision resistance
                # while keeping the hash reasonably short.
                #
                # 8 characters (32 bits): ~4.3 billion possibilities; ~50% collision
                # risk after ~65,536 items, more than enough for our use case (as
                # patient_id and file name would _also_ have to collide)
                #
                # We cannot use relative paths (as we do in the EHR data upload)
                # as we don't control where the image files actually are. Using
                # the full path in the key would also potentially be too long.
                path_str = str(file_path.as_posix())
                path_hash = hashlib.sha256(path_str.encode()).hexdigest()[:8]

                # Construct S3 key:
                # <data_owner_username>/<dataset_name>/<patient_id>/<hash>_<file_name>
                s3_key = (
                    f"{data_owner_username}"
                    f"/{dataset_name}"
                    f"/{patient_id}"
                    f"/{path_hash}_{file_path.name}"
                )
                files_to_s3_keys[file_path] = s3_key

            # Upload files for this patient
            if files_to_s3_keys:
                _logger.info("Retrieving S3 upload URL")
                (
                    s3_upload_url,
                    s3_upload_fields,
                ) = await s3_upload_algo.get_S3_presigned_upload_url(self.mailbox)
                s3_upload_algo.run(
                    files_to_upload=cast(dict[str | Path, str], files_to_s3_keys),
                    presigned_url=s3_upload_url,
                    presigned_fields=s3_upload_fields,
                )
                uploaded_count += len(files_to_s3_keys)
                patient_upload_counts[patient_id] += len(files_to_s3_keys)

        if uploaded_count > 0:
            _logger.info(
                f"Uploaded {uploaded_count} image file(s) to S3 for "
                f"{len(patient_upload_counts)} patient(s)"
            )
        else:
            _logger.info("No matching image files found to upload to S3")


class DataExtractionProtocolCharcoal(BaseProtocolFactory):
    """Protocol for running EHR Data Extraction for Charcoal."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "trial_name": fields.Str(allow_none=True),
    }

    def __init__(
        self,
        *,
        algorithm: Sequence[
            PatientIDExchangeAlgorithm
            | EHRPatientInfoDownloadAlgorithm
            | ImageSelectionAlgorithm
            | S3UploadAlgorithm
        ],
        trial_name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Data extraction protocol for Charcoal project.

        Args:
            algorithm: The sequence of algorithms to be used. The first algorithm
                must be PatientIDExchangeAlgorithm, which should be configured with
                patient_ids or patient_ids_file.
            trial_name: Name of the trial.
            **kwargs: Additional keyword arguments.
        """
        # TODO: [BIT-5727] Need to ensure that `run_on_new_data_only` is `False` when
        #       using this protocol, but think those args are only exposed at the
        #       _Worker/Modeller-level. Might have to just be explicit in templates
        #       using this protocol.
        super().__init__(algorithm=algorithm, **kwargs)

        self.trial_name = trial_name

    @classmethod
    def _validate_algorithm(cls, algorithm: BaseCompatibleAlgoFactory) -> None:
        """Validates the algorithms by ensuring they are compatible types.

        For this protocol these are:
            - PatientIDExchangeAlgorithm (must be first)
            - EHRPatientInfoDownloadAlgorithm
            - ImageSelectionAlgorithm
            - S3UploadAlgorithm
        """
        if algorithm.class_name not in (
            "bitfount.PatientIDExchangeAlgorithm",
            "bitfount.EHRPatientInfoDownloadAlgorithm",
            "bitfount.ImageSelectionAlgorithm",
            "bitfount.S3UploadAlgorithm",
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
                PatientIDExchangeAlgorithm
                | EHRPatientInfoDownloadAlgorithm
                | ImageSelectionAlgorithm
                | S3UploadAlgorithm
            ],
            self.algorithms,
        )

        modeller_algos: list[
            _PatientIDExchangeModellerSide
            | NoResultsModellerAlgorithm
            | _S3UploadModellerSide
        ] = []
        for i, algo in enumerate(algorithms):
            if i == 0:
                # First algorithm must be PatientIDExchangeAlgorithm
                if not isinstance(algo, PatientIDExchangeAlgorithm):
                    raise TypeError(
                        f"First algorithm must be PatientIDExchangeAlgorithm, "
                        f"got {type(algo).__name__} instead"
                    )
                # Patient IDs come from the algorithm's config, not from protocol
                modeller_algos.append(algo.modeller(context=context))
            elif hasattr(algo, "pretrained_file"):
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
        """Returns worker side of the DataExtractionProtocolCharcoal protocol.

        Args:
            mailbox: Worker mailbox instance to allow communication to the modeller.
            hub: `BitfountHub` object to use for communication with the hub.
            context: Optional. Run-time protocol context details for running.
            **kwargs: Additional keyword arguments.
        """
        algorithms = cast(
            Sequence[
                PatientIDExchangeAlgorithm
                | EHRPatientInfoDownloadAlgorithm
                | ImageSelectionAlgorithm
                | S3UploadAlgorithm
            ],
            self.algorithms,
        )

        # Verify first algorithm is PatientIDExchangeAlgorithm
        if not isinstance(algorithms[0], PatientIDExchangeAlgorithm):
            raise TypeError(
                f"First algorithm must be PatientIDExchangeAlgorithm, "
                f"got {type(algorithms[0]).__name__} instead"
            )

        task_results_dir = get_task_results_directory(context)
        _logger.info(
            f"Setting worker side output directory for {self.class_name}"
            f" to {str(task_results_dir)}"
        )

        return _WorkerSide(
            algorithm=[algo.worker(hub=hub, context=context) for algo in algorithms],
            mailbox=mailbox,
            output_dir=task_results_dir,
            trial_name=self.trial_name,
            **kwargs,
        )
