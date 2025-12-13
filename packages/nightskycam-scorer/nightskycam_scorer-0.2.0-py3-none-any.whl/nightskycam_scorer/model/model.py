# nightskycam_scorer/model/model.py
from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn
from torchvision import models

from ..constants import ImageSize


class BinaryClassifier(nn.Module):
    """Binary classifier for night-sky image quality (positive vs negative)."""

    def __init__(
        self,
        backbone: str = "auto",
        pretrained: bool = True,
        image_size: Optional[ImageSize] = None,
        dropout: float = 0.4,
    ) -> None:
        """
        Initialize binary classifier.

        Args:
            backbone: Model backbone ('auto', 'mobilenet_v3_small', 'resnet18', 'resnet50', 'efficientnet_b0')
            pretrained: Whether to use ImageNet pretrained weights
            image_size: Image size as (height, width) tuple. Required if backbone='auto'
            dropout: Dropout probability for regularization (0.0 to disable)
        """
        super().__init__()

        # Auto-select backbone based on image size
        if backbone == "auto":
            if image_size is None:
                raise ValueError("image_size required when backbone='auto'")

            num_pixels = image_size[0] * image_size[1]

            if num_pixels < 50000:  # Small images (e.g., 136×200 = 27,200)
                backbone = "mobilenet_v3_small"
            elif num_pixels < 200000:  # Medium images
                backbone = "efficientnet_b0"
            else:  # Large images (e.g., 600×600 = 360,000)
                backbone = "resnet18"

        self._feat_dim: int

        # Initialize backbone
        if backbone == "mobilenet_v3_small":
            try:
                weights = (
                    models.MobileNet_V3_Small_Weights.IMAGENET1K_V1
                    if pretrained
                    else None
                )
                base = models.mobilenet_v3_small(weights=weights)
            except Exception:
                base = models.mobilenet_v3_small(weights=None)
            self._feat_dim = base.classifier[0].in_features  # 576
            # Remove classifier, keep features + pool
            self._backbone = nn.Sequential(
                *list(base.children())[:-1]
            )  # Features + pool

        elif backbone == "resnet18":
            try:
                weights = models.ResNet18_Weights.IMAGENET1K_V1 if pretrained else None
                base = models.resnet18(weights=weights)
            except Exception:
                base = models.resnet18(weights=None)
            self._feat_dim = base.fc.in_features  # 512
            # Remove original FC head
            self._backbone = nn.Sequential(
                *list(base.children())[:-1]
            )  # output Bx512x1x1

        elif backbone == "resnet50":
            try:
                weights = models.ResNet50_Weights.IMAGENET1K_V2 if pretrained else None
                base = models.resnet50(weights=weights)
            except Exception:
                base = models.resnet50(weights=None)
            self._feat_dim = base.fc.in_features  # 2048
            # Remove original FC head
            self._backbone = nn.Sequential(
                *list(base.children())[:-1]
            )  # output Bx2048x1x1

        elif backbone == "efficientnet_b0":
            try:
                weights = (
                    models.EfficientNet_B0_Weights.IMAGENET1K_V1 if pretrained else None
                )
                base = models.efficientnet_b0(weights=weights)
            except Exception:
                base = models.efficientnet_b0(weights=None)
            self._feat_dim = base.classifier[1].in_features  # 1280
            # Remove classifier, keep features
            self._backbone = nn.Sequential(
                *list(base.children())[:-1]
            )  # Features + pool

        else:
            raise ValueError(
                f"Unsupported backbone: {backbone}. "
                f"Supported: 'auto', 'mobilenet_v3_small', 'resnet18', 'resnet50', 'efficientnet_b0'"
            )

        # Dropout for regularization (critical for small datasets)
        self._dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

        # Single binary classification head
        self._classifier = nn.Linear(self._feat_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.

        Args:
            x: Input tensor of shape (B, C, H, W)

        Returns:
            Logits of shape (B, 1)
        """
        feats = self._backbone(x)  # BxC x1x1 or BxC (depending on backbone)
        feats = torch.flatten(feats, 1)  # BxC
        feats = self._dropout(feats)  # Apply dropout
        return self._classifier(feats)  # Bx1
