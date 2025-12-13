from __future__ import annotations

from pathlib import Path


class File:
    """
    Desc:
        Represents a file with path resolution and validation.

    Params:
        path: str | Path: File path as string or Path object

    Methods:
        is_exist: Check if file exists
        is_file: Check if path points to a file
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:
        self.path = self._resolve_path(path)
        self.name = self._resolve_name()

    def _resolve_path(
        self,
        path: str | Path,
    ) -> Path:
        path = Path(path).expanduser()
        try:
            path = path.resolve(strict=False)
        except Exception:
            path = path.absolute()
        return path

    def _resolve_name(self) -> str:
        return self.path.stem

    def is_exist(self) -> bool:
        return self.path.exists()

    def is_file(self) -> bool:
        return self.path.is_file()
