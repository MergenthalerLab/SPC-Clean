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

import numpy as np
import tifffile
from magicgui import magic_factory
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import os

from ._algorithm import spc_clean_binary_mask


def _process_one_image(img_path, spc_mask_folder, filtered_image_folder,
                       threshold, min_neighbors, generate_filtered):
    

    img = tifffile.imread(str(img_path))

    # generate SPC-Clean mask
    spc_mask = spc_clean_binary_mask(
        img,
        threshold=threshold,
        min_neighbors=min_neighbors,
    )

    # save mask
    mask_path = spc_mask_folder / f"{img_path.stem}-SPCclean.tif"
    tifffile.imwrite(str(mask_path), spc_mask)

    out_path = None
    filtered_img = None

    # apply mask and save filtered image (optional)
    if generate_filtered:
        mask01 = (spc_mask > 0).astype(img.dtype)
        filtered_img = img * mask01

        out_path = filtered_image_folder / f"{img_path.stem}-SPCfiltered.tif"
        tifffile.imwrite(str(out_path), filtered_img)

    
    return {
        "img_path": img_path,
        "mask_path": mask_path,
        "filtered_path": out_path,
        "generate_filtered": generate_filtered,
    }


@magic_factory(
    call_button="Run SPC-Clean",
    raw_image_folder={"mode": "d"},
    spc_mask_folder={"mode": "d"},
    filtered_image_folder={"mode": "d"},
)
def spc_clean_widget(
    viewer: "napari.viewer.Viewer",
    raw_image_folder: Path = Path("."),
    spc_mask_folder: Path = Path("."),
    filtered_image_folder: Path = Path("."),
    threshold: int = 128,
    min_neighbors: int = 3,
    generate_filtered: bool = False,   # ✅ DEFAULT FALSE
    num_cpu_workers: int = max(1, os.cpu_count() - 1),  # optional control
):

    
    
    
    if not raw_image_folder.exists():
        print("Input folder does not exist")
        return

    spc_mask_folder.mkdir(parents=True, exist_ok=True)

    if generate_filtered:
        filtered_image_folder.mkdir(parents=True, exist_ok=True)

    extensions = (".tif", ".tiff", ".png", ".jpg", ".jpeg")
    image_files = [f for f in raw_image_folder.iterdir() if f.suffix.lower() in extensions]

    if len(image_files) == 0:
        print("No images found in input folder")
        return

    print(f"Found {len(image_files)} images.")
    print(f"Using {num_cpu_workers} CPU workers...")
    print(f"Generate filtered images: {generate_filtered}")

    
    
    
    futures = []
    with ProcessPoolExecutor(max_workers=num_cpu_workers) as executor:

        for img_path in image_files:
            futures.append(
                executor.submit(
                    _process_one_image,
                    img_path,
                    spc_mask_folder,
                    filtered_image_folder,
                    threshold,
                    min_neighbors,
                    generate_filtered,
                )
            )

        for fut in as_completed(futures):
            result = fut.result()

            img_path = result["img_path"]
            mask_path = result["mask_path"]
            filtered_path = result["filtered_path"]

            print("Finished:", img_path.name)
            print("Saved mask:", mask_path)

            
            
            
            img = tifffile.imread(str(img_path))
            spc_mask = tifffile.imread(str(mask_path))

            viewer.add_image(img, name=f"Original - {img_path.stem}")
            viewer.add_labels(spc_mask, name=f"SPC Mask - {img_path.stem}")

            if generate_filtered and filtered_path is not None:
                filtered_img = tifffile.imread(str(filtered_path))
                viewer.add_image(filtered_img, name=f"Filtered - {img_path.stem}")
                print("Saved filtered image:", filtered_path)

    print("Done")
