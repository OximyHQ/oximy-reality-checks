# Distribution plan

The collection should be distributed as a useful diagnostic instrument, not as a bundle of ten prompts. Lead with one painful question and let the collection provide depth.

## What is live

| Surface | Status | User action |
|---|---|---|
| [GitHub](https://github.com/OximyHQ/oximy-reality-checks) | Public source, MIT license, CI and CodeQL passing | Inspect, star, fork or install |
| [Skills.sh](https://skills.sh/OximyHQ/oximy-reality-checks) | All ten skill pages live | Browse and install with `npx skills add OximyHQ/oximy-reality-checks` |
| Oximy Claude marketplace | Clean installation verified | `claude plugin marketplace add OximyHQ/oximy-reality-checks` |
| Oximy Codex marketplace | Public manifest; portable skills install in Codex | `codex plugin marketplace add OximyHQ/oximy-reality-checks` |

## Highest-value submissions

### 1. OpenAI's universal Plugins Directory

Why: one approved public listing is discoverable in both ChatGPT and Codex. Skills-only plugins are eligible.

Submit: [OpenAI plugin submission portal](https://platform.openai.com/plugins)

Exact proposed listing:

- Name: `Oximy Reality Checks`
- Short description: `Verify what AI touched, changed, remembered, and actually completed.`
- Long description: `Ten local-first checks for consequential AI work. Trace where data moved, review what an agent can remember, compare AI drafts with accepted work, right-size agent access, diagnose failed runs, and verify claimed outcomes against durable systems of record. Every check separates evidence from inference, preserves unknowns, and ends with a visible completion criterion.`
- Category: `Productivity`
- Website: `https://github.com/OximyHQ/oximy-reality-checks`
- Support: `https://github.com/OximyHQ/oximy-reality-checks/issues`
- Privacy: `https://oximy.com/privacy`
- Terms: `https://oximy.com/terms`

OpenAI requires five positive and three negative review cases for a skills submission. Keep the exact cases and release notes in the approval packet rather than copying a review fixture into public marketing copy.

Do not describe the package as submitted, approved or published until the portal and directory independently show those states.

### 2. Anthropic's official plugin directory

Why: it is built into Claude Code and is also surfaced to Claude users. This is the highest-leverage reviewed listing.

Submit: [Claude plugin submission](https://platform.claude.com/plugins/submit)

Exact proposed listing:

- Name: `Oximy Reality Checks`
- Repository: `https://github.com/OximyHQ/oximy-reality-checks`
- Description: `Ten local-first checks that verify what AI work touched, changed, remembered, and actually completed.`
- Category: `Productivity`
- Primary use: `Audit AI-assisted work with explicit evidence, unknowns, and completion criteria.`

Do not describe this as accepted or listed until the official directory returns that state.

### 3. SkillMD

Why: cross-agent discovery, safety review and per-skill capability flags. Publish each check from its source folder as a pack so its deterministic helper, references and eval fixtures stay attached.

Submit: [SkillMD publishing documentation](https://skillmd.com/docs/cli)

All ten source folders pass the registry's strict lint at 100/100 and its pack publication dry-run. Because publication requires an account token, record each final submission receipt separately.

### 4. agentskill.sh

Why: GitHub import, daily synchronization, author verification, analytics and skillset bundling.

Submit: [agentskill.sh repository import](https://agentskill.sh/submit)

Import `OximyHQ/oximy-reality-checks`, connect the Oximy GitHub organization for ownership, and enable a push webhook only after reviewing the requested permissions.

### 5. ClawHub

Why: native discovery for OpenClaw users and visible scan status. Publish each skill independently so users can install only the check they need.

Guide: [ClawHub publishing quickstart](https://docs.openclaw.ai/clawhub/quickstart)

Use `clawhub skill publish --dry-run` on all ten folders first. The first public upload is a separate external publication and should preserve the repository URL and MIT license.

## Curated lists, after real usage

- [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) has strong reach but explicitly asks new projects to establish real community usage before submitting. Do not send a premature PR.
- Smaller security-aware or cross-agent awesome lists can be approached after independent users, issue history and stable releases exist.
- GitHub Topics already provide durable discovery. Keep `agent-skills`, `ai-agents`, `ai-safety`, `privacy` and `security`; avoid tag stuffing.

## Additional reviewed visibility

- [OpenAI Developer Showcase](https://developers.openai.com/showcase) can feature a concrete build story after the universal plugin submission is in review. Lead with a reproducible `did-it-land` example, not a general product pitch.
- GitHub Marketplace is not a fit for a standalone skill repository unless this becomes a GitHub App or Action. Do not manufacture a wrapper only to obtain a listing.

## The launch should feature three checks

Ten choices are useful after discovery but weak as a first message. Lead with:

1. **Did It Land?** The agent said it finished. What does the system of record say?
2. **Safe to Paste.** Preserve the task while removing data the task does not need.
3. **Agent Autopsy.** Find the first consequential divergence, not the final error.

Each launch artifact should show one real input shape, one product action, and one output fragment. Never use invented customer results.

## Visibility channels

| Channel | Useful artifact | Primary call to action |
|---|---|---|
| Oximy website | A focused `/reality-checks` page with the three flagship examples | Try one skill |
| LinkedIn | Founder post showing a completion claim beside durable readback | Open `did-it-land` |
| X | Three short demonstrations, one per flagship skill | Browse the collection |
| Show HN | Technical write-up: why completion criteria and unknown states matter in agent skills | Inspect the repository |
| Reddit | A complete worked example tailored to `r/ClaudeAI`, `r/codex`, or `r/AI_Agents` | Critique or test one check |
| Dev.to or Hashnode | Reproducible teardown of one agent failure using `agent-autopsy` | Install and reproduce |
| Practitioner outreach | Ask security, platform and AI-ops practitioners to test one relevant skill | File an eval report |

Do not cross-post identical launch copy. The evidence example should match the community's actual work.

## What to measure

- Repository-to-install conversion by source
- Installs by individual skill, not only collection installs
- First successful completed report
- Boundary failures and false activations reported by users
- Human corrections required after the skill runs
- Repeat usage and version retention

Stars, impressions and directory rank are discovery signals. They do not establish that a Reality Check improved an outcome.
