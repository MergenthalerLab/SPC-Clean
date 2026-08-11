# =============================================================================
# SPC-Clean: Sparse Pixel Cluster Cleaning
# Neighborhood Topology-Based Reduction of Speckle and Isolated Pixel Noise
# in Fluorescence Microscopy Images
#
# Author: Pendar Alirezazadeh
# Copyright (c) 2026 Pendar Alirezazadeh
#
# SPDX-License-Identifier: GPL-3.0-or-later
# =============================================================================

import numpy as np
from scipy import ndimage


def spc_clean_binary_mask(
    img: np.ndarray,
    threshold: int = 128,
    min_neighbors: int = 3,
) -> np.ndarray:
    

    if img.ndim != 2:
        raise ValueError(
            f"SPC-Clean expects a 2D image, but received shape {img.shape}."
        )

    if not 0 <= min_neighbors <= 8:
        raise ValueError("min_neighbors must be between 0 and 8.")

    # -------------------------------------------------------------------------
    # Stage 1: Initial threshold-derived foreground mask
    # -------------------------------------------------------------------------
    bw = (img > threshold).astype(np.uint8)

    # 3 x 3 neighborhood, including center pixel.
    kernel = np.ones((3, 3), dtype=np.int32)

    # -------------------------------------------------------------------------
    # Stage 2: Iterative neighborhood-topology pruning
    # -------------------------------------------------------------------------
    while True:

        neighbor_count = ndimage.convolve(
            bw,
            kernel,
            mode="constant",
            cval=0,
        )

        # Remove contribution of the center pixel itself.
        neighbor_count = neighbor_count - bw

        remove = (
            (bw == 1)
            & (neighbor_count < min_neighbors)
        )

        if not np.any(remove):
            break

        bw[remove] = 0

    return (bw * 255).astype(np.uint8)


def spc_clean(
    img: np.ndarray,
    threshold: int = 128,
    min_neighbors: int = 3,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Apply SPC-Clean and return both the refined mask and filtered image.
    
    """

    mask = spc_clean_binary_mask(
        img,
        threshold=threshold,
        min_neighbors=min_neighbors,
    )

    mask01 = (mask > 0).astype(img.dtype)

    filtered = img * mask01

    return mask, filtered
