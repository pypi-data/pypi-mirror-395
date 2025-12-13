"""Generic EHR query algorithm for patient data access.

This module implements a generic algorithm for querying patient data from EHR systems.
It provides functionality to:
- Work with NextGen's FHIR, Enterprise, and SMART on FHIR APIs
- Work with generic FHIR R4 compatible systems
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, ClassVar, List, Literal, Optional

from nameparser import HumanName
import pandas as pd

from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.datastructure import DataStructure
from bitfount.externals.ehr.exceptions import (
    GetPatientInfoError,
    NoMatchingPatientError,
    NonSpecificPatientError,
    NoPatientIDError,
)
from bitfount.externals.ehr.nextgen.querier import (
    FromPatientQueryError,
)
from bitfount.externals.ehr.nextgen.types import (
    PatientCodeDetails,
    RetrievedPatientDetailsJSON,
)
from bitfount.externals.ehr.types import EHRAppointment, Observation
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ehr.ehr_base_algorithm import (
    BaseEHRWorkerAlgorithm,
    PatientDetails,
)
from bitfount.federated.algorithms.ophthalmology.dataframe_generation_extensions import (  # noqa: E501
    generate_bitfount_patient_id,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    _BITFOUNT_PATIENT_ID_KEY,
    ACQUISITION_DATE_COL,
    ADDRESS_COL,
    AGE_COL,
    CELL_NUMBER_COL,
    CPT4_COLUMN,
    DOB_COL,
    EMAIL_COL,
    FAMILY_NAME_COL,
    GIVEN_NAME_COL,
    HOME_NUMBER_COL,
    ICD10_COLUMN,
    LATERALITY_COL,
    LATEST_PRACTITIONER_NAME_COL,
    MRN_COL,
    NAME_COL,
    NEW_PATIENT_COL,
    NEXT_APPOINTMENT_COL,
    PREV_APPOINTMENTS_COL,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ProtocolContext
from bitfount.hub.api import (
    BitfountHub,
)
from bitfount.hub.authentication_flow import (
    BitfountSession,
)
from bitfount.types import T_FIELDS_DICT
from bitfount.utils.pandas_utils import (
    BITFOUNT_ID_COLUMNS,
    DOB_COLUMNS,
    FULL_NAME_COLUMNS,
    find_bitfount_id_column,
    find_dob_column,
    find_family_name_column,
    find_full_name_column,
    find_given_name_column,
)

_logger = _get_federated_logger(__name__)

GENDER_COL_EHR = "Sex (EHR)"
EHR_QUERY_COLUMNS = [
    _BITFOUNT_PATIENT_ID_KEY,
    DOB_COL,
    NAME_COL,
    GENDER_COL_EHR,
    HOME_NUMBER_COL,
    CELL_NUMBER_COL,
    EMAIL_COL,
    ADDRESS_COL,
    MRN_COL,
    GIVEN_NAME_COL,
    FAMILY_NAME_COL,
    NEXT_APPOINTMENT_COL,
    PREV_APPOINTMENTS_COL,
    NEW_PATIENT_COL,
    ORIGINAL_FILENAME_METADATA_COLUMN,
    ACQUISITION_DATE_COL,
    LATERALITY_COL,
    ICD10_COLUMN,
    CPT4_COLUMN,
    LATEST_PRACTITIONER_NAME_COL,
]

QuerierType = Literal["nextgen", "fhir_r4"]


class _ModellerSide(NoResultsModellerAlgorithm):
    """Modeller side of the EHR Patient Query Algorithm.

    This custom modeller-side class allows protocols to identify the EHR algorithm
    by checking its class_name attribute.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(log_message="Running EHR Patient Query Algorithm", **kwargs)
        # Override class_name to match the factory's class_name for protocol detection
        self.class_name = "bitfount.EHRPatientQueryAlgorithm"


@dataclass(frozen=True)
class PatientQueryResults:
    """Container indicating the results of the various queries for a given patient."""

    codes: PatientCodeDetails
    next_appointment: Optional[date]
    previous_appointments: Optional[List[EHRAppointment]]
    id: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    date_of_birth: Optional[str | date]
    gender: Optional[str]
    home_numbers: List[str]
    cell_numbers: List[str]
    emails: List[str]
    mailing_address: Optional[str]
    medical_record_number: Optional[str]
    latest_practitioner_name: Optional[str]
    visual_acuity: Optional[Observation] = None


