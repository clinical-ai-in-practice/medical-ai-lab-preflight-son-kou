"""
Stage 05 — Model Swap (Controlled Change)

Applies one pedagogically meaningful post-processing change to the baseline
predictions and measures its effect on Dice.

The change: **largest connected component (largest-CC) filtering.**

Rationale: The baseline threshold sometimes produces many small, isolated
positive predictions that do not correspond to a real tumour region. A simple
spatial prior — that the target region is a single connected structure — can
filter out these spurious detections.  This is a standard post-processing
technique in medical image segmentation; testing it teaches students about
the role of spatial priors and the limits of pixel-independent thresholds.

Inputs  (must exist):
  outputs/metrics/val_metrics.json   — baseline threshold and Dice values

Outputs:
  outputs/metrics/model_swap_comparison.json
  outputs/figures/model_swap_comparison.png
  reports/model_swap.md
  outputs/status/stage_05_model_swap.json
"""

from pathlib import Path
import json
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import load_pack, pack_info

BASE = Path(__file__).resolve().parents[1]
METRICS_PATH = BASE / "outputs" / "metrics" / "val_metrics.json"

CHANGE_DESCRIPTION = (
    "Post-processed threshold predictions by retaining only the single largest "
    "connected component per slice, discarding all smaller isolated regions."
)

CHANGE_RATIONALE = (
    "The threshold baseline sometimes produces scattered small positive predictions "
    "that are unlikely to represent a real tumour. A spatial prior — that the "
    "target region should be one connected structure — can remove these false "
    "positives. This is a standard, interpretable post-processing step that adds "
    "no learned parameters and is easy to audit."
)


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def dice_score(pred: np.ndarray, gt: np.ndarray) -> float:
    intersection = int(((pred == 1) & (gt == 1)).sum())
    denom = int(pred.sum()) + int(gt.sum())
    return (2 * intersection) / (denom + 1e-8)


