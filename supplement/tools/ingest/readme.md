# Ingest: Materialize Processed Evaluation Records

This directory contains the **authoritative ingestion utilities** used to materialize
**standardized processed records** (`record_*.json`) from **raw judge evaluation bundles**.

> Route A policy: **Aggregation/scoring outputs are frozen** and provided under judge-specific directories:
> - `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/`
> - `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`
> - `supplement/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/`
>
> Ingest only produces **record-level** artifacts.

---

## What this step does

- Reads raw judge evaluation bundles under:
  - `supplement/04_results/02_raw_judge_evaluations/`
- Applies consistent parsing + validation + filtering to produce standardized records.
- Writes record-level outputs under:
  - `supplement/04_results/03_processed_evaluations/**/valid_evaluations/record_*.json`

These `record_*.json` files are the **audit anchor** for all downstream figures.

---

## Entry points

### 1) `materialize_records.py` (authoritative)

Canonical script for materializing processed records.

**Recommended run (from repo root):**

```bash
python supplement/tools/ingest/materialize_records.py
```

### 2) `reproduce_valid_evaluations.py` (optional helper)

Helper script that may perform additional filtering/selection but **still only outputs** `record_*.json`.

**Run (from repo root):**

```bash
python supplement/tools/ingest/reproduce_valid_evaluations.py
```

> Note: This script is **record-level only**. It does **not** generate `scores_long.csv` / `scores_grouped.csv`.

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

- `supplement/04_results/03_processed_evaluations/**/valid_evaluations/record_*.json`

If your run produces exclusions, they should be stored alongside records (e.g., `excluded_records.jsonl`) in the same `valid_evaluations/` directory.

---

## Judge versions and input protocols

Differences between judge versions are encoded **in the raw input bundles** (directory layout + bundle metadata), not by changing ingestion logic.

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

The ingestion code path is intended to be identical across versions; the version-specific behavior should be driven by the bundle contents.

---

## Repro checklist

- [ ] **Run from repo root** (recommended) so relative paths are stable.
- [ ] **Execute the authoritative entry**:
  - `python supplement/tools/ingest/materialize_records.py`
- [ ] **Verify outputs exist**:
  - Check that `supplement/04_results/03_processed_evaluations/**/valid_evaluations/record_*.json` files were created/updated.
- [ ] **Spot-check record integrity**:
  - Open one `record_*.json` and confirm it contains the expected task identifiers + model/judge metadata.
- [ ] **Check exclusions (if any)**:
  - If the run produces an exclusion list (e.g., `excluded_records.jsonl`), ensure it is saved next to `record_*.json` under the same `valid_evaluations/` directory.
- [ ] **Confirm Route A boundary**:
  - No aggregation/scoring needs to be run; tables are already under:
    - `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/`
    - `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`
    - `supplement/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/`
- [ ] **Downstream compatibility**:
  - Figure scripts should only read `record_*.json` and the judge-specific `summary_tables/` directories under:
    - `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/`
    - `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`
    - `supplement/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/`