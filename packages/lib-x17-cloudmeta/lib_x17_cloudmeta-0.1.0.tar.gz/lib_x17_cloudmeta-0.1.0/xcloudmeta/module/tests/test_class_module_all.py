from __future__ import annotations

import tempfile
from pathlib import Path

from xcloudmeta.base.modulekind import ModuleKind
from xcloudmeta.component.makefile import MakeFile
from xcloudmeta.component.metafile import MetaFile
from xcloudmeta.module.module import Module


def test_init_with_string_path_only():
    m = Module("/tmp/test-module")
    assert isinstance(m.path, Path)
    assert m.name == "test-module"
    assert m.kind == ModuleKind.UNDEFINED
    assert m.metafile is None
    assert m.makefile is None
    assert m.meta == {}


def test_init_with_path_object():
    p = Path("/tmp/my-module")
    m = Module(p)
    assert isinstance(m.path, Path)
    assert m.name == "my-module"


def test_init_with_kind_as_string():
    m = Module("/tmp/test-module", kind="package")
    assert m.kind == ModuleKind.PACKAGE


def test_init_with_kind_as_modulekind():
    m = Module("/tmp/test-module", kind=ModuleKind.SERVICE)
    assert m.kind == ModuleKind.SERVICE


def test_init_with_metafile_string():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        m = Module(tmp_dir, metafile="pyproject.toml")
        assert m.metafile is not None
        assert isinstance(m.metafile, MetaFile)
        assert m.metafile.name == "pyproject"


def test_init_with_makefile_string():
    with tempfile.TemporaryDirectory() as tmp_dir:
        make_file = Path(tmp_dir) / "Makefile"
        make_file.write_text('all:\n\techo "test"\n')
        m = Module(tmp_dir, makefile="Makefile")
        assert m.makefile is not None
        assert isinstance(m.makefile, MakeFile)
        assert m.makefile.name == "Makefile"


def test_init_with_all_parameters():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        make_file = Path(tmp_dir) / "Makefile"
        make_file.write_text('all:\n\techo "test"\n')
        m = Module(tmp_dir, kind="package", metafile="pyproject.toml", makefile="Makefile")
        assert m.kind == ModuleKind.PACKAGE
        assert m.metafile is not None
        assert m.makefile is not None


def test_resolve_kind_with_none_returns_undefined():
    m = Module("/tmp/test-module", kind=None)
    assert m.kind == ModuleKind.UNDEFINED


def test_resolve_kind_with_valid_string():
    m = Module("/tmp/test-module", kind="platform")
    assert m.kind == ModuleKind.PLATFORM


def test_resolve_kind_with_uppercase_string():
    m = Module("/tmp/test-module", kind="ENVIRON")
    assert m.kind == ModuleKind.ENVIRON


def test_resolve_kind_with_invalid_string():
    m = Module("/tmp/test-module", kind="invalid")
    assert m.kind == ModuleKind.UNDEFINED


def test_resolve_kind_with_modulekind_enum():
    m = Module("/tmp/test-module", kind=ModuleKind.SERVICE)
    assert m.kind == ModuleKind.SERVICE


def test_resolve_kind_with_invalid_type_returns_undefined():
    m = Module("/tmp/test-module", kind=123)
    assert m.kind == ModuleKind.UNDEFINED


def test_resolve_metafile_with_none_returns_none():
    m = Module("/tmp/test-module", metafile=None)
    assert m.metafile is None


def test_resolve_metafile_with_empty_string_returns_none():
    m = Module("/tmp/test-module", metafile="")
    assert m.metafile is None


def test_resolve_metafile_creates_metafile_instance():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "config.toml"
        toml_file.write_text("[settings]\nvalue = 1\n")
        m = Module(tmp_dir, kind="service", metafile="config.toml")
        assert isinstance(m.metafile, MetaFile)
        assert m.metafile.kind == ModuleKind.SERVICE


