# Mission 3 — Investigate Failure

## What this mission is about

Blind improvement without error understanding is engineering guesswork, not science.
Before you change anything about the model, you need to understand *where* and *why*
it fails — slice by slice, case by case. The hypothesis you form here determines
whether Mission 4 is a valid controlled experiment or random tweaking.

---

## Prompt Principle: Observation → hypothesis

Asking Claude to first observe (rank predictions, visualize failures) and then form
a hypothesis (what is the dominant failure mode?) forces it to ground its explanation
in evidence. A prompt that asks for a hypothesis *before* evidence invites speculation.
Always sequence: look first, explain second.

---

## Layer A — Base Prompt

> I need to understand where my baseline segmentation model is failing.
>
> Please do the following:
>
> 1. Load the baseline model results. Look at `outputs/metrics/val_metrics.json`
>    and `outputs/status/stage_03_train_baseline.json` to understand what was trained.
>    Examine `scripts/error_analysis.py` — create or complete it as needed.
>
> 2. Run per-slice Dice evaluation across all validation slices.
>    Identify the best-performing slice and the worst-performing slice.
>
> 3. Create error visualizations:
>    - One figure for the best-case prediction: image, ground truth, prediction, and error map
>      (where TP=green, FP=red, FN=blue)
>    - One figure for the worst-case prediction: same layout
>    - Save to `outputs/figures/error_analysis_best.png` and `outputs/figures/error_analysis_worst.png`
>
> 4. Write an error analysis report to `reports/error_analysis.md` with:
>    - Best-case and worst-case Dice scores
>    - What the error patterns look like visually (describe what you see in the figures)
>    - Your hypothesis: what is the dominant failure mode?
>    - Your prediction: what kind of change would most likely improve the worst cases?
>
> 5. Write a status file to `outputs/status/stage_04_error_analysis.json` with:
>    `{"status": "ok", "best_case": {"slice_idx": N, "dice": X}, "worst_case": {"slice_idx": N, "dice": X}, "n_slices": N}`
>
> Be specific in the error report. "The model does poorly on some slices" is not a hypothesis.
> A hypothesis is: "The model over-segments in slices with low contrast at the boundary."

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `outputs/figures/error_analysis_best.png` | Best-case: image, GT, prediction, error map |
| `outputs/figures/error_analysis_worst.png` | Worst-case: image, GT, prediction, error map |
| `reports/error_analysis.md` | Best/worst Dice, visual description, failure hypothesis |
| `outputs/status/stage_04_error_analysis.json` | `{"status": "ok", "best_case": {...}, "worst_case": {...}, "n_slices": N}` |

---

## Layer B — Reflection Prompt

> Read `reports/error_analysis.md` and look at both error figures.
>
> Now put on two hats and give me two separate assessments:
>
> **As the developer:** What one code or algorithm change would you try first, based on the
> error patterns? Be specific about what you would change and why you think it would help.
>
> **As the critic:** What weaknesses do you see in your own error analysis?
> - Are there failure patterns you might be missing because of how the metric was computed?
> - Is your hypothesis testable? How would you know if your proposed fix worked?
> - What evidence would change your hypothesis?

---

## Layer C — Exploration Challenge

> Extend the error analysis to find additional patterns:
>
> - Compute the Dice score distribution across all slices and plot a histogram.
>   Save to `outputs/figures/dice_distribution.png`.
> - Are the worst-case slices clustered (e.g., all from the same patient or same
>   region), or random? If you can tell from the data, note it.
> - What is the 10th percentile Dice score? How does it compare to the mean?
>
> Update `reports/error_analysis.md` with these distributional findings.
>
> *Why this matters: mean Dice hides tail failures. In clinical AI, worst-case
> performance matters as much as average performance.*

---

## Discussion questions

- Why does the prompt ask Claude to "describe what you see in the figures" rather
  than just create the figures?
- What is the difference between a description ("the model does poorly in some regions")
  and a hypothesis ("the model fails when the boundary contrast is below X")?
- How would you test whether your hypothesis is correct in Mission 4?
