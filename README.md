# SPC-Clean

**SPC-Clean (Sparse Pixel Cluster Cleaning)** is a neighborhood
topology-based method for reducing speckle and isolated pixel noise in
fluorescence microscopy images.

SPC-Clean operates on the **thresholded foreground topology rather than
directly modifying image intensities**. It iteratively removes
foreground pixels with insufficient local neighborhood support until the
mask converges. The refined mask can then be mapped back to the original
image while preserving the original intensities of retained foreground
pixels.

## Installation

Clone the repository and install SPC-Clean:

``` bash
git clone https://github.com/MergenthalerLab/SPC-Clean.git
cd SPC-Clean
pip install -e .
```

SPC-Clean requires **Python \>= 3.9**.

## Usage

### napari plugin

After installation, launch napari:

``` bash
napari
```

Open **SPC-Clean** from the napari plugin menu. The plugin supports
folder-based processing and generates SPC-Clean binary masks and,
optionally, filtered intensity images.

### Python

SPC-Clean can also be used directly as a Python function:

``` python
import tifffile
from spc_clean import spc_clean

image = tifffile.imread("image.tif")

mask, filtered = spc_clean(
    image,
    threshold=128,
    min_neighbors=3,
)

tifffile.imwrite("SPC_mask.tif", mask)
tifffile.imwrite("SPC_filtered.tif", filtered)
```

Standalone examples for single-image and batch processing are provided
in the `examples/` directory.

## Parameters

-   **`threshold`** --- intensity threshold used to generate the initial
    foreground mask.
-   **`min_neighbors`** --- minimum number of foreground neighbors
    required for a foreground pixel to remain in the mask during
    iterative pruning.

## Outputs

SPC-Clean returns:

-   **SPC-Clean mask** --- refined binary foreground mask.
-   **Filtered image** --- original image masked by the refined
    foreground topology, preserving the original intensities of retained
    pixels.

## Repository Structure

``` text
SPC-Clean/
├── LICENSE
├── README.md
├── pyproject.toml
├── .gitignore
├── examples/
│   ├── spc_clean_single_image.py
│   └── spc_clean_batch.py
└── src/
    └── spc_clean/
        ├── __init__.py
        ├── _algorithm.py
        ├── _widget.py
        └── napari.yaml
```

## Citation

If you use SPC-Clean in scientific work, please cite the associated
publication.

**SPC-Clean: A napari Plugin for Reducing Speckle and Isolated Pixel Noise in Fluorescence Microscopy Images**
Pendar Alirezazadeh, Elena Marie Kirsch, Yuan Tian, Joerg Bewersdorf, Jens Rittscher, Philipp Mergenthaler
bioRxiv 2026.08.24.744862; doi: https://doi.org/10.64898/2026.08.24.744862

## Sample data

Sample image data that allow rapid evaluation of SPC-Clean were deposited on the open science platform Zenodo (https://doi.org/10.5281/zenodo.21934521).

## License

SPC-Clean is released under a **PolyForm Noncommercial License 1.0.0** for non-commercial and academic research. For commercial licensing inquiries (including AI training, product development, or commercial applicatio), please contact us. See the `LICENSE` file for details.

## Author

**Pendar Alirezazadeh**

Copyright © 2026 Pendar Alirezazadeh
