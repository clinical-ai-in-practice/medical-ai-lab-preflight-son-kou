# Stage 07 — Challenge Plan
## Mission 5: Design the Next Study

## Goal

Before writing any code, produce a concrete written plan for the Day 2 challenge:
replacing the fixed threshold with per-slice Otsu adaptive thresholding.

Research planning is a distinct skill from execution. A written plan forces clarity
about what you believe and why — before you commit to any implementation.
Planning before acting is a required step, not a formality.

## Layer A — Base prompt

> "Run `make challenge-plan`. Then open `reports/challenge_plan.md` and tell me:
> - what weakness in the Day 1 baseline the plan is targeting
> - why Otsu's method is the proposed solution for that weakness
> - what the comparison will control for (what stays the same between baseline and Day 2)
> - what the two main risks are if the assumption turns out to be wrong
> Does the plan look grounded in the actual Day 1 Dice numbers, or is it generic?"

## What this stage produces

| Artifact | Description |
|---|---|
| `reports/challenge_plan.md` | Written plan: weakness identified, proposed change, controlled comparison, risks, success criteria |
| `outputs/status/stage_07_challenge_plan.json` | `{"status":"ok","proposed_change":"...","baseline_dice":…}` |

## Files

**Allowed to edit:** `scripts/challenge_plan.py`, `reports/challenge_plan.md`

**Protected — do not modify:** `reports/day1_summary.md` (Day 1 record — do not overwrite),
all `outputs/metrics/` from Day 1, `tests/`, `artifacts/schema.json`, `prompts/`

## Check

```bash
make challenge-plan
# Prints: identified weakness, proposed Day 2 change
# Open: reports/challenge_plan.md — confirm it references actual Day 1 Dice numbers
```

**What to inspect manually:**
- Does `reports/challenge_plan.md` include the `# Day 2 Challenge Plan` header? (grading requires it)
- Does the plan reference a specific Day 1 Dice value — not a generic description?
  If the plan reads as if it could have been written without running Day 1, it is not grounded.
- Does the plan identify what "success" looks like for the Day 2 experiment?

## Layer B — Reflection prompt

After reviewing the plan, ask Claude:

> "Test this plan for scientific rigour:
> - Is the comparison fair? What exactly will be held constant between the Day 1 baseline
>   and the Day 2 Otsu-based approach?
> - Otsu's method assumes a bimodal intensity histogram. Does the data we saw in Stage 02
>   support that assumption? Which slices are most likely to violate it?
> - What would a negative result look like — and how would you report it honestly?
> Add a section called '## Success criteria and failure conditions' to `reports/challenge_plan.md`
> that addresses these questions in concrete terms."

## Layer C — What you can customize

Ask Claude: "What other threshold strategies could we have chosen instead of Otsu's method?"
Then ask it to write a one-paragraph rationale for why Otsu was selected over each alternative.
This is not required for grading but is a good scientific exercise — and makes the final
translation memo stronger.

## Discussion questions

- Does the plan commit to a fair comparison? What stays constant between the baseline
  and the Day 2 adaptation, and what changes?
- Otsu's method assumes a bimodal intensity histogram. For which slices in this dataset
  is that assumption most likely to fail — and does that matter for interpreting the result?
- What would a failed Day 2 experiment look like, and how would you report it differently
  from a succeeded one?

## What comes next

Stage 08 implements the plan exactly as written. If the implementation deviates from the plan,
you should update `reports/challenge_plan.md` to reflect what was actually done.
Stage 09 then assembles the final clinical translation memo using all Day 1 and Day 2 results.
