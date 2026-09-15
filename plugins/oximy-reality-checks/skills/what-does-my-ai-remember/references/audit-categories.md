# Memory audit categories

| Category | Evidence question | Typical action to propose |
|---|---|---|
| Useful | Is it current, sourced, correctly scoped, and demonstrably helpful? | Keep with expiry or review date |
| Stale | Has a time-sensitive fact outlived its source or project? | Refresh or expire |
| Sensitive | Would retrieval expose personal, customer, credential, legal, health, or financial data? | Narrow scope, redact, or delete |
| Unsupported | Is the entry a claim without traceable source or confirmation? | Add provenance or quarantine |
| Contradictory | Does another active entry make an incompatible claim? | Resolve with a source; do not silently choose |
| Duplicated | Do several entries encode the same fact with drift? | Merge while preserving provenance |
| Over-broad | Can more agents, users, or projects retrieve it than the task requires? | Narrow retrieval scope |
| Wrong-scope | Did project, tenant, person, or environment context cross a boundary? | Move or delete after impact review |
| Behavioral instruction | Does it change future agent conduct rather than store a fact? | Review authority and source before retaining |
| Unknown | Is content, source, scope, or influence unavailable? | Identify the readback needed |

Deletion has at least three separate questions: was the visible entry removed, can it still be retrieved, and does a backup or derived memory retain it? Report only what was verified.

