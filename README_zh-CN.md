# Prompt Drift Lab

[![en](https://img.shields.io/badge/Language-English-blue.svg)](README.md)

本项目包含了 **Prompt Drift Lab** (提示词漂移实验室) 的冻结评估工件与工具。这套方法论用于研究微小、看似无害的提示词扰动如何导致大语言模型 (LLM) 在遵循指令、格式合规性和语义对齐方面发生灾难性故障。本代码库作为一个可审计的数据库，包含了提示词、生成器原始输出 (PDF)、LLM 裁判输出包 (JSON) 以及处理过的评分表 (CSV)，这为配套论文的核心结论提供了支撑。我们提供了用于确定性审计、数据记录生成以及基于已有数据直接生成图表的离线代码工具。

**作者**: Yuchen Zhu

### 核心贡献
- **可审计的评估链条**：建立了一个从提示词变体到生成器原始输出、裁判包，再到最终 CSV 表格的严格单向可验证流水线。
- **冻结数据工件**：所有模型响应和裁判判断均预先计算并保存，确保在不依赖存在随机性的 LLM API 调用的情况下实现确定性复现。
- **失效分类法**：格式化的 schema 用于追踪模型故障的特定性质（例如：语义失败与格式失败）。
- **离线工具支持**：提供离线代码脚本，支持准确还原论文图表并进行中间层 JSON 文件的聚合。

---

## 目录

1. [可复现状态](#可复现状态)
2. [快速开始 (Minimal Runnable Path)](#快速开始-minimal-runnable-path)
3. [完整复现流水线](#完整复现流水线)
4. [代码库结构图](#代码库结构图)
5. [数据工件与审计追踪](#数据工件与审计追踪)
6. [已知问题与路线图](#已知问题与路线图)
7. [引用](#引用)
8. [开源协议](#开源协议)

---

## 可复现状态

✅ **可复现 (已验证)**
- 基于已处理的 CSV 自动重新绘制论文最终 PDF 图表 (`supplement/tools/figures/*.py`)。
- 从缓存的原始裁判 JSON 数据包重新生成处理后的 JSON 记录并重新计算提取 CSV 总结数据表。
- 安装本地 Python 依赖 `supplement/tools/requirements.txt`。

⚠️ **部分可复现**
- Schema 验证与评分维度逻辑。`compute_scores.py` 作为一个存档工具存在，用于说明评分规则如何映射到 JSON 数据上，但如果要从零开始进行全新的全面评估，你需要自己编写调用任意 LLM provider 接口的代码。

❌ **不可复现 (在设计上缺失)**
- **生成模型推理**：调用 Anthropic, OpenAI 或 Google API 服务并结合 `02_prompt_variants` 来生成原始 PDF 结果的代码脚本和密钥未包含在内。
- **裁判模型执行**：针对原始 PDF 运行评估协议 (`judge_prompt.md`) 进而产生 `02_raw_judge_evaluations` 的 API 代码未包含在内。

---

## 快速开始 (Minimal Runnable Path)

本项目提供了离线代码用于完全确定性地重新生成研究数据表和图表。请在代码库根目录运行以下命令。相关依赖很少 (NumPy, Pandas, Matplotlib, Seaborn)。

**1. 安装依赖:**
```bash
python -m pip install -r supplement/tools/requirements.txt
```

**2. 审计并重新生成记录与表格:**
此步骤从原始 JSON 裁判包数据重新生成权威的 CSV 数据。
```bash
python -u supplement/tools/ingest/materialize_records.py \
  --ack-legacy --overwrite \
  --runs v0_baseline_judge v1_paraphrase_judge v2_schema_strict_judge
```
*预期输出:*
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_long.csv`
- `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/scores_grouped.csv`

**3. 重新生成图表:**
此步骤采用上述的 `scores_long.csv` 重新生成 PDF 格式论文图。
```bash
python supplement/tools/figures/make_figure1_schema_failure_cliff.py
python supplement/tools/figures/make_figure6_judge_comparison.py
```
*预期输出:*
图表将被生成保存在 `paper_anon_submission/figures/` 文件夹下。

---

## 完整复现流水线

本基准实验强制实施严密的单向数据流动隔离。虽然调用生成器与裁判模型 API 执行步骤的代码在此处缺失 (Broken Link)，但完整的端到端概念化数据流水线如下：

1. **提示词生成:** `02_prompt_variants/` (变体和 manifests 定义)
2. **模型推理 [BROKEN LINK ❌]:** 调用 LLM 生成器产生标准格式回答。
3. **生成器原始输出存储:** `04_results/01_raw_model_outputs/` (冻结的 `.pdf` 文件)
4. **裁判执行 [BROKEN LINK ❌]:** 应用 `03_evaluation_rules/judge_prompt.md` 执行 LLM 裁判。
5. **原始裁判结果:** `04_results/02_raw_judge_evaluations/` (依照 `judge_bundle.schema.json` 存储的 JSON 包)
6. **处理与总结:** `tools/ingest/` 将裁判包验证并转化为标准的 JSON 记录，最终摊平为 `04_results/03_processed_evaluations/.../scores_long.csv`。
7. **图表绘制:** `tools/figures/` 直接读取 `scores_long.csv` 绘制可视化 PDF。

---

## 代码库结构图

```text
prompt-drift-lab/
├── README_FOR_REVIEWERS.md          # 内部元数据文档，说明复现限制
├── README.md                        # 英文版 README
├── README_zh-CN.md                  # 中文版 README
├── paper_anon_submission/           # 论文 LaTeX 源码
│   └── figures/                     # 编译后用于论文 PDF 的图表
└── supplement/                      # 包含所有实验设计、数据与工具
    ├── 01_experiment_design/        # 测试问题、工作流详情、数据集划分标准
    ├── 02_prompt_variants/          # 提示词变体及具体测试扰动
    ├── 03_evaluation_rules/         # 评估协议、schemas 与评分标准
    ├── 04_results/                  # 冻结数据工件目录 (权威数据映射)
    │   ├── 01_raw_model_outputs/    # 模型生成的原始 PDF 文件
    │   ├── 02_raw_judge_evaluations/# LLM 裁判输出的 JSON 数据块
    │   └── 03_processed_evaluations/# 经过评估验证的记录 JSON 及最终 CSV
    └── tools/                       # 工具集
        ├── ingest/                  # JSON 到 CSV 转换工具 (materialize_records.py)
        ├── figures/                 # 绘制数据图表的脚本
        └── requirements.txt         # 核心依赖追踪
```
*(注：项目中间分支中可能会出现重复的 `final-version` / `reproducibility` 文件夹。离线组件的逻辑权威根目录准确映射为上述的 `supplement/` 与 `paper_anon_submission/` 命名空间。)*

---

## 数据工件与审计追踪

为了保证每一个数据点的可验证溯源，我们在此提供直接映射指南。

- **协议与规则:** 请仅参考 `supplement/03_evaluation_rules/eval_protocol.md`。此处的规则优先于所有其他元数据。
- **论文数据 (评分):** 严格来源于 `supplement/04_results/03_processed_evaluations/<judge_version>/summary_tables/`。请查找 `scores_long.csv` 或 `scores_grouped.csv`。**切勿合并**不同裁判版本 (如 `v0_baseline`, `v1_paraphrase`) 的记录。
- **审计流程 (行 -> 证据):**
  1. 从 `scores_long.csv` 中选取任意一行数据。
  2. 使用行标识符 (`file`, `generator_model` 等) 在 `.../valid_evaluations/**/record_*.json` 映射到处理过的 JSON。
  3. 从 `supplement/04_results/01_raw_model_outputs/` 中加载相应的原始生成 PDF 文件。
- **图表:** 
  - *Figure 1 (Failure Cliff):* 由 `supplement/tools/figures/make_figure1_schema_failure_cliff.py` 生成
  - *Figure 6 (Judge Comparison):* 由 `supplement/tools/figures/make_figure6_judge_comparison.py` 生成
  - *(其他图表)* → *待办: 待剩余画图脚本合并后更新人工精确追踪映射。*

---

## 已知问题与路线图

**已知问题:**
- **工具链执行未补全:** `tools/aggregate/` 脚本已被标记为弃用，如果不进行自定义修改，则无法直接从原始记录重新构建 CSV。
- **运行代码骨架缺失:** 目前必须由社区手动实现用于调用生成器和进行评估的 API 绑定。我们仅提供提示词和最终运行结果工件。

**路线图:**
- [ ] 提供一个 shim 层骨架代码，让用户能够完全通过本地 API 或标准 provider 无缝重放任意新模型。
- [ ] 纳入针对评分维度阈值的综合测试和单元断言。
- [ ] 自动生成 `CITATION.cff` 集成。
- [ ] 合并 `final-version` 与 `reproducibility` 别名文件夹，以严格反映顶层的 `supplement` 路径结构。

---

## 引用

如果您在研究中使用了本项目，请引用：
*(待办: 替换为实际的论文引用/arXiv 链接。考虑在根目录下提供 `CITATION.cff`)。*
```bibtex
@misc{prompt-drift-lab-2026,
  author = {Yuchen Zhu},
  title = {Prompt Drift Lab: Frozen Artifact for Auditable Prompt-Drift Evaluation},
  year = {2026},
  howpublished = {\url{https://github.com/prompt-drift-lab/prompt-drift-lab}}
}
```

---

## 开源协议

**待办**: 代码库根目录下目前还没有显式声明全局 LICENSE 文件（常用选择：针对代码工具使用 MIT 或 Apache 2.0，针对数据工件使用 CC-BY 4.0）。（注意：`supplement/tools/LICENSE` 已存在，如果使用离线工具代码请直接查阅）。
