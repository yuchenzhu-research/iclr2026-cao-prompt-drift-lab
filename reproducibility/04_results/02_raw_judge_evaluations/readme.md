# supplement/04_results/02_raw_judge_evaluations — Raw judge outputs

This directory stores judge outputs exactly as produced by the judge model.

- Downstream processing reads from here: `supplement/04_results/03_processed_evaluations/`
- Summary tables are not stored here.

---

## Structure

Judge runs are grouped by intent:

- `diagnostic/` — exploratory runs kept for debugging and reference
- `final/` — runs used for reported results and downstream aggregation

Each run lives in its own directory:

- `supplement/04_results/02_raw_judge_evaluations/{diagnostic|final}/<judge_run_dir>/`

A judge-run directory typically includes judge bundles and run metadata such as `run_meta.json`.

---

## Handling policy

- Files are preserved exactly as generated and are not modified in place.
- Judge outputs are treated as immutable evidence once written.
- Any filtering, exclusion, or regeneration logic is applied only in downstream processing, with the mechanism recorded under:
  - `supplement/04_results/03_processed_evaluations/`