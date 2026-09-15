# The Reality Check standard

A Reality Check resolves one consequential uncertainty about AI-assisted work. It is an investigation protocol, not a persona, prompt collection or general-purpose consultant.

## Required anatomy

Every skill must include:

1. A frontmatter description that says what it does, when it should activate, and a meaningful non-goal.
2. A boundary that limits scope, authority and interpretation.
3. A numbered workflow with observable inputs and decisions.
4. Evidence labels: `supplied`, `observed`, `inferred` and `unknown`, or a more specific compatible model.
5. A required output that a reviewer can inspect.
6. A completion criterion that prevents premature success claims.
7. At least three eval cases: direct use, tempting misuse, and insufficient evidence.
8. A local deterministic helper when computation or validation would otherwise be improvised.

## Writing rules

- Begin with the user decision, not a description of AI.
- Use concrete nouns: artifact, request, tool call, endpoint, merged change, resolved case, accepted draft.
- Make unknown a legitimate result.
- State what each measurement does not prove.
- Prefer short imperative steps over essays.
- Keep detailed taxonomies in `references/`; keep the controlling workflow in `SKILL.md`.
- Never use popularity, confidence-sounding prose or a clean scan as a substitute for evidence.

## Evidence rules

- An agent statement is a claim until read back from the true system of record.
- Configuration proves availability, not use. A trace can show an observed event, not every unobserved event.
- Structural change is not effort, quality, authorship or causality.
- Collection, transmission, storage, retrieval and reporting are separate lifecycle events.
- Before-and-after comparisons are descriptive until comparability and alternative explanations are addressed.

## Authority rules

The default operation is read-only. A skill may create a local report or a new sanitized copy when requested. It must not send, publish, delete, revoke, rotate, deploy or change external configuration unless the user explicitly authorizes that exact action.

## Review gate

A release reviewer should be able to answer:

- What exact user sentence activates this skill?
- What similar request must not activate it?
- Which artifact establishes completion?
- Where can it produce a false positive?
- Which unknowns survive a successful run?
- Can its mechanical assertions be reproduced?

If any answer is vague, the skill is not ready.

