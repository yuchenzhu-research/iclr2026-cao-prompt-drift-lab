from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import argparse

curr_dir = Path(__file__).resolve().parent          # .../figures
reproducibility_dir = curr_dir.parent.parent             # .../reproducibility
project_dir = reproducibility_dir.parent                 # .../prompt-drift-lab

BASE_PATH = reproducibility_dir / "04_results" / "03_processed_evaluations"
JUDGES = {
    "v0_baseline_judge": "v0 (baseline)",
    "v1_paraphrase_judge": "v1 (paraphrased)",
    "v2_schema_strict_judge": "v2 (schema-strict)",
}

# --------------------------------------------------
# Arguments
# --------------------------------------------------
parser = argparse.ArgumentParser(description="Generate Fig5: judge version comparison (v0/v1/v2)")
parser.add_argument(
    "--out_dir",
    type=Path,
    default=reproducibility_dir / "tools" / "figures",
    help="Output directory for figures (default: reproducibility/tools/figures)"
)
parser.add_argument(
    "--show",
    action="store_true",
    help="display the figure window after saving",
)
args = parser.parse_args()

# output directory
out_dir = args.out_dir
out_dir.mkdir(parents=True, exist_ok=True)

# === helper functions ===
def load_scores(judge_dir: str) -> pd.DataFrame:
    """
    IMPORTANT: Always read scores_long.csv (authoritative).
    """
    summary_dir = BASE_PATH / judge_dir / "summary_tables"
    path = summary_dir / "scores_long.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing expected CSV: {path}")
    return pd.read_csv(path)

def summarize_implicit(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate mean total scores under implicit triggers,
    grouped by generator model (after canonicalization).
    """
    df = df.copy()

    # Canonicalize to prevent ChatGPT being missed (e.g., "ChatGPT", " chatgpt ", etc.)
    df["generator_model"] = df["generator_model"].astype(str).str.strip().str.lower()
    df["trigger_type"] = df["trigger_type"].astype(str).str.strip().str.lower()

    # Ensure total is numeric
    df["total"] = pd.to_numeric(df["total"], errors="coerce")

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

# Keep ONLY ChatGPT and Gemini (remove Claude entirely)
expected_generators = ["chatgpt", "gemini"]
judge_labels = list(JUDGES.values())

# Pivot to wide format for plotting: rows = generator models, cols = judges
wide = all_summary.pivot(index="generator_model", columns="judge", values="mean_total")
wide = wide.reindex(index=expected_generators, columns=judge_labels)

# === plot ===
plt.figure(figsize=(7, 4))
ax = plt.gca()

x = range(len(expected_generators))
width = 0.25

for i, judge in enumerate(judge_labels):
    vals = wide[judge].values
    ax.bar([p + i * width for p in x], vals, width=width, label=judge)

ax.set_xticks([p + width for p in x])
ax.set_xticklabels(expected_generators, rotation=25, ha="right")
ax.set_ylabel("Mean Total Score (Implicit)  ↑ higher is better")
ax.set_title("Judge Comparison (ChatGPT + Gemini only)")
ax.legend(title="Judge Version")
ax.grid(True, axis="y", linestyle="--", alpha=0.35)

plt.tight_layout()
fig_path = out_dir / "fig5_judge_comparison.pdf"
plt.savefig(fig_path, bbox_inches="tight")
if args.show:
    plt.show()
plt.close()

print(f"[Fig5 judge comparison] Saved: {fig_path}")
print("[Sanity] Mean totals (implicit):")
print(wide)
