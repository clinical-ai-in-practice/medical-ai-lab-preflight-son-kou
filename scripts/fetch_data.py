"""
Stage 01 — Fetch Teaching Pack

Downloads or copies the imaging teaching pack into data/sample/imaging/.
The teaching pack is a small, curated dataset prepared by the instructor.
Students do NOT download or interact with raw BraTS data.

Source configuration (checked in this order):
  1. TEACHING_PACK_PATH  env var   — path to a local directory or .zip file
  2. TEACHING_PACK_URL   env var   — URL to a .zip archive
  3. data/teaching_pack.cfg         — config file with  path =  or  url =  line

If no source is configured, this script exits with a clear error message.
"""

from pathlib import Path
import json
import os
import shutil
import sys
import urllib.request
import zipfile

import numpy as np

BASE = Path(__file__).resolve().parents[1]
TARGET_DIR = BASE / "data" / "sample" / "imaging"
STATUS_PATH = BASE / "outputs" / "status" / "stage_01_fetch_sample.json"
CONFIG_PATH = BASE / "data" / "teaching_pack.cfg"

REQUIRED_FILES = ["slices.npz", "slices_meta.json"]
REQUIRED_META_KEYS = ["dataset", "n_slices", "modality"]

# Accepted array key names — must match data_utils.py
_IMAGE_KEYS = ["images", "image", "imgs", "img", "flair", "t1", "t1ce", "t2", "vol"]
_MASK_KEYS = ["masks", "mask", "segs", "seg", "labels", "label", "gt", "tumor"]


# ------------------------------------------------------------------ #
# Source resolution                                                   #
# ------------------------------------------------------------------ #

def _read_config() -> dict:
    cfg = {}
    if not CONFIG_PATH.exists():
        return cfg
    for raw_line in CONFIG_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        cfg[key.strip().lower()] = value.strip()
    return cfg


def _resolve_source() -> tuple[str, str]:
    """
    Returns (source_type, source_value).
    source_type is 'local' or 'url'.
    Exits with a clear message if nothing is configured.
    """
    env_path = os.environ.get("TEACHING_PACK_PATH", "").strip()
    if env_path:
        return "local", env_path

    env_url = os.environ.get("TEACHING_PACK_URL", "").strip()
    if env_url:
        return "url", env_url

    cfg = _read_config()
    cfg_path = cfg.get("path", "").strip()
    if cfg_path and not cfg_path.upper().startswith("PLACEHOLDER"):
        return "local", cfg_path

    cfg_url = cfg.get("url", "").strip()
    if cfg_url and not cfg_url.upper().startswith("PLACEHOLDER"):
        return "url", cfg_url

    _print_config_error()
    sys.exit(1)


def _print_config_error() -> None:
    lines = [
        "",
        "  [ERROR] No teaching pack source is configured.",
        "",
        "  To fix, do ONE of the following:",
        "",
        "  Option A — Edit data/teaching_pack.cfg (ask your instructor for the URL):",
        "    url = https://your-instructor-server.example.com/teaching_pack.zip",
        "",
        "  Option B — Set an environment variable (local path):",
        "    export TEACHING_PACK_PATH=/path/to/teaching_pack/",
        "",
        "  Option C — Set an environment variable (URL):",
        "    export TEACHING_PACK_URL=https://example.com/teaching_pack.zip",
        "",
        "  Contact your instructor if you do not have the teaching pack URL.",
        "",
    ]
    for line in lines:
        print(line, file=sys.stderr)


# ------------------------------------------------------------------ #
# Fetch logic                                                         #
# ------------------------------------------------------------------ #

def _copy_from_dir(src: Path) -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    for fname in REQUIRED_FILES:
        src_file = src / fname
        if not src_file.exists():
            print(f"  [ERROR] Required file missing from source directory: {src_file}", file=sys.stderr)
            sys.exit(1)
        shutil.copy2(src_file, TARGET_DIR / fname)
        print(f"  Copied {fname}")


def _extract_zip(zip_path: Path) -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        for fname in REQUIRED_FILES:
            # Accept file at archive root or inside one subdirectory level.
            candidates = [n for n in names if Path(n).name == fname]
            if not candidates:
                print(
                    f"  [ERROR] '{fname}' not found in archive.\n"
                    f"  Archive contents (first 20): {names[:20]}",
                    file=sys.stderr,
                )
                sys.exit(1)
            # Prefer shortest path (closest to root).
            src_name = sorted(candidates, key=lambda x: x.count("/"))[0]
            with zf.open(src_name) as src_f:
                (TARGET_DIR / fname).write_bytes(src_f.read())
            print(f"  Extracted {fname}")


