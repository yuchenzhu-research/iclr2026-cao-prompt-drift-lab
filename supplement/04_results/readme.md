# supplement/04_results

This directory is the paper evidence store. It contains preserved artifacts and the canonical tables used for every reported number.

## Authority

- Evaluation rules are defined under `supplement/03_evaluation_rules/`.
- Paper-citable numeric sources are the CSV files under:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`
- This file is an index only and must not override the two items above.

## Layout

- `01_raw_model_outputs/` — frozen generator outputs (PDF).
- `02_raw_judge_evaluations/` — preserved judge bundles (JSON) produced from those PDFs.
- `03_processed_evaluations/` — canonical processed records and summary tables organized by judge version.
- `04_results_analysis.md` — provenance note describing how paper numbers map to files and how to trace rows back to raw evidence.

## One-way data flow

```
01_raw_model_outputs (PDF)
→ 02_raw_judge_evaluations (JSON bundles)
→ 03_processed_evaluations (record_*.json + summary_tables/*.csv)
→ 04_results_analysis.md
```

Later stages must not modify earlier stages.

## Paper numeric sources

All numeric claims in the paper must cite files under `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`.

- Use `scores_grouped.csv` for grouped means.
- Use `scores_long.csv` for per-file evidence.

No-merge rule: do not pool results across different judge versions.

## Inclusion and exclusion

Validity criteria are defined under `supplement/03_evaluation_rules/`.

- If exclusions exist, they are recorded in:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/excluded_records.jsonl`
- If `excluded_records.jsonl` is absent, treat it as **zero exclusions** for that judge version.

## Figures

Figures are not stored under `04_results/`.

- Figure generation scripts live at `supplement/tools/figures/`.
- Figure outputs for LaTeX compilation live at `paper/figures/`.

## Traceability recipe (grouped row → long rows → record → raw PDF)

1) Choose a row in `scores_grouped.csv` under the cited judge version.
2) Locate supporting row(s) in `scores_long.csv`.
3) From a `scores_long.csv` row, use join keys such as `file`, `generator_model`, `prompt_variant`, `question_id`, `trigger_type` as applicable.
4) Locate the matching `record_*.json` under:
   - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/`
5) Open the raw PDF under `01_raw_model_outputs/` using the resolution rule documented in `04_results_analysis.md`.