#!/usr/bin/env python3
"""
Rubric scorer (analysis-level only) for Prompt Drift Lab.

POSITIONING
-----------
This module maps *detected failures* (schema violations and drift signals)
into **rubric-aligned scores** using transparent, deterministic rules.

It does NOT judge model quality holistically and does NOT perform model inference.
It only scores *observed outputs* based on a fixed rubric.

NOTES (artifact boundary)
------------------------
This tool consumes detected failure labels. It does not depend on how scores_long.csv
is generated, and is compatible with the "CSV → Figures" reproducibility boundary.
"""

from __future__ import annotations

from typing import Dict, List
import json
import hashlib


TOOL_NAME = "rubric_scorer"
__version__ = "0.2.0"


# -----------------------------
# Rubric definition (fixed)
# -----------------------------

DEFAULT_RUBRIC = {
    "schema_compliance": {
        "max_score": 2,
        "penalties": {
            "schema_violation": 2,
        },
    },
    "instruction_following": {
        "max_score": 3,
        "penalties": {
            "instruction_deviation": 2,
            "extraneous_content": 1,
        },
    },
    "semantic_fidelity": {
        "max_score": 3,
        "penalties": {
            "semantic_drift": 2,
        },
    },
}

# Optional, documentation-only: how this 3-dim rubric can relate to other taxonomies (e.g., A–E)
# This does NOT affect scoring; it is included to reduce reviewer confusion.
DIMENSION_ALIASES = {
    "schema_compliance": ["A_structure", "B_snapshot_constraint"],
    "instruction_following": ["C_actionability", "D_completeness"],
    "semantic_fidelity": ["E_drift_failure"],
}


# -----------------------------
# Core scoring logic
# -----------------------------

def score_dimension(detected_failures: List[str], dimension_cfg: Dict) -> Dict:
    """Score a single rubric dimension given detected failure types."""
    score = dimension_cfg["max_score"]
    applied_penalties = []

    for failure, penalty in dimension_cfg.get("penalties", {}).items():
        if failure in detected_failures:
            score -= penalty
            applied_penalties.append({"failure": failure, "penalty": penalty})

    score = max(score, 0)

    return {
        "score": score,
        "max_score": dimension_cfg["max_score"],
        "penalties": applied_penalties,
    }


def score_output(detected_failures: List[str], rubric: Dict = DEFAULT_RUBRIC) -> Dict:
    """
    Map detected failure types to rubric-aligned scores.

    Returns stable totals + normalized score, plus tool metadata and rubric hash for auditability.
    """
    dimension_scores: Dict[str, Dict] = {}
    total_score = 0
    total_max = 0

    for dim, cfg in rubric.items():
        dim_result = score_dimension(detected_failures, cfg)
        dimension_scores[dim] = dim_result
        total_score += dim_result["score"]
        total_max += dim_result["max_score"]

    normalized = round(total_score / total_max, 3) if total_max > 0 else 0.0

    return {
        "tool": TOOL_NAME,
        "version": __version__,
        "rubric_hash": stable_hash(json.dumps(rubric, sort_keys=True)),
        "dimension_scores": dimension_scores,
        "total_score": total_score,
        "total_max": total_max,
        "normalized_score": normalized,
        "dimension_aliases": DIMENSION_ALIASES,  # documentation-only; safe to ignore downstream
    }


# -----------------------------
# Utility
# -----------------------------

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# -----------------------------
# Example usage
# -----------------------------

if __name__ == "__main__":
    failures = ["schema_violation", "semantic_drift"]

    report = {
        "output_hash": stable_hash("example output"),
        "rubric_score": score_output(failures),
    }

    print(json.dumps(report, indent=2))