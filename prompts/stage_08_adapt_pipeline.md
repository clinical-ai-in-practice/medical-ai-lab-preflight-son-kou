# Stage 08 — Adapt Pipeline (Day 2 Challenge)
## Mission 5: Implement and Measure

## Goal

Implement the adaptation described in `reports/challenge_plan.md`:
per-slice Otsu adaptive thresholding combined with the largest-CC post-processing step
from Day 1. Measure the result against the Day 1 baseline with the same metric.

The key scientific question is whether your Day 2 hypothesis holds up under measurement.
A negative result reported honestly is as valuable as a positive one.

## The Day 2 change

**Per-slice Otsu thresholding:** for each slice, compute the threshold that maximises
inter-class variance between background and foreground intensity modes
(`skimage.filters.threshold_otsu`), then apply it as the binary decision boundary.
The largest-CC step from Day 1 is applied to both the baseline and the Day 2 predictions
to ensure a fair comparison.

## Layer A — Base prompt

> "Run `make adapt-pipeline`. Then open `reports/adapt_pipeline.md` and look at
> `outputs/figures/challenge_comparison.png`. Explain:
> - what Otsu's method does differently from the fixed threshold used in Day 1
> - what the per-slice threshold statistics (mean ± std) tell us about this dataset's
>   intensity variability across slices
> - whether the Day 2 adaptation improved, degraded, or left Dice unchanged
> - whether the outcome is consistent with the plan we wrote in Stage 07
> - what that outcome tells us about the intensity distribution assumptions in this pack"

## What this stage produces

| Artifact | Description |
|---|---|
| `outputs/figures/challenge_comparison.png` | 4-panel: GT / fixed threshold / Otsu / bar chart |
| `outputs/metrics/challenge_comparison.json` | `baseline_dice`, `new_dice`, `delta`, `change_description`, `otsu_thresholds_per_slice` |
| `reports/adapt_pipeline.md` | Written comparison with interpretation and scientific takeaway |
| `outputs/status/stage_08_adapt_pipeline.json` | `{"status":"ok","changes_summary":"...","baseline_dice":…,"new_dice":…,"delta":…}` |

## Files

**Allowed to edit:** `scripts/adapt_pipeline.py`, `reports/adapt_pipeline.md`

**Protected — do not modify:** `outputs/metrics/challenge_comparison.json` (written by the script),
`reports/challenge_plan.md` (written in Stage 07 — do not retroactively change the plan),
`tests/`, `artifacts/schema.json`, `prompts/`

## Check

```bash
make adapt-pipeline
# Prints: baseline Dice, new Dice, direction (↑ improved / ↓ degraded / → unchanged)
# Prints: Otsu threshold statistics (mean ± std across slices)
```

**What to inspect manually:**
- Open `outputs/figures/challenge_comparison.png` — does the Otsu prediction look visually different?
  Does it look more or less accurate than the fixed-threshold prediction?
- Check `outputs/metrics/challenge_comparison.json` — does the `delta` match the direction
  shown in the bar chart?
- Compare the actual outcome to the prediction in `reports/challenge_plan.md` — did the experiment confirm or refute the plan?

## Layer B — Reflection prompt

After reviewing the result, ask Claude:

> "Compare the Day 2 outcome to the Stage 07 plan:
> - Did Otsu's method generalise better across slices with different intensity distributions,
>   as the plan predicted? What does the per-slice threshold variation tell you?
> - If the result degraded, does that refute the hypothesis that intensity variability
>   was the problem — or does it suggest a different problem?
> - Add a section called '## Comparison to plan' to `reports/adapt_pipeline.md`
>   that states: (a) what the plan predicted, (b) what actually happened, and (c) what you conclude."

## Layer C — What you can customize

Ask Claude: "What would the comparison look like if we evaluated both pipelines *without*
the CC post-processing step?" This isolates the effect of Otsu alone, separate from the CC
effect. It does not require changing any committed outputs — just ask Claude to reason through it analytically.

## Discussion questions

- Did Otsu's method generalise better across slices? What does the variance in per-slice
  thresholds tell you about the intensity distribution of this dataset?
- If the bimodal-histogram assumption fails on some slices, should you report the aggregate
  Dice or a per-slice breakdown? What is more scientifically honest?
- Both pipelines use the CC post-processing step. How would the comparison look if you
  also evaluated without CC filtering? Does the CC step mask the effect of the threshold change?

## What comes next

Stage 09 assembles the final clinical translation memo using all Day 1 and Day 2 results.
This is the capstone artifact of the lab.