def fetch_from_local(src_value: str) -> None:
    src = Path(src_value)
    if src.is_dir():
        print(f"Teaching pack source: local directory  →  {src}")
        _copy_from_dir(src)
    elif src.is_file() and src.suffix.lower() == ".zip":
        print(f"Teaching pack source: local zip  →  {src}")
        _extract_zip(src)
    else:
        print(
            f"  [ERROR] TEACHING_PACK_PATH is not a directory or .zip file: {src}",
            file=sys.stderr,
        )
        sys.exit(1)


def fetch_from_url(url: str) -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    tmp_zip = BASE / "data" / "_tp_download.zip"
    print(f"Teaching pack source: URL  →  {url}")
    print("Downloading …")
    try:
        urllib.request.urlretrieve(url, tmp_zip)
    except Exception as exc:
        print(f"  [ERROR] Download failed: {exc}", file=sys.stderr)
        print("  Check that the URL in data/teaching_pack.cfg is correct.", file=sys.stderr)
        if tmp_zip.exists():
            tmp_zip.unlink()
        sys.exit(1)
    print(f"  Downloaded to {tmp_zip}  ({tmp_zip.stat().st_size / 1024:.1f} KB)")
    _extract_zip(tmp_zip)
    tmp_zip.unlink(missing_ok=True)


# ------------------------------------------------------------------ #
# Validation                                                          #
# ------------------------------------------------------------------ #

def validate_pack() -> dict:
    """Validate the fetched pack and return a metadata dict. Exits on error."""
    for fname in REQUIRED_FILES:
        fpath = TARGET_DIR / fname
        if not fpath.exists():
            print(f"  [ERROR] Required file missing after fetch: {fpath}", file=sys.stderr)
            sys.exit(1)

    # Validate slices.npz
    try:
        pack = np.load(TARGET_DIR / "slices.npz")
        npz_keys = list(pack.keys())
    except Exception as exc:
        print(f"  [ERROR] Cannot open slices.npz: {exc}", file=sys.stderr)
        sys.exit(1)

    img_key = next((k for k in _IMAGE_KEYS if k in npz_keys), None)
    mask_key = next((k for k in _MASK_KEYS if k in npz_keys), None)
    if img_key is None or mask_key is None:
        print(
            f"  [ERROR] Cannot identify image/mask arrays in slices.npz.\n"
            f"  Available keys: {npz_keys}",
            file=sys.stderr,
        )
        sys.exit(1)

    n_slices_from_npz = len(pack[img_key])

    # Validate slices_meta.json
    try:
        meta = json.loads((TARGET_DIR / "slices_meta.json").read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"  [ERROR] Cannot parse slices_meta.json: {exc}", file=sys.stderr)
        sys.exit(1)

    for key in REQUIRED_META_KEYS:
        if key not in meta:
            print(f"  [WARN] slices_meta.json is missing expected key: '{key}'", file=sys.stderr)

    return {
        "dataset": meta.get("dataset", "unknown"),
        "modality": meta.get("modality", "unknown"),
        "n_slices": meta.get("n_slices", n_slices_from_npz),
        "npz_keys": npz_keys,
    }


# ------------------------------------------------------------------ #
# Entry point                                                         #
# ------------------------------------------------------------------ #

def main() -> None:
    source_type, source_value = _resolve_source()

    if source_type == "local":
        fetch_from_local(source_value)
    else:
        fetch_from_url(source_value)

    print("Validating …")
    meta = validate_pack()

    status = {
        "status": "ok",
        "dataset": meta["dataset"],
        "source": source_type,
        "n_slices": meta["n_slices"],
        "modality": meta["modality"],
        "npz_keys": meta["npz_keys"],
        "pack_path": "data/sample/imaging",
    }

    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(status, indent=2), encoding="utf-8")

    print()
    print("Teaching pack ready.")
    print(f"  Location : {TARGET_DIR}")
    print(f"  Dataset  : {meta['dataset']}")
    print(f"  Modality : {meta['modality']}")
    print(f"  Slices   : {meta['n_slices']}")
    print()
    print("Next step: make inspect-data   (or skip straight to: make visualize)")


if __name__ == "__main__":
    main()
