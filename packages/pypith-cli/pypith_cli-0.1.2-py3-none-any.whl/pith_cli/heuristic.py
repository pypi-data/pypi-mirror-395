from __future__ import annotations

import re

from pith.core import Command, Option, PithSchema, Tier1, Tier2


def infer_description(help_text: str | None) -> str:
    """Extract first non-empty line as description."""
    if not help_text:
        return "CLI tool"
    for line in help_text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return "CLI tool"


def _find_section(help_text: str, patterns: list[str]) -> list[str]:
    """Find a section in help text by header patterns."""
    lines = help_text.splitlines()
    in_section = False
    section_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        # Check if this line starts a known section
        if any(stripped.lower().startswith(p.lower()) for p in patterns):
            in_section = True
            continue
        # Check if we hit another section header (ends current section)
        if (
            in_section
            and stripped
            and not stripped.startswith("-")
            and ":" in stripped[:20]
            # Likely a new section header
            and not stripped.startswith(" ")
            and stripped[0].isupper()
        ):
            break
        if in_section and stripped:
            section_lines.append(line)

    return section_lines


def _parse_command_line(line: str) -> tuple[str, str]:
    """Parse a command listing line like '  copy   Copy files'."""
    stripped = line.strip()
    # Split on multiple spaces or tabs
    parts = re.split(r"\s{2,}|\t+", stripped, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    # Try single space split for short descriptions
    parts = stripped.split(" ", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return stripped, stripped


def _parse_option_line(line: str) -> Option | None:
    """Parse an option line like '  -f, --force  Force operation'."""
    stripped = line.strip()
    if not stripped.startswith("-"):
        return None

    # Match patterns like "-f, --force TEXT  Description"
    match = re.match(
        r"(-\w)(?:,\s*(--[\w-]+))?\s*(?:(\w+))?\s*(.*)",
        stripped,
    )
    if match:
        short, long_opt, arg_type, desc = match.groups()
        aliases = [short]
        name = long_opt or short
        if long_opt:
            aliases.append(long_opt)
        return Option(
            name=name.lstrip("-"),
            aliases=aliases,
            description=desc.strip() if desc else name.lstrip("-"),
            type=arg_type.lower() if arg_type else "flag",
            required=False,
        )

    # Try simpler pattern: "--option  Description"
    match = re.match(r"(--[\w-]+)\s+(.*)", stripped)
    if match:
        opt, desc = match.groups()
        return Option(
            name=opt.lstrip("-"),
            aliases=[opt],
            description=desc.strip() if desc else opt.lstrip("-"),
            type="flag",
            required=False,
        )

    return None


def heuristic_analyze(
    tool: str,
    help_output: str,
    subcommands: list[str] | None = None,
) -> PithSchema:
    """Best-effort parsing of help text without LLM.

    Recognizes common patterns from Click, Typer, argparse, and Cobra.

    Args:
        tool: Tool name
        help_output: Raw help text
        subcommands: Pre-discovered subcommand names

    Returns:
        PithSchema with extracted content (marked as heuristic)
    """
    help_text = help_output or ""
    description = infer_description(help_text)

    commands: dict[str, Command] = {}

    # Extract commands from subcommands list or by parsing
    cmd_names = subcommands or []
    if not cmd_names:
        # Try to find Commands section
        cmd_section = _find_section(
            help_text,
            ["Commands:", "COMMANDS:", "Subcommands:", "Available commands:"],
        )
        for line in cmd_section:
            name, _ = _parse_command_line(line)
            if name and not name.startswith("-"):
                cmd_names.append(name)

    # Parse global options
    global_options: list[Option] = []
    opt_section = _find_section(
        help_text,
        ["Options:", "OPTIONS:", "Flags:", "Global options:"],
    )
    for line in opt_section:
        opt = _parse_option_line(line)
        if opt:
            global_options.append(opt)

    # Create commands
    for name in cmd_names:
        tier1 = Tier1(
            summary=name.replace("-", " ").title(),
            run=f"{tool} {name}",
        )
        tier2 = (
            Tier2(arguments=[], options=global_options.copy())
            if global_options
            else None
        )
        commands[name] = Command(
            name=name,
            pith=name.replace("-", " ").title(),
            tier1=tier1,
            tier2=tier2,
            intents=[name, name.replace("-", " ")],
        )

    # If no commands found, create a default help command
    if not commands:
        tier1 = Tier1(summary=description, run=f"{tool} <command> [args...]")
        commands["help"] = Command(
            name="help",
            pith=description,
            tier1=tier1,
            intents=["help", "usage"],
        )

    return PithSchema(
        tool=tool,
        pith=description,
        commands=commands,
        schema_version="1.0",
    )
