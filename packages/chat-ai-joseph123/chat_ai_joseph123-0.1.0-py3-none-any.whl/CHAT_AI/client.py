"""
CHAT_AI.client
Simple client functions to query an LLM provider.
"""

from typing import Optional, Dict
import os
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

API_PROVIDER = os.getenv("AI_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def _call_openai(prompt: str, max_tokens: int = 150, **kwargs) -> str:
    """
    Minimal OpenAI API-like call.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing in environment variables")

    import requests

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": kwargs.get("temperature", 0.7),
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()

    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return json.dumps(data)


def get_response(prompt: str, max_tokens: int = 150, **kwargs) -> str:
    """
    Send a prompt to the AI provider and return generated text.
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must be non-empty.")

    if API_PROVIDER.lower() == "openai":
        return _call_openai(prompt, max_tokens=max_tokens, **kwargs)

    raise NotImplementedError(f"Provider {API_PROVIDER} not supported.")
