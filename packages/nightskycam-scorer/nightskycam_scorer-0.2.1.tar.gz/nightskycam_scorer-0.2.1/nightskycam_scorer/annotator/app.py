"""
Simple web-based binary annotation tool for night-sky images.
Shows images one at a time and saves them to positive/ or negative/ directories.
"""

from __future__ import annotations

import base64
import io
import os
import shutil
from dataclasses import dataclass
from typing import List, Optional

import numpy as np
from flask import Flask, redirect, render_template_string, request, url_for
from PIL import Image

from ..constants import IMAGE_SUFFIXES
from ..utils import load_image_any


@dataclass
class AnnotatorConfig:
    """Configuration for the binary annotator."""

    input_dir: str  # Directory containing images to annotate
    output_dir: str  # Root directory for positive/ and negative/ subdirs
    preview_size: int = 600  # Size for browser preview


def discover_images(input_dir: str) -> List[str]:
    """
    Discover all images in input directory (non-recursive).

    Args:
        input_dir: Directory to search for images

    Returns:
        Sorted list of image paths
    """
    images: List[str] = []
    if not os.path.isdir(input_dir):
        return images

    for filename in os.listdir(input_dir):
        _, ext = os.path.splitext(filename)
        if ext.lower() in IMAGE_SUFFIXES:
            images.append(os.path.join(input_dir, filename))

    images.sort()
    return images


class AnnotationState:
    """Manages annotation state and file operations."""

    def __init__(self, cfg: AnnotatorConfig) -> None:
        self._cfg = cfg
        self._all_images = discover_images(cfg.input_dir)
        self._current_idx = 0

        # Create output directories
        self._positive_dir = os.path.join(cfg.output_dir, "positive")
        self._negative_dir = os.path.join(cfg.output_dir, "negative")
        os.makedirs(self._positive_dir, exist_ok=True)
        os.makedirs(self._negative_dir, exist_ok=True)

    def get_current_image(self) -> Optional[str]:
        """Get path to current image, or None if done."""
        if self._current_idx >= len(self._all_images):
            return None
        return self._all_images[self._current_idx]

    def get_progress(self) -> tuple[int, int]:
        """Return (current_index, total_images)."""
        return (self._current_idx + 1, len(self._all_images))

    def save_annotation(self, label: str) -> None:
        """
        Save current image to positive/ or negative/ directory and advance.

        Args:
            label: Either "positive" or "negative"
        """
        img_path = self.get_current_image()
        if img_path is None:
            return

        filename = os.path.basename(img_path)

        if label == "positive":
            dest = os.path.join(self._positive_dir, filename)
        elif label == "negative":
            dest = os.path.join(self._negative_dir, filename)
        else:
            return  # Invalid label, skip

        # Copy file to destination
        shutil.copy2(img_path, dest)

        # Advance to next image
        self._current_idx += 1

    def skip(self) -> None:
        """Skip current image without saving."""
        self._current_idx += 1

    def make_preview(self, img_path: str) -> str:
        """
        Create a base64-encoded JPEG preview for browser display.

        Args:
            img_path: Path to image file

        Returns:
            Data URI string (data:image/jpeg;base64,...)
        """
        # Load image as RGB float [0,1]
        img = load_image_any(img_path, force_rgb=True)

        # Convert to 8-bit
        img8 = np.clip(img * 255.0, 0, 255).astype(np.uint8)
        pil_img = Image.fromarray(img8, mode="RGB")

        # Resize if needed
        if (
            pil_img.width != self._cfg.preview_size
            or pil_img.height != self._cfg.preview_size
        ):
            pil_img = pil_img.resize(
                (self._cfg.preview_size, self._cfg.preview_size),
                Image.Resampling.LANCZOS,
            )

        # Encode as JPEG
        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG", quality=90, optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")

        return f"data:image/jpeg;base64,{b64}"


