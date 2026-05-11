# Advisor Preview — Student Lab OS v1

**Date:** 2026-05-11
**Status:** Internal prototype — advisor review only

---

## What this is

A browser-based dashboard that guides PhD students through a structured Medical AI lab sequence. Students work entirely in VS Code + Claude Code; this dashboard provides orientation, prompt delivery, artifact inspection, and progress tracking.

The prototype is built on Streamlit and runs locally (no server required beyond `streamlit run app/streamlit_app.py`).

---

## Student workflow (primary path)

1. Student opens the dashboard in a browser.
2. Dashboard shows the current mission, its goal, and the base prompt to copy.
3. Student pastes the prompt into VS Code and runs it via Claude Code.
4. Claude writes or extends scripts, produces artifacts (figures, metrics, reports).
5. Student returns to the dashboard, clicks **Refresh**, and sees new outputs.
6. When all stage checks pass, student clicks **I finished — check my progress**.
7. Dashboard confirms completion and unlocks the next mission.
8. Student creates a checkpoint commit and pushes to GitHub Classroom.

---

## What is working in v1

- Full 7-mission sequence with stage-level status tracking
- Prompt delivery: Layer A (base), Layer B (reflection, locked until stages pass), Layer C (optional extension)
- Artifact preview: figures, metrics, status JSON, report excerpts per mission
- Mission Map tab with revisit mode for completed missions
- Results tab: key metrics across missions, figure gallery
- Reports tab: all written summaries in one place
- Evaluation tab: mirrors autograding CI checks
- Prompt Archive tab: read-only reference for all prompts
- Sidebar: progress rail, primary check-in button, advanced tools (rebuild, archive, reset)
- First-run tutorial: 7-step guided tour with orange focus highlight on UI targets
- Session archiving before any reset operation

---

## Intentionally deferred (not in v1)

- **Multi-student monitoring view** — no advisor-facing aggregation dashboard yet
- **Live run history / prompt ledger** — `.lab_history/` structure exists but is not yet surfaced in the dashboard
- **Push confirmation in-dashboard** — students push manually via VS Code; no in-app push button
- **Bonus mission unlock UI** — bonus prompts are shown per-mission but no separate bonus tracking panel
- **Dark-mode theme** — design spec mentions it; current build uses the light-mode variant only
- **GitHub Classroom integration** — assignment distribution and autograding are set up; classroom roster view is not wired into this dashboard

---

## Known limitations at this stage

- Dashboard requires local Python environment with `streamlit` installed
- No authentication — anyone with the URL can view and interact
- Metric display assumes specific JSON schemas; unexpected schema variations show `—`
- Tutorial focus highlight requires a Streamlit iframe to inject JS into the parent frame — works in Chrome and Safari, minor rendering variation in Firefox

---

*This document is for internal advisor review. Do not distribute to students.*
