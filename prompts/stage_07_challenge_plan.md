# Stage 07 — Challenge Plan

## Goal
Before writing any code, produce a concrete written plan for the Day 2
challenge: replacing the fixed threshold with per-slice Otsu adaptive
thresholding.  Planning before acting is a required step.

## What to ask Claude Code

> "Run `make challenge-plan`. Then open `reports/challenge_plan.md` and tell me:
> - what weakness in the Day 1 baseline the plan is targeting
> - why Otsu's method is the proposed solution
> - what the comparison will control for (what stays the same)
> - what the two main risks are
> Does the plan look grounded in the actual Day 1 numbers?"

## What this stage produces

| Artifact | Description |
|---|---|
| `reports/challenge_plan.md` | Written plan grounded in Day 1 metrics — weakness, proposed change, risks, success criteria |
| `outputs/status/stage_07_challenge_plan.json` | `{"status":"ok","proposed_change":"...","baseline_dice":…}` |

## Check

```bash
make challenge-plan
# Prints: identified weakness, proposed Day 2 change
# Open: reports/challenge_plan.md — confirm it references real Day 1 Dice numbers
```

## Discussion questions

- Does the plan commit to a fair comparison? What stays constant between
  the baseline and the Day 2 adaptation?
- Otsu's method assumes a bimodal intensity histogram. Which slices in the
  teaching pack are most likely to violate that assumption?
- If you had three more hours, what other threshold strategies would you
  consider and why?
- What would a failed experiment look like, and how would you report it?

## What comes next

Stage 08 implements the plan. Stage 09 writes the clinical translation memo.
