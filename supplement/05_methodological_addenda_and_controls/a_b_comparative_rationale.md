# A/B Comparative Rationale

## Scope

This note describes the intended methodological roles of Prompt Family A and Prompt Family B in the frozen study. It is descriptive only.

Constraints
- No new experiments, prompts, variables, or evaluation dimensions are introduced.
- This note does not modify evaluation rules, scoring criteria, or any released artifact.
- Any examples referenced are illustrative and are not used to compute, select, or modify reported results.

## Prompt families

### Prompt Family A: exploratory probing

Prompt Family A is used to broaden the observable failure surface under weaker structural constraints. Its purpose is failure discovery and qualitative inspection, not quantitative benchmarking.

Typical properties
- Looser structure and higher degrees of freedom
- Weaker or implicit constraint signaling
- Greater variance across runs

Family A is used to surface breakdowns that may be masked by stricter interfaces, including format collapse, instruction omission/substitution, and semantic drift. Outputs from Family A are not included in any reported aggregates, rankings, or cross-model comparisons.

### Prompt Family B: protocolized measurement anchor

Prompt Family B defines the measurement interface used for reported quantitative analysis. It constrains generation to a stable format suitable for automated scoring and aggregation.

Typical properties
- Fixed output sections and explicit constraints
- Stable field boundaries suitable for scoring
- Reduced degrees of freedom relative to Family A

All reported quantitative results are derived from Prompt Family B and its frozen variants.

## Comparison boundaries

The released setup supports quantitative comparisons only within Prompt Family B.

- No cross-family normalization or ranking is performed.
- Cross-family remarks (A vs B) are descriptive only and should not be interpreted as performance evidence.
- Causal attribution requires minimal ablations (single-factor changes under otherwise fixed conditions); observations without ablation are treated as descriptive.

## Relation to released artifacts

Reported numbers are computed from judge-specific summary tables under:

supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/

Prompt Family A is not used to populate these tables. Prompt Family B (and its frozen variants) is the exclusive source for quantitative reporting.

## Rationale

The A/B separation decouples failure discovery from failure measurement. Family A increases the chance of observing rare or brittle breakdowns for qualitative characterization. Family B provides a controlled interface that makes failures measurable and auditable under fixed rules.