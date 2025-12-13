"""Algorithms and related functionality for simply outputting data to CSV."""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Mapping, Optional, Union
import warnings

from marshmallow import fields
import pandas as pd

from bitfount.data.datasources.base_source import (
    BaseSource,
    FileSystemIterableSource,
)
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import DOB_COL
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ProtocolContext, get_task_results_directory
from bitfount.types import T_FIELDS_DICT
from bitfount.utils.pandas_utils import append_dataframe_to_csv

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig


_logger = _get_federated_logger(__name__)


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algorithm."""

    def __init__(
        self,
        save_path: Path,
        rename_columns: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        """Create a new worker side of the _SimpleCSVAlgorithm algorithm.

        Args:
            save_path: The path to a directory to output the CSV to from the worker.
            rename_columns: Mapping of replacement column names to use when saving
                the dataframe out to CSV.
            **kwargs: Passed to parent.
        """
        super().__init__(**kwargs)
        self.save_path = save_path
        self.rename_columns = rename_columns
        self.output_files: set[Path] = set()

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
        """Sets Datasource."""
        self.initialise_data(datasource=datasource, data_splitter=data_splitter)

    def run(
        self,
        task_id: str,
        df: Optional[pd.DataFrame] = None,
        output_filename: Optional[str] = None,
        output_columns: Optional[list[str]] = None,
    ) -> None:
        """Output the dataframe to CSV.

        Args:
            task_id: The task identifier.
            df: Optional DataFrame to write to CSV.
            output_filename: Optional custom filename for the CSV output.
                            Defaults to "results.csv" if not provided.
            output_columns: Optional list of columns to include in output.
        """
        if df is None:
            _logger.warning(
                f"_SimpleCSVAlgorithm ({self.__class__.__name__})"
                f' specified save path "{str(self.save_path)}",'
                f" but was not passed a dataframe"
            )
        else:
            # Create a copy of the input DataFrame
            df = df.copy()

            # Add image column true/false mask
            self._add_img_col_mask(df)
            df = self._format_dob(df)

            # Perform column renamings
            if self.rename_columns is not None:
                df.rename(columns=self.rename_columns, inplace=True, errors="ignore")

            # Perform column pruning
            if output_columns is not None:
                df = df[output_columns]

            # Get the path to the CSV file.
            csv_path = self.get_csv_results_path(task_id, output_filename)
            _logger.info(f"Saving dataframe to CSV at {csv_path}")

            # Write the dataframe to CSV, handling appending to existing CSV
            csv_path = append_dataframe_to_csv(csv_path, df)

            # Store file path actually output to
            self.output_files.add(csv_path)

            _logger.info(f"CSV output to {csv_path}")

    def _format_dob(self, df: pd.DataFrame) -> pd.DataFrame:
        if DOB_COL in df and pd.core.dtypes.common.is_datetime64_ns_dtype(df[DOB_COL]):
            df[DOB_COL] = df[DOB_COL].apply(
                lambda timestamp: timestamp.strftime("%Y-%m-%d")
            )
        return df

    def _add_img_col_mask(self, df: pd.DataFrame) -> None:
        """Adds a True/False mask for img columns if needed."""
        if (
            isinstance(self.datasource, FileSystemIterableSource)
            and self.datasource.cache_images is False
        ):
            img_columns = list(self.datasource.image_columns)

            # Find the intersection of image_cols and data.columns
            existing_img_columns = list(set(img_columns) & set(df.columns))
            missing_img_columns = set(img_columns) - set(df.columns)

            if missing_img_columns:
                _logger.warning(
                    f"DataFrame has {len(existing_img_columns)} out of"
                    f" {len(img_columns)} image columns."
                    f"Missing {len(missing_img_columns)} image columns."
                )
                _logger.debug(
                    "The following image columns are missing from"
                    f" the DataFrame: {missing_img_columns}"
                )

            # Add True/None to indicate the number of frame based
            # on the pixel data columns if images are not cached.
            if existing_img_columns:
                img_df = df[existing_img_columns]
                # Replace non-NA elements with True
                img_df = img_df.mask(img_df.notna(), other=True)
                # Replace NA elements with False
                img_df = img_df.mask(img_df.isna(), other=None)
                df[existing_img_columns] = img_df

    def get_csv_results_path(
        self, task_id: str, output_filename: Optional[str] = None
    ) -> Path:
        """Get the path for the CSV results to be output to."""
        if output_filename is None:
            output_filename = "results.csv"

        # Append task_id as a subdirectory if it's not already present at the end
        # of the path
        if self.save_path.name != task_id:
            (self.save_path / task_id).mkdir(parents=True, exist_ok=True)
            csv_path = self.save_path / task_id / output_filename
        else:
            self.save_path.mkdir(parents=True, exist_ok=True)
            csv_path = self.save_path / output_filename

        return csv_path


class _SimpleCSVAlgorithm(
    BaseNonModelAlgorithmFactory[NoResultsModellerAlgorithm, _WorkerSide]
):
    """Algorithm that allows simple outputting of dataframes to CSV.

    Allows the data to be saved to CSV from either the worker or the modeller (or both).


    Args:
        datastructure: The datastructure to use.
        **kwargs: Passed to parent.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        # TODO: [BIT-6393] save_path deprecation
        "save_path": fields.Str(allow_none=True),
    }

    def __init__(
        self,
        datastructure: DataStructure,
        # TODO: [BIT-6393] save_path deprecation
        save_path: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(datastructure=datastructure, **kwargs)

        # TODO: [BIT-6393] save_path deprecation
        if save_path is not None:
            warnings.warn(
                f"The `save_path` argument is deprecated in {type(self).__name__}."
                "Use the BITFOUNT_OUTPUT_DIR,"
                " BITFOUNT_TASK_RESULTS,"
                " or BITFOUNT_PRIMARY_RESULTS_DIR"
                " environment variables instead.",
                DeprecationWarning,
            )
        self.save_path = None

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> NoResultsModellerAlgorithm:
        """Modeller-side of the _SimpleCSVAlgorithm algorithm."""
        return NoResultsModellerAlgorithm(
            log_message="Running Simple CSV Algorithm",
            **kwargs,
        )

    def worker(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the _SimpleCSVAlgorithm algorithm."""
        task_results_dir = get_task_results_directory(context)

        return _WorkerSide(
            save_path=task_results_dir,
            **kwargs,
        )
