#!/usr/bin/env python3
"""Lightweight repository checks for BadUSB-GPT payloads."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOADS = [ROOT / "PentestGPT.txt", *sorted((ROOT / "unconfirmed_experiments").glob("*.txt"))]
ALLOWED_COMMANDS = {
    "REM",
    "DELAY",
    "GUI",
    "STRING",
    "ENTER",
    "LEFTARROW",
    "RIGHTARROW",
    "UPARROW",
    "DOWNARROW",
    "CTRL",
    "ALT",
    "SHIFT",
    "TAB",
    "SPACE",
}
API_KEY_PLACEHOLDER = "PASTE_OPENAI_API_KEY_HERE"
EXPECTED_BASE_URL = "https://api.openai.com/v1"
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"Bearer\s+(?!\$apiKey)[A-Za-z0-9._-]{20,}", re.IGNORECASE),
]


def validate_payload(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines:
        return [f"{path}: empty payload"]

    if not any("explicit permission" in line.lower() or "authorized" in line.lower() for line in lines):
        errors.append(f"{path}: missing authorized-use reminder")

    if API_KEY_PLACEHOLDER not in text:
        errors.append(f"{path}: missing hardcoded API-key placeholder")

    if EXPECTED_BASE_URL not in text:
        errors.append(f"{path}: missing hardcoded OpenAI API base URL")

    api_env_names = [
        "OPENAI_API_KEY",
        "BADUSB_GPT_API_KEY",
        "OPENAI_BASE_URL",
        "BADUSB_GPT_BASE_URL",
        "OPENAI_MODEL",
        "BADUSB_GPT_MODEL",
    ]
    api_config_text = text.replace(API_KEY_PLACEHOLDER, "")
    for name in api_env_names:
        if name in api_config_text:
            errors.append(f"{path}: still references environment-based API setting {name}")

    if "chatCompletionsUrl" not in text:
        errors.append(f"{path}: does not build a chat completions URL")

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path}: possible embedded real secret or bearer token")

    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        command = line.split(maxsplit=1)[0]
        if command not in ALLOWED_COMMANDS:
            errors.append(f"{path}:{number}: unknown DuckyScript command {command!r}")

    return errors


def main() -> int:
    errors: list[str] = []
    for payload in PAYLOADS:
        errors.extend(validate_payload(payload))

    if errors:
        print("Payload validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(PAYLOADS)} payload(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
