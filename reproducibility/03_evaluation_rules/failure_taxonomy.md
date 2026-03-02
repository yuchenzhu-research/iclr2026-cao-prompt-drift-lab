# failure taxonomy — contract-violation types

This file defines **failure labels** as a classification table of **contract violations**.

- Each label answers only which contract clause was violated.
- Labels are assigned based on observable violations only.
- Labels do not describe causes, consequences, mitigation, stability, drift, or trends.
- Labels do not reference score values.
- Multiple labels may be assigned to the same record. Label definitions do not overlap.

---

## 1) label set

All labels in this file map to INVALID conditions defined in `validity_criteria.md` and apply to **raw judge bundle outputs**.

### table

| Label | Definition (contract violation) | Contract source |
|---|---|---|
| `NOT_STRICT_JSON` | Violates the strict JSON requirement. The output is not a single JSON object. | `validity_criteria.md` §2.1; `eval_protocol.md` §4.1 |
| `SCHEMA_VALIDATION_FAILURE` | Violates JSON schema validation against `schema/judge_bundle.schema.json`. Required fields are missing, field types are incorrect, or unexpected top-level keys are present. | `validity_criteria.md` §2.2; `eval_protocol.md` §4.1 |
| `PER_FILE_MAPPING_VIOLATION` | Violates the one evaluated file to one `per_file_scores` entry mapping requirement. | `validity_criteria.md` §2.3; `eval_protocol.md` §4.2 |
| `SNAPSHOT_BLOCK_MALFORMED` | Violates the Snapshot block structure. The output does not start with exactly one Snapshot block or the block does not contain exactly one header line and one body paragraph. | `validity_criteria.md` §2.3; `snapshot_contracts.md` §1 |
| `SNAPSHOT_HEADER_MISMATCH` | Violates the Snapshot header requirement. The header is not the canonical form `1. [事实快照]` or its approved English translation `1. [Snapshot]`. | `validity_criteria.md` §2.3; `snapshot_contracts.md` §1 |
| `SNAPSHOT_BODY_SHAPE_VIOLATION` | Violates the Snapshot body shape requirement. The body is not a single paragraph or contains list markers, headings, or a new top-level section. | `validity_criteria.md` §2.3; `snapshot_contracts.md` §1 |
| `SNAPSHOT_WORD_LIMIT_VIOLATION` | Violates the Snapshot length limit of the active snapshot contract. | `validity_criteria.md` §2.4; `snapshot_contracts.md` §3 |
| `SNAPSHOT_PROHIBITED_CONTENT_TYPE` | Violates the Snapshot content-type requirement of the active snapshot contract. | `validity_criteria.md` §2.4; `snapshot_contracts.md` §2 |
| `EXTRA_TOP_LEVEL_CONTENT` | Violates the no-extra-top-level-content requirement. Preamble text, appendix content, trailing paragraphs, or any additional top-level section are present. | `validity_criteria.md` §2.5; `eval_protocol.md` §4.1 |

---

## 2) assignment rules

- A label is assigned if and only if its definition is satisfied.
- If multiple definitions are satisfied, multiple labels are assigned.
- No label is used as a catch-all.

---

## 3) recording format

When storing failure labels in a judge record:
- store labels as an array of strings
- if evidence is stored, include a short excerpt that directly shows the violating text span or missing structure