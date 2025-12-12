from __future__ import annotations

from pith.core import PithSchema

from .heuristic import heuristic_analyze
from .providers import Provider, ProviderName, get_provider


def analyze_help(
    tool: str,
    help_text: str | None,
    subcommands: list[str] | None = None,
    provider: Provider | ProviderName | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> PithSchema:
    """Analyze CLI help text to generate a PithSchema.

    Uses the specified provider (or heuristic fallback) to parse help output
    and extract progressive discovery tiers.

    Args:
        tool: Tool name (e.g., "kubectl")
        help_text: Captured --help output
        subcommands: Pre-discovered subcommand names
        provider: Provider instance or name ("anthropic", "openai", "ollama", "none")
        model: Model override for LLM providers
        api_key: API key override

    Returns:
        PithSchema with extracted tiers
    """
    if help_text is None:
        help_text = ""

    # Resolve provider
    if provider is None:
        # Default to heuristic
        return heuristic_analyze(tool, help_text, subcommands)

    if isinstance(provider, str):
        resolved_provider = get_provider(provider, model=model, api_key=api_key)
    else:
        resolved_provider = provider

    return resolved_provider.analyze_help(tool, help_text, subcommands)
