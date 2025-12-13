"""CLI entry point for the binary annotation tool."""

from __future__ import annotations

import argparse
import logging

from .app import AnnotatorConfig, create_app

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Binary annotation tool for night-sky images."
    )
    p.add_argument(
        "input_dir",
        type=str,
        help="Directory containing images to annotate (600x600 RGB).",
    )
    p.add_argument(
        "output_dir",
        type=str,
        help="Output directory (will create positive/ and negative/ subdirectories).",
    )
    p.add_argument(
        "--preview-size",
        type=int,
        default=600,
        help="Preview size in pixels for browser display (default: 600).",
    )
    p.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host to bind the server to (default: 127.0.0.1).",
    )
    p.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port for the web server (default: 5000).",
    )
    p.add_argument(
        "--debug",
        action="store_true",
        help="Enable Flask debug mode.",
    )
    return p.parse_args()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    args = parse_args()

    cfg = AnnotatorConfig(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        preview_size=args.preview_size,
    )

    app = create_app(cfg)

    logger.info(f"Starting binary annotator at http://{args.host}:{args.port}")
    logger.info(f"  Input:  {args.input_dir}")
    logger.info(f"  Output: {args.output_dir}")
    logger.info(f"  Positive images will be saved to: {args.output_dir}/positive/")
    logger.info(f"  Negative images will be saved to: {args.output_dir}/negative/")
    logger.info("")
    logger.info("Open the URL in your browser and use:")
    logger.info("  - Click 'Positive' or press 'P' for clear night sky")
    logger.info("  - Click 'Negative' or press 'N' for unsuitable images")
    logger.info("  - Click 'Skip' or press 'S' to skip without saving")

    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
