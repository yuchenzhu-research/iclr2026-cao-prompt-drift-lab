<div align="center">

# Prompt Drift Lab

**Catch, Adapt, and Operate: Monitoring ML Models Under Drift Workshop**

<p align="center">
  <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY%204.0-yellow?style=flat-square" alt="License: CC BY 4.0" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License: MIT" /></a>
  <img src="https://img.shields.io/badge/Release-Verified-blue?style=flat-square" alt="Release: Verified" />
  <img src="https://img.shields.io/badge/Paper-ICLR%202026%20Workshop-red?style=flat-square&logo=arXiv" alt="Paper" />
</p>

<p align="center">
  <strong>
    <a href="README.md">English</a> |
    简体中文
  </strong>
</p>

</div>

> **"用同一个提示词评估模型真的可靠吗？"**
>
> 本项目通过系统的审计式评估发现：微小的提示词改动就能让模型评分"过山车"——从 9.31 暴跌到 0.50。

---

## 🧭 项目要解决什么问题？

### 现实困境

在 LLM 评估中，我们经常这样做：

1. 选定一个提示词
2. 让模型跑一遍
3. 根据结果宣称"模型 A 更好"或"模型 B 通过了测试"

但问题在于：**提示词本身就是评估协议的一部分**。同一个任务，换个说法问，模型的回答可能天差地别。

### 我们的立场

我们不打算提出新的提示技巧，而是直接问：

> **如果任务和解码参数都不变，提示词的微小变化（改改措辞、加点约束、换种说法）会不会直接推翻评估结论？**

这就是 **Prompt Drift Lab** 在做的事情——对评估稳定性进行**审计**。

---

## 🔬 实验设计和核心发现

### 1. 实验怎么设计的？

| 维度 | 设置 |
|------|------|
| **问题划分** | 总共 4 个固定问题：Q1-Q2 只用于提示词迭代与 sanity check，Q3-Q4 才是正式保留的评测集 |
| **报告任务** | 2 个结构化输出任务 (Q3、Q4) |
| **生成模型** | OpenAI GPT-5.2 with extended thinking、Google Gemini 3 Pro、Anthropic Claude Sonnet 4.5 with extended thinking |
| **提示词变体** | 4 种：baseline / weak / long / conflict |
| **指令明确性** | 2 种：explicit（直接点明三段结构和顺序）/ implicit（用更间接、更弱的约束来传达结构要求） |
| **总测试量** | 每个模型 16 个输出（4 变体 × 2 明确性） |
| **裁判方式** | 交叉模型裁判（Model A 评价 Model B）+ 自评交叉验证 |

这里的 question ID 来自 [`reproducibility/01_experiment_design/eval_questions_ZH.jsonl`](/Users/yuchenzhu/Desktop/github/ICLR2026/reproducibility/01_experiment_design/eval_questions_ZH.jsonl) 和 [`reproducibility/01_experiment_design/eval_questions_EN.jsonl`](/Users/yuchenzhu/Desktop/github/ICLR2026/reproducibility/01_experiment_design/eval_questions_EN.jsonl)。其中中文文件是权威语义定义，英文文件是给 reviewer 阅读的参考翻译。`Q1-Q2` 只用于前期调 prompt 和执行层面的 sanity check，仓库里所有正式报告的数字都只来自保留评测集 `Q3-Q4`。

仓库里保留的原始生成输出目录分别是 [`openai_gpt-5.2_extended-thinking`](/Users/yuchenzhu/Desktop/github/ICLR2026/reproducibility/04_results/01_raw_model_outputs/openai_gpt-5.2_extended-thinking)、[`google_gemini-3-pro`](/Users/yuchenzhu/Desktop/github/ICLR2026/reproducibility/04_results/01_raw_model_outputs/google_gemini-3-pro)、[`anthropic_claude-sonnet-4.5_extended-thinking`](/Users/yuchenzhu/Desktop/github/ICLR2026/reproducibility/04_results/01_raw_model_outputs/anthropic_claude-sonnet-4.5_extended-thinking)。最初的 `v0_baseline_judge` 包含这三个生成模型；后续的 `v1_paraphrase_judge` 和 `v2_schema_strict_judge` 则是有意只保留 GPT-5.2 和 Gemini 3 Pro，因为 Claude 在 `v0` 这类任务上的表现明显偏弱，在 canonical table 里有 `24/32` 条是零分，所以后续对比不再继续纳入它。

