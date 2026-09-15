# Marketplace distribution

The public repository is the source for portable skill installation and the self-hosted Oximy Codex and Claude marketplaces. An official curated listing is a separate state.

## Included

- Portable `skills/<name>/SKILL.md` packages for skills-compatible agents
- Codex plugin manifest and repository marketplace catalog
- Claude plugin manifest and repository marketplace catalog
- Oximy artwork with provenance
- Deterministic repository checks, helper tests and behavior-oriented eval fixtures

## Install checks

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
claude plugin validate --strict .
```

Test discovery from a clean temporary environment:

```sh
npx skills add OximyHQ/oximy-reality-checks --list
```

## Distribution states

| Channel | State established by this repository | Stronger state still requiring readback |
|---|---|---|
| Skills-compatible agents | Public source, clean installation, and ten live Skills.sh pages verified 2026-09-15 | Skills.sh security-audit ingestion |
| Codex | Public Oximy marketplace manifest and portable-skill installation through the Skills CLI | Clean plugin installation in a separate Codex configuration |
| Claude Code | Public Oximy marketplace manifest and clean isolated installation verified 2026-09-15 | Official Anthropic marketplace submission and approval |

Before claiming a stronger state:

- Run each skill against its eval set in every supported host and record results by host version.
- Check a clean install from the public repository.
- Submit official-review forms only with their exact final answers recorded.
- Verify the catalog or marketplace directly after submission and again after approval.
- Announce only after durable marketplace readback confirms the listing.

The presence of a manifest proves packaging, not discovery, installation, review or approval.

## Live links

- [GitHub repository](https://github.com/OximyHQ/oximy-reality-checks)
- [Skills.sh collection](https://skills.sh/OximyHQ/oximy-reality-checks)
- [Anthropic official marketplace submission](https://platform.claude.com/plugins/submit), not yet submitted
