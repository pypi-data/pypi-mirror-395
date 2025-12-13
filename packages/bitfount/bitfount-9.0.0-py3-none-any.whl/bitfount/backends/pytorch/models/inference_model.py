"""PyTorch inference models for Bitfount."""

from abc import abstractmethod
from io import BytesIO
import logging
import os
from typing import Any, Optional, Union, cast

import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch
from torch import nn as nn
from torch.utils.data import DataLoader as PyTorchDataLoader

from bitfount.backends.pytorch import autodetect_gpu
from bitfount.backends.pytorch.models.base_models import (
    _TEST_STEP_OUTPUT,
    _TEST_STEP_OUTPUT_GENERIC,
)
from bitfount.backends.pytorch.utils import enhanced_torch_load
from bitfount.data.databunch import BitfountDataBunch
from bitfount.data.dataloaders import BitfountDataLoader
from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasplitters import DatasetSplitter, _InferenceSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.federated.types import TaskContext
from bitfount.types import InferrableModelProtocol, PredictReturnType
from bitfount.utils import _merge_list_of_dicts

logger = logging.getLogger(__name__)


class _BaseInferenceModel(InferrableModelProtocol):
    """Base class for PyTorch inference models with common functionality."""

    def __init__(
        self,
        *,
        datastructure: DataStructure,
        schema: BitfountSchema,
        batch_size: int = 32,
        **kwargs: Any,
    ) -> None:
        """Base initialization for inference models."""

        # Attributes from the arguments
        self.datastructure: DataStructure = datastructure
        self.schema: BitfountSchema = schema
        self.batch_size = batch_size

        # Public attributes
        self.databunch: Optional[BitfountDataBunch] = None
        self.test_dl: Optional[BitfountDataLoader] = None

        # Private attributes
        self._initialised: bool = False
        self._model: Optional[nn.Module] = None
        self._context: Optional[TaskContext] = None

        # Test attributes
        self._test_preds: Optional[Union[list[np.ndarray], pd.DataFrame]] = None
        self._test_keys: Optional[list[str]] = None

    @property
    def initialised(self) -> bool:
        """Return True if the model has been initialised."""
        return self._initialised

    @abstractmethod
    def create_model(self) -> nn.Module:
        """Creates and returns the underlying PyTorch model."""
        raise NotImplementedError("Subclasses must implement create_model()")

    def split_dataloader_output(self, data: Any) -> tuple[Any, ...]:
        """Splits the dataloader output into input data and loss modifiers."""
        if isinstance(data, (list, tuple)) and len(data) >= 2:
            x, sup = data[:2]
            return x[0], sup
        else:
            return (data,)

    def serialize(self, filename: Union[str, os.PathLike]) -> None:
        """Serialize model to file."""
        if not self._initialised:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model()
        assert self._model is not None  # nosec assert_used
        torch.save(self._model.state_dict(), filename)

    def deserialize(
        self,
        content: Union[str, os.PathLike, bytes],
        weights_only: bool = True,
        **kwargs: Any,
    ) -> None:
        """Deserialize model from file or bytes."""
        kwargs.update({"weights_only": weights_only})
        if not self._initialised:
            logger.info("Model not yet initialised. Auto-initialising model.")
            self.initialise_model()
        # Model has been initialised, assuring mypy of this
        assert self._model is not None  # nosec assert_used
        load_contents = BytesIO(content) if isinstance(content, bytes) else content
        self._model.load_state_dict(enhanced_torch_load(load_contents, **kwargs))

    def _set_dataloaders(self, batch_size: Optional[int] = None) -> None:
        """Set test dataloader from the `databunch`."""
        if self.databunch is None:
            raise ValueError(
                "_set_dataloaders() requires the databunch to be set "
                "before being called."
            )
        self.test_dl = self.databunch.get_test_dataloader(batch_size or self.batch_size)

    def _expect_keys(self) -> bool:
        """Return True if filenames should be returned as data keys."""
        if self.databunch is None:
            raise ValueError(
                "_expect_keys() requires the databunch to be set before being called."
            )
        try:
            return isinstance(self.databunch.datasource, FileSystemIterableSource)
        except Exception:
            return False


