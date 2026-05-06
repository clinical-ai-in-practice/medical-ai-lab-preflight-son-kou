"""
Stage 08 — Adapt Pipeline (Day 2 Challenge)

Implements the adaptation described in reports/challenge_plan.md:
  Per-slice Otsu adaptive thresholding + largest-CC post-processing

The baseline (fixed threshold) is evaluated on the same slices for a fair
comparison.  Both pipelines apply largest-CC post-processing so the only
variable is the threshold selection method.

Inputs (must exist):
  outputs/metrics/val_metrics.json     — baseline threshold and Dice
  outputs/status/stage_07_challenge_plan.json

Outputs:
  outputs/figures/challenge_comparison.png
  outputs/metrics/challenge_comparison.json
  reports/adapt_pipeline.md
  outputs/status/stage_08_adapt_pipeline.json
"""

from pathlib import Path
import json
import sys

import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import load_pack, pack_info

BASE = Path(__file__).resolve().parents[1]
VAL_METRICS = BASE / "outputs" / "metrics" / "val_metrics.json"
PLAN_STATUS = BASE / "outputs" / "status" / "stage_07_challenge_plan.json"

CHANGE_DESCRIPTION = (
    "Replaced the fixed intensity threshold with per-slice Otsu adaptive "
    "thresholding, combined with the largest-CC post-processing step from Day 1."
)


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def dice_score(pred: np.ndarray, gt: np.ndarray) -> float:
    intersection = int(((pred == 1) & (gt == 1)).sum())
    denom = int(pred.sum()) + int(gt.sum())
    return (2 * intersection) / (denom + 1e-8)


