# Lab Assignment — Medical AI + Agentic Coding for Clinical Research

## Overview

This two-day lab asks you to build a **reproducible medical image segmentation pipeline** using Python, Claude Code, and structured prompts. You will analyze a curated medical image dataset, train a deterministic baseline model, investigate its errors, make one justified improvement, and produce a written summary suitable for clinical discussion.

The lab assesses both the technical outputs you produce and your ability to reason about them clearly.

---

## What you submit

You submit this GitHub repository. At submission time, the repository must contain all of the required artifacts listed below. Grading runs automated tests against your committed files.

**Submission = your final commit pushed before the deadline.**

There is no separate upload step. Push your work and you are done.

---

## Required artifacts

All paths are relative to the repository root.

### Status files (written automatically by scripts — do not edit)

| File | Required keys |
|---|---|
| `outputs/status/stage_00_bootstrap.json` | `status`, `python_version`, `platform` |
| `outputs/status/stage_01_fetch_sample.json` | `status`, `dataset` |
| `outputs/status/stage_02_load_visualize.json` | `status`, `figure` |
| `outputs/status/stage_03_train_baseline.json` | `status`, `dice` |
| `outputs/status/stage_04_error_analysis.json` | `status`, `best_case`, `worst_case` |
| `outputs/status/stage_05_model_swap.json` | `status`, `baseline_dice`, `new_dice`, `change_description` |
| `outputs/status/stage_06_pack_report.json` | `status`, `sections` |

Day 2 (required for full credit):

| File | Required keys |
|---|---|
| `outputs/status/stage_07_challenge_plan.json` | `status` |
| `outputs/status/stage_08_adapt_pipeline.json` | `status` |
| `outputs/status/stage_09_translation_memo.json` | `status` |

### Figures

| File | Notes |
|---|---|
| `outputs/figures/sample_overlay.png` | Must be non-empty |
| `outputs/figures/loss_curve.png` | Must be non-empty |
| `outputs/figures/error_analysis_best.png` | Must be non-empty |
| `outputs/figures/error_analysis_worst.png` | Must be non-empty |
| `outputs/figures/model_swap_comparison.png` | Must be non-empty |
| `outputs/figures/challenge_comparison.png` | Must be non-empty (Day 2) |

### Metrics

| File | Required keys | Constraints |
|---|---|---|
| `outputs/metrics/val_metrics.json` | `dice` | Float between 0.0 and 1.0 |
| `outputs/metrics/model_swap_comparison.json` | `baseline_dice`, `new_dice`, `change_description` | Both dice values must be valid floats |

### Reports (written by you with Claude's help)

| File | Minimum requirement |
|---|---|
| `reports/env_check.md` | Non-empty |
| `reports/data_notes.md` | Non-empty |
| `reports/train_notes.md` | Contains Dice score |
| `reports/error_analysis.md` | Describes at least one failure case |
| `reports/model_swap.md` | Describes the change and outcome |
| `reports/day1_summary.md` | Covers all Day 1 stages |
| `reports/translation_memo.md` | Addresses prototype vs. clinical deployment |

---

## Academic integrity

This lab requires you to use Claude Code. That is intentional. Using AI assistance is part of the assignment.

The following are violations of academic integrity:

- **Fabricating metrics.** All metric values in `outputs/metrics/` must come from actually running the pipeline. Do not write or edit metric files by hand.
- **Copying another student's artifacts.** Your outputs must come from running your own pipeline on your own assigned dataset.
- **Misrepresenting Claude's work as independent insight.** Reports are expected to reflect your own understanding. Use Claude to help you write clearly, not to replace your reasoning.
- **Bypassing a stage.** If a stage fails, debug it. Do not manually write the status JSON to make it appear complete.

If you are unsure whether something is allowed, ask before doing it.

---

## How grading works

Grading is partly automated and partly manual.

**Automated (CI):** When you push, GitHub Actions runs `pytest -q tests/`. Visible test results are shown in the Actions tab of your repository. You can push as many times as you like before the deadline.

Run `make test` locally at any time to see the same results before pushing.
Run `make preflight` for a quick structural check that requires no data.

**Manual review:** The instructor will review your `reports/` for quality of reasoning, honesty about results, and clarity of clinical discussion.

---

## What good work looks like in this course

- **Reproducible.** Running `make run-day1` from a clean clone produces the same outputs.
- **Honest.** Reports accurately describe the metrics, including failures and limitations.
- **Minimal.** The pipeline does exactly what is needed at each stage — not more.
- **Explainable.** You can describe every step in plain language to a clinical collaborator.
- **Staged.** Each stage is complete before the next begins. Status files confirm this.

You are not graded on achieving a high Dice score. You are graded on the quality of your process and reasoning.
