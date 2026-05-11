# Mission 5 — Design the Next Study (Part 2): Implement and Measure

## What this mission is about

Now you execute the plan. The goal is to implement the proposed change from
`reports/challenge_plan.md` and measure the outcome honestly against the
Day 1 baseline. The plan you wrote before is the test: did the experiment
match the intent?

---

## Prompt Principle: Ask for comparison, not just generation

A prompt that says "implement the change and measure it" produces a number.
A prompt that says "compare against the baseline using the same metric, same
data split, and same evaluation protocol — and explain any deviation from
the plan" produces a scientific result. The comparison instruction is not
optional.

---

## Layer A — Base Prompt

> I need to implement the Day 2 study plan from `reports/challenge_plan.md`
> and measure whether it achieved what was planned.
>
> Please do the following:
>
> 1. Read `reports/challenge_plan.md`. Summarize the proposed change and the
>    success criterion I set before running the experiment.
>
> 2. Implement the proposed change in `scripts/adapt_pipeline.py`.
>    - Use the same random seed (42) as the baseline
>    - Use the same validation split
>    - Compute Dice on the same metric as before
>
> 3. Run the evaluation and report:
>    - The Day 1 baseline Dice (from `outputs/metrics/val_metrics.json`)
>    - The Day 2 result Dice
>    - The delta (improvement or regression)
>    - Whether the pre-specified success criterion was met
>
> 4. Save a comparison figure to `outputs/figures/challenge_comparison.png`.
>
> 5. Write comparison metrics to `outputs/metrics/challenge_comparison.json`:
>    `{"baseline_dice": X, "new_dice": Y, "delta": Z, "change_description": "..."}`
>
> 6. Write an adaptation report to `reports/adapt_pipeline.md` with:
>    - What was implemented (brief description)
>    - The numerical result
>    - Whether the pre-specified success criterion was met (yes/no/partially)
>    - If the result differs from the plan, explain why
>
> 7. Write a status file to `outputs/status/stage_08_adapt_pipeline.json`:
>    `{"status": "ok", "changes_summary": "...", "baseline_dice": X, "new_dice": Y, "delta": Z}`
>
> Do not revise the success criterion retroactively. If it was not met, say so.

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `outputs/figures/challenge_comparison.png` | Before/after Day 1 vs Day 2 comparison figure |
| `outputs/metrics/challenge_comparison.json` | `{"baseline_dice": X, "new_dice": Y, "delta": Z, "change_description": "..."}` |
| `reports/adapt_pipeline.md` | Implementation description, result, plan vs outcome assessment |
| `outputs/status/stage_08_adapt_pipeline.json` | `{"status": "ok", "changes_summary": "...", "baseline_dice": X, "new_dice": Y, "delta": Z}` |

---

## Layer B — Reflection Prompt

> Compare `reports/challenge_plan.md` (the plan) with `reports/adapt_pipeline.md` (the outcome).
>
> Answer these questions as if writing a **methods section and results discussion** for a paper:
>
> - Was the implementation faithful to the plan? What changed and why?
> - Was the success criterion met? If partially, what was achieved and what was not?
> - What does this result tell you about the original hypothesis from Mission 3?
> - If the result was negative: does that mean the hypothesis was wrong, or that the
>   implementation did not adequately test it?
> - What would you report to a co-author who invested in this direction?

---

## Layer C — Exploration Challenge

> Investigate the result more deeply by running a sensitivity analysis:
>
> - Try two small variations on the Day 2 implementation (e.g., different threshold,
>   different preprocessing step, different number of training iterations).
> - Save results to `outputs/metrics/day2_sensitivity.json` as a list of
>   `[{"variation": "...", "dice": X}, ...]`.
> - In `reports/adapt_pipeline.md`, add a `## Sensitivity Analysis` section
>   discussing how stable the result is.
>
> *Why this matters: a single result can be a lucky seed. Sensitivity analysis
> tests whether the conclusion holds across small variations.*

---

## Discussion questions

- Why does the prompt say "do not revise the success criterion retroactively"?
  What is the risk of changing the goalposts after seeing the result?
- What does it mean if the adaptation improved Dice but did not meet the
  pre-specified success criterion?
- How would you report a negative result in a way that is still scientifically useful?
