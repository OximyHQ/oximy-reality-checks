# Marketplace readiness

The packaging is ready for private installation, not public release.

## Included

- Portable `skills/<name>/SKILL.md` packages for skills-compatible agents
- Codex plugin manifest and repository marketplace catalog
- Claude plugin manifest and repository marketplace catalog
- Oximy artwork with provenance
- Deterministic repository checks, helper tests and behavior-oriented eval fixtures

## Private install checks

```sh
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
claude plugin validate --strict .
```

After the private GitHub repository exists, also test discovery from a clean temporary environment:

```sh
npx skills add OximyHQ/oximy-reality-checks --list
```

## Public release gates

- Approve the exact README, descriptions, artwork and screenshots that will be public.
- Select a public software/content license.
- Add a confirmed security contact, privacy URL and terms URL where a marketplace requires them.
- Run each skill against its eval set in every supported host and record results by host version.
- Check a clean install from the public repository.
- Submit to the Claude official marketplace only after the repository is public and approved.
- Verify the Skills.sh listing after public installation activity makes it discoverable.
- Announce only after durable marketplace readback confirms the listing.

No item in the public-release section is represented as completed by the presence of a manifest.

