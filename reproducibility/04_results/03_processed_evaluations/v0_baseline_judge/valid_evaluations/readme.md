# v0 valid_evaluations

This directory mixes one canonical record layer with preserved historical residue.

## Canonical path

Only this subdirectory is part of the current offline rebuild chain:

```text
main_method_cross_model/record_*.json
```

These 96 canonical records are the normalized v0 record layer used for:

- traceability from `scores_long.csv` back to raw evidence
- deterministic rebuilds from raw judge bundles

## Historical residue to ignore in current analysis

The following contents are preserved only for audit history:

- root-level `*.json` files: 79
- `supporting_method_self_eval/`: 48 JSON files

These files reflect earlier export layouts and naming conventions.
Do not glob all JSON under `valid_evaluations/`; target only:

```text
main_method_cross_model/record_*.json
```

## Numeric authority

Paper-citable values still come only from:

```text
../summary_tables/scores_long.csv
../summary_tables/scores_grouped.csv
```
