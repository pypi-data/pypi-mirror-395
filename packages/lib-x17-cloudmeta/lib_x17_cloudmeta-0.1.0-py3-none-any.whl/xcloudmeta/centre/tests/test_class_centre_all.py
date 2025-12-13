from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from xcloudmeta.centre.centre import Centre


def test_init_with_defaults():
    c = Centre()
    assert c.layout is not None
    assert c.root is not None
    assert isinstance(c.platforms, list)
    assert isinstance(c.environs, list)
    assert isinstance(c.packages, list)
    assert isinstance(c.services, list)


def test_init_with_custom_root():
    with tempfile.TemporaryDirectory() as tmp_dir:
        c = Centre(root=tmp_dir)
        assert str(tmp_dir) in str(c.root)


def test_init_with_custom_paths():
    with tempfile.TemporaryDirectory() as tmp_dir:
        c = Centre(root=tmp_dir, platform_path="plat/", environ_path="env/", package_path="pkg/", service_path="svc/")
        assert c.layout is not None


def test_repr_contains_class_and_root():
    c = Centre()
    repr_str = repr(c)
    assert "Centre" in repr_str
    assert "root=" in repr_str


def test_str_returns_root_path():
    with tempfile.TemporaryDirectory() as tmp_dir:
        c = Centre(root=tmp_dir)
        assert tmp_dir in str(c)


def test_get_platform_with_name():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        plat_dir.mkdir()
        (plat_dir / "plat1").mkdir()
        (plat_dir / "plat2").mkdir()

        c = Centre(root=tmp_dir)
        p = c.get_platform("plat1")
        assert p is not None
        assert p.name == "plat1"


def test_get_platform_without_name_returns_single():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        plat_dir.mkdir()
        (plat_dir / "only-one").mkdir()

        c = Centre(root=tmp_dir)
        p = c.get_platform()
        assert p is not None
        assert p.name == "only-one"


def test_get_platform_without_name_returns_none_for_multiple():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        plat_dir.mkdir()
        (plat_dir / "plat1").mkdir()
        (plat_dir / "plat2").mkdir()

        c = Centre(root=tmp_dir)
        p = c.get_platform()
        assert p is None


def test_get_platform_returns_none_for_nonexistent():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        plat_dir.mkdir()

        c = Centre(root=tmp_dir)
        p = c.get_platform("nonexistent")
        assert p is None


def test_get_environ_with_name():
    with tempfile.TemporaryDirectory() as tmp_dir:
        env_dir = Path(tmp_dir) / "environ"
        env_dir.mkdir()
        (env_dir / "env1").mkdir()
        (env_dir / "env2").mkdir()

        c = Centre(root=tmp_dir)
        e = c.get_environ("env1")
        assert e is not None
        assert e.name == "env1"


def test_get_environ_without_name_returns_single():
    with tempfile.TemporaryDirectory() as tmp_dir:
        env_dir = Path(tmp_dir) / "environ"
        env_dir.mkdir()
        (env_dir / "only-one").mkdir()

        c = Centre(root=tmp_dir)
        e = c.get_environ()
        assert e is not None
        assert e.name == "only-one"


def test_get_environ_without_name_returns_none_for_multiple():
    with tempfile.TemporaryDirectory() as tmp_dir:
        env_dir = Path(tmp_dir) / "environ"
        env_dir.mkdir()
        (env_dir / "env1").mkdir()
        (env_dir / "env2").mkdir()

        c = Centre(root=tmp_dir)
        e = c.get_environ()
        assert e is None


def test_get_package_with_name():
    with tempfile.TemporaryDirectory() as tmp_dir:
        pkg_dir = Path(tmp_dir) / "package"
        pkg_dir.mkdir()
        (pkg_dir / "pkg1").mkdir()
        (pkg_dir / "pkg2").mkdir()

        c = Centre(root=tmp_dir)
        p = c.get_package("pkg1")
        assert p is not None
        assert p.name == "pkg1"


def test_get_package_without_name_returns_single():
    with tempfile.TemporaryDirectory() as tmp_dir:
        pkg_dir = Path(tmp_dir) / "package"
        pkg_dir.mkdir()
        (pkg_dir / "only-one").mkdir()

        c = Centre(root=tmp_dir)
        p = c.get_package()
        assert p is not None
        assert p.name == "only-one"


def test_get_service_with_name():
    with tempfile.TemporaryDirectory() as tmp_dir:
        svc_dir = Path(tmp_dir) / "service"
        svc_dir.mkdir()
        (svc_dir / "svc1").mkdir()
        (svc_dir / "svc2").mkdir()

        c = Centre(root=tmp_dir)
        s = c.get_service("svc1")
        assert s is not None
        assert s.name == "svc1"


