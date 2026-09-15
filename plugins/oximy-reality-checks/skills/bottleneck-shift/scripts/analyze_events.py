#!/usr/bin/env python3
"""Compare workflow phase durations from normalized before/after event CSV data."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


REQUIRED = {"item_id", "cohort", "phase", "started_at", "ended_at"}


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def describe(values: list[float]) -> dict:
    ordered = sorted(values)
    return {
        "count": len(ordered),
        "median_minutes": round(statistics.median(ordered), 3),
        "mean_minutes": round(statistics.fmean(ordered), 3),
        "p90_minutes": round(ordered[min(len(ordered) - 1, int(len(ordered) * 0.9))], 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path)
    args = parser.parse_args()
    durations: dict[tuple[str, str], list[float]] = defaultdict(list)
    items: dict[str, set[str]] = defaultdict(set)
    invalid: list[dict] = []
    try:
        with args.events.open(newline="") as handle:
            reader = csv.DictReader(handle)
            missing = REQUIRED - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"missing columns: {sorted(missing)}")
            for number, row in enumerate(reader, 2):
                try:
                    start, end = parse_time(row["started_at"]), parse_time(row["ended_at"])
                    minutes = (end - start).total_seconds() / 60
                    if minutes < 0:
                        raise ValueError("ended_at precedes started_at")
                    durations[(row["cohort"], row["phase"])].append(minutes)
                    items[row["cohort"]].add(row["item_id"])
                except ValueError as error:
                    invalid.append({"row": number, "reason": str(error)})
    except (OSError, ValueError) as error:
        print(f"analyze_events: {error}", file=sys.stderr)
        return 2
    report = defaultdict(dict)
    for (cohort, phase), values in sorted(durations.items()):
        report[cohort][phase] = describe(values)
    print(json.dumps({
        "source": str(args.events.resolve()),
        "items_by_cohort": {cohort: len(ids) for cohort, ids in sorted(items.items())},
        "phase_durations": report,
        "invalid_rows": invalid,
        "warning": "Before-and-after durations are descriptive; assess cohort comparability before attributing changes to AI.",
    }, indent=2))
    return 0 if not invalid else 1


if __name__ == "__main__":
    raise SystemExit(main())

