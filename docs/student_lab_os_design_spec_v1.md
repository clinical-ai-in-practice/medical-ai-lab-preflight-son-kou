# Student Lab OS Design Spec v1

## 1. Product Definition

### 1.1 Name

**Student Lab OS**
A prompt-driven, dashboard-guided, artifact-based research training environment for a PhD-level Medical AI summer school.

### 1.2 One-sentence definition

Students use **VS Code + Claude Code** to drive the lab through structured prompts, while a **local dashboard** gives them mission guidance, feedback, progress, artifacts, and submission readiness.

### 1.3 Core promise

Students do **not** need traditional programming fluency to participate in high-level medical AI experimentation.
They learn to use **prompts as experimental instruments**, and to judge results through artifacts, metrics, and scientific reasoning.

---

## 2. Core Principles

### 2.1 Prompt-first

Every mission, including environment setup, data access, visualization, modeling, and reporting, must be executable through Claude prompts.

### 2.2 Dashboard-first feedback

The dashboard is the student’s navigation and feedback console.
It is **not** the Claude chat interface.
The actual Claude interaction happens in **VS Code + Claude Code**.

### 2.3 Artifact-driven learning

Students are not graded on chat output.
They are graded on:

- files produced
- metrics generated
- comparisons made
- reports written
- reflections grounded in evidence

### 2.4 Serious but motivating

The course should feel like a real research mission:

- intellectually serious
- narratively engaging
- visually motivating
- rich in immediate feedback
- not childish
- not startup-like

### 2.5 Safe autonomy

Students should have freedom to iterate, but the system should prevent them from destroying the repo or drifting too far from the lab structure.

### 2.6 End-to-end continuity

The lab should feel like one coherent research journey, not disconnected exercises.

---

## 3. Course Structure Model

## 3.1 Repo model

Use **one all-in-one student lab repo** containing all missions.

## 3.2 Classroom model

Use **two GitHub Classroom assignments** backed by the same template repo:

- **Preflight Assignment**
- **Main Lab Assignment**

This preserves end-to-end continuity while reducing classroom risk.

## 3.3 Student experience model

Students should experience the repo as:

- one continuous lab world
- one mission map
- one progress system
- one artifact history
- one dashboard

---

## 4. User Experience Model

## 4.1 Student workflow

The primary student loop is:

1. Open dashboard
2. See current mission
3. Read framing and objective
4. Copy or adapt the current prompt
5. Go to VS Code + Claude Code
6. Run the prompt-driven task
7. Return to dashboard
8. Inspect new outputs, metrics, and feedback
9. Check if mission is complete
10. Create checkpoint commit and push

## 4.2 Division of roles

### VS Code + Claude Code

- where action happens
- where prompts are executed
- where code is created or modified
- where scripts run

### Student dashboard

- where orientation happens
- where prompt guidance is shown
- where artifacts are visualized
- where progress and evaluation are shown
- where students see whether they are on track

---

## 5. Narrative Model

## 5.1 Narrative tone

Use a **clinical research mission** tone:

- high-stakes but educational
- future-facing but plausible
- motivating without becoming a game parody

## 5.2 Narrative frame

Students are positioned as:

- junior clinical AI investigators
- research fellows in a translational imaging lab
- AI-assisted PhD trainees solving a real research task

## 5.3 Narrative function

Narrative is used to:

- create motivation
- reduce intimidation
- reinforce mission logic
- make progress feel meaningful

Narrative is **not** used to trivialize the science.

## 5.4 Visual style

Recommended visual identity:

- dark theme
- clean scientific UI
- subtle retro / mission-console elements
- badge / mission card aesthetics
- optional pixel / comic accents in small doses only

---

## 6. Mission Architecture

## 6.1 Top-level missions

The lab is organized into missions, not merely scripts.

### Mission 0 — Wake the Lab

Goal:

- environment setup
- Claude readiness
- repo readiness
- first prompt-driven success

### Mission 1 — Receive the Signal

Goal:

- fetch teaching pack
- inspect dataset
- first data understanding
- first image exposure

### Mission 2 — Build the First Detector

Goal:

- baseline visualization and segmentation/modeling
- first meaningful metric
- first research artifact set

### Mission 3 — Investigate Failure

Goal:

- best/worst case analysis
- error maps
- failure interpretation
- explicit hypothesis formation

### Mission 4 — Improve With Intent

