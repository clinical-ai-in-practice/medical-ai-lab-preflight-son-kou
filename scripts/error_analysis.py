"""
Stage 04 — Error Analysis

Identifies the best-performing and worst-performing slices from the baseline
run, produces annotated error-map figures for each, and writes a concise
report explaining what the patterns suggest.

Inputs  (must exist before running this stage):
  outputs/metrics/val_metrics.json   — baseline threshold and Dice values

Outputs:
  outputs/figures/error_analysis_best.png
  outputs/figures/error_analysis_worst.png
  reports/error_analysis.md
  outputs/status/stage_04_error_analysis.json
"""

from pathlib import Path
import json
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import load_pack, pack_info

BASE = Path(__file__).resolve().parents[1]
METRICS_PATH = BASE / "outputs" / "metrics" / "val_metrics.json"


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def dice_score(pred: np.ndarray, gt: np.ndarray) -> float:
    intersection = int(((pred == 1) & (gt == 1)).sum())
    denom = int(pred.sum()) + int(gt.sum())
    return (2 * intersection) / (denom + 1e-8)


def make_error_rgba(pred: np.ndarray, gt: np.ndarray) -> np.ndarray:
    """
    RGBA overlay encoding prediction errors:
      TP = green,  FP = red,  FN = orange,  TN = transparent
    """
    h, w = pred.shape
    rgba = np.zeros((h, w, 4), dtype=float)
    rgba[(pred == 1) & (gt == 1)] = [0.20, 0.78, 0.20, 0.70]  # TP green
    rgba[(pred == 1) & (gt == 0)] = [0.90, 0.20, 0.20, 0.70]  # FP red
    rgba[(pred == 0) & (gt == 1)] = [1.00, 0.60, 0.00, 0.70]  # FN orange
    return rgba


def save_case_figure(
    image: np.ndarray,
    gt: np.ndarray,
    pred: np.ndarray,
    dice: float,
    title: str,
    out_path: Path,
) -> None:
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))

    axes[0].imshow(image, cmap="gray")
    axes[0].set_title("Image", fontsize=9)
    axes[0].axis("off")

    axes[1].imshow(image, cmap="gray")
    axes[1].imshow(np.ma.masked_where(gt == 0, gt), cmap="Reds", alpha=0.5)
    axes[1].set_title("Ground truth", fontsize=9)
    axes[1].axis("off")

    axes[2].imshow(image, cmap="gray")
    axes[2].imshow(np.ma.masked_where(pred == 0, pred), cmap="Blues", alpha=0.5)
    axes[2].set_title(f"Prediction  Dice={dice:.3f}", fontsize=9)
    axes[2].axis("off")

    axes[3].imshow(image, cmap="gray")
    axes[3].imshow(make_error_rgba(pred, gt))
    axes[3].set_title("Error map", fontsize=9)
    axes[3].axis("off")

    tp_patch = mpatches.Patch(color=(0.20, 0.78, 0.20), label="TP")
    fp_patch = mpatches.Patch(color=(0.90, 0.20, 0.20), label="FP (false alarm)")
    fn_patch = mpatches.Patch(color=(1.00, 0.60, 0.00), label="FN (missed)")
    fig.legend(handles=[tp_patch, fp_patch, fn_patch],
               loc="lower center", ncol=3, fontsize=8, framealpha=0.8)

    fig.suptitle(title, fontsize=10)
    fig.tight_layout(rect=[0, 0.09, 1, 1])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ #
# Main                                                                #
# ------------------------------------------------------------------ #

