# Stage 09 — Clinical Translation Memo
## Mission 6: Translate Responsibly

## Goal

Reflect on the clinical implications of your work and produce a concise memo
that honestly locates the prototype on the path from a toy pipeline to a
research contribution to a clinical tool.

Overstating prototype capabilities in clinical AI can cause direct patient harm.
This memo is the most important writing exercise of the lab. It should be grounded
in your actual results — including disappointing ones.

## Memo structure

1. **Current status** — what the prototype does and critically what it does NOT do
2. **Path to research-grade** — specific, ordered validation steps
3. **Path to clinical deployment** — regulatory, safety, and evidence requirements
4. **Key limitation** — the single most important thing a clinician should understand

## Layer A — Base prompt

> "Run `make translation-memo`. Then open `reports/translation_memo.md`.
> Read through it and tell me:
> - whether the current-status section honestly describes what the pipeline does NOT do
>   (not just what it does)
> - whether the research-grade path is specific and realistic, or vague and hand-wavy
> - whether the key limitation section identifies the most important thing a clinical
>   collaborator should understand before relying on this tool
> - what you would add or change before showing this document to a real clinician"

## What this stage produces

| Artifact | Description |
|---|---|
| `reports/translation_memo.md` | ~400–600 word clinical memo grounded in actual pipeline results |
| `outputs/status/stage_09_translation_memo.json` | `{"status":"ok","best_dice":…,"best_method":"…"}` |

## Files

**Allowed to edit:** `scripts/translation_memo.py`, `reports/translation_memo.md`

**Protected — do not modify:** all prior `outputs/metrics/` and `reports/` files (the memo must
reflect what actually happened, not a revised version of history), `tests/`, `artifacts/schema.json`, `prompts/`

## Check

```bash
make translation-memo
# Prints: dataset, best Dice achieved, and best method
# Open: reports/translation_memo.md — confirm it uses actual numbers from the pipeline
```

**What to inspect manually:**
- Does the memo include the `# Clinical Translation Memo` header? (grading requires it)
- Does the current-status section mention the actual Dice score by value, not just "promising results"?
- Does the memo use the word "limitation" or an equivalent? (grading checks for this)
- Is the memo longer than 400 characters? (one-paragraph stubs fail the autograding check)
- Does the memo discuss both research-grade validation AND clinical deployment?

## Layer B — Reflection prompt

After reviewing the memo, ask Claude:

> "Steelman the biggest limitation of this prototype:
> - If a senior clinical researcher reviewed this memo, what would they say is the most
>   important thing you have not addressed?
> - What would a rigorous external validation study for this pipeline look like?
>   How many patients, from how many sites, using what ground-truth standard?
> - Add or revise the '## Key Limitation' section of `reports/translation_memo.md`
>   to reflect this level of scrutiny. Make it specific — not 'more data is needed'
>   but *what kind* of data, *why*, and *what threshold would constitute sufficient evidence*."

## Layer C — What you can customize

Ask Claude to write a single-paragraph version of the memo targeted at a different audience:
either a startup looking to commercialise the approach, or a PhD student writing a methods section.
Compare how the emphasis shifts. This is not a required artifact — it is a calibration exercise
to see how much framing affects the perceived strength of your results.

## Discussion questions

- The Dice results you report are in-sample estimates from a small teaching pack.
  What would an honest out-of-sample estimate require — in terms of data, sites, and study design?
- EU MDR and FDA 510(k) are mentioned in the translation memo. What class of medical device
  would a fully automated tumour segmentation tool most likely fall into, and why?
- If you were presenting this work at a clinical-AI conference, what would you say
  in the limitations slide that is not already in the memo?
- This is the final lab artifact. What is the single most important scientific insight
  you developed across Day 1 and Day 2?
