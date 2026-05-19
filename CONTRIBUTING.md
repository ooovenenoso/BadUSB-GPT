# Contributing

Thanks for improving BadUSB-GPT.

## Workflow

1. Keep new or modified payloads in `unconfirmed_experiments/` until tested.
2. Use `scripts/generate_payloads.py` when updating the maintained payload family.
3. Do not hard-code API keys, tokens, hostnames, usernames, IP addresses, or private report output.
4. Keep changes defensive, authorized-use oriented, and non-destructive.
5. Run checks before opening a pull request:

```bash
python scripts/generate_payloads.py
python scripts/validate_payloads.py
```

## Payload style

- Start with `REM` comments that identify purpose and authorized-use requirements.
- Prefer environment variables for API keys, base URLs, and model configuration.
- Keep model names easy to override.
- Add clear error handling for missing prerequisites.
- Escape generated report content before writing HTML.
