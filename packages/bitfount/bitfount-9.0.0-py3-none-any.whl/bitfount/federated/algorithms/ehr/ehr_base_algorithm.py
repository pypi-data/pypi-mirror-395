"""Base class for EHR algorithms.

This module implements a base algorithm for any algos that need to set up
a NextGen and FHIR R4 sessions and queriers. It sets up EHR secrets as well
as required URL and other config in its initialise method.
It provides functionality to:
- Work with NextGen's FHIR, Enterprise, and SMART on FHIR APIs
- Work with generic FHIR R4 compatible systems
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Any, Optional, cast

from bitfount import config
from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.externals.ehr.fhir_r4.fhir_client import FHIRClient
from bitfount.externals.ehr.fhir_r4.querier import FHIRR4PatientQuerier
from bitfount.externals.ehr.nextgen.api import NextGenEnterpriseAPI, NextGenFHIRAPI
from bitfount.externals.ehr.nextgen.authentication import NextGenAuthSession
from bitfount.externals.ehr.nextgen.querier import (
    NextGenPatientQuerier,
)
from bitfount.externals.general.authentication import (
    ExternallyManagedJWT,
    ExternallyManagedJWTSession,
    GenericExternallyManagedJWTHandler,
)
from bitfount.federated.algorithms.base import (
    BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.types import EHRConfig
from bitfount.hub.api import (
    BitfountHub,
    SMARTOnFHIR,
)
from bitfount.hub.authentication_flow import (
    BitfountSession,
)
from bitfount.hub.helper import _create_bitfounthub

_logger = _get_federated_logger(__name__)


class QuerierType(Enum):
    """EHR Querier for use in algorithm."""

    NEXTGEN = "nextgen"
    FHIR_R4 = "fhir r4"


@dataclass(frozen=True)
class PatientDetails:
    """Patient identifying information."""

    bitfount_patient_id: str
    dob: str | date
    given_name: Optional[str] = None
    family_name: Optional[str] = None


class BaseEHRWorkerAlgorithm(BaseWorkerAlgorithm):
    """EHR Base worker algorithm for workers that need to access EHR."""

    def __init__(
        self,
        *,
        hub: Optional[BitfountHub] = None,
        session: Optional[BitfountSession] = None,
        **kwargs: Any,
    ) -> None:
        """Init method for EHR Base worker algorithm.

        Args:
            hub: BitfountHub object to use for communication with the hub (nextgen only)
            session: BitfountSession object for use with SMARTOnFHIR service.
                Will be created if not provided. (nextgen only)
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

        self.hub = hub
        self.session = session

        # These are set in the initialise method
        self.ehr_secrets: Optional[ExternallyManagedJWT] = None
        self.ehr_session: Optional[ExternallyManagedJWTSession] = None

    def initialise(
        self,
        *,
        datasource: BaseSource,
        task_id: str,
        data_splitter: Optional[DatasetSplitter] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        ehr_secrets: Optional[ExternallyManagedJWT] = None,
        ehr_config: Optional[EHRConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource and EHR secrets, and initialise EHR sessions."""
        if ehr_config is None:
            raise ValueError("ehr_config is missing.")
        self.ehr_config = ehr_config

        if ehr_secrets:
            self.ehr_secrets = ehr_secrets
            self.ehr_session = ExternallyManagedJWTSession(
                authentication_handler=GenericExternallyManagedJWTHandler(
                    jwt=self.ehr_secrets.jwt,
                    expires=self.ehr_secrets.expires,
                    get_token=self.ehr_secrets.get_token,
                )
            )

        self.initialise_data(datasource=datasource, data_splitter=data_splitter)

        if self.ehr_config.provider == "nextgen enterprise":
            self.querier_type = QuerierType.NEXTGEN
            self.fhir_url = (
                ehr_config.base_url or NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL
            )
            self.enterprise_url: Optional[str] = (
                ehr_config.enterprise_url
                or NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL
            )
            self.smart_on_fhir_url: Optional[str] = ehr_config.smart_on_fhir_url
            self.smart_on_fhir_resource_server_url: Optional[str] = (
                ehr_config.smart_on_fhir_resource_server_url
            )

            if self.hub is None and self.session is None:
                raise ValueError(
                    "One of hub or session must be provided for NextGen querier."
                )

            if self.hub is not None and self.session is not None:
                _logger.warning(
                    "Both hub and session were provided;"
                    " using provided session in preference to hub session."
                )
            elif self.hub is not None:
                self.session = self.hub.session

            if self.session is None:
                self.hub = _create_bitfounthub()
                self.session = self.hub.session

            if not self.session.authenticated:
                self.session.authenticate()

            self._get_nextgen_session()

            self.fhir_client: Optional[FHIRClient] = None

        elif self.ehr_config.provider and self.ehr_config.provider.endswith("r4"):
            if not self.ehr_config.base_url:
                raise ValueError("ehr_config.base_url must be provided.")
            self.querier_type = QuerierType.FHIR_R4
            self.fhir_url = self.ehr_config.base_url

            self.fhir_client = FHIRClient(self.fhir_url)

            self.session = None
            self.nextgen_session: Optional[NextGenAuthSession] = None
        else:
            raise ValueError(
                f"Invalid provider: {self.ehr_config.provider}. "
                f"Must be one of the allowed providers."
            )

    def _get_nextgen_session(self) -> None:
        """Get NextGenAuthSession."""
        # Get SMART on FHIR bearer token
        smart_auth = SMARTOnFHIR(
            session=self.session,
            smart_on_fhir_url=self.smart_on_fhir_url,
            resource_server_url=self.smart_on_fhir_resource_server_url,
        )
        self.nextgen_session = NextGenAuthSession(smart_auth)

    def _refresh_fhir_client_token(self) -> None:
        """Refresh the FHIR client access token."""
        if self.querier_type == QuerierType.FHIR_R4:
            if self.fhir_client is None:
                raise ValueError(
                    "Worker should not have been initialized without fhir_client"
                )

            if self.ehr_secrets is None:
                if config.settings.allow_no_ehr_secrets:
                    _logger.warning(
                        "No EHR secrets detected; no token could be retrieved"
                        " for the FHIR client."
                        " This is allowed by the BITFOUNT_ALLOW_NO_EHR_SECRETS flag."
                    )
                    return
                else:
                    raise ValueError(
                        "Worker should have been initialised"
                        " with ehr secrets before run"
                    )

            # If self.ehr_secrets is not None at this point then self.ehr_session is
            # not None. Reassure mypy of this.
            self.ehr_session = cast(ExternallyManagedJWTSession, self.ehr_session)
            handler: GenericExternallyManagedJWTHandler = (
                self.ehr_session.authentication_handler
            )
            token: str = handler.get_valid_token()
            self.fhir_client.authorization = f"Bearer {token}"

    def get_patient_querier(
        self, patient: PatientDetails
    ) -> NextGenPatientQuerier | FHIRR4PatientQuerier:
        """Get Patient Querier class for this patient."""
        patient_querier: NextGenPatientQuerier | FHIRR4PatientQuerier
        if self.querier_type == QuerierType.NEXTGEN:
            if self.nextgen_session is None:
                raise ValueError("Worker should not be run without nextgen_session.")
            patient_querier = NextGenPatientQuerier.from_patient_query(
                patient_dob=patient.dob,
                given_name=patient.given_name,
                family_name=patient.family_name,
                nextgen_session=self.nextgen_session,
            )
        elif self.querier_type == QuerierType.FHIR_R4:
            if self.fhir_client is None:
                raise ValueError(
                    "Worker should not have been initialized without fhir_client"
                )
            patient_querier = FHIRR4PatientQuerier.from_patient_query(
                patient_dob=patient.dob,
                given_name=patient.given_name,
                family_name=patient.family_name,
                fhir_client=self.fhir_client,
                ehr_provider=self.ehr_config.provider,
            )
        return patient_querier
