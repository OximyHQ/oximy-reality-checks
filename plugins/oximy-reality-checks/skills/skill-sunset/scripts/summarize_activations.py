#!/usr/bin/env python3
"""Summarize structured skill activation evidence from CSV."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


TRUE = {"1", "true", "yes", "y"}
FALSE = {"0", "false", "no", "n"}


def boolean(value: str, field: str, row: int) -> bool:
    normalized = value.strip().lower()
    if normalized in TRUE:
        return True
    if normalized in FALSE:
        return False
    raise ValueError(f"row {row}: {field} must be true or false")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    args = parser.parse_args()
    required = {"skill", "expected", "activated", "outcome"}
    summary: dict[str, Counter] = defaultdict(Counter)
    rows = 0
    try:
        with args.csv_file.open(newline="") as handle:
            reader = csv.DictReader(handle)
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"missing columns: {sorted(missing)}")
            for number, row in enumerate(reader, 2):
                expected = boolean(row["expected"], "expected", number)
                activated = boolean(row["activated"], "activated", number)
                key = "true_activation" if expected and activated else "missed_activation" if expected else "false_activation" if activated else "true_non_activation"
                summary[row["skill"]][key] += 1
                summary[row["skill"]][f"outcome:{row['outcome'].strip() or 'unknown'}"] += 1
                rows += 1
    except (OSError, ValueError) as error:
        print(f"summarize_activations: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "source": str(args.csv_file.resolve()),
        "rows": rows,
        "skills": {skill: dict(counts) for skill, counts in sorted(summary.items())},
        "warning": "Routing counts do not establish why a skill activated or whether its output caused the outcome.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

