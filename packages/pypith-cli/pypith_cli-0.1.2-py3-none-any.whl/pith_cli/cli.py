"""pith-cli: Wrap existing tools for agent-friendly progressive discovery.

This CLI is itself built with the Pith library, enabling agents to discover
pith-cli's own commands using the same progressive discovery pattern.
"""

from __future__ import annotations

import json
from pathlib import Path

from pith import Argument, Option, Pith, PithException, confirm, echo, prompt
from pith.core import Argument as SchemaArgument
from pith.core import Command as CoreCommand
from pith.core import Option as SchemaOption
from pith.core import PithSchema, SchemaMetadata, Tier1, Tier2, Tier3

from .analyze import analyze_help
from .capture import capture_help, discover_subcommands
from .config import (
    DEFAULT_API_KEY_ENVS,
    DEFAULT_HOME,
    DEFAULT_MODELS,
    ensure_home,
    list_wrapped_tools,
    load_config,
    load_global_config,
    load_schema,
    save_config,
    schema_path,
    validate_api_key,
)
from .diff import compare_schemas
from .platforms import detect_shell, find_tool, get_activation_command
from .providers import ProviderName
from .query import OutputFormat, render, search
from .wrappers import BashWrapper, CmdWrapper, PowerShellWrapper

# --- Pith App Definition ---

app = Pith(
    name="pith",
    pith="Agent-friendly CLI wrappers: init to configure, wrap <tool> to add tools, find to search",
)


# --- Commands ---


@app.command(pith="Configure LLM provider - first step for new users", priority=10)
@app.intents(
    "setup pith",
    "configure llm",
    "set api key",
    "initialize",
    "first time setup",
    "configure api",
    "change provider",
    "getting started",
    "how to start",
    "new user setup",
    "connect to openai",
    "connect to anthropic",
    "use ollama",
    "set model",
    "switch llm",
    "configure settings",
    "what provider am I using",
    "authentication",
)
def init(
    provider: str | None = Option(
        None,
        "--provider",
        pith="LLM provider: anthropic, openai, ollama, or none",
    ),
    model: str | None = Option(None, "--model", pith="Model name override"),
    api_key_env: str | None = Option(
        None, "--api-key-env", pith="Environment variable for API key"
    ),
) -> None:
    """Configure pith with LLM provider settings.

    Sets up the LLM provider used for analyzing CLI help output.
    Run interactively (no flags) for guided setup, or use flags
    for non-interactive configuration.

    Examples:
        $ pith init
        $ pith init --provider anthropic --model claude-sonnet-4-20250514
        $ pith init --provider none

    Related:
        wrap - Wrap a CLI tool after configuration
    """
    config = load_global_config()
    providers = ["anthropic", "openai", "ollama", "none"]

    # Interactive mode if provider not specified
    if provider is None:
        provider = prompt("LLM Provider", default=config.provider, choices=providers)
    elif provider not in providers:
        raise PithException(
            f"Invalid provider: {provider}. Choose from: {', '.join(providers)}"
        )

    config.provider = provider  # type: ignore[assignment]

    # Model with provider-specific default
    if model is None and provider != "none":
        default_model = config.model or DEFAULT_MODELS.get(provider) or ""
        model = prompt("Model", default=default_model)
    config.model = model if provider != "none" else None

    # API key env (skip for ollama/none)
    if api_key_env is None and provider not in ("none", "ollama"):
        default_env = config.api_key_env or DEFAULT_API_KEY_ENVS.get(provider) or ""
        api_key_env = prompt("API key environment variable", default=default_env)
    config.api_key_env = api_key_env if provider not in ("none", "ollama") else None

    # Validate API key
    if not validate_api_key(config):
        echo(f"Warning: {config.api_key_env} not set in environment", err=True)

    # Save (silently overwrites)
    path = save_config(config)
    echo(f"Configuration saved to {path}")


