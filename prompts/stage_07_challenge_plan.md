# Mission 5 — Design the Next Study (Part 1): Research Plan

## What this mission is about

Before writing any code, write the plan. Research planning is a distinct skill
from execution. A written study design forces clarity about what you believe
before you commit to implementation — and gives you something to compare against
when the result arrives.

This mission teaches **structured study design**: not just "what will I try next"
but "what question am I asking, what would count as an answer, and what could
make me wrong."

---

## Prompt Principle: Plan before code

Asking Claude to write a structured plan first — before any implementation —
forces it to reason through the approach and surface assumptions. The plan
becomes the check on whether the implementation drifted from intent.
Code written without a plan is hard to evaluate. Code written after a plan
is testable against it.

---

## Layer A — Base Prompt

> Based on everything from Day 1, I need to design a study plan for Day 2.
> Before writing any code, I want a structured research design document.
>
> Please do the following:
>
> 1. Read `reports/day1_summary.md` and `reports/error_analysis.md`.
>    Remind me of the open questions and the hypothesis that was not fully resolved.
>
> 2. Write a Day 2 Challenge Plan to `reports/challenge_plan.md` using this structure:
>
>    `# Day 2 Challenge Plan`
>
>    `## Identified Weakness`
>    What specific limitation of the Day 1 pipeline are you targeting?
>    Cite evidence from the error analysis.
>
>    `## Research Question`
>    State the question as: "Does [intervention X] improve [metric Y] compared to [baseline Z]
>    in [context C]?"
>
>    `## Proposed Method`
>    What change to the pipeline will you make? Be specific: name the component,
>    the change, and why you expect it to help.
>
>    `## What Would Count as Success`
>    A specific, measurable criterion. Example: "Dice improves by > 0.05 on the validation set."
>    Not: "performance gets better."
>
>    `## Risks and Failure Conditions`
>    What could go wrong? What would it mean if the result is negative?
>    Is there a result that would cause you to abandon this direction?
>
>    `## What I Would Try Next if This Fails`
>    Name one alternative direction.
>
> 3. Write a status file to `outputs/status/stage_07_challenge_plan.json`:
>    `{"status": "ok", "identified_weakness": "...", "proposed_change": "..."}`
>
> The plan should be analytical. "Try a better model" is not a research question.
> "Does replacing the threshold with a learned U-Net decoder improve Dice by >0.05
> on the FLAIR segmentation task?" is a research question.

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `reports/challenge_plan.md` | All 6 sections, > 200 chars, `# Day 2 Challenge Plan` header |
| `outputs/status/stage_07_challenge_plan.json` | `{"status": "ok", "identified_weakness": "...", "proposed_change": "..."}` |

---

## Layer B — Reflection Prompt

> Read `reports/challenge_plan.md` from the perspective of two different reviewers:
>
> **As a methods reviewer:** Is the proposed method change specific enough to be reproducible?
> If someone else read this plan, could they implement the same experiment?
>
> **As a devil's advocate:** What is the strongest argument that this plan will fail?
> What assumption in the plan is most likely to be wrong?
> What would you change about the study design to make it more robust?
>
> Update `reports/challenge_plan.md` with a `## Critique Response` section that
> addresses the strongest objections to the plan.

---

## Layer C — Exploration Challenge

> Extend the study design with a **role-switching exercise**:
>
> Ask Claude to answer these two questions in separate paragraphs in the report:
>
> *As the algorithm designer:* What is the most technically promising change you
> could make to improve performance on the identified weakness?
>
> *As a clinical safety reviewer:* What change from the day 1 pipeline would you
> most want validated before this system gets closer to clinical use?
>
> Do the two perspectives agree on what to prioritize? If not, how would you
> decide between them?
>
> Add a `## Perspective Analysis` section to `reports/challenge_plan.md` with this content.
>
> *Why this matters: in clinical AI, technical performance and clinical safety are
> different optimization objectives. Recognizing when they conflict is essential.*

---

## Discussion questions

- What is the difference between a "proposed change" and a "research question"?
  Why does the structure ask for both?
- The "Risks and Failure Conditions" section asks what a negative result would mean.
  Why is this important to think about *before* running the experiment?
- How does writing "What Would Count as Success" before running the experiment
  protect against p-hacking or motivated reasoning?
