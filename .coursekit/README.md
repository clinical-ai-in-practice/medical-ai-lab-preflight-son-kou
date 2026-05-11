# .coursekit — Instructor / Advisor Reference

This hidden directory contains course infrastructure and reference materials.
Students do not need to interact with it.

## Contents

| File / Folder | Purpose |
|---|---|
| `classroom_handoff.md` | Instructor setup and classroom logistics |
| `student_lab_os_design_spec_v1.md` | Full design specification for the Lab OS |
| `advisor_preview_v1.md` | Short prototype summary for advisor review |
| `archive/` | Earlier planning documents |

## What students work with

Students operate entirely in:

- `prompts/` — the natural-language prompts that drive each mission
- `scripts/` — Python scripts that Claude creates and extends on the student's behalf
- `reports/` — written outputs produced during the lab
- `outputs/` — figures, metrics, and status files produced by scripts
- `README.md`, `ASSIGNMENT.md`, `CLAUDE.md` — orientation and contract documents
- `Makefile` — pipeline commands (`make dashboard`, `make fetch-sample`, etc.)

## Hidden support infrastructure

The following directories are part of the system but hidden from the VS Code Explorer
by default (via `.vscode/settings.json`):

| Directory | Role |
|---|---|
| `app/` | Dashboard source — run via `make dashboard`, not edited by students |
| `artifacts/` | Grading contract schema — do not edit |
| `.github/` | CI autograding workflows — do not edit |
| `.devcontainer/` | Dev container configuration |
| `.session_archives/` | Runtime session snapshots (auto-created) |
| `.student_state/` | Mission progress state (auto-created) |

## Design intent

The lab is designed to feel **prompt-first**: students use natural-language prompts
in VS Code + Claude Code to direct the research workflow. The scripts in `scripts/`
are their workspace — Claude creates, modifies, and runs them based on the prompts.

The grading system (in `tests/`) checks that required artifacts exist at required
paths. It does not inspect how the scripts were written or who wrote them.

## For instructors

If you need to replace a student's broken script with a reference implementation,
place reference scripts here and copy them as needed. Do not commit reference
scripts to the visible `scripts/` directory — that would defeat the prompt-first pedagogy.
