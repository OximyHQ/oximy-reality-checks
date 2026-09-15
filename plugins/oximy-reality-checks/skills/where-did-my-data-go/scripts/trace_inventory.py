#!/usr/bin/env python3
"""Extract content-minimized endpoints, tools, and paths from JSONL traces."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse


URL = re.compile(r"https?://[^\s\"'<>]+")
PATH = re.compile(r"(?<![\w.-])(?:/[^\s\"'<>:]+){2,}")
TOOL_KEYS = {"tool", "tool_name", "name", "function_name"}
TIME_KEYS = ("timestamp", "created_at", "time", "ts")


def walk(value: object, key: str = ""):
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from walk(child, str(child_key))
    elif isinstance(value, list):
        for child in value:
            yield from walk(child, key)
    elif isinstance(value, str):
        yield key, value


def compact_path(value: str, show: bool) -> str:
    if show:
        return value
    return f"{Path(value).name}#{hashlib.sha256(value.encode()).hexdigest()[:10]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("--show-paths", action="store_true", help="include full local paths")
    args = parser.parse_args()
    tools: Counter[str] = Counter()
    hosts: Counter[str] = Counter()
    paths: Counter[str] = Counter()
    invalid = 0
    events = 0
    first_time = last_time = None
    try:
        with args.trace.open() as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    invalid += 1
                    continue
                events += 1
                if isinstance(record, dict):
                    times = [record.get(key) for key in TIME_KEYS if record.get(key)]
                    if times:
                        first_time = first_time or str(times[0])
                        last_time = str(times[0])
                for key, value in walk(record):
                    if key.lower() in TOOL_KEYS and len(value) < 200 and re.match(r"^[\w.:-]+$", value):
                        tools[value] += 1
                    for match in URL.findall(value):
                        host = urlparse(match.rstrip(".,);]")).hostname
                        if host:
                            hosts[host] += 1
                    for match in PATH.findall(value):
                        paths[compact_path(match.rstrip(".,);]"), args.show_paths)] += 1
    except OSError as error:
        print(f"trace_inventory: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "trace": str(args.trace.resolve()),
        "trace_sha256": hashlib.sha256(args.trace.read_bytes()).hexdigest(),
        "events": events,
        "invalid_lines": invalid,
        "first_timestamp": first_time,
        "last_timestamp": last_time,
        "tools": tools.most_common(),
        "endpoint_hosts": hosts.most_common(),
        "paths": paths.most_common(),
        "content_minimized": not args.show_paths,
        "warning": "Presence is evidence of a string in the trace, not proof of transmission, storage, or invocation.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

