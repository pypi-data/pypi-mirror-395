"""Datadog logging handlers for sending logs to Datadog's API.

This module provides handlers that integrate with Python's logging framework
to send logs to Datadog, with automatic batching and size management.
"""

import json
import logging
from logging.handlers import MemoryHandler
import socket
from typing import Optional, Union

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.model_utils import UnsetType
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem

from bitfount.utils.logging_utils import SampleFilter

logger = logging.getLogger(__name__)
logger.addFilter(SampleFilter())

# Module-level telemetry logger - safe to use anywhere
# Will send to Datadog if configured, otherwise silently discards logs
telemetry_logger = logging.getLogger("bitfount.telemetry")
telemetry_logger.setLevel(logging.INFO)
telemetry_logger.propagate = False  # Prevent propagation to other loggers

# Keep track of handler for shutdown
_telemetry_handler: Optional["DatadogLogsHandler"] = None


def setup_datadog_telemetry(
    dd_client_token: Optional[str] = None,
    dd_site: Optional[str] = None,
    service: str = "pod",
    hostname: Optional[str] = None,
    tags: Optional[list[str]] = None,
) -> None:
    """Setup Datadog telemetry logging if credentials are available.

    If credentials are not provided, the telemetry logger will exist but
    have no handlers, meaning all telemetry logs will be silently dropped.

    This function is idempotent - calling it multiple times is safe.

    Args:
        dd_client_token: The Datadog client token.
        dd_site: The Datadog site to use (e.g., 'datadoghq.com', 'datadoghq.eu').
        service: The service to use for the logs.
        hostname: The hostname to use for the logs. Defaults to system hostname.
        tags: The tags to use for the logs.

    Returns:
        None
    """
    global _telemetry_handler

    # If already configured, don't reconfigure
    if _telemetry_handler is not None:
        logger.debug("Datadog telemetry already configured.")
        return

    # If no client token exists, return early. Logger exists but does nothing.
    if not dd_client_token or not dd_site:
        logger.info("Datadog credentials not provided, telemetry logging disabled.")
        return

    try:
        api_config = Configuration()
        api_config.api_key["apiKeyAuth"] = dd_client_token
        api_config.server_variables["site"] = dd_site
        api_client = ApiClient(api_config)
        logs_api = LogsApi(api_client)

        _telemetry_handler = DatadogLogsHandler(
            api_instance=logs_api,
            source="pod",
            hostname=hostname or socket.gethostname(),
            service=service,
            tags=tags,
        )
        telemetry_logger.addHandler(_telemetry_handler)
        logger.info("Datadog telemetry configured successfully.")
    except Exception as e:
        logger.warning(f"Failed to configure Datadog telemetry: {e}")
        _telemetry_handler = None


def flush_datadog_telemetry() -> None:
    """Flush the Datadog telemetry buffer.

    This should be called to ensure all buffered logs are sent to Datadog.
    """
    global _telemetry_handler
    if _telemetry_handler is not None:
        try:
            logger.debug("Flushing Datadog telemetry...")
            _telemetry_handler.flush()
            logger.debug("Datadog telemetry flushed successfully.")
        except Exception as e:
            logger.warning(f"Failed to flush Datadog telemetry: {e}")


def shutdown_datadog_telemetry() -> None:
    """Shutdown Datadog telemetry logging and flush any pending logs.

    This should be called during application shutdown to ensure all buffered
    logs are sent to Datadog.
    """
    global _telemetry_handler

    if _telemetry_handler is not None:
        try:
            logger.info("Shutting down Datadog telemetry...")
            _telemetry_handler.flush()
            _telemetry_handler.close()
            telemetry_logger.removeHandler(_telemetry_handler)
            logger.info("Datadog telemetry shutdown complete.")
        except Exception as e:
            logger.warning(f"Error during Datadog telemetry shutdown: {e}")
        finally:
            _telemetry_handler = None


class DatadogLogsHandler(MemoryHandler):
    """A MemoryHandler that sends logs to Datadog.

    This handler automatically flushes when the buffer approaches a 5MB limit.
    These numbers are taken from Datadog's Logs API documentation:
    https://docs.datadoghq.com/api/latest/logs/

    We piggyback off Python's MemoryHandler class since we do not want to
    implement our own buffer management system, including what happens when there are
    records left in the buffer when the handler is closed.
    """

    # We need to be slightly conservative due to JSON overhead
    BUFFER_PERCENTAGE = 10  # 10% buffer to avoid hitting the limit
    MAX_BUFFER_SIZE = int((1 - (BUFFER_PERCENTAGE / 100)) * 5 * 1024 * 1024)

    def __init__(
        self,
        api_instance: LogsApi,
        source: str,
        hostname: str,
        service: str,
        tags: Optional[list[str]] = None,
        capacity: int = 1000,
    ):
        """Initialize the DatadogMemoryHandler.

        Args:
            api_instance: The Datadog API instance.
            source: The source of the logs.
            hostname: The hostname of the logs.
            service: The service of the logs.
            tags: The tags of the logs.
            capacity: The capacity of the buffer, defaulted to 1000 according to
                Datadog's documentation.
        """
        super().__init__(capacity, target=None)
        self.api_instance = api_instance
        self.source = source
        self.hostname = hostname
        self.service = service
        self.tags = tags
        self.current_buffer_size = 0
        self.log_items_buffer: list[HTTPLogItem] = []

        # Join tags into a string for the log item
        self._tags_as_str: Union[str, UnsetType] = (
            ", ".join(tags) if tags else UnsetType.unset
        )

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record to the buffer.

        Note that we immediately build the HTTPLogItem object and add it to
        a separate buffer, rather than waiting for the flush operation to do so.

        Args:
            record: The log record.
        """
        if not isinstance(record.msg, str):
            message = json.dumps(record.msg, default=str)
        else:
            message = self.format(record)

        log_item = HTTPLogItem(
            ddsource=self.source,
            ddtags=self._tags_as_str,
            hostname=self.hostname,
            message=message,
            service=self.service,
        )

        # Calculate the size of the log item
        item_json = json.dumps(log_item.to_dict())
        item_size = len(item_json.encode("utf-8"))

        # Check if we should flush before adding to buffer
        if self.shouldFlush(record, item_size):
            self.flush()

        # Add to both buffers and track HTTPLogItem size
        self.buffer.append(record)  # Parent class expects this
        self.log_items_buffer.append(log_item)
        self.current_buffer_size += item_size

    def shouldFlush(self, record: logging.LogRecord, item_size: int = 0) -> bool:
        """Determine if we should flush the buffer.

        Args:
            record: The log record.
            item_size: The size of the item to add to the buffer.

        Returns:
            True if we should flush the buffer, False otherwise.
        """
        # Flush if we are approaching the 5MB limit
        if self.current_buffer_size + item_size >= self.MAX_BUFFER_SIZE:
            return True

        # Flush if we have hit capacity
        if len(self.log_items_buffer) >= self.capacity:
            return True

        return False

    def flush(self) -> None:
        """Flush the buffer by sending all records to Datadog in a single request.

        Override the parent's flush method to flush records instead of calling
        emit() per record.
        """
        if not self.buffer:
            return

        self.acquire()
        try:
            body = HTTPLog(self.log_items_buffer)
            self.api_instance.submit_log(
                content_encoding=ContentEncoding.GZIP, body=body
            )
        except Exception as e:
            logger.error(f"Failed to send logs to Datadog: {e}")
        finally:
            # Clear both buffers
            self.buffer.clear()
            self.log_items_buffer.clear()
            self.current_buffer_size = 0

            self.release()
