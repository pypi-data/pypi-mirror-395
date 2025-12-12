"""Core functions for ai-helper."""

from __future__ import annotations

import re
import textwrap
from typing import Optional

from ai_helper.providers.base import AIProvider
from ai_helper.providers.local import LocalProvider

_default_provider: AIProvider = LocalProvider()


def get_default_provider() -> AIProvider:
    """Return the globally configured provider."""
    return _default_provider


def set_default_provider(provider: AIProvider) -> None:
    """Override the global provider used by helper functions."""
    global _default_provider
    _default_provider = provider


def format_response(text: str) -> str:
    """Normalize AI responses by trimming whitespace and dropping empty lines."""
    stripped = text.strip()
    cleaned: list[str] = []
    for raw_line in stripped.splitlines():
        line = re.sub(r"\s+", " ", raw_line).strip()
        if line:
            cleaned.append(line)
    return "\n".join(cleaned)


def get_response(
    prompt: str,
    *,
    provider: Optional[AIProvider] = None,
    system_prompt: Optional[str] = None,
    **kwargs,
) -> str:
    """Send a prompt to the chosen provider and return a cleaned response."""
    active_provider = provider or _default_provider
    raw = active_provider.get_response(prompt, system_prompt=system_prompt, **kwargs)
    return format_response(raw)


def summarize_text(
    text: str,
    *,
    provider: Optional[AIProvider] = None,
    max_words: int = 120,
    **kwargs,
) -> str:
    """Summarize text using the provider or a lightweight local fallback."""
    if max_words <= 0:
        raise ValueError("max_words must be positive")
    if not text.strip():
        return ""

    active_provider = provider or _default_provider

    if hasattr(active_provider, "summarize"):
        # Some providers offer a native summarize implementation.
        summary = active_provider.summarize(text, max_words=max_words)
    else:
        prompt = _build_summary_prompt(text, max_words)
        summary = active_provider.get_response(prompt, **kwargs)

    return _trim_to_words(format_response(summary), max_words)


def _build_summary_prompt(text: str, max_words: int) -> str:
    return textwrap.dedent(
        f"""
        Summarize the following text in at most {max_words} words.
        Focus on the key points and write in plain English.

        Text:
        {text.strip()}
        """
    ).strip()


def _trim_to_words(text: str, max_words: int) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])
