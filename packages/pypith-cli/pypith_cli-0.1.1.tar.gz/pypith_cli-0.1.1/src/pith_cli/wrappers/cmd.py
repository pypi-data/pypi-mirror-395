from __future__ import annotations

from pathlib import Path

from pith.core import PithSchema

from .base import ensure_executable


class CmdWrapper:
    """Generate Windows CMD wrapper that delegates to PowerShell script."""

    def __init__(self, schema: PithSchema, original_path: str) -> None:
        self.schema = schema
        self.original_path = original_path

    def write(self, root: Path) -> Path:
        path = root / "bin" / f"{self.schema.tool}.cmd"
        path.parent.mkdir(parents=True, exist_ok=True)

        # CMD wrapper simply invokes the PowerShell script
        # This ensures consistent behavior across both shells
        content = f"""@echo off
setlocal

set PITH_DIR=%~dp0..
set SCRIPT_PATH=%~dp0{self.schema.tool}.ps1

if exist "%SCRIPT_PATH%" (
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_PATH%" %*
) else (
    echo Error: PowerShell wrapper not found: %SCRIPT_PATH% >&2
    exit /b 1
)
"""

        path.write_text(content, encoding="utf-8")
        ensure_executable(path)
        return path
