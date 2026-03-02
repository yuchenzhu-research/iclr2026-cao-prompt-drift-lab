# Tools readme

This directory contains deterministic, offline utilities used to **audit** and **render figures** from shipped artifacts.
No API calls, no model execution, no randomness.

## Reproducibility boundary (IMPORTANT！！！)

**Reproduction for this submission starts from the shipped evaluation tables (`scores_long.csv`).**

Authoritative CSV tables:

- `reproducibility/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/scores_long.csv`
- `reproducibility/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/scores_long.csv`
- `reproducibility/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/scores_long.csv`

All paper figures are reproducible from these CSVs (**CSV → Figures**).

### What is out of scope

Regenerating `scores_long.csv` from upstream raw judge bundles / intermediate records is **not supported** for this submission.
See `reproducibility/tools/aggregate/README.md` for the deprecated aggregation note.

## v0 / v1 / v2 meaning

- `v0_baseline_judge`, `v1_paraphrase_judge`, `v2_schema_strict_judge` are **judge prompt versions** (instrumentation).
- `v0` is **not legacy** in this submission: it is included as a **comparison condition** via the shipped CSV table above.

---

## Directory layout

```text
reproducibility/tools/
  figures/             # scores_long.csv → PDF figures (reproducible)
  ingest/              # optional audit utilities (raw bundles → record JSON)
  aggregate/           # deprecated/historical notes (no supported CSV regen)
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

### 1) Figures (reproducible): CSV → PDF

All figure scripts read directly from the shipped `scores_long.csv` tables and write PDFs under:

- `reproducibility/tools/figures/`

Example:
```bash
python reproducibility/tools/figures/make_fig2_heatmap_v0_implicit_collapse.py
```

See `reproducibility/tools/figures/README.md` for the script → input CSV → output PDF mapping.

### 2) Ingest (optional audit only)

The ingest utilities materialize record-level JSON from raw bundles for auditing/debugging.
They are **not required** for reproducing figures or paper numbers.

Entry point:
- `reproducibility/tools/ingest/materialize_records.py`

---

## Related materials

Evaluation rules and schemas:
- `reproducibility/03_evaluation_rules/`

These tools consume stored artifacts and do not redefine the evaluation rules.