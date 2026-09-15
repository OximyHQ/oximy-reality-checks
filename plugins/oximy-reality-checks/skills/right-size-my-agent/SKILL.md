---
name: right-size-my-agent
description: Compare an agent's configured capabilities with observed tool use and propose a least-privilege configuration for defined workflows. Use when someone wants to reduce agent permissions, MCP access, filesystem scope, network reach, or approval bypasses. Do not apply permission changes or infer safe denial from non-use alone.
license: MIT
---

# Right-Size My Agent

Derive a proposed permission envelope from actual work, then challenge it with the workflows the agent must still perform.

## Boundary

- Produce a reviewable proposal; do not change permissions, credentials or agent configuration.
- Treat configured capability, observed use and required capability as separate states.
- Do not remove access solely because it is absent from a limited trace window.

## Required inputs

- The agent and workflows being scoped.
- Current configuration or a reliable capability inventory.
- A representative trace window, including exceptional work when available.

If traces are not representative, produce an exposure map and evidence plan rather than a least-privilege recommendation.

## Workflow

1. Define the unit: one agent identity, environment, user or service account, and named workflow set. Do not aggregate identities with different authority.
2. Inventory configured capability across tools, MCP servers, commands, filesystem roots, network destinations, credentials, approval policies, and downstream service roles.
3. Run `scripts/summarize_tool_use.py` on available JSONL traces. Verify high-risk and ambiguous calls in the raw evidence.
4. Map each observed capability use to the workflow step it enabled. Label capability not observed, observed, or required-but-not-observed.
5. Identify privilege gaps: write when read sufficed, broad path when one directory sufficed, reusable credential when one-action authorization sufficed, owner-level role when a narrower resource role sufficed, or external communication when a draft-only action sufficed.
6. Propose the narrowest envelope that supports the named workflows. Include explicit approval gates and a break-glass path where removal would otherwise make legitimate exceptional work impossible.
7. Run counterexamples against historical and anticipated tasks. State which tasks the proposal would block.
8. Produce a reviewable patch or configuration diff, but do not apply it without explicit authorization. After any later application, rerun representative tasks and inspect denials.

Read [references/capability-model.md](references/capability-model.md) before combining permissions across tools or identities.

## Completion criterion

Every configured capability is accounted for; every retained high-risk capability maps to a named workflow or break-glass case; non-use is not treated as proof of safety to remove; counterexamples are recorded; and all proposed mutations remain unapplied unless separately approved.

## Output

1. Scope and trace coverage
2. Configured capability map
3. Observed use by workflow
4. Excess or ambiguous privilege findings
5. Proposed envelope and approval gates
6. Tasks that may break
7. Reviewable patch, if the format is known
8. Validation plan and evidence limits
