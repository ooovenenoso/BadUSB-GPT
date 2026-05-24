# Security Policy

## Intended use

BadUSB-GPT is for authorized defensive security testing, lab demonstrations, and education. Do not use it against systems where you do not have explicit permission.

## Sensitive data handling

Payloads may collect basic Windows inventory and send it to OpenAI for report generation. Before running a payload:

- confirm the target system is in scope;
- review what the payload collects;
- confirm external AI processing is allowed by your policy;
- avoid committing generated reports if they contain private host details.

## API keys

The public payloads are structurally hardcoded in the original plug-and-play style, but the committed API key value must remain the safe placeholder `PASTE_OPENAI_API_KEY_HERE`.

Before authorized lab use, replace that placeholder only in your private/local copy. Never commit a real API key, bearer token, private endpoint, or generated report with host-specific data.

## Reporting concerns

If you find a payload that embeds real credentials, performs destructive actions, exfiltrates data outside the stated scope, or provides unsafe offensive guidance, report it to the owner without including secrets.
