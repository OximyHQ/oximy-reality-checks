# Review guide

Use the narrowest category that explains the risk. One item may appear in more than one category when the combination matters.

| Category | Examples | Default treatment |
|---|---|---|
| Credential | API key, token, cookie, private key, password | Remove; rotate if exposure may already have occurred |
| Direct identifier | Email, phone, account number, employee ID | Tokenize or remove |
| Quasi-identifier | Rare job title, exact location, event date, small-team detail | Test whether the combination re-identifies a person or company |
| Confidential business data | Customer name, roadmap, pricing, unreleased result | Keep only with a confirmed permissible destination and task need |
| Regulated or privileged material | Health, finance, legal advice, authentication data | Escalate to the responsible human or policy owner |
| Protected process | Internal control, incident procedure, negotiation position | Generalize unless the task requires exact mechanics |

## Format surfaces

- Markdown and text: links, comments, fenced output, filenames, copied headers.
- CSV: hidden meaning in headers, rare row combinations, free-text cells.
- JSON and logs: tokens, request headers, URLs, IDs, nested payloads.
- DOCX: core properties, comments, tracked changes, headers, footers, relationships.
- XLSX: hidden sheets, formulas, names, comments, document properties.
- PPTX: speaker notes, comments, image metadata, hidden slides.
- PDF: metadata, annotations, embedded files, OCR text, redaction overlays that do not remove underlying text.

## Decision discipline

`Safe` is always conditional on the named destination, task, and version of the reviewed artifact. Prefer `safe after listed changes` when contractual or technical handling cannot be observed locally. Never equate absence of a pattern match with absence of sensitive meaning.