@app.command(
    pith="Wrap a CLI tool for agent-friendly progressive discovery",
    priority=20,
    aliases=["w"],
)
@app.intents(
    "wrap tool",
    "add wrapper",
    "enable discovery",
    "analyze cli",
    "make tool agent-friendly",
    "add tool to pith",
    "enable pith for tool",
    "how to wrap",
    "analyze help output",
    "create schema for tool",
)
def wrap(
    tool: str = Argument(..., pith="Name of the CLI tool to wrap"),
    as_name: str | None = Option(
        None, "--as", pith="Create wrapper with different name"
    ),
    pith_text: str | None = Option(None, "--pith", pith="One-line summary override"),
    provider: str | None = Option(
        None, "--provider", pith="LLM provider: anthropic, openai, ollama, none"
    ),
    model: str | None = Option(None, "--model", pith="Model override for LLM provider"),
    deep: bool = Option(False, "--deep", pith="Recursively analyze subcommands"),
    depth: int | None = Option(None, "--depth", pith="Subcommand discovery depth"),
    no_llm: bool = Option(False, "--no-llm", pith="Use heuristic parsing only"),
    force: bool = Option(False, "-f", "--force", pith="Overwrite existing wrapper"),
    timeout: int | None = Option(
        None, "--timeout", pith="Help capture timeout in seconds"
    ),
) -> None:
    """Wrap a CLI tool by capturing help and generating a schema.

    Analyzes the tool's help output using an LLM (or heuristic fallback)
    to generate a schema with progressive discovery tiers. Creates
    wrapper scripts for Bash, PowerShell, and CMD.

    Examples:
        $ pith wrap git                      # Basic wrapping
        $ pith wrap kubectl --deep --depth 2 # Deep subcommand analysis
        $ pith wrap docker --as dkr          # Create alias wrapper
        $ pith wrap npm --no-llm             # Fast heuristic-only mode
        $ pith wrap terraform --provider anthropic  # Specify provider

    Related:
        unwrap - Remove a wrapped tool
        refresh - Re-analyze and update a wrapper
        list - Show all wrapped tools
        init - Configure LLM provider first
    """
    # Load config with precedence: CLI flags > env vars > local config > global config > defaults
    config = load_config()

    # Apply CLI overrides (highest priority)
    resolved_provider = provider if provider is not None else config.provider
    resolved_model = model if model is not None else config.model
    resolved_depth = depth if depth is not None else config.default_depth
    resolved_timeout = timeout if timeout is not None else config.timeout

    home = ensure_home(DEFAULT_HOME)
    wrapper_name = as_name or tool
    existing = schema_path(wrapper_name, home)

    if existing.exists() and not force:
        raise PithException(
            f"Wrapper for {wrapper_name} already exists. Use --force to overwrite."
        )

    # Find original tool path
    echo(f"Finding {tool}...")
    original_path = find_tool(tool)
    if original_path is None:
        raise PithException(f"Could not find {tool} in PATH")
    echo(f"  ✓ Found at {original_path}")

    # Capture help output using multi-strategy approach
    echo("Capturing help output...")
    help_capture = capture_help(tool, timeout=resolved_timeout)
    if help_capture is None:
        raise PithException(f"Could not capture help for {tool}")
    echo(f"  ✓ Captured using {help_capture.strategy} strategy")

    # Discover subcommands if --deep flag is set
    subcommands: list[str] | None = None
    subcommand_helps: dict[str, str | None] | None = None
    if deep:
        echo(f"Discovering subcommands (depth={resolved_depth})...")
        subcommand_helps = discover_subcommands(
            tool, help_capture.output, depth=resolved_depth, timeout=resolved_timeout
        )
        subcommands = list(subcommand_helps.keys())
        echo(f"  ✓ Found {len(subcommands)} subcommands")

    # Analyze with LLM or heuristic
    echo("Analyzing help output...")
    provider_name: ProviderName = "none" if no_llm else resolved_provider  # type: ignore[assignment]
    schema = analyze_help(
        wrapper_name,
        help_capture.output,
        subcommands=subcommands,
        provider=provider_name,
        model=resolved_model,
    )
    echo(f"  ✓ Generated schema with {len(schema.commands)} commands")

    # Override pith if specified
    if pith_text:
        schema.pith = pith_text
        for cmd in schema.commands.values():
            cmd.pith = pith_text
            cmd.tier1.summary = pith_text

    # Add metadata
    schema.metadata = SchemaMetadata.create(
        original_path=str(original_path),
        generator="pith-cli",
    )

    # Save schema
    path = schema_path(wrapper_name, home)
    path.write_text(json.dumps(schema.to_dict(), indent=2), encoding="utf-8")
    echo(f"  ✓ Saved schema to {path}")

    # Generate wrappers
    echo("Generating wrappers...")
    BashWrapper(schema, str(original_path)).write(home)
    PowerShellWrapper(schema, str(original_path)).write(home)
    CmdWrapper(schema, str(original_path)).write(home)
    echo("  ✓ Generated Bash, PowerShell, and CMD wrappers")

    echo(f"\n✓ Wrapped {tool}" + (f" as {wrapper_name}" if as_name else ""))
    echo('\nTo activate, run: eval "$(pith activate)"')


