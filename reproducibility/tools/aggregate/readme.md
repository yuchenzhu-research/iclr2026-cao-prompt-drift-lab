# Aggregate (Deprecated)

> **Status: DEPRECATED / HISTORICAL.**
>
> This directory is kept only to explain older assumptions that caused the
> processed tables to drift.
>
> Canonical rebuild now lives in:
> `reproducibility/tools/reproduce_valid_evaluations.py --from_raw`

---

## What this directory means now

Earlier drafts mixed together several unstable ideas:

- model-name normalization based on inconsistent metadata
- filename parsing that assumed `versions` / `trigger_types` were always present
- `total` handling that broke when bundles omitted top-level totals

Those behaviors are no longer the canonical path. The supported rebuild path is:

```text
raw judge bundles -> record_*.json -> scores_long.csv / scores_grouped.csv
```

via `reproducibility/tools/reproduce_valid_evaluations.py --from_raw`.

---

## How figures should be reproduced

Figure rendering remains the downstream deterministic pipeline:

```
(scores_long.csv tables; v0/v1/v2)  →  figure scripts  →  PDF figures
```

See `reproducibility/tools/figures/readme.md` for the script-to-figure mapping and one-command reproduction instructions.

---

## Non-goals

- This directory does not define the live pipeline.
- No script here should be treated as an execution entry point.
