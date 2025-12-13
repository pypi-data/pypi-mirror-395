# nightskycam_scorer/model/infer.py
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

import numpy as np
import torch

from ..constants import ImageSize
from ..utils import to_float_image, validate_image_shape
from .model import BinaryClassifier
from .transforms import Preprocess


@dataclass
class PredictionResult:
    """Result of a binary classification prediction."""

    probability: float  # Probability of positive class [0, 1]
    prediction: str  # "positive" or "negative"
    confidence: float  # Confidence in the prediction [0, 1]


class SkyScorer:
    """Binary classifier for night-sky image quality."""

    def __init__(
        self,
        checkpoint_path: str,
        validate_size: bool = True,
        threshold: Optional[float] = None,
    ) -> None:
        """
        Initialize the scorer from a checkpoint.

        Args:
            checkpoint_path: Path to the trained model checkpoint
            validate_size: Whether to validate input image sizes during inference
            threshold: Custom classification threshold (default: 0.5)
        """
        payload = torch.load(checkpoint_path, map_location="cpu")
        backbone = payload.get("backbone", "resnet50")
        image_size_raw = payload.get("image_size", (600, 600))
        # Support both old (int) and new (tuple) checkpoint formats
        image_size: ImageSize
        if isinstance(image_size_raw, (list, tuple)):
            image_size = tuple(image_size_raw)  # type: ignore
        else:
            # Convert single int to tuple for backward compatibility
            image_size = (int(image_size_raw), int(image_size_raw))
        grayscale = bool(payload.get("grayscale", False))
        dropout = float(
            payload.get("dropout", 0.0)
        )  # For inference, dropout is disabled anyway
        normalize_mean = payload.get("normalize_mean", None)
        normalize_std = payload.get("normalize_std", None)

        # Convert lists to tuples if needed
        if normalize_mean is not None and isinstance(normalize_mean, list):
            normalize_mean = tuple(normalize_mean)
        if normalize_std is not None and isinstance(normalize_std, list):
            normalize_std = tuple(normalize_std)

        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._model = BinaryClassifier(
            backbone=backbone,
            pretrained=False,
            image_size=image_size,
            dropout=dropout,  # Will be disabled in eval mode
        )
        self._model.load_state_dict(payload["model_state"], strict=True)
        self._model.to(self._device)
        self._model.eval()

        self._image_size = image_size
        self._validate_size = validate_size
        self._threshold = threshold if threshold is not None else 0.5
        self._pp = Preprocess(
            image_size=image_size,
            grayscale=grayscale,
            train=False,
            normalize_mean=normalize_mean,
            normalize_std=normalize_std,
        )

    @torch.no_grad()
    def predict(
        self, rgb_images: np.ndarray
    ) -> Union[PredictionResult, List[PredictionResult]]:
        """
        Predict whether image(s) are clear night sky (positive) or not (negative).

        Args:
            rgb_images: Input image(s) as numpy array:
                - Single image: (H, W, 3) RGB, uint8/uint16/float
                - Batch of images: (N, H, W, 3) RGB, uint8/uint16/float

        Returns:
            For single image: PredictionResult dataclass
            For batch: List of PredictionResult dataclasses
        """
        # Detect if input is a batch or single image
        is_batch = rgb_images.ndim == 4

        if not is_batch:
            # Single image case - use original logic
            if rgb_images.ndim == 2:
                rgb_images = np.stack([rgb_images, rgb_images, rgb_images], axis=-1)
            assert (
                rgb_images.ndim == 3 and rgb_images.shape[2] == 3
            ), "Input must be HxWx3 RGB array or NxHxWx3 batch"

            # Normalize to [0,1] float
            imgf = to_float_image(rgb_images)

            # Validate image size
            if self._validate_size:
                validate_image_shape(imgf, self._image_size)

            t = self._pp(imgf)
            t = t.unsqueeze(0).to(self._device)  # 1xCxHxW

            logits = self._model(t)
            prob = torch.sigmoid(logits[0, 0]).cpu().item()

            prediction = "positive" if prob >= self._threshold else "negative"
            confidence = prob if prob >= self._threshold else (1.0 - prob)

            return PredictionResult(
                probability=float(prob),
                prediction=prediction,
                confidence=float(confidence),
            )
        else:
            # Batch case
            assert rgb_images.shape[3] == 3, "Batch input must be NxHxWx3 RGB array"

            # Process all images in the batch
            batch_tensors = []
            for i in range(rgb_images.shape[0]):
                imgf = to_float_image(rgb_images[i])

                # Validate image size
                if self._validate_size:
                    validate_image_shape(imgf, self._image_size)

                t = self._pp(imgf)
                batch_tensors.append(t)

            # Stack into batch tensor
            batch_t = torch.stack(batch_tensors).to(self._device)  # NxCxHxW

            # Run inference on entire batch
            logits = self._model(batch_t)  # Nx1
            probs = torch.sigmoid(logits.squeeze(1)).cpu().numpy()  # N

            # Build results list
            results = []
            for prob in probs:
                prob = float(prob)
                prediction = "positive" if prob >= self._threshold else "negative"
                confidence = prob if prob >= self._threshold else (1.0 - prob)
                results.append(
                    PredictionResult(
                        probability=prob,
                        prediction=prediction,
                        confidence=confidence,
                    )
                )

            return results
