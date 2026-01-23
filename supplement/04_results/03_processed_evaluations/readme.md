# supplement/04_results/03_processed_evaluations — Processed Evaluations 

This directory stores **deterministic derived artifacts** produced from preserved judge outputs.
It is the canonical home for:

- processed record JSON (`valid_evaluations/**/*.json`), and
- paper-citable numeric tables (`summary_tables/*.csv`).

**Source inputs**
- Raw judge bundles: `supplement/04_results/02_raw_judge_evaluations/`

**Scope constraints**
- Processing operates only on judge JSON bundles + recorded metadata.
- No model inference is executed.

---

## Layout

Each judge run is written to its own subdirectory:

- `supplement/04_results/03_processed_evaluations/<judge_version>/`

Within a `<judge_version>` directory:

- **Valid processed records (audit anchor):**
  - `valid_evaluations/**/*.json`
- Optional invalid records (if produced by the pipeline):
  - `invalid_evaluations/**/*.json`
- **Derived summary tables (paper-citable numeric source):**
  - `summary_tables/scores_long.csv`
  - `summary_tables/scores_grouped.csv`
  - `summary_tables/run_meta.json`
  - `summary_tables/excluded_records.jsonl` (optional; only when exclusions are non-empty)

**Filename contract**
- Processed record JSON filenames are **not a contract** and may be hash-based.
- Consumers should locate records via JSON fields (e.g., `file`, `generator_model`, `judge_model`) rather than filename patterns.

---

## Numeric authority

Paper-citable numbers come **only** from:

- `supplement/04_results/03_processed_evaluations/**/summary_tables/*.csv`

---

## Exclusions (audit)

- `excluded_records.jsonl` is **optional** and only present when exclusions are non-empty.
- If `excluded_records.jsonl` is absent for a judge version, interpret this as **0 exclusions**.

---

## Provenance and regeneration rules

- Every processed record JSON is generated from raw judge bundles under:
  - `supplement/04_results/02_raw_judge_evaluations/`
- Each processed record corresponds to exactly one evaluated file instance.
- `record.file` preserves the evaluated file identifier from the raw judge bundle.
  - v0: may be a bundle-side identifier (not necessarily a repo-relative path).
  - v1/v2: intended to be a repo-relative pointer under `supplement/04_results/01_raw_model_outputs/` for direct lookup.

Derived artifacts in this directory are produced by scripts under:
- `supplement/tools/`

Tools may support overwrite flags (e.g., `--overwrite`). Absent explicit overwrite, existing derived artifacts are treated as immutable.

---

## What this directory does not contain

- Evaluation rules and validity definitions → `supplement/03_evaluation_rules/`
- Raw model outputs (PDFs) → `supplement/04_results/01_raw_model_outputs/`
- Raw judge bundles → `supplement/04_results/02_raw_judge_evaluations/`