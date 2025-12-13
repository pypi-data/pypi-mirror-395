"""Algorithm to train and evaluate a model on remote data."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Optional, TypeVar

from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
    _DistributedModelTypeOrReference,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ModelURLs, ProtocolContext
from bitfount.hub.api import BitfountHub
from bitfount.metrics import MetricCollection
from bitfount.types import (
    DistributedModelProtocol,
    _SerializedWeights,
)
from bitfount.utils import delegates

logger = _get_federated_logger(__name__)


DISTRIBUTED_MODEL_T = TypeVar("DISTRIBUTED_MODEL_T", bound=DistributedModelProtocol)
DISTRIBUTED_MODEL_TR = TypeVar(
    "DISTRIBUTED_MODEL_TR", bound=_DistributedModelTypeOrReference
)


class _ModellerSide(_BaseModellerModelAlgorithm[DISTRIBUTED_MODEL_T]):
    """Modeller side of the ModelTrainingAndEvaluation algorithm."""

    def run(
        self, results: Mapping[str, dict[str, float]]
    ) -> dict[str, dict[str, float]]:
        """Simply returns results."""
        return dict(results)


class _WorkerSide(_BaseWorkerModelAlgorithm[DISTRIBUTED_MODEL_T]):
    """Worker side of the ModelTrainingAndEvaluation algorithm."""

    def update_params(self, params: _SerializedWeights) -> None:
        """Updates model parameters."""
        model_params = self.model.deserialize_params(params)
        self.model.update_params(model_params)

    def run(
        self, model_params: Optional[_SerializedWeights] = None, **kwargs: Any
    ) -> dict[str, float]:
        """Runs training and evaluation and returns metrics."""
        if model_params is not None:
            self.update_params(model_params)
        self.model.fit(self.datasource)

        eval_output = self.model.evaluate()
        preds = eval_output.preds
        target = eval_output.targs

        m = MetricCollection.create_from_model(self.model)
        return m.compute(target, preds)


@delegates()
class ModelTrainingAndEvaluation(
    _BaseModelAlgorithmFactory[
        _ModellerSide, _WorkerSide, DISTRIBUTED_MODEL_T, DISTRIBUTED_MODEL_TR
    ],
):
    """Algorithm for training a model, evaluating it and returning metrics.

    :::note

    The metrics cannot currently be specified by the user.

    :::

    Args:
        model: The model to train and evaluate on remote data.

    Attributes:
        model: The model to train and evaluate on remote data.
    """

    _inference_algorithm: bool = False

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _ModellerSide:
        """Returns the modeller side of the ModelTrainingAndEvaluation algorithm."""
        model = self._get_model_from_reference_and_upload_weights(
            project_id=self.project_id
        )
        return _ModellerSide(model=model, **kwargs)

    def worker(
        self,
        *,
        hub: BitfountHub,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Returns the worker side of the ModelTrainingAndEvaluation algorithm.

        Args:
            hub: `BitfountHub` object to use for communication with the hub.
            context: Optional. Run-time protocol context details for running.
                May contain URLs for downloading models directly rather than from
                the hub.
            **kwargs: Additional keyword arguments to pass to the worker side.

        Returns:
            Worker side of the ModelTrainingAndEvaluation algorithm.
        """
        model_urls: Optional[dict[str, ModelURLs]] = context.model_urls
        model = self._get_model_and_download_weights(
            hub=hub,
            project_id=self.project_id,
            auth_model_urls=model_urls,
        )
        return _WorkerSide(model=model, **kwargs)
