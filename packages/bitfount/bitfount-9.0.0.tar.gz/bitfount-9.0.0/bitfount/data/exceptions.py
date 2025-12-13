"""Custom exceptions for the data package."""

from __future__ import annotations

from bitfount.exceptions import BitfountError


class BitfountSchemaError(BitfountError):
    """Errors related to BitfountSchema."""

    pass


class DataStructureError(BitfountError):
    """Errors related to Datastructure."""

    pass


class DataSourceError(BitfountError):
    """Errors related to Datasource."""

    pass


class IterableDataSourceError(DataSourceError):
    """Errors related to IterableSource-specific functionality."""

    pass


class ElevatedPermissionsError(DataSourceError):
    """Errors related to datasource connections having elevated write permissions.

    This exception is raised when a datasource connection is detected to have
    write permissions (INSERT, UPDATE, DELETE, CREATE, etc.) when read-only
    access is required for security purposes.
    """

    pass


class DataNotLoadedError(BitfountError):
    """Raised if a data operation is attempted prior to data loading.

    This is usually raised because `load_data` has not been called yet.
    """

    pass


class DuplicateColumnError(BitfountError):
    """Raised if the column names are duplicated in the data.

    This can be raised by the sql algorithms with multi-table pods.
    """

    pass


class DataCacheError(BitfountError):
    """Error related to data cache interaction."""

    pass


class DataNotAvailableError(BitfountError):
    """Error when data is not available.

    This is raised when data is initially expected from the first read of a datasource,
    but an error is raised during the subsequent reads rendering no data available.
    """

    pass


class InterMineServiceUnavailableError(DataSourceError):
    """Error raised when the InterMine service is temporarily unavailable.

    This exception is raised when the InterMine service returns an HTTP 500 error
    or similar server-side error, indicating that the service is temporarily down
    but the configuration may still be valid.

    This is distinct from configuration errors (wrong URL, missing template) which
    indicate a permanent problem that requires user intervention.
    """

    pass
