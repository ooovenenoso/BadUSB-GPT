# BadUSB-GPT: Rubber Ducky Meets GPT

![BadUSB x GPT](https://github.com/ooovenenoso/BadUSB-GPT/blob/main/banner.png)

BadUSB-GPT contains USB Rubber Ducky payload experiments that generate an AI-assisted defensive assessment report from basic Windows system inventory.

> **Ethical-use only:** run these payloads only on systems you own or where you have explicit written permission. The project is intended for lab work, security education, and authorized defensive assessments.

## Current build

- Restores the original plug-and-play style: API key, OpenAI base URL, and model are hardcoded directly in each payload.
- Keeps the committed API key as the safe placeholder `PASTE_OPENAI_API_KEY_HERE`; replace it privately before authorized lab use.
- Uses the hardcoded OpenAI-compatible base URL `https://api.openai.com/v1`.
- Keeps safer report generation: AI output and inventory are HTML-escaped before being written to disk.
- Maintained as an owner-controlled project by `ooovenenoso`.

## Payloads

- `PentestGPT.txt` — main demo payload, default model: `gpt-4.1-mini`.
- `unconfirmed_experiments/PentestGPT_4oMini.txt` — experimental `gpt-4o-mini` variant.
- `unconfirmed_experiments/PentestGPT_4o.txt` — experimental `gpt-4o` variant.
- `unconfirmed_experiments/PentestGPT_4Turbo.txt` — experimental `gpt-4-turbo` variant.

## Requirements

- Authorized Windows test machine or VM.
- USB Rubber Ducky-compatible device/encoder.
- PowerShell available on the test machine.
- A valid OpenAI API key inserted directly in the payload before use.

Edit the payload line:

```powershell
$apiKey = 'PASTE_OPENAI_API_KEY_HERE'
```

Replace only the placeholder value locally/private. Do **not** commit a real API key.

The base URL and model are also hardcoded in the payload:

```powershell
$baseUrl = 'https://api.openai.com/v1'
$model = 'gpt-4.1-mini'
```

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

Validate payload syntax and placeholder safety:

```bash
python scripts/validate_payloads.py
```

## Confirmation workflow

1. Review a payload before running it.
2. Test only in a VM or dedicated authorized lab machine.
3. Record OS version, device/encoder used, model, and results.
4. Move scripts from `unconfirmed_experiments/` to `confirmed_experiments/` only after validation.

## Supporters and donations

If this project helps you, caffeine is appreciated: [Buy Me a Coffee](https://www.buymeacoffee.com/ooovenenoso).
