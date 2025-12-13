"""Data source for loading ophthalmology files using Topcon."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import (
    Any,
    Final,
    Mapping,
    Optional,
    Union,
)

import pandas as pd

from bitfount.data.datasources.ophthalmology.ophth_ds_types import (
    ProcessedDataRequiredTypes,
)
from bitfount.data.datasources.ophthalmology.ophthalmology_base_source import (
    IMAGE_COLUMN_PREFIX,
)
from bitfount.data.datasources.ophthalmology.private_eye_base_source import (
    PrivateEyeParser,
    _PrivateEyeSource,
)
from bitfount.data.datasources.utils import (
    LAST_MODIFIED_METADATA_COLUMN,
    ORIGINAL_FILENAME_METADATA_COLUMN,
    FileSystemFilter,
    calculate_dimensionality,
)
from bitfount.utils import delegates, get_type_hints

logger = logging.getLogger(__name__)

TOPCON_FILE_EXTENSION: Final[str] = ".fda"
TOPCON_REQUIRED_FIELDS = get_type_hints(ProcessedDataRequiredTypes)


@delegates()
class TopconSource(_PrivateEyeSource):
    """Data source for loading Topcon files.

    Args:
        path: The path to the directory containing the Topcon .fda files.
        parsers: The private eye parsers to use for the different file extensions.
            Only needs to be supplied if file_extension filter is non-default. Can
            either be a single parser to use for all file extensions or a mapping of
            file extensions to parser type. Defaults to appropriate parser(s) for the
            default file extension(s).
        **kwargs: Keyword arguments passed to the parent base classes.
    """

    def __init__(
        self,
        path: Union[os.PathLike, str],
        parsers: Optional[
            Union[PrivateEyeParser, Mapping[str, PrivateEyeParser]]
        ] = None,
        required_fields: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        if parsers is None:
            parsers = {
                ".fda": PrivateEyeParser.TOPCON,
            }

        filter_: Optional[FileSystemFilter] = kwargs.pop("filter", None)
        if filter_ is not None:
            file_extension = filter_.file_extension or []
            if file_extension != [TOPCON_FILE_EXTENSION]:
                logger.warning(
                    "TopconSource only supports '.fda' files. Ignoring "
                    f"file_extension={file_extension}."
                )
                filter_.file_extension = [TOPCON_FILE_EXTENSION]
        else:
            filter_ = FileSystemFilter(file_extension=TOPCON_FILE_EXTENSION)

        super().__init__(
            private_eye_parser=parsers,
            path=path,
            filter=filter_,
            **kwargs,
        )
        if required_fields is None:
            required_fields = TOPCON_REQUIRED_FIELDS
        self.required_fields = required_fields
        self.image_fields = IMAGE_COLUMN_PREFIX

    def _add_metadata_to_data(
        self, data: dict[str, Any], filename: str
    ) -> dict[str, Any]:
        """Adds metadata to the data.

        Args:
            data: The data to add metadata to.
            filename: The filename of the file to be processed.

        Returns:
            The data with metadata added.
        """
        data[ORIGINAL_FILENAME_METADATA_COLUMN] = filename
        data[LAST_MODIFIED_METADATA_COLUMN] = self._get_file_m_time(filename)

        # Track the first two directory levels so that we can easily
        # process the possible labels later on as needed
        relative_filepath = Path(filename).relative_to(self.path).parts
        if len(relative_filepath) > 1:
            data[self._first_directory_in_path] = relative_filepath[0]
        if len(relative_filepath) > 2:
            data[self._second_directory_in_path] = relative_filepath[1]

        return data

    def _post_process_file(
        self, data: dict[str, Any], filename_path: Path
    ) -> dict[str, Any]:
        """Apply any post-processing to the data found in _process_file.

        This is a no-op for TopconSource, as we are not enabling CSV support.
        """
        return data

    def _extract_file_metadata_for_telemetry(
        self, data: Optional[dict[str, Any]]
    ) -> dict[str, Any]:
        """Extracts file metadata for telemetry.

        Args:
            data: The data to extract metadata from.

        Returns:
            A dictionary of file metadata.
        """
        telemetry_data = super()._extract_file_metadata_for_telemetry(data)

        if data is not None:
            updates = {
                "number_of_frames": data.get("Number of Frames"),
                "dimensionality": calculate_dimensionality(data),
                "series_description": data.get("Series Description"),
                "modality": data.get("Modality"),
                "manufacturers_model_name": data.get("Manufacturer's Model Name"),
                "manufacturer": data.get("Manufacturer"),
                "pixel_spacing_row": data.get("Pixel Spacing Row"),
                "pixel_spacing_column": data.get("Pixel Spacing Column"),
                "slice_thickness": data.get("Slice Thickness"),
            }
            # Only update telemetry data with values that are not already set
            telemetry_data.update(
                {k: v for k, v in updates.items() if telemetry_data.get(k) is None}
            )

        return telemetry_data

    def _extract_metadata_from_skipped_file(
        self, file_path: str
    ) -> list[dict[str, Any]]:
        """Extract metadata from a skipped Topcon file for metrics purposes.

        Uses _process_file with skip_non_tabular_data=True to read metadata
        without loading image data.

        Args:
            file_path: Path to the skipped Topcon file.

        Returns:
            A list of metadata dictionaries (may contain multiple records if file
            has data for both eyes), empty list if processing fails.
        """
        try:
            return self._process_file(file_path, skip_non_tabular_data=True)
        except Exception as e:
            logger.debug(f"Could not extract metadata from {file_path}: {e}")
            return []

    def _get_datasource_specific_metrics(
        self, data: Optional[pd.DataFrame] = None
    ) -> dict[str, Any]:
        """Get datasource-specific metrics for the additional_metrics field.

        Subclasses should override this to provide their specific metrics.

        Returns:
            Dictionary containing datasource-specific metrics.
        """
        # Fields to track from the telemetry method (with their telemetry keys)
        fields_to_count = {
            "manufacturer": "Manufacturer",
            "modality": "Modality",
            "manufacturers_model_name": "Manufacturer's Model Name",
            "series_description": "Series Description",
        }

        # If data is empty, try to get metadata from skipped files
        if data is None or data.empty:
            return self._get_metrics_from_skipped_files(fields_to_count)

        # Normal case: data is provided (successfully processed files)
        additional_metrics = super()._get_datasource_specific_metrics(data)

        for key, field in fields_to_count.items():
            if field in data.columns:
                # Count occurrences of each value, filling NaN with "Unknown"
                value_counts = data[field].fillna("Unknown").value_counts()
                # Only add values that are not already in the additional_metrics
                # dictionary
                if key not in additional_metrics:
                    additional_metrics[key] = {
                        str(k): int(v) for k, v in value_counts.items()
                    }

        return additional_metrics
