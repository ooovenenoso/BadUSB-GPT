# Security Policy

## Intended use

BadUSB-GPT is for authorized defensive security testing, lab demonstrations, and education. Do not use it against systems where you do not have explicit permission.

## Sensitive data handling

Payloads may collect basic Windows inventory and send it to an AI provider for report generation. Before running a payload:

- confirm the target system is in scope;
- review what the payload collects;
- confirm external AI processing is allowed by your policy;
- avoid committing generated reports if they contain private host details.

## API keys

Never embed API keys or provider endpoints in payload files. The maintained payloads read `BADUSB_GPT_API_KEY` / `BADUSB_GPT_BASE_URL` from the Windows user environment, with compatibility fallbacks for `OPENAI_API_KEY` / `OPENAI_BASE_URL`, and support model override through `BADUSB_GPT_MODEL` / `OPENAI_MODEL`.

## Reporting concerns

If you find a payload that embeds credentials, performs destructive actions, exfiltrates data outside the stated scope, or provides unsafe offensive guidance, open a private report to the maintainer or create a minimal public issue without secrets.