def create_app(cfg: AnnotatorConfig) -> Flask:
    """
    Create Flask app for binary annotation.

    Args:
        cfg: Annotator configuration

    Returns:
        Flask application
    """
    app = Flask(__name__)
    state = AnnotationState(cfg)

    TEMPLATE = """
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>Binary Image Annotator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: #f5f5f5;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .header {
                text-align: center;
                margin-bottom: 20px;
            }
            .progress {
                font-size: 18px;
                color: #555;
                margin-bottom: 10px;
            }
            .image-container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .preview-img {
                max-width: 600px;
                max-height: 600px;
                border: 2px solid #ddd;
                border-radius: 4px;
            }
            .filename {
                text-align: center;
                margin-top: 10px;
                font-size: 14px;
                color: #666;
                word-break: break-all;
            }
            .controls {
                display: flex;
                gap: 20px;
                justify-content: center;
            }
            .btn {
                padding: 15px 40px;
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.2s;
            }
            .btn-positive {
                background: #28a745;
                color: white;
            }
            .btn-positive:hover {
                background: #218838;
                transform: scale(1.05);
            }
            .btn-negative {
                background: #dc3545;
                color: white;
            }
            .btn-negative:hover {
                background: #c82333;
                transform: scale(1.05);
            }
            .btn-skip {
                background: #6c757d;
                color: white;
            }
            .btn-skip:hover {
                background: #5a6268;
                transform: scale(1.05);
            }
            .info {
                text-align: center;
                margin-top: 20px;
                padding: 15px;
                background: white;
                border-radius: 8px;
                max-width: 600px;
            }
            .complete {
                text-align: center;
                padding: 40px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .complete h2 {
                color: #28a745;
            }
            .shortcut-hint {
                font-size: 12px;
                color: #999;
                margin-top: 10px;
            }
        </style>
        <script>
            document.addEventListener('keydown', function(e) {
                if (e.key === 'p' || e.key === 'P') {
                    document.getElementById('positive-btn').click();
                } else if (e.key === 'n' || e.key === 'N') {
                    document.getElementById('negative-btn').click();
                } else if (e.key === 's' || e.key === 'S') {
                    document.getElementById('skip-btn').click();
                }
            });
        </script>
    </head>
    <body>
        {% if done %}
        <div class="complete">
            <h2>✓ Annotation Complete!</h2>
            <p>All images have been processed.</p>
            <p><strong>Annotated:</strong> {{ progress[0] }} / {{ progress[1] }} images</p>
            <p>Output saved to: {{ output_dir }}</p>
        </div>
        {% else %}
        <div class="header">
            <h1>Binary Image Annotator</h1>
            <div class="progress">Image {{ progress[0] }} / {{ progress[1] }}</div>
        </div>

        <div class="image-container">
            <img class="preview-img" src="{{ preview_data }}" alt="Current image">
            <div class="filename">{{ filename }}</div>
        </div>

        <div class="controls">
            <form method="post" action="{{ url_for('annotate') }}" style="display: inline;">
                <input type="hidden" name="label" value="positive">
                <button id="positive-btn" class="btn btn-positive" type="submit">
                    ✓ Positive (P)
                </button>
            </form>

            <form method="post" action="{{ url_for('annotate') }}" style="display: inline;">
                <input type="hidden" name="label" value="negative">
                <button id="negative-btn" class="btn btn-negative" type="submit">
                    ✗ Negative (N)
                </button>
            </form>

            <form method="post" action="{{ url_for('skip') }}" style="display: inline;">
                <button id="skip-btn" class="btn btn-skip" type="submit">
                    → Skip (S)
                </button>
            </form>
        </div>

        <div class="info">
            <strong>Instructions:</strong><br>
            Click <strong>Positive</strong> for clear night sky images (or press <kbd>P</kbd>)<br>
            Click <strong>Negative</strong> for unsuitable images (or press <kbd>N</kbd>)<br>
            Click <strong>Skip</strong> to skip without saving (or press <kbd>S</kbd>)
            <div class="shortcut-hint">Keyboard shortcuts enabled for faster annotation</div>
        </div>
        {% endif %}
    </body>
    </html>
    """

    @app.get("/")
    def index():
        """Main annotation page."""
        img_path = state.get_current_image()
        progress = state.get_progress()

        if img_path is None:
            # All done
            return render_template_string(
                TEMPLATE,
                done=True,
                progress=progress,
                output_dir=cfg.output_dir,
            )

        preview_data = state.make_preview(img_path)
        filename = os.path.basename(img_path)

        return render_template_string(
            TEMPLATE,
            done=False,
            preview_data=preview_data,
            filename=filename,
            progress=progress,
            output_dir=cfg.output_dir,
        )

    @app.post("/annotate")
    def annotate():
        """Handle positive/negative annotation."""
        label = request.form.get("label", "")
        state.save_annotation(label)
        return redirect(url_for("index"))

    @app.post("/skip")
    def skip():
        """Handle skip action."""
        state.skip()
        return redirect(url_for("index"))

    return app
