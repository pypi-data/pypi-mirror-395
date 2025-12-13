"""Module containing InterMineSource class.

InterMineSource class handles loading data stored in InterMine Templates.

InterMine is an open source biological data warehouse developed by the University
of Cambridge http://intermine.org/ .
Please see InterMine's tutorials for a detailed overview of the
python API: https://github.com/intermine/intermine-ws-python-docs.
"""

from __future__ import annotations

import collections as _collections
import datetime
import importlib.util
import itertools
import logging
import sys
import types
from typing import Any, Iterator, Optional, cast, overload
import urllib.parse as _up

import pandas as pd
from pandas.core.dtypes.common import pandas_dtype
from typing_extensions import override

from bitfount.data.datasources.base_source import BaseSource
from bitfount.data.datasources.types import DatasourceSummaryStats
from bitfount.data.exceptions import DataSourceError, InterMineServiceUnavailableError
from bitfount.data.types import SingleOrMulti
from bitfount.types import _Dtypes, _DtypesValues
from bitfount.utils import delegates

logger = logging.getLogger(__name__)


# Python 3 compatibility shim for old intermine package versions
# Intermine Service is currently compatible with Python 3.8 and not 3.10.
# Provide a 'urlparse' module backed by urllib.parse when not present
if importlib.util.find_spec("urlparse") is None:
    m = types.ModuleType("urlparse")
    for name in (
        "urlparse",
        "urlunparse",
        "urljoin",
        "urlsplit",
        "urlunsplit",
        "parse_qs",
        "parse_qsl",
        "quote",
        "unquote",
        "urlencode",
    ):
        setattr(m, name, getattr(_up, name))
    sys.modules["urlparse"] = m

# Expose collections.MutableMapping for libs expecting the old location
if not hasattr(_collections, "MutableMapping"):
    import collections.abc as _abc

    _collections.MutableMapping = _abc.MutableMapping  # type: ignore[attr-defined] # Reason: shim for old intermine

# Import InterMine Service with Python 3 compatibility shims
try:
    from intermine.query import Template
    from intermine.webservice import Service, ServiceError

except Exception as e1:
    # Try again after applying shims
    # (they may not have been applied yet in some import orders)
    try:
        from intermine.query import Template
        from intermine.webservice import Service, ServiceError

    except Exception as e2:
        raise ImportError(
            "Failed to import 'intermine.webservice.Service'. Please install a "
            "Python 3 compatible version of 'intermine'. "
            f"Original error: {e1!r}; after applying shims: {e2!r}"
        ) from e2


INTERMINE_TYPE_MAPPING = {
    "java.lang.String": str,
    "java.lang.Double": float,
    "java.lang.Float": float,
    "java.lang.Integer": int,
    "java.lang.Boolean": bool,
    "org.intermine.objectstore.query.ClobAccess": object,
    "java.util.Date": datetime.date,
    "int": int,
}
INTERMINE_YIELD_PARTITION_SIZE = 10_000


