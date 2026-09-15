---
name: human-review-tax
description: Compare an AI-produced artifact with the accepted final artifact and quantify the human correction and review it required. Use when someone asks whether AI saved work or shifted effort into editing, review, rework, or escalation. Do not infer time saved, authorship, or causality from a text diff alone.
license: MIT
---

# Human Review Tax

Measure the work between AI output and accepted output. A large diff is not automatically bad, and a small diff is not automatically correct.

## Boundary

- Analyze artifacts and workflow evidence, not individual reviewer performance.
- Do not infer effort, quality, authorship, savings or causality from diff size.
- Preserve both source artifacts; write derived reports or diffs to new files only.

## Required inputs

- The first AI-produced artifact or identifiable AI-assisted revision.
- The accepted final artifact, or the latest available revision clearly labeled as not yet accepted.
- The task and quality criteria used by the reviewer.

Optional evidence includes timestamps, comments, tracked changes, review rounds, ticket history, test failures, and the reviewer's own time estimate.

If the first AI artifact cannot be isolated, analyze the review process qualitatively and label attribution unknown.

## Workflow

1. Establish comparable versions. Record hashes, timestamps, formats, and acceptance status. Do not compare unrelated drafts merely because their filenames match.
2. Run `scripts/compare_artifacts.py` for a deterministic structural baseline. Its counts describe changed material, not effort or quality.
3. Review every material change and classify its primary reason: correctness, omission, unsupported claim, task misunderstanding, judgment, structure, style, policy or risk, formatting, or scope added after the AI draft.
4. Separate repair from preference. A reviewer choosing another valid style is not the same as fixing wrong work.
5. Reconstruct the review loop from available evidence: review rounds, elapsed time, active human time, blockers, reopens, and escalations. Keep reported time separate from inferred time.
6. Identify displaced work. Name the upstream effort AI reduced and the downstream work it created.
7. Recommend at most three changes tied to recurrent evidence: improve the task contract, constrain the AI step, add a verifier, change the handoff, or stop using AI for that part.

Read [references/classification.md](references/classification.md) before classifying changes in a high-stakes artifact.

## Completion criterion

Every material difference is classified or marked unresolved; repair is separated from preference and changed scope; time values identify their source; accepted status is explicit; and no statement of savings or causality exceeds the available evidence.

## Output

1. Net assessment in plain language
2. Artifact identity and comparison coverage
3. Review ledger by change category
4. Review loop: rounds, elapsed time, active time, and evidence source
5. Work removed versus work created
6. Repeated failure pattern, if the evidence supports one
7. Up to three workflow changes
8. Evidence limits
