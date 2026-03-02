# 04 Results — Invalid Evaluations

This directory contains **evaluation records that are excluded from quantitative aggregation**.
These records are preserved **solely for auditability, diagnosis, and transparency**.
They do **not** contribute to any reported statistics or conclusions in the paper.

---

## What “Invalid” Means in This Project

An evaluation record is classified as **invalid** when the judge fails to execute the evaluation contract in a way that is **structurally auditable**.

Invalid evaluations are **not low-quality results**. Low scores (including `0`) correspond to valid evaluations under the protocol. An invalid evaluation is one that cannot be reliably parsed, aligned, or verified, regardless of apparent answer quality.

---

## Relation to Failure Flags

Each invalid evaluation is marked using one or more **failure flags** recorded in the evaluation bundles (e.g., `PROTOCOL_VIOLATION`, `UNPARSABLE_OUTPUT`).

These flags are defined and explained in:

- `supplement/03_evaluation_rules/failure_taxonomy.md`

Failure flags **do not replace scoring dimensions**. They explain *why* an evaluation record is excluded from aggregation.

---

## Unified Evaluation Protocol

All evaluations—both valid and invalid—are expected to follow a **single, unified evaluation protocol**. The protocol defines:

- evaluation units and stable identifiers (`question_id`, `prompt_variant`, `target_model`, `output_id`),
- evaluation methods (cross-model judging and self-judging),
- scoring dimensions and scales,
- strict JSON output requirements,
- and criteria for determining validity.

The protocol itself is fixed for the entire experiment cycle and is **not modified or redefined** within this directory.

---

## Judge Prompts Used

During the evaluation stage, a fixed set of **judge prompts** is used to elicit structured evaluation outputs from judge models. These prompts:

- are identified by stable IDs,
- explicitly reference the unified evaluation protocol,
- enforce strict JSON-only outputs,
- and are reused across all samples within the same evaluation method.

No additional or ad-hoc judge prompts are introduced for invalid evaluations.

---

## Why These Records Are Kept

Invalid evaluations are retained in this directory in order to:

- audit protocol execution failures,
- diagnose failure modes (e.g., role drift, format breakdowns, inconsistencies),
- verify that exclusion rules are applied consistently,
- and support transparency for reviewers.

They are **never** reintegrated into quantitative analysis or summary tables.

---

## Directory Contents

- `main_method_cross_model/`  
  Invalid evaluations produced during cross-model judging.

- `supporting_method_self_eval/`  
  Invalid evaluations produced during self-judging.

- `invalid_report.md`  
  A compact overview of invalid cases, grouped narratively and mapped to failure flags.