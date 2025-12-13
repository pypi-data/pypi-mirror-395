from __future__ import annotations

import tempfile
from pathlib import Path

from xcloudmeta.base.file import File


def test_init_with_string_path():
    f = File("/tmp/test.txt")
    assert isinstance(f.path, Path)
    assert f.name == "test"


def test_init_with_path_object():
    p = Path("/tmp/example.py")
    f = File(p)
    assert isinstance(f.path, Path)
    assert f.name == "example"


def test_resolve_path_expands_user():
    f = File("~/test.txt")
    assert "~" not in str(f.path)
    assert f.path.is_absolute()


def test_resolve_path_makes_absolute():
    f = File("relative/path/file.txt")
    assert f.path.is_absolute()


def test_resolve_name_returns_stem():
    f = File("/some/path/document.txt")
    assert f.name == "document"


def test_resolve_name_without_extension():
    f = File("/some/path/noext")
    assert f.name == "noext"


def test_is_exist_returns_false_for_nonexistent():
    f = File("/nonexistent/path/file.txt")
    assert f.is_exist() is False


def test_is_exist_returns_true_for_existing_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        f = File(tmp_path)
        assert f.is_exist() is True
        Path(tmp_path).unlink()


def test_is_file_returns_false_for_nonexistent():
    f = File("/nonexistent/file.txt")
    assert f.is_file() is False


def test_is_file_returns_true_for_existing_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        f = File(tmp_path)
        assert f.is_file() is True
        Path(tmp_path).unlink()


def test_is_file_returns_false_for_directory():
    with tempfile.TemporaryDirectory() as tmp_dir:
        f = File(tmp_dir)
        assert f.is_file() is False


def test_path_with_special_characters():
    f = File("/tmp/test file with spaces.txt")
    assert f.name == "test file with spaces"
    assert isinstance(f.path, Path)


def test_multiple_extensions():
    f = File("/tmp/archive.tar.gz")
    assert f.name == "archive.tar"


def test_path_resolution_handles_dots():
    f = File("/tmp/../tmp/./test.txt")
    assert f.path.is_absolute()
    assert ".." not in str(f.path)
