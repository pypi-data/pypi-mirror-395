from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from xcloudmeta.centre.overlay import Overlay
from xcloudmeta.module.environ import Environ
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.service import Service


def test_init_with_all_modules():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "test-platform"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "test-environ"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "test-service"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        assert overlay.platform == p
        assert overlay.environ == e
        assert overlay.service == s


def test_merge_simple_dicts():
    base = {"a": 1, "b": 2}
    override = {"b": 3, "c": 4}
    result = Overlay._merge(base, override)
    assert result["a"] == 1
    assert result["b"] == 3
    assert result["c"] == 4


def test_merge_nested_dicts():
    base = {"user": {"name": "john", "age": 30}}
    override = {"user": {"age": 31, "city": "NYC"}}
    result = Overlay._merge(base, override)
    assert result["user"]["name"] == "john"
    assert result["user"]["age"] == 31
    assert result["user"]["city"] == "NYC"


def test_merge_lists_combines_unique():
    base = {"items": [1, 2, 3]}
    override = {"items": [3, 4, 5]}
    result = Overlay._merge(base, override)
    assert 1 in result["items"]
    assert 2 in result["items"]
    assert 3 in result["items"]
    assert 4 in result["items"]
    assert 5 in result["items"]


def test_merge_with_none_override():
    base = {"a": 1, "b": 2}
    result = Overlay._merge(base, None)
    assert result == {"a": 1, "b": 2}


def test_merge_deeply_nested():
    base = {"a": {"b": {"c": 1}}}
    override = {"a": {"b": {"d": 2}}}
    result = Overlay._merge(base, override)
    assert result["a"]["b"]["c"] == 1
    assert result["a"]["b"]["d"] == 2


def test_resolve_refs_with_simple_ref():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "plat1"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "{{ ref(platform.name) }}"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "svc1"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        assert overlay.compose["environ"]["name"] == "plat1"


def test_resolve_refs_in_string():
    compose = {"base": "value", "derived": "prefix-{{ ref(base) }}-suffix"}
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        result = overlay.resolve_refs(compose)
        assert result["derived"] == "prefix-value-suffix"


def test_resolve_refs_with_nested_dict():
    compose = {"config": {"value": "test"}, "ref": "{{ ref(config.value) }}"}
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        result = overlay.resolve_refs(compose)
        assert result["ref"] == "test"


def test_resolve_refs_raises_on_invalid_path():
    compose = {"ref": "{{ ref(nonexistent.path) }}"}
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        with pytest.raises(KeyError):
            overlay.resolve_refs(compose)


def test_get_compose_returns_dict():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        compose = overlay.get_compose()
        assert isinstance(compose, dict)
        assert "platform" in compose
        assert "environ" in compose
        assert "service" in compose


def test_get_namespace_returns_namespace():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        ns = overlay.get_namespace()
        assert hasattr(ns, "platform")
        assert hasattr(ns, "environ")
        assert hasattr(ns, "service")


def test_get_delegates_to_namespace():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "test-plat"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        assert overlay.get("platform.name") == "test-plat"


def test_set_delegates_to_namespace():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        overlay.set("custom.value", 123)
        assert overlay.get("custom.value") == 123


def test_ref_pattern_matches_simple_ref():
    pattern = Overlay.REF_PATTERN
    match = pattern.fullmatch("{{ ref(path.to.value) }}")
    assert match is not None
    assert match.group(1) == "path.to.value"


def test_ref_pattern_with_spaces():
    pattern = Overlay.REF_PATTERN
    match = pattern.fullmatch("{{  ref( path.to.value )  }}")
    assert match is not None


def test_merge_all_combines_platform_environ_service():
    with tempfile.TemporaryDirectory() as tmp_dir:
        plat_dir = Path(tmp_dir) / "platform"
        env_dir = Path(tmp_dir) / "environ"
        svc_dir = Path(tmp_dir) / "service"
        plat_dir.mkdir()
        env_dir.mkdir()
        svc_dir.mkdir()

        (plat_dir / "platform.toml").write_text('[platform]\nname = "p"\n[shared]\na = 1\n')
        (env_dir / "environ.toml").write_text('[environ]\nname = "e"\n[shared]\nb = 2\n')
        (svc_dir / "service.toml").write_text('[service]\nname = "s"\n[shared]\nc = 3\n')

        p = Platform(plat_dir, metafile="platform.toml")
        e = Environ(env_dir, metafile="environ.toml")
        s = Service(svc_dir, metafile="service.toml")

        overlay = Overlay(platform=p, environ=e, service=s)
        assert overlay.compose["shared"]["a"] == 1
        assert overlay.compose["shared"]["b"] == 2
        assert overlay.compose["shared"]["c"] == 3
