# Stage 04 — Error Analysis

## Goal
Understand where the baseline segmentation succeeds and where it fails,
and produce figures and a report that make the error pattern concrete.

## What to ask Claude Code

> "Run `make error-analysis`. Then open `reports/error_analysis.md` and
> `outputs/figures/error_analysis_best.png` and `error_analysis_worst.png`.
> Explain to me in plain language:
> - which slice was the best case and why the threshold worked there
> - which slice was the worst case and why the threshold failed there
> - what the error map colours mean (TP/FP/FN)
> - what this error pattern suggests we should try in Stage 05"

## What this stage produces

| Artifact | Description |
|---|---|
| `outputs/figures/error_analysis_best.png` | 4-panel figure: image / GT mask / prediction / error map |
| `outputs/figures/error_analysis_worst.png` | Same layout for the worst slice |
| `reports/error_analysis.md` | Written analysis with TP/FP/FN counts and reflection |
| `outputs/status/stage_04_error_analysis.json` | `{"status":"ok","best_case":{...},"worst_case":{...}}` |

## Check

```bash
make error-analysis
# Prints: best-case slice index and Dice, worst-case slice index and Dice
# Then open the two PNG figures and read the report
```

## Discussion questions

After running this stage, discuss with Claude:
- Is the Dice gap between best and worst case large or small?
- What type of error dominates in the worst case: false positives or false negatives?
- If you were to change one thing about the pipeline, what would you change first?

## What comes next

The error analysis motivates the controlled experiment in Stage 05.
Stage 05 tests whether a simple spatial post-processing step (keeping only
the largest connected component of the prediction) can address the dominant
error pattern.
