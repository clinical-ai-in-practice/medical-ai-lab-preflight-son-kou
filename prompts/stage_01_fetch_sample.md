# Stage 01 — Fetch Sample

## Goal
Explore the repository structure, download the teaching data sample, and confirm
it is ready for the pipeline.

## What to ask Claude Code

> "Read the repo structure and give me a one-paragraph description of what lives
> in each top-level folder. Then run `make fetch-sample` and confirm that
> `data/sample/` was created with at least an image file and a mask file.
> Finally, confirm that `outputs/status/stage_01_fetch_sample.json` was written."

## What this stage must produce

- `data/sample/image.npy` — the sample image array
- `data/sample/mask.npy` — the corresponding ground-truth mask
- `outputs/status/stage_01_fetch_sample.json` with at minimum:
  ```json
  {"status": "ok", "dataset": "<name>"}
  ```

## Check

```bash
make fetch-sample
# Expected output confirms the sample was created
# Verify: ls data/sample/
```

## Notes

- The current implementation generates a synthetic 64×64 sample. A real
  medical teaching dataset will be distributed by the instructor separately.
- `data/sample/` is in `.gitignore` — the pipeline regenerates it on demand.
