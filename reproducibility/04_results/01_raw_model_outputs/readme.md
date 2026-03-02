# Raw Model Outputs

This directory stores **frozen, unmodified** raw outputs produced by each generation model.

## What is included
- Each subdirectory corresponds to **one generation model**.
- Each subdirectory contains the **same set of PDF files**, aligned **by exact file name**.

## What is NOT done here
- No PDF is re-parsed, summarized, or post-processed.
- No content interpretation is performed in this directory.

## Role in the pipeline
This directory serves as an **immutable input snapshot** for downstream judge evaluations and deterministic aggregation.

