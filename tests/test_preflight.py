"""
Structural tests — verify the repository skeleton is intact.

These tests run without executing any pipeline stages. They check that
required files exist and meet minimum quality criteria.
"""

from pathlib import Path
import json


# ------------------------------------------------------------------ #
# Core repository files                                               #
# ------------------------------------------------------------------ #

def test_readme_exists_and_nontrivial():
    p = Path("README.md")
    assert p.exists(), "README.md is missing"
    assert len(p.read_text(encoding="utf-8")) > 200, "README.md is too short to be useful"


def test_assignment_exists():
    assert Path("ASSIGNMENT.md").exists(), "ASSIGNMENT.md is missing"


def test_claude_md_exists_and_nontrivial():
    p = Path("CLAUDE.md")
    assert p.exists(), "CLAUDE.md is missing"
    assert len(p.read_text(encoding="utf-8")) > 200, "CLAUDE.md is too short"


def test_makefile_exists():
    assert Path("Makefile").exists(), "Makefile is missing"


def test_requirements_txt_exists():
    assert Path("requirements.txt").exists(), "requirements.txt is missing"


def test_artifacts_schema_exists():
    p = Path("artifacts/schema.json")
    assert p.exists(), "artifacts/schema.json is missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "required_outputs" in data, "schema.json must have a 'required_outputs' key"


# ------------------------------------------------------------------ #
# Teaching pack configuration                                         #
# ------------------------------------------------------------------ #

def test_teaching_pack_cfg_exists():
    assert Path("data/teaching_pack.cfg").exists(), (
        "data/teaching_pack.cfg is missing. "
        "This file must be present so students can configure the data source."
    )


def test_teaching_pack_cfg_example_exists():
    assert Path("data/teaching_pack.cfg.example").exists(), (
        "data/teaching_pack.cfg.example is missing."
    )


# ------------------------------------------------------------------ #
# Prompts                                                             #
# ------------------------------------------------------------------ #

def test_all_stage_prompts_exist():
    expected = [
        "stage_00_bootstrap.md",
        "stage_01_fetch_sample.md",
        "stage_02_load_visualize.md",
        "stage_03_train_baseline.md",
        "stage_04_error_analysis.md",
        "stage_05_model_swap.md",
        "stage_06_pack_report.md",
        "stage_07_challenge_plan.md",
        "stage_08_adapt_pipeline.md",
        "stage_09_translation_memo.md",
    ]
    for name in expected:
        assert (Path("prompts") / name).exists(), f"Missing prompt: prompts/{name}"


# ------------------------------------------------------------------ #
# Scripts                                                             #
# ------------------------------------------------------------------ #

def test_all_stage_scripts_exist():
    expected = [
        "bootstrap.py",
        "fetch_data.py",
        "inspect_data.py",
        "data_utils.py",
        "visualize_sample.py",
        "run_train.py",
        "error_analysis.py",
        "model_swap.py",
        "pack_report.py",
        "challenge_plan.py",
        "adapt_pipeline.py",
        "translation_memo.py",
    ]
    for name in expected:
        assert (Path("scripts") / name).exists(), f"Missing script: scripts/{name}"
