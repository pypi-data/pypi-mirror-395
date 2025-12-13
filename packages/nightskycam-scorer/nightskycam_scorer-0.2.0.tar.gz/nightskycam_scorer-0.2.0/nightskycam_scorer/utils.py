# skyscorer/utils.py
from __future__ import annotations

import math
import os
import random
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
from PIL import Image

from .constants import PATCH_SIZE, RESIZED_FULL_SIZE, ImageSize


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except Exception:
        pass


def timestamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def to_float_image(arr, out_dtype=np.float32):
    x = np.asarray(arr)

    # Booleans: 0/1 -> 0.0/1.0
    if x.dtype == np.bool_:
        return x.astype(out_dtype, copy=False)

    # Unsigned integers: scale by nominal dtype max
    if np.issubdtype(x.dtype, np.unsignedinteger):
        scale = np.float64(np.iinfo(x.dtype).max)
        y = x.astype(np.float64, copy=False) / scale
        return y.astype(out_dtype, copy=False)

    # Floating point
    if np.issubdtype(x.dtype, np.floating):
        return x

    raise TypeError(
        f"Unsupported dtype {x.dtype}; expected unsigned int, float, or bool."
    )


def load_image_any(path: str, force_rgb: bool = True) -> np.ndarray:
    """
    Load image as numpy array HxWxC in [0,1] float32.
    Supports 8/16-bit, various formats.
    """
    with Image.open(path) as img:
        # Convert to RGB if requested
        if force_rgb:
            img = img.convert("RGB")
        else:
            # Keep original if not forcing RGB (not used here)
            pass
        arr = np.array(img)
    arr = to_float_image(arr)
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    elif arr.ndim == 3 and arr.shape[2] == 4:  # RGBA
        arr = arr[..., :3]
    return arr.astype(np.float32)


def rgb_to_grayscale(rgb: np.ndarray) -> np.ndarray:
    """
    Convert RGB image in [0,1] to grayscale luminance Y, shape HxW.
    """
    # Rec. 601 luma coefficients
    y = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    return y.astype(np.float32)


def get_image_size(path: str) -> ImageSize:
    """
    Get the size of an image as (height, width) tuple.

    Args:
        path: Path to image file

    Returns:
        Tuple of (height, width)
    """
    with Image.open(path) as img:
        width, height = img.size
        return (height, width)


def detect_dataset_image_size(
    samples: List[Tuple[str, int]], max_check: int = 10
) -> ImageSize:
    """
    Detect the image size from a dataset by checking the first few samples.
    Assumes all images in the dataset have the same size.

    Args:
        samples: List of (image_path, label) tuples
        max_check: Maximum number of images to check for consistency

    Returns:
        Detected image size as (height, width) tuple

    Raises:
        ValueError: If images have inconsistent sizes or dataset is empty
    """
    if not samples:
        raise ValueError("Cannot detect image size from empty dataset")

    # Check first image
    first_path, _ = samples[0]
    detected_size = get_image_size(first_path)

    # Verify consistency across first max_check images
    num_to_check = min(len(samples), max_check)
    for i in range(1, num_to_check):
        path, _ = samples[i]
        size = get_image_size(path)
        if size != detected_size:
            raise ValueError(
                f"Inconsistent image sizes detected: {first_path} has size {detected_size}, "
                f"but {path} has size {size}. All images must have the same dimensions."
            )

    return detected_size


def validate_image_size(detected_size: ImageSize) -> ImageSize:
    """
    Validate that the detected image size is one of the supported sizes.

    Args:
        detected_size: Detected image size as (height, width)

    Returns:
        The validated image size

    Raises:
        ValueError: If the size is not supported
    """
    supported_sizes = [PATCH_SIZE, RESIZED_FULL_SIZE]

    if detected_size not in supported_sizes:
        raise ValueError(
            f"Unsupported image size: {detected_size}. "
            f"Supported sizes are: {PATCH_SIZE} (patch) and {RESIZED_FULL_SIZE} (resized). "
            f"Please resize your images to one of these dimensions or use --image-height and --image-width "
            f"to specify a custom size."
        )

    return detected_size


def validate_image_shape(
    image: np.ndarray, expected_size: ImageSize, image_path: Optional[str] = None
) -> None:
    """
    Validate that an image has the expected shape.

    Args:
        image: Image array with shape (H, W, C)
        expected_size: Expected (height, width) tuple
        image_path: Optional path to image for error messages

    Raises:
        ValueError: If image shape doesn't match expected size
    """
    if image.ndim != 3:
        path_str = f" ({image_path})" if image_path else ""
        raise ValueError(
            f"Invalid image shape{path_str}: expected 3D array (H, W, C), got shape {image.shape}"
        )

    actual_size: ImageSize = (image.shape[0], image.shape[1])

    if actual_size != expected_size:
        path_str = f" ({image_path})" if image_path else ""
        raise ValueError(
            f"Invalid image size{path_str}: expected {expected_size}, got {actual_size}. "
            f"All images must match the size used during training."
        )


def compute_normalization_stats(
    dataset_root: str, num_samples: int = 500, grayscale: bool = False
) -> Tuple[List[float], List[float]]:
    """
    Compute mean and std for normalization from a dataset.

    Args:
        dataset_root: Path to dataset root (with positive/negative dirs)
        num_samples: Number of samples to use for statistics
        grayscale: Whether to compute stats for grayscale conversion

    Returns:
        Tuple of (mean, std) as lists of [R, G, B] values (or [Y, Y, Y] for grayscale)
    """
    from .model.data import discover_binary_samples

    samples = discover_binary_samples(dataset_root)
    samples = samples[:num_samples]  # Sample subset

    if not samples:
        raise ValueError(f"No samples found in {dataset_root}")

    pixel_sum = np.zeros(3, dtype=np.float64)
    pixel_sq_sum = np.zeros(3, dtype=np.float64)
    pixel_count = 0

    for img_path, _ in samples:
        img = load_image_any(img_path, force_rgb=True)  # Returns [0,1] float HxWx3

        # Convert to grayscale if needed
        if grayscale:
            y = rgb_to_grayscale(img)
            img = np.stack([y, y, y], axis=-1)

        pixel_sum += img.sum(axis=(0, 1))
        pixel_sq_sum += (img**2).sum(axis=(0, 1))
        pixel_count += img.shape[0] * img.shape[1]

    mean = pixel_sum / pixel_count
    std = np.sqrt(pixel_sq_sum / pixel_count - mean**2)

    return mean.tolist(), std.tolist()
