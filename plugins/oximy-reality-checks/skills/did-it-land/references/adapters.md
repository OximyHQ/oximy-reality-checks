# Systems of record

Choose the evidence source that owns the claimed state.

| Claim | Strong readback | Common false proof |
|---|---|---|
| File created | Read the resolved path and inspect contents | Agent printed a path |
| Code committed | `git show` at the named SHA | Working-tree diff exists |
| Pull request ready | PR head SHA, checks, review state, mergeability | Local tests passed |
| Merged | Target branch contains the commit | PR was opened or approved |
| Deployed | Provider deployment for the exact revision | Merge completed |
| Working in production | Direct production readback or bounded live check | Deployment is green |
| Email sent | Message present in Sent with message ID and recipients | Draft or queued API response |
| Calendar changed | Fresh event read with ID, participants, and status | Local calendar payload built |
| CRM updated | Fresh record read with target ID and field values | Mutation returned HTTP 200 |
| Ticket completed | Tracker state plus required linked artifacts | Agent said issue is done |

For nested API responses, inspect the application payload. `200 OK`, `success: true`, and the desired resulting state are three different assertions.

