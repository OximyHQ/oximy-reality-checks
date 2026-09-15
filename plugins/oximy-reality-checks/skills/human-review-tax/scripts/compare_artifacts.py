#!/usr/bin/env python3
"""Create a deterministic structural diff for text and Office Open XML files."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree


OOXML_PARTS = {
    ".docx": ("word/document.xml", "word/header", "word/footer", "word/comments.xml"),
    ".pptx": ("ppt/slides/slide", "ppt/notesSlides/notesSlide"),
    ".xlsx": ("xl/sharedStrings.xml", "xl/worksheets/sheet"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xml_text(data: bytes) -> str:
    root = ElementTree.fromstring(data)
    values = []
    for element in root.iter():
        if element.text and element.text.strip():
            values.append(element.text.strip())
    return "\n".join(values)


def extract(path: Path) -> str:
    if path.suffix.lower() not in OOXML_PARTS:
        if b"\x00" in path.read_bytes()[:4096]:
            raise ValueError(f"unsupported binary format: {path.suffix}")
        return path.read_text(errors="replace")
    prefixes = OOXML_PARTS[path.suffix.lower()]
    chunks = []
    with zipfile.ZipFile(path) as archive:
        for name in sorted(archive.namelist()):
            if name.endswith(".xml") and any(name == prefix or name.startswith(prefix) for prefix in prefixes):
                chunks.append(xml_text(archive.read(name)))
    return "\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--diff", type=Path, help="write a unified text diff")
    args = parser.parse_args()
    try:
        before = extract(args.before)
        after = extract(args.after)
    except (OSError, ValueError, zipfile.BadZipFile, ElementTree.ParseError) as error:
        print(f"compare_artifacts: {error}", file=sys.stderr)
        return 2
    before_lines, after_lines = before.splitlines(), after.splitlines()
    matcher = difflib.SequenceMatcher(a=before_lines, b=after_lines, autojunk=False)
    operations = {"equal": 0, "replace": 0, "delete": 0, "insert": 0}
    changed_before = changed_after = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        operations[tag] += 1
        if tag != "equal":
            changed_before += i2 - i1
            changed_after += j2 - j1
    report = {
        "before": {"path": str(args.before.resolve()), "sha256": sha(args.before), "lines": len(before_lines), "words": len(re.findall(r"\b\w+\b", before))},
        "after": {"path": str(args.after.resolve()), "sha256": sha(args.after), "lines": len(after_lines), "words": len(re.findall(r"\b\w+\b", after))},
        "sequence_similarity": round(matcher.ratio(), 6),
        "changed_lines_before": changed_before,
        "changed_lines_after": changed_after,
        "operation_blocks": operations,
        "interpretation_warning": "Structural change is not effort, quality, authorship, or causality.",
    }
    if args.diff:
        rendered = "\n".join(difflib.unified_diff(before_lines, after_lines, fromfile=str(args.before), tofile=str(args.after), lineterm="")) + "\n"
        args.diff.write_text(rendered)
        report["diff"] = str(args.diff.resolve())
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

