"""
ai_text_ap.core
Helper functions for AI text tasks using Groq.

This module expects an environment variable GROQ_API_KEY.
"""

import os
import requests
from typing import Optional

# Environment variable for Groq key
GROQ_API_KEY_ENV = "GROQ_API_KEY"

def _get_api_key() -> Optional[str]:
    """Return API key from environment or None."""
    return os.environ.get(GROQ_API_KEY_ENV)

def format_response(text: str) -> str:
    """
    Light cleaning of AI responses.
    - Strips leading/trailing whitespace.
    - Replaces repeated newlines with a single newline.
    - Collapses multiple spaces to one.
    """
    if text is None:
        return ""
    out = " ".join(line.strip() for line in text.strip().splitlines() if line.strip())
    out = " ".join(out.split())
    return out


def get_response(prompt: str, model: str = "llama-3.1-8b-instant", max_tokens: int = 150) -> str:
    """
    Send prompt to Groq (OpenAI-compatible endpoint).

    Args:
        prompt: The user prompt.
        model: Groq model name.
        max_tokens: Max tokens to request.

    Returns:
        Cleaned text response.
    """
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError("No API key found. Set the environment variable GROQ_API_KEY.")

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(f"Groq API Error {resp.status_code}: {resp.text}")

    data = resp.json()
    raw_text = data["choices"][0]["message"]["content"]

    return format_response(raw_text)


def summarize_text(text: str, max_tokens: int = 120) -> str:
    """
    Summarize text using Groq.
    """
    prompt = f"Please summarize the following text in 3-5 simple sentences for a teen:\n\n{text}"
    return get_response(prompt, max_tokens=max_tokens)