在这个仓库里，`explicit` 不是模型参数，而是提示词层面的“结构信号是否直接写明”：`explicit` 会直接指定必须输出的三段结构及其顺序；`implicit` 则保持同样的任务目标，但用更间接、更弱的措辞去传达这个结构要求。这个区分来自 [`reproducibility/02_prompt_variants/`](/Users/yuchenzhu/Desktop/github/ICLR2026/reproducibility/02_prompt_variants) 的 prompt 设计，并在 raw / processed artifacts 里统一记录为 `trigger_type`。

### 2. 核心发现

#### 关键发现 F1：指令明确性是决定性因素

同一模型，在 explicit 和 implicit 条件下的表现差异巨大：

| 模型 | Explicit 平均 | Implicit 平均 |
|------|---------------|---------------|
| Gemini | **9.31** | **0.50** |
| Claude | 4.38 | **0.00** |
| ChatGPT | 9.38 | 7.75 |

> Gemini 换个说法问，平均分直接从 9.31 掉到 0.50——几乎等于没及格。

这说明**"隐式合规"是一个独立且脆弱的能力**。模型能听懂弦外之音这件事，并没有我们想象的那么可靠。

#### 关键发现 F2：换个说法，结论大变

只看 Q3 的平均分变化（保持任务不变）：

| 模型 | Baseline → Conflict | 变化幅度 |
|------|---------------------|----------|
| ChatGPT | 7.50 → 9.75 | **+3.25** |
| Claude | 4.25 → 4.50 | +0.25 |
| Gemini | 4.00 → 4.75 | +0.75 |

同一个模型，仅仅换个提示词风格，结论就可能从"这模型表现一般"变成"这模型很强"。

#### 关键发现 F3：单提示词评估具有误导性

单一提示词的评估结果，可能恰好选中了一个对某模型"友好"或"不友好"的说法，进而高估（低估）模型的真实可靠性。

这是审计的核心价值：**让这些结论翻转变得可追溯、可审计，而不是事后诸葛亮式的叙事。**

### 3. 为什么关注"失效"案例？

传统评估会这样做：低分记录下来，然后默默扔掉不合理的、格式错的、法官拒绝评分的案例。

我们的做法不同：我们**把失效视为一等公民**。

**常见失效类型：**

| 类型 | 描述 |
|------|------|
| 📦 Schema/格式破坏 | JSON 少了字段、多了层级 |
| 🚪 指令漂移 | 直接忽略格式要求 |
| 💬 评估污染 | 法官开始讨论评分标准而不是给出评分 |
| 📉 鲁棒性失效 | 同一模型自评和互评结果差距过大 |

失效不是"噪声"，而是**协议本身脆弱性的证据**。

---

## 📁 代码库结构

```
prompt-drift-lab/
├── ANONYMIZATION_CHECKLIST.md          # 匿名化与发布检查清单
├── README.md
├── README_zh-CN.md
├── README_FOR_REVIEWERS.md
├── paper_anon_submission/              # 匿名投稿包与冻结图表
├── final-version/                      # 定稿论文包与发布版图表
└── reproducibility/
    ├── 01_experiment_design/           # 任务设计、协议 YAML、schema 与设计笔记
    ├── 02_prompt_variants/             # baseline / weak / long / conflict 提示词
    ├── 03_evaluation_rules/            # 权威协议与有效性规则
    ├── 04_results/                     # 原始证据与规范化结果
    ├── 05_methodological_addenda_and_controls/  # 方法补充说明与控制项
    ├── TECHNICAL_MAP.md                # 面向工程审计的结构地图
    └── tools/                          # 离线重建、审计、作图脚本
```

说明：

- `reproducibility/04_results/03_processed_evaluations/` 是论文和图表使用的规范化结果主层。
- `reproducibility/04_results/03_processed_evaluations_rebuilt/` 是本地重建输出目录，不作为主 artifact 结构的一部分。
- `.DS_Store`、`__pycache__/` 这类缓存文件不属于 artifact，应忽略。

推荐入口：

