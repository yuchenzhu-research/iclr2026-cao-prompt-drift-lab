# compute scores — deterministic JSON-to-summary mapping

## 0. scope

This file specifies the **mechanical behavior** of `03_evaluation_rules/compute_scores.py` only.

- It SHALL describe only actions that `03_evaluation_rules/compute_scores.py` actually performs.
- It MUST NOT introduce evaluation rules, scoring rules, validity rules, or any analysis narrative.
- It MUST NOT parse PDFs or read any natural-language sections from model outputs.

---

## 1. stable inputs

`03_evaluation_rules/compute_scores.py` MUST consume only the following stable inputs:

- `--run_dir`: path to one run directory
- `--rubric`: path to one rubric markdown file
- `--output`: path to one output JSON file

The script MUST NOT:
- read or parse any PDF files
- read any model output text content
- infer semantics from directory names, file names, model names, or metadata labels
- use any `bundle_meta` or run-level metadata as a decision signal

---

## 2. deterministic procedure

Given the same CLI arguments and filesystem existence state, the script MUST behave deterministically.

The procedure is:

1) Check that `run_dir` exists and is a directory.
2) Check that the `rubric` file exists.
3) Create the parent directory for `output` if needed.
4) Write exactly one JSON object to `output` with the fields defined in Section 3.

The procedure MUST NOT depend on:
- filesystem traversal order
- OS-specific directory listing order
- path name semantics

No randomness SHALL be used.

---

## 3. output JSON

The script MUST write a single JSON object to `--output` with exactly the following keys:

- `run_dir`: string, the serialized CLI `--run_dir` value
- `rubric`: string, the serialized CLI `--rubric` value
- `status`: string, fixed value `ok`
- `note`: string, fixed value `Utility script executed for internal analysis only.`

The output MUST be valid strict JSON.

---

## 4. prohibited content

This file and the script behavior it describes MUST NOT include:

- any aggregation of per_file_scores
- any computation over judge records
- any explanation of what summary values mean
- any phase identifiers or phase-based logic
- any result or trend language

---

## 5. correspondence to code

Each section above corresponds directly to `03_evaluation_rules/compute_scores.py`:

- Section 1: argparse definitions for `--run_dir`, `--rubric`, and `--output`
- Section 2 Steps 1–3: filesystem existence checks and parent directory creation
- Section 3: construction of the summary object and JSON serialization

No other behavior is specified in this document.