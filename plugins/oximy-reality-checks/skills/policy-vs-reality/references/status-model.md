# Policy comparison status model

Assign one primary status to each atomic statement.

- `aligned`: fresh configuration or runtime evidence directly supports the statement.
- `configured-not-observed`: a control is configured, but runtime operation was not established.
- `observed-not-documented`: practice exists but the in-scope policy does not describe it.
- `contradictory`: fresh evidence conflicts with the policy statement.
- `exception`: a documented, in-scope exception explains the difference.
- `ambiguous-policy`: the statement cannot be mapped to one testable requirement.
- `unknown`: the required evidence is unavailable or incomplete.

Mismatch classes describe the system, not a person's intent:

- policy defect
- documentation lag
- control gap
- implementation drift
- exception-management gap
- evidence gap

Use `aligned` only for the lifecycle stage and scope the evidence covers. For example, transmission controls do not establish deletion, and tenant configuration does not establish every endpoint state.

