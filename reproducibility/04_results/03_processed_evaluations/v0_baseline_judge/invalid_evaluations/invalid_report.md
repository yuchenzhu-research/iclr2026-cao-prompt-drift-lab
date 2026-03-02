# 04 Results — Invalid Evaluation Report

## Scope

This report documents **invalid evaluation records** identified during the evaluation phase. All referenced paths are **relative to the repository root**. The report is intended for **audit and inspection only**.

Invalid evaluations are **excluded from all quantitative aggregation and summary tables**. This document does **not** redefine evaluation rules, scoring rubrics, or inclusion criteria.

---

## Overview

- **Location**: `supplement/04_results/03_processed_evaluations/v0_baseline_judge/invalid_evaluations/`
- **Purpose**: summarize evaluation records that fail **protocol-level validity checks** and therefore cannot be aggregated
- **Role**: descriptive and diagnostic; not normative

---

## What Counts as “Invalid”

An evaluation record is classified as **invalid** when the judge output cannot be parsed, aligned, or verified under the evaluation contract.

Invalid evaluations are **not low-scoring results**. A score of `0` is a valid outcome. Invalid records are excluded solely due to **structural or contractual violations**, independent of apparent answer quality.

---

## Relation to Failure Flags

Each invalid record is marked using one or more **failure flags** recorded in the evaluation bundle (e.g., `PROTOCOL_VIOLATION`, `UNPARSABLE_OUTPUT`).

Failure flags are defined in:

- `supplement/03_evaluation_rules/failure_taxonomy.md`

These flags **do not replace scoring dimensions**. They record *why* a record is excluded from aggregation.

---

## Invalid Case Taxonomy

For reporting and inspection, invalid records are grouped into the following categories. These categories are **descriptive**, not normative.

### A. Schema / Format Violation

- Missing required JSON fields
- Incorrect data types
- Extra text outside the JSON object
- Non-parseable JSON

Common flag: `UNPARSABLE_OUTPUT`

---

### B. Instruction Deviation

- Output does not follow the evaluation contract
- Required dimensions are skipped or replaced
- The judge reframes the task (e.g., advisory or meta commentary)

Common flag: `PROTOCOL_VIOLATION`

---

### C. Semantic or Internal Inconsistency

- Assigned scores contradict the accompanying rationale
- Rationale does not correspond to the evaluated content
- Internal contradictions within a single record

Common flags: `INTERNAL_INCONSISTENCY`, `CONTEXT_MISALIGNMENT`

---

### D. Partial Output or Truncation

- Output terminates before completion
- Only a subset of required dimensions is returned

Common flag: `INCOMPLETE_COVERAGE`

---

### E. File-Level Corruption

- Empty files
- Encoding errors
- Files that are not valid JSON

Common flag: *(reserved; not observed in the current snapshot)*

---

## Documented Invalid Cases

The cases below are **illustrative summaries** rather than an exhaustive listing.

### Case 01 — Protocol Violation via Role Drift

- Narrative category: B
- Failure flag(s): `PROTOCOL_VIOLATION`
- Location: `supplement/04_results/03_processed_evaluations/v0_baseline_judge/invalid_evaluations/main_method_cross_model/`
- Description: the judge output departs from the required evaluation structure and shifts into advisory or diagnostic commentary.

---

### Case 02 — Partial Output / Truncation

- Narrative category: D
- Failure flag(s): `INCOMPLETE_COVERAGE`
- Location: `supplement/04_results/03_processed_evaluations/v0_baseline_judge/invalid_evaluations/supporting_method_self_eval/`
- Description: the output terminates before all required dimensions are evaluated.

---

### Case 03 — Instruction Deviation with Inconsistency

- Narrative category: B, C
- Failure flag(s): `PROTOCOL_VIOLATION`, `INTERNAL_INCONSISTENCY`
- Location: `supplement/04_results/03_processed_evaluations/v0_baseline_judge/invalid_evaluations/main_method_cross_model/`
- Description: scores are present, but rationales do not align with the evaluated content or violate the evaluation contract.

---

## Handling Policy

- Invalid evaluations are **excluded from aggregate scoring** and summary tables.
- Invalid records are stored separately from numeric summary tables.
- No manual correction or reinterpretation is applied.

---

## Reproducibility Notes

- This report references directories and categories, not individual filenames.
- Paths correspond to directories present in the submitted artifact.
- The document supports auditability of exclusion decisions rather than completeness.

---

## Limitations

- This report does not attempt to attribute root causes beyond protocol-level classification.
- Categories are not mutually exclusive across cases.
- This document reflects the state of invalid records **at the time this snapshot was generated**.