@app.command(
    name="list",
    pith="List all wrapped tools in the pith workspace",
    priority=30,
    aliases=["ls"],
)
@app.intents(
    "show wrapped tools",
    "list wrappers",
    "what tools are wrapped",
    "see available tools",
    "show installed wrappers",
    "inventory",
    "what tools do I have",
    "show my wrappers",
    "available commands",
    "what can I use",
    "which tools",
    "ls",
    "dir",
    "show all",
)
def list_tools(
    verbose: bool = Option(False, "-v", "--verbose", pith="Show more details"),
) -> None:
    """List wrapped tools in the current workspace.

    Shows all tools that have been wrapped with pith. Use -v for
    additional details including command count and original path.

    Examples:
        $ pith list
        $ pith list -v

    Related:
        wrap - Wrap a new tool
        unwrap - Remove a wrapped tool
    """
    home = ensure_home(DEFAULT_HOME)
    tools = list_wrapped_tools(home)
    if not tools:
        echo("No tools wrapped yet.")
        return
    echo("Wrapped tools:")
    for tool in tools:
        if verbose:
            raw = load_schema(tool, home)
            if raw:
                data = json.loads(raw)
                cmd_count = len(data.get("commands", {}))
                metadata = data.get("metadata", {})
                original_path = metadata.get("original_path", "unknown")
                generator = metadata.get("generator", "unknown")
                echo(f"  {tool} ({cmd_count} commands)")
                echo(f"    path: {original_path}")
                echo(f"    generator: {generator}")
            else:
                echo(f"  {tool}")
        else:
            echo(f"- {tool}")


@app.command(
    pith="Display progressive discovery tiers for a wrapped tool",
    priority=35,
    aliases=["s"],
)
@app.intents(
    "show tool info",
    "display schema",
    "view wrapper details",
    "get tool help",
    "explore commands",
    "what can tool do",
    "how to use tool",
    "help me understand",
    "tool documentation",
    "see tool commands",
)
def show(
    tool: str = Argument(..., pith="Name of the wrapped tool"),
    command_name: str | None = Option(None, "-c", pith="Specific command to render"),
    verbosity: int = Option(
        0, "-v", pith="Tier level: 0=summary, 1=options, 2=examples"
    ),
    json_output: bool = Option(False, "--json", pith="Output as JSON"),
    query_text: str | None = Option(None, "--find", pith="Search commands by intent"),
) -> None:
    """Render stored schema tiers for a wrapped tool.

    Displays progressive discovery information for a wrapped tool.
    Use -v 1 for options (tier 2), -v 2 for examples (tier 3).

    Examples:
        $ pith show git
        $ pith show kubectl -c get -v 1
        $ pith show docker --find "run container"
        $ pith show git --json

    Related:
        query - Query tool used by wrappers
        find - Search across all tools
    """
    raw = load_schema(tool, DEFAULT_HOME)
    if raw is None:
        raise PithException(f"No schema found for {tool}")
    schema = _schema_from_json(raw)

    output_format: OutputFormat = "json" if json_output else "text"

    if query_text:
        # Semantic search mode
        echo(search(schema, query_text, output_format=output_format))
    else:
        # Standard tier rendering
        level = 1 if verbosity == 0 else min(verbosity + 1, 3)
        echo(render(schema, command_name, level, output_format=output_format))


