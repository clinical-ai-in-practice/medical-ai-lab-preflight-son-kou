# data/

This folder holds the imaging teaching pack used in the lab.

## What is the teaching pack?

The teaching pack is a small, curated collection of medical image slices
prepared by the instructor from a publicly available brain tumour dataset.
It is NOT the full raw dataset — it is a pre-processed subset designed to
be lightweight enough to download and analyse in a single lab session.

**Students never download raw BraTS or other primary research datasets directly.**
The instructor has done that work and packaged the relevant slices for you.

## What appears after running `make fetch-sample`

```
data/
  sample/
    imaging/
      slices.npz          ← imaging slices array (images + masks)
      slices_meta.json    ← metadata: dataset name, modality, n_slices, etc.
  teaching_pack.cfg       ← source configuration (URL or local path)
  teaching_pack.cfg.example  ← reference / documented template
```

`data/sample/` is in `.gitignore`. You do **not** commit the teaching pack
files — they are regenerated on demand by `make fetch-sample`.

## How the source is configured

The file `data/teaching_pack.cfg` controls where `make fetch-sample` downloads
the pack from. Your instructor will set the URL before distributing this
repository. If the URL is not yet configured, `make fetch-sample` will print
a clear error message telling you what to do.

If you are working offline or the instructor has placed the pack on a shared
drive, you can override the config with an environment variable:

```bash
export TEACHING_PACK_PATH=/path/to/teaching_pack/
make fetch-sample
```

## slices.npz format

The `.npz` file contains at least two arrays:

| Key | Shape | Description |
|---|---|---|
| `images` | (N, H, W) | Normalised MRI slices, float32 |
| `masks` | (N, H, W) | Binary tumour masks, int32 {0, 1} |

Exact key names may vary — `data_utils.py` handles the most common variants
automatically. Run `make inspect-data` to see the actual keys and shapes.

## If `make fetch-sample` fails

1. Check that `data/teaching_pack.cfg` contains a `url =` or `path =` line
   (not a PLACEHOLDER comment).
2. Verify you have an internet connection if using a URL.
3. Ask your instructor for the correct teaching pack URL.
