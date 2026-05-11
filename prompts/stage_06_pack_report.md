# Mission 4 — Improve With Intent (Part 2): Assemble Day 1 Summary

## What this mission is about

A research day only counts if it is recorded. Before Day 2 begins, you need
a single coherent document that captures what was learned on Day 1: the baseline
result, the error analysis, the controlled experiment, and an honest assessment
of where things stand. This is the record a future collaborator would read.

---

## Prompt Principle: Request synthesis, not just aggregation

Asking Claude to "write a summary" without specifying what to synthesize produces
a list. Asking Claude to "draw conclusions from X, Y, Z and explain what they mean
together" produces a synthesis. The difference is the difference between a data dump
and a scientific narrative.

---

## Layer A — Base Prompt

> I need to write a comprehensive Day 1 research summary that synthesizes everything
> completed so far.
>
> Please do the following:
>
> 1. Read all the reports and metrics from today:
>    - `reports/data_notes.md` — data observations
>    - `reports/train_notes.md` — baseline training notes
>    - `reports/error_analysis.md` — error analysis and hypothesis
>    - `reports/model_swap.md` — controlled improvement result
>    - `outputs/metrics/val_metrics.json` — baseline metrics
>    - `outputs/metrics/model_swap_comparison.json` — comparison metrics
>
> 2. Write a Day 1 research summary to `reports/day1_summary.md` with these sections:
>    - `# Day 1 Summary`
>    - `## Data` — what the dataset is and its key characteristics
>    - `## Baseline` — what was trained, the baseline Dice, and what the loss curve showed
>    - `## Error Analysis` — what failure patterns were identified and the hypothesis formed
>    - `## Improvement` — what change was made, the result, and whether the hypothesis was supported
>    - `## Open Questions` — what remains uncertain and what would be worth testing on Day 2
>
> 3. Write a status file to `outputs/status/stage_06_pack_report.json`:
>    `{"status": "ok", "sections": ["Data", "Baseline", "Error Analysis", "Improvement", "Open Questions"]}`
>
> The summary should be analytical, not just descriptive. Each section should contain
> conclusions, not just facts. The "Open Questions" section should be honest about
> what did not work or what remains unexplained.

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `reports/day1_summary.md` | 5 sections minimum, analytical content, > 400 chars |
| `outputs/status/stage_06_pack_report.json` | `{"status": "ok", "sections": [...]}` |

---

## Layer B — Reflection Prompt

> Read `reports/day1_summary.md` as if you were a **supervisor** reviewing a
> student's Day 1 research log.
>
> - Is the summary analytical or just a list of events? What is missing?
> - Does the "Open Questions" section contain genuine uncertainty, or is it vague?
> - What question from Day 1 do you think is most important to answer on Day 2?
> - If you were writing this for a conference abstract, what would the one-sentence
>   finding be?

---

## Layer C — Exploration Challenge

> Add a `## Limitations` section to `reports/day1_summary.md` that addresses:
>
> - Limitations of the dataset (size, synthetic vs real, annotation quality)
> - Limitations of the baseline (architecture simplicity, training data size)
> - Limitations of the error analysis (what patterns might have been missed)
> - What conclusions from Day 1 would *not* hold on a larger or different dataset
>
> *Why this matters: in peer-reviewed research, limitations sections are taken
> seriously. Acknowledging them honestly is a sign of scientific maturity.*

---

## Discussion questions

- What is the difference between a "summary" and a "synthesis"? How do you tell them apart
  when reading the final document?
- Why does the prompt specify section names explicitly rather than letting Claude choose them?
- What is the purpose of the "Open Questions" section for Day 2 planning?
