from __future__ import annotations

import tempfile
from pathlib import Path

from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.component.makefile import MakeFile
from xcloudmeta.component.metafile import MetaFile
from xcloudmeta.module.environ import Environ


def test_init_with_string_path_only():
    e = Environ("/tmp/test-environ")
    assert isinstance(e.path, Path)
    assert e.name == "test-environ"
    assert e.kind == ModuleKind.ENVIRON


def test_init_with_path_object():
    path = Path("/tmp/my-environ")
    e = Environ(path)
    assert isinstance(e.path, Path)
    assert e.name == "my-environ"
    assert e.kind == ModuleKind.ENVIRON


def test_kind_is_always_environ():
    e = Environ("/tmp/test-environ")
    assert e.kind == ModuleKind.ENVIRON
    assert e.kind.value == "environ"


def test_init_with_metafile_string():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        e = Environ(tmp_dir, metafile="pyproject.toml")
        assert e.metafile is not None
        assert isinstance(e.metafile, MetaFile)


def test_init_with_makefile_string():
    with tempfile.TemporaryDirectory() as tmp_dir:
        make_file = Path(tmp_dir) / "Makefile"
        make_file.write_text('all:\n\techo "test"\n')
        e = Environ(tmp_dir, makefile="Makefile")
        assert e.makefile is not None
        assert isinstance(e.makefile, MakeFile)


def test_init_with_both_metafile_and_makefile():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        make_file = Path(tmp_dir) / "Makefile"
        make_file.write_text('all:\n\techo "test"\n')
        e = Environ(tmp_dir, metafile="pyproject.toml", makefile="Makefile")
        assert e.metafile is not None
        assert e.makefile is not None


def test_metafile_has_environ_kind():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        e = Environ(tmp_dir, metafile="pyproject.toml")
        assert e.metafile.kind == ModuleKind.ENVIRON


def test_meta_returns_data_from_metafile():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "environ-test"\n')
        e = Environ(tmp_dir, metafile="pyproject.toml")
        assert "project" in e.meta
        assert e.meta["project"]["name"] == "environ-test"


def test_meta_returns_empty_dict_when_no_metafile():
    e = Environ("/tmp/test-environ")
    assert e.meta == {}


def test_str_returns_environ_name():
    e = Environ("/tmp/my-environ")
    assert str(e) == "my-environ"


def test_repr_returns_class_and_path():
    e = Environ("/tmp/test-environ")
    repr_str = repr(e)
    assert "Environ" in repr_str
    assert "path=" in repr_str


def test_describe_returns_environ_kind():
    e = Environ("/tmp/test-environ")
    desc = e.describe()
    assert desc["kind"] == "environ"


def test_describe_contains_metadata():
    e = Environ("/tmp/test-environ")
    desc = e.describe()
    assert "path" in desc
    assert "kind" in desc
    assert "meta" in desc


def test_inherits_from_module_class():
    e = Environ("/tmp/test-environ")
    assert hasattr(e, "is_exist")
    assert hasattr(e, "is_folder")
    assert hasattr(e, "describe")


def test_is_exist_returns_false_for_nonexistent():
    e = Environ("/nonexistent/environ")
    assert e.is_exist() is False


def test_is_exist_returns_true_for_existing_folder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        e = Environ(tmp_dir)
        assert e.is_exist() is True


def test_multiple_environ_instances_independent():
    e1 = Environ("/tmp/environ1")
    e2 = Environ("/tmp/environ2")
    assert e1.name != e2.name
    assert e1.kind == e2.kind


def test_metafile_path_is_relative_to_environ():
    with tempfile.TemporaryDirectory() as tmp_dir:
        e = Environ(tmp_dir, metafile="config.toml")
        expected_path = (Path(tmp_dir) / "config.toml").resolve()
        assert e.metafile.path == expected_path


def test_makefile_path_is_relative_to_environ():
    with tempfile.TemporaryDirectory() as tmp_dir:
        e = Environ(tmp_dir, makefile="Makefile")
        expected_path = (Path(tmp_dir) / "Makefile").resolve()
        assert e.makefile.path == expected_path
