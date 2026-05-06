# Stage 04 — Error Analysis
## Mission 3: Investigate Failure

## Goal

Understand where the baseline segmentation succeeds and where it fails —
slice by slice, error type by error type — and produce figures and a report
that make the error pattern concrete and interpretable.

Blind improvement without error understanding is engineering guesswork, not science.
The hypothesis you form here determines whether Mission 4 is a valid experiment.

## Layer A — Base prompt

> "Run `make error-analysis`. Then open `reports/error_analysis.md`,
> `outputs/figures/error_analysis_best.png`, and `outputs/figures/error_analysis_worst.png`.
> Explain to me in plain language:
> - which slice was the best case and why the threshold worked there
> - which slice was the worst case and why the threshold failed there
> - what the error map colours mean (TP/FP/FN)
> - what this error pattern suggests we should try in Stage 05"

## What this stage produces

| Artifact | Description |
|---|---|
| `outputs/figures/error_analysis_best.png` | 4-panel figure: image / GT mask / prediction / error map |
| `outputs/figures/error_analysis_worst.png` | Same layout for the worst-case slice |
| `reports/error_analysis.md` | Written analysis with TP/FP/FN counts and a failure hypothesis |
| `outputs/status/stage_04_error_analysis.json` | `{"status":"ok","best_case":{...},"worst_case":{...}}` |

## Files

**Allowed to edit:** `scripts/error_analysis.py`, `reports/error_analysis.md`

**Protected — do not modify:** `outputs/status/stage_04_error_analysis.json` (written by the script),
`tests/`, `artifacts/schema.json`, `prompts/`

## Check

```bash
make error-analysis
# Prints: best-case slice index and Dice, worst-case slice index and Dice
# Then open both PNG figures and read the report
```

**What to inspect manually:**
- Open both figures side by side — can you see a visual pattern that explains the gap between best and worst case?
- Read `reports/error_analysis.md` — does the written interpretation match what you see in the figures?
  If the report says "FP dominates" but the error map shows FN in red, that is a contradiction worth raising with Claude.

## Layer B — Reflection prompt

After reviewing the figures and the report, ask Claude:

> "Based on the error maps for the best and worst case:
> - What is the dominant error type — false positives or false negatives?
> - Does the spatial distribution of errors suggest a problem with the threshold, the mask shape, or something else?
> - Write a one-paragraph hypothesis at the end of `reports/error_analysis.md` under a heading called
>   '## Hypothesis for Stage 05'. The hypothesis should state: what you think the problem is,
>   what you will test, and what a positive result would look like."

## Layer C — What you can customize

Ask Claude to identify a specific slice index that is neither the best nor the worst —
a "middle case." Ask it to explain why this slice performed as it did relative to the other two.
Does the middle case support or challenge your hypothesis?

## Discussion questions

- Is the Dice gap between best and worst case large enough to be clinically meaningful,
  or is it within the range of sampling noise for a 10-slice dataset?
- What type of error dominates in the worst case — false positives or false negatives?
  Why does the answer matter for which post-processing step to try next?
- If you had no quantitative metric and only the figures, could you still identify which
  slice was best and which was worst? What does this tell you about visual inspection vs. metrics?

## What comes next

Stage 05 tests one specific, well-motivated change to address the dominant error pattern
you identified here. The hypothesis written in this stage is what makes Stage 05 a valid experiment.
