#!/usr/bin/env python3
"""Terminal-based ChatGPT using GPT-4o mini."""
import os
import json
import requests

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise SystemExit("OPENAI_API_KEY environment variable not set")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

messages = []
print("Terminal GPT (gpt-4o mini). Type 'exit' to quit.")
while True:
    user = input("You: ")
    if user.lower() == "exit":
        break
    messages.append({"role": "user", "content": user})
    print("Assistant: ...", end="\r")
    body = {"model": "gpt-4o-mini", "messages": messages}
    try:
        resp = requests.post("https://api.openai.com/v1/chat/completions",
                             headers=headers, data=json.dumps(body))
        resp.raise_for_status()
        answer = resp.json()["choices"][0]["message"]["content"].strip()
        print("Assistant:", answer)
        messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        print("Error:", e)
