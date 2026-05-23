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

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"Bearer\s+(?!\$apiKey)[A-Za-z0-9._-]{20,}", re.IGNORECASE),
    re.compile(r"https://(?:discord(?:app)?\.com|canary\.discord\.com)/api/webhooks/\d+/[A-Za-z0-9_-]+", re.IGNORECASE),
]


def _is_report_payload(text: str) -> bool:
    return "chatCompletionsUrl" in text or "BADUSB_GPT_API_KEY" in text or "OPENAI_API_KEY" in text


def _is_windows_mcp_installer(text: str) -> bool:
    return "Windows-MCP installer" in text or "windows-mcp install" in text


def validate_payload(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines:
        return [f"{path}: empty payload"]

    if not any("explicit permission" in line.lower() or "authorized" in line.lower() for line in lines):
        errors.append(f"{path}: missing authorized-use reminder")

    if "YOUR_OPENAI_API_KEY" in text:
        errors.append(f"{path}: still contains hard-coded API-key placeholder")

    if "https://api.openai.com" in text:
        errors.append(f"{path}: contains a hard-coded OpenAI API endpoint")

    if _is_report_payload(text):
        if "OPENAI_API_KEY" not in text and "BADUSB_GPT_API_KEY" not in text:
            errors.append(f"{path}: does not read an API key from environment")
        if "chatCompletionsUrl" not in text:
            errors.append(f"{path}: does not use configurable chat completions URL")

    if _is_windows_mcp_installer(text):
        if "BADUSB_GPT_AUTHORIZED_INSTALL" not in text:
            errors.append(f"{path}: Windows-MCP installer lacks explicit opt-in environment gate")
        if "BADUSB_GPT_DISCORD_WEBHOOK" not in text:
            errors.append(f"{path}: Windows-MCP installer does not read Discord webhook from environment")
        if "windows-mcp install" not in text:
            errors.append(f"{path}: Windows-MCP installer does not register the server")

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path}: possible embedded secret, bearer token, or Discord webhook")

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
