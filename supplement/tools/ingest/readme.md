# Ingest: Materialize Processed Evaluation Records

This directory contains ingestion utilities used to materialize **standardized processed records**
(`valid_evaluations/**/*.json`) from **raw judge evaluation bundles**.

**Scope / contract**
- This ingest step produces **record-level** artifacts only (JSON + optional exclusions log).
- **Do not** treat this step as a table generator. Any `summary_tables/*.csv` shipped with the repo are
  treated as **provided artifacts**.

---

## Reproducibility status (important)

- **v1_paraphrase_judge** ✅ reproducible
- **v2_schema_strict_judge** ✅ reproducible
- **v0_baseline_judge** ❌ not reproducible

Why v0 is non-reproducible (documented limitation):
- Historical bundle formats / filenames changed over time, and earlier runs contained **model-name inconsistencies**
  (e.g., `ChatGPT → unknown`, duplicated `claude` variants), which makes faithful re-materialization impossible.
- We therefore keep **v0 artifacts as provided** and do not claim they can be regenerated from raw inputs.

If you need v0 for *debugging only*, you may run it explicitly (see below), but the outputs are **non-authoritative**.

---

## What this step does

- Reads raw judge evaluation bundles under:
  - `supplement/04_results/02_raw_judge_evaluations/`
- Applies consistent parsing + validation + filtering to produce standardized records.
- Writes record-level outputs under:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`

These JSON files are the **audit anchor** for downstream analyses and figures.

---

## Entry point

### `materialize_records.py`

**Recommended run (from repo root):**

```bash
python supplement/tools/ingest/materialize_records.py --ack-legacy
```

Default behavior: materialize **v1 + v2** only.

#### (Optional) Include v0 (legacy / not reproducible)

```bash
python supplement/tools/ingest/materialize_records.py --ack-legacy --include-v0 --runs v0_baseline_judge
```

This is for debugging only; do not use it to claim reproducibility of v0 numbers.

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

## Repro checklist

- [ ] Run from repo root so relative paths are stable.
- [ ] Execute:
  - `python supplement/tools/ingest/materialize_records.py --ack-legacy`
- [ ] Verify outputs exist:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`
- [ ] Spot-check record integrity:
  - Confirm each JSON contains `file` + judge/generator metadata + per-dimension scores.
- [ ] Confirm you are not regenerating tables:
  - Do not add scripts that overwrite `summary_tables/*.csv` in the reproducibility path.
