"""Core AI helper functions.

This module provides thin wrappers around the OpenAI API. It expects the
`OPENAI_API_KEY` environment variable to be set. Functions include:
- get_response(prompt): returns AI-generated text for the prompt
- summarize_text(text): asks the AI to summarize given text
- format_response(text): simple sanitizer/formatter for AI output

The implementation uses the ChatCompletion endpoint (gpt-3.5-turbo by default).
"""
from __future__ import annotations

import os
import re
from typing import Optional

import openai


# If OPENAI_API_KEY is present in the environment, configure openai client
_api_key = os.getenv("OPENAI_API_KEY")
if _api_key:
    openai.api_key = _api_key


def _ensure_api_key() -> None:
    """Raise RuntimeError if OPENAI_API_KEY is not configured."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")


def get_response(prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 150) -> str:
    """Send `prompt` to the AI and return the text response.

    Args:
        prompt: The user prompt to send to the model.
        model: Model name to use.
        max_tokens: Maximum tokens for the response.

    Returns:
        The assistant's text reply.

    Raises:
        RuntimeError: if API key missing or the API call fails.
    """
    _ensure_api_key()

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7,
        )

        # ChatCompletion returns choices with message objects
        choice = response.choices[0]
        # Some SDKs return a nested message object
        message = getattr(choice, "message", None)
        if message and getattr(message, "content", None) is not None:
            content = message.content
        else:
            # Fallback for older response shapes
            content = choice.text if hasattr(choice, "text") else str(choice)

        return format_response(content)

    except Exception as exc:  # pragma: no cover - hard to simulate network errors
        raise RuntimeError(f"AI request failed: {exc}") from exc


def summarize_text(text: str, max_tokens: int = 100) -> str:
    """Return a short summary (2-3 sentences) of the provided `text`.

    This function delegates to `get_response` with a clear instruction prompt.
    """
    prompt = (
        "Please provide a concise summary (2-3 sentences) of the following text:\n\n"
        f"{text}\n\nSummary:"
    )
    return get_response(prompt, max_tokens=max_tokens)


def format_response(text: Optional[str]) -> str:
    """Clean and normalize AI-generated text.

    - Trim whitespace
    - Collapse multiple blank lines
    - Normalize repeated spaces

    Args:
        text: Raw text from AI.

    Returns:
        Cleaned text string.
    """
    if not text:
        return ""

    # Normalize line endings and strip leading/trailing whitespace
    out = text.replace("\r\n", "\n").strip()
    # Collapse multiple blank lines
    out = re.sub(r"\n{2,}", "\n\n", out)
    # Collapse repeated spaces
    out = re.sub(r"[ \t]{2,}", " ", out)

    return out
