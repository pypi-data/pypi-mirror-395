"""Resilience handling for batch execution in federated protocols.

This module handles batch resilience, individual file retry logic, error reporting,
and failure recovery mechanisms extracted from the main ProtocolExecution class.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

import pandas as pd

from bitfount import config
from bitfount.data.exceptions import DataNotAvailableError
from bitfount.federated.exceptions import BatchResilienceAbortError
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.protocols.types import ERROR_REPORT_FOLDER, BatchConfig
from bitfount.federated.protocols.utils import add_patient_metadata_columns
from bitfount.federated.transport.types import Reason
from bitfount.federated.types import ProtocolContext
from bitfount.hooks import HookType, get_hooks

if TYPE_CHECKING:
    from bitfount.federated.protocols.base import BaseWorkerProtocol

logger = _get_federated_logger(__name__)

ignored_errors = (DataNotAvailableError,)


class ResilienceHandler:
    """Handles batch resilience, retry logic, and error reporting."""

    def __init__(
        self,
        protocol: BaseWorkerProtocol,
        hook_kwargs: dict,
        execute_run_func: Callable,
        context: ProtocolContext,
    ) -> None:
        self.protocol = protocol
        self.hook_kwargs = hook_kwargs
        self.execute_run_func = execute_run_func
        self.context = context

    async def handle_batch_resilience_and_reporting(
        self, batch_config: BatchConfig
    ) -> None:
        """Handle batch resilience reporting and individual file retry logic.

        Args:
            batch_config: The batch configuration containing success/failure info.
        """
        if not config.settings.enable_batch_resilience:
            logger.info(
                "Batch resilience is disabled. Skipping batch resilience handling."
            )
            return
        elif not batch_config.failed_batches:
            logger.info(
                "No batch failures to report. Skipping batch resilience handling."
            )
            return

        logger.info(
            f"Batch processing completed. Summary: "
            f"{len(batch_config.successful_batches)} successful batches, "
            f"{len(batch_config.failed_batches)} failed batches"
        )

        if config.settings.individual_file_retry_enabled:
            failed_files = set()
            for batch_num in batch_config.failed_batches:
                files_in_batch = batch_config.failed_batch_file_mapping.get(
                    batch_num, []
                )
                failed_files.update(files_in_batch)
            if failed_files:
                for hook in get_hooks(HookType.POD):
                    hook.on_resilience_start(
                        task_id=self.protocol.mailbox.task_id,
                        modeller_username=getattr(
                            self.protocol.mailbox, "modeller_name", ""
                        ),
                        total_failed_files=len(failed_files),
                    )
            logger.info("Starting individual file diagnosis phase...")

            await self.retry_failed_files_individually(batch_config)
            successful_files = sum(
                1 for result in batch_config.individual_file_results.values() if result
            )
            failed_files_count = (
                len(batch_config.individual_file_results) - successful_files
            )

            for hook in get_hooks(HookType.POD):
                hook.on_resilience_complete(
                    task_id=self.protocol.mailbox.task_id,
                    modeller_username=getattr(
                        self.protocol.mailbox, "modeller_name", ""
                    ),
                    total_attempted=len(batch_config.individual_file_results),
                    total_succeeded=successful_files,
                    total_failed=failed_files_count,
                )
            # Check if we need to abort after individual file diagnosis
            await self.check_and_handle_zero_successful_files(batch_config)
        else:
            logger.debug(
                "Batch resilience enabled, but individual file retry disabled. "
                "Skipping individual file diagnosis."
            )
            # Check if we need to abort if all batches failed
            await self.check_and_handle_zero_successful_batches(batch_config)

        # Write report if resilience was enabled and there were failures
        self.write_failed_files_report(batch_config)

    async def handle_batch_failure(
        self,
        error: Exception,
        batch_num: int,
        batch_config: BatchConfig,
    ) -> None:
        """Handle a batch failure with resilience logic.

        Args:
            error: The exception that caused the batch to fail
            batch_num: The batch number that failed
            batch_config: The batch configuration object

        Raises:
            The original exception if batch resilience is disabled
            BatchResilienceAbortError if consecutive failure threshold is reached
        """
        # If batch resilience is disabled, re-raise the original error
        if not config.settings.enable_batch_resilience:
            logger.info(
                f"Batch resilience is disabled. Raising original error: {error}"
            )
            raise error

        # Track this batch failure and files in the batch
        batch_config.failed_batches[batch_num] = error
        batch_config.failed_batch_file_mapping[batch_num] = (
            batch_config.current_batch_files.copy()
        )

        # Only increment consecutive_failures if error is not in ignored_errors
        if isinstance(error, ignored_errors):
            logger.info(
                f"Batch {batch_num} failed with {error}; "
                "not incrementing consecutive failure counter."
            )
        else:
            batch_config.consecutive_failures += 1

        logger.warning(
            f"Batch {batch_num} failed with error: {error}. "
            f"Consecutive failures: {batch_config.consecutive_failures}",
            exc_info=True,
        )

        # Write immediate batch failure report
        self.write_immediate_batch_failure_report(batch_config, batch_num)

        # Only enforce threshold if not unlimited (-1)
        if (
            config.settings.max_consecutive_batch_failures != -1
            and batch_config.consecutive_failures
            >= config.settings.max_consecutive_batch_failures
        ):
            error_msg = (
                f"Aborting task after {batch_config.consecutive_failures} "
                f"consecutive batch failures. Last error: {str(error)}"
            )
            logger.error(error_msg)

            # Send abort message to modeller
            await self.protocol.mailbox.send_task_abort_message(
                error_msg, Reason.WORKER_ERROR
            )

            # Raise the abort error
            raise BatchResilienceAbortError(
                error_msg,
                batch_config.consecutive_failures,
                batch_config.failed_batches,
            )
        # Continue with next batch
        logger.info(f"Continuing with next batch after failure in batch {batch_num}")
        return

    async def check_and_handle_zero_successful_batches(
        self, batch_config: BatchConfig
    ) -> None:
        """Check if all batches failed and handle task abort.

        Args:
            batch_config: The batch configuration object

        Raises:
            BatchResilienceAbortError: If all batches failed and no successful
                processing occurred, and individual file retry is not enabled
                or not applicable.
        """
        # Only check if batch resilience is enabled and we have failures
        # but no successes
        if not (
            config.settings.enable_batch_resilience
            and len(batch_config.successful_batches) == 0
            and len(batch_config.failed_batches) > 0
        ):
            return

        if config.settings.individual_file_retry_enabled:
            logger.info(
                f"All {len(batch_config.failed_batches)} batches failed, "
                f"but individual file retry is enabled. Will attempt "
                f"individual file diagnosis before aborting."
            )
            return

        # If individual file retry is not enabled, send a task abort message
        await self.abort_task_all_batches_failed(batch_config)

    def write_immediate_batch_failure_report(
        self, batch_config: BatchConfig, batch_num: int
    ) -> None:
        """Write immediate batch failure report to a single CSV file.

        Appends the current batch failure to an ongoing report file, creating it
        with headers if it doesn't exist.

        Args:
            batch_config: The batch configuration object
            batch_num: The batch number that failed
        """
        if not config.settings.enable_batch_resilience:
            return  # Don't write reports if resilience is disabled

        try:
            # Find save path from algorithms or use current directory
            error_reports_dir = self.get_error_reports_save_dir()

            # Use a consistent filename for all batch failures in this task
            report_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report_date = datetime.now().strftime("%Y-%m-%d")
            report_file = error_reports_dir / f"Batch_failures_report_{report_date}.csv"

            # Use the existing function to build data for ALL failed batches
            all_batch_data = self.build_batch_level_report_data(
                batch_config, report_timestamp
            )

            # Filter to only include data for the current failed batch
            current_batch_data = [
                row for row in all_batch_data if row["Batch number"] == batch_num + 1
            ]

            if not current_batch_data:
                logger.debug(f"No data to write for batch {batch_num} failure report")
                return

            # Create DataFrame for this batch only
            df = pd.DataFrame(current_batch_data)

            # Check if file exists to determine if we need headers
            file_exists = report_file.exists()

            # Append to CSV (create with headers if first time)
            df.to_csv(
                report_file,
                mode="a" if file_exists else "w",
                header=not file_exists,
                index=False,
            )

            action = "Appended to" if file_exists else "Created"
            logger.info(
                f"{action} immediate batch failure report: "
                f"{report_file} (batch {batch_num})"
            )

        except Exception as e:
            logger.error(
                f"Failed to write immediate batch failure report for"
                f" batch {batch_num}: {e}"
            )

    async def abort_task_all_batches_failed(self, batch_config: BatchConfig) -> None:
        """Abort the task when all batches failed and no recovery is possible.

        Args:
            batch_config: The batch configuration object

        Raises:
            BatchResilienceAbortError: Always raised to abort the task
        """
        # Extract and deduplicate error messages
        error_messages = set()
        for _, error in batch_config.failed_batches.items():
            error_messages.add(str(error))

        # Create detailed error message
        if len(error_messages) == 1:
            # Single error type
            error_detail = f"Error: {list(error_messages)[0]}"
        else:
            # Multiple error types
            error_detail = "Errors: " + " | ".join(sorted(error_messages))

        error_msg = (
            f"Aborting task: All {len(batch_config.failed_batches)} batches failed. "
            f"No successful processing occurred. {error_detail}"
        )
        logger.error(error_msg)

        # Send abort message to modeller
        await self.protocol.mailbox.send_task_abort_message(
            error_msg, Reason.WORKER_ERROR
        )

        # Raise the abort error
        raise BatchResilienceAbortError(error_msg)

    async def check_and_handle_zero_successful_files(
        self, batch_config: BatchConfig
    ) -> None:
        """Check if both all batches failed AND all individual files failed.

        This is called after individual file diagnosis to determine if we should abort.

        Args:
            batch_config: The batch configuration object

        Raises:
            BatchResilienceAbortError: If no files succeeded in either batch
                or individual processing
        """
        # Check if we had no successful batches
        if len(batch_config.successful_batches) > 0:
            return  # We had some successful batches

        # Check if we had any successful individual files
        successful_individual_files = sum(
            1 for result in batch_config.individual_file_results.values() if result
        )

        if successful_individual_files > 0:
            logger.info(
                f"All batches failed, but {successful_individual_files} "
                f"{'file' if successful_individual_files == 1 else 'files'} "
                f"succeeded individually. Task will be marked as complete."
            )
            return  # We had some successful individual files

        # Both batches and individual files all failed - abort the task
        error_msg = (
            f"Aborting task: All {len(batch_config.failed_batches)} batches failed AND "
            f"all individual file retries failed. No successful processing occurred."
        )
        logger.error(error_msg)

        # Send abort message to modeller & raise error
        await self.protocol.mailbox.send_task_abort_message(
            error_msg, Reason.WORKER_ERROR
        )
        raise BatchResilienceAbortError(error_msg)

    async def retry_failed_files_individually(self, batch_config: BatchConfig) -> None:
        """Retry files from failed batches individually to identify problematic files.

        Test each file from failed batches individually to determine if the file itself
        is problematic or if the issue was batch-level (e.g., resource constraints).

        This runs as part of the batch execution flow, before the batch complete message
        is sent.

        Args:
            batch_config: The batch configuration for the worker.
        """
        # Collect all files from failed batches
        failed_files = set()
        for batch_num in batch_config.failed_batches:
            files_in_batch = batch_config.failed_batch_file_mapping.get(batch_num, [])
            failed_files.update(files_in_batch)

        if not failed_files:
            logger.info("No files to retry individually.")
            return

        logger.info(f"Individual file diagnosis: testing {len(failed_files)} files...")

        # Save current datasource state
        original_override = batch_config.datasource.selected_file_names_override.copy()

        successful_individual_files = 0
        failed_individual_files = 0

        for i, file_path in enumerate(failed_files, 1):
            try:
                # Set datasource to process only this file
                batch_config.datasource.selected_file_names_override = [file_path]

                # Reinitialize algorithms with single-file datasource
                for algo in self.protocol.algorithms:
                    algo.initialise_data(
                        datasource=batch_config.datasource,
                        data_splitter=batch_config.data_splitter,
                    )

                # Run the protocol on this single file
                logger.debug(
                    f"Testing individual file {i}/{len(failed_files)}: {file_path}"
                )
                # Only mark as final batch if this is the LAST file being retried
                is_final_individual_file = i == len(failed_files)

                return_val = await self.execute_run_func(
                    final_batch=is_final_individual_file
                )

                # Manually call on_run_end hooks to ensure processed files
                # are saved to cache
                hook_kwargs_copy = self.hook_kwargs.copy()
                hook_kwargs_copy["results"] = return_val
                try:
                    for hook in get_hooks(HookType.PROTOCOL):
                        hook.on_run_end(self.protocol, **hook_kwargs_copy)
                except Exception as e:
                    logger.error(
                        f"`on_run_end` hook failed during resilience retry: {e}"
                    )

                # If we get here, the file processed successfully
                successful_individual_files += 1
                batch_config.individual_file_results[file_path] = True
                logger.debug(f"File processed successfully individually: {file_path}")
                # Call resilience progress hook for success
                for pod_hook in get_hooks(HookType.POD):
                    pod_hook.on_resilience_progress(
                        task_id=self.protocol.mailbox.task_id,
                        modeller_username=getattr(
                            self.protocol.mailbox, "modeller_name", ""
                        ),
                        current_file=i,
                        total_files=len(failed_files),
                        file_name=file_path,
                        success=True,
                    )
            except Exception as e:
                # This file failed individually - it's genuinely problematic
                failed_individual_files += 1
                batch_config.file_level_errors[file_path] = e
                batch_config.individual_file_results[file_path] = False
                logger.debug(f"File failed individually: {file_path} - {str(e)}")
                for pod_hook in get_hooks(HookType.POD):
                    pod_hook.on_resilience_progress(
                        task_id=self.protocol.mailbox.task_id,
                        modeller_username=getattr(
                            self.protocol.mailbox, "modeller_name", ""
                        ),
                        current_file=i,
                        total_files=len(failed_files),
                        file_name=file_path,
                        success=False,
                    )
        # Restore original datasource state
        batch_config.datasource.selected_file_names_override = original_override

        # Log summary
        logger.info(
            f"Individual file diagnosis completed: "
            f"{successful_individual_files} file(s) succeeded individually, "
            f"{failed_individual_files} file(s) failed individually"
        )

        # Log diagnostic insights
        if successful_individual_files > 0:
            logger.info(
                f"{successful_individual_files} file(s) work individually but "
                f"failed in batch - this suggests resource constraints "
                f"or batch-level issues."
            )

        if failed_individual_files > 0:
            logger.info(
                f"{failed_individual_files} file(s) are genuinely problematic and "
                f"should be investigated or removed from the dataset"
            )

    def get_error_reports_save_dir(self) -> Path:
        """Establish which directory to save error reports to.

        Either uses the task results folder if available, or the current directory.

        Returns:
            Path object for where to save the batch resilience report
        """
        error_report_folder: Path

        # Will either be the TASK_RESULTS_DIR with project ID and task ID
        # folders, or OUTPUT_DIR/"task-results".
        #
        # Use the direct get_task_results_dir() method rather than the
        # get_task_results_directory() utility method, as we have different
        # handling for the context=None case.
        task_results_dir = self.context.get_task_results_dir()
        error_report_folder = task_results_dir / ERROR_REPORT_FOLDER

        error_report_folder.mkdir(parents=True, exist_ok=True)

        logger.info(f"Using task save path for batch report: {error_report_folder}")

        return error_report_folder

    def write_failed_files_report(self, batch_config: BatchConfig) -> None:
        """Write CSV report for all failed batches and their files.

        If individual file retry is enabled, creates a detailed file-level report.
        """
        if not batch_config.failed_batches:
            return  # No failures to report

        # Find error reports directory
        error_reports_dir = self.get_error_reports_save_dir()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Choose report type based on whether individual file retry was enabled
        if (
            config.settings.individual_file_retry_enabled
            and batch_config.individual_file_results
        ):
            # Create detailed file-level report
            output_file = error_reports_dir / f"File_error_report_{timestamp}.csv"
            data = self.build_file_level_report_data(batch_config, report_timestamp)
            report_type = "file-level diagnosis"
            try:
                # Create DataFrame and write to CSV
                df = pd.DataFrame(data)
                df.to_csv(output_file, index=False)
                logger.info(
                    f"{report_type.title()} CSV report written to: {output_file}"
                )

            except Exception as e:
                logger.error(f"Failed to write {report_type} CSV report: {e}")
        else:
            logger.info(
                "Batch-level failures already reported immediately. "
                "No end-of-task batch report needed."
            )

        hook_kwargs = self.hook_kwargs.copy()
        hook_kwargs["batch_config"] = batch_config
        if (
            config.settings.individual_file_retry_enabled
            and config.settings.enable_batch_resilience
        ):
            try:
                for hook in get_hooks(HookType.PROTOCOL):
                    hook.on_resilience_end(self.protocol, **hook_kwargs)
            except Exception as e:
                logger.error(f"`on_resilience_end` hook failed: {e}")

    def build_file_level_report_data(
        self, batch_config: BatchConfig, report_timestamp: str
    ) -> list[dict]:
        """Build data for file-level diagnosis report.

        Args:
            batch_config: The batch configuration object
            report_timestamp: Timestamp for the report

        Returns:
            List of dictionaries containing file-level diagnosis data
        """
        data = []

        # Collect all files from failed batches
        all_failed_batch_files = set()
        for batch_num in batch_config.failed_batches:
            files_in_batch = batch_config.failed_batch_file_mapping.get(batch_num, [])
            all_failed_batch_files.update(files_in_batch)

        # Create a row for each file that was in a failed batch
        for file_path in sorted(all_failed_batch_files):
            # Determine the individual test result
            individual_result = batch_config.individual_file_results.get(
                file_path, "Not tested"
            )

            if individual_result is True:
                individual_status = "Success"
                individual_error = "No error. File processed successfully on retry."
                diagnosis = "Batch-level issue (resource constraints, timing, etc.)"
            elif individual_result is False:
                individual_status = "Failed"
                individual_error = str(
                    batch_config.file_level_errors.get(file_path, "Unknown error")
                )
                diagnosis = "File-level issue (corrupted file, processing error, etc.)"
            else:
                individual_status = "Not tested"
                individual_error = "Individual file diagnosis was not performed"
                diagnosis = "Unknown - file not tested individually"

            # Find which batch(es) this file was in
            batch_numbers = []
            for (
                batch_num,
                files_in_batch,
            ) in batch_config.failed_batch_file_mapping.items():
                if file_path in files_in_batch:
                    batch_numbers.append(str(batch_num + 1))

            batch_info = ", ".join(batch_numbers) if batch_numbers else "Unknown"
            row_data: dict[str, Any] = {}
            # Add patient metadata columns if available
            add_patient_metadata_columns(row_data, batch_config.datasource, file_path)
            row_data.update(
                {
                    "File path": file_path,
                    "Batch number": batch_info,
                    "Retry result": individual_status,
                    "Error": individual_error,
                    "Diagnosis": diagnosis,
                    "Report generated": report_timestamp,
                }
            )
            data.append(row_data)

        return data

    def build_batch_level_report_data(
        self, batch_config: BatchConfig, report_timestamp: str
    ) -> list[dict]:
        """Build data for batch-level failure report (original behavior).

        Args:
            batch_config: The batch configuration object
            report_timestamp: Timestamp for the report

        Returns:
            List of dictionaries containing batch-level failure data
        """
        data = []

        for batch_num, error in sorted(batch_config.failed_batches.items()):
            files_in_batch = batch_config.failed_batch_file_mapping.get(batch_num, [])
            for file_path in files_in_batch:
                row_data: dict[str, Any] = {}
                # Add patient metadata columns if available
                add_patient_metadata_columns(
                    row_data, batch_config.datasource, file_path
                )
                row_data.update(
                    {
                        "Batch number": batch_num + 1,
                        "Error": str(error),
                        "File path": file_path,
                        "Report generated": report_timestamp,
                        "Successful batches so far": len(
                            batch_config.successful_batches
                        ),
                        "Failed batches so far": len(batch_config.failed_batches),
                    }
                )
                data.append(row_data)

        return data
