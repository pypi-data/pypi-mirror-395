from __future__ import annotations

import os
import random
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
from torch.utils.data import Dataset

from ..constants import IMAGE_SUFFIXES, ImageSize
from ..utils import load_image_any, validate_image_shape
from .transforms import Preprocess


class BinaryDataset(Dataset):
    """Dataset for binary classification (positive vs negative night-sky patches)."""

    def __init__(
        self,
        samples: List[Tuple[str, int]],
        image_size: ImageSize,
        grayscale: bool = False,
        train: bool = True,
        validate_size: bool = True,
        normalize_mean: Optional[Tuple[float, float, float]] = None,
        normalize_std: Optional[Tuple[float, float, float]] = None,
    ) -> None:
        """
        Initialize the dataset.

        Args:
            samples: List of (image_path, label) tuples where label is 0 (negative) or 1 (positive)
            image_size: Target image size as (height, width) tuple
            grayscale: Whether to convert to grayscale
            train: Whether to apply training augmentations
            validate_size: Whether to validate image sizes match expected dimensions
            normalize_mean: Custom normalization mean (R, G, B). If None, uses ImageNet stats.
            normalize_std: Custom normalization std (R, G, B). If None, uses ImageNet stats.
        """
        self._samples = samples
        self._image_size = image_size
        self._validate_size = validate_size
        self._pp = Preprocess(
            image_size=image_size,
            grayscale=grayscale,
            train=train,
            normalize_mean=normalize_mean,
            normalize_std=normalize_std,
        )

    def __len__(self) -> int:
        return len(self._samples)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        img_path, label = self._samples[idx]
        img = load_image_any(img_path, force_rgb=True)

        # Validate image size if requested
        if self._validate_size:
            validate_image_shape(img, self._image_size, img_path)

        img_t = self._pp(img)
        return {
            "image": img_t,
            "label": torch.tensor(label, dtype=torch.float32),
        }


def discover_binary_samples(root: str) -> List[Tuple[str, int]]:
    """
    Discover image samples from positive/ and negative/ subdirectories.

    Args:
        root: Root directory containing positive/ and negative/ subdirectories

    Returns:
        List of (image_path, label) tuples where label is 0 (negative) or 1 (positive)
    """
    samples: List[Tuple[str, int]] = []

    # Discover positive samples
    positive_dir = os.path.join(root, "positive")
    if os.path.isdir(positive_dir):
        for dirpath, _, filenames in os.walk(positive_dir):
            for name in filenames:
                _, ext = os.path.splitext(name)
                if ext.lower() in IMAGE_SUFFIXES:
                    img_path = os.path.join(dirpath, name)
                    samples.append((img_path, 1))

    # Discover negative samples
    negative_dir = os.path.join(root, "negative")
    if os.path.isdir(negative_dir):
        for dirpath, _, filenames in os.walk(negative_dir):
            for name in filenames:
                _, ext = os.path.splitext(name)
                if ext.lower() in IMAGE_SUFFIXES:
                    img_path = os.path.join(dirpath, name)
                    samples.append((img_path, 0))

    samples.sort(key=lambda s: s[0])
    return samples


def split_samples(
    samples: List[Tuple[str, int]], val_ratio: float = 0.2, seed: int = 42
) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
    """
    Split samples into train and validation sets.

    Args:
        samples: List of (image_path, label) tuples
        val_ratio: Fraction of samples to use for validation
        seed: Random seed for reproducibility

    Returns:
        Tuple of (train_samples, val_samples)
    """
    rng = random.Random(seed)
    shuffled = samples[:]
    rng.shuffle(shuffled)
    n = len(shuffled)
    n_val = max(1, int(n * val_ratio)) if n > 1 else 0
    val = shuffled[:n_val]
    train = shuffled[n_val:]
    return train, val


def compute_class_counts(samples: List[Tuple[str, int]]) -> Tuple[int, int]:
    """
    Compute class counts for positive and negative samples.

    Args:
        samples: List of (image_path, label) tuples

    Returns:
        Tuple of (num_negative, num_positive)
    """
    num_negative = sum(1 for _, label in samples if label == 0)
    num_positive = sum(1 for _, label in samples if label == 1)
    return num_negative, num_positive


def validate_all_images_upfront(
    samples: List[Tuple[str, int]], expected_size: ImageSize, max_check: int = 100
) -> None:
    """
    Validate that ALL images in the dataset are the expected size.

    This performs upfront validation before training starts to catch size mismatches early.
    Checks a sample of images (up to max_check) to verify consistency.

    Args:
        samples: List of (image_path, label) tuples
        expected_size: Expected image size as (height, width) tuple
        max_check: Maximum number of images to check (default: 100)

    Raises:
        ValueError: If any image has incorrect size or if images have inconsistent sizes
    """
    from ..utils import get_image_size

    if not samples:
        raise ValueError("Cannot validate empty dataset")

    num_to_check = min(len(samples), max_check)

    for i in range(num_to_check):
        img_path, _ = samples[i]
        try:
            actual_size = get_image_size(img_path)
        except Exception as e:
            raise ValueError(f"Failed to read image {img_path}: {e}")

        if actual_size != expected_size:
            raise ValueError(
                f"Image size mismatch detected during upfront validation!\n"
                f"  Image: {img_path}\n"
                f"  Expected size: {expected_size}\n"
                f"  Actual size: {actual_size}\n"
                f"  ALL images in the dataset must be exactly {expected_size}.\n"
                f"  Supported sizes are: (600, 600) for patches or (136, 200) for thumbnails.\n"
                f"  NO mixed sizes allowed!"
            )
