from __future__ import annotations

from pith.core import PithSchema

from ..heuristic import heuristic_analyze


class NoProvider:
    """Heuristic-only provider that parses help text without LLM.

    Use this provider when:
    - No API key is available
    - Offline operation is required
    - Quick wrapping with reduced quality is acceptable
    """

    name = "none"

    def analyze_help(
        self,
        tool: str,
        help_output: str,
        subcommands: list[str] | None = None,
    ) -> PithSchema:
        """Analyze help using heuristic parsing only.

        Args:
            tool: Tool name
            help_output: Captured --help output
            subcommands: Discovered subcommand names (used for schema)

        Returns:
            PithSchema with heuristic-extracted content
        """
        return heuristic_analyze(tool, help_output, subcommands)
