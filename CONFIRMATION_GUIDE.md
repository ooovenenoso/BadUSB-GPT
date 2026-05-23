# Community Confirmation Guide

This guide explains how contributors can validate scripts in `unconfirmed_experiments/` and promote them to `confirmed_experiments/`.

## Ground rules

- Test only on systems you own or have explicit permission to assess.
- Prefer an isolated VM or dedicated lab machine.
- Never commit API keys, bearer tokens, screenshots containing secrets, or private system data.
- Keep filenames and documentation in English.

## Validation checklist

1. Select a script from `unconfirmed_experiments/`.
2. Read the full payload and confirm what it types/runs.
3. For GPT report payloads, set `BADUSB_GPT_API_KEY` and `BADUSB_GPT_BASE_URL` in the Windows user environment; optionally set `BADUSB_GPT_MODEL`.
   For the Windows-MCP installer, set `BADUSB_GPT_AUTHORIZED_INSTALL=YES` and `BADUSB_GPT_DISCORD_WEBHOOK` instead.
4. Run the payload in a lab machine.
5. Confirm the expected artifact:
   - GPT report payloads create `Pentesting_Report.html` on the desktop.
   - Windows-MCP installer creates the `windows-mcp-server` Scheduled Task and sends a status embed to Discord.
6. Review any report or webhook output for safe defensive guidance only and verify no secrets were included.
7. Document:
   - Windows version/build
   - hardware/encoder used
   - payload filename
   - model used, or Windows-MCP version/path for installer tests
   - whether the report opened or the MCP Scheduled Task/webhook succeeded
   - any changes required
8. Open a pull request or issue with your results.

After enough successful validation, maintainers can move a script to `confirmed_experiments/`.

## Repository checks

Before submitting a pull request, run:

```bash
python scripts/generate_payloads.py
python scripts/validate_payloads.py
```
