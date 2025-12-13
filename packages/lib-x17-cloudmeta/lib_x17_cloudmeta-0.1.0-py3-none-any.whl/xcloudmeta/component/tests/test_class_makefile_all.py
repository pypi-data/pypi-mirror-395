from __future__ import annotations

import tempfile
from pathlib import Path

from xcloudmeta.component.makefile import MakeFile


def test_init_with_string_path():
    mf = MakeFile("/tmp/Makefile")
    assert isinstance(mf.path, Path)
    assert mf.name == "Makefile"


def test_init_with_path_object():
    p = Path("/tmp/makefile")
    mf = MakeFile(p)
    assert isinstance(mf.path, Path)
    assert mf.name == "makefile"


def test_inherits_from_file_class():
    mf = MakeFile("/tmp/Makefile")
    assert hasattr(mf, "path")
    assert hasattr(mf, "name")
    assert hasattr(mf, "is_exist")
    assert hasattr(mf, "is_file")


def test_resolve_path_expands_user():
    mf = MakeFile("~/Makefile")
    assert "~" not in str(mf.path)
    assert mf.path.is_absolute()


def test_resolve_path_makes_absolute():
    mf = MakeFile("relative/Makefile")
    assert mf.path.is_absolute()


def test_resolve_name_returns_stem():
    mf = MakeFile("/project/build/Makefile")
    assert mf.name == "Makefile"


def test_is_exist_returns_false_for_nonexistent():
    mf = MakeFile("/nonexistent/Makefile")
    assert mf.is_exist() is False


def test_is_exist_returns_true_for_existing_file():
    with tempfile.NamedTemporaryFile(suffix="Makefile", delete=False) as tmp:
        tmp_path = tmp.name
        mf = MakeFile(tmp_path)
        assert mf.is_exist() is True
        Path(tmp_path).unlink()


def test_is_file_returns_false_for_nonexistent():
    mf = MakeFile("/nonexistent/Makefile")
    assert mf.is_file() is False


def test_is_file_returns_true_for_existing_file():
    with tempfile.NamedTemporaryFile(suffix="Makefile", delete=False) as tmp:
        tmp_path = tmp.name
        mf = MakeFile(tmp_path)
        assert mf.is_file() is True
        Path(tmp_path).unlink()


def test_is_file_returns_false_for_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        mf = MakeFile(tmp_dir)
        assert mf.is_file() is False


def test_path_resolution_handles_dots():
    mf = MakeFile("/tmp/../tmp/./Makefile")
    assert mf.path.is_absolute()
    assert ".." not in str(mf.path)


def test_lowercase_makefile_name():
    mf = MakeFile("/project/makefile")
    assert mf.name == "makefile"


def test_uppercase_makefile_name():
    mf = MakeFile("/project/MAKEFILE")
    assert mf.name == "MAKEFILE"
