from __future__ import annotations

import json
import os
from typing import Any

from pith.core import Argument, Command, Option, PithSchema, Tier1, Tier2, Tier3

from ..heuristic import heuristic_analyze

# Prompt template for OpenAI GPT
ANALYSIS_PROMPT = """You are analyzing CLI help output to generate a progressive discovery schema for AI agents.

Tool name: {tool}

Help output:
{help_output}

Subcommands:
{subcommands}

Generate a pith schema following these rules:

1. **pith** (tool level): One line, max 60 chars, captures the tool's essence
2. **tier1** per command: One-line summary + execution syntax
3. **tier2** per command: All arguments and options with concise descriptions (max 40 chars)
4. **tier3** per command: 3-5 realistic examples showing common use cases, related commands
5. **intents** per command: 3-5 natural language phrases an agent might use to find this command

RUN-LINE FORMAT (critical for agents to construct commands):
- Required positional args: <arg_name> (e.g., <src>, <dest>, <file>)
- Optional positional args: [<arg_name>] (e.g., [<path>])
- Boolean flags: [-f/--force] (short and long forms)
- Options with values: [--output <path>] or [-o <file>]
- Example: "{tool} copy <src> <dest> [-r] [-f/--force] [--exclude <pattern>]"

INTENTS GUIDANCE (for semantic search):
- Use natural language phrases like "copy files", "backup directory", "sync folders"
- Include action verbs and domain terms
- Think: what would someone type to find this command?

EXAMPLE GUIDANCE:
- Show complete, runnable commands with realistic values
- Cover common scenarios (basic use, with options, edge cases)
- Use realistic file paths, names, and values

Output valid JSON with this structure:
{{
  "tool": "{tool}",
  "pith": "One-line description",
  "commands": {{
    "command_name": {{
      "pith": "Short description",
      "tier1": {{"summary": "What this command does", "run": "{tool} cmd <required_arg> [<optional_arg>] [-o/--option]"}},
      "tier2": {{
        "arguments": [{{"name": "arg", "description": "desc", "type": "path|text|integer", "required": true}}],
        "options": [{{"name": "option", "aliases": ["-o", "--option"], "description": "desc", "type": "flag|text|path"}}]
      }},
      "tier3": {{
        "examples": ["{tool} cmd file.txt", "{tool} cmd -o output.txt input.txt"],
        "related": ["other_cmd"]
      }},
      "intents": ["natural phrase to find this", "another way to describe it"]
    }}
  }}
}}

IMPORTANT:
- Keep descriptions concise — agents pay per token
- Generate realistic examples even if not in the original help
- Infer argument types from context (path, text, integer, etc.)
- Output ONLY valid JSON, no markdown or explanation"""


class OpenAIProvider:
    """OpenAI GPT provider for help text analysis."""

    name = "openai"

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: str | None = None,
        api_key_env: str = "OPENAI_API_KEY",
    ) -> None:
        self.model = model
        self.api_key = api_key or os.environ.get(api_key_env)

    def analyze_help(
        self,
        tool: str,
        help_output: str,
        subcommands: list[str] | None = None,
    ) -> PithSchema:
        """Analyze help using OpenAI GPT.

        Falls back to heuristic parsing if API call fails.
        """
        if not self.api_key:
            return heuristic_analyze(tool, help_output, subcommands)

        try:
            import openai
        except ImportError:
            return heuristic_analyze(tool, help_output, subcommands)

        try:
            client = openai.OpenAI(api_key=self.api_key)
            prompt = ANALYSIS_PROMPT.format(
                tool=tool,
                help_output=help_output,
                subcommands="\n".join(subcommands or []),
            )

            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content or ""
            return self._parse_response(tool, content, help_output, subcommands)

        except Exception:
            return heuristic_analyze(tool, help_output, subcommands)

    def _parse_response(
        self,
        tool: str,
        response: str,
        help_output: str,
        subcommands: list[str] | None,
    ) -> PithSchema:
        """Parse LLM JSON response into PithSchema."""
        try:
            data: dict[str, Any] = json.loads(response.strip())
            return self._dict_to_schema(data)
        except (json.JSONDecodeError, KeyError, TypeError):
            return heuristic_analyze(tool, help_output, subcommands)

    def _dict_to_schema(self, data: dict[str, Any]) -> PithSchema:
        """Convert parsed dict to PithSchema."""
        commands: dict[str, Command] = {}

        for name, cmd_data in data.get("commands", {}).items():
            tier1_data = cmd_data.get("tier1", {})
            tier1 = Tier1(
                summary=tier1_data.get("summary", name),
                run=tier1_data.get("run", f"{data.get('tool', 'tool')} {name}"),
            )

            tier2 = None
            if tier2_data := cmd_data.get("tier2"):
                arguments = [
                    Argument(
                        name=arg["name"],
                        description=arg.get("description", arg["name"]),
                        type=arg.get("type", "text"),
                        required=arg.get("required", True),
                        default=arg.get("default"),
                    )
                    for arg in tier2_data.get("arguments", [])
                ]
                options = [
                    Option(
                        name=opt["name"],
                        aliases=opt.get("aliases", []),
                        description=opt.get("description", opt["name"]),
                        type=opt.get("type", "text"),
                        required=opt.get("required", False),
                        default=opt.get("default"),
                    )
                    for opt in tier2_data.get("options", [])
                ]
                tier2 = Tier2(arguments=arguments, options=options)

            tier3 = None
            if tier3_data := cmd_data.get("tier3"):
                tier3 = Tier3(
                    examples=tier3_data.get("examples", []),
                    related=tier3_data.get("related", []),
                )

            commands[name] = Command(
                name=name,
                pith=cmd_data.get("pith", name),
                tier1=tier1,
                tier2=tier2,
                tier3=tier3,
                intents=cmd_data.get("intents", []),
            )

        return PithSchema(
            tool=data.get("tool", "tool"),
            pith=data.get("pith", "CLI tool"),
            commands=commands,
            schema_version="1.0",
        )
