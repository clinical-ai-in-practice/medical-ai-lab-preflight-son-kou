# Error Analysis

Dataset: BraTS_teaching_pack
Modality: FLAIR
Threshold used: 0.5
Slices analysed: 20

## Method

Each slice is segmented with the same intensity threshold (0.5) used in the
baseline. We compute Dice between the thresholded prediction and the ground-truth
mask, then rank slices from best to worst.

## Best Case — Slice 15  (Dice = 0.2570)

| Metric | Value |
|---|---|
| Ground-truth positives | 373 px |
| True positives (TP) | 333 px |
| False positives (FP) | 1885 px |
| False negatives (FN) | 40 px |

The prediction closely matches the ground truth on this slice.
The tumour pixels have a noticeably higher intensity than background, making
the fixed threshold effective. This is the kind of slice the baseline is
well-suited to.

See: `outputs/figures/error_analysis_best.png`

## Worst Case — Slice 8  (Dice = 0.0339)

| Metric | Value |
|---|---|
| Ground-truth positives | 69 px |
| True positives (TP) | 36 px |
| False positives (FP) | 2022 px |
| False negatives (FN) | 33 px |

The dominant error is **false positives** — the model predicts tumour where there is none. The intensity threshold is too permissive for this slice.

See: `outputs/figures/error_analysis_worst.png`

## Reflection

The performance gap between best and worst case is 0.2232
(best Dice = 0.2570, worst = 0.0339, overall mean = 0.1209).

A fixed intensity threshold is brittle because it does not use any spatial
context — it treats every pixel independently. The cases where it fails
most severely are slices where the tumour intensity distribution overlaps
with healthy tissue.

**Suggested experiment for Stage 05:**
A spatial post-processing step — such as keeping only the largest connected
component of the prediction — could reduce isolated false-positive predictions
without needing a fundamentally different model. Stage 05 will test this.
