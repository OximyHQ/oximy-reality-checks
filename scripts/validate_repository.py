#!/usr/bin/env python3
"""Validate the repository's ten-skill contract without third-party packages."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "oximy-reality-checks"
EXPECTED = {
    "agent-autopsy", "bottleneck-shift", "did-it-land", "human-review-tax",
    "policy-vs-reality", "right-size-my-agent", "safe-to-paste", "skill-sunset",
    "what-does-my-ai-remember", "where-did-my-data-go",
}


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return {}
    values = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def main() -> int:
    errors: list[str] = []
    skills_root = PLUGIN / "skills"
    skills = {path.name for path in skills_root.iterdir() if path.is_dir()}
    if skills != EXPECTED:
        errors.append(f"skill set mismatch: expected {sorted(EXPECTED)}, found {sorted(skills)}")

    for name in sorted(EXPECTED & skills):
        root = skills_root / name
        skill_file = root / "SKILL.md"
        if not skill_file.exists():
            errors.append(f"{name}: missing SKILL.md")
            continue
        text = skill_file.read_text()
        meta = frontmatter(text)
        if meta.get("name") != name:
            errors.append(f"{name}: frontmatter name mismatch")
        description = meta.get("description", "")
        if len(description) < 80 or "Use when" not in description or "Do not" not in description:
            errors.append(f"{name}: description needs purpose, Use when, and Do not routing guidance")
        for heading in ("## Boundary", "## Workflow", "## Completion criterion", "## Output"):
            if heading not in text:
                errors.append(f"{name}: missing {heading}")
        if re.search(r"\b(TODO|TBD|placeholder)\b", text, re.IGNORECASE):
            errors.append(f"{name}: contains unfinished marker")
        for link in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
            if "://" not in link and not (root / link).exists():
                errors.append(f"{name}: broken relative link {link}")
        scripts = list((root / "scripts").glob("*.py"))
        if len(scripts) != 1:
            errors.append(f"{name}: expected exactly one deterministic helper")
        for script in scripts:
            result = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True)
            if result.returncode:
                errors.append(f"{name}: helper --help failed: {result.stderr.strip()}")
        yaml_path = root / "agents" / "openai.yaml"
        if not yaml_path.exists():
            errors.append(f"{name}: missing agents/openai.yaml")
        else:
            yaml_text = yaml_path.read_text()
            if f"${name}" not in yaml_text or '#FF4D00' not in yaml_text:
                errors.append(f"{name}: openai.yaml needs skill prompt and Oximy color")
        cases_path = root / "evals" / "cases.json"
        if not cases_path.exists():
            errors.append(f"{name}: missing evals/cases.json")
        else:
            try:
                cases = json.loads(cases_path.read_text())
                kinds = {case.get("kind") for case in cases}
                if len(cases) < 3 or not {"direct", "boundary", "insufficient-evidence"} <= kinds:
                    errors.append(f"{name}: evals need direct, boundary, and insufficient-evidence cases")
            except (json.JSONDecodeError, AttributeError) as error:
                errors.append(f"{name}: invalid eval JSON: {error}")

    for manifest in (
        ROOT / ".agents/plugins/marketplace.json",
        ROOT / ".claude-plugin/marketplace.json",
        PLUGIN / ".codex-plugin/plugin.json",
        PLUGIN / ".claude-plugin/plugin.json",
    ):
        try:
            json.loads(manifest.read_text())
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"invalid manifest {manifest.relative_to(ROOT)}: {error}")

    for required in ("README.md", "AUTHORING.md", "PRIVACY.md", "SECURITY.md", "LICENSE.md"):
        if not (ROOT / required).exists():
            errors.append(f"missing {required}")

    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    print(json.dumps({"valid": True, "skills": len(skills), "contract_checks": "passed"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

