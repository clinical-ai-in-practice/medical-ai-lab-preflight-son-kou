"""
Artifact tests — verify that required pipeline outputs are present and
structurally valid.

These tests assume the student has run the pipeline and committed the outputs.
They check for correct file locations, required JSON keys, and minimum content.
Tests are deterministic: they do not re-run scripts.
"""

from pathlib import Path
import json
import pytest


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def _load_status(stage_name: str) -> dict:
    path = Path(f"outputs/status/{stage_name}.json")
    assert path.exists(), f"Status file missing: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def _require_keys(data: dict, keys: list, context: str) -> None:
    for k in keys:
        assert k in data, f"{context}: required key '{k}' not found. Got: {list(data.keys())}"


# ------------------------------------------------------------------ #
# Stage 00 — Bootstrap                                                #
# ------------------------------------------------------------------ #

def test_stage_00_status_exists():
    _load_status("stage_00_bootstrap")


def test_stage_00_required_keys():
    data = _load_status("stage_00_bootstrap")
    _require_keys(data, ["status", "python_version", "platform"], "stage_00_bootstrap.json")


def test_stage_00_status_ok():
    data = _load_status("stage_00_bootstrap")
    assert data["status"] == "ok", f"stage_00 status is not 'ok': {data['status']}"


def test_stage_00_env_check_report_exists():
    p = Path("reports/env_check.md")
    assert p.exists(), "reports/env_check.md missing"
    assert len(p.read_text(encoding="utf-8").strip()) > 10, "reports/env_check.md is empty"


# ------------------------------------------------------------------ #
# Stage 01 — Fetch Teaching Pack                                      #
# ------------------------------------------------------------------ #

def test_stage_01_status_exists():
    _load_status("stage_01_fetch_sample")


def test_stage_01_required_keys():
    data = _load_status("stage_01_fetch_sample")
    _require_keys(
        data,
        ["status", "dataset", "n_slices", "modality", "source", "pack_path"],
        "stage_01_fetch_sample.json",
    )


def test_stage_01_status_ok():
    data = _load_status("stage_01_fetch_sample")
    assert data["status"] == "ok", (
        f"stage_01 status is not 'ok': {data['status']}. "
        "Run 'make fetch-sample' with a configured teaching pack source."
    )


def test_stage_01_n_slices_positive():
    data = _load_status("stage_01_fetch_sample")
    n = data.get("n_slices", 0)
    assert isinstance(n, int) and n > 0, (
        f"n_slices must be a positive integer, got: {n}"
    )


def test_stage_01_dataset_is_not_synthetic():
    data = _load_status("stage_01_fetch_sample")
    dataset = data.get("dataset", "")
    assert dataset != "synthetic_sample", (
        "stage_01 dataset is still 'synthetic_sample'. "
        "Re-run 'make fetch-sample' with the real teaching pack."
    )


# ------------------------------------------------------------------ #
# Stage 02 — Load & Visualize                                         #
# ------------------------------------------------------------------ #

def test_stage_02_status_exists():
    _load_status("stage_02_load_visualize")


def test_stage_02_required_keys():
    data = _load_status("stage_02_load_visualize")
    _require_keys(data, ["status", "figure"], "stage_02_load_visualize.json")


def test_stage_02_overlay_figure_exists_and_nonempty():
    p = Path("outputs/figures/sample_overlay.png")
    assert p.exists(), "outputs/figures/sample_overlay.png missing"
    assert p.stat().st_size > 1000, "sample_overlay.png looks empty (< 1 KB)"


# ------------------------------------------------------------------ #
# Stage 03 — Train Baseline                                           #
# ------------------------------------------------------------------ #

def test_stage_03_status_exists():
    _load_status("stage_03_train_baseline")


def test_stage_03_required_keys():
    data = _load_status("stage_03_train_baseline")
    _require_keys(data, ["status", "dice", "n_slices"], "stage_03_train_baseline.json")


def test_stage_03_val_metrics_exists():
    p = Path("outputs/metrics/val_metrics.json")
    assert p.exists(), "outputs/metrics/val_metrics.json missing"


def test_stage_03_val_metrics_has_dice():
    p = Path("outputs/metrics/val_metrics.json")
    if not p.exists():
        pytest.skip("val_metrics.json not yet generated")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "dice" in data, "val_metrics.json must contain a 'dice' key"
    assert isinstance(data["dice"], (int, float)), "dice must be a number"
    assert 0.0 <= data["dice"] <= 1.0, f"dice={data['dice']} is outside [0, 1]"


