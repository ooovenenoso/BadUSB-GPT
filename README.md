# BadUSB-GPT: Rubber Ducky Meets GPT

![BadUSB x GPT](https://github.com/ooovenenoso/BadUSB-GPT/blob/main/banner.png)

BadUSB-GPT contains USB Rubber Ducky payload experiments that generate an AI-assisted defensive assessment report from basic Windows system inventory.

> **Ethical-use only:** run these payloads only on systems you own or where you have explicit written permission. The project is intended for lab work, security education, and authorized defensive assessments.

## 2026 refresh

- Uses current GPT-class model defaults instead of legacy `gpt-3.5-turbo`.
- Reads API credentials and API base URL from environment variables; no keys or provider endpoints are embedded in payloads.
- Supports `BADUSB_GPT_MODEL` / `OPENAI_MODEL` override without editing payload files.
- Adds safer report generation: AI output and inventory are HTML-escaped before being written to disk.
- Adds payload generation and validation scripts plus GitHub Actions checks.
- Keeps untested variants in `unconfirmed_experiments/` until they are validated.

## Payloads

- `PentestGPT.txt` — main demo payload, default model: `gpt-4.1-mini`.
- `unconfirmed_experiments/PentestGPT_4oMini.txt` — experimental `gpt-4o-mini` variant.
- `unconfirmed_experiments/PentestGPT_4o.txt` — experimental `gpt-4o` variant.
- `unconfirmed_experiments/PentestGPT_4Turbo.txt` — experimental `gpt-4-turbo` variant.
- `unconfirmed_experiments/Install_Windows_MCP_Discord_Webhook.txt` — experimental authorized installer for [Windows-MCP](https://github.com/CursorTouch/Windows-MCP) that posts installation status to a Discord webhook supplied through an environment variable.

## Requirements

- Authorized Windows test machine or VM.
- USB Rubber Ducky-compatible device/encoder.
- PowerShell available on the test machine.
- API key and OpenAI-compatible base URL stored in the Windows user environment:

```powershell
setx BADUSB_GPT_API_KEY "your_api_key_here"
setx BADUSB_GPT_BASE_URL "https://your-openai-compatible-provider/v1"
```

The payload also accepts compatible `OPENAI_API_KEY` and `OPENAI_BASE_URL` variables if you already use those.

For the experimental Windows-MCP installer payload, set these variables instead:

```powershell
setx BADUSB_GPT_AUTHORIZED_INSTALL "YES"
setx BADUSB_GPT_DISCORD_WEBHOOK "https://discord.com/api/webhooks/..."
```

That installer reports only installation status metadata to Discord. Do not commit webhook URLs or generated logs.

Optional model override:

```powershell
setx BADUSB_GPT_MODEL "gpt-4.1-mini"
```

Restart the PowerShell/session after `setx` so the new variables are visible.

## What the payload collects

The payload gathers a compact defensive inventory:

- OS caption, version, architecture, computer name, and last boot time.
- Five most recent hotfix IDs.
- Enabled network adapter descriptions.
- Enabled firewall profiles.
- Enabled local user names.
- Top five process names by CPU.

The inventory is sent to OpenAI to generate a defensive hardening report. Review your organization's data-handling policy before use.

## Local maintenance

Regenerate all payload variants:

```bash
python scripts/generate_payloads.py
```

Validate payload syntax and safety checks:

```bash
python scripts/validate_payloads.py
```

## Confirmation workflow

1. Review a payload before running it.
2. Test only in a VM or dedicated authorized lab machine.
3. Record OS version, device/encoder used, model, and results.
4. Submit notes via issue or pull request.
5. Move scripts from `unconfirmed_experiments/` to `confirmed_experiments/` only after validation.

## Supporters and donations

If this project helps you, caffeine is appreciated: [Buy Me a Coffee](https://www.buymeacoffee.com/ooovenenoso).
