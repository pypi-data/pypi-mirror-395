from __future__ import annotations

from typing import Protocol

from pith.core import PithSchema


class Provider(Protocol):
    """Interface for LLM providers that analyze CLI help text.

    Providers convert raw help output into a structured PithSchema
    with progressive discovery tiers.
    """

    name: str

    def analyze_help(
        self,
        tool: str,
        help_output: str,
        subcommands: list[str] | None = None,
    ) -> PithSchema:
        """Analyze help output and return a pith schema.

        Args:
            tool: Tool name (e.g., "kubectl")
            help_output: Captured --help output
            subcommands: List of discovered subcommand names

        Returns:
            Populated PithSchema with all tiers
        """
        ...