@app.command(
    pith="Query pith info for a wrapped tool - used internally by wrappers", priority=90
)
@app.intents(
    "query wrapper",
    "get pith info",
    "lookup command",
    "internal query",
    "wrapper script query",
    "programmatic access",
)
def query(
    tool: str | None = Argument(None, pith="Name of the wrapped tool"),
    command_name: str | None = Argument(None, pith="Specific command to query"),
    tier: int = Option(1, "--tier", pith="Tier level (0-3)"),
    json_output: bool = Option(False, "--json", pith="Output as JSON"),
    query_text: str | None = Option(None, "--find", pith="Search commands by intent"),
    schema_dir: str | None = Option(None, "--schema-dir", pith="Schema directory path"),
) -> None:
    """Query pith info for a wrapped tool (used by wrappers).

    This command is called by wrapper scripts to display progressive
    discovery information. If no tool is specified with --find,
    searches across all wrapped tools.

    Examples:
        $ pith query git status --tier 2
        $ pith query kubectl --find "list pods"
        $ pith query --find "version control" --json

    Related:
        show - Interactive tool exploration
        find - Semantic search shortcut
    """
    home = Path(schema_dir).parent if schema_dir else DEFAULT_HOME
    output_format: OutputFormat = "json" if json_output else "text"

    # Global search mode: no tool specified with --find
    if tool is None:
        if query_text is None:
            raise PithException(
                "Tool argument required. Use --find <query> to search all tools."
            )
        # Search across all wrapped tools
        tools = list_wrapped_tools(home)
        if not tools:
            echo("No tools wrapped yet.")
            return

        all_results: list[str] = []
        for tool_name in tools:
            raw = load_schema(tool_name, home)
            if raw:
                schema = _schema_from_json(raw)
                result = search(
                    schema, query_text, output_format=output_format, limit=3
                )
                if result.strip():
                    all_results.append(result)

        if all_results:
            echo("\n\n".join(all_results))
        else:
            echo("No matching commands found.")
        return

    # Single tool mode
    raw = load_schema(tool, home)
    if raw is None:
        raise PithException(f"No schema found for {tool}")

    schema = _schema_from_json(raw)

    if query_text:
        echo(search(schema, query_text, output_format=output_format))
    else:
        echo(render(schema, command_name, tier, output_format=output_format))


@app.command(
    pith="Search all wrapped tools using natural language",
    priority=40,
    aliases=["f", "search"],
)
@app.intents(
    "search tools",
    "find command",
    "semantic search",
    "discover commands",
    "what command does",
    "how to do",
    "search by intent",
)
def find(
    query_text: str = Argument(..., pith="Natural language query"),
    json_output: bool = Option(False, "--json", pith="Output as JSON"),
) -> None:
    """Semantic search across all wrapped tools.

    Searches all wrapped tool schemas for commands matching your
    natural language query. Returns ranked results with relevance scores.
    This is the recommended way for agents to discover tool capabilities.

    Examples:
        $ pith find "list files"              # Find file listing commands
        $ pith find "deploy application"      # Find deployment commands
        $ pith find "version control commit"  # Find VCS commands
        $ pith find "container management"    # Cross-tool search
        $ pith find "how to delete" --json    # Agent-friendly output

    Related:
        query - Query specific tool
        show - View tool details
        list - See all wrapped tools first
    """
    home = ensure_home(DEFAULT_HOME)
    tools = list_wrapped_tools(home)

    if not tools:
        echo("No tools wrapped yet.")
        return

    output_format: OutputFormat = "json" if json_output else "text"
    all_results: list[str] = []

    for tool in tools:
        raw = load_schema(tool, home)
        if raw:
            schema = _schema_from_json(raw)
            result = search(schema, query_text, output_format=output_format, limit=3)
            if result.strip():
                all_results.append(result)

    if all_results:
        echo("\n\n".join(all_results))
    else:
        echo("No matching commands found.")


