# Tools readme

This directory contains deterministic, offline utilities for the reproducibility bundle.
No API calls, no model execution, no randomness.

## Canonical pipeline

The supported offline rebuild path is:

```text
02_raw_judge_evaluations/*.json
-> valid_evaluations/main_method_cross_model/record_*.json
-> summary_tables/scores_long.csv + scores_grouped.csv
-> figures/*.pdf
```

`v0` contains `chatgpt`, `gemini`, and `claude`.
`v1` / `v2` contain only `chatgpt` and `gemini`.

The pipeline is deterministic because it only normalizes preserved artifacts.
It does **not** claim that LLM judging itself is reproducible.

## v0 / v1 / v2 meaning

- `v0_baseline_judge`, `v1_paraphrase_judge`, `v2_schema_strict_judge` are **judge prompt versions** (instrumentation).
- `v0` is **not legacy** in this submission: it is included as a **comparison condition** via the shipped CSV table above.

---

## Directory layout

```text
reproducibility/tools/
  figures/             # scores_long.csv → PDF figures
  ingest/              # raw bundles → record JSON
  aggregate/           # deprecated/historical notes
  validation_utils/    # schema validation / consistency checks
  scoring_utils/       # rubric scoring helpers (deterministic)
  analysis_utils/      # lightweight analysis helpers (grouping, pivots)
  examples/            # minimal examples / smoke tests
  LICENSE
  README.md
```

---

## Reproduction workflow

Run from repository root:

### 1) Full rebuild from raw judge bundles

One command:

```bash
python reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records
```

This does two deterministic steps:

1. `reproducibility/tools/ingest/materialize_records.py`
   - reads `04_results/02_raw_judge_evaluations/**/judge_*.json`
   - writes canonical `record_*.json`
   - normalizes generator/judge families (`chatgpt`, `gemini`, `claude`)
   - derives `total` when raw bundles omit it or place it under `scores.total`

2. `reproducibility/tools/reproduce_valid_evaluations.py`
   - reads those `record_*.json`
   - writes `scores_long.csv` and `scores_grouped.csv`

### 2) Figures: CSV → PDF

All figure scripts read directly from the shipped `scores_long.csv` tables and write PDFs under:

- `reproducibility/tools/figures/`

Example:
```bash
python reproducibility/tools/figures/make_fig2_heatmap_v0_implicit_collapse.py
```

See `reproducibility/tools/figures/README.md` for the script → input CSV → output PDF mapping.

### 3) Record-only rebuild

If you only want the record JSON layer:

```bash
python reproducibility/tools/ingest/materialize_records.py --overwrite
```

---

## Related materials

Evaluation rules and schemas:
- `reproducibility/03_evaluation_rules/`

These tools consume stored artifacts and do not redefine the evaluation rules.
