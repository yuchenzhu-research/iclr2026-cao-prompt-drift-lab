"""
Figure 6: Comparison of Judge Versions on Identical Generator Outputs

This script reproduces an extended version of FigureÂ 3 in the CAO
submission, comparing all available judge versions under implicit
triggers.

Purpose
-------
Demonstrate how the choice of judge (i.e., the prompting of the
evaluation model) can alter reported severity even when generator
outputs are fixed.  This figure includes all available judge versions,
aggregates mean total scores under implicit triggers, and visualizes
differences via a grouped bar chart.

Inputs
------
- Processed score tables for each judge version:
  supplement/04_results/03_processed_evaluations/<judge>/summary_tables/scores_long.csv

Outputs
-------
- Figure saved to the project-level figures directory:
  paper/figures/fig6_judge_comparison.pdf

Usage
-----
python supplement/tools/figures/make_figure6_judge_comparison.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# === resolve data and output locations ===
# Determine the absolute base path for the processed results and the
# projectâ€‘level figures directory.  This allows the script to be
# executed from within the `supplement/tools/figures` directory
# without assuming a particular working directory.

curr_dir = Path(__file__).resolve().parent          # .../figures
supplement_dir = curr_dir.parent.parent             # .../supplement
project_dir = supplement_dir.parent                 # .../prompt-drift-lab

BASE_PATH = supplement_dir / "04_results" / "03_processed_evaluations"
JUDGES = {
    "v0_baseline_judge": "v0 (baseline)",
    "v1_paraphrase_judge": "v1 (paraphrased)",
    "v2_schema_strict_judge": "v2 (schema-strict)",
}

# ONLY CHANGE: output directory -> supplement/tools/figures (repo-relative)
out_dir = supplement_dir / "tools" / "figures"
out_dir.mkdir(parents=True, exist_ok=True)

# === helper functions ===
def load_scores(judge_dir: str) -> pd.DataFrame:
    """
    Load the long-form scores CSV for a given judge.
    """
    path = (
        BASE_PATH
        / judge_dir
        / "summary_tables"
        / "scores_long.csv"
    )
    return pd.read_csv(path)

def summarize_implicit(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate mean total scores under implicit triggers,
    grouped by generator model.
    """
    imp = df[df["trigger_type"] == "implicit"]
    summary = (
        imp.groupby("generator_model")["total"]
           .mean()
           .reset_index()
           .rename(columns={"total": "mean_total"})
    )
    return summary

# === load and aggregate ===
summaries = []
for judge_dir, judge_label in JUDGES.items():
    scores = load_scores(judge_dir)
    summary = summarize_implicit(scores)
    summary["judge"] = judge_label
    summaries.append(summary)

all_summary = pd.concat(summaries, ignore_index=True)

# Ensure consistent ordering of generator models across judges
gen_models = sorted(all_summary["generator_model"].unique())
judge_labels = list(JUDGES.values())

# Pivot to wide format for plotting: rows = generator models, cols = judges
wide = all_summary.pivot(index="generator_model", columns="judge", values="mean_total")
wide = wide.reindex(index=gen_models, columns=judge_labels)

# === plot ===
plt.figure(figsize=(7, 4))
ax = plt.gca()

x = range(len(gen_models))
width = 0.25

for i, judge in enumerate(judge_labels):
    vals = wide[judge].values
    ax.bar([p + i * width for p in x], vals, width=width, label=judge)

ax.set_xticks([p + width for p in x])
ax.set_xticklabels(gen_models, rotation=25, ha="right")
ax.set_ylabel("Mean Total Score (Implicit)")
ax.set_title("Judge Comparison on Identical Generator Outputs")
ax.legend(title="Judge Version")
ax.grid(True, axis="y", linestyle="--", alpha=0.35)

plt.tight_layout()

fig_path = out_dir / "fig6_judge_comparison.pdf"
plt.savefig(fig_path, bbox_inches="tight")
plt.show()