# Stage 05 — Model Swap (Controlled Change)
## Mission 4: Improve With Intent

## Goal

Test whether a single, well-motivated change to the baseline improves the mean Dice —
and understand *why* it helped or hurt.

One controlled change with honest reporting is more scientifically valuable than
multiple unjustified tweaks. The measure of success is not the direction of the result
but the quality of your reasoning about it.

## The controlled change

**Largest connected component filtering:** after thresholding, only the single
largest connected region of positive pixels is kept; all smaller isolated blobs
are discarded.

This tests the assumption from Mission 3: *"the dominant error is scattered false positives
that could be removed by enforcing spatial continuity."* If that assumption was correct,
Dice should improve. If the tumour regions are naturally fragmented, it may hurt.

## Layer A — Base prompt

> "Run `make model-swap`. Then read `reports/model_swap.md` and look at
> `outputs/figures/model_swap_comparison.png`. Explain:
> - what the largest connected component (largest-CC) post-processing step does geometrically
> - which slice was chosen as the representative and why
> - whether the change improved, degraded, or left Dice unchanged
> - what that outcome tells us about the spatial structure of tumours in this pack
> - whether the result is consistent with the hypothesis we wrote in Stage 04"

## What this stage produces

| Artifact | Description |
|---|---|
| `outputs/figures/model_swap_comparison.png` | 4-panel: GT / baseline prediction / CC prediction / bar chart |
| `outputs/metrics/model_swap_comparison.json` | `baseline_dice`, `new_dice`, `delta`, `change_description` |
| `reports/model_swap.md` | Written comparison with rationale, outcome, and scientific takeaway |
| `outputs/status/stage_05_model_swap.json` | `{"status":"ok","baseline_dice":…,"new_dice":…,"delta":…}` |

## Files

**Allowed to edit:** `scripts/model_swap.py`, `reports/model_swap.md`

**Protected — do not modify:** `outputs/metrics/model_swap_comparison.json` (written by the script),
`tests/`, `artifacts/schema.json`, `prompts/`

## Check

```bash
make model-swap
# Prints: baseline Dice, new Dice, and direction (↑ improved / ↓ degraded / → unchanged)
```

**What to inspect manually:**
- Open `outputs/figures/model_swap_comparison.png` — does the CC-filtered prediction look visually better or worse?
- Read `reports/model_swap.md` — does the written interpretation match the actual direction of the delta?
  A report that says "the change improved results" when delta is negative is a honesty violation.
- Compare the delta against your Stage 04 hypothesis — did the experiment confirm or refute it?

## Layer B — Reflection prompt

After reviewing the result, ask Claude:

> "Given the actual delta of [paste the value from model_swap_comparison.json]:
> - Was our Stage 04 hypothesis confirmed, partially confirmed, or refuted?
> - If the change degraded Dice, does that mean the change was a bad scientific idea?
>   Or does it mean the assumption was wrong for this dataset?
> - Add a section called '## Scientific interpretation' to `reports/model_swap.md`
>   that addresses these questions in 3–4 sentences."

## Layer C — What you can customize

Ask Claude: "What is the minimum connected component size below which the CC step
is removing signal rather than noise?" Then ask it to find the slice in the dataset
where CC filtering had the biggest effect (positive or negative). This deepens your
understanding of when the assumption holds.

## Discussion questions

- Did the assumption "tumour is one spatially connected region" hold for this dataset?
  What would the anatomy need to look like for it to fail systematically?
- If the metric degraded, does that make this a failed experiment?
  What is the difference between a failed experiment and a bad one?
- How would you test the CC assumption more rigorously on a larger dataset?
  What additional data would you need?

## What comes next

Stage 06 assembles all Day 1 results into a summary report. The Dice values from
this stage will appear as comparison reference points in the Day 2 challenge.
