# Figures: Render Plots from Frozen Artifacts

This directory contains **figure-generation scripts** that render the paper/supplement plots from **already-provided artifacts**:

- processed evaluation records (`**/*.json`, filenames are not a contract), and
- precomputed summary tables (`summary_tables/*.csv`, paper-citable numeric source).

> Aggregation/scoring outputs are **frozen** and already provided.
> Figure scripts must **not** recompute aggregation/scoring; they only read artifacts and render plots.

---

## Inputs

### Processed records

Figure scripts may read processed record files from:

- `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`

**Notes**:
- Record JSON filenames are **not a contract** and may be hash-based.
- Scripts should locate records via JSON fields (e.g., `file`, `generator_model`, `judge_model`) rather than filename patterns.

### Precomputed summary tables

Precomputed tables live under judge-specific directories:

- `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/`
- `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`
- `supplement/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/`

Typical files include:

- `scores_long.csv`
- `scores_grouped.csv`

---

## Outputs

By default, scripts write figures to:

- `paper/figures/`

If a script supports an output directory argument, use `--out_dir`.

---

## How to run

Recommended: run from **repo root** so relative paths are stable.

Example:

```bash
python supplement/tools/figures/<SCRIPT_NAME>.py
```

If the script supports output selection:

```bash
python supplement/tools/figures/<SCRIPT_NAME>.py --out_dir paper/figures
```

---

## Script inventory

The following scripts correspond to paper/supplement figures (names may map to figure numbers in the manuscript):

- `make_figure1_schema_failure_cliff.py`
- `make_figure2_implicit_heatmap.py`
- `make_figure3_dimension_breakdown.py`
- `make_figure4_dimension_failure_rate.py`
- `make_figure5_judge_comparison.py`

---

## Repro checklist

- [ ] Run from repo root.
- [ ] Confirm processed records exist:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`
- [ ] Confirm precomputed tables exist:
  - `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`
- [ ] Run the desired figure script.
- [ ] Verify outputs were written under `paper/figures/` (or `--out_dir`).

---

## Contract: no hidden recomputation

Figure scripts must be:

- **read-only** w.r.t. record/table artifacts
- **deterministic** (no randomness)
- **side-effect free** except writing image files

Any change in figure appearance must be attributable to changes in the input artifacts, not implicit recomputation.