# =============================================================================
# SPC-Clean: Sparse Pixel Cluster Cleaning
# Neighborhood Topology-Based Reduction of Speckle and Isolated Pixel Noise
# in Fluorescence Microscopy Images
#
# Author: Pendar Alirezazadeh
# Copyright (c) 2026 Pendar Alirezazadeh
#
# Licensed under the PolyForm Noncommercial License 1.0.0.
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
#
# See the LICENSE file in the project repository for the full license terms.
# =============================================================================

from pathlib import Path
import tifffile
from spc_clean import spc_clean

# =============================================================================
# User settings
# =============================================================================

INPUT_IMAGE = Path("input_image.tif")
OUTPUT_MASK = Path("SPC_mask.tif")
OUTPUT_FILTERED = Path("SPC_filtered.tif")

THRESHOLD = 128
MIN_NEIGHBORS = 3


# =============================================================================
# Run SPC-Clean
# =============================================================================

image = tifffile.imread(INPUT_IMAGE)

mask, filtered = spc_clean(
    image,
    threshold=THRESHOLD,
    min_neighbors=MIN_NEIGHBORS,
)

# =============================================================================
# Save results
# =============================================================================

tifffile.imwrite(OUTPUT_MASK, mask)

tifffile.imwrite(OUTPUT_FILTERED, filtered)

print("SPC-Clean completed successfully.")
print(f"Mask saved to:     {OUTPUT_MASK}")
print(f"Filtered image:    {OUTPUT_FILTERED}")
