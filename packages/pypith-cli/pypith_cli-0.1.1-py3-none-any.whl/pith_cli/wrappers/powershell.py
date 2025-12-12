from __future__ import annotations

from pathlib import Path

from pith.core import PithSchema

from .base import ensure_executable


class PowerShellWrapper:
    """Generate PowerShell wrapper script for progressive discovery."""

    def __init__(self, schema: PithSchema, original_path: str) -> None:
        self.schema = schema
        self.original_path = original_path

    def write(self, root: Path) -> Path:
        path = root / "bin" / f"{self.schema.tool}.ps1"
        path.parent.mkdir(parents=True, exist_ok=True)

        # Generate wrapper script that:
        # - Bare command → tier 0
        # - pith subcommand → tier 1-3 based on -v flags
        # - All other commands → passthrough to original
        content = f'''$ErrorActionPreference = "Stop"

$PITH_TOOL = "{self.schema.tool}"
$PITH_ORIGINAL = "{self.original_path}"
$PITH_DIR = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Bare command: show tier 0
if ($args.Length -eq 0) {{
    pith query $PITH_TOOL --tier 0 --schema-dir "$PITH_DIR\\schemas"
    exit 0
}}

# pith subcommand: progressive discovery
if ($args[0] -eq "pith") {{
    $remaining = $args[1..($args.Length - 1)]
    $tier = 1
    $jsonFlag = ""
    $findQuery = ""
    $commandName = ""

    $i = 0
    while ($i -lt $remaining.Length) {{
        switch ($remaining[$i]) {{
            "-vv" {{
                $tier = 3
                $i++
            }}
            "-v" {{
                $tier = 2
                $i++
            }}
            "--json" {{
                $jsonFlag = "--json"
                $i++
            }}
            "--find" {{
                $findQuery = $remaining[$i + 1]
                $i += 2
            }}
            default {{
                if ($remaining[$i].StartsWith("-")) {{
                    Write-Error "Unknown option: $($remaining[$i])"
                    exit 1
                }}
                $commandName = $remaining[$i]
                $i++
            }}
        }}
    }}

    if ($findQuery) {{
        pith query $PITH_TOOL --find $findQuery $jsonFlag --schema-dir "$PITH_DIR\\schemas"
    }} elseif ($commandName) {{
        pith query $PITH_TOOL $commandName --tier $tier $jsonFlag --schema-dir "$PITH_DIR\\schemas"
    }} else {{
        pith query $PITH_TOOL --tier 0 $jsonFlag --schema-dir "$PITH_DIR\\schemas"
    }}
    exit 0
}}

# Passthrough to original tool
& $PITH_ORIGINAL @args
'''

        path.write_text(content, encoding="utf-8")
        ensure_executable(path)
        return path
