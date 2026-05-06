"""
Stage 01 (inspect) — Inspect Teaching Pack

Prints a human-readable summary of the fetched teaching pack.
Run with: make inspect-data

This command is safe to run multiple times. It does not modify any files.
"""

from pathlib import Path
import json
import sys

import numpy as np

BASE = Path(__file__).resolve().parents[1]
PACK_DIR = BASE / "data" / "sample" / "imaging"
STATUS_PATH = BASE / "outputs" / "status" / "stage_01_fetch_sample.json"

_SEP = "─" * 52


def main() -> None:
    if not PACK_DIR.exists() or not any(PACK_DIR.iterdir()):
        print(_SEP)
        print("Teaching Pack: NOT FOUND")
        print(_SEP)
        print()
        print("  No teaching pack has been fetched yet.")
        print("  Run:  make fetch-sample")
        print()
        sys.exit(0)

    print(_SEP)
    print("  Teaching Pack Inspection")
    print(_SEP)

    # ---- Status file ----
    if STATUS_PATH.exists():
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        print(f"  Status   : {status.get('status', '?')}")
        print(f"  Dataset  : {status.get('dataset', '?')}")
        print(f"  Modality : {status.get('modality', '?')}")
        print(f"  Slices   : {status.get('n_slices', '?')}")
        print(f"  Source   : {status.get('source', '?')}")
        print(f"  Location : {PACK_DIR}")
    else:
        print("  [WARN] No status file found.")
        print("  The pack may have been placed manually without running make fetch-sample.")
        print(f"  Location : {PACK_DIR}")

    # ---- slices.npz ----
    npz_path = PACK_DIR / "slices.npz"
    if npz_path.exists():
        print()
        print("  slices.npz")
        try:
            pack = np.load(npz_path)
            for key in pack.keys():
                arr = pack[key]
                arr_f = arr.astype(float)
                print(
                    f"    {key:<12}  shape={arr.shape}  dtype={arr.dtype}"
                    f"  min={arr_f.min():.3f}  max={arr_f.max():.3f}"
                )
        except Exception as exc:
            print(f"    [ERROR] Cannot open slices.npz: {exc}")
    else:
        print()
        print("  slices.npz: NOT FOUND")

    # ---- slices_meta.json ----
    meta_path = PACK_DIR / "slices_meta.json"
    if meta_path.exists():
        print()
        print("  slices_meta.json")
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            for k, v in meta.items():
                print(f"    {k:<20} {v}")
        except Exception as exc:
            print(f"    [ERROR] Cannot read slices_meta.json: {exc}")
    else:
        print()
        print("  slices_meta.json: NOT FOUND")

    print()
    print(_SEP)
    print("  Next step: make visualize")
    print(_SEP)


if __name__ == "__main__":
    main()
