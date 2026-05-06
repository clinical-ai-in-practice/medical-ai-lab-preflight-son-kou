"""
data_utils.py — shared utilities for loading the imaging teaching pack.

All pipeline scripts import from here so the data loading logic lives
in exactly one place. Do not import from this module inside fetch_data.py
or inspect_data.py (they run before the pack exists).
"""

from pathlib import Path
import sys

import numpy as np

BASE = Path(__file__).resolve().parents[1]
PACK_DIR = BASE / "data" / "sample" / "imaging"

# Accepted array key names in slices.npz, checked in priority order.
_IMAGE_KEYS = ["images", "image", "imgs", "img", "flair", "t1", "t1ce", "t2", "vol"]
_MASK_KEYS = ["masks", "mask", "segs", "seg", "labels", "label", "gt", "tumor"]


def _find_key(available: list[str], candidates: list[str], role: str) -> str:
    key = next((k for k in candidates if k in available), None)
    if key is None:
        print(
            f"[ERROR] Cannot find {role} array in slices.npz.\n"
            f"  Available keys: {available}\n"
            f"  Expected one of: {candidates}",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def load_pack() -> tuple[np.ndarray, np.ndarray]:
    """
    Load the full teaching pack.

    Returns
    -------
    images : ndarray, shape (N, H, W), float64, normalised to [0, 1]
    masks  : ndarray, shape (N, H, W), int32, binary {0, 1}
    """
    npz_path = PACK_DIR / "slices.npz"
    if not npz_path.exists():
        print(
            f"[ERROR] Teaching pack not found at {npz_path}\n"
            "Run: make fetch-sample",
            file=sys.stderr,
        )
        sys.exit(1)

    pack = np.load(npz_path)
    available = list(pack.keys())

    img_key = _find_key(available, _IMAGE_KEYS, "images")
    mask_key = _find_key(available, _MASK_KEYS, "masks")

    images = pack[img_key].astype(np.float64)
    masks = (pack[mask_key] > 0).astype(np.int32)

    # Normalise to [0, 1] per-volume if not already in that range.
    vmax = images.max()
    vmin = images.min()
    if vmax > 1.0 or vmin < 0.0:
        images = (images - vmin) / (vmax - vmin + 1e-8)

    return images, masks


def load_slice(idx: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """
    Load a single 2-D slice from the pack.

    Returns (image_2d, mask_2d).
    idx is clamped to [0, N-1].
    """
    images, masks = load_pack()
    idx = min(max(idx, 0), len(images) - 1)
    return images[idx], masks[idx]


def pack_info() -> dict:
    """
    Return a lightweight summary dict (does NOT load full arrays).
    Reads slices_meta.json if present; falls back to npz inspection.
    """
    meta_path = PACK_DIR / "slices_meta.json"
    if meta_path.exists():
        import json
        return json.loads(meta_path.read_text(encoding="utf-8"))

    npz_path = PACK_DIR / "slices.npz"
    if npz_path.exists():
        pack = np.load(npz_path)
        available = list(pack.keys())
        img_key = next((k for k in _IMAGE_KEYS if k in available), available[0])
        return {"n_slices": len(pack[img_key]), "keys": available}

    return {}
