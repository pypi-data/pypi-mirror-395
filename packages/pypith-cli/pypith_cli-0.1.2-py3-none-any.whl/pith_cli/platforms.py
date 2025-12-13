from __future__ import annotations

import os
import platform
import shutil
import sys
from pathlib import Path


def default_shell_extension() -> str:
    """Get default script extension for current platform."""
    system = platform.system().lower()
    if system == "windows":
        return ".cmd"
    if system in {"darwin", "linux"}:
        return ""
    return ""


def get_pith_dir(root: Path | None = None) -> Path:
    """Get .pith directory in current working directory or specified root.

    Args:
        root: Optional root path (defaults to cwd)

    Returns:
        Path to .pith directory
    """
    if root is None:
        root = Path.cwd()
    return root / ".pith"


def get_global_pith_dir() -> Path:
    """Get global ~/.pith directory for user-wide configuration.

    Returns:
        Path to ~/.pith directory
    """
    return Path.home() / ".pith"


def get_bin_dir(root: Path | None = None) -> Path:
    """Get wrapper scripts directory.

    Args:
        root: Optional root path (defaults to cwd)

    Returns:
        Path to .pith/bin directory
    """
    return get_pith_dir(root) / "bin"


def get_schemas_dir(root: Path | None = None) -> Path:
    """Get schemas directory.

    Args:
        root: Optional root path (defaults to cwd)

    Returns:
        Path to .pith/schemas directory
    """
    return get_pith_dir(root) / "schemas"


def bin_path(root: Path) -> Path:
    """Legacy alias for get_bin_dir."""
    return root / "bin"


def get_original_path(tool: str, exclude_pith_bin: bool = True) -> Path | None:
    """Find original tool path, excluding pith wrapper.

    Searches PATH for the tool executable, optionally excluding
    the .pith/bin directory to find the real binary.

    Args:
        tool: Tool name to find
        exclude_pith_bin: Whether to exclude .pith/bin from search

    Returns:
        Path to original tool, or None if not found
    """
    pith_bin = str(get_bin_dir())

    # Get PATH entries
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)

    for path_dir in path_dirs:
        if exclude_pith_bin and path_dir == pith_bin:
            continue

        candidate = Path(path_dir) / tool
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate

        # Windows: check .exe, .cmd, .bat extensions
        if sys.platform == "win32":
            for ext in [".exe", ".cmd", ".bat"]:
                candidate = Path(path_dir) / f"{tool}{ext}"
                if candidate.is_file():
                    return candidate

    return None


def find_tool(tool: str) -> Path | None:
    """Find tool using shutil.which, excluding pith wrappers.

    Args:
        tool: Tool name to find

    Returns:
        Path to tool, or None if not found
    """
    # First try shutil.which
    result = shutil.which(tool)
    if result is None:
        return None

    result_path = Path(result)

    # Check if it's our wrapper
    pith_bin = get_bin_dir()
    if pith_bin.exists() and result_path.parent == pith_bin:
        # It's our wrapper, search PATH manually excluding pith/bin
        return get_original_path(tool, exclude_pith_bin=True)

    return result_path


def detect_shell() -> str:
    """Detect current shell for activation command.

    On Windows, prefer:
      1. 'cmd' if COMSPEC env var points to cmd.exe,
      2. 'powershell' if PSModulePath is present (explicit PS env),
      3. 'powershell' if pwsh/powershell is found in PATH,
      4. fall back to 'cmd'.
    On Unix-like systems, use the SHELL env var basename and fall back to 'sh'.

    Returns:
        Shell name (bash, zsh, fish, powershell, cmd, sh)
    """
    if sys.platform == "win32":
        # If COMSPEC points to cmd.exe -> cmd (check first, most reliable)
        comspec = os.environ.get("COMSPEC", "")
        if comspec:
            basename = Path(comspec).name.lower()
            if basename in ("cmd.exe", "cmd"):
                return "cmd"

        # Explicit PowerShell environment
        if os.environ.get("PSModulePath"):  # noqa: SIM112
            return "powershell"

        # If PowerShell binary is available in PATH -> powershell
        if (
            shutil.which("pwsh")
            or shutil.which("pwsh.exe")
            or shutil.which("powershell.exe")
        ):
            return "powershell"

        # Default to cmd on Windows
        return "cmd"

    shell = os.environ.get("SHELL", "").lower()
    if "zsh" in shell:
        return "zsh"
    elif "fish" in shell:
        return "fish"
    elif "bash" in shell:
        return "bash"

    return "sh"


def get_activation_command(shell: str | None = None) -> str:
    """Get shell-specific PATH activation command.

    Args:
        shell: Shell name (auto-detected if None)

    Returns:
        Shell command to add .pith/bin to PATH
    """
    if shell is None:
        shell = detect_shell()

    pith_bin = get_bin_dir()

    commands = {
        "bash": f'export PATH="{pith_bin}:$PATH"',
        "zsh": f'export PATH="{pith_bin}:$PATH"',
        "fish": f'set -gx PATH "{pith_bin}" $PATH',
        "powershell": f'$env:PATH = "{pith_bin};$env:PATH"',
        "cmd": f"set PATH={pith_bin};%PATH%",
        "sh": f'export PATH="{pith_bin}:$PATH"',
    }

    return commands.get(shell, commands["sh"])
