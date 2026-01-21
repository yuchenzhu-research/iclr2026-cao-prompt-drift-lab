"""
Figure 2: Implicit Trigger Score Collapse Heatmap

This script reproduces Figure 2 in the paper.
It visualizes mean total scores under implicit triggers,
sliced by prompt_variant × generator_model.

Data source:
supplement/04_results/03_processed_evaluations/
v0_baseline_judge/summary_tables/scores_long.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === configuration ===
DATA_PATH = (
    "supplement/04_results/03_processed_evaluations/"
    "v0_baseline_judge/summary_tables/scores_long.csv"
)

# === load data (THIS WAS MISSING) ===
df = pd.read_csv(DATA_PATH)

# === filter implicit only ===
imp = df[df["trigger_type"] == "implicit"]

# === aggregate ===
heatmap_df = (
    imp.groupby(["prompt_variant", "generator_model"])
       .agg(total_mean=("total", "mean"))
       .reset_index()
       .pivot(
           index="prompt_variant",
           columns="generator_model",
           values="total_mean"
       )
)

# === plot ===
plt.figure(figsize=(6, 4))
sns.heatmap(
    heatmap_df,
    annot=True,
    fmt=".2f",
    cmap="Reds",
    cbar_kws={"label": "Mean Total Score"}
)

plt.title("Implicit Trigger: Score Collapse by Prompt Variant and Model")
plt.xlabel("Generator Model")
plt.ylabel("Prompt Variant")
OUT_DIR = "paper/figures"

plt.tight_layout()
plt.savefig(
    f"{OUT_DIR}/fig2_implicit_heatmap.pdf",
    bbox_inches="tight"
)
plt.show()