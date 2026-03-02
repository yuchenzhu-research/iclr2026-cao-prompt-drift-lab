# scoring dimensions

This file defines the meanings of the five scoring fields used in each `per_file_scores.scores` entry.

- Field names MUST match the JSON keys exactly.
- Each dimension is judged independently.
- This file does not define aggregation, validity gates, or run-level rules.

---

## fields

The judge output uses exactly the following five score fields:

- `A_structure`
- `B_snapshot_constraint`
- `C_actionability`
- `D_completeness`
- `E_drift_failure`

Each field is scored on a three-point scale: `0`, `1`, or `2`.

---

## A_structure — three-section structure compliance

**Judged object:** presence and order of the required three sections.

### observable requirements
The output contains three top-level sections in the required order:

1) Snapshot
2) ChatGPT web-search instruction
3) Gemini deep-research instruction

Section identity is determined by the active section header rules.

### score mapping

- **2**: All three required section headers are present, appear in the required order, and each section contains non-empty content.
- **1**: At least two required section headers are present, but one required header is missing, the order is incorrect, or one section is empty.
- **0**: Fewer than two required section headers are present.

---

## B_snapshot_constraint — snapshot contract compliance

**Judged object:** the Snapshot section only.

### observable requirements
The Snapshot section satisfies the active Snapshot contract referenced by run metadata.

Checks include, when applicable:

- required Snapshot header token
- required body shape
- length limit
- allowed and forbidden content types

### score mapping

- **2**: All contract checks pass.
- **1**: At most one contract check fails and the violation is minor.
- **0**: Two or more contract checks fail, or any hard requirement is violated.

---

## C_actionability — ChatGPT web-search instruction executability

**Judged object:** the ChatGPT web-search instruction section only.

### observable requirements
The section is an instruction and includes all of the following:

1) a search target such as a query string or keyword set
2) at least one verifiable constraint
3) a concrete deliverable specification

### score mapping

- **2**: All three components are present.
- **1**: Exactly two of the three components are present.
- **0**: Zero or one component is present, or the section is missing.

---

## D_completeness — Gemini deep-research instruction coverage

**Judged object:** the Gemini deep-research instruction section only.

### observable requirements
The section includes both of the following requirement types:

1) evidence requirements such as sources, links, or timestamps
2) structured-output requirements such as tables, taxonomies, or comparisons

### score mapping

- **2**: Both requirement types are present.
- **1**: Exactly one requirement type is present.
- **0**: Neither requirement type is present, or the section is missing.

---

## E_drift_failure — out-of-protocol content presence

**Judged object:** any text outside the three required sections.

### observable requirements
No additional top-level material appears outside the required sections.

Out-of-protocol material includes:

- preamble text before the first required section
- appendix or trailing content after the third required section
- any additional top-level section

### score mapping

- **2**: No out-of-protocol material is present. Whitespace-only content is allowed.
- **1**: One short out-of-protocol fragment is present.
- **0**: Multiple fragments or any multi-paragraph appendix is present.