"""Algorithm for uploading documents to an AWS S3 bucket."""

from __future__ import annotations

import base64
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, cast

from boto3 import Session as BotoSession
import dateutil.parser
import dateutil.utils
from requests import HTTPError, RequestException

from bitfount.data.datasources.base_source import (
    BaseSource,
)
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.federated.algorithms.base import (
    BaseModellerAlgorithm,
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
)
from bitfount.federated.exceptions import AlgorithmError
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.transport.base_transport import AsyncHandler, Handler
from bitfount.federated.transport.message_service import (
    _BitfountMessage,
    _BitfountMessageType,
)
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import ProtocolContext
from bitfount.storage import _upload_file_to_s3
from bitfount.types import T_FIELDS_DICT, _S3PresignedPOSTFields, _S3PresignedPOSTURL
from bitfount.utils.aws_utils import AWSError, get_boto_session

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


logger = _get_federated_logger(__name__)

S3_UPLOAD_RETRY_ATTEMPTS = 3

DEFAULT_URL_EXPIRY_IN_SECONDS = 10800  # 3 hours
_5_MINUTE_TIMEDELTA = timedelta(minutes=5)


@dataclass
class _S3UploadURLDetails:
    """Container for details related to S3 upload POST URLs."""

    url: _S3PresignedPOSTURL
    fields: _S3PresignedPOSTFields

    def expires_at(self) -> datetime | None:
        """Returns the expiration time of the presigned S3 URL.

        If unable to parse the expiration time, it returns None.
        """
        try:
            # Policy information is stored as a base64 encoded string in the policy
            # field, and expiration is stored within that string
            policy_string: str = self.fields["policy"]
            policy_decoded: str = base64.b64decode(policy_string).decode("utf-8")
            # The deserialized policy is not actually a dict[str, str], but we only care
            # about "expiration" which _is_ a string
            policy_deserialized: dict[str, str] = json.loads(policy_decoded)
            expiration_time_str: str = policy_deserialized["expiration"]
            expiration_time: datetime = dateutil.parser.parse(expiration_time_str)
            # dateutil.parser.parse() might return a naive or aware datetime (though
            # the expiration given from AWS _should_ have a timezone); convert it
            # here for certainty
            expiration_time = dateutil.utils.default_tzinfo(
                expiration_time, tzinfo=timezone.utc
            )
            return expiration_time
        except Exception as e:
            logger.warning(
                f"Error parsing expiration time for the presigned S3 URL: {str(e)}"
            )
            return None

    def is_expired(self, buffer: timedelta = _5_MINUTE_TIMEDELTA) -> bool:
        """Check if the presigned S3 URL has expired.

        Checks if the expiration time is within the buffer time from now.

        Args:
            buffer: Buffer time in seconds to account for potential delays.
        """
        # If the expiration time is None, we could not extract the expiration time,
        # so we treat it as expired
        if (expires_at := self.expires_at()) is None:
            return True
        else:
            # datetime.now(timezone.utc) is an aware datetime
            current_time = datetime.now(timezone.utc)

            # Return true if the current time (buffer minutes in the future) is greater
            # than the expiration time
            return current_time + buffer > expires_at


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the S3Upload algorithm."""

    def __init__(
        self,
        s3_bucket: Optional[str],
        aws_region: Optional[str] = None,
        aws_profile: str = "default",
        **kwargs: Any,
    ):
        """Init method for the Modeller side of S3 Upload Algo.

        Args:
            s3_bucket: Name of S3 bucket to upload into.
            aws_region: AWS region in which the bucket resides.
            aws_profile: Name of AWS profile with which to generate the
              pre-signed POST.
            kwargs: Additional args to pass to the base class.
        """
        super().__init__(**kwargs)

        # Env var for AWS region will override argument
        if os.getenv("AWS_REGION"):
            aws_region = os.getenv("AWS_REGION")

        if any(param is None for param in [s3_bucket, aws_region]):
            null_params = []
            if s3_bucket is None:
                null_params.append("s3_bucket")
            if aws_region is None:
                null_params.append("aws_region")

            raise AlgorithmError(
                f"Required params not set on the S3UploadAlgorithm Modeller:"
                f" {null_params}"
            )

        self.s3_bucket: str = s3_bucket  # type:ignore[assignment]
        self.aws_profile: str = aws_profile
        self.aws_region: str = aws_region  # type:ignore[assignment]

        self._boto_session: Optional[BotoSession] = None
        self._s3_client: Optional[S3Client] = None

    @property
    def boto_session(self) -> BotoSession:
        """Return a boto3 session for the algorithm."""
        if self._boto_session is None:
            try:
                self._boto_session = get_boto_session(aws_profile=self.aws_profile)
            except AWSError as e:
                raise AlgorithmError(
                    "No credentials provided in environment variables,"
                    " and no aws_profile set."
                ) from e
        return self._boto_session

    @property
    def s3_client(self) -> S3Client:
        """Return a boto3 S3 client for the algorithm."""
        if self._s3_client is None:
            self._s3_client = self.boto_session.client(
                "s3", region_name=self.aws_region
            )
        return self._s3_client

    def run(
        self,
        subdirectory_for_upload: str,
        url_expiry_in_seconds: int = DEFAULT_URL_EXPIRY_IN_SECONDS,
    ) -> tuple[_S3PresignedPOSTURL, _S3PresignedPOSTFields]:
        """Provides a S3 presigned POST URL to send to the worker.

        Args:
            subdirectory_for_upload: Limit the generated presigned POST
              to only uploads within this bucket key.
            url_expiry_in_seconds: Amount of time the generated pre-signed
              POST url will last for before expiring.
        """
        return self._generate_presigned_post_url(
            subdirectory_for_upload, url_expiry_in_seconds
        )

    def initialise(
        self,
        *,
        task_id: str,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def _generate_presigned_post_url(
        self,
        subdirectory_for_upload: str,
        url_expiry_in_seconds: int = DEFAULT_URL_EXPIRY_IN_SECONDS,
    ) -> tuple[_S3PresignedPOSTURL, _S3PresignedPOSTFields]:
        """Provides a S3 presigned POST URL to send to the worker.

        Args:
            subdirectory_for_upload: Limit the generated presigned POST
              to only uploads within this bucket key.
            url_expiry_in_seconds: Amount of time the generated pre-signed
              POST url will last for before expiring.
        """
        # Remove any extra slashes
        subdirectory_for_upload = subdirectory_for_upload.strip("/")

        presigned_url = self.s3_client.generate_presigned_post(
            Bucket=self.s3_bucket,
            Key=f"{subdirectory_for_upload}/${{filename}}",  # limits any uploads to this subdirectory  #noqa: E501
            ExpiresIn=url_expiry_in_seconds,
            Conditions=[["starts-with", "$key", f"{subdirectory_for_upload}/"]],
        )

        logger.info(
            f"Modeller generated pre-signed POST for"
            f" worker for bucket: {self.s3_bucket}"
        )

        return presigned_url["url"], presigned_url["fields"]

    def register_s3_upload_url_request_handler(
        self,
        mailbox: _ModellerMailbox,
        subdirectory_for_upload: str,
        url_expiry_in_seconds: int = DEFAULT_URL_EXPIRY_IN_SECONDS,
    ) -> Handler:
        """Register a handler for WORKER_REQUEST messages to generate S3 upload URLs.

        Registers a handler that, when receiving a WORKER_REQUEST message, generates
        a presigned S3 POST URL and sends it to the workers as a MODELER_RESPONSE
        message.

        Args:
            mailbox: Modeller mailbox for registering the handler (and sending the
                responses).
            subdirectory_for_upload: Limit the generated presigned POST to only
                uploads within this bucket key.
            url_expiry_in_seconds: Amount of time the generated pre-signed POST url
                will last for before expiring.

        Returns:
            The registered (asynchronous) handler responding to WORKER_REQUEST messages.
        """
        return mailbox.register_handler(
            _BitfountMessageType.WORKER_REQUEST,
            self.get_s3_upload_url_request_handler(
                mailbox, subdirectory_for_upload, url_expiry_in_seconds
            ),
        )

    def get_s3_upload_url_request_handler(
        self,
        mailbox: _ModellerMailbox,
        subdirectory_for_upload: str,
        url_expiry_in_seconds: int = DEFAULT_URL_EXPIRY_IN_SECONDS,
    ) -> AsyncHandler:
        """Creates an asynchronous handler for worker requests for S3 upload URLs.

        Args:
            mailbox: Modeller mailbox for sending the response.
            subdirectory_for_upload: Limit the generated presigned POST to only
                uploads within this bucket key.
            url_expiry_in_seconds: Amount of time the generated pre-signed POST url
                will last for before expiring.

        Returns:
            An asynchronous handler for worker requests for S3 upload URLs. This
            handler takes in only a Bitfount message, generates a presigned POST URL,
            and sends it to the worker(s).
        """

        async def _s3_upload_url_request_handler(message: _BitfountMessage) -> None:
            """Asynchronous handler for worker requests for S3 upload URLs.

            Takes in only a Bitfount message, generates a presigned POST URL,
            and sends it to the worker(s).
            """
            logger.info(
                f"Received worker request (from {message.sender})"
                f" for an S3 presigned upload URL"
            )
            presigned_url, presigned_fields = self._generate_presigned_post_url(
                subdirectory_for_upload, url_expiry_in_seconds
            )
            await mailbox.send_S3_presigned_upload_url(presigned_url, presigned_fields)
            logger.info("S3 upload URL sent to Pods.")

        return _s3_upload_url_request_handler


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algorithm."""

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._s3_presigned_upload_url: Optional[_S3UploadURLDetails] = None

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
        files_to_upload: Mapping[str | Path, str],
        presigned_url: _S3PresignedPOSTURL,
        presigned_fields: _S3PresignedPOSTFields,
        retry_attempts: int = S3_UPLOAD_RETRY_ATTEMPTS,
    ) -> dict[str | Path, str]:
        """Uploads a list of files to a bucket.

        Args:
            files_to_upload: dict of local paths of files to be uploaded,
              to desired uploaded S3 key+filename for this file.
              If desired file name is an empty string, will upload as
              local file name.
            presigned_url: Pre-signed URL received from modeller.
            presigned_fields: Pre-signed fields for uploading file.
            retry_attempts: Number of retry attempts for a failed upload.

        Returns:
            A dictionary of file names that were successfully uploaded.
        """
        current_upload_dict = files_to_upload
        current_attempt = 1

        failed_files = {}
        successful_files = {}
        skipped_files = []

        subdirectory_for_upload = presigned_fields["key"].replace("/${filename}", "")

        while current_attempt <= retry_attempts and current_upload_dict:
            logger.info(
                f"Uploading files (attempt {current_attempt} of"
                f" {retry_attempts}):"
                f" uploading {len(current_upload_dict)} file(s)."
            )

            for file_name, upload_name in current_upload_dict.items():
                if not os.path.exists(file_name):
                    logger.warning(f"{file_name} does not exist, skipping.")
                    skipped_files.append(file_name)
                    continue

                if not upload_name:
                    upload_name = Path(file_name).name
                elif (
                    "." not in upload_name.split("/")[-1]
                ):  # a directory is provided instead of file name
                    upload_name = (Path(upload_name) / Path(file_name).name).as_posix()

                full_upload_path: str = (
                    Path(subdirectory_for_upload) / upload_name
                ).as_posix()

                upload_presigned_fields: _S3PresignedPOSTFields = cast(
                    _S3PresignedPOSTFields, presigned_fields.copy()
                )
                upload_presigned_fields["key"] = full_upload_path

                try:
                    _upload_file_to_s3(
                        upload_url=presigned_url,
                        presigned_fields=upload_presigned_fields,
                        file_path=file_name,
                    )
                except HTTPError as e:
                    logger.error(f"Encountered error uploading file {file_name}: {e}")
                    failed_files[file_name] = upload_name
                except RequestException as e:
                    logger.error(f"Encountered error uploading file {file_name}: {e}")
                    failed_files[file_name] = upload_name
                else:
                    logger.info(
                        f"Successfully uploaded file {file_name} to bucket,"
                        f" s3 key: {full_upload_path}"
                    )
                    successful_files[file_name] = full_upload_path

            current_upload_dict = failed_files
            failed_files = {}
            current_attempt += 1

        if current_upload_dict:
            logger.info(
                f"Failed to upload {len(current_upload_dict)} files"
                f" after maximum retries ({retry_attempts}):"
                f" {list(current_upload_dict.keys())}"
            )
        if skipped_files:
            logger.info(f"Skipped {len(skipped_files)} missing files: {skipped_files}")

        logger.info(f"Successfully uploaded {len(successful_files)} file(s).")

        return successful_files

    async def get_S3_presigned_upload_url(
        self, mailbox: _WorkerMailbox
    ) -> tuple[_S3PresignedPOSTURL, _S3PresignedPOSTFields]:
        """Get a presigned POST URL for uploading files to S3.

        If we already have one, and it is not expired, this will return that one.

        Otherwise, it will request a new one from the Modeller and wait for the
        response.

        Args:
            mailbox: The mailbox to send the request to the modeller if needed.

        Returns:
            A tuple containing the presigned URL and fields for uploading files.
        """
        s3_url_expired: bool = False
        if (no_s3_url := self._s3_presigned_upload_url is None) or (
            s3_url_expired := self._s3_presigned_upload_url.is_expired()
        ):
            if no_s3_url:
                logger.info("No S3 presigned URL found, requesting one from modeller.")
            if s3_url_expired:
                logger.info(
                    "S3 presigned URL expired, requesting new one from modeller."
                )

            # Request a new presigned URL from the modeller
            await mailbox.request_S3_presigned_upload_url()

            # Wait for the response
            (
                s3_upload_url,
                s3_upload_fields,
            ) = await mailbox.get_S3_presigned_upload_url()

            self._s3_presigned_upload_url = _S3UploadURLDetails(
                s3_upload_url, s3_upload_fields
            )
            logger.info("Received S3 presigned POST URL from modeller.")

            return s3_upload_url, s3_upload_fields
        else:
            return (
                self._s3_presigned_upload_url.url,
                self._s3_presigned_upload_url.fields,
            )


class S3UploadAlgorithm(BaseNonModelAlgorithmFactory[_ModellerSide, _WorkerSide]):
    """Algorithm for uploading files to S3.

    Args:
        datastructure: The data structure to use for the algorithm.
        s3_bucket: AWS S3 Bucket name to upload files into.
        aws_region: AWS region in which the bucket resides.
        aws_profile: Name of AWS profile with which to generate the
          pre-signed POST.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {}

    def __init__(
        self,
        datastructure: DataStructure,
        s3_bucket: Optional[str] = None,
        aws_region: Optional[str] = None,
        aws_profile: str = "default",
        **kwargs: Any,
    ) -> None:
        super().__init__(datastructure=datastructure, **kwargs)
        self.s3_bucket = s3_bucket
        self.aws_region = aws_region
        self.aws_profile = aws_profile

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _ModellerSide:
        """Modeller-side of the algorithm."""
        return _ModellerSide(
            s3_bucket=self.s3_bucket,
            aws_profile=self.aws_profile,
            aws_region=self.aws_region,
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
