# Lab Goals — What This Repository Is For

This is your personal workspace for the Medical AI + Agentic Coding lab.
By the end of the two sessions, your repository will contain a complete,
reproducible medical image segmentation pipeline that you built and can explain.

---

## What "complete" means

At the end of Day 2, `make test` should pass all 67 tests.
Each test checks for a specific artifact that your pipeline must have produced.

Running `make test` locally gives you the same feedback that CI gives on every push.
Green = everything is in place.  Red = something is missing or malformed.

---

## The three guarantees this lab asks for

1. **Reproducible.** Someone else should be able to clone your repo, run `make run-day1`,
   and get the same outputs you did.

2. **Honest.** Every number in `outputs/metrics/` must come from actually running
   the pipeline.  Never edit metric files by hand.

3. **Explainable.** Your `reports/` should describe what happened in plain language,
   including any results that were poor or unexpected.

---

## Quick reference

| What you want to do | Command |
|---|---|
| Check everything is working (no data needed) | `make preflight` |
| Run the full Day 1 pipeline | `make run-day1` |
| Run the full Day 2 pipeline | `make run-day2` |
| See your progress dashboard | `make app` |
| Run the autograding tests | `make test` |
| Get help on all commands | `make help` |

---

## If something goes wrong

1. Read the error message carefully — most errors name the missing file or key.
2. Check which stage failed: `cat outputs/status/stage_NN_*.json`
3. Re-run just that stage: `make <stage-command>`
4. Ask Claude Code: paste the error and the relevant prompt from `prompts/`.
5. If the environment is broken: `make bootstrap` resets the output folders.
