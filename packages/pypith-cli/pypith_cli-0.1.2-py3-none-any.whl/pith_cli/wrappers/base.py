from __future__ import annotations

from pathlib import Path
from typing import Protocol

from pith.core import PithSchema


class WrapperGenerator(Protocol):
    schema: PithSchema
    original_path: str

    def write(self, root: Path) -> Path: ...


def ensure_executable(path: Path) -> None:
    mode = path.stat().st_mode
    path.chmod(mode | 0o111)
