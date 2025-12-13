"""Utility functions concerning data sources."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
import datetime
from enum import Enum
import logging
import os
from pathlib import Path
from typing import Any, Dict, Final, Optional, Union, cast, overload

from filetype import guess_extension
import numpy as np
import pandas as pd

import bitfount.data.datasources.base_source as base_source
from bitfount.data.datasources.types import Date, DateTD
from bitfount.data.types import DataPathModifiers, SingleOrMulti
from bitfount.utils.fs_utils import (
    get_file_creation_date,
    get_file_last_modification_date,
    get_file_size,
    is_file,
)
from bitfount.utils.logging_utils import SampleFilter

_logger = logging.getLogger(__name__)
_logger.addFilter(SampleFilter())

# Used for converting megabytes to bytes
NUM_BYTES_IN_A_MEGABYTE: Final[int] = 1024 * 1024

# FileSystemIterableSource metadata columns
ORIGINAL_FILENAME_METADATA_COLUMN: Final[str] = "_original_filename"
LAST_MODIFIED_METADATA_COLUMN: Final[str] = "_last_modified"
FILE_SYSTEM_ITERABLE_METADATA_COLUMNS: Final[tuple[str, ...]] = (
    ORIGINAL_FILENAME_METADATA_COLUMN,
    LAST_MODIFIED_METADATA_COLUMN,
)


def get_datetime(
    date: Optional[Union[Date, DateTD, datetime.date]],
) -> Optional[datetime.date]:
    """Convert a Date or DateTD object to a datetime.date object.

    Args:
        date: The Date or DateTD object to convert.

    Returns:
        The datetime.date object if date is a Date object, otherwise None.
    """
    if date:
        if isinstance(date, Date):
            return date.get_date()
        elif isinstance(date, datetime.date):
            # Already a datetime.date object
            return date
        else:  # is typed dict
            try:
                return Date(**date).get_date()
            except Exception as e:
                _logger.error(f"Unexpected date format: {date}. Error was: {e}")
                return None

    return None


def strip_dicom_null_chars(input_string: str) -> str:
    r"""Removes null byte data suffix and strips whitespace from DICOM strings.

    DICOM files often contain null terminators and padding bytes in text fields.
    This function removes everything from the first null byte onwards and strips
    leading/trailing whitespace.

    Args:
        input_string: The string to clean.

    Returns:
        The cleaned string with null bytes and surrounding whitespace removed.

    Examples:
        >>> strip_dicom_null_chars("Carl Zeiss Meditec\\x00\\x00U\\x12")
        "Carl Zeiss Meditec"
        >>> strip_dicom_null_chars("  Test  \\x00garbage")
        "Test"
    """
    byte_idx = input_string.find("\x00")
    if byte_idx != -1:
        input_string = input_string[:byte_idx]
    return input_string.strip()


def standardize_datetime_for_telemetry(
    value: Optional[Union[str, datetime.date, datetime.datetime, pd.Timestamp]],
) -> Optional[str]:
    """Standardize datetime/date values to ISO 8601 format for telemetry.

    This function converts various datetime formats (DICOM datetime, ISO dates,
    datetime objects) into a consistent ISO 8601 format: YYYY-MM-DDTHH:MM:SS.fffZ

    Args:
        value: The datetime value to standardize. Can be:
            - DICOM datetime string: "YYYYMMDDHHMMSS.ffffff" or "YYYYMMDDHHMMSS"
            - DICOM date string: "YYYYMMDD"
            - ISO date string: "YYYY-MM-DD"
            - datetime.date object
            - datetime.datetime object
            - pd.Timestamp object
            - None

    Returns:
        Standardized datetime string in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.fffZ),
        or None if the value is None or cannot be parsed.

    Examples:
        >>> standardize_datetime_for_telemetry("20240304154545.000")
        "2024-03-04T15:45:45.000Z"
        >>> standardize_datetime_for_telemetry("20240304")
        "2024-03-04T00:00:00.000Z"
        >>> standardize_datetime_for_telemetry("2025-05-07")
        "2025-05-07T00:00:00.000Z"
    """
    if value is None:
        return None

    try:
        # Handle pandas Timestamp
        if isinstance(value, pd.Timestamp):
            dt = value.to_pydatetime()
            # Format with milliseconds
            return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        # Handle datetime.datetime object
        if isinstance(value, datetime.datetime):
            # Format with milliseconds
            return value.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        # Handle datetime.date object (no time component)
        if isinstance(value, datetime.date):
            # Add midnight time
            return f"{value.isoformat()}T00:00:00.000Z"

        # Handle string values
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None

            # Try to parse DICOM datetime format: YYYYMMDDHHMMSS.ffffff or
            # YYYYMMDDHHMMSS
            if len(value) >= 8 and value[:8].isdigit():
                # Extract date part
                date_str = value[:8]
                year = int(date_str[0:4])
                month = int(date_str[4:6])
                day = int(date_str[6:8])

                # Check if there's a time component (length > 8)
                if len(value) > 8:
                    # Extract time part (HHMMSS.ffffff)
                    time_str = value[8:]

                    # Parse hour, minute, second
                    hour = int(time_str[0:2]) if len(time_str) >= 2 else 0
                    minute = int(time_str[2:4]) if len(time_str) >= 4 else 0
                    second = int(time_str[4:6]) if len(time_str) >= 6 else 0

                    # Parse fractional seconds if present
                    microsecond = 0
                    if len(time_str) > 6 and "." in time_str:
                        frac_str = time_str[7:]  # After the dot
                        # Pad or truncate to 6 digits (microseconds)
                        frac_str = frac_str.ljust(6, "0")[:6]
                        microsecond = int(frac_str)

                    dt = datetime.datetime(
                        year, month, day, hour, minute, second, microsecond
                    )
                    # Format with milliseconds (first 3 digits of microseconds)
                    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
                else:
                    # Date only, add midnight time
                    dt = datetime.datetime(year, month, day, 0, 0, 0)
                    return f"{dt.isoformat()}.000Z"

            # Try to parse ISO date format: YYYY-MM-DD
            if "-" in value and len(value) == 10:
                date_obj = datetime.date.fromisoformat(value)
                dt = datetime.datetime(
                    date_obj.year, date_obj.month, date_obj.day, 0, 0, 0
                )
                return f"{dt.isoformat()}.000Z"

            # Try generic parsing as fallback
            _logger.debug(f"Attempting generic datetime parsing for value: {value}")
            # This will handle various ISO datetime formats
            dt = pd.to_datetime(value)
            if isinstance(dt, pd.Timestamp):
                return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    except Exception as e:
        _logger.warning(
            f"Failed to standardize datetime value '{value}' for telemetry: {e}"
        )
        return None


def _modify_column(
    column: Union[np.ndarray, pd.Series],
    modifier_dict: DataPathModifiers,
) -> Union[np.ndarray, pd.Series]:
    """Modify the given column.

    Args:
        column: The column you are operating on.
        modifier_dict: A dictionary with the key as the
            prefix/suffix and the value to be prefixed/suffixed.
    """
    # Get the modifier dictionary:
    for modifier_type, modifier_string in modifier_dict.items():
        # TypedDicts mark values as object() so have to reassure mypy
        modifier_string = cast(str, modifier_string)

        if modifier_type == "prefix":
            column = modifier_string + column.astype(str)

        elif modifier_type == "suffix":
            column = column.astype(str) + modifier_string
    return column


def _modify_file_paths(
    data: pd.DataFrame, modifiers: dict[str, DataPathModifiers]
) -> None:
    """Modifies image file paths if provided.

    Args:
        data: The dataframe to modify.
        modifiers: A dictionary with the column name and
            prefix and/or suffix to modify file path.
    """
    for column_name in modifiers:
        # Get the modifier dictionary:
        modifier_dict = modifiers[column_name]
        data[column_name] = _modify_column(data[column_name], modifier_dict)


@contextmanager
def task_running_context_manager(
    datasource: base_source.BaseSource,
) -> Generator[base_source.BaseSource, None, None]:
    """A context manager to temporarily set a datasource in a "task running" context."""
    old_status = datasource.is_task_running
    try:
        datasource.is_task_running = True
        yield datasource
    finally:
        datasource.is_task_running = old_status


def load_data_in_memory(
    datasource: base_source.BaseSource, **kwargs: Any
) -> pd.DataFrame:
    """Load all data from a datasource into memory and return a singular DataFrame.

    Args:
        datasource: the datasource to load from.
        kwargs: kwargs to pass through to the underlying yield_data() call.
    """
    _logger.warning(
        f'Attempting to load all data from datasource "{datasource}" into memory.'
    )
    with task_running_context_manager(datasource):
        return pd.concat(datasource.yield_data(**kwargs), axis="index")


class FileSystemFilter:
    """Filter files based on various criteria.

    Args:
        file_extension: File extension(s) of the data files. If None, all files
            will be searched. Can either be a single file extension or a list of
            file extensions. Case-insensitive. Defaults to None.
        strict_file_extension: Whether File loading should be strictly done on files
            with the explicit file extension provided. If set to True will only load
            those files in the dataset. Otherwise, it will scan the given path
            for files of the same type as the provided file extension. Only
            relevant if `file_extension` is provided. Defaults to False.
        file_creation_min_date: The oldest possible date to consider for file
            creation. If None, this filter will not be applied. Defaults to None.
        file_modification_min_date: The oldest possible date to consider for file
            modification. If None, this filter will not be applied. Defaults to None.
        file_creation_max_date: The newest possible date to consider for file
            creation. If None, this filter will not be applied. Defaults to None.
        file_modification_max_date: The newest possible date to consider for file
            modification. If None, this filter will not be applied. Defaults to None.
        min_file_size: The minimum file size in megabytes to consider. If None, all
            files will be considered. Defaults to None.
        max_file_size: The maximum file size in megabytes to consider. If None, all
            files will be considered. Defaults to None.
    """

    def __init__(
        self,
        file_extension: Optional[SingleOrMulti[str]] = None,
        strict_file_extension: bool = False,
        file_creation_min_date: Optional[Union[Date, DateTD]] = None,
        file_modification_min_date: Optional[Union[Date, DateTD]] = None,
        file_creation_max_date: Optional[Union[Date, DateTD]] = None,
        file_modification_max_date: Optional[Union[Date, DateTD]] = None,
        min_file_size: Optional[float] = None,
        max_file_size: Optional[float] = None,
    ) -> None:
        self.file_extension: Optional[list[str]] = None
        if file_extension:
            file_extension_: list[str] = (
                [file_extension]
                if isinstance(file_extension, str)
                else list(file_extension)
            )
            self.file_extension = [
                f".{fe}" if not fe.startswith(".") else fe for fe in file_extension_
            ]

        self.strict_file_extension = (
            strict_file_extension if self.file_extension is not None else False
        )

        self.file_creation_min_date: Optional[datetime.date] = get_datetime(
            file_creation_min_date
        )
        self.file_modification_min_date: Optional[datetime.date] = get_datetime(
            file_modification_min_date
        )
        self.file_creation_max_date: Optional[datetime.date] = get_datetime(
            file_creation_max_date
        )
        self.file_modification_max_date: Optional[datetime.date] = get_datetime(
            file_modification_max_date
        )

        if not any(
            [
                self.file_creation_min_date,
                self.file_modification_min_date,
                self.file_creation_max_date,
                self.file_modification_max_date,
            ]
        ):
            _logger.warning(
                "No file creation or modification min/max dates provided. All files in "
                "the directory will be considered which may impact performance."
            )

        # Set the min and max file sizes in megabytes
        self.min_file_size: Optional[float] = min_file_size
        self.max_file_size: Optional[float] = max_file_size

        if not self.min_file_size and not self.max_file_size:
            _logger.warning(
                "No file size limits provided. All files in the directory will be "
                "considered which may impact performance."
            )

    def _filter_file_by_extension(self, file: Union[str, os.PathLike]) -> bool:
        """Return True if file matches extension/file type criteria, False otherwise.

        If allowed_extensions is provided, files will be matched against those,
        disallowed if their file types aren't in that set. If not provided, as long
        as a file type can be determined, it will be allowed.

        If strict is True, only explicit file extensions will be checked. Otherwise,
        if a file has no extension, the extension will be inferred based on file type.
        """
        file = Path(file)

        allowed_extensions_lower: Optional[set[str]]
        if self.file_extension is not None:
            allowed_extensions_lower = {x.lower() for x in self.file_extension}
        else:
            allowed_extensions_lower = None

        # Order: file extension, guessed extension
        if self.strict_file_extension:
            file_type = file.suffix
        else:
            file_type = file.suffix or f".{guess_extension(file)}"

        # If guessing the extension failed the result is ".None"
        if file_type == ".None":
            _logger.warning(
                f"Could not determine file type of '{file.resolve()}'. Ignoring..."
            )
            return False

        # Otherwise, is it of the correct file type
        elif (
            allowed_extensions_lower is not None
            and file_type.lower() not in allowed_extensions_lower
        ):
            return False
        else:
            return True

    def _filter_file_by_dates(
        self, file: Union[str, os.PathLike], stat: Optional[os.stat_result] = None
    ) -> bool:
        """True iff file matches creation/modification date criteria."""
        try:
            file = Path(file)

            # We want to do this just once here, to avoid having to make multiple
            # `.stat()` calls later
            if stat is None:
                stat = os.stat(file)

            # Check creation date in range
            if self.file_creation_min_date or self.file_creation_max_date:
                file_creation_date = get_file_creation_date(file, stat)

                # Check if before min
                if (
                    self.file_creation_min_date
                    and file_creation_date < self.file_creation_min_date
                ):
                    return False

                # Check if after max
                if (
                    self.file_creation_max_date
                    and file_creation_date > self.file_creation_max_date
                ):
                    return False

            # Check modification date criteria
            if self.file_modification_min_date or self.file_modification_max_date:
                file_modification_date = get_file_last_modification_date(file, stat)

                # Check if before min
                if (
                    self.file_modification_min_date
                    and file_modification_date < self.file_modification_min_date
                ):
                    return False

                # Check if after max
                if (
                    self.file_modification_max_date
                    and file_modification_date > self.file_modification_max_date
                ):
                    return False

            # If we've gotten here, must match all of the above criteria
            return True
        except Exception as e:
            _logger.warning(
                f"Could not determine creation/modification date of '{file}';"
                f" error was: {e}. Ignoring..."
            )
            return False

    def _filter_file_by_size(
        self, file: Union[str, os.PathLike], stat: Optional[os.stat_result] = None
    ) -> bool:
        """True iff file matches file size criteria."""
        try:
            file = Path(file)

            # We want to do this just once here, to avoid having to make multiple
            # `.stat()` calls later
            if stat is None:
                stat = os.stat(file)

            file_size = get_file_size(file, stat)

            # Check if too small
            if self.min_file_size and file_size < (
                self.min_file_size * NUM_BYTES_IN_A_MEGABYTE
            ):
                return False

            # Check if too large
            if self.max_file_size and file_size > (
                self.max_file_size * NUM_BYTES_IN_A_MEGABYTE
            ):
                return False

            # If we've gotten here, must match all of the above criteria
            return True
        except Exception as e:
            _logger.warning(
                f"Could not determine size of '{file}'; error was: {e}. Ignoring..."
            )
            return False

    def log_files_found_with_extension(
        self, num_found_files: int, interim: bool = True
    ) -> None:
        """Log the files found with the given extension."""
        if interim:
            msg = "File-system filters in progress: "
        else:
            msg = "File-system filters final: "

        if self.strict_file_extension and self.file_extension:
            msg += (
                f"Found {num_found_files} files with the explicit extensions "
                f"{self.file_extension} and matching other file-system criteria"
            )
        elif self.file_extension:  # and strict=False
            msg += (
                f"Found {num_found_files} files that match file types "
                f"{self.file_extension} and matching other file-system criteria"
            )
        else:
            msg += f"Found {num_found_files} files matching file-system criteria"

        if interim:
            _logger.info(msg + " so far.", extra={"sample": True})
        else:
            _logger.info(msg + ".")

    @overload
    def check_skip_file(
        self, entry: os.DirEntry, path: None = ..., stat: None = ...
    ) -> tuple[bool, Optional[FileSkipReason]]: ...

    @overload
    def check_skip_file(
        self,
        entry: None = ...,
        path: str | os.PathLike = ...,
        stat: Optional[os.stat_result] = ...,
    ) -> tuple[bool, Optional[FileSkipReason]]: ...

    def check_skip_file(
        self,
        entry: Optional[os.DirEntry] = None,
        path: Optional[str | os.PathLike] = None,
        stat: Optional[os.stat_result] = None,
    ) -> tuple[bool, Optional[FileSkipReason]]:
        """Filter files based on the criteria provided.

        Check the following things in order:
        - is this a file?
        - is this an allowed type of file?
        - does this file meet the date criteria?
        - does this file meet the file size criteria?

        Either `entry` OR `path` should be supplied. If path is supplied, `stat` may
        be optionally provided, but will be newly read if not.

        If both `entry` and `path` are provided, then `entry` will take precedence.

        Args:
            entry: The file to check as an `os.DirEntry` object,
                as from `os.scandir()`. Mutually exclusive with `path`.
            path: The file path to check. Mutually exclusive with `entry`.
            stat: The `os.stat()` details associated with `path`.
                Optional, will be read directly if not provided.

        Returns:
            True if the file should be skipped, False otherwise
        """
        if entry is None and path is None:
            _logger.error(
                "Neither `path` nor `entry` were provided;"
                " exactly one should be provided."
            )
            raise ValueError(
                "Neither `path` nor `entry` were provided;"
                " exactly one should be provided."
            )

        if entry is not None and path is not None:
            _logger.warning(
                f"Both `path` ({path}) and `entry` ({entry.path}) were provided."
                f" Only one should be provided."
                f" Giving precendence to `entry`."
            )
            path = None

        if path is None and stat is not None:
            _logger.warning(
                "`stat` was provided but without `path`. Setting `stat` to None."
            )
            stat = None

        # This is the fully resolved path of the entry
        path_: Path
        if entry is not None:
            path_ = Path(entry.path)
        else:  # path is not None
            assert path is not None  # nosec[assert_used] # Reason: This is only to make mypy happy; checks above ensure that path is not None in this branch # noqa: E501
            path_ = Path(path)

        # Get the `os.stat()` details here so that we can avoid multiple calls.
        # We use entry.stat if possible as this makes use of the potential caching
        # mechanisms of scandir().
        stat_: os.stat_result
        if entry is not None:
            stat_ = entry.stat()
        else:  # path is not None
            if stat is not None:
                stat_ = stat
            else:
                stat_ = path_.stat()

        # - is this a file?
        if not is_file(entry if entry is not None else path_, stat_):
            return True, FileSkipReason.NOT_A_FILE

        # - is this an allowed type of file?
        if not self._filter_file_by_extension(path_):
            return True, FileSkipReason.EXTENSION_NOT_ALLOWED

        # - does this file meet the date criteria?
        if not self._filter_file_by_dates(path_, stat_):
            return True, FileSkipReason.DATE_OUT_OF_RANGE

        # - does this file meet the file size criteria?
        if not self._filter_file_by_size(path_, stat_):
            return True, FileSkipReason.SIZE_OUT_OF_RANGE

        return False, None


class FileSkipReason(Enum):
    """Enumeration of all possible reasons why a file might be skipped."""

    # Any changes to the values here should be reflected in
    # both "File Skip Reason Codes" Notion Page and
    # "Dataset Metrics - Production" Grafana dashboard.
    # For the Grafana dashboard, the Dataset Diagnostic Statistics panel
    # needs to be edited for the new codes (convert, group by, organise transforms).
    # For the Grafana dashboard, the Dataset Metrics Documentation panels
    # markdown needs to be updated.

    # Filesystem-level filtering (1-7)
    NOT_A_FILE = 1
    EXTENSION_NOT_ALLOWED = 2
    DATE_OUT_OF_RANGE = 3
    SIZE_OUT_OF_RANGE = 4
    PROCESSING_ERROR = 5
    ALREADY_SKIPPED = 6
    MAX_FILES_EXCEEDED = 7

    # Datasource-specific filtering (8)
    DATASOURCE_FILTER_FAILED = 8

    # DICOM-specific issues (9-15)
    DICOM_LOAD_FAILED = 9
    DICOM_NO_IMAGES_SOP_CLASS = 10
    # While the following two may seem similar, they are raised at different
    # stages in the dicom processing. Essentially, NO_PIXEL_DATA gets
    # used in the _read_image_ds_elements and in _process_conventional_dicom ,
    # i.e. when actually trying to process the pixel data of the dicom. Even
    # though all skipping on dicoms with no images should happen at that stage,
    # we still have an additional skip here if we end up reading the data and
    # have no DICOM_IMAGE_ATTRIBUTE. This should technically not happen and
    # should have been caught by the NO_PIXEL_DATA, and thought it could indicate
    # something is wrong in our Pixel data processing.
    DICOM_NO_IMAGE_DATA = 11
    DICOM_NO_PIXEL_DATA = 12
    DICOM_PIXEL_EXTRACTION_FAILED = 13
    DICOM_EMPTY_FILE = 14
    DICOM_UNEXPECTED_ERROR = 15

    # Ophthalmology-specific issues (16-21)
    OPHTH_DOB_OUT_OF_RANGE = 16
    OPHTH_DOB_UNAVAILABLE = 17
    OPHTH_BSCAN_COUNT_OUT_OF_RANGE = 18
    OPHTH_BSCAN_COUNT_UNAVAILABLE = 19
    OPHTH_MODALITY_MISMATCH = 20
    OPHTH_PROPERTY_EXTRACTION_FAILED = 21

    # Private Eye issues (22-24)
    PRIVATE_EYE_NO_PARSER = 22
    PRIVATE_EYE_PROCESSING_FAILED = 23
    PRIVATE_EYE_EMPTY_RESULT = 24

    # Image processing issues (25-26)
    IMAGE_PROCESSING_FAILED = 25
    IMAGE_EMPTY_DATA = 26

    # Zeiss-specific issues (27)
    DICOM_UNSUPPORTED_ZEISS_MODALITY = 27

    # Ophthalmology required fields (28)
    OPHTH_MISSING_REQUIRED_FIELD = 28


# Mapping of skip reasons to human-readable descriptions
SKIP_REASON_DESCRIPTIONS: Dict[FileSkipReason, str] = {
    FileSkipReason.NOT_A_FILE: "Path is not a regular file",
    FileSkipReason.EXTENSION_NOT_ALLOWED: "File extension not in allowed list",
    FileSkipReason.DATE_OUT_OF_RANGE: "File creation/modification date outside allowed range",  # noqa: E501
    FileSkipReason.SIZE_OUT_OF_RANGE: "File size outside allowed range",
    FileSkipReason.PROCESSING_ERROR: "Error during file iteration/processing",
    FileSkipReason.ALREADY_SKIPPED: "File was previously marked as skipped",
    FileSkipReason.MAX_FILES_EXCEEDED: "Maximum number of files limit exceeded",
    FileSkipReason.DATASOURCE_FILTER_FAILED: "Failed datasource-specific filters",
    FileSkipReason.DICOM_LOAD_FAILED: "DICOM file could not be loaded",
    FileSkipReason.DICOM_NO_IMAGES_SOP_CLASS: "DICOM SOP Class indicates no images",
    FileSkipReason.DICOM_NO_IMAGE_DATA: "DICOM file contains no image data",
    FileSkipReason.DICOM_NO_PIXEL_DATA: "DICOM file contains no pixel data",
    FileSkipReason.DICOM_PIXEL_EXTRACTION_FAILED: "Failed to extract pixel data from DICOM",  # noqa: E501
    FileSkipReason.DICOM_EMPTY_FILE: "DICOM file is empty after processing",
    FileSkipReason.DICOM_UNEXPECTED_ERROR: "Unexpected error processing DICOM file",
    FileSkipReason.OPHTH_DOB_OUT_OF_RANGE: "Patient date of birth outside specified range",  # noqa: E501
    FileSkipReason.OPHTH_DOB_UNAVAILABLE: "Patient date of birth could not be extracted",  # noqa: E501
    FileSkipReason.OPHTH_BSCAN_COUNT_OUT_OF_RANGE: "B-scan count outside specified range",  # noqa: E501
    FileSkipReason.OPHTH_BSCAN_COUNT_UNAVAILABLE: "B-scan count could not be determined",  # noqa: E501
    FileSkipReason.OPHTH_MODALITY_MISMATCH: "File modality does not match required modality",  # noqa: E501
    FileSkipReason.OPHTH_PROPERTY_EXTRACTION_FAILED: "Failed to extract required DICOM properties",  # noqa: E501
    FileSkipReason.PRIVATE_EYE_NO_PARSER: "No private eye parser available for file extension",  # noqa: E501
    FileSkipReason.PRIVATE_EYE_PROCESSING_FAILED: "Private eye processing failed",
    FileSkipReason.PRIVATE_EYE_EMPTY_RESULT: "Private eye processing returned no data",
    FileSkipReason.IMAGE_PROCESSING_FAILED: "Image file processing failed",
    FileSkipReason.IMAGE_EMPTY_DATA: "Image processing returned no data",
    FileSkipReason.DICOM_UNSUPPORTED_ZEISS_MODALITY: "DICOM file has unsupported Zeiss modality",  # noqa: E501
    FileSkipReason.OPHTH_MISSING_REQUIRED_FIELD: "File missing one or more required fields for calculation",  # noqa: E501
}
ERROR_REASONS: set[FileSkipReason] = {
    FileSkipReason.PROCESSING_ERROR,
    FileSkipReason.DICOM_LOAD_FAILED,
    FileSkipReason.DICOM_PIXEL_EXTRACTION_FAILED,
    FileSkipReason.DICOM_UNEXPECTED_ERROR,
    FileSkipReason.OPHTH_PROPERTY_EXTRACTION_FAILED,
    FileSkipReason.PRIVATE_EYE_PROCESSING_FAILED,
    FileSkipReason.IMAGE_PROCESSING_FAILED,
}


def get_skip_reason_description(reason: FileSkipReason) -> str:
    """Get human-readable description for a skip reason.

    Args:
        reason: The skip reason enum value.

    Returns:
        Human-readable description of the skip reason.
    """
    return SKIP_REASON_DESCRIPTIONS.get(reason, f"Unknown skip reason: {reason}")


def get_file_size_str(filename: str | os.PathLike) -> str:
    """Get file size as a human-readable string.

    Args:
        filename: Path to the file.

    Returns:
        Human-readable file size string, or 'unknown' if file doesn't exist.
    """
    try:
        size_bytes = float(os.path.getsize(filename))
        if size_bytes == 0:
            return "0 bytes"

        # Convert bytes to human-readable format
        for unit in ["bytes", "KB", "MB", "GB", "TB"]:
            # loop through the units and
            # return when getting to the right one
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        # if none of the given ones match, assume petabytes (PB)
        return f"{size_bytes:.1f} PB"
    except Exception as e:
        return f"Unknown size, raised {str(e)}"


def calculate_dimensionality(data: dict[str, Any]) -> str:
    """Calculate the dimensionality of a file.

    Tries to extract dimensionality from DICOM metadata first (Number of Frames,
    Rows, Columns). If metadata is unavailable, falls back to extracting dimensions
    from actual pixel data arrays in the data dictionary.

    Args:
        data: The data to calculate the dimensionality from.

    Returns:
        The dimensionality of the file as a string in format "(frames, rows, cols)".
        Returns "Unknown" if dimensions cannot be determined.
    """
    # Try metadata first (fastest and most reliable when available)
    number_of_frames = data.get("Number of Frames")
    rows = data.get("Rows")
    columns = data.get("Columns")

    if rows is not None and columns is not None:
        return f"({str(number_of_frames)}, {str(rows)}, {str(columns)})"

    # Fallback: Extract dimensions from actual pixel data arrays
    # Look for image attribute keys containing numpy arrays
    for key in data:
        # Check if this is an image data key
        if any(prefix in key for prefix in ["Pixel Data", "SLO Image Data"]):
            value = data[key]
            # Check if it's a numpy array (not "<SKIPPED>" string or None)
            if isinstance(value, np.ndarray):
                shape = value.shape
                # Handle 2D vs 3D arrays
                if len(shape) == 2:
                    # 2D image: (rows, cols) - assume single frame
                    return f"(1, {shape[0]}, {shape[1]})"
                elif len(shape) == 3:
                    # 3D image: (frames, rows, cols)
                    return f"({shape[0]}, {shape[1]}, {shape[2]})"
                # Found a valid array, exit after first valid one
                break

    return "Unknown"
