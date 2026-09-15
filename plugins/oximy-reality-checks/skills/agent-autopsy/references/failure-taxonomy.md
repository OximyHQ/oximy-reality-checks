# Failure taxonomy

Use the earliest supported category as primary. Later effects are contributing events or symptoms.

| Class | Observable test |
|---|---|
| Contract failure | Required target, constraint, or finish condition was missing or changed without reconciliation |
| Goal drift | Actions optimize a materially different objective from the active request |
| Assumption failure | A consequential belief lacks evidence or contradicts available evidence |
| Target failure | The action reaches the wrong file, account, tenant, branch, record, or environment |
| Tool-selection failure | A less suitable or unnecessarily privileged tool is chosen |
| Observation failure | Tool output contains a relevant signal that subsequent reasoning ignores or misreads |
| Loop failure | A retry repeats the same state without new evidence, parameter change, or hypothesis |
| Instruction conflict | Active instructions impose incompatible requirements that are not surfaced |
| Authorization failure | The agent acts beyond authority or stops despite an in-scope authorized path |
| Verification failure | Evidence is absent, stale, partial, or taken from the wrong system boundary |
| Handoff failure | Required context, state, identifiers, or unresolved work is lost between actors or sessions |

Do not diagnose intent or motivation. Diagnose observable decisions, actions, and state transitions.

