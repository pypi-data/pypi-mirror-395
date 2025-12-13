"""Algorithm for calculating Central Subfield Thickness (CST)."""

from __future__ import annotations

from bisect import bisect_left
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    List,
    Literal,
    Mapping,
    Optional,
    TypedDict,
    cast,
)

from marshmallow import fields
from natsort import natsorted
import numpy as np
import pandas as pd

from bitfount.data.datasources.base_source import (
    BaseSource,
    FileSystemIterableSource,
)
from bitfount.data.datasources.utils import ORIGINAL_FILENAME_METADATA_COLUMN
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.federated.algorithms.base import (
    BaseNonModelAlgorithmFactory,
    BaseWorkerAlgorithm,
    NoResultsModellerAlgorithm,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_types import (
    CST_DEFAULT_DIAMETER_MM,
    CST_DEFAULT_ILM_LAYER_NAME,
    CST_DEFAULT_RPE_LAYER_NAME,
    FOVEA_CENTRE_LANDMARK_INDEX,
    LAYER_DISPLAY_NAMES,
    LAYER_NAME_MAP,
    CSTMetrics,
    RetinalLayer,
)
from bitfount.federated.algorithms.ophthalmology.ophth_algo_utils import (
    get_data_for_files,
    is_file_iterable_source,
)
from bitfount.federated.exceptions import DataProcessingError
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.types import ProtocolContext

if TYPE_CHECKING:
    from bitfount.federated.privacy.differential import DPPodConfig
    from bitfount.types import T_FIELDS_DICT

logger = _get_federated_logger("bitfount.federated")

CENTRAL_SLICE = "central_slice"
FOVEA_LANDMARK = "landmarks"


class RLInstance(TypedDict, total=False):
    """Typed Dict for Retinal Layer instance."""

    type: Literal["polygon"]
    className: str
    points: List[float] | List[int]
    attributes: List[Any]
    classId: int
    probability: float


class RLMask(TypedDict, total=False):
    """Typed Dict for Retinal Layer mask."""

    instances: List[RLInstance]
    metadata: dict[str, Any]


class RLPrediction(TypedDict, total=False):
    """Typed Dict for Retinal Layer prediction."""

    mask: RLMask


class _WorkerSide(BaseWorkerAlgorithm):
    """Worker side of the algorithm for CST/CRT calculation."""

    def __init__(
        self,
        cst_diameter_mm: float = CST_DEFAULT_DIAMETER_MM,
        ilm_layer_name: str = CST_DEFAULT_ILM_LAYER_NAME,
        rpe_layer_name: str = CST_DEFAULT_RPE_LAYER_NAME,
        fovea_landmark_idx: int = FOVEA_CENTRE_LANDMARK_INDEX,
        strict_measurement: bool = False,
        **kwargs: Any,
    ) -> None:
        """Initialize the CST calculation algorithm.

        Args:
            cst_diameter_mm: Diameter of the circular region for CST calculation.
            ilm_layer_name: Name of the ILM layer in the segmentation.
            rpe_layer_name: Name of the RPE layer in the segmentation.
            fovea_landmark_idx: Index of the fovea landmark to use
                (0=start, 1=end, 2=middle).
            strict_measurement: If True, only calculate if both ILM and RPE are
                available. If False, use next available layer as fallback
                (default: False).
            **kwargs: Additional keyword arguments.
        """
        self.cst_diameter_mm = cst_diameter_mm
        self.ilm_layer_name = ilm_layer_name
        self.rpe_layer_name = rpe_layer_name
        self.fovea_landmark_idx = fovea_landmark_idx
        self.strict_measurement = strict_measurement
        super().__init__(**kwargs)

    def initialise(
        self,
        *,
        datasource: BaseSource,
        data_splitter: Optional[DatasetSplitter] = None,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the algorithm with datasource."""
        self.initialise_data(datasource=datasource, data_splitter=data_splitter)

    def run(
        self,
        layer_predictions: pd.DataFrame,
        fovea_predictions: pd.DataFrame,
        filenames: Optional[list[str]] = None,
    ) -> dict[str, Optional[CSTMetrics]]:
        """Calculate CST/CRT metrics for each file from model predictions.

        Args:
            layer_predictions: DataFrame with retinal layer segmentation predictions.
            fovea_predictions: DataFrame with fovea predictions containing
                'central_slice' and 'landmarks' columns.
            filenames: List of files that the results correspond to. If not
                provided, will use filenames from predictions.

        Returns:
            Dictionary of original filenames to CSTMetrics objects.
        """
        # Fail fast if there are no predictions
        if layer_predictions.empty:
            logger.warning("No layer predictions provided")
            return {}

        if fovea_predictions.empty:
            logger.warning("No fovea predictions provided")
            return {}
        # Get filenames if not provided
        if filenames is None:
            if ORIGINAL_FILENAME_METADATA_COLUMN not in layer_predictions.columns:
                raise DataProcessingError(
                    f"Column '{ORIGINAL_FILENAME_METADATA_COLUMN}' not found "
                    f"in predictions"
                )
            filenames = layer_predictions[ORIGINAL_FILENAME_METADATA_COLUMN].tolist()

        # Verify fovea predictions have the filename column for merging
        if ORIGINAL_FILENAME_METADATA_COLUMN not in fovea_predictions.columns:
            raise DataProcessingError(
                f"Column '{ORIGINAL_FILENAME_METADATA_COLUMN}' not found "
                f"in Fovea model predictions."
            )

        # Get DICOM metadata for each file
        if not is_file_iterable_source(self.datasource):
            raise DataProcessingError(
                "CST calculation requires a FileSystemIterableSource."
            )

        datasource_df = get_data_for_files(
            cast(FileSystemIterableSource, self.datasource),
            filenames,
        )
        # Check that we have the expected number of results for the number of files
        if len(filenames) != len(datasource_df):
            raise DataProcessingError(
                f"Length of results ({len(datasource_df)}"
                f" does not match the number of files ({len(filenames)})"
                f" while processing trial calculations."
            )
        # TODO: [BIT-6545] remove this check if we have datasource filters
        #  for required fields
        # Verify required columns exist
        required_columns = [
            "Slice Thickness",
            "Pixel Spacing Row",
            "Pixel Spacing Column",
        ]
        missing_columns = [
            col for col in required_columns if col not in datasource_df.columns
        ]
        if missing_columns:
            logger.error(f"Missing required columns in datasource: {missing_columns}")
            return {fn: None for fn in (filenames or [])}

        # Merge fovea predictions with metadata
        merged_df = datasource_df.merge(
            fovea_predictions,
            on=ORIGINAL_FILENAME_METADATA_COLUMN,
            how="left",
            suffixes=("", "_fovea"),
        )

        results: dict[str, Optional[CSTMetrics]] = {}
        if ORIGINAL_FILENAME_METADATA_COLUMN not in layer_predictions.columns:
            raise DataProcessingError(
                f"Column '{ORIGINAL_FILENAME_METADATA_COLUMN}' not found "
                f"in Retinal Layer model predictions."
            )
        # Null keys are not allowed since filenames this is a strict key
        null_mask = layer_predictions[ORIGINAL_FILENAME_METADATA_COLUMN].isna()
        if null_mask.any():
            n_null = int(null_mask.sum())
            raise DataProcessingError(
                f"Found {n_null} row(s) with null "
                f"'{ORIGINAL_FILENAME_METADATA_COLUMN}' in layer_predictions"
            )

        try:
            layer_predictions_indexed = layer_predictions.set_index(
                ORIGINAL_FILENAME_METADATA_COLUMN,
                verify_integrity=True,  # ensures uniqueness
            )
        except ValueError as e:
            # Diagnose duplicates and report the top offenders
            dup_counts = (
                layer_predictions[ORIGINAL_FILENAME_METADATA_COLUMN]
                .value_counts()
                .loc[lambda s: s > 1]
                .sort_values(ascending=False)
            )
            top = ", ".join([f"{k} x{int(v)}" for k, v in dup_counts.head(10).items()])
            logger.error(
                "Duplicate _original_filename values in layer_predictions. "
                f"Top duplicates: {top}"
            )
            raise DataProcessingError(
                f"Duplicate keys in '{ORIGINAL_FILENAME_METADATA_COLUMN}' in "
                f"layer_predictions. Resolve duplicates before running. "
                f"Top duplicates: {top}"
            ) from e
        for filename in filenames:
            try:
                layer_pred_obj = layer_predictions_indexed.loc[filename]

                # Ensure a single-row Series (pandas typing: Series | DataFrame)
                if isinstance(layer_pred_obj, pd.DataFrame):
                    layer_pred = layer_pred_obj.iloc[0]
                else:
                    layer_pred = layer_pred_obj

                # Get metadata and fovea prediction for this file
                file_data = merged_df[
                    merged_df[ORIGINAL_FILENAME_METADATA_COLUMN] == filename
                ]

                if file_data.empty:
                    logger.warning(f"No metadata found for {filename}")
                    results[filename] = None
                    continue

                file_row = file_data.iloc[0]

                # Calculate CST/CRT metrics
                metrics = self._calculate_cst_crt(layer_pred, file_row)
                results[filename] = metrics

            except Exception as e:
                logger.error(f"Error calculating CST/CRT for {filename}: {e}")
                logger.debug(e, exc_info=True)
                results[filename] = None

        return results

    def _calculate_cst_crt(
        self,
        layer_pred: pd.Series,
        file_row: pd.Series,
    ) -> CSTMetrics:
        """Calculate CST or CRT for a single file.

        Args:
            layer_pred: Layer segmentation predictions for one file.
            file_row: Row containing DICOM metadata and fovea predictions.

        Returns:
            CSTMetrics object with calculated values.
        """
        # Parse fovea coordinates from the fovea model output
        fovea_coords = self._parse_fovea_coordinates(file_row)

        if fovea_coords is None:
            logger.warning("Fovea coordinates not available")
            return CSTMetrics()

        # Extract DICOM metadata
        slice_thickness_mm = file_row.get("Slice Thickness", None)
        pixel_spacing_row_mm = file_row.get("Pixel Spacing Row", None)
        pixel_spacing_column_mm = file_row.get("Pixel Spacing Column", None)

        if (
            slice_thickness_mm is None
            or pd.isna(slice_thickness_mm)
            or pixel_spacing_row_mm is None
            or pd.isna(pixel_spacing_row_mm)
            or pixel_spacing_column_mm is None
            or pd.isna(pixel_spacing_column_mm)
        ):
            logger.warning(
                f"Required DICOM metadata not available: "
                f"slice_thickness={slice_thickness_mm}, "
                f"pixel_spacing_row={pixel_spacing_row_mm}, "
                f"pixel_spacing_column={pixel_spacing_column_mm}"
            )
            return CSTMetrics(fovea_coordinates=fovea_coords)

        # Parse layer segmentations and build thickness map
        thickness_result = self._build_thickness_map(
            layer_pred, float(pixel_spacing_row_mm)
        )

        if thickness_result is None or thickness_result[0] is None:
            return CSTMetrics(
                fovea_coordinates=fovea_coords,
                ilm_layer_present=False,
                rpe_layer_present=False,
            )
        thickness_map_um, ilm_present, rpe_present, inner_layer, outer_layer = (
            thickness_result
        )

        # Calculate CST or CRT based on diameter. If diameter is 0, calculate
        # only CRT (Central Retinal Thickness at single center point)
        # Otherwise, calculate CST (Central Subfield Thickness)
        cst_metrics = self._compute_cst(
            thickness_map_um,
            fovea_coords,
            float(slice_thickness_mm),
            float(pixel_spacing_column_mm),
            self.cst_diameter_mm,
        )

        # Create measurement type description
        measurement_type = f"{inner_layer} to {outer_layer}"
        # Ensure n_samples is an integer or None
        cst_n_samples = (
            int(n_samples)
            if (n_samples := cst_metrics.get("n_samples")) is not None
            else None
        )
        return CSTMetrics(
            cst_mean_um=cst_metrics.get("mean_um"),
            cst_median_um=cst_metrics.get("median_um"),
            cst_std_um=cst_metrics.get("std_um"),
            cst_n_samples=cst_n_samples,
            cst_diameter_mm=cst_metrics.get("diameter_mm"),
            fovea_coordinates=fovea_coords,
            ilm_layer_present=ilm_present,
            rpe_layer_present=rpe_present,
            inner_layer_used=inner_layer,
            outer_layer_used=outer_layer,
            measurement_type=measurement_type,
        )

    def _parse_fovea_coordinates(
        self, file_row: pd.Series
    ) -> Optional[tuple[float, float, float]]:
        """Parse fovea center coordinates from fovea model predictions.

        This follows the same approach as the GA trial calculation algorithm,
        extracting a specific landmark from the central slice. Assumes landmarks
        are contiguous triples per slice: [start, end, middle].

        Args:
            file_row: Row containing 'central_slice' and 'landmarks' columns.

        Returns:
            Tuple of (slice, x, y) coordinates, or None if parsing fails.
        """
        try:
            # Get central slice & landmarks from the file row
            central_slice = file_row.get(CENTRAL_SLICE, None)
            landmarks_list = file_row.get(FOVEA_LANDMARK, None)

            if central_slice is None or pd.isna(central_slice):
                logger.warning(
                    "Central slice prediction missing. Skipping CST calculation."
                )
                return None
            # The model should always output at least 3 landmarks (start, end, middle)
            if landmarks_list is None or len(landmarks_list) < 3:
                logger.warning(
                    "Fovea landmarks missing/invalid. Skipping CST calculation."
                )
                return None
            cs = int(central_slice)
            # landmarks_list is a list of [slice, x, y] coordinates
            # Example: [[62, 467, 694], [62, 585, 685], [62, 515, 700], ...]
            # There are typically 3 landmarks per slice (start, end, middle)
            if not landmarks_list or not isinstance(landmarks_list, list):
                logger.warning("Invalid fovea_landmarks format")
                return None

            # Get the index of the first landmark at central_slice
            central_slice_column_idx = bisect_left(
                landmarks_list, cs, key=lambda x: x[0]
            )

            # Ensure the index found truly corresponds to the desired slice.
            if (
                central_slice_column_idx >= len(landmarks_list)
                or int(landmarks_list[central_slice_column_idx][0]) != cs
            ):
                logger.warning(
                    f"Central slice {central_slice} not found in landmarks. "
                    "Skipping CST calculation."
                )
                return None

            # With contiguous triples per slice, the start entry is at
            # central_slice_column_idx, so the target entry is offset
            # by fovea_landmark_idx (0=start, 1=end, 2=middle).
            landmark_idx = self.fovea_landmark_idx + central_slice_column_idx

            if (
                landmark_idx >= len(landmarks_list)
                or int(landmarks_list[landmark_idx][0]) != cs
            ):
                logger.warning(
                    f"Landmark index {landmark_idx} not found at central slice"
                    f" {central_slice}.  Skipping distance calculation."
                )
                return None

            # Get the landmark coordinates [slice, x, y]
            fovea_center = landmarks_list[landmark_idx]

            fovea_slice = float(fovea_center[0])
            fovea_x = float(fovea_center[1])
            fovea_y = float(fovea_center[2])

            logger.debug(
                f"Parsed fovea center from central_slice={central_slice}, "
                f"landmark_idx={landmark_idx}: ({fovea_slice}, {fovea_x}, {fovea_y})"
            )

            return (fovea_slice, fovea_x, fovea_y)

        except Exception as e:
            logger.error(f"Error parsing fovea coordinates: {e}")
            logger.debug(e, exc_info=True)
            return None

    def _parse_bscan_prediction(self, bscan_prediction: Any) -> Optional[RLPrediction]:
        """Preprocess B-scan prediction string for JSON parsing."""
        if bscan_prediction is None or bscan_prediction is pd.NA:
            return None
        if isinstance(bscan_prediction, float) and np.isnan(bscan_prediction):
            return None
        # Normalize to dict root with "instances"
        if isinstance(bscan_prediction, list):
            if len(bscan_prediction) == 0:
                return None
            bscan_prediction = bscan_prediction[0]
        if isinstance(bscan_prediction, dict) and "mask" in bscan_prediction:
            mask = bscan_prediction.get("mask", None)
            if isinstance(mask, dict) and "instances" in mask:
                return cast(RLPrediction, bscan_prediction)
        logger.warning(
            f"B-scan prediction has unexpected structure: {type(bscan_prediction)}"
        )
        return None

    def _get_available_layers(
        self, bscan_prediction: RLPrediction, available_layers: set[str]
    ) -> set[str]:
        """Collect unique layer names from a B-scan prediction into available_layers."""
        # bscan_prediction expected format is {'mask': {'instances': [...]}}
        # the layer names can then be found in each instance's 'className' field
        mask = (bscan_prediction or {}).get("mask") or {}
        instances: List[RLInstance] = mask.get("instances") or []
        for instance in instances:
            layer_name = instance.get("className", "")
            if layer_name:
                available_layers.add(layer_name)
        return available_layers

    def _build_thickness_map(
        self, layer_pred: pd.Series, pixel_spacing_row_mm: float
    ) -> Optional[tuple[np.ndarray, bool, bool, str, str]]:
        """Build thickness map from layer segmentations with fallback support.

        Args:
            layer_pred: Layer predictions for one file.
            pixel_spacing_row_mm: Pixel spacing in row direction (mm/pixel).

        Returns:
            Tuple of (thickness_map_um, ilm_present, rpe_present,
            inner_layer_name, outer_layer_name). thickness_map_um is of
            shape (num_slices, width) in micrometers. Returns None if
            no valid thickness map can be built.
        """
        # Extract prediction columns based on altris model assumptions
        pred_cols = [
            col
            for col in layer_pred.index
            if col.startswith("Pixel_Data_") and col.endswith("_prediction")
        ]
        if not pred_cols:
            logger.warning("No prediction columns found")
            return None

        # Sort columns to maintain B-scan order
        pred_cols_sorted = natsorted(pred_cols)

        # Collect available layers across B-scans
        parsed_predictions: list[Optional[RLPrediction]] = []
        available_layers: set[str] = set()
        for col in pred_cols_sorted:
            bscan_prediction = layer_pred[col]
            bscan_prediction = self._parse_bscan_prediction(bscan_prediction)
            parsed_predictions.append(bscan_prediction)

            if bscan_prediction is not None and len(available_layers) < len(
                LAYER_NAME_MAP
            ):
                available_layers = self._get_available_layers(
                    bscan_prediction, available_layers
                )
        if not available_layers:
            logger.warning("No layers found in any predictions")
            return None

        logger.info(f"Available layers across all B-scans: {available_layers}")

        # Check if requested ILM and RPE are present
        ilm_present = self.ilm_layer_name in available_layers
        rpe_present = self.rpe_layer_name in available_layers

        # Determine which layers to use for thickness measurement
        inner_layer_name, outer_layer_name = self._select_measurement_layers(
            available_layers, ilm_present, rpe_present
        )
        # if no suitable layer pair found, return None and log warning
        if inner_layer_name is None or outer_layer_name is None:
            if self.strict_measurement:
                logger.warning(
                    f"Strict measurement enabled: both {self.ilm_layer_name} and "
                    f"{self.rpe_layer_name} required but not available"
                )
            else:
                logger.warning("No suitable layer pair found for thickness measurement")
            return None
        # Second pass: parse layer boundaries using cached predictions
        all_layers_per_bscan: list[dict[str, np.ndarray]] = []
        for bscan_prediction in parsed_predictions:
            if bscan_prediction is None:
                # Add empty dict for missing B-scans to maintain alignment
                all_layers_per_bscan.append({})
            else:
                # Parse using the already-loaded prediction
                layers = self._parse_layer_prediction(
                    bscan_prediction, inner_layer_name, outer_layer_name
                )
                all_layers_per_bscan.append(layers)
        # Determine maximum width from all B-scans
        max_width = 0
        for layers_dict in all_layers_per_bscan:
            inner_boundary = layers_dict.get(inner_layer_name)
            outer_boundary = layers_dict.get(outer_layer_name)

            # Check both boundaries
            for boundary in [inner_boundary, outer_boundary]:
                if (
                    boundary is not None
                    and isinstance(boundary, np.ndarray)
                    and len(boundary) > 0
                ):
                    max_x = int(np.max(boundary[:, 0]))  # X is first column
                    max_width = max(max_width, max_x + 1)

        if max_width == 0:
            logger.warning(
                "Could not determine image width - no valid boundaries found"
            )
            return None

        logger.debug(f"Interpolating boundaries to common grid with width={max_width}")

        # Only calculate thickness where BOTH layers have valid data
        inner_boundaries = []
        outer_boundaries = []
        num_valid_bscans = 0
        num_partial_overlap = 0

        for i, layers_dict in enumerate(all_layers_per_bscan):
            inner_boundary = layers_dict.get(inner_layer_name)
            outer_boundary = layers_dict.get(outer_layer_name)

            # Initialize with NaN (invalid by default)
            inner_interp = np.full(max_width, np.nan)
            outer_interp = np.full(max_width, np.nan)

            # Check if both boundaries present and valid
            if (
                inner_boundary is not None
                and isinstance(inner_boundary, np.ndarray)
                and len(inner_boundary) > 1
                and outer_boundary is not None
                and isinstance(outer_boundary, np.ndarray)
                and len(outer_boundary) > 1
            ):
                # Extract X and Y coordinates
                inner_x, inner_y = inner_boundary[:, 0], inner_boundary[:, 1]
                outer_x, outer_y = outer_boundary[:, 0], outer_boundary[:, 1]

                # Find the overlapping X-range where both layers have data
                inner_x_min, inner_x_max = int(np.min(inner_x)), int(np.max(inner_x))
                outer_x_min, outer_x_max = int(np.min(outer_x)), int(np.max(outer_x))

                # Calculate overlap range
                overlap_min = max(inner_x_min, outer_x_min)
                overlap_max = min(inner_x_max, outer_x_max)

                if overlap_max >= overlap_min:
                    # Interpolate only within the overlapping region
                    overlap_x_range = np.arange(overlap_min, overlap_max + 1)
                    inner_interp[overlap_min : overlap_max + 1] = np.interp(
                        overlap_x_range, inner_x, inner_y
                    )
                    outer_interp[overlap_min : overlap_max + 1] = np.interp(
                        overlap_x_range, outer_x, outer_y
                    )

                    num_valid_bscans += 1

                    # Log if we have partial coverage (not full width)
                    if overlap_min > 0 or overlap_max < max_width - 1:
                        num_partial_overlap += 1
                        logger.debug(
                            f"B-scan {i}: Partial overlap [{overlap_min}:{overlap_max}]"
                            f" of {max_width} (inner: [{inner_x_min}:{inner_x_max}], "
                            f"outer: [{outer_x_min}:{outer_x_max}])"
                        )
                else:
                    # No overlap between the two layers
                    logger.debug(
                        f"B-scan {i}: No overlap between inner and outer layer X-ranges"
                        f" (inner: [{inner_x_min}:{inner_x_max}], outer: "
                        f"[{outer_x_min}:{outer_x_max}])"
                    )
            else:
                # One or both boundaries missing or invalid
                logger.debug(
                    f"B-scan {i}: Missing or invalid boundary "
                    f"(inner="
                    f"{'valid' if inner_boundary is not None and len(inner_boundary) > 1 else 'invalid'}, "  # noqa: E501
                    f"outer="
                    f"{'valid' if outer_boundary is not None and len(outer_boundary) > 1 else 'invalid'})"  # noqa: E501
                )

            inner_boundaries.append(inner_interp)
            outer_boundaries.append(outer_interp)

        logger.info(
            f"Using {num_valid_bscans}/{len(all_layers_per_bscan)} B-scans "
            f"for thickness calculation"
        )
        if num_partial_overlap > 0:
            logger.info(
                f"{num_partial_overlap} B-scan(s) have partial X-range overlap "
                f"(thickness only calculated where both layers detected)"
            )

        # Try to convert to numpy arrays of shape: (num_slices, width)
        try:
            inner_array = np.array(inner_boundaries)
            outer_array = np.array(outer_boundaries)
        except Exception as e:
            logger.error(f"Error creating boundary arrays: {e}")
            logger.debug(
                f"Inner boundaries shapes: "
                f"{[b.shape if isinstance(b, np.ndarray) else len(b) for b in inner_boundaries]}"  # noqa: E501
            )
            logger.debug(
                f"Outer boundaries shapes: "
                f"{[b.shape if isinstance(b, np.ndarray) else len(b) for b in outer_boundaries]}"  # noqa: E501
            )
            return None

        # Calculate thickness in pixels (outer - inner, absolute value)
        # NaN values will propagate through this calculation
        thickness_pixels = np.abs(outer_array - inner_array)

        # Convert to micrometers (1 mm = 1000 µm)
        thickness_um = thickness_pixels * pixel_spacing_row_mm * 1000.0

        # Count how many valid thickness values we have
        num_valid_thickness = int(np.sum(~np.isnan(thickness_um)))
        total_possible = thickness_um.size

        logger.info(
            f"Built thickness map using {inner_layer_name} to {outer_layer_name}: "
            f"shape={thickness_um.shape}, mean={np.nanmean(thickness_um):.1f}µm, "
            f"valid_points={num_valid_thickness}/{total_possible} "
            f"({100 * num_valid_thickness / total_possible:.1f}%)"
        )
        return (
            thickness_um,
            ilm_present,
            rpe_present,
            inner_layer_name,
            outer_layer_name,
        )

    def _find_available_layers(
        self, all_layers_per_bscan: list[dict[str, np.ndarray]]
    ) -> set[str]:
        """Find which layers are available across the B-scans.

        Args:
            all_layers_per_bscan: List of dicts mapping layer names
                to boundaries for each B-scan.

        Returns:
            Set of layer names that appear in at least one B-scan.
        """
        available: set[str] = set()
        for layers_dict in all_layers_per_bscan:
            available.update(layers_dict.keys())
        return available

    def _select_measurement_layers(
        self,
        available_layers: set[str],
        ilm_present: bool,
        rpe_present: bool,
    ) -> tuple[Optional[str], Optional[str]]:
        """Select which layers to use for thickness measurement with fallback logic.

        Args:
            available_layers: Set of available layer names.
            ilm_present: Whether the requested ILM layer is present.
            rpe_present: Whether the requested RPE layer is present.

        Returns:
            Tuple of (inner_layer_name, outer_layer_name) or (None, None)
            if no suitable pair found.
        """
        # If strict measurement is enabled, only use ILM and RPE
        if self.strict_measurement:
            if ilm_present and rpe_present:
                return self.ilm_layer_name, self.rpe_layer_name
            else:
                return None, None

        # Non-strict: use fallback logic
        inner_layer = self._find_fallback_layer(
            self.ilm_layer_name, available_layers, search_direction="inner"
        )
        outer_layer = self._find_fallback_layer(
            self.rpe_layer_name, available_layers, search_direction="outer"
        )

        if inner_layer and outer_layer:
            # Get enum values for the layers
            inner_enum = LAYER_NAME_MAP.get(inner_layer)
            outer_enum = LAYER_NAME_MAP.get(outer_layer)
            # Verify that inner layer comes before outer layer in the retinal order
            if inner_enum is not None and outer_enum is not None:
                if inner_enum < outer_enum:
                    if (
                        inner_layer != self.ilm_layer_name
                        or outer_layer != self.rpe_layer_name
                    ):
                        logger.info(
                            f"Using fallback layers: {inner_layer} to {outer_layer} "
                            f"(requested: {self.ilm_layer_name} to {self.rpe_layer_name})"  # noqa: E501
                        )
                    return inner_layer, outer_layer
                else:
                    logger.warning(
                        f"Invalid layer order: {inner_layer} (depth {inner_enum}) "
                        f"should come before {outer_layer} (depth {outer_enum})"
                    )
            else:
                logger.warning(
                    f"Layer not found in LAYER_NAME_MAP: {inner_layer=}, {outer_layer=}"
                )
        return None, None

    def _find_fallback_layer(
        self,
        preferred_layer: str,
        available_layers: set[str],
        search_direction: Literal["inner", "outer"],
    ) -> Optional[str]:
        """Find a fallback layer if the preferred layer is not available."""
        # If preferred layer is available, use it
        if preferred_layer in available_layers:
            return preferred_layer

        # Get enum value for preferred layer
        preferred_enum = LAYER_NAME_MAP.get(preferred_layer)
        if preferred_enum is None:
            logger.warning(f"Preferred layer '{preferred_layer}' not in LAYER_NAME_MAP")
            return None

        # Search in the specified direction
        if search_direction == "inner":
            # Search towards ILM (decreasing depth)
            candidate_enums = sorted(
                [e for e in RetinalLayer if e < preferred_enum],
                reverse=True,  # Start from closest to preferred
            )
        else:  # "outer"
            # Search towards Bruch's Membrane (increasing depth)
            candidate_enums = sorted([e for e in RetinalLayer if e > preferred_enum])

        # Find first available candidate
        for candidate_enum in candidate_enums:
            candidate_layer = LAYER_DISPLAY_NAMES[candidate_enum]
            if candidate_layer in available_layers:
                logger.debug(
                    f"Fallback: using {candidate_layer} (depth {candidate_enum}) "
                    f"instead of {preferred_layer} (depth {preferred_enum})"
                )
                return candidate_layer

        logger.warning(
            f"No fallback layer found for {preferred_layer} in direction "
            f"{search_direction}"
        )
        return None

    def _get_available_layer_names(self, bscan_prediction: Any) -> set[str]:
        """Quickly extract available layer names without parsing full boundaries.

        Args:
            bscan_prediction: Prediction data.

        Returns:
            Set of available layer names.
        """
        try:
            # Handle double-nested list structure
            if isinstance(bscan_prediction, list):
                if len(bscan_prediction) > 0 and isinstance(bscan_prediction[0], list):
                    bscan_prediction = bscan_prediction[0][0]
                elif len(bscan_prediction) > 0:
                    bscan_prediction = bscan_prediction[0]

            # Extract just the layer names
            if isinstance(bscan_prediction, dict) and "mask" in bscan_prediction:
                instances = bscan_prediction["mask"].get("instances", [])
                return {
                    instance.get("className", "")
                    for instance in instances
                    if instance.get("className")
                }

            return set()
        except Exception as e:
            logger.error(f"Error getting available layer names: {e}")
            return set()

    def _split_points(self, points: np.ndarray) -> List[np.ndarray]:
        """Split flat points array into Nx2 coordinate array with [x, y] per row.

        Args:
            points: Flat array [x0, y0, x1, y1, ..., xN, yN]

        Returns:
            List containing single Nx2 array where each row is [x, y].
            Returns empty list if insufficient points.
        """
        if len(points) < 4:  # Need at least 2 coordinate pairs
            return []

        # Reshape flat array to Nx2: [[x0, y0], [x1, y1], ..., [xN, yN]]
        # Keep as float64 for sub-pixel precision (don't convert to int32)
        points_2d = points.reshape(-1, 2)

        # For closed polygons, extract only the boundary (from start to max X)
        x_coords = points_2d[:, 0]
        max_x_idx = np.argmax(x_coords)

        # Take from start to max_x (the forward boundary)
        boundary = points_2d[: max_x_idx + 1]

        # If boundary goes right-to-left, reverse it to be left-to-right
        if len(boundary) > 1 and boundary[0, 0] > boundary[-1, 0]:
            boundary = boundary[::-1]

        return [boundary]

    def _parse_layer_prediction(
        self, pred_data: RLPrediction, inner_layer_name: str, outer_layer_name: str
    ) -> dict[str, np.ndarray]:
        """Parse layer segmentation prediction and extract boundary coordinates.

        Handles multiple polygon instances per layer (combines their points).

        Args:
            pred_data: Prediction dict with key 'mask' → 'instances'.
            inner_layer_name: Name of the inner layer to extract (e.g., "ILM").
            outer_layer_name: Name of the outer layer to extract (e.g., "RPE Layer").

        Returns:
            Dictionary mapping layer names to lists of Nx2 arrays.
            Each array has rows of [x, y] coordinates representing the boundary.
            Format: {'ILM': [array([[x0, y0], [x1, y1], ...])], 'RPE Layer': [...]}
            Only returns the two requested layers.
        """

        required_layers = [inner_layer_name, outer_layer_name]

        try:
            layers: dict[str, np.ndarray] = {}

            instances: List[RLInstance] = []
            # Extract instances from the prediction structure
            if isinstance(pred_data, dict) and "mask" in pred_data:
                instances = pred_data["mask"].get("instances", [])
            # Collect points for inner and outer layers separately
            inner_layer_points: list[float] = []
            outer_layer_points: list[float] = []
            for instance in instances:
                if instance.get("type") != "polygon":
                    continue
                layer_name = instance.get("className", "")
                if layer_name not in required_layers:
                    continue
                points = instance.get("points", [])
                if not points or len(points) < 4:  # Need at least 2 coordinate pairs
                    continue
                # There might be more than one instance per layer - need to combine them
                if layer_name == inner_layer_name:
                    inner_layer_points.extend(points)
                if layer_name == outer_layer_name:
                    outer_layer_points.extend(points)
            # Process inner layer if we have points
            if len(inner_layer_points) >= 4:
                pts = self._split_points(np.array(inner_layer_points, dtype=np.float64))
                layers[inner_layer_name] = self._dedupe_layer_points(
                    pts[0], keep_mode="min"
                )
            else:
                layers[inner_layer_name] = np.array([], dtype=np.float64).reshape(
                    0, 2
                )  # Empty Nx2 array

            # Process outer layer if we have points
            if len(outer_layer_points) >= 4:
                pts = self._split_points(np.array(outer_layer_points, dtype=np.float64))
                layers[outer_layer_name] = self._dedupe_layer_points(
                    pts[0], keep_mode="max"
                )
            else:
                layers[outer_layer_name] = np.array([], dtype=np.float64).reshape(
                    0, 2
                )  # Empty Nx2 array
            return layers

        except Exception as e:
            logger.error(f"Error parsing layer prediction: {e}")
            logger.debug(e, exc_info=True)
            return {}

    def _dedupe_layer_points(
        self, points: np.ndarray, keep_mode: Literal["min", "max"] = "min"
    ) -> np.ndarray:
        """Remove duplicate X coordinates, keeping only one Y value per X.

        For retinal layer boundaries, when multiple Y values exist at the same X:
        - Inner layers (ILM, RNFL, etc.): keep minimum Y
        - Outer layers (RPE, Bruch's, etc.): keep maximum Y

        Args:
            points: Nx2 array where each row is [x, y]
            keep_mode: "min" to keep minimum Y, "max" to keep maximum Y

        Returns:
            Mx2 array with unique X values (M <= N)
        """
        if len(points) == 0:
            return points

        # Sort by X coordinate first (ensures proper ordering)
        points = points[points[:, 0].argsort()]

        # Find unique X values and their indices
        unique_x, inverse_indices = np.unique(points[:, 0], return_inverse=True)

        # For each unique X, select the appropriate Y value
        unique_points = np.zeros((len(unique_x), 2), dtype=points.dtype)
        unique_points[:, 0] = unique_x

        for i, _x_val in enumerate(unique_x):
            # Get all Y values for this X coordinate
            mask = inverse_indices == i
            y_values = points[mask, 1]

            # Keep min or max Y depending on mode
            if keep_mode == "min":
                unique_points[i, 1] = np.min(y_values)
            else:  # "max"
                unique_points[i, 1] = np.max(y_values)

        return unique_points

    def _compute_cst(
        self,
        thickness_um: np.ndarray,
        fovea_coords: tuple[float, float, float],
        slice_thickness_mm: float,
        pixel_spacing_x_mm: float,
        diameter_mm: float = 1.0,
    ) -> dict[str, Optional[float]]:
        """Compute CST and/or CRT based on diameter setting.

            - If diameter_mm == 0: This measures only CRT (single center point)
            - If diameter_mm > 0: We measure CST, using a circular region of the
            provided diameter.

        Args:
            thickness_um: Thickness map in micrometers, shape (num_slices, width).
            fovea_coords: Fovea center (slice, x, y). Only slice and x are used.
            slice_thickness_mm: Slice thickness in mm.
            pixel_spacing_x_mm: Pixel spacing in x direction in mm.
            diameter_mm: Diameter of circular region in mm.
                If 0, uses single center point (equivalent to CRT).

        Returns:
            Dictionary with mean_um, median_um, std_um, n_samples, and diameter_mm.
        """
        # Use only slice and x coordinates (en-face projection)
        cz, cx, _ = fovea_coords  # Ignore y coordinate
        num_slices, width = thickness_um.shape

        # Special case: diameter_mm == 0 means CRT only (single center point)
        if diameter_mm == 0:
            # Get integer indices for the center point
            slice_idx = int(round(cz))
            x_idx = int(round(cx))

            # Validate indices
            if not (0 <= slice_idx < num_slices and 0 <= x_idx < width):
                logger.warning(
                    f"Fovea center ({slice_idx}, {x_idx}) is outside image bounds "
                    f"({num_slices}, {width})"
                )
                return {
                    "mean_um": None,
                    "median_um": None,
                    "std_um": None,
                    "n_samples": 0,
                    "diameter_mm": diameter_mm,
                }

            # Get thickness at center point
            center_value = thickness_um[slice_idx, x_idx]

            # Check for NaN
            if np.isnan(center_value):
                logger.warning("Thickness value at fovea center is NaN")
                return {
                    "mean_um": None,
                    "median_um": None,
                    "std_um": None,
                    "n_samples": 0,
                    "diameter_mm": diameter_mm,
                }

            # For diameter=0, mean/median is just the center point value
            center_value_float = float(center_value)
            logger.debug(
                f"Center point thickness at ({slice_idx}, {x_idx}): "
                f"{center_value_float:.1f}µm"
            )

            return {
                "mean_um": center_value_float,
                "median_um": center_value_float,
                "std_um": 0.0,  # No variance for single point
                "n_samples": 1,
                "diameter_mm": diameter_mm,
            }

        # Otherwise, calculate CST using circular region
        # Build mm coordinate grids
        z_coords_mm = (np.arange(num_slices) - cz) * slice_thickness_mm
        x_coords_mm = (np.arange(width) - cx) * pixel_spacing_x_mm

        # Create meshgrid
        Z, X = np.meshgrid(z_coords_mm, x_coords_mm, indexing="ij")

        # Calculate distance from fovea center (Euclidean distance in en-face plane)
        d_mm = np.sqrt(Z**2 + X**2)

        # Create circular mask
        mask = d_mm <= (diameter_mm / 2.0)

        # Extract values within mask
        values = thickness_um[mask]

        # Calculate statistics
        n_valid = int(np.sum(~np.isnan(values)))

        if n_valid == 0:
            logger.warning("No valid thickness values within CST circular region")
            return {
                "mean_um": None,
                "median_um": None,
                "std_um": None,
                "n_samples": 0,
                "diameter_mm": diameter_mm,
            }

        result: dict[str, Optional[float]] = {
            "mean_um": float(np.nanmean(values)),
            "median_um": float(np.nanmedian(values)),
            "std_um": float(np.nanstd(values)),
            "n_samples": n_valid,
            "diameter_mm": diameter_mm,
        }

        logger.debug(
            f"CST (diameter={diameter_mm}mm): mean={result['mean_um']:.1f}µm, "
            f"n={result['n_samples']}"
        )

        return result

    @staticmethod
    def convert_cst_metrics_to_df(
        cst_metrics: Mapping[str, Optional[CSTMetrics]],
    ) -> pd.DataFrame:
        """Convert a dict of CSTMetrics objects into a dataframe.

        Args:
            cst_metrics: Mapping of original filename to CSTMetrics (or None).

        Returns:
            A dataframe with each row representing the CSTMetrics for a single file.
        """
        metrics_df = pd.DataFrame.from_records(
            (m.to_record() if m is not None else dict()) for m in cst_metrics.values()
        )
        metrics_df[ORIGINAL_FILENAME_METADATA_COLUMN] = list(cst_metrics.keys())

        expected_cols = CSTMetrics.expected_cols()
        existing_cols = metrics_df.columns.to_list()
        missing_cols = sorted(list(set(expected_cols) - set(existing_cols)))
        if missing_cols:
            logger.warning(
                "Columns were missing from the CST Metrics DataFrame: "
                f" {', '.join(missing_cols)}."
                f" Adding empty columns for these."
            )
            metrics_df = metrics_df.reindex(columns=existing_cols + expected_cols)

        return metrics_df


class CSTCalculationAlgorithm(
    BaseNonModelAlgorithmFactory[NoResultsModellerAlgorithm, _WorkerSide]
):
    """Algorithm for calculating Central Subfield Thickness (CST).

    This algorithm calculates:
    - CST: Mean thickness within a circular region (default 1mm diameter)
        centered on the fovea
    - CRT: Thickness at the single fovea center point, if the diameter
        is set to 0.

    The algorithm builds a 2D thickness map from B-scan layer segmentations
    (ILM to RPE distance) and samples this map using a circular region (CST)
    or single point (CRT) centered on the fovea coordinates. Measurements
    follow ETDRS grid standards.

    The algorithm supports fallback layer selection: if ILM or RPE are not
    available, it will automatically use the next closest layer in the retinal
    layer order (unless strict_measurement is enabled). The actual layers used
    are reported in the output.

    Args:
        datastructure: The data structure to use for the algorithm.
        cst_diameter_mm: Diameter of circular region for CST calculation in mm
            (default: 1.0).
        ilm_layer_name: Name of the Inner Limiting Membrane layer (default: "ILM").
        rpe_layer_name: Name of the Retinal Pigment Epithelium layer (default: "RPE").
        fovea_landmark_idx: Index of fovea landmark to use: 0=start, 1=end, 2=middle
            (default: 2).
        strict_measurement: If True, only calculate if both ILM and RPE are available.
            If False, use next available layer as fallback (default: False).
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "cst_diameter_mm": fields.Float(allow_none=True),
        "ilm_layer_name": fields.String(allow_none=True),
        "rpe_layer_name": fields.String(allow_none=True),
        "fovea_landmark_idx": fields.Integer(allow_none=True),
        "strict_measurement": fields.Boolean(allow_none=True),
    }

    def __init__(
        self,
        datastructure: DataStructure,
        cst_diameter_mm: float = CST_DEFAULT_DIAMETER_MM,
        ilm_layer_name: str = CST_DEFAULT_ILM_LAYER_NAME,
        rpe_layer_name: str = CST_DEFAULT_RPE_LAYER_NAME,
        fovea_landmark_idx: int = FOVEA_CENTRE_LANDMARK_INDEX,
        strict_measurement: bool = False,
        **kwargs: Any,
    ) -> None:
        self.cst_diameter_mm = cst_diameter_mm
        self.ilm_layer_name = ilm_layer_name
        self.rpe_layer_name = rpe_layer_name
        self.fovea_landmark_idx = fovea_landmark_idx
        self.strict_measurement = strict_measurement
        super().__init__(datastructure=datastructure, **kwargs)

    def modeller(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> NoResultsModellerAlgorithm:
        """Modeller-side of the algorithm."""
        return NoResultsModellerAlgorithm(
            log_message="Running CST Calculation Algorithm",
            **kwargs,
        )

    def worker(
        self,
        *,
        context: ProtocolContext,
        **kwargs: Any,
    ) -> _WorkerSide:
        """Worker-side of the algorithm."""
        return _WorkerSide(
            cst_diameter_mm=self.cst_diameter_mm,
            ilm_layer_name=self.ilm_layer_name,
            rpe_layer_name=self.rpe_layer_name,
            fovea_landmark_idx=self.fovea_landmark_idx,
            strict_measurement=self.strict_measurement,
            **kwargs,
        )
