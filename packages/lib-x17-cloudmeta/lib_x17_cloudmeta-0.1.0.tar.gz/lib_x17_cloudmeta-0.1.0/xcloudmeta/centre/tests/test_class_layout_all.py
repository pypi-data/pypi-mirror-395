from __future__ import annotations

import tempfile
from pathlib import Path

from xcloudmeta.centre.layout import Layout
from xcloudmeta.module.environ import Environ
from xcloudmeta.module.package import Package
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.service import Service


def test_init_with_defaults():
    layout = Layout()
    assert layout._root is not None
    assert layout.platform_path is not None
    assert layout.environ_path is not None
    assert layout.package_path is not None
    assert layout.service_path is not None


def test_init_with_custom_root():
    layout = Layout(root="/custom/path")
    assert "/custom/path" in str(layout._root)


def test_init_with_custom_paths():
    layout = Layout(platform="plat/", environ="env/", package="pkg/", service="svc/")
    assert "plat" in str(layout.platform_path)
    assert "env" in str(layout.environ_path)
    assert "pkg" in str(layout.package_path)
    assert "svc" in str(layout.service_path)


def test_resolve_root_with_none_uses_default():
    layout = Layout()
    assert layout._root.is_absolute()


def test_resolve_root_expands_user():
    layout = Layout(root="~/test")
    assert "~" not in str(layout._root)


def test_resolve_root_makes_absolute():
    layout = Layout(root="relative/path")
    assert layout._root.is_absolute()


def test_resolve_platform_with_none_uses_default():
    layout = Layout()
    assert "platform" in str(layout.platform_path)


def test_resolve_platform_with_custom_path():
    layout = Layout(platform="custom-platform/")
    assert "custom-platform" in str(layout.platform_path)


def test_resolve_environ_with_none_uses_default():
    layout = Layout()
    assert "environ" in str(layout.environ_path)


def test_resolve_environ_with_custom_path():
    layout = Layout(environ="custom-environ/")
    assert "custom-environ" in str(layout.environ_path)


def test_resolve_package_with_none_uses_default():
    layout = Layout()
    assert "package" in str(layout.package_path)


def test_resolve_package_with_custom_path():
    layout = Layout(package="custom-package/")
    assert "custom-package" in str(layout.package_path)


def test_resolve_service_with_none_uses_default():
    layout = Layout()
    assert "service" in str(layout.service_path)


def test_resolve_service_with_custom_path():
    layout = Layout(service="custom-service/")
    assert "custom-service" in str(layout.service_path)


def test_resolve_metafile_with_value():
    layout = Layout()
    result = layout._resolve_metafile("custom.toml", "default.toml")
    assert result == "custom.toml"


def test_resolve_metafile_with_none_uses_default():
    layout = Layout()
    result = layout._resolve_metafile(None, "default.toml")
    assert result == "default.toml"


def test_resolve_metafile_with_empty_string_uses_default():
    layout = Layout()
    result = layout._resolve_metafile("", "default.toml")
    assert result == "default.toml"


def test_list_folder_paths_with_nonexistent():
    layout = Layout()
    result = layout.list_folder_paths(Path("/nonexistent/path"))
    assert result == []


def test_list_folder_paths_with_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = Path(tmp.name)
        layout = Layout()
        result = layout.list_folder_paths(tmp_path)
        assert result == []
        tmp_path.unlink()


def test_list_folder_paths_with_empty_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        layout = Layout()
        result = layout.list_folder_paths(Path(tmp_dir))
        assert result == []


def test_list_folder_paths_with_subdirectories():
    with tempfile.TemporaryDirectory() as tmp_dir:
        (Path(tmp_dir) / "dir1").mkdir()
        (Path(tmp_dir) / "dir2").mkdir()
        (Path(tmp_dir) / "file.txt").write_text("test")
        layout = Layout()
        result = layout.list_folder_paths(Path(tmp_dir))
        assert len(result) == 2
        assert all(p.is_dir() for p in result)