def test_get_service_without_name_returns_single():
    with tempfile.TemporaryDirectory() as tmp_dir:
        svc_dir = Path(tmp_dir) / "service"
        svc_dir.mkdir()
        (svc_dir / "only-one").mkdir()

        c = Centre(root=tmp_dir)
        s = c.get_service()
        assert s is not None
        assert s.name == "only-one"


def test_overlay_with_all_parameters():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform" / "plat1"
        env_dir = Path(tmp_dir) / "environ" / "env1"
        svc_dir = Path(tmp_dir) / "service" / "svc1"
        plat_dir.mkdir(parents=True)
        env_dir.mkdir(parents=True)
        svc_dir.mkdir(parents=True)

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        c = Centre(root=tmp_dir)
        overlay = c.overlay(platform="plat1", environ="env1", service="svc1")
        assert overlay is not None


def test_overlay_raises_for_nonexistent_platform():
    with tempfile.TemporaryDirectory() as tmp_dir:
        c = Centre(root=tmp_dir)
        with pytest.raises(ValueError) as exc_info:
            c.overlay(platform="nonexistent")
        assert "Platform" in str(exc_info.value)


def test_overlay_raises_for_nonexistent_environ():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform" / "plat1"
        plat_dir.mkdir(parents=True)
        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')

        c = Centre(root=tmp_dir)
        with pytest.raises(ValueError) as exc_info:
            c.overlay(platform="plat1", environ="nonexistent")
        assert "Environ" in str(exc_info.value)


def test_overlay_raises_for_nonexistent_service():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform" / "plat1"
        plat_dir.mkdir(parents=True)
        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')

        c = Centre(root=tmp_dir)
        with pytest.raises(ValueError) as exc_info:
            c.overlay(platform="plat1", service="nonexistent")
        assert "Service" in str(exc_info.value)


def test_describe_returns_dict():
    c = Centre()
    desc = c.describe()
    assert isinstance(desc, dict)
    assert "layout" in desc
    assert "platforms" in desc
    assert "environs" in desc
    assert "packages" in desc
    assert "services" in desc


def test_describe_contains_lists_of_names():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        plat_dir.mkdir()
        (plat_dir / "plat1").mkdir()
        (plat_dir / "plat2").mkdir()

        c = Centre(root=tmp_dir)
        desc = c.describe()
        assert isinstance(desc["platforms"], list)
        assert "plat1" in desc["platforms"]
        assert "plat2" in desc["platforms"]


def test_platforms_list_populated():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        plat_dir.mkdir()
        (plat_dir / "plat1").mkdir()

        c = Centre(root=tmp_dir)
        assert len(c.platforms) == 1


def test_environs_list_populated():
    with tempfile.TemporaryDirectory() as tmp_dir:
        env_dir = Path(tmp_dir) / "environ"
        env_dir.mkdir()
        (env_dir / "env1").mkdir()

        c = Centre(root=tmp_dir)
        assert len(c.environs) == 1


def test_packages_list_populated():
    with tempfile.TemporaryDirectory() as tmp_dir:
        pkg_dir = Path(tmp_dir) / "package"
        pkg_dir.mkdir()
        (pkg_dir / "pkg1").mkdir()

        c = Centre(root=tmp_dir)
        assert len(c.packages) == 1


def test_services_list_populated():
    with tempfile.TemporaryDirectory() as tmp_dir:
        svc_dir = Path(tmp_dir) / "service"
        svc_dir.mkdir()
        (svc_dir / "svc1").mkdir()

        c = Centre(root=tmp_dir)
        assert len(c.services) == 1


def test_overlay_works_without_environ():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform" / "plat1"
        svc_dir = Path(tmp_dir) / "service" / "svc1"
        plat_dir.mkdir(parents=True)
        svc_dir.mkdir(parents=True)

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        c = Centre(root=tmp_dir)
        overlay = c.overlay(platform="plat1", service="svc1")
        assert overlay is not None
        assert overlay.platform is not None
        assert overlay.environ is None
        assert overlay.service is not None


def test_overlay_works_without_service():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform" / "plat1"
        env_dir = Path(tmp_dir) / "environ" / "env1"
        plat_dir.mkdir(parents=True)
        env_dir.mkdir(parents=True)

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')

        c = Centre(root=tmp_dir)
        overlay = c.overlay(platform="plat1", environ="env1")
        assert overlay is not None
        assert overlay.platform is not None
        assert overlay.environ is not None
        assert overlay.service is None
