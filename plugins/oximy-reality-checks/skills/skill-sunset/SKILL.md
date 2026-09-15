---
name: skill-sunset
description: Decide whether an installed agent skill should be kept, narrowed, revised, merged, quarantined, or retired using real activation and outcome evidence. Use when skills are stale, conflicting, noisy, costly, unused, or suspected of worsening work. Do not delete or rewrite a skill without explicit approval.
---

# Skill Sunset

Evaluate the skill as a production dependency. Installation and popularity are not evidence that it improves this user's work.

## Boundary

- Inspect the exact installed version and preserve it during the review.
- Do not delete, disable, edit, publish or change marketplace state without separate authorization.
- Do not equate activation count, repository stars or marketplace installs with outcome quality.

## Workflow

1. Identify the exact skill version, source, installation scope, supported agents, and intended trigger. Hash the reviewed files.
2. Recover the skill's contract: what behavior it should change, when it should activate, when it should not, what artifact it should produce, and how completion is checked. Missing contract elements are findings, not assumptions.
3. Gather representative evidence: activation logs, sessions where it should and should not have fired, user corrections, outputs, review burden, tool calls, failures, and cost. Record coverage and selection bias.
4. Run `scripts/summarize_activations.py` when structured activation records exist. Inspect the source sessions for every high-impact result.
5. Evaluate routing: true activation, missed activation, false activation, and ambiguous activation. Separate discovery failure from execution failure.
6. Evaluate execution: contract compliance, outcome, consistency, added work, instruction conflicts, permission expansion, and whether a simpler instruction or deterministic script would do better.
7. Compare alternatives only when the tasks are comparable. Synthetic with-skill/without-skill evaluation may supplement production evidence but must not replace it.
8. Choose one disposition using [references/dispositions.md](references/dispositions.md). Tie it to evidence and state what new evidence would change the decision.
9. Produce a patch or migration plan for review. Do not alter installed skills, marketplace state, or dependent workflows without explicit authorization.

## Completion criterion

The exact version and intended contract are recorded; routing and execution are evaluated separately; representative evidence and its gaps are stated; the disposition is tied to observed behavior; dependent workflows are identified; and no mutation has occurred without separate approval.

## Output

1. Disposition and confidence
2. Skill identity and intended contract
3. Evidence coverage
4. Routing findings
5. Execution and outcome findings
6. Cost, review, and permission effects
7. Dependencies and migration risk
8. Proposed patch or retirement plan
9. Evidence that would reverse the recommendation
