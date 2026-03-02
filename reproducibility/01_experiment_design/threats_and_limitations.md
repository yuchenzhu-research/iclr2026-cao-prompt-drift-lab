# Threats and Limitations

This document records scope boundaries and limitations of the experimental design. It characterizes factors that may influence interpretation of results without defining or interpreting any evaluation criteria, scoring rules, or validity judgments.

---

## Non-goals

- This file does not define, modify, or interpret evaluation rules, scoring scales, validity criteria, failure definitions, or judgment procedures.
- All evaluation logic is defined exclusively in `supplement/03_evaluation_rules/`.

---

## 1. Construct Validity

### 1.1 Operational Scope of Prompt Drift

This study focuses on observable behavioral changes under small prompt or format perturbations, including:
- instruction-following degradation,
- structural or format breakdown,
- semantic deviation from the requested task intent.

These behaviors may co-occur. This document makes no causal claims regarding relationships among overlapping behaviors.

### 1.2 Measurement Resolution

The definition and granularity of reported evaluation signals are determined by a fixed evaluation protocol. This design documentation does not restate scoring scales, thresholds, or per-level criteria.

### 1.3 Handling Boundaries

Some generated outputs may be deemed non-evaluable under the fixed evaluation protocol.  
Criteria and handling procedures for such cases are defined exclusively in `supplement/03_evaluation_rules/` and are not duplicated here.

---

## 2. Internal Validity

### 2.1 System-Level Factors

Model outputs may be influenced by system-level factors beyond prompt variation, including backend updates, safety enforcement, truncation, and session initialization. Each sample is generated in an independent session with recorded visible parameters. Unobservable system factors are treated as part of the execution environment.

### 2.2 Multi-Factor Prompt Variants

Defined prompt variants (baseline, long, weak, conflict) simultaneously modify multiple prompt attributes such as length, constraint signaling, and conflict degree. Reported comparisons therefore describe associations across conditions rather than isolated causal effects. Accordingly, this study does not attempt single-factor causal attribution within these variants.

### 2.3 Procedure Effects

Fixed evaluation procedures may introduce systematic effects. To support auditability, raw outputs and associated records are preserved to enable third-party inspection.

---

## 3. External Validity

### 3.1 Task Coverage

The evaluated tasks focus on structured-output and template-following scenarios. Findings are not intended to generalize to open-ended question answering, code generation, or long-form writing.

### 3.2 Model and Time Dependence

Observed behaviors depend on specific model versions and execution windows. Model identifiers and execution timestamps are recorded for traceability; systematic cross-time consistency testing is out of scope.

### 3.3 Language Scope

The evaluation primarily uses Chinese-language questions. Language-specific conventions may influence formatting preferences and instruction interpretation. Conclusions are not generalized across languages.

---

## 4. Conclusion Validity

### 4.1 Replication Limits

Each experimental condition currently produces a single output. Variance estimation (e.g., repeated sampling, confidence intervals) is out of scope for this study and is therefore not reported. Findings reflect single realizations rather than distributional properties.

### 4.2 Multi-Dimensional Reporting

Comparisons across questions, models, and reported metrics are descriptive. No significance testing or multiple-comparison correction is applied.

---

## 5. Reproducibility and Auditability

### 5.1 Artifact Alignment

A single execution protocol, unified naming conventions, and frozen evaluation bundles are used to support reproducibility and auditability.

### 5.2 Raw Output Preservation

All model outputs are stored in their original form without manual modification. Evaluation operates directly on raw outputs to preserve an intact evidence chain.