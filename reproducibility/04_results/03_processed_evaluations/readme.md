# 03_processed_evaluations — Processed Evaluations

This directory stores **deterministic, derived artifacts** produced from preserved judge outputs.
It is the canonical source for **paper-citable numeric tables** and **audit-only record traces**.

---

## Reproducibility boundary

**All reproducible results and figures start from:**

```
*/summary_tables/scores_long.csv
```

No figure script reads record-level JSON files directly.

---

## Directory layout

Each judge configuration is written to its own subdirectory:

```
v0_baseline_judge/
v1_paraphrase_judge/
v2_schema_strict_judge/
```

Within each judge directory:

- `summary_tables/`  
  Authoritative, paper-citable numeric tables (CSV/JSON). **This is the only normative source for analysis.**

- `valid_evaluations/`  
  Record-level processed evaluations. **Audit-only; not used for reproduction.**

- `invalid_evaluations/` (optional)  
  Records excluded by evaluation rules, when applicable.

---

## Important note on v0_baseline_judge

The `v0_baseline_judge` directory reflects an **earlier iteration of the evaluation pipeline**.

As a result:

- Record-level files under `v0_baseline_judge/valid_evaluations/` may contain:
  - historical or inferred model identifiers (e.g., `unknown_*`, legacy Gemini variants)
  - intermediate naming conventions that are no longer used in later versions

These artifacts are preserved **for auditability only**.

> **They are NOT used for computing any paper numbers or figures.**

For authoritative v0 results, consumers **must** use:

```
v0_baseline_judge/summary_tables/scores_long.csv
```

Model usage is normalized and finalized at the summary-table level.

---

## v1 / v2 judge runs

`v1_paraphrase_judge` and `v2_schema_strict_judge` were produced after the evaluation contract
was stabilized.

- Record-level naming is consistent
- Generator model identifiers are canonical
- No special handling is required beyond reading `summary_tables/`

---

## Numeric authority

Paper-citable numbers come **only** from:

```
supplement/04_results/03_processed_evaluations/**/summary_tables/*.csv
```

Any other files in this directory should be treated as **non-normative supporting evidence**.

---

## Provenance

- Source inputs: `supplement/04_results/02_raw_judge_evaluations/`
- Processing scripts: `supplement/tools/`
- No model inference is executed in this stage

---

## What this directory does NOT contain

- Prompt variants → `supplement/02_prompt_variants/`
- Evaluation rules → `supplement/03_evaluation_rules/`
- Raw model outputs (PDFs) → `supplement/04_results/01_raw_model_outputs/`
- Reproduction scripts → `supplement/tools/`