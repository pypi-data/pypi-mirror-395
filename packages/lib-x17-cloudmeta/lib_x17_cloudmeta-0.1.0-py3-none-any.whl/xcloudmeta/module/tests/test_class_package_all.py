from __future__ import annotations

import tempfile
from pathlib import Path

from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.component.makefile import MakeFile
from xcloudmeta.component.metafile import MetaFile
from xcloudmeta.module.package import Package


def test_init_with_string_path_only():
    p = Package("/tmp/test-package")
    assert isinstance(p.path, Path)
    assert p.name == "test-package"
    assert p.kind == ModuleKind.PACKAGE


def test_init_with_path_object():
    path = Path("/tmp/my-package")
    p = Package(path)
    assert isinstance(p.path, Path)
    assert p.name == "my-package"
    assert p.kind == ModuleKind.PACKAGE


def test_kind_is_always_package():
    p = Package("/tmp/test-package")
    assert p.kind == ModuleKind.PACKAGE
    assert p.kind.value == "package"


def test_init_with_metafile_string():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        p = Package(tmp_dir, metafile="pyproject.toml")
        assert p.metafile is not None
        assert isinstance(p.metafile, MetaFile)


def test_init_with_makefile_string():
    with tempfile.TemporaryDirectory() as tmp_dir:
        make_file = Path(tmp_dir) / "Makefile"
        make_file.write_text('all:\n\techo "test"\n')
        p = Package(tmp_dir, makefile="Makefile")
        assert p.makefile is not None
        assert isinstance(p.makefile, MakeFile)


def test_init_with_both_metafile_and_makefile():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        make_file = Path(tmp_dir) / "Makefile"
        make_file.write_text('all:\n\techo "test"\n')
        p = Package(tmp_dir, metafile="pyproject.toml", makefile="Makefile")
        assert p.metafile is not None
        assert p.makefile is not None


def test_metafile_has_package_kind():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        p = Package(tmp_dir, metafile="pyproject.toml")
        assert p.metafile.kind == ModuleKind.PACKAGE


def test_meta_returns_data_from_metafile():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "package-test"\n')
        p = Package(tmp_dir, metafile="pyproject.toml")
        assert "project" in p.meta
        assert p.meta["project"]["name"] == "package-test"


def test_meta_returns_empty_dict_when_no_metafile():
    p = Package("/tmp/test-package")
    assert p.meta == {}


def test_str_returns_package_name():
    p = Package("/tmp/my-package")
    assert str(p) == "my-package"


def test_repr_returns_class_and_path():
    p = Package("/tmp/test-package")
    repr_str = repr(p)
    assert "Package" in repr_str
    assert "path=" in repr_str


def test_describe_returns_package_kind():
    p = Package("/tmp/test-package")
    desc = p.describe()
    assert desc["kind"] == "package"


def test_describe_contains_metadata():
    p = Package("/tmp/test-package")
    desc = p.describe()
    assert "path" in desc
    assert "kind" in desc
    assert "meta" in desc


def test_inherits_from_module_class():
    p = Package("/tmp/test-package")
    assert hasattr(p, "is_exist")
    assert hasattr(p, "is_folder")
    assert hasattr(p, "describe")


def test_is_exist_returns_false_for_nonexistent():
    p = Package("/nonexistent/package")
    assert p.is_exist() is False


def test_is_exist_returns_true_for_existing_folder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        p = Package(tmp_dir)
        assert p.is_exist() is True


def test_multiple_package_instances_independent():
    p1 = Package("/tmp/package1")
    p2 = Package("/tmp/package2")
    assert p1.name != p2.name
    assert p1.kind == p2.kind


def test_metafile_path_is_relative_to_package():
    with tempfile.TemporaryDirectory() as tmp_dir:
        p = Package(tmp_dir, metafile="config.toml")
        expected_path = (Path(tmp_dir) / "config.toml").resolve()
        assert p.metafile.path == expected_path


def test_makefile_path_is_relative_to_package():
    with tempfile.TemporaryDirectory() as tmp_dir:
        p = Package(tmp_dir, makefile="Makefile")
        expected_path = (Path(tmp_dir) / "Makefile").resolve()
        assert p.makefile.path == expected_path
