#!/usr/bin/env python3

"""
Ingest utility: materialize processed evaluation records (record-level JSON)
from raw judge evaluation bundles.

This is an OPTIONAL audit utility.
- It does NOT run any model inference.
- It does NOT generate summary CSV tables (e.g., scores_long.csv).

Reproducibility boundary for this submission:
- Authoritative evaluation tables are the shipped scores_long.csv files under:
  reproducibility/04_results/03_processed_evaluations/*/summary_tables/scores_long.csv
- Figures are reproducible from these shipped CSV tables.
- Regenerating scores_long.csv from raw bundles/records is out of scope for artifact reproduction.
"""


import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# -----------------------------
# Run routing (repo-specific)
# -----------------------------
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



# -----------------------------
# Helpers
# -----------------------------
def stable_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def load_json(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def parse_bundle_filename(stem: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Expected: judge_<judge>_bundle_<generator>
    e.g., judge_chatgpt_bundle_gemini
    """
    m = re.match(r"^judge_(?P<judge>.+?)_bundle_(?P<gen>.+?)$", stem)
    if not m:
        return None, None
    return m.group("judge"), m.group("gen")


def parse_file_label(file_label: str, known_variants: List[str], known_triggers: List[str]) -> Dict[str, Optional[str]]:
    """
    Robust parsing for labels like:
      'q3 baseline explicit.pdf'
      'q4_long_implicit.pdf'  (fallback)
    Returns fields: question_id, prompt_variant, trigger_type
    """
    raw = file_label
    base = raw
    if base.lower().endswith(".pdf"):
        base = base[:-4]

    # normalize separators
    norm = re.sub(r"[_\s]+", " ", base.strip())
    toks = norm.split(" ")

    q = next((t for t in toks if re.fullmatch(r"q\d+", t.lower())), None)
    trig = next((t for t in toks if t.lower() in set(map(str.lower, known_triggers))), None)
    var = next((t for t in toks if t.lower() in set(map(str.lower, known_variants))), None)

    # best-effort: sometimes variant/trig might be missing in tokens
    return {
        "question_id": q.lower() if q else None,
        "prompt_variant": var.lower() if var else None,
        "trigger_type": trig.lower() if trig else None,
        "raw_label": raw,
    }


def flatten_scores(scores: Dict) -> Dict[str, Optional[float]]:
    out = {}
    for k in ["A_structure", "B_snapshot_constraint", "C_actionability", "D_completeness", "E_drift_failure"]:
        out[k] = scores.get(k)
    return out


def safe_record_filename(generator_model: str, judge_model: str, parsed: Dict, file_label: str) -> str:
    q = parsed.get("question_id") or "qX"
    v = parsed.get("prompt_variant") or "varX"
    t = parsed.get("trigger_type") or "trigX"
    h = stable_hash(f"{judge_model}|{generator_model}|{file_label}")
    return f"{generator_model}__judged_by__{judge_model}__{q}_{v}_{t}__{h}.json"



# -----------------------------
# Core
# -----------------------------
def process_one_run(repo_root: Path, run_name: str, overwrite: bool) -> None:
    cfg = RUNS[run_name]
    in_dir = repo_root / cfg["in_rel"]
    out_dir = repo_root / cfg["out_rel"]

    if not in_dir.exists():
        raise FileNotFoundError(f"Missing input dir: {in_dir}")

    valid_dir = out_dir / "valid_evaluations" / "main_method_cross_model"
    summary_dir = out_dir / "summary_tables"
    excluded_path = summary_dir / "excluded_records.jsonl"

    if overwrite and out_dir.exists():
        # remove only generated subtrees we own
        for p in (valid_dir, summary_dir):
            if p.exists():
                for x in p.rglob("*"):
                    if x.is_file():
                        x.unlink()

    valid_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    # copy run_meta if present
    run_meta_path = in_dir / "run_meta.json"
    run_meta = load_json(run_meta_path) if run_meta_path.exists() else {}
    if run_meta:
        write_json(summary_dir / "run_meta.json", run_meta)

    rows = []
    excluded = []

    # iterate judge bundle json files
    for bundle_path in sorted(in_dir.glob("*.json")):
        if bundle_path.name == "run_meta.json":
            continue

        try:
            bundle = load_json(bundle_path)
        except Exception as e:
            excluded.append({"file": str(bundle_path), "reason": f"json_load_failed: {e}"})
            continue

        # minimal structural checks
        if "bundle_meta" not in bundle or "per_file_scores" not in bundle:
            excluded.append({"file": str(bundle_path), "reason": "missing_keys: bundle_meta/per_file_scores"})
            continue

        meta = bundle.get("bundle_meta", {}) or {}
        per_file = bundle.get("per_file_scores", []) or []

        judge_model, gen_from_name = parse_bundle_filename(bundle_path.stem)
        generator_model = (meta.get("model") or gen_from_name or "unknown").lower()
        judge_model = (judge_model or "unknown").lower()

        known_variants = meta.get("versions", []) or []
        known_triggers = meta.get("trigger_types", []) or []
        # normalize to strings
        known_variants = [str(x) for x in known_variants]
        known_triggers = [str(x) for x in known_triggers]

        for item in per_file:
            file_label = item.get("file")
            scores = item.get("scores") or {}
            total = item.get("total")
            evidence = item.get("evidence") or {}
            notes = item.get("notes")

            if not file_label or not isinstance(scores, dict):
                excluded.append({
                    "file": str(bundle_path),
                    "reason": "bad_item: missing file or scores",
                    "item": item,
                })
                continue

            parsed = parse_file_label(file_label, known_variants, known_triggers)

            record = {
                "judge_version": run_name,
                "snapshot_contract_id": run_meta.get("snapshot_contract_id"),
                "snapshot_word_limit": run_meta.get("snapshot_word_limit"),
                "snapshot_allow_extension": run_meta.get("snapshot_allow_extension"),
                "judge_model": judge_model,
                "generator_model": generator_model,
                "bundle_file": bundle_path.name,
                "bundle_meta": meta,
                "file": file_label,
                "question_id": parsed.get("question_id"),
                "prompt_variant": parsed.get("prompt_variant"),
                "trigger_type": parsed.get("trigger_type"),
                "scores": scores,
                "total": total,
                "evidence": evidence,
                "notes": notes,
                "method": "cross_model",
            }

            out_name = safe_record_filename(generator_model, judge_model, parsed, file_label)
            write_json(valid_dir / out_name, record)

            flat = flatten_scores(scores)
            rows.append({
                "judge_version": run_name,
                "snapshot_contract_id": run_meta.get("snapshot_contract_id"),
                "judge_model": judge_model,
                "generator_model": generator_model,
                "bundle_file": bundle_path.name,
                "file": file_label,
                "question_id": parsed.get("question_id"),
                "prompt_variant": parsed.get("prompt_variant"),
                "trigger_type": parsed.get("trigger_type"),
                **flat,
                "total": total,
            })

    # write excluded log
    if excluded:
        excluded_path.parent.mkdir(parents=True, exist_ok=True)
        with open(excluded_path, "w", encoding="utf-8") as f:
            for r in excluded:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # NOTE: We intentionally do NOT generate summary tables here.
    # Summary tables (if provided) live under each judge_version's summary_tables/ directory.
    # This script only materializes record-level JSON + optional excluded_records.jsonl for auditability.

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action="store_true", help="overwrite generated outputs under 03_processed_evaluations/")
    parser.add_argument(
        "--runs",
        nargs="*",
        default=["v0_baseline_judge", "v1_paraphrase_judge", "v2_schema_strict_judge"],
        choices=list(RUNS.keys()),
        help="which runs to materialize",
    )
    args = parser.parse_args()

    reproducibility_root = Path(__file__).resolve().parents[2]
    for r in args.runs:
        if r == "v0_baseline_judge":
            print("[WARN] Running v0_baseline_judge (legacy / not reproducible). Outputs are non-authoritative.")
        process_one_run(reproducibility_root, r, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
