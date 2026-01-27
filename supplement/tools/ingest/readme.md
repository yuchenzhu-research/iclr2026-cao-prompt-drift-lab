# Ingest: Materialize Processed Evaluation Records (Optional Audit Utility)

This directory contains **offline ingestion utilities** used to materialize standardized processed records
(`valid_evaluations/**/*.json`) from raw judge evaluation bundles.

**Scope / contract**
- This ingest step produces **record-level** artifacts only (JSON + optional exclusions log).
- **Do not** treat this step as a table generator. Any `summary_tables/*.csv` shipped with the repo are
  treated as **provided artifacts**.

---

## Reproducibility boundary (important)

For this submission, **reproduction starts from the shipped evaluation tables**:

- `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/scores_long.csv`
- `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/scores_long.csv`
- `supplement/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/scores_long.csv`

All paper figures are reproducible from these CSVs (see `supplement/tools/figures/`).

We provide ingest utilities only as an **optional audit tool** to inspect record-level JSON derived from
raw judge bundles. Regenerating `scores_long.csv` from raw bundles/records is **out of scope** and **not supported**
for artifact reproduction.

---

## What this step does

- Reads raw judge evaluation bundles under:
  - `supplement/04_results/02_raw_judge_evaluations/`
- Applies consistent parsing + validation + filtering to produce standardized records.
- Writes record-level outputs under:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`

These JSON files can serve as an **audit anchor** for debugging and spot-checking.

---

## Entry point

### `materialize_records.py`

**Recommended run (from repo root):**

```bash
python supplement/tools/ingest/materialize_records.py
```

By default, the script attempts to materialize records for:
- `v0_baseline_judge`
- `v1_paraphrase_judge`
- `v2_schema_strict_judge`

If a raw input directory is missing for a run, it will print a warning and skip that run.

---

## Inputs and outputs

### Inputs

Raw judge bundles are organized by setting:

- Diagnostic bundles:
  - `supplement/04_results/02_raw_judge_evaluations/diagnostic/...`
- Final bundles:
  - `supplement/04_results/02_raw_judge_evaluations/final/...`

### Outputs

Processed records are written to:

- `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`

Exclusions (audit):
- `excluded_records.jsonl` is optional and only present when exclusions are non-empty.
- If absent, treat this as **0 exclusions**.
- If present, it is stored under:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/excluded_records.jsonl`

> Note: This script intentionally does **not** generate `scores_long.csv` / `scores_grouped.csv`.
> If such tables exist under `summary_tables/`, they are shipped artifacts.

---

## Repro checklist (audit-only)

- [ ] Run from repo root so relative paths are stable.
- [ ] Execute:
  - `python supplement/tools/ingest/materialize_records.py`
- [ ] Verify outputs exist:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`
- [ ] Confirm you are not regenerating tables:
  - Do not add scripts that overwrite `summary_tables/*.csv` in the reproducibility path.
