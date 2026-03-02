#!/usr/bin/env python3
"""
Analysis-level drift analyzer for Prompt Drift Lab.

IMPORTANT SCOPE NOTE
--------------------
This script performs **post-hoc, deterministic analysis** on already-generated
LLM outputs. It does NOT run, call, or reproduce any model inference.

Given the same input files and configuration, the outputs of this script are
fully reproducible.
"""

from typing import Dict, List
import json
import hashlib

# -----------------------------
# Analysis metadata (fixed)
# -----------------------------
ANALYSIS_KIND = "derived_descriptive"  # machine-readable audit label
SCOPE_NOTE = "derived-only; descriptive; no causal claims; non-authoritative"


# -----------------------------
# Failure taxonomy (fixed)
# -----------------------------
FAILURE_TYPES = [
    "schema_violation",
    "instruction_deviation",
    "semantic_drift",
    "extraneous_content",
]


# -----------------------------
# Core analysis functions
# -----------------------------

def detect_schema_violation(text: str, required_markers: List[str]) -> Dict:
    """
    Check whether required structural markers are missing.
    This is a shallow, rule-based detector by design.
    """
    missing = [m for m in required_markers if m not in text]
    return {
        "type": "schema_violation",
        "missing_markers": missing,
        "triggered": len(missing) > 0,
    }


def detect_instruction_deviation(text: str, forbidden_phrases: List[str]) -> Dict:
    """
    Detect explicit violations of instruction constraints
    (e.g., adding steps, explanations, or sections that were disallowed).
    """
    found = [p for p in forbidden_phrases if p.lower() in text.lower()]
    return {
        "type": "instruction_deviation",
        "violated_constraints": found,
        "triggered": len(found) > 0,
    }


def detect_semantic_drift(text: str, anchor_terms: List[str]) -> Dict:
    """
    Approximate semantic drift by checking whether anchor terms
    (key concepts that must appear) are absent.

    This is NOT a semantic model; it is a conservative proxy.
    """
    missing = [t for t in anchor_terms if t.lower() not in text.lower()]
    confidence = round(len(missing) / max(len(anchor_terms), 1), 2)

    return {
        "type": "semantic_drift",
        "missing_anchor_terms": missing,
        "confidence": confidence,
        "triggered": confidence > 0.0,
    }


def detect_extraneous_content(text: str, max_length: int) -> Dict:
    """
    Flag outputs that significantly exceed expected length.
    Used as a proxy for verbosity drift or unsolicited content.
    """
    return {
        "type": "extraneous_content",
        "length": len(text),
        "max_expected": max_length,
        "triggered": len(text) > max_length,
    }


# -----------------------------
# Aggregator
# -----------------------------

def analyze_output(
    raw_output: str,
    required_markers: List[str],
    forbidden_phrases: List[str],
    anchor_terms: List[str],
    max_length: int,
) -> Dict:
    """
    Run all drift detectors on a single output.
    """
    results = []

    results.append(detect_schema_violation(raw_output, required_markers))
    results.append(detect_instruction_deviation(raw_output, forbidden_phrases))
    results.append(detect_semantic_drift(raw_output, anchor_terms))
    results.append(detect_extraneous_content(raw_output, max_length))

    triggered = [r for r in results if r.get("triggered")]

    return {
        "analysis_kind": ANALYSIS_KIND,
        "scope_note": SCOPE_NOTE,
        "total_failures": len(triggered),
        "failure_types": [r["type"] for r in triggered],
        "details": results,
    }


# -----------------------------
# Utility
# -----------------------------

def stable_hash(text: str) -> str:
    """
    Generate a stable hash for raw outputs to support auditability.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# -----------------------------
# Example CLI-style usage
# -----------------------------

if __name__ == "__main__":
    # Example only: this block documents intended usage
    example_output = "Example response without required sections."

    analysis = analyze_output(
        raw_output=example_output,
        required_markers=["## Result", "## Analysis"],
        forbidden_phrases=["step by step", "let's think"],
        anchor_terms=["prompt drift", "instruction following"],
        max_length=500,
    )

    report = {
        "output_hash": stable_hash(example_output),
        "analysis_kind": ANALYSIS_KIND,
        "scope_note": SCOPE_NOTE,
        "analysis": analysis,
    }

    print(json.dumps(report, indent=2))