@app.command(
    pith="Add pith wrappers to shell PATH - enables wrapped tool discovery", priority=25
)
@app.intents(
    "enable wrappers",
    "add to path",
    "activate pith",
    "setup shell",
    "make wrappers available",
    "start using wrappers",
    "enable discovery",
    "configure path",
    "shell integration",
    "bashrc",
    "zshrc",
    "profile setup",
    "environment variable",
    "path configuration",
)
def activate(
    eval_mode: bool = Option(
        False, "--eval", pith="Output bare command for eval (no comments)"
    ),
) -> None:
    """Print PATH update for wrapper binaries.

    Outputs the shell command to add pith wrappers to your PATH.
    Use with --eval for shell integration.

    Examples:
        $ pith activate
        $ eval "$(pith activate --eval)"

    Related:
        wrap - Wrap a tool first
        list - See available wrappers
    """
    shell = detect_shell()
    cmd = get_activation_command(shell)
    if eval_mode:
        echo(cmd)
    else:
        echo(f"# For {shell}, run:")
        echo(cmd)


@app.command(pith="Export schema JSON for sharing or backup", priority=60)
@app.intents(
    "export schema",
    "save schema",
    "backup wrapper",
    "get json",
    "share schema",
    "download schema",
    "serialize wrapper",
    "dump schema",
    "output json",
    "save to file",
    "extract schema",
    "schema file",
)
def export(
    tool: str = Argument(..., pith="Name of the wrapped tool to export"),
    output_file: str | None = Option(None, "-o", "--output", pith="Output file path"),
    pretty: bool = Option(True, "--pretty", pith="Pretty-print JSON"),
) -> None:
    """Export schema JSON for a wrapped tool.

    Writes the schema to stdout by default. Use --output to write
    to a file. Use --no-pretty for compact JSON.

    Examples:
        $ pith export git
        $ pith export kubectl -o kubectl.pith.json
        $ pith export docker --no-pretty

    Related:
        import - Import a schema file
        show - View schema in human-readable format
    """
    raw = load_schema(tool, DEFAULT_HOME)
    if raw is None:
        raise PithException(f"No schema found for {tool}")

    # Validate schema can be parsed (fail fast)
    try:
        schema = _schema_from_json(raw)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise PithException(f"Invalid schema for {tool}: {e}") from e

    # Format output
    if pretty:
        output = json.dumps(schema.to_dict(), indent=2)
    else:
        output = json.dumps(schema.to_dict(), separators=(",", ":"))

    if output_file:
        Path(output_file).write_text(output, encoding="utf-8")
        echo(f"Exported {tool} schema to {output_file}")
    else:
        echo(output)


