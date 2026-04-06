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
    <a href="README.md">English</a> |
    简体中文
  </strong>
</p>

> **"用同一个提示词评估模型真的可靠吗？"**
>
> 我们的审计研究发现：微小的提示词改动就能让模型评分出现“过山车”级别的波动——从 9.31 暴跌到 0.50。

</div>

---

> 💡 本项目是 ICLR 2026 论文的官方实现：
> **Prompt-Level Drift as an Operational Monitoring Problem: Schema Failure Cliffs and Judge-Version Risk in Artifact-Grounded Evaluation**。

我们在本项目中提出了通过**审计式监测**来解决 LLM 评估稳定性的问题。无论你是**学术界研究员**（探索模型能力边界与评估方法论）还是**工业界专家**（构建生产级 LLM 应用、监控线上 Prompt 漂移），本项目都为你提供了极具参考价值的数据工件和一站式审计工具。

## 🌟 核心价值与亮点

### 1. 破除“单提示词评估”的迷信
当前的评估常常依赖单一提示词（Prompt）跑分，这忽视了**提示词本身就是评估协议的一部分**。在保证任务要求和解码参数不变的前提下，仅仅改变提示词的措辞、甚至只是调弱约束的语气，结论就可能完全翻转。

### 2. 工业界视角：生产环境的监控排雷
- **“隐式合规”十分脆弱**：实验表明，Google Gemini 3 Pro 在提示词要求不明确（Implicit）时，平均分会从 9.31 悬崖式掉落至 0.50。听懂“弦外之音”是大模型在工程落地时最大的不确定性。
- **第一性原理看“失效案例”**：把输出格式错误、结构混乱、强行说教（评估污染）等情况作为监控领域的一等公民，而不是作为脏数据随意丢弃——失效恰恰是协议脆弱性的最直接证据。

### 3. 学术界视角：Artifact 级精准复现
- 构建了多组极具区分度的数据协议（Baseline, Weak, Long, Conflict）。
- 每一个对外报告的结论与数字，均支持从最终的 CSV 报表一路向下**回溯到原始的模型评审输出及 PDF 文档**，实现了极其严苛的工件级可追溯性。

---

## 🔬 实验打法与震撼发现

**实验版图：**
- **多模型碰撞**：OpenAI GPT-5.2 (Extended), Google Gemini 3 Pro, Anthropic Claude Sonnet 4.5
- **精细化控制变量**：4种变体 × 2种清晰度（Explicit 直接点明 vs Implicit 间接表述）。
- **裁判机制**：多维交叉评判（模型A评模型B）与自举验证。

### 📉 发现一：换一种说法，烂模型也能霸榜
仅看 Q3 任务的平均分波动（模型与任务均不变）：

| 模型 | Baseline → Conflict | 波动与变化 |
|------|---------------------|------------|
| ChatGPT | 7.50 → 9.75 | 🚀 **+3.25** |
| Claude | 4.25 → 4.50 | 📈 +0.25 |
| Gemini | 4.00 → 4.75 | 📈 +0.75 |

结论：单一视角下的跑分榜单（Leaderboard）经常掩盖了 Prompt 风格给评分带来的剧烈噪音。

### 📉 发现二：明确指引是模型落地的生命线
在 Explicit 和 Implicit 条件下跑分差异极大：

| 模型 | Explicit (明确告知格式) | Implicit (暗示格式) |
|------|-----------------------|-------------------|
| Gemini | **9.31** | **0.50** |
| Claude | 4.38 | **0.00** |
| ChatGPT| 9.38 | 7.75 |

结论：如果你在工业级部署时不直接提供结构约束（Structure Signaling），绝大多数模型的表现将直接崩溃。

---

## 🚀 审计与复现 Quickstart

环境依赖准备完毕后，通过本项目的 `tools` 套件，可一键复现论文全流程：

```bash
# 1. 准备依赖
python -m pip install -r reproducibility/tools/requirements.txt

# 2. 一键工件审计（校验结构、契约和数据不变量）
python reproducibility/tools/audit_reproducibility_bundle.py --strict

# 3. 离线全量重建（从 judge bundles 一路算出规范化结果与表格）
python reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records

# 4. 论文图表重绘（支持输出到任何目录）
OUT_DIR=/tmp/prompt_drift_figures
mkdir -p "$OUT_DIR"
for f in reproducibility/tools/figures/make_fig*.py; do
  python "$f" --out_dir "$OUT_DIR"
done
```

> **📌 代码库快速指南**：
> - 想要 review 代码与策略？详见 `README_FOR_REVIEWERS.md`。
> - 想要探索原始生成数据？进入 `reproducibility/04_results/`。
> - 想要查看权威协议定义？浏览 `reproducibility/03_evaluation_rules/eval_protocol.md`。

---

## 📌 总结与应用启示

通过这个项目，我们能够明确地告诉社区：
1. **上线前必测鲁棒性**：跑评测前，用 2-3 个语义等价的不同 Prompt 试试水深。
2. **正确记录“系统报错”**：在评估时，将 `invalid evaluation`（格式不对等情况）单独追踪统计，而不是一股脑归入低分。
3. **数据资产的极致溯源链**：交付或发布前引入严格的 Structural Audit 流程，确保数据说服力。

无论你是在卷下一个顶会，还是在优化公司业务大模型的 Prompt 工程，这个研究都是极佳的“避坑指南”。

---

## 📖 学术引用

如果这篇探索为您带来了灵感或帮助到了您的工程实践，请以如下规范引用：

```bibtex
@misc{promptdriftlab2026,
  author       = {Yuchen Zhu},
  title        = {{PROMPT-LEVEL DRIFT AS AN OPERATIONAL MONITORING PROBLEM: SCHEMA FAILURE CLIFFS AND JUDGE-VERSION RISK IN ARTIFACT-GROUNDED EVALUATION}},
  year         = {2026},
  howpublished = {\url{https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab}},
}
```

#### 📄 开源许可证
- 🛠️ 工具代码架构：MIT License
- 📦 数据工件集合：CC-BY 4.0

**Yuchen Zhu (朱宇晨)**
- 🏠 GitHub: [@yuchenzhu-research](https://github.com/yuchenzhu-research)
- 💼 有工业落地探讨或是学术 Ideas 碰撞？欢迎点击 **[提个 Issue](https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab/issues)** 交流探讨！
