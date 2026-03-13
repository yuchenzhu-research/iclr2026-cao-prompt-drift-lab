#!/usr/bin/env python3

"""
Offline structural audit for the reproducibility bundle.

This script does not write anything. It reports:
- raw PDF inventory,
- raw judge-bundle counts,
- canonical record/table counts,
- how `total` is recovered across judge versions,
- zero-score counts that are valid outcomes rather than exclusions,
- historical residue that should not be globbed into the active pipeline.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict


INGEST_DIR = Path(__file__).resolve().parent / "ingest"
if str(INGEST_DIR) not in sys.path:
    sys.path.insert(0, str(INGEST_DIR))

from materialize_records import (  # noqa: E402
    RUNS,
    canonical_model_family,
    parse_bundle_filename,
    resolve_output_root,
)


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for _ in reader)


def count_jsonl_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def sorted_counter(counter: Counter[str]) -> Dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def analyze_raw_outputs(reproducibility_root: Path) -> Dict[str, Dict[str, Any]]:
    raw_root = reproducibility_root / "04_results" / "01_raw_model_outputs"
    rows: Dict[str, Dict[str, Any]] = {}

    for path in sorted(raw_root.iterdir()):
        if not path.is_dir():
            continue
        family = canonical_model_family(path.name)
        if family is None:
            continue
        rows[family] = {
            "directory": path.name,
            "pdf_count": len(list(path.glob("*.pdf"))),
        }

    return rows


def analyze_raw_run(reproducibility_root: Path, run_name: str) -> Dict[str, Any]:
    run_dir = reproducibility_root / RUNS[run_name]["in_rel"]
    total_sources: Counter[str] = Counter()
    judge_models = set()
    generator_models = set()
    bundle_count = 0
    item_count = 0

    for bundle_path in sorted(run_dir.glob("judge_*.json")):
        bundle_count += 1
        judge_model, generator_model = parse_bundle_filename(bundle_path.stem)
        judge_models.add(judge_model)
        generator_models.add(generator_model)

        with bundle_path.open("r", encoding="utf-8") as handle:
            bundle = json.load(handle)

        items = bundle.get("per_file_scores") or []
        item_count += len(items)
        for item in items:
            scores = item.get("scores") or {}
            if item.get("total") not in (None, ""):
                total_sources["item.total"] += 1
            elif scores.get("total") not in (None, ""):
                total_sources["scores.total"] += 1
            else:
                total_sources["derived_from_dimensions"] += 1

    return {
        "raw_bundle_count": bundle_count,
        "raw_item_count": item_count,
        "judge_models": sorted(judge_models),
        "generator_models": sorted(generator_models),
        "total_sources": sorted_counter(total_sources),
    }


def analyze_processed_run(output_root: Path, run_name: str) -> Dict[str, Any]:
    run_root = output_root / run_name
    valid_root = run_root / "valid_evaluations"
    canonical_dir = valid_root / "main_method_cross_model"
    summary_dir = run_root / "summary_tables"
    long_path = summary_dir / "scores_long.csv"
    grouped_path = summary_dir / "scores_grouped.csv"
    excluded_path = summary_dir / "excluded_records.jsonl"

    record_count = len(list(canonical_dir.glob("record_*.json"))) if canonical_dir.exists() else 0
    long_rows = count_csv_rows(long_path)
    grouped_rows = count_csv_rows(grouped_path)
    excluded_rows = count_jsonl_rows(excluded_path)

    zero_totals: Counter[str] = Counter()
    long_generators = set()
    if long_path.exists():
        with long_path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                generator_model = row.get("generator_model") or ""
                if generator_model:
                    long_generators.add(generator_model)
                total = float(row.get("total") or 0)
                if total == 0:
                    zero_totals[generator_model] += 1

    historical_root_json = len(list(valid_root.glob("*.json"))) if valid_root.exists() else 0
    historical_dirs: Dict[str, int] = {}
    if valid_root.exists():
        for child in sorted(valid_root.iterdir()):
            if child.is_dir() and child.name != "main_method_cross_model":
                historical_dirs[child.name] = len(list(child.rglob("*.json")))

    issues = []
    if record_count != long_rows:
        issues.append(f"canonical record count ({record_count}) != scores_long rows ({long_rows})")
    if grouped_rows > long_rows:
        issues.append(f"scores_grouped rows ({grouped_rows}) > scores_long rows ({long_rows})")

    return {
        "record_count": record_count,
        "long_rows": long_rows,
        "grouped_rows": grouped_rows,
        "excluded_rows": excluded_rows,
        "generator_models": sorted(long_generators),
        "zero_totals": sorted_counter(zero_totals),
        "historical_root_json": historical_root_json,
        "historical_dirs": historical_dirs,
        "issues": issues,
    }


def build_audit(project_root: Path, output_root: Path) -> Dict[str, Any]:
    reproducibility_root = project_root / "reproducibility"
    raw_outputs = analyze_raw_outputs(reproducibility_root)
    runs: Dict[str, Dict[str, Any]] = {}
    issues = []

    for run_name in RUNS:
        raw = analyze_raw_run(reproducibility_root, run_name)
        processed = analyze_processed_run(output_root, run_name)
        run_issues = list(processed["issues"])

        if raw["raw_item_count"] != processed["record_count"] + processed["excluded_rows"]:
            run_issues.append(
                "raw bundle item count "
                f"({raw['raw_item_count']}) != records + exclusions "
                f"({processed['record_count']} + {processed['excluded_rows']})"
            )
        if raw["generator_models"] != processed["generator_models"]:
            run_issues.append(
                f"generator family mismatch: raw={raw['generator_models']} "
                f"processed={processed['generator_models']}"
            )

        status = "ok" if not run_issues else "needs_attention"
        run_summary = {
            "status": status,
            **raw,
            **processed,
            "issues": run_issues,
        }
        runs[run_name] = run_summary
        issues.extend(f"{run_name}: {issue}" for issue in run_issues)

    return {
        "project_root": str(project_root),
        "output_root": str(output_root),
        "raw_outputs": raw_outputs,
        "runs": runs,
        "issues": issues,
    }


def print_text(audit: Dict[str, Any]) -> None:
    print("Artifact audit")
    print("")
    print("Raw outputs")
    total_pdfs = 0
    for family, row in sorted(audit["raw_outputs"].items()):
        total_pdfs += row["pdf_count"]
        print(f"- {family}: {row['pdf_count']} PDFs ({row['directory']})")
    print(f"- total: {total_pdfs} PDFs")

    print("")
    print("Judge versions")
    for run_name, row in audit["runs"].items():
        print(
            f"- {run_name}: status={row['status']}, bundles={row['raw_bundle_count']}, "
            f"raw_items={row['raw_item_count']}, records={row['record_count']}, "
            f"long_rows={row['long_rows']}, grouped_rows={row['grouped_rows']}, "
            f"excluded={row['excluded_rows']}"
        )
        judges = ", ".join(row["judge_models"]) or "none"
        generators = ", ".join(row["generator_models"]) or "none"
        print(f"  judges={judges}; generators={generators}")

        total_sources = ", ".join(
            f"{key}={value}" for key, value in row["total_sources"].items()
        ) or "none"
        zero_totals = ", ".join(
            f"{key}={value}" for key, value in row["zero_totals"].items()
        ) or "none"
        print(f"  total_sources={total_sources}")
        print(f"  zero_totals={zero_totals}")

        if row["historical_root_json"] or row["historical_dirs"]:
            residue = []
            if row["historical_root_json"]:
                residue.append(f"root_json={row['historical_root_json']}")
            residue.extend(
                f"{name}={count}" for name, count in sorted(row["historical_dirs"].items())
            )
            print(f"  historical_residue={', '.join(residue)}")

        for issue in row["issues"]:
            print(f"  issue={issue}")

    if audit["issues"]:
        print("")
        print("Overall issues")
        for issue in audit["issues"]:
            print(f"- {issue}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output_root",
        type=Path,
        default=Path("reproducibility/04_results/03_processed_evaluations"),
        help="processed evaluation directory to audit",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="render audit in human-readable text or JSON",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit non-zero if any invariant check fails",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[2]
    output_root = resolve_output_root(project_root, args.output_root)
    audit = build_audit(project_root, output_root)

    if args.format == "json":
        json.dump(audit, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_text(audit)

    if args.strict and audit["issues"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
