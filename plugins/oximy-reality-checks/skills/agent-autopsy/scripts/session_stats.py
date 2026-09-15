#!/usr/bin/env python3
"""Extract content-minimized retry and failure signals from a JSONL session."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


FAILURE = re.compile(r"\b(error|failed|failure|denied|timeout|exception|unauthorized|forbidden)\b", re.IGNORECASE)
TOOL_KEYS = {"tool", "tool_name", "function_name"}


def flatten(value: object, key: str = ""):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from flatten(child, str(child_key))
    elif isinstance(value, list):
        for child in value:
            yield from flatten(child, key)
    elif isinstance(value, str):
        yield key.lower(), value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", type=Path)
    args = parser.parse_args()
    tool_sequence: list[dict] = []
    tools: Counter[str] = Counter()
    failures = invalid = records = 0
    repeated_adjacent = 0
    previous_tool = None
    try:
        raw = args.session.read_bytes()
        for line_number, line in enumerate(raw.decode("utf-8", errors="replace").splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
                continue
            records += 1
            pairs = list(flatten(record))
            record_failed = any(FAILURE.search(value) for _, value in pairs)
            failures += int(record_failed)
            names = [value for key, value in pairs if (key in TOOL_KEYS or key == "name") and re.match(r"^[\w.:-]{1,200}$", value)]
            for name in names:
                tools[name] += 1
                if name == previous_tool:
                    repeated_adjacent += 1
                previous_tool = name
                tool_sequence.append({"line": line_number, "tool": name, "failure_signal": record_failed})
    except OSError as error:
        print(f"session_stats: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "session": str(args.session.resolve()),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "records": records,
        "invalid_lines": invalid,
        "failure_signal_records": failures,
        "tool_counts": tools.most_common(),
        "adjacent_repeated_tool_calls": repeated_adjacent,
        "tool_timeline": tool_sequence,
        "content_included": False,
        "warning": "Counts identify investigation leads; they do not establish root cause or wasted work.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