@app.command(
    name="import",
    pith="Import schema from a JSON file - use community schemas",
    priority=55,
)
@app.intents(
    "import schema",
    "load schema",
    "restore wrapper",
    "add from file",
    "use community schema",
    "install schema",
    "load pith json",
    "read schema file",
    "install wrapper",
    "add schema",
    "from json",
    "restore backup",
)
def import_schema(
    file: str = Argument(..., pith="Path to schema JSON file"),
    tool_name: str | None = Option(
        None, "--name", pith="Override tool name from schema"
    ),
    force: bool = Option(False, "-f", "--force", pith="Overwrite existing wrapper"),
) -> None:
    """Import schema from a JSON file and generate wrappers.

    The schema is validated before import. Use --name to override
    the tool name from the schema file.

    Examples:
        $ pith import git.pith.json
        $ pith import kubectl-schema.json --name kctl
        $ pith import docker.pith.json --force

    Related:
        export - Export a schema
        wrap - Generate schema from tool
    """
    home = ensure_home(DEFAULT_HOME)
    file_path = Path(file)

    if not file_path.exists():
        raise PithException(f"File not found: {file}")

    raw = file_path.read_text(encoding="utf-8")

    # Validate schema (fail fast)
    try:
        schema = _schema_from_json(raw)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise PithException(f"Invalid schema file: {e}") from e

    # Save original tool name for PATH lookup before potentially overriding
    original_tool_name = schema.tool

    # Override tool name if specified
    if tool_name:
        schema.tool = tool_name

    existing = schema_path(schema.tool, home)
    if existing.exists() and not force:
        raise PithException(
            f"Wrapper for {schema.tool} already exists. Use --force to overwrite."
        )

    # Get original path from metadata or try to find it (use original tool name for lookup)
    original_path = None
    if schema.metadata and schema.metadata.original_path:
        original_path = schema.metadata.original_path
    else:
        found = find_tool(original_tool_name)
        if found:
            original_path = str(found)

    if not original_path:
        raise PithException(
            f"Could not find original path for {schema.tool}. "
            "Ensure the tool is in PATH or schema includes metadata.original_path."
        )

    # Mark schema as imported with updated metadata
    schema.metadata = SchemaMetadata.create(
        original_path=original_path,
        generator="imported",
        tool_version=schema.metadata.tool_version if schema.metadata else None,
    )

    # Save schema with updated metadata
    path = schema_path(schema.tool, home)
    path.write_text(json.dumps(schema.to_dict(), indent=2), encoding="utf-8")

    BashWrapper(schema, original_path).write(home)
    PowerShellWrapper(schema, original_path).write(home)
    CmdWrapper(schema, original_path).write(home)

    echo(f"Imported {schema.tool} from {file}")
    echo(f"  ✓ Schema saved to {path}")
    echo(f"  ✓ Generated wrappers in {home / 'bin'}")


