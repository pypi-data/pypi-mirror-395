"""Algorithm to evaluate a model on remote data."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Optional, TypeVar, cast

from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmFactory,
    _BaseModellerModelAlgorithm,
    _BaseWorkerModelAlgorithm,
    _EvaluableModelTypeOrReference,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ModelURLs, ProtocolContext
from bitfount.hub.api import BitfountHub
from bitfount.metrics import MetricCollection
from bitfount.models.base_models import _BaseModel
from bitfount.types import EvaluableModelProtocol
from bitfount.utils import delegates

logger = _get_federated_logger(__name__)


EVALUABLE_MODEL_T = TypeVar("EVALUABLE_MODEL_T", bound=EvaluableModelProtocol)
EVALUABLE_MODEL_TR = TypeVar("EVALUABLE_MODEL_TR", bound=_EvaluableModelTypeOrReference)


class _ModellerSide(_BaseModellerModelAlgorithm[EVALUABLE_MODEL_T]):
    """Modeller side of the ModelEvaluation algorithm."""

    def run(
        self, results: Mapping[str, dict[str, float]]
    ) -> dict[str, dict[str, float]]:
        """Simply returns results."""
        return dict(results)


class _WorkerSide(_BaseWorkerModelAlgorithm[EVALUABLE_MODEL_T]):
    """Worker side of the ModelEvaluation algorithm."""

    def run(self, **kwargs: Any) -> dict[str, float]:
        """Runs evaluation and returns metrics."""

        eval_output = self.model.evaluate()
        preds = eval_output.preds
        target = eval_output.targs

        m = MetricCollection.create_from_model(
            cast(_BaseModel, self.model), self.model.metrics
        )

        return m.compute(target, preds)


@delegates()
class ModelEvaluation(
    _BaseModelAlgorithmFactory[
        _ModellerSide, _WorkerSide, EVALUABLE_MODEL_T, EVALUABLE_MODEL_TR
    ]
):
    """Algorithm for evaluating a model and returning metrics.

    :::note

    The metrics cannot currently be specified by the user.

    :::

    Args:
        model: The model to evaluate on remote data.

    Attributes:
        model: The model to evaluate on remote data.
    """

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _ModellerSide:
        """Returns the modeller side of the ModelEvaluation algorithm."""
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
        """Returns the worker side of the ModelEvaluation algorithm.

        Args:
            hub: `BitfountHub` object to use for communication with the hub.
            context: Optional. Run-time protocol context details for running.
                May contain URLs for downloading models directly rather than from
                the hub.
            **kwargs: Additional keyword arguments.

        Returns:
            The worker side of the ModelEvaluation algorithm.
        """
        model_urls: Optional[dict[str, ModelURLs]] = context.model_urls
        model = self._get_model_and_download_weights(
            hub=hub,
            project_id=self.project_id,
            auth_model_urls=model_urls,
        )
        return _WorkerSide(model=model, **kwargs)
