#!/usr/bin/env python3
"""Capture the public skills.sh leaderboard without copying skill content."""

from __future__ import annotations

import argparse
import csv
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


SKILL_PATH = re.compile(r"^/([^/]+/[^/]+)/([^/]+)$")


class LeaderboardParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current: dict | None = None
        self.depth = 0
        self.rows: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        href = values.get("href", "") or ""
        if tag == "a" and self.current is None and SKILL_PATH.match(href):
            self.current = {"href": href, "parts": []}
            self.depth = 1
        elif self.current is not None:
            self.depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.current is None:
            return
        self.depth -= 1
        if self.depth == 0:
            text = " ".join(" ".join(self.current["parts"]).split())
            match = SKILL_PATH.match(self.current["href"])
            if match:
                rank = re.match(r"^(\d+)\s", text)
                install = re.search(r"(\d+(?:\.\d+)?[KMB]?)$", text)
                self.rows.append(
                    {
                        "rank": rank.group(1) if rank else "",
                        "source": match.group(1),
                        "skill": match.group(2),
                        "installs_display": install.group(1) if install else "",
                        "url": f"https://skills.sh{self.current['href']}",
                    }
                )
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.current is not None and data.strip():
            self.current["parts"].append(data.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--output", type=Path, default=Path("research/leaderboard.csv"))
    args = parser.parse_args()
    request = urllib.request.Request("https://www.skills.sh/", headers={"User-Agent": "oximy-skill-study/0.1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")
    collector = LeaderboardParser()
    collector.feed(html)
    seen: set[tuple[str, str]] = set()
    rows = []
    for row in collector.rows:
        key = (row["source"], row["skill"])
        if key in seen or not row["rank"]:
            continue
        seen.add(key)
        rows.append(row)
        if len(rows) >= args.limit:
            break
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("rank", "source", "skill", "installs_display", "url"))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} leaderboard entries to {args.output}")
    return 0 if len(rows) >= min(args.limit, 100) else 1


if __name__ == "__main__":
    raise SystemExit(main())

