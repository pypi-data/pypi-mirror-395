from __future__ import annotations

import tempfile
from pathlib import Path

from xcloudmeta.base.folder import Folder


def test_init_with_string_path():
    f = Folder("/tmp/testdir")
    assert isinstance(f.path, Path)
    assert f.name == "testdir"


def test_init_with_path_object():
    p = Path("/tmp/example")
    f = Folder(p)
    assert isinstance(f.path, Path)
    assert f.name == "example"


def test_resolve_path_expands_user():
    f = Folder("~/testdir")
    assert "~" not in str(f.path)
    assert f.path.is_absolute()


def test_resolve_path_makes_absolute():
    f = Folder("relative/path/folder")
    assert f.path.is_absolute()


def test_resolve_name_returns_stem():
    f = Folder("/some/path/documents")
    assert f.name == "documents"


def test_resolve_name_for_root():
    f = Folder("/")
    assert isinstance(f.name, str)


def test_is_exist_returns_false_for_nonexistent():
    f = Folder("/nonexistent/path/folder")
    assert f.is_exist() is False


def test_is_exist_returns_true_for_existing_folder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        f = Folder(tmp_dir)
        assert f.is_exist() is True


def test_is_folder_returns_false_for_nonexistent():
    f = Folder("/nonexistent/folder")
    assert f.is_folder() is False


def test_is_folder_returns_true_for_existing_folder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        f = Folder(tmp_dir)
        assert f.is_folder() is True


def test_is_folder_returns_false_for_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        f = Folder(tmp_path)
        assert f.is_folder() is False
        Path(tmp_path).unlink()


def test_path_with_special_characters():
    f = Folder("/tmp/folder with spaces")
    assert f.name == "folder with spaces"
    assert isinstance(f.path, Path)


def test_path_with_trailing_slash():
    f = Folder("/tmp/testdir/")
    assert f.name == "testdir"
    assert isinstance(f.path, Path)


def test_path_resolution_handles_dots():
    f = Folder("/tmp/../tmp/./testdir")
    assert f.path.is_absolute()
    assert ".." not in str(f.path)


def test_nested_folder_paths():
    f = Folder("/parent/child/grandchild")
    assert f.name == "grandchild"
    assert f.path.is_absolute()


def test_current_directory():
    f = Folder(".")
    assert f.path.is_absolute()
    assert f.is_exist() is True
