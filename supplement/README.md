# supplement/ — Index and evidence bundle

This `supplement/` directory is an **index + evidence bundle**. If you are reviewing the whole repository, the single entry point is the repo-root `README_FOR_REVIEWERS.md`.

This artifact evaluates **prompt drift** under small prompt perturbations (instruction following, schema/format compliance, semantic deviation). Evidence is organized as a one-way chain:

inputs → raw outputs (PDF) → judge bundles (JSON) → processed records (JSON) → summary tables (CSV)

Reported numbers in the CSV tables are traceable to stored per-file record JSON and the original PDF outputs.

---

## Authority

Normative sources of truth:

- Evaluation rules and validity criteria:
  `supplement/03_evaluation_rules/eval_protocol.md`

- Paper-citable numeric sources (per judge version):
  `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`

This file is an index/explainer only and must not override the two items above.

---

## Quickstart (no code)

1) Fix a judge version under:
`/supplement/04_results/03_processed_evaluations/`

This artifact includes:
- `v0_baseline_judge/`
- `v1_paraphrase_judge/`
- `v2_schema_strict_judge/`

2) Open the canonical tables for the chosen `<judge_version>`:
- `summary_tables/scores_grouped.csv`
- `summary_tables/scores_long.csv`

3) Open the normative protocol:
- `supplement/03_evaluation_rules/eval_protocol.md`

Interpret tables only within the cited `<judge_version>` (no merging across judge versions).

---

## Directory guide

- `01_experiment_design/` — questions, splits, execution notes
- `02_prompt_variants/` — generator-side prompt variants and manifests
- `03_evaluation_rules/` — protocol, schema, scoring, validity
- `04_results/` — frozen evidence and derived outputs (PDF/JSON/CSV)
- `05_methodological_addenda_and_controls/` — non-authoritative addenda and interpretation boundaries
- `tools/` — optional offline utilities (deterministic; not required for audit)

---

## One-way data flow

```
02_prompt_variants/
→ 04_results/01_raw_model_outputs/      (PDF)
→ 04_results/02_raw_judge_evaluations/  (JSON bundles)
→ 04_results/03_processed_evaluations/  (record_*.json + summary_tables/*.csv)
```

Later stages must not modify earlier stages.

---

## Traceability (CSV → record JSON → raw PDF)

Target chain:

scores_grouped.csv → scores_long.csv → record_*.json → raw PDF

1) Choose a row in:
`.../<judge_version>/summary_tables/scores_grouped.csv`

2) Locate supporting row(s) in:
`.../<judge_version>/summary_tables/scores_long.csv`

3) Use identifiers from the selected `scores_long.csv` row (columns such as `file`, `generator_model`, `question_id`, `prompt_variant`, `trigger_type`) to locate the matching record:

`.../<judge_version>/valid_evaluations/**/record_*.json`

4) Open the raw PDF under:
`04_results/01_raw_model_outputs/`

Identifier conventions:
- `file` is the canonical file identifier in judge bundles and processed records.
- `record.file` may be path-like (contains `/`) or filename-only. If it is filename-only, locate the PDF by searching within `01_raw_model_outputs/`.

Optional helper (filename-only lookup):
```bash
cd supplement/04_results/01_raw_model_outputs
PDF_NAME="q4_conflict_explicit.pdf"  # from record.file or inferred from table join keys
find . -type f -name "$PDF_NAME" -print
```

---

## Reproducibility scope

- This pack is self-contained for audit: the shipped CSV tables are backed by stored record JSON and raw PDFs.
- Deterministic re-materialization of records/tables from preserved judge bundles is supported via `supplement/tools/`.
- Re-running LLM judging is not claimed as reproducible (judge models are stochastic and version-sensitive).