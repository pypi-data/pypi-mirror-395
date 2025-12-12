"""
CHAT_AI.utils
Helper functions for summarization and formatting.
"""

from .client import get_response
import re


def summarize_text(text: str, max_tokens: int = 120) -> str:
    """
    Summarize large text into a short explanation.
    """
    if not text or not text.strip():
        return ""

    prompt = f"Summarize the following text clearly:\n\n{text}"
    return get_response(prompt, max_tokens=max_tokens)


def format_response(text: str) -> str:
    """
    Normalize whitespace in AI output.
    """
    if not text:
        return ""

    text = text.strip()
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text
