"""Provides a high-level abstraction for extracting patient info from FHIR R4 APIs."""

from __future__ import annotations

import base64
from datetime import date, datetime
import hashlib
import json
import logging
from pathlib import Path
from typing import (
    Any,
    Container,
    Final,
    Iterable,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc
from fhirpy.base.exceptions import (
    InvalidResponse,
    MultipleResourcesFound,
    OperationOutcome,
    ResourceNotFound,
)
from fhirpy.base.utils import AttrDict
import pydash
from slugify import slugify
from typing_extensions import (
    NotRequired,
    # We import this version of TypedDict rather than typing.TypedDict as in Python
    # <3.11 typing.TypedDict does not support generics in TypedDict.
    # TODO: [Python 3.11]
    TypedDict as ExtendedTypedDict,
)

from bitfount.data.persistence.caching import (
    EncryptedDiskcacheFunctionCache,
    FunctionCache,
)
from bitfount.externals.ehr.base_querier import (
    DEFAULT_DUMP_ELEMENTS,
    BaseEHRQuerier,
    CodeSystems,
)
from bitfount.externals.ehr.exceptions import GetPatientInfoError
from bitfount.externals.ehr.fhir_r4.exceptions import (
    FHIRR4APIError,
    FHIRR4DataError,
    NoFHIRR4PatientIDError,
    NoMatchingFHIRR4PatientError,
    NonSpecificFHIRR4PatientError,
)
from bitfount.externals.ehr.fhir_r4.fhir_client import FHIRClient
from bitfount.externals.ehr.fhir_r4.types import (
    FHIRAppointment,
    FHIRCondition,
    FHIRPatient,
)
from bitfount.externals.ehr.nextgen.api import DocumentInfo
from bitfount.externals.ehr.nextgen.types import (
    PatientCodeDetails,
    RetrievedPatientDetailsJSON,
)
from bitfount.externals.ehr.types import (
    EHR_CACHE_TTL,
    ClinicalStatus,
    Condition,
    EHRAppointment,
    Observation,
    Procedure,
    ProcedureStatus,
)
from bitfount.federated.types import EHRProvider

_logger = logging.getLogger(__name__)

func_cache: FunctionCache = EncryptedDiskcacheFunctionCache()


ICD_10_SYSTEM_IDENTIFIER: Final[str] = "http://hl7.org/fhir/sid/icd-10-cm"
SNOMED_SYSTEM_IDENTIFIER: Final[str] = "http://snomed.info/sct"
CPT_4_SYSTEM_IDENTIFIER: Final[str] = "http://www.ama-assn.org/go/cpt"
LOINC_SYSTEM_IDENTIFIER: Final[str] = "http://loinc.org"

CODE_SYSTEM_TO_IDENTIFIER: dict[str, str] = {
    "icd10": ICD_10_SYSTEM_IDENTIFIER,
    "snomed": SNOMED_SYSTEM_IDENTIFIER,
    "cpt4": CPT_4_SYSTEM_IDENTIFIER,
    "loinc": LOINC_SYSTEM_IDENTIFIER,
}

# Add EHR Provider here to not try appointments endpoint
EHR_PROVIDER_WITHOUT_APPOINTMENTS: set[str] = {
    "nextech intellechartpro r4",
}


class _FHIRR4PatientJSONDump(ExtendedTypedDict):
    """FHIR R4 Data Transfer JSON dump object."""

    patientInfo: NotRequired[dict[str, Any]]
    appointments: NotRequired[list[dict[str, Any]]]
    conditions: NotRequired[list[dict[str, Any]]]
    encounters: NotRequired[list[dict[str, Any]]]
    medications: NotRequired[list[dict[str, Any]]]
    procedures: NotRequired[list[dict[str, Any]]]


def _get_token_hash(
    fhir_client: FHIRClient,
) -> str:
    """Get a hashed token to use as cache key."""
    token = fhir_client.authorization
    if token is None:
        return ""
    return hashlib.sha256(token.encode("UTF-8")).hexdigest()


@func_cache.memoize(
    # NOTE: EHR cache is only persisted for a single process run; restarting the
    #       app/SDK process will effectively clear the cache
    expire=EHR_CACHE_TTL,
    ignore=(0, "fhir_client"),
)
def _cached_search_resources(
    fhir_client: FHIRClient,
    resource_type: str,
    token_hash: str,
    search_params: Mapping[str, Union[str, Sequence[str]]],
) -> list[dict[str, Any]]:
    """Cached search for FHIR resources.

    Args:
        fhir_client: The FHIR client instance (ignored in cache key).
        resource_type: The type of FHIR resource to search for.
        token_hash: Hash of current token as cache key, cache will be
          invalidated when token is refreshed.
        search_params: JSON-serializable search parameters.

    Returns:
        List of serialized FHIR resources.
    """
    try:
        resources = (
            fhir_client.resources(resource_type).search(**search_params).fetch_all()
        )
    except (FHIRR4APIError, OperationOutcome):
        # the fhir_client would have handled the appropriate logging.
        return []

    return [dict(resource) for resource in resources]


@func_cache.memoize(
    # NOTE: EHR cache is only persisted for a single process run; restarting the
    #       app/SDK process will effectively clear the cache
    expire=EHR_CACHE_TTL,
    ignore=(0, "fhir_client"),
)
def _cached_get_resource(
    fhir_client: FHIRClient,
    resource_type: str,
    token_hash: str,
    search_params: dict[str, str],
) -> Optional[dict[str, Any]]:
    """Cached get for a single FHIR resource.

    Args:
        fhir_client: The FHIR client instance (ignored in cache key).
        resource_type: The type of FHIR resource to search for.
        token_hash: Hash of current token as cache key, cache will be
          invalidated when token is refreshed.
        search_params: JSON-serializable search parameters.

    Returns:
        Serialized FHIR resource or None if API or OperationOutcome error

    Raises:
        ResourceNotFound: If ResourceNotFound is raised by fhirpy.
    """
    try:
        resource = fhir_client.resources(resource_type).search(**search_params).get()
        return dict(resource) if resource else None
    except ResourceNotFound:
        _logger.info(f"No {resource_type} fount with given search params.")
        return None
    except MultipleResourcesFound:
        _logger.info(
            f"More than one {resource_type} found with given search params, "
            f"when not more than one was expected."
        )
        raise
    except (FHIRR4APIError, OperationOutcome):
        # the fhir_client would have handled the appropriate logging.
        return None


@func_cache.memoize(
    # NOTE: EHR cache is only persisted for a single process run; restarting the
    #       app/SDK process will effectively clear the cache
    expire=EHR_CACHE_TTL,
    ignore=(0, "fhir_client"),
)
def _cached_first_resource(
    fhir_client: FHIRClient,
    resource_type: str,
    token_hash: str,
    search_params: Mapping[str, Union[str, Sequence[str]]],
) -> Optional[dict[str, Any]]:
    """Cached first for a single FHIR resource.

    Args:
        fhir_client: The FHIR client instance (ignored in cache key).
        resource_type: The type of FHIR resource to search for.
        token_hash: Hash of current token as cache key, cache will be
          invalidated when token is refreshed.
        search_params: JSON-serializable search parameters.

    Returns:
        Serialized FHIR resource or None if not found.
    """
    try:
        resource = fhir_client.resources(resource_type).search(**search_params).first()
    except (FHIRR4APIError, OperationOutcome):
        # the fhir_client would have handled the appropriate logging.
        return None

    return dict(resource) if resource else None


class FHIRR4PatientQuerier(BaseEHRQuerier):
    """Provides query/data extraction methods for a given patient.

    This class is a higher-level abstraction than the direct API interactions,
    providing methods for extracting/munging data from the API responses.

    Args:
        patient_id: The patient ID this querier corresponds to.
        fhir_client: FHIRClient instance.
        fhir_patient_info: FHIR Patient Info with contact details.
        ehr_provider: The EHR provider eg. "nextech", "epic"
        patient_dict: Optional patient details. If we've created this class
          with from_patient_query, we'll store the obtained patient_dict
          for later reference.
    """

    def __init__(
        self,
        patient_id: str,
        *,
        fhir_client: FHIRClient,
        fhir_patient_info: Optional[RetrievedPatientDetailsJSON] = None,
        ehr_provider: Optional[str] = None,
        patient_dict: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(patient_id=patient_id)
        self.fhir_client = fhir_client
        self.fhir_patient_info: Optional[RetrievedPatientDetailsJSON] = (
            fhir_patient_info
        )
        self.ehr_provider = ehr_provider
        self.patient_dict = patient_dict

    @classmethod
    def from_patient_query(
        cls,
        patient_dob: str | date,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        *,
        fhir_client: FHIRClient,
        ehr_provider: Optional[EHRProvider] = None,
    ) -> FHIRR4PatientQuerier:
        """Build a FHIRR4PatientQuerier from patient query details.

        Args:
            patient_dob: Patient date of birth.
            given_name: Patient given name.
            family_name: Patient family name.
            fhir_client: FHIRClient instance
            ehr_provider: The EHR provider

        Returns:
            NextGenPatientQuerier for the target patient.

        Raises:
            NoMatchingFHIRR4PatientError: No patients matching the name/dob criteria
               could be found
            NonSpecificFHIRR4PatientError: Multiple patients match the criteria, could
               not determine the correct one
            NoFHIRR4PatientIDError: Patient matching the criteria was found, but no
               patient ID was associated
        """
        try:
            patient_dict = cls.get_patient_response_by_name(
                fhir_client, patient_dob, given_name, family_name
            )
            if patient_dict is None:
                fhir_patient = None
            else:
                fhir_patient = fhir_client.resource(FHIRPatient, **patient_dict)
        except MultipleResourcesFound as e:
            raise NonSpecificFHIRR4PatientError(
                "Multiple patients found based on name and dob"
            ) from e

        if fhir_patient is None:
            _logger.warning("Unable to find patient record based on name and dob")
            raise NoMatchingFHIRR4PatientError(
                "Unable to find patient record based on name and dob"
            )

        patient_id = fhir_patient.id

        if not patient_id:
            raise NoFHIRR4PatientIDError(
                "Found matching patient information but could not extract patient ID."
            )

        dob_string: Optional[str] = None
        if isinstance(patient_dob, str):
            dob_string = patient_dob
        elif isinstance(patient_dob, date):
            dob_string = patient_dob.strftime("%Y-%m-%d")

        patient_info = RetrievedPatientDetailsJSON(
            id=patient_id,
            given_name=given_name,
            family_name=family_name,
            date_of_birth=dob_string,
            gender=fhir_patient.gender,
            home_numbers=cls._get_phone_number_from_patient(fhir_patient, use="home"),
            cell_numbers=cls._get_phone_number_from_patient(fhir_patient, use="mobile"),
            emails=[
                tel.value for tel in fhir_patient.telecom or [] if tel.system == "email"
            ],
            mailing_address=cls._get_address_from_patient(fhir_patient),
            medical_record_number=cls._extract_mrn(fhir_patient),
        )

        return cls(
            patient_id,
            fhir_client=fhir_client,
            fhir_patient_info=patient_info,
            ehr_provider=ehr_provider,
            patient_dict=patient_dict,
        )

    @classmethod
    def from_mrn(
        cls,
        mrn: str,
        *,
        fhir_client: FHIRClient,
        ehr_provider: Optional[EHRProvider] = None,
    ) -> FHIRR4PatientQuerier:
        """Build a FHIRR4PatientQuerier from MRN.

        Args:
            mrn: Medical Record Number
            fhir_client: FHIRClient instance
            ehr_provider: The EHR provider

        Returns:
            FHIRR4PatientQuerier for the target patient.

        Raises:
            NoMatchingFHIRR4PatientError: No patient matching the MRN could be found
            NonSpecificFHIRR4PatientError: Multiple patients match the MRN
            NoFHIRR4PatientIDError: Patient matching the MRN was found, but no
               patient ID was associated
        """
        try:
            patient_dict = cls.get_patient_response_by_mrn(fhir_client, mrn)
            if patient_dict is None:
                fhir_patient = None
            else:
                fhir_patient = fhir_client.resource(FHIRPatient, **patient_dict)
        except MultipleResourcesFound as e:
            raise NonSpecificFHIRR4PatientError(
                "Multiple patients found based on MRN"
            ) from e

        if fhir_patient is None:
            _logger.warning("Unable to find patient record based on MRN")
            raise NoMatchingFHIRR4PatientError(
                "Unable to find patient record based on MRN"
            )

        patient_id = fhir_patient.id

        if not patient_id:
            raise NoFHIRR4PatientIDError(
                "Found matching patient information but could not extract patient ID."
            )

        # Extract name(s) from the patient object
        given_name, family_name = cls._extract_name_fields(fhir_patient)

        patient_info = RetrievedPatientDetailsJSON(
            id=patient_id,
            given_name=given_name,
            family_name=family_name,
            date_of_birth=(cls._extract_dob(fhir_patient)),
            gender=fhir_patient.gender,
            home_numbers=cls._get_phone_number_from_patient(fhir_patient, use="home"),
            cell_numbers=cls._get_phone_number_from_patient(fhir_patient, use="mobile"),
            emails=[
                tel.value for tel in fhir_patient.telecom or [] if tel.system == "email"
            ],
            mailing_address=cls._get_address_from_patient(fhir_patient),
            medical_record_number=cls._extract_mrn(fhir_patient),
        )

        return cls(
            patient_id,
            fhir_client=fhir_client,
            fhir_patient_info=patient_info,
            ehr_provider=ehr_provider,
            patient_dict=patient_dict,
        )

    @classmethod
    def get_patient_response_by_name(
        cls,
        fhir_client: FHIRClient,
        patient_dob: str | date,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """Get JSON response from /Patient endpoint given name and DOB."""
        # There also exists a Patient/$match operation in FHIR R4
        # Which exists for services that have an MPI (Master Patient Index)
        # However it's not a first class operation in most FHIR clients,
        # probably as most servers don't have an MPI.
        # So we'll use the Patient.where operation for now until we know how to identify
        # if $match is supported.
        if isinstance(patient_dob, str):
            patient_dob_str = patient_dob
        else:
            patient_dob_str = patient_dob.strftime("%Y-%m-%d")

        # Use cached search for patient lookup
        search_params = {}
        if given_name:
            search_params["name"] = given_name
        if family_name:
            search_params["family"] = family_name
        search_params["birthdate"] = patient_dob_str

        return cls._query_patient_endpoint(
            fhir_client=fhir_client, search_params=search_params
        )

    def get_patient_response_by_id(self) -> Optional[dict[str, Any]]:
        """Get JSON response from /Patient endpoint given a Patient ID."""
        search_params = {"id": self.patient_id}
        return self._query_patient_endpoint(
            fhir_client=self.fhir_client, search_params=search_params
        )

    @classmethod
    def get_patient_response_by_mrn(
        cls,
        fhir_client: FHIRClient,
        mrn: str,
    ) -> Optional[dict[str, Any]]:
        """Get JSON response from /Patient endpoint given an MRN.

        Args:
            fhir_client: FHIRClient instance
            mrn: Medical Record Number

        Returns:
            Patient resource dict if found, None otherwise
        """
        # Search by identifier - FHIR supports identifier search parameter
        # Format: identifier={system}|{value} or identifier={value}
        search_params = {"identifier": mrn}
        return cls._query_patient_endpoint(
            fhir_client=fhir_client, search_params=search_params
        )

    @classmethod
    def _query_patient_endpoint(
        cls, fhir_client: FHIRClient, search_params: dict[str, str]
    ) -> Optional[dict[str, Any]]:
        """Given a set of search params, return a raw Patient resource.

        This is a class method as it is used by from_patient_query
        before instantiation.
        """
        return _cached_get_resource(
            fhir_client=fhir_client,
            resource_type="Patient",
            token_hash=_get_token_hash(fhir_client),
            search_params=search_params,
        )

    @staticmethod
    def _get_phone_number_from_patient(patient: FHIRPatient, use: str) -> list[str]:
        """Extract phone number from FHIRPatient object."""
        # Refer to https://build.fhir.org/datatypes.html#ContactPoint
        # use values: home | work | temp | old | mobile
        # system values: phone | fax | email | pager | url | sms | other
        return [
            tel.value
            for tel in patient.telecom
            if tel.use == use and tel.system not in ("email", "url")
        ]

    @staticmethod
    def _get_address_from_patient(patient: FHIRPatient) -> Optional[str]:
        """Extract address from FHIRPatient object."""
        if not patient.address:
            return None

        # Refer to https://build.fhir.org/datatypes.html#Address
        address_object = patient.address[0]

        # It might already exist fully constructed
        if address_object.text:
            address_string: Optional[str] = address_object.text
            return address_string

        # If text is not available, build it from its parts.
        if not address_object.line:
            address_string = ""
        else:
            address_string = " ".join(address_object.line)

        for address_part in [
            getattr(address_object, "city", ""),
            getattr(address_object, "district", ""),
            getattr(address_object, "state", ""),
            getattr(address_object, "postalCode", ""),
        ]:
            if address_part:
                address_string += f" {address_part}"

        return address_string

    @staticmethod
    def _extract_name_fields(
        patient: FHIRPatient,
    ) -> tuple[Optional[str], Optional[str]]:
        """Extract name fields from FHIRPatient object.

        Args:
            patient: FHIRPatient object

        Returns:
            Tuple of (given_name, family_name)
        """
        if not patient.name:
            _logger.info("No name found in FHIR Patient entry.")
            return None, None

        if len(patient.name) > 1:
            # This may happen if there are nicknames and aliases
            # See HumanName:
            # https://www.hl7.org/fhir/R4/datatypes.html#HumanName
            _logger.info("Found more than 1 name, returning the first one.")

        name_entry = patient.name[0]
        given_name = None
        family_name = None

        if name_entry.given:
            # given is a list, take the first one (should be "first name")
            given_name = name_entry.given[0]
        if name_entry.family:
            family_name = name_entry.family

        return given_name, family_name

    @staticmethod
    def _extract_dob(patient: FHIRPatient) -> Optional[str]:
        """Extract date of birth from FHIRPatient object.

        Args:
            patient: FHIRPatient object

        Returns:
            Date of birth as string in YYYY-MM-DD format, or None if not found
        """
        birth_date = patient.birthDate
        if birth_date is None:
            _logger.info("No birth date found in FHIR Patient entry.")
            return None

        # birthDate can be a date or datetime object, or a string
        if isinstance(birth_date, str):
            return birth_date
        elif hasattr(birth_date, "strftime"):
            return cast(str, birth_date.strftime("%Y-%m-%d"))
        else:
            return str(birth_date)

    @staticmethod
    def _extract_mrn(patient_entry: FHIRPatient) -> Optional[str]:
        """Extract MRN from FHIRPatient object."""
        mrns = pydash.filter_(
            getattr(patient_entry, "identifier", []),
            {"type": {"text": "Medical Record Number"}},
        )

        if len(mrns) == 0:
            _logger.info("No MRN identifier found.")
            return None

        if len(mrns) > 1:
            _logger.info("Found more than one MRN, returning the first one found.")

        mrn_value: str = mrns[0].value
        return mrn_value

    def get_patient_conditions(
        self,
        statuses_filter: Optional[list[ClinicalStatus]] = None,
        code_types_filter: Optional[list[CodeSystems]] = None,
    ) -> list[Condition]:
        """Get conditions related to this patient.

        Args:
            statuses_filter: If provided, returns only conditions of that status
               e.g. ['active','recurrence']
            code_types_filter: If provided, returns only conditions with codes
               of a specific code system (ICD10, Snomed) e.g. ["icd10"]

        Returns:
            A list of Condition objects relevant for the patient, detailing its
            status and dates, sorted by condition onset date.

        Raises:
            FHIRR4GetPatientInfoError: If unable to retrieve patient condition
            information.
        """
        params = {}
        if statuses_filter:
            params["clinical_status"] = ",".join(statuses_filter)
        if code_types_filter:
            params["code"] = ",".join(
                CODE_SYSTEM_TO_IDENTIFIER[code_type] + "|"
                for code_type in code_types_filter
            )

        try:
            # Use cached search for conditions
            search_params = {"patient": self.patient_id}
            search_params.update(params)

            condition_dicts = _cached_search_resources(
                fhir_client=self.fhir_client,
                resource_type="Condition",
                token_hash=_get_token_hash(self.fhir_client),
                search_params=search_params,
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve conditions information for patient: {str(e)}"
            )
            raise FHIRR4GetPatientInfoError(
                "Unable to retrieve conditions information for patient"
            ) from e

        try:
            patient_conditions = [
                self.fhir_client.resource(FHIRCondition, **resource_dict)
                for resource_dict in condition_dicts
            ]
        except Exception as e:
            _logger.error(
                f"Unable to deserialise conditions information for patient: {str(e)}"
            )
            raise FHIRR4DataError(
                "Unable to deserialise conditions information for patient"
            ) from e

        # Extract all codes from each condition
        all_conditions: list[Condition] = []
        for condition in patient_conditions:
            onset_date_raw = getattr(condition, "onsetDateTime", None)
            if isinstance(onset_date_raw, str):
                onset_datetime = self._parse_timestamp(onset_date_raw, "condition")
            elif isinstance(onset_date_raw, datetime):
                onset_datetime = onset_date_raw.astimezone(tzutc())
            else:
                onset_datetime = None

            clinical_status = None
            clinical_status_raw = getattr(condition, "clinicalStatus", None)
            if clinical_status_raw:
                clinical_status_codings = getattr(clinical_status_raw, "coding", None)
                if clinical_status_codings:
                    clinical_status = getattr(clinical_status_codings[0], "code", None)

            code = getattr(condition, "code", None)
            if not code:
                continue

            codings = code.coding
            if not codings:
                continue

            # a condition can have multiple codes
            # likely to handle different systems of coding
            # We'll represent them as separate Condition
            for coding in codings:
                new_condition = Condition(
                    onset_datetime=onset_datetime,
                    code_system=getattr(coding, "system", None),
                    code_code=getattr(coding, "code", None),
                    code_display=getattr(coding, "display", None),
                    code_text=getattr(code, "text", None),
                    clinical_status=clinical_status,
                )
                all_conditions.append(new_condition)

        return sorted(
            all_conditions,
            # Only really care about the date, not the time. This allows us to avoid
            # timezone issues.
            key=lambda cond: (
                cond.onset_datetime.date() if cond.onset_datetime else None
            )
            or date(1900, 1, 1),
        )

    def get_patient_procedures(
        self,
        statuses_filter: Optional[list[ProcedureStatus]] = None,
        code_types_filter: Optional[list[CodeSystems]] = None,
    ) -> list[Procedure]:
        """Get information of procedure codes this patient has.

        Args:
            statuses_filter: If provided, returns only procedures of that status
               e.g. ['completed', 'in-progress']
            code_types_filter: If provided, returns only conditions with codes
               of a specific code system (CPT4, Snomed) e.g. ["cpt4", "snomed"]

        Returns:
            A list of Procedure objects relevant for the patient, detailing its
            status and dates, sorted by procedure date.

        Raises:
            FHIRR4GetPatientInfoError: If unable to retrieve patient procedures
            information.
        """
        params = {}
        if statuses_filter:
            params["status"] = ",".join(statuses_filter)
        if code_types_filter:
            params["code"] = ",".join(
                CODE_SYSTEM_TO_IDENTIFIER[code_type] + "|"
                for code_type in code_types_filter
            )

        try:
            # Use cached search for procedures
            search_params = {"patient": self.patient_id}
            search_params.update(params)

            procedure_dicts = _cached_search_resources(
                fhir_client=self.fhir_client,
                resource_type="Procedure",
                token_hash=_get_token_hash(self.fhir_client),
                search_params=search_params,
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve procedures information for patient: {str(e)}"
            )
            raise FHIRR4GetPatientInfoError(
                "Unable to retrieve procedures information for patient"
            ) from e

        try:
            patient_procedures = [
                self.fhir_client.resource("Procedure", **resource_dict)
                for resource_dict in procedure_dicts
            ]
        except Exception as e:
            _logger.error(
                f"Unable to deserialise procedures information for patient: {str(e)}"
            )
            raise FHIRR4DataError(
                "Unable to deserialise procedures information for patient"
            ) from e

        # Extract the codes from each procedure
        all_procedures: list[Procedure] = []
        for procedure in patient_procedures:
            performed_date_raw = getattr(procedure, "performedDateTime", None)
            if isinstance(performed_date_raw, str):
                performed_datetime = self._parse_timestamp(
                    performed_date_raw, "procedure"
                )
            elif isinstance(performed_date_raw, datetime):
                performed_datetime = performed_date_raw.astimezone(tzutc())
            else:
                performed_datetime = None

            code = getattr(procedure, "code", None)
            if not code:
                continue

            codings: list = code.coding
            if not codings:
                continue

            # a procedure can have multiple codes
            # likely to handle different systems of coding
            # We'll represent them as separate Procedure
            for coding in codings:
                new_procedure = Procedure(
                    performed_datetime=performed_datetime,
                    code_system=getattr(coding, "system", None),
                    code_code=getattr(coding, "code", None),
                    code_display=getattr(coding, "display", None),
                    code_text=getattr(code, "text", None),
                )
                all_procedures.append(new_procedure)

        return sorted(
            all_procedures,
            # Only really care about the date, not the time. This allows us to avoid
            # timezone issues.
            key=lambda proc: (
                proc.performed_datetime.date() if proc.performed_datetime else None
            )
            or date(1900, 1, 1),
        )

    def get_patient_code_states(self) -> PatientCodeDetails:
        """Get information of Conditions and Procedures codes this patient has.

        Sugar method that combines get_patient_condition_code_states() and
        get_patient_procedure_code_states() and returns a pre-constructed
        PatientCodeDetails container.

        Returns:
            A PatientCodeDetails instance detailing the presence or absence of the
            provided Conditions and Procedures codes for the patient.

        Raises:
            FHIRR4GetPatientInfoError: If unable to retrieve condition information.
        """
        try:
            condition_code_states = self.get_patient_conditions()
        except FHIRR4GetPatientInfoError:
            # If error occurred, mark all entries as unknown, carry on
            condition_code_states = None

        # Extract CPT4 Code details for patient
        try:
            procedure_code_states = self.get_patient_procedures()
        except FHIRR4GetPatientInfoError:
            # If error occurred, mark all entries as unknown, carry on
            procedure_code_states = None

        # Construct code details object
        return PatientCodeDetails(
            condition_codes=condition_code_states, procedure_codes=procedure_code_states
        )

    def get_next_appointment(self) -> Optional[date]:
        """Get the next appointment date for the patient.

        Falls back to encounters if appointments are not available or empty.

        Returns:
            The next appointment date for the patient from today, or None if they
            have no future appointment. Any cancelled or errored appointments
            are ignored.

        Raises:
            FHIRR4GetPatientInfoError: If unable to retrieve patient information.
        """
        if self.ehr_provider not in EHR_PROVIDER_WITHOUT_APPOINTMENTS:
            try:
                appointment_date = (
                    self._get_next_appointment_from_appointments_endpoint()
                )
                if appointment_date is not None:
                    return appointment_date
            except Exception as e:
                _logger.warning(
                    f"Failed to retrieve next appointment, trying encounters: {str(e)}"
                )
            else:
                _logger.info(
                    "Did not find a next appointment date, trying encounters endpoint."
                )

        # Fallback to encounters if appointments failed or returned None
        try:
            encounter_date = self._get_next_appointment_from_encounters_endpoint()
            return encounter_date
        except Exception as e:
            _logger.error(
                f"Unable to retrieve upcoming appointments/encounters"
                f" for patient: {str(e)}"
            )
            raise FHIRR4GetPatientInfoError(
                "Unable to retrieve upcoming appointments/encounters for patient"
            ) from e

    def _get_next_appointment_from_appointments_endpoint(self) -> Optional[date]:
        """Get next appointment from Appointment resources."""
        search_params = {
            "patient": self.patient_id,
            "date__gt": datetime.now().date().strftime("%Y-%m-%d"),
            "status__not": ["cancelled", "entered-in-error"],
            "_sort": "date",
        }

        appointment_dict = _cached_first_resource(
            fhir_client=self.fhir_client,
            resource_type="Appointment",
            token_hash=_get_token_hash(self.fhir_client),
            search_params=search_params,
        )

        if appointment_dict is None:
            return None

        next_appointment = self.fhir_client.resource(
            FHIRAppointment, **appointment_dict
        )
        appointment_date: Optional[datetime] = next_appointment.start

        if appointment_date is None:
            # start date may be None if status is proposed/waitlist/cancelled
            return None

        return appointment_date.date()

    def _get_next_appointment_from_encounters_endpoint(self) -> Optional[date]:
        """Get next appointment from Encounter resources."""
        # We use period.start instead of date, and different status values
        # planned | arrived | triaged | in-progress | onleave | finished | cancelled
        search_params = {
            "patient": self.patient_id,
            "date__gt": datetime.now().date().strftime("%Y-%m-%d"),
            "status__not": "cancelled",
            "_sort": "date",
        }
        encounter_dict = _cached_first_resource(
            fhir_client=self.fhir_client,
            resource_type="Encounter",
            token_hash=_get_token_hash(self.fhir_client),
            search_params=search_params,
        )

        if encounter_dict is None:
            return None

        # Extract the start date from the encounter period
        period = encounter_dict.get("period")
        if period and period.get("start"):
            next_encounter_date = self._parse_timestamp(period["start"], "encounter")
            if next_encounter_date:
                return next_encounter_date.date()

        return None

    def _get_previous_appointment_details(
        self,
        include_maybe_attended: bool = True,
    ) -> list[FHIRAppointment] | list[dict]:
        """Get the FHIRAppointment details of previous appointments.

        Falls back to encounters if appointments are not available or empty.

        Returns:
            The list of previous appointments for the patient, sorted
            chronologically, or an empty list if they have no
            previous appointments.

        Raises:
            FHIRR4GetPatientInfoError: If unable to retrieve patient information.
        """
        # First try to get appointments
        try:
            appointments = self._get_previous_appointments_from_appointments_endpoint(
                include_maybe_attended
            )
            if appointments:
                return appointments
        except Exception as e:
            _logger.warning(
                f"Failed to retrieve past appointments, trying encounters: {str(e)}"
            )
        else:
            _logger.info("Did not find any past appointment, trying encounters.")

        # Fallback to encounters if appointments failed or returned empty list
        try:
            appointments_from_encounters: list[dict] = (
                self._get_previous_appointments_from_encounters(include_maybe_attended)
            )
            return appointments_from_encounters
        except Exception as e:
            _logger.error(
                f"Unable to retrieve past appointments/encounters for patient: {str(e)}"
            )
            raise FHIRR4GetPatientInfoError(
                "Unable to retrieve past appointments/encounters for patient"
            ) from e

    def _get_previous_appointments_from_appointments_endpoint(
        self,
        include_maybe_attended: bool = True,
    ) -> list[FHIRAppointment]:
        """Get previous appointments from Appointment resources."""
        # Definitely attended: arrived | fulfilled | checked-in
        # Maybe attended: waitlist | booked | pending | proposed
        # Not attended: cancelled | entered-in-error | noshow

        if include_maybe_attended:
            excluded_status = ["cancelled", "entered-in-error", "noshow"]
        else:
            excluded_status = [
                "cancelled",
                "entered-in-error",
                "noshow",
                "waitlist",
                "booked",
                "pending",
                "proposed",
            ]

        # Use cached search for previous appointments
        search_params = {
            "patient": self.patient_id,
            "date__lt": datetime.now().date().strftime("%Y-%m-%d"),
            "status__not": excluded_status,
            "_sort": "date",
        }

        appointment_dicts = _cached_search_resources(
            fhir_client=self.fhir_client,
            resource_type="Appointment",
            token_hash=_get_token_hash(self.fhir_client),
            search_params=search_params,
        )

        # Creates FHIRAppointment object from dict
        previous_appointments: list[FHIRAppointment] = [
            self.fhir_client.resource(FHIRAppointment, **resource_dict)
            for resource_dict in appointment_dicts
        ]

        return previous_appointments

    def _get_previous_appointments_from_encounters(
        self,
        include_maybe_attended: bool = True,
    ) -> list[dict]:
        """Get previous appointments from Encounters."""
        # Definitely attended: arrived | finished
        # Maybe attended: planned | in-progress | triaged
        # Not attended: cancelled | onleave

        if include_maybe_attended:
            excluded_status = ["cancelled", "onleave"]
        else:
            excluded_status = [
                "cancelled",
                "onleave",
                "planned",
                "in-progress",
                "triaged",
            ]

        # Use cached search for previous encounters
        search_params = {
            "patient": self.patient_id,
            "date__lt": datetime.now().date().strftime("%Y-%m-%d"),
            "status__not": excluded_status,
            "_sort": "date",
        }

        encounter_dicts = _cached_search_resources(
            fhir_client=self.fhir_client,
            resource_type="Encounter",
            token_hash=_get_token_hash(self.fhir_client),
            search_params=search_params,
        )

        return encounter_dicts

    def get_previous_appointment_details(
        self,
        include_maybe_attended: bool = True,
    ) -> list[EHRAppointment]:
        """Get list of previous appointments for the patient.

        Returns:
            A list of EHRAppointment for the patient, sorted
            chronologically, or an empty list if they have no
            previous appointments.

        Raises:
            FHIRR4GetPatientInfoError: If unable to retrieve patient information.
        """
        previous_appointments_or_encounters: list[FHIRAppointment] | list[dict] = (
            self._get_previous_appointment_details(
                include_maybe_attended=include_maybe_attended
            )
        )

        appointments_list: list[EHRAppointment] = []
        for appt in previous_appointments_or_encounters:
            appointment_date: Optional[date] = None
            event_name = ""
            if isinstance(appt, FHIRAppointment):
                if getattr(appt, "start", None):
                    appointment_date = appt.start.date()
                event_name = getattr(appt, "description", "")
            elif isinstance(appt, dict):
                # if it was a dict, it was retrieve from Encounters
                if start := appt.get("period", {}).get("start", None):
                    if isinstance(start, str):
                        appointment_datetime = self._parse_timestamp(start, "encounter")
                    else:
                        appointment_datetime = start

                    if appointment_datetime is not None:
                        appointment_date = appointment_datetime.date()

                # We use the encounter type display as an event name, eg.
                # "type" : [{
                #     "coding" : [{
                #       "system" : "http://snomed.info/sct",
                #       "code" : "183807002",
                #       "display" : "Inpatient stay 9 days"
                #     }]
                #   }],
                if appt_type := appt.get("type"):
                    if coding := appt_type[0].get("coding"):
                        event_name = coding[0].get("display", "")

            appointments_list.append(
                EHRAppointment(
                    appointment_date=appointment_date,
                    location_name=None,
                    event_name=event_name,
                )
            )

        return appointments_list

    def get_patient_latest_medical_practitioner(self) -> Optional[str]:
        """Retrieves the latest medical practitioner for the patient.

        This is the rendering provider for the patient's last encounter.

        Returns:
            The name of the latest medical practitioner for the patient, or None if
            there is no name listed on the latest encounter.

        Raises:
            FHIRR4GetPatientInfoError: If unable to retrieve patient encounter
            information.
        """
        # This list of appointments is sorted chronologically
        previous_appointments: list[FHIRAppointment] | list[dict] = (
            self._get_previous_appointment_details()
        )

        # Iterate through list of appointment/encounter starting from latest
        #  to find a Practitioner
        # Practitioners will be found amongst list of participants of the appointment
        # and can be identified by the actor.reference "Practitioner/{practitioner-id}"
        # See https://build.fhir.org/appointment.html
        practitioner_id = None
        for appt in previous_appointments[::-1]:
            if isinstance(appt, FHIRAppointment):
                participants = getattr(appt, "participant", [])
                for participant in participants:
                    actor = getattr(participant, "actor", None)
                    if actor and (
                        practitioner := getattr(actor, "reference", "")
                    ).startswith("Practitioner"):
                        practitioner_id = practitioner.split("/")[1]
                        break
            elif isinstance(appt, dict):
                participants = appt.get("participant", [])
                for participant in participants:
                    individual = participant.get("individual")
                    if individual and (
                        practitioner := individual.get("reference", "")
                    ).startswith("Practitioner"):
                        practitioner_id = practitioner.split("/")[1]
                        break

            if practitioner_id is not None:
                break

        if practitioner_id is None:
            # We were unable to find any Practitioner records in previous appointments
            return None

        try:
            # Use cached search for practitioner
            search_params = {"_id": practitioner_id}

            practitioner_dict = _cached_first_resource(
                fhir_client=self.fhir_client,
                resource_type="Practitioner",
                token_hash=_get_token_hash(self.fhir_client),
                search_params=search_params,
            )

            if practitioner_dict is None:
                result = None
            else:
                result = self.fhir_client.resource("Practitioner", **practitioner_dict)

        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve latest medical practitioner for patient: {str(e)}"
            )
            raise FHIRR4GetPatientInfoError(
                "Unable to retrieve latest medical practitioner for patient"
            ) from e

        if result is None:
            # Could not find any Practitioners with this reference id
            return None

        if result.name:
            # result.name is a list of HumanName, we'll use the first one
            # https://build.fhir.org/datatypes.html#HumanName
            return self._format_practitioner_name(result.name[0])

        return None

    def _format_practitioner_name(self, practitioner_name: AttrDict) -> str:
        """Formats name of practioner by prefix-given-family name."""
        # See HumanName https://build.fhir.org/datatypes.html#HumanName
        name_parts = []

        if prefix := (practitioner_name.get("prefix") or [""])[0]:
            name_parts.append(prefix)

        if given := (practitioner_name.get("given") or [""])[0]:
            name_parts.append(given)

        if family := practitioner_name.get("family", ""):
            name_parts.append(family)

        return " ".join(name_parts)

    def get_document_infos(self) -> Iterable[list[DocumentInfo]]:
        """Yields document items related to this patient."""
        try:
            for document_ref_obj in iter(
                self.fhir_client.resources("DocumentReference").search(
                    patient=self.patient_id,
                )
            ):
                document_infos = []
                # Note: one DocumentReference resource can contain more than one content
                for content in document_ref_obj.content:
                    if hasattr(content.attachment, "url"):
                        binary_id = content.attachment.url.split("/")[-1]
                        extension = content.attachment.contentType
                        if "/" in extension:
                            extension = extension.split("/")[-1]
                        document_date = document_ref_obj.get("date")

                        document_date_str = ""
                        if document_date:
                            document_date = self._parse_timestamp(
                                document_date, "document"
                            )
                            if isinstance(document_date, datetime):
                                document_date_str = document_date.strftime("%Y-%m-%d")

                        document_infos.append(
                            DocumentInfo(
                                document_id=binary_id,
                                document_date=document_date_str,
                                document_description=document_ref_obj.get(
                                    "type", {}
                                ).get("text"),
                                extension=extension,
                            )
                        )
                yield document_infos
        except InvalidResponse as e:
            _logger.warning(f"Unable to fetch document references: {e}")

    def download_all_documents(self, save_path: Path) -> list[Path]:
        """Download PDF documents for the current patient.

        Args:
            save_path: Documents path for the PDF documents to be saved.
        """
        all_success_doc_paths: list[Path] = []
        all_failed_doc_ids: list[str] = []

        for batch_document_infos in self.get_document_infos():
            success_documents, failed_documents = self.download_documents_batch(
                save_path, batch_document_infos
            )

            all_success_doc_paths += success_documents
            all_failed_doc_ids += failed_documents

        if all_failed_doc_ids:
            _logger.info(
                f"The following documents failed to download: {all_failed_doc_ids}"
            )
        if all_success_doc_paths:
            _logger.info(
                f"Successfully downloaded {len(all_success_doc_paths)} documents"
            )
        else:
            _logger.info("No documents downloaded for patient.")

        return all_success_doc_paths

    def download_documents_batch(
        self, save_path: Path, batch_document_infos: list[DocumentInfo]
    ) -> Tuple[list[Path], list[str]]:
        """Downloads a batch of documents.

        Returns:
            A tuple containing:
              - list of documents that downloaded successfully.
              - list of documents that could not be downloaded.
        """
        success_documents = []
        failed_documents = []
        for document_info in batch_document_infos:
            download_path: Optional[Path] = self._download_single_document(
                save_path=save_path, document_info=document_info
            )
            if download_path is not None:
                success_documents.append(download_path)
            else:
                failed_documents.append(document_info.document_id)

        return success_documents, failed_documents

    def _download_single_document(
        self, save_path: Path, document_info: DocumentInfo
    ) -> Optional[Path]:
        """Download a single document."""
        document_id = document_info.document_id
        try:
            # Note: we will not be caching these queries
            document_response = self.fhir_client.get("Binary", document_id)
        except (FHIRR4APIError, OperationOutcome) as e:
            _logger.warning(f"Failed to download {document_id}: {e}")
            return None

        encoded_data = document_response.get("data")

        if not encoded_data:
            _logger.warning(
                f"Failed to download {document_id}: got response {document_response}"
            )
            return None

        try:
            decoded_data = base64.b64decode(encoded_data)
        except Exception as e:
            _logger.warning(f"Encountered error decoding data: {e}")
            return None

        truncated_doc_id = document_id[:15]
        extension = document_info.extension or "txt"

        filename_elements = []
        if document_info.document_date:
            filename_elements.append(document_info.document_date)
        if document_info.document_description:
            filename_elements.append(document_info.document_description)
        file_name = slugify("_".join(filename_elements))

        if len(file_name) > 40:
            file_name = file_name[:40]

        if file_name:
            download_path: Path = (
                save_path / f"{file_name}_{truncated_doc_id}.{extension}"
            )
        else:
            download_path = save_path / f"{truncated_doc_id}.{extension}"

        with open(download_path, "wb") as f:
            f.write(decoded_data)
        return download_path

    def produce_json_dump(
        self, save_path: Path, elements_to_dump: Container[str] = DEFAULT_DUMP_ELEMENTS
    ) -> None:
        """Produce a JSON dump of patient information for the target patient.

        Saves the JSON dump out to file and the contents can be controlled by
        `elements_to_dump`.

        The following options are recognised:
            - "patientInfo": /Patient
            - "appointments": `/Appointment` (not always available)
            - "conditions": `/Conditions`
            - "encounters": `/Encounters`
            - "medications": `/MedicationRequest`
            - "procedures": `/Procedures`

        Args:
            save_path: The file location to save the JSON dump to.
            elements_to_dump: Collection of elements to include in the dump.
                See above for what options can be included.
        """

        output_json: _FHIRR4PatientJSONDump = {}

        # patientInfo
        if "patientInfo" in elements_to_dump:
            if self.patient_dict:
                # Already populated when instantiated, no need to call /Patient endpoint
                output_json["patientInfo"] = self.patient_dict
            else:
                patient_info_json = self.get_patient_response_by_id()
                if patient_info_json is not None:
                    output_json["patientInfo"] = patient_info_json
                else:
                    _logger.warning(
                        f"Failed to retrieve patient information, "
                        f"got {patient_info_json}"
                    )

        # encounters
        if "encounters" in elements_to_dump:
            # We want to get all encounters for the patient
            # However some providers do not like when no filters are included
            # in the query. Hence, here we set a wide boundary of -30 years
            # to +10 years from today.
            encounter_search_params = {
                "patient": self.patient_id,
                "date__gt": (datetime.now() - relativedelta(years=30))
                .date()
                .strftime("%Y-%m-%d"),
                "date__lt": (datetime.now() + relativedelta(years=10))
                .date()
                .strftime("%Y-%m-%d"),
                "_sort": "date",
            }
            encounter_dicts = _cached_search_resources(
                fhir_client=self.fhir_client,
                resource_type="Encounter",
                token_hash=_get_token_hash(self.fhir_client),
                search_params=encounter_search_params,
            )
            if encounter_dicts:
                output_json["encounters"] = encounter_dicts
            else:
                _logger.warning("Failed to retrieve patient encounters information")

        # appointments
        if "appointments" in elements_to_dump:
            # We want to get all appointments for the patient
            # However some providers do not like when no filters are included
            # in the query. Hence, here we set a wide boundary of -30 years
            # to +10 years from today.
            appts_search_params = {
                "patient": self.patient_id,
                "date__gt": (datetime.now() - relativedelta(years=30))
                .date()
                .strftime("%Y-%m-%d"),
                "date__lt": (datetime.now() + relativedelta(years=10))
                .date()
                .strftime("%Y-%m-%d"),
                "_sort": "date",
            }
            appointment_dicts = _cached_search_resources(
                fhir_client=self.fhir_client,
                resource_type="Appointment",
                token_hash=_get_token_hash(self.fhir_client),
                search_params=appts_search_params,
            )
            if appointment_dicts:
                output_json["appointments"] = appointment_dicts
            else:
                _logger.warning("Failed to retrieve patient appointments information")

        # conditions
        if "conditions" in elements_to_dump:
            all_conditions = _cached_search_resources(
                fhir_client=self.fhir_client,
                resource_type="Condition",
                token_hash=_get_token_hash(self.fhir_client),
                search_params={"patient": self.patient_id},
            )  # it is possible that this may fail for some EHRs
            # due to the lack of search filters
            if all_conditions:
                output_json["conditions"] = all_conditions
            else:
                _logger.warning("Failed to retrieve patient conditions information")

        # procedures
        if "procedures" in elements_to_dump:
            all_procedures = _cached_search_resources(
                fhir_client=self.fhir_client,
                resource_type="Procedure",
                token_hash=_get_token_hash(self.fhir_client),
                search_params={"patient": self.patient_id},
            )
            if all_procedures:
                output_json["procedures"] = all_procedures
            else:
                _logger.warning("Failed to retrieve patient procedures information")

        # medications
        if "medications" in elements_to_dump:
            medication_req_search_params = {
                "patient": self.patient_id,
                "_sort": "date",
            }
            medication_req_dict = _cached_search_resources(
                fhir_client=self.fhir_client,
                resource_type="MedicationRequest",
                token_hash=_get_token_hash(self.fhir_client),
                search_params=medication_req_search_params,
            )
            if medication_req_dict:
                output_json["medications"] = medication_req_dict
            else:
                _logger.warning("Failed to retrieve patient medications information")

        # Save out the generated JSON dump
        with open(save_path, "w") as f:
            json.dump(output_json, f, indent=2)

    def get_visual_acuity(self) -> Optional[Observation]:
        """Get Visual Acuity observation for a patient."""
        loinc_bcva_codes = [
            CODE_SYSTEM_TO_IDENTIFIER["loinc"] + "|" + bcva_code
            for bcva_code in [
                "98498-9",
                "98499-7",  # VA (uncorrected)
                "65897-1",
                "65893-0",  # Best corrected VA
                "79877-7",
                "79876-9",  # Best corrected VA by ETDRS eye chart
                "79881-9",
                "79880-1",  # Best corrected VA by Snellen eye chart
                "98511-9",
                "98512-7",  # Far best corrected VA
                "98508-5",
                "98509-3",  # Near best corrected VA
            ]
        ]
        snomed_bcva_codes = [
            CODE_SYSTEM_TO_IDENTIFIER["snomed"] + "|" + bcva_code
            for bcva_code in [
                "363983007",  # Visual Acuity
                "397536007",  # Corrected VA
                "419775003",  # Best Corrected VA
                "397534005",  # Corrected VA (left)
                "397535006",  # Corrected VA (right)
            ]
        ]

        search_params = {
            "patient": self.patient_id,
            "code": ",".join(loinc_bcva_codes + snomed_bcva_codes),
            "_sort": "date",
        }

        try:
            observations = _cached_search_resources(
                fhir_client=self.fhir_client,
                resource_type="Observation",
                token_hash=_get_token_hash(self.fhir_client),
                search_params=search_params,
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve Observation information for patient"
                f" when getting BCVA: {str(e)}"
            )
            raise FHIRR4GetPatientInfoError(
                "Unable to retrieve Observation information for patient"
                " when getting BCVA"
            ) from e

        # observations are sorted by timestamp, we take the latest one
        if not observations:
            return None

        latest_obs = observations[-1]

        # obs.code is of the format: {'coding': [{'system': 'http://loinc.org',
        # 'code': '65893-0',
        # 'display': 'Best corrected visual acuity - right eye'}],
        # 'text': 'BCVA (OD)'}
        coding = latest_obs.get("code", {}).get("coding")
        if coding:
            code = coding[0]
        else:
            code = None

        effectiveDateTime = latest_obs.get("effectiveDateTime")
        if isinstance(effectiveDateTime, str):
            obs_date = self._parse_timestamp(effectiveDateTime, "observation")
        else:
            obs_date = None

        return Observation(
            date=obs_date,
            code_system=code.get("system") if code else None,
            code_code=code.get("code") if code else None,
            code_display=code.get("display") if code else None,
            code_text=latest_obs.get("code", {}).get("text"),
            value=latest_obs.get("valueQuantity", {}).get("value"),
            unit=latest_obs.get("valueQuantity", {}).get("unit"),
        )


# DEV: This exception is here because it is explicitly tied to this class. If
#      they begin to be used externally they should be moved to a common exceptions.py.
class FHIRR4GetPatientInfoError(GetPatientInfoError, FHIRR4APIError):
    """Could not retrieve patient info."""

    pass
