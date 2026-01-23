# Tools

This directory contains deterministic, offline utilities for reproducing **record- and figure-level artifacts** from saved judge outputs. The code is intended to be auditable: given fixed inputs, it produces identical outputs.

**Scope constraints**
- No API calls; no model execution.
- No randomness or sampling.
- Tools operate on files already stored in the repository.

**Review boundary**
- Summary tables are **precomputed and shipped** under judge-specific `summary_tables/` directories.
- Reviewers are **not expected** to re-run aggregation/scoring to reproduce reported plots and tables.

---

## Directory layout

Paths are relative to the repository root.

```text
supplement/tools/
  ingest/              # raw judge bundles → processed records (**/*.json)
  aggregate/           # optional dev utilities (records → summary tables)
  figures/             # records/tables → figures
  validation_utils/    # schema validation / consistency checks
  scoring_utils/       # score key conventions (A–E) and helper utilities
  analysis_utils/      # lightweight analysis helpers (grouping, pivots)
  examples/            # minimal examples / smoke tests
  LICENSE
  README.md
```

---

## Reproduction workflow

Run commands from the repository root so relative paths are stable.

### 1) Ingest (optional): raw bundles → processed records

Entry point:
- `supplement/tools/ingest/materialize_records.py`

Inputs:
- `supplement/04_results/02_raw_judge_evaluations/`
  - `diagnostic/v0_baseline_judge/*.json`
  - `final/v1_paraphrase_judge/*.json`
  - `final/v2_schema_strict_judge/*.json`

Outputs (record-level JSON; filenames are not a contract and may be hash-based):
- `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`

Optional logs (audit only):
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/run_meta.json`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/excluded_records.jsonl`
  - Optional; present only when exclusions are non-empty.
  - If absent, interpret as **0 exclusions**.

Example:
```bash
python supplement/tools/ingest/materialize_records.py \
  --ack-legacy \
  --runs v0_baseline_judge v1_paraphrase_judge v2_schema_strict_judge \
  --overwrite
```

---

### 2) Aggregate (not required for review): processed records → summary tables

Precomputed tables are shipped under:

- `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/`
- `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`
- `supplement/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/`

Typical files:
- `scores_long.csv`
- `scores_grouped.csv`
- `run_meta.json`

If you re-generate tables for development/debugging (optional), see:
- `supplement/tools/aggregate/README.md`

---

### 3) Figures: records/tables → paper figures

Figure scripts under `supplement/tools/figures/` render plots from existing artifacts.

Reads (depending on the script):
- `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`

Writes (default):
- `paper/figures/`

Example:
```bash
python supplement/tools/figures/make_figure1_schema_failure_cliff.py
```

---

## Related materials

Evaluation rules and schemas are defined in:
- `supplement/03_evaluation_rules/`

The tools consume these rules through stored artifacts and do not redefine them.