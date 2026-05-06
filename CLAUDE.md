# CLAUDE.md — Lab Instructions for Claude Code

Read this file before taking any action in this repository.
This file is the project-level contract between you and the student.

---

## Repository purpose

You are helping a PhD student complete a staged medical image analysis workflow.
The workflow has 10 stages (stage_00 through stage_09).
Each stage produces specific artifacts. Later stages depend on earlier ones.
Do not attempt to complete multiple stages at once.

---

## Staged workflow

| Stage | Script | Key outputs |
|---|---|---|
| stage_00_bootstrap | scripts/bootstrap.py | outputs/status/stage_00_bootstrap.json, reports/env_check.md |
| stage_01_fetch_sample | scripts/fetch_data.py | data/sample/, outputs/status/stage_01_fetch_sample.json |
| stage_02_load_visualize | scripts/visualize_sample.py | outputs/figures/sample_overlay.png, reports/data_notes.md |
| stage_03_train_baseline | scripts/run_train.py | outputs/metrics/val_metrics.json, outputs/figures/loss_curve.png, reports/train_notes.md |
| stage_04_error_analysis | scripts/error_analysis.py | reports/error_analysis.md, outputs/figures/error_analysis_*.png, outputs/status/stage_04_error_analysis.json |
| stage_05_model_swap | scripts/model_swap.py | outputs/metrics/model_swap_comparison.json, reports/model_swap.md, outputs/status/stage_05_model_swap.json |
| stage_06_pack_report | scripts/pack_report.py | reports/day1_summary.md, outputs/status/stage_06_pack_report.json |
| stage_07_challenge_plan | scripts/challenge_plan.py | reports/challenge_plan.md, outputs/status/stage_07_challenge_plan.json |
| stage_08_adapt_pipeline | scripts/adapt_pipeline.py | outputs/metrics/challenge_comparison.json, outputs/figures/challenge_comparison.png, reports/adapt_pipeline.md, outputs/status/stage_08_adapt_pipeline.json |
| stage_09_translation_memo | scripts/translation_memo.py | reports/translation_memo.md, outputs/status/stage_09_translation_memo.json |

---

## Required artifact locations

Save all outputs to exactly these paths. Grading tests check these exact locations.

**Status files:** `outputs/status/stage_NN_<name>.json`
Required minimum: `{"status": "ok", ...stage-specific keys...}`

**Figures:** `outputs/figures/<descriptive_name>.png`

**Metrics:**
- `outputs/metrics/val_metrics.json` — required key: `dice` (float)
- `outputs/metrics/model_swap_comparison.json` — required keys: `baseline_dice`, `new_dice`, `change_description`

**Reports:** `reports/<name>.md` — written in plain Markdown

---

## Naming rules

- Stage status files: `stage_NN_<lowercase_slug>.json` — two-digit number, underscore, short slug
- Figures: descriptive, lowercase snake_case, `.png` extension
- Reports: lowercase snake_case, `.md` extension
- Never use spaces in output filenames
- Never invent new output directories — use the ones defined above

---

## Minimal-edit philosophy

- Read the relevant prompt in `prompts/` before making any changes
- State your plan in plain language before editing any file — the student should approve it
- Edit the smallest number of files needed to complete the current stage
- Prefer adding to existing scripts rather than rewriting them
- One stage at a time — do not reach ahead
- After completing a stage, confirm that `make <stage-command>` runs without errors

---

## Reproducibility requirements

- Every script must run from the repo root: `python scripts/<script>.py`
- Use `Path(__file__).resolve().parents[1]` for the base path — never hardcode absolute paths
- Set random seeds explicitly if any randomness is used (`numpy.random.seed(42)`)
- Scripts must be idempotent — safe to run more than once
- Do not write outputs that depend on the local machine environment (timestamps, usernames, etc.)

---

## Honesty requirements

- Never fabricate or invent metric values
- Never write a report that contradicts the actual computed metrics
- If a result is poor, report it honestly and explain what the numbers mean
- If a script raises an error, diagnose and fix the root cause — do not catch and suppress errors silently
- If a stage cannot complete due to missing data, say so clearly rather than writing a stub status

---

## What must never be deleted

- `CLAUDE.md` (this file)
- `ASSIGNMENT.md`
- `artifacts/schema.json`
- Any file in `prompts/`
- Any file in `tests/`
- `Makefile`
- `requirements.txt`
- Any existing `outputs/status/*.json` that has `"status": "ok"`

---

## Files Claude is expected to edit

- `scripts/*.py` — extend and complete stage logic per the prompt instructions
- `reports/*.md` — write and update stage summaries
- `app/streamlit_app.py` — extend the dashboard if explicitly instructed
- `prompts/*.md` — never edit these; they are the student's instructions
- `docs/classroom_handoff.md` — instructor-only reference; do not modify

---

## Files Claude should not change without explicit instruction

- `.github/workflows/*.yml` — grading infrastructure
- `tests/*.py` — autograding tests
- `requirements.txt` — only update if a new package is genuinely required for the current stage
- `artifacts/schema.json` — output contract definition
- `ASSIGNMENT.md` — course instructions, not a working document
- `Makefile` — only update if adding a new make target is explicitly part of the stage work
