"""pith-cli package: Wrap any CLI with agent-friendly progressive discovery."""

from .analyze import analyze_help
from .capture import capture_help
from .cli import app, main
from .heuristic import heuristic_analyze
from .platforms import (
    detect_shell,
    find_tool,
    get_activation_command,
    get_bin_dir,
    get_original_path,
    get_pith_dir,
)
from .providers import (
    AnthropicProvider,
    NoProvider,
    OllamaProvider,
    OpenAIProvider,
    Provider,
    ProviderName,
    get_provider,
)
from .query import render, search

__all__ = [
    "AnthropicProvider",
    "NoProvider",
    "OllamaProvider",
    "OpenAIProvider",
    "Provider",
    "ProviderName",
    "analyze_help",
    "app",
    "capture_help",
    "detect_shell",
    "find_tool",
    "get_activation_command",
    "get_bin_dir",
    "get_original_path",
    "get_pith_dir",
    "get_provider",
    "heuristic_analyze",
    "main",
    "render",
    "search",
]