def largest_connected_component(binary: np.ndarray) -> np.ndarray:
    """
    Return a binary mask that keeps only the largest connected component.
    Returns the input unchanged if the prediction is empty (all zeros).
    """
    from skimage.measure import label as sk_label

    labeled = sk_label(binary)
    n_components = int(labeled.max())

    if n_components == 0:
        return binary.copy()

    sizes = [int((labeled == k).sum()) for k in range(1, n_components + 1)]
    largest_label = int(np.argmax(sizes)) + 1
    return (labeled == largest_label).astype(np.int32)


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
    baseline_dice = float(metrics["dice"])

    images, masks = load_pack()
    n = len(images)

    baseline_per_slice: list[float] = []
    new_per_slice: list[float] = []

    for i in range(n):
        pred_base = (images[i] > threshold).astype(np.int32)
        pred_cc = largest_connected_component(pred_base)
        baseline_per_slice.append(dice_score(pred_base, masks[i]))
        new_per_slice.append(dice_score(pred_cc, masks[i]))

    new_dice = float(np.mean(new_per_slice))
    delta = new_dice - baseline_dice

    # Pick the slice where the change had the largest absolute effect
    # for the comparison figure — most instructive for students.
    effect = [abs(new_per_slice[i] - baseline_per_slice[i]) for i in range(n)]
    rep_idx = int(np.argmax(effect))

    pred_rep_base = (images[rep_idx] > threshold).astype(np.int32)
    pred_rep_cc = largest_connected_component(pred_rep_base)

    # ---- Comparison figure ----
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))

    axes[0].imshow(images[rep_idx], cmap="gray")
    axes[0].imshow(
        np.ma.masked_where(masks[rep_idx] == 0, masks[rep_idx]),
        cmap="Reds", alpha=0.5,
    )
    axes[0].set_title("Ground truth", fontsize=9)
    axes[0].axis("off")

    axes[1].imshow(images[rep_idx], cmap="gray")
    axes[1].imshow(
        np.ma.masked_where(pred_rep_base == 0, pred_rep_base),
        cmap="Blues", alpha=0.5,
    )
    d_base = baseline_per_slice[rep_idx]
    axes[1].set_title(f"Baseline  Dice={d_base:.3f}", fontsize=9)
    axes[1].axis("off")

    axes[2].imshow(images[rep_idx], cmap="gray")
    axes[2].imshow(
        np.ma.masked_where(pred_rep_cc == 0, pred_rep_cc),
        cmap="Greens", alpha=0.5,
    )
    d_cc = new_per_slice[rep_idx]
    axes[2].set_title(f"Largest-CC  Dice={d_cc:.3f}", fontsize=9)
    axes[2].axis("off")

    bar_colors = ["steelblue", "seagreen" if delta >= 0 else "tomato"]
    axes[3].bar(["Baseline", "Largest CC"], [baseline_dice, new_dice], color=bar_colors)
    axes[3].set_ylim(0, max(1.0, baseline_dice + 0.05, new_dice + 0.05))
    axes[3].set_ylabel("Mean Dice (all slices)")
    axes[3].set_title("Global comparison", fontsize=9)
    for x_pos, val in enumerate([baseline_dice, new_dice]):
        axes[3].text(x_pos, val + 0.01, f"{val:.4f}", ha="center", fontsize=8)

    info = pack_info()
    fig.suptitle(
        f"Model swap — largest-CC post-processing  |  "
        f"representative slice {rep_idx}  |  "
        f"mean Dice: {baseline_dice:.4f} → {new_dice:.4f}  (Δ {delta:+.4f})",
        fontsize=9,
    )
    fig.tight_layout()

    fig_dir = BASE / "outputs" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig_path = fig_dir / "model_swap_comparison.png"
    fig.savefig(fig_path, dpi=120, bbox_inches="tight")
    plt.close(fig)

    # ---- Comparison metrics JSON ----
    comparison = {
        "baseline_dice": round(baseline_dice, 4),
        "new_dice": round(new_dice, 4),
        "delta": round(delta, 4),
        "change_description": CHANGE_DESCRIPTION,
        "threshold": threshold,
        "n_slices": n,
        "representative_slice_idx": rep_idx,
    }

    metrics_dir = BASE / "outputs" / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    (metrics_dir / "model_swap_comparison.json").write_text(
        json.dumps(comparison, indent=2), encoding="utf-8"
    )

    # ---- Report ----
    if delta > 0.001:
        outcome = "improved"
        interpretation = (
            f"The largest-CC filter helped on this dataset. It removed small "
            f"isolated positive predictions that were false alarms, improving "
            f"the mean Dice by {delta:+.4f}. This confirms that the baseline "
            f"threshold produces some spurious scattered predictions, and that "
            f"the target region is reasonably well-described as a single connected "
            f"structure."
        )
    elif delta < -0.001:
        outcome = "degraded"
        interpretation = (
            f"The largest-CC filter hurt on this dataset (Δ = {delta:+.4f}). "
            f"This likely means the target region in some slices is naturally "
            f"fragmented, or the largest predicted component is not the true "
            f"tumour region. The spatial prior 'one connected region' does not "
            f"hold uniformly across this pack — a useful finding."
        )
    else:
        outcome = "left unchanged"
        interpretation = (
            f"The filter had negligible effect (Δ = {delta:+.4f}). The baseline "
            f"predictions are already mostly single-blob. The largest-CC step "
            f"neither helps nor hurts in a meaningful way on this dataset."
        )

    report = f"""# Model Swap — Largest Connected Component Post-Processing

Dataset: {info.get("dataset", "?")}
Modality: {info.get("modality", "?")}
Threshold: {threshold}
Slices evaluated: {n}

## Change Made

**{CHANGE_DESCRIPTION}**

## Rationale

{CHANGE_RATIONALE}

## Results

| Method | Mean Dice |
|---|---|
| Baseline (threshold = {threshold}) | {baseline_dice:.4f} |
| Largest-CC post-processing | {new_dice:.4f} |
| Delta | {delta:+.4f} |

See: `outputs/figures/model_swap_comparison.png`
Representative slice: {rep_idx}
(selected as the slice where the change had the largest absolute effect)

## Interpretation

The controlled change {outcome} the mean Dice score.

{interpretation}

## What to Take Away

1. **A spatial prior is a modelling decision.** Choosing to keep only the
   largest component encodes the assumption "the target is one connected region."
   That assumption may be valid for some datasets and wrong for others — always
   verify empirically.

2. **One honest comparison beats ten cherry-picked numbers.** The metric
   either improves, degrades, or stays flat. All three outcomes are informative.
   What matters is that the comparison is fair: same data, same threshold,
   only one thing changed.

3. **Post-processing is not free.** Even a rule-based filter introduces a
   hyperparameter (here: connectivity definition, 2-D vs. 3-D). For a
   publishable result you would tune and validate this on a held-out set.

4. **Day 2 challenge.** What if you tried this on a harder slice distribution
   where the tumour is smaller or more irregular? Would the conclusion change?
"""

    report_path = BASE / "reports" / "model_swap.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    # ---- Status JSON ----
    status = {
        "status": "ok",
        "baseline_dice": round(baseline_dice, 4),
        "new_dice": round(new_dice, 4),
        "delta": round(delta, 4),
        "change_description": CHANGE_DESCRIPTION,
    }

    status_path = BASE / "outputs" / "status" / "stage_05_model_swap.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")

    direction = "↑ improved" if delta > 0.001 else ("↓ degraded" if delta < -0.001 else "→ unchanged")
    print(f"Model swap complete.")
    print(f"  Baseline Dice : {baseline_dice:.4f}")
    print(f"  New Dice      : {new_dice:.4f}  {direction}")
    print(f"  Delta         : {delta:+.4f}")
    print("Next step: make pack-report")


if __name__ == "__main__":
    main()
