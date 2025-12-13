"""Module containing NullSource class.

NullSource is a datasource that contains no data, used for protocols that don't
require data access.

This datasource is incompatible with `batched execution`, `run on new data`
or `test run` functionalities.
"""

from __future__ import annotations

from typing import Any, Iterator, Optional

import pandas as pd
from typing_extensions import override

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.types import DatasourceSummaryStats
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SingleOrMulti
from bitfount.types import _JSONDict


class NullSource(BaseSource):
    """Data source that contains no data.

    This datasource is used for protocols that don't require data access.

    Args:
        **kwargs: Additional keyword arguments passed to BaseSource.
    """

    # Predefined schema indicating no data
    has_predefined_schema: bool = True

    def __init__(self, **kwargs: Any) -> None:
        """Initialize NullSource."""
        super().__init__(**kwargs)

    def __len__(self) -> int:
        """Return the number of records in the datasource.

        Returns:
            0, as NullSource contains no data.
        """
        return 0

    @override
    def get_schema(self) -> _JSONDict:
        """Get the pre-defined empty schema for this datasource.

        Returns:
            An empty schema dictionary.
        """
        return BitfountSchema(name=self._name or "").to_json()

    @override
    def _get_data(
        self,
        data_keys: SingleOrMulti[str] | SingleOrMulti[int],
        *,
        use_cache: bool = True,
        **kwargs: object,
    ) -> pd.DataFrame:
        """Get data method.

        Since NullSource contains no data, this always returns an empty DataFrame.

        Args:
            data_keys: Key(s) for which to get the data. Ignored for NullSource.
            use_cache: Whether the cache should be used. Ignored for NullSource.
            **kwargs: Additional keyword arguments. Ignored for NullSource.

        Returns:
            An empty DataFrame.
        """
        return pd.DataFrame()

    @override
    def _yield_data(
        self,
        data_keys: Optional[SingleOrMulti[str] | SingleOrMulti[int]] = None,
        *,
        use_cache: bool = True,
        partition_size: Optional[int] = None,
        **kwargs: object,
    ) -> Iterator[pd.DataFrame]:
        """Yield data method.

        Since NullSource contains no data, this always yields nothing.

        Args:
            data_keys: Key(s) for which to get the data. Ignored for NullSource.
            use_cache: Whether the cache should be used. Ignored for NullSource.
            partition_size: Size of each partition. Ignored for NullSource.
            **kwargs: Additional keyword arguments. Ignored for NullSource.

        Yields:
            Nothing (empty iterator).
        """
        # Return empty iterator - no data to yield
        # Using yield from empty tuple to make this a generator function
        yield from ()

    def get_project_db_sqlite_create_table_query(self) -> str:
        """Returns the required columns and types for project database.

        Since NullSource has no data, this returns a minimal table structure.

        Returns:
            A SQL string for creating a minimal table with just an ID column.
        """
        return "id TEXT PRIMARY KEY"

    def _get_datasource_metrics(
        self, use_skip_codes: bool = False, data: Optional[pd.DataFrame] = None
    ) -> DatasourceSummaryStats:
        """Get metadata about this datasource.

        Args:
            use_skip_codes: Whether to use skip reason codes. Ignored for NullSource.
            data: The data to use for getting the metrics. Ignored for NullSource.

        Returns:
            A dictionary containing metadata about this datasource with all zeros.
        """
        return {
            "total_files_found": 0,
            "total_files_successfully_processed": 0,
            "total_files_skipped": 0,
            "files_with_errors": 0,
            "skip_reasons": {},
            "additional_metrics": {},
        }
