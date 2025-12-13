from __future__ import annotations

from pathlib import Path
from typing import Optional

from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.module.module import Module


class Service(Module):
    """
    Desc:
        Represents a service module (e.g., API, web app, worker).

    Params:
        path: str | Path: Path to the service directory
        metafile: Optional[str]: Name of the service metadata file
        makefile: Optional[str]: Name of the service makefile

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
            kind=ModuleKind.SERVICE,
            metafile=metafile,
            makefile=makefile,
        )
