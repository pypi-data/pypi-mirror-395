from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Dict, Optional

from xcloudmeta.base.file import File
from xcloudmeta.base.modulekind import ModuleKind


class MetaFile(File):
    """
    Desc:
        Represents a TOML metadata file with automatic parsing and module kind resolution.

    Params:
        path: str | Path: Path to the TOML metadata file
        kind: Optional[str | ModuleKind]: Module type identifier
        data: Optional[Dict]: Pre-loaded metadata dictionary

    Methods:
        Inherits all methods from File class
    """

    def __init__(
        self,
        path: str | Path,
        kind: Optional[str | ModuleKind] = None,
        data: Optional[Dict] = None,
    ):
        super().__init__(path)
        self.kind = self._resolve_kind(kind)
        self.data = self._resolve_data(data)

    def _resolve_kind(
        self,
        kind: Optional[str | ModuleKind] = None,
    ) -> ModuleKind:
        if kind is None:
            return ModuleKind.UNDEFINED
        if isinstance(kind, ModuleKind):
            return kind
        if isinstance(kind, str):
            return ModuleKind.from_str(kind)
        return ModuleKind.UNDEFINED

    def _resolve_data(
        self,
        data: Optional[Dict] = None,
    ) -> Dict:
        if data and isinstance(data, Dict):
            return data
        else:
            if not self.path.exists() or not self.path.is_file():
                return {}
            try:
                with self.path.open("rb") as f:
                    return tomllib.load(f)
            except Exception:
                raise IOError(f"Fail to read from: {self.path}")