Goal:

- one controlled improvement
- measured comparison
- scientific reasoning over blind tweaking

### Mission 5 — Design the Next Study

Goal:

- Day 2 challenge planning
- propose a new strategy
- adapt the pipeline

### Mission 6 — Translate Responsibly

Goal:

- move from experiment to research judgment
- clinical gap
- product gap
- human oversight and validity discussion

### Bonus Missions

Optional, unlocked after core completion:

- alternate hypothesis
- unoptimized data pack
- custom research question
- compare prompt strategies
- alternate translation memo for clinic vs startup vs paper

---

## 7. Prompt Architecture

## 7.1 Prompt types

Each mission contains three prompt layers.

### Layer A — Base Prompt

Provided by the course.
Used to reliably start the mission.

### Layer B — Reflection Prompt

Prompts students to inspect results, interpret outputs, and identify weaknesses.

### Layer C — Student-customized Prompt

Student edits or extends the prompt to improve clarity, control, or scientific reasoning.

## 7.2 Prompt rules

Prompts should always state:

- mission goal
- files Claude may edit
- files Claude should avoid
- expected outputs
- completion criteria
- what the student must inspect manually

## 7.3 Prompt literacy goal

Students should learn:

- prompts are not magic
- prompts are experimental instructions
- better prompts improve experimental control
- prompts must be grounded in evidence and outputs

---

## 8. Run History and Prompt Versioning

## 8.1 Problem being solved

Students will iterate prompts many times.
Without a clear system, they may:

- lose track of what changed
- confuse results
- damage the repo
- struggle to explain decisions

## 8.2 Proposed model

Use **Prompt Ledger + Run Snapshot**.

Each meaningful run should create a structured record:

- prompt text
- prompt type
- timestamp
- mission
- changed files
- artifacts produced
- result summary
- notes
- commit hash if available

## 8.3 Recommended storage

```text
.lab_history/
  mission_02/
    run_001/
      prompt.md
      result.json
      notes.md
      changed_files.json
    run_002/
      ...
```

## 8.4 Dashboard representation

For each mission, dashboard shows:

- run timeline
- prompt versions
- outcome changes
- metric differences
- what improved / worsened

## 8.5 Versioning model

Do **not** rely on git branches as the primary student experience.
Use:

- run snapshots for experimental memory
- checkpoint commits for durable save points
- git push for classroom supervision

---

## 9. Soft Sandbox Model

## 9.1 Purpose

Prevent students from wrecking the repo while preserving autonomy.

## 9.2 File edit constraints

Claude should be allowed to edit only specific mission-relevant files by default.

### Allowed to edit

- mission workspace files
- selected scripts
- reports
- outputs
- student notes

### Protected / discouraged

- tests
- grading contract files
- GitHub workflow files
- dashboard core files
- key config files
- mission definitions

## 9.3 Mission-level allowed files

Each mission explicitly declares:

- Allowed files
- Protected files
- Expected outputs

## 9.4 Reset model

Each mission should support a “reset mission state” action that:

- restores mission-editable scaffold files if needed
- clears mission-specific outputs
- preserves history where possible

## 9.5 Checkpoint model

After each meaningful mission completion, dashboard should recommend:

- create checkpoint commit
- push to classroom

---

## 10. Student Dashboard Information Architecture

## 10.1 Dashboard role

The dashboard is a **Student Command Center**.

It should not be the coding environment.
It should be the place where students understand:

- where they are
- what to do
- what changed
- whether they are succeeding

## 10.2 Top-level tabs

### Tab 1 — Mission Map

Shows:

- all missions
- current mission
- completion status
- unlock state
- bonus availability
- overall progress

### Tab 2 — Prompt Studio

Shows:

- base prompt
- reflection prompt
- student-customized prompt notes
- run history
- prompt/result comparisons

### Tab 3 — Workflow

Shows:

- current mission stages
- required artifacts
- expected outputs
- allowed files
- progress state
- stage checklist

### Tab 4 — Results

Shows:

- figures
- metrics
- comparisons
- best/worst cases
- summaries
- memo outputs

### Tab 5 — Evaluation

Shows:

- visible checks
- mission completion checklist
- required artifact status
- submission readiness
- bonus status
- feedback summary

### Tab 6 — Story / Context

Shows:

- mission framing
- why this mission exists
- hints
- common pitfalls
- bonus quests
- FAQ

---

