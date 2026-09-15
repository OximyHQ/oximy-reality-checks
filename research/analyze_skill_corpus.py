#!/usr/bin/env python3
"""Build a reproducible structural study of public Agent Skills.

The script uses the authenticated GitHub CLI already configured by the user.
It stores source text only in the gitignored cache and commits only URLs,
hashes, and structural measurements. It intentionally does not republish
other authors' instructions.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path


QUERIES = (
    'filename:SKILL.md',
    'filename:SKILL.md "When to use"',
    'filename:SKILL.md "Required Output"',
    'filename:SKILL.md "references/"',
    'filename:SKILL.md "completion"',
    'filename:SKILL.md "evidence"',
)

FIELDS = (
    "repository",
    "path",
    "url",
    "blob_sha",
    "content_sha256",
    "matched_queries",
    "bytes",
    "lines",
    "words",
    "frontmatter",
    "name",
    "description_chars",
    "headings",
    "numbered_steps",
    "has_when_to_use",
    "has_when_not_to_use",
    "has_workflow",
    "has_completion_criterion",
    "has_required_output",
    "has_progressive_disclosure",
    "has_scripts",
    "has_examples",
    "has_evidence_language",
    "has_unknown_state",
    "has_safety_boundary",
    "has_explicit_authorization",
    "has_machine_readable_output",
)


def gh_api(endpoint: str, fields: dict[str, str] | None = None) -> dict:
    command = ["gh", "api", "-X", "GET", endpoint]
    for key, value in (fields or {}).items():
        command.extend(["-f", f"{key}={value}"])
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def search(query: str, per_page: int, page: int = 1) -> list[dict]:
    return gh_api(
        "search/code",
        {"q": query, "per_page": str(per_page), "page": str(page)},
    ).get("items", [])


def fetch_blob(repository: str, sha: str) -> str:
    payload = gh_api(f"repos/{repository}/git/blobs/{sha}")
    if payload.get("encoding") != "base64":
        raise ValueError(f"unexpected encoding for {repository}@{sha}")
    return base64.b64decode(payload["content"]).decode("utf-8", errors="replace")


def frontmatter(text: str) -> tuple[bool, dict[str, str]]:
    if not text.startswith("---"):
        return False, {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return False, {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t", "-")):
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return True, values


def analyze(record: dict, text: str) -> dict[str, str | int | bool]:
    lower = text.lower()
    has_fm, metadata = frontmatter(text)
    headings = re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    numbered_steps = len(re.findall(r"^\s*\d+[.)]\s+", text, re.MULTILINE))
    description = metadata.get("description", "")
    return {
        "repository": record["repository"],
        "path": record["path"],
        "url": record["url"],
        "blob_sha": record["sha"],
        "content_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "matched_queries": " | ".join(sorted(record["queries"])),
        "bytes": len(text.encode()),
        "lines": len(text.splitlines()),
        "words": len(re.findall(r"\b\w+\b", text)),
        "frontmatter": has_fm,
        "name": metadata.get("name", ""),
        "description_chars": len(description),
        "headings": len(headings),
        "numbered_steps": numbered_steps,
        "has_when_to_use": bool(re.search(r"when to use|use when|trigger", lower)),
        "has_when_not_to_use": bool(re.search(r"when not to use|do not use|avoid when|out of scope", lower)),
        "has_workflow": "workflow" in lower or numbered_steps >= 3,
        "has_completion_criterion": bool(re.search(r"completion criter|definition of done|done when|stop condition", lower)),
        "has_required_output": bool(re.search(r"required output|output format|deliverable|artifact", lower)),
        "has_progressive_disclosure": bool(re.search(r"references/|read .*\.md|consult .*\.md", lower)),
        "has_scripts": bool(re.search(r"scripts/|python3? .*\.py|node .*\.(?:js|mjs|ts)", lower)),
        "has_examples": bool(re.search(r"example|sample", lower)),
        "has_evidence_language": bool(re.search(r"evidence|verify|verification|source attribution", lower)),
        "has_unknown_state": bool(re.search(r"unknown|unverifiable|insufficient evidence|not established", lower)),
        "has_safety_boundary": bool(re.search(r"read-only|non-destructive|destructive|sensitive|privacy|security", lower)),
        "has_explicit_authorization": bool(re.search(r"explicit (?:approval|authorization|consent)|ask (?:for )?(?:approval|confirmation)", lower)),
        "has_machine_readable_output": bool(re.search(r"json|jsonl|yaml|schema", lower)),
    }


def write_summary(rows: list[dict], output: Path, queries: tuple[str, ...]) -> None:
    numeric = ("bytes", "lines", "words", "description_chars", "headings", "numbered_steps")
    booleans = [field for field in FIELDS if field.startswith("has_") or field == "frontmatter"]
    totals = {field: sum(int(row[field]) for row in rows) for field in booleans}
    medians: dict[str, int] = {}
    for field in numeric:
        values = sorted(int(row[field]) for row in rows)
        medians[field] = values[len(values) // 2] if values else 0
    repos = Counter(row["repository"] for row in rows)
    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "method": "GitHub code search, deduplicated by content SHA-256",
        "queries": list(queries),
        "skills_analyzed": len(rows),
        "repositories": len(repos),
        "medians": medians,
        "feature_prevalence": {
            field: {"count": totals[field], "percent": round(100 * totals[field] / len(rows), 1)}
            for field in booleans
        },
        "largest_repository_samples": repos.most_common(20),
        "limitations": [
            "GitHub code search is relevance-ranked, not a random sample.",
            "The corpus measures written structure, not behavioral effectiveness.",
            "Repository stars and marketplace installs are analyzed separately.",
            "Forked or copied text is deduplicated by exact content hash only.",
        ],
    }
    output.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=int, default=400)
    parser.add_argument("--per-query", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path("research/corpus.csv"))
    parser.add_argument("--summary", type=Path, default=Path("research/corpus-summary.json"))
    parser.add_argument("--cache", type=Path, default=Path(".research-cache/skills"))
    args = parser.parse_args()

    candidates: dict[tuple[str, str], dict] = {}
    for query in QUERIES:
        print(f"searching: {query}", file=sys.stderr)
        try:
            items = search(query, args.per_query)
        except subprocess.CalledProcessError as error:
            print(f"search slice unavailable: {query}: {error.stderr.strip()}", file=sys.stderr)
            continue
        for item in items:
            repository = item["repository"]["full_name"]
            key = (repository, item["path"])
            current = candidates.setdefault(
                key,
                {
                    "repository": repository,
                    "path": item["path"],
                    "url": item["html_url"],
                    "sha": item["sha"],
                    "queries": set(),
                },
            )
            current["queries"].add(query)

    # Fill a large target without spending more semantic-search slices. GitHub
    # caps code search at 1,000 results, and later pages remain deterministic
    # for the query during one run.
    page = 2
    while len(candidates) < args.target * 2 and page <= 8:
        print(f"searching fallback page: {page}", file=sys.stderr)
        try:
            items = search(QUERIES[0], args.per_query, page=page)
        except subprocess.CalledProcessError as error:
            print(f"fallback page unavailable: {error.stderr.strip()}", file=sys.stderr)
            break
        for item in items:
            repository = item["repository"]["full_name"]
            key = (repository, item["path"])
            current = candidates.setdefault(
                key,
                {
                    "repository": repository,
                    "path": item["path"],
                    "url": item["html_url"],
                    "sha": item["sha"],
                    "queries": set(),
                },
            )
            current["queries"].add(f"{QUERIES[0]} page:{page}")
        page += 1

    ranked = sorted(
        candidates.values(),
        key=lambda item: (-len(item["queries"]), item["repository"], item["path"]),
    )
    args.cache.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    seen_hashes: set[str] = set()
    for index, record in enumerate(ranked, 1):
        if len(rows) >= args.target:
            break
        cache_file = args.cache / f"{record['sha']}.md"
        try:
            if cache_file.exists():
                text = cache_file.read_text(errors="replace")
            else:
                text = fetch_blob(record["repository"], record["sha"])
                cache_file.write_text(text)
        except (subprocess.CalledProcessError, ValueError) as error:
            print(f"skip {record['repository']}/{record['path']}: {error}", file=sys.stderr)
            continue
        digest = hashlib.sha256(text.encode()).hexdigest()
        if digest in seen_hashes:
            continue
        seen_hashes.add(digest)
        rows.append(analyze(record, text))
        if len(rows) % 50 == 0:
            print(f"analyzed {len(rows)} unique skills from {index} candidates", file=sys.stderr)

    if len(rows) < args.target:
        print(f"only found {len(rows)} unique skills; requested {args.target}", file=sys.stderr)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    write_summary(rows, args.summary, QUERIES)
    print(f"wrote {len(rows)} skills to {args.output}")
    return 0 if len(rows) >= min(args.target, 300) else 1


if __name__ == "__main__":
    raise SystemExit(main())
