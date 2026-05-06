"""
Script existence tests — kept as a separate file for backward compatibility
with existing CI references.

For a more thorough check, see test_preflight.py::test_all_stage_scripts_exist.
"""

from pathlib import Path


def test_day1_scripts_exist():
    for p in [
        "scripts/bootstrap.py",
        "scripts/fetch_data.py",
        "scripts/visualize_sample.py",
        "scripts/run_train.py",
        "scripts/error_analysis.py",
        "scripts/model_swap.py",
        "scripts/pack_report.py",
    ]:
        assert Path(p).exists(), f"Missing: {p}"


def test_day2_scripts_exist():
    for p in [
        "scripts/challenge_plan.py",
        "scripts/adapt_pipeline.py",
        "scripts/translation_memo.py",
    ]:
        assert Path(p).exists(), f"Missing: {p}"
