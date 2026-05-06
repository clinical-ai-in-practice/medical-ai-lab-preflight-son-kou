# Stage 06 — Pack Day 1 Report
## Mission 4: Close Day 1

## Goal

Assemble all Day 1 results into a single summary document that you can review, present,
and push as your Day 1 deliverable.

This is not just a formatting step. Reading your own summary back is a calibration exercise:
does the written record accurately represent what you actually found?
If the numbers in the summary do not match the metrics files, something went wrong.

## Layer A — Base prompt

> "Run `make pack-report`. Then open `reports/day1_summary.md`.
> Read through the assembled summary and tell me:
> - whether all five sections are present (environment, dataset, baseline, error analysis, model swap)
> - whether the numbers are consistent with what was computed in stages 03–05
> - what the three most important scientific findings from Day 1 are
> - what the single most honest open question for Day 2 is
> Does the summary accurately represent what we found, including any disappointing results?"

## What this stage produces

| Artifact | Description |
|---|---|
| `reports/day1_summary.md` | Full Day 1 summary: environment, dataset, baseline, error analysis, model swap |
| `outputs/status/stage_06_pack_report.json` | `{"status":"ok","sections":[...],"baseline_dice":…,"model_swap_delta":…}` |

## Files

**Allowed to edit:** `scripts/pack_report.py`, `reports/day1_summary.md`

**Protected — do not modify:** `tests/`, `artifacts/schema.json`, `prompts/`,
all prior `outputs/metrics/` files (do not alter to improve the summary)

## Check

```bash
make pack-report
# Prints: list of found sections and path to day1_summary.md

# Review the summary
cat reports/day1_summary.md

# Review the full dashboard
make dashboard
```

**What to inspect manually:**
- Read the `# Day 1 Summary` header — is it present? (grading requires it)
- Check that Dice values in the summary match `outputs/metrics/val_metrics.json` and `model_swap_comparison.json`
- Confirm the summary is longer than 400 characters — one-sentence stubs will fail the autograding check

## Layer B — Reflection prompt

After reviewing the summary, ask Claude:

> "Looking at the Day 1 summary as a whole:
> - If a clinician with no programming background read this document, what would they conclude
>   about the state of this prototype?
> - Are there any results in the summary that are presented more positively than the numbers justify?
> - Add a final paragraph to `reports/day1_summary.md` under a heading '## What Day 2 must address'
>   that states the one thing you most need to learn or test on Day 2, and why."

## Layer C — What you can customize

Before pushing, read the summary aloud to yourself (or ask Claude to read it back to you).
Does the description of the baseline match your understanding from Stage 03?
If anything sounds wrong or unclear, ask Claude to revise that section before committing.
This is your report — it should reflect your understanding, not Claude's default output.

## Checkpoint commit

Once you are satisfied with `reports/day1_summary.md`, commit and push:

```bash
git add outputs/ reports/
git commit -m "Day 1 complete: baseline, error analysis, model swap"
git push
```

Grading CI will run `make test` and check that all required status files, figures, metrics, and reports are present.

## Discussion questions

- Does the summary honestly represent what you found, including results that were
  weaker than expected?
- If a clinical collaborator read only this document, what follow-up question would
  they ask first?
- What would you do differently in Day 1 if you were to run this experiment again?

## What comes next

Stage 07 opens Day 2 with a challenge plan. Before writing any code, you will produce
a written plan for the Day 2 experiment grounded in Day 1 findings.
