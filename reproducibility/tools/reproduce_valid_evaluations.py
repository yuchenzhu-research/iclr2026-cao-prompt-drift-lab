#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reproduce valid evaluation summary tables from processed record JSONs.

Behavior:
- If --judge_version is provided:
    process only that version.
- If not provided:
    automatically process all judge_version directories under
    supplement/04_results/03_processed_evaluations/

Guarantees:
- Raw judge bundles are NOT modified.
- Per-dimension scores are NOT modified.
- `total` is treated as a derived field and deterministically backfilled.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


# -------------------------
# IO helpers
# -------------------------

def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    import csv
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# -------------------------
# Aggregation
# -------------------------

def aggregate(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []

    for r in records:
        scores = r.get("scores", {})

        # derived total (safe & deterministic)
        total = r.get("total")
        if total is None and isinstance(scores, dict):
            total = sum(int(v) for v in scores.values() if v is not None)

        rows.append({
            "judge_version": r.get("judge_version"),
            "source_bundle": r.get("source_bundle"),
            "judge_model": r.get("judge_model"),
            "generator_model": r.get("generator_model"),
            "file": r.get("file"),
            "question_id": r.get("question_id"),
            "prompt_variant": r.get("prompt_variant"),
            "trigger_type": r.get("trigger_type"),
            "A_structure": scores.get("A_structure"),
            "B_snapshot_constraint": scores.get("B_snapshot_constraint"),
            "C_actionability": scores.get("C_actionability"),
            "D_completeness": scores.get("D_completeness"),
            "E_drift_failure": scores.get("E_drift_failure"),
            "total": total,
        })

    return rows


def group_scores(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    from collections import defaultdict

    groups = defaultdict(list)
    for r in rows:
        key = (
            r["judge_version"],
            r["generator_model"],
            r["question_id"],
            r["prompt_variant"],
            r["trigger_type"],
        )
        groups[key].append(r)

    grouped = []
    for (jv, gm, qid, pv, tt), items in groups.items():
        agg = {
            "judge_version": jv,
            "generator_model": gm,
            "question_id": qid,
            "prompt_variant": pv,
            "trigger_type": tt,
            "n": len(items),
        }
        for k in [
            "A_structure",
            "B_snapshot_constraint",
            "C_actionability",
            "D_completeness",
            "E_drift_failure",
            "total",
        ]:
            vals = [i[k] for i in items if i[k] is not None]
            agg[k] = sum(vals) / len(vals) if vals else None
        grouped.append(agg)

    return grouped


# -------------------------
# Per-version processing
# -------------------------

def process_one_version(judge_version: str) -> None:
    base = (
        Path("supplement/04_results/03_processed_evaluations")
        / judge_version
        / "valid_evaluations"
    )

    if not base.exists():
        print(f"[SKIP] {judge_version}: no valid_evaluations/")
        return

    valid, excluded = [], []

    for p in base.rglob("record_*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("is_valid", True):
            valid.append(d)
        else:
            excluded.append(d)

    rows = aggregate(valid)
    grouped = group_scores(rows)

    out_root = (
        Path("supplement/04_results/03_processed_evaluations")
        / judge_version
        / "summary_tables"
    )
    out_root.mkdir(parents=True, exist_ok=True)

    write_csv(out_root / "scores_long.csv", rows)
    write_csv(out_root / "scores_grouped.csv", grouped)
    write_jsonl(out_root / "excluded_records.jsonl", excluded)

    run_meta = {
        "judge_version": judge_version,
        "n_valid": len(valid),
        "n_excluded": len(excluded),
        "note": "Derived tables regenerated from processed records; total is computed as sum of per-dimension scores.",
    }
    (out_root / "run_meta.json").write_text(
        json.dumps(run_meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"[OK] {judge_version}: wrote summary_tables/")


# -------------------------
# Main
# -------------------------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--judge_version",
        help="Optional. If omitted, all judge versions will be processed.",
    )
    args = parser.parse_args()

    root = Path("supplement/04_results/03_processed_evaluations")

    if args.judge_version:
        process_one_version(args.judge_version)
    else:
        for d in sorted(root.iterdir()):
            if d.is_dir() and d.name.startswith("v"):
                process_one_version(d.name)


if __name__ == "__main__":
    main()