#!/usr/bin/env python3
"""Generate BadUSB-GPT Rubber Ducky payload variants.

The public payloads are intentionally plug-and-play in the original style:
- API key, endpoint, and model are hardcoded directly in the PowerShell block
- committed API keys are safe placeholders, never real secrets
- generated report content is HTML-escaped before writing to disk
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

API_KEY_PLACEHOLDER = "PASTE_OPENAI_API_KEY_HERE"
OPENAI_BASE_URL = "https://api.openai.com/v1"

VARIANTS = {
    ROOT / "PentestGPT.txt": "gpt-4.1-mini",
    ROOT / "unconfirmed_experiments" / "PentestGPT_4oMini.txt": "gpt-4o-mini",
    ROOT / "unconfirmed_experiments" / "PentestGPT_4o.txt": "gpt-4o",
    ROOT / "unconfirmed_experiments" / "PentestGPT_4Turbo.txt": "gpt-4-turbo",
}

POWERSHELL_LINES = [
    "$ErrorActionPreference = 'Stop'",
    "$apiKey = '__API_KEY__'",
    "$baseUrl = '__BASE_URL__'",
    "$model = '__MODEL__'",
    "if ($apiKey -eq 'PASTE_OPENAI_API_KEY_HERE') { throw 'Replace PASTE_OPENAI_API_KEY_HERE inside this payload before running it in an authorized lab.' }",
    "$baseUrl = $baseUrl.TrimEnd('/')",
    "$chatCompletionsUrl = if ($baseUrl -match '/chat/completions$') { $baseUrl } else { \"$baseUrl/chat/completions\" }",
    "$reportPath = Join-Path $env:USERPROFILE 'Desktop\\Pentesting_Report.html'",
    "$systemInfo = [ordered]@{",
    "  OS = (Get-CimInstance Win32_OperatingSystem).Caption",
    "  Version = (Get-CimInstance Win32_OperatingSystem).Version",
    "  Architecture = (Get-CimInstance Win32_OperatingSystem).OSArchitecture",
    "  ComputerName = $env:COMPUTERNAME",
    "  LastBootTime = (Get-CimInstance Win32_OperatingSystem).LastBootUpTime",
    "  InstalledUpdates = @((Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5).HotFixID)",
    "  NetworkAdapters = @((Get-CimInstance Win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -eq $true } | Select-Object -ExpandProperty Description))",
    "  FirewallProfilesEnabled = @((Get-NetFirewallProfile | Where-Object Enabled | Select-Object -ExpandProperty Name))",
    "  LocalEnabledUsers = @((Get-LocalUser | Where-Object Enabled | Select-Object -ExpandProperty Name))",
    "  TopProcessesByCPU = @((Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 -ExpandProperty ProcessName))",
    "}",
    "$systemJson = $systemInfo | ConvertTo-Json -Depth 4 -Compress",
    "$promptText = @\"",
    "Authorized defensive assessment only. Review this Windows system inventory and produce a concise security-hardening report in English. Focus on likely configuration risks, verification steps, and prioritized remediation. Do not provide exploitation steps.",
    "System inventory JSON:",
    "$systemJson",
    "\"@",
    "$messages = @(",
    "  @{ role = 'system'; content = 'You are a defensive security assistant. Provide safe, authorized hardening guidance only.' },",
    "  @{ role = 'user'; content = $promptText }",
    ")",
    "$headers = @{ Authorization = \"Bearer $apiKey\"; 'Content-Type' = 'application/json' }",
    "$body = @{ model = $model; messages = $messages; temperature = 0.2 } | ConvertTo-Json -Depth 6",
    "$response = Invoke-RestMethod -Uri $chatCompletionsUrl -Method POST -Headers $headers -Body $body -TimeoutSec 90",
    "$reportText = $response.choices[0].message.content",
    "if ([string]::IsNullOrWhiteSpace($reportText)) { throw 'OpenAI returned an empty report.' }",
    "$encodedReport = [System.Net.WebUtility]::HtmlEncode($reportText)",
    "$encodedInventory = [System.Net.WebUtility]::HtmlEncode(($systemInfo | ConvertTo-Json -Depth 4))",
    "$generatedAt = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss K')",
    "$htmlContent = @\"",
    "<!doctype html>",
    "<html lang='en'>",
    "<head>",
    "  <meta charset='utf-8'>",
    "  <meta name='viewport' content='width=device-width, initial-scale=1'>",
    "  <title>BadUSB-GPT Defensive Assessment</title>",
    "  <style>",
    "    :root { color-scheme: dark; --bg: #0b1020; --panel: #111827; --text: #e5e7eb; --muted: #9ca3af; --accent: #38bdf8; --border: #263244; }",
    "    body { margin: 0; padding: 32px; background: var(--bg); color: var(--text); font-family: Inter, Segoe UI, Arial, sans-serif; line-height: 1.55; }",
    "    main { max-width: 980px; margin: 0 auto; }",
    "    section { background: var(--panel); border: 1px solid var(--border); border-radius: 16px; padding: 24px; margin: 18px 0; box-shadow: 0 20px 50px rgba(0,0,0,.25); }",
    "    h1, h2 { margin-top: 0; }",
    "    h1 { color: var(--accent); }",
    "    .meta { color: var(--muted); }",
    "    pre { white-space: pre-wrap; word-break: break-word; background: #050816; border: 1px solid var(--border); border-radius: 12px; padding: 16px; overflow-x: auto; }",
    "  </style>",
    "</head>",
    "<body>",
    "  <main>",
    "    <section>",
    "      <h1>BadUSB-GPT Defensive Assessment</h1>",
    "      <p class='meta'>Generated: $generatedAt | Model: $model | Scope: authorized defensive review</p>",
    "    </section>",
    "    <section>",
    "      <h2>AI Report</h2>",
    "      <pre>$encodedReport</pre>",
    "    </section>",
    "    <section>",
    "      <h2>Collected Inventory</h2>",
    "      <pre>$encodedInventory</pre>",
    "    </section>",
    "  </main>",
    "</body>",
    "</html>",
    "\"@",
    "Set-Content -Path $reportPath -Value $htmlContent -Encoding UTF8",
    "Start-Process $reportPath",
]


def ducky_payload(model: str) -> str:
    lines = [
        "REM BadUSB-GPT defensive assessment payload",
        "REM Author: ooovenenoso",
        "REM Generated by scripts/generate_payloads.py",
        "REM Use only on systems where you have explicit permission.",
        "REM Hardcoded API style: replace PASTE_OPENAI_API_KEY_HERE before authorized lab use.",
        "DELAY 700",
        "GUI r",
        "DELAY 500",
        "STRING powershell -NoProfile -ExecutionPolicy Bypass",
        "ENTER",
        "DELAY 1200",
    ]

    for ps_line in POWERSHELL_LINES:
        line = (
            ps_line.replace("__API_KEY__", API_KEY_PLACEHOLDER)
            .replace("__BASE_URL__", OPENAI_BASE_URL)
            .replace("__MODEL__", model)
        )
        lines.extend([f"STRING {line}", "ENTER", "DELAY 80"])

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    for path, model in VARIANTS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(ducky_payload(model), encoding="utf-8")
        print(f"generated {path.relative_to(ROOT)} ({model})")


if __name__ == "__main__":
    main()
