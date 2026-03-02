# 🏛️ Prompt Drift Lab

<div align="center">

[![EN](https://img.shields.io/badge/English-blue?style=flat-square&logo=readme)](README.md)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-yellow?style=flat-square)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/Status-Audit-blue?style=flat-square)
![Paper](https://img.shields.io/badge/Paper-ICLR%202026%20Workshop-red?style=flat-square&logo=arXiv)

**Catch, Adapt, and Operate: Monitoring ML Models Under Drift Workshop**

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
| **测试任务** | 2 个结构化输出任务 (Q3、Q4) |
| **生成模型** | 3 个主流 LLM（ChatGPT、Claude、Gemini） |
| **提示词变体** | 4 种：baseline / weak / long / conflict |
| **指令明确性** | 2 种：explicit（直接说明格式）/ implicit（间接暗示） |
| **总测试量** | 每个模型 16 个输出（4 变体 × 2 明确性） |
| **裁判方式** | 交叉模型裁判（Model A 评价 Model B）+ 自评交叉验证 |

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
📂 prompt-drift-lab/
├── 📄 README.md                        # 英文说明
├── 📄 README_zh-CN.md                  # 中文说明（你正在看）
├── 📂 paper_anon_submission/           # 📝 论文 LaTeX 源码、图表
│   └── 📂 figures/                     # 论文插图
├── 📂 reproducibility/                 # 🔧 完整可复现的实验材料
│   ├── 📂 01_experiment_design/        # 🎯 实验设计：任务定义、输出结构、分割策略
│   ├── 📂 02_prompt_variants/          # 💬 提示词变体（中文） + 变体清单
│   ├── 📂 03_evaluation_rules/         # ⚖️ 评估协议、评分维度、失效分类法
│   │   ├── 📄 eval_protocol.md         # 核心协议（权威版本）
│   │   ├── 📄 judge_prompt.md          # 法官提示词模板
│   │   ├── 📄 compute_scores.py        # 评分计算脚本
│   │   ├── 📄 scoring_dimensions.md    # 评分维度说明
│   │   ├── 📄 failure_taxonomy.md      # 失效类型分类
│   │   └── 📂 schema/                  # JSON Schema 定义
│   └── 📂 04_results/                  # 📦 冻结的实验数据
│       ├── 📂 01_raw_model_outputs/    # 📄 模型原始输出（PDF）
│       ├── 📂 02_raw_judge_evaluations/# 📊 法官评分原始结果（JSON）
│       └── 📂 03_processed_evaluations/# 📈 处理后的评分数据（CSV）+ 失效分析
└── 📂 final-version/                   # 🎯 最终版论文 PDF + 补充材料
```

---

## ⚡ 快速上手：复现核心结果

### 环境准备

```bash
cd prompt-drift-lab
python -m pip install -r reproducibility/03_evaluation_rules/tools/requirements.txt
```

> 依赖：NumPy、Pandas、Matplotlib、Seaborn

### 步骤 1：生成权威评分表

```bash
python -u reproducibility/03_evaluation_rules/tools/materialize_records.py \
  --ack-legacy --overwrite \
  --runs v0_baseline_judge v1_paraphrase_judge v2_schema_strict_judge
```

**输出文件：**
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`
- `reproducibility/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`

### 步骤 2：重新绘制论文图表

```bash
python reproducibility/03_evaluation_rules/tools/figures/make_figure1_schema_failure_cliff.py
python reproducibility/03_evaluation_rules/tools/figures/make_figure6_judge_comparison.py
```

> 📁 图表输出到 `paper_anon_submission/figures/`

---

## 🔗 数据溯源：从数字到证据

每一个报告的数据点都可以追溯到原始工件：

**1. 从表格到原始记录**

1. 打开 `scores_long.csv`，选择任意一行
2. 记住 `record_id` 或文件名
3. 在 `.../valid_evaluations/` 找对应的 `record_*.json`

**2. 从记录到原始输出**

1. 从 JSON 中找到 `file` 字段
2. 在 `01_raw_model_outputs/` 找到同名 PDF
3. 对比 PDF 内容和评分是否一致

**3. 评估协议的权威版本**

> ⚠️ 以 `reproducibility/03_evaluation_rules/eval_protocol.md` 为准，这是唯一权威文档。

---

## ✅ 可复现性状态

| 能力 | 状态 | 说明 |
|------|------|------|
| 🔄 绑定论文图表 | ✅ 可复现 | 本地 CSV 即可生成 |
| 📊 生成汇总表格 | ✅ 可复现 | 从缓存法官 JSON 生成 |
| 🧮 评分逻辑验证 | ⚠️ 部分 | 脚本仅作存档参考 |
| 🚀 从零运行完整评估 | ❌ 不可复现 | 缺少 LLM API 调用代码 |

> **为什么没有 API 代码？**
>
> 为了避免密钥泄露和 API 版本变动带来的复现问题，我们选择**只开源冻结的结果**，而非可运行但可能过时的 API 代码。

---

## 🎯 主要贡献

1. **🔍 可审计的评估链条**
   > 从提示词 → 模型输出 → 法官评分 → 最终 CSV，每一步都可追溯验证

2. **❄️ 冻结的实验工件**
   > 所有结果预先生成并存储，不依赖任何 LLM API，确保 100% 确定可复现

3. **📋 失效分类法**
   > 将法官失效（格式错误、拒绝评分等）系统化分类，让"评不了"本身成为一种证据

4. **🛠️ 离线工具支持**
   > 无需 API，无外部依赖，直接在本地复现论文所有图表和分析

---

## 📋 研究启示：如何做更好的评估？

基于本审计工作，我们建议评估协议设计者：

| 建议 | 要做什么 |
|------|----------|
| 💡 提示词敏感度检查 | 用 2-3 个同类说法测试，不要只用一个提示词 |
| 📉 失效率报告 | 说明有多少比例的输出因格式/协议问题无法评估 |
| 🔗 工件映射 | 每个报告的数字都要能追溯到原始输出和法官记录 |

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
| 🛠️ 工具代码 (`reproducibility/03_evaluation_rules/tools/*`) | MIT License |
| 📦 数据工件 (`reproducibility/04_results/*`) | CC-BY 4.0 |

---

## 👤 作者

**朱宇晨** (Yuchen Zhu)

- 🏠 GitHub: [@yuchenzhu-research](https://github.com/yuchenzhu-research)
- 🌍 项目主页: [iclr2026-cao-prompt-drift-lab](https://github.com/yuchenzhu-research/iclr2026-cao-prompt-drift-lab)

有问题或建议，欢迎提 Issue！