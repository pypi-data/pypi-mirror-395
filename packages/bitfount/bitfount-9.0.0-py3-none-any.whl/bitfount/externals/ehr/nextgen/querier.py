"""Provides a high-level abstraction for extracting patient info from NextGen."""

from __future__ import annotations

from collections.abc import Container
from datetime import date, datetime
from functools import partial
import json
import logging
from pathlib import Path
from typing import Any, Optional

import pydash
from typing_extensions import (
    NotRequired,
    # We import this version of TypedDict rather than typing.TypedDict as in Python
    # <3.11 typing.TypedDict does not support generics in TypedDict.
    # TODO: [Python 3.11]
    TypedDict as ExtendedTypedDict,
)

from bitfount.externals.ehr.base_querier import (
    DEFAULT_DUMP_ELEMENTS,
    BaseEHRQuerier,
    CodeSystems,
)
from bitfount.externals.ehr.exceptions import GetPatientInfoError
from bitfount.externals.ehr.nextgen.api import (
    AppointmentTemporalState,
    NextGenEnterpriseAPI,
    NextGenFHIRAPI,
)
from bitfount.externals.ehr.nextgen.authentication import NextGenAuthSession
from bitfount.externals.ehr.nextgen.exceptions import (
    NextGenEnterpriseAPIError,
    NextGenFHIRAPIError,
)
from bitfount.externals.ehr.nextgen.types import (
    NextGenEnterpriseAppointmentsEntryJSON,
    NextGenEnterpriseChartJSON,
    NextGenEnterpriseDiagnosesEntryJSON,
    NextGenEnterpriseEncountersEntryJSON,
    NextGenEnterpriseMedicationsEntryJSON,
    NextGenEnterprisePersonJSON,
    NextGenEnterpriseProceduresEntryJSON,
    NextGenEnterpriseSocialHistoryEntryJSON,
    PatientCodeDetails,
    RetrievedPatientDetailsJSON,
)
from bitfount.externals.ehr.types import (
    ClinicalStatus,
    Condition,
    EHRAppointment,
    Observation,
    Procedure,
    ProcedureStatus,
)

_logger = logging.getLogger(__name__)


# DEV: Some keys are of a form that are invalid Python identifiers so they can't just
#      be supplied in the class-style TypedDict definitions. Instead we define them
#      here as a mixin.
_PatientJSONDumpPatientInfoInvalidKeys = ExtendedTypedDict(
    "_PatientJSONDumpPatientInfoInvalidKeys",
    {
        "social-history": NotRequired[list[NextGenEnterpriseSocialHistoryEntryJSON]],
    },
)


def recursively_remove_links(dictionary: Any) -> Any:
    """Remove any references to _links in the patient data from Nextgen."""
    if isinstance(dictionary, dict):
        return {
            key: recursively_remove_links(value)
            for key, value in dictionary.items()
            if key != "_links"
        }
    elif isinstance(dictionary, list):
        return [recursively_remove_links(item) for item in dictionary]
    else:
        return dictionary


class _PatientJSONDumpPatientInfo(
    NextGenEnterprisePersonJSON, _PatientJSONDumpPatientInfoInvalidKeys
):
    """Patient Info JSON dump object."""

    pass


class _NextGenPatientJSONDump(ExtendedTypedDict):
    """NextGen Data Transfer JSON dump object."""

    patientInfo: NotRequired[_PatientJSONDumpPatientInfo]
    appointments: NotRequired[list[NextGenEnterpriseAppointmentsEntryJSON]]
    chart: NotRequired[NextGenEnterpriseChartJSON]
    conditions: NotRequired[list[NextGenEnterpriseDiagnosesEntryJSON]]
    encounters: NotRequired[list[NextGenEnterpriseEncountersEntryJSON]]
    medications: NotRequired[list[NextGenEnterpriseMedicationsEntryJSON]]
    procedures: NotRequired[list[NextGenEnterpriseProceduresEntryJSON]]


