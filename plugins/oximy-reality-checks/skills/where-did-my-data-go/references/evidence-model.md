# Data-journey evidence model

## Lifecycle verbs

Use one verb per event. Split events when more than one applies.

- `read`: accessed from an existing source.
- `collect`: brought into the in-scope system.
- `transmit`: crossed a process, host, account, or organizational boundary.
- `process`: transformed or evaluated without established persistence.
- `cache`: retained temporarily for operational reuse.
- `store`: persisted beyond the immediate operation.
- `remember`: made available to future agent sessions as memory.
- `display`: rendered to a person or user-facing surface.
- `report`: included in analytics, monitoring, or aggregated output.
- `delete`: removal was directly observed and its scope identified.

## Evidence states

| State | Meaning |
|---|---|
| Observed | A trace, state read, or artifact directly records the event |
| Configured | The path is enabled but invocation was not observed |
| Vendor-stated | A cited policy or contract describes handling; runtime conformance was not independently observed |
| Inferred | Evidence supports the conclusion indirectly; state the inference |
| Contradicted | Fresh evidence conflicts with the claim or configuration |
| Unknown | The evidence needed to decide is unavailable |

Absence of an observed log entry is not evidence that an event did not happen unless the log's completeness for that event class is independently established.

