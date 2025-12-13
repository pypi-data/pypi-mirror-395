# nightskycam_scorer/model/evaluate_cli.py
"""
CLI for evaluating trained models on validation or test datasets.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys

import torch

from ..utils import set_seed
from .data import (BinaryDataset, discover_binary_samples, split_samples,
                   validate_all_images_upfront)
from .evaluate import evaluate_model
from .model import BinaryClassifier

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate a trained NightSkyCam binary classifier"
    )
    parser.add_argument(
        "model_path",
        type=str,
        help="Path to the trained model checkpoint (.pt file)",
    )
    parser.add_argument(
        "dataset_path",
        type=str,
        help="Path to dataset root (containing positive/ and negative/ folders)",
    )
    parser.add_argument(
        "--split",
        type=str,
        choices=["all", "train", "val"],
        default="all",
        help="Which split to evaluate: 'all' (entire dataset), 'train', or 'val' (default: all)",
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.2,
        help="Validation split ratio (only used if --split is 'train' or 'val')",
    )
    parser.add_argument(
        "--batch-size", type=int, default=16, help="Batch size for evaluation"
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=4,
        help="Number of data loading workers",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Force CPU evaluation (default: use CUDA if available)",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional path to save metrics as JSON",
    )

    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.model_path):
        logger.error(f"Model checkpoint not found: {args.model_path}")
        sys.exit(1)

    if not os.path.isdir(args.dataset_path):
        logger.error(f"Dataset directory not found: {args.dataset_path}")
        sys.exit(1)

    # Set seed
    set_seed(args.seed)

    # Load checkpoint
    logger.info(f"Loading model from {args.model_path}")
    checkpoint = torch.load(args.model_path, map_location="cpu")

    # Extract model configuration
    backbone = checkpoint.get("backbone", "resnet50")
    image_size = checkpoint["image_size"]
    grayscale = checkpoint.get("grayscale", False)
    dropout = checkpoint.get("dropout", 0.0)
    normalize_mean = checkpoint.get("normalize_mean", None)
    normalize_std = checkpoint.get("normalize_std", None)

    # Handle legacy checkpoints with int image_size
    if isinstance(image_size, int):
        logger.warning(
            f"Legacy checkpoint detected with int image_size={image_size}. "
            f"Assuming square images ({image_size}x{image_size})."
        )
        image_size = (image_size, image_size)

    # Convert lists to tuples if needed
    if normalize_mean is not None and isinstance(normalize_mean, list):
        normalize_mean = tuple(normalize_mean)
    if normalize_std is not None and isinstance(normalize_std, list):
        normalize_std = tuple(normalize_std)

    logger.info(
        f"Model configuration: backbone={backbone}, image_size={image_size}, grayscale={grayscale}"
    )

    # Create model and load weights
    model = BinaryClassifier(
        backbone=backbone,
        pretrained=False,
        image_size=image_size,
        dropout=dropout,
    )
    model.load_state_dict(checkpoint["model_state"])

    # Discover dataset samples
    logger.info(f"Discovering samples in {args.dataset_path}")
    all_samples = discover_binary_samples(args.dataset_path)
    logger.info(f"Found {len(all_samples)} total samples")

    # CRITICAL: Validate ALL images are the correct size BEFORE evaluation
    logger.info(f"Validating that all images are exactly {image_size}...")
    try:
        validate_all_images_upfront(all_samples, image_size, max_check=100)
        logger.info("✓ Image size validation passed")
    except ValueError as e:
        logger.error(f"Image size validation FAILED: {e}")
        sys.exit(1)

    # Select appropriate split
    if args.split == "all":
        samples = all_samples
        split_name = "entire dataset"
    else:
        train_samples, val_samples = split_samples(
            all_samples, val_ratio=args.val_ratio, seed=args.seed
        )
        if args.split == "train":
            samples = train_samples
            split_name = "training split"
        else:  # val
            samples = val_samples
            split_name = "validation split"
        logger.info(f"Using {split_name}: {len(samples)} samples")

    # Create dataset
    dataset = BinaryDataset(
        samples=samples,
        image_size=image_size,
        grayscale=grayscale,
        train=False,  # No augmentation during evaluation
        normalize_mean=normalize_mean,
        normalize_std=normalize_std,
    )

    # Run evaluation
    device = "cpu" if args.cpu else "cuda"
    logger.info(f"Evaluating on {device}...")
    metrics = evaluate_model(
        model=model,
        dataset=dataset,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        device=device,
    )

    # Print results
    print("\n")
    print(f"Evaluation Results on {split_name}")
    print(str(metrics))

    # Save to JSON if requested
    if args.output:
        output_dir = os.path.dirname(args.output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(args.output, "w") as f:
            json.dump(metrics.to_dict(), f, indent=2)
        logger.info(f"Metrics saved to {args.output}")


if __name__ == "__main__":
    main()
