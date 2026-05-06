# Error Analysis

Dataset: ?
Modality: FLAIR (channel 3), per-slice normalised to [0, 255]
Threshold used: 0.5
Slices analysed: 10

## Method

Each slice is segmented with the same intensity threshold (0.5) used in the
baseline. We compute Dice between the thresholded prediction and the ground-truth
mask, then rank slices from best to worst.

## Best Case — Slice 3  (Dice = 0.8697)

| Metric | Value |
|---|---|
| Ground-truth positives | 2705 px |
| True positives (TP) | 2139 px |
| False positives (FP) | 75 px |
| False negatives (FN) | 566 px |

The prediction closely matches the ground truth on this slice.
The tumour pixels have a noticeably higher intensity than background, making
the fixed threshold effective. This is the kind of slice the baseline is
well-suited to.

See: `outputs/figures/error_analysis_best.png`

## Worst Case — Slice 9  (Dice = 0.0437)

| Metric | Value |
|---|---|
| Ground-truth positives | 965 px |
| True positives (TP) | 113 px |
| False positives (FP) | 4088 px |
| False negatives (FN) | 852 px |

The dominant error is **false positives** — the model predicts tumour where there is none. The intensity threshold is too permissive for this slice.

See: `outputs/figures/error_analysis_worst.png`

## Reflection

The performance gap between best and worst case is 0.8259
(best Dice = 0.8697, worst = 0.0437, overall mean = 0.5741).

A fixed intensity threshold is brittle because it does not use any spatial
context — it treats every pixel independently. The cases where it fails
most severely are slices where the tumour intensity distribution overlaps
with healthy tissue.

**Suggested experiment for Stage 05:**
A spatial post-processing step — such as keeping only the largest connected
component of the prediction — could reduce isolated false-positive predictions
without needing a fundamentally different model. Stage 05 will test this.