class PytorchLightningInferenceModel(pl.LightningModule, _BaseInferenceModel):
    """PyTorch Lightning inference model for Bitfount."""

    # Order is important here to ensure the pl Module is initialised properly
    # Required attributes
    _test_preds: Optional[Union[list[np.ndarray], pd.DataFrame]] = None
    _test_targets: Optional[list[np.ndarray]] = None
    _test_keys: Optional[list[str]] = None
    _pl_trainer: pl.Trainer

    def __init__(
        self,
        *,
        datastructure: DataStructure,
        schema: BitfountSchema,
        batch_size: int = 32,
        **kwargs: Any,
    ) -> None:
        """Inference model for PyTorch."""
        super().__init__(**kwargs)

        # Attributes from the arguments
        self.datastructure: DataStructure = datastructure
        self.schema: BitfountSchema = schema
        self.batch_size = batch_size

        # Private attributes
        self._initialised: bool = False
        self._model: Optional[nn.Module] = None
        self._context: Optional[TaskContext] = None

        # Test attributes
        self._test_preds: Optional[Union[list[np.ndarray], pd.DataFrame]] = None
        self._test_keys: Optional[list[str]] = None

        # Lightning-specific attributes
        self._pl_trainer: pl.Trainer = self.trainer_init()
        self._pl_test_step_outputs: list[_TEST_STEP_OUTPUT] = []

    def trainer_init(self) -> pl.Trainer:
        """Initialize PyTorch Lightning trainer."""
        gpu_kwargs = autodetect_gpu()
        trainer = pl.Trainer(
            max_epochs=-1,
            max_steps=-1,
            enable_checkpointing=False,
            logger=False,
            enable_model_summary=False,
            deterministic=True,
            **gpu_kwargs,
        )
        return trainer

    def forward(self, x: Any) -> Any:
        """Forward pass through the model."""
        if self._model is None:
            raise ValueError("Model not initialized. Call initialise_model() first.")

        if (
            self.datastructure.image_cols is not None
            and len(self.datastructure.image_cols) > 1
        ):
            aux = []
            for i in range(len(x)):
                aux.append(self._model(x[i]))
            return torch.cat([item[0] for item in aux], 1)
        else:
            return self._model(x)

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
            )
            self._set_dataloaders(self.batch_size)
        if self._model is None:
            self._model = self.create_model()

    def test_step(self, batch: Any, batch_idx: int) -> _TEST_STEP_OUTPUT:
        """Process a single batch during testing/inference.

        Override this step as required.

        Args:
            batch: The batch data
            batch_idx: Index of the batch

        Returns:
            Dictionary with predictions and targets
        """
        # Extract input data and optional keys
        # Extract X, y and other data from batch
        data, _y = batch[:2]
        # If the data provides data keys, extract those as well
        keys: Optional[list[str]] = None
        if self._expect_keys():
            keys = list(batch[2])
        x, *loss_modifiers = self.split_dataloader_output(data)
        # Get validation output and loss
        y_hat = self(x)
        # Output targets and prediction for later
        result: _TEST_STEP_OUTPUT
        if keys is not None:
            result = {"predictions": y_hat, "keys": keys}
        else:
            result = {"predictions": y_hat}

        self._pl_test_step_outputs.append(result)
        return result

    def on_test_epoch_end(self) -> None:
        """Called at the end of the test epoch.

        Aggregates the predictions and targets from the test set.

        :::caution

        If you are overwriting this method, ensure you set `self._test_preds` to
        maintain compatibility with `self._predict_local` unless you are overwriting
        both of them.

        :::
        """
        # Pass through copy as we are about to clear the original
        self._test_epoch_end(self._pl_test_step_outputs.copy())
        self._pl_test_step_outputs.clear()

    def _test_epoch_end(
        self,
        outputs: list[_TEST_STEP_OUTPUT],
    ) -> None:
        """Aggregates the predictions and targets from the test set.

        :::caution

        If you are overwriting this method, ensure you set `self._test_preds` to
        maintain compatibility with `self._predict_local` unless you are overwriting
        both of them.

        :::

        Args:
            outputs: list of outputs from each test step.
        """
        # Override the pl.lightning method, as it requires a different type for outputs.

        # Merge outputs into singular lists rather than a list of dicts.
        # NOTE: This also _flattens_ the non-scalar outputs
        # such that a list (of len Z) MxN tensors becomes a list
        # (of len ZxM) (N,) tensors
        merged_outputs: dict[str, list[Union[torch.Tensor, str]]] = (
            _merge_list_of_dicts(cast(list[_TEST_STEP_OUTPUT_GENERIC], outputs))
        )
        self._test_preds = [
            i.cpu().numpy()
            for i in cast(list[torch.Tensor], merged_outputs["predictions"])
        ]

        if self._expect_keys():
            self._test_keys = cast(list[str], merged_outputs["keys"])

            # If keys are expected, there should be the same number as the number of
            # predictions
            if (predictions_len := len(merged_outputs["predictions"])) != (
                keys_len := len(merged_outputs["keys"])
            ):
                raise ValueError(
                    f"Mismatch in number of predictions vs data keys;"
                    f" got {predictions_len} predictions and {keys_len} keys."
                )

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
        self._pl_trainer.test(
            model=self, dataloaders=cast(PyTorchDataLoader, self.test_dl)
        )
        if self._test_preds is not None:
            return PredictReturnType(preds=self._test_preds, keys=self._test_keys)

        raise ValueError("'self._test_preds' was not set by the model after inference.")


