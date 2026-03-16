# Technical Map

This file is for technical auditors who want the artifact boundary, active pipeline,
and current inventory without first reading the scripts.

## Active pipeline

```text
02_prompt_variants/
-> 04_results/01_raw_model_outputs/*.pdf
-> 04_results/02_raw_judge_evaluations/**/judge_*.json
-> 04_results/03_processed_evaluations/<judge_version>/valid_evaluations/main_method_cross_model/record_*.json
-> 04_results/03_processed_evaluations/<judge_version>/summary_tables/{scores_long.csv,scores_grouped.csv}
-> tools/figures/make_fig*.py
```

This pipeline is deterministic and offline. It does not re-run model generation or judging.

## Artifact inventory

| Layer | Current inventory | Notes |
| --- | --- | --- |
| Prompt targets | 2 questions x 4 variants x 2 trigger styles = 16 per generator | design contract |
| Raw generator outputs | 48 PDFs total | 3 generators x 16 PDFs |
| Raw judge bundles | 10 JSON bundles total | `v0=6`, `v1=2`, `v2=2` |
| Canonical processed records | 160 `record_*.json` total | `v0=96`, `v1=32`, `v2=32` |
| Canonical numeric tables | 6 CSV files total | 2 tables per judge version |

## Judge-version matrix

| Judge version | Generator families | Raw judge bundles | Canonical records | Interpretation |
| --- | --- | --- | --- | --- |
| `v0_baseline_judge` | `chatgpt`, `gemini`, `claude` | 6 | 96 | baseline comparison condition |
| `v1_paraphrase_judge` | `chatgpt`, `gemini` | 2 | 32 | Claude removed by design |
| `v2_schema_strict_judge` | `chatgpt`, `gemini` | 2 | 32 | Claude removed by design |

`v1` and `v2` intentionally exclude Claude. That is an experiment-design decision, not a missing-data bug.

## `total` normalization across preserved judge bundles

The current materializer resolves `total` in this order:

1. `item.total`
2. `scores.total`
3. sum of the five rubric dimensions

Observed bundle reality in this snapshot:

| Judge version | `item.total` | `scores.total` | derived from dimensions |
| --- | --- | --- | --- |
| `v0_baseline_judge` | 96 | 0 | 0 |
| `v1_paraphrase_judge` | 16 | 0 | 16 |
| `v2_schema_strict_judge` | 16 | 16 | 0 |

This is the main reason older rebuild scripts could turn missing totals into downstream `0.0`.

## `0` scores vs invalid / excluded records

`total = 0` in `scores_long.csv` is a valid judged outcome. It is not an exclusion.

Exclusions are tracked separately:

- canonical location: `summary_tables/excluded_records.jsonl`
- absence of that file means `0` exclusions for that judge version

Observed valid zero-score counts in the shipped tables:

| Judge version | Generator | Valid zero totals |
| --- | --- | --- |
| `v0_baseline_judge` | `chatgpt` | 3 / 32 |
| `v0_baseline_judge` | `gemini` | 15 / 32 |
| `v0_baseline_judge` | `claude` | 24 / 32 |
| `v1_paraphrase_judge` | `chatgpt` | 0 / 16 |
| `v1_paraphrase_judge` | `gemini` | 0 / 16 |
| `v2_schema_strict_judge` | `chatgpt` | 2 / 16 |
| `v2_schema_strict_judge` | `gemini` | 0 / 16 |

## Canonical vs historical paths

### Canonical paths

- numeric authority:
  - `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/`
- canonical record layer:
  - `reproducibility/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/main_method_cross_model/record_*.json`

### Historical residue to ignore for current rebuild / analysis

Only `v0` contains extra preserved residue outside the canonical record layer:

- `v0_baseline_judge/valid_evaluations/*.json` root-level historical exports: 79 files
- `v0_baseline_judge/valid_evaluations/supporting_method_self_eval/`: 48 files

These files are preserved for audit history only. Current rebuild and figure scripts do not consume them.

## One-command audit

```bash
python reproducibility/tools/audit_reproducibility_bundle.py
```

Useful options:

- `--format json` for machine-readable output
- `--strict` to exit non-zero on invariant mismatch

## Figure-snapshot policy

The repository currently preserves two different figure snapshots:

- `paper_anon_submission/figures/` = anonymized-paper snapshot
- `final-version/figures/` = current camera-ready snapshot

These directories are preserved for different release contexts and are not required to remain byte-identical.

## Optional full release-sync check

```bash
python reproducibility/tools/verify_release_bundle.py
```

Use this command only if you intentionally synchronize the anonymized-paper and camera-ready figure directories.

When that condition is met, the command:

- rebuilds processed artifacts into a temp directory
- runs the structural audit on that rebuilt output
- smoke-tests all figure scripts
- checks that `paper_anon_submission/figures/` is byte-identical to `final-version/figures/`

## One-command rebuild

```bash
python reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records
```

This rebuilds:

- canonical `record_*.json`
- `scores_long.csv`
- `scores_grouped.csv`
- `run_meta.json`
