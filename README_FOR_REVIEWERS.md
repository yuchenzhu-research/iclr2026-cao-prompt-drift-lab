# README_FOR_REVIEWERS.md

# Prompt Drift Lab — Frozen Artifact for Auditable Prompt-Drift Evaluation

This repository is a frozen artifact pack for studying **prompt drift**: small prompt perturbations that trigger failures in instruction following, schema compliance, and semantic alignment.

**What is frozen.** All raw outputs, judge bundles, rules, and derived tables shipped here are fixed. Tools are deterministic file transforms.

**Single source of truth.**
- Evaluation rules and validity criteria: `supplement/03_evaluation_rules/`
- Paper-citable numbers: `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`

Everything else is explanatory.

---

## Repository entry points

- Reviewer entry: this file (`README_FOR_REVIEWERS.md`)
- Supplement index (directory map): `supplement/README.md`
- Canonical results store: `supplement/04_results/`

Top-level layout:
- `paper/` — LaTeX source (figures are read from `paper/figures/`)
- `supplement/` — design, rules, results, and tools

---

## 30-second check (no code)

1) Choose a judge version under:
`\supplement/04_results/03_processed_evaluations/`

This artifact includes:
- `v0_baseline_judge/`
- `v1_paraphrase_judge/`
- `v2_schema_strict_judge/`

2) Open the per-judge tables (paper-citable):
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`

3) Open the protocol:
- `supplement/03_evaluation_rules/eval_protocol.md`

Interpret tables only under the cited `<judge_version>` (no merging across judge versions).

---

## Traceability (table row → record JSON → raw evidence)

A) From `scores_long.csv` to `record_*.json`

Each row in `scores_long.csv` corresponds to one processed record:
- `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/**/record_*.json`

Join keys are the columns present in the tables (e.g., `file`, `generator_model`, `question_id`, `prompt_variant`, `trigger_type`). Use the row’s identifiers to locate the matching record file.

B) From `record_*.json` to raw PDFs

Raw model outputs are preserved under:
- `supplement/04_results/01_raw_model_outputs/`

Use record-level identifiers (e.g., `file` and/or the table join keys) to locate the corresponding PDF within the appropriate model bucket directory.

Notes:
- `file` is the canonical identifier in judge bundles and processed records.
- If `excluded_records.jsonl` is absent under `summary_tables/`, treat it as zero exclusions for that judge version.

---

## Optional reproducibility (local; deterministic)

The shipped tables are sufficient for inspection. The commands below are a local sanity check that tables can be regenerated from preserved judge bundles.

Run from the repository root:

```bash
python -m pip install -r supplement/tools/requirements.txt

# 1) materialize per-file records (valid_evaluations/record_*.json)
python supplement/tools/ingest/reproduce_valid_evaluations.py \
  --runs v0_baseline_judge v1_paraphrase_judge v2_schema_strict_judge \
  --overwrite

# 2) regenerate per-judge summary tables (scores_long.csv, scores_grouped.csv)
python -u supplement/tools/ingest/materialize_records.py \
  --ack-legacy --overwrite \
  --runs v0_baseline_judge v1_paraphrase_judge v2_schema_strict_judge
```

Expected outputs (for each judge version):
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/run_meta.json`

Optional figure regeneration:

```bash
python supplement/tools/figures/make_figure1_schema_failure_cliff.py
python supplement/tools/figures/make_figure6_judge_comparison.py
```

Figures are written under `paper/figures/`.

---

## Anonymization

See `ANONYMIZATION_CHECKLIST.md`.



# supplement/README.md

# Supplement index

This directory is an index over frozen study materials. It does not override the normative rules or the canonical numeric sources.

Authority
- Rules and validity criteria: `supplement/03_evaluation_rules/`
- Paper-citable numbers: `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`

Directory map
- `01_experiment_design/` — experimental design notes and frozen study framing
- `02_prompt_variants/` — prompt variants used in controlled perturbations
- `03_evaluation_rules/` — evaluation protocol, schema constraints, validity criteria
- `04_results/` — preserved artifacts and canonical processed tables
- `05_methodological_addenda_and_controls/` — non-authoritative methodological notes and comparison boundaries
- `tools/` — deterministic utilities for regenerating records/tables/figures from preserved artifacts