---
name: agent-autopsy
description: Reconstruct a completed, failed, expensive, or confusing agent session to find where its trajectory broke and what one change would prevent recurrence. Use when investigating post-hoc session diagnosis, tool-loop analysis, goal drift, premature completion, or repeated human rescue. Do not use as employee performance scoring.
---

# Agent Autopsy

Find the first consequential divergence, not merely the last visible error.

## Boundary

- Diagnose one bounded trajectory and preserve the source session unchanged.
- Do not score a person, infer intent, or convert tool counts into productivity.
- Do not implement proposed fixes unless the user separately asks for implementation.

## Workflow

1. Freeze the case. Record the session identifier, time range, original task, expected finish, and final observed state. Preserve the source transcript unchanged.
2. Run `scripts/session_stats.py` for a content-minimized timeline of tool calls, errors, repeated calls, and elapsed gaps. Treat statistics as leads, not diagnoses.
3. Reconstruct the trajectory as intent, decision, action, observation, and response. Include user corrections, permission denials, tool failures, context compaction, and handoffs.
4. Mark divergences: goal drift, assumption without evidence, wrong tool or target, ignored observation, retry without new information, instruction conflict, approval gap, premature completion, or verification at the wrong system boundary.
5. Identify the earliest point where a different decision would probably have changed the outcome. Distinguish triggering event, contributing conditions, and the final symptom.
6. Measure waste only from observable proxies: repeated tool calls, discarded artifacts, idle gaps, retries, review rounds, and reported cost. Do not convert tokens or elapsed time directly into productivity.
7. Propose at most three changes. Prefer one tighter task contract, one deterministic guard or verifier, and one instruction or permission change. Each proposal must cite the failure event it addresses.
8. Define a replay or fixture that would distinguish improvement from a cosmetically better explanation.

Read [references/failure-taxonomy.md](references/failure-taxonomy.md) when multiple failure classes overlap.

## Completion criterion

The original task and final state are explicit; the timeline accounts for every consequential branch; the first divergence is separated from the final symptom; each recommendation maps to evidence; and a repeatable check is defined for the highest-priority change.

## Output

1. One-paragraph finding
2. Case boundary and evidence coverage
3. Timeline of consequential events
4. First divergence, contributing conditions, and final symptom
5. Human interventions and recovery points
6. Observable waste
7. Up to three corrective changes
8. Replay plan and remaining unknowns