- `README_FOR_REVIEWERS.md`：review 流程
- `reproducibility/TECHNICAL_MAP.md`：pipeline、数量、契约
- `reproducibility/01_experiment_design/`：任务设计与实验设置
- `reproducibility/02_prompt_variants/`：实际测试的提示词变体
- `reproducibility/03_evaluation_rules/eval_protocol.md`：唯一权威协议
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/`：论文可引用数字

---

## ⚡ 快速上手：验证与重建

### 环境准备

```bash
cd prompt-drift-lab
python -m pip install -r reproducibility/tools/requirements.txt
```

标准 Python 依赖：NumPy、Pandas、Matplotlib、Seaborn。

### 一键做发布验收

```bash
python reproducibility/tools/verify_release_bundle.py
```

这个命令会：

- 在临时目录里重建 processed artifacts
- 跑结构审计
- smoke test 全部 figure 脚本
- 校验 `paper_anon_submission/figures/` 与 `final-version/figures/` 字节一致

### 从保留的 judge bundles 离线重建

```bash
python reproducibility/tools/reproduce_valid_evaluations.py --from_raw --overwrite_records
```

输出：

- `valid_evaluations/main_method_cross_model/record_*.json`
- `scores_long.csv`
- `scores_grouped.csv`
- `run_meta.json`

### 重新生成图表

```bash
for f in reproducibility/tools/figures/make_fig*.py; do
  python "$f" --out_dir paper_anon_submission/figures
done
```

---

## 🔗 数据溯源：从数字到证据

每一个报告值都能沿着固定链路回溯：

```text
scores_grouped.csv
→ scores_long.csv
→ valid_evaluations/main_method_cross_model/record_*.json
→ 01_raw_model_outputs/*.pdf
```

解释规则以这三条为准：

- 协议与有效性标准：`reproducibility/03_evaluation_rules/eval_protocol.md`
- 数值权威层：`reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/`
- 不同 judge version（`v0`、`v1`、`v2`）之间不能混合汇总

---

## ✅ 发布状态

| 能力 | 状态 | 说明 |
|------|------|------|
| 发布验收 | ✅ 已验证 | `verify_release_bundle.py` 会临时重建并检查发布图哈希 |
| 离线 artifact 重建 | ✅ 已验证 | preserved judge bundles → canonical records → summary tables |
| 图表重生成 | ✅ 已验证 | `scores_long.csv` → PDF 图表 |
| 在线 API 重放 | 设计上不包含 | 仓库不提供供应商 API key 或在线 judge 脚本 |

这个仓库支持的是 **artifact-scope reproducibility**，不是针对持续变化的外部模型 API 做逐次重放。

---

## 🎯 这个工件为什么重要

1. **对 workshop 叙事有价值**
   Prompt drift 不是修辞细节，小改措辞就可能直接翻转评估结论。

2. **对工业界有审计价值**
   这个包按审计交付思路拆层：原始证据、规范化记录、权威表格、发布验收各自有清晰边界。

3. **对运营监控有方法价值**
   低分和 invalid evaluation 不是一回事。本仓库把两者拆开保存，而不是混成一个失败桶。

4. **对发布流程有工程价值**
   `final-version/figures/` 是发布图集，`paper_anon_submission/figures/` 是镜像副本，并有单独校验命令。

---

## 📋 研究启示：如何把评估做得更稳

基于本审计工作，我们建议评估协议设计者：

| 建议 | 要做什么 |
|------|----------|
| 提示词敏感度检查 | 用 2-3 个语义等价说法测试，不要只押一个 prompt |
| 失效率报告 | 把 exclusion cause 和低分结果分开报告 |
| 工件契约 | 每个报告数字都必须可回溯到原始证据 |
| 发布验收 | 在发布前加入 temp-directory verification 命令 |

---

## 📖 引用

如果本工作对你的研究有帮助，请引用：

```bibtex
@misc{promptdriftlab2026,
  author       = {Yuchen Zhu},
  title        = {Prompt Drift Lab: Auditing Structured Compliance under Benign Prompt Drift},
  year         = {2026},
  howpublished = {\url{https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab}},
}
```

---

## 📄 协议

| 内容 | 协议 |
|------|------|
| 🛠️ 工具代码 (`reproducibility/tools/*`) | MIT License |
| 📦 数据工件 (`reproducibility/04_results/*`) | CC-BY 4.0 |

---

## 👤 作者

**朱宇晨**

- 🏠 GitHub: [@yuchenzhu-research](https://github.com/yuchenzhu-research)
- 🌍 项目主页: [iclr2026-cao-prompt-drift-lab](https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab)

有问题或建议，欢迎提 Issue！
