from __future__ import annotations

from pathlib import Path
from typing import Optional

from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.module.module import Module


class Environ(Module):
    """
    Desc:
        Represents an environment module (e.g., dev, staging, production).

    Params:
        path: str | Path: Path to the environment directory
        metafile: Optional[str]: Name of the environment metadata file
        makefile: Optional[str]: Name of the environment makefile

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
            kind=ModuleKind.ENVIRON,
            metafile=metafile,
            makefile=makefile,
        )
