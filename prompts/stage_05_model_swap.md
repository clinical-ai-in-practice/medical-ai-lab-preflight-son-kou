# Mission 4 — Improve With Intent (Part 1): Controlled Change

## What this mission is about

One controlled change with honest reporting is more scientifically valuable
than three unjustified tweaks. This mission tests whether the hypothesis you
formed in Mission 3 holds up: you change exactly one thing, hold everything
else constant, and measure the outcome with the same metric.

---

## Prompt Principle: Control variable framing

Specifying "change only X, hold everything else constant" is not
micromanagement — it is experimental design. A prompt that names the control
variable produces a comparable result. One that does not produces uninterpretable
noise. Good prompting is good science communication.

---

## Layer A — Base Prompt

> Based on the error analysis in `reports/error_analysis.md`, I want to test
> one targeted improvement to the baseline segmentation model.
>
> Please do the following:
>
> 1. Read `reports/error_analysis.md` and remind me of the hypothesis:
>    what was identified as the dominant failure mode?
>
> 2. Propose one specific, well-motivated change that directly addresses that
>    failure mode. This might be:
>    - A different model architecture
>    - A change to preprocessing (normalization, augmentation)
>    - A change to the threshold or post-processing
>    - A different loss function
>    Tell me what the change is and why it follows from the hypothesis.
>
> 3. Implement the change in `scripts/model_swap.py`. Keep everything else
>    the same as the baseline (same data split, same random seed 42, same metric).
>
> 4. Run the evaluation and compare:
>    - Baseline Dice (from `outputs/metrics/val_metrics.json`)
>    - New Dice after the change
>    - Delta (new minus baseline)
>
> 5. Save a comparison figure to `outputs/figures/model_swap_comparison.png`
>    showing the before/after results visually.
>
> 6. Write comparison metrics to `outputs/metrics/model_swap_comparison.json`:
>    `{"baseline_dice": X, "new_dice": Y, "delta": Z, "change_description": "..."}`
>
> 7. Write a report to `reports/model_swap.md` explaining:
>    - What change was made and why
>    - The numerical result
>    - Whether the hypothesis was supported or not
>
> 8. Write a status file to `outputs/status/stage_05_model_swap.json`:
>    `{"status": "ok", "baseline_dice": X, "new_dice": Y, "delta": Z, "change_description": "..."}`
>
> Report the result honestly. A negative delta is a valid scientific result.

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `outputs/figures/model_swap_comparison.png` | Before/after comparison figure |
| `outputs/metrics/model_swap_comparison.json` | `{"baseline_dice": X, "new_dice": Y, "delta": Z, "change_description": "..."}` |
| `reports/model_swap.md` | Change description, result, hypothesis assessment |
| `outputs/status/stage_05_model_swap.json` | `{"status": "ok", "baseline_dice": X, "new_dice": Y, "delta": Z, "change_description": "..."}` |

---

## Layer B — Reflection Prompt

> Look at the result in `outputs/metrics/model_swap_comparison.json`
> and `reports/model_swap.md`.
>
> Now act as a **peer reviewer** of this experiment:
> - Was this a fair controlled experiment? What else changed beyond the intended variable?
> - Did the result support or contradict the hypothesis from Mission 3?
> - If the delta was positive: is this a meaningful improvement, or within noise?
>   How would you know?
> - If the delta was negative or zero: what does that tell you about the hypothesis?
>   What would you try next?
> - What would a convincing validation of this result look like on more data?

---

## Layer C — Exploration Challenge

> Try one additional variation — a second, different change to the same baseline:
>
> - Choose a different improvement direction than the one already tested.
> - Save the result to `outputs/metrics/model_swap_v2.json` (same schema as above).
> - In `reports/model_swap.md`, add a section comparing both variations.
>
> *Important: do NOT overwrite `model_swap_comparison.json` — that is the canonical
> Mission 4 result. The exploration files are supplementary.*
>
> Which change produced a better result? Does the combination of both changes
> produce better or worse results than either alone?

---

## Discussion questions

- Why does the prompt insist on using the same random seed and data split as the baseline?
- What does a "negative delta" tell you scientifically? Is it a failure?
- The prompt says "report the result honestly." Why does this instruction need to be explicit?
  What would dishonest reporting look like in this context?
