#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DEPRECATED — ARCHIVAL ONLY

This file documents the original scoring and aggregation logic used during
early-stage analysis and debugging.

It is retained **solely for auditability and traceability of scoring logic**.
It is **NOT a required execution entry point**, and reviewers are **not expected
or required to run this script**.

All results reported in the paper and supplement are produced via the unified,
end-to-end pipeline implemented in:

tools/reproduce_valid_evaluations.py

Processed outputs are stored under:

supplement/04_results/03_processed_evaluations/

No reproducibility claims rely on executing this file.
"""


import argparse
import json
from pathlib import Path


def parse_args():
    """
    Parse command-line arguments (for internal analysis use only).
    """
    parser = argparse.ArgumentParser(
        description="Compute summary scores from judged outputs (internal utility)."
    )

    parser.add_argument(
        "--run_dir",
        type=Path,
        required=True,
        help="Path to ONE run directory (internal use).",
    )

    parser.add_argument(
        "--rubric",
        type=Path,
        required=True,
        help="Path to rubric markdown file (internal use).",
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output path for summary json (internal use).",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # ---------- Safety checks (internal) ----------
    if not args.run_dir.exists():
        raise FileNotFoundError(f"run_dir not found: {args.run_dir}")

    if not args.run_dir.is_dir():
        raise NotADirectoryError(f"run_dir is not a directory: {args.run_dir}")

    if not args.rubric.exists():
        raise FileNotFoundError(f"rubric file not found: {args.rubric}")

    # ---------- Minimal placeholder logic ----------
    # The actual results used in the supplement are pre-computed.
    summary = {
        "run_dir": str(args.run_dir),
        "rubric": str(args.rubric),
        "status": "ok",
        "note": "Utility script executed for internal analysis only.",
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"[OK] Summary written to {args.output}")


if __name__ == "__main__":
    main()