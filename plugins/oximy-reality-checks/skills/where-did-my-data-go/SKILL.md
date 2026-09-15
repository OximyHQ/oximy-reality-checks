---
name: where-did-my-data-go
description: Reconstruct the data journey of a specific AI task from local traces, tool configuration, logs, and artifacts. Use when someone asks what an agent read, transmitted, processed, stored, remembered, displayed, or reported. Do not infer vendor retention or deletion from local traffic evidence alone.
---

# Where Did My Data Go?

Build a data lineage map for one bounded task or session. Keep observed movement separate from configured possibility and vendor-policy claims.

## Boundary

- Analyze the supplied or locally available evidence. Do not resend the sensitive content to test where it goes.
- Minimize excerpts. Prefer hashes, field names, record counts, endpoint hosts, and source-line references over reproducing content.
- Do not say `not stored` when the evidence establishes only no observed local write.
- A component being configured does not prove it was invoked. A tool call does not prove the remote system retained the payload.

## Workflow

1. Bound the journey by session, time window, task, user, and data item. Give the data item a neutral label.
2. Inventory evidence sources: transcript, tool calls, MCP configuration, environment, proxy logs, filesystem changes, memory writes, model/provider settings, and downstream artifacts.
3. Run `scripts/trace_inventory.py` on JSONL traces for a content-minimized event inventory. Inspect the source records for material events the generic parser cannot classify.
4. Build nodes for origin, local agent, model endpoint, MCP server, external service, local artifact, telemetry, cache, and memory. Add a hop only when evidence identifies both sides or mark an endpoint unknown.
5. Label each hop with exactly one lifecycle verb: `read`, `collect`, `transmit`, `process`, `cache`, `store`, `remember`, `display`, `report`, or `delete`.
6. Assign an evidence state: observed, configured, vendor-stated, inferred, contradicted, or unknown. Include timestamp and evidence pointer.
7. Test the lifecycle for gaps. Specifically ask what proves retention, deletion, training use, administrative access, geographic processing, logging, and downstream propagation. Usually several will remain unknown.
8. Produce the smallest risk-reduction actions tied to the observed route. Do not substitute a generic privacy checklist.

Read [references/evidence-model.md](references/evidence-model.md) before interpreting vendor statements or absence of events.

## Completion criterion

Every in-scope data source has an origin; every observed destination has an incoming hop; every hop has a lifecycle verb, evidence state, and pointer; configured paths are not presented as observed use; and retention, access, and deletion unknowns are explicit.

## Output

1. Plain-language journey summary
2. Mermaid or text flow map
3. Hop ledger
4. Storage and memory end states
5. Configured-but-unobserved paths
6. Unknowns and the evidence required to resolve them
7. Risk-reduction actions tied to specific hops
