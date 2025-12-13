"""FHIR Client implementation."""

from __future__ import annotations

import json
import logging
from typing import (
    Any,
    Union,
)

from fhirpy import SyncFHIRClient
from fhirpy.base.exceptions import (
    MultipleResourcesFound,
    ResourceNotFound,
)
from fhirpy.base.utils import AttrDict
import requests

from bitfount.externals.ehr.fhir_r4.exceptions import (
    FHIRR4AuthenticationError,
    FHIRR4HTTPError,
    FHIRR4OperationOutcomeError,
    FHIRR4RateLimitError,
    FHIRR4ServerError,
)

_logger = logging.getLogger(__name__)


class FHIRClient(SyncFHIRClient):
    """Implementation of FHIR Client for error handling."""

    def _do_request(
        self,
        method: str,
        path: str,
        data: Union[dict, None] = None,
        params: Union[dict, None] = None,
        returning_status: bool = False,
    ) -> Union[tuple[Any, int], Any]:
        """This method overrides the fhirpy _do_request method.

        This was implemented to handle more types of responses returned by
        servers that were not expected by the fhirpy method. Notably,
        results cannot be expected even when a 200 is received, and we
        would need to log the reasons in the OperationOutcome in order to
        diagnose any issues.
        """
        headers = self._build_request_headers()
        url = self._build_request_url(path, params)
        resp = requests.request(
            method, url, json=data, headers=headers, **self.requests_config
        )
        # Success responses (2xx)
        if 200 <= resp.status_code < 300:
            r_data = (
                json.loads(resp.content.decode(), object_hook=AttrDict)
                if resp.content
                else None
            )

            # It is possible that even with a 200 response, the resp content
            # contains OperationOutcome. When this happens even though there
            # are entries, the total is 0
            if isinstance(r_data, dict) and r_data.get("total") == 0:
                for entry in r_data.get("entry", []):
                    resource = entry.get("resource", {})
                    if resource.get("resourceType") == "OperationOutcome":
                        _logger.warning(
                            f"FHIR R4 OperationOutcome received: {resource}"
                        )
                        diagnostic_string = self._build_diagnostic_string(resource)
                        raise FHIRR4OperationOutcomeError(diagnostic_string)

            return (r_data, resp.status_code) if returning_status else r_data

        # Handle non-success status codes with proper logging and exceptions
        raw_data = resp.content.decode() if resp.content else ""

        # Log the error for debugging
        # NOTE: Do not log the full URL as the search params will contain PII
        _logger.error(f"FHIR API request failed: {method} -> HTTP {resp.status_code}. ")

        # Try to parse if it is an Operation Outcome
        try:
            parsed_data = json.loads(raw_data)
            if (
                isinstance(parsed_data, dict)
                and parsed_data.get("resourceType") == "OperationOutcome"
            ):
                diagnostic_string = self._build_diagnostic_string(parsed_data)
            else:
                diagnostic_string = ""
        except (KeyError, json.JSONDecodeError):
            # Not valid JSON or not an OperationOutcome
            parsed_data = None
            diagnostic_string = ""

        # Handle specific status codes
        if resp.status_code == 400:  # Bad Request
            _logger.warning(f"Bad request to FHIR API: {raw_data}")
            raise FHIRR4HTTPError(
                resp.status_code,
                f"Bad request - invalid parameters or malformed request"
                f" – {diagnostic_string}",
                raw_data,
            )

        elif resp.status_code == 401:  # Unauthorized
            _logger.error("Encounter 401: Authentication failed for FHIR API request")
            raise FHIRR4AuthenticationError(
                resp.status_code,
                f"Authentication required or invalid credentials – {diagnostic_string}",
                raw_data,
            )

        elif resp.status_code == 403:  # Forbidden
            _logger.error("Access forbidden for FHIR API request")
            raise FHIRR4AuthenticationError(
                resp.status_code,
                f"Access forbidden - insufficient permissions – {diagnostic_string}",
                raw_data,
            )

        elif resp.status_code in (404, 410):  # Not Found / Gone
            _logger.debug(f"Resource not found: {raw_data}")
            raise ResourceNotFound(raw_data)

        elif resp.status_code == 412:  # Precondition Failed
            _logger.warning(f"Multiple resources found: {raw_data}")
            raise MultipleResourcesFound(raw_data)

        elif resp.status_code == 422:  # Unprocessable Entity
            _logger.warning(f"Unprocessable entity in FHIR request: {raw_data}")
            raise FHIRR4HTTPError(
                resp.status_code,
                f"Unprocessable entity - request understood "
                f"but contains semantic errors – {diagnostic_string}",
                raw_data,
            )

        elif resp.status_code == 429:  # Too Many Requests
            _logger.warning("Rate limit exceeded for FHIR API")
            raise FHIRR4RateLimitError(
                resp.status_code,
                f"Rate limit exceeded - too many requests – {diagnostic_string}",
                raw_data,
            )

        elif 500 <= resp.status_code < 600:  # Server errors
            _logger.error(f"FHIR server error {resp.status_code}: {raw_data}")
            raise FHIRR4ServerError(
                resp.status_code,
                f"Server error - the FHIR server encountered an internal error"
                f" – {diagnostic_string}",
                raw_data,
            )

        if diagnostic_string:
            # We know there was an OperationOutcome resource
            raise FHIRR4OperationOutcomeError(diagnostic_string)
        else:
            # Generic fallback for unhandled status codes
            _logger.error(f"Unhandled FHIR API error with status {resp.status_code}")
            raise FHIRR4HTTPError(
                resp.status_code,
                f"Unexpected HTTP status code {resp.status_code}",
                raw_data,
            )

    def _build_diagnostic_string(self, resource: dict) -> str:
        if resource.get("resourceType") == "OperationOutcome":
            diagnostics = []
            for issue in resource.get("issue", []):
                if diagnostic := issue.get("diagnostics"):
                    diagnostics.append(diagnostic)
            return ", ".join(diagnostics)
        return ""
