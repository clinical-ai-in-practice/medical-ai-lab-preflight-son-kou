# Day 2 Challenge Plan

Dataset: ?
Modality: FLAIR (channel 3), per-slice normalised to [0, 255]
Slices: 10

---

## Day 1 Results Summary

| Stage | Result |
|---|---|
| Baseline threshold | 0.5 |
| Baseline mean Dice | 0.5741 |
| After largest-CC post-processing | 0.5917  (Δ +0.0176) |
| Best slice (slice 3) | Dice = 0.8697 |
| Worst slice (slice 9) | Dice = 0.0437 |

---

## Identified Weakness

The Day 1 error analysis revealed that the fixed threshold (t = 0.5) is
**sensitive to slice-level intensity variation**.  Slices where tumour pixels happen
to be brighter than the population mean perform well; slices where the intensity
distributions of tumour and background overlap perform poorly (Dice gap of
0.8260).

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
histogram rather than applying the fixed constant t = 0.5.

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

  Baseline: fixed threshold = 0.5
  Day 2:    Otsu per-slice threshold + largest-CC filter

---

## Expected New Artifacts

| Artifact | Location | Description |
|---|---|---|
| `challenge_comparison.png` | `outputs/figures/` | 4-panel: GT / baseline / Otsu / bar chart |
| `challenge_comparison.json` | `outputs/metrics/` | baseline_dice, new_dice, delta, description |
| `adapt_pipeline.md` | `reports/` | Written comparison with rationale and takeaways |
| `stage_08_adapt_pipeline.json` | `outputs/status/` | `{"status":"ok","changes_summary":"..."}` |

---

## Success Criteria

- `new_dice` is computed fairly: same 10 slices, same GT masks, only the
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

3. **Comparison confound.** The baseline Dice reported in Day 1 (0.5741)
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
