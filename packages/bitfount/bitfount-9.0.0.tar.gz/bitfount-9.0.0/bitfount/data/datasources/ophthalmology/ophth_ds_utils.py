"""Utility functions for interacting with ophthalmology datasources."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final, Union

from bitfount.utils.fs_utils import normalize_path

SLO_ORIGINAL_FILENAME_METADATA_COLUMN: Final[str] = "_slo_original_filename"


class NoParserForFileExtension(KeyError):
    """Indicates no parser was specified for a file extension."""

    pass


def make_path_absolute(
    file_path: Union[str, os.PathLike], parent_folder: Union[str, os.PathLike]
) -> Path:
    """Makes a relative file path absolute with respect to a parent folder.

    Does not change an already absolute file path.
    """
    file_path = Path(file_path)
    parent_folder = Path(parent_folder)
    return (
        file_path if file_path.is_absolute() else parent_folder / file_path
    ).resolve()


def make_path_relative(
    file_path: Union[str, os.PathLike], parent_folder: Union[str, os.PathLike]
) -> Path:
    """Makes an absolute file path relative with respect to a parent folder.

    Does not change an already relative file path.

    This function normalizes paths to handle mapped drives vs UNC paths equivalently
    on Windows, ensuring that paths referring to the same location are treated as
    equivalent.
    """
    file_path = Path(file_path)
    parent_folder = Path(parent_folder)
    if not file_path.is_absolute():
        return file_path

    # Normalize both paths to handle mapped drives vs UNC paths equivalently
    # This ensures that S:\patients and \\FileServer\Filestorage1\Images\patients
    # are treated as the same location
    normalized_file_path = normalize_path(file_path)
    normalized_parent_folder = normalize_path(parent_folder)
    return normalized_file_path.relative_to(normalized_parent_folder)