def test_stage_03_n_slices_matches_stage_01():
    s01 = _load_status("stage_01_fetch_sample")
    s03 = _load_status("stage_03_train_baseline")
    n01 = s01.get("n_slices")
    n03 = s03.get("n_slices")
    if n01 is not None and n03 is not None:
        assert n01 == n03, (
            f"Stage 01 reports {n01} slices but stage 03 processed {n03}. "
            "Re-run 'make fetch-sample' and 'make smoke-train'."
        )


def test_stage_03_loss_curve_figure_exists():
    p = Path("outputs/figures/loss_curve.png")
    assert p.exists(), "outputs/figures/loss_curve.png missing"
    assert p.stat().st_size > 1000, "loss_curve.png looks empty (< 1 KB)"


# ------------------------------------------------------------------ #
# Stage 04 — Error Analysis                                           #
# ------------------------------------------------------------------ #

def test_stage_04_status_exists():
    _load_status("stage_04_error_analysis")


def test_stage_04_status_ok():
    data = _load_status("stage_04_error_analysis")
    assert data.get("status") == "ok", (
        f"stage_04 status is not 'ok': {data.get('status')}. "
        "Run 'make error-analysis'."
    )


def test_stage_04_required_keys():
    data = _load_status("stage_04_error_analysis")
    _require_keys(
        data,
        ["status", "best_case", "worst_case", "n_slices"],
        "stage_04_error_analysis.json",
    )


def test_stage_04_best_worst_case_schema():
    data = _load_status("stage_04_error_analysis")
    for case_name in ("best_case", "worst_case"):
        case = data.get(case_name, {})
        assert isinstance(case, dict), f"stage_04: '{case_name}' must be a dict"
        _require_keys(case, ["slice_idx", "dice"], f"stage_04 {case_name}")
        d = case["dice"]
        assert isinstance(d, (int, float)) and 0.0 <= d <= 1.0, (
            f"stage_04 {case_name} dice={d} is not in [0, 1]"
        )


def test_stage_04_best_dice_ge_worst_dice():
    data = _load_status("stage_04_error_analysis")
    best = data.get("best_case", {})
    worst = data.get("worst_case", {})
    if "dice" in best and "dice" in worst:
        assert best["dice"] >= worst["dice"], (
            f"best_case dice ({best['dice']}) must be >= worst_case dice ({worst['dice']})"
        )


def test_stage_04_error_figures_exist():
    for fname in ("error_analysis_best.png", "error_analysis_worst.png"):
        p = Path(f"outputs/figures/{fname}")
        assert p.exists(), f"outputs/figures/{fname} missing"
        assert p.stat().st_size > 1000, f"{fname} looks empty (< 1 KB)"


def test_stage_04_error_analysis_report_nontrivial():
    p = Path("reports/error_analysis.md")
    assert p.exists(), "reports/error_analysis.md missing"
    text = p.read_text(encoding="utf-8").strip()
    assert len(text) > 200, "reports/error_analysis.md is too short — still a stub"
    assert "# Error Analysis" in text, "reports/error_analysis.md is missing its header"


# ------------------------------------------------------------------ #
# Stage 05 — Model Swap                                               #
# ------------------------------------------------------------------ #

def test_stage_05_status_exists():
    _load_status("stage_05_model_swap")


def test_stage_05_status_ok():
    data = _load_status("stage_05_model_swap")
    assert data.get("status") == "ok", (
        f"stage_05 status is not 'ok': {data.get('status')}. "
        "Run 'make model-swap'."
    )


def test_stage_05_required_keys():
    data = _load_status("stage_05_model_swap")
    _require_keys(
        data,
        ["status", "baseline_dice", "new_dice", "delta", "change_description"],
        "stage_05_model_swap.json",
    )


def test_stage_05_new_dice_is_valid():
    data = _load_status("stage_05_model_swap")
    new_dice = data.get("new_dice")
    assert isinstance(new_dice, (int, float)), (
        f"stage_05 new_dice must be a number, got: {new_dice!r}"
    )
    assert 0.0 <= new_dice <= 1.0, f"stage_05 new_dice={new_dice} is outside [0, 1]"


