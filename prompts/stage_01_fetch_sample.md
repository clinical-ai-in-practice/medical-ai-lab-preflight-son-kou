# Mission 1 — Receive the Signal

## What this mission is about

You cannot evaluate a model on data you have not inspected. This mission
locates the teaching dataset, confirms its basic structure, and verifies
that it is intact and ready for the pipeline. **Receiving and validating
data is a scientific act, not just a download step.**

---

## Prompt Principle: File permission scope + state assertion

Telling Claude which files it may touch prevents unintended side effects.
Asserting expected state ("confirm N slices were loaded") forces explicit
validation rather than silent completion. A prompt that specifies *what
Claude should verify* is more reproducible than one that just says "fetch the data."

---

## Layer A — Base Prompt

> I need to load the medical imaging teaching dataset for this lab.
>
> Please complete the following steps and report at each one:
>
> 1. Read `data/teaching_pack.cfg` and tell me:
>    - What data source it is configured to use (local path or URL)
>    - Whether that source is currently accessible from this machine
>
> 2. Fetch the data sample by running `scripts/fetch_data.py`.
>    This script should load imaging data into `data/sample/`.
>    If the script needs modifications to work with the configured source, make them.
>
> 3. Confirm that `data/sample/` contains imaging data. Tell me:
>    - How many image slices or cases were loaded
>    - What file format they are in
>    - The approximate size of the loaded data on disk
>
> 4. Write a status file to `outputs/status/stage_01_fetch_sample.json` with:
>    `{"status": "ok", "dataset": "<name>", "n_slices": N, "modality": "...", "source": "...", "pack_path": "..."}`
>
> Do not generate or invent synthetic data unless I explicitly say to.
> Tell me clearly what the data source is and whether the real teaching pack was loaded.

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `data/sample/` | At least one image file and one mask file |
| `outputs/status/stage_01_fetch_sample.json` | `{"status": "ok", "dataset": "...", "n_slices": N, "modality": "...", "source": "...", "pack_path": "..."}` |

---

## Layer B — Reflection Prompt

> Looking at the dataset you just loaded:
>
> - What type of medical imaging data is this? (modality, anatomy if visible)
> - How many cases or slices does the teaching pack contain?
> - What format are the image files? (numpy array, NIfTI, DICOM, etc.)
> - What would you need to check before trusting this data for model evaluation?
> - Is there anything about the data structure that might cause problems in later stages?
>
> Be specific — reference actual file names, shapes, or sizes where you can.

---

## Layer C — Exploration Challenge

> Inspect the data more deeply:
>
> - Load the first image array. What is its shape, dtype, and value range (min, max)?
> - Load the corresponding mask. What fraction of pixels are foreground (value > 0)?
> - Do the image and mask have compatible shapes?
>
> Write these statistics as a preliminary data characterization section at the top of
> `reports/data_notes.md`. Use factual language — do not speculate about anatomy unless
> you can see it from file metadata.
>
> *Why this matters: unexpected image shapes or value ranges are a common source of
> silent errors in segmentation pipelines.*

---

## Discussion questions

- Why does the prompt say "do not generate synthetic data unless I say to"?
  What would happen to downstream evaluation if Claude silently created fake data?
- What is the difference between `n_slices` being 0 versus the status file being missing?
- Why does the prompt ask Claude to check whether the source is "accessible" rather
  than just assuming the script will handle that?
