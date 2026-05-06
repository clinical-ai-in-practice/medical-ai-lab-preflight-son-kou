"""
Stage 09 — Clinical Translation Memo

Reads Day 1 and Day 2 artifacts and produces a concise written memo that
honestly situates the prototype pipeline within the clinical development
pathway.

Inputs (read if available):
  reports/day1_summary.md
  outputs/metrics/val_metrics.json
  outputs/metrics/model_swap_comparison.json
  outputs/metrics/challenge_comparison.json
  outputs/status/stage_07_challenge_plan.json
  outputs/status/stage_08_adapt_pipeline.json

Outputs:
  reports/translation_memo.md
  outputs/status/stage_09_translation_memo.json
"""

from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_utils import pack_info

BASE = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def main() -> None:
    val = _load_json(BASE / "outputs" / "metrics" / "val_metrics.json")
    swap = _load_json(BASE / "outputs" / "metrics" / "model_swap_comparison.json")
    challenge = _load_json(BASE / "outputs" / "metrics" / "challenge_comparison.json")
    s07 = _load_json(BASE / "outputs" / "status" / "stage_07_challenge_plan.json")
    s08 = _load_json(BASE / "outputs" / "status" / "stage_08_adapt_pipeline.json")
    info = pack_info()

    dataset = info.get("dataset", "a teaching-pack dataset")
    modality = info.get("modality", "MRI")
    n_slices = val.get("n_slices", info.get("n_slices", "?"))

    baseline_dice = val.get("dice", None)
    threshold = val.get("threshold", 0.5)
    cc_dice = swap.get("new_dice", None)
    cc_delta = swap.get("delta", None)
    otsu_dice = challenge.get("new_dice", None)
    otsu_delta = challenge.get("delta", None)

    def _fmt(v, fmt=".4f"):
        try:
            return format(float(v), fmt)
        except (TypeError, ValueError):
            return str(v) if v is not None else "not available"

    # Build the best result summary
    if otsu_dice is not None and baseline_dice is not None:
        best_dice = max(float(baseline_dice), float(cc_dice or 0), float(otsu_dice))
        best_method = (
            "Otsu adaptive thresholding + largest-CC post-processing"
            if float(otsu_dice) == best_dice
            else (
                "largest-CC post-processing"
                if cc_dice and float(cc_dice) == best_dice
                else f"fixed threshold (t={threshold})"
            )
        )
    elif cc_dice is not None and baseline_dice is not None:
        best_dice = max(float(baseline_dice), float(cc_dice))
        best_method = (
            "largest-CC post-processing"
            if float(cc_dice) == best_dice
            else f"fixed threshold (t={threshold})"
        )
    else:
        best_dice = baseline_dice
        best_method = f"fixed threshold (t={threshold})"

    memo = f"""# Clinical Translation Memo

**Pipeline:** {dataset} tumour segmentation prototype
**Modality:** {modality}
**Evaluation dataset:** {n_slices} 2-D slices from {dataset}
**Best result achieved:** Mean Dice = {_fmt(best_dice)} ({best_method})

---

## 1. Current Status — What This Prototype Does and Does Not Do

This pipeline is a **research prototype**, not a clinical tool.

**What it does:**

- Ingests normalised {modality} slices and outputs binary tumour segmentation masks.
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
- It has been evaluated on {n_slices} slices from a single curated teaching pack.
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
   multiple institutions and scanners. The {n_slices}-slice teaching pack is
   not a valid research dataset.

2. **Replace the threshold with a learned model.** A convolutional neural
   network (e.g. U-Net or nnU-Net) trained on annotated volumes would be the
   current state of the art for this task. The threshold pipeline is a baseline,
   not a candidate final method.

3. **3-D evaluation.** Report volumetric Dice and Hausdorff distance on 3-D
   volumes, not per-slice Dice on independent 2-D slices.

4. **External validation.** Evaluate on at least one dataset not used during
   development, from a different institution or scanner. Dice = {_fmt(best_dice)}
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

The fixed threshold (t={threshold}) and the Otsu-adaptive variant were both
tuned and evaluated on the {dataset} teaching pack.  There has been no
held-out test set, no cross-validation, and no external validation cohort.
The Dice score of {_fmt(best_dice)} is an in-sample estimate and almost
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
| Fixed threshold (t={threshold}) | {_fmt(baseline_dice)} |
| + Largest-CC post-processing | {_fmt(cc_dice)} |
| + Otsu adaptive thresholding + CC | {_fmt(otsu_dice)} |

All results on {n_slices} slices from {dataset} ({modality}).
No train/test split. Results are in-sample.
"""

    report_path = BASE / "reports" / "translation_memo.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(memo, encoding="utf-8")

    status = {
        "status": "ok",
        "dataset": dataset,
        "modality": modality,
        "n_slices": n_slices,
        "best_dice": round(float(best_dice), 4) if best_dice is not None else None,
        "best_method": best_method,
    }

    status_path = BASE / "outputs" / "status" / "stage_09_translation_memo.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")

    print("Translation memo written.")
    print(f"  Dataset    : {dataset}  ({modality},  {n_slices} slices)")
    print(f"  Best Dice  : {_fmt(best_dice)}  ({best_method})")
    print(f"  Memo saved : reports/translation_memo.md")
    print("Day 2 complete.")


if __name__ == "__main__":
    main()