def main() -> None:
    if not METRICS_PATH.exists():
        print(
            "[ERROR] outputs/metrics/val_metrics.json not found.\n"
            "Run: make smoke-train",
            file=sys.stderr,
        )
        sys.exit(1)

    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    threshold = float(metrics.get("threshold", 0.5))

    images, masks = load_pack()
    n = len(images)

    # Compute per-slice Dice using the same threshold as the baseline.
    per_slice: list[dict] = []
    for i in range(n):
        pred = (images[i] > threshold).astype(np.int32)
        d = dice_score(pred, masks[i])
        tp = int(((pred == 1) & (masks[i] == 1)).sum())
        fp = int(((pred == 1) & (masks[i] == 0)).sum())
        fn = int(((pred == 0) & (masks[i] == 1)).sum())
        gt_pos = int(masks[i].sum())
        per_slice.append({"idx": i, "dice": d, "pred": pred,
                          "tp": tp, "fp": fp, "fn": fn, "gt_pos": gt_pos})

    per_slice_sorted = sorted(per_slice, key=lambda x: x["dice"])
    worst = per_slice_sorted[0]
    best = per_slice_sorted[-1]

    # ---- Figures ----
    fig_dir = BASE / "outputs" / "figures"

    save_case_figure(
        images[best["idx"]], masks[best["idx"]], best["pred"], best["dice"],
        f"Best case — slice {best['idx']}  |  Dice = {best['dice']:.3f}",
        fig_dir / "error_analysis_best.png",
    )

    save_case_figure(
        images[worst["idx"]], masks[worst["idx"]], worst["pred"], worst["dice"],
        f"Worst case — slice {worst['idx']}  |  Dice = {worst['dice']:.3f}",
        fig_dir / "error_analysis_worst.png",
    )

    # ---- Report ----
    info = pack_info()
    mean_dice = float(metrics.get("dice", 0.0))
    dice_gap = best["dice"] - worst["dice"]

    # Interpret worst-case error pattern
    if worst["fp"] > worst["fn"]:
        error_pattern = (
            "The dominant error is **false positives** — the model predicts tumour "
            "where there is none. The intensity threshold is too permissive for this slice."
        )
    elif worst["fn"] > worst["fp"]:
        error_pattern = (
            "The dominant error is **false negatives** — the model misses real tumour "
            "pixels. The intensity of the tumour region in this slice is not distinct "
            "enough from background to be captured by the threshold."
        )
    else:
        error_pattern = (
            "False positives and false negatives are roughly balanced, "
            "suggesting the threshold sits near the decision boundary for this slice."
        )

    report = f"""# Error Analysis

Dataset: {info.get("dataset", "?")}
Modality: {info.get("modality", "?")}
Threshold used: {threshold}
Slices analysed: {n}

## Method

Each slice is segmented with the same intensity threshold ({threshold}) used in the
baseline. We compute Dice between the thresholded prediction and the ground-truth
mask, then rank slices from best to worst.

## Best Case — Slice {best["idx"]}  (Dice = {best["dice"]:.4f})

| Metric | Value |
|---|---|
| Ground-truth positives | {best["gt_pos"]} px |
| True positives (TP) | {best["tp"]} px |
| False positives (FP) | {best["fp"]} px |
| False negatives (FN) | {best["fn"]} px |

The prediction closely matches the ground truth on this slice.
The tumour pixels have a noticeably higher intensity than background, making
the fixed threshold effective. This is the kind of slice the baseline is
well-suited to.

See: `outputs/figures/error_analysis_best.png`

## Worst Case — Slice {worst["idx"]}  (Dice = {worst["dice"]:.4f})

| Metric | Value |
|---|---|
| Ground-truth positives | {worst["gt_pos"]} px |
| True positives (TP) | {worst["tp"]} px |
| False positives (FP) | {worst["fp"]} px |
| False negatives (FN) | {worst["fn"]} px |

{error_pattern}

See: `outputs/figures/error_analysis_worst.png`

## Reflection

The performance gap between best and worst case is {dice_gap:.4f}
(best Dice = {best["dice"]:.4f}, worst = {worst["dice"]:.4f}, overall mean = {mean_dice:.4f}).

A fixed intensity threshold is brittle because it does not use any spatial
context — it treats every pixel independently. The cases where it fails
most severely are slices where the tumour intensity distribution overlaps
with healthy tissue.

**Suggested experiment for Stage 05:**
A spatial post-processing step — such as keeping only the largest connected
component of the prediction — could reduce isolated false-positive predictions
without needing a fundamentally different model. Stage 05 will test this.
"""

    report_path = BASE / "reports" / "error_analysis.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    # ---- Status JSON ----
    status = {
        "status": "ok",
        "threshold": threshold,
        "n_slices": n,
        "best_case": {
            "slice_idx": best["idx"],
            "dice": round(best["dice"], 4),
            "true_positives": best["tp"],
            "false_positives": best["fp"],
            "false_negatives": best["fn"],
        },
        "worst_case": {
            "slice_idx": worst["idx"],
            "dice": round(worst["dice"], 4),
            "true_positives": worst["tp"],
            "false_positives": worst["fp"],
            "false_negatives": worst["fn"],
        },
    }

    status_path = BASE / "outputs" / "status" / "stage_04_error_analysis.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")

    print(f"Error analysis complete  ({n} slices evaluated).")
    print(f"  Best case:  slice {best['idx']}   Dice = {best['dice']:.4f}")
    print(f"  Worst case: slice {worst['idx']}  Dice = {worst['dice']:.4f}")
    print(f"  Gap:        {dice_gap:.4f}")
    print("Next step: make model-swap")


if __name__ == "__main__":
    main()