class PytorchInferenceModel(_BaseInferenceModel):
    """Simple PyTorch inference model for Bitfount.

    This class provides a minimal implementation for inference-only models,
    without requiring PyTorch Lightning or complex inheritance.

    Users only need to implement:
    1. create_model() - Return the PyTorch nn.Module to use

    All other methods have sensible defaults for inference.
    """

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        """Inference model for PyTorch."""
        super().__init__(**kwargs)
        # Device configuration
        self.device = self._get_device()

    def initialise_model(
        self,
        data: Optional[BaseSource] = None,
        data_splitter: Optional[DatasetSplitter] = None,
        context: Optional[TaskContext] = None,
    ) -> None:
        """Initialize model and prepare dataloaders for inference.

        Args:
            data: Optional datasource for inference. If provided, a test dataloader
                is created using an inference-only splitter.
            data_splitter: Optional splitter to use instead of `_InferenceSplitter`.
            context: Optional execution context (unused).
        """
        self._context = context
        self._initialised = True

        # Create databunch and dataloaders if data is provided
        if data is not None:
            if data_splitter is None:
                data_splitter = _InferenceSplitter()
            self.databunch = BitfountDataBunch(
                data_structure=self.datastructure,
                schema=self.schema,
                datasource=data,
                data_splitter=data_splitter,
            )
            self._set_dataloaders(self.batch_size)
        # Create the model if it doesn't exist
        if self._model is None:
            self._model = self.create_model()
            self._model.to(self.device)
            self._model.eval()  # Set to evaluation mode

    def forward(self, x: Any) -> Any:
        """Forward pass through the model."""
        if self._model is None:
            raise ValueError("Model not initialized. Call initialise_model() first.")

        if (
            self.datastructure.image_cols is not None
            and len(self.datastructure.image_cols) > 1
        ):
            aux = []
            for i in range(len(x)):
                aux.append(self._model(x[i]))
            return torch.cat([item[0] for item in aux], 1)
        else:
            return self._model(x)

    def _get_device(self) -> torch.device:
        """Get the appropriate device."""
        gpu_kwargs = autodetect_gpu()
        if gpu_kwargs["accelerator"] == "mps":
            return torch.device("mps")
        elif gpu_kwargs["accelerator"] == "gpu":
            return torch.device("cuda:0")
        else:
            return torch.device("cpu")

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
            PredictReturnType containing predictions and optional data keys.

        Raises:
            ValueError: If no test dataloader is available.
        """
        # Initialize model if needed
        if not self._initialised or (data is not None):
            self.initialise_model(data=data)

        if not hasattr(self, "test_dl") or self.test_dl is None:
            raise ValueError("No test dataloader available. Please provide data.")

        # Prepare to collect predictions and keys
        all_predictions: list[Any] = []
        all_keys = []

        # Set model to evaluation mode
        if self._model is not None:
            self._model.eval()

        # Run inference on batches
        with torch.no_grad():
            for batch in self.test_dl:
                # Handle batch structure like the working model
                if isinstance(batch, (list, tuple)) and len(batch) >= 2:
                    data_part, _y = batch[:2]
                else:
                    data_part = batch

                # Split dataloader output like your working model
                x, *loss_modifiers = self.split_dataloader_output(data_part)

                predictions = self.forward(x)

                # Split batch into individual samples
                all_predictions.extend(np.asarray(predictions.cpu()))

                if self._expect_keys():
                    all_keys.extend(list(batch[2]))
        # Return predictions
        return PredictReturnType(preds=all_predictions, keys=all_keys or None)
