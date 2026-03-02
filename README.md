# 🏛️ Prompt Drift Lab

<div align="center">

[![中文](https://img.shields.io/badge/Chinese-blue?style=flat-square&logo=readme)](README_zh-CN.md)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-yellow?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/Status-Audit-blue?style=flat-square)
![Paper](https://img.shields.io/badge/Paper-ICLR%202026%20Workshop-red?style=flat-square&logo=arXiv)

**Catch, Adapt, and Operate: Monitoring ML Models Under Drift Workshop**

</div>

> **"Is single-prompt evaluation really reliable?"**
>
> Our audit reveals that harmless prompt variations can swing model scores dramatically—from 9.31 to 0.50.

---

## 🧭 What Problem Are We Solving?

### The Real-World Dilemma

In LLM evaluation, we commonly follow this workflow:

1. Pick a single prompt
2. Let the model run
3. Declare "Model A is better" or "Model B passes"

But here's the issue: **the prompt is part of the evaluation protocol**. The same task, phrased differently, can yield vastly different results.

### Our Stance

We don't propose new prompting tricks. Instead, we ask directly:

> **If tasks and decoding parameters stay fixed, can tiny prompt changes (rephrasing, adding constraints, rewording) completely flip evaluation conclusions?**

That's exactly what **Prompt Drift Lab** is about—**auditing** evaluation stability.

---

## 🔬 Experimental Design & Key Findings

### 1. How Was the Experiment Set Up?

| Dimension | Setting |
|-----------|---------|
| **Test Tasks** | 2 structured output tasks (Q3, Q4) |
| **Generator Models** | 3 LLMs (ChatGPT, Claude, Gemini) |
| **Prompt Variants** | 4 types: baseline / weak / long / conflict |
| **Instruction Explicitness** | 2 conditions: explicit / implicit |
| **Total Runs** | 16 outputs per model (4 variants × 2 explicitness) |
| **Judging** | Cross-model (Model A judges Model B) + self-judge validation |

### 2. Key Findings

#### Finding F1: Explicitness Dominates Stability

Same model, stark difference between explicit and implicit conditions:

| Model | Explicit Avg | Implicit Avg |
|-------|--------------|--------------|
| Gemini | **9.31** | **0.50** |
| Claude | 4.38 | **0.00** |
| ChatGPT | 9.38 | 7.75 |

> Gemini under implicit instructions drops from 9.31 to 0.50—basically failing.

This shows **"implicit compliance" is a distinct and fragile capability**. Models don't understand hints as reliably as we thought.

#### Finding F2: Rephrasing Changes Conclusions

Looking at Q3 mean scores (task held constant):

| Model | Baseline → Conflict | Change |
|-------|---------------------|--------|
| ChatGPT | 7.50 → 9.75 | **+3.25** |
| Claude | 4.25 → 4.50 | +0.25 |
| Gemini | 4.00 → 4.75 | +0.75 |

Just changing prompt style can turn "this model is mediocre" into "this model is excellent".

#### Finding F3: Single-Prompt Evaluation Misleads

A single snapshot can pick a "good" or "bad" framing, overstating (or understating) reliability.

The audit's value: **making these flips traceable and auditable**, not just post-hoc storytelling.

### 3. Why We Track "Invalid" Cases

Traditional evaluation: record low scores, silently drop cases where judges couldn't evaluate.

Our approach: **treat failures as first-class citizens**.

**Common Failure Types:**

| Type | Description |
|------|-------------|
| 📦 Schema/Format Break | Missing JSON fields, wrong structure |
| 🚪 Instruction Drift | Ignoring format requirements |
| 💬 Evaluation Pollution | Judge discusses rubric instead of scoring |
| 📉 Robustness Failure | Self-judge vs. cross-judge mismatch |

Failures aren't "noise"—they're **evidence of protocol brittleness**.

---

## 📁 Repository Structure

```
📂 prompt-drift-lab/
├── 📄 README.md                        # English README (you're here)
├── 📄 README_zh-CN.md                  # 中文说明
├── 📂 paper_anon_submission/           # 📝 LaTeX source, figures
│   └── 📂 figures/                     # Paper figures
├── 📂 reproducibility/                 # 🔧 Complete reproducible materials
│   ├── 📂 01_experiment_design/        # 🎯 Tasks, output structure, splits
│   ├── 📂 02_prompt_variants/          # 💬 Prompt variants (Chinese)
│   ├── 📂 03_evaluation_rules/         # ⚖️ Eval protocol, scoring, taxonomy
│   │   ├── 📄 eval_protocol.md         # Core protocol (authoritative)
│   │   ├── 📄 judge_prompt.md          # Judge template
│   │   ├── 📄 compute_scores.py        # Scoring script
│   │   ├── 📄 scoring_dimensions.md    # Scoring dimensions
│   │   ├── 📄 failure_taxonomy.md      # Failure classification
│   │   └── 📂 schema/                  # JSON Schema definitions
│   └── 📂 04_results/                  # 📦 Frozen artifacts
│       ├── 📂 01_raw_model_outputs/    # 📄 Raw PDFs
│       ├── 📂 02_raw_judge_evaluations/# 📊 Judge JSON bundles
│       └── 📂 03_processed_evaluations/# 📈 Processed CSVs + failure analysis
└── 📂 final-version/                   # 🎯 Final paper PDF + supplement
```

---

## ⚡ Quickstart: Reproduce Core Results

### Setup

```bash
cd prompt-drift-lab
python -m pip install -r reproducibility/tools/requirements.txt
```

> Dependencies: NumPy, Pandas, Matplotlib, Seaborn

### Step 1: Generate Authoritative CSVs

```bash
python -u reproducibility/tools/ingest/materialize_records.py \
  --overwrite \
  --runs v0_baseline_judge v1_paraphrase_judge v2_schema_strict_judge
```

**Outputs:**
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`

### Step 2: Regenerate Paper Figures

```bash
python reproducibility/tools/figures/make_fig1_heatmap_v1_schema_failure_cliff.py
python reproducibility/tools/figures/make_fig5_judge_comparison_v0_v1_v2.py
```

> 📁 Figures output to `paper_anon_submission/figures/`

---

## 🔗 Data Provenance: From Numbers to Evidence

Every reported data point traces back to raw artifacts:

**1. Table → Raw Record**

1. Open `scores_long.csv`, pick any row
2. Note `record_id` or filename
3. Find corresponding `record_*.json` in `.../valid_evaluations/`

**2. Record → Original Output**

1. Find `file` field in the JSON
2. Locate the PDF in `01_raw_model_outputs/`
3. Compare PDF content with judge scores

**3. Authoritative Protocol**

> ⚠️ Refer to `reproducibility/03_evaluation_rules/eval_protocol.md` as the single source of truth.

---

## ✅ Reproducibility Status

| Capability | Status | Notes |
|------------|--------|-------|
| 🔄 Regenerate Figures | ✅ Verified | Local CSVs work |
| 📊 Generate Summary Tables | ✅ Verified | From cached judge JSONs |
| 🧮 Scoring Logic | ⚠️ Partial | Scripts are archival only |
| 🚀 Full Evaluation from Scratch | ❌ Missing | No LLM API code included |

> **Why no API code?**
>
> To avoid key leakage and API version drift issues, we publish **frozen results only**, not runnable but potentially outdated API scripts.

---

## 🎯 Key Contributions

1. **🔍 Auditable Evaluation Chain**
   > Prompt → Model Output → Judge Bundle → CSV—every step traceable and verifiable

2. **❄️ Frozen Artifacts**
   > Pre-computed results, no LLM API calls needed, 100% deterministic reproducibility

3. **📋 Failure Taxonomy**
   > Systematized classification of judge failures (format errors, refusal to score, etc.)

4. **🛠️ Offline Tooling**
   > No APIs, no dependencies—just run scripts to regenerate all paper figures and analyses

---

## 📋 Best Practices for Evaluation Design

Based on this audit, we recommend:

| Recommendation | Action |
|----------------|--------|
| 💡 Prompt Sensitivity Check | Test with 2-3 rephrasings, don't rely on single prompt |
| 📉 Report Invalid Rates | Document how many outputs couldn't be evaluated |
| 🔗 Artifact Mapping | Every reported number should trace to raw outputs + judge records |

---

## 📖 Citation

If this work aids your research, please cite:

```bibtex
@misc{promptdriftlab2026,
  author       = {Yuchen Zhu},
  title        = {Prompt Drift Lab: Auditing Structured Compliance under Benign Prompt Drift},
  year         = {2026},
  howpublished = {\url{https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab}},
}
```

---

## 📄 License

| Content | License |
|---------|---------|
| 🛠️ Tool Code | MIT License |
| 📦 Data Artifacts | CC-BY 4.0 |

---

## 👤 Author

**Yuchen Zhu(朱宇晨)**

- 🏠 GitHub: [@yuchenzhu-research](https://github.com/yuchenzhu-research)
- 🌍 Project: [iclr2026-cao-prompt-drift-lab](https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab)

Questions or suggestions? Feel free to open an issue!