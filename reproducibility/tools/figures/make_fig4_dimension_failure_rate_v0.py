import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

curr_dir = Path(__file__).resolve().parent
reproducibility_dir = curr_dir.parent.parent
project_dir = reproducibility_dir.parent

# === authoritative v0 input ===
data_path = (
    reproducibility_dir
    / "04_results"
    / "03_processed_evaluations"
    / "v0_baseline_judge"
    / "summary_tables"
    / "scores_long.csv"
)

if not data_path.exists():
    raise FileNotFoundError(f"Expected input file not found:\n{data_path}")

# output directory -> reproducibility/tools/figures
out_dir = reproducibility_dir / "tools" / "figures"
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

# === compute failure indicators ===
failure_records = []
for dim in DIMENSIONS:
    max_score = df[dim].max()
    df[f"{dim}_fail"] = df[dim] < max_score
    grouped = (
        df.groupby("trigger_type")[f"{dim}_fail"]
        .mean()
        .reset_index()
        .assign(dimension=dim)
        .rename(columns={f"{dim}_fail": "failure_rate"})
    )
    failure_records.append(grouped)

failure_df = pd.concat(failure_records, ignore_index=True)

# ensure consistent order of triggers and dimensions
failure_df["dimension"] = pd.Categorical(
    failure_df["dimension"], categories=DIMENSIONS, ordered=True
)
failure_df["trigger_type"] = pd.Categorical(
    failure_df["trigger_type"], categories=["explicit", "implicit"], ordered=True
)
failure_df = failure_df.sort_values(["dimension", "trigger_type"])

# pivot for plotting
pivot_df = failure_df.pivot(index="dimension", columns="trigger_type", values="failure_rate")

# === plot ===
x = range(len(DIMENSIONS))
bar_width = 0.35

plt.figure(figsize=(6, 4))
plt.bar(
    [p - bar_width / 2 for p in x],
    pivot_df["explicit"].values,
    width=bar_width,
    label="Explicit"
)
plt.bar(
    [p + bar_width / 2 for p in x],
    pivot_df["implicit"].values,
    width=bar_width,
    label="Implicit"
)

plt.xticks(
    x,
    [d.replace("_", "\n").replace("E_drift_failure", "E_drift\nfailure") for d in DIMENSIONS]
)
plt.ylim(0, 1.0)
plt.ylabel("Failure Rate (score < max)")
plt.title("Dimension Failure Rate by Trigger Type")
plt.legend()
plt.grid(True, axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

# write to reproducibility/tools/figures directory
fig_path = out_dir / "fig4_dimension_failure_rate.pdf"
plt.savefig(fig_path, bbox_inches="tight")
plt.show()

print(f"[Fig4 dimension failure rate] Saved: {fig_path}")