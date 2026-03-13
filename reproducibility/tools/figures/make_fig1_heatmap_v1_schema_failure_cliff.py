from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse

# --------------------------------------------------
# Resolve paths relative to this script (reviewer-safe)
# --------------------------------------------------
curr_path = Path(__file__).resolve()
repo_root = None
for p in [curr_path.parent] + list(curr_path.parents):
    if (p / "reproducibility").is_dir():
        repo_root = p
        break
if repo_root is None:
    repo_root = curr_path.parent.parent.parent
reproducibility_dir = repo_root / "reproducibility"

# --------------------------------------------------
# Arguments
# --------------------------------------------------
parser = argparse.ArgumentParser(description="Generate Fig1: v1 heatmap for implicit triggers")
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

# --------------------------------------------------
# Input data (v1 only)
#   NOTE: if you want scores_long.csv, change the filename below.
# --------------------------------------------------
DATA_PATH = (
    reproducibility_dir
    / "04_results"
    / "03_processed_evaluations"
    / "v1_paraphrase_judge"
    / "summary_tables"
    / "scores_long.csv"
)

# --------------------------------------------------
# Output figures
# --------------------------------------------------
out_dir = args.out_dir
out_dir.mkdir(parents=True, exist_ok=True)
OUT_FIG = out_dir / "fig1_heatmap_v1.pdf"

# --------------------------------------------------
# Load data
# --------------------------------------------------
if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Expected input file not found:\n{DATA_PATH}\n"
        "Please ensure the v1 scores_long.csv exists before generating figures."
    )
df = pd.read_csv(DATA_PATH)

# --------------------------------------------------
# Canonicalize generator model into 3 families (ChatGPT/Gemini/Claude)
# --------------------------------------------------
def canon_family(x: str) -> str:
    s = str(x).strip().lower()
    # ChatGPT / OpenAI variants
    if "chatgpt" in s or s.startswith("openai") or "gpt-" in s or "gpt " in s:
        return "ChatGPT"
    # Gemini variants
    if "gemini" in s or "google" in s:
        return "Gemini"
    # If anything unexpected appears, keep it (but you can also raise)
    return s

# normalize keys
df = df.copy()
df["trigger_type"] = df["trigger_type"].astype(str).str.strip().str.lower()
df["prompt_variant"] = df["prompt_variant"].astype(str).str.strip()
df["generator_family"] = df["generator_model"].map(canon_family)

# Keep only the 2 families you care about (drop noise)
df = df[df["generator_family"].isin(["ChatGPT", "Gemini"])]

# Filter implicit only
df = df[df["trigger_type"] == "implicit"].copy()

# --------------------------------------------------
# Aggregate
# --------------------------------------------------
heatmap_df = (
    df.groupby(["prompt_variant", "generator_family"])
      .agg(total_mean=("total", "mean"))
      .reset_index()
      .pivot(index="prompt_variant", columns="generator_family", values="total_mean")
)

# Force column order and ensure all 2 exist (missing stays NaN, NOT 0)
for col in ["ChatGPT", "Gemini"]:
    if col not in heatmap_df.columns:
        heatmap_df[col] = np.nan

heatmap_df = heatmap_df[["ChatGPT", "Gemini"]].astype(float)

# --------------------------------------------------
# Plot
# --------------------------------------------------
plt.figure(figsize=(6, 4))
sns.heatmap(
    heatmap_df,
    annot=True,
    fmt=".2f",
    cmap="Reds",
    cbar_kws={"label": "Mean Total Score"}
)
plt.title("heatmap_v1")
plt.tight_layout()

# --------------------------------------------------
# Save
# --------------------------------------------------
plt.savefig(OUT_FIG, bbox_inches="tight")
if args.show:
    plt.show()
plt.close()

print(f"[Fig1] INPUT: {DATA_PATH}")
print(f"[Fig1] generator_family counts:\n{df['generator_family'].value_counts()}")
print(f"[Fig1] Saved: {OUT_FIG}")
