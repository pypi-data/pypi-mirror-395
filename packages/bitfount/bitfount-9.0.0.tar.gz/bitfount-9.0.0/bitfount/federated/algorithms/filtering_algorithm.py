"""Algorithm for filtering data records based on configurable strategies."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import os
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Optional,
    Sequence,
    TypedDict,
    Union,
    cast,
)

from dateutil.relativedelta import relativedelta
from marshmallow import fields
from methodtools import lru_cache
import pandas as pd
from typing_extensions import NotRequired

from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.federated.algorithms.base import (
    BaseModellerAlgorithm,
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import PATIENT_ID_COL
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.types import ProtocolContext, TaskContext
from bitfount.utils import delegates

if TYPE_CHECKING:
    from bitfount.types import T_FIELDS_DICT

logger = _get_federated_logger(__name__)


COMBINED_ID_COLUMN = "BitfountFilterCombinedID"


class _FilterArgsTypedDict(TypedDict, total=False):
    """Typed dictionary for filter arguments.

    Args:
        remote_modeller: Whether the filter strategy is being used by a remote modeller.
    """

    remote_modeller: NotRequired[bool]


@dataclass(kw_only=True)
class _FilterStrategyBase:
    """Base class for filter strategies."""

    task_context: TaskContext
    remote_modeller: bool = False

    def __post_init__(self) -> None:
        self.validate_args()

    def validate_args(self) -> None:
        """Validate the arguments for the filter strategy."""
        raise NotImplementedError

    def get_column_names(self) -> list[str]:
        """Get the column names used in the filter strategy.

        Returns:
            list[str]: List of column names used in the filter strategy.
        """
        raise NotImplementedError

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the filter strategy to the DataFrame."""
        raise NotImplementedError


class LatestFilterArgs(_FilterArgsTypedDict):
    """Arguments for LATEST filter strategy.

    This filtering strategy keeps only the latest records per ID.

    See dataclass for meanings of args.
    """

    date_column: str
    id_column: Union[str, list[str]]
    num_latest: int


