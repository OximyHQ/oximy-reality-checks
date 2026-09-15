# Capability model

Represent capability as a tuple rather than a tool name:

`identity × operation × resource × scope × destination × time × approval`

For example, `GitHub` is not a permission. `release-bot can create pull requests in repository A during a release workflow after human approval` is.

## Review dimensions

- Identity: whose authority is used, and whether credentials are shared.
- Operation: read, propose, create, update, delete, execute, approve, or administer.
- Resource: exact repository, mailbox, calendar, dataset, host, path, or record class.
- Scope: one object, prefix, project, tenant, account, or global.
- Destination: where data or side effects can travel.
- Time: persistent, session-bound, expiring, or one action.
- Approval: none, user confirmation, role approval, policy gate, or break-glass.

Analyze aggregate capability. Two individually modest tools can combine into a high-risk path, such as private-data read plus unrestricted external send.