@app.command(pith="Re-analyze a wrapped tool and show changes", priority=70)
@app.intents(
    "update wrapper",
    "re-analyze tool",
    "refresh schema",
    "sync wrapper",
    "update schema",
    "tool updated",
    "new version of tool",
    "regenerate wrapper",
)
def refresh(
    tool: str = Argument(..., pith="Name of the wrapped tool to refresh"),
    provider: str | None = Option(
        None, "--provider", pith="LLM provider for re-analysis"
    ),
    model: str | None = Option(None, "--model", pith="Model override for LLM provider"),
    deep: bool = Option(False, "--deep", pith="Recursively analyze subcommands"),
    depth: int | None = Option(None, "--depth", pith="Subcommand discovery depth"),
    no_llm: bool = Option(False, "--no-llm", pith="Use heuristic parsing only"),
    yes: bool = Option(False, "-y", "--yes", pith="Apply changes without prompting"),
    timeout: int | None = Option(
        None, "--timeout", pith="Help capture timeout in seconds"
    ),
) -> None:
    """Re-analyze a wrapped tool and show changes.

    Compares the new analysis against the existing schema and displays
    a command-level diff. Use --yes to apply changes without prompting.

    Examples:
        $ pith refresh git
        $ pith refresh kubectl --deep --yes
        $ pith refresh docker --no-llm

    Related:
        wrap - Initial tool wrapping
        unwrap - Remove wrapper
    """
    home = ensure_home(DEFAULT_HOME)

    # Load existing schema
    raw = load_schema(tool, home)
    if raw is None:
        raise PithException(f"No schema found for {tool}. Use 'pith wrap' first.")

    try:
        old_schema = _schema_from_json(raw)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise PithException(f"Invalid existing schema: {e}") from e

    # Get original path from existing schema or find it
    original_path = None
    if old_schema.metadata and old_schema.metadata.original_path:
        original_path = old_schema.metadata.original_path
    else:
        found = find_tool(tool)
        if found:
            original_path = str(found)

    if not original_path:
        raise PithException(f"Could not find original path for {tool}")

    # Load config for defaults
    config = load_config()
    resolved_provider = provider if provider is not None else config.provider
    resolved_model = model if model is not None else config.model
    resolved_depth = depth if depth is not None else config.default_depth
    resolved_timeout = timeout if timeout is not None else config.timeout

    # Capture new help output
    echo(f"Re-analyzing {tool}...")
    help_capture = capture_help(tool, timeout=resolved_timeout)
    if help_capture is None:
        raise PithException(f"Could not capture help for {tool}")
    echo(f"  ✓ Captured help using {help_capture.strategy} strategy")

    # Discover subcommands if --deep flag is set
    subcommands: list[str] | None = None
    if deep:
        echo(f"Discovering subcommands (depth={resolved_depth})...")
        subcommand_helps = discover_subcommands(
            tool, help_capture.output, depth=resolved_depth, timeout=resolved_timeout
        )
        subcommands = list(subcommand_helps.keys())
        echo(f"  ✓ Found {len(subcommands)} subcommands")

    # Analyze with LLM or heuristic
    echo("Analyzing help output...")
    provider_name: ProviderName = "none" if no_llm else resolved_provider  # type: ignore[assignment]
    new_schema = analyze_help(
        tool,
        help_capture.output,
        subcommands=subcommands,
        provider=provider_name,
        model=resolved_model,
    )
    echo(f"  ✓ Generated schema with {len(new_schema.commands)} commands")

    # Compare schemas (command-level diff)
    diff = compare_schemas(old_schema, new_schema)

    if not diff.has_changes:
        echo("\nNo changes detected. Schema is up to date.")
        return

    # Display diff summary
    echo("\n" + diff.summary())

    # Prompt for confirmation unless --yes
    if not yes and not confirm("\nApply these changes?"):
        echo("Aborted.")
        return

    # Apply changes: update metadata and save
    new_schema.metadata = SchemaMetadata.create(
        original_path=original_path,
        generator="pith-cli",
        tool_version=old_schema.metadata.tool_version if old_schema.metadata else None,
    )

    path = schema_path(tool, home)
    path.write_text(json.dumps(new_schema.to_dict(), indent=2), encoding="utf-8")
    echo(f"  ✓ Updated schema at {path}")

    # Regenerate wrappers
    BashWrapper(new_schema, original_path).write(home)
    PowerShellWrapper(new_schema, original_path).write(home)
    CmdWrapper(new_schema, original_path).write(home)
    echo("  ✓ Regenerated wrappers")

    echo(f"\n✓ Refreshed {tool}")


