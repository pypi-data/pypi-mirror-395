from __future__ import annotations

from pathlib import Path
from typing import Optional

from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.module.module import Module


class Package(Module):
    """
    Desc:
        Represents a package module for shared libraries or dependencies.

    Params:
        path: str | Path: Path to the package directory
        metafile: Optional[str]: Name of the package metadata file
        makefile: Optional[str]: Name of the package makefile

    Methods:
        Inherits all methods from Module class
    """

    def __init__(
        self,
        path: str | Path,
        metafile: Optional[str] = None,
        makefile: Optional[str] = None,
    ) -> None:
        super().__init__(
            path,
            kind=ModuleKind.PACKAGE,
            metafile=metafile,
            makefile=makefile,
        )
