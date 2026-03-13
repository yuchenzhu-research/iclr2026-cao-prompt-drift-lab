#!/usr/bin/env python3

"""
One-command verification for the shipped reproducibility bundle.

What it checks:
- raw judge bundles can be rebuilt into processed records/tables in a temp output root
- structural audit passes on that rebuilt output
- all figure scripts execute successfully against the shipped tables
- shipped paper figures are byte-identical to final-version/figures

This command is designed to leave the git worktree untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List


EXPECTED_GENERATED_FIGURES = [
    "fig1_heatmap_v1.pdf",
    "fig2_heatmap_v0.pdf",
    "fig3_dimension_breakdown_chatgpt.pdf",
    "fig3_dimension_breakdown_claude.pdf",
    "fig3_dimension_breakdown_gemini.pdf",
    "fig4_dimension_failure_rate.pdf",
    "fig5_judge_comparison.pdf",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_cmd(cmd: List[str], cwd: Path, env: Dict[str, str]) -> None:
    result = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            f"{' '.join(cmd)}\n\n"
            f"stdout:\n{result.stdout}\n\n"
            f"stderr:\n{result.stderr}"
        )


def compare_release_figures(final_dir: Path, paper_dir: Path) -> List[Dict[str, str]]:
    rows = []
    names = sorted({path.name for path in final_dir.glob("*.pdf")} | {path.name for path in paper_dir.glob("*.pdf")})
    for name in names:
        final_path = final_dir / name
        paper_path = paper_dir / name
        if not final_path.exists() or not paper_path.exists():
            raise FileNotFoundError(f"Release figure missing: {name}")
        final_hash = sha256(final_path)
        paper_hash = sha256(paper_path)
        if final_hash != paper_hash:
            raise ValueError(
                f"Release figure hash mismatch for {name}: "
                f"final={final_hash} paper={paper_hash}"
            )
        rows.append({"name": name, "sha256": final_hash})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workdir",
        type=Path,
        help="optional temp workspace for verification artifacts",
    )
    parser.add_argument(
        "--keep",
        action="store_true",
        help="keep the verification workdir instead of deleting it on success",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    temp_root = args.workdir or Path(tempfile.mkdtemp(prefix="repro_bundle_verify_"))
    processed_root = temp_root / "processed_evaluations"
    generated_figures = temp_root / "generated_figures"
    cache_root = temp_root / "cache"
    cache_root.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env.setdefault("MPLCONFIGDIR", str(cache_root / "matplotlib"))
    env.setdefault("XDG_CACHE_HOME", str(cache_root / "xdg-cache"))
    env.setdefault("REPRO_FIG_CACHE_DIR", str(cache_root))

    run_cmd(
        [
            sys.executable,
            "reproducibility/tools/reproduce_valid_evaluations.py",
            "--from_raw",
            "--overwrite_records",
            "--output_root",
            str(processed_root),
        ],
        cwd=project_root,
        env=env,
    )
    run_cmd(
        [
            sys.executable,
            "reproducibility/tools/audit_reproducibility_bundle.py",
            "--strict",
            "--output_root",
            str(processed_root),
        ],
        cwd=project_root,
        env=env,
    )

    figure_scripts = sorted((project_root / "reproducibility" / "tools" / "figures").glob("make_fig*.py"))
    for script in figure_scripts:
        run_cmd([sys.executable, str(script), "--out_dir", str(generated_figures)], cwd=project_root, env=env)

    missing_generated = [name for name in EXPECTED_GENERATED_FIGURES if not (generated_figures / name).exists()]
    if missing_generated:
        raise FileNotFoundError(f"Generated figure(s) missing: {missing_generated}")

    release_rows = compare_release_figures(
        project_root / "final-version" / "figures",
        project_root / "paper_anon_submission" / "figures",
    )

    report = {
        "status": "ok",
        "verification_root": str(temp_root),
        "processed_output_root": str(processed_root),
        "generated_figure_root": str(generated_figures),
        "generated_figures": EXPECTED_GENERATED_FIGURES,
        "release_figures": release_rows,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not args.keep and args.workdir is None:
        shutil.rmtree(temp_root)


if __name__ == "__main__":
    main()
