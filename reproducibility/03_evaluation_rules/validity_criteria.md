# validity criteria

This file defines a binary validity adjudication for **raw judge bundle outputs** only.

The adjudication determines whether a raw judge bundle is structurally admissible under the active evaluation protocol.

It does not assess score quality, semantic correctness, or analytical value.

---

## 1. validity states

Each raw judge bundle is assigned exactly one of the following states:

- **VALID**
- **INVALID**

A bundle marked INVALID MUST NOT be used for aggregation or reporting. It MUST be retained for audit.

---

## 2. invalid conditions

A raw judge bundle is INVALID if any of the following conditions holds.

### 2.1 malformed JSON

The output is not strict JSON.

---

### 2.2 schema validation failure

The output fails validation against `schema/judge_bundle.schema.json`.

This includes, but is not limited to:

- missing required top-level fields
- incorrect field types
- unexpected top-level keys
- `per_file_scores` missing or not an array
- any element of `per_file_scores` missing required subfields

---

### 2.3 per-file structural violation

For any entry in `per_file_scores`, one or more of the following holds:

- the Snapshot header is not the canonical form `1. [事实快照]`, or its approved English translation `1. [Snapshot]`
- required sections are missing or appear out of order
- a required section is empty

---

### 2.4 snapshot contract violation

For any entry in `per_file_scores`, the Snapshot section violates the active Snapshot contract.

This includes violations of:

- required header form
- body structure
- length limit
- prohibited content types

---

### 2.5 extra top-level material

The output contains additional top-level material outside the required sections.

This includes:

- preamble text before the Snapshot section
- appendix or trailing content after the final required section
- any additional top-level section

---

## 3. non-criteria

The following MUST NOT affect validity adjudication:

- numerical score values
- score distribution across files
- presence or absence of optional evidence fields
- bundle-level metadata values
- model identity or run configuration

---

## 4. scope of enforcement

Validity adjudication is applied at the **raw judge bundle level**.

It is not applied to canonical eval_records derived during normalization.

Canonical record validation is governed separately by `schema/eval_record.schema.json`.

---

## 5. precedence

If any subordinate document describes validity in a way that conflicts with this file, this file takes precedence.