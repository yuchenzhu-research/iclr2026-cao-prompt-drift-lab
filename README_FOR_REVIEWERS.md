# Prompt Drift Lab — Frozen Artifact for Auditable Prompt-Drift Evaluation

This repository is a frozen artifact pack for studying **prompt drift**: small prompt perturbations that trigger failures in instruction following, schema compliance, and semantic alignment.

**What is frozen.** All raw outputs, judge bundles, rules, and derived tables shipped here are fixed. Tools are deterministic file transforms.

**Single source of truth.**
- Evaluation rules and validity criteria: `reproducibility/03_evaluation_rules/`
- Paper-citable numbers: `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/`

Everything else is explanatory.

---

## Repository entry points

- Reviewer entry: this file (`README_FOR_REVIEWERS.md`)
- Supplement index (directory map): `reproducibility/README.md`
- Technical audit map: `reproducibility/TECHNICAL_MAP.md`
- Canonical results store: `reproducibility/04_results/`

Top-level layout:
- `paper_anon_submission/` — LaTeX source (figures are read from `paper_anon_submission/figures/`)
- `reproducibility/` — design, rules, results, and tools

---

## 30-second check

1) Choose a judge version under:
`reproducibility/04_results/03_processed_evaluations/`

This artifact includes:
- `v0_baseline_judge/`
- `v1_paraphrase_judge/`
- `v2_schema_strict_judge/`

2) Open the per-judge tables (paper-citable):
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`

3) Open the protocol:
- `reproducibility/03_evaluation_rules/eval_protocol.md`

Interpret tables only under the cited `<judge_version>`.

---

## Traceability (table row → record JSON → raw evidence)

A) From `scores_long.csv` to `record_*.json`

Each row in `scores_long.csv` corresponds to one processed record:
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/main_method_cross_model/record_*.json`

Join keys are the columns present in the tables (e.g., `file`, `generator_model`, `question_id`, `prompt_variant`, `trigger_type`). Use the row’s identifiers to locate the matching record file.

B) From `record_*.json` to raw PDFs

Raw model outputs are preserved under:
- `reproducibility/04_results/01_raw_model_outputs/`

Use record-level identifiers (e.g., `file` and/or the table join keys) to locate the corresponding PDF within the appropriate model bucket directory.

Notes:
- `file` is the canonical identifier in judge bundles and processed records.
- If `excluded_records.jsonl` is absent under `summary_tables/`, treat it as zero exclusions for that judge version.

---

## Reproducibility boundary

**Offline rebuild (reproducible):**
- raw judge bundles → record JSON → `scores_long.csv` + `scores_grouped.csv`
- this path is deterministic and does not re-run judging

**Offline structural audit (reproducible):**
```bash
python reproducibility/tools/audit_reproducibility_bundle.py --strict
```

**Release verification (reproducible, temp-directory, no dirty worktree):**
```bash
python reproducibility/tools/verify_release_bundle.py
```

**Downstream (REPRODUCIBLE):**
- `scores_long.csv` → PDF figures (deterministic)
- published release figures are frozen under `final-version/figures/` and mirrored in `paper_anon_submission/figures/`

Run from the repository root:

### CSV → Figures (reproducible)
```bash
python -m pip install -r reproducibility/tools/requirements.txt

# Generate all figures from frozen CSV tables
for f in reproducibility/tools/figures/make_fig*.py; do
  python "$f" --out_dir paper_anon_submission/figures
done
```

**Full rebuild from preserved raw judge bundles:**
```bash
python reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records
```

Expected outputs (for each judge version):
- `valid_evaluations/main_method_cross_model/record_*.json`
- `scores_long.csv`
- `scores_grouped.csv`
- `run_meta.json`
