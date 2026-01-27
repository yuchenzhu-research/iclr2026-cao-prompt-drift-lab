from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

DIMENSIONS = [
    "A_structure",
    "B_snapshot_constraint",
    "C_actionability",
    "D_completeness",
    "E_drift_failure",
]
TRIGGERS = ["explicit", "implicit"]


def nice_dim_label(d: str) -> str:
    if d == "E_drift_failure":
        return "E_drift\nfailure"
    return d.replace("_", "\n")


def main():
    # === fig5-style path resolution ===
    curr_dir = Path(__file__).resolve().parent          # .../supplement/tools/figures
    supplement_dir = curr_dir.parent.parent             # .../supplement

    # === authoritative v0 input (NO fixed) ===
    data_path = (
        supplement_dir
        / "04_results"
        / "03_processed_evaluations"
        / "v0_baseline_judge"
        / "summary_tables"
        / "scores_long.csv"
    )
    if not data_path.exists():
        raise FileNotFoundError(f"Expected input file not found:\n{data_path}")

    # === relative output dir (same as fig5) ===
    out_dir = supplement_dir / "tools" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)

    # Prefer generator_model directly (more robust than inferring from bundle_file)
    if "generator_model" not in df.columns:
        raise ValueError("CSV missing required column: generator_model")
    df["generator_model"] = df["generator_model"].astype(str).str.strip().str.lower()

    # Average dimension scores by generator + trigger
    grouped = (
        df.groupby(["generator_model", "trigger_type"])[DIMENSIONS]
        .mean()
        .reset_index()
    )

    bar_width = 0.38
    x = list(range(len(DIMENSIONS)))
    x_labels = [nice_dim_label(d) for d in DIMENSIONS]

    # Plot one figure per generator model (restricted to the three canonical names if present)
    gens = [g for g in ["chatgpt", "gemini", "claude"] if g in set(df["generator_model"].unique())]

    for gen in gens:
        sub = grouped[grouped["generator_model"] == gen].set_index("trigger_type")

        exp_vals = (
            sub.loc["explicit"][DIMENSIONS].values
            if "explicit" in sub.index else [float("nan")] * len(DIMENSIONS)
        )
        imp_vals = (
            sub.loc["implicit"][DIMENSIONS].values
            if "implicit" in sub.index else [float("nan")] * len(DIMENSIONS)
        )

        plt.figure(figsize=(7.0, 4.2))
        ax = plt.gca()

        ax.bar([p - bar_width / 2 for p in x], exp_vals, width=bar_width, label="Explicit")
        ax.bar([p + bar_width / 2 for p in x], imp_vals, width=bar_width, label="Implicit")

        ax.set_xticks(x)
        ax.set_xticklabels(x_labels)
        ax.set_ylabel("Mean Dimension Score")
        ax.set_ylim(0.0, 2.05)
        ax.set_title(f"Dimension Breakdown (Explicit vs Implicit) — {gen.capitalize()}")
        ax.legend()
        ax.grid(True, axis="y", linestyle="--", alpha=0.35)

        plt.tight_layout()
        out_path = out_dir / f"fig3_dimension_breakdown_{gen}.pdf"
        plt.savefig(out_path, bbox_inches="tight")
        plt.show()
        print(f"[Fig3 dimension breakdown] Saved: {out_path}")


if __name__ == "__main__":
    main()