def test_stage_05_comparison_metrics_exists():
    p = Path("outputs/metrics/model_swap_comparison.json")
    assert p.exists(), "outputs/metrics/model_swap_comparison.json missing"


def test_stage_05_comparison_metrics_schema():
    p = Path("outputs/metrics/model_swap_comparison.json")
    if not p.exists():
        pytest.skip("model_swap_comparison.json not yet generated")
    data = json.loads(p.read_text(encoding="utf-8"))
    _require_keys(
        data,
        ["baseline_dice", "new_dice", "delta", "change_description"],
        "model_swap_comparison.json",
    )
    assert isinstance(data["new_dice"], (int, float)), "new_dice must be a number"
    assert 0.0 <= data["new_dice"] <= 1.0, f"new_dice={data['new_dice']} is outside [0, 1]"


def test_stage_05_comparison_figure_exists():
    p = Path("outputs/figures/model_swap_comparison.png")
    assert p.exists(), "outputs/figures/model_swap_comparison.png missing"
    assert p.stat().st_size > 1000, "model_swap_comparison.png looks empty (< 1 KB)"


def test_stage_05_model_swap_report_nontrivial():
    p = Path("reports/model_swap.md")
    assert p.exists(), "reports/model_swap.md missing"
    text = p.read_text(encoding="utf-8").strip()
    assert len(text) > 200, "reports/model_swap.md is too short — still a stub"


# ------------------------------------------------------------------ #
# Stage 06 — Pack Report                                              #
# ------------------------------------------------------------------ #

def test_stage_06_status_exists():
    _load_status("stage_06_pack_report")


def test_stage_06_status_ok():
    data = _load_status("stage_06_pack_report")
    assert data.get("status") == "ok", (
        f"stage_06 status is not 'ok': {data.get('status')}. "
        "Run 'make pack-report'."
    )


def test_stage_06_required_keys():
    data = _load_status("stage_06_pack_report")
    _require_keys(data, ["status", "sections"], "stage_06_pack_report.json")


def test_stage_06_day1_summary_nontrivial():
    p = Path("reports/day1_summary.md")
    assert p.exists(), "reports/day1_summary.md missing"
    text = p.read_text(encoding="utf-8").strip()
    assert len(text) > 400, (
        f"reports/day1_summary.md is too short ({len(text)} chars) — still a stub. "
        "Run 'make pack-report'."
    )
    assert "# Day 1 Summary" in text, "reports/day1_summary.md is missing its header"


def test_stage_06_day1_summary_has_metrics():
    p = Path("reports/day1_summary.md")
    if not p.exists():
        pytest.skip("day1_summary.md not yet generated")
    text = p.read_text(encoding="utf-8")
    assert "Baseline" in text or "baseline" in text, (
        "day1_summary.md does not mention the baseline — pack-report may not have run correctly"
    )


# ------------------------------------------------------------------ #
# Stage 07 — Challenge Plan                                           #
# ------------------------------------------------------------------ #

def test_stage_07_status_exists():
    _load_status("stage_07_challenge_plan")


def test_stage_07_status_ok():
    data = _load_status("stage_07_challenge_plan")
    assert data.get("status") == "ok", (
        f"stage_07 status is not 'ok': {data.get('status')}. "
        "Run 'make challenge-plan'."
    )


def test_stage_07_required_keys():
    data = _load_status("stage_07_challenge_plan")
    _require_keys(
        data,
        ["status", "proposed_change", "identified_weakness"],
        "stage_07_challenge_plan.json",
    )


def test_stage_07_challenge_plan_nontrivial():
    p = Path("reports/challenge_plan.md")
    assert p.exists(), "reports/challenge_plan.md missing"
    text = p.read_text(encoding="utf-8").strip()
    assert len(text) > 200, (
        f"reports/challenge_plan.md is too short ({len(text)} chars) — still a stub. "
        "Run 'make challenge-plan'."
    )
    assert "# Day 2 Challenge Plan" in text, (
        "reports/challenge_plan.md is missing its header"
    )


def test_stage_07_challenge_plan_has_weakness():
    p = Path("reports/challenge_plan.md")
    if not p.exists():
        pytest.skip("challenge_plan.md not yet generated")
    text = p.read_text(encoding="utf-8")
    assert "weakness" in text.lower() or "limitation" in text.lower(), (
        "challenge_plan.md should identify a weakness or limitation of the Day 1 baseline"
    )


