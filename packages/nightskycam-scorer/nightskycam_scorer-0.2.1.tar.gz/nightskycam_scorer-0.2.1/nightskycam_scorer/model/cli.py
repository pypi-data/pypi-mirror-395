# nightskycam_scorer/model/cli.py
from __future__ import annotations

import argparse
import logging

from ..constants import PATCH_SIZE, RESIZED_FULL_SIZE, ImageSize
from ..utils import (compute_normalization_stats, detect_dataset_image_size,
                     set_seed, validate_image_size)
from .data import (BinaryDataset, discover_binary_samples, split_samples,
                   validate_all_images_upfront)
from .train import TrainConfig, train_model

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Train a binary classifier for night-sky image quality."
    )
    p.add_argument(
        "data_dir",
        type=str,
        help="Path to dataset root folder (must contain positive/ and negative/ subdirectories).",
    )
    p.add_argument(
        "--out", type=str, default="./runs", help="Output directory for checkpoints."
    )
    p.add_argument(
        "--image-size",
        type=str,
        default=None,
        choices=["patch", "resized", "auto"],
        help=f"Image size: 'auto' (detect from dataset, default), 'patch' for {PATCH_SIZE}, 'resized' for {RESIZED_FULL_SIZE}. Mutually exclusive with --image-height and --image-width.",
    )
    p.add_argument(
        "--image-height",
        type=int,
        default=None,
        help="Custom image height (disables auto-detection). Must be used with --image-width.",
    )
    p.add_argument(
        "--image-width",
        type=int,
        default=None,
        help="Custom image width (disables auto-detection). Must be used with --image-height.",
    )
    p.add_argument(
        "--grayscale",
        action="store_true",
        help="Convert RGB to grayscale (replicated to 3 channels).",
    )
    p.add_argument("--batch-size", type=int, default=16, help="Batch size.")
    p.add_argument("--epochs", type=int, default=30, help="Number of training epochs.")
    p.add_argument("--lr", type=float, default=3e-4, help="Learning rate.")
    p.add_argument("--weight-decay", type=float, default=1e-4, help="Weight decay.")
    p.add_argument(
        "--val-ratio", type=float, default=0.2, help="Validation split ratio."
    )
    p.add_argument("--seed", type=int, default=42, help="Random seed.")
    p.add_argument("--num-workers", type=int, default=4, help="DataLoader workers.")
    p.add_argument("--cpu", action="store_true", help="Force training on CPU.")
    p.add_argument(
        "--backbone",
        type=str,
        default="auto",
        choices=[
            "auto",
            "mobilenet_v3_small",
            "resnet18",
            "resnet50",
            "efficientnet_b0",
        ],
        help="Model backbone. 'auto' selects based on image size (default: auto).",
    )
    p.add_argument(
        "--dropout",
        type=float,
        default=0.4,
        help="Dropout probability for regularization (default: 0.4).",
    )
    p.add_argument(
        "--compute-norm-stats",
        action="store_true",
        help="Compute dataset-specific normalization statistics instead of using ImageNet.",
    )
    p.add_argument(
        "--pos-weight",
        type=float,
        default=1.2,
        help="Positive class weight multiplier (default: 1.2 for balanced datasets).",
    )
    return p.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    args = parse_args()
    set_seed(args.seed)
    data_dir = args.data_dir

    # Discover samples from positive/ and negative/ directories
    samples = discover_binary_samples(data_dir)
    if not samples:
        logger.error(
            f"No samples found in {data_dir}. Ensure the directory contains "
            f"positive/ and negative/ subdirectories with images."
        )
        return

    # Determine image size
    image_size: ImageSize
    if args.image_height is not None and args.image_width is not None:
        # Custom size specified
        if args.image_size is not None:
            logger.error(
                "Cannot specify both --image-size and --image-height/--image-width"
            )
            return
        image_size = (args.image_height, args.image_width)
        logger.info(f"Using custom image size: {image_size}")
    elif args.image_height is not None or args.image_width is not None:
        logger.error("Must specify both --image-height and --image-width together")
        return
    elif args.image_size == "patch":
        image_size = PATCH_SIZE
        logger.info(f"Using patch size: {PATCH_SIZE}")
    elif args.image_size == "resized":
        image_size = RESIZED_FULL_SIZE
        logger.info(f"Using resized full image size: {RESIZED_FULL_SIZE}")
    else:
        # Auto-detect from dataset (default behavior)
        logger.info("Auto-detecting image size from dataset...")
        try:
            detected_size = detect_dataset_image_size(samples)
            logger.info(f"Detected image size: {detected_size}")

            # Validate it's a supported size
            image_size = validate_image_size(detected_size)

            # Log which preset it matches
            if image_size == PATCH_SIZE:
                logger.info(f"Image size matches PATCH_SIZE {PATCH_SIZE}")
            elif image_size == RESIZED_FULL_SIZE:
                logger.info(f"Image size matches RESIZED_FULL_SIZE {RESIZED_FULL_SIZE}")
        except ValueError as e:
            logger.error(f"Failed to detect image size: {e}")
            return

    # CRITICAL: Validate ALL images are the correct size BEFORE training starts
    logger.info(f"Validating that all images are exactly {image_size}...")
    try:
        validate_all_images_upfront(samples, image_size, max_check=100)
        logger.info("✓ Image size validation passed")
    except ValueError as e:
        logger.error(f"Image size validation FAILED: {e}")
        return

    train_s, val_s = split_samples(samples, val_ratio=args.val_ratio, seed=args.seed)
    logger.info(
        f"Discovered {len(samples)} samples. Train={len(train_s)} Val={len(val_s)}"
    )

    # Compute dataset-specific normalization statistics if requested
    normalize_mean_tuple = None
    normalize_std_tuple = None
    if args.compute_norm_stats:
        logger.info("Computing dataset-specific normalization statistics...")
        mean_list, std_list = compute_normalization_stats(
            data_dir, num_samples=min(500, len(train_s)), grayscale=args.grayscale
        )
        normalize_mean_tuple = (
            float(mean_list[0]),
            float(mean_list[1]),
            float(mean_list[2]),
        )
        normalize_std_tuple = (
            float(std_list[0]),
            float(std_list[1]),
            float(std_list[2]),
        )
        logger.info(f"Computed mean: {normalize_mean_tuple}")
        logger.info(f"Computed std:  {normalize_std_tuple}")
    else:
        logger.info("Using ImageNet normalization statistics")

    train_ds = BinaryDataset(
        samples=train_s,
        image_size=image_size,
        grayscale=args.grayscale,
        train=True,
        normalize_mean=normalize_mean_tuple,
        normalize_std=normalize_std_tuple,
    )
    val_ds = BinaryDataset(
        samples=val_s,
        image_size=image_size,
        grayscale=args.grayscale,
        train=False,
        normalize_mean=normalize_mean_tuple,
        normalize_std=normalize_std_tuple,
    )

    cfg = TrainConfig(
        image_size=image_size,
        grayscale=args.grayscale,
        batch_size=args.batch_size,
        epochs=args.epochs,
        lr=args.lr,
        weight_decay=args.weight_decay,
        seed=args.seed,
        num_workers=args.num_workers,
        device="cpu" if args.cpu else "cuda",
        backbone=args.backbone,
        dropout=args.dropout,
        out_dir=args.out,
        normalize_mean=normalize_mean_tuple,
        normalize_std=normalize_std_tuple,
        pos_weight_multiplier=args.pos_weight,
    )
    ckpt = train_model(train_ds, val_ds, cfg)
    logger.info(f"Training complete! Best model saved at: {ckpt}")


if __name__ == "__main__":
    main()
