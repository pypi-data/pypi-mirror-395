"""Exceptions for data sources."""

from bitfount.data.exceptions import DataSourceError


# TODO: [BIT-6438] Move all DataSourceErrors to this module
class ZeissModalityError(DataSourceError):
    """Errors related to unsupported Zeiss modality types."""

    pass
