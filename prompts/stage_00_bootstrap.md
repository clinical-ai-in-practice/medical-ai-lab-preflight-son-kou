# Stage 00 — Bootstrap
## Mission 0: Wake the Lab

## Goal

Confirm that your environment is working, that Claude Code can navigate this repository,
and produce the first two research artifacts: an environment report and a bootstrap status file.

This is not just a setup step. It is your first proof that the full tool chain —
Python, Claude Code, VS Code, and the repo scaffold — is operational and ready
for scientific work.

## Layer A — Base prompt

> "Read `CLAUDE.md` and give me a one-paragraph description of what this lab is for
> and how it is structured. Then run `make bootstrap` and confirm that:
> - `reports/env_check.md` was created and is non-empty
> - `outputs/status/stage_00_bootstrap.json` was created with `"status": "ok"`
>
> Show me the contents of both files and explain what each field means."

## What this stage produces

| Artifact | Description |
|---|---|
| `reports/env_check.md` | Environment summary: Python version, platform, package check |
| `outputs/status/stage_00_bootstrap.json` | `{"status":"ok","python_version":"...","platform":"..."}` |

## Files

**Allowed to edit:** `scripts/bootstrap.py`, `reports/env_check.md`

**Protected — do not modify:** `CLAUDE.md`, `tests/`, `artifacts/schema.json`, `prompts/`

## Check

```bash
make bootstrap
# Expected: prints "Bootstrap complete" without error
# Then verify:
cat reports/env_check.md
cat outputs/status/stage_00_bootstrap.json
```

**What to inspect manually:**
- `reports/env_check.md` — does it list the Python version and packages you expect?
- `outputs/status/stage_00_bootstrap.json` — confirm `"status"` is `"ok"`, not `"error"`

## Layer B — Reflection prompt

After confirming the outputs, ask Claude:

> "Explain the repository structure to me as if I were a new research fellow joining
> this project for the first time. What does each top-level folder contain?
> What is my role versus your role in this lab?
> What would you flag as the most important thing to understand before beginning Mission 1?"

## Layer C — What you can customize

Ask Claude to add one observation to `reports/env_check.md` that is specific to your
machine — for example, GPU availability or available RAM — if you think it is relevant
to the pipeline. This is your first opportunity to make the lab record accurate to your environment.

## Discussion questions

- What does `"status": "ok"` in the status file guarantee? What does it *not* guarantee?
- If `make bootstrap` fails with a Python import error, what is the first thing to check?
- What is the difference between `make preflight` and `make bootstrap`?
  Which one would you run if you suspected a corrupted output folder?

## What comes next

Stage 01 fetches the teaching data pack from the configured source.
Stage 02 loads the data and produces the first visual artifact.
