# Ingest: Materialize Processed Evaluation Records

This directory contains the ingestion utilities used to materialize **standardized processed records**
(`**/*.json`, filenames are not a contract) from **raw judge evaluation bundles**.

> Summary tables (`scores_long.csv`, `scores_grouped.csv`) are **already provided** under judge-specific
> `summary_tables/` directories. Ingest produces **record-level** artifacts only.

---

## What this step does

- Reads raw judge evaluation bundles under:
  - `supplement/04_results/02_raw_judge_evaluations/`
- Applies consistent parsing + validation + filtering to produce standardized records.
- Writes record-level outputs under:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`

These JSON files are the **audit anchor** for all downstream tables and figures.

---

## Entry points

### 1) `materialize_records.py`

Canonical script for materializing processed records.

**Recommended run (from repo root):**

```bash
python supplement/tools/ingest/materialize_records.py --ack-legacy
```

> Note: this script is treated as a legacy-compatible entry in this repository.
> It is offline and deterministic. It does not execute any model inference.

### 2) `reproduce_valid_evaluations.py` (optional helper)

Helper script that may perform additional filtering/selection but **still only outputs** record-level JSON.

**Run (from repo root):**

```bash
python supplement/tools/ingest/reproduce_valid_evaluations.py
```

> Note: This script is record-level only. It does **not** generate `scores_long.csv` / `scores_grouped.csv`.

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
- `excluded_records.jsonl` is **optional** and only present when exclusions are non-empty.
- If `excluded_records.jsonl` is absent for a judge version, treat this as **0 exclusions**.
- If present, store it under:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/excluded_records.jsonl`

---

## Judge versions and input protocols

Differences between judge versions are encoded **in the raw input bundles** (directory layout + bundle metadata),
not by changing ingestion logic.

- `v0_baseline_judge`
  - Diagnostic setting
  - Multiple judge–generator cross combinations
  - Input path: `supplement/04_results/02_raw_judge_evaluations/diagnostic/...`

- `v1_paraphrase_judge`
  - Final setting
  - Paraphrase-robustness evaluation
  - Input path: `supplement/04_results/02_raw_judge_evaluations/final/...`

- `v2_schema_strict_judge`
  - Final setting
  - Strict schema enforcement
  - Input path: `supplement/04_results/02_raw_judge_evaluations/final/...`

The ingestion code path is intended to be identical across versions; version-specific behavior should be driven by
bundle contents.

---

## Repro checklist

- [ ] Run from repo root so relative paths are stable.
- [ ] Execute the entry point:
  - `python supplement/tools/ingest/materialize_records.py --ack-legacy`
- [ ] Verify outputs exist:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`
- [ ] Spot-check record integrity:
  - Open one JSON and confirm it contains `file` + model/judge metadata.
- [ ] Exclusions (if any):
  - If `excluded_records.jsonl` exists, it must be under `summary_tables/` and explain exclusions.
- [ ] Confirm you are not recomputing tables:
  - `scores_long.csv` / `scores_grouped.csv` are already provided under each judge version’s `summary_tables/`.
- [ ] Downstream compatibility:
  - Figure scripts read record JSON + `summary_tables/` and render plots without recomputation.