# Mission 6 — Translate Responsibly

## What this mission is about

Overstating prototype capabilities in clinical AI can cause direct patient harm.
This mission asks you to locate your prototype honestly on the path from
toy pipeline to research contribution — and to write a memo a clinical
collaborator could actually read and act on.

This is the most important writing exercise of the lab.

---

## Prompt Principle: Honesty constraint + audience framing

Telling Claude "write this for a clinical collaborator who knows medicine but
not ML, and do not overstate what has been demonstrated" shapes both honesty
and register. Without audience framing, Claude defaults to technical optimism.
Without an explicit honesty instruction, Claude may soften limitations or
omit them entirely. Both constraints are necessary.

---

## Layer A — Base Prompt

> I need to write a clinical translation memo for the segmentation prototype
> I have built over the past two days. This memo should be honest and written
> for a clinical collaborator who knows medicine but is not an ML expert.
>
> Please do the following:
>
> 1. Gather the key results from:
>    - `outputs/metrics/val_metrics.json` — baseline Dice
>    - `outputs/metrics/model_swap_comparison.json` — Day 1 improvement
>    - `outputs/metrics/challenge_comparison.json` — Day 2 improvement
>    - `reports/day1_summary.md` and `reports/adapt_pipeline.md`
>
> 2. Write a translation memo to `reports/translation_memo.md` with these sections:
>
>    `# Clinical Translation Memo`
>
>    `## Current Status`
>    Where does this prototype sit on the path to clinical use?
>    Use this framing: research prototype / research tool / research-grade software /
>    clinical validation needed / regulatory submission ready.
>    Be honest — do not advance the prototype beyond what the evidence supports.
>
>    `## What Was Demonstrated`
>    Summarize the key quantitative results in plain language.
>    Include the best Dice score achieved and what it means practically.
>
>    `## What Was Not Demonstrated`
>    What clinical validity questions remain unanswered?
>    (e.g., generalization to other sites, other patient populations, real-time use)
>
>    `## Key Limitations`
>    At least 3 concrete limitations of the current prototype.
>
>    `## Path to Research-Grade Use`
>    What would need to happen next for this to become a publishable research tool?
>    Not a clinical product — just a research contribution.
>
>    `## Human Oversight Requirements`
>    If this system were used in a research setting today, what human review
>    process would be required? Be specific.
>
> 3. Write a status file to `outputs/status/stage_09_translation_memo.json`:
>    `{"status": "ok", "best_dice": <highest dice across all methods>, "best_method": "..."}`
>
> Do not invent clinical claims. Do not describe the prototype as "ready for deployment."
> The goal of this memo is not to sell the prototype — it is to characterize it honestly.

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `reports/translation_memo.md` | 6 sections, honest assessment, > 400 chars, `# Clinical Translation Memo` header |
| `outputs/status/stage_09_translation_memo.json` | `{"status": "ok", "best_dice": X, "best_method": "..."}` |

---

## Layer B — Reflection Prompt

> Read `reports/translation_memo.md` from the perspective of three different readers:
>
> **A clinical radiologist:** What questions would they ask that the memo does not answer?
> What would concern them most about deploying this in their workflow?
>
> **A regulatory reviewer:** What evidence is missing before this could be submitted
> for even a research use authorization? What section of the memo is most incomplete
> from a regulatory perspective?
>
> **A patient:** If they knew this system might be used to assist with their diagnosis,
> what would they want to know that the memo does not say?
>
> Add a `## Stakeholder Questions` section to the memo with your assessment of each perspective.

---

## Layer C — Exploration Challenge

> Compare two versions of the translation memo:
>
> - **Version A (current):** honest and conservative
> - **Version B (alternative):** write a second version that is more optimistic —
>   emphasizes achievements more, minimizes limitations, positions the prototype more ambitiously
>
> Save the second version as `reports/translation_memo_optimistic.md`.
>
> Then write a brief `reports/translation_comparison.md` that analyzes:
> - What specific claims differ between the two versions?
> - Which version would be more appropriate for each of these contexts:
>   a conference abstract, an FDA submission, a conversation with a patient?
>
> *Why this matters: the pressure to overstate AI performance in clinical contexts
> is real. Recognizing it and resisting it is a professional skill.*

---

## Discussion questions

- What is the difference between "research prototype" and "research-grade software"?
  Where does your prototype sit?
- Why does the prompt say "do not describe the prototype as ready for deployment"
  rather than just "be honest"?
- What ethical obligations do you have when communicating AI system limitations
  to a clinical collaborator who may not understand the technical caveats?
