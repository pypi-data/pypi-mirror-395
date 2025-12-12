"""
ai_helpers.core
Simple helper library for AI-powered responses.

Functions:
 - get_response(prompt, provider="openai", **kwargs)
 - summarize_text(text, max_tokens=200)
 - format_response(text)
"""

import os
import json
from typing import Optional, Dict

# Example: OpenAI client wrapper (optional)
try:
    import openai
except Exception:
    openai = None

API_PROVIDER = os.getenv("AI_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def _call_openai(prompt: str, max_tokens: int = 150, temperature: float = 0.2) -> str:
    if openai is None:
        raise RuntimeError("openai package not installed")
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = OPENAI_API_KEY
    resp = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1
    )
    text = resp.choices[0].text.strip()
    return text

def get_response(prompt: str, provider: Optional[str] = None, **kwargs) -> str:
    """
    Send a prompt to a configured AI provider and return the response string.

    Args:
        prompt: text prompt to send.
        provider: optional override (e.g., "openai"). If None uses AI_PROVIDER env var.
        kwargs: forwarded to provider call (e.g., max_tokens, temperature).

    Returns:
        str: AI response text.
    """
    provider = provider or API_PROVIDER
    if provider == "openai":
        return _call_openai(prompt, **kwargs)
    else:
        # Placeholder fallback: simple local echo or dummy transformer
        return f"[mock response] you asked: {prompt[:200]}"

def summarize_text(text: str, max_tokens: int = 120) -> str:
    """
    Summarize a longer text via AI or a simple rule fallback.
    """
    prompt = f"Summarize the following text in 3-4 lines:\n\n{text}"
    return get_response(prompt, max_tokens=max_tokens)

def format_response(text: str) -> str:
    """
    Clean and format AI output for UI display: trims whitespace and converts stray newlines.
    """
    if text is None:
        return ""
    out = text.strip()
    # simple formatting rules:
    out = out.replace("\r\n", "\n")
    # collapse multiple blank lines
    while "\n\n\n" in out:
        out = out.replace("\n\n\n", "\n\n")
    return out
