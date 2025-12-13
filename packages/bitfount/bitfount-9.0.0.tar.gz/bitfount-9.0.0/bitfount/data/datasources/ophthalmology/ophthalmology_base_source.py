"""Data source for loading ophthalmology files using private-eye."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
import datetime
import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, TypedDict, Union

import desert
from marshmallow import fields, validate
import numpy as np

from bitfount.data.datasources.base_source import FileSystemIterableSourceInferrable
from bitfount.data.datasources.ophthalmology.ophth_ds_types import (
    DEFAULT_REQUIRED_FIELDS_FOR_CALCULATIONS,
    OphthalmologyModalityType,
)
from bitfount.data.datasources.types import Date, DateTD
from bitfount.data.datasources.utils import FileSkipReason, get_datetime
from bitfount.data.exceptions import DataNotAvailableError
from bitfount.types import UsedForConfigSchemas
from bitfount.utils import delegates

if TYPE_CHECKING:
    from typing_extensions import NotRequired

logger = logging.getLogger(__name__)

OPHTHALMOLOGY_MODALITIES: list[str] = ["OCT", "SLO"]
OCT_ACQUISITION_DEVICE_TYPE = "Optical Coherence Tomography Scanner"
SLO_ACQUISITION_DEVICE_TYPE = "Scanning Laser Ophthalmoscope"
ACQUISITION_DEVICE_TYPE_MODALITY_MAPPING: dict[str, OphthalmologyModalityType] = {
    OCT_ACQUISITION_DEVICE_TYPE: "OCT",
    "OCT": "OCT",
    SLO_ACQUISITION_DEVICE_TYPE: "SLO",
    "SLO": "SLO",
}
IMAGE_COLUMN_PREFIX: str = "Pixel Data"
SLO_IMAGE_ATTRIBUTE: str = "SLO Image Data"


@dataclass
class OphthalmologyDataSourceArgs(UsedForConfigSchemas):
    """Arguments for ophthalmology modality data.

    More information about the acquisition device types can be found in the
    DICOM standard supplements 91 and 110.

    Args:
        modality: The modality of the data. Must be either 'OCT', 'SLO' or None. OCT
            refers to Optical Coherence Tomography (OCT), typically these are a series
            of 2D images used to show a cross-section of the tissue layers in the
            retina (specifically the macula), combined to form a 3D image. SLO
            refers to Scanning Laser Ophthalmoscope (SLO), typically referred
            to as an 'en-face' image of the retina (specifically the macula). Defaults
            to None.
        match_slo: Only relevant if `modality` is 'OCT'. Whether to match SLO files
            to OCT files on a best effort basis. If true, patient name, date of birth
            and laterality must be an exact match on the OCT and SLO files. Acquistion
            date and time must be within 24 hours of each other. Defaults to True.
        drop_row_on_missing_slo: Only relevant if `modality` is 'OCT' and `match_slo`
            is True. Whether to drop the OCT row if the corresponding SLO file is
            missing i.e. ignore the OCT file. Defaults to False.
        minimum_dob: The minimum date of birth to consider. If not None, only patients
            with a date of birth greater than or equal to this value will be considered.
            Defaults to None.
        maximum_dob: The maximum date of birth to consider. If not None, only patients
            with a date of birth less than or equal to this value will be considered.
            Defaults to None.
        minimum_num_bscans: The minimum number of B-scans to consider. If not None, only
            files with a number of B-scans greater than or equal to this value will be
            considered. Defaults to None.
        maximum_num_bscans: The maximum number of B-scans to consider. If not None, only
            files with a number of B-scans less than or equal to this value will be
            considered. Defaults to None.
        check_required_fields: Whether to filter out files that are missing required
            fields for calculations. Defaults to False.
        required_field_names: List of required field names to check for. If None,
            uses default required fields for calculations. If specified, overrides the
            default required fields for calculations.
    """

    modality: OphthalmologyModalityType = desert.field(
        fields.String(validate=validate.OneOf(("OCT", "SLO")), allow_none=True),
        default=None,
    )
    match_slo: bool = False
    drop_row_on_missing_slo: bool = False

    # desert typing is actually stricter than the mypy typing as Date and DateTD will
    # look the same when serialized so we restrict to Date only
    minimum_dob: Optional[Union[Date, DateTD]] = desert.field(
        fields.Nested(desert.schema_class(Date), allow_none=True), default=None
    )
    maximum_dob: Optional[Union[Date, DateTD]] = desert.field(
        fields.Nested(desert.schema_class(Date), allow_none=True), default=None
    )

    minimum_num_bscans: Optional[int] = None
    maximum_num_bscans: Optional[int] = None

    check_required_fields: bool = False
    required_field_names: Optional[list[str]] = None

    def __post_init__(self) -> None:
        # OCT/SLO strings kept for private-eye source compatibility
        self.oct_string = "OCT"
        self.slo_string = "SLO"

        if self.modality is None:
            if self.match_slo or self.drop_row_on_missing_slo:
                raise ValueError(
                    "If `modality` is not specified, then `match_slo` and "
                    "`drop_row_on_missing_slo` must be False."
                )
        elif self.modality == self.oct_string:
            if not self.match_slo and self.drop_row_on_missing_slo:
                logger.warning(
                    "`drop_row_on_missing_slo` is only relevant if `match_slo` is True."
                    " It will be ignored."
                )

        elif self.modality == self.slo_string:
            if self.match_slo or self.drop_row_on_missing_slo:
                raise ValueError(
                    "If `modality` is 'SLO', then `match_slo` and "
                    "`drop_row_on_missing_slo` must be False."
                )
        else:
            raise ValueError(
                f"Unsupported modality: '{self.modality}'. "
                "If specified, must be one of "
                f"{', '.join(OPHTHALMOLOGY_MODALITIES)}."
            )

        # Set default required field names if not specified
        if self.required_field_names is None:
            self.required_field_names = DEFAULT_REQUIRED_FIELDS_FOR_CALCULATIONS.copy()


class _OphthalmologyDataSourceArgsTD(TypedDict):
    """Typed dict form of OphthalmologyDataSourceArgs dataclass."""

    modality: OphthalmologyModalityType
    match_slo: NotRequired[bool]
    drop_row_on_missing_slo: NotRequired[bool]
    minimum_dob: NotRequired[DateTD]
    maximum_dob: NotRequired[DateTD]
    minimum_num_bscans: NotRequired[int]
    maximum_num_bscans: NotRequired[int]
    check_required_fields: NotRequired[bool]
    required_field_names: NotRequired[list[str]]


@delegates()
class _OphthalmologySource(FileSystemIterableSourceInferrable, ABC):
    """Base OphthalmologySource.

    Args:
        path: Path to the directory which contains the data files. Subdirectories
            will be searched recursively.
        ophthalmology_args: Arguments for ophthalmology modality data.
        **kwargs: Additional keyword arguments to pass to the base class.

    Raises:
        ValueError: If the minimum DOB is greater than the maximum DOB.
        ValueError: If the minimum number of B-scans is greater than the maximum number
            of B-scans.
    """

    def __init__(
        self,
        path: Union[str, os.PathLike],
        ophthalmology_args: Optional[
            Union[OphthalmologyDataSourceArgs, _OphthalmologyDataSourceArgsTD]
        ] = None,
        **kwargs: Any,
    ) -> None:
        # Parse the ophthalmology arguments, converting from the dict-form to
        # dataclass-form if needed
        if ophthalmology_args is None:
            self.ophthalmology_args = OphthalmologyDataSourceArgs()
        elif isinstance(ophthalmology_args, OphthalmologyDataSourceArgs):
            self.ophthalmology_args = ophthalmology_args
        else:
            self.ophthalmology_args = OphthalmologyDataSourceArgs(**ophthalmology_args)

        # DOB conversion and validation
        self.minimum_dob_date: Optional[datetime.date] = get_datetime(
            self.ophthalmology_args.minimum_dob
        )
        self.maximum_dob_date: Optional[datetime.date] = get_datetime(
            self.ophthalmology_args.maximum_dob
        )
        if (
            self.minimum_dob_date
            and self.maximum_dob_date
            and self.minimum_dob_date > self.maximum_dob_date
        ):
            raise ValueError(
                "The minimum DOB must be less than or equal to the maximum DOB."
            )

        # B-scan validation
        self.minimum_num_bscans: Optional[int] = (
            self.ophthalmology_args.minimum_num_bscans
        )
        self.maximum_num_bscans: Optional[int] = (
            self.ophthalmology_args.maximum_num_bscans
        )
        if (
            self.minimum_num_bscans
            and self.maximum_num_bscans
            and self.minimum_num_bscans > self.maximum_num_bscans
        ):
            raise ValueError(
                "The minimum number of B-scans must be less than or equal to the "
                "maximum number of B-scans."
            )

        super().__init__(path=path, **kwargs)

        # Cache for expensive additional_metrics calculation
        self._cached_additional_metrics: Optional[dict[str, Any]] = None

        # Required fields configuration (must be after super().__init__)
        self.check_required_fields: bool = self.ophthalmology_args.check_required_fields
        # Only initialize required field names if the filter is enabled
        self.required_field_names: list[str]
        if self.check_required_fields:
            # Use configured required field names, or default if not provided
            self.required_field_names = (
                self.ophthalmology_args.required_field_names
                if self.ophthalmology_args.required_field_names is not None
                else DEFAULT_REQUIRED_FIELDS_FOR_CALCULATIONS.copy()
            )
        else:
            self.required_field_names = []

        if self.minimum_dob_date or self.maximum_dob_date:
            self._datasource_filters_to_apply.append(self._filter_files_by_dob)
        if self.minimum_num_bscans or self.maximum_num_bscans:
            self._datasource_filters_to_apply.append(self._filter_files_by_num_bscans)
        if self.check_required_fields:
            self._datasource_filters_to_apply.append(
                self._filter_files_by_required_fields
            )

    @abstractmethod
    def _get_dob_from_cache(self, file_names: list[str]) -> dict[str, datetime.date]:
        """Get the date of birth from the cache.

        Args:
            file_names: The filenames of the files to be processed.

        Returns:
            The date of birth of the patient or None if the field is missing.
        """
        raise NotImplementedError

    @abstractmethod
    def _get_num_bscans_from_cache(self, file_names: list[str]) -> dict[str, int]:
        """Get the number of B-scans from the cache.

        Args:
            file_names: The filenames of the files to be processed.

        Returns:
            The number of B-scans in the file or None if the field is missing.
        """
        raise NotImplementedError

    @staticmethod
    def _convert_string_to_datetime(
        date_str: str, fmt: str = "%Y%m%d"
    ) -> datetime.datetime:
        """Convert a date string to a datetime object.

        Args:
            date_str: The date string to be converted.
            fmt: The format to use to parse the date string.

        Returns:
            The datetime object.
        """
        return datetime.datetime.strptime(date_str, fmt)

    def _get_oct_images_from_paths(
        self, save_path: Path, file_prefix: str
    ) -> list[Path]:
        """Retrieve OCT PNG images that were generated from `file_prefix`.

        NOTE: This method of getting the OCT images is deprecated and only
        kept for private-eye compatibility.
        """
        oct_file_pattern = f"*{file_prefix}"
        if self.ophthalmology_args:
            oct_file_pattern += f"*-{self.ophthalmology_args.oct_string}*"
        return [
            x
            for x in save_path.glob(oct_file_pattern)
            if x.is_file() and x.suffix == ".png"
        ]

    def _get_images_from_dict(
        self, image_arrays: list[Mapping[str, np.ndarray]]
    ) -> dict[str, np.ndarray]:
        """Retrieve OCT and SLO image arrays.

        NOTE: This method of getting the OCT images is deprecated and only
        kept for private-eye compatibility.
        """
        data = {}
        if self.ophthalmology_args and self.ophthalmology_args.oct_string:
            for item in image_arrays:
                for key, value in item.items():
                    modality, idx = key.split("-")
                    if (
                        self.ophthalmology_args.oct_string
                        and self.ophthalmology_args.oct_string in modality
                    ):
                        img_col_name = f"{IMAGE_COLUMN_PREFIX} {idx}"
                        data[img_col_name] = value
                        self.image_columns.add(img_col_name)
                    elif (
                        self.ophthalmology_args.slo_string
                        and self.ophthalmology_args.slo_string in modality
                    ):
                        slo_img_col_name = f"{SLO_IMAGE_ATTRIBUTE} {idx}"
                        data[slo_img_col_name] = value
                        self.image_columns.add(slo_img_col_name)
        else:
            logger.warning("Ophthalmology args not set, no images will be loaded.")

        return data

    def _get_slo_images_from_paths(
        self, save_path: Path, file_prefix: str
    ) -> list[Path]:
        """Retrieve SLO PNG images that were generated from `file_prefix`.

        NOTE: This method of getting the OCT images is deprecated and only
        kept for private-eye compatibility.
        """
        slo_file_pattern = f"*{file_prefix}"
        if self.ophthalmology_args:
            slo_file_pattern += f"*-{self.ophthalmology_args.slo_string}*"
        return [
            x
            for x in save_path.glob(slo_file_pattern)
            if x.is_file() and x.suffix == ".png"
        ]

    def _filter_files_by_dob(self, file_names: list[str]) -> list[str]:
        """Filter the files by date of birth based on the ophthalmology_args.

        Args:
            file_names: The list of file names to be filtered.

        Returns:
            The filtered list of file names.
        """
        if not self.minimum_dob_date and not self.maximum_dob_date:
            return file_names

        filtered_file_names: list[str] = []
        dob_datetimes = self._get_dob_from_cache(file_names)

        for file_name in file_names:
            dob_datetime = dob_datetimes.get(file_name)
            if dob_datetime is not None:
                meets_dob_criteria = True
                if self.minimum_dob_date is not None:
                    meets_dob_criteria = dob_datetime >= self.minimum_dob_date
                if meets_dob_criteria and self.maximum_dob_date is not None:
                    meets_dob_criteria = dob_datetime <= self.maximum_dob_date
                if meets_dob_criteria:
                    filtered_file_names.append(file_name)
                else:
                    self.skip_file(file_name, FileSkipReason.OPHTH_DOB_OUT_OF_RANGE)
                    # If the DOB is retrieved but not within the specified
                    # range, then we skip the file.
            else:
                # If the DOB is retrieved as None, then we want to take a more
                # conservative approach and skip the file
                # as we are not certain that the DOB within range.
                self.skip_file(file_name, FileSkipReason.OPHTH_DOB_UNAVAILABLE)

        return filtered_file_names

    def _filter_files_by_num_bscans(self, file_names: list[str]) -> list[str]:
        """Filter the files by number of B-scans.

        Args:
            file_names: The list of file names to be filtered.

        Returns:
            The filtered list of file names.
        """
        if not self.minimum_num_bscans and not self.maximum_num_bscans:
            return file_names

        filtered_file_names: list[str] = []
        num_bscans = self._get_num_bscans_from_cache(file_names)

        for file_name in file_names:
            num_bscans_file = num_bscans.get(file_name)
            if num_bscans_file is None:
                # If the number of B-scans is retrieved as None,
                # then we have to open the file to extract the number of frames.
                # This field gets processed and added to the cache when using
                # the `_get_data` call.
                try:
                    self.get_data([file_name])
                except DataNotAvailableError:
                    # If the file cannot be loaded (e.g., no pixel data),
                    # skip it instead of aborting the entire task.
                    self.skip_file(file_name, FileSkipReason.DICOM_LOAD_FAILED)
                    continue
                num_bscans_file = self._get_num_bscans_from_cache([file_name]).get(
                    file_name
                )
            if num_bscans_file is not None:
                meets_criteria = True
                if self.minimum_num_bscans is not None:
                    meets_criteria = num_bscans_file >= self.minimum_num_bscans
                if meets_criteria and self.maximum_num_bscans is not None:
                    meets_criteria = num_bscans_file <= self.maximum_num_bscans
                if meets_criteria:
                    filtered_file_names.append(file_name)
                else:
                    # If the number of B-scans is retrieved but not within the
                    # specified range, then we skip the file.
                    self.skip_file(
                        file_name, FileSkipReason.OPHTH_BSCAN_COUNT_OUT_OF_RANGE
                    )
            else:
                self.skip_file(file_name, FileSkipReason.OPHTH_BSCAN_COUNT_UNAVAILABLE)
        return filtered_file_names

    def _filter_files_by_required_fields(self, file_names: list[str]) -> list[str]:
        """Filter the files by checking for required fields.

        Args:
            file_names: The list of file names to be filtered.

        Returns:
            The filtered list of file names.
        """
        if not self.required_field_names:
            return file_names

        filtered_file_names: list[str] = []

        for file_name in file_names:
            try:
                # Get data to check if required fields are present and non-empty
                data = self.get_data([file_name])

                if data is None:
                    self.skip_file(
                        file_name,
                        FileSkipReason.OPHTH_PROPERTY_EXTRACTION_FAILED,
                    )
                    continue

                # Check if all required fields are present and non-empty
                has_all_required_fields = True
                for field in self.required_field_names:
                    # Check if the field exists in the dataframe
                    if field not in data.columns:
                        has_all_required_fields = False
                        break

                    # Check if the field has at least one non-null value
                    field_values = data[field].dropna()
                    if field_values.empty:
                        # All values for this field are NaN/null
                        has_all_required_fields = False
                        break

                    # Check if all non-null values are empty strings
                    if all(isinstance(v, str) and v == "" for v in field_values):
                        has_all_required_fields = False
                        break

                if has_all_required_fields:
                    filtered_file_names.append(file_name)
                else:
                    self.skip_file(
                        file_name, FileSkipReason.OPHTH_MISSING_REQUIRED_FIELD
                    )
            except DataNotAvailableError:
                # If the file cannot be loaded, skip it
                self.skip_file(file_name, FileSkipReason.DICOM_LOAD_FAILED)
            except Exception as e:
                # Log and skip on any other error
                logger.warning(
                    f"Error checking required fields for file {file_name}: {e}"
                )
                self.skip_file(
                    file_name, FileSkipReason.OPHTH_PROPERTY_EXTRACTION_FAILED
                )

        return filtered_file_names

    @abstractmethod
    def _extract_metadata_from_skipped_file(
        self, file_path: str
    ) -> list[dict[str, Any]]:
        """Extract metadata from a skipped file for metrics purposes.

        This method should attempt to read basic metadata from a file that was
        previously skipped, without fully processing it. Different ophthalmology
        sources implement this differently:
        - DICOM sources use _attempt_best_effort_metadata_read()
        - Private-eye sources use _process_file(skip_non_tabular_data=True)

        Args:
            file_path: Path to the skipped file.

        Returns:
            A list of metadata dictionaries. May contain multiple entries if a
            file contains data for multiple records (e.g., both eyes). Returns
            empty list if metadata cannot be extracted.
        """
        raise NotImplementedError

    def _get_metrics_from_skipped_files(
        self, fields_to_count: dict[str, str]
    ) -> dict[str, dict[str, int]]:
        """Helper method to retrieve and count metrics from skipped files.

        This shared implementation eliminates code duplication across ophthalmology
        datasources. It handles the common logic of:
        1. Getting list of skipped files from cache
        2. Extracting metadata from each file
        3. Converting to telemetry format
        4. Accumulating counts

        Results are cached to avoid expensive file I/O on repeated calls.

        Args:
            fields_to_count: Dictionary mapping telemetry keys to raw field names.
                Example: {"manufacturer": "Manufacturer", ...}

        Returns:
            Dictionary of accumulated counts per field, or empty dict if no
            metadata could be retrieved.
        """
        # Return cached metrics if available
        if self._cached_additional_metrics is not None:
            logger.debug("Returning cached additional metrics from skipped files")
            return self._cached_additional_metrics

        if not self.data_cache:
            return {}

        logger.debug(
            "No successfully processed data available. "
            "Attempting to retrieve metadata from skipped files."
        )

        # Get list of skipped files from cache
        skipped_files = self.data_cache.get_all_skipped_files()
        if not skipped_files:
            # Cache empty result
            self._cached_additional_metrics = {}
            return {}

        # Directly accumulate counts from telemetry data
        accumulated_counts: dict[str, dict[str, int]] = {
            key: {} for key in fields_to_count
        }
        successful_reads = 0

        for file_path in skipped_files:
            try:
                # Extract metadata from skipped file (implementation varies by source)
                metadata_list = self._extract_metadata_from_skipped_file(file_path)

                if not metadata_list:
                    continue

                # Process each metadata record (may be multiple per file)
                for metadata in metadata_list:
                    # Extract telemetry data using the same method as skip_file
                    telemetry_data = self._extract_file_metadata_for_telemetry(metadata)
                    successful_reads += 1

                    # Accumulate counts for each field we're tracking
                    for key in fields_to_count:
                        value = telemetry_data.get(key)
                        # Convert None to "Unknown" for consistency
                        value_str = str(value) if value is not None else "Unknown"
                        accumulated_counts[key][value_str] = (
                            accumulated_counts[key].get(value_str, 0) + 1
                        )
            except Exception as e:
                logger.debug(
                    f"Could not extract metadata from skipped file {file_path}: {e}"
                )
                continue

        if successful_reads > 0:
            logger.debug(
                f"Successfully retrieved metadata from {successful_reads} "
                f"records from skipped files out of {len(skipped_files)} total."
            )
            # Filter out empty dicts and cache the result
            result = {k: v for k, v in accumulated_counts.items() if v}
            self._cached_additional_metrics = result
            return result

        # Cache empty result
        self._cached_additional_metrics = {}
        return {}
