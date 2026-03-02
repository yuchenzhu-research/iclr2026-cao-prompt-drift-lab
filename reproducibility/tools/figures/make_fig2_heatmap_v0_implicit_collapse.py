from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse


def _canon_series(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower()


# === configuration ===
# Find repo root by locating a directory containing `reproducibility/`
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
parser = argparse.ArgumentParser(description="Generate Fig2: v0 heatmap for implicit triggers")
parser.add_argument(
    "--out_dir",
    type=Path,
    default=reproducibility_dir / "tools" / "figures",
    help="Output directory for figures (default: reproducibility/tools/figures)"
)
args = parser.parse_args()

DATA_PATH = (
    reproducibility_dir
    / "04_results"
    / "03_processed_evaluations"
    / "v0_baseline_judge"
    / "summary_tables"
    / "scores_long.csv"
)

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Expected input file not found:\n{DATA_PATH}")

# === load data ===
df = pd.read_csv(DATA_PATH)

# --- required columns ---
required = ["trigger_type", "prompt_variant", "generator_model", "total"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"CSV missing required columns: {missing}\nColumns found: {list(df.columns)}")

# === canonicalize key fields (prevents ChatGPT being 'missed') ===
df = df.copy()
df["trigger_type"] = _canon_series(df["trigger_type"])
df["prompt_variant"] = _canon_series(df["prompt_variant"])
df["generator_model"] = _canon_series(df["generator_model"])

# Ensure total is numeric
df["total"] = pd.to_numeric(df["total"], errors="coerce")
if df["total"].isna().any():
    bad = df[df["total"].isna()].head(5)
    raise ValueError(
        "Found non-numeric total values after coercion. Sample bad rows:\n"
        f"{bad}"
    )

# === filter implicit only ===
imp = df[df["trigger_type"] == "implicit"].copy()
if imp.empty:
    raise ValueError(
        "After filtering trigger_type=='implicit', dataframe is empty.\n"
        "Check trigger_type values in CSV."
    )

# === forensics print (so you can verify ChatGPT is actually included) ===
print(f"[Fig2] INPUT CSV: {DATA_PATH}")
print("[Fig2] implicit mean(total) by generator_model:")
print(imp.groupby("generator_model")["total"].agg(["count", "mean", "min", "max"]).sort_index())

# === aggregate ===
heatmap_df = (
    imp.groupby(["prompt_variant", "generator_model"])
       .agg(total_mean=("total", "mean"))
       .reset_index()
       .pivot(index="prompt_variant", columns="generator_model", values="total_mean")
)

# Stable model order if present
preferred = [c for c in ["chatgpt", "gemini", "claude"] if c in heatmap_df.columns]
rest = [c for c in heatmap_df.columns if c not in preferred]
heatmap_df = heatmap_df[preferred + sorted(rest)]

# === plot ===
plt.figure(figsize=(6.2, 4.2))
sns.heatmap(
    heatmap_df,
    annot=True,
    fmt=".2f",
    cmap="Reds",
    cbar_kws={"label": "Mean Total Score (Implicit)"}
)

plt.title("Implicit Trigger: Mean Total by Prompt Variant × Generator (v0 baseline judge)")
plt.xlabel("Generator Model")
plt.ylabel("Prompt Variant")

out_dir = args.out_dir
out_dir.mkdir(parents=True, exist_ok=True)
out_path = out_dir / "fig2_heatmap_v0.pdf"

plt.tight_layout()
plt.savefig(out_path, bbox_inches="tight")
plt.show()
print(f"[Fig2] Saved: {out_path}")