"""ONNX inference backend for Bitfount models.

This module provides an inference-only `ONNXModel` that integrates with Bitfount
infrastructure (datastructure, databunch, dataloaders) and executes ONNX graphs via
onnxruntime on CPU, CUDA GPUs, or Apple Silicon (CoreML provider when available).
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
import os
from typing import Any, Optional, Union

import numpy as np
import onnxruntime as ort

from bitfount.config import has_cuda, has_mps
from bitfount.data.databunch import BitfountDataBunch
from bitfount.data.dataloaders import BitfountDataLoader
from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasplitters import DatasetSplitter, _InferenceSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.federated.types import TaskContext
from bitfount.types import InferrableModelProtocol, PredictReturnType

logger = logging.getLogger(__name__)


@dataclass
class ONNXSessionConfig:
    """Configuration for ONNX Runtime sessions.

    Args:
        providers: Preferred execution providers in order of priority. If not
            provided, a set of sensible defaults is auto-selected based on
            availability: CUDA, then CoreML (Apple Silicon), then CPU.
        intra_op_num_threads: Threads within a single operator. Defaults to
            onnxruntime's internal default when None.
        inter_op_num_threads: Threads across independent operators. Defaults to
            onnxruntime's internal default when None.
        graph_optimization_level: onnxruntime graph optimisations; defaults to
            ORT_ENABLE_ALL.
    """

    providers: Optional[list[str]] = None
    intra_op_num_threads: Optional[int] = None
    inter_op_num_threads: Optional[int] = None
    graph_optimization_level: ort.GraphOptimizationLevel = (
        ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    )


class ONNXModel(InferrableModelProtocol):
    """ONNX inference model using onnxruntime.

    This implementation is inference-only. It creates a Bitfount `BitfountDataBunch`
    and test dataloader for the provided datasource, converts any backend tensors to
    numpy arrays, and feeds them to an ONNX Runtime session.

    The entrypoint for execution is `predict`, which returns a `PredictReturnType`.
    Training and evaluation are not supported for this backend.
    """

    def __init__(
        self,
        *,
        datastructure: DataStructure,
        schema: BitfountSchema,
        batch_size: int = 32,
        session_config: Optional[ONNXSessionConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise an ONNXModel.

        Args:
            datastructure: Bitfount `DataStructure` describing inputs/targets.
            schema: Bitfount `BitfountSchema` associated with the datasource.
            batch_size: Batch size to use for test dataloader. Defaults to 32.
            session_config: Optional onnxruntime session configuration.
            **kwargs: Forwarded to `_BaseModel` base class.
        """
        # Attributes from the arguments
        self.datastructure: DataStructure = datastructure
        self.schema: BitfountSchema = schema
        self.batch_size = batch_size
        self.session_config = session_config or ONNXSessionConfig()

        # Public attributes
        self.databunch: Optional[BitfountDataBunch] = None
        self.test_dl: Optional[BitfountDataLoader] = None

        # Private attributes
        self._session: Optional[ort.InferenceSession] = None
        self._initialised: bool = False
        self._context: Optional[TaskContext] = None

    @property
    def initialised(self) -> bool:
        """Return True if the model has been initialised."""
        return self._initialised

    def initialise_model(
        self,
        data: Optional[BaseSource] = None,
        data_splitter: Optional[DatasetSplitter] = None,
        context: Optional[TaskContext] = None,
    ) -> None:
        """Initialise ORT session and prepare dataloaders for inference.

        Args:
            data: Optional datasource for inference. If provided, a test dataloader
                is created using an inference-only splitter.
            data_splitter: Optional splitter to use instead of `_InferenceSplitter`.
            context: Optional execution context (unused).
        """
        self._context = context
        self._initialised = True

        if data is not None:
            if data_splitter is None:
                data_splitter = _InferenceSplitter()
            self.databunch = BitfountDataBunch(
                data_structure=self.datastructure,
                schema=self.schema,
                datasource=data,
                data_splitter=data_splitter,
                ignore_support_cols=True,
            )
            self._set_dataloaders(self.batch_size)

    def predict(
        self,
        data: Optional[BaseSource] = None,
        **_: Any,
    ) -> PredictReturnType:
        """Run inference and return predictions.

        Args:
            data: Optional datasource to run inference on. If provided, the model may
                be (re-)initialised to use this datasource.

        Returns:
            PredictReturnType containing predictions and optional data keys. Data keys
                must be present if the datasource is file-based.

        Raises:
            ValueError: If no test dataloader is available.
        """
        if not self._initialised:
            if data is None:
                raise ValueError(
                    (
                        "Model not initialised and no data provided. Call "
                        "initialise_model() or pass a datasource to "
                        "predict(data=...)."
                    )
                )
            self.initialise_model(data=data)

        if self.test_dl is None:
            raise ValueError(
                "No test dataloader available. Initialise the model "
                "with a datasource first."
            )

        if self._session is None:
            raise ValueError("No session available. Deserialize the model first.")

        logger.info("Running inference on the test dataloader.")

        preds: list[np.ndarray] = []
        keys: list[str] = []
        for batch in self.test_dl:
            x, _y = batch[:2]  # Ignore keys for now if they are present
            # Stack the tensors along the last axis so that the first dimension is the
            # batch size and the last dimension is the number of features
            x_arr = np.stack(
                [x_i.cpu().numpy() for x_i in x], axis=-1, dtype=np.float32
            )
            result = self._session.run(
                None,  # None means "return all outputs"
                {self._session.get_inputs()[0].name: x_arr},  # use the first input name
            )
            # There is only one output but it still needs to be indexed; it should also
            # be a numpy array anyway but we convert it anyway just in case.
            preds.extend(list(np.asarray(result[0])))
            if self._expect_keys():
                keys.extend(list(batch[2]))

        return PredictReturnType(preds=preds, keys=keys or None)

    def deserialize(self, content: Union[str, os.PathLike, bytes], **_: Any) -> None:
        """Deserialise ONNX model from a path or bytes content.

        Args:
            content: Path to the ONNX file or a bytes object containing the model.
        """
        self._session = ort.InferenceSession(
            path_or_bytes=content,
            sess_options=self._create_session_options(),
            providers=self._select_providers(),
        )

    def _set_dataloaders(self, batch_size: Optional[int] = None) -> None:
        """Set train/validation/test dataloaders from the `databunch`.

        Args:
            batch_size: Optional batch size override. Defaults to `self.batch_size`.
        """
        if self.databunch is None:
            raise ValueError(
                "_set_dataloaders() requires the databunch to be set before being "
                "called."
            )

        self.test_dl = self.databunch.get_test_dataloader(batch_size or self.batch_size)

    def _expect_keys(self) -> bool:
        """Return True if filenames should be returned as data keys.

        This is True when the underlying datasource is file-based.

        Returns:
            True if filenames should be returned as data keys, False otherwise.

        Raises:
            ValueError: If the databunch is not set.
        """
        if self.databunch is None:
            raise ValueError(
                "_expect_keys() requires the databunch to be set before being called."
            )
        try:
            return isinstance(self.databunch.datasource, FileSystemIterableSource)
        except Exception:
            return False

    def _select_providers(self) -> list[str]:
        """Select ORT execution providers based on availability and settings."""
        available = set(ort.get_available_providers())
        if self.session_config.providers:
            requested = [p for p in self.session_config.providers if p in available]
            if requested:
                return requested
        if has_cuda() and "CUDAExecutionProvider" in available:
            return ["CUDAExecutionProvider", "CPUExecutionProvider"]
        if has_mps() and "CoreMLExecutionProvider" in available:
            return ["CoreMLExecutionProvider", "CPUExecutionProvider"]
        return ["CPUExecutionProvider"]

    def _create_session_options(self) -> ort.SessionOptions:
        """Create an ORT session options object."""
        so = ort.SessionOptions()
        if self.session_config.intra_op_num_threads is not None:
            so.intra_op_num_threads = self.session_config.intra_op_num_threads
        if self.session_config.inter_op_num_threads is not None:
            so.inter_op_num_threads = self.session_config.inter_op_num_threads
        so.graph_optimization_level = self.session_config.graph_optimization_level

        return so
