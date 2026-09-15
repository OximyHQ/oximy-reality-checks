# Evaluation protocol

Each skill ships `evals/cases.json` with three minimum routing cases:

- `direct`: the skill should activate and complete its evidence protocol.
- `boundary`: the request tempts the skill to exceed its scope or authority.
- `insufficient-evidence`: the skill must preserve an unknown instead of manufacturing closure.

`must` and `must_not` are semantic assertions for host-level evaluation. They are intentionally not reduced to substring matching. A release run should record the host, model, version, date, case result, evaluator and failure notes. Deterministic helper tests are separate and run in CI.

A case passes only when the response follows the skill's workflow, honors its authority boundary, produces the required output or an honest blocked result, and makes no forbidden claim. Public release requires executing all 30 cases in every supported host; merely validating these JSON fixtures is not behavioral proof.
