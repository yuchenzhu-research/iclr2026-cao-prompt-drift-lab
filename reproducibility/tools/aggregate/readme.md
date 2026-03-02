# Aggregate (Deprecated)

> **Status: DEPRECATED / HISTORICAL.**
>
> This directory is kept for documentation only.
>
> **Reproduction for this artifact starts from the shipped summary tables (`scores_long.csv`).**
> We do **not** support regenerating these CSV tables from upstream raw bundles / intermediate records.

---

## Reproducibility boundary

**The only authoritative evaluation tables are the shipped `scores_long.csv` files (manually audited/fixed by the authors):**

- `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/scores_long.csv`
- `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/scores_long.csv`
- `supplement/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/scores_long.csv`

All paper figures are reproducible from these CSVs.

### What is *not* reproducible in this submission

We do **not** claim reproducibility for the upstream step that would regenerate `scores_long.csv` from:

- raw judge bundles (e.g., `04_results/02_raw_judge_evaluations/...`)
- intermediate `valid_evaluations/record_*.json`

This upstream aggregation step was used during early development and is **out of scope** for artifact reproduction.

---

## How reviewers should reproduce figures

Reproduction is limited to the following deterministic pipeline:

```
(scores_long.csv tables; v0/v1/v2)  →  figure scripts  →  PDF figures
```

See `supplement/tools/figures/README.md` for the script-to-figure mapping and one-command reproduction instructions.

---

## Rationale

During development, the aggregation step (raw bundles/records → `scores_long.csv`) involved evolving conventions:

- generator model naming normalization
- column completion (`prompt_variant`, `trigger_type`)
- `total` score aggregation consistency

The shipped `scores_long.csv` tables are treated as **frozen artifacts** because they were manually audited and corrected to ensure:

- consistent columns and types
- correct `total` computation
- correct inclusion of non-zero ChatGPT data

---

## Non-goals

- This directory does **not** provide a supported entry point to regenerate CSV tables.
- Reviewers are **not expected** to run any aggregation scripts.

If you are looking for reproduction steps, start from:

- `supplement/04_results/03_processed_evaluations/*/summary_tables/scores_long.csv`
- and run `supplement/tools/figures/*.py`.