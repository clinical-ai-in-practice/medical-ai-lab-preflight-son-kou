"""
Stage 03 — Train Baseline

Runs a deterministic, threshold-based segmentation baseline over all slices
in the teaching pack. Computes mean Dice, saves a mock loss curve, and writes
the stage status and metrics files.

This is an intentionally simple baseline — the goal is to establish a
reproducible reference point for error analysis (stage 04) and model swap
(stage 05).
"""

from pathlib import Path
import json
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import load_pack, pack_info

BASE = Path(__file__).resolve().parents[1]

# Threshold applied to normalised [0,1] image intensities.
THRESHOLD = 0.5


def dice_score(pred: np.ndarray, gt: np.ndarray) -> float:
    intersection = int(((pred == 1) & (gt == 1)).sum())
    denom = pred.sum() + gt.sum()
    return (2 * intersection) / (denom + 1e-8)


def main() -> None:
    images, masks = load_pack()
    n = len(images)

    per_slice_dice = []
    for i in range(n):
        pred = (images[i] > THRESHOLD).astype(int)
        per_slice_dice.append(dice_score(pred, masks[i]))

    mean_dice = float(np.mean(per_slice_dice))

    # ---- Metrics ----
    metrics = {
        "dice": mean_dice,
        "n_slices": n,
        "threshold": THRESHOLD,
        "per_slice_dice_mean": mean_dice,
        "per_slice_dice_std": float(np.std(per_slice_dice)),
    }
    metrics_dir = BASE / "outputs" / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = metrics_dir / "val_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    # ---- Mock loss curve (placeholder for a real training loop) ----
    fig, ax = plt.subplots(figsize=(5, 3))
    mock_loss = [1.0 - (i / max(n - 1, 1)) * 0.4 for i in range(n)]
    ax.plot(mock_loss, label="mock loss", color="steelblue")
    ax.axhline(1 - mean_dice, linestyle="--", color="tomato", label=f"1 - mean Dice ({mean_dice:.3f})")
    ax.set_xlabel("slice index")
    ax.set_ylabel("value")
    ax.set_title("Baseline — mock loss curve")
    ax.legend(fontsize=8)
    fig.tight_layout()

    fig_dir = BASE / "outputs" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    curve_path = fig_dir / "loss_curve.png"
    fig.savefig(curve_path, dpi=120, bbox_inches="tight")
    plt.close(fig)

    # ---- Report ----
    info = pack_info()
    report_dir = BASE / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "train_notes.md").write_text(
        f"# Train Notes — Baseline\n\n"
        f"Dataset: {info.get('dataset', '?')}\n"
        f"Modality: {info.get('modality', '?')}\n"
        f"Slices evaluated: {n}\n\n"
        f"## Results\n\n"
        f"- Threshold: {THRESHOLD}\n"
        f"- Mean Dice: {mean_dice:.4f}\n"
        f"- Dice std:  {np.std(per_slice_dice):.4f}\n",
        encoding="utf-8",
    )

    # ---- Status ----
    status = {"status": "ok", "dice": mean_dice, "n_slices": n, "threshold": THRESHOLD}
    (BASE / "outputs" / "status" / "stage_03_train_baseline.json").write_text(
        json.dumps(status, indent=2), encoding="utf-8"
    )

    print(f"Baseline complete — mean Dice: {mean_dice:.4f}  ({n} slices)")
    print(f"Saved metrics : {metrics_path}")
    print("Next step: make error-analysis")


if __name__ == "__main__":
    main()
