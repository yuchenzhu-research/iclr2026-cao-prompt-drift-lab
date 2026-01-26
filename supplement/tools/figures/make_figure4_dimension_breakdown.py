import re
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


def repo_root_from_here() -> Path:
    """
    Find repo root by walking up until we see 'supplement' directory.
    Assumption: this script lives under <repo>/supplement/tools/.
    """
    curr = Path(__file__).resolve()
    for p in [curr.parent] + list(curr.parents):
        if (p / "supplement").is_dir():
            return p
    # Fallback: two levels up (should still work if layout is unchanged)
    return curr.parent.parent


def main():
    repo_root = repo_root_from_here()
    supplement_dir = repo_root / "supplement"

    data_path = (
        supplement_dir
        / "04_results"
        / "03_processed_evaluations"
        / "v0_baseline_judge"
        / "summary_tables"
        / "scores_long.csv"
    )

    # === relative output dir for reviewers ===
    out_dir = supplement_dir / "tools" / "figures"
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)

    # Infer generator family from bundle_file suffix, e.g. *_bundle_claude.json
    def infer_gen(bundle_file: str) -> str:
        m = re.search(r"_bundle_(chatgpt|claude|gemini)\.json$", str(bundle_file))
        return m.group(1) if m else "unknown"

    df["generator_family"] = df["bundle_file"].map(infer_gen)

    # Average dimension scores by generator + trigger
    grouped = (
        df.groupby(["generator_family", "trigger_type"])[DIMENSIONS]
        .mean()
        .reset_index()
    )

    bar_width = 0.38
    x = list(range(len(DIMENSIONS)))
    x_labels = [nice_dim_label(d) for d in DIMENSIONS]

    # Plot one figure per generator family
    for gen in ["chatgpt", "claude", "gemini"]:
        sub = grouped[grouped["generator_family"] == gen].set_index("trigger_type")

        # Ensure both triggers exist; if not, fill with NaNs (still reproducible)
        exp_vals = sub.loc["explicit"][DIMENSIONS].values if "explicit" in sub.index else [float("nan")] * len(DIMENSIONS)
        imp_vals = sub.loc["implicit"][DIMENSIONS].values if "implicit" in sub.index else [float("nan")] * len(DIMENSIONS)

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
        plt.savefig(out_dir / f"fig4_dimension_breakdown_{gen}.pdf", bbox_inches="tight")
        plt.close()


if __name__ == "__main__":
    main()