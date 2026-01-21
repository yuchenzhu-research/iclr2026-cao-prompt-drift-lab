# Tools

This folder contains **offline** utilities for reproducing tables and generating figures from the saved judge artifacts.

---

## Main reproduction script

### `reproduce_valid_evaluations.py`
Regenerates the summary tables from the stored per-file judge records.

**Reads**
```
supplement/04_results/03_processed_evaluations/*/valid_evaluations/
```

**Writes**
```
supplement/04_results/03_processed_evaluations/*/summary_tables/
```

Notes:
- Deterministic: same inputs → same tables.
- Offline: no API calls, no LLM invocation.

---

## Figures

Scripts under `figures/` are only for plotting from the processed outputs; they don’t change validity/scoring and aren’t needed if you only want the tables.

- `figures/make_figure1_schema_failure_cliff.py`
- `figures/make_figure2_implicit_heatmap.py`
- `figures/make_figure3_judge_sensitivity.py`

Run these after the summary tables exist (i.e., after `reproduce_valid_evaluations.py`).

---

## Other utilities

- `validation_utils/` — helpers for schema checks (diagnostics)
- `scoring_utils/` — helpers for mapping labels → rubric scores (diagnostics)
- `analysis_utils/` — small analysis helpers (diagnostics)
- `examples/` — example files only
- `legacy/` — archived scripts kept for reference

---

## Where the rules live

Evaluation rules / schemas are defined upstream under:

```
supplement/03_evaluation_rules/
```