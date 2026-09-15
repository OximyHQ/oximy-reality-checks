---
name: what-does-my-ai-remember
description: Audit persistent information an AI agent can reuse across sessions, including provenance, sensitivity, staleness, contradictions, scope, and deletion evidence. Use when someone asks what an assistant remembers about them or a project, or wants a memory cleanup plan. Do not delete or rewrite memories without explicit approval.
license: MIT
---

# What Does My AI Remember?

Treat memory as a user-visible data product, not an opaque convenience. Inspect only stores the user identifies or that are narrowly associated with the active agent or project.

## Boundary

- Inventory first. Do not delete, merge, correct, or re-scope memory during the audit.
- Do not recursively scan a home directory or broad workspace root. Resolve explicit memory locations or narrow known agent directories.
- Do not claim to cover cloud memory that is inaccessible from the current environment.
- A memory's text is not proof that its claim is true. Preserve its source and confidence separately.

## Workflow

1. Define the audit surface: agent, account or project, local and cloud stores, and cutoff date. Record inaccessible surfaces.
2. Run `scripts/inventory_memory.py` against each explicit root to collect paths, sizes, timestamps, and hashes without printing content.
3. Inspect the memory entries using the appropriate application or file tools. For each entry, record source, created and last-used dates when available, subject, scope, confidence, and whether a person confirmed it.
4. Classify the entry: useful, stale, sensitive, unsupported, contradictory, duplicated, over-broad, wrong-scope, behavioral instruction, or unknown.
5. Check influence. Identify which agents, projects, users, or workflows can retrieve the memory and whether that scope is observed, configured, inferred, or unknown.
6. Build a cleanup proposal. For each proposed delete, correction, merge, expiry, or scope change, state the expected benefit and what could break.
7. If the user later approves changes, make the smallest reversible change and verify the resulting store with a fresh readback. Approval to audit is not approval to alter memory.

Read [references/audit-categories.md](references/audit-categories.md) when handling behavioral instructions, sensitive memories, or contradictions.

## Completion criterion

Every discovered store is covered or explicitly inaccessible; every reviewed entry has provenance, scope, and a classification or unknown; proposed changes remain unapplied unless separately authorized; and deletion is never claimed without a post-change readback.

## Output

1. Coverage statement
2. Memory map by agent and scope
3. Findings ledger with evidence pointers
4. Contradictions and high-risk behavioral instructions
5. Cleanup proposal, ordered by impact and reversibility
6. Unavailable surfaces and unresolved questions
