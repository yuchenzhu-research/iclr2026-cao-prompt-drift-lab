"""
Figure 1: Schema Failure Cliff under Reduced Contract Salience

This script reproduces Figure 1 in the paper.

Purpose
-------
Visualize the schema hard-break rate (A_structure = 0) as the trigger
condition shifts from explicit to implicit, across generator models.
This figure is used to demonstrate an instrumentation-level failure
(cliff-like collapse) rather than gradual quality degradation.

Data source (derived artifact only)
-----------------------------------
supplement/04_results/03_processed_evaluations/
v0_baseline_judge/summary_tables/scores_long.csv

Notes
-----
- This script reads ONLY derived summary tables.
- No manual data editing or post-processing is performed.
- One execution produces exactly one paper figure.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # kept for consistency with other figure scripts

# === configuration ===
DATA_PATH = (
    "supplement/04_results/03_processed_evaluations/"
    "v0_baseline_judge/summary_tables/scores_long.csv"
)

# === load data ===
df = pd.read_csv(DATA_PATH)

# === compute schema hard-break indicator ===
# A_structure == 0 indicates a hard schema failure
df["A_hard_break"] = (df["A_structure"] == 0).astype(int)

# === aggregate by generator model and trigger type ===
grouped = (
    df.groupby(["generator_model", "trigger_type"])
      .agg(hard_break_rate=("A_hard_break", "mean"))
      .reset_index()
)

# enforce consistent trigger order for x-axis
trigger_order = ["explicit", "implicit"]

# === plot ===
plt.figure(figsize=(6, 4))

for model in grouped["generator_model"].unique():
    sub = grouped[grouped["generator_model"] == model]
    sub = sub.set_index("trigger_type").loc[trigger_order].reset_index()

    plt.plot(
        sub["trigger_type"],
        sub["hard_break_rate"],
        marker="o",
        linewidth=2,
        label=model
    )

plt.xlabel("Trigger Salience")
plt.ylabel("Schema Hard-Break Rate (A_structure = 0)")
plt.title("Schema Failure Cliff under Reduced Contract Salience")
plt.ylim(0, 1.05)
plt.legend(title="Generator Model")
plt.grid(True, linestyle="--", alpha=0.4)
OUT_DIR = "supplement/tools/figures"

plt.tight_layout()
plt.savefig(
    f"{OUT_DIR}/fig1_schema_failure_cliff.pdf",
    bbox_inches="tight"
)
plt.show()