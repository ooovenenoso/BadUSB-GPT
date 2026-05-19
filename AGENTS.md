# Repository Instructions

This repository contains USB Rubber Ducky payloads that interact with GPT-based services for authorized defensive assessment workflows.

Two top-level folders store experiments:

- `unconfirmed_experiments/` – draft or proof-of-concept scripts. Anything here should be treated as experimental.
- `confirmed_experiments/` – scripts that have been tested and approved for general use.

When contributing new scripts:

1. Place untested or in-progress payloads inside `unconfirmed_experiments/`.
2. After validating a script, move it to `confirmed_experiments/`.
3. Keep filenames and documentation in English.
4. Do not embed API keys, bearer tokens, host-specific secrets, or generated private report data.
5. Keep payloads non-destructive and scoped to authorized defensive use.
6. Run repository checks before committing:

```bash
python scripts/generate_payloads.py
python scripts/validate_payloads.py
```

These instructions apply to all files in this repository.
