# Prompt Drift Lab — Audit-Oriented Evaluation of Prompt Drift under Small Prompt Perturbations

> **Reviewer entry (single entry point):** start from `README_FOR_REVIEWERS.md`.

## Overview

This repository is a frozen artifact pack for studying **prompt drift** in large language models: how small, localized changes in prompt structure, wording, or formatting can lead to failures in instruction following, output schema compliance, and semantic alignment.

The focus is audit-oriented: failures are made explicit, traceable, and inspectable under controlled prompt variations.

---

## Evidence chain

**inputs → raw outputs (PDF) → judge artifacts (JSON) → summary tables (CSV)**

All numbers reported in the CSV tables are traceable to stored per-file record JSON and the original raw PDF outputs.

---

## Authority

- **Normative evaluation rules:** `supplement/03_evaluation_rules/eval_protocol.md`
- **Normative reported numbers:** `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/*.csv`
- Other READMEs / notes are **explanatory only** and must not override the two items above.

---

## Quickstart (2–5 minutes)

### 1) Specify the judge version

Judge versions live under:
- `supplement/04_results/03_processed_evaluations/`

This artifact pack includes:
- `v0_baseline_judge/`
- `v1_paraphrase_judge/`
- `v2_schema_strict_judge/`
- `readme.md`

Set `<judge_version>` to the version you cite and keep it fixed when reading tables.

Example:
- `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`

### 2) Open the cited result tables (no code required)

- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`

### 3) Open the normative evaluation protocol

- `supplement/03_evaluation_rules/eval_protocol.md`

---

## Repository structure

- `supplement/` — all materials needed for audit covering design, rules, controls and results
  - `supplement/README.md` — index of the supplement; does not override the **Authority** section above
  - `supplement/01_experiment_design/` — prompt sets, question sets and output schemas
  - `supplement/02/prompt_variants/` - alternative prompt wordings used for robustness comparision; non-normative
  - `supplement/03_evaluation_rules/` — evaluation protocol defining the normative rules
  - `supplement/04_results/` — raw outputs and processed evaluation results used to produce reported numbers
  - `supplement/05_methodological_addenda_and_controls` - methodological notes and control analyses supporting interpretation
  - `supplement/tools/` — reproducible scripts that transform raw outputs into evaluation tables

---

## Traceability (table row → record JSON → raw PDF)

### A) From a CSV row to its record JSON

Each CSV row corresponds to a per-file record stored in:

- `supplement/04_results/02_cross_model_evaluation/valid_evaluations/*.json`

Use the `record_id` / `file` / `pdf_name` fields (as present) to locate the exact record.

### B) From record JSON to raw PDF

Raw model outputs are stored under:

- `supplement/04_results/01_raw_model_outputs/<raw_model_dir>/<pdf_name>`

Where `<raw_model_dir>` is the model bucket directory (e.g., `chatgpt-5.2-thinking/`, `google_gemini-3-pro/`, `claude-3.x/`) and `<pdf_name>` is the PDF file name referenced by the record.

If a record field is:
- `pdf_name: q3_baseline_explicit.pdf`

Then the corresponding raw PDF is found by:
- locating the model bucket directory for that record, then
- opening `supplement/04_results/01_raw_model_outputs/<raw_model_dir>/q3_baseline_explicit.pdf`

> Note: record fields may not include the model bucket prefix; the authoritative raw PDF location is the two-level path above.

---

## Optional local check

If you want to sanity-check file presence locally, these are optional:

```bash
# show the normative summary tables
ls supplement/04_results/03_processed_evaluations/*/summary_tables/

# find a specific raw pdf name anywhere under raw outputs
find supplement/04_results/01_raw_model_outputs -name "q3_baseline_explicit.pdf"
```

---

## Privacy / anonymization

- `ANONYMIZATION_CHECKLIST.md` is provided as a **suggested** reviewer-facing checklist.
- The artifact aims to avoid personal identifiers in file contents and paths.