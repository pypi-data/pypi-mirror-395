"""Algorithm for establishing number of results that match a given criteria."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, ClassVar, Mapping, Optional

from marshmallow import fields
import pandas as pd

from bitfount.federated.algorithms.ophthalmology.ga_trial_inclusion_criteria_match_algorithm_base import (  # noqa: E501
    BaseGATrialInclusionAlgorithmFactorySingleEye,
    BaseGATrialInclusionWorkerAlgorithmSingleEye,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    AGE_COL,
    FILTER_FAILED_REASON_COLUMN,
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
PATIENT_AGE_LOWER_BOUND_SAPPHIRE = 49
PATIENT_AGE_UPPER_BOUND_SAPPHIRE = 90

EPSILON = 0.00001

logger = _get_federated_logger("bitfount.federated")


class _WorkerSide(BaseGATrialInclusionWorkerAlgorithmSingleEye):
    """Worker side of the algorithm."""

    def __init__(
        self,
        *,
        patient_age_lower_bound: Optional[int] = None,
        patient_age_upper_bound: Optional[int] = None,
        renamed_columns: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        if patient_age_lower_bound is None:
            patient_age_lower_bound = PATIENT_AGE_LOWER_BOUND_SAPPHIRE
        if patient_age_upper_bound is None:
            patient_age_upper_bound = PATIENT_AGE_UPPER_BOUND_SAPPHIRE

        super().__init__(
            renamed_columns=renamed_columns,
            patient_age_lower_bound=patient_age_lower_bound,
            patient_age_upper_bound=patient_age_upper_bound,
            **kwargs,
        )

    # Note: The following method was renamed from run() as it returns a dataframe
    #     and hence has a different signature from the parent class
    def run_and_return_dataframe(
        self,
        dataframe: pd.DataFrame,
        ehr_dataframe: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:
        """Finds number of patients that match the clinical criteria.

        Args:
            dataframe: The dataframe to process.
            ehr_dataframe: Optional EHR dataframe to use for filtering.

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
        Sapphire clinical criteria.
        The criteria are as follows:
        1. Age between 50-90 inclusive
        2. First and second visits within timeframe, with CST/Fluid volume criteria

        """
        # Note: We are not using self.get_base_column_filters here as it contains
        #     filters not required for sapphire

        if self.patient_age_lower_bound is None or self.patient_age_upper_bound is None:
            # We are sure it won't be None due to init method
            # This is just to appease mypy
            raise ValueError(
                "patient_age_lower_bound or patient_age_upper_bound not set"
            )

        return [
            ColumnFilter(
                column=AGE_COL,
                operator=">=",
                value=self.patient_age_lower_bound,
            ),
            ColumnFilter(
                column=AGE_COL,
                operator="<=",
                value=self.patient_age_upper_bound,
            ),
            MethodFilter(
                method=self.cst_fluid_history_filter,
                required_columns={
                    "cst_mean_um_longitudinal",
                    "srf_total_fluid_volume_longitudinal",
                    "irf_total_fluid_volume_longitudinal",
                },
                filter_name="Aflibercept Response Criteria",
                filter_failed_message="Patient did not meet required "
                "Aflibercept Response Criteria",
            ),
        ]

    def cst_fluid_history_filter(self, row: pd.Series) -> tuple[bool, Optional[str]]:
        """Filter for CST/Fluid values at first and second visit.

        Returns eligibility (boolean value) and a string explaining
        context if eligible, as a tuple.
        """
        metrics_by_date: dict[datetime, dict[str, float]] = defaultdict(dict)
        for metric in [
            "cst_mean_um",
            "srf_total_fluid_volume",
            "irf_total_fluid_volume",
        ]:
            metric_over_time: list[tuple[float, datetime]] = row[
                metric + "_longitudinal"
            ]
            for value, measurement_datetime in metric_over_time:
                metrics_by_date[measurement_datetime].update({metric: value})

        # metrics_by_date eg.:
        # {'2020-01-01':
        #   {'cst_mean_um': 101.0,
        #    'srf_total_fluid_volume': 0.0063,
        #    'irf_total_fluid_volume': 0.00636
        #    }, ...
        # }

        # Find first visit in the last 10 months
        sorted_scan_dates = sorted(metrics_by_date.keys())
        for idx, visit_date in enumerate(sorted_scan_dates):
            if visit_date < datetime.now() - timedelta(days=30.42 * 10):
                continue

            first_visit_date = visit_date
            for potential_second_date in sorted_scan_dates[idx:]:
                # Second visit must be between 4-16 weeks of the first
                if potential_second_date > first_visit_date + timedelta(
                    days=7 * 4
                ) and potential_second_date < first_visit_date + timedelta(days=7 * 16):
                    second_visit_date = potential_second_date

                    first_visit_metrics = metrics_by_date[first_visit_date]
                    second_visit_metrics = metrics_by_date[second_visit_date]
                    cst_first = first_visit_metrics.get("cst_mean_um")
                    cst_second = second_visit_metrics.get("cst_mean_um")
                    srf_first = first_visit_metrics.get("srf_total_fluid_volume")
                    srf_second = second_visit_metrics.get("srf_total_fluid_volume")
                    irf_first = first_visit_metrics.get("irf_total_fluid_volume")
                    irf_second = second_visit_metrics.get("irf_total_fluid_volume")
                    eligible = self._check_criteria_for_date_pair(
                        cst_first=cst_first,
                        cst_second=cst_second,
                        srf_first=srf_first,
                        srf_second=srf_second,
                        irf_first=irf_first,
                        irf_second=irf_second,
                    )
                    if eligible:
                        first_visit_date_str = first_visit_date.strftime("%Y-%m-%d")
                        second_visit_date_str = second_visit_date.strftime("%Y-%m-%d")

                        if (
                            cst_first is not None
                            and cst_second is not None
                            and cst_second < cst_first
                        ):
                            cst_first_str = self._format_value(cst_first)
                            cst_second_str = self._format_value(cst_second)
                            cst_reduction = round(
                                (1 - (cst_second / cst_first)) * 100, 1
                            )
                            cst_reduction_string = (
                                f"CST reduction: -{cst_reduction}%"
                                f" ({cst_first_str}um to {cst_second_str} um)\n"
                            )
                        else:
                            cst_reduction_string = ""

                        srf_first_str = self._format_value(srf_first)
                        srf_second_str = self._format_value(srf_second)
                        irf_first_str = self._format_value(irf_first)
                        irf_second_str = self._format_value(irf_second)
                        explanation = (
                            f"Responsiveness to Aflibercept assessed using "
                            f"Visit 1 as {first_visit_date_str} and "
                            f"Visit 2 as {second_visit_date_str}\n"
                            f"{cst_reduction_string}"
                            f"SRF: {srf_first_str} to {srf_second_str}nL\n"
                            f"IRF: {irf_first_str} to {irf_second_str}nL"
                        )
                        return True, explanation

        return False, None

    def _format_value(self, value: Optional[float]) -> str:
        """Format value for explanation string."""
        if value is None:
            return "None"

        return str(round(value, 2))

    def _check_criteria_for_date_pair(
        self,
        cst_first: Optional[float],
        cst_second: Optional[float],
        srf_first: Optional[float],
        srf_second: Optional[float],
        irf_first: Optional[float],
        irf_second: Optional[float],
    ) -> bool:
        """Check for eligibility based on given First and Second visit metrics."""
        #     CST/IRF criterium:
        # If CST > 300 μm at the first OCT date
        #   CST ≤ 350 μm at the second OCT date +
        #   ≥ 10% reduction in CST OR
        #   complete resolution of SRF and/or IRF on OCT
        #   (if both were present, both need to be completely resolved)
        # If CST ≤ 300 μm at the first OCT date
        #   CST ≤ 350 μm at the second OCT date +
        #   ≥ 5% reduction in CST OR
        #   complete resolution of SRF and/or IRF on OCT
        #   (if both were present, both need to be completely resolved)
        if cst_first is None or cst_second is None:
            return False

        if cst_second > 350:
            return False

        percent_reduction_in_cst = 1 - (cst_second / cst_first)
        # if percent_reduction_in_cst < 0: #this means there was an increase in CST
        #     return False

        if cst_first > 300:
            if percent_reduction_in_cst >= 0.1:  # more than 10% reduction
                return True
        else:  # CST at first vist <= 300
            if percent_reduction_in_cst >= 0.05:  # more than 5% reduction
                return True

        # IRF or SRF Fluid Volume completely resolved

        # None indicates calculation error and unknown, consider ineligible
        if irf_second is None or srf_second is None:
            return False

        # allowing tiny margin of error
        if irf_second < EPSILON and srf_second < EPSILON:
            if irf_first is None and srf_first is None:
                return False
            if irf_first is not None and irf_first >= EPSILON:
                return True
            if srf_first is not None and srf_first >= EPSILON:
                return True

        return False

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


class TrialInclusionCriteriaMatchAlgorithmSapphire(
    BaseGATrialInclusionAlgorithmFactorySingleEye
):
    """Algorithm for establishing number of patients that match clinical criteria."""

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "patient_age_lower_bound": fields.Integer(allow_none=True),
        "patient_age_upper_bound": fields.Integer(allow_none=True),
    }

    def __init__(
        self,
        patient_age_lower_bound: Optional[int] = None,
        patient_age_upper_bound: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            patient_age_lower_bound=patient_age_lower_bound,
            patient_age_upper_bound=patient_age_upper_bound,
            **kwargs,
        )

    def worker(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the algorithm."""
        return _WorkerSide(
            patient_age_lower_bound=self.patient_age_lower_bound,
            patient_age_upper_bound=self.patient_age_upper_bound,
            **kwargs,
        )
