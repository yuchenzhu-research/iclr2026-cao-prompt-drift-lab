# Prompt Drift Lab

[![zh-CN](https://img.shields.io/badge/Language-中文-blue.svg)](README_zh-CN.md)

This repository contains the frozen evaluation artifacts and tooling for **Prompt Drift Lab**, a methodology for studying how small, seemingly benign perturbations in instructions trigger catastrophic failures in Large Language Models (LLMs) regarding instruction following, schema compliance, and semantic alignment. The repository acts as an auditable database of prompts, raw generator outputs (PDFs), LLM judge bundles (JSON), and processed scoring tables (CSVs) which support the main findings of the accompanying paper. Tools are provided for deterministic audit, record materialization, and figure generation directly from frozen artifacts.

**Author**: Yuchen Zhu

### Key Contributions
- **Auditable Evaluation Chain**: A strict, one-way verifiable pipeline from prompt variant to raw model output, judge bundle, and final CSV table.
- **Frozen Artifacts**: All responses and judge decisions are pre-computed and stored to ensure deterministic reproducibility without relying on stochastic LLM APIs.
- **Failure Taxonomy**: A formalized schema tracking the specific nature of failures (e.g., semantic vs. schema).
- **Tooling Support**: Offline utilities capable of exactly regenerating paper figures and aggregating intermediate JSONs.

---

## Table of Contents

1. [Reproducibility Status](#reproducibility-status)
2. [Quickstart (Minimal Runnable Path)](#quickstart-minimal-runnable-path)
3. [Full Reproduction Pipeline](#full-reproduction-pipeline)
4. [Repository Map](#repository-map)
5. [Artifacts & Audit Trail](#artifacts--audit-trail)
6. [Known Issues & Roadmap](#known-issues--roadmap)
7. [Citation](#citation)
8. [License](#license)

---

## Reproducibility Status

✅ **Runnable (Verified)**
- Rebuilding final PDF figures from processed CSV files (`supplement/tools/figures/*.py`).
- Materializing processed JSON records and recalculating CSV summary tables from cached raw judge JSON bundles.
- Installing the documented python dependencies locally `supplement/tools/requirements.txt`.

⚠️ **Partially Runnable**
- Schema validations and scoring dimensions logic. `compute_scores.py` exists as an archival utility illustrating how scoring rules map onto JSON payloads, but running a full fresh evaluation from scratch requires bringing an arbitrary LLM judge provider.

❌ **Not Runnable (Missing by Design)**
- **Generator Model Inference**: The scripts and API harnesses to invoke Anthropic, OpenAI, or Google endpoints with `02_prompt_variants` to generate the raw PDFs are intentionally absent.
- **Judge Model Execution**: The API scripts to run the evaluation protocol (`judge_prompt.md`) against raw PDFs to build the `02_raw_judge_evaluations` are missing.

---

## Quickstart (Minimal Runnable Path)

The repository provides offline tools to regenerate tables and figures deterministically. Run these commands from the repository root. All dependencies are minimal (NumPy, Pandas, Matplotlib, Seaborn).

**1. Install Dependencies:**
```bash
python -m pip install -r supplement/tools/requirements.txt
```

**2. Audit/Regenerate Records & Summary Tables:**
This step regenerates the authoritative CSV data from raw JSON bundles.
```bash
python -u supplement/tools/ingest/materialize_records.py \
  --ack-legacy --overwrite \
  --runs v0_baseline_judge v1_paraphrase_judge v2_schema_strict_judge
```
*Expected Outputs:*
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`

**3. Regenerate Figures:**
This step creates PDF figures utilizing the `scores_long.csv` tables.
```bash
python supplement/tools/figures/make_figure1_schema_failure_cliff.py
python supplement/tools/figures/make_figure6_judge_comparison.py
```
*Expected Outputs:*
Figures are written directly into `paper_anon_submission/figures/`. 

---

## Full Reproduction Pipeline

The experiment enforces a strictly isolated, one-way data flow. While the generator and judge API execution stages are broken, the intended end-to-end conceptual flow is as follows:

1. **Prompt Generation:** `02_prompt_variants/` (Variants & manifests definitions)
2. **Model Inference [BROKEN LINK ❌]:** Call LLM generators to produce standard formatted responses.
3. **Raw Generator Output Storage:** `04_results/01_raw_model_outputs/` (Saved as frozen `.pdf` files)
4. **Judge Execution [BROKEN LINK ❌]:** Apply `03_evaluation_rules/judge_prompt.md` using LLM as a judge.
5. **Raw Judge Outcomes:** `04_results/02_raw_judge_evaluations/` (Stored as JSON bundles according to `judge_bundle.schema.json`)
6. **Processing & Summary:** `tools/ingest/` validates bundles into standardized JSON records, which are flattened into `04_results/03_processed_evaluations/.../scores_long.csv`.
7. **Plotting:** `tools/figures/` reads `scores_long.csv` directly to plot visual PDFs.

---

## Repository Map

```text
prompt-drift-lab/
├── README_FOR_REVIEWERS.md          # Internal meta documentation for reproduction limits
├── README.md                        # This production README
├── README_zh-CN.md                  # Simplified Chinese README
├── paper_anon_submission/           # LaTeX source code for the paper
│   └── figures/                     # Compiled figures targeting paper PDF
└── supplement/                      # Contains ALL experimental designs, data & tools
    ├── 01_experiment_design/        # Questions, workflow details, split criteria
    ├── 02_prompt_variants/          # Prompt variants and specific perturbations tested
    ├── 03_evaluation_rules/         # Eval protocols, schemas, and scoring criteria
    ├── 04_results/                  # FROZEN Artifacts Directory (Authority mapping)
    │   ├── 01_raw_model_outputs/    # Model generated raw PDF files
    │   ├── 02_raw_judge_evaluations/# LLM judge output JSON blocks
    │   └── 03_processed_evaluations/# Evaluated valid records JSONs AND the final CSVs
    └── tools/                       # Tooling
        ├── ingest/                  # JSON to CSV conversion (materialize_records.py)
        ├── figures/                 # Scripts rendering metrics to plots
        └── requirements.txt         # Minimal dependency tracking
```
*(Note: A duplicate folder `final-version` / `reproducibility` may appear in intermediate repository branches. The logical authoritative root for offline components maps exactly to the `supplement/` and `paper_anon_submission/` namespaces as modeled above.)*

---

## Artifacts & Audit Trail

We provide a direct mapping to establish the provenance of every data point.

- **Protocol & Rules:** Look exclusively at `supplement/03_evaluation_rules/eval_protocol.md`. Everything here overrides other metadata.
- **Paper Numbers (Scores):** Derived strictly from `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`. Look for `scores_long.csv` or `scores_grouped.csv`. **DO NOT MERGE** records across judge versions (e.g. `v0_baseline`, `v1_paraphrase`).
- **Audit Process (Row -> Evidence):**
  1. Pick an arbitrary file row from `scores_long.csv`.
  2. Map to processed JSON in `.../valid_evaluations/**/record_*.json` using row identifiers (`file`, `generator_model`, etc).
  3. Load the corresponding raw generated PDF from `supplement/04_results/01_raw_model_outputs/`.
- **Figures:** 
  - *Figure 1 (Failure Cliff):* Produced by `supplement/tools/figures/make_figure1_schema_failure_cliff.py`
  - *Figure 6 (Judge Comparison):* Produced by `supplement/tools/figures/make_figure6_judge_comparison.py`
  - *(Other figures)* → *TODO: add exact manual tracking maps once remaining figure scripts are consolidated.*

---

## Known Issues & Roadmap

**Known Issues:**
- **Incomplete tooling execution:** `tools/aggregate/` scripts are marked deprecated and cannot rebuild CSVs directly from raw records without custom adaptations.
- **Missing Code Harness:** API execution bindings for generators and evaluating judges currently must be implemented by the community. We solely provide prompts and artifacts.

**Roadmap:**
- [ ] Provide a shim harness to actually let users replay arbitrary new models seamlessly entirely through local APIs or standard providers.
- [ ] Incorporate comprehensive testing and unit-assertions for scoring dimension thresholds.
- [ ] Auto-generate `CITATION.cff` integration.
- [ ] Consolidate the `final-version` and `reproducibility` alias folders to strictly reflect top-level `supplement` paths.

---

## Citation

If you use this repository, please cite:
*(TODO: Replace with actual paper citation/arXiV link. Consider providing a `CITATION.cff` in the root).*
```bibtex
@misc{prompt-drift-lab-2026,
  author = {Yuchen Zhu},
  title = {Prompt Drift Lab: Frozen Artifact for Auditable Prompt-Drift Evaluation},
  year = {2026},
  howpublished = {\url{https://github.com/prompt-drift-lab/prompt-drift-lab}}
}
```

---

## License

**TODO**: An explicit canonical LICENSE file (e.g., MIT or Apache 2.0 for tools, and CC-BY 4.0 for frozen data artifacts) hasn't been mapped to the repo root yet. (Although `supplement/tools/LICENSE` exists, please consult it directly for using the tools).
