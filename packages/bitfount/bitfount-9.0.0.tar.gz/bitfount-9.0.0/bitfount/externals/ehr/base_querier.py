"""Provides query/data extraction methods for a given patient.

This class is a higher-level abstraction than the direct API interactions,
providing methods for extracting/munging data from the API responses.
"""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Container
from datetime import date, datetime
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Optional

from dateutil.parser import ParserError, parse as dateutil_parse

if TYPE_CHECKING:
    from bitfount.externals.ehr.nextgen.types import (
        PatientCodeDetails,
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

DEFAULT_DUMP_ELEMENTS: frozenset[str] = frozenset(
    (
        "patientInfo",
        "appointments",
        "chart",
        "conditions",
        "encounters",
        "medications",
        "procedures",
    )
)


CodeSystems = Literal["icd10", "snomed", "cpt4"]


class BaseEHRQuerier:
    """Base Class for various EHR Queriers.

    Args:
        patient_id: The patient ID this querier corresponds to.
    """

    def __init__(
        self,
        patient_id: str,
    ) -> None:
        self.patient_id = patient_id

    @abstractmethod
    def get_patient_conditions(
        self,
        statuses_filter: Optional[list[ClinicalStatus]] = None,
        code_types_filter: Optional[list[CodeSystems]] = None,
    ) -> list[Condition]:
        """Get conditions related to this patient."""
        raise NotImplementedError

    @abstractmethod
    def get_patient_procedures(
        self,
        statuses_filter: Optional[list[ProcedureStatus]] = None,
        code_types_filter: Optional[list[CodeSystems]] = None,
    ) -> list[Procedure]:
        """Get information of procedure codes this patient has.

        Returns:
            A list of procedure codes relevant for the patient.
        """
        raise NotImplementedError

    @abstractmethod
    def get_patient_code_states(self) -> PatientCodeDetails:
        """Get information of Condition and Procedure codes this patient has.

        Sugar method that combines get_patient_condition_code_states() and
        get_patient_procedure_code_states() and returns a pre-constructed
        PatientCodeDetails container.

        Returns:
            A PatientCodeDetails instance detailing the presence or absence of the
            provided Condition and Procedure codes for the patient.
        """
        raise NotImplementedError

    @abstractmethod
    def get_next_appointment(self) -> Optional[date]:
        """Get the next appointment date for the patient.

        Returns:
            The next appointment date for the patient from today, or None if they
            have no future appointment.

        Raises:
            NextGenGetPatientInfoError: If unable to retrieve patient information.
        """
        raise NotImplementedError

    @abstractmethod
    def get_previous_appointment_details(
        self,
        include_maybe_attended: bool = True,
    ) -> list[EHRAppointment]:
        """Get the details of previous appointments for the patient.

        Returns:
            The list of previous appointments for the patient, or an empty list if they
            have no previous appointments.
        """
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @staticmethod
    def _parse_timestamp(
        datetime_str: str, containing_entry_type_str: str
    ) -> Optional[datetime]:
        """Parses the timestamp string from an encounter to a datetime object.

        Timestamp string may contain milliseconds or not, so we use a more lenient
        parser than tying it to a specific format.

        Args:
            datetime_str: The timestamp string to be parsed.
            containing_entry_type_str: Type of entry that contains the timestamp,
                e.g. "appointment" or "encounter".

        Returns:
            The parsed datetime object, or None if the parsing failed.
        """
        try:
            return dateutil_parse(datetime_str)
        except (ParserError, TypeError) as e:
            _logger.warning(
                f"Unable to parse '{datetime_str}'; error was '{str(e)}'."
                f" Ignoring {containing_entry_type_str}."
            )
            return None

    @abstractmethod
    def download_all_documents(self, save_path: Path) -> list[Path]:
        """Download PDF documents for the current patient.

        Args:
            save_path: Documents path for the PDF documents to be saved.
        """
        raise NotImplementedError

    @abstractmethod
    def produce_json_dump(
        self, save_path: Path, elements_to_dump: Container[str] = DEFAULT_DUMP_ELEMENTS
    ) -> None:
        """Produce a JSON dump of patient information for the target patient.

        Saves the JSON dump out to file and the contents can be controlled by
        `elements_to_dump`.

        The options that are recognised depends on the querier.

        Args:
            save_path: The file location to save the JSON dump to.
            elements_to_dump: Collection of elements to include in the dump.
                See above for what options can be included.
        """
        raise NotImplementedError

    @abstractmethod
    def get_visual_acuity(self) -> Optional[Observation]:
        """Get Visual Acuity observation for a patient.

        BCVA = Best Corrected Visual Acuity.
        """
        raise NotImplementedError
