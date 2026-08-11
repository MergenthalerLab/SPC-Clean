# =============================================================================
# SPC-Clean: Sparse Pixel Cluster Cleaning
# Example: Batch Processing of Microscopy Images
#
# Author: Pendar Alirezazadeh
# Copyright (c) 2026 Pendar Alirezazadeh
#
# SPDX-License-Identifier: GPL-3.0-or-later
# =============================================================================

from pathlib import Path
import tifffile
from spc_clean import spc_clean


# =============================================================================
# User settings
# =============================================================================

INPUT_FOLDER = Path("images")
MASK_FOLDER = Path("SPC_masks")
FILTERED_FOLDER = Path("SPC_filtered")

THRESHOLD = 128
MIN_NEIGHBORS = 3


# =============================================================================
# Prepare output folders
# =============================================================================

MASK_FOLDER.mkdir(parents=True, exist_ok=True)
FILTERED_FOLDER.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Find microscopy images
# =============================================================================

extensions = {
    ".tif",
    ".tiff",
}

image_files = sorted(
    path
    for path in INPUT_FOLDER.iterdir()
    if path.suffix.lower() in extensions
)


print(f"Found {len(image_files)} images.")


# =============================================================================
# Apply SPC-Clean
# =============================================================================

for image_path in image_files:

    print(f"Processing: {image_path.name}")
    image = tifffile.imread(image_path)
    mask, filtered = spc_clean(
        image,
        threshold=THRESHOLD,
        min_neighbors=MIN_NEIGHBORS,
    )
    mask_path = (
        MASK_FOLDER
        / f"{image_path.stem}-SPCclean.tif"
    )
    filtered_path = (
        FILTERED_FOLDER
        / f"{image_path.stem}-SPCfiltered.tif"
    )

    tifffile.imwrite(mask_path, mask)
    tifffile.imwrite(filtered_path, filtered)

print("SPC-Clean batch processing completed.")
