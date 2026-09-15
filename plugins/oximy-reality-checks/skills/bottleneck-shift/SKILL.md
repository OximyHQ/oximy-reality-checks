---
name: bottleneck-shift
description: Compare a workflow before and after AI assistance to determine whether work disappeared or moved into review, waiting, correction, exception handling, or rework. Use when someone asks whether AI improved an end-to-end process rather than one production step. Do not claim causal impact from an uncontrolled before-and-after comparison.
license: MIT
---

# Bottleneck Shift

Measure the whole path to accepted completion. Faster creation can coexist with a slower system.

## Boundary

- Compare a named workflow and accepted completion event, not generic activity totals.
- Keep descriptive change separate from causal attribution and financial impact.
- Do not rank individual workers or infer personal productivity from phase timing.

## Required inputs

- A named workflow with a stable start and accepted completion event.
- Work-item or cohort evidence from a pre-AI baseline and an AI-assisted period.
- Phase timestamps or credible duration estimates.
- Quality and exception signals relevant to the work.

If the workflow definition, population, or completion event changed, record the mismatch before comparing periods.

## Workflow

1. Define the work item, start, accepted completion, phases, exceptions, and quality guardrails. Exclude activity that does not advance an item toward acceptance.
2. Assess comparability: volume, mix, staffing, seasonality, policy, tooling, and measurement changes. Label controlled, adjusted, directional, or not comparable.
3. Run `scripts/analyze_events.py` on a normalized event CSV when available. Inspect anomalies and missing spans before interpreting aggregates.
4. Compare creation, queue, review, correction, exception, escalation, rework, and total elapsed time. Include completion rate and quality guardrails.
5. Identify the constraint in each period. A phase with the most elapsed time is not automatically the constraint; test whether it limits accepted throughput.
6. Trace displaced work: which upstream effort fell, which downstream effort rose, and which role absorbed it.
7. Separate observation from explanation. Generate plausible mechanisms only after the measured changes are clear.
8. Recommend one operating change and its next measurement. Prefer a bounded experiment over a universal rollout conclusion.

Read [references/comparison-guide.md](references/comparison-guide.md) before comparing non-equivalent cohorts or reporting savings.

## Completion criterion

The unit of work and accepted completion event are fixed; both periods cover the same phase model or disclose differences; missing data and comparability limits are explicit; downstream review and rework are included; and any causal or savings language matches the study design.

## Output

1. Bottom line and evidence strength
2. Workflow and cohort definitions
3. Comparability assessment
4. Phase and throughput comparison
5. Quality, exception, and rework comparison
6. Work removed, work created, and role absorbing it
7. Candidate explanation, clearly labeled
8. Next operating change and measurement
