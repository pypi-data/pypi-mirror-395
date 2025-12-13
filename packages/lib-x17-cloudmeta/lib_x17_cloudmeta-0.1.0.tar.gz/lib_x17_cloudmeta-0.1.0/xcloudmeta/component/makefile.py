from __future__ import annotations

from pathlib import Path

from xcloudmeta.base.file import File


class MakeFile(File):
    """
    Desc:
        Represents a makefile with file handling capabilities.

    Params:
        path: str | Path: Path to the makefile

    Methods:
        Inherits all methods from File class
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:
        super().__init__(path)
