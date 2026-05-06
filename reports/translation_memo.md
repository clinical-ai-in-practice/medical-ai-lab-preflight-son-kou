# Clinical Translation Memo

**Pipeline:** BraTS_teaching_pack tumour segmentation prototype
**Modality:** FLAIR
**Evaluation dataset:** 20 2-D slices from BraTS_teaching_pack
**Best result achieved:** Mean Dice = 0.1258 (Otsu adaptive thresholding + largest-CC post-processing)

---

## 1. Current Status — What This Prototype Does and Does Not Do

This pipeline is a **research prototype**, not a clinical tool.

**What it does:**

- Ingests normalised FLAIR slices and outputs binary tumour segmentation masks.
- Applies a deterministic thresholding rule (originally a fixed threshold,
  then per-slice Otsu adaptive thresholding in the Day 2 challenge).
- Evaluates predictions against ground-truth masks using the Dice similarity
  coefficient.
- Produces reproducible, auditable outputs from a small teaching-pack dataset.

**What it does not do:**

- It has **not been trained** on patient data. The pipeline uses no learned
  parameters; it applies a hand-crafted intensity rule.
- It processes **2-D slices independently**, ignoring the 3-D continuity of
  real tumour volumes. Clinical segmentation systems operate on full 3-D volumes.
- It has been evaluated on 20 slices from a single curated teaching pack.
  This is far too small a sample to draw any conclusions about generalisability.
- It has **not been validated** against radiologist annotations. The ground-truth
  masks used here are provided for educational purposes, not as clinical reference
  standards.
- It outputs **no uncertainty estimates**, confidence scores, or quality indicators
  — all of which a clinical system would require.

---

## 2. Path to Research-Grade

For this pipeline to constitute a publishable research contribution, the
following steps would be required, roughly in order:

1. **Scale the dataset.** A minimum of several hundred patients, ideally from
   multiple institutions and scanners. The 20-slice teaching pack is
   not a valid research dataset.

2. **Replace the threshold with a learned model.** A convolutional neural
   network (e.g. U-Net or nnU-Net) trained on annotated volumes would be the
   current state of the art for this task. The threshold pipeline is a baseline,
   not a candidate final method.

3. **3-D evaluation.** Report volumetric Dice and Hausdorff distance on 3-D
   volumes, not per-slice Dice on independent 2-D slices.

4. **External validation.** Evaluate on at least one dataset not used during
   development, from a different institution or scanner. Dice = 0.1258
   on the training/evaluation set does not predict performance on unseen data.

5. **Inter-rater reliability.** The ceiling for segmentation metrics is not 1.0 —
   it is the agreement between expert human raters. Report a radiologist
   inter-rater Dice to contextualise the model's performance.

6. **Prospective cohort study.** Collect data under a prospective protocol
   to avoid the selection bias common in retrospective teaching packs.

---

## 3. Path to Clinical Deployment

Clinical deployment involves requirements beyond research validity:

1. **Regulatory approval.** In the EU, this pipeline would require CE marking
   as a Class IIa or IIb medical device under the EU MDR (Regulation 2017/745).
   In the US, FDA 510(k) clearance or De Novo classification would apply.
   Both processes require clinical evidence of safety and effectiveness.

2. **Prospective clinical trial.** A randomised or non-inferior trial comparing
   pipeline-assisted segmentation against the current standard of care, with
   patient-level endpoints (not just Dice).

3. **Failure mode analysis and safety studies.** Systematic testing on edge
   cases: rare tumour morphologies, low-field scanners, paediatric patients,
   post-treatment anatomy. Failure modes must be characterised and mitigated
   before patient-facing deployment.

4. **Human-in-the-loop validation.** A clinical decision-support tool would
   present pipeline outputs to a radiologist for review and correction — it
   would not act autonomously. The workflow and interface design must be validated
   separately from the algorithm.

5. **Institutional review and governance.** Hospital approval, data governance,
   GDPR / HIPAA compliance for patient data, and clinical governance sign-off.

6. **Post-market surveillance.** Ongoing monitoring of algorithm performance
   after deployment, with a defined process for detecting and correcting drift.

---

## 4. Key Limitation — What a Clinical Collaborator Should Know First

**This prototype has been evaluated on the same data it was calibrated on.**

The fixed threshold (t=0.5) and the Otsu-adaptive variant were both
tuned and evaluated on the BraTS_teaching_pack teaching pack.  There has been no
held-out test set, no cross-validation, and no external validation cohort.
The Dice score of 0.1258 is an in-sample estimate and almost
certainly overestimates the performance a clinical collaborator would see
on their own scanner or patient population.

Before any clinical discussion of performance, this pipeline must be evaluated
on data it has never seen, collected under independent conditions.  Until that
step is taken, the numbers in this report should be treated as proofs-of-concept,
not performance claims.

---

## Appendix: Numeric Results Summary

| Pipeline | Mean Dice |
|---|---|
| Fixed threshold (t=0.5) | 0.1209 |
| + Largest-CC post-processing | 0.1238 |
| + Otsu adaptive thresholding + CC | 0.1258 |

All results on 20 slices from BraTS_teaching_pack (FLAIR).
No train/test split. Results are in-sample.
