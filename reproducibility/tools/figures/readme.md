# Figures: Render Plots from Frozen Artifacts

This directory contains **figure-generation scripts** that render the paper/reproducibility plots from **already-provided artifacts**:

- processed evaluation records (`**/*.json`, filenames are not a contract), and
- precomputed summary tables (`summary_tables/*.csv`, paper-citable numeric source).

> Figure scripts must **not** recompute aggregation/scoring.
> They only read the processed artifacts already present under `03_processed_evaluations/`,
> whether those tables are the shipped copies or were rebuilt upstream via
> `reproducibility/tools/reproduce_valid_evaluations.py --from_raw`.

---

## Inputs

### Processed records

Figure scripts may read processed record files from:

- `reproducibility/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/*.json`

**Notes**:
- Record JSON filenames are **not a contract** and may be hash-based.
- Scripts should locate records via JSON fields (e.g., `file`, `generator_model`, `judge_model`) rather than filename patterns.

### Precomputed summary tables

Precomputed tables live under judge-specific directories:

- `reproducibility/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/`
- `reproducibility/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`
- `reproducibility/04_results/03_processed_evaluations/v2_schema_strict_judge/summary_tables/`

Typical files include:

- `scores_long.csv`
- `scores_grouped.csv`

All figure scripts save PDFs without opening a GUI window by default.
If you want an interactive preview, pass `--show`.

---

## Outputs

Figure scripts support configurable output directories via `--out_dir`:

- **Default**: `reproducibility/tools/figures/` (tool-reproducibility mode)
- **Paper mode**: `paper_anon_submission/figures/` (for LaTeX compilation)

### Usage

**Default (outputs to `reproducibility/tools/figures/`):**
```bash
python reproducibility/tools/figures/make_fig1_heatmap_v1_schema_failure_cliff.py
```

**Custom output directory:**
```bash
python reproducibility/tools/figures/make_fig1_heatmap_v1_schema_failure_cliff.py --out_dir paper_anon_submission/figures
```

**Generate all figures to paper directory:**
```bash
for f in reproducibility/tools/figures/make_fig*.py; do python "$f" --out_dir paper_anon_submission/figures; done
```

---

## Script inventory

| Script | Description | Data Source |
|--------|-------------|-------------|
| `make_fig1_heatmap_v1_schema_failure_cliff.py` | Figure 1: Heatmap of mean total scores under implicit triggers (v1) | `v1_paraphrase_judge` |
| `make_fig2_heatmap_v0_implicit_collapse.py` | Figure 2: Heatmap showing implicit trigger collapse (v0) | `v0_baseline_judge` |
| `make_fig3_dimension_breakdown_v0.py` | Figure 3: Dimension breakdown by generator (explicit vs implicit, v0) | `v0_baseline_judge` |
| `make_fig4_dimension_failure_rate_v0.py` | Figure 4: Dimension failure rates by trigger type (v0) | `v0_baseline_judge` |
| `make_fig5_judge_comparison_v0_v1_v2.py` | Figure 5: Judge version comparison (v0/v1/v2) | All judge versions |

---

## Repro checklist

- [ ] Run from repository root (so relative paths resolve correctly).
- [ ] Confirm precomputed tables exist:
  - `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/`
- [ ] Run the desired figure script:
  - Default: outputs to `reproducibility/tools/figures/`
  - Custom: `python <script>.py --out_dir paper_anon_submission/figures`
- [ ] Verify outputs were written to the specified directory.

---

## Contract: no hidden recomputation

Figure scripts must be:

- **read-only** w.r.t. record/table artifacts
- **deterministic** (no randomness)
- **side-effect free** except writing image files

Any change in figure appearance must be attributable to changes in the input artifacts, not implicit recomputation.

---

## Relationship to paper

Paper figures (`paper_anon_submission/figures/*.pdf`) are **frozen snapshots** of the generated outputs. If you modify code and regenerate figures, the outputs in `reproducibility/tools/figures/` will reflect your changes. For paper compilation, either:
1. Use the frozen figures in `paper_anon_submission/figures/`, or
2. Run scripts with `--out_dir paper_anon_submission/figures` to regenerate.

Do not mix outputs from different script versions when compiling the paper.
