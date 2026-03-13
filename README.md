<div align="center">

# Prompt Drift Lab

**Catch, Adapt, and Operate: Monitoring ML Models Under Drift Workshop**

<p align="center">
  <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY%204.0-yellow?style=flat-square" alt="License: CC BY 4.0" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License: MIT" /></a>
  <img src="https://img.shields.io/badge/Status-Audit-blue?style=flat-square" alt="Status" />
  <img src="https://img.shields.io/badge/Paper-ICLR%202026%20Workshop-red?style=flat-square&logo=arXiv" alt="Paper" />
</p>

<p align="center">
  <strong>
    <a href="README_zh-CN.md">简体中文</a> |
    English
  </strong>
</p>

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
prompt-drift-lab/
├── README.md
├── README_zh-CN.md
├── README_FOR_REVIEWERS.md
├── paper_anon_submission/figures/      # frozen paper figures
├── final-version/figures/              # published release figures
└── reproducibility/
    ├── TECHNICAL_MAP.md                # engineering-facing artifact map
    ├── 03_evaluation_rules/            # authoritative protocol and validity rules
    ├── 04_results/                     # raw evidence + canonical processed outputs
    └── tools/                          # offline rebuild, audit, and figure scripts
```

Recommended entry points:

- `README_FOR_REVIEWERS.md` for review flow
- `reproducibility/TECHNICAL_MAP.md` for pipeline, counts, and contracts
- `reproducibility/03_evaluation_rules/eval_protocol.md` for normative protocol
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/` for paper-citable numbers

---

## ⚡ Quickstart: Verification and Rebuild

### Setup

```bash
cd prompt-drift-lab
python -m pip install -r reproducibility/tools/requirements.txt
```

Standard Python dependencies: NumPy, Pandas, Matplotlib, Seaborn.

### One-command release verification

```bash
python reproducibility/tools/verify_release_bundle.py
```

This command:

- rebuilds processed artifacts into a temp directory
- runs the structural audit
- smoke-tests all figure scripts
- verifies that `paper_anon_submission/figures/` is byte-identical to `final-version/figures/`

### Full offline rebuild from preserved judge bundles

```bash
python reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records
```

Outputs:

- `valid_evaluations/main_method_cross_model/record_*.json`
- `scores_long.csv`
- `scores_grouped.csv`
- `run_meta.json`

### Regenerate figures

```bash
for f in reproducibility/tools/figures/make_fig*.py; do
  python "$f" --out_dir paper_anon_submission/figures
done
```

---

## 🔗 Data Provenance: From Numbers to Evidence

Every reported value is traceable through a fixed artifact chain:

```text
scores_grouped.csv
→ scores_long.csv
→ valid_evaluations/main_method_cross_model/record_*.json
→ 01_raw_model_outputs/*.pdf
```

Authoritative interpretation rules:

- Protocol and validity criteria: `reproducibility/03_evaluation_rules/eval_protocol.md`
- Numeric authority: `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/`
- Do not merge results across different judge versions (`v0`, `v1`, `v2`)

---

## ✅ Release Status

| Capability | Status | Notes |
|------------|--------|-------|
| Release verification | ✅ Verified | `verify_release_bundle.py` rebuilds in temp space and checks release-figure hashes |
| Offline artifact rebuild | ✅ Verified | preserved judge bundles → canonical records → summary tables |
| Figure regeneration | ✅ Verified | `scores_long.csv` → PDF figures |
| Live API replay | Out of scope by design | no vendor API keys or live judging scripts are shipped |

This repository supports **artifact-scope reproducibility**. It does not claim replayability against changing external model APIs.

---

## 🎯 Why This Artifact Matters

1. **Workshop-facing story**
   Prompt drift is not cosmetic. Small wording changes can flip evaluation conclusions under otherwise fixed conditions.

2. **Industry-facing traceability**
   The bundle is structured like an audit package: raw evidence, normalized records, authoritative tables, and release verification are all separated by contract.

3. **Operational lesson**
   A low score and an invalid evaluation are different events. This repository preserves both, instead of collapsing them into a single failure bucket.

4. **Release discipline**
   The shipped figure set under `final-version/figures/` is mirrored in `paper_anon_submission/figures/` and checked by an explicit verification command.

---

## 📋 Practical Recommendations

Based on this audit, we recommend:

| Recommendation | Action |
|----------------|--------|
| Prompt sensitivity check | Test with 2-3 semantically equivalent prompt phrasings |
| Invalid-rate reporting | Track exclusion causes separately from low scores |
| Artifact contracts | Make every reported number traceable to raw evidence |
| Release verification | Add a temp-directory verification command before publication |

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