class _WorkerSide(BaseEHRWorkerAlgorithm):
    """Worker side of the algorithm for querying EHR systems."""

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        """Initialize the worker-side algorithm.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

    def run(
        self,
        data: pd.DataFrame,
        get_appointments: bool = True,
        get_conditions_and_procedures: bool = True,
        get_practitioner: bool = False,
        get_visual_acuity: bool = False,
    ) -> dict[PatientDetails, PatientQueryResults]:
        """Query EHR APIs for matching patient information.

        Args:
            data: DataFrame containing patient information. Must have `NAME_COL`
                and `DOB_COL`.
            get_appointments:  When set to True, returns next and previous
              Appointment details for the patient (where available).
            get_conditions_and_procedures: When set to True, returns
              conditions and procedures details for the patient.
            get_practitioner:  When set to True, returns last practitioner
              details for the patient (where available).
            get_visual_acuity: When set to True, returns Visual Acuity
              for the patient (where available).

        Returns:
            Dict of {patient: query_results}. There will be an entry for every
            patient in `patients`, with an "empty" query results for those whose
            query results could not be retrieved (which is distinct from just having
            empty results).
        """
        self._refresh_fhir_client_token()
        patients = self.dataframe_to_patient_details(data)

        patient_query_results = self._run(
            patients,
            get_appointments=get_appointments,
            get_conditions_and_procedures=get_conditions_and_procedures,
            get_practitioner=get_practitioner,
            get_visual_acuity=get_visual_acuity,
        )

        _logger.info(
            f"Retrieved patient details from EHR"
            f" for {len(patient_query_results)}"
            f" of {len(patients)} patients"
        )

        # For any patient for whom results were not found, create an empty
        # PatientQueryDetails entry
        missed_patients = [p for p in patients if p not in patient_query_results]
        if missed_patients:
            _logger.warning(
                f"Could not retrieve patient details from EHR for Bitfount Patient IDs"
                f" {[p.bitfount_patient_id for p in missed_patients]}"
            )
        for missed_patient in missed_patients:
            patient_query_results[missed_patient] = PatientQueryResults(
                codes=PatientCodeDetails(
                    condition_codes=None,
                    procedure_codes=None,
                ),
                next_appointment=None,
                previous_appointments=None,
                id="",
                given_name=missed_patient.given_name,
                family_name=missed_patient.family_name,
                date_of_birth=missed_patient.dob,
                gender=None,
                home_numbers=[],
                cell_numbers=[],
                emails=[],
                mailing_address=None,
                medical_record_number=None,
                latest_practitioner_name=None,
                visual_acuity=None,
            )

        return patient_query_results

    def _run(
        self,
        patients: List[PatientDetails],
        get_appointments: bool,
        get_conditions_and_procedures: bool,
        get_practitioner: bool,
        get_visual_acuity: bool,
    ) -> dict[PatientDetails, PatientQueryResults]:
        """Run patient queries."""
        patient_query_results: dict[PatientDetails, PatientQueryResults] = {}

        # Process each patient
        for patient in patients:
            # Build patient querier for accessing all information
            try:
                patient_querier = self.get_patient_querier(patient)
            except (
                NoMatchingPatientError,
                NonSpecificPatientError,
                NoPatientIDError,
                FromPatientQueryError,
            ):
                _logger.warning(
                    f"Unable to retrieve EHR patient ID"
                    f" for Bitfount Patient ID {patient.bitfount_patient_id};"
                    f" skipping."
                )
                continue
            else:
                _logger.info(
                    f"Retrieved EHR Patient ID for Bitfount ID"
                    f" {patient.bitfount_patient_id}"
                )

            patient_code_details = PatientCodeDetails(
                condition_codes=None,
                procedure_codes=None,
            )
            # Get patient code states
            if get_conditions_and_procedures:
                try:
                    patient_code_details = patient_querier.get_patient_code_states()
                except GetPatientInfoError:
                    # This would have been logged
                    pass

            next_appointment: Optional[date] = None
            previous_appointments: Optional[list[EHRAppointment]] = None
            # Find next appointment for patient
            if get_appointments:
                try:
                    next_appointment = patient_querier.get_next_appointment()
                except GetPatientInfoError:
                    # This would have been logged
                    pass

                try:
                    previous_appointments = (
                        patient_querier.get_previous_appointment_details()
                    )
                except GetPatientInfoError:
                    # This would have been logged
                    pass

            latest_practitioner_name = None
            # Get latest practitioner name for patient
            if get_practitioner:
                try:
                    latest_practitioner_name = (
                        patient_querier.get_patient_latest_medical_practitioner()
                    )
                except GetPatientInfoError:
                    # This would have been logged
                    pass

            visual_acuity_obs: Optional[Observation] = None
            if get_visual_acuity:
                # Get visual acuity for patient
                visual_acuity_obs = patient_querier.get_visual_acuity()

            # Create entry for this patient
            fhir_patient_info: RetrievedPatientDetailsJSON | dict = (
                patient_querier.fhir_patient_info or {}
            )
            patient_query_results[patient] = PatientQueryResults(
                codes=patient_code_details,
                next_appointment=next_appointment,
                previous_appointments=previous_appointments,
                id=patient_querier.patient_id,
                given_name=patient.given_name,
                family_name=patient.family_name,
                date_of_birth=patient.dob,
                gender=fhir_patient_info.get("gender"),
                home_numbers=fhir_patient_info.get("home_numbers", []),
                cell_numbers=fhir_patient_info.get("cell_numbers", []),
                emails=fhir_patient_info.get("emails", []),
                mailing_address=fhir_patient_info.get("mailing_address"),
                medical_record_number=(fhir_patient_info.get("medical_record_number")),
                latest_practitioner_name=latest_practitioner_name,
                visual_acuity=visual_acuity_obs,
            )

        return patient_query_results

    @staticmethod
    def dataframe_to_patient_details(
        df: pd.DataFrame,
        bitfount_patient_id_column: str = _BITFOUNT_PATIENT_ID_KEY,
        dob_column: str = DOB_COL,
        name_column: Optional[str] = None,
        given_name_column: Optional[str] = None,
        family_name_column: Optional[str] = None,
    ) -> list[PatientDetails]:
        """Convert a pandas DataFrame into a list of PatientDetails objects.

        Args:
            df: DataFrame containing patient information. Must have
                `NAME_COL` and `DOB_COL`.
            bitfount_patient_id_column: Explicit column name for Bitfount patient ID.
            dob_column: Explicit column name for date of birth.
            name_column: Optional explicit column name for full name. Mutually
                exclusive with given_name_column and family_name_column.
            given_name_column: Optional explicit column name for given name.
            family_name_column: Optional explicit column name for family name.

        Returns:
            List of PatientDetails objects constructed from the DataFrame rows.

        Raises:
            ValueError: If required date of birth or Bitfount patient ID columns are
                missing, or if both name_column and given/family name columns are
                provided.
        """
        if df.empty:
            return []

        # Check for mutually exclusive name columns
        if name_column and (given_name_column or family_name_column):
            raise ValueError(
                "Cannot specify both name_column"
                " and given_name_column/family_name_column"
            )

        # Check if BitfountPatientID already exists
        bitfount_id_col: Optional[str]
        if bitfount_patient_id_column in df.columns:
            bitfount_id_col = bitfount_patient_id_column
        else:
            bitfount_id_col = find_bitfount_id_column(df)

        # Track if we created NAME_COL from given_name/family_name columns.
        # This is important because we need to ensure consistency: if the ID
        # was generated from a combined NAME_COL, we should extract patient
        # details from the same NAME_COL, not from the original separate columns.
        created_name_col_from_parts = False
        # Only generate BitfountPatientID if it doesn't exist
        if bitfount_id_col is None:
            # Add name and DOB columns
            found_name_col = find_full_name_column(df)
            found_dob_col = find_dob_column(df)

            # Validate DOB column exists before generating ID
            if found_dob_col is None:
                raise ValueError(
                    f"DataFrame must contain a Bitfount patient ID column or "
                    f"the columns needed to generate it."
                    f" Missing date of birth column. Expected one of: {DOB_COLUMNS}"
                    f" or explicitly provided column: {dob_column}"
                )

            # If no full name column but we have given_name/family_name, create one
            if found_name_col is None:
                found_given_name_col = find_given_name_column(df)
                found_family_name_col = find_family_name_column(df)
                if (
                    found_given_name_col is not None
                    and found_family_name_col is not None
                ):
                    # Create a full name column from given_name and family_name for
                    # generating BitfountPatientID
                    df[NAME_COL] = (
                        df[found_family_name_col].astype(str)
                        + ", "
                        + df[found_given_name_col].astype(str)
                    )
                    found_name_col = NAME_COL
                    created_name_col_from_parts = True
                else:
                    # We don't have a full name column and can't create one
                    raise ValueError(
                        f"DataFrame must contain a Bitfount patient ID column or "
                        f"the columns needed to generate it.Missing name column. "
                        f"Expected one of: {FULL_NAME_COLUMNS} or both given_name "
                        f"and family_name columns"
                    )

            df = generate_bitfount_patient_id(
                df,
                name_col=found_name_col,
                dob_col=found_dob_col,
            )

            if found_name_col is not None and found_name_col != NAME_COL:
                df = df.rename({found_name_col: NAME_COL}, axis=1)
            if found_dob_col is not None and found_dob_col != DOB_COL:
                df = df.rename({found_dob_col: DOB_COL}, axis=1)
            bitfount_id_col = _BITFOUNT_PATIENT_ID_KEY

        # Determine which columns to use for extracting patient details.
        # This section ensures we use the same source columns that were used for
        # ID generation to maintain consistency.
        dob_col: Optional[str]
        if dob_column in df.columns:
            dob_col = dob_column
        else:
            dob_col = find_dob_column(df)
        if dob_col is None:
            raise ValueError(
                f"DataFrame must contain a date of birth column."
                f" Expected one of: {DOB_COLUMNS}"
                f" or explicitly provided column: {dob_column}"
            )
        # Determine which name column(s) to use for patient detail extraction.
        # Priority: explicit name_column parameter > found full name column >
        #           created NAME_COL (if we created it from parts) > separate columns
        name_col: Optional[str] = (
            name_column
            if name_column in df.columns
            else (
                find_full_name_column(df)
                if not (given_name_column or family_name_column)
                else None
            )
        )
        # If we created NAME_COL from given_name/family_name columns, we must use it
        # for patient detail extraction to ensure consistency with ID generation.
        # Otherwise, we might extract names from the original separate columns which
        # could have different values (e.g., if they were modified or have different
        # formatting) than the combined NAME_COL used for ID generation.
        if created_name_col_from_parts and name_col is None:
            name_col = NAME_COL
        # Determine given_name column to use, but only if we're not using a full
        # name column. If we created NAME_COL from parts and are using it, we should
        # NOT use the original separate columns to avoid inconsistency.
        given_name_col: Optional[str] = (
            given_name_column
            if given_name_column in df.columns
            else (
                find_given_name_column(df)
                if not name_column
                and not (created_name_col_from_parts and name_col == NAME_COL)
                else None
            )
        )
        # Determine family_name column to use, but only if we're not using a full
        # name column. If we created NAME_COL from parts and are using it, we should
        # NOT use the original separate columns to avoid inconsistency.
        family_name_col: Optional[str] = (
            family_name_column
            if family_name_column in df.columns
            else (
                find_family_name_column(df)
                if not name_column
                and not (created_name_col_from_parts and name_col == NAME_COL)
                else None
            )
        )
        # Extract patient details from each row using the determined columns
        patients = []
        for _, row in df.iterrows():
            # Get date of birth value
            dob = row[dob_col]

            # Convert string to date if needed
            if isinstance(dob, str):
                try:
                    dob = pd.to_datetime(dob).date()
                except (ValueError, TypeError):
                    _logger.warning(f"Invalid date format for DOB: {dob}")
                    continue

            # Get Bitfount patient ID (required)
            bitfount_patient_id: str = row[bitfount_id_col]
            if pd.isna(bitfount_patient_id):
                _logger.warning("Missing required Bitfount patient ID, skipping record")  # type: ignore[unreachable] # Reason: should be unreachable but just sanity checking # noqa: E501
                continue

            # Handle name fields
            given_name: Optional[str]
            family_name: Optional[str]

            if name_col:
                # Split full name into given and family names
                # This maintains consistency: if ID was generated from NAME_COL,
                # we extract names from the same NAME_COL
                given_name, family_name = _WorkerSide._split_full_name(row[name_col])
            else:
                # Get separate name fields (only used when no full name column exists)
                given_name = row[given_name_col] if given_name_col else None
                family_name = row[family_name_col] if family_name_col else None

            # Create PatientDetails object
            patient = PatientDetails(
                bitfount_patient_id=bitfount_patient_id,
                dob=dob,
                given_name=given_name,
                family_name=family_name,
            )
            patients.append(patient)

        return patients

    @staticmethod
    def _split_full_name(full_name: str) -> tuple[Optional[str], Optional[str]]:
        """Split a full name into given name and family name components.

        Args:
            full_name: The full name string to split.

        Returns:
            Tuple of (given_name, family_name). Either component may be None if
            the name cannot be split properly.
        """
        if pd.isna(full_name) or not full_name.strip():
            return None, None

        # Handle DICOM-style names with carets
        if "^" in full_name:
            name_parts = full_name.split("^")
            if len(name_parts) >= 2:
                return name_parts[1], name_parts[0]  # DICOM format is Last^First
            return None, name_parts[0]

        # Handle other formats of name
        human_name = HumanName(full_name.strip())
        return (
            human_name.first if human_name.first else None,
            human_name.last if human_name.last else None,
        )

    @staticmethod
    def merge_results_with_dataframe(
        query_results: dict[PatientDetails, PatientQueryResults],
        df: pd.DataFrame,
        bitfount_patient_id_column: str = _BITFOUNT_PATIENT_ID_KEY,
        next_appointment_col: str = NEXT_APPOINTMENT_COL,
        prev_appointments_col: str = PREV_APPOINTMENTS_COL,
    ) -> pd.DataFrame:
        """Merge patient query results with the original DataFrame.

        Args:
            query_results: Dictionary mapping PatientDetails to their query results.
            df: DataFrame containing patient information. Must have a Bitfount patient
                ID column, `NAME_COL`, `DOB_COL`, `ORIGINAL_FILENAME_METADATA_COLUMN`,
                `ACQUISITION_DATE_COL`, and `LATERALITY_COL`.
            bitfount_patient_id_column: Explicit column name for Bitfount patient ID.
            next_appointment_col: The name to use for the column containing next
                appointment date information.
            prev_appointments_col: The name to use for the column containing previous
                appointments information.

        Returns:
            DataFrame with additional columns for query results information.

        Raises:
            ValueError: If required Bitfount patient ID column is missing.
        """
        # Create a copy of the input DataFrame
        result_df = df.reset_index(drop=True).copy()

        # Use explicit column names if provided, otherwise try to find a matching
        # column from the potential name lists that is in the dataframe.
        bitfount_id_col: Optional[str]
        if bitfount_patient_id_column in df.columns:
            bitfount_id_col = bitfount_patient_id_column
        else:
            bitfount_id_col = find_bitfount_id_column(df)
            if bitfount_id_col is None:
                raise ValueError(
                    f"DataFrame must contain a Bitfount patient ID column."
                    f" Expected one of: {BITFOUNT_ID_COLUMNS}"
                    f" or explicitly provided column: {bitfount_patient_id_column}"
                )
            else:
                result_df[_BITFOUNT_PATIENT_ID_KEY] = df[bitfount_id_col]

        required_cols = [
            NAME_COL,
            DOB_COL,
            ORIGINAL_FILENAME_METADATA_COLUMN,
            ACQUISITION_DATE_COL,
            LATERALITY_COL,
        ]
        missing_cols = [col for col in required_cols if col not in result_df.columns]
        if missing_cols:
            raise ValueError(
                f"DataFrame must contain required columns. Missing: {missing_cols}"
            )

        # Add next appointment information as column
        # Initialise column to all `None`s
        result_df[next_appointment_col] = None
        result_df[prev_appointments_col] = None
        result_df[GENDER_COL_EHR] = None
        result_df[HOME_NUMBER_COL] = None
        result_df[CELL_NUMBER_COL] = None
        result_df[EMAIL_COL] = None
        result_df[ADDRESS_COL] = None
        result_df[MRN_COL] = None
        result_df[CPT4_COLUMN] = None
        result_df[ICD10_COLUMN] = None
        result_df[LATEST_PRACTITIONER_NAME_COL] = None
        if DOB_COL not in result_df:
            result_df[DOB_COL] = None

        for patient, patient_query_results in query_results.items():
            mask = result_df[_BITFOUNT_PATIENT_ID_KEY] == patient.bitfount_patient_id
            result_df.loc[mask, next_appointment_col] = (
                patient_query_results.next_appointment
            )
            result_df.loc[mask, GENDER_COL_EHR] = patient_query_results.gender
            result_df.loc[mask, ADDRESS_COL] = patient_query_results.mailing_address
            result_df.loc[mask, MRN_COL] = patient_query_results.medical_record_number
            result_df.loc[mask, DOB_COL] = (
                patient.dob or patient_query_results.date_of_birth
            )
            result_df.loc[mask, GIVEN_NAME_COL] = patient_query_results.given_name
            result_df.loc[mask, FAMILY_NAME_COL] = patient_query_results.family_name
            result_df.loc[mask, LATEST_PRACTITIONER_NAME_COL] = (
                patient_query_results.latest_practitioner_name
            )

            # This is for elements which are lists, as they don't work with .loc
            for idx in result_df[mask].index:
                if patient_query_results.previous_appointments is not None:
                    result_df.at[idx, prev_appointments_col] = [
                        appt.format_for_csv()
                        for appt in patient_query_results.previous_appointments
                    ]
                result_df.at[idx, HOME_NUMBER_COL] = patient_query_results.home_numbers
                result_df.at[idx, CELL_NUMBER_COL] = patient_query_results.cell_numbers
                result_df.at[idx, EMAIL_COL] = patient_query_results.emails

                if patient_query_results.codes.condition_codes is not None:
                    result_df.at[idx, ICD10_COLUMN] = (
                        patient_query_results.codes.condition_codes
                    )

                if patient_query_results.codes.procedure_codes is not None:
                    result_df.at[idx, CPT4_COLUMN] = (
                        patient_query_results.codes.procedure_codes
                    )

        result_df[NEW_PATIENT_COL] = result_df[prev_appointments_col].apply(
            lambda x: len(x) <= 1 if x is not None else "Unknown"
        )

        # Drop other unnecessary columns
        final_df = result_df[EHR_QUERY_COLUMNS]

        # Return age col if present
        if AGE_COL in result_df:
            final_df[AGE_COL] = result_df[AGE_COL]

        return final_df


class EHRPatientQueryAlgorithm(
    BaseNonModelAlgorithmFactory[NoResultsModellerAlgorithm, _WorkerSide]
):
    """Algorithm for querying patient data from EHR systems."""

    # This algo has no init args. Most configuration will come from the pod config
    # when worker.initialise(...) is called
    fields_dict: ClassVar[T_FIELDS_DICT] = {}

    def __init__(
        self,
        datastructure: DataStructure,
        **kwargs: Any,
    ) -> None:
        """Initialize the algorithm.

        Args:
            datastructure: The data structure definition
            **kwargs: Additional keyword arguments.
        """
        super().__init__(datastructure=datastructure, **kwargs)

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _ModellerSide:  # Update return type
        """Modeller-side of the algorithm."""
        return _ModellerSide(**kwargs)

    def worker(
        self,
        *,
        hub: Optional[BitfountHub] = None,
        session: Optional[BitfountSession] = None,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the algorithm."""

        return _WorkerSide(
            hub=hub,
            session=session,
            **kwargs,
        )
