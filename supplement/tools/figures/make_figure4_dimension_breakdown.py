"""
Figure 4: Dimension Score Breakdown by Trigger Type

This script generates FigureÂ 4 in the CAO workshop submission.

Purpose
-------
Summarise the mean values of each rubric dimension
(A_structure, B_snapshot_constraint, C_actionability,
D_completeness and E_drift_failure) under explicit and implicit
trigger conditions for each generator model.  The resulting bar
charts reveal which aspects of compliance degrade most when
contract salience is reduced.

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
from pathlib import Path

# === resolve data and output locations ===
# This script is designed to be executed from within the
# `supplement/tools/figures` directory.  The raw data lives in
# `supplement/04_results/03_processed_evaluations/v0_baseline_judge/summary_tables/`,
# and the resulting figure should be written to the projectâ€‘level
# `paper/figures` folder.  To make the script robust to the working
# directory, we derive absolute paths from the location of this file.

curr_dir = Path(__file__).resolve().parent          # .../figures
supplement_dir = curr_dir.parent.parent             # .../supplement
project_dir = supplement_dir.parent                 # .../prompt-drift-lab

data_path = (
    supplement_dir
    / "04_results"
    / "03_processed_evaluations"
    / "v0_baseline_judge"
    / "summary_tables"
    / "scores_long.csv"
)

out_dir = project_dir / "paper" / "figures"
out_dir.mkdir(parents=True, exist_ok=True)

# === load data ===
df = pd.read_csv(data_path)

# === define dimensions ===
DIMENSIONS = [
    "A_structure",
    "B_snapshot_constraint",
    "C_actionability",
    "D_completeness",
    "E_drift_failure",
]

# === aggregate mean scores by generator and trigger ===
grouped = (
    df.groupby(["generator_model", "trigger_type"])[DIMENSIONS]
    .mean()
    .reset_index()
)

# preserve consistent ordering
models = sorted(grouped["generator_model"].unique())
triggers = ["explicit", "implicit"]

# === plot ===
num_models = len(models)
fig, axes = plt.subplots(1, num_models, figsize=(5 * num_models, 4), sharey=True)

if num_models == 1:
    axes = [axes]  # ensure iterable

bar_width = 0.35

for idx, model in enumerate(models):
    ax = axes[idx]
    sub = grouped[grouped["generator_model"] == model]

    # ensure triggers order
    sub = sub.set_index("trigger_type").loc[triggers].reset_index()

    x = range(len(DIMENSIONS))
    # explicit values
    exp_vals = sub[sub["trigger_type"] == "explicit"][DIMENSIONS].values[0]
    imp_vals = sub[sub["trigger_type"] == "implicit"][DIMENSIONS].values[0]

    ax.bar(
        [p - bar_width / 2 for p in x],
        exp_vals,
        width=bar_width,
        label="Explicit",
    )
    ax.bar(
        [p + bar_width / 2 for p in x],
        imp_vals,
        width=bar_width,
        label="Implicit",
    )

    ax.set_xticks(x)
    ax.set_xticklabels([d.replace("_", "\n").replace("E_drift_failure", "E_drift\nfailure") for d in DIMENSIONS])
    ax.set_ylim(0, max(2, max(exp_vals.max(), imp_vals.max())) + 0.1)
    ax.set_ylabel("Mean Dimension Score")
    ax.set_title(f"{model}")
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    if idx == 0:
        ax.legend()

fig.suptitle("Dimension Score Breakdown by Trigger Type")
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Write to the projectâ€‘level paper/figures directory
fig_path = out_dir / "fig4_dimension_breakdown.pdf"
plt.savefig(fig_path, bbox_inches="tight")
plt.show()