@app.command(
    pith="Remove a wrapped tool and its generated files",
    priority=80,
    aliases=["rm"],
)
@app.intents(
    "remove wrapper",
    "delete wrapper",
    "unwrap tool",
    "clean up",
    "uninstall wrapper",
    "stop wrapping",
    "remove tool from pith",
    "delete schema",
    "rm wrapper",
    "uninstall tool",
    "disable discovery",
    "remove pith",
    "cleanup",
)
def unwrap(
    tool: str = Argument(..., pith="Name of the wrapped tool to remove"),
) -> None:
    """Remove wrapper and clean up.

    Removes the wrapper scripts and schema for a wrapped tool.
    Does not affect the original tool.

    Examples:
        $ pith unwrap git
        $ pith unwrap kubectl

    Related:
        wrap - Wrap a tool
        list - See wrapped tools
    """
    home = ensure_home(DEFAULT_HOME)
    removed: list[str] = []
    errors: list[str] = []

    # Remove schema
    schema_file = schema_path(tool, home)
    if schema_file.exists():
        try:
            schema_file.unlink()
            removed.append(str(schema_file))
        except OSError as e:
            errors.append(f"Failed to remove {schema_file}: {e}")

    # Remove wrappers
    bin_dir = home / "bin"
    for wrapper in [tool, f"{tool}.ps1", f"{tool}.cmd"]:
        wrapper_path = bin_dir / wrapper
        if wrapper_path.exists():
            try:
                wrapper_path.unlink()
                removed.append(str(wrapper_path))
            except OSError as e:
                errors.append(f"Failed to remove {wrapper_path}: {e}")

    # Clean up empty directories (bin/ and schemas/, but not config or root)
    schemas_dir = home / "schemas"
    for directory in [bin_dir, schemas_dir]:
        if directory.exists() and directory.is_dir():
            try:
                # Check if directory is empty (no files or subdirs)
                if not any(directory.iterdir()):
                    directory.rmdir()
            except OSError:
                # Ignore errors when cleaning empty directories
                pass

    # Report results
    if removed:
        echo(f"Removed {tool}:")
        for path in removed:
            echo(f"  - {path}")
    else:
        echo(f"No wrapper found for {tool}")

    # Report errors (continue despite errors)
    for error in errors:
        echo(f"Warning: {error}", err=True)


# --- Helper Functions ---


def _schema_from_json(content: str) -> PithSchema:
    """Parse a PithSchema from JSON content."""
    data = json.loads(content)
    commands: dict[str, CoreCommand] = {}
    for name, raw_command in data.get("commands", {}).items():
        tier1_data = raw_command.get("tier1", {})
        tier1 = Tier1(
            summary=tier1_data.get("summary", name),
            run=tier1_data.get("run", f"{data.get('tool', name)} {name}"),
        )

        tier2_data = raw_command.get("tier2") or {}
        arguments = [
            SchemaArgument(
                name=arg["name"],
                description=arg.get("description", arg["name"]),
                type=arg.get("type", "text"),
                required=bool(arg.get("required", False)),
                default=arg.get("default"),
            )
            for arg in tier2_data.get("arguments", [])
        ]
        options = [
            SchemaOption(
                name=opt["name"],
                aliases=list(opt.get("aliases", [])),
                description=opt.get("description", opt["name"]),
                type=opt.get("type", "text"),
                required=bool(opt.get("required", False)),
                default=opt.get("default"),
            )
            for opt in tier2_data.get("options", [])
        ]
        tier2 = (
            Tier2(arguments=arguments, options=options)
            if arguments or options
            else None
        )

        tier3_data = raw_command.get("tier3") or {}
        tier3 = None
        if tier3_data.get("examples") or tier3_data.get("related"):
            tier3 = Tier3(
                examples=list(tier3_data.get("examples", [])),
                related=list(tier3_data.get("related", [])),
            )

        commands[name] = CoreCommand(
            name=name,
            pith=raw_command.get("pith", name),
            tier1=tier1,
            tier2=tier2,
            tier3=tier3,
            intents=list(raw_command.get("intents", [])),
        )

    # Parse metadata if present
    metadata = None
    if "metadata" in data:
        meta_data = data["metadata"]
        metadata = SchemaMetadata(
            original_path=meta_data.get("original_path"),
            tool_version=meta_data.get("tool_version"),
            generated_at=meta_data.get("generated_at"),
            generator=meta_data.get("generator"),
        )

    return PithSchema(
        tool=data.get("tool", "tool"),
        pith=data.get("pith", ""),
        commands=commands,
        schema_version=str(data.get("schema_version", "1.0")),
        metadata=metadata,
    )


def main() -> None:
    """Entry point for pith-cli."""
    app.run()


if __name__ == "__main__":
    main()