def largest_connected_component(binary: np.ndarray) -> np.ndarray:
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
    if not VAL_METRICS.exists():
        print(
            "[ERROR] outputs/metrics/val_metrics.json not found.\n"
            "Run: make smoke-train",
            file=sys.stderr,
        )
        sys.exit(1)

    if not PLAN_STATUS.exists():
        print(
            "[ERROR] outputs/status/stage_07_challenge_plan.json not found.\n"
            "Run: make challenge-plan",
            file=sys.stderr,
        )
        sys.exit(1)

    from skimage.filters import threshold_otsu

    metrics = json.loads(VAL_METRICS.read_text(encoding="utf-8"))
    threshold = float(metrics.get("threshold", 0.5))

    images, masks = load_pack()
    n = len(images)

    baseline_per_slice: list[float] = []
    otsu_per_slice: list[float] = []
    otsu_thresholds: list[float] = []

    for i in range(n):
        # Baseline: fixed threshold + CC filter (same as Day 1 Stage 05)
        pred_base = (images[i] > threshold).astype(np.int32)
        pred_base_cc = largest_connected_component(pred_base)
        baseline_per_slice.append(dice_score(pred_base_cc, masks[i]))

        # Day 2: Otsu per-slice threshold + CC filter
        t_otsu = float(threshold_otsu(images[i]))
        pred_otsu = (images[i] > t_otsu).astype(np.int32)
        pred_otsu_cc = largest_connected_component(pred_otsu)
        otsu_per_slice.append(dice_score(pred_otsu_cc, masks[i]))
        otsu_thresholds.append(round(t_otsu, 4))

    baseline_dice = float(np.mean(baseline_per_slice))
    new_dice = float(np.mean(otsu_per_slice))
    delta = new_dice - baseline_dice

    # Representative slice: largest absolute effect
    effect = [abs(otsu_per_slice[i] - baseline_per_slice[i]) for i in range(n)]
    rep_idx = int(np.argmax(effect))

    pred_rep_base = largest_connected_component(
        (images[rep_idx] > threshold).astype(np.int32)
    )
    pred_rep_otsu = largest_connected_component(
        (images[rep_idx] > threshold_otsu(images[rep_idx])).astype(np.int32)
    )

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
    axes[1].set_title(f"Fixed threshold  Dice={d_base:.3f}", fontsize=9)
    axes[1].axis("off")

    axes[2].imshow(images[rep_idx], cmap="gray")
    axes[2].imshow(
        np.ma.masked_where(pred_rep_otsu == 0, pred_rep_otsu),
        cmap="Greens", alpha=0.5,
    )
    d_otsu = otsu_per_slice[rep_idx]
    t_rep = otsu_thresholds[rep_idx]
    axes[2].set_title(f"Otsu (t={t_rep:.3f})  Dice={d_otsu:.3f}", fontsize=9)
    axes[2].axis("off")

    bar_colors = ["steelblue", "seagreen" if delta >= 0 else "tomato"]
    axes[3].bar(
        ["Fixed threshold\n+ CC", "Otsu\n+ CC"],
        [baseline_dice, new_dice],
        color=bar_colors,
    )
    axes[3].set_ylim(0, max(1.0, baseline_dice + 0.05, new_dice + 0.05))
    axes[3].set_ylabel("Mean Dice (all slices)")
    axes[3].set_title("Global comparison", fontsize=9)
    for x_pos, val in enumerate([baseline_dice, new_dice]):
        axes[3].text(x_pos, val + 0.01, f"{val:.4f}", ha="center", fontsize=8)

    info = pack_info()
    fig.suptitle(
        f"Day 2 challenge — Otsu adaptive thresholding  |  "
        f"representative slice {rep_idx}  |  "
        f"mean Dice: {baseline_dice:.4f} → {new_dice:.4f}  (Δ {delta:+.4f})",
        fontsize=9,
    )
    fig.tight_layout()

    fig_dir = BASE / "outputs" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    fig_path = fig_dir / "challenge_comparison.png"
    fig.savefig(fig_path, dpi=120, bbox_inches="tight")
    plt.close(fig)

    # ---- Comparison metrics JSON ----
    comparison = {
        "baseline_dice": round(baseline_dice, 4),
        "new_dice": round(new_dice, 4),
        "delta": round(delta, 4),
        "change_description": CHANGE_DESCRIPTION,
        "fixed_threshold": threshold,
        "otsu_thresholds_per_slice": otsu_thresholds,
        "n_slices": n,
        "representative_slice_idx": rep_idx,
    }

    metrics_dir = BASE / "outputs" / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    (metrics_dir / "challenge_comparison.json").write_text(
        json.dumps(comparison, indent=2), encoding="utf-8"
    )

    # ---- Report ----
    otsu_mean = float(np.mean(otsu_thresholds))
    otsu_std = float(np.std(otsu_thresholds))

    if delta > 0.001:
        outcome = "improved"
        interpretation = (
            f"Per-slice Otsu thresholding outperformed the fixed threshold. "
            f"The mean Dice improved by {delta:+.4f}, confirming that per-slice "
            f"intensity calibration addresses the sensitivity identified in the "
            f"Day 1 error analysis. The Otsu thresholds varied across slices "
            f"(mean {otsu_mean:.3f} ± {otsu_std:.3f}), showing that no single fixed "
            f"value is optimal for all slices in this pack."
        )
    elif delta < -0.001:
        outcome = "degraded"
        interpretation = (
            f"Per-slice Otsu thresholding did not outperform the fixed threshold "
            f"on this pack (Δ = {delta:+.4f}). The Otsu thresholds varied "
            f"(mean {otsu_mean:.3f} ± {otsu_std:.3f}); on slices with poorly "
            f"separated intensity modes, Otsu can set a threshold that includes "
            f"too much background or misses sparse tumour pixels. This is a valid, "
            f"informative finding: the assumption that intensity histograms are "
            f"bimodal does not hold uniformly across this dataset."
        )
    else:
        outcome = "left unchanged"
        interpretation = (
            f"Otsu thresholding had negligible effect on mean Dice (Δ = {delta:+.4f}). "
            f"The per-slice Otsu thresholds (mean {otsu_mean:.3f} ± {otsu_std:.3f}) "
            f"were close to the fixed threshold ({threshold}) on most slices, so the "
            f"two methods produce nearly identical predictions. This suggests either "
            f"that the fixed threshold was already well-calibrated for this pack, or "
            f"that the intensity histograms are bimodal with a consistent separation "
            f"point across slices."
        )

    report = f"""# Adapt Pipeline — Day 2 Challenge

Dataset: {info.get("dataset", "?")}
Modality: {info.get("modality", "?")}
Slices evaluated: {n}

---

## Change Made

**{CHANGE_DESCRIPTION}**

Both pipelines include the largest-CC post-processing step from Day 1.
The only variable is how the threshold is selected:

- **Baseline**: fixed threshold t = {threshold} (applied to every slice)
- **Day 2**: per-slice Otsu threshold computed from the intensity histogram

---

## Motivation

The Day 1 error analysis (Stage 04) identified that the fixed threshold was
sensitive to slice-level intensity variation — the Dice gap between the best
and worst slice was large.  Otsu's method addresses this by finding the
optimal threshold for each slice independently, removing the assumption that
a single global constant calibrates correctly for all slices.

Reference: Otsu, N. (1979). A threshold selection method from gray-level
histograms. IEEE Transactions on Systems, Man, and Cybernetics, 9(1), 62–66.

---

## Results

| Pipeline | Mean Dice |
|---|---|
| Fixed threshold (t={threshold}) + CC | {baseline_dice:.4f} |
| Otsu per-slice + CC | {new_dice:.4f} |
| Delta | {delta:+.4f} |

Otsu threshold statistics across {n} slices:
- Mean: {otsu_mean:.4f}
- Std:  {otsu_std:.4f}
- Min:  {min(otsu_thresholds):.4f}
- Max:  {max(otsu_thresholds):.4f}

See: `outputs/figures/challenge_comparison.png`
Representative slice: {rep_idx}
(selected as the slice where the two methods differed most)

---

## Interpretation

The Day 2 adaptation {outcome} the mean Dice score.

{interpretation}

---

## What to Take Away

1. **Adaptive thresholding is not always better.** Otsu's method makes an
   assumption (bimodal histogram) that may not hold for every slice in a
   medical image dataset.  The empirical comparison is the only reliable judge.

2. **Fair comparisons require controlled conditions.** Both pipelines here use
   the same CC post-processing step, the same slices, and the same GT masks.
   The only variable is the threshold selection method — that is what we are
   measuring.

3. **Per-slice statistics are informative.** Reporting the distribution of
   Otsu thresholds (mean ± std) tells us whether the dataset has consistent
   or variable intensity calibration — information that a fixed threshold
   cannot reveal.

4. **Next steps.** If performance is still limited, the next candidate
   improvements are: (a) a learned classifier that uses local texture features
   rather than global intensity, (b) 3-D context (adjacent slices), or (c)
   a stronger spatial prior (morphological operations, atlas-based priors).
"""

    report_path = BASE / "reports" / "adapt_pipeline.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    # ---- Status JSON ----
    status = {
        "status": "ok",
        "changes_summary": CHANGE_DESCRIPTION,
        "baseline_dice": round(baseline_dice, 4),
        "new_dice": round(new_dice, 4),
        "delta": round(delta, 4),
        "n_slices": n,
    }

    status_path = BASE / "outputs" / "status" / "stage_08_adapt_pipeline.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")

    direction = "↑ improved" if delta > 0.001 else ("↓ degraded" if delta < -0.001 else "→ unchanged")
    print("Day 2 adaptation complete.")
    print(f"  Method           : Otsu adaptive thresholding + largest-CC")
    print(f"  Baseline Dice    : {baseline_dice:.4f}  (fixed t={threshold} + CC)")
    print(f"  New Dice         : {new_dice:.4f}  {direction}")
    print(f"  Delta            : {delta:+.4f}")
    print(f"  Otsu thresholds  : mean={otsu_mean:.4f} ± {otsu_std:.4f}")
    print("Next step: make translation-memo")


if __name__ == "__main__":
    main()
