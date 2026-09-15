---
name: did-it-land
description: Reconcile an AI agent's completion claims with durable evidence in the relevant system of record. Use when someone asks whether agent work actually finished, shipped, sent, changed, or reached production. Do not use a passing local check as proof of an unobserved remote or real-world state.
license: MIT
---

# Did It Land?

Treat the agent's narration as claims, not evidence. Verify the post-condition in the system that owns the state.

## Boundary

- Verification is read-only by default. Do not create, resend, redeploy, approve, or otherwise mutate state to make a check pass.
- Do not perform a risky live test without explicit authorization.
- Keep local, committed, reviewed, merged, deployed and production-observed states distinct.

## Workflow

1. Recover the contract. Identify the original request, target, acceptance criteria, exclusions, and any later user corrections. Mark criteria that were never defined.
2. Extract completion claims from the agent's messages and artifacts. Split compound statements so each row can receive one verdict.
3. Name the system of record for each claim. Examples: filesystem, git commit, GitHub check, deployment provider, production URL, sent mailbox, calendar event, CRM record, payment ledger, or issue tracker.
4. Select an independent readback. Prefer a fresh API read, command, or direct artifact inspection over the same agent's summary. Never create or mutate state merely to verify it.
5. Capture evidence with timestamp, target identity, source, and the smallest excerpt or result needed. Inspect success envelopes: transport success is not application success.
6. Assign exactly one verdict from the evidence model below. A chain may contain different verdicts, such as committed = verified, deployed = verified, production behavior = unknown.
7. State the next smallest check needed for every partial, failed, or unknown claim. Do not quietly perform a risky live test.

Read [references/adapters.md](references/adapters.md) for common systems of record. Validate a JSON result with `scripts/validate_outcome.py`.

## Verdicts

- `verified`: fresh evidence directly establishes the claimed post-condition.
- `partial`: some, but not all, of the claimed state is established.
- `failed`: fresh evidence contradicts the claim.
- `claimed-only`: the agent stated it, but no independent evidence was collected.
- `unknown`: the required system, authority, or observation is unavailable.
- `not-applicable`: the recovered contract does not require this claim.

Do not convert `claimed-only` or `unknown` into failure. Do not convert a created artifact into proof that it was accepted, sent, merged, deployed, or used.

## Completion criterion

The check is complete when every acceptance criterion and every material completion claim appears in the evidence ledger; each has a named system of record, verdict, and evidence or explicit evidence gap; and the overall status is no stronger than its weakest required criterion.

## Output

Lead with one sentence: what is verified, what is not, and whether required work remains. Then provide:

1. Contract recovered
2. Evidence ledger
3. State chain, when work crosses multiple systems
4. Missing checks and why they were not run
5. Overall status: verified complete, partially verified, failed, or not verifiable
