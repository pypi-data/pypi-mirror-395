from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from xcloudmeta.module.environ import Environ
from xcloudmeta.module.package import Package
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.service import Service


class Layout:
    """
    Desc:
        Manages directory structure and module organization for infrastructure.

    Params:
        root: Optional[str]: Root directory path
        platform: Optional[str]: Platform subdirectory path
        environ: Optional[str]: Environment subdirectory path
        package: Optional[str]: Package subdirectory path
        service: Optional[str]: Service subdirectory path

    Methods:
        list_platforms: List all Platform modules
        list_environs: List all Environ modules
        list_packages: List all Package modules
        list_services: List all Service modules
        describe: Return layout paths as dictionary
    """

    ROOT = "."
    PLATFORM_PATH = "platform/"
    ENVIRON_PATH = "environ/"
    PACKAGE_PATH = "package/"
    SERVICE_PATH = "service/"
    PLATFORM_METAFILE = "platform.toml"
    ENVIRON_METAFILE = "environ.toml"
    PACKAGE_METAFILE = "package.toml"
    SERVICE_METAFILE = "service.toml"
    MAKEFILE = "makefile"

    def __init__(
        self,
        root: Optional[str] = None,
        platform: Optional[str] = None,
        environ: Optional[str] = None,
        package: Optional[str] = None,
        service: Optional[str] = None,
    ) -> None:
        self._root = self._resolve_root(root)
        self.platform_path = self._resolve_platform(platform)
        self.environ_path = self._resolve_environ(environ)
        self.package_path = self._resolve_package(package)
        self.service_path = self._resolve_service(service)

    def _resolve_root(
        self,
        path: Optional[str],
    ) -> Path:
        if path is None:
            path = self.ROOT
        path = Path(path).expanduser()
        try:
            path = path.resolve(strict=False)
        except Exception:
            path = path.absolute()
        return path

    def _resolve_platform(
        self,
        platform: Optional[str],
    ) -> Path:
        if platform is None:
            platform = self.PLATFORM_PATH
        return self._root / platform

    def _resolve_environ(
        self,
        environ: Optional[str],
    ) -> Path:
        if environ is None:
            environ = self.ENVIRON_PATH
        return self._root / environ

    def _resolve_package(
        self,
        package: Optional[str],
    ) -> Path:
        if package is None:
            package = self.PACKAGE_PATH
        return self._root / package

    def _resolve_service(
        self,
        service: Optional[str],
    ) -> Path:
        if service is None:
            service = self.SERVICE_PATH
        return self._root / service

    def _resolve_metafile(
        self,
        value: Optional[str] = None,
        default: Optional[str] = None,
    ) -> Optional[str]:
        return value if value else default

    def list_folder_paths(
        self,
        folder: Path,
    ) -> List[Path]:
        result = []
        if not folder.exists() or not folder.is_dir():
            return result
        for item in folder.iterdir():
            if item.is_dir():
                result.append(item)
        return result

    def list_platforms(self) -> List[Platform]:
        result = []
        for item in self.list_folder_paths(self.platform_path):
            result.append(
                Platform(
                    path=item,
                    metafile=self.PLATFORM_METAFILE,
                    makefile=self.MAKEFILE,
                )
            )
        return result

    def list_environs(self) -> List[Environ]:
        result = []
        for item in self.list_folder_paths(self.environ_path):
            result.append(
                Environ(
                    path=item,
                    metafile=self.ENVIRON_METAFILE,
                    makefile=self.MAKEFILE,
                )
            )
        return result

    def list_packages(self) -> List[Package]:
        result = []
        for item in self.list_folder_paths(self.package_path):
            result.append(
                Package(
                    path=item,
                    metafile=self.PACKAGE_METAFILE,
                    makefile=self.MAKEFILE,
                )
            )
        return result

    def list_services(self) -> List[Service]:
        result = []
        for item in self.list_folder_paths(self.service_path):
            result.append(
                Service(
                    path=item,
                    metafile=self.SERVICE_METAFILE,
                    makefile=self.MAKEFILE,
                )
            )
        return result

    def describe(self) -> Dict[str, str]:
        return {
            "root": str(self._root),
            "platform_path": str(self.platform_path),
            "environ_path": str(self.environ_path),
            "package_path": str(self.package_path),
            "service_path": str(self.service_path),
        }
