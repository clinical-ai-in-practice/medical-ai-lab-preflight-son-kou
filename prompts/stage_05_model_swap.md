# Stage 05 — Model Swap (Controlled Change)

## Goal
Test whether a single, well-motivated change to the baseline improves
the mean Dice — and understand *why* it helped or hurt.

## What to ask Claude Code

> "Run `make model-swap`. Then read `reports/model_swap.md` and look at
> `outputs/figures/model_swap_comparison.png`. Explain:
> - what the largest connected component (largest-CC) post-processing step does
> - which slice was chosen as the representative and why
> - whether the change improved, degraded, or left Dice unchanged
> - what that outcome tells us about the spatial structure of tumours in this pack"

## What this stage produces

| Artifact | Description |
|---|---|
| `outputs/figures/model_swap_comparison.png` | 4-panel figure: GT / baseline prediction / CC prediction / bar chart |
| `outputs/metrics/model_swap_comparison.json` | Baseline dice, new dice, delta, description |
| `reports/model_swap.md` | Written comparison with rationale and takeaways |
| `outputs/status/stage_05_model_swap.json` | `{"status":"ok","baseline_dice":…,"new_dice":…,"delta":…}` |

## The controlled change

**Largest connected component filtering:** after thresholding, only the single
largest connected region of positive pixels is kept; all smaller isolated blobs
are discarded.

This tests the assumption: *"the target tumour region is one spatially connected
structure."* If true, removing small scattered predictions should help. If the
tumours are naturally fragmented, it may hurt.

## Check

```bash
make model-swap
# Prints: baseline Dice, new Dice, and direction (↑ improved / ↓ degraded / → unchanged)
```

## Discussion questions

- Did the assumption "tumour is one connected region" hold for this dataset?
- If the metric degraded, does that mean the change was a bad idea?
- How would you test this assumption more rigorously on a larger dataset?
- What other post-processing steps might be worth testing on Day 2?

## What comes next

Stage 06 assembles all Day 1 results into a single summary report.
