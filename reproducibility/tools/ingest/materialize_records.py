#!/usr/bin/env python3

"""
Materialize record-level JSON from preserved raw judge bundles.

This script is deterministic and offline:
- it never calls an API,
- it never re-runs judging,
- it only normalizes preserved bundle metadata into stable record JSON files.

The companion script `reproducibility/tools/reproduce_valid_evaluations.py`
can then aggregate these records into `scores_long.csv` and `scores_grouped.csv`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


DIMENSIONS = [
    "A_structure",
    "B_snapshot_constraint",
    "C_actionability",
    "D_completeness",
    "E_drift_failure",
]

DEFAULT_VARIANTS = ("baseline", "conflict", "long", "weak")
DEFAULT_TRIGGERS = ("explicit", "implicit")
KNOWN_MODEL_FAMILIES = ("chatgpt", "gemini", "claude")


RUNS = {
    "v0_baseline_judge": {
        "in_rel": "04_results/02_raw_judge_evaluations/diagnostic/v0_baseline_judge",
    },
    "v1_paraphrase_judge": {
        "in_rel": "04_results/02_raw_judge_evaluations/final/v1_paraphrase_judge",
    },
    "v2_schema_strict_judge": {
        "in_rel": "04_results/02_raw_judge_evaluations/final/v2_schema_strict_judge",
    },
}


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, obj: Dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(obj, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def resolve_output_root(project_root: Path, output_root: Path) -> Path:
    return output_root if output_root.is_absolute() else project_root / output_root


def canonical_model_family(label: Optional[str]) -> Optional[str]:
    if label is None:
        return None

    normalized = re.sub(r"[^a-z0-9]+", " ", str(label).strip().lower())
    if not normalized:
        return None

    if "chatgpt" in normalized or "openai" in normalized or re.search(r"\bgpt\b", normalized) or re.search(r"\bgpt\s*5\b", normalized):
        return "chatgpt"
    if "gemini" in normalized or "google" in normalized:
        return "gemini"
    if "claude" in normalized or "anthropic" in normalized:
        return "claude"
    if normalized in KNOWN_MODEL_FAMILIES:
        return normalized
    return None


def parse_bundle_filename(stem: str) -> Tuple[str, str]:
    match = re.match(r"^judge_(?P<judge>.+?)_bundle_(?P<generator>.+?)$", stem)
    if not match:
        raise ValueError(f"Unexpected bundle filename: {stem}")

    judge = canonical_model_family(match.group("judge"))
    generator = canonical_model_family(match.group("generator"))
    if judge is None or generator is None:
        raise ValueError(f"Could not canonicalize bundle filename: {stem}")
    return judge, generator


def discover_raw_output_dirs(raw_outputs_root: Path) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for path in sorted(raw_outputs_root.iterdir()):
        if not path.is_dir():
            continue
        family = canonical_model_family(path.name)
        if family is None:
            continue
        if family in mapping and mapping[family] != path.name:
            raise ValueError(
                f"Multiple raw-output directories map to {family}: "
                f"{mapping[family]} vs {path.name}"
            )
        mapping[family] = path.name

    missing = [family for family in KNOWN_MODEL_FAMILIES if family not in mapping]
    if missing:
        raise FileNotFoundError(
            f"Missing raw-output directories for: {missing}. "
            f"Found: {mapping}"
        )
    return mapping


def normalize_pdf_name(label: str) -> str:
    base = Path(str(label).replace("\\", "/")).name.lower()
    return re.sub(r"[^a-z0-9]+", "", base)


def choose_known_values(values: Optional[Sequence[str]], defaults: Sequence[str]) -> List[str]:
    cleaned = [str(value).strip().lower() for value in values or [] if str(value).strip()]
    return cleaned or list(defaults)


def parse_file_label(
    file_label: str,
    known_variants: Sequence[str],
    known_triggers: Sequence[str],
) -> Dict[str, Optional[str]]:
    base_name = Path(str(file_label).replace("\\", "/")).name
    stem = base_name[:-4] if base_name.lower().endswith(".pdf") else base_name
    normalized = re.sub(r"[_\s]+", " ", stem.strip().lower())
    tokens = normalized.split()

    question_id = next((token for token in tokens if re.fullmatch(r"q\d+", token)), None)
    prompt_variant = next((token for token in tokens if token in set(known_variants)), None)
    trigger_type = next((token for token in tokens if token in set(known_triggers)), None)

    return {
        "question_id": question_id,
        "prompt_variant": prompt_variant,
        "trigger_type": trigger_type,
        "base_name": base_name,
    }


def resolve_raw_pdf_relpath(
    reproducibility_root: Path,
    raw_output_dirs: Dict[str, str],
    generator_model: str,
    file_label: str,
) -> str:
    raw_outputs_root = reproducibility_root / "04_results" / "01_raw_model_outputs"
    label = str(file_label).replace("\\", "/")
    path_like = Path(label)

    direct_candidates: List[Path] = []
    if "/" in label:
        direct_candidates.append(raw_outputs_root / path_like)
        direct_candidates.append(reproducibility_root / path_like)

    for candidate in direct_candidates:
        if candidate.exists():
            return candidate.relative_to(reproducibility_root).as_posix()

    target_name = Path(label).name
    family_dir = raw_outputs_root / raw_output_dirs[generator_model]
    exact = family_dir / target_name
    if exact.exists():
        return exact.relative_to(reproducibility_root).as_posix()

    normalized_target = normalize_pdf_name(target_name)
    family_matches = [
        path for path in family_dir.glob("*.pdf")
        if normalize_pdf_name(path.name) == normalized_target
    ]
    if len(family_matches) == 1:
        return family_matches[0].relative_to(reproducibility_root).as_posix()
    if len(family_matches) > 1:
        raise ValueError(f"Ambiguous raw PDF match for {file_label}: {family_matches}")

    global_matches = [
        path for path in raw_outputs_root.rglob("*.pdf")
        if normalize_pdf_name(path.name) == normalized_target
    ]
    if len(global_matches) == 1:
        return global_matches[0].relative_to(reproducibility_root).as_posix()
    raise FileNotFoundError(
        f"Could not resolve raw PDF for {file_label!r} (generator={generator_model})."
    )


def coerce_score(value: object, field: str) -> int:
    if value is None:
        raise ValueError(f"Missing score for {field}")
    return int(value)


def extract_total(item: Dict, scores: Dict[str, object]) -> Tuple[int, str]:
    for source_name, candidate in (
        ("item.total", item.get("total")),
        ("scores.total", scores.get("total")),
    ):
        if candidate not in (None, ""):
            return int(candidate), source_name

    derived = sum(coerce_score(scores.get(field), field) for field in DIMENSIONS)
    return derived, "derived_from_dimensions"


def clear_generated_records(valid_dir: Path) -> None:
    if not valid_dir.exists():
        return
    for path in valid_dir.glob("*.json"):
        path.unlink()


def write_excluded_rows(path: Path, rows: Iterable[Dict]) -> None:
    rows = list(rows)
    if not rows:
        if path.exists():
            path.unlink()
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")


def build_record(
    run_name: str,
    run_meta: Dict,
    bundle_path: Path,
    bundle_meta: Dict,
    item: Dict,
    raw_output_dirs: Dict[str, str],
    reproducibility_root: Path,
) -> Dict:
    judge_model, generator_model = parse_bundle_filename(bundle_path.stem)

    known_variants = choose_known_values(bundle_meta.get("versions"), DEFAULT_VARIANTS)
    known_triggers = choose_known_values(bundle_meta.get("trigger_types"), DEFAULT_TRIGGERS)
    parsed = parse_file_label(str(item["file"]), known_variants, known_triggers)

    scores = item.get("scores") or {}
    missing_dimensions = [field for field in DIMENSIONS if field not in scores]
    if missing_dimensions:
        raise ValueError(f"Missing score fields: {missing_dimensions}")

    total, total_source = extract_total(item, scores)
    raw_pdf = resolve_raw_pdf_relpath(
        reproducibility_root=reproducibility_root,
        raw_output_dirs=raw_output_dirs,
        generator_model=generator_model,
        file_label=str(item["file"]),
    )

    record_id = stable_hash(
        "|".join(
            [
                run_name,
                bundle_path.name,
                judge_model,
                generator_model,
                str(item["file"]),
                raw_pdf,
            ]
        )
    )

    return {
        "record_id": f"record_{record_id}",
        "judge_version": run_name,
        "snapshot_contract_id": run_meta.get("snapshot_contract_id"),
        "snapshot_word_limit": run_meta.get("snapshot_word_limit"),
        "snapshot_allow_extension": run_meta.get("snapshot_allow_extension"),
        "judge_model": judge_model,
        "generator_model": generator_model,
        "source_bundle": bundle_path.name,
        "bundle_file": bundle_path.name,
        "bundle_meta": bundle_meta,
        "file": str(item["file"]),
        "raw_pdf": raw_pdf,
        "question_id": parsed["question_id"],
        "prompt_variant": parsed["prompt_variant"],
        "trigger_type": parsed["trigger_type"],
        "scores": {field: coerce_score(scores.get(field), field) for field in DIMENSIONS},
        "total": total,
        "total_source": total_source,
        "evidence": item.get("evidence") or {},
        "notes": item.get("notes"),
        "method": "cross_model",
        "is_valid": True,
    }


def process_one_run(
    reproducibility_root: Path,
    output_root: Path,
    run_name: str,
    overwrite: bool,
) -> None:
    in_dir = reproducibility_root / RUNS[run_name]["in_rel"]
    out_dir = output_root / run_name

    if not in_dir.exists():
        raise FileNotFoundError(f"Missing input directory: {in_dir}")

    valid_dir = out_dir / "valid_evaluations" / "main_method_cross_model"
    summary_dir = out_dir / "summary_tables"
    excluded_path = summary_dir / "excluded_records.jsonl"
    run_meta_out_path = summary_dir / "run_meta.json"

    if overwrite:
        clear_generated_records(valid_dir)
        if excluded_path.exists():
            excluded_path.unlink()

    valid_dir.mkdir(parents=True, exist_ok=True)
    summary_dir.mkdir(parents=True, exist_ok=True)

    run_meta_in_path = in_dir / "run_meta.json"
    run_meta = load_json(run_meta_in_path) if run_meta_in_path.exists() else {}
    if run_meta:
        write_json(run_meta_out_path, run_meta)

    raw_output_dirs = discover_raw_output_dirs(
        reproducibility_root / "04_results" / "01_raw_model_outputs"
    )

    excluded_rows: List[Dict] = []
    written = 0

    for bundle_path in sorted(in_dir.glob("*.json")):
        if bundle_path.name == "run_meta.json":
            continue

        try:
            bundle = load_json(bundle_path)
            bundle_meta = bundle.get("bundle_meta") or {}
            per_file_scores = bundle.get("per_file_scores") or []
            if not isinstance(per_file_scores, list):
                raise ValueError("per_file_scores is not a list")
        except Exception as exc:  # noqa: BLE001
            excluded_rows.append(
                {
                    "bundle_file": bundle_path.name,
                    "reason": f"bundle_load_failed: {exc}",
                }
            )
            continue

        for index, item in enumerate(per_file_scores):
            try:
                if "file" not in item or "scores" not in item:
                    raise ValueError("missing required keys: file/scores")
                record = build_record(
                    run_name=run_name,
                    run_meta=run_meta,
                    bundle_path=bundle_path,
                    bundle_meta=bundle_meta,
                    item=item,
                    raw_output_dirs=raw_output_dirs,
                    reproducibility_root=reproducibility_root,
                )
            except Exception as exc:  # noqa: BLE001
                excluded_rows.append(
                    {
                        "bundle_file": bundle_path.name,
                        "item_index": index,
                        "file": item.get("file"),
                        "reason": str(exc),
                    }
                )
                continue

            record_path = valid_dir / f"{record['record_id']}.json"
            write_json(record_path, record)
            written += 1

    write_excluded_rows(excluded_path, excluded_rows)
    print(
        f"[OK] {run_name}: wrote {written} records to {valid_dir} "
        f"(excluded={len(excluded_rows)})"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="overwrite generated record JSON files under valid_evaluations/main_method_cross_model/",
    )
    parser.add_argument(
        "--runs",
        nargs="*",
        default=list(RUNS.keys()),
        choices=list(RUNS.keys()),
        help="judge versions to materialize",
    )
    parser.add_argument(
        "--output_root",
        type=Path,
        default=Path("reproducibility/04_results/03_processed_evaluations"),
        help="output directory for processed evaluation artifacts",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[3]
    reproducibility_root = project_root / "reproducibility"
    output_root = resolve_output_root(project_root, args.output_root)

    for run_name in args.runs:
        process_one_run(
            reproducibility_root=reproducibility_root,
            output_root=output_root,
            run_name=run_name,
            overwrite=args.overwrite,
        )


if __name__ == "__main__":
    main()
