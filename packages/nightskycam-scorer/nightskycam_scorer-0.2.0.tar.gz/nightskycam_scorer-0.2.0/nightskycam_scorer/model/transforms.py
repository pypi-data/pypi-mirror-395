# skyscorer/transforms.py
from __future__ import annotations

import random
from typing import Callable, Optional, Tuple, Union

import numpy as np
import torch
from torchvision import transforms as T

from ..constants import ImageSize
from ..utils import rgb_to_grayscale


class RandomRotate90:
    def __init__(self, p: float = 0.5) -> None:
        self._p = p

    def __call__(self, img: np.ndarray) -> np.ndarray:
        if random.random() < self._p:
            # Check if image is square
            h, w = img.shape[:2]
            if h == w:
                # Square image: can rotate 90, 180, or 270 degrees
                k = random.choice([1, 2, 3])
            else:
                # Non-square image: only rotate 180 degrees (k=2) to preserve dimensions
                k = 2
            return np.ascontiguousarray(np.rot90(img, k, axes=(0, 1)))
        return img


class RandomGamma:
    def __init__(
        self, gamma_range: Tuple[float, float] = (0.95, 1.05), p: float = 0.5
    ) -> None:
        self._gmin, self._gmax = gamma_range
        self._p = p

    def __call__(self, img: np.ndarray) -> np.ndarray:
        if random.random() >= self._p:
            return img
        gamma = random.uniform(self._gmin, self._gmax)
        eps = 1e-6
        return np.power(np.clip(img, 0.0, 1.0) + eps, gamma).astype(np.float32)


class GaussianNoise:
    def __init__(self, sigma: float = 0.01, p: float = 0.5) -> None:
        self._sigma = sigma
        self._p = p

    def __call__(self, img: np.ndarray) -> np.ndarray:
        if random.random() >= self._p:
            return img
        noise = np.random.normal(0.0, self._sigma, size=img.shape).astype(np.float32)
        out = img + noise
        return np.clip(out, 0.0, 1.0)


class NumpyToTensor:
    def __call__(self, img: np.ndarray) -> torch.Tensor:
        # HWC [0,1] -> CHW float32
        return torch.from_numpy(np.transpose(img, (2, 0, 1))).float()


class NormalizeImageNet:
    def __init__(self, grayscale: bool = False) -> None:
        if grayscale:
            # Use RGB means replicated; grayscale used as repeated channel
            mean = [0.485, 0.456, 0.406]
            std = [0.229, 0.224, 0.225]
            self._mean = torch.tensor(mean).view(3, 1, 1)
            self._std = torch.tensor(std).view(3, 1, 1)
        else:
            self._mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
            self._std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)

    def __call__(self, t: torch.Tensor) -> torch.Tensor:
        return (t - self._mean) / self._std


class NormalizeCustom:
    """Custom normalization with user-provided or dataset-specific statistics."""

    def __init__(
        self, mean: Tuple[float, float, float], std: Tuple[float, float, float]
    ) -> None:
        """
        Initialize with custom mean and std.

        Args:
            mean: RGB mean values as (R, G, B) tuple
            std: RGB std values as (R, G, B) tuple
        """
        self._mean = torch.tensor(mean).view(3, 1, 1)
        self._std = torch.tensor(std).view(3, 1, 1)

    def __call__(self, t: torch.Tensor) -> torch.Tensor:
        return (t - self._mean) / self._std


class Preprocess:
    def __init__(
        self,
        image_size: ImageSize,
        grayscale: bool = False,
        train: bool = True,
        normalize_mean: Optional[Tuple[float, float, float]] = None,
        normalize_std: Optional[Tuple[float, float, float]] = None,
    ) -> None:
        """
        Initialize preprocessing pipeline.

        Args:
            image_size: Target image size as (height, width)
            grayscale: Whether to convert to grayscale
            train: Whether to apply training augmentations
            normalize_mean: Custom normalization mean (R, G, B). If None, uses ImageNet stats.
            normalize_std: Custom normalization std (R, G, B). If None, uses ImageNet stats.
        """
        self._image_size: ImageSize = image_size
        self._grayscale = grayscale
        self._train = train

        # NO RESIZE - images must already be the correct size!
        # Size validation happens in the dataset, not here
        self._hflip = T.RandomHorizontalFlip(p=0.5)
        self._vflip = T.RandomVerticalFlip(p=0.5)

        # Stronger augmentation for small datasets (only during training)
        if train:
            self._color = T.ColorJitter(
                brightness=0.4,  # Increased from 0.1
                contrast=0.4,  # Increased from 0.1
                saturation=0.3,  # NEW: add saturation variation
                hue=0.05,  # NEW: slight hue shift
            )
        else:
            self._color = T.ColorJitter(brightness=0.1, contrast=0.1)

        self._to_pil = T.ToPILImage()
        self._to_tensor = (
            T.ToTensor()
        )  # Converts to [0,1] float CHW but we already have [0,1]

        # Use custom normalization if provided, otherwise ImageNet
        if normalize_mean is not None and normalize_std is not None:
            self._norm: Union[NormalizeCustom, NormalizeImageNet] = NormalizeCustom(
                normalize_mean, normalize_std
            )
        else:
            self._norm = NormalizeImageNet(grayscale=grayscale)

        # Numpy-based augmentations (stronger for training)
        self._rot90 = RandomRotate90(p=0.5)
        if train:
            self._gamma = RandomGamma(
                (0.7, 1.3), p=0.8
            )  # Increased from (0.95, 1.05), p=0.5
            self._noise = GaussianNoise(
                sigma=0.05, p=0.8
            )  # Increased from sigma=0.01, p=0.5
        else:
            self._gamma = RandomGamma((0.95, 1.05), p=0.5)
            self._noise = GaussianNoise(sigma=0.01, p=0.5)

        self._numpy_to_tensor = NumpyToTensor()

        # Random erasing for training (simulates occlusions)
        if train:
            self._random_erasing = T.RandomErasing(p=0.3, scale=(0.02, 0.1))
        else:
            self._random_erasing = None

    def __call__(self, img_np: np.ndarray) -> torch.Tensor:
        # Optional grayscale conversion: compute luma and replicate to 3 channels
        if self._grayscale:
            y = rgb_to_grayscale(img_np)
            img_np = np.stack([y, y, y], axis=-1)
        # Geometric + photometric augmentations on numpy to avoid repeated quantization
        if self._train:
            img_np = self._rot90(img_np)
        # Convert to PIL for color jitter and flips (NO RESIZE!)
        img_pil = self._to_pil((img_np * 255.0).astype(np.uint8))
        # Apply augmentations (flips, color jitter) but NO resize
        if self._train:
            img_pil = self._hflip(img_pil)
            img_pil = self._vflip(img_pil)
            img_pil = self._color(img_pil)
        # Back to numpy [0,1]
        img_np2 = np.array(img_pil).astype(np.float32) / 255.0
        # Remaining numpy-space photometrics
        if self._train:
            img_np2 = self._gamma(img_np2)
            img_np2 = self._noise(img_np2)
        # To tensor CHW
        t = self._numpy_to_tensor(img_np2)
        # Normalize
        t = self._norm(t)
        # Apply random erasing if training
        if self._train and self._random_erasing is not None:
            t = self._random_erasing(t)
        return t
