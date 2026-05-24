# Owner Confirmation Guide

This guide explains how to validate scripts in `unconfirmed_experiments/` and promote them to `confirmed_experiments/`.

## Ground rules

- Test only on systems you own or have explicit permission to assess.
- Prefer an isolated VM or dedicated lab machine.
- Never commit real API keys, bearer tokens, screenshots containing secrets, or private system data.
- Keep filenames and documentation in English.

## Validation steps

1. Select a script from `unconfirmed_experiments/`.
2. Read the full payload and confirm what it types/runs.
3. Replace the hardcoded `PASTE_OPENAI_API_KEY_HERE` placeholder privately on the Windows lab machine.
4. Run the payload in a lab machine.
5. Confirm that `Pentesting_Report.html` is created on the desktop.
6. Review the report for defensive guidance only.
7. If the script works cleanly, promote it to `confirmed_experiments/`.

## Repository checks

```bash
python scripts/generate_payloads.py
python scripts/validate_payloads.py
```
