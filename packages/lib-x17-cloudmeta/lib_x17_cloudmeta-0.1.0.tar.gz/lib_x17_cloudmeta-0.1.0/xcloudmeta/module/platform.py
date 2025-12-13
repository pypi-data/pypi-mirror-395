from __future__ import annotations

from pathlib import Path
from typing import Optional

from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.module.module import Module


class Platform(Module):
    """
    Desc:
        Represents a cloud platform module (e.g., AWS, GCP, Azure).

    Params:
        path: str | Path: Path to the platform directory
        metafile: Optional[str]: Name of the platform metadata file
        makefile: Optional[str]: Name of the platform makefile

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
            kind=ModuleKind.PLATFORM,
            metafile=metafile,
            makefile=makefile,
        )
