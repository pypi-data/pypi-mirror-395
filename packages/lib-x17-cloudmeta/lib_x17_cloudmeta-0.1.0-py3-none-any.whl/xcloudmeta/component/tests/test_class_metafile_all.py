from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.component.metafile import MetaFile


def test_init_with_string_path_only():
    mf = MetaFile("/tmp/pyproject.toml")
    assert isinstance(mf.path, Path)
    assert mf.name == "pyproject"
    assert mf.kind == ModuleKind.UNDEFINED
    assert mf.data == {}


def test_init_with_path_object():
    p = Path("/tmp/config.toml")
    mf = MetaFile(p)
    assert isinstance(mf.path, Path)
    assert mf.name == "config"


def test_init_with_kind_as_string():
    mf = MetaFile("/tmp/pyproject.toml", kind="package")
    assert mf.kind == ModuleKind.PACKAGE


def test_init_with_kind_as_modulekind():
    mf = MetaFile("/tmp/pyproject.toml", kind=ModuleKind.SERVICE)
    assert mf.kind == ModuleKind.SERVICE


def test_init_with_data_dict():
    data = {"name": "test-project", "version": "1.0.0"}
    mf = MetaFile("/tmp/pyproject.toml", data=data)
    assert mf.data == data
    assert mf.data["name"] == "test-project"


def test_init_with_all_parameters():
    data = {"tool": {"pytest": {"testpaths": ["tests"]}}}
    mf = MetaFile("/tmp/pyproject.toml", kind="package", data=data)
    assert mf.kind == ModuleKind.PACKAGE
    assert mf.data == data


def test_resolve_path_raises_error_for_none():
    with pytest.raises(Exception):
        MetaFile(None)


def test_resolve_path_expands_user():
    mf = MetaFile("~/pyproject.toml")
    assert "~" not in str(mf.path)
    assert mf.path.is_absolute()


def test_resolve_path_makes_absolute():
    mf = MetaFile("relative/pyproject.toml")
    assert mf.path.is_absolute()


def test_resolve_kind_with_none_returns_undefined():
    mf = MetaFile("/tmp/pyproject.toml", kind=None)
    assert mf.kind == ModuleKind.UNDEFINED


def test_resolve_kind_with_valid_string():
    mf = MetaFile("/tmp/pyproject.toml", kind="platform")
    assert mf.kind == ModuleKind.PLATFORM


def test_resolve_kind_with_uppercase_string():
    mf = MetaFile("/tmp/pyproject.toml", kind="ENVIRON")
    assert mf.kind == ModuleKind.ENVIRON


def test_resolve_kind_with_invalid_string():
    mf = MetaFile("/tmp/pyproject.toml", kind="invalid")
    assert mf.kind == ModuleKind.UNDEFINED


def test_resolve_kind_with_modulekind_enum():
    mf = MetaFile("/tmp/pyproject.toml", kind=ModuleKind.SERVICE)
    assert mf.kind == ModuleKind.SERVICE


def test_resolve_kind_with_invalid_type_returns_undefined():
    mf = MetaFile("/tmp/pyproject.toml", kind=123)
    assert mf.kind == ModuleKind.UNDEFINED


def test_resolve_data_with_provided_dict():
    data = {"key": "value", "nested": {"item": 1}}
    mf = MetaFile("/tmp/pyproject.toml", data=data)
    assert mf.data == data


def test_resolve_data_with_none_and_nonexistent_file():
    mf = MetaFile("/nonexistent/pyproject.toml")
    assert mf.data == {}


def test_resolve_data_with_none_and_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        mf = MetaFile(tmp_dir)
        assert mf.data == {}


def test_resolve_data_reads_valid_toml_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as tmp:
        tmp.write('[project]\nname = "test"\nversion = "1.0.0"\n')
        tmp_path = tmp.name

    mf = MetaFile(tmp_path)
    assert "project" in mf.data
    assert mf.data["project"]["name"] == "test"
    assert mf.data["project"]["version"] == "1.0.0"
    Path(tmp_path).unlink()


def test_resolve_data_raises_error_for_invalid_toml():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as tmp:
        tmp.write("invalid toml content {]}")
        tmp_path = tmp.name

    with pytest.raises(IOError) as exc_info:
        MetaFile(tmp_path)
    assert "Fail to read from" in str(exc_info.value)
    Path(tmp_path).unlink()


def test_resolve_data_with_empty_toml_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as tmp:
        tmp.write("")
        tmp_path = tmp.name

    mf = MetaFile(tmp_path)
    assert mf.data == {}
    Path(tmp_path).unlink()


def test_resolve_data_with_complex_toml():
    toml_content = """
[tool.pytest]
testpaths = ["tests"]
python_files = ["test_*.py"]

[tool.mypy]
strict = true
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as tmp:
        tmp.write(toml_content)
        tmp_path = tmp.name

    mf = MetaFile(tmp_path)
    assert "tool" in mf.data
    assert "pytest" in mf.data["tool"]
    assert "mypy" in mf.data["tool"]
    assert mf.data["tool"]["mypy"]["strict"] is True
    Path(tmp_path).unlink()


def test_inherits_from_file_class():
    mf = MetaFile("/tmp/pyproject.toml")
    assert hasattr(mf, "is_exist")
    assert hasattr(mf, "is_file")


def test_is_exist_returns_false_for_nonexistent():
    mf = MetaFile("/nonexistent/pyproject.toml")
    assert mf.is_exist() is False


def test_is_exist_returns_true_for_existing_file():
    with tempfile.NamedTemporaryFile(suffix=".toml", delete=False) as tmp:
        tmp_path = tmp.name
        mf = MetaFile(tmp_path)
        assert mf.is_exist() is True
        Path(tmp_path).unlink()


def test_multiple_metafile_instances_independent():
    data1 = {"name": "project1"}
    data2 = {"name": "project2"}
    mf1 = MetaFile("/tmp/file1.toml", kind="package", data=data1)
    mf2 = MetaFile("/tmp/file2.toml", kind="service", data=data2)
    assert mf1.data != mf2.data
    assert mf1.kind != mf2.kind
