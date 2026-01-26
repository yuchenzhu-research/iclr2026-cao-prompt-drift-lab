import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DIMENSIONS = [
    "A_structure",
    "B_snapshot_constraint",
    "C_actionability",
    "D_completeness",
    "E_drift_failure",
]
TRIGGERS = ["explicit", "implicit"]

def nice_dim_label(d: str) -> str:
    return d.replace("_", "\n").replace("E_drift_failure", "E_drift\nfailure")

def main():
    curr_dir = Path(__file__).resolve().parent
    supplement_dir = curr_dir.parent.parent
    project_dir = supplement_dir.parent

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

    df = pd.read_csv(data_path)

    def infer_gen(bundle_file: str) -> str:
        m = re.search(r"_bundle_(chatgpt|claude|gemini)\.json$", str(bundle_file))
        return m.group(1) if m else "unknown"

    df["generator_family"] = df["bundle_file"].map(infer_gen)

    grouped = (
        df.groupby(["generator_family", "trigger_type"])[DIMENSIONS]
        .mean()
        .reset_index()
    )

    y_min, y_max = 0.0, 2.05
    bar_width = 0.35
    x = list(range(len(DIMENSIONS)))

    for gen in ["chatgpt", "claude", "gemini"]:
        sub = grouped[grouped["generator_family"] == gen].set_index("trigger_type")
        sub = sub.loc[TRIGGERS].reset_index()

        exp_vals = sub[sub["trigger_type"] == "explicit"][DIMENSIONS].values[0]
        imp_vals = sub[sub["trigger_type"] == "implicit"][DIMENSIONS].values[0]

        fig = plt.figure(figsize=(6, 4))
        ax = plt.gca()

        ax.bar([p - bar_width / 2 for p in x], exp_vals, width=bar_width, label="Explicit")
        ax.bar([p + bar_width / 2 for p in x], imp_vals, width=bar_width, label="Implicit")

        ax.set_xticks(x)
        ax.set_xticklabels([nice_dim_label(d) for d in DIMENSIONS])
        ax.set_ylim(y_min, y_max)
        ax.set_ylabel("Mean Dimension Score")
        ax.set_title(f"Dimension Breakdown ({gen})")
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)
        ax.legend(loc="upper right")

        fig.subplots_adjust(left=0.12, right=0.98, bottom=0.25, top=0.88)

        out_path = out_dir / f"fig4_dimension_breakdown_{gen}.pdf"
        fig.savefig(out_path)
        plt.close(fig)

if __name__ == "__main__":
    main()