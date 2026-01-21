# supplement/04_results

> This directory is the paper evidence store. It contains preserved outputs and the canonical tables used for every reported number.

## Authority

- Normative evaluation rules live at `supplement/03_evaluation_rules/eval_protocol.md`.
- Normative reported numbers live at `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/*.csv`.
- This file is an index and must not override the two items above.

## Layout

- `01_raw_model_outputs/` holds frozen generator outputs in PDF format.
- `02_raw_judge_evaluations/` holds preserved judge bundles in JSON format produced from those PDFs.
- `03_processed_evaluations/` holds canonical processed records and summary tables organized by judge version.
- `04_results_analysis.md` specifies how paper numbers are derived and traced.

## One way data flow

```
01_raw_model_outputs (PDF)
→ 02_raw_judge_evaluations (JSON bundles)
→ 03_processed_evaluations (record_*.json + summary_tables/*.csv)
→ 04_results_analysis.md
```
Later stages never modify earlier stages.

## Paper numeric sources

All numeric claims in the paper must cite files under `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`.
- Use `scores_grouped.csv` for grouped means.
- Use `scores_long.csv` for row level evidence.
No merge rule. Do not pool results across different judge versions.

## Inclusion and exclusion

Validity criteria are defined under `supplement/03_evaluation_rules/`.
Excluded records and reasons are listed at `03_processed_evaluations/<judge_version>/summary_tables/excluded_records.jsonl`.
Canonical summaries include only valid records.

## Figures

Figures are not stored under `04_results/`.
- Figure generation scripts live at `supplement/tools/figures/`.
- Figure files for LaTeX compilation live at `paper/figures/`.

## Traceability recipe

Target chain is `scores_grouped.csv → scores_long.csv → record_*.json → raw PDF`.
1) Choose a row in `scores_grouped.csv` under the cited judge version.
2) Locate supporting per file row(s) in `scores_long.csv`.
3) From the selected `scores_long.csv` row, copy `file`, `generator_model`, and `prompt_variant`.
4) Locate the matching `record_*.json` under `03_processed_evaluations/<judge_version>/valid_evaluations/`.
5) Open the raw PDF under `01_raw_model_outputs/` using the `record.file` resolution rule documented in `04_results_analysis.md`.

## Guarantees

- Raw artifacts are preserved.
- Processed