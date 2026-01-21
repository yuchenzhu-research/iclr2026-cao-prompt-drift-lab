# Prompt Drift Lab — Audit-Oriented Evaluation of Prompt Drift under Small Prompt Perturbations

> This `supplement/` folder is an **index + evidence bundle**. If you are reviewing the whole repository, the **single reviewer entry** is the repo-root `README_FOR_REVIEWERS.md`.

This artifact pack evaluates **prompt drift** under small prompt changes (instruction following, schema/format compliance, semantic deviation).

Evidence is organized as a one-way chain:

**inputs → raw outputs (PDF) → judge records (JSON) → summary tables (CSV)**

Numbers in the cited CSV tables are traceable to stored per-file record JSON and the original PDF outputs.

---

## Authority

- **Normative evaluation rules:** `supplement/03_evaluation_rules/eval_protocol.md`
- **Normative reported numbers:** `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/*.csv`
- This `supplement/README.md` is an **index/explainer** and must not override the two items above.

---

## Quickstart

### 1) Fix the judge version

Judge versions live under:
- `supplement/04_results/03_processed_evaluations/`

Available in this artifact pack:
- `v0_baseline_judge/`
- `v1_paraphrase_judge/`
- `v2_schema_strict_judge/`

Set `<judge_version>` to the version used in the submission, then keep it fixed in citations.

**Example path:**
- `supplement/04_results/03_processed_evaluations/v1_paraphrase_judge/summary_tables/`

### 2) Open the cited result tables (no code required)

- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`

### 3) Open the normative evaluation protocol

- `supplement/03_evaluation_rules/eval_protocol.md`

---

## Repository guide

- `supplement/01_experiment_design/` — questions, dev/held-out split, execution notes
- `supplement/02_prompt_variants/` — generator-side prompt variants and manifests
- `supplement/03_evaluation_rules/` — evaluation contracts (protocol, schema, scoring, validity)
- `supplement/04_results/` — frozen evidence and derived outputs (PDF/JSON/CSV)
- `supplement/05_methodological_addenda_and_controls/` — interpretation boundaries, controls, notes
- `supplement/tools/` — **optional** offline utilities (not required for audit)

---

## One-way data flow

```
supplement/01_experiment_design/      
→  supplement/02_prompt_variants/
→  supplement/04_results/01_raw_model_outputs/      (PDF)
→  supplement/04_results/02_raw_judge_evaluations/  (JSON bundles)
→  supplement/04_results/03_processed_evaluations/  (record_*.json + summary_tables/*.csv)
```

---

## Traceability recipe (csv → json → pdf)

Target chain:

**scores_grouped.csv → scores_long.csv → record_*.json → raw PDF**

1) Choose a row in:
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`

2) Locate its supporting per-file row(s) in:
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`

3) From the selected `scores_long.csv` row, copy:
- `file`
- `generator_model`
- `prompt_variant`

4) Locate the corresponding `record_*.json` under:
- `supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations/`

**Optional helper (jq):**
```bash
FILE="...from scores_long.csv..."
MODEL="...from scores_long.csv..."
VARIANT="...from scores_long.csv..."

BASE="./supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations"
find "$BASE" -type f -name 'record_*.json' -print0 \
  | xargs -0 jq -r --arg file "$FILE" --arg model "$MODEL" --arg variant "$VARIANT" \
    'select(.file==$file and .generator_model==$model and .prompt_variant==$variant) | input_filename'
```

**Optional fallback (grep, no jq):**
```bash
FILE="...from scores_long.csv..."
MODEL="...from scores_long.csv..."
VARIANT="...from scores_long.csv..."

BASE="./supplement/04_results/03_processed_evaluations/<judge_version>/valid_evaluations"
find "$BASE" -type f -name 'record_*.json' -print0 \
  | xargs -0 grep -l "\"file\": \"$FILE\"" \
  | xargs grep -l "\"generator_model\": \"$MODEL\"" \
  | xargs grep -l "\"prompt_variant\": \"$VARIANT\""
```

5) Open the raw PDF referenced by the matched record:

Raw PDFs live under:
- `supplement/04_results/01_raw_model_outputs/`

The `record.file` field appears in two forms:
- **Form A (path-like):** `google_gemini-3-pro/q4_weak_explicit.pdf` (already includes the model bucket)
- **Form B (filename-only):** `q3_conflict_implicit.pdf` or `q4 conflict explicit.pdf` (no bucket prefix; sometimes uses spaces)

Use this rule:
- If `record.file` contains `/` → open:
  - `supplement/04_results/01_raw_model_outputs/<record.file>`
- Otherwise, choose `<raw_model_dir>` by `generator_model` and open:
  - `supplement/04_results/01_raw_model_outputs/<raw_model_dir>/<pdf_name>`

`generator_model` → `<raw_model_dir>` mapping used in this pack:
- `chatgpt` → `openai_gpt-5.2_extended-thinking/`
- `gemini` → `google_gemini-3-pro/`
- `claude` → `anthropic_claude-sonnet-4.5_extended-thinking/`

Filename normalization (observed in stored evidence):
- If the filename contains spaces (e.g., `q4 conflict explicit.pdf`), replace spaces with underscores:
  - `q4_conflict_explicit.pdf`

---

## Reproducibility scope

- This pack is **self-contained for audit**: cited CSV tables are backed by stored per-file record JSON and raw PDFs.
- Exact reproduction of LLM judging by re-running a judge model is **not claimed** (LLM judging is stochastic and version-sensitive).