class NextGenPatientQuerier(BaseEHRQuerier):
    """Provides query/data extraction methods for a given patient.

    This class is a higher-level abstraction than the direct API interactions,
    providing methods for extracting/munging data from the API responses.

    Args:
        patient_id: The patient ID this querier corresponds to.
        fhir_api: NextGenFHIRAPI instance.
        enterprise_api: NextGenEnterpriseAPI instance.
        fhir_patient_info: FHIR Patient Info with contact details.
    """

    def __init__(
        self,
        patient_id: str,
        *,
        fhir_api: NextGenFHIRAPI,
        enterprise_api: NextGenEnterpriseAPI,
        fhir_patient_info: Optional[RetrievedPatientDetailsJSON] = None,
    ) -> None:
        super().__init__(patient_id=patient_id)
        self.fhir_api = fhir_api
        self.enterprise_api = enterprise_api
        self.fhir_patient_info: Optional[RetrievedPatientDetailsJSON] = (
            fhir_patient_info
        )

    @classmethod
    def from_nextgen_session(
        cls,
        patient_id: str,
        nextgen_session: NextGenAuthSession,
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
    ) -> NextGenPatientQuerier:
        """Build a NextGenPatientQuerier from a NextGenAuthSession.

        Args:
            patient_id: The patient ID this querier will correspond to.
            nextgen_session: NextGenAuthSession for constructing API instances against.
            fhir_url: Optional, the FHIR API url to use.
            enterprise_url: Optional, the Enterprise API url to use.

        Returns:
            NextGenPatientQuerier for the target patient.
        """
        # TODO: [BIT-5621] This method is currently unable to identify the patient
        #   as it is missing dob and name. This method is currently unused.
        return cls(
            patient_id,
            fhir_api=NextGenFHIRAPI(nextgen_session, fhir_url),
            enterprise_api=NextGenEnterpriseAPI(nextgen_session, enterprise_url),
        )

    @classmethod
    def from_patient_query(
        cls,
        patient_dob: str | date,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        *,
        fhir_api: Optional[NextGenFHIRAPI] = None,
        enterprise_api: Optional[NextGenEnterpriseAPI] = None,
        nextgen_session: Optional[NextGenAuthSession] = None,
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
    ) -> NextGenPatientQuerier:
        """Build a NextGenPatientQuerier from patient query details.

        Args:
            patient_dob: Patient date of birth.
            given_name: Patient given name.
            family_name: Patient family name.
            fhir_api: Optional, NextGenFHIRAPI instance. If not provided,
                `nextgen_session` must be.
            enterprise_api: Optional, NextGenEnterpriseAPI instance. If not provided,
                `nextgen_session` must be.
            nextgen_session: Optional, NextGenAuthSession instance. Only needed if
                `fhir_api` or `enterprise_api` are not provided.
            fhir_url: Optional, FHIR API url. Only needed if `fhir_api` is not
                provided and a non-default URL is wanted.
            enterprise_url: Optional, Enterprise API url. Only needed if `fhir_api`
                is not provided and a non-default URL is wanted.

        Returns:
            NextGenPatientQuerier for the target patient.

        Raises:
            FromPatientQueryError: if patient ID could not be found (maybe because
                multiple patients match the criteria, or none do)
            ValueError: if unable to construct the API instances because session
                information was not provided.
        """
        fhir_api, enterprise_api = cls._use_or_build_apis(
            fhir_api=fhir_api,
            enterprise_api=enterprise_api,
            nextgen_session=nextgen_session,
            fhir_url=fhir_url,
            enterprise_url=enterprise_url,
        )

        patient_info = fhir_api.get_patient_info(patient_dob, given_name, family_name)
        if patient_info is None:
            raise FromPatientQueryError("Unable to find patient record")

        patient_id = patient_info["id"]

        return cls(
            patient_id,
            fhir_patient_info=patient_info,
            fhir_api=fhir_api,
            enterprise_api=enterprise_api,
        )

    @classmethod
    def from_mrn(
        cls,
        mrn: str,
        *,
        fhir_api: Optional[NextGenFHIRAPI] = None,
        enterprise_api: Optional[NextGenEnterpriseAPI] = None,
        nextgen_session: Optional[NextGenAuthSession] = None,
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
    ) -> NextGenPatientQuerier:
        """Build a NextGenPatientQuerier from MRN.

        Args:
            mrn: Medical Record Number
            fhir_api: Optional, NextGenFHIRAPI instance. If not provided,
                `nextgen_session` must be.
            enterprise_api: Optional, NextGenEnterpriseAPI instance. If not provided,
                `nextgen_session` must be.
            nextgen_session: Optional, NextGenAuthSession instance. Only needed if
                `fhir_api` or `enterprise_api` are not provided.
            fhir_url: Optional, FHIR API url. Only needed if `fhir_api` is not
                provided and a non-default URL is wanted.
            enterprise_url: Optional, Enterprise API url. Only needed if `fhir_api`
                is not provided and a non-default URL is wanted.

        Returns:
            NextGenPatientQuerier for the target patient.

        Raises:
            FromPatientQueryError: if patient ID could not be found (maybe because
                multiple patients match the MRN, or none do)
            ValueError: if unable to construct the API instances because session
                information was not provided.
        """
        fhir_api, enterprise_api = cls._use_or_build_apis(
            fhir_api=fhir_api,
            enterprise_api=enterprise_api,
            nextgen_session=nextgen_session,
            fhir_url=fhir_url,
            enterprise_url=enterprise_url,
        )

        patient_info = fhir_api.get_patient_info_by_mrn(mrn)
        if patient_info is None:
            raise FromPatientQueryError("Unable to find patient record by MRN")

        patient_id = patient_info["id"]

        return cls(
            patient_id,
            fhir_patient_info=patient_info,
            fhir_api=fhir_api,
            enterprise_api=enterprise_api,
        )

    @classmethod
    def _use_or_build_apis(
        cls,
        fhir_api: Optional[NextGenFHIRAPI] = None,
        enterprise_api: Optional[NextGenEnterpriseAPI] = None,
        nextgen_session: Optional[NextGenAuthSession] = None,
        fhir_url: str = NextGenFHIRAPI.DEFAULT_NEXT_GEN_FHIR_URL,
        enterprise_url: str = NextGenEnterpriseAPI.DEFAULT_NEXT_GEN_ENTERPRISE_URL,
    ) -> tuple[NextGenFHIRAPI, NextGenEnterpriseAPI]:
        """Handle multiple ways of providing/building FHIR/Enterprise API instances."""
        # Need session if no FHIR API instance
        if fhir_api is None and nextgen_session is None:
            raise ValueError(
                f"Got {fhir_api=} and {nextgen_session=}; one or other need to be set."
            )

        # Need session if no Enterprise API instance
        if enterprise_api is None and nextgen_session is None:
            raise ValueError(
                f"Got {enterprise_api=} and {nextgen_session=};"
                f" one or other need to be set."
            )

        # Should not get session if both API instances provided
        if (
            enterprise_api is not None
            and fhir_api is not None
            and nextgen_session is not None
        ):
            _logger.warning(
                "Got NextGenFHIRAPI and NextGenEnterpriseAPI instances,"
                " as well as a NextGenAuthSession instance;"
                " will use the API instances in preference"
                " to constructing them using the session instance."
            )

        # Build/use FHIR API instance
        fhir_api_: NextGenFHIRAPI
        if fhir_api is not None:
            fhir_api_ = fhir_api
        else:
            assert nextgen_session is not None  # nosec[assert_used] # Reason: see above checks # noqa: E501
            fhir_api_ = NextGenFHIRAPI(nextgen_session, fhir_url)

        # Build/use Enterprise API instance
        enterprise_api_: NextGenEnterpriseAPI
        if enterprise_api is not None:
            enterprise_api_ = enterprise_api
        else:
            assert nextgen_session is not None  # nosec[assert_used] # Reason: see above checks # noqa: E501
            enterprise_api_ = NextGenEnterpriseAPI(nextgen_session, enterprise_url)

        return fhir_api_, enterprise_api_

    def get_patient_conditions(
        self,
        statuses_filter: Optional[
            list[ClinicalStatus]
        ] = None,  # not yet implemented for nextgen
        code_types_filter: Optional[
            list[CodeSystems]
        ] = None,  # not yet implemented for nextgen
    ) -> list[Condition]:
        """Get conditions related to this patient.

        Returns:
            A list of Condition objects relevant for the patient, detailing its
            status and dates, sorted by condition onset date.

        Raises:
            NextGenGetPatientInfoError: If unable to retrieve patient condition
            information.
        """
        # Get patient conditions
        try:
            patient_conditions: Optional[list[NextGenEnterpriseDiagnosesEntryJSON]] = (
                self.enterprise_api.get_conditions_information(self.patient_id)
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve conditions information for patient: {str(e)}"
            )
            raise NextGenGetPatientInfoError(
                "Unable to retrieve conditions information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if patient_conditions is None:
            _logger.warning(
                "Patient conditions/diagnoses information could not be retrieved"
            )
            raise NextGenGetPatientInfoError(
                "Patient conditions/diagnoses information could not be retrieved"
            )

        # Check for matching Conditions codes
        list_of_conditions: list[Condition] = []
        for condition in patient_conditions:
            onset_date_raw = condition.get("onsetDate", None)
            if isinstance(onset_date_raw, str):
                onset_datetime = self._parse_timestamp(onset_date_raw, "condition")
            else:
                onset_datetime = None

            new_condition = Condition(
                onset_datetime=onset_datetime,
                code_system="icd" + condition.get("icdCodeSystem", "") or "",
                code_code=condition.get("icdCode"),
                code_display=condition.get("description"),
                code_text=condition.get("billingDescription"),
                clinical_status=condition.get("statusDescription"),
            )
            list_of_conditions.append(new_condition)

        return sorted(
            list_of_conditions,
            # Only really care about the date, not the time. This allows us to avoid
            # timezone issues.
            key=lambda cond: (
                cond.onset_datetime.date() if cond.onset_datetime else None
            )
            or date(1900, 1, 1),
        )

    def get_patient_procedures(
        self,
        statuses_filter: Optional[
            list[ProcedureStatus]
        ] = None,  # not yet implemented for nextgen
        code_types_filter: Optional[
            list[CodeSystems]
        ] = None,  # not yet implemented for nextgen
    ) -> list[Procedure]:
        """Get information of procedure codes this patient has.

        Returns:
            A list of Procedure objects relevant for the patient, detailing its
            status and dates, sorted by procedure date.

        Raises:
            NextGenGetPatientInfoError: If unable to retrieve patient procedures
            information.
        """
        try:
            patient_procedures: Optional[list[NextGenEnterpriseProceduresEntryJSON]] = (
                self.enterprise_api.get_procedures_information(self.patient_id)
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve procedures information for patient: {str(e)}"
            )
            raise NextGenGetPatientInfoError(
                "Unable to retrieve procedures information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if patient_procedures is None:
            _logger.warning("Patient procedures information could not be retrieved")
            raise NextGenGetPatientInfoError(
                "Patient procedures information could not be retrieved"
            )

        list_of_procedures: list[Procedure] = []
        for procedure in patient_procedures:
            procedure_date_raw = procedure.get("serviceDate", None)
            if isinstance(procedure_date_raw, str):
                procedure_datetime = self._parse_timestamp(
                    procedure_date_raw, "procedure"
                )
            else:
                procedure_datetime = None

            new_procedure = Procedure(
                performed_datetime=procedure_datetime,
                code_system="cpt4",  # nextgen only return cpt4 codes, no other systems
                code_code=procedure.get("cpt4Code"),
                code_display=procedure.get("serviceItemDescription"),
                code_text=procedure.get("serviceItemDescription"),
            )
            list_of_procedures.append(new_procedure)

        return sorted(
            list_of_procedures,
            # Only really care about the date, not the time. This allows us to avoid
            # timezone issues.
            key=lambda proc: (
                proc.performed_datetime.date() if proc.performed_datetime else None
            )
            or date(1900, 1, 1),
        )

    def get_patient_code_states(self) -> PatientCodeDetails:
        """Get information of Condition and Procedure codes this patient has.

        Sugar method that combines get_patient_condition_code_states() and
        get_patient_procedure_code_states() and returns a pre-constructed
        PatientCodeDetails container.

        Returns:
            A PatientCodeDetails instance detailing the presence or absence of the
            provided Condition and Procedure codes for the patient.
        """
        # Extract condition Code details for patient
        try:
            condition_code_states = self.get_patient_conditions()
        except NextGenGetPatientInfoError:
            # If error occurred, mark all entries as unknown, carry on
            condition_code_states = None

        # Extract CPT4 Code details for patient
        try:
            procedure_code_states = self.get_patient_procedures()
        except NextGenGetPatientInfoError:
            # If error occurred, mark all entries as unknown, carry on
            procedure_code_states = None

        # Construct code details object
        return PatientCodeDetails(
            condition_codes=condition_code_states, procedure_codes=procedure_code_states
        )

    def get_next_appointment(self) -> Optional[date]:
        """Get the next appointment date for the patient.

        Returns:
            The next appointment date for the patient from today, or None if they
            have no future appointment.

        Raises:
            NextGenGetPatientInfoError: If unable to retrieve patient information.
        """
        # Get list of upcoming appointments
        try:
            upcoming_appointments = self.enterprise_api.get_appointments_information(
                self.patient_id,
                appointment_temporal_state=AppointmentTemporalState.FUTURE,
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve upcoming appointments information for patient:"
                f" {str(e)}"
            )
            raise NextGenGetPatientInfoError(
                "Unable to retrieve upcoming appointments information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if upcoming_appointments is None:
            _logger.warning(
                "Patient upcoming appointments information could not be retrieved"
            )
            raise NextGenGetPatientInfoError(
                "Patient upcoming appointments information could not be retrieved"
            )

        # Extract next appointment information from the list
        next_appointment_datetime: Optional[datetime] = (
            pydash.chain(upcoming_appointments)
            # Only consider not cancelled appointments
            .filter(predicate={"isCancelled": False})
            # Pull out the appointmentDate field
            .pluck("appointmentDate")
            # Remove any that didn't have an appointmentDate field
            .filter_()
            # Convert from str to datetime instance
            .map_(
                partial(self._parse_timestamp, containing_entry_type_str="appointment")
            )
            # Remove any that couldn't be parsed
            .filter_()
            # Sort datetimes in ascending order
            .sort()
            # Return the first item (if any)
            .nth(0)
            # Extract the actual item
            .value()
        )

        if next_appointment_datetime is None:
            return None
        else:
            return next_appointment_datetime.date()

    def get_previous_appointment_details(
        self,
        include_maybe_attended: bool = True,  # not yet implemented for nextgen
    ) -> list[EHRAppointment]:
        """Get the details of previous appointments for the patient.

        Returns:
            The list of previous appointments for the patient, or an empty list if they
            have no previous appointments.

        Raises:
            NextGenGetPatientInfoError: If unable to retrieve patient information.
        """
        try:
            previous_appointments = self.enterprise_api.get_appointments_information(
                self.patient_id,
                appointment_temporal_state=AppointmentTemporalState.PAST,
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve past appointments information for patient:"
                f" {str(e)}"
            )
            raise NextGenGetPatientInfoError(
                "Unable to retrieve past appointments information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if previous_appointments is None:
            _logger.warning(
                "Patient past appointments information could not be retrieved"
            )
            raise NextGenGetPatientInfoError(
                "Patient past appointments information could not be retrieved"
            )

        ehr_appointments = []
        for appt in previous_appointments:
            appointment_date_obj: Optional[date] = None
            if isinstance(appt.get("appointmentDate"), str):
                appointment_date: Optional[datetime] = self._parse_timestamp(
                    appt["appointmentDate"], containing_entry_type_str="appointment"
                )
                if appointment_date is not None:
                    appointment_date_obj = appointment_date.date()

            ehr_appointments.append(
                EHRAppointment(
                    appointment_date=appointment_date_obj,
                    location_name=appt.get("locationName"),
                    event_name=appt.get("eventName"),
                )
            )

        return ehr_appointments

    def get_patient_latest_medical_practitioner(self) -> Optional[str]:
        """Retrieves the latest medical practitioner for the patient.

        This is the rendering provider for the patient's last encounter.

        Returns:
            The name of the latest medical practitioner for the patient, or None if
            there is no name listed on the latest encounter.

        Raises:
            NextGenGetPatientInfoError: If unable to retrieve patient encounter
            information.
        """
        try:
            encounters: Optional[list[NextGenEnterpriseEncountersEntryJSON]] = (
                self.enterprise_api.get_encounters(self.patient_id)
            )
        except Exception as e:
            # If an error occurred, raise an exception for this
            _logger.error(
                f"Unable to retrieve encounters information for patient: {str(e)}"
            )
            raise NextGenGetPatientInfoError(
                "Unable to retrieve encounters information for patient"
            ) from e

        # If None is returned, it's not just that there were no entries, it's that
        # there was an issue retrieving the list itself. Raise an error in this event.
        if encounters is None:
            _logger.warning("Patient encounters information could not be retrieved")
            raise NextGenGetPatientInfoError(
                "Patient encounters information could not be retrieved"
            )

        latest_practitioner: Optional[str] = (
            pydash.chain(encounters)
            # Convert from str to Optional[datetime] instance
            .map_(
                lambda x: pydash.update(
                    x,
                    "timestamp",
                    partial(
                        self._parse_timestamp, containing_entry_type_str="encounter"
                    ),
                )
            )
            # Remove any that didn't have a timestamp that could be parsed
            .filter_("timestamp")
            # Sort encounters by timestamp in descending order
            .sort_by("timestamp", reverse=True)
            .pluck("renderingProviderName")
            .nth(0)
            .value()
        )
        return latest_practitioner

    def download_all_documents(self, save_path: Path) -> list[Path]:
        """Download PDF documents for the current patient.

        Args:
            save_path: Documents path for the PDF documents to be saved.
        """
        all_success_doc_paths: list[Path] = []
        all_failed_doc_ids: list[str] = []

        for document_ids in self.enterprise_api.yield_document_infos(self.patient_id):
            success_documents, failed_documents = (
                self.enterprise_api.download_documents_batch(
                    save_path, self.patient_id, document_ids
                )
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

    def produce_json_dump(
        self, save_path: Path, elements_to_dump: Container[str] = DEFAULT_DUMP_ELEMENTS
    ) -> None:
        """Produce a JSON dump of patient information for the target patient.

        Saves the JSON dump out to file and the contents can be controlled by
        `elements_to_dump`.

        The following options are recognised:
            - "patientInfo": Contains:
                - `/persons/{{personId}}`, `/persons/{{personId}}/address-histories`
                - `/persons/{{personId}}/ethnicities`
                - `/persons/{{personId}}/gender-identities`
                - `/persons/{{personId}}/races`
                - `/persons/{personId}/chart/social-history`
            - "appointments": `/appointments` for the target patient.
            - "chart": `/persons/{{personId}}/chart` (`$expand=SupportRoles`)
            - "conditions": `/persons/{{personId}}/chart/diagnoses`
            - "encounters": `/persons/{{personId}}/chart/encounters`
            - "medications": `/persons/{{personId}}/charts/medications`
            - "procedures": `/persons/{{personId}}/chart/procedures`

        Args:
            save_path: The file location to save the JSON dump to.
            elements_to_dump: Collection of elements to include in the dump.
                See above for what options can be included.
        """
        output_json: _NextGenPatientJSONDump = {}

        # patientInfo
        if "patientInfo" in elements_to_dump:
            if patient_info_json := self.enterprise_api.get_person_information_for_dump(
                self.patient_id
            ):
                output_json["patientInfo"] = patient_info_json  # type: ignore[typeddict-item] # Reason: The two typeddict are subtyped so will be compatible # noqa: E501

                if social_history_json := self.enterprise_api.get_social_history(
                    self.patient_id
                ):
                    output_json["patientInfo"]["social-history"] = social_history_json
                else:
                    _logger.warning(
                        f"Failed to retrieve patient social history,"
                        f" got {social_history_json}"
                    )
            else:
                _logger.warning(
                    f"Failed to retrieve patient information, got {patient_info_json}"
                )

        # appointments
        if "appointments" in elements_to_dump:
            if (
                appointments_json
                := self.enterprise_api.get_appointments_information_for_dump(
                    self.patient_id
                )
            ):
                output_json["appointments"] = appointments_json
            else:
                _logger.warning(
                    f"Failed to retrieve patient appointments information,"
                    f" got {appointments_json}"
                )

        # chart
        if "chart" in elements_to_dump:
            if chart_json := self.enterprise_api.get_patient_chart_for_dump(
                self.patient_id
            ):
                output_json["chart"] = chart_json
            else:
                _logger.warning(
                    f"Failed to retrieve patient chart information, got {chart_json}"
                )

        # conditions
        if "conditions" in elements_to_dump:
            if (
                conditions_json
                := self.enterprise_api.get_conditions_information_for_dump(
                    self.patient_id
                )
            ):
                output_json["conditions"] = conditions_json
            else:
                _logger.warning(
                    f"Failed to retrieve patient conditions information,"
                    f" got {conditions_json}"
                )

        # encounters
        if "encounters" in elements_to_dump:
            if encounters_json := self.enterprise_api.get_encounters_for_dump(
                self.patient_id
            ):
                output_json["encounters"] = encounters_json
            else:
                _logger.warning(
                    f"Failed to retrieve patient encounters information,"
                    f" got {encounters_json}"
                )

        # medications
        if "medications" in elements_to_dump:
            if medications_json := self.enterprise_api.get_medications_for_dump(
                self.patient_id
            ):
                output_json["medications"] = medications_json
            else:
                _logger.warning(
                    f"Failed to retrieve patient medications information,"
                    f" got {medications_json}"
                )

        # procedures
        if "procedures" in elements_to_dump:
            if (
                procedures_json
                := self.enterprise_api.get_procedures_information_for_dump(
                    self.patient_id
                )
            ):
                output_json["procedures"] = procedures_json
            else:
                _logger.warning(
                    f"Failed to retrieve patient procedures information,"
                    f" got {procedures_json}"
                )

        # Save out the generated JSON dump
        output_cleaned = recursively_remove_links(output_json)
        with open(save_path, "w") as f:
            json.dump(output_cleaned, f, indent=2)

    def get_visual_acuity(self) -> Optional[Observation]:
        """Get Visual Acuity observation for a patient."""
        # Unable to find a way for VA to be accessed from NextGen
        _logger.info("Visual Acuity not available with NextGen API.")
        return None


# DEV: These exceptions are here because they are explicitly tied to this class. If
#      they begin to be used externally they should be moved to a common exceptions.py.
class FromPatientQueryError(NextGenFHIRAPIError):
    """No patient was returned when constructing from query."""

    pass


# DEV: These exceptions are here because they are explicitly tied to this class. If
#      they begin to be used externally they should be moved to a common exceptions.py.
class NextGenGetPatientInfoError(GetPatientInfoError, NextGenEnterpriseAPIError):
    """Could not retrieve patient info."""

    pass
