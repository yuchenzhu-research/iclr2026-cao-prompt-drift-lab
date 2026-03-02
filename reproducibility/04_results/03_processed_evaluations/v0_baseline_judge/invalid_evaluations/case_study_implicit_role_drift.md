# 04 Results — Case Study: Implicit Prompt Role Drift

## Context

This case documents an invalid evaluation observed under the **implicit prompt** setting.
The evaluation was intended to follow the standard three-section judge contract defined in the evaluation protocol.

Instead of executing the evaluation task, the judge response deviated at the role level.

---

## What was expected

The judge was required to:

1. Produce a **fact snapshot** (≤50 characters, descriptive only)
2. Provide **ChatGPT online search instructions**
3. Provide **Gemini deep research instructions**

These three sections must appear in order and be directly usable for aggregation.

---

## What happened

The actual output did not contain the required three sections.

Rather than evaluating the provided content, the judge response reframed the task and produced a free-form analysis that critiques the prompt/task framing and suggests refinements.

The response resembled advisory or diagnostic commentary instead of an evaluation record.

---

## Failure classification

This record is marked with the following failure flag:

- **PROTOCOL_VIOLATION**

Rationale:

- The judge did not execute the evaluation contract.
- The output structure was replaced by prompt critique and meta-level discussion.
- As a result, the output cannot be parsed or scored under the rubric.

---

## Evidence excerpt

> *"The prompt is attempting to combine several objectives, which makes it difficult to produce a clean evaluation. A clearer separation between analysis and instruction would improve reliability..."*

This excerpt illustrates role drift from *evaluator* to *advisor*.

---

## Why this case matters

This failure is not a formatting error in isolation.
It illustrates that LLM-based judges can drift away from an evaluation role under implicit or weakly specified constraints.

Such cases motivate the explicit separation between:

- valid but low-scoring evaluations, and
- evaluations that fail to execute the protocol altogether.

---

## Handling in analysis

- This record is retained in the artifact for transparency.
- It is excluded from quantitative aggregation.
- It is logged as an invalid record with failure flag `PROTOCOL_VIOLATION` for audit and inspection.

This treatment avoids silent exclusions and preserves auditability.