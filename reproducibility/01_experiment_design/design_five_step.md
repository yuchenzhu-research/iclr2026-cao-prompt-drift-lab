# Five-Step Experimental Workflow

This document describes the end-to-end experimental workflow of Prompt Drift Lab. It documents how experimental inputs are prepared, how model outputs are generated and preserved, and how evidence is organized for downstream processing. It does not define evaluation criteria, scoring logic, or validity rules.

---

### Scope and Freeze Declaration

Across all prompt variants within an evaluation batch, the following elements remain fixed and are not modified:

- Task definition and question content
- Output contract and required section structure
- Model configuration and execution protocol
- Evaluation criteria, validity rules, and scoring procedures

Prompt wording and instruction emphasis are the only intentionally manipulated variables.  
All observed differences in model behavior are therefore attributed to prompt-level perturbations under a fixed experimental context.

---

## Step 1: Identify Core Artifacts

Each reproducible evaluation batch produces the following artifact categories:

1. Raw model outputs preserved verbatim
2. Per-sample processing records derived from raw outputs
3. Aggregated summaries derived from downstream processing
4. Failure and drift observation notes derived from recorded outputs
5. Protocol and configuration records defining execution context

These categories describe logical roles rather than fixed filenames. Concrete file realizations are specified elsewhere in the repository.

---

## Step 2: Define Task and Output Contract

**Objective:** Fix the task formulation and output structure so that any observed changes in model behavior can be attributed to prompt-level perturbations rather than task or structure drift.

- Evaluation questions are drawn from a predefined question set and are not modified across prompt variants.
- A standard output contract specifies the required section structure and ordering.
- Task intent, question content, and output structure are treated as fixed elements within an evaluation batch.
- This document records the existence of an output contract but does not restate, interpret, or define any evaluation criteria or scoring logic.

---

## Step 3: Apply Minimal Prompt Perturbations

**Objective:** Introduce controlled prompt variations that remain interpretable.

Prompt variants include baseline, long, weak, and conflict conditions. Constraint signaling is applied at implicit and explicit levels. These variants modify prompt wording and instruction emphasis without altering the underlying task specification.

Prompt wording and instruction emphasis are the only manipulated variables in this step.  
No changes are introduced to the underlying task definition, output contract, or evaluation logic.

---

## Step 4: Execute and Preserve Evidence

**Objective:** Ensure traceability and auditability of all generated outputs.

All model outputs are preserved in their original form without manual modification. Each output is associated with execution metadata such as model identifier, prompt variant, trigger type, and question identifier.

Once generated, raw model outputs are treated as immutable artifacts and are not edited, filtered, or post-processed prior to downstream evaluation.

---

## Step 5: Organize Outputs for Downstream Evaluation

**Objective:** Prepare generated outputs for downstream evaluation and analysis without defining evaluation logic.
This step performs no evaluation, interpretation, or judgment of model behavior.

Generated outputs are organized and stored to support downstream evaluation, aggregation, and analysis. All evaluation criteria, validity handling, scoring procedures, and failure definitions are specified exclusively in `supplement/03_evaluation_rules/` and are not duplicated or interpreted here.