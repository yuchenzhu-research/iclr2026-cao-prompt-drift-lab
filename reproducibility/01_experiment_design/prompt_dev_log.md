# Prompt Development Log

This document records the prompt development process used in this project. It serves as an audit log describing how the base prompt was revised during the development stage prior to evaluation. This file documents process history only and does not define evaluation criteria or outcome judgments.

---

## Scope and Usage

- This log documents prompt construction and revision activities only.
- All observations in this file are based on the development set (Q1–Q2).
- No quantitative results from this stage are reported or aggregated.
- All reported experimental results are derived exclusively from the held-out evaluation set (Q3–Q4).

---

## Base Prompt Versions

- **Base A**: initial prompt version used at the start of development.
- **Base B**: revised prompt version obtained after development-stage revisions.

The transition from Base A to Base B is treated as a revision process driven by observed behaviors during development, not as performance tuning or optimization.

---

## Observed Behaviors (Development Stage)

The following behaviors were observed when applying Base A to the development set (Q1–Q2). These observations are descriptive and are not used for scoring, comparison, or evaluation.

1. **Structural omission**  
   Output sections were sometimes missing or merged, deviating from the intended section layout.

2. **Uncontrolled verbosity**  
   Snapshot sections sometimes contained extended text beyond the intended concise format.

3. **Instruction ambiguity**  
   In cases involving multiple instructions, resolution of instruction priority was inconsistent.

---

## Revision Actions

Each revision listed below corresponds to one or more observed behaviors and reflects adjustments to prompt wording and structure.

1. **Explicit section labeling**  
   Section names and ordering were made explicit in the prompt.

2. **Snapshot brevity guidance**  
   The prompt was revised to encourage concise snapshot content.

3. **Instruction ordering clarification**  
   The prompt wording was adjusted to reduce ambiguity in instruction precedence.

These revisions were applied conservatively and are limited to addressing behaviors observed during development.

---

## Non-Goals and Exclusions

- No quantitative results are computed or reported during development.
- No quantitative comparisons between Base A and Base B are computed or reported; Base A is not used in the evaluation stage.
- No evaluation rules, scoring criteria, or validity definitions are introduced or modified in this file.

---

## Relation to Evaluation Stage

- Base B is treated as a fixed input for all evaluation experiments.
- All prompt variants and ablations are derived from Base B and evaluated only on Q3–Q4.
- Evaluation-stage processing, aggregation, and interpretation are defined exclusively in `supplement/03_evaluation_rules/`.