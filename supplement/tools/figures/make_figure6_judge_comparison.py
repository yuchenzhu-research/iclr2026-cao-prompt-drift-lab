"""
Figure 6: Comparison of Judge Versions on Identical Generator Outputs

This script reproduces an extended version of FigureÂ 3 in the CAO
submission, comparing all available judge versions under implicit
triggers.

Purpose
-------
Demonstrate how the choice of judge (i.e., the prompting of the
evaluation model) can alter reported severity even when generator
outputs are fixed.  This figure includes all three judges packaged
in the artifact (baseline, paraphrased, and schema-strict) and
aggregates mean total scores under implicit trigger conditions by
generator model.

Data sources (derived artifacts only)
-------------------------------------
supplement/04_results/03_processed_evaluations/
- v0_baseline_judge/summary_tables/scores_long.csv
- v1_paraphrase_judge/summary_tables/scores_long.csv
- v2_schema_strict_judge/summary_tables/scores_long.csv

Notes
-----
- Only overlapping slices are compared.
- No generator inference is re-run.
- Differences reflect judge behavior, not model capability.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

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

out_dir = project_dir / "paper" / "figures"
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
    return (
        df[df["trigger_type"] == "implicit"]
        .groupby("generator_model")
        .agg(total_mean=("total", "mean"))
        .reset_index()
    )

# === load and summarize data ===
summary_frames = []
for judge_dir, label in JUDGES.items():
    df_judge = load_scores(judge_dir)
    summary = summarize_implicit(df_judge)
    summary["judge"] = label
    summary_frames.append(summary)

cmp = pd.concat(summary_frames, ignore_index=True)

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
plt.title("Judge Comparison on Identical Outputs (Implicit)")
plt.legend(title="Judge Version")
plt.tight_layout()

# Save the figure into the projectâ€‘level paper/figures directory
fig_path = out_dir / "fig6_judge_comparison.pdf"
plt.savefig(fig_path, bbox_inches="tight")
plt.show()