def test_list_platforms_with_nonexistent_path():
    layout = Layout(root="/nonexistent")
    result = layout.list_platforms()
    assert result == []


def test_list_platforms_with_existing_directories():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        plat_dir.mkdir()
        (plat_dir / "plat1").mkdir()
        (plat_dir / "plat2").mkdir()
        layout = Layout(root=tmp_dir)
        result = layout.list_platforms()
        assert len(result) == 2
        assert all(isinstance(p, Platform) for p in result)


def test_list_environs_with_nonexistent_path():
    layout = Layout(root="/nonexistent")
    result = layout.list_environs()
    assert result == []


def test_list_environs_with_existing_directories():
    with tempfile.TemporaryDirectory() as tmp_dir:
        env_dir = Path(tmp_dir) / "environ"
        env_dir.mkdir()
        (env_dir / "env1").mkdir()
        (env_dir / "env2").mkdir()
        layout = Layout(root=tmp_dir)
        result = layout.list_environs()
        assert len(result) == 2
        assert all(isinstance(e, Environ) for e in result)


def test_list_packages_with_nonexistent_path():
    layout = Layout(root="/nonexistent")
    result = layout.list_packages()
    assert result == []


def test_list_packages_with_existing_directories():
    with tempfile.TemporaryDirectory() as tmp_dir:
        pkg_dir = Path(tmp_dir) / "package"
        pkg_dir.mkdir()
        (pkg_dir / "pkg1").mkdir()
        (pkg_dir / "pkg2").mkdir()
        layout = Layout(root=tmp_dir)
        result = layout.list_packages()
        assert len(result) == 2
        assert all(isinstance(p, Package) for p in result)


def test_list_services_with_nonexistent_path():
    layout = Layout(root="/nonexistent")
    result = layout.list_services()
    assert result == []


def test_list_services_with_existing_directories():
    with tempfile.TemporaryDirectory() as tmp_dir:
        svc_dir = Path(tmp_dir) / "service"
        svc_dir.mkdir()
        (svc_dir / "svc1").mkdir()
        (svc_dir / "svc2").mkdir()
        layout = Layout(root=tmp_dir)
        result = layout.list_services()
        assert len(result) == 2
        assert all(isinstance(s, Service) for s in result)


def test_describe_returns_dict_with_paths():
    layout = Layout()
    desc = layout.describe()
    assert isinstance(desc, dict)
    assert "root" in desc
    assert "platform_path" in desc
    assert "environ_path" in desc
    assert "package_path" in desc
    assert "service_path" in desc


def test_describe_contains_string_paths():
    layout = Layout(root="/test")
    desc = layout.describe()
    assert isinstance(desc["root"], str)
    assert isinstance(desc["platform_path"], str)


def test_class_constants():
    assert Layout.ROOT == "."
    assert Layout.PLATFORM_PATH == "platform/"
    assert Layout.ENVIRON_PATH == "environ/"
    assert Layout.PACKAGE_PATH == "package/"
    assert Layout.SERVICE_PATH == "service/"
    assert Layout.PLATFORM_METAFILE == "platform.toml"
    assert Layout.ENVIRON_METAFILE == "environ.toml"
    assert Layout.PACKAGE_METAFILE == "package.toml"
    assert Layout.SERVICE_METAFILE == "service.toml"
    assert Layout.MAKEFILE == "makefile"


def test_platform_path_relative_to_root():
    with tempfile.TemporaryDirectory() as tmp_dir:
        layout = Layout(root=tmp_dir)
        assert str(layout._root) in str(layout.platform_path)


def test_list_platforms_creates_platform_with_metafile():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        plat_dir.mkdir()
        (plat_dir / "plat1").mkdir()
        layout = Layout(root=tmp_dir)
        result = layout.list_platforms()
        assert result[0].name == "plat1"
