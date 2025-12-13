"""Algorithm for establishing number of results that match a given criteria."""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime
from typing import TYPE_CHECKING, Any, ClassVar, Mapping, Optional

from dateutil.relativedelta import relativedelta
from marshmallow import fields
import pandas as pd

from bitfount.externals.ehr.types import DATE_STR_FORMAT, Condition
from bitfount.federated.algorithms.ophthalmology.ga_trial_inclusion_criteria_match_algorithm_base import (  # noqa: E501
    BaseGATrialInclusionAlgorithmFactorySingleEye,
    BaseGATrialInclusionWorkerAlgorithmSingleEye,
    CodeFilterMixIn,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    AGE_COL,
    CNV_THRESHOLD,
    CPT4_COLUMN,
    FILTER_FAILED_REASON_COLUMN,
    ICD10_COLUMN,
    LARGEST_GA_LESION_LOWER_BOUND,
    MAX_CNV_PROBABILITY_COL_PREFIX,
    PREV_APPOINTMENTS_COL,
    SEGMENTATION_AREAS_COL,
    TOTAL_GA_AREA_COL_PREFIX,
    TOTAL_GA_AREA_LOWER_BOUND,
    TOTAL_GA_AREA_UPPER_BOUND,
    max_pathology_prob_col_name,
)
from bitfount.federated.algorithms.ophthalmology.trial_inclusion_filters import (
    ColumnFilter,
    MethodFilter,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ProtocolContext

if TYPE_CHECKING:
    from bitfount.types import T_FIELDS_DICT


# Constrain on age of patient
# Allow for patients about to turn 50 in the next year
PATIENT_AGE_LOWER_BOUND_CHARCOAL = 50 - 1

# Constraint on minimum number of years of history = 3
# Allow for patients with slightly fewer years of history
YEARS_OF_APPOINTMENT_HISTORY: int = 2
MIN_APPOINTMENTS_PER_HISTORY_YEAR: int = 2

# Constraint on the recency of appointments to be considered a "current" patient
CURRENT_PATIENT_MONTHS_THRESHOLD: int = 12

CHARCOAL_INCLUDED_CONDITIONS: set[str] = {
    "H35.3112",  # Right: Intermediate Dry Stage
    "H35.3113",  # Right: Advanced Atrophic w/o Subfoveal Involvement
    "H35.3114",  # Right: Advanced Atrophic w/ Subfoveal Involvement
    "H35.3122",  # Left: Intermediate Dry Stage
    "H35.3123",  # Left: Advance Atrophic w/o Subfoveal Involvement
    "H35.3124",  # Left: Advance Atrophic w/ Subfoveal Involvement
    "H35.3132",  # BiLateral: Intermediate Dry Stage
    "H35.3133",  # BiLateral: Advance Atrophic w/o Subfoveal Involvement
    "H35.3134",  # BiLateral: Advance Atrophic w/ Subfoveal Involvement
}

# Default thresholds for inclusion/exclusion criteria
DEFAULT_AREA_EXCLUSION_THRESHOLD: float = 15.0  # mm^2
DEFAULT_UNSPECIFIED_PATHOLOGY_INCLUSION_THRESHOLD: float = 0.5
DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD: float = 0.5

logger = _get_federated_logger(__name__)


class _WorkerSide(CodeFilterMixIn, BaseGATrialInclusionWorkerAlgorithmSingleEye):
    """Worker side of the algorithm."""

    def __init__(
        self,
        *,
        cnv_threshold: float = CNV_THRESHOLD,
        largest_ga_lesion_lower_bound: float = LARGEST_GA_LESION_LOWER_BOUND,
        largest_ga_lesion_upper_bound: Optional[float] = None,
        total_ga_area_lower_bound: float = TOTAL_GA_AREA_LOWER_BOUND,
        total_ga_area_upper_bound: float = TOTAL_GA_AREA_UPPER_BOUND,
        patient_age_lower_bound: Optional[int] = None,
        patient_age_upper_bound: Optional[int] = None,
        renamed_columns: Optional[Mapping[str, str]] = None,
        conditions_inclusion_codes: Optional[list[str]] = None,
        conditions_exclusion_codes: Optional[list[str]] = None,
        procedures_exclusion_codes: Optional[list[str]] = None,
        hypertransmission_threshold: Optional[float] = None,
        neurosensory_retina_atrophy_threshold: Optional[float] = None,
        drusen_threshold: Optional[float] = None,
        diffuse_edema_threshold: Optional[float] = None,
        epiretinal_fibrosis_threshold: Optional[float] = None,
        hard_exudates_threshold: Optional[float] = None,
        intraretinal_cystoid_fluid_threshold: Optional[float] = None,
        serous_rpe_detachment_threshold: Optional[float] = None,
        subretinal_fluid_threshold: Optional[float] = None,
        subretinal_hyperreflective_material__shrm__threshold: Optional[float] = None,
        diabetic_macular_edema_threshold: Optional[float] = None,
        wet_amd_threshold: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        if patient_age_lower_bound is not None:
            logger.warning(
                f"Charcoal algorithm explicitly sets patient_age_lower_bound;"
                f" received value of {patient_age_lower_bound}."
                f" Using {PATIENT_AGE_LOWER_BOUND_CHARCOAL} instead."
            )
        super().__init__(
            cnv_threshold=cnv_threshold,
            largest_ga_lesion_lower_bound=largest_ga_lesion_lower_bound,  # not used
            largest_ga_lesion_upper_bound=largest_ga_lesion_upper_bound,  # not used
            total_ga_area_lower_bound=total_ga_area_lower_bound,
            total_ga_area_upper_bound=total_ga_area_upper_bound,  # not used
            patient_age_lower_bound=PATIENT_AGE_LOWER_BOUND_CHARCOAL,  # Explicitly overridden  # noqa: E501
            patient_age_upper_bound=patient_age_upper_bound,
            renamed_columns=renamed_columns,
            conditions_inclusion_codes=conditions_inclusion_codes,
            conditions_exclusion_codes=conditions_exclusion_codes,
            procedures_exclusion_codes=procedures_exclusion_codes,
            **kwargs,
        )
        self.hypertransmission_threshold = (
            hypertransmission_threshold
            if hypertransmission_threshold is not None
            else DEFAULT_AREA_EXCLUSION_THRESHOLD
        )
        self.neurosensory_retina_atrophy_threshold = (
            neurosensory_retina_atrophy_threshold
            if neurosensory_retina_atrophy_threshold is not None
            else DEFAULT_AREA_EXCLUSION_THRESHOLD
        )
        self.drusen_threshold = (
            drusen_threshold
            if drusen_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_INCLUSION_THRESHOLD
        )
        self.diffuse_edema_threshold = (
            diffuse_edema_threshold
            if diffuse_edema_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )
        self.epiretinal_fibrosis_threshold = (
            epiretinal_fibrosis_threshold
            if epiretinal_fibrosis_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )
        self.hard_exudates_threshold = (
            hard_exudates_threshold
            if hard_exudates_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )
        self.intraretinal_cystoid_fluid_threshold = (
            intraretinal_cystoid_fluid_threshold
            if intraretinal_cystoid_fluid_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )
        self.serous_rpe_detachment_threshold = (
            serous_rpe_detachment_threshold
            if serous_rpe_detachment_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )
        self.subretinal_fluid_threshold = (
            subretinal_fluid_threshold
            if subretinal_fluid_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )
        self.subretinal_hyperreflective_material__shrm__threshold = (
            subretinal_hyperreflective_material__shrm__threshold
            if subretinal_hyperreflective_material__shrm__threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )
        self.diabetic_macular_edema_threshold = (
            diabetic_macular_edema_threshold
            if diabetic_macular_edema_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )
        self.wet_amd_threshold = (
            wet_amd_threshold
            if wet_amd_threshold is not None
            else DEFAULT_UNSPECIFIED_PATHOLOGY_EXCLUSION_THRESHOLD
        )

        if self.conditions_inclusion_codes is None:
            logger.info(
                "Charcoal Trial Inclusion: no conditions inclusion codes"
                " provided. Using default AMD ICD10 codes for inclusion."
            )
            self.conditions_inclusion_codes = CHARCOAL_INCLUDED_CONDITIONS

    # Note: The following method was renamed from run() as it returns a dataframe
    #     and hence has a different signature from the parent class
    def run_and_return_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """Finds number of patients that match the clinical criteria.

        Args:
            dataframe: The dataframe to process.

        Returns:
            A tuple of counts of patients that match the clinical criteria.
            Tuple is of form (match criteria, don't match criteria).
        """
        if dataframe.empty:
            return dataframe

        dataframe = self._add_age_col(dataframe)
        dataframe = self._filter_by_criteria(dataframe)

        return dataframe

    def get_filters(self) -> list[ColumnFilter | MethodFilter]:
        """Returns the eligibility filters for the algorithm.

        Returns a list of ColumnFilter or MethodFilter objects for filtering
        patients eligible for trial.

        This algorithm is designed to find patients that match the
        Charcoal clinical criteria.
        The criteria are as follows:
        1. No CNV (CNV probability less than CNV_THRESHOLD)
        2. Age greater than PATIENT_AGE_LOWER_BOUND_CHARCOAL
        3. Has diagnosis of Dry AMD OR
               Total GA area greater than TOTAL_GA_AREA_LOWER_BOUND
        4. Patient is not diagnosed with any of excluded conditions
        5. Patient has not had any of excluded procedures/medications
        6. Appointment history going back at least YEARS_OF_APPOINTMENT_HISTORY years
        7. Had appointment within last CURRENT_PATIENT_MONTHS_THRESHOLD months
        8. Hypertransmission area less than specified threshold
        9. Neurosensory retina atrophy area less than specified threshold
        10. Diffuse edema probability less than specified threshold
        11. Epiretinal fibrosis probability less than specified threshold
        12. Hard exudates probability less than specified threshold
        13. Intraretinal cystoid fluid probability less than specified threshold
        14. Serous RPE detachment probability less than specified threshold
        15. Subretinal fluid probability less than specified threshold
        16. Subretinal hyperreflective material prob. less than specified threshold
        17. Diabetic macular edema probability less than specified threshold
        18. Wet AMD probability less than specified threshold
        """
        max_cnv_column = self._get_column_name(MAX_CNV_PROBABILITY_COL_PREFIX)

        # Note: We are not using self.get_base_column_filters here as it contains
        #     filters not required for charcoal

        return [
            # 1. No CNV (CNV probability less than CNV_THRESHOLD)
            ColumnFilter(
                column=max_cnv_column,
                operator="<=",
                value=self.cnv_threshold,
            ),
            # 2. Age greater than PATIENT_AGE_LOWER_BOUND_CHARCOAL
            ColumnFilter(
                column=AGE_COL,
                operator=">=",
                value=PATIENT_AGE_LOWER_BOUND_CHARCOAL,
            ),
            # 3. Has diagnosis of Dry AMD OR
            #    Total GA area greater than TOTAL_GA_AREA_LOWER_BOUND OR
            #    Evidence of hard or soft drusen bodies in scan
            MethodFilter(
                method=self.diagnosis_filter,
                required_columns={
                    TOTAL_GA_AREA_COL_PREFIX,
                    ICD10_COLUMN,
                    max_pathology_prob_col_name("hard_drusen"),
                    max_pathology_prob_col_name("soft_drusen"),
                },
                filter_name="MD detected in diagnosis or in scan",
                filter_failed_message="patient does not have"
                " diagnosis for macular degeneration",
            ),
            # 4. Patient is not diagnosed with any of excluded conditions
            MethodFilter(
                method=self.excluded_conditions_filter,
                required_columns={ICD10_COLUMN},
                filter_name="Excluded Conditions",
                filter_failed_message="patient diagnosed with one of the"
                " excluded conditions",
            ),
            # 5. Patient has not had any of excluded procedures/medications
            MethodFilter(
                method=self.excluded_procedures_filter,
                required_columns={CPT4_COLUMN},
                filter_name="Excluded Treatments",
                filter_failed_message="patient has had treatment that"
                " precludes them from the trial",
            ),
            # 6. Appointment history going back at least YEARS_OF_APPOINTMENT_HISTORY
            # years
            MethodFilter(
                method=self.appointment_history_filter,
                required_columns={PREV_APPOINTMENTS_COL},
                filter_name=f">{YEARS_OF_APPOINTMENT_HISTORY} years"
                f" of appointment history",
                filter_failed_message="patient did not have sufficiently"
                " long history of macular degeneration",
            ),
            # 7. Had appointment within last CURRENT_PATIENT_MONTHS_THRESHOLD months
            MethodFilter(
                method=self.is_current_patient,
                required_columns={PREV_APPOINTMENTS_COL},
                filter_name=(
                    f"Had appointment within last"
                    f" {CURRENT_PATIENT_MONTHS_THRESHOLD} months"
                ),
                filter_failed_message="patient is not a current patient",
            ),
            # 8. Hypertransmission area less than specified threshold
            MethodFilter(
                method=self.hypertransmission_area_filter,
                required_columns={SEGMENTATION_AREAS_COL},
                filter_name=f"Hypertransmission area less than {self.hypertransmission_threshold} mm^2",  # noqa: E501
                filter_failed_message=f"patient has hypertransmission area greater than {self.hypertransmission_threshold} mm^2",  # noqa: E501
            ),
            # 9. Neurosensory retina atrophy area less than specified threshold
            MethodFilter(
                method=self.neurosensory_retina_atrophy_area_filter,
                required_columns={SEGMENTATION_AREAS_COL},
                filter_name=f"Neurosensory retina atrophy area less than {self.neurosensory_retina_atrophy_threshold} mm^2",  # noqa: E501
                filter_failed_message=f"patient has neurosensory retina atrophy area greater than {self.neurosensory_retina_atrophy_threshold} mm^2",  # noqa: E501
            ),
            # 10. Diffuse edema probability less than specified threshold
            ColumnFilter(
                column=max_pathology_prob_col_name("diffuse_edema"),
                operator="<=",
                value=self.diffuse_edema_threshold,
            ),
            # 11. Epiretinal fibrosis probability less than specified threshold
            ColumnFilter(
                column=max_pathology_prob_col_name("epiretinal_fibrosis"),
                operator="<=",
                value=self.epiretinal_fibrosis_threshold,
            ),
            # 12. Hard exudates probability less than specified threshold
            ColumnFilter(
                column=max_pathology_prob_col_name("hard_exudates"),
                operator="<=",
                value=self.hard_exudates_threshold,
            ),
            # 13. Intraretinal cystoid fluid probability less than specified threshold
            ColumnFilter(
                column=max_pathology_prob_col_name("intraretinal_cystoid_fluid"),
                operator="<=",
                value=self.intraretinal_cystoid_fluid_threshold,
            ),
            # 14. Serous RPE detachment probability less than specified threshold
            ColumnFilter(
                column=max_pathology_prob_col_name("serous_rpe_detachment"),
                operator="<=",
                value=self.serous_rpe_detachment_threshold,
            ),
            # 15. Subretinal fluid probability less than specified threshold
            ColumnFilter(
                column=max_pathology_prob_col_name("subretinal_fluid"),
                operator="<=",
                value=self.subretinal_fluid_threshold,
            ),
            # 16. Subretinal hyperreflective material probability less than specified
            # threshold
            ColumnFilter(
                column=max_pathology_prob_col_name(
                    "subretinal_hyperreflective_material__shrm_"
                ),
                operator="<=",
                value=self.subretinal_hyperreflective_material__shrm__threshold,
            ),
            # 17. Diabetic macular edema probability less than specified threshold
            ColumnFilter(
                column=max_pathology_prob_col_name("diabetic_macular_edema"),
                operator="<=",
                value=self.diabetic_macular_edema_threshold,
            ),
            # 18. Wet AMD probability less than specified threshold
            ColumnFilter(
                column=max_pathology_prob_col_name("wet_amd"),
                operator="<=",
                value=self.wet_amd_threshold,
            ),
        ]

    def diagnosis_filter(self, row: pd.Series) -> tuple[bool, Optional[str]]:
        """Filter to check patient diagnosis.

        Matches patient if ANY of the following:
          - Patient has a matching diagnosis code in inclusion list OR
          - Patient has GA detected in scan (total GA area ≥ lower bound) OR
          - Patient has evidence of hard or soft drusen bodies in scan
            (probability > 0 for either)
        """
        # Any matching diagnosis code to conditions_inclusion_codes
        if row[ICD10_COLUMN] and self.conditions_inclusion_codes:
            patient_conditions: list[Condition] = row[ICD10_COLUMN]
            patient_conditions_str = set(i.code_code for i in patient_conditions)
            for code in self.conditions_inclusion_codes:
                if code in patient_conditions_str:
                    return True, None

        # Check if GA detected in scan
        if row[TOTAL_GA_AREA_COL_PREFIX] is not None and hasattr(
            self, "total_ga_area_lower_bound"
        ):
            if row[TOTAL_GA_AREA_COL_PREFIX] >= self.total_ga_area_lower_bound:
                return True, None

        # Check for hard or soft drusen evidence (probability > 0)
        hard_drusen_col = max_pathology_prob_col_name("hard_drusen")
        if pd.notna(row[hard_drusen_col]) and row[hard_drusen_col] > 0:
            return True, None

        soft_drusen_col = max_pathology_prob_col_name("soft_drusen")
        if pd.notna(row[soft_drusen_col]) and row[soft_drusen_col] > 0:
            return True, None

        return False, None

    def appointment_history_filter(self, row: pd.Series) -> tuple[bool, Optional[str]]:
        """Filter to check patient appointment history length.

        Matches patient with at least YEARS_OF_APPOINTMENT_HISTORY history and at
        least MIN_APPOINTMENTS_PER_HISTORY_YEAR appointment dates per year.
        """
        if not row[PREV_APPOINTMENTS_COL]:
            return False, None

        appointment_dates = self._convert_appointment_dates(row)

        historic_cutoff_date: date = date.today() - relativedelta(
            years=YEARS_OF_APPOINTMENT_HISTORY
        )

        # Check that there are at least YEARS_OF_APPOINTMENT_HISTORY years of
        # appointments; check that there is at least one appointment at or before the
        # historic cutoff date
        if not any(d <= historic_cutoff_date for d in appointment_dates):
            return False, None

        # Filter down only to appointments within the last
        # YEARS_OF_APPOINTMENT_HISTORY years
        appointment_dates_within_history: list[date] = [
            d for d in appointment_dates if d >= historic_cutoff_date
        ]

        return self._check_min_appointments_per_year(
            appointment_dates_within_history,
        ), None

    def _check_min_appointments_per_year(
        self, appointment_dates_within_history: list[date]
    ) -> bool:
        """Checks if patient has at least MIN_APPOINTMENTS_PER_HISTORY_YEAR."""

        # Group the appointment dates into year blocks based from today and count the
        # number of appointments in each year block
        appointments_by_year_ago: Counter[int] = Counter(
            relativedelta(date.today(), d).years
            for d in appointment_dates_within_history
        )

        # Note: Counter[missing_item] == 0 so don't need to worry about KeyError
        return all(
            appointments_by_year_ago[years_ago] >= MIN_APPOINTMENTS_PER_HISTORY_YEAR
            for years_ago in range(YEARS_OF_APPOINTMENT_HISTORY)
        )

    def is_current_patient(self, row: pd.Series) -> tuple[bool, Optional[str]]:
        """Checks if the patient has had an appointment in the last X months."""
        if not row[PREV_APPOINTMENTS_COL]:
            return False, None

        appointment_dates = self._convert_appointment_dates(row)

        historic_cutoff_date: date = date.today() - relativedelta(
            months=CURRENT_PATIENT_MONTHS_THRESHOLD
        )

        return any(d >= historic_cutoff_date for d in appointment_dates), None

    def _convert_appointment_dates(self, row: pd.Series) -> list[date]:
        """Converts appointment dates from JSON format to list of dates."""
        appointment_dates = []
        for appt in row[PREV_APPOINTMENTS_COL]:
            if appt.get("Appointment Date"):
                appointment_dates.append(
                    datetime.strptime(
                        appt.get("Appointment Date"),
                        DATE_STR_FORMAT,
                    ).date()
                )
        return sorted(appointment_dates)

    def _filter_by_criteria(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies matching criteria to a dataframe to determine eligibility.

        This method adds eligibility column and exclusion reason column.
        """

        if FILTER_FAILED_REASON_COLUMN not in df:
            df[FILTER_FAILED_REASON_COLUMN] = ""

        for filter_ in self.get_filters():
            df = filter_.apply_filter(df)

        df[FILTER_FAILED_REASON_COLUMN] = df[FILTER_FAILED_REASON_COLUMN].apply(
            lambda x: x.strip(", ")
        )
        return df

    def hypertransmission_area_filter(
        self, row: pd.Series
    ) -> tuple[bool, Optional[str]]:
        """Filter to check patient hypertransmission area is less than specified threshold."""  # noqa: E501
        return (
            float(row[SEGMENTATION_AREAS_COL]["hypertransmission"])
            <= self.hypertransmission_threshold
        ), None

    def neurosensory_retina_atrophy_area_filter(
        self, row: pd.Series
    ) -> tuple[bool, Optional[str]]:
        """Filter to check patient neurosensory retina atrophy area is less than specified threshold."""  # noqa: E501
        return (
            float(row[SEGMENTATION_AREAS_COL]["neurosensory_retina_atrophy"])
            <= self.neurosensory_retina_atrophy_threshold
        ), None


class TrialInclusionCriteriaMatchAlgorithmCharcoal(
    BaseGATrialInclusionAlgorithmFactorySingleEye
):
    """Algorithm for establishing number of patients that match clinical criteria."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "cnv_threshold": fields.Float(allow_none=True),
        "largest_ga_lesion_lower_bound": fields.Float(allow_none=True),
        "largest_ga_lesion_upper_bound": fields.Float(allow_none=True),
        "total_ga_area_lower_bound": fields.Float(allow_none=True),
        "total_ga_area_upper_bound": fields.Float(allow_none=True),
        "patient_age_lower_bound": fields.Integer(allow_none=True),
        "patient_age_upper_bound": fields.Integer(allow_none=True),
        "conditions_inclusion_codes": fields.List(fields.Str(), allow_none=True),
        "conditions_exclusion_codes": fields.List(fields.Str(), allow_none=True),
        "procedures_exclusion_codes": fields.List(fields.Str(), allow_none=True),
        "hypertransmission_threshold": fields.Float(allow_none=True),
        "neurosensory_retina_atrophy_threshold": fields.Float(allow_none=True),
        "drusen_threshold": fields.Float(allow_none=True),
        "diffuse_edema_threshold": fields.Float(allow_none=True),
        "epiretinal_fibrosis_threshold": fields.Float(allow_none=True),
        "hard_exudates_threshold": fields.Float(allow_none=True),
        "intraretinal_cystoid_fluid_threshold": fields.Float(allow_none=True),
        "serous_rpe_detachment_threshold": fields.Float(allow_none=True),
        "subretinal_fluid_threshold": fields.Float(allow_none=True),
        "subretinal_hyperreflective_material__shrm__threshold": fields.Float(
            allow_none=True
        ),
        "diabetic_macular_edema_threshold": fields.Float(allow_none=True),
        "wet_amd_threshold": fields.Float(allow_none=True),
    }

    def __init__(
        self,
        cnv_threshold: float = CNV_THRESHOLD,
        largest_ga_lesion_lower_bound: float = LARGEST_GA_LESION_LOWER_BOUND,
        largest_ga_lesion_upper_bound: Optional[float] = None,
        total_ga_area_lower_bound: float = TOTAL_GA_AREA_LOWER_BOUND,
        total_ga_area_upper_bound: float = TOTAL_GA_AREA_UPPER_BOUND,
        patient_age_lower_bound: Optional[int] = None,
        patient_age_upper_bound: Optional[int] = None,
        conditions_inclusion_codes: Optional[list[str]] = None,
        conditions_exclusion_codes: Optional[list[str]] = None,
        procedures_exclusion_codes: Optional[list[str]] = None,
        hypertransmission_threshold: Optional[float] = None,
        neurosensory_retina_atrophy_threshold: Optional[float] = None,
        drusen_threshold: Optional[float] = None,
        diffuse_edema_threshold: Optional[float] = None,
        epiretinal_fibrosis_threshold: Optional[float] = None,
        hard_exudates_threshold: Optional[float] = None,
        intraretinal_cystoid_fluid_threshold: Optional[float] = None,
        serous_rpe_detachment_threshold: Optional[float] = None,
        subretinal_fluid_threshold: Optional[float] = None,
        subretinal_hyperreflective_material__shrm__threshold: Optional[float] = None,
        diabetic_macular_edema_threshold: Optional[float] = None,
        wet_amd_threshold: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            cnv_threshold=cnv_threshold,
            largest_ga_lesion_lower_bound=largest_ga_lesion_lower_bound,
            total_ga_area_lower_bound=total_ga_area_lower_bound,
            total_ga_area_upper_bound=total_ga_area_upper_bound,
            largest_ga_lesion_upper_bound=largest_ga_lesion_upper_bound,
            patient_age_lower_bound=patient_age_lower_bound,
            patient_age_upper_bound=patient_age_upper_bound,
            **kwargs,
        )
        self.conditions_inclusion_codes = conditions_inclusion_codes
        self.conditions_exclusion_codes = conditions_exclusion_codes
        self.procedures_exclusion_codes = procedures_exclusion_codes
        self.hypertransmission_threshold = hypertransmission_threshold
        self.neurosensory_retina_atrophy_threshold = (
            neurosensory_retina_atrophy_threshold
        )
        self.drusen_threshold = drusen_threshold
        self.diffuse_edema_threshold = diffuse_edema_threshold
        self.epiretinal_fibrosis_threshold = epiretinal_fibrosis_threshold
        self.hard_exudates_threshold = hard_exudates_threshold
        self.intraretinal_cystoid_fluid_threshold = intraretinal_cystoid_fluid_threshold
        self.serous_rpe_detachment_threshold = serous_rpe_detachment_threshold
        self.subretinal_fluid_threshold = subretinal_fluid_threshold
        self.subretinal_hyperreflective_material__shrm__threshold = (
            subretinal_hyperreflective_material__shrm__threshold
        )
        self.diabetic_macular_edema_threshold = diabetic_macular_edema_threshold
        self.wet_amd_threshold = wet_amd_threshold

    def worker(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the algorithm."""
        return _WorkerSide(
            cnv_threshold=self.cnv_threshold,
            largest_ga_lesion_lower_bound=self.largest_ga_lesion_lower_bound,
            largest_ga_lesion_upper_bound=self.largest_ga_lesion_upper_bound,
            total_ga_area_lower_bound=self.total_ga_area_lower_bound,
            total_ga_area_upper_bound=self.total_ga_area_upper_bound,
            patient_age_lower_bound=self.patient_age_lower_bound,
            patient_age_upper_bound=self.patient_age_upper_bound,
            conditions_inclusion_codes=self.conditions_inclusion_codes,
            conditions_exclusion_codes=self.conditions_exclusion_codes,
            procedures_exclusion_codes=self.procedures_exclusion_codes,
            hypertransmission_threshold=self.hypertransmission_threshold,
            neurosensory_retina_atrophy_threshold=self.neurosensory_retina_atrophy_threshold,
            drusen_threshold=self.drusen_threshold,
            diffuse_edema_threshold=self.diffuse_edema_threshold,
            epiretinal_fibrosis_threshold=self.epiretinal_fibrosis_threshold,
            hard_exudates_threshold=self.hard_exudates_threshold,
            intraretinal_cystoid_fluid_threshold=self.intraretinal_cystoid_fluid_threshold,
            serous_rpe_detachment_threshold=self.serous_rpe_detachment_threshold,
            subretinal_fluid_threshold=self.subretinal_fluid_threshold,
            subretinal_hyperreflective_material__shrm__threshold=self.subretinal_hyperreflective_material__shrm__threshold,
            diabetic_macular_edema_threshold=self.diabetic_macular_edema_threshold,
            wet_amd_threshold=self.wet_amd_threshold,
            **kwargs,
        )
