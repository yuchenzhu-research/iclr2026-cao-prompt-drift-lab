#!/usr/bin/env python3
"""
Schema checker (analysis-level only) for Prompt Drift Lab.

SCOPE
-----
This module validates whether model outputs conform to a *declared output schema*
using deterministic, transparent rules.

It does NOT execute any model inference and does NOT attempt semantic understanding
beyond explicit structural constraints.

NOTES (artifact boundary)
------------------------
This tool operates on observed outputs/text and does not depend on how any CSV
tables are produced. It is safe under the "CSV → Figures" reproducibility boundary.
"""

from __future__ import annotations

from typing import Dict, List, Any
import json
import hashlib
import re


TOOL_NAME = "schema_checker"
__version__ = "0.2.0"


# -----------------------------
# Schema definition
# -----------------------------

DEFAULT_SCHEMA = {
    "required_sections": [],        # e.g., ["## Answer", "## Reasoning"]
    "forbidden_sections": [],       # e.g., ["## Analysis"]
    "ordered_sections": [],         # e.g., ["## Step 1", "## Step 2"]
    "max_sections": None,           # e.g., 3 (counts '## ' headings)
    "allow_extra_text": True,       # strict mode if False
}


# -----------------------------
# Internal helpers
# -----------------------------

_CODE_FENCE_RE = re.compile(r"(?ms)^```.*?$.*?^``` *$", re.MULTILINE)
_H2_HEADING_RE = re.compile(r"(?m)^##\s+.*$")


def _strip_code_fences(text: str) -> str:
    """Remove fenced code blocks so headings inside code don't affect counts/logic."""
    return re.sub(_CODE_FENCE_RE, "", text)


def _extract_h2_headings_lines(text: str) -> List[str]:
    """
    Return a list of '## ...' heading lines (exact lines) at line-start.
    Code-fence content is ignored.
    """
    t = _strip_code_fences(text)
    return _H2_HEADING_RE.findall(t)


# -----------------------------
# Core validation functions
# -----------------------------

def check_required_sections(text: str, required: List[str]) -> Dict:
    missing = [s for s in required if s not in text]
    return {
        "rule": "required_sections",
        "missing": missing,
        "triggered": len(missing) > 0,
    }


def check_forbidden_sections(text: str, forbidden: List[str]) -> Dict:
    present = [s for s in forbidden if s in text]
    return {
        "rule": "forbidden_sections",
        "present": present,
        "triggered": len(present) > 0,
    }


def check_section_order(text: str, ordered: List[str]) -> Dict:
    positions = []
    for s in ordered:
        idx = text.find(s)
        positions.append(idx)

    out_of_order = False
    if all(p >= 0 for p in positions):
        out_of_order = positions != sorted(positions)

    return {
        "rule": "ordered_sections",
        "positions": dict(zip(ordered, positions)),
        "triggered": out_of_order,
    }


def check_max_sections(text: str, max_sections: int) -> Dict:
    # More robust than text.count("## "): only counts H2 headings at line-start,
    # and ignores code fences.
    headings = _extract_h2_headings_lines(text)
    section_count = len(headings)
    return {
        "rule": "max_sections",
        "count": section_count,
        "max_allowed": max_sections,
        "triggered": section_count > max_sections,
    }


def check_extra_text(text: str, schema: Dict[str, Any]) -> Dict:
    """
    Strict-mode extra-text policy (only when allow_extra_text == False):

    We treat the output as valid ONLY IF:
      1) There is no non-whitespace text before the first '## ' heading.
      2) Every '## ' heading line belongs to the allowed set:
           allowed = required_sections ∪ ordered_sections
      3) (Optional) forbidden_sections handled elsewhere.

    This avoids the previous incorrect behavior of deleting only markers and
    checking remaining text (which would almost always flag extra content).
    """
    if schema.get("allow_extra_text", True):
        return {"rule": "extra_text", "triggered": False}

    allowed_markers = set(schema.get("required_sections", [])) | set(schema.get("ordered_sections", []))

    # If no allowed markers were declared, strict mode is ill-defined;
    # interpret as "no text allowed".
    if not allowed_markers:
        has_any = len(text.strip()) > 0
        return {
            "rule": "extra_text",
            "triggered": has_any,
            "reason": "strict mode with empty allowed sections",
        }

    # Work on code-fence-stripped version for heading checks
    t = _strip_code_fences(text)

    # 1) No text before first heading
    first_h2 = re.search(r"(?m)^##\s+", t)
    if first_h2:
        prefix = t[:first_h2.start()]
        has_prefix_text = len(prefix.strip()) > 0
    else:
        # No headings at all, but strict mode expects headings
        return {
            "rule": "extra_text",
            "triggered": True,
            "reason": "strict mode requires allowed section headings, but none were found",
        }

    # 2) All headings must be allowed
    headings = _extract_h2_headings_lines(text)
    disallowed = [h for h in headings if h not in allowed_markers]

    triggered = has_prefix_text or (len(disallowed) > 0)

    payload: Dict[str, Any] = {
        "rule": "extra_text",
        "triggered": triggered,
    }
    if triggered:
        payload.update({
            "has_text_before_first_section": has_prefix_text,
            "disallowed_headings": disallowed,
            "allowed_headings": sorted(allowed_markers),
        })
    return payload


# -----------------------------
# Aggregator
# -----------------------------

def validate_schema(text: str, schema: Dict[str, Any]) -> Dict:
    results = []

    results.append(check_required_sections(text, schema.get("required_sections", [])))
    results.append(check_forbidden_sections(text, schema.get("forbidden_sections", [])))

    if schema.get("ordered_sections"):
        results.append(check_section_order(text, schema.get("ordered_sections", [])))

    if schema.get("max_sections") is not None:
        results.append(check_max_sections(text, schema.get("max_sections")))

    results.append(check_extra_text(text, schema))

    triggered = [r for r in results if r.get("triggered")]

    return {
        "tool": TOOL_NAME,
        "version": __version__,
        "schema_valid": len(triggered) == 0,
        "violations": triggered,
        "details": results,
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
    example_text = "## Answer\n42\n## Reasoning\nBecause it is."  # mock output

    schema = {
        "required_sections": ["## Answer", "## Reasoning"],
        "forbidden_sections": ["## Analysis"],
        "ordered_sections": ["## Answer", "## Reasoning"],
        "max_sections": 2,
        "allow_extra_text": True,
    }

    report = {
        "output_hash": stable_hash(example_text),
        "schema_check": validate_schema(example_text, schema),
    }

    print(json.dumps(report, indent=2))