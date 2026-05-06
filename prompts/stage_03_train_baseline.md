# Stage 03 — Train Baseline
## Mission 2: Build the First Detector

## Goal

Run the smallest deterministic baseline model and record the first quantitative metric.
The goal is **not** a high Dice score. The goal is a reproducible starting point
that you understand and can explain.

Every number this stage produces is the reference point for everything that follows.
If you cannot explain the baseline, you cannot meaningfully evaluate any improvement.

## Layer A — Base prompt

> "Run `make smoke-train`. Then open `outputs/metrics/val_metrics.json`,
> `outputs/figures/loss_curve.png`, and `reports/train_notes.md`. Explain to me:
> - what algorithm was used and why it was chosen as the baseline
> - what the Dice score means in plain language — what would 0.0 look like? What would 1.0?
> - whether the loss curve looks like the training converged or is still decreasing
> - whether this Dice score is better or worse than you expected, given the data you saw in Stage 02"

## What this stage produces

| Artifact | Description |
|---|---|
| `outputs/metrics/val_metrics.json` | `{"dice": <float 0–1>}` — the primary baseline metric |
| `outputs/figures/loss_curve.png` | Training loss over iterations |
| `reports/train_notes.md` | Written summary: algorithm, Dice result, convergence, interpretation |
| `outputs/status/stage_03_train_baseline.json` | `{"status":"ok","dice":...,"n_slices":...}` |

## Files

**Allowed to edit:** `scripts/run_train.py`, `reports/train_notes.md`

**Protected — do not modify:** `outputs/metrics/val_metrics.json` (written by the script — do not edit by hand),
`tests/`, `artifacts/schema.json`, `prompts/`

## Check

```bash
make smoke-train
# Expected: prints Dice score and confirms metric files were written
# Then verify:
cat outputs/metrics/val_metrics.json          # dice key, value between 0 and 1
ls -lh outputs/figures/loss_curve.png         # should be non-empty
cat reports/train_notes.md
```

**What to inspect manually:**
- `outputs/metrics/val_metrics.json` — is the `dice` value a float between 0 and 1?
  If it is exactly 0.0 or exactly 1.0, investigate before continuing.
- `outputs/figures/loss_curve.png` — does the loss decrease and flatten, or is it erratic?
  A loss that never decreases suggests a problem with the training setup.
- `reports/train_notes.md` — does the written interpretation match the actual number?
  If the Dice is 0.15 but the report says "good performance," that is a honesty violation.

## Layer B — Reflection prompt

After reviewing the metric, loss curve, and report, ask Claude:

> "Given a Dice score of [paste the actual value here]:
> - Is this what you would expect from a simple threshold-based baseline on this dataset?
> - What is the most likely cause of the error that Dice does not capture?
> - If I had to explain this result to a clinician who had never heard of Dice score,
>   what would I say?
> Add a section called '## Clinical interpretation' to `reports/train_notes.md`
> that answers this last question in 2–3 sentences."

## Layer C — What you can customize

The baseline uses a fixed threshold. Ask Claude what happens if you change the threshold
value by a small amount — does the Dice score improve or degrade? This is not a required
change; it is a quick manual experiment to build intuition before Stage 04.

## Discussion questions

- The Dice score is computed on the teaching pack sample.
  Is this an in-sample estimate or an out-of-sample estimate? Why does the distinction matter?
- If the loss curve flattens but Dice is still low, what does that tell you about the
  relationship between the training objective and the evaluation metric?
- What would it mean if two very different models produced the same Dice score on this sample?
  Would you trust them equally?
- Why is it important to record the baseline *before* attempting any improvement?

## What comes next

Stage 04 investigates where the baseline fails — slice by slice, error type by error type.
The Dice score you recorded here will appear again in Stage 05 as the comparison reference.
