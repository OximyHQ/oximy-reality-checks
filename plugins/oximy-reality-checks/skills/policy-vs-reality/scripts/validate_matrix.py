#!/usr/bin/env python3
"""Validate a policy-vs-reality comparison matrix in CSV or JSON form."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


REQUIRED = {"policy_statement", "policy_source", "evidence_point", "status", "evidence", "gap"}
STATUSES = {"aligned", "configured-not-observed", "observed-not-documented", "contradictory", "exception", "ambiguous-policy", "unknown"}


def rows(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text())
        if not isinstance(value, list):
            raise ValueError("JSON root must be an array")
        return value
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path)
    args = parser.parse_args()
    errors = []
    try:
        data = rows(args.matrix)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"validate_matrix: {error}", file=sys.stderr)
        return 2
    if not data:
        errors.append("matrix must contain at least one row")
    for index, row in enumerate(data, 1):
        if not isinstance(row, dict):
            errors.append(f"row {index} must be an object")
            continue
        missing = [field for field in REQUIRED if field not in row]
        if missing:
            errors.append(f"row {index} missing fields: {sorted(missing)}")
            continue
        if row["status"] not in STATUSES:
            errors.append(f"row {index} invalid status: {row['status']}")
        if row["status"] == "aligned" and not str(row["evidence"]).strip():
            errors.append(f"row {index} is aligned without evidence")
        if row["status"] in {"unknown", "ambiguous-policy", "configured-not-observed"} and not str(row["gap"]).strip():
            errors.append(f"row {index} needs an explicit gap for status {row['status']}")
    print(json.dumps({"valid": not errors, "rows": len(data), "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

