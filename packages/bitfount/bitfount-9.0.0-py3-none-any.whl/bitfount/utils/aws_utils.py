"""Utility functions for interacting with AWS services."""

from __future__ import annotations

import logging
import os
from typing import Optional

import boto3
import botocore.exceptions

from bitfount.exceptions import BitfountError

_logger = logging.getLogger(__name__)


def get_boto_session(aws_profile: Optional[str] = "default") -> boto3.Session:
    """Creates a Boto3 session using provided AWS credentials.

    If AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION (and optionally
    AWS_SESSION_TOKEN) environment variables are set, these are used as priority.

    Otherwise, if aws_profile is provided, credentials will be loaded from the AWS
    credentials file and the provided profile is used. The default path to the AWS
    credentials can be overridden using the AWS_SHARED_CREDENTIALS_FILE environment
    variable.

    Args:
        aws_profile: The AWS profile to use for credentials if credentials are to be
            loaded from the credentials file. Defaults to "default".

    Returns:
        A Boto3 session with the provided AWS credentials.

    Raises:
        AWSError: If there is not enough information to construct a boto3 Session.
    """
    if (
        os.getenv("AWS_ACCESS_KEY_ID")
        and os.getenv("AWS_SECRET_ACCESS_KEY")
        and os.getenv("AWS_REGION")
    ):
        _logger.info("Using environment variables for AWS credentials.")
        # Uses environment variables if present
        session_kwargs = {
            "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
            "region_name": os.environ["AWS_REGION"],
        }

        # Add session token if present (for temporary credentials)
        if os.getenv("AWS_SESSION_TOKEN"):
            session_kwargs["aws_session_token"] = os.environ["AWS_SESSION_TOKEN"]

        session = boto3.Session(**session_kwargs)  # type:ignore[arg-type]
    elif aws_profile:
        credentials_file = os.getenv(
            "AWS_SHARED_CREDENTIALS_FILE", "~/.aws/credentials"
        )
        _logger.info(f"Using credentials from {credentials_file}.")
        session = boto3.Session(profile_name=aws_profile)
    else:
        raise AWSError(
            "No credentials provided in environment variables, and no aws_profile set."
        )

    return session


def check_aws_credentials_are_valid(
    boto3_session: Optional[boto3.Session] = None,
) -> None:
    """Checks if the provided AWS credentials are valid.

    Args:
        boto3_session: A Boto3 session with the provided AWS credentials. If
            None, a new session will be created using the default AWS credentials.

    Raises:
        AWSError: If the provided AWS credentials are invalid.
    """
    if boto3_session is None:
        boto3_session = get_boto_session()

    try:
        # Create AWS Security Token Service instance, as this allows us to test the
        # validity of the credentials
        sts = boto3_session.client("sts")
        sts.get_caller_identity()
    except botocore.exceptions.ClientError as e:
        _logger.error(f"Error checking AWS credentials: {e}")
        raise AWSError("Invalid AWS credentials") from e


class AWSError(BitfountError):
    """Exception related to AWS errors."""

    pass
