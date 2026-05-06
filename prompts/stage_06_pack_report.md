# Stage 06 — Pack Day 1 Report

## Goal
Assemble all Day 1 results into a single summary document that you can
review, present, and push as your Day 1 deliverable.

## What to ask Claude Code

> "Run `make pack-report`. Then open `reports/day1_summary.md`.
> Read through the assembled summary and tell me:
> - whether all five sections are present
> - whether the numbers look consistent with what we computed in stages 03–05
> - what the three most important things we learned today are
> - what the most honest open question for Day 2 is"

## What this stage produces

| Artifact | Description |
|---|---|
| `reports/day1_summary.md` | Full Day 1 summary: env, dataset, baseline, error analysis, model swap |
| `outputs/status/stage_06_pack_report.json` | `{"status":"ok","sections":[...],"baseline_dice":…,"model_swap_delta":…}` |

## Check

```bash
make pack-report
# Prints: list of found sections, path to day1_summary.md

# Open the summary
cat reports/day1_summary.md

# Optional: review the full dashboard
make app
```

## Submission

Once you are satisfied with `reports/day1_summary.md`, commit and push your work:

```bash
git add outputs/ reports/
git commit -m "Day 1 complete: baseline, error analysis, model swap"
git push
```

Grading CI will run `make test` on your commit and check:
- all required status files exist with `"status": "ok"`
- all required figures exist and are non-empty
- all required metrics files have the correct schema
- all required reports are non-trivial

## Discussion questions

- Does the summary honestly represent what we found?
- Is there anything in the numbers that surprised you?
- If a clinical collaborator read this summary, what would they ask first?
