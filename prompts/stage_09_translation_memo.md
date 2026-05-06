# Stage 09 — Clinical Translation Memo

## Goal
Reflect on the clinical implications of your work and produce a concise memo
that honestly locates the prototype on the path from a toy pipeline to a
research contribution to a clinical tool.

## What to ask Claude Code

> "Run `make translation-memo`. Then open `reports/translation_memo.md`.
> Read through it and tell me:
> - whether the current-status section honestly describes what the pipeline
>   does NOT do (not just what it does)
> - whether the research-grade path is realistic or hand-wavy
> - whether the key limitation section identifies the most important thing
>   a clinical collaborator should know
> - what you would add or change before showing this to a real clinician"

## What this stage produces

| Artifact | Description |
|---|---|
| `reports/translation_memo.md` | ~400–600 word clinical memo grounded in actual pipeline results |
| `outputs/status/stage_09_translation_memo.json` | `{"status":"ok","best_dice":…,"best_method":"…"}` |

## Memo structure

1. **Current status** — what the prototype does and critically what it does NOT do
2. **Path to research-grade** — specific, ordered validation steps
3. **Path to clinical deployment** — regulatory, safety, and evidence requirements
4. **Key limitation** — the single most important thing a clinician should understand

## Check

```bash
make translation-memo
# Prints: dataset, best Dice achieved, method
# Open: reports/translation_memo.md — confirm it uses actual numbers from the pipeline
```

## Discussion questions

- The memo states the Dice results are in-sample estimates. What would an
  honest out-of-sample estimate require?
- EU MDR and FDA 510(k) are mentioned. What class of medical device would a
  fully automated tumour segmentation tool most likely be, and why?
- If you were presenting this work at a clinical-AI conference, what would
  you say in the limitations slide?
- This is the final lab artifact. What is the single most important thing
  you learned across Day 1 and Day 2?
