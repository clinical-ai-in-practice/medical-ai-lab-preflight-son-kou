"""
Reset Student Lab State

Clears all student-generated runtime outputs and restores the repo to a
clean Mission 0 start position. Run this before a new student test session.

Safe to run: scaffold files, scripts, tests, prompts, and docs are NOT touched.
A timestamped archive of the current state is written to .session_archives/.

Usage:
    python scripts/reset_student_state.py            # interactive confirmation
    python scripts/reset_student_state.py --force    # skip confirmation prompt
"""

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

# ── What gets cleared on reset ────────────────────────────────────────────────

OUTPUT_SUBDIRS = ["status", "figures", "metrics"]

GENERATED_REPORTS = [
    "env_check.md",
    "data_notes.md",
    "train_notes.md",
    "error_analysis.md",
    "model_swap.md",
    "day1_summary.md",
    "challenge_plan.md",
    "adapt_pipeline.md",
    "translation_memo.md",
]

# ── What is NEVER touched ─────────────────────────────────────────────────────
# scripts/, tests/, prompts/, docs/, artifacts/, app/, Makefile, CLAUDE.md,
# ASSIGNMENT.md, README.md, requirements.txt, .github/, .devcontainer/,
# data/teaching_pack.cfg, data/README.md

DEFAULT_STATE = {
    "current_mission":    0,
    "completed_missions": [],
    "unlocked_missions":  [0],
    "last_checked":       None,
    "mode":               "guided",
}


def _archive_current_state() -> Path:
    """Write a metadata snapshot to .session_archives/ before clearing anything."""
    archive_dir = BASE / ".session_archives"
    archive_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    archive_path = archive_dir / f"session_{ts}.json"

    state_path = BASE / ".student_state" / "current_mission.json"
    student_state = {}
    if state_path.exists():
        try:
            student_state = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    snapshot = {
        "archived_at": datetime.now(timezone.utc).isoformat(),
        "archived_by": "reset_student_state.py",
        "missions_completed": len(student_state.get("completed_missions", [])),
        "student_state": student_state,
        "artifacts_present": {
            "status_files": [p.name for p in sorted((BASE / "outputs" / "status").glob("*.json"))],
            "figures":      [p.name for p in sorted((BASE / "outputs" / "figures").glob("*.png"))],
            "metrics":      [p.name for p in sorted((BASE / "outputs" / "metrics").glob("*.json"))],
            "reports":      [r for r in GENERATED_REPORTS if (BASE / "reports" / r).exists()],
        },
    }
    archive_path.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return archive_path


def _clear_outputs() -> list[str]:
    cleared: list[str] = []
    for subdir in OUTPUT_SUBDIRS:
        d = BASE / "outputs" / subdir
        if d.exists():
            for f in d.iterdir():
                if f.is_file():
                    f.unlink()
                    cleared.append(f"outputs/{subdir}/{f.name}")
    return cleared


def _clear_reports() -> list[str]:
    cleared: list[str] = []
    for fname in GENERATED_REPORTS:
        p = BASE / "reports" / fname
        if p.exists():
            p.unlink()
            cleared.append(f"reports/{fname}")
    return cleared


def _clear_imaging_data() -> list[str]:
    cleared: list[str] = []
    imaging_dir = BASE / "data" / "sample" / "imaging"
    if imaging_dir.exists():
        for f in imaging_dir.iterdir():
            if f.is_file():
                f.unlink()
                cleared.append(f"data/sample/imaging/{f.name}")
    return cleared


def _clear_lab_history() -> bool:
    lab_history = BASE / ".lab_history"
    if lab_history.exists():
        shutil.rmtree(lab_history, ignore_errors=True)
        return True
    return False


def _reset_student_state() -> None:
    state_path = BASE / ".student_state" / "current_mission.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(DEFAULT_STATE, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reset student lab state to Mission 0.")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompt.")
    args = parser.parse_args()

    print()
    print("  Medical AI Lab — Reset Student State")
    print("  " + "─" * 42)
    print()

    # Describe what will be cleared
    print("  The following will be cleared:")
    print("    • outputs/status/*.json")
    print("    • outputs/figures/*.png")
    print("    • outputs/metrics/*.json")
    print("    • reports/ (generated .md files)")
    print("    • data/sample/imaging/ (fetched teaching pack)")
    print("    • .lab_history/ (if present)")
    print("    • .student_state/current_mission.json → reset to Mission 0")
    print()
    print("  The following will NOT be touched:")
    print("    • scripts/, tests/, prompts/, docs/, app/")
    print("    • Makefile, CLAUDE.md, ASSIGNMENT.md, requirements.txt")
    print("    • data/teaching_pack.cfg  ← preserves your fetch source")
    print()
    print("  A session snapshot will be archived to .session_archives/ first.")
    print()

    if not args.force:
        answer = input("  Proceed? [y/N]: ").strip().lower()
        if answer != "y":
            print("  Cancelled.")
            sys.exit(0)

    print()
    print("  Archiving current session …")
    archive_path = _archive_current_state()
    print(f"  Archived to {archive_path.relative_to(BASE)}")

    print("  Clearing outputs …")
    for f in _clear_outputs():
        print(f"    ✓ {f}")

    print("  Clearing reports …")
    for f in _clear_reports():
        print(f"    ✓ {f}")

    print("  Clearing imaging data …")
    cleared_imaging = _clear_imaging_data()
    for f in cleared_imaging:
        print(f"    ✓ {f}")
    if not cleared_imaging:
        print("    (none found)")

    if _clear_lab_history():
        print("  Cleared .lab_history/")

    print("  Resetting student state …")
    _reset_student_state()

    print()
    print("  ✓ Reset complete. Repo is ready for a fresh student run.")
    print()
    print("  Next steps:")
    print("    1. make dashboard      → open the dashboard (should show Mission 0)")
    print("    2. Student runs Mission 0 in VS Code + Claude Code")
    print("    3. For Mission 1: ensure data/teaching_pack.cfg is configured")
    print()


if __name__ == "__main__":
    main()
