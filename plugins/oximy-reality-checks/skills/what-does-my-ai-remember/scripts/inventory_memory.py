#!/usr/bin/env python3
"""Inventory explicit memory roots without printing memory contents."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


DEFAULT_EXTENSIONS = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".db", ".sqlite", ".sqlite3"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path, help="explicit files or narrow directories to inventory")
    parser.add_argument("--max-files", type=int, default=5000)
    args = parser.parse_args()
    files: list[dict] = []
    skipped: list[dict] = []
    seen: set[Path] = set()
    try:
        for supplied in args.roots:
            root = supplied.expanduser().resolve()
            if root == Path.home().resolve() or root == Path("/"):
                raise ValueError(f"refusing broad root: {root}")
            candidates = [root] if root.is_file() else root.rglob("*")
            for path in candidates:
                if len(files) >= args.max_files:
                    raise ValueError(f"file limit reached: {args.max_files}")
                if path.is_symlink() or not path.is_file():
                    continue
                resolved = path.resolve()
                if resolved in seen:
                    continue
                seen.add(resolved)
                if path.suffix.lower() not in DEFAULT_EXTENSIONS:
                    skipped.append({"path": str(path), "reason": "extension outside default memory set"})
                    continue
                raw = path.read_bytes()
                stat = path.stat()
                files.append({
                    "path": str(path),
                    "extension": path.suffix.lower(),
                    "bytes": stat.st_size,
                    "modified_at": stat.st_mtime,
                    "sha256": hashlib.sha256(raw).hexdigest(),
                })
    except (OSError, ValueError) as error:
        print(f"inventory_memory: {error}", file=sys.stderr)
        return 2
    print(json.dumps({
        "roots": [str(path.expanduser().resolve()) for path in args.roots],
        "files": files,
        "skipped_count": len(skipped),
        "content_included": False,
        "coverage_warning": "This inventories only the explicit accessible roots; it does not establish cloud-memory coverage or retrievability.",
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
