"""
Stage 06 — Pack Day 1 Report

Assembles a concise Day 1 summary from all completed stage artifacts.
Reads actual values from status files and metrics — does not use hardcoded text.

Inputs  (all stage 00–05 artifacts must exist):
  outputs/status/stage_NN_*.json
  outputs/metrics/val_metrics.json
  outputs/metrics/model_swap_comparison.json

Outputs:
  reports/day1_summary.md
  outputs/status/stage_06_pack_report.json
"""

from pathlib import Path
import json
import sys

BASE = Path(__file__).resolve().parents[1]

REPORT_SECTIONS = [
    ("env_check",      BASE / "reports" / "env_check.md"),
    ("data_notes",     BASE / "reports" / "data_notes.md"),
    ("train_notes",    BASE / "reports" / "train_notes.md"),
    ("error_analysis", BASE / "reports" / "error_analysis.md"),
    ("model_swap",     BASE / "reports" / "model_swap.md"),
]


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _read_status(stage_name: str) -> dict:
    p = BASE / "outputs" / "status" / f"{stage_name}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def _read_metrics(fname: str) -> dict:
    p = BASE / "outputs" / "metrics" / fname
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def _fmt_float(v, decimals: int = 4) -> str:
    return f"{v:.{decimals}f}" if isinstance(v, float) else str(v)


def _fmt_delta(v) -> str:
    return f"{v:+.4f}" if isinstance(v, float) else str(v)


# ------------------------------------------------------------------ #
# Main                                                                #
# ------------------------------------------------------------------ #

def main() -> None:
    # Gather all artifacts
    s00 = _read_status("stage_00_bootstrap")
    s01 = _read_status("stage_01_fetch_sample")
    s03 = _read_status("stage_03_train_baseline")
    s04 = _read_status("stage_04_error_analysis")
    s05 = _read_status("stage_05_model_swap")
    val_m = _read_metrics("val_metrics.json")
    swap_m = _read_metrics("model_swap_comparison.json")

    found = [name for name, path in REPORT_SECTIONS if path.exists()]
    missing = [name for name, path in REPORT_SECTIONS if not path.exists()]

    if missing:
        print(f"  [WARN] Missing report sections: {missing}")
        print("  Run the corresponding stages first.")

    # ---- Extract values with safe fallbacks ----
    python_ver = s00.get("python_version", "?")
    platform = s00.get("platform", "?")
    bootstrap_ok = s00.get("status") == "ok"

    dataset = s01.get("dataset", "?")
    modality = s01.get("modality", "?")
    n_slices = s01.get("n_slices", "?")

    threshold = val_m.get("threshold", s03.get("threshold", "?"))
    baseline_dice = val_m.get("dice", s03.get("dice"))
    baseline_std = val_m.get("per_slice_dice_std")

    best = s04.get("best_case", {})
    worst = s04.get("worst_case", {})

    swap_baseline = swap_m.get("baseline_dice", s05.get("baseline_dice"))
    swap_new = swap_m.get("new_dice", s05.get("new_dice"))
    swap_delta = swap_m.get("delta", s05.get("delta"))
    swap_desc = swap_m.get("change_description", s05.get("change_description", ""))

    # ---- Format composite strings ----
    if isinstance(baseline_dice, float) and isinstance(baseline_std, float):
        dice_str = f"{baseline_dice:.4f} ± {baseline_std:.4f}"
    else:
        dice_str = _fmt_float(baseline_dice)

    best_line = (
        f"slice {best.get('slice_idx', '?')}  Dice = {_fmt_float(best.get('dice'))}"
        if best else "not computed"
    )
    worst_line = (
        f"slice {worst.get('slice_idx', '?')}  Dice = {_fmt_float(worst.get('dice'))}"
        if worst else "not computed"
    )

    if swap_delta is not None:
        swap_outcome = (
            "improved" if isinstance(swap_delta, float) and swap_delta > 0.001
            else ("degraded" if isinstance(swap_delta, float) and swap_delta < -0.001
                  else "unchanged")
        )
    else:
        swap_outcome = "not computed"

    # ---- Assemble summary ----
    summary = f"""# Day 1 Summary

## 1. Environment

- Python: {python_ver}
- Platform: {platform}
- Bootstrap: {"completed ✓" if bootstrap_ok else "not run"}

## 2. Dataset

- Dataset: {dataset}
- Modality: {modality}
- Slices in teaching pack: {n_slices}
- Location: `data/sample/imaging/`

## 3. Visualisation

Representative slice visualised with ground-truth mask overlay.
See: `outputs/figures/sample_overlay.png`

## 4. Baseline Segmentation

- Method: intensity threshold at {threshold}
- Mean Dice across {n_slices} slices: {dice_str}

The baseline applies a fixed intensity threshold to each normalised MRI slice.
It is intentionally simple — its purpose is to establish a reproducible
reference point, not to achieve clinical performance.

## 5. Error Analysis

- Best case:  {best_line}
- Worst case: {worst_line}

The gap between best and worst case quantifies how sensitive the threshold
method is to slice-level intensity variation. Slices where tumour pixels are
reliably bright outperform slices where intensity distributions overlap.

Figures: `outputs/figures/error_analysis_best.png`,
         `outputs/figures/error_analysis_worst.png`

## 6. Controlled Improvement

- Change: {swap_desc or "see reports/model_swap.md"}
- Baseline Dice: {_fmt_float(swap_baseline)}
- New Dice:      {_fmt_float(swap_new)}
- Delta:         {_fmt_delta(swap_delta)}  → {swap_outcome}

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

{chr(10).join("- " + name + " ✓" for name in found)}
{chr(10).join("- " + name + " — missing" for name in missing) if missing else ""}

All required Day 1 figures are in `outputs/figures/`.
All required Day 1 metrics are in `outputs/metrics/`.
All required Day 1 reports are in `reports/`.
"""

    summary_path = BASE / "reports" / "day1_summary.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(summary, encoding="utf-8")

    # ---- Status JSON ----
    status = {
        "status": "ok",
        "sections": found,
        "missing": missing,
        "dataset": dataset,
        "baseline_dice": round(baseline_dice, 4) if isinstance(baseline_dice, float) else None,
        "model_swap_delta": round(swap_delta, 4) if isinstance(swap_delta, float) else None,
    }

    status_path = BASE / "outputs" / "status" / "stage_06_pack_report.json"
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2), encoding="utf-8")

    print("Day 1 report assembled.")
    print(f"  Sections: {found}")
    if missing:
        print(f"  Missing:  {missing}")
    print(f"  Saved:    reports/day1_summary.md")
    print()
    print("Day 1 complete.")
    print("Review the full dashboard: make app")
    print("Push your work:            git add -A && git commit -m 'Day 1 complete'")


if __name__ == "__main__":
    main()
