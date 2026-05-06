"""
Stage 07 — Challenge Plan

Reads Day 1 artifacts and produces a concrete written plan for the Day 2
challenge: replacing the fixed intensity threshold with per-slice adaptive
thresholding (Otsu's method).

No pipeline code is written here — this stage is planning only.

Inputs (must exist):
  outputs/metrics/val_metrics.json
  outputs/metrics/model_swap_comparison.json
  outputs/status/stage_04_error_analysis.json

Outputs:
  reports/challenge_plan.md
  outputs/status/stage_07_challenge_plan.json
"""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import pack_info

BASE = Path(__file__).resolve().parents[1]
VAL_METRICS = BASE / "outputs" / "metrics" / "val_metrics.json"
SWAP_METRICS = BASE / "outputs" / "metrics" / "model_swap_comparison.json"
ERROR_STATUS = BASE / "outputs" / "status" / "stage_04_error_analysis.json"


def _load(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def main() -> None:
    val = _load(VAL_METRICS)
    swap = _load(SWAP_METRICS)
    err = _load(ERROR_STATUS)
    info = pack_info()

    baseline_dice = val.get("dice", "?")
    threshold = val.get("threshold", 0.5)
    cc_dice = swap.get("new_dice", "?")
    cc_delta = swap.get("delta", "?")
    best_dice = err.get("best_case", {}).get("dice", "?")
    worst_dice = err.get("worst_case", {}).get("dice", "?")
    best_idx = err.get("best_case", {}).get("slice_idx", "?")
    worst_idx = err.get("worst_case", {}).get("slice_idx", "?")
    n_slices = val.get("n_slices", info.get("n_slices", "?"))
    dataset = info.get("dataset", "?")
    modality = info.get("modality", "?")

    # Format numbers if available
    def _fmt(v, fmt=".4f"):
        try:
            return format(float(v), fmt)
        except (TypeError, ValueError):
            return str(v)

    report = f"""# Day 2 Challenge Plan

Dataset: {dataset}
Modality: {modality}
Slices: {n_slices}

---

## Day 1 Results Summary

| Stage | Result |
|---|---|
| Baseline threshold | {threshold} |
| Baseline mean Dice | {_fmt(baseline_dice)} |
| After largest-CC post-processing | {_fmt(cc_dice)}  (Δ {_fmt(cc_delta, "+.4f")}) |
| Best slice (slice {best_idx}) | Dice = {_fmt(best_dice)} |
| Worst slice (slice {worst_idx}) | Dice = {_fmt(worst_dice)} |

---

## Identified Weakness

The Day 1 error analysis revealed that the fixed threshold (t = {threshold}) is
**sensitive to slice-level intensity variation**.  Slices where tumour pixels happen
to be brighter than the population mean perform well; slices where the intensity
distributions of tumour and background overlap perform poorly (Dice gap of
{_fmt(float(_fmt(best_dice)) - float(_fmt(worst_dice)) if best_dice != '?' and worst_dice != '?' else '?')}).

The root cause is that a single global threshold ignores per-slice differences in
brightness, contrast, and scanner gain.  A fixed constant cannot adapt to slices
where the tumour is not the brightest structure or where background tissue is
unusually bright.

The largest-CC post-processing (Stage 05) addressed the *spatial* false-positive
problem but did not address the *intensity calibration* problem — per-slice Dice
variance remained high.

---

## Proposed Day 2 Modification

**Otsu adaptive thresholding** — compute a per-slice threshold from the intensity
histogram rather than applying the fixed constant t = {threshold}.

### What it does

For each slice independently:
1. Compute the normalised intensity histogram.
2. Apply Otsu's criterion: find the threshold that maximises inter-class variance
   between the two intensity modes (background vs. foreground).
3. Use that per-slice threshold as the binary decision boundary.

This is implemented in `skimage.filters.threshold_otsu`, which is already in
`requirements.txt`.

### Why this is the right next step

- It **directly addresses the identified weakness**: intensity calibration is done
  per slice, not globally.
- It adds **zero learned parameters** — the threshold is fully determined by the
  data and is easy to inspect and audit.
- It is a **single, isolated change** to the thresholding step, which keeps the
  comparison fair (same data, same post-processing, only the threshold selection
  changes).
- It is a **well-understood clinical technique**: adaptive thresholding is widely
  used in histology and radiology preprocessing pipelines.

### Combination strategy

The adaptation will be applied *with* the largest-CC post-processing from Stage 05,
since that step was independently validated to help (or at minimum, not hurt).
The comparison will therefore be:

  Baseline: fixed threshold = {threshold}
  Day 2:    Otsu per-slice threshold + largest-CC filter

---

## Expected New Artifacts

| Artifact | Location | Description |
|---|---|---|
| `challenge_comparison.png` | `outputs/figures/` | 4-panel: GT / baseline / Otsu / bar chart |
| `challenge_comparison.json` | `outputs/metrics/` | baseline_dice, new_dice, delta, description |
| `adapt_pipeline.md` | `reports/` | Written comparison with rationale and takeaways |
| `stage_08_adapt_pipeline.json` | `outputs/status/` | `{{"status":"ok","changes_summary":"..."}}` |

---

## Success Criteria

- `new_dice` is computed fairly: same {n_slices} slices, same GT masks, only the
  threshold method changes.
- The change is **honest**: if Otsu performs worse than the fixed threshold,
  that outcome is reported and explained.
- The comparison figure clearly shows at least one representative slice where the
  per-slice threshold makes a visible difference.
- `make test` passes after Stage 08 completes.

---

## Risks and Failure Modes

1. **Otsu fails on bimodal-poor slices.** Otsu's method assumes a bimodal
   intensity histogram.  In slices where tumour pixels are very sparse, the
   histogram may be strongly unimodal and Otsu will set the threshold near the
   tail of the background distribution, producing many false positives.
   Mitigation: report per-slice thresholds; flag slices where the Otsu threshold
   is unusually low or high.

2. **Otsu threshold higher than 0.5 on bright slices.** If the majority of
   pixels are bright background, Otsu may set a high threshold that misses real
   tumour.  This would show as degraded performance relative to the fixed
   threshold on some slices.  This is a valid, instructive finding — not a bug.

3. **Comparison confound.** The baseline Dice reported in Day 1 ({_fmt(baseline_dice)})
   was computed without largest-CC post-processing.  To keep the Day 2 comparison
   clean, Stage 08 will report the *pure fixed-threshold baseline* alongside the
   *Otsu + CC* pipeline, and note the confound explicitly in the report.

---

## Implementation Sketch (for Stage 08)

```python
from skimage.filters import threshold_otsu

# Per-slice Otsu thresholding
for i in range(n):
    t_otsu = threshold_otsu(images[i])
    pred_otsu = (images[i] > t_otsu).astype(np.int32)
    pred_otsu_cc = largest_connected_component(pred_otsu)
    ...
```

This sketch is not production code — it is here to confirm the plan is
implementable before writing Stage 08.
"""

    report_path = BASE / "reports" / "challenge_plan.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    status = {
        "status": "ok",
        "proposed_change": "Per-slice Otsu adaptive thresholding + largest-CC post-processing",
        "baseline_dice": round(float(baseline_dice), 4) if baseline_dice != "?" else None,
        "identified_weakness": "Fixed threshold is sensitive to slice-level intensity variation",
        "n_slices": n_slices,
    }

    status_path = BASE / "outputs" / "status" / "stage_07_challenge_plan.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")

    print("Challenge plan written.")
    print(f"  Identified weakness : fixed threshold (t={threshold}) is intensity-sensitive")
    print(f"  Proposed Day 2 change: Otsu per-slice adaptive thresholding + largest-CC")
    print(f"  Plan saved to       : reports/challenge_plan.md")
    print("Next step: make adapt-pipeline")


if __name__ == "__main__":
    main()
