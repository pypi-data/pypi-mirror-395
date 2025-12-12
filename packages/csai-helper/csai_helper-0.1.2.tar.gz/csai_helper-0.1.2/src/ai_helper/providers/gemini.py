"""Google Gemini provider using the public generativelanguage API."""

from __future__ import annotations

import os
from typing import Optional

import requests

from ai_helper.providers.base import AIProvider, ProviderError


class GeminiProvider(AIProvider):
    """Call Gemini via the Generative Language REST API.

    Requires a `GOOGLE_API_KEY` (or explicit api_key argument). Default model: `gemini-1.5-flash`.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: str = "gemini-1.5-flash",
        base_url: str = "https://generativelanguage.googleapis.com/v1",
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ProviderError("GOOGLE_API_KEY is not set")
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_response(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        url = f"{self.base_url}/models/{self.model}:generateContent"
        text = prompt if not system_prompt else f"{system_prompt}\n\n{prompt}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": text},
                    ],
                }
            ],
        }
        try:
            resp = requests.post(
                url,
                params={"key": self.api_key},
                json=payload,
                timeout=kwargs.get("timeout", self.timeout),
            )
        except requests.RequestException as exc:  # pragma: no cover - network errors
            raise ProviderError(f"Gemini request failed: {exc}") from exc

        if resp.status_code != 200:
            message = resp.text
            if resp.status_code == 404:
                message = (
                    "Model not found. Set `model` to one of the names returned by "
                    "https://generativelanguage.googleapis.com/v1/models."
                )
            raise ProviderError(f"Gemini error {resp.status_code}: {message}")

        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as exc:  # pragma: no cover - unexpected response shape
            raise ProviderError(f"Unexpected Gemini response: {data}") from exc


__all__ = ["GeminiProvider"]