@delegates()
class InterMineSource(BaseSource):
    """Data Source for loading data from InterMine Templates.

    Args:
        service_url: Required. The URL of the InterMine service.
            An example service URL is "https://www.humanmine.org/humanmine/service".
            Omitting the "/service" suffix may also work depending
            on the server version.
        template_name: Required. The name of the InterMine template to load.
        token: Optional. The user token for accessing the InterMine service.
            Bitfount does not support username/password authentication
            (is supported by all webservices). A user token must be provided if
            authentication is required. This is supported on webservices version 6+.
        **kwargs: Additional keyword arguments passed to the BaseSource.

    Raises:
        DataSourceError: If the connection to the InterMine service fails.
        ValueError: If no value is provided for template_name. Or if the template
            is not found in the service or if duplicate template names are found
            in the service.
    """

    def __init__(
        self,
        service_url: str,
        template_name: str,
        token: Optional[str] = None,
        is_reconnection: bool = False,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        if template_name is None or template_name.strip() == "":
            raise ValueError("template_name must be provided for InterMineSource.")

        # Variables to track the service
        self._is_reconnection = is_reconnection
        self._service_available = False
        self.service = self._establish_service_connection(service_url, token=token)

        # Template name and template object
        self.template_name = template_name
        self.intermine_template = self._retrieve_template_from_service()

    def _establish_service_connection(
        self, service_url: str, token: Optional[str] = None
    ) -> Optional[Service]:
        """Establish connection to InterMine service at given URL.

        Args:
            service_url: Required. The URL of the InterMine service.
                An example service URL is "https://www.humanmine.org/humanmine/service".
                Omitting the "/service" suffix may also work depending
                on the server version.
            token: Optional. The user token for accessing the InterMine service.
                Bitfount does not support username/password authentication
                (is supported by all webservices). A user token must be provided if
                authentication is required. This is supported on webservices version 6+.

        Raises:
            DataSourceError: If the connection to the InterMine service fails due to
                configuration errors (wrong URL, authentication issues, etc.).
            InterMineServiceUnavailableError: If the InterMine service is temporarily
                unavailable (HTTP 5xx) during first-time connection.

        Returns:
            The connected InterMine service object, or None if the service is
            temporarily unavailable during a reconnection attempt.
        """
        try:
            service = Service(service_url, token=token)
            logger.info(
                f"Connected to InterMine service at {service_url} with "
                f"datawarehouse version: {service.release}, "
                f"webservice version: {service.version}"
            )
            self._service_available = True
            return service
        except ServiceError as e:
            # ServiceError contains HTTP status information from the InterMine service
            # Check if this is a server-side error (5xx status codes)
            is_server_error = self._is_server_error(e)

            # Regardless of the error, the service won't be available.
            self._service_available = False

            if is_server_error and self._is_reconnection:
                # During reconnection (e.g., Pod restart), if the service is temporarily
                # unavailable, log a warning but don't raise an exception.
                # This prevents the Pod from getting stuck in an infinite retry loop
                # and allows other datasources to come online.
                logger.warning(
                    f"InterMine service at {service_url} is temporarily unavailable "
                    f"(server error). The datasource will not be available until "
                    f"the service recovers. Error: {e!r}"
                )
                return None
            elif is_server_error:
                # First-time connection with server error - raise specific exception
                logger.error(
                    f"InterMine service at {service_url} is temporarily unavailable "
                    f"(server error): {e!r}"
                )
                raise InterMineServiceUnavailableError(
                    f"InterMine service at {service_url} is temporarily unavailable. "
                    f"Please try again later. Error: {e!r}"
                ) from e
            else:
                # Client-side error (4xx) or other ServiceError - likely config issue
                logger.error(
                    f"Failed to connect to InterMine service at {service_url}: {e!r}"
                )
                raise DataSourceError(
                    f"Failed to connect to InterMine service at {service_url}: {e!r}"
                ) from e
        except Exception as e:
            # Other exceptions (connection errors, DNS failures, etc.)

            # Regardless of the error, the service won't be available.
            self._service_available = False

            if self._is_reconnection:
                # During reconnection (e.g., Pod restart), if the service is unreachable
                # (DNS failure, connection timeout, etc.), log a warning but don't raise
                # This prevents the Pod from getting stuck in an infinite retry loop
                # and allows other datasources to come online.
                logger.warning(
                    f"InterMine service at {service_url} is unreachable "
                    f"(connection error). The datasource will not be available until "
                    f"the service recovers. Error: {e!r}"
                )
                return None

            logger.error(f"Failed to connect to InterMine service at {service_url}")
            raise DataSourceError(
                f"Failed to connect to InterMine service at {service_url}: {e!r}"
            ) from e

    @staticmethod
    def _is_server_error(error: ServiceError) -> bool:
        """Check if a ServiceError represents a server-side error (HTTP 5xx).

        Args:
            error: The ServiceError to check.

        Returns:
            True if the error represents a server-side error (HTTP 5xx),
            False otherwise.
        """
        # ServiceError may contain status code information in various ways
        # Check the message for HTTP status codes or known server error patterns
        error_message = str(error).lower()

        # Check for explicit 5xx status codes in the error message
        if any(f"{code}" in str(error) for code in range(500, 600)):
            return True

        # Check for common server error indicators -
        # this has been populated with the contents of this method in the intermine
        # Python library, but more can be added here if needed.
        # https://github.com/intermine/intermine-ws-python/blob/dev/intermine/results.py
        server_error_indicators = [
            "internal server error",
        ]
        return any(indicator in error_message for indicator in server_error_indicators)

    def _retrieve_template_from_service(self) -> Optional[Template]:
        """Retrieve the Template object from the InterMine service.

        Initially, a call to `get_template` is made to try and retrieve the template
        by name. This endpoint has access to templates available to the current
        auth session. This includes public templates and any private
        templates accessible.
        If the above fails, an attempt to retrieve all templates is made. This,
        however, requires admin authentication, so may fail if the user does
        not have sufficient privileges. If successful, a retrieval based on the
        template name and owner username is performed.

        Raises:
            ValueError: If the template is not found in the service or
                if duplicate template names are found in the service.
                An output of the available templates is logged for debugging.
            InterMineServiceUnavailableError: If the service is unavailable and
                is_reconnection is False.

        Returns:
            The InterMine Template object.
        """
        if not self._service_available or self.service is None:
            if self._is_reconnection:
                return None
            raise InterMineServiceUnavailableError(
                f"Cannot retrieve template '{self.template_name}' - "
                "InterMine service is unavailable"
            ) from None

        # Strategy 1: Direct retrieval by name
        template = self._try_get_template_directly()
        if template is not None:
            return template

        # Strategy 2: Retrieval through all templates (admin auth required)
        template = self._try_get_template_via_admin()
        if template is not None:
            return template

        # Both strategies failed - raise with debugging info
        self._raise_template_not_found_error()

        return None

    def _try_get_template_directly(self) -> Optional[Template]:
        """Attempt direct template retrieval by name.

        Returns:
            The Template if found, None otherwise.
        """
        try:
            _service = cast(Service, self.service)
            template = _service.get_template(self.template_name)
            logger.info(f"Retrieved template '{self.template_name}' from service.")
            return template
        except Exception as e:
            logger.error(
                f"Failed to access template '{self.template_name}' "
                f"- template does not exist: {e!r}."
                "Retrying with all templates..."
            )
            return None

    def _try_get_template_via_admin(self) -> Optional[Template]:
        """Attempt template retrieval via admin all_templates_names endpoint.

        Returns:
            The Template if found, None otherwise.
        """
        _service = cast(Service, self.service)
        try:
            all_templates_mapping = _service.all_templates_names
        except Exception as e:
            logger.error(f"Failed to access all templates: {e!r}.")
            return None

        self._validate_no_duplicate_template_names(all_templates_mapping)

        # Build reverse mapping: template_name -> owner
        templates_to_users = {
            template: user
            for user, templates in all_templates_mapping.items()
            for template in templates
        }

        if self.template_name not in templates_to_users:
            return None

        try:
            template = _service.get_template_by_user(
                self.template_name, templates_to_users[self.template_name]
            )
            logger.info(f"Retrieved template '{self.template_name}' from service.")
            return template
        except Exception as e:
            logger.error(
                f"Failed to access template '{self.template_name}' "
                f"- template or user does not exist: {e!r}."
            )
            return None

    def _validate_no_duplicate_template_names(
        self, all_templates_mapping: dict[str, list[str]]
    ) -> None:
        """Raise ValueError if any template name appears for multiple users.

        Args:
            all_templates_mapping: Mapping of username to list of template names.

        Raises:
            ValueError: If duplicate template names are found across users.
        """
        all_names = list(itertools.chain.from_iterable(all_templates_mapping.values()))
        seen: set[str] = set()
        for name in all_names:
            if name in seen:
                logger.debug(f"Found templates: {all_names}")
                raise ValueError(
                    f"Template names must be unique across all users in the service. "
                    f"Duplicated template name found: '{name}'."
                )
            seen.add(name)

    def _raise_template_not_found_error(self) -> None:
        """Raise ValueError with available templates logged for debugging.

        Raises:
            ValueError: Raised if template was not found and not reconnecting.
        """
        try:
            _service = cast(Service, self.service)
            available = list(_service.templates.keys())
            logger.debug(f"Found templates: {available}")
        except Exception as e:
            logger.debug(f"Failed to get any template from service: {e!r}")

        # If we are reconnecting, return None as the template is not available
        # otherwise raise an error
        if self._is_reconnection:
            return None
        raise ValueError(
            f"Template '{self.template_name}' not found in service: {_service}."
        )

    def _convert_python_dtypes_to_pandas_dtypes(
        self, dtype: _DtypesValues, col_name: str
    ) -> _DtypesValues:
        """Convert the python dtypes to pandas dtypes.

        Args:
            dtype: The python dtype to convert.
            col_name: The name of the column.

        Returns:
            The corresponding pandas dtype.
        """
        if dtype is str:
            return pd.StringDtype()
        # Date/datetime -> StringDtype
        elif dtype == datetime.date or dtype == datetime.datetime:
            return pd.StringDtype()
        # Explicitly handle pandas Timestamp by mapping to datetime64[ns]
        elif dtype is pd.Timestamp:
            return pandas_dtype("datetime64[ns]")
        else:
            try:
                return pandas_dtype(dtype)
            except Exception as e:
                raise ValueError(
                    f"Data type {dtype} not recognised for column {col_name}"
                ) from e

    def _get_dtypes(self) -> _Dtypes:
        """Loads and returns the columns and column types of the InterMine Template.

        Maps the InterMine Java types to Pandas dtypes.

        Returns:
            A mapping from column names to column types. Empty dict if service
            is unavailable.
        """
        template = self.intermine_template
        if template is None:
            logger.warning("Cannot get dtypes - InterMine service is unavailable")
            return {}

        # InterMine Template view_types are given in their java types
        java_dtypes = dict(zip(template.views, template.view_types))
        dtypes = {
            k.replace(".", "_"): self._convert_python_dtypes_to_pandas_dtypes(
                INTERMINE_TYPE_MAPPING[v], k
            )
            for k, v in java_dtypes.items()
        }
        return dtypes

    @override
    def get_data(
        self,
        data_keys: SingleOrMulti[str] | SingleOrMulti[int],
        *,
        use_cache: bool = True,
        **kwargs: Any,
    ) -> Optional[pd.DataFrame]:
        """Get data using the set InterMine Template.

        Args:
            data_keys: String or integer based indices for which rows should be
                returned.
            use_cache: Whether to use cached data if available.
            **kwargs: Additional keyword arguments.

        Returns:
            DataFrame containing the selected rows or None if no data is returned.
        """
        data = self._get_data(data_keys, use_cache=use_cache, **kwargs)

        for hook in self._hooks:
            try:
                hook.on_datasource_get_data(data)
            except NotImplementedError:
                logger.debug(
                    f"{hook.hook_name} does not implement `on_datasource_get_data`."
                )
            except Exception as e:
                logger.error(f"Error in hook {hook.hook_name}: {e}")

        if not data.empty:
            return data
        else:
            return None

    def _get_data(
        self,
        data_keys: Optional[SingleOrMulti[str] | SingleOrMulti[int]] = None,
        *,
        use_cache: bool = True,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Loads and returns data from a selected InterMine Template.

        It performs a query on the InterMine Template and returns the results.
        Replaces any dots (`.`) in column names with underscores (`_`).

        Args:
            data_keys: String based indices for which rows should be
                returned.
            use_cache: Whether to use cached data if available.
            **kwargs: Additional keyword arguments.

        Returns:
            DataFrame containing the selected rows. Empty DataFrame if service
            is unavailable.
        """
        template = self.intermine_template
        if template is None:
            logger.warning("Cannot get data - InterMine service is unavailable")
            return pd.DataFrame()

        df = pd.DataFrame(
            template.results(row="list"),
            columns=[col.replace(".", "_") for col in template.views],
        )

        # Filter by data_keys if provided
        if data_keys is not None:
            data_keys = self._convert_to_multi(data_keys)

            # Handle different index types
            index_type = df.index.inferred_type
            if index_type == "integer":
                df = df.loc[df.index.intersection([int(i) for i in data_keys])]
            else:
                df = df.loc[df.index.intersection([str(s) for s in data_keys])]

        # Apply modifiers and ignore columns
        df = self.apply_modifiers(df)
        df = self.apply_ignore_cols(df)

        return df

    @override
    def yield_data(
        self,
        data_keys: Optional[SingleOrMulti[str] | SingleOrMulti[int]] = None,
        *,
        use_cache: bool = True,
        partition_size: Optional[int] = INTERMINE_YIELD_PARTITION_SIZE,
        **kwargs: Any,
    ) -> Iterator[pd.DataFrame]:
        """Generator for providing data chunkwise from the InterMine Template query.

        Args:
            data_keys: String or integer based indices for which rows should be
                returned.
            use_cache: Whether to use cached data if available.
            partition_size: Size of each partition to yield.
            **kwargs: Additional keyword arguments.

        Yields:
            DataFrame chunks containing the selected data.
        """
        logger.debug(
            f"Yielding data from InterMine Template '{self.template_name}' "
            f"with partition_size={partition_size}, use_cache={use_cache}"
        )
        for data in self._yield_data(
            data_keys, use_cache=use_cache, partition_size=partition_size, **kwargs
        ):
            for hook in self._hooks:
                try:
                    hook.on_datasource_yield_data(
                        data,
                        metrics=self.get_datasource_metrics(use_skip_codes=True),
                    )
                except NotImplementedError:
                    logger.warning(
                        f"{hook.hook_name} does not implement "
                        "`on_datasource_yield_data`."
                    )
                except Exception as e:
                    logger.error(f"Error in hook {hook.hook_name}: {e}")

            if not data.empty:
                yield data

    def _yield_data(
        self,
        data_keys: Optional[SingleOrMulti[str] | SingleOrMulti[int]] = None,
        *,
        use_cache: bool = True,
        partition_size: Optional[int] = None,
        **kwargs: Any,
    ) -> Iterator[pd.DataFrame]:
        """Generator for providing data chunkwise from the InterMine Template query.

        Args:
            data_keys: String or integer based indices for which rows should be
                returned.
            use_cache: Whether to use cached data if available.
            partition_size: Size of each partition to yield.
            **kwargs: Additional keyword arguments.

        Yields:
            DataFrame chunks containing the selected data. Yields nothing if
            service is unavailable.
        """
        template = self.intermine_template
        if template is None:
            logger.warning("Cannot yield data - InterMine service is unavailable")
            return

        if data_keys is not None:
            data_keys = self._convert_to_multi(data_keys)

        partition_size_: int
        if partition_size:
            partition_size_ = partition_size
        else:
            partition_size_ = self.partition_size

        # Page through template results using start/size and yield DataFrame chunks
        start = 0
        cols = [col.replace(".", "_") for col in template.views]

        while True:
            logger.debug(
                f"InterMineSource: fetching partition at start={start} "
                f"size={partition_size_}"
            )
            try:
                rows_iter = template.results(
                    row="list", start=start, size=partition_size_
                )
            except Exception as e:
                logger.error(
                    (
                        "Failed to fetch template results at start="
                        f"{start}, size={partition_size_}: {e!r}"
                    )
                )
                break

            rows = list(rows_iter)
            logger.debug(
                f"InterMineSource: fetched {len(rows)} rows for "
                f"partition starting at {start}"
            )
            if not rows:
                break

            df_chunk = pd.DataFrame(rows, columns=cols)
            # Align index to global row offsets so index-based filtering works
            df_chunk.index = pd.RangeIndex(start=start, stop=start + len(df_chunk))

            # Optional filtering by provided data_keys
            if data_keys is not None and len(df_chunk) > 0:
                index_type = df_chunk.index.inferred_type
                if index_type == "integer":
                    df_chunk = df_chunk.loc[
                        df_chunk.index.intersection([int(i) for i in data_keys])
                    ]
                else:
                    df_chunk = df_chunk.loc[
                        df_chunk.index.intersection([str(s) for s in data_keys])
                    ]

            # Apply modifiers and ignore columns consistently with get_data
            if len(df_chunk) > 0:
                df_chunk = self.apply_modifiers(df_chunk)
                df_chunk = self.apply_ignore_cols(df_chunk)

            if not df_chunk.empty:
                yield df_chunk

            start += len(rows)

    def _get_datasource_metrics(
        self, use_skip_codes: bool = False, data: Optional[pd.DataFrame] = None
    ) -> DatasourceSummaryStats:
        """Returns basic metrics for InterMine datasource."""
        return {
            "total_files_found": 1,
            "total_files_successfully_processed": 1,
            "total_files_skipped": 0,
            "files_with_errors": 0,
            "skip_reasons": {},
            "additional_metrics": {},
        }

    @staticmethod
    @overload
    def _convert_to_multi(
        som: SingleOrMulti[str],
    ) -> list[str]: ...

    @staticmethod
    @overload
    def _convert_to_multi(
        som: SingleOrMulti[int],
    ) -> list[int]: ...

    @staticmethod
    def _convert_to_multi(
        som: SingleOrMulti[str] | SingleOrMulti[int],
    ) -> list[str] | list[int]:
        """Convert single or multi value to list."""
        # If already a list, return unchanged
        if isinstance(som, list):
            return som
        # If it's a string, wrap in list
        elif isinstance(som, str):
            return [som]
        # If it's an int, wrap in list
        elif isinstance(som, int):
            return [som]
        # If it's some other sequence (tuple, etc.), convert to list
        else:
            # At this point, som must be a sequence of either str or int
            # We use cast to help mypy understand the type
            return cast(list[str] | list[int], list(som))

    def __len__(self) -> int:
        """Return the total number of rows in the InterMine Template Query.

        Uses the InterMine Template.count() endpoint which requests only the
        count from the server (no full data fetch).

        Returns:
            The total number of rows in the InterMine Template Query.
            Returns 0 if the service is unavailable.
        """
        template = self.intermine_template
        if template is None:
            logger.warning("Cannot get count - InterMine service is unavailable")
            return 0

        try:
            return int(template.count())
        except Exception as e:
            logger.error(f"Failed to get count for template `{template}` {e!r}")
            return 0
