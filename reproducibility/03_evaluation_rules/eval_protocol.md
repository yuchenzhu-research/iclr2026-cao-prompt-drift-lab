# eval protocol

## 0. authority and precedence

This file is the **only normative authority** for evaluation rules in `supplement/03_evaluation_rules/`.

- If any other document conflicts with this file, **this file MUST be followed**.
- `schema/judge_bundle.schema.json` defines the **raw judge bundle JSON shape** and applies **only** to runtime judge outputs.
- `schema/eval_record.schema.json` defines the **canonical eval_record JSON shape** used for validation, aggregation, and reporting.
- Other documents are **subordinate references**. They MUST NOT introduce parallel definitions or alternative atomic units.

---

## 1. scope

This protocol defines:
- what the judge receives as input
- what the judge MUST produce as output at runtime
- how raw judge bundle outputs are normalized
- what counts as a valid/invalid canonical eval_record
- the canonical atomic unit for aggregation

This protocol does **not** define research claims, effect sizes, or performance conclusions.

---

## 2. terms

### 2.1 evaluated file
An **evaluated file** is one artifact produced by a model run.

- In this repository, an evaluated file is stored as a **PDF** that contains a model output.
- The PDF is treated as an **opaque container** whose visible content is the only material the judge may use.

### 2.2 raw judge bundle
A **raw judge bundle** is a single JSON object produced by the judge at runtime.

- A raw judge bundle contains a fixed list of evaluated files.
- A raw judge bundle MAY contain bundle-level metadata for traceability.
- A raw judge bundle MUST NOT be used directly for aggregation or reporting.

### 2.3 canonical eval_record
A **canonical eval_record** is the normalized evaluation unit derived from a raw judge bundle.

- Each canonical eval_record corresponds to **exactly one evaluated file**.
- Canonical eval_records are the **only atomic units** permitted for aggregation, analysis, and reporting.
- Canonical eval_records MUST conform to `schema/eval_record.schema.json`.

---

## 3. judge input and prohibited behaviors

### 3.1 judge input
For each evaluated file, the judge input MUST be:
1) the evaluated file content
2) the active evaluation rules
3) the active scoring scale definitions

No other inputs are permitted.

### 3.2 prohibited behaviors
The judge MUST NOT:
- re-parse or reconstruct the PDF into a new representation
- manually reinterpret the task by injecting unstated assumptions
- infer semantics from file paths, file names, directory names, model names, or bundle composition
- use external knowledge of repository structure as a scoring shortcut

The evaluated file name MAY be recorded for alignment only, but it MUST NOT affect scoring.

---

## 4. runtime judge output

### 4.1 raw judge bundle output
Each evaluation run MUST produce **one** raw judge bundle.

- The raw judge bundle MUST validate against `schema/judge_bundle.schema.json`.
- The raw judge bundle MAY include run-level metadata and bundle-level notes.
- The raw judge bundle MUST include `per_file_scores` entries, one per evaluated file.

### 4.2 per_file_scores
`per_file_scores` exists **only** in raw judge bundles.

Rules:
- One evaluated file MUST map to exactly one `per_file_scores` entry.
- The `file` field MUST preserve the file identifier character-for-character.
- Scores and optional evidence in `per_file_scores` MUST be produced according to `scoring_dimensions.md` and `snapshot_contracts.md`.

`per_file_scores` MUST NOT be treated as an aggregation unit.

---

## 5. normalization

Raw judge bundles MUST be deterministically normalized into canonical eval_records.

Normalization rules:
- Each `per_file_scores` entry in a raw judge bundle produces exactly one canonical eval_record.
- Scores and evidence are copied **without modification**.
- Bundle-level metadata MUST NOT influence canonical scores.
- Normalization MUST be lossless and deterministic.

---

## 6. validity screening

A canonical eval_record is INVALID if any of the following holds:
- it is not strict JSON
- validation against `schema/eval_record.schema.json` fails
- any required canonical field is missing or has the wrong type
- any structural constraint required by the active phase is violated

Invalid canonical records:
- MUST be retained for protocol audit
- MUST NOT be included in aggregation or reporting

---

## 7. phases

Phases differ only by **judge mode** and **structural constraints**.

### 7.1 Phase 0: diagnostic
- Diagnostic only
- MUST NOT be used for final claims
- Any relaxations MUST be explicitly stated in the judge prompt

### 7.2 Phase 1: primary judging
- Primary mode used for aggregation
- MUST enforce all active structural constraints

### 7.3 Phase 2: strict structure enforcement
- Enforces all Phase 1 requirements
- Enforces additional structure rules stated for Phase 2

A run MUST NOT mix multiple phases within a single raw judge bundle.

---

## 8. cross-model judging and self-judging

### 8.1 cross-model judging
- Judge evaluates outputs produced by a different model
- Canonical eval_records MAY be aggregated if valid

### 8.2 self-judging
- Generator model judges its own outputs
- MUST be labeled in metadata
- MUST NOT be the sole basis of aggregated results

---

## 9. references

The following documents are subordinate references and MUST NOT override this protocol:

- `snapshot_contracts.md`
- `scoring_dimensions.md`
- `failure_taxonomy.md`
- `judge_prompt.md`
- `schema/judge_bundle.schema.json`
- `schema/eval_record.schema.json`

---

## 10. change control

- Any change to this protocol MUST be versioned by commit.
- Runs MUST record the protocol version identifier used in metadata.