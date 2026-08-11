# =============================================================================
# SPC-Clean: Sparse Pixel Cluster Cleaning
#
# Author: Pendar Alirezazadeh
# Copyright (c) 2026 Pendar Alirezazadeh
#
# SPDX-License-Identifier: GPL-3.0-or-later
# =============================================================================

from ._algorithm import spc_clean, spc_clean_binary_mask

__all__ = [
    "spc_clean",
    "spc_clean_binary_mask",
]
