"""
Figure 3: Judge Sensitivity under Identical Generator Outputs

This script reproduces Figure 3 in the paper.

Purpose
-------
Demonstrate that changing the judge prompt alone (instrumentation change),
while holding generator outputs fixed, can substantially alter reported
severity under implicit triggers. This motivates gated adaptation and
change control in CAO-style monitoring systems.

Data sources (derived artifacts only)
-------------------------------------
supplement/04_results/03_processed_evaluations/
- v0_baseline_judge/summary_tables/scores_long.csv
- v1_paraphrase_judge/summary_tables/scores_long.csv

Notes
-----
- Only overlapping slices are compared.
- No generator inference is re-run.
- Differences reflect judge behavior, not model capability.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === configuration ===
BASE_PATH = "supplement/04_results/03_processed_evaluations"

JUDGES = {
    "v0": "v0_baseline_judge",
    "v1": "v1_paraphrase_judge",
}

# === helper functions ===
def load_scores(judge_dir):
    return pd.read_csv(
        f"{BASE_PATH}/{judge_dir}/summary_tables/scores_long.csv"
    )

def summarize_implicit(df):
    """
    Aggregate mean total scores under implicit triggers,
    grouped by generator model.
    """
    return (
        df[df["trigger_type"] == "implicit"]
        .groupby("generator_model")
        .agg(total_mean=("total", "mean"))
        .reset_index()
    )

# === load data ===
df_v0 = load_scores(JUDGES["v0"])
df_v1 = load_scores(JUDGES["v1"])

# === summarize overlapping slice ===
s0 = summarize_implicit(df_v0).assign(judge="v0 (baseline)")
s1 = summarize_implicit(df_v1).assign(judge="v1 (paraphrased)")

cmp = pd.concat([s0, s1], ignore_index=True)

# === plot ===
plt.figure(figsize=(6, 4))

sns.barplot(
    data=cmp,
    x="generator_model",
    y="total_mean",
    hue="judge"
)

plt.xlabel("Generator Model")
plt.ylabel("Mean Total Score (Implicit)")
plt.title("Judge Sensitivity on Identical Outputs")
OUT_DIR = "supplement/tools/figures"

plt.tight_layout()
plt.savefig(
    f"{OUT_DIR}/fig3_judge_sensitivity.pdf",
    bbox_inches="tight"
)
plt.show()