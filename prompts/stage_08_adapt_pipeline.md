# Stage 08 — Adapt Pipeline (Day 2 Challenge)

## Goal
Implement the adaptation described in `reports/challenge_plan.md`:
per-slice Otsu adaptive thresholding combined with the largest-CC
post-processing step from Day 1.

## What to ask Claude Code

> "Run `make adapt-pipeline`. Then open `reports/adapt_pipeline.md` and look
> at `outputs/figures/challenge_comparison.png`. Explain:
> - what Otsu's method does differently from the fixed threshold
> - what the per-slice threshold statistics tell us about this dataset
> - whether the Day 2 adaptation improved, degraded, or left Dice unchanged
> - what that outcome tells us about the intensity distributions in this pack"

## What this stage produces

| Artifact | Description |
|---|---|
| `outputs/figures/challenge_comparison.png` | 4-panel: GT / fixed threshold / Otsu / bar chart |
| `outputs/metrics/challenge_comparison.json` | `baseline_dice`, `new_dice`, `delta`, `change_description`, `otsu_thresholds_per_slice` |
| `reports/adapt_pipeline.md` | Written comparison with interpretation and takeaways |
| `outputs/status/stage_08_adapt_pipeline.json` | `{"status":"ok","changes_summary":"...","baseline_dice":…,"new_dice":…,"delta":…}` |

## The Day 2 change

**Per-slice Otsu thresholding:** for each slice, compute the threshold that
maximises inter-class variance between the background and foreground intensity
modes (`skimage.filters.threshold_otsu`), then apply it as the binary decision
boundary.  The largest-CC post-processing step from Day 1 is applied to both
the baseline and the Day 2 predictions for a fair comparison.

## Check

```bash
make adapt-pipeline
# Prints: baseline Dice, new Dice, direction (↑ improved / ↓ degraded / → unchanged)
# Prints: Otsu threshold statistics (mean ± std across slices)
```

## Discussion questions

- Did Otsu's method generalise better across slices with different intensity
  distributions? What does the per-slice threshold variation tell you?
- If the result degraded, what does that say about the bimodal-histogram
  assumption on this dataset?
- Both pipelines here include the CC post-processing step. How would the
  comparison look if you also evaluated without CC filtering?
- What would be your next candidate improvement after this experiment?

## What comes next

Stage 09 assembles a clinical translation memo using all Day 1 and Day 2 results.
