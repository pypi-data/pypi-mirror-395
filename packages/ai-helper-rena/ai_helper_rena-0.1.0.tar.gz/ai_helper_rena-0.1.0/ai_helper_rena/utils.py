"""
Utility functions for GPT_Helper.
"""

import re
from typing import Optional
from .client import ChatGPTClient


def format_response(text: str, max_length: Optional[int] = None) -> str:
    """
    Clean ChatGPT response (strip spaces, reduce newlines, truncate).
    """
    if text is None:
        return ""

    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)

    if max_length and len(text) > max_length:
        return text[:max_length].rstrip() + "..."

    return text


def summarize_text(text: str, client: ChatGPTClient, max_tokens: int = 150) -> str:
    """
    Summarize long text using ChatGPT.
    """
    if not text.strip():
        return ""

    prompt = f"Summarize the following text in 3–5 sentences:\n\n{text}\n\nSummary:"

    raw = client.get_response(prompt, max_tokens=max_tokens)
    return format_response(raw)
