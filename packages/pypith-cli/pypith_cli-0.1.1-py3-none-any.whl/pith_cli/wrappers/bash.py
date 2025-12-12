from __future__ import annotations

from pathlib import Path

from pith.core import PithSchema

from .base import ensure_executable


class BashWrapper:
    """Generate Bash wrapper script for progressive discovery."""

    def __init__(self, schema: PithSchema, original_path: str) -> None:
        self.schema = schema
        self.original_path = original_path

    def write(self, root: Path) -> Path:
        path = root / "bin" / self.schema.tool
        path.parent.mkdir(parents=True, exist_ok=True)

        # Generate wrapper script that:
        # - Bare command → tier 0
        # - pith subcommand → tier 1-3 based on -v flags
        # - All other commands → passthrough to original
        content = f'''#!/usr/bin/env bash
set -euo pipefail

PITH_TOOL="{self.schema.tool}"
PITH_ORIGINAL="{self.original_path}"
PITH_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/.." && pwd)"

# Bare command: show tier 0
if [[ $# -eq 0 ]]; then
    pith query "$PITH_TOOL" --tier 0 --schema-dir "$PITH_DIR/schemas"
    exit 0
fi

# pith subcommand: progressive discovery
if [[ "$1" == "pith" ]]; then
    shift

    # Default tier 1, -v for tier 2, -vv for tier 3
    tier=1
    json_flag=""
    find_query=""
    command_name=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -vv)
                tier=3
                shift
                ;;
            -v)
                tier=2
                shift
                ;;
            --json)
                json_flag="--json"
                shift
                ;;
            --find)
                find_query="$2"
                shift 2
                ;;
            -*)
                echo "Unknown option: $1" >&2
                exit 1
                ;;
            *)
                command_name="$1"
                shift
                ;;
        esac
    done

    if [[ -n "$find_query" ]]; then
        pith query "$PITH_TOOL" --find "$find_query" $json_flag --schema-dir "$PITH_DIR/schemas"
    elif [[ -n "$command_name" ]]; then
        pith query "$PITH_TOOL" "$command_name" --tier "$tier" $json_flag --schema-dir "$PITH_DIR/schemas"
    else
        pith query "$PITH_TOOL" --tier 0 $json_flag --schema-dir "$PITH_DIR/schemas"
    fi
    exit 0
fi

# Passthrough to original tool
exec "$PITH_ORIGINAL" "$@"
'''

        path.write_text(content, encoding="utf-8")
        ensure_executable(path)
        return path
