# Maintainer Notes

BadUSB-GPT is currently maintained as an owner-controlled project by `ooovenenoso`.

## Payload style

- Start with `REM` comments that identify purpose and authorized-use requirements.
- Keep the public payload structurally hardcoded for API key, base URL, and model.
- Commit only the safe API key placeholder `PASTE_OPENAI_API_KEY_HERE`; never commit a real API key.
- Keep model names easy to edit directly in the payload.
- Add clear error handling for missing placeholder replacement.
- Escape generated report content before writing HTML.

## Checks

```bash
python scripts/generate_payloads.py
python scripts/validate_payloads.py
```
