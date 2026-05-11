# Medical AI + Agentic Coding Lab

**PhD Course: Medical AI + Agentic Coding for Clinical Research**

> **Open in VS Code:** double-click `student-lab.code-workspace` — this gives you the intended student-facing view. Do not open the raw folder directly.

You are positioned as a **junior clinical AI investigator**. Over seven missions you will build a medical image segmentation prototype, investigate its failures, make one justified improvement, and produce written outputs suitable for clinical discussion.

You do not need traditional programming fluency. You work by writing structured prompts in **VS Code + Claude Code**, guided by a local dashboard.

---

## Start here

```bash
pip install -r requirements.txt   # install dependencies (one-time)
make preflight                    # confirm environment is intact
make fetch-sample                 # download the teaching data
make dashboard                    # open the mission dashboard
```

---

## The loop

Every mission follows the same rhythm:

> **dashboard → prompt → VS Code + Claude Code → artifact → dashboard**

1. Open the dashboard (`make dashboard`) and read the current mission.
2. Copy the prompt shown in the dashboard into your Claude Code session.
3. Let Claude run the task — it reads the repo, writes or extends scripts, produces artifacts.
4. Return to the dashboard and inspect the new outputs.
5. When the mission checklist shows complete, create a checkpoint commit and push.

The dashboard is your **navigation and feedback console**. All Claude interaction happens in VS Code + Claude Code — not in the dashboard.

---

## What you generate

This repo starts intentionally sparse. You and Claude gradually fill it in:

```
prompts/          read these to guide each mission
outputs/
  figures/        PNG figures — overlays, loss curves, error maps
  metrics/        JSON metric files — dice scores, comparisons
  status/         per-stage completion checks
reports/          written mission summaries
```

`outputs/` and `reports/` are empty at the start. Filling them is the lab.

---

## Missions

| Mission | Goal | Key output |
|---|---|---|
| 0 — Wake the Lab | Environment setup | `reports/env_check.md` |
| 1 — Receive the Signal | Fetch and inspect the dataset | `data/sample/` |
| 2 — Build the First Detector | Baseline model + first metric | `outputs/metrics/val_metrics.json` |
| 3 — Investigate Failure | Error analysis + hypothesis | `reports/error_analysis.md` |
| 4 — Improve With Intent | One controlled improvement | `outputs/metrics/model_swap_comparison.json` |
| 5 — Design the Next Study | Day 2 challenge plan + adaptation | `reports/challenge_plan.md` |
| 6 — Translate Responsibly | Clinical translation memo | `reports/translation_memo.md` |

Complete them in order. The dashboard unlocks the next mission when the current one passes.

---

## Using Claude Code

- Paste prompts from the dashboard — they specify exactly what Claude may edit and what to produce.
- Ask Claude to **state its plan before editing anything**.
- Never ask Claude to fabricate metric values or skip a mission.
- Push a checkpoint commit after each completed mission.

See [ASSIGNMENT.md](ASSIGNMENT.md) for full artifact requirements and grading criteria.

---

## Commands

```bash
make dashboard        # open the mission dashboard (primary interface)
make preflight        # structural check — run first, no data required
make fetch-sample     # download the teaching dataset
make test             # run autograding checks (same as CI)
make help             # list all available commands
```

---

*This repo contains support scaffold for teaching infrastructure and autograding. It is hidden from the workspace view by default and does not affect student work.*
