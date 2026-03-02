# valid_evaluations (audit-only, non-normative)

This directory contains record-level evaluation artifacts generated during
early iterations of the evaluation pipeline.

These files are **preserved for auditability only** and are **NOT part of the
reproducible pipeline** for this submission.

---

## Reproducibility boundary (IMPORTANT)

All paper-citable numbers and all figures are reproduced **exclusively** from:

```
../summary_tables/scores_long.csv
```

Files under `valid_evaluations/` are **not read by any figure script** and are
not required for reproducing results.

---

## About model naming in this directory

You may notice record filenames or metadata referring to model identifiers such as:

- `Gemini-3-Flash`
- `unknown_*`
- other historical or inferred identifiers

These identifiers appear due to **historical differences between experimental
design iterations and early processing scripts**, including:

- evolving generator model naming conventions
- intermediate inference metadata used during early audit passes
- partial or inferred labels recorded at the time of evaluation

Importantly:

> **These identifiers do NOT reflect the actual set of generator models used in
the final experiments reported in the paper.**

---

## Canonical generator models used in this submission

Across all reported experiments and figures, the **only generator models used**
are:

```
anthropic_claude-sonnet-4.5_extended-thinking
google_gemini-3-pro
openai_gpt-5.2_extended-thinking
```

Any other model names appearing in this directory should be treated as
**historical artifacts** and **ignored for analysis and interpretation**.

---

## Why these files are kept

These record-level JSON files are retained to support:

- end-to-end traceability (table → record → raw output)
- offline auditing and debugging
- methodological transparency

They are **read-only evidence**, not analytical inputs.

---

## Summary

- ✅ Authoritative data source: `summary_tables/scores_long.csv`
- ❌ `valid_evaluations/` is NOT part of the reproducible pipeline
- ❌ Model names in this directory are NOT normative
- ✅ Final analysis uses exactly three generator models (listed above)

For reproduction instructions, please refer to:
- `supplement/tools/README.md`
- repository root `README_FOR_REVIEWERS.md`