def test_resolve_metafile_path_is_relative_to_module():
    with tempfile.TemporaryDirectory() as tmp_dir:
        m = Module(tmp_dir, metafile="pyproject.toml")
        expected_path = (Path(tmp_dir) / "pyproject.toml").resolve()
        assert m.metafile.path == expected_path


def test_resolve_makefile_with_none_returns_none():
    m = Module("/tmp/test-module", makefile=None)
    assert m.makefile is None


def test_resolve_makefile_with_empty_string_returns_none():
    m = Module("/tmp/test-module", makefile="")
    assert m.makefile is None


def test_resolve_makefile_creates_makefile_instance():
    with tempfile.TemporaryDirectory() as tmp_dir:
        make_file = Path(tmp_dir) / "makefile"
        make_file.write_text('build:\n\techo "building"\n')
        m = Module(tmp_dir, makefile="makefile")
        assert isinstance(m.makefile, MakeFile)


def test_resolve_makefile_path_is_relative_to_module():
    with tempfile.TemporaryDirectory() as tmp_dir:
        m = Module(tmp_dir, makefile="Makefile")
        expected_path = (Path(tmp_dir) / "Makefile").resolve()
        assert m.makefile.path == expected_path


def test_resolve_meta_returns_empty_dict_when_no_metafile():
    m = Module("/tmp/test-module")
    assert m.meta == {}


def test_resolve_meta_returns_data_from_metafile():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test-project"\nversion = "1.0.0"\n')
        m = Module(tmp_dir, metafile="pyproject.toml")
        assert "project" in m.meta
        assert m.meta["project"]["name"] == "test-project"
        assert m.meta["project"]["version"] == "1.0.0"


def test_str_returns_module_name():
    m = Module("/tmp/my-awesome-module")
    assert str(m) == "my-awesome-module"


def test_repr_returns_class_and_path():
    m = Module("/tmp/test-module")
    repr_str = repr(m)
    assert "Module" in repr_str
    assert "path=" in repr_str
    assert "/tmp/test-module" in repr_str


def test_describe_returns_dict_with_metadata():
    m = Module("/tmp/test-module", kind="package")
    desc = m.describe()
    assert isinstance(desc, dict)
    assert "path" in desc
    assert "kind" in desc
    assert "meta" in desc


def test_describe_contains_correct_path():
    m = Module("/tmp/test-module")
    desc = m.describe()
    assert "test-module" in desc["path"]


def test_describe_contains_correct_kind():
    m = Module("/tmp/test-module", kind="service")
    desc = m.describe()
    assert desc["kind"] == "service"


def test_describe_contains_meta_dict():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[tool]\nname = "value"\n')
        m = Module(tmp_dir, metafile="pyproject.toml")
        desc = m.describe()
        assert isinstance(desc["meta"], dict)
        assert "tool" in desc["meta"]


def test_inherits_from_folder_class():
    m = Module("/tmp/test-module")
    assert hasattr(m, "is_exist")
    assert hasattr(m, "is_folder")


def test_is_exist_returns_false_for_nonexistent():
    m = Module("/nonexistent/module")
    assert m.is_exist() is False


def test_is_exist_returns_true_for_existing_folder():
    with tempfile.TemporaryDirectory() as tmp_dir:
        m = Module(tmp_dir)
        assert m.is_exist() is True


def test_multiple_module_instances_independent():
    m1 = Module("/tmp/module1", kind="package")
    m2 = Module("/tmp/module2", kind="service")
    assert m1.kind != m2.kind
    assert m1.name != m2.name


def test_metafile_inherits_module_kind():
    with tempfile.TemporaryDirectory() as tmp_dir:
        toml_file = Path(tmp_dir) / "pyproject.toml"
        toml_file.write_text('[project]\nname = "test"\n')
        m = Module(tmp_dir, kind=ModuleKind.PLATFORM, metafile="pyproject.toml")
        assert m.metafile.kind == ModuleKind.PLATFORM
