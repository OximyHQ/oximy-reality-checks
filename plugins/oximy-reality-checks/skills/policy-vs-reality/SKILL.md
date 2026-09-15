---
name: policy-vs-reality
description: Compare written AI policy with observed agent configuration and runtime evidence, producing a non-accusatory mismatch ledger. Use when someone wants to test whether approved tools, data rules, permissions, retention, review gates, or prohibited actions match practice. Do not use individual activity as a proxy for intent or misconduct.
license: MIT
---

# Policy vs Reality

Test policy statements at the enforcement point they imply. A document can be current while implementation is missing; configuration can be compliant while runtime conformance remains unobserved.

## Boundary

- Default to system, workflow, or cohort evidence. Name individuals only when the user explicitly requires it and the evidence and policy authorize that use.
- Do not characterize a mismatch as misconduct. It may be policy ambiguity, stale documentation, configuration drift, an approved exception, or incomplete evidence.
- Do not change policy, configuration, permissions, or records during the comparison.

## Workflow

1. Establish scope: policy version, effective date, covered population, environments, workflows, and observation window.
2. Decompose the policy into atomic, testable statements. Separate requirements, prohibitions, approvals, exceptions, and aspirations.
3. For each statement, name its expected enforcement or evidence point: identity provider, model gateway, endpoint, device policy, agent configuration, tool permission, log, review system, retention control, or human procedure.
4. Inventory configuration and runtime evidence. Run `scripts/validate_matrix.py` after constructing the structured comparison matrix.
5. Assign one status per statement: aligned, configured-not-observed, observed-not-documented, contradictory, exception, ambiguous-policy, or unknown.
6. Distinguish collection, transmission, processing, storage, memory, display, reporting, and deletion. A control covering one does not silently cover the others.
7. Determine the likely mismatch class without assigning blame: policy defect, documentation lag, control gap, implementation drift, exception-management gap, or evidence gap.
8. Prioritize remediation by plausible harm, breadth, reversibility, and evidence strength. State the owner role and verification readback, not a person's name unless supplied.

Read [references/status-model.md](references/status-model.md) before finalizing the matrix.

## Completion criterion

Every in-scope policy statement is atomic and mapped to an evidence or enforcement point; every row has one status and an evidence pointer or explicit gap; lifecycle stages are not conflated; exceptions remain distinct from contradictions; and the output contains no unsupported allegation about individual behavior.

## Output

1. Scope and policy identity
2. Coverage and evidence limitations
3. Policy-to-reality matrix
4. Mismatches by class, not by person
5. Approved or unresolved exceptions
6. Prioritized remediation with owner role
7. Verification plan
