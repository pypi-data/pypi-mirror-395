"""EHR types."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Final, Literal, Optional

from bitfount import config

DATE_STR_FORMAT: Final[str] = "%Y-%m-%d"
EHR_CACHE_TTL: Final[int] = config.settings.ehr_cache_ttl

# Status for conditions, see for definition:
#    https://www.hl7.org/fhir/R4/valueset-condition-clinical.html
ClinicalStatus = Literal[
    "active", "recurrence", "relapse", "inactive", "remission", "resolved"
]

# Statuses for procedures, see for definition:
#    http://hl7.org/fhir/ValueSet/event-status
ProcedureStatus = Literal[
    "preparation",
    "in-progress",
    "not-done",
    "on-hold",
    "stopped",
    "completed",
    "entered-in-error",
    "unknown",
]


@dataclass
class Observation:
    """Observation object from FHIR."""

    date: Optional[datetime]
    code_system: Optional[str]
    code_code: Optional[str]
    code_display: Optional[str]
    code_text: Optional[str]
    value: Optional[float]
    unit: Optional[str]


@dataclass
class Condition:
    """Dataclass to describe patient Condition."""

    onset_datetime: Optional[datetime]
    code_system: Optional[str]
    code_code: Optional[str]
    code_display: Optional[str]
    code_text: Optional[str]
    clinical_status: Optional[str]


@dataclass
class Procedure:
    """Dataclass to describe patient Procedure."""

    performed_datetime: Optional[datetime]
    code_system: Optional[str]
    code_code: Optional[str]
    code_display: Optional[str]
    code_text: Optional[str]


@dataclass
class EHRAppointment:
    """Class for Patient Appointment."""

    appointment_date: Optional[date]
    location_name: Optional[str]
    event_name: Optional[str]

    def format_for_csv(self) -> dict[str, str]:
        """Format into a readable dictionary for csv."""
        output = {}

        if self.appointment_date:
            output["Appointment Date"] = self.appointment_date.strftime(DATE_STR_FORMAT)
        if self.location_name:
            output["Location Name"] = self.location_name
        if self.event_name:
            output["Event Name"] = self.event_name

        return output
