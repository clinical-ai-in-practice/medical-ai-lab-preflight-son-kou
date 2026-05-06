# CLAUDE.md — Lab Instructions for Claude Code

Read this file before taking any action in this repository.
This file is the project-level contract between you and the student.

---

## Design authority

**Primary design specification:** `docs/student_lab_os_design_spec_v1.md`

@docs/student_lab_os_design_spec_v1.md

If any instruction in this file conflicts with the design spec, the design spec takes precedence.
This CLAUDE.md provides operational shortcuts and concrete path rules; the design spec provides conceptual authority.

---

## Repository purpose

This repository is a **Student Lab OS** — a mission-based, prompt-driven, dashboard-guided, artifact-producing research training environment for a PhD-level Medical AI summer school.

Students are positioned as junior clinical AI investigators working through a sequence of research missions. They do not need traditional programming fluency. They learn by using **prompts as experimental instruments** and judging results through artifacts, metrics, and scientific reasoning.

This is not a conventional script-execution pipeline. Stages exist to support missions, not as the primary organizing concept.

---

## Student interaction model

- Students act in **VS Code + Claude Code** — this is where prompts are executed and code runs.
- The **local dashboard** (Streamlit app) is the student's navigation and feedback console: it shows mission guidance, artifacts, metrics, run history, and progress.
- The dashboard is **not** the Claude chat interface. Students do not interact with Claude through the dashboard.
- **Prompts are experimental instruments**, not magic commands. Better prompts improve experimental control. Prompts must be grounded in evidence and outputs.
- The primary student loop is: **dashboard → prompt → VS Code + Claude Code → artifact → dashboard feedback**.

---

## Mission architecture

The lab is organized into missions. Each mission has a goal, a set of allowed files, expected outputs, and completion criteria.

| Mission | Theme | Core goal |
| ------- | ----- | --------- |
| Mission 0 — Wake the Lab | Bootstrap | Environment setup, Claude readiness, first prompt-driven success |
| Mission 1 — Receive the Signal | Data acquisition | Fetch teaching pack, inspect dataset, first image exposure |
| Mission 2 — Build the First Detector | Modeling | Baseline segmentation/modeling, first meaningful metric, first artifact set |
| Mission 3 — Investigate Failure | Error analysis | Best/worst case analysis, error maps, failure interpretation, hypothesis formation |
| Mission 4 — Improve With Intent | Controlled improvement | One controlled improvement, measured comparison, scientific reasoning |
| Mission 5 — Design the Next Study | Challenge planning | Day 2 challenge plan, adapt the pipeline |
| Mission 6 — Translate Responsibly | Research judgment | Clinical gap, product gap, human oversight, translation memo |

---

## Stage-to-script mapping (implementation detail)

Stages are the underlying implementation structure that missions are built on. They are not the conceptual center of the student experience — missions are.

| Stage | Script | Key outputs |
| ----- | ------ | ----------- |
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

**Run history:** `.lab_history/mission_NN/run_NNN/` — prompt text, result, changed files, notes

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
- Edit the smallest number of files needed to advance the current mission
- Prefer adding to existing scripts rather than rewriting them
- Focus on one mission at a time; do not race ahead into unrelated missions or stages
- After completing a mission, verify that the expected artifacts exist and `make <stage-command>` runs without errors

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
- If a mission cannot complete due to missing data, say so clearly rather than writing a stub status

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

## Files Claude may edit

- `scripts/*.py` — extend and complete mission logic per the prompt instructions
- `reports/*.md` — write and update mission summaries
- `app/streamlit_app.py` — extend the dashboard only if explicitly instructed
- `.lab_history/**` — run history and prompt ledger records

## Files Claude must not edit without explicit instruction

- `prompts/*.md` — these are the student's experimental instruments; never modify them
- `docs/classroom_handoff.md` — instructor-only reference
- `.github/workflows/*.yml` — grading infrastructure
- `tests/*.py` — autograding tests
- `requirements.txt` — only update if a new package is genuinely required for the current mission
- `artifacts/schema.json` — output contract definition
- `ASSIGNMENT.md` — course instructions, not a working document
- `Makefile` — only update if adding a new make target is explicitly part of the mission work
- `docs/student_lab_os_design_spec_v1.md` — design authority; do not modify

---

## Summary

This repository is student-facing. It is not primarily a teacher dashboard repo.

The student is a junior clinical AI investigator. Their work is judged by artifacts, metrics, comparisons, and reports — not by chat verbosity or raw code complexity.

The main loop is:

> **dashboard → prompt → VS Code + Claude Code → artifact → dashboard**

Every action you take should serve that loop: help the student advance a mission, produce a real artifact, and return to the dashboard with something new to inspect.
