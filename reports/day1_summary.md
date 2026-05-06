# Day 1 Summary

## 1. Environment

- Python: 3.13.12
- Platform: macOS-26.3.1-x86_64-i386-64bit-Mach-O
- Bootstrap: completed ✓

## 2. Dataset

- Dataset: unknown
- Modality: FLAIR (channel 3), per-slice normalised to [0, 255]
- Slices in teaching pack: 10
- Location: `data/sample/imaging/`

## 3. Visualisation

Representative slice visualised with ground-truth mask overlay.
See: `outputs/figures/sample_overlay.png`

## 4. Baseline Segmentation

- Method: intensity threshold at 0.5
- Mean Dice across 10 slices: 0.5741 ± 0.2363

The baseline applies a fixed intensity threshold to each normalised MRI slice.
It is intentionally simple — its purpose is to establish a reproducible
reference point, not to achieve clinical performance.

## 5. Error Analysis

- Best case:  slice 3  Dice = 0.8697
- Worst case: slice 9  Dice = 0.0437

The gap between best and worst case quantifies how sensitive the threshold
method is to slice-level intensity variation. Slices where tumour pixels are
reliably bright outperform slices where intensity distributions overlap.

Figures: `outputs/figures/error_analysis_best.png`,
         `outputs/figures/error_analysis_worst.png`

## 6. Controlled Improvement

- Change: Post-processed threshold predictions by retaining only the single largest connected component per slice, discarding all smaller isolated regions.
- Baseline Dice: 0.5741
- New Dice:      0.5917
- Delta:         +0.0176  → improved

The experiment demonstrates how a single auditable change can be evaluated
with a fair comparison. Whether it helped, hurt, or changed nothing is
secondary — what matters is the reasoning and the honest reporting.

Figure: `outputs/figures/model_swap_comparison.png`

## 7. Open Questions for Day 2

1. **Better features.** Can a simple learned classifier outperform the threshold
   on the worst-case slices identified in Stage 04?

2. **Multi-class segmentation.** This pack uses binary masks. BraTS contains
   multiple sub-regions (enhancing tumour, oedema, necrotic core). What would
   change if we tried to predict them separately?

3. **Beyond Dice.** Hausdorff distance and surface Dice are commonly used in
   clinical contexts. How do our results look under those metrics?

4. **Generalisation.** All slices came from the same teaching pack. Would the
   threshold and post-processing choices transfer to a different scanner or
   patient population?

## 8. Completed Sections

- env_check ✓
- data_notes ✓
- train_notes ✓
- error_analysis ✓
- model_swap ✓


All required Day 1 figures are in `outputs/figures/`.
All required Day 1 metrics are in `outputs/metrics/`.
All required Day 1 reports are in `reports/`.
