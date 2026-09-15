#!/usr/bin/env python3
"""Detect and consistently tokenize common sensitive strings in text files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


MAX_BYTES = 20 * 1024 * 1024
PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,255}\b")),
    ("slack-token", re.compile(r"\bxox(?:b|p|a|r|s)-[A-Za-z0-9-]{10,200}\b")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")),
    ("generic-api-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,200}\b")),
    ("email", re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w-])", re.IGNORECASE)),
    ("ssn-us", re.compile(r"(?<!\d)(?!000|666|9\d\d)\d{3}[- ]?(?!00)\d{2}[- ]?(?!0000)\d{4}(?!\d)")),
    ("ipv4", re.compile(r"(?<!\d)(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?!\d)")),
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_text(path: Path) -> tuple[bytes, str]:
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError(f"file exceeds {MAX_BYTES} bytes")
    if b"\x00" in raw:
        raise ValueError("binary or office files require format-specific inspection")
    return raw, raw.decode("utf-8")


def redact(text: str) -> tuple[str, list[dict]]:
    tokens: dict[tuple[str, str], str] = {}
    counts: Counter[str] = Counter()
    lines: dict[str, set[int]] = defaultdict(set)
    result = text
    for category, pattern in PATTERNS:
        def replace(match: re.Match[str]) -> str:
            value = match.group(0)
            key = (category, value)
            if key not in tokens:
                tokens[key] = f"[{category.upper().replace('-', '_')}_{sum(1 for c, _ in tokens if c == category) + 1}]"
            counts[category] += 1
            lines[category].add(text.count("\n", 0, match.start()) + 1)
            return tokens[key]
        result = pattern.sub(replace, result)
    findings = [
        {"category": category, "count": counts[category], "lines": sorted(lines[category])}
        for category in sorted(counts)
    ]
    return result, findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, help="write a redacted copy; source overwrite is refused")
    parser.add_argument("--report", type=Path, help="write the JSON report instead of stdout")
    args = parser.parse_args()
    try:
        source_raw, source = load_text(args.input)
        transformed, findings = redact(source)
        report = {
            "source": str(args.input.resolve()),
            "source_sha256": digest(source_raw),
            "scanner_scope": [category for category, _ in PATTERNS],
            "findings": findings,
            "finding_count": sum(item["count"] for item in findings),
            "semantic_review_required": True,
        }
        if args.output:
            if args.output.resolve() == args.input.resolve():
                raise ValueError("refusing to overwrite source")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(transformed)
            report["output"] = str(args.output.resolve())
            report["output_sha256"] = digest(transformed.encode())
        rendered = json.dumps(report, indent=2) + "\n"
        if args.report:
            args.report.write_text(rendered)
        else:
            sys.stdout.write(rendered)
        return 0
    except (OSError, UnicodeDecodeError, ValueError) as error:
        print(f"redact_text: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
