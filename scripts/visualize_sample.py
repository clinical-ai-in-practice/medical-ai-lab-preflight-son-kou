"""
Stage 02 — Load & Visualize

Loads the teaching pack and produces a labeled overlay figure for one
representative slice. Saves figure to outputs/figures/ and writes the
stage status file.
"""

from pathlib import Path
import json
import sys

import numpy as np
import matplotlib.pyplot as plt

# Add scripts/ to path so data_utils is importable as a plain module.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import load_slice, pack_info

BASE = Path(__file__).resolve().parents[1]


def main() -> None:
    image, mask = load_slice(idx=0)

    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))

    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Image")
    axes[0].axis("off")

    axes[1].imshow(mask, cmap="Reds", vmin=0, vmax=1)
    axes[1].set_title("Ground truth mask")
    axes[1].axis("off")

    # Overlay: image + mask contour
    axes[2].imshow(image, cmap="gray")
    axes[2].imshow(np.ma.masked_where(mask == 0, mask), cmap="Reds", alpha=0.45)
    axes[2].set_title("Overlay")
    axes[2].axis("off")

    info = pack_info()
    modality = info.get("modality", "")
    dataset = info.get("dataset", "")
    fig.suptitle(f"{dataset}  |  {modality}  |  slice 0", fontsize=9)

    fig.tight_layout()

    out_dir = BASE / "outputs" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "sample_overlay.png"
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)

    report_dir = BASE / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "data_notes.md").write_text(
        f"# Data Notes\n\n"
        f"Dataset: {dataset}\n"
        f"Modality: {modality}\n"
        f"Slices available: {info.get('n_slices', '?')}\n\n"
        f"Visualisation produced for slice 0. See outputs/figures/sample_overlay.png.\n",
        encoding="utf-8",
    )

    status = {"status": "ok", "figure": out_path.name, "slice_idx": 0}
    status_dir = BASE / "outputs" / "status"
    status_dir.mkdir(parents=True, exist_ok=True)
    (status_dir / "stage_02_load_visualize.json").write_text(
        json.dumps(status, indent=2), encoding="utf-8"
    )

    print(f"Saved figure: {out_path}")
    print("Next step: make smoke-train")


if __name__ == "__main__":
    main()
