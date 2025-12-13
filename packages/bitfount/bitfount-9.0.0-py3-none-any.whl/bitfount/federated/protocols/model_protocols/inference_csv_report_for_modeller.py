"""Copy of the InferenceAndCSVReport protocol that sends metrics to Bitfount."""

from __future__ import annotations

from collections.abc import Sequence
from inspect import unwrap
import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Union, cast

import pandas as pd

from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.protocols.model_protocols.inference_csv_report import (
    InferenceAndCSVReport,
    _InferenceAndCSVReportCompatibleAlgoFactory_,
    _InferenceAndCSVReportCompatibleHuggingFaceAlgoFactory,
    _InferenceAndCSVReportCompatibleModelAlgoFactory,
    _InferenceAndCSVReportCompatibleModellerAlgorithm,
    _ModellerSide as _InferenceCSVModellerSide,
    _WorkerSide as _InferenceCSVWorkerSide,
)
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.types import ProtocolContext, get_task_results_directory
from bitfount.types import _StrAnyDict

if TYPE_CHECKING:
    from bitfount.federated.pod_vitals import _PodVitals
    from bitfount.hub.api import BitfountHub

logger = _get_federated_logger("bitfount.federated.protocols" + __name__)


class _ModellerSide(_InferenceCSVModellerSide):
    """Modeller side of the protocol.

    Args:
        algorithm: A list of algorithms to be run by the protocol. This should be
            a list of two algorithms, the first being the model inference algorithm
            and the second being the csv report algorithm.
        mailbox: The mailbox to use for communication with the Workers.
        **kwargs: Additional keyword arguments.
    """

    algorithm: Sequence[_InferenceAndCSVReportCompatibleModellerAlgorithm]

    def __init__(
        self,
        *,
        algorithm: Sequence[_InferenceAndCSVReportCompatibleModellerAlgorithm],
        mailbox: _ModellerMailbox,
        save_path: str | os.PathLike,
        **kwargs: Any,
    ) -> None:
        super().__init__(algorithm=algorithm, mailbox=mailbox, **kwargs)
        self.save_path = save_path

    async def run(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> Optional[_StrAnyDict]:
        """Runs Modeller side of the protocol.

        This just sends the model parameters to the workers and then tells
        the workers when the protocol is finished.

        Args:
            context: Optional. Run-time context for the protocol.
            **kwargs: Additional keyword arguments.
        """
        # Unwrap is hardcoded as return type of Any instead of generic
        # so we've had to cast it to conform.
        results = cast(
            Optional[_StrAnyDict],
            await unwrap(super().run)(
                self, context=context, results_from_worker=True, **kwargs
            ),
        )

        # Find the CSV Report save path and store the CSV results
        if results:
            task_results_dir = Path(self.save_path)

            for pod_identifier in results:
                # Carefully extract the CSV result in case it's not there or
                # if one pod returns something different
                maybe_csv = results[pod_identifier].get("csv", None)
                if maybe_csv:
                    csv_path = (
                        task_results_dir
                        / f"results_{pod_identifier.replace('/', '_')}.csv"
                    )
                    logger.info(
                        f"""Writing CSV results from pod '{pod_identifier}'
                        to '{csv_path}'
                        """
                    )

                    with open(csv_path, "w") as text_file:
                        text_file.write(maybe_csv)
                else:
                    logger.info(f'No CSV result returned by "{pod_identifier}"')

        return results


class _WorkerSide(_InferenceCSVWorkerSide):
    """Worker side of the protocol.

    Args:
        algorithm: A list of algorithms to be run by the protocol. This should be
            a list of two algorithms, the first being the model inference algorithm
            and the second being the csv report algorithm.
        mailbox: The mailbox to use for communication with the Modeller.
        **kwargs: Additional keyword arguments.
    """

    async def run(
        self,
        *,
        pod_vitals: Optional[_PodVitals] = None,
        context: ProtocolContext,
        final_batch: bool = False,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Runs the algorithm on worker side.

        Args:
            pod_vitals: Optional. Pod vitals instance for recording run-time details
                from the protocol run.
            context: Optional. Run-time context for the protocol.
            final_batch: If this run of the protocol represents the final run within
                a task.
            **kwargs: Additional keyword arguments.
        """
        # Unwrap is hardcoded as return type of Any instead of generic
        # so we've had to cast it to conform.
        return cast(
            pd.DataFrame,
            await unwrap(super().run)(
                self,
                pod_vitals=pod_vitals,
                context=context,
                return_results_to_modeller=True,
                final_batch=final_batch,
                **kwargs,
            ),
        )


class InferenceAndReturnCSVReport(InferenceAndCSVReport):
    """Protocol that sends runs inference and sends the result as CSV to the modeller.

    Extends InferenceAndCSVReport to send the number of records output to CSV.
    """

    def modeller(
        self,
        *,
        mailbox: _ModellerMailbox,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _ModellerSide:
        """Returns the Modeller side of the protocol."""
        algorithms = cast(
            Sequence[
                Union[
                    _InferenceAndCSVReportCompatibleAlgoFactory_,
                    _InferenceAndCSVReportCompatibleModelAlgoFactory,
                    _InferenceAndCSVReportCompatibleHuggingFaceAlgoFactory,
                ]
            ],
            self.algorithms,
        )
        modeller_algos = []
        for algo in algorithms:
            if hasattr(algo, "pretrained_file"):
                modeller_algos.append(
                    algo.modeller(pretrained_file=algo.pretrained_file, context=context)
                )
            else:
                modeller_algos.append(algo.modeller(context=context))
        return _ModellerSide(
            algorithm=modeller_algos,
            mailbox=mailbox,
            save_path=get_task_results_directory(context),
            **kwargs,
        )

    def worker(
        self,
        *,
        mailbox: _WorkerMailbox,
        hub: BitfountHub,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Returns worker side of the InferenceAndReturnCSVReport protocol.

        Args:
            mailbox: Worker mailbox instance to allow communication to the modeller.
            hub: `BitfountHub` object to use for communication with the hub.
            context: Optional. Run-time protocol context details for running.
            **kwargs: Additional keyword arguments.
        """
        algorithms = cast(
            Sequence[
                Union[
                    _InferenceAndCSVReportCompatibleAlgoFactory_,
                    _InferenceAndCSVReportCompatibleModelAlgoFactory,
                    _InferenceAndCSVReportCompatibleHuggingFaceAlgoFactory,
                ]
            ],
            self.algorithms,
        )
        return _WorkerSide(
            algorithm=[algo.worker(hub=hub, context=context) for algo in algorithms],
            mailbox=mailbox,
            **kwargs,
        )
