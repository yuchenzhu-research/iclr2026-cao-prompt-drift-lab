#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Rebuild processed evaluation tables from record JSON files.

Supported modes:
- records -> summary tables
- raw judge bundles -> records -> summary tables (`--from_raw`)

This script is deterministic and offline. It never re-runs judging.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


DIMENSIONS = [
    "A_structure",
    "B_snapshot_constraint",
    "C_actionability",
    "D_completeness",
    "E_drift_failure",
]


INGEST_DIR = Path(__file__).resolve().parent / "ingest"
if str(INGEST_DIR) not in sys.path:
    sys.path.insert(0, str(INGEST_DIR))

from materialize_records import RUNS, process_one_run, resolve_output_root  # noqa: E402


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def discover_record_paths(base: Path) -> List[Path]:
    canonical_dir = base / "main_method_cross_model"
    record_paths = sorted(canonical_dir.glob("record_*.json"))
    if record_paths:
        return record_paths
    return sorted(base.rglob("record_*.json"))


def derive_total(record: Dict[str, Any]) -> int:
    total = record.get("total")
    if total not in (None, ""):
        return int(total)
    scores = record.get("scores") or {}
    return sum(int(scores[field]) for field in DIMENSIONS)


def aggregate(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    for record in records:
        scores = record.get("scores") or {}
        row = {
            "judge_version": record.get("judge_version"),
            "snapshot_contract_id": record.get("snapshot_contract_id"),
            "judge_model": record.get("judge_model"),
            "generator_model": record.get("generator_model"),
            "bundle_file": record.get("bundle_file") or record.get("source_bundle"),
            "file": record.get("file"),
            "question_id": record.get("question_id"),
            "prompt_variant": record.get("prompt_variant"),
            "trigger_type": record.get("trigger_type"),
            "A_structure": int(scores["A_structure"]),
            "B_snapshot_constraint": int(scores["B_snapshot_constraint"]),
            "C_actionability": int(scores["C_actionability"]),
            "D_completeness": int(scores["D_completeness"]),
            "E_drift_failure": int(scores["E_drift_failure"]),
            "total": derive_total(record),
        }
        rows.append(row)

    rows.sort(
        key=lambda row: (
            row["judge_version"] or "",
            row["judge_model"] or "",
            row["generator_model"] or "",
            row["question_id"] or "",
            row["prompt_variant"] or "",
            row["trigger_type"] or "",
            row["file"] or "",
        )
    )
    return rows


def group_scores(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[tuple, List[Dict[str, Any]]] = defaultdict(list)

    for row in rows:
        key = (
            row["judge_version"],
            row["judge_model"],
            row["generator_model"],
            row["question_id"],
            row["prompt_variant"],
            row["trigger_type"],
        )
        groups[key].append(row)

    grouped: List[Dict[str, Any]] = []
    for (
        judge_version,
        judge_model,
        generator_model,
        question_id,
        prompt_variant,
        trigger_type,
    ), items in sorted(groups.items()):
        row = {
            "judge_version": judge_version,
            "judge_model": judge_model,
            "generator_model": generator_model,
            "question_id": question_id,
            "prompt_variant": prompt_variant,
            "trigger_type": trigger_type,
            "n": len(items),
        }
        for field in DIMENSIONS + ["total"]:
            values = [float(item[field]) for item in items]
            row[f"{field}_mean"] = sum(values) / len(values)
        grouped.append(row)

    return grouped


def count_existing_exclusions(summary_dir: Path) -> int:
    path = summary_dir / "excluded_records.jsonl"
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def process_one_version(output_root: Path, judge_version: str) -> None:
    base = output_root / judge_version / "valid_evaluations"
    if not base.exists():
        print(f"[SKIP] {judge_version}: no valid_evaluations/")
        return

    record_paths = discover_record_paths(base)
    if not record_paths:
        print(f"[SKIP] {judge_version}: no record_*.json files found")
        return

    records = [load_json(path) for path in record_paths]
    rows = aggregate(records)
    grouped = group_scores(rows)

    summary_dir = output_root / judge_version / "summary_tables"
    summary_dir.mkdir(parents=True, exist_ok=True)

    write_csv(summary_dir / "scores_long.csv", rows)
    write_csv(summary_dir / "scores_grouped.csv", grouped)

    existing_run_meta = load_json(summary_dir / "run_meta.json") if (summary_dir / "run_meta.json").exists() else {}
    existing_run_meta.update(
        {
            "judge_version": judge_version,
            "n_records": len(rows),
            "n_grouped_rows": len(grouped),
            "n_excluded": count_existing_exclusions(summary_dir),
            "generated_by": "reproducibility/tools/reproduce_valid_evaluations.py",
            "pipeline": "raw judge bundles -> record JSON -> summary tables",
        }
    )
    with (summary_dir / "run_meta.json").open("w", encoding="utf-8") as handle:
        json.dump(existing_run_meta, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"[OK] {judge_version}: wrote summary tables to {summary_dir}")


def select_versions(output_root: Path, judge_version: str | None, from_raw: bool) -> List[str]:
    if judge_version:
        return [judge_version]
    if from_raw:
        return list(RUNS.keys())

    versions: List[str] = []
    for path in sorted(output_root.iterdir() if output_root.exists() else []):
        if path.is_dir() and path.name in RUNS:
            versions.append(path.name)
    return versions or list(RUNS.keys())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--judge_version",
        choices=list(RUNS.keys()),
        help="optional single judge version to rebuild",
    )
    parser.add_argument(
        "--from_raw",
        action="store_true",
        help="first rebuild record JSON from raw judge bundles, then write summary tables",
    )
    parser.add_argument(
        "--overwrite_records",
        action="store_true",
        help="when used with --from_raw, overwrite generated record JSON files before rebuilding",
    )
    parser.add_argument(
        "--output_root",
        type=Path,
        default=Path("reproducibility/04_results/03_processed_evaluations"),
        help="output directory for processed evaluation artifacts",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    reproducibility_root = project_root / "reproducibility"
    output_root = resolve_output_root(project_root, args.output_root)
    versions = select_versions(output_root, args.judge_version, args.from_raw)

    if args.from_raw:
        for run_name in versions:
            process_one_run(
                reproducibility_root=reproducibility_root,
                output_root=output_root,
                run_name=run_name,
                overwrite=args.overwrite_records,
            )

    for run_name in versions:
        process_one_version(output_root=output_root, judge_version=run_name)


if __name__ == "__main__":
    main()
