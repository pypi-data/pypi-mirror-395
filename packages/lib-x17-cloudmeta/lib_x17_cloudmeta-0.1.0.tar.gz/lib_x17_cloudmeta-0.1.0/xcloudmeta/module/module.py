from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from xcloudmeta.base.folder import Folder
from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.component.makefile import MakeFile
from xcloudmeta.component.metafile import MetaFile


class Module(Folder):
    """
    Desc:
        Base class for infrastructure modules with metadata and makefile support.

    Params:
        path: str | Path: Path to the module directory
        kind: Optional[str | ModuleKind]: Module type identifier
        metafile: Optional[str]: Name of the metadata TOML file
        makefile: Optional[str]: Name of the makefile

    Methods:
        describe: Return module information as dictionary
    """

    def __init__(
        self,
        path: str | Path,
        kind: Optional[str | ModuleKind] = None,
        metafile: Optional[str] = None,
        makefile: Optional[str] = None,
    ) -> None:
        super().__init__(path)
        self.kind = self._resolve_kind(kind)
        self.metafile = self._resolve_metafile(metafile)
        self.meta = self._resolve_meta()
        self.makefile = self._resolve_makefile(makefile)

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

    def _resolve_metafile(
        self,
        metafile: Optional[str],
    ) -> Optional[MetaFile]:
        if not metafile:
            return None
        else:
            return MetaFile(
                path=self.path / metafile,
                kind=self.kind,
            )

    def _resolve_makefile(
        self,
        makefile: Optional[str],
    ) -> Optional[MakeFile]:
        if not makefile:
            return None
        else:
            return MakeFile(
                path=self.path / makefile,
            )

    def _resolve_meta(
        self,
    ) -> Dict[str, Any]:
        if not self.metafile:
            return {}
        else:
            return getattr(self.metafile, "data", {})

    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path={self.path})"

    def describe(self) -> Dict[str, Any]:
        return {
            "path": str(self.path),
            "kind": str(self.kind),
            "meta": self.meta,
        }