# ------------------------------------------------------------------ #
# Stage 08 — Adapt Pipeline                                           #
# ------------------------------------------------------------------ #

def test_stage_08_status_exists():
    _load_status("stage_08_adapt_pipeline")


def test_stage_08_status_ok():
    data = _load_status("stage_08_adapt_pipeline")
    assert data.get("status") == "ok", (
        f"stage_08 status is not 'ok': {data.get('status')}. "
        "Run 'make adapt-pipeline'."
    )


def test_stage_08_required_keys():
    data = _load_status("stage_08_adapt_pipeline")
    _require_keys(
        data,
        ["status", "changes_summary", "baseline_dice", "new_dice", "delta"],
        "stage_08_adapt_pipeline.json",
    )


def test_stage_08_challenge_comparison_exists():
    p = Path("outputs/metrics/challenge_comparison.json")
    assert p.exists(), "outputs/metrics/challenge_comparison.json missing"


def test_stage_08_challenge_comparison_schema():
    p = Path("outputs/metrics/challenge_comparison.json")
    if not p.exists():
        pytest.skip("challenge_comparison.json not yet generated")
    data = json.loads(p.read_text(encoding="utf-8"))
    _require_keys(
        data,
        ["baseline_dice", "new_dice", "delta", "change_description"],
        "challenge_comparison.json",
    )
    assert isinstance(data["new_dice"], (int, float)), "new_dice must be a number"
    assert 0.0 <= data["new_dice"] <= 1.0, f"new_dice={data['new_dice']} is outside [0, 1]"
    assert isinstance(data["baseline_dice"], (int, float)), "baseline_dice must be a number"
    assert 0.0 <= data["baseline_dice"] <= 1.0, (
        f"baseline_dice={data['baseline_dice']} is outside [0, 1]"
    )


def test_stage_08_challenge_figure_exists():
    p = Path("outputs/figures/challenge_comparison.png")
    assert p.exists(), "outputs/figures/challenge_comparison.png missing"
    assert p.stat().st_size > 1000, "challenge_comparison.png looks empty (< 1 KB)"


def test_stage_08_adapt_pipeline_report_nontrivial():
    p = Path("reports/adapt_pipeline.md")
    assert p.exists(), "reports/adapt_pipeline.md missing"
    text = p.read_text(encoding="utf-8").strip()
    assert len(text) > 200, "reports/adapt_pipeline.md is too short — still a stub"


# ------------------------------------------------------------------ #
# Stage 09 — Translation Memo                                         #
# ------------------------------------------------------------------ #

def test_stage_09_status_exists():
    _load_status("stage_09_translation_memo")


def test_stage_09_status_ok():
    data = _load_status("stage_09_translation_memo")
    assert data.get("status") == "ok", (
        f"stage_09 status is not 'ok': {data.get('status')}. "
        "Run 'make translation-memo'."
    )


def test_stage_09_required_keys():
    data = _load_status("stage_09_translation_memo")
    _require_keys(data, ["status", "best_dice", "best_method"], "stage_09_translation_memo.json")


def test_stage_09_translation_memo_nontrivial():
    p = Path("reports/translation_memo.md")
    assert p.exists(), "reports/translation_memo.md missing"
    text = p.read_text(encoding="utf-8").strip()
    assert len(text) > 400, (
        f"reports/translation_memo.md is too short ({len(text)} chars) — still a stub. "
        "Run 'make translation-memo'."
    )
    assert "# Clinical Translation Memo" in text, (
        "reports/translation_memo.md is missing its header"
    )


def test_stage_09_memo_covers_required_topics():
    p = Path("reports/translation_memo.md")
    if not p.exists():
        pytest.skip("translation_memo.md not yet generated")
    text = p.read_text(encoding="utf-8")
    assert "Current Status" in text or "current status" in text.lower(), (
        "translation_memo.md should contain a 'Current Status' section"
    )
    assert "research" in text.lower(), (
        "translation_memo.md should discuss the path to research-grade"
    )
    assert "clinical" in text.lower() or "deployment" in text.lower(), (
        "translation_memo.md should discuss clinical deployment requirements"
    )
    assert "limitation" in text.lower() or "limitation" in text.lower(), (
        "translation_memo.md should identify a key limitation"
    )
