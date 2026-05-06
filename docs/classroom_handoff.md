# GitHub Classroom Handoff Guide

This document is for the **instructor** setting up the assignment in GitHub Classroom.
Students do not need to read this file.

---

## What this repository is

This is the **student template repository** for the two-day PhD lab:
_Medical AI + Agentic Coding for Clinical Research._

It contains:
- 10 staged Python scripts (`scripts/`) — scaffolded, ready for students to run
- 10 stage prompt files (`prompts/`) — Claude Code instructions for each stage
- Autograding tests (`tests/`) — 67 artifact-contract tests, deterministic, no data required
- A Makefile with one command per stage
- `ASSIGNMENT.md` — the student-facing grading rubric
- `CLAUDE.md` — project-level instructions for Claude Code
- A Streamlit dashboard (`app/`) for progress visualization

---

## What GitHub Classroom distributes

When a student accepts the assignment, GitHub Classroom forks this template into a
private repository named `<assignment-slug>-<student-username>` under your GitHub
Classroom organization.

The student's copy is pre-populated with all scaffolding including the example
`outputs/` and `reports/` directories from this template run.  Autograding runs
`pytest -q tests/` on every push; students see pass/fail counts in their repo's
Actions tab.

---

## What a student does after accepting

```
1. Accept the GitHub Classroom assignment link  →  gets their private repo
2. Clone it locally (or open in Codespace / devcontainer)
3. pip install -r requirements.txt
4. Configure the teaching pack source (see below)
5. make preflight                   ← structural checks, no data needed
6. make fetch-sample                ← downloads/copies the teaching pack
7. make run-day1                    ← Stages 00–06 in sequence
8. git add outputs/ reports/ && git commit && git push
9. Check the Actions tab — all tests should pass
10. make run-day2                   ← Stages 07–09 in sequence
11. Final push before deadline
```

---

## Visible autograding command

The canonical visible autograding command is:

```
pytest -q tests/
```

or equivalently:

```
make test
```

Configure this as the single autograding test in GitHub Classroom:
- **Run command:** `pytest -q tests/`
- **Timeout:** 60 seconds (tests are deterministic artifact checks, no computation)
- **Points:** assign as you see fit; all 67 tests must pass for full credit

Students run `make test` locally at any time to see the same results CI sees.

---

## Preflight assignment

Run this as a short **first-session** assignment to confirm every student's
environment is working before Day 1 begins.

Preflight checks (run with `make preflight`):
1. Python ≥ 3.10 is available
2. All required packages install without error
3. All scaffold files are present (prompts, scripts, tests, CLAUDE.md)
4. `make bootstrap` completes — creates output folders, writes `stage_00_bootstrap.json`
5. The teaching pack config exists (`data/teaching_pack.cfg`)

The preflight does **not** require the teaching pack data — it only checks the
environment and file structure.

---

## Required artifacts (what CI checks)

| Artifact | Check |
|---|---|
| `outputs/status/stage_NN_*.json` with `"status":"ok"` | 10 status files, stages 00–09 |
| `outputs/figures/*.png` (non-empty) | 5 figures: overlay, loss curve, 2× error analysis, model swap comparison |
| `outputs/metrics/val_metrics.json` | `dice` key, float ∈ [0, 1] |
| `outputs/metrics/model_swap_comparison.json` | `baseline_dice`, `new_dice`, `change_description` |
| `outputs/metrics/challenge_comparison.json` | `baseline_dice`, `new_dice`, `delta` |
| `reports/day1_summary.md` | ≥ 400 chars, `# Day 1 Summary` header |
| `reports/error_analysis.md` | ≥ 200 chars, `# Error Analysis` header |
| `reports/model_swap.md` | ≥ 200 chars |
| `reports/challenge_plan.md` | ≥ 200 chars, `# Day 2 Challenge Plan` header |
| `reports/adapt_pipeline.md` | ≥ 200 chars |
| `reports/translation_memo.md` | ≥ 400 chars, `# Clinical Translation Memo` header, covers research + clinical + limitation |

---

## What you must configure before opening the assignment

### 1. Teaching pack URL or path

Edit `data/teaching_pack.cfg` in **this template repo** before marking it as the
Classroom template.  Set the URL or path where students can fetch the data:

```ini
# data/teaching_pack.cfg
url = https://your-server.example.com/teaching_pack.zip
```

Or use a path to a shared network drive / Codespace secret / environment variable.

Students with the correct `teaching_pack.cfg` will run `make fetch-sample` and
get the data automatically.

Alternatively, distribute the pack as a GitHub release asset and set:

```ini
url = https://github.com/<org>/<repo>/releases/download/<tag>/teaching_pack.zip
```

### 2. GitHub Classroom organization

Create the Classroom under your GitHub organization.  Use this repo as the
starter code (template repository).

### 3. Autograding configuration

In the GitHub Classroom assignment settings:
- Enable autograding
- Add one test: **Run command** = `pytest -q tests/`, **Timeout** = 60s
- Set maximum points (e.g., 100) — all 67 tests pass = full credit

### 4. Deadline

Set a deadline in GitHub Classroom.  Students push their final commit before
the deadline.  Late pushes after the deadline are not counted (GitHub Classroom
enforces this automatically if enabled).

### 5. Codespaces (optional)

The `.devcontainer/devcontainer.json` is pre-configured for GitHub Codespaces.
Enable Codespaces in GitHub Classroom if you want students to work in the browser
without a local Python setup.  The devcontainer installs all dependencies automatically.

---

## Teacher-side vs student-side

| Responsibility | Who |
|---|---|
| Set `data/teaching_pack.cfg` URL | **Teacher** (before distributing) |
| Distribute the assignment link | **Teacher** |
| Review `reports/` for quality | **Teacher** (manual, after deadline) |
| Run `make run-day1` and `make run-day2` | **Student** |
| Push outputs to their repo | **Student** |
| Configure GitHub Classroom org and autograding | **Teacher** |
| Provide Claude Code access (API key or app) | **Teacher** (pre-lab logistics) |

---

## Workflows overview

| Workflow | Trigger | Purpose |
|---|---|---|
| `autograde-visible.yml` | Every push | Runs `pytest -q tests/` and uploads artifacts to Actions |
| `preflight.yml` | Push on `main` only | Runs `make bootstrap` + `pytest -q tests/test_preflight.py` |
| `evaluate-hidden.yml` | Manual (`workflow_dispatch`) | Placeholder for teacher-run hidden evaluation |

---

## Important notes

- **Do not add the teaching pack data to this template repo.** `data/sample/` is in `.gitignore`.
- The template repo contains example `outputs/` and `reports/` from the scaffold run.
  Students' graded outputs replace these.
- `CLAUDE.md` contains project-level instructions for Claude Code. Do not modify it
  without testing that the student workflow still works.
- Tests in `tests/` are the grading contract. Do not change them without updating
  `ASSIGNMENT.md` to match.
