from __future__ import annotations

from typing import Literal, cast

from pith.core import (
    PithSchema,
    render_search_results,
    render_search_results_json,
    render_tier0,
    render_tier0_json,
    render_tier1,
    render_tier1_json,
    render_tier2,
    render_tier2_json,
    render_tier3,
    render_tier3_json,
    search_commands,
)
from pith.core.types import TierLevel

OutputFormat = Literal["text", "json"]


def render(
    schema: PithSchema,
    command: str | None = None,
    level: int = 0,
    output_format: OutputFormat = "text",
) -> str:
    """Render schema at the specified tier level.

    Args:
        schema: PithSchema to render
        command: Specific command to render (None for tier 0)
        level: Tier level (0-3)
        output_format: "text" or "json"

    Returns:
        Formatted output string
    """
    if command is None:
        if output_format == "json":
            return render_tier0_json(schema)
        return render_tier0(schema)

    target = schema.commands.get(command)
    if not target:
        # Command not found, fall back to tier 0
        if output_format == "json":
            return render_tier0_json(schema)
        return render_tier0(schema)

    tier = cast("TierLevel", max(1, min(level, 3)))

    if output_format == "json":
        if tier == 1:
            return render_tier1_json(schema, command)
        if tier == 2:
            return render_tier2_json(schema, command)
        return render_tier3_json(schema, command)
    else:
        if tier == 1:
            return render_tier1(schema, command)
        if tier == 2:
            return render_tier2(schema, command)
        return render_tier3(schema, command)


def search(
    schema: PithSchema,
    query: str,
    output_format: OutputFormat = "text",
    limit: int = 5,
) -> str:
    """Search commands by semantic query.

    Args:
        schema: PithSchema to search
        query: Natural language query
        output_format: "text" or "json"
        limit: Maximum results to return

    Returns:
        Formatted search results
    """
    results = search_commands(schema, query, limit=limit)

    if output_format == "json":
        return render_search_results_json(schema, results, query)
    return render_search_results(schema, results, query)
