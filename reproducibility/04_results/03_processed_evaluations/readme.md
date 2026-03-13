# 03_processed_evaluations — Processed Evaluations

This directory stores **deterministic, derived artifacts** produced from preserved judge outputs.
It contains both the **paper-citable numeric layer** and the **canonical normalized record layer**
used to rebuild those tables from raw judge bundles.

---

## Reproducibility boundary

**All paper-citable numeric analysis starts from:**

```
*/summary_tables/scores_long.csv
```

Figure scripts read `scores_long.csv`.
The rebuild path uses canonical records under:

```
*/valid_evaluations/main_method_cross_model/record_*.json
```

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

- `valid_evaluations/main_method_cross_model/`
  Canonical normalized record JSON used by the active offline rebuild path:
  `raw bundles -> record_*.json -> summary_tables/*.csv`

- `valid_evaluations/` siblings outside `main_method_cross_model/`
  Historical residue kept only for audit context. These paths are not consumed by the current rebuild or figure scripts.

- `invalid_evaluations/` (optional)  
  Records excluded by evaluation rules, when applicable.

---

## Important note on v0_baseline_judge

The `v0_baseline_judge` directory includes an **earlier iteration of the record-export layout**.

As a result:

- Only `v0_baseline_judge/valid_evaluations/main_method_cross_model/record_*.json`
  is canonical for the current rebuild path.
- Additional JSON files under `v0_baseline_judge/valid_evaluations/` root and
  `supporting_method_self_eval/` are preserved historical residue.
- Those historical files may contain inferred model identifiers (e.g., `unknown_*`)
  and earlier naming conventions.

Historical residue is preserved **for auditability only**.
It is not read by the current rebuild scripts or figure scripts.

---

## v1 / v2 judge runs

`v1_paraphrase_judge` and `v2_schema_strict_judge` were produced after the record contract
was stabilized.

- Record-level naming is consistent
- Generator model identifiers are canonical
- No special handling is required beyond reading `summary_tables/`

---

## Numeric authority

Paper-citable numbers come **only** from:

```
reproducibility/04_results/03_processed_evaluations/**/summary_tables/*.csv
```

Any other files in this directory should be treated as **non-normative supporting evidence**.

---

## Provenance

- Source inputs: `reproducibility/04_results/02_raw_judge_evaluations/`
- Processing scripts: `reproducibility/tools/`
- No model inference is executed in this stage
- Structural audit command: `python reproducibility/tools/audit_reproducibility_bundle.py`

---

## What this directory does NOT contain

- Prompt variants → `reproducibility/02_prompt_variants/`
- Evaluation rules → `reproducibility/03_evaluation_rules/`
- Raw model outputs (PDFs) → `reproducibility/04_results/01_raw_model_outputs/`
- Reproduction scripts → `reproducibility/tools/`
