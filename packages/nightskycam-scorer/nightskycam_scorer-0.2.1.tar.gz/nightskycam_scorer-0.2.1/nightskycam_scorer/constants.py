from typing import Final, List, Literal, Tuple

# Image suffixes supported
IMAGE_SUFFIXES: Final[List[str]] = [".png", ".jpg", ".jpeg", ".tif", ".tiff"]

# Binary classification labels
BINARY_CLASSES: Final[List[str]] = ["negative", "positive"]

# Image size constants
# Patch size for 600x600 image patches extracted from full-size images
PATCH_SIZE: Final[Tuple[int, int]] = (600, 600)

# Resized full image size (height, width)
RESIZED_FULL_SIZE: Final[Tuple[int, int]] = (136, 200)

# Type definitions for image sizes
# Generic image size as (height, width) tuple
ImageSize = Tuple[int, int]
