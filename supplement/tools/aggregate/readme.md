# Aggregate: Processed Records → Summary Tables

This directory documents (and may optionally contain) **deterministic aggregation utilities** that transform
**processed evaluation records** (`**/*.json`, filenames are not a contract) into analysis-ready summary tables
(e.g., `scores_long.csv`, `scores_grouped.csv`) used by the paper/supplement.

> Aggregation outputs are **already provided** in this repository.
> Reviewers do **not** need to run any aggregation script to reproduce the reported results/figures.

---

## Where the precomputed tables live

Precomputed summary tables are stored under judge-specific directories:

- `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/`
- `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`
- `supplement/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/`

Typical files include:

- `scores_long.csv` — long-format, per-record table with dimensions + metadata.
- `scores_grouped.csv` — grouped/aggregated table used for most plots and summaries.
- `run_meta.json` — lightweight metadata (counts/scope) for auditability.

Optional audit artifact:
- `excluded_records.jsonl` (if present): records excluded from aggregation with reasons.
  If absent, interpret as **0 exclusions**.

---

## Scope and responsibilities

The aggregation stage assumes all inputs satisfy:

- Records are **schema-normalized** and stored as individual JSON files under `valid_evaluations/`.
- Each record corresponds to exactly one judged (generator output, prompt variant) instance.
- All schema validation and raw ingestion have already been completed upstream.

This stage is responsible **only** for:

- Reading processed records from:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`
- Grouping, averaging, and reshaping scores
- Producing summary tables written to:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`

This stage is **not** responsible for:

- Parsing raw judge bundles
- Validity filtering of raw judge outputs
- Schema enforcement or normalization
- Any form of model execution or re-evaluation

---

## Determinism and reproducibility

If you choose to re-run aggregation (not required for artifact review), the aggregation utilities are intended to be:

- **Purely deterministic**
- **Stateless**
- **Order-invariant** with respect to input records

Given the same set of input JSON files, aggregation results (`scores_long.csv`, `scores_grouped.csv`, and any derived figures)
should be identical across runs.

No randomness, sampling, or heuristic filtering should occur at this stage.

---

## Judge version independence

Aggregation logic should be identical across judge versions, including:

- `v0_baseline_judge`
- `v1_paraphrase_judge`
- `v2_schema_strict_judge`

Differences between judge versions (diagnostic vs. final settings, schema strictness, prompt robustness) are encoded in the **input records**,
not by branching in aggregation code paths.

---

## Entry point (optional)

No entry point is required for review (tables are precomputed).

If you are regenerating tables for development/debugging, run the script(s) in this directory as documented in their file headers.

---

## Interpretation boundary

Results produced at this stage reflect **point estimates over a fixed set of records**.
They do not estimate variance, statistical significance, or distributional robustness.

---

## Design principle

> Aggregation is treated as a transparent accounting operation, not an experimental manipulation.

Any change in aggregation outputs must be attributable to changes in input records, never to hidden logic at this stage.