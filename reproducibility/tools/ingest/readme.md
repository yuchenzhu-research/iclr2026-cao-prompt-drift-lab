# Ingest: Materialize Processed Evaluation Records

This directory contains deterministic, offline utilities that normalize preserved
judge bundles into canonical record JSON files.

## Scope

- `materialize_records.py` handles only:
  - `raw judge bundles -> valid_evaluations/main_method_cross_model/record_*.json`
- `reproducibility/tools/reproduce_valid_evaluations.py --from_raw` is the canonical
  full rebuild entry point when you want:
  - `raw judge bundles -> record JSON -> summary tables`

The scripts never call a model and never regenerate judge outputs.

## Canonical usage

Full rebuild:

```bash
python reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records
```

Record-only rebuild:

```bash
python reproducibility/tools/ingest/materialize_records.py --overwrite
```

## What gets normalized

- judge / generator model families are canonicalized to:
  - `chatgpt`
  - `gemini`
  - `claude`
- raw file labels are parsed into:
  - `question_id`
  - `prompt_variant`
  - `trigger_type`
- `total` is sourced in this order:
  - `item.total`
  - `scores.total`
  - derived sum of the five rubric dimensions

This is important because the preserved bundles are not perfectly uniform:
- `v0` uses three generator families: `chatgpt`, `gemini`, `claude`
- `v1` / `v2` only include `chatgpt` and `gemini`
- some bundles omit top-level `total`
- some bundles store totals under `scores.total`
- some bundle metadata uses inconsistent model labels

## Inputs

- `reproducibility/04_results/02_raw_judge_evaluations/diagnostic/...`
- `reproducibility/04_results/02_raw_judge_evaluations/final/...`

## Outputs

- `reproducibility/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/main_method_cross_model/record_*.json`
- optional exclusions log:
  - `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/excluded_records.jsonl`

`materialize_records.py` does not write `scores_long.csv` or `scores_grouped.csv`.
Those tables are written by the top-level rebuild script.
