from __future__ import annotations

from typing import Literal

from .anthropic import AnthropicProvider
from .base import Provider
from .none import NoProvider
from .ollama import OllamaProvider
from .openai import OpenAIProvider

ProviderName = Literal["anthropic", "openai", "ollama", "none"]


def get_provider(
    name: ProviderName,
    model: str | None = None,
    api_key: str | None = None,
) -> Provider:
    """Factory function to get a provider by name.

    Args:
        name: Provider name (anthropic, openai, ollama, none)
        model: Optional model override
        api_key: Optional API key override

    Returns:
        Provider instance
    """
    if name == "anthropic":
        kwargs: dict[str, str] = {}
        if model:
            kwargs["model"] = model
        if api_key:
            kwargs["api_key"] = api_key
        return AnthropicProvider(**kwargs)
    elif name == "openai":
        kwargs = {}
        if model:
            kwargs["model"] = model
        if api_key:
            kwargs["api_key"] = api_key
        return OpenAIProvider(**kwargs)
    elif name == "ollama":
        kwargs = {}
        if model:
            kwargs["model"] = model
        return OllamaProvider(**kwargs)
    else:
        return NoProvider()


__all__ = [
    "AnthropicProvider",
    "NoProvider",
    "OllamaProvider",
    "OpenAIProvider",
    "Provider",
    "ProviderName",
    "get_provider",
]
