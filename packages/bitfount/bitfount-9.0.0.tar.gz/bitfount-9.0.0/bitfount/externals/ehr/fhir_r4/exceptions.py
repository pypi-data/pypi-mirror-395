"""Exceptions related to NextGen interactions."""

from __future__ import annotations

from typing import Optional

from bitfount.exceptions import BitfountError
from bitfount.externals.ehr.exceptions import (
    DataError,
    NoMatchingPatientError,
    NonSpecificPatientError,
    NoPatientIDError,
    QuotaExceeded,
)


class FHIRR4APIError(BitfountError):
    """Exception raised when interacting with FHIR R4 APIs."""

    pass


class NonSpecificFHIRR4PatientError(NonSpecificPatientError, FHIRR4APIError):
    """Exception raised when patient could not be narrowed to a single person."""

    pass


class NoMatchingFHIRR4PatientError(NoMatchingPatientError, FHIRR4APIError):
    """Exception raised when no patient matching filters is found."""

    pass


class NoFHIRR4PatientIDError(NoPatientIDError, FHIRR4APIError):
    """Exception raised when patient ID could not be extracted."""

    pass


class FHIRR4QuotaExceeded(QuotaExceeded, FHIRR4APIError):
    """Exception raised when we have exceeded any FHIR R4 call limit."""

    pass


class FHIRR4DataError(DataError, FHIRR4APIError):
    """Exception raised when we have exceeded any FHIR R4 call limit."""

    pass


class FHIRR4HTTPError(FHIRR4APIError):
    """Exception for HTTP errors from FHIR R4 API."""

    def __init__(
        self, status_code: int, message: str, response_content: Optional[str] = None
    ) -> None:
        self.status_code = status_code
        self.response_content = response_content
        super().__init__(f"HTTP {status_code}: {message}")


class FHIRR4AuthenticationError(FHIRR4HTTPError):
    """Exception for authentication/authorization errors (401, 403)."""

    pass


class FHIRR4RateLimitError(FHIRR4HTTPError):
    """Exception for rate limiting errors (429)."""

    pass


class FHIRR4ServerError(FHIRR4HTTPError):
    """Exception for server errors (5xx)."""

    pass


class FHIRR4OperationOutcomeError(FHIRR4APIError):
    """Exception for server side operation errors.

    These can be raised even when server returns a 200, accompanied by
    an OperationOutcome resource that details
    """
