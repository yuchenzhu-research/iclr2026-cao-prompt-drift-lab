#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DEPRECATED (kept for backward compatibility)

Use:
  python supplement/tools/ingest/materialize_records.py

This wrapper exists because earlier drafts referenced `reproduce_valid_evaluations.py`.
The ingest step is an OPTIONAL audit utility and does NOT generate summary CSV tables.

Reproducibility boundary for this submission:
- Authoritative evaluation tables are the shipped scores_long.csv files under:
  supplement/04_results/03_processed_evaluations/*/summary_tables/scores_long.csv
- Figures are reproducible from these shipped CSV tables.
- Regenerating scores_long.csv from raw bundles/records is out of scope for artifact reproduction.
"""

import sys
from pathlib import Path

# Ensure this directory is importable
sys.path.insert(0, str(Path(__file__).resolve().parent))

from materialize_records import main  # noqa: E402


if __name__ == "__main__":
    print(
        "[DEPRECATED] reproduce_valid_evaluations.py → use materialize_records.py instead.",
        file=sys.stderr,
    )
    main()
