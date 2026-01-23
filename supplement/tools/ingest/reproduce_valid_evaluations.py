#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ingestion Utility: Raw Judge Bundles → Processed Evaluation Records

This script materializes schema-normalized evaluation records (`record_*.json`)
from raw judge bundle outputs under:

  supplement/04_results/02_raw_judge_evaluations/

Responsibilities:
- Parse raw judge bundle JSONs
- Normalize per-file evaluation entries
- Write deterministic, schema-aligned `record_*.json` files

Non-responsibilities:
- Model execution
- PDF parsing
- Score computation or modification
- Aggregation or statistics

This script performs deterministic post-processing only.
"""

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------
# Paths & run configuration
# ---------------------------------------------------------

SUPPLEMENT_ROOT = Path(__file__).resolve().parents[2]

RUNS = {
    "v0_baseline_judge": {
        "in_rel": "04_results/02_raw_judge_evaluations/diagnostic/v0_baseline_judge",
        "out_rel": "04_results/03_processed_evaluations/v0_baseline_judge",
    },
    "v1_paraphrase_judge": {
        "in_rel": "04_results/02_raw_judge_evaluations/final/v1_paraphrase_judge",
        "out_rel": "04_results/03_processed_evaluations/v1_paraphrase_judge",
    },
    "v2_schema_strict_judge": {
        "in_rel": "04_results/02_raw_judge_evaluations/final/v2_schema_strict_judge",
        "out_rel": "04_results/03_processed_evaluations/v2_schema_strict_judge",
    },
}

DIM_KEYS = [
    "A_structure",
    "B_snapshot_constraint",
    "C_actionability",
    "D_completeness",
    "E_drift_failure",
]

DEFAULT_VARIANTS = ["baseline", "long", "weak", "conflict"]
DEFAULT_TRIGGERS = ["explicit", "implicit"]

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def sha12(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def load_json(p: Path) -> Dict:
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(p: Path, obj: Dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_bundle_filename(stem: str):
    """
    Expected pattern:
      judge_<judge_model>_bundle_<generator_model>.json
    """
    m = re.match(r"^judge_(?P<judge>.+?)_bundle_(?P<gen>.+?)$", stem)
    if not m:
        return "unknown", "unknown"
    return m.group("judge").lower(), m.group("gen").lower()


def parse_file_label(
    file_label: str,
    known_variants: Optional[List[str]] = None,
    known_triggers: Optional[List[str]] = None,
) -> Dict[str, Optional[str]]:
    known_variants = (known_variants or []) + DEFAULT_VARIANTS
    known_triggers = (known_triggers or []) + DEFAULT_TRIGGERS

    base = file_label[:-4] if file_label.lower().endswith(".pdf") else file_label
    norm = re.sub(r"[_\s]+", " ", base.strip())
    toks = norm.split(" ")

    qid = next((t for t in toks if re.fullmatch(r"q\d+", t.lower())), None)
    variant = next((t for t in toks if t.lower() in set(map(str.lower, known_variants))), None)
    trigger = next((t for t in toks if t.lower() in set(map(str.lower, known_triggers))), None)

    return {
        "question_id": qid.lower() if qid else None,
        "prompt_variant": variant.lower() if variant else None,
        "trigger_type": trigger.lower() if trigger else None,
    }

# ---------------------------------------------------------
# Core logic
# ---------------------------------------------------------

def process_run(run_name: str, overwrite: bool) -> None:
    cfg = RUNS[run_name]
    in_dir = SUPPLEMENT_ROOT / cfg["in_rel"]
    out_dir = SUPPLEMENT_ROOT / cfg["out_rel"]

    if not in_dir.exists():
        raise FileNotFoundError(f"Missing input directory: {in_dir}")

    valid_dir = out_dir / "valid_evaluations" / "main_method_cross_model"
    summary_dir = out_dir / "summary_tables"

    if overwrite:
        for d in [valid_dir, summary_dir]:
            if d.exists():
                for f in d.rglob("*"):
                    if f.is_file():
                        f.unlink()

    valid_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    excluded = []
    n_written = 0

    for bundle_path in sorted(in_dir.glob("*.json")):
        if bundle_path.name == "run_meta.json":
            continue

        try:
            bundle = load_json(bundle_path)
        except Exception as e:
            excluded.append({
                "bundle": bundle_path.name,
                "reason": f"json_load_failed: {e}",
            })
            continue

        if "bundle_meta" not in bundle or "per_file_scores" not in bundle:
            excluded.append({
                "bundle": bundle_path.name,
                "reason": "missing bundle_meta or per_file_scores",
            })
            continue

        bundle_meta = bundle["bundle_meta"]
        per_file_scores = bundle["per_file_scores"]

        judge_model, generator_model = parse_bundle_filename(bundle_path.stem)

        known_variants = [str(x) for x in bundle_meta.get("versions", [])]
        known_triggers = [str(x) for x in bundle_meta.get("trigger_types", [])]

        for item in per_file_scores:
            file_label = item.get("file")
            if not file_label:
                excluded.append({
                    "bundle": bundle_path.name,
                    "reason": "missing file field",
                    "item": item,
                })
                continue

            scores_raw = item.get("scores", {})
            evidence = item.get("evidence", {})
            notes = item.get("notes")

            scores = {k: scores_raw.get(k) for k in DIM_KEYS}
            total = item.get("total")
            if total is None:
                total = sum(int(v) for v in scores.values() if v is not None)

            parsed = parse_file_label(
                file_label,
                known_variants=known_variants,
                known_triggers=known_triggers,
            )

            rid = sha12(
                f"{run_name}|{judge_model}|{generator_model}|{bundle_path.name}|{file_label}"
            )

            record = {
                "judge_version": run_name,
                "judge_model": judge_model,
                "generator_model": generator_model,
                "source_bundle": bundle_path.name,
                "bundle_meta": bundle_meta,
                "file": file_label,
                "question_id": parsed["question_id"],
                "prompt_variant": parsed["prompt_variant"],
                "trigger_type": parsed["trigger_type"],
                "scores": scores,
                "total": total,
                "evidence": evidence,
                "notes": notes,
                "method": "cross_model",
            }

            write_json(valid_dir / f"record_{rid}.json", record)
            n_written += 1

    # excluded records
    if excluded:
        with (summary_dir / "excluded_records.jsonl").open("w", encoding="utf-8") as f:
            for r in excluded:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # run meta
    run_meta = {
        "judge_version": run_name,
        "n_valid_written": n_written,
        "n_excluded_items": len(excluded),
        "note": "Records materialized from raw judge bundles; schema-normalized; scores unchanged.",
    }
    write_json(summary_dir / "run_meta.json", run_meta)

    print(f"[OK] {run_name}: wrote {n_written} records, excluded {len(excluded)}")

# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Materialize processed evaluation records from raw judge bundles."
    )
    parser.add_argument(
        "--runs",
        nargs="*",
        choices=RUNS.keys(),
        default=list(RUNS.keys()),
        help="Judge versions to process",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing outputs",
    )
    args = parser.parse_args()

    for r in args.runs:
        process_run(r, overwrite=args.overwrite)


if __name__ == "__main__":
    main()