#!/usr/bin/env python3
"""Summarize observed tool names and error outcomes from JSONL traces."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


TOOL_KEYS = {"tool", "tool_name", "function_name"}
ERROR_WORDS = re.compile(r"\b(error|failed|failure|denied|unauthorized|forbidden)\b", re.IGNORECASE)


def values(value: object, key: str = ""):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from values(child, str(child_key))
    elif isinstance(value, list):
        for child in value:
            yield from values(child, key)
    elif isinstance(value, str):
        yield key.lower(), value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traces", nargs="+", type=Path)
    args = parser.parse_args()
    tools: Counter[str] = Counter()
    error_tools: Counter[str] = Counter()
    invalid = records = 0
    sources = []
    try:
        for path in args.traces:
            sources.append({"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
            with path.open() as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        invalid += 1
                        continue
                    records += 1
                    found = []
                    strings = list(values(record))
                    for key, value in strings:
                        if (key in TOOL_KEYS or key == "name") and len(value) < 200 and re.match(r"^[\w.:-]+$", value):
                            found.append(value)
                            tools[value] += 1
                    if any(ERROR_WORDS.search(value) for _, value in strings):
                        for tool in set(found):
                            error_tools[tool] += 1
    except OSError as error:
        print(f"summarize_tool_use: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "sources": sources,
        "records": records,
        "invalid_lines": invalid,
        "observed_tools": [{"tool": name, "events": count, "error_records": error_tools[name]} for name, count in tools.most_common()],
        "warning": "Observed absence is not proof that a capability is unnecessary; validate trace coverage and exceptional workflows.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