@dataclass(kw_only=True)
class _LatestFilterStrategy(_FilterStrategyBase):
    """Filter strategy to keep only the latest records per ID.

    Args:
        date_column: The name of the column containing date information.
        id_column: Name of column (or columns) to use as the ID(s) for grouping
            and filtering the dates.
        num_latest: The number of records to return for each ID.
    """

    date_column: str
    id_column: Union[str, list[str]]
    num_latest: int = 1

    def validate_args(self) -> None:
        """Validate the arguments for the LATEST strategy.

        Raises:
            ValueError: If date_column is not provided.
            ValueError: If id_column is not provided.
            ValueError: If num_latest is not a positive integer.
        """
        if not self.date_column:
            raise ValueError("date_column is required for LATEST strategy")
        if not self.id_column:
            raise ValueError("id_column is required for LATEST strategy")
        if self.num_latest < 1:
            raise ValueError("num_latest must be at least 1")

    def get_column_names(self) -> list[str]:
        """Get the column names used in the filter strategy.

        Returns:
            List of column names used in the filter strategy.
        """
        if isinstance(self.id_column, list):
            return [self.date_column] + self.id_column
        return [self.date_column, self.id_column]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the latest filter strategy to the DataFrame.

        This method filters the DataFrame to keep only the latest records
        per unique ID. It handles both single and multiple ID columns by
        creating a combined ID column if necessary. The method retains only
        the latest records for each unique ID based on the specified date column.

        Args:
            df: The input DataFrame to be filtered.

        Returns:
            The filtered DataFrame containing only the latest records for each unique
            ID.

        Raises:
            ValueError: If any of the specified ID columns or the date column are not
                found in the DataFrame.
        """
        if self.date_column not in df.columns:
            raise ValueError(f"Date column '{self.date_column}' not found in data")

        # Get ID column to use, either a combined ID if multiple ID columns were
        # selected, or the single ID column itself.
        if isinstance(self.id_column, list):
            for col in self.id_column:
                if col not in df.columns:
                    raise ValueError(f"ID column '{col}' not found in data")
            id_column = COMBINED_ID_COLUMN
            df[id_column] = df[self.id_column].astype(str).agg("-".join, axis=1)
        else:
            id_column = self.id_column
            if id_column not in df.columns:
                raise ValueError(f"ID column '{id_column}' not found in data")

        # Sort, group, and filter for the latest records for the ID combination
        df.loc[:, self.date_column] = pd.to_datetime(df[self.date_column])
        df = df.sort_values([id_column, self.date_column], ascending=[True, False])
        latest_records = (
            df.groupby(id_column).head(self.num_latest).reset_index(drop=True)
        )

        logger.info(
            f"Filtered {len(df)} records down to {len(latest_records)} latest records"
        )
        return latest_records


class FrequencyFilterArgs(_FilterArgsTypedDict):
    """Arguments for FREQUENCY filter strategy.

    This filtering strategy keeps only records with a specified
    frequency of ID occurrence.
    """

    id_column: Union[str, list[str]]
    min_frequency: int
    max_frequency: int


@dataclass(kw_only=True)
class _FrequencyFilterStrategy(_FilterStrategyBase):
    """Filter strategy to keep records based on frequency of ID occurrence."""

    id_column: Union[str, list[str]]
    min_frequency: Optional[int] = None
    max_frequency: Optional[int] = None

    def validate_args(self) -> None:
        """Validate the arguments for the FREQUENCY strategy."""
        if not self.id_column:
            raise ValueError("id_column is required for FREQUENCY strategy")
        if self.min_frequency is None and self.max_frequency is None:
            raise ValueError(
                "Either min_frequency or max_frequency "
                "must be specified for FREQUENCY strategy"
            )
        if self.min_frequency is not None and self.min_frequency < 1:
            raise ValueError("min_frequency must be a non-negative non-zero integer")
        if self.max_frequency is not None and self.max_frequency < 1:
            raise ValueError("max_frequency must be a non-negative non-zero integer")
        if (
            self.min_frequency is not None
            and self.max_frequency is not None
            and self.min_frequency > self.max_frequency
        ):
            raise ValueError(
                "min_frequency must be less than or equal to max_frequency"
            )

    def get_column_names(self) -> list[str]:
        """Get the column names used in the filter strategy.

        Returns:
            List of column names used in the filter strategy.
        """
        if isinstance(self.id_column, list):
            return self.id_column
        return [self.id_column]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the frequency filter strategy to the DataFrame.

        This method filters the DataFrame based on the frequency of occurrences
        of specified ID columns. It handles both single and multiple ID columns
        by creating a combined ID column if necessary. The method retains only
        the records with IDs that meet the specified minimum and maximum frequency
        criteria.

        Args:
            df: The input DataFrame to be filtered.

        Returns:
            The filtered DataFrame containing only the records with IDs that meet the
            frequency criteria.

        Raises:
            ValueError: If any of the specified ID columns are not
                found in the DataFrame.
        """
        if isinstance(self.id_column, list):
            for col in self.id_column:
                if col not in df.columns:
                    raise ValueError(f"ID column '{col}' not found in data")
            df[COMBINED_ID_COLUMN] = (
                df[self.id_column].astype(str).agg("-".join, axis=1)
            )
            id_column = COMBINED_ID_COLUMN
        else:
            id_column = self.id_column
            if id_column not in df.columns:
                raise ValueError(f"ID column '{id_column}' not found in data")

        id_counts = df[id_column].value_counts()
        valid_ids = id_counts.copy()

        if self.min_frequency is not None:
            valid_ids = valid_ids[valid_ids >= self.min_frequency]
        if self.max_frequency is not None:
            valid_ids = valid_ids[valid_ids <= self.max_frequency]

        filtered_df = df[df[id_column].isin(valid_ids.index)]

        logger.info(
            f"Filtered {len(df)} records down to {len(filtered_df)} records "
            f"based on frequency criteria "
            f"(min={self.min_frequency}, max={self.max_frequency})"
        )
        return filtered_df


class AgeRangeFilterArgs(_FilterArgsTypedDict):
    """Arguments for AGE_RANGE filter strategy.

    This filtering strategy keeps only records within a specified age range
    in a given column.
    """

    birth_date_column: str
    min_age: int
    max_age: int


