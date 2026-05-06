# Model Swap — Largest Connected Component Post-Processing

Dataset: ?
Modality: FLAIR (channel 3), per-slice normalised to [0, 255]
Threshold: 0.5
Slices evaluated: 10

## Change Made

**Post-processed threshold predictions by retaining only the single largest connected component per slice, discarding all smaller isolated regions.**

## Rationale

The threshold baseline sometimes produces scattered small positive predictions that are unlikely to represent a real tumour. A spatial prior — that the target region should be one connected structure — can remove these false positives. This is a standard, interpretable post-processing step that adds no learned parameters and is easy to audit.

## Results

| Method | Mean Dice |
|---|---|
| Baseline (threshold = 0.5) | 0.5741 |
| Largest-CC post-processing | 0.5917 |
| Delta | +0.0176 |

See: `outputs/figures/model_swap_comparison.png`
Representative slice: 1
(selected as the slice where the change had the largest absolute effect)

## Interpretation

The controlled change improved the mean Dice score.

The largest-CC filter helped on this dataset. It removed small isolated positive predictions that were false alarms, improving the mean Dice by +0.0176. This confirms that the baseline threshold produces some spurious scattered predictions, and that the target region is reasonably well-described as a single connected structure.

## What to Take Away

1. **A spatial prior is a modelling decision.** Choosing to keep only the
   largest component encodes the assumption "the target is one connected region."
   That assumption may be valid for some datasets and wrong for others — always
   verify empirically.

2. **One honest comparison beats ten cherry-picked numbers.** The metric
   either improves, degrades, or stays flat. All three outcomes are informative.
   What matters is that the comparison is fair: same data, same threshold,
   only one thing changed.

3. **Post-processing is not free.** Even a rule-based filter introduces a
   hyperparameter (here: connectivity definition, 2-D vs. 3-D). For a
   publishable result you would tune and validate this on a held-out set.

4. **Day 2 challenge.** What if you tried this on a harder slice distribution
   where the tumour is smaller or more irregular? Would the conclusion change?
