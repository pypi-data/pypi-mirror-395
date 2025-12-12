"""OpenAI provider implementation."""

from __future__ import annotations

import os
from typing import Optional

from ai_helper.providers.base import AIProvider, ProviderError

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover - exercised only when package missing
    raise ImportError(
        "openai package is not installed. Install with `pip install ai-helper[openai]`."
    ) from exc


class OpenAIProvider(AIProvider):
    """Thin wrapper around the OpenAI Chat Completions API."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        client: Optional[object] = None,
        temperature: float = 0.2,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key and client is None:
            raise ProviderError("OPENAI_API_KEY is not set")
        self.client = client or OpenAI(api_key=self.api_key)
        self.model = model
        self.temperature = temperature

    def get_response(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.pop("temperature", self.temperature),
            **kwargs,
        )
        try:
            content = response.choices[0].message.content
        except (AttributeError, IndexError) as exc:  # pragma: no cover
            raise ProviderError("OpenAI returned an unexpected response format") from exc
        if content is None:
            raise ProviderError("OpenAI returned empty content")
        return content.strip()


__all__ = ["OpenAIProvider"]
