# nightskycam_scorer/model/train.py
from __future__ import annotations

import logging
import os
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ..constants import ImageSize
from .data import BinaryDataset, compute_class_counts
from .model import BinaryClassifier

logger = logging.getLogger(__name__)


@dataclass
class TrainConfig:
    image_size: ImageSize  # (height, width) tuple
    grayscale: bool = False
    batch_size: int = 16
    epochs: int = 30
    lr: float = 3e-4
    weight_decay: float = 1e-4
    seed: int = 42
    num_workers: int = 4
    patience: int = 5
    device: str = "cuda"  # "cuda" or "cpu"
    backbone: str = "auto"  # Changed default from "resnet50" to "auto"
    pretrained: bool = True
    dropout: float = 0.4  # NEW: dropout for regularization
    out_dir: str = "./runs"
    dataset_name: str = "binary_classifier"
    # NEW: Custom normalization statistics
    normalize_mean: Optional[Tuple[float, float, float]] = None
    normalize_std: Optional[Tuple[float, float, float]] = None
    # NEW: Simpler class balancing
    pos_weight_multiplier: float = (
        1.2  # Mild boost for positive class (was automatic N_neg/N_pos)
    )


def _compute_loss_and_metrics(
    logits: torch.Tensor,
    labels: torch.Tensor,
    criterion: nn.BCEWithLogitsLoss,
) -> Tuple[torch.Tensor, Dict[str, float]]:
    """
    Compute loss and metrics for binary classification.

    Args:
        logits: Model outputs of shape (B, 1)
        labels: Ground truth labels of shape (B,) with values 0 or 1
        criterion: BCE loss function

    Returns:
        Tuple of (loss, metrics_dict)
    """
    # Compute loss
    loss = criterion(logits.squeeze(1), labels)

    with torch.no_grad():
        # Compute predictions
        probs = torch.sigmoid(logits.squeeze(1))
        preds = (probs >= 0.5).float()

        # Compute metrics
        correct = (preds == labels).float().sum().item()
        total = labels.size(0)
        accuracy = correct / total if total > 0 else 0.0

        # Precision, recall, F1
        tp = ((preds == 1.0) & (labels == 1.0)).float().sum().item()
        fp = ((preds == 1.0) & (labels == 0.0)).float().sum().item()
        fn = ((preds == 0.0) & (labels == 1.0)).float().sum().item()
        tn = ((preds == 0.0) & (labels == 0.0)).float().sum().item()

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    return loss, metrics


def train_model(
    train_ds: BinaryDataset,
    val_ds: BinaryDataset,
    cfg: TrainConfig,
) -> str:
    """
    Train the binary classifier.

    Args:
        train_ds: Training dataset
        val_ds: Validation dataset
        cfg: Training configuration

    Returns:
        Path to the best model checkpoint
    """
    device = torch.device(
        cfg.device if torch.cuda.is_available() and cfg.device == "cuda" else "cpu"
    )
    model = BinaryClassifier(
        backbone=cfg.backbone,
        pretrained=cfg.pretrained,
        image_size=cfg.image_size,
        dropout=cfg.dropout,
    ).to(device)

    # Compute class counts
    num_negative, num_positive = compute_class_counts(train_ds._samples)
    logger.info(f"Class counts: negative={num_negative}, positive={num_positive}")

    # Simplified class balancing: use mild multiplier instead of automatic N_neg/N_pos
    # For balanced datasets (55/45), this provides gentle boost without overweighting
    pos_weight = torch.tensor([cfg.pos_weight_multiplier], device=device)
    logger.info(f"Using pos_weight={pos_weight.item():.3f} (multiplier, not ratio)")

    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    optimizer = torch.optim.AdamW(
        model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=cfg.epochs)

    train_loader = DataLoader(
        train_ds,
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
        pin_memory=True,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=cfg.batch_size,
        shuffle=False,
        num_workers=cfg.num_workers,
        pin_memory=True,
    )

    best_val_loss = float("inf")
    epochs_no_improve = 0
    out_root = os.path.join(cfg.out_dir, cfg.dataset_name)
    os.makedirs(out_root, exist_ok=True)
    ckpt_path = os.path.join(out_root, "best_model.pt")

    scaler = torch.cuda.amp.GradScaler(enabled=(device.type == "cuda"))

    for epoch in range(1, cfg.epochs + 1):
        model.train()
        total_loss = 0.0
        n_batches = 0
        for batch in train_loader:
            images = batch["image"].to(device, non_blocking=True)
            labels = batch["label"].to(device, non_blocking=True)

            optimizer.zero_grad(set_to_none=True)
            with torch.cuda.amp.autocast(enabled=(device.type == "cuda")):
                logits = model(images)
                loss, _ = _compute_loss_and_metrics(logits, labels, criterion)

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            total_loss += float(loss.item())
            n_batches += 1

        scheduler.step()
        avg_train_loss = total_loss / max(1, n_batches)

        # Validation
        model.eval()
        val_loss = 0.0
        v_batches = 0
        all_metrics: Dict[str, list[float]] = {
            "accuracy": [],
            "precision": [],
            "recall": [],
            "f1": [],
        }

        with torch.no_grad():
            for batch in val_loader:
                images = batch["image"].to(device, non_blocking=True)
                labels = batch["label"].to(device, non_blocking=True)
                logits = model(images)
                loss, metrics = _compute_loss_and_metrics(logits, labels, criterion)
                val_loss += float(loss.item())
                v_batches += 1

                for key in all_metrics:
                    all_metrics[key].append(metrics[key])

        avg_val_loss = val_loss / max(1, v_batches)
        avg_metrics = {
            key: sum(values) / max(1, len(values))
            for key, values in all_metrics.items()
        }

        logger.info(
            f"Epoch {epoch:03d} | train_loss={avg_train_loss:.4f} val_loss={avg_val_loss:.4f} "
            f"acc={avg_metrics['accuracy']:.3f} prec={avg_metrics['precision']:.3f} "
            f"rec={avg_metrics['recall']:.3f} f1={avg_metrics['f1']:.3f}"
        )

        if avg_val_loss < best_val_loss:
            best_val_loss = avg_val_loss
            epochs_no_improve = 0
            # Save checkpoint
            payload = {
                "model_state": model.state_dict(),
                "backbone": cfg.backbone,
                "image_size": cfg.image_size,
                "grayscale": cfg.grayscale,
                "dropout": cfg.dropout,
                "normalize_mean": cfg.normalize_mean,
                "normalize_std": cfg.normalize_std,
                "config": asdict(cfg),
            }
            torch.save(payload, ckpt_path)
            logger.info(f"Saved checkpoint to {ckpt_path}")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= cfg.patience:
                logger.info("Early stopping.")
                break

    return ckpt_path
