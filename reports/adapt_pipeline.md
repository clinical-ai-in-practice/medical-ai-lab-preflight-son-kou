# Adapt Pipeline — Day 2 Challenge

Dataset: ?
Modality: FLAIR (channel 3), per-slice normalised to [0, 255]
Slices evaluated: 10

---

## Change Made

**Replaced the fixed intensity threshold with per-slice Otsu adaptive thresholding, combined with the largest-CC post-processing step from Day 1.**

Both pipelines include the largest-CC post-processing step from Day 1.
The only variable is how the threshold is selected:

- **Baseline**: fixed threshold t = 0.5 (applied to every slice)
- **Day 2**: per-slice Otsu threshold computed from the intensity histogram

---

## Motivation

The Day 1 error analysis (Stage 04) identified that the fixed threshold was
sensitive to slice-level intensity variation — the Dice gap between the best
and worst slice was large.  Otsu's method addresses this by finding the
optimal threshold for each slice independently, removing the assumption that
a single global constant calibrates correctly for all slices.

Reference: Otsu, N. (1979). A threshold selection method from gray-level
histograms. IEEE Transactions on Systems, Man, and Cybernetics, 9(1), 62–66.

---

## Results

| Pipeline | Mean Dice |
|---|---|
| Fixed threshold (t=0.5) + CC | 0.5917 |
| Otsu per-slice + CC | 0.5657 |
| Delta | -0.0259 |

Otsu threshold statistics across 10 slices:
- Mean: 0.4034
- Std:  0.1058
- Min:  0.2041
- Max:  0.5371

See: `outputs/figures/challenge_comparison.png`
Representative slice: 1
(selected as the slice where the two methods differed most)

---

## Interpretation

The Day 2 adaptation degraded the mean Dice score.

Per-slice Otsu thresholding did not outperform the fixed threshold on this pack (Δ = -0.0259). The Otsu thresholds varied (mean 0.403 ± 0.106); on slices with poorly separated intensity modes, Otsu can set a threshold that includes too much background or misses sparse tumour pixels. This is a valid, informative finding: the assumption that intensity histograms are bimodal does not hold uniformly across this dataset.

---

## What to Take Away

1. **Adaptive thresholding is not always better.** Otsu's method makes an
   assumption (bimodal histogram) that may not hold for every slice in a
   medical image dataset.  The empirical comparison is the only reliable judge.

2. **Fair comparisons require controlled conditions.** Both pipelines here use
   the same CC post-processing step, the same slices, and the same GT masks.
   The only variable is the threshold selection method — that is what we are
   measuring.

3. **Per-slice statistics are informative.** Reporting the distribution of
   Otsu thresholds (mean ± std) tells us whether the dataset has consistent
   or variable intensity calibration — information that a fixed threshold
   cannot reveal.

4. **Next steps.** If performance is still limited, the next candidate
   improvements are: (a) a learned classifier that uses local texture features
   rather than global intensity, (b) 3-D context (adjacent slices), or (c)
   a stronger spatial prior (morphological operations, atlas-based priors).
