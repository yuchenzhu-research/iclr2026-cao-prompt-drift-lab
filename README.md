<div align="center">

# Prompt Drift Lab
**Catch, Adapt, and Operate: Monitoring ML Models Under Drift (ICLR 2026 Workshop)**

<p align="center">
  <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY%204.0-yellow?style=flat-square" alt="License: CC BY 4.0" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License: MIT" /></a>
  <img src="https://img.shields.io/badge/Status-Artifact%20Bundle-blue?style=flat-square" alt="Status: Artifact Bundle" />
  <a href="https://openreview.net/forum?id=PGoKUAy8XW#discussion"><img src="https://img.shields.io/badge/Paper-OpenReview-red?style=flat-square&logo=arXiv" alt="Paper" /></a>
</p>

<p align="center">
  <strong>
    English |
    <a href="README_zh-CN.md">简体中文</a>
  </strong>
</p>

> **"Is single-prompt evaluation really reliable?"**
>
> Our systematic audit reveals that harmless prompt variations can swing model scores dramatically—acting like a rollercoaster from 9.31 down to 0.50.

</div>

---

> 💡 This is the official repository for the ICLR 2026 paper:
> **Prompt-Level Drift as an Operational Monitoring Problem: Schema Failure Cliffs and Judge-Version Risk in Artifact-Grounded Evaluation** ([OpenReview](https://openreview.net/forum?id=PGoKUAy8XW#discussion)).

We approach LLM evaluation stability through **audit-driven operational monitoring**. Whether you're an **Academic Researcher** (probing foundation model boundaries) or an **Industry Practitioner** (building robust pipelines and monitoring prompt drift in production), this artifact bundle serves as both a methodological benchmark and a practical engineering toolkit.

## 🌟 Why This Matters: Bridges between Academia & Industry

### 1. Breaking the "Single-Prompt" Illusion
In standard LLM evaluations, we rely on one prompt, run the model, and declare a winner. However, **the prompt is an inherent part of the evaluation protocol**. The same task, rephrased, can yield totally inverted conclusions. We don't propose "magic" prompt hacks; instead, we **audit** this exact evaluation brittleness.

### 2. The Production Nightmare: "Implicit Compliance" is Fragile
- **The Schema Failure Cliff**: We found that top models like Gemini drop from an excellent `9.31` average to `0.50` when the prompt stops explicitly spelling out structural constraints. Models' abilities to read "between the lines" remain highly unreliable for enterprise deployments.
- **Failures are First-Class Citizens**: Traditional pipelines silently drop invalid outputs (bad JSON, missed steps). We categorize them (e.g., schema breaking, instruction drift) because these failures are **hard evidence of protocol brittleness**.

### 3. Artifact-Scope Reproducibility
- Every reported metric, graph, and table is traceable directly back to the raw generated logs (`.json` and `.pdf`). This repository enforces strict transparency via artifact bundle audits.

---

## 🔬 Experimental Setup & Shocking Discoveries

| Setup Dimension | Configuration |
|-----------------|---------------|
| **Generators** | OpenAI GPT-5.2 (Extended), Google Gemini 3 Pro, Anthropic Claude Sonnet 4.5 |
| **Prompt Variants** | 4 types: `Baseline` / `Weak` / `Long` / `Conflict` |
| **Instruction Style**| `Explicit` (structural contract strictly defined) vs `Implicit` (soft constraints) |

### 🚨 Finding F1: Rephrasing completely flips the leaderboard
Looking at Q3 mean scores (task held strictly constant!):

| LLM Model | Baseline → Conflict | Shift |
|-----------|---------------------|-------|
| ChatGPT | 7.50 → 9.75 | 🚀 **+3.25** |
| Claude  | 4.25 → 4.50 | 📈 +0.25 |
| Gemini  | 4.00 → 4.75 | 📈 +0.75 |

> **Takeaway:** Merely changing the prompt style can turn a mediocre evaluation into a state-of-the-art result. A single screenshot snapshot is heavily misleading. 

### 🚨 Finding F2: Models collapse without explicit architecture
Comparing the `Explicit` vs `Implicit` condition logic across exactly the same task goals:

| LLM Model | Explicit Avg | Implicit Avg |
|-----------|--------------|--------------|
| Gemini | **9.31** | **0.50** |
| Claude | 4.38 | **0.00** |
| ChatGPT| 9.38 | 7.75 |

> **Takeaway:** Explicit constraints dominate stability. We shouldn't trust ML pipelines that bank heavily on "implicit" instruction following.

---

## 🚀 Quickstart: Rebuilding & Auditing

With standard Python installed, our `tools/` suite covers the end-to-end trace context:

```bash
# 1. Install dependencies
python -m pip install -r reproducibility/tools/requirements.txt

# 2. Strict Artifact Audit
# Checks counts, contracts, and canonical judge-version invariants
python reproducibility/tools/audit_reproducibility_bundle.py --strict

# 3. Offline Data Rebuild
# Re-compiles valid canonical records from the raw judge bundles
python reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records

# 4. Generate Paper Figures
# Generates all plot artifacts securely to a target output path
OUT_DIR=/tmp/prompt_drift_figures
mkdir -p "$OUT_DIR"
for f in reproducibility/tools/figures/make_fig*.py; do
  python "$f" --out_dir "$OUT_DIR"
done
```

> **📚 Where to explore next?**
> - For a review walkthrough: `README_FOR_REVIEWERS.md`
> - To check experimental setup: `reproducibility/01_experiment_design/`
> - To view the valid interpretation rules: `reproducibility/03_evaluation_rules/eval_protocol.md`

---

## 📌 Operational Takeaways

1. **Always Check Prompt Sensitivity**: Try 2-3 semantically identical variations before setting your benchmark protocol.
2. **Track the Exclusivity Rate**: Keep a dedicated log for `invaild_evaluation` cases alongside the raw score stats. 
3. **Audit Your Artifacts**: Adopt a strict structural script test locally before handing over ML datasets or running analysis.

This work serves as an essential "landmine map" regardless if you are aiming for high-impact AI research submissions or engineering large-language architectures inside a startup.

---

## 📖 Citation

If this insight or infrastructure helped you, please use the citation below:

```bibtex
@misc{promptdriftlab2026,
  author       = {Yuchen Zhu},
  title        = {{PROMPT-LEVEL DRIFT AS AN OPERATIONAL MONITORING PROBLEM: SCHEMA FAILURE CLIFFS AND JUDGE-VERSION RISK IN ARTIFACT-GROUNDED EVALUATION}},
  year         = {2026},
  howpublished = {\url{https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab}},
}
```

#### 📄 License
- 🛠️ Engine & Tools (`reproducibility/tools/*`): MIT License
- 📦 Data & Responses (`reproducibility/04_results/*`): CC-BY 4.0

**Yuchen Zhu**
- 🏠 GitHub: [@yuchenzhu-research](https://github.com/yuchenzhu-research)
- 💼 Let me know your thoughts or feedback! [Feel free to drop an Issue](https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab/issues).
