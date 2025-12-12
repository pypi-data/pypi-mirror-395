"""Local fallback provider for deterministic responses without external APIs."""

from __future__ import annotations

import re
from typing import Optional

from ai_helper.providers.base import AIProvider


class LocalProvider(AIProvider):
    """A lightweight provider that avoids network calls.

    Useful for testing, demos, and environments where an API key is not available.
    """

    def __init__(self, *, prefix: str = "[local]", max_chars: int = 1200) -> None:
        self.prefix = prefix
        self.max_chars = max_chars

    def get_response(self, prompt: str, *, system_prompt: Optional[str] = None, **kwargs) -> str:
        cleaned = self._tidy(prompt)
        if system_prompt:
            cleaned = f"{self._tidy(system_prompt)}\n\n{cleaned}"
        message = f"{self.prefix} {cleaned}" if self.prefix else cleaned
        return message[: self.max_chars].strip()

    def summarize(self, text: str, *, max_words: int = 120) -> str:
        if max_words <= 0:
            raise ValueError("max_words must be positive")
        words: list[str] = []
        for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
            for word in sentence.split():
                if len(words) >= max_words:
                    break
                words.append(word)
            if len(words) >= max_words:
                break
        if not words and text:
            words = text.split()[:max_words]
        summary = " ".join(words)
        return f"{self.prefix} {summary}".strip()

    def _tidy(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.strip())


__all__ = ["LocalProvider"]
