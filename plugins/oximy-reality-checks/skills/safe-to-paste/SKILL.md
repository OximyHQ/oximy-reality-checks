---
name: safe-to-paste
description: Inspect text or files before they are shared with an AI service, make a task-preserving redacted copy, and explain residual exposure. Use when someone asks whether material is safe to paste or upload, or wants sensitive content sanitized for AI use. Do not treat the result as legal approval or a guarantee of vendor handling.
---

# Safe to Paste

Perform a local data-minimization review. The goal is not to make the source anonymous at any cost; it is to preserve the minimum information the requested AI task genuinely needs.

## Boundary

- Do not upload, paste, transmit, or quote the user's material into an external service as part of the review.
- Never modify the source file. Write a sibling copy only when the user asks for one.
- Treat scanner output as candidate detection. Names, trade secrets, privilege, and identifying combinations require semantic review.
- A vendor policy, enterprise contract, destination model, and retention setting can change the decision. If the destination is unknown, record it as unknown instead of inventing a policy.

## Workflow

1. Establish the intended AI destination and task. Record each as supplied, observed, or unknown. Do not block a local inspection when either is unknown.
2. Inspect the visible content and format-specific hidden surfaces. For office files, include metadata, comments, tracked changes, hidden sheets, speaker notes, and embedded filenames when the available document tools support them.
3. Build a sensitivity ledger. Account for credentials, direct identifiers, quasi-identifiers, customer or employer confidential material, regulated data, privileged material, and instructions that reveal protected business processes.
4. Decide what the task needs. For every sensitive element, choose keep, generalize, tokenize, remove, or escalate for human judgment. Consistent tokens such as `[CUSTOMER_1]` should preserve relationships without preserving identity.
5. If a redacted copy was requested, create it locally and run the deterministic scanner in `scripts/redact_text.py` against the copy. Do not claim that a clean scan proves anonymity.
6. Report residual risk and the evidence gaps that prevent a stronger conclusion. If the destination's handling terms matter, identify the exact term the user must verify rather than making a broad vendor claim.

Read [references/review-guide.md](references/review-guide.md) when classifying sensitive material or reviewing a non-plain-text file.

## Completion criterion

The review is complete only when the destination and task are recorded; every detected sensitive element has a disposition; the source remains unchanged; any redacted copy has been re-scanned; and residual risks and unknowns are explicit.

## Output

Return:

1. `Decision`: safe for the stated task, safe after listed changes, needs human approval, or insufficient evidence.
2. `Destination and task`: including unknowns.
3. `Sensitivity ledger`: item, location, category, disposition, reason.
4. `Redacted artifact`: path, if created.
5. `Residual risk`: what could still identify, expose, or mislead.
6. `Evidence limits`: what this review did not establish.
