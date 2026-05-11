# GitHub Classroom Handoff Guide

This document is for the **instructor** setting up the assignment in GitHub Classroom.
Students do not need to read this file.

---

## What this repository is

This is the **student template repository** for the two-day PhD lab:
_Medical AI + Agentic Coding for Clinical Research._

It implements the **Student Lab OS** model: a mission-based, prompt-driven,
dashboard-guided, artifact-producing research training environment.
Students work through a sequence of research missions in **VS Code + Claude Code**,
guided by a local Streamlit dashboard that shows mission objectives, prompt guidance,
artifacts, and submission readiness. Students do not need traditional programming
fluency — they learn by using prompts as experimental instruments.

The repo contains:
- 10 staged Python scripts (`scripts/`) — scaffolded, one per mission stage
- 10 stage prompt files (`prompts/`) — Claude Code instructions for each stage
- Autograding tests (`tests/`) — 67 artifact-contract tests, deterministic, no data required
- A Makefile with one command per stage
- `ASSIGNMENT.md` — the student-facing grading contract and workflow guide
- `CLAUDE.md` — project-level instructions for Claude Code
- A Streamlit dashboard (`app/`) — the student's mission map, prompt studio, and evaluation console
- `docs/student_lab_os_design_spec_v1.md` — the authoritative design blueprint (instructor reference)

---

## What GitHub Classroom distributes

When a student accepts the assignment, GitHub Classroom forks this template into a
private repository named `<assignment-slug>-<student-username>` under your GitHub
Classroom organization.

The student's copy is pre-populated with all scaffolding including prompt files,
scripts, and any example artifacts committed to the template at distribution time.

> **Note:** Before marking this repo as the Classroom template, verify which
> `outputs/` and `reports/` files are committed. Example artifacts from a
> template run are useful as orientation scaffolding, but students should
> understand their graded outputs must come from running their own pipeline.

Autograding runs `pytest -q tests/` on every push; students see pass/fail counts
in their repo's Actions tab.

---

## What a student does after accepting

```
1. Accept the GitHub Classroom assignment link  →  gets their private repo
2. Clone it locally (or open in Codespace / devcontainer)
3. pip install -r requirements.txt
4. Configure the teaching pack source (see below)
5. make preflight                   ← structural checks, no data needed
6. make fetch-sample                ← downloads/copies the teaching pack
7. make dashboard                   ← open the mission dashboard
8. Follow the mission sequence in the dashboard (Day 1 missions → checkpoint push)
9. Continue to Day 2 missions → final push before deadline
```

The primary student loop is:
**dashboard → prompt → VS Code + Claude Code → artifact → dashboard**

Students do not interact with Claude through the dashboard. The dashboard is for
orientation, prompt guidance, and feedback; all Claude interaction happens in
VS Code + Claude Code. The Student Lab OS design spec (`docs/student_lab_os_design_spec_v1.md`)
describes the full experience model.

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
The dashboard's Evaluation tab shows the same checks in real time.

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
Classroom template. Set the URL or path where students can fetch the data:

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

### 2. Template repository visibility and ownership

GitHub Classroom requires the starter/template repository to be either:
- **Public**, or
- **Owned by the same GitHub organization** as the Classroom.

If this repo lives under a personal account or a different org, move or transfer
it before creating the assignment. A repo that does not meet this requirement
will cause Classroom to fail silently when students accept the link.

In the repository settings, enable **"Template repository"** so GitHub Classroom
can fork it correctly.

### 3. GitHub Classroom organization

Create the Classroom under your GitHub organization. Use this repo as the
starter code (template repository).

### 4. Autograding configuration

In the GitHub Classroom assignment settings:
- Enable autograding
- Add one test: **Run command** = `pytest -q tests/`, **Timeout** = 60s
- Set maximum points (e.g., 100) — all 67 tests pass = full credit

### 5. Deadline

Set a deadline in GitHub Classroom. Students push their final commit before
the deadline. The Student Lab OS model encourages at least one checkpoint push
per completed mission, so push history is useful for instructor monitoring during
the lab, not just at the deadline.

### 6. Codespaces (optional)

The `.devcontainer/devcontainer.json` is pre-configured for GitHub Codespaces.
Enable Codespaces in GitHub Classroom if you want students to work in the browser
without a local Python setup. The devcontainer installs all dependencies automatically.

---

## Updating the template after distribution

Changes to the template repo do **not** propagate automatically to student repos.

- **Critical bug fixes or test corrections:** Use GitHub Classroom's feedback pull
  request feature to push changes into each student repo. Never change `tests/`
  after distribution without notifying students and re-running autograding — test
  changes alter the grading contract.
- **Prompt updates (`prompts/`):** Distribute corrected files out-of-band (e.g.,
  post in the course chat) and ask students to replace them manually. This is
  simpler than a mass PR for non-grading-critical files.
- **CLAUDE.md changes:** Test the full student mission workflow before distributing
  any update, as CLAUDE.md governs what Claude Code is allowed to do in each repo.

---

## Teacher-side vs student-side

| Responsibility | Who |
|---|---|
| Set `data/teaching_pack.cfg` URL | **Teacher** (before distributing) |
| Verify template repo is public or org-owned | **Teacher** (before distributing) |
| Distribute the assignment link | **Teacher** |
| Provide Claude Code access (API key or app) | **Teacher** (pre-lab logistics) |
| Monitor mission-level push cadence during lab | **Teacher** (during lab) |
| Review `reports/` for reasoning quality | **Teacher** (manual, after deadline) |
| Configure GitHub Classroom org and autograding | **Teacher** |
| Complete missions via dashboard + VS Code + Claude Code | **Student** |
| Push checkpoint commits per completed mission | **Student** |

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
- Verify which example `outputs/` and `reports/` files are committed before distribution.
  Students' graded outputs replace any scaffolding files, but be deliberate about
  what you ship in the template.
- `CLAUDE.md` is the operational contract for the Student Lab OS model. Do not modify
  it without testing the full student mission workflow.
- `docs/student_lab_os_design_spec_v1.md` is the authoritative design blueprint.
  Consult it when making structural changes to the lab.
- Tests in `tests/` are the grading contract. Do not change them without updating
  `ASSIGNMENT.md` to match and notifying students.