## 11. Mission Page Structure

Each mission page should contain five consistent blocks:

### 11.1 Story / Framing

Why this mission matters scientifically and pedagogically.

### 11.2 Prompt

Base prompt, reflection prompt, and prompt guidance.

### 11.3 Run / Execute

Instructions for what to do in VS Code + Claude Code.

### 11.4 Inspect

Artifacts, figures, metrics, logs, run comparisons.

### 11.5 Evaluate / Submit

Checklist, pass state, missing requirements, checkpoint recommendation, push recommendation.

---

## 12. Evaluation Model

## 12.1 What is graded

Primary grading inputs:

- generated artifacts
- metrics
- comparison files
- reports
- memo quality
- prompt-result coherence

## 12.2 What is not graded directly

- chat verbosity
- raw code complexity
- whether students wrote code manually
- superficial polish

## 12.3 Evaluation layers

### Layer 1 — Automatic

- files exist
- schema valid
- metrics in plausible range
- stage completed
- reports non-trivial

### Layer 2 — Interpretive

- error analysis quality
- controlled improvement rationale
- challenge plan quality
- translation memo quality

### Layer 3 — Bonus

- optional challenge completion
- originality
- thoughtful prompt iteration

---

## 13. Commit and Push Model

## 13.1 Why frequent push matters

Frequent push enables:

- teacher-side monitoring
- TA intervention
- progress awareness
- auditability
- less student drift

## 13.2 Required cadence

Minimum:

- one push per completed mission

Preferred:

- one checkpoint push per meaningful run cluster

## 13.3 Dashboard guidance

At mission completion, dashboard should show:

- ready to checkpoint
- ready to push
- suggested commit prompt

## 13.4 Prompt-based git interaction

Students can still use Claude for git operations, e.g.:

- create checkpoint commit
- summarize mission progress
- push current work

This keeps the workflow prompt-first.

---

## 14. Teacher / Student / Classroom Relationship

## 14.1 Teacher repo

Teacher repo is:

- advanced
- demo-driven
- dashboard-driven
- supervision-driven
- materials-driven

## 14.2 Student repo

Student repo is:

- mission-driven
- prompt-driven
- guided
- simpler
- artifact-producing

## 14.3 GitHub Classroom

GitHub Classroom is the distribution and monitoring layer:

- template repo distribution
- assignment repo creation
- autograding
- feedback PRs
- progress visibility

---

## 15. Bonus System

## 15.1 Purpose

Bonus quests create:

- curiosity
- autonomy
- differentiation for strong students
- replayability

## 15.2 Bonus quest types

- alternate hypothesis
- harder data pack
- prompt comparison challenge
- custom research question
- translation challenge

## 15.3 Reward model

Rewards can be represented as:

- bonus badges
- mission completion markers
- optional leaderboard-free prestige markers
- special instructor discussion prompts

Do not make grading depend on bonus completion.

---

## 16. Non-goals

The Student Lab OS is **not**:

- a deployable clinical product
- a benchmark leaderboard system
- a full coding bootcamp
- a replacement for scientific judgment
- a pure game

---

## 17. Implementation Roadmap

## Phase 1 — Reframe current student repo

- preserve working pipeline
- convert stage language into mission language
- add mission map
- add prompt ledger
- add richer dashboard IA

## Phase 2 — Prompt-first dashboard integration

- dashboard shows prompts but does not execute Claude
- students use VS Code + Claude Code for action
- dashboard shows run history and outputs

## Phase 3 — Soft sandbox and checkpoint layer

- file edit constraints
- mission reset
- checkpoint support
- run snapshots

## Phase 4 — Narrative and bonus layer

- mission cards
- role framing
- bonus quests
- feedback polish

## Phase 5 — Classroom integration polish

- push cadence
- teacher dashboard aggregation
- final evaluation views
- feedback loops

---

## 18. Success Criteria

The Student Lab OS is successful if:

### Student side

- students can complete the lab without programming background
- students understand what each mission is for
- students can inspect what changed after each prompt
- students do not get lost or depressed by repo complexity

### Teacher side

- teacher can monitor progress meaningfully
- teacher can identify who is stuck
- teacher can discuss artifacts, not just submissions
- teacher can standardize grading

### Pedagogical side

- students learn to treat prompts as experimental instruments
- students learn to interpret outputs critically
- students learn that research quality depends on evidence, not AI confidence
