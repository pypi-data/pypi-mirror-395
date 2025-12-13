# nightskycam_scorer/model/evaluate.py
"""
Comprehensive evaluation script for trained models.
Provides detailed metrics, confusion matrix, and per-class analysis.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from .data import BinaryDataset
from .model import BinaryClassifier

logger = logging.getLogger(__name__)


@dataclass
class EvaluationMetrics:
    """Comprehensive metrics for binary classification."""

    # Confusion matrix components
    true_positives: int
    true_negatives: int
    false_positives: int
    false_negatives: int

    # Aggregate metrics
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    specificity: float
    balanced_accuracy: float

    # Per-class metrics
    positive_accuracy: float  # Recall for positive class
    negative_accuracy: float  # Recall for negative class (specificity)

    # Additional statistics
    total_samples: int
    positive_samples: int
    negative_samples: int

    # Probability statistics
    mean_positive_prob: float  # Mean predicted probability for positive samples
    mean_negative_prob: float  # Mean predicted probability for negative samples
    std_positive_prob: float  # Std dev of predicted probability for positive samples
    std_negative_prob: float  # Std dev of predicted probability for negative samples

    def __str__(self) -> str:
        """Format metrics as a readable string."""
        lines = [
            "=" * 70,
            "EVALUATION METRICS",
            "=" * 70,
            "",
            "CONFUSION MATRIX:",
            f"  True Positives:  {self.true_positives:5d}",
            f"  True Negatives:  {self.true_negatives:5d}",
            f"  False Positives: {self.false_positives:5d}",
            f"  False Negatives: {self.false_negatives:5d}",
            "",
            "OVERALL METRICS:",
            f"  Accuracy:          {self.accuracy:.4f}",
            f"  Balanced Accuracy: {self.balanced_accuracy:.4f}",
            f"  Precision:         {self.precision:.4f}",
            f"  Recall:            {self.recall:.4f}",
            f"  F1 Score:          {self.f1_score:.4f}",
            f"  Specificity:       {self.specificity:.4f}",
            "",
            "PER-CLASS METRICS:",
            f"  Positive Class (Label=1):",
            f"    Samples:         {self.positive_samples:5d}",
            f"    Accuracy:        {self.positive_accuracy:.4f} (recall)",
            f"    Mean Prob:       {self.mean_positive_prob:.4f} ± {self.std_positive_prob:.4f}",
            f"  Negative Class (Label=0):",
            f"    Samples:         {self.negative_samples:5d}",
            f"    Accuracy:        {self.negative_accuracy:.4f} (specificity)",
            f"    Mean Prob:       {self.mean_negative_prob:.4f} ± {self.std_negative_prob:.4f}",
            "",
            "DATASET STATISTICS:",
            f"  Total Samples:     {self.total_samples:5d}",
            f"  Positive Ratio:    {self.positive_samples / self.total_samples:.2%}",
            f"  Negative Ratio:    {self.negative_samples / self.total_samples:.2%}",
            "=" * 70,
        ]
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, float]:
        """Convert metrics to a dictionary for logging or saving."""
        return {
            "accuracy": self.accuracy,
            "balanced_accuracy": self.balanced_accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "specificity": self.specificity,
            "true_positives": float(self.true_positives),
            "true_negatives": float(self.true_negatives),
            "false_positives": float(self.false_positives),
            "false_negatives": float(self.false_negatives),
            "positive_accuracy": self.positive_accuracy,
            "negative_accuracy": self.negative_accuracy,
            "mean_positive_prob": self.mean_positive_prob,
            "mean_negative_prob": self.mean_negative_prob,
            "std_positive_prob": self.std_positive_prob,
            "std_negative_prob": self.std_negative_prob,
        }


def evaluate_model(
    model: BinaryClassifier,
    dataset: BinaryDataset,
    batch_size: int = 16,
    num_workers: int = 4,
    device: str = "cuda",
) -> EvaluationMetrics:
    """
    Comprehensive evaluation of a binary classifier.

    Args:
        model: Trained BinaryClassifier model
        dataset: Dataset to evaluate on
        batch_size: Batch size for evaluation
        num_workers: Number of data loading workers
        device: Device to run evaluation on

    Returns:
        EvaluationMetrics containing all computed metrics
    """
    device_obj = torch.device(
        device if torch.cuda.is_available() and device == "cuda" else "cpu"
    )
    model = model.to(device_obj)
    model.eval()

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    all_predictions: list[float] = []
    all_probabilities: list[float] = []
    all_labels: list[int] = []

    with torch.no_grad():
        for batch in loader:
            images = batch["image"].to(device_obj, non_blocking=True)
            labels = batch["label"].to(device_obj, non_blocking=True)

            logits = model(images)
            probs = torch.sigmoid(logits.squeeze(1))
            preds = (probs >= 0.5).float()

            all_predictions.extend(preds.cpu().numpy())
            all_probabilities.extend(probs.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # Convert to numpy arrays
    predictions = np.array(all_predictions)
    probabilities = np.array(all_probabilities)
    labels = np.array(all_labels)

    # Compute confusion matrix components
    tp = int(np.sum((predictions == 1) & (labels == 1)))
    tn = int(np.sum((predictions == 0) & (labels == 0)))
    fp = int(np.sum((predictions == 1) & (labels == 0)))
    fn = int(np.sum((predictions == 0) & (labels == 1)))

    # Compute aggregate metrics
    total = len(labels)
    accuracy = (tp + tn) / total if total > 0 else 0.0

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )
    balanced_acc = (recall + specificity) / 2.0

    # Per-class metrics
    positive_mask = labels == 1
    negative_mask = labels == 0

    num_positive = int(np.sum(positive_mask))
    num_negative = int(np.sum(negative_mask))

    positive_accuracy = recall  # Same as recall for positive class
    negative_accuracy = specificity  # Same as specificity for negative class

    # Probability statistics
    if num_positive > 0:
        positive_probs = probabilities[positive_mask]
        mean_pos_prob = float(np.mean(positive_probs))
        std_pos_prob = float(np.std(positive_probs))
    else:
        mean_pos_prob = 0.0
        std_pos_prob = 0.0

    if num_negative > 0:
        negative_probs = probabilities[negative_mask]
        mean_neg_prob = float(np.mean(negative_probs))
        std_neg_prob = float(np.std(negative_probs))
    else:
        mean_neg_prob = 0.0
        std_neg_prob = 0.0

    return EvaluationMetrics(
        true_positives=tp,
        true_negatives=tn,
        false_positives=fp,
        false_negatives=fn,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=f1,
        specificity=specificity,
        balanced_accuracy=balanced_acc,
        positive_accuracy=positive_accuracy,
        negative_accuracy=negative_accuracy,
        total_samples=total,
        positive_samples=num_positive,
        negative_samples=num_negative,
        mean_positive_prob=mean_pos_prob,
        mean_negative_prob=mean_neg_prob,
        std_positive_prob=std_pos_prob,
        std_negative_prob=std_neg_prob,
    )


def find_optimal_threshold(
    probabilities: np.ndarray,
    labels: np.ndarray,
    optimize_for: Literal["recall", "f1", "precision", "balanced"] = "recall",
    min_precision: float = 0.7,
    min_recall: float = 0.0,
) -> Tuple[float, Dict[str, float]]:
    """
    Find optimal classification threshold based on optimization criterion.

    Args:
        probabilities: Predicted probabilities for positive class (shape: N)
        labels: True labels (0 or 1) (shape: N)
        optimize_for: Metric to optimize ('recall', 'f1', 'precision', 'balanced')
        min_precision: Minimum acceptable precision (for recall optimization)
        min_recall: Minimum acceptable recall (for precision optimization)

    Returns:
        Tuple of (optimal_threshold, metrics_at_threshold)
            - optimal_threshold: Best threshold value
            - metrics_at_threshold: Dict with precision, recall, f1, etc. at that threshold
    """
    thresholds = np.linspace(0.05, 0.95, 100)
    best_threshold = 0.5
    best_score = 0.0
    best_metrics = {}

    for thresh in thresholds:
        preds = (probabilities >= thresh).astype(int)

        tp = np.sum((preds == 1) & (labels == 1))
        fp = np.sum((preds == 1) & (labels == 0))
        fn = np.sum((preds == 0) & (labels == 1))
        tn = np.sum((preds == 0) & (labels == 0))

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )
        balanced_acc = (recall + specificity) / 2.0

        # Select best threshold based on optimization criterion
        if optimize_for == "recall":
            # Maximize recall while maintaining minimum precision
            if precision >= min_precision and recall > best_score:
                best_score = recall
                best_threshold = thresh
                best_metrics = {
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "specificity": specificity,
                    "balanced_accuracy": balanced_acc,
                }
        elif optimize_for == "f1":
            if f1 > best_score:
                best_score = f1
                best_threshold = thresh
                best_metrics = {
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "specificity": specificity,
                    "balanced_accuracy": balanced_acc,
                }
        elif optimize_for == "precision":
            # Maximize precision while maintaining minimum recall
            if recall >= min_recall and precision > best_score:
                best_score = precision
                best_threshold = thresh
                best_metrics = {
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "specificity": specificity,
                    "balanced_accuracy": balanced_acc,
                }
        elif optimize_for == "balanced":
            if balanced_acc > best_score:
                best_score = balanced_acc
                best_threshold = thresh
                best_metrics = {
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "specificity": specificity,
                    "balanced_accuracy": balanced_acc,
                }

    best_metrics["optimal_threshold"] = best_threshold
    return best_threshold, best_metrics
