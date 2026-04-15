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

> 💡 This is the official artifact repository for the ICLR 2026 paper:
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
| **Question Split** | `Q1-Q2`: development-only slices for prompt/judge iteration and sanity checks; `Q3-Q4`: held-out evaluation slices used for all reported analyses |
| **Generators** | OpenAI GPT-5.2 Thinking (Extended), Google Gemini 3 Pro, Anthropic Claude Sonnet 4.5 (extended thinking) |
| **Prompt Variants** | 4 types: `Baseline` / `Weak` / `Long` / `Conflict` |
| **Instruction Style**| `Explicit` (structural contract strictly defined) vs `Implicit` (soft constraints) |

> **Boundary note:** `Q1-Q2` are not part of the scored benchmark. They were used only during development to iterate prompts/judge setup and are excluded from all quantitative summaries, tables, and figures.

### Evaluation Questions

The fixed output contract requires exactly three top-level sections, in order: `fact snapshot`, `ChatGPT web search instructions`, and `Gemini deep research instructions`.

All experimental execution was conducted on the original Chinese questions. The English text below is a semantic translation provided for readability only.

| ID | Role | Question |
|----|------|----------|
| `Q1` | Development only | What has the weather been like in Shanghai over the past three days? |
| `Q2` | Development only | When doing street photography on a rainy day, how is ISO typically set? |
| `Q3` | Held-out evaluation | I tried many times to make the model follow a required output format, but it kept failing and became very frustrating. Why does this happen? |
| `Q4` | Held-out evaluation | Some people claim that as long as a prompt is sufficiently long, the model will always follow instructions. What is your view? |

Authoritative source: `reproducibility/01_experiment_design/eval_questions_ZH.jsonl`

### Design Intuition Behind the Question Set

- `Q1` was selected as a direct everyday factual query that strongly tempts the model to answer immediately, instead of switching into the required prompt-generator protocol.
- `Q2` served as a relatively cleaner control-style question during development: it is concrete, bounded, and easier to compress into a short factual snapshot plus two downstream research prompts.
- `Q3` was intentionally affect-laden and meta-evaluative. It tends to trigger diagnosis, reassurance, unsolicited advice, or full direct answering, all of which compete with the required three-section structure.
- `Q4` probes a different but related failure mode: opinionated argumentation about prompting. In the frozen `Q3-Q4` evaluation slices, `Q4` was not easier than `Q3`; it also remained highly failure-prone under weak / implicit structural signaling.
- The public artifact preserves only `Q3-Q4` evaluation outputs. The discussion of `Q1-Q2` here records the development-stage design rationale rather than a scored empirical claim.

### 🚨 Finding F1: Rephrasing completely flips the leaderboard
Looking at Q3 mean scores (task held strictly constant!):

| LLM Model | Baseline → Conflict | Shift |
|-----------|---------------------|-------|
| ChatGPT | 7.50 → 9.75 | 🚀 **+3.25** |
| Claude  | 4.25 → 4.50 | 📈 +0.25 |
| Gemini  | 4.00 → 4.75 | 📈 +0.75 |

> **Takeaway:** Merely changing the prompt style can turn a mediocre evaluation into a state-of-the-art result. A single snapshot can be deeply misleading.

### 🚨 Finding F2: Models collapse without explicit structural guidance
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
python3 -m pip install -r reproducibility/tools/requirements.txt

# 2. Strict Artifact Audit
# Checks counts, contracts, and canonical judge-version invariants
python3 reproducibility/tools/audit_reproducibility_bundle.py --strict

# 3. Optional Offline Data Rebuild
# Re-compiles canonical records/tables from preserved raw judge bundles
# Warning: this rewrites tracked JSON/CSV artifacts under reproducibility/04_results/03_processed_evaluations/
python3 reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records

# 4. Generate Paper Figures
# Generates all plot artifacts securely to a target output path
OUT_DIR=/tmp/prompt_drift_figures
mkdir -p "$OUT_DIR"
for f in reproducibility/tools/figures/make_fig*.py; do
  python3 "$f" --out_dir "$OUT_DIR"
done
```

> **📚 Where to explore next?**
> - For a review walkthrough: `README_FOR_REVIEWERS.md`
> - To check experimental setup: `reproducibility/01_experiment_design/`
> - To view the valid interpretation rules: `reproducibility/03_evaluation_rules/eval_protocol.md`

---

## 📌 Operational Takeaways

1. **Always Check Prompt Sensitivity**: Try 2-3 semantically identical variations before setting your benchmark protocol.
2. **Track Invalid Evaluations Separately**: Keep `invalid evaluations` and exclusions separate from valid low-score cases; `total = 0` can still be a valid judged outcome.
3. **Audit Your Artifacts**: Adopt a strict structural script test locally before handing over ML datasets or running analysis.

This work serves as an essential "landmine map" whether you are aiming for a high-impact AI research submission or engineering a production LLM workflow inside a startup.

---

## 📖 Citation

If this insight or infrastructure helped you, please use the citation below:

```bibtex
@misc{promptdriftlab2026,
  author       = {Yuchen Zhu},
  title        = {{PROMPT-LEVEL DRIFT AS AN OPERATIONAL MONITORING PROBLEM: SCHEMA FAILURE CLIFFS AND JUDGE-VERSION RISK IN ARTIFACT-GROUNDED EVALUATION}},
  year         = {2026},
  howpublished = {\url{https://openreview.net/forum?id=PGoKUAy8XW}},
}
```

#### 📄 License
- 🛠️ Engine & Tools (`reproducibility/tools/*`): MIT License
- 📦 Data & Responses (`reproducibility/04_results/*`): CC-BY 4.0

**Yuchen Zhu**
- 🏠 GitHub: [@yuchenzhu-research](https://github.com/yuchenzhu-research)
- 💼 Let me know your thoughts or feedback! [Feel free to drop an Issue](https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab/issues).
