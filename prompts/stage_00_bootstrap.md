# Mission 0 — Wake the Lab

## What this mission is about

Before any scientific work can begin, your tool chain must be operational.
This mission confirms that Python, the package environment, and the lab's
output structure are all working — and teaches you the first pattern you
will use throughout the course: **prompt → artifact → inspect**.

---

## Prompt Principle: Explicit task + expected output

Naming the exact output file and its required structure in your prompt is
not micromanagement — it is a specification. Without explicit paths and
key names, Claude may write outputs anywhere or skip them. With an explicit
contract, the output becomes independently verifiable.

---

## Layer A — Base Prompt

> I am beginning a medical AI research lab on this machine.
>
> Please complete the following steps in order and report what you find at each step:
>
> 1. Read `CLAUDE.md` and give me a two-sentence summary of what this lab is for
>    and what my role is versus yours.
>
> 2. Check that the following Python packages are importable and print their versions
>    where available: numpy, matplotlib, pathlib, json.
>    If any are missing, tell me what to install.
>
> 3. Make sure the following output directories exist. Create any that are missing:
>    - `outputs/status/`
>    - `outputs/figures/`
>    - `outputs/metrics/`
>    - `reports/`
>
> 4. Write a brief environment summary to `reports/env_check.md` that includes:
>    - Python version and platform
>    - Which packages are available
>    - Any issues or concerns
>
> 5. Write a status file to `outputs/status/stage_00_bootstrap.json` with this structure:
>    `{"status": "ok", "python_version": "X.Y.Z", "platform": "..."}`
>    If something failed, use `"status": "error"` and explain the problem.
>
> Show me the content of both output files and confirm they were written successfully.

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `reports/env_check.md` | Python version, platform, package status, any issues |
| `outputs/status/stage_00_bootstrap.json` | `{"status": "ok", "python_version": "...", "platform": "..."}` |

---

## Layer B — Reflection Prompt

> Now that the lab is running, help me understand what I am working with.
>
> Explain this repository to me as if I were a new research fellow joining the project:
> - What does each top-level folder contain and what is its purpose in the pipeline?
> - What is my role versus your role throughout this lab?
> - What is the most important thing I should understand before beginning Mission 1?
> - Is there anything about the current environment or setup that concerns you?

---

## Layer C — Exploration Challenge

> Extend the environment check to include hardware context:
>
> - Check whether a GPU is available (try `import torch; torch.cuda.is_available()`).
>   If torch is not installed, note that.
> - Check approximate available RAM using `psutil` if available.
> - Check disk space available in the current directory.
>
> Update `reports/env_check.md` to include this additional context.
> Do not fabricate values — if something cannot be checked, say so explicitly.
>
> *Why this matters: pipeline training time and memory requirements depend on hardware.
> An honest hardware summary is the first step toward realistic timeline estimation.*

---

## Discussion questions

- What does `"status": "ok"` in the status file guarantee? What does it *not* guarantee?
- Why does the prompt name the exact JSON keys (`python_version`, `platform`) rather than
  just saying "write a status file"?
- What would happen to downstream grading checks if `outputs/status/stage_00_bootstrap.json`
  was missing or had `"status": "error"`?
