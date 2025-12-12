"""Provider interface for ai-helper."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class AIProvider(ABC):
    """Abstract provider for language model backends."""

    @abstractmethod
    def get_response(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Return a response for the given prompt."""


class ProviderError(RuntimeError):
    """Raised when a provider cannot fulfill the request."""


__all__ = ["AIProvider", "ProviderError"]
