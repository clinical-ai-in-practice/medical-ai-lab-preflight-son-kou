# Stage 02 — Load & Visualize
## Mission 1: First Look at the Data

## Goal

Load the teaching dataset and produce a labeled overlay figure — the first visual artifact
of the lab. More importantly, use this figure to make your first evidence-based observation
about the data: what does the anatomy look like, how clear is the boundary between target
and background, and what challenges does the image quality suggest for segmentation?

Visualization is not decoration. It is the first act of scientific investigation.

## Layer A — Base prompt

> "Run `make visualize`. Then open `outputs/figures/sample_overlay.png` and
> `reports/data_notes.md`. Explain to me in plain language:
> - what the image shows (anatomy, modality, approximate resolution)
> - how the ground-truth mask was drawn — does it look clean or noisy at the boundary?
> - what the most difficult aspect of this dataset looks like for a segmentation algorithm
> - whether there is anything surprising or unusual about this particular sample"

## What this stage produces

| Artifact | Description |
|---|---|
| `outputs/figures/sample_overlay.png` | Overlay figure: image with ground-truth mask contour |
| `reports/data_notes.md` | Written data description: modality, anatomy, boundary quality, initial observations |
| `outputs/status/stage_02_load_visualize.json` | `{"status":"ok","figure":"sample_overlay.png"}` |

## Files

**Allowed to edit:** `scripts/visualize_sample.py`, `reports/data_notes.md`

**Protected — do not modify:** `data/sample/`, `tests/`, `artifacts/schema.json`, `prompts/`

## Check

```bash
make visualize
# Expected: prints path to saved figure without error
# Then verify:
ls -lh outputs/figures/sample_overlay.png   # should be non-empty
cat reports/data_notes.md
```

**What to inspect manually:**
- Open `outputs/figures/sample_overlay.png` — can you clearly see the image and the mask overlay?
- Read `reports/data_notes.md` — does it reflect what you actually see in the figure?
  If the report says the boundary is "clean" but the figure shows jagged edges, that is a problem.

## Layer B — Reflection prompt

After reviewing the figure and the report, ask Claude:

> "Based on what you can see in the overlay figure and the data_notes report:
> - What threshold strategy would you expect to work best on this data and why?
> - What failure mode would you predict for a simple intensity threshold on this dataset?
> - If you had to describe this dataset to a radiologist, what would you say?
> Write your answers as an addition to `reports/data_notes.md` under a heading called
> '## Initial Hypothesis'."

## Layer C — What you can customize

Ask Claude to show you a different slice from the teaching pack — either the first slice,
the middle slice, or a slice you choose. Does the anatomy look consistent across slices?
This is a good early sanity check before committing to the full pipeline.

## Discussion questions

- Does the ground-truth mask boundary look hand-drawn or algorithmically generated?
  Why does this matter for how you interpret your Dice score later?
- If the image has poor contrast between target and background, what does that predict
  about the baseline model's performance in Stage 03?
- What is the difference between a good visualization and a useful one?
  Is `sample_overlay.png` useful for making a scientific decision?

## What comes next

Stage 03 trains the first baseline model on this dataset and produces the first
quantitative metric. The observations you made here will directly motivate how
you interpret that metric in Stage 03.
