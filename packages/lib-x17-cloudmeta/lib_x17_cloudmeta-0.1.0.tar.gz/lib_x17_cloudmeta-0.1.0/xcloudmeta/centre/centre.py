from __future__ import annotations

from typing import Any, Dict, Optional

from xcloudmeta.centre.layout import Layout
from xcloudmeta.centre.overlay import Overlay
from xcloudmeta.module.environ import Environ
from xcloudmeta.module.package import Package
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.service import Service


class Centre:
    """
    Desc:
        Central management for complete infrastructure hierarchy with modules and overlays.

    Params:
        root: Optional[str]: Root directory path
        platform_path: Optional[str]: Platform directory path
        environ_path: Optional[str]: Environment directory path
        package_path: Optional[str]: Package directory path
        service_path: Optional[str]: Service directory path

    Methods:
        get_platform: Get platform module by name
        get_environ: Get environment module by name
        get_package: Get package module by name
        get_service: Get service module by name
        overlay: Create configuration overlay for deployment scenario
    """

    def __init__(
        self,
        root: Optional[str] = None,
        platform_path: Optional[str] = None,
        environ_path: Optional[str] = None,
        package_path: Optional[str] = None,
        service_path: Optional[str] = None,
    ) -> None:
        self.layout = self._resolve_layout(
            root=root,
            platform_path=platform_path,
            environ_path=environ_path,
            package_path=package_path,
            service_path=service_path,
        )
        self.root = self.layout._root
        self.platforms = self.layout.list_platforms()
        self.environs = self.layout.list_environs()
        self.packages = self.layout.list_packages()
        self.services = self.layout.list_services()

    def _resolve_layout(
        self,
        root: Optional[str] = None,
        platform_path: Optional[str] = None,
        environ_path: Optional[str] = None,
        package_path: Optional[str] = None,
        service_path: Optional[str] = None,
    ) -> Layout:
        return Layout(
            root=root,
            platform=platform_path,
            environ=environ_path,
            package=package_path,
            service=service_path,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(root={self.root})"

    def __str__(self):
        return str(self.root)

    def get_platform(
        self,
        name: Optional[str] = None,
    ) -> Optional[Platform]:
        if not name:
            if len(self.platforms) == 1:
                return self.platforms[0]
        for platform in self.platforms:
            if platform.name == name:
                return platform
        return None

    def get_environ(
        self,
        name: Optional[str] = None,
    ) -> Optional[Environ]:
        if not name:
            if len(self.environs) == 1:
                return self.environs[0]
        for environ in self.environs:
            if environ.name == name:
                return environ
        return None

    def get_package(
        self,
        name: Optional[str] = None,
    ) -> Optional[Package]:
        if not name:
            if len(self.packages) == 1:
                return self.packages[0]
        for package in self.packages:
            if package.name == name:
                return package
        return None

    def get_service(
        self,
        name: Optional[str] = None,
    ) -> Optional[Service]:
        if not name:
            if len(self.services) == 1:
                return self.services[0]
        for service in self.services:
            if service.name == name:
                return service
        return None

    def overlay(
        self,
        platform: Optional[str] = None,
        environ: Optional[str] = None,
        service: Optional[str] = None,
    ) -> Dict[str, Any]:
        platform_obj = self.get_platform(platform)
        if not platform_obj:
            raise ValueError(f"Platform {platform} not found")

        environ_obj = self.get_environ(environ)
        if environ and not environ_obj:
            raise ValueError(f"Environ {environ} not found")

        service_obj = self.get_service(service)
        if service and not service_obj:
            raise ValueError(f"Service {service} not found")

        overlay = Overlay(
            platform=platform_obj,
            environ=environ_obj,
            service=service_obj,
        )
        return overlay

    def describe(self) -> Dict[str, Any]:
        return {
            "layout": self.layout.describe(),
            "platforms": [plat.name for plat in self.platforms],
            "environs": [env.name for env in self.environs],
            "packages": [pkg.name for pkg in self.packages],
            "services": [svc.name for svc in self.services],
        }
