# Mission 2 — Build the First Detector (Part 1): Inspect the Data

## What this mission is about

Visualization is not decoration — it is the first act of scientific investigation.
Before training any model, you need to see the data: what the anatomy looks like,
how clean the ground-truth mask boundary is, and what challenges the image quality
presents for a segmentation algorithm.

---

## Prompt Principle: Inspect before you act

Asking Claude to analyze and describe an artifact *before* taking action grounds
its subsequent work in evidence. A prompt that says "visualize, then interpret"
produces a more useful artifact than one that says "visualize." The interpretation
is as important as the figure.

---

## Layer A — Base Prompt

> I have a medical imaging dataset in `data/sample/`. I need to visualize it
> and record my first scientific observations.
>
> Please do the following:
>
> 1. Load the sample image and mask from `data/sample/`.
>    Show me their shapes, data types, and value ranges before doing anything else.
>
> 2. Create a visualization that overlays the ground-truth mask contour on the image.
>    Save it to `outputs/figures/sample_overlay.png`.
>    The figure should be clear enough that I can see both the anatomy and the mask boundary.
>
> 3. After creating the figure, tell me in plain language:
>    - What the image shows (anatomy, imaging modality, approximate resolution)
>    - How clean or noisy the mask boundary looks
>    - What looks most challenging about this dataset for a segmentation algorithm
>    - Anything surprising or unusual
>
> 4. Write these observations to `reports/data_notes.md` with a "## Data Observations" section.
>
> 5. Write a status file to `outputs/status/stage_02_load_visualize.json` with:
>    `{"status": "ok", "figure": "sample_overlay.png"}`

---

## Required outputs

| File | Minimum content |
|------|-----------------|
| `outputs/figures/sample_overlay.png` | Image with mask overlay, non-empty |
| `reports/data_notes.md` | Written observations: modality, anatomy, boundary quality, challenges |
| `outputs/status/stage_02_load_visualize.json` | `{"status": "ok", "figure": "sample_overlay.png"}` |

---

## Layer B — Reflection Prompt

> Look at `outputs/figures/sample_overlay.png` and the notes in `reports/data_notes.md`.
>
> Put yourself in the role of a **skeptical peer reviewer** evaluating this dataset:
> - Would you trust this ground-truth mask for training? What evidence supports or undermines that trust?
> - What annotation artifacts or biases might be present?
> - If you were designing a segmentation algorithm for this data, what is your biggest concern?
> - What additional data or metadata would you want before proceeding to model training?

---

## Layer C — Exploration Challenge

> Extend the visualization to give a more complete picture:
>
> - Create a second figure showing at least 3 different image slices side by side
>   (if the dataset has multiple slices), each with its mask overlay.
>   Save it to `outputs/figures/multi_slice_overview.png`.
> - For each slice, note its mask foreground fraction. Does coverage vary across slices?
>
> Update `reports/data_notes.md` with this multi-slice characterization.
>
> *Why this matters: a single-slice visualization can be unrepresentative.
> Variation across slices reveals dataset heterogeneity.*

---

## Discussion questions

- Why does the prompt ask Claude to report shapes and value ranges *before* creating the figure?
- What is the difference between a "clean" and a "noisy" mask boundary for model training?
- If `sample_overlay.png` is created but `data_notes.md` is empty or trivial,
  has this mission succeeded? Why or why not?
