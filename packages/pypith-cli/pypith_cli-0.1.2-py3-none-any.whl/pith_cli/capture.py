from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass


@dataclass
class HelpCapture:
    """Result of help capture with metadata."""

    output: str
    strategy: str  # "flag", "short_flag", "subcommand", "bare"
    exit_code: int


# Patterns that indicate help output
HELP_INDICATORS = [
    r"\busage\b",
    r"\bcommands?\b",
    r"\boptions?\b",
    r"\barguments?\b",
    r"--help",
    r"-h\b",
    r"\bdescription\b",
]


def looks_like_help(text: str) -> bool:
    """Check if text appears to be help output.

    Args:
        text: Output text to analyze

    Returns:
        True if text looks like CLI help output
    """
    if not text or len(text) < 20:
        return False

    text_lower = text.lower()
    matches = sum(1 for p in HELP_INDICATORS if re.search(p, text_lower))
    return matches >= 2


def _try_capture(tool: str, args: list[str], timeout: int) -> tuple[str | None, int]:
    """Try to capture output with given arguments.

    Returns:
        Tuple of (output, exit_code) or (None, -1) on failure
    """
    try:
        result = subprocess.run(
            [tool, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output or None, result.returncode
    except FileNotFoundError:
        return None, -1
    except subprocess.SubprocessError:
        return None, -1


def capture_help(
    tool: str,
    flag: str | None = None,
    timeout: int = 10,
) -> HelpCapture | None:
    """Capture help output using multiple strategies.

    Tries strategies in order:
    1. --help flag
    2. -h short flag
    3. help subcommand
    4. bare command (no args)

    Args:
        tool: Tool name or path to capture help from
        flag: Specific flag to try (skips multi-strategy if provided)
        timeout: Command timeout in seconds

    Returns:
        HelpCapture with output and metadata, or None if all strategies fail
    """
    if flag is not None:
        # Single strategy mode (backwards compatibility)
        output, exit_code = _try_capture(tool, [flag], timeout)
        if output and looks_like_help(output):
            return HelpCapture(output=output, strategy="flag", exit_code=exit_code)
        return None

    # Multi-strategy mode
    strategies: list[tuple[str, list[str]]] = [
        ("flag", ["--help"]),
        ("short_flag", ["-h"]),
        ("subcommand", ["help"]),
        ("bare", []),
    ]

    for strategy_name, args in strategies:
        output, exit_code = _try_capture(tool, args, timeout)
        if output and looks_like_help(output):
            return HelpCapture(
                output=output,
                strategy=strategy_name,
                exit_code=exit_code,
            )

    return None


def capture_subcommand_help(
    tool: str,
    subcommand: str,
    timeout: int = 10,
) -> str | None:
    """Capture help for a specific subcommand.

    Args:
        tool: Tool name
        subcommand: Subcommand to get help for
        timeout: Command timeout

    Returns:
        Help output or None
    """
    # Try common patterns for subcommand help
    patterns: list[list[str]] = [
        [subcommand, "--help"],
        [subcommand, "-h"],
        ["help", subcommand],
    ]

    for args in patterns:
        output, _ = _try_capture(tool, args, timeout)
        if output and looks_like_help(output):
            return output

    return None


def discover_subcommands(
    tool: str,
    help_text: str,
    depth: int = 1,
    timeout: int = 10,
) -> dict[str, str | None]:
    """Discover and capture help for subcommands.

    Args:
        tool: Tool name
        help_text: Main help output to parse for subcommands
        depth: How many levels deep to discover (1 = direct subcommands only)
        timeout: Command timeout

    Returns:
        Dict mapping subcommand name to its help text (or None if capture failed)
    """
    subcommands = _parse_subcommands(help_text)
    result: dict[str, str | None] = {}

    for subcmd in subcommands:
        subcmd_help = capture_subcommand_help(tool, subcmd, timeout)
        result[subcmd] = subcmd_help

        # Recursive discovery if depth > 1
        if depth > 1 and subcmd_help:
            nested = discover_subcommands(
                f"{tool} {subcmd}",
                subcmd_help,
                depth=depth - 1,
                timeout=timeout,
            )
            for nested_name, nested_help in nested.items():
                result[f"{subcmd} {nested_name}"] = nested_help

    return result


def _parse_subcommands(help_text: str) -> list[str]:
    """Parse subcommand names from help output.

    Handles various CLI frameworks:
    - Click/Typer: "Commands:" section with indented commands
    - Git: "available git commands" with column layout
    - Docker: "Commands:" or "Management Commands:" sections
    - Cobra (Go): "Available Commands:" section
    - argparse: "subcommands:" or "positional arguments:" section

    Args:
        help_text: Help output to parse

    Returns:
        List of subcommand names
    """
    subcommands: list[str] = []

    # Section headers that indicate command listings
    command_headers = [
        "commands:",
        "available commands:",
        "subcommands:",
        "management commands:",
        "available git commands",
        "main porcelain commands",
        "ancillary commands",
    ]

    # Git uses descriptive section headers - these indicate command sections too
    git_section_patterns = [
        "start a working area",
        "work on the current change",
        "examine the history",
        "grow, mark and tweak",
        "collaborate",
        "branch",
        "merge",
    ]

    # Headers that end a commands section
    end_headers = [
        "options:",
        "flags:",
        "global options:",
        "environment:",
        "examples:",
        "see also:",
        "learn more:",
        "'git help",  # Git's help hint at end
    ]

    lines = help_text.split("\n")
    in_commands_section = False

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        # Detect commands section header
        if any(h in line_lower for h in command_headers):
            in_commands_section = True
            continue

        # Detect Git-style section headers (they contain "see also:")
        if any(p in line_lower for p in git_section_patterns):
            in_commands_section = True
            continue

        # Detect end of commands section
        if in_commands_section:
            # Check for end headers
            if any(h in line_lower for h in end_headers):
                in_commands_section = False
                continue

            # Skip empty lines but don't exit section
            if not line_stripped:
                continue

            # New non-indented header ends section (but not Git descriptive ones)
            if (
                line_stripped.endswith(":")
                and not line.startswith(" ")
                and not line.startswith("\t")
            ):
                # Check if it's another command section
                if any(h in line_lower for h in command_headers):
                    continue  # Stay in commands mode
                in_commands_section = False
                continue

            # Parse command name (first word, usually indented)
            # Handle both "  cmd  Description" and "   cmd" formats
            if line.startswith(" ") or line.startswith("\t"):
                parts = line_stripped.split()
                if parts:
                    cmd_name = parts[0].rstrip(",")
                    # Skip if it looks like an option, description, or meta
                    if (
                        not cmd_name.startswith("-")
                        and not cmd_name.startswith("(")
                        and not cmd_name.startswith("[")
                        and not cmd_name.startswith("'")
                        and _is_valid_command_name(cmd_name)
                        and cmd_name not in subcommands
                    ):
                        subcommands.append(cmd_name)

    return subcommands


def _is_valid_command_name(name: str) -> bool:
    """Check if a string looks like a valid command name.

    Args:
        name: Potential command name

    Returns:
        True if it looks like a command name
    """
    if not name:
        return False
    # Must start with letter or underscore
    if not (name[0].isalpha() or name[0] == "_"):
        return False
    # Allow letters, numbers, underscores, and hyphens
    return all(c.isalnum() or c in "_-" for c in name)
