#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Deprecated compatibility wrapper.

Canonical entry point:
  python reproducibility/tools/reproduce_valid_evaluations.py --from_raw
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


if __name__ == "__main__":
    root_script = Path(__file__).resolve().parents[1] / "reproduce_valid_evaluations.py"
    print(
        "[DEPRECATED] use reproducibility/tools/reproduce_valid_evaluations.py --from_raw",
        file=sys.stderr,
    )
    sys.argv = [str(root_script), "--from_raw", *sys.argv[1:]]
    runpy.run_path(str(root_script), run_name="__main__")
