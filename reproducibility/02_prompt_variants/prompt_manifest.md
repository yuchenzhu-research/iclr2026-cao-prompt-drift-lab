# Prompt Manifest

## Purpose

This document enumerates all executable prompt files used in the project and
states their experimental roles and inclusion rules for quantitative summary tables.
Prompt files are treated as fixed experimental inputs and are not modified during evaluation.

A pilot prompt (Prompt A) may exist for early pipeline/interface validation.
Quantitative evaluation uses a single fixed baseline prompt (Prompt B) plus controlled perturbations.

---

## Prompt Language and Authority

All executable prompt files in this directory are written in **Chinese** and are
used verbatim during experimental execution. English descriptions provided here
are explanatory only and are not executable artifacts.

---

## Prompt Inventory

| File | Variant | Experimental Role |
|---|---|---|
| `00_baseline_prompt_A.txt` | pilot | Pilot / smoke test (qualitative only; excluded from all quantitative summaries) |
| `01_structured_prompt_B.txt` | baseline | Sole evaluation baseline (primary experimental anchor) |
| `02_conflict_prompt.txt` | conflict | Competing-requirements perturbation |
| `03_long_prompt.txt` | long | Redundancy / length perturbation |
| `04_weak_prompt.txt` | weak | Softer-constraint wording perturbation |

**Baseline convention:** The `baseline` label refers exclusively to `01_structured_prompt_B.txt`.
`00_baseline_prompt_A.txt` is dev/pilot-only and is excluded from the evaluation baseline set; the filename is historical and does not indicate its experimental role.

---

## Inclusion Rules for Summary Tables

- **Quantitative aggregation:** `01_structured_prompt_B.txt` and its perturbations
  (`02_conflict_prompt.txt`, `03_long_prompt.txt`, `04_weak_prompt.txt`).
- **Excluded from quantitative summary tables and comparisons:** `00_baseline_prompt_A.txt`.
  No cross-variant or cross-model quantitative comparisons involving Prompt A are computed or reported.
  Prompt A may be referenced only in qualitative notes/examples.

---

## Variant Descriptions (English Summary)

- **pilot**  
  Early development prompt used only to validate the output interface/pipeline. Not used for quantitative evaluation.

- **baseline**  
  Defines the fixed three-section output interface and serves as the sole evaluation reference input (Prompt B).

- **conflict**  
  Adds a competing requirement while keeping the same interface.

- **long**  
  Adds redundant background and repeated guidance to increase input length.

- **weak**  
  Uses softer wording around constraints while keeping the same task.

---

## Reproducibility Notes

Each run records the prompt file name and a cryptographic hash to ensure
traceability across raw outputs, judged records, and aggregated summaries.

---

## Relation to Evaluation Rules

This directory contains only executable prompt inputs. Evaluation procedures and
definitions are specified exclusively in `supplement/03_evaluation_rules/`.