@dataclass(kw_only=True)
class _AgeRangeFilterStrategy(_FilterStrategyBase):
    """Filter strategy to keep records within a specified age range."""

    birth_date_column: str
    min_age: Optional[int] = None
    max_age: Optional[int] = None

    def validate_args(self) -> None:
        """Validate the arguments for the AGE_RANGE strategy."""
        if not self.birth_date_column:
            raise ValueError("birth_date_column is required for AGE_RANGE strategy")
        if self.min_age is None and self.max_age is None:
            raise ValueError(
                "Either min_age or max_age must be specified for AGE_RANGE strategy"
            )
        if self.min_age is not None and self.min_age < 1:
            raise ValueError("min_age must be a non-negative non-zero integer")
        if self.max_age is not None and self.max_age < 1:
            raise ValueError("max_age must be a non-negative non-zero integer")
        if (
            self.min_age is not None
            and self.max_age is not None
            and self.min_age > self.max_age
        ):
            raise ValueError("min_age must be less than or equal to max_age")

    def get_column_names(self) -> list[str]:
        """Get the column names used in the filter strategy.

        Returns:
            List of column names used in the filter strategy.
        """
        return [self.birth_date_column]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the age range filter strategy to the DataFrame.

        This method filters the DataFrame based on the specified age range
        in the given column. It retains only the records with dates that fall
        within the specified start and end date range.

        Args:
            df: The input DataFrame to be filtered.

        Returns:
            The filtered DataFrame containing only the records with dates that fall
            within the specified range.

        Raises:
            ValueError: If the specified column is not found in the DataFrame.
        """
        if self.birth_date_column not in df.columns:
            raise ValueError(f"Column '{self.birth_date_column}' not found in data")

        df.loc[:, self.birth_date_column] = pd.to_datetime(df[self.birth_date_column])

        current_date = datetime.now()
        if self.min_age is not None:
            start_date = current_date - relativedelta(years=self.min_age)
            df = df[df[self.birth_date_column] <= start_date]
        if self.max_age is not None:
            end_date = current_date - relativedelta(years=self.max_age)
            df = df[df[self.birth_date_column] >= end_date]

        logger.info(
            f"Filtered {len(df)} records based on age range criteria "
            f"(min_age={self.min_age}, max_age={self.max_age})"
        )
        return df


class PatientIDFilterArgs(_FilterArgsTypedDict):
    """Arguments for PATIENT_ID filter strategy.

    This filtering strategy excludes records with a specified patient ID.
    """

    filename: Union[str, os.PathLike]
    patient_id_column: str


@dataclass(kw_only=True)
class _PatientIDFilterStrategy(_FilterStrategyBase):
    """Filter strategy to exclude records with a specified patient ID."""

    filename: Union[str, os.PathLike]
    patient_id_column: str

    # Initialise the patient IDs as an empty list, but not as an argument to the class
    _patient_ids: list[str] = field(default_factory=list, init=False, repr=False)

    @property
    def patient_ids(self) -> list[str]:
        """Get the patient IDs from the file."""
        if self.task_context == TaskContext.WORKER and self.remote_modeller:
            return self._patient_ids
        return self._read_patient_ids_from_file()

    @patient_ids.setter
    def patient_ids(self, patient_ids: list[str]) -> None:
        """Set the patient IDs from the file."""
        self._patient_ids = patient_ids

    @lru_cache(maxsize=1)
    def _read_patient_ids_from_file(self) -> list[str]:
        """Read the patient IDs from the file."""
        df = pd.read_csv(self.filename)
        return df[self.patient_id_column].tolist()

    def validate_args(self) -> None:
        """Validate the arguments for the PATIENT_ID strategy.

        Validation is only done on the side where the CSV file is located.

        Raises:
            ValueError: If the file path does not exist.
            ValueError: If the patient ID column is not found in the file.
        """
        if (self.task_context == TaskContext.WORKER and not self.remote_modeller) or (
            self.task_context == TaskContext.MODELLER and self.remote_modeller
        ):
            # Check if the filename exists
            path = Path(self.filename)
            if not path.exists():
                raise ValueError(f"File '{path}' does not exist")

            # Check if the patient ID column exists in the file
            df = pd.read_csv(path)
            if self.patient_id_column not in df.columns:
                raise ValueError(f"Column '{self.patient_id_column}' not found in file")

    def get_column_names(self) -> list[str]:
        """Get the column names used in the filter strategy.

        This refers to the patient ID column in the dataframe, not the patient ID
        column from the patient IDs file.

        Returns:
            List of column names used in the filter strategy.
        """
        return [PATIENT_ID_COL]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the patient ID filter strategy to the DataFrame.

        This method filters the DataFrame to exclude records with the specified patient
        IDs in the file.
        """
        return df[~df[PATIENT_ID_COL].isin(self.patient_ids)]


class ScanFrequencyFilterArgs(_FilterArgsTypedDict):
    """Arguments for SCAN_FREQUENCY filter strategy.

    This filtering strategy keeps only patients with a minimum specified number of scans
    per year over a specified number of years.
    """

    min_number_of_scans_per_year: int
    number_of_years: int
    date_column: str
    id_column: Union[str, list[str]]


@dataclass(kw_only=True)
class _ScanFrequencyFilterStrategy(_FilterStrategyBase):
    """Filter strategy to keep only patients with a minimum number of scans per year.

    Args:
        min_number_of_scans_per_year: The minimum required number of scans per year.
        number_of_years: The number of years to consider for the scan frequency.
        date_column: The name of the column containing date information.
        id_column: Name of column (or columns) to use as the ID(s) for grouping
            and filtering the dates.
    """

    min_number_of_scans_per_year: int
    number_of_years: int
    date_column: str
    id_column: Union[str, list[str]]

    def validate_args(self) -> None:
        """Validate the arguments for the SCAN_FREQUENCY strategy.

        Raises:
            ValueError: If min_number_of_scans_per_year is not a non-negative non-zero
                integer.
            ValueError: If number_of_years is not a non-negative non-zero integer.
            ValueError: If date_column is not provided.
            ValueError: If id_column is not provided.
        """
        if self.min_number_of_scans_per_year is None:
            raise ValueError(
                "min_number_of_scans_per_year is required for SCAN_FREQUENCY strategy"
            )
        if self.min_number_of_scans_per_year < 1:
            raise ValueError(
                "min_number_of_scans_per_year must be a non-negative non-zero integer"
            )
        if self.number_of_years is None:
            raise ValueError("number_of_years is required for SCAN_FREQUENCY strategy")
        if self.number_of_years < 1:
            raise ValueError("number_of_years must be a non-negative non-zero integer")

        if not self.date_column:
            raise ValueError("date_column is required for SCAN_FREQUENCY strategy")
        if not self.id_column:
            raise ValueError("id_column is required for SCAN_FREQUENCY strategy")

    def get_column_names(self) -> list[str]:
        """Get the column names used in the filter strategy.

        Returns:
            List of column names used in the filter strategy.
        """
        if isinstance(self.id_column, list):
            return [self.date_column] + self.id_column
        return [self.date_column, self.id_column]

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the scan frequency filter strategy to the DataFrame.

        This method filters the DataFrame to keep only patients with a minimum number
        of scans per year over a specified number of years. The most recent number of
        years are considered. The filtering is lenient, allowing a patient to be missing
        some records in a given year as long as they make up for it in other years.

        There are three hard requirements:
        1. The patient must have a recent record (within the last year).
        2. The patient must have `number_of_years` unique years with records.
        3. The patient must have a total of
            `min_number_of_scans_per_year` * `number_of_years` records over any number
            of years.

        Args:
            df: The input DataFrame to be filtered.

        Returns:
            The filtered DataFrame containing only the patients with a minimum number
            of scans per year over a specified number of years.
        """
        if self.date_column not in df.columns:
            raise ValueError(f"Date column '{self.date_column}' not found in data")

        # Get ID column to use, either a combined ID if multiple ID columns were
        # selected, or the single ID column itself.
        if isinstance(self.id_column, list):
            for col in self.id_column:
                if col not in df.columns:
                    raise ValueError(f"ID column '{col}' not found in data")
            id_column = COMBINED_ID_COLUMN
            df[id_column] = df[self.id_column].astype(str).agg("-".join, axis=1)
        else:
            id_column = self.id_column
            if id_column not in df.columns:
                raise ValueError(f"ID column '{id_column}' not found in data")

        # Normalize the date column to remove any time information
        df.loc[:, self.date_column] = pd.to_datetime(
            df[self.date_column]
        ).dt.normalize()
        if df[self.date_column].dt.tz is not None:
            df.loc[:, self.date_column] = df[self.date_column].dt.tz_localize(None)

        # Sort records by ID and date with most recent date first
        df = df.sort_values([id_column, self.date_column], ascending=[True, False])
        original_number_of_records = len(df)
        current_timestamp = pd.Timestamp.utcnow()
        if current_timestamp.tz is not None:
            current_timestamp = current_timestamp.tz_localize(None)
        current_timestamp = current_timestamp.normalize()
        past_year_cutoff = current_timestamp - pd.DateOffset(years=1)

        # Group records by patient ID and count the number of records and the number of
        # unique years with records
        group_dates = df.groupby(id_column)[self.date_column]
        patient_stats = group_dates.agg(
            total_records="count",
            year_count=lambda values: values.dt.year.nunique(),
            has_recent=lambda values: (values >= past_year_cutoff).any(),
        )

        # Get eligible patient IDs
        min_required_records = self.min_number_of_scans_per_year * self.number_of_years
        eligible_ids = patient_stats[
            (patient_stats["total_records"] >= min_required_records)
            & patient_stats["has_recent"]
            & (patient_stats["year_count"] >= self.number_of_years)
        ].index

        # Filter records to only include eligible patient IDs
        df = df[df[id_column].isin(eligible_ids)]

        logger.info(
            f"Filtered {original_number_of_records} records down to {len(df)} "
            f"records based on {self.min_number_of_scans_per_year} scans per year over "
            f"{self.number_of_years} years"
        )
        return df


class FilterStrategy(str, Enum):
    """Enumeration of available filtering strategies.

    Inherits from str to allow for easy conversion to string
    and comparison with other strings.
    The ordering of the inheritance is important (first str then Enum).
    This replicates the strEnum behaviour in Python 3.11+.
    TODO: [Python 3.11] Convert to strEnum when Python 3.11 is the minimum version.
    """

    LATEST = "latest"
    FREQUENCY = "frequency"
    AGE_RANGE = "age_range"
    PATIENT_ID = "patient_id"
    SCAN_FREQUENCY = "scan_frequency"


class FilterStrategyClass(Enum):
    """Enumeration map of filter strategies to TypedDict and classes."""

    LATEST = (LatestFilterArgs, _LatestFilterStrategy)
    FREQUENCY = (FrequencyFilterArgs, _FrequencyFilterStrategy)
    AGE_RANGE = (AgeRangeFilterArgs, _AgeRangeFilterStrategy)
    PATIENT_ID = (PatientIDFilterArgs, _PatientIDFilterStrategy)
    SCAN_FREQUENCY = (ScanFrequencyFilterArgs, _ScanFrequencyFilterStrategy)


FilterArgs = Union[
    LatestFilterArgs,
    FrequencyFilterArgs,
    AgeRangeFilterArgs,
    PatientIDFilterArgs,
    ScanFrequencyFilterArgs,
]


class _RecordFilter:
    """Class to handle record filtering logic."""

    def __init__(
        self,
        strategies: list[FilterStrategy],
        filter_args_list: list[FilterArgs],
        task_context: TaskContext,
    ) -> None:
        self.task_context = task_context
        self.filters = self._parse_filter_args(strategies, filter_args_list)
        # Use a set to handle duplicates and flatten the list of columns in use
        self.list_of_columns_in_use = list(
            {
                col
                for filter_strategy in self.filters
                for col in filter_strategy.get_column_names()
            }
        )

    def _parse_filter_args(
        self, strategies: list[FilterStrategy], filter_args_list: list[FilterArgs]
    ) -> list[_FilterStrategyBase]:
        """Convert dictionaries to the appropriate filter strategy class instances."""
        filters = []
        for strategy, filter_args in zip(strategies, filter_args_list):
            typed_dict_class, strategy_class = FilterStrategyClass[strategy.name].value
            try:
                # Attempt to convert the dictionary to the appropriate class instance
                filters.append(
                    strategy_class(task_context=self.task_context, **filter_args)
                )
            except TypeError as e:
                # Capture the error and provide a detailed message
                logger.error(
                    "Error converting filter arguments for strategy "
                    f"'{strategy}': {e}\n"
                    "Valid arguments: "
                    f"{list(typed_dict_class.__annotations__.keys())}"
                )
                logger.error("Filter will be skipped")
        return filters

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply the appropriate filtering strategy to the DataFrame.

        Args:
            df: Input DataFrame

        Returns:
            Filtered DataFrame
        """
        for filter_ in self.filters:
            if not df.empty:
                df = filter_.apply(df)
        return df


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algorithm.

    Args:
        strategies: List of filtering strategies
        filter_args_list: List of strategy-specific arguments
        task_context: Task context
        **kwargs: Additional keyword arguments
    """

    def __init__(
        self,
        strategies: list[FilterStrategy],
        filter_args_list: list[FilterArgs],
        task_context: TaskContext,
        **kwargs: Any,
    ) -> None:
        self.strategies = strategies
        self.filter_args_list = filter_args_list
        self.record_filter = _RecordFilter(strategies, filter_args_list, task_context)

        super().__init__(**kwargs)

    @property
    def remote_modeller(self) -> bool:
        """Get the values to send to the worker side of the algorithm."""
        return any(
            filter_args.get("remote_modeller", False)
            for filter_args in self.filter_args_list
        )

    def initialise(
        self,
        *,
        datasource: BaseSource,
        task_id: str,
        data_splitter: Optional[DatasetSplitter] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the algorithm with data source.

        Args:
            datasource: The data source to use
            task_id: The ID of the task being run.
            data_splitter: Optional data splitter
            pod_dp: Optional differential privacy configuration
            pod_identifier: Optional pod identifier
            **kwargs: Additional keyword arguments
        """
        self.initialise_data(datasource=datasource, data_splitter=data_splitter)

    def setup_run(self, **kwargs: Any) -> None:
        """Initial setup run that executes before any batching.

        This method is called by protocols tagged with InitialSetupWorkerProtocol
        before any batching occurs.

        Raises:
            ValueError: If datasource does not have a data cache.
        """
        if not isinstance(self.datasource, FileSystemIterableSource):
            logger.warning(
                "Filtering is currently only supported for file-based sources"
            )
            return

        # Ensure use of cache data
        if (
            not hasattr(self.datasource, "data_cache")
            or self.datasource.data_cache is None
        ):
            raise ValueError("No data cache provided for filtering")

        data_iterables = []
        for data_chunk in self.datasource.yield_data(use_cache=True):
            # Select only the columns in use, ignoring missing columns
            # Ensure ORIGINAL_FILENAME_METADATA_COLUMN is included
            columns_to_include = [
                ORIGINAL_FILENAME_METADATA_COLUMN
            ] + self.record_filter.list_of_columns_in_use
            available_columns = [
                col for col in columns_to_include if col in data_chunk.columns
            ]
            data_iterables.append(data_chunk[available_columns])

        if not data_iterables:
            logger.warning("No data found in datasource")
            return

        df = pd.concat(data_iterables)
        if df is None or df.empty:
            logger.warning("No data found in concatenated DataFrame")
            return

        # Apply the appropriate filtering strategy
        df = self.record_filter.filter(df)

        # Store the filtered indices/files for subsequent algorithms
        if hasattr(self.datasource, "selected_file_names_override"):
            self.datasource.selected_file_names_override = df[
                ORIGINAL_FILENAME_METADATA_COLUMN
            ].tolist()
            logger.info(
                "Selected files successfully overridden with "
                f"{len(self.datasource.selected_file_names_override)} files"
            )
        else:
            logger.warning("Data source does not support file name override")
            return

    @property
    def should_output_data(self) -> bool:
        """Indicates whether the initial setup algorithm should output data.

        For the most part initial setup algorithms will set up data, filtering it,
        grouping it, etc., and so this property should return True. However, there are
        some algorithms that don't produce any data (e.g., algorithms that use the
        initial setup phase to exchange runtime information) and so this property
        should return False.'
        """
        return True

    def run(self, *args: Any, **kwargs: Any) -> None:
        """Regular run method - does nothing as filtering is done in setup."""
        pass

    def update_values_from_modeller(self, values: dict[str, Any]) -> None:
        """Update the values sent from the modeller side of the algorithm."""
        for strategy_name, value in values.items():
            strategy = FilterStrategy[strategy_name]
            match strategy:
                case FilterStrategy.PATIENT_ID:
                    for filter_ in self.record_filter.filters:
                        if filter_.remote_modeller and isinstance(
                            filter_, _PatientIDFilterStrategy
                        ):
                            filter_.patient_ids = value
                case _:
                    pass


class _ModellerSide(BaseModellerAlgorithm):
    """Modeller side of the filtering algorithm."""

    def __init__(
        self,
        strategies: list[FilterStrategy],
        filter_args_list: list[FilterArgs],
        task_context: TaskContext,
        **kwargs: Any,
    ) -> None:
        self.strategies = strategies
        self.filter_args_list = filter_args_list
        self.task_context = task_context
        super().__init__(**kwargs)

    @property
    def remote_modeller(self) -> bool:
        """Get the values to send to the worker side of the algorithm."""
        return any(
            filter_args.get("remote_modeller", False)
            for filter_args in self.filter_args_list
        )

    def initialise(
        self,
        *,
        task_id: str,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""

    def run(self, *args: Any, **kwargs: Any) -> None:
        """Modeller side just logs the log message."""
        pass

    def values_to_send_to_worker(self) -> dict[str, Any]:
        """Get the values to send to the worker side of the algorithm."""
        if not self.remote_modeller:
            return dict()

        values_to_send: dict[str, Any] = dict()

        for strategy, filter_args in zip(self.strategies, self.filter_args_list):
            if filter_args.get("remote_modeller", False):
                match strategy:
                    case FilterStrategy.PATIENT_ID:
                        filter_args = cast(PatientIDFilterArgs, filter_args)
                        typed_dict_class, strategy_class = FilterStrategyClass[
                            strategy.name
                        ].value
                        try:
                            # Attempt to convert the dictionary to the appropriate class
                            # instance
                            filter_strategy = strategy_class(
                                task_context=self.task_context, **filter_args
                            )
                            values_to_send[strategy.name] = filter_strategy.patient_ids
                        except TypeError as e:
                            # Capture the error and provide a detailed message
                            logger.error(
                                "Error converting filter arguments for strategy "
                                f"'{strategy}': {e}\n"
                                "Valid arguments: "
                                f"{list(typed_dict_class.__annotations__.keys())}"
                            )
                    case _:
                        pass

        return values_to_send


@delegates()
class RecordFilterAlgorithm(BaseNonModelAlgorithmFactory[_ModellerSide, _WorkerSide]):
    """Algorithm factory for filtering records based on various strategies.

    Args:
        datastructure: The data structure to use for the algorithm.
        strategies: List of filtering strategies
        filter_args_list: List of strategy-specific arguments

    Attributes:
        datastructure: The data structure to use for the algorithm
        strategies: List of filtering strategies
        filter_args_list: List of strategy-specific arguments
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "strategies": fields.List(
            fields.Enum(FilterStrategy),
            required=True,
        ),
        "filter_args_list": fields.List(fields.Dict(), required=True),
    }

    def __init__(
        self,
        datastructure: DataStructure,
        strategies: Sequence[Union[FilterStrategy, str]],
        filter_args_list: list[FilterArgs],
        **kwargs: Any,
    ) -> None:
        self.strategies: list[FilterStrategy] = [
            FilterStrategy(strategy) if isinstance(strategy, str) else strategy
            for strategy in strategies
        ]
        self.filter_args_list = filter_args_list
        super().__init__(datastructure=datastructure, **kwargs)

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _ModellerSide:
        """Modeller-side of the algorithm."""
        return _ModellerSide(
            strategies=self.strategies,
            filter_args_list=self.filter_args_list,
            task_context=context.task_context,
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
            strategies=self.strategies,
            filter_args_list=self.filter_args_list,
            task_context=context.task_context,
            **kwargs,
        )


if TYPE_CHECKING:
    # Type checking to verify that the classes correctly implement the Protocol
    # interfaces. These assertions will be checked by type checkers like mypy.
    from bitfount.federated.algorithms.base import (
        InitialSetupModellerAlgorithm,
        InitialSetupWorkerAlgorithm,
    )

    # Verify _ModellerSide implements InitialSetupModellerAlgorithm
    _modeller_side_check: InitialSetupModellerAlgorithm = _ModellerSide(
        strategies=[FilterStrategy.LATEST],
        filter_args_list=[
            LatestFilterArgs(date_column="date", id_column="id", num_latest=1)
        ],
        task_context=TaskContext.MODELLER,
    )

    # Verify _WorkerSide implements InitialSetupWorkerAlgorithm
    _worker_side_check: InitialSetupWorkerAlgorithm = _WorkerSide(
        strategies=[FilterStrategy.LATEST],
        filter_args_list=[
            LatestFilterArgs(date_column="date", id_column="id", num_latest=1)
        ],
        task_context=TaskContext.WORKER,
    )
