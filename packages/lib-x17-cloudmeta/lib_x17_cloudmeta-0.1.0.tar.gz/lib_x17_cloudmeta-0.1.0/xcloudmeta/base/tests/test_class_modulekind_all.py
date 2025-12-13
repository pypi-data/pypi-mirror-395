from __future__ import annotations

from xcloudmeta.base.modulekind import ModuleKind


def test_enum_values():
    assert ModuleKind.PLATFORM.value == "platform"
    assert ModuleKind.ENVIRON.value == "environ"
    assert ModuleKind.PACKAGE.value == "package"
    assert ModuleKind.SERVICE.value == "service"
    assert ModuleKind.UNDEFINED.value == "undefined"


def test_from_str_lowercase():
    assert ModuleKind.from_str("platform") == ModuleKind.PLATFORM
    assert ModuleKind.from_str("environ") == ModuleKind.ENVIRON
    assert ModuleKind.from_str("package") == ModuleKind.PACKAGE
    assert ModuleKind.from_str("service") == ModuleKind.SERVICE
    assert ModuleKind.from_str("undefined") == ModuleKind.UNDEFINED


def test_from_str_uppercase():
    assert ModuleKind.from_str("PLATFORM") == ModuleKind.PLATFORM
    assert ModuleKind.from_str("ENVIRON") == ModuleKind.ENVIRON
    assert ModuleKind.from_str("PACKAGE") == ModuleKind.PACKAGE
    assert ModuleKind.from_str("SERVICE") == ModuleKind.SERVICE


def test_from_str_mixed_case():
    assert ModuleKind.from_str("PlAtFoRm") == ModuleKind.PLATFORM
    assert ModuleKind.from_str("EnViRoN") == ModuleKind.ENVIRON
    assert ModuleKind.from_str("PaCkAgE") == ModuleKind.PACKAGE


def test_from_str_invalid_returns_undefined():
    assert ModuleKind.from_str("invalid") == ModuleKind.UNDEFINED
    assert ModuleKind.from_str("unknown") == ModuleKind.UNDEFINED
    assert ModuleKind.from_str("") == ModuleKind.UNDEFINED


def test_missing_with_valid_string():
    mk = ModuleKind("platform")
    assert mk == ModuleKind.PLATFORM


def test_missing_with_uppercase_string():
    mk = ModuleKind("ENVIRON")
    assert mk == ModuleKind.ENVIRON


def test_missing_with_invalid_string_returns_undefined():
    mk = ModuleKind("invalid")
    assert mk == ModuleKind.UNDEFINED


def test_str_representation():
    assert str(ModuleKind.PLATFORM) == "platform"
    assert str(ModuleKind.ENVIRON) == "environ"
    assert str(ModuleKind.PACKAGE) == "package"
    assert str(ModuleKind.SERVICE) == "service"
    assert str(ModuleKind.UNDEFINED) == "undefined"


def test_repr_representation():
    assert repr(ModuleKind.PLATFORM) == "ModuleKind.PLATFORM"
    assert repr(ModuleKind.ENVIRON) == "ModuleKind.ENVIRON"
    assert repr(ModuleKind.PACKAGE) == "ModuleKind.PACKAGE"
    assert repr(ModuleKind.SERVICE) == "ModuleKind.SERVICE"
    assert repr(ModuleKind.UNDEFINED) == "ModuleKind.UNDEFINED"


def test_eq_with_string_lowercase():
    assert ModuleKind.PLATFORM == "platform"
    assert ModuleKind.ENVIRON == "environ"
    assert ModuleKind.PACKAGE == "package"
    assert ModuleKind.SERVICE == "service"


def test_eq_with_string_uppercase():
    assert ModuleKind.PLATFORM == "PLATFORM"
    assert ModuleKind.ENVIRON == "ENVIRON"
    assert ModuleKind.PACKAGE == "PACKAGE"


def test_eq_with_string_mixed_case():
    assert ModuleKind.PLATFORM == "PlAtFoRm"
    assert ModuleKind.ENVIRON == "EnViRoN"


def test_eq_with_enum():
    assert ModuleKind.PLATFORM == ModuleKind.PLATFORM
    assert ModuleKind.ENVIRON == ModuleKind.ENVIRON


def test_eq_returns_false_for_different_values():
    assert not (ModuleKind.PLATFORM == "environ")
    assert not (ModuleKind.PACKAGE == "service")


def test_ne_with_string():
    assert ModuleKind.PLATFORM != "environ"
    assert ModuleKind.ENVIRON != "package"
    assert ModuleKind.PACKAGE != "service"


def test_ne_with_enum():
    assert ModuleKind.PLATFORM != ModuleKind.ENVIRON
    assert ModuleKind.ENVIRON != ModuleKind.PACKAGE


def test_ne_returns_false_for_same_values():
    assert not (ModuleKind.PLATFORM != "platform")
    assert not (ModuleKind.ENVIRON != ModuleKind.ENVIRON)


def test_iteration_over_all_values():
    kinds = list(ModuleKind)
    assert ModuleKind.PLATFORM in kinds
    assert ModuleKind.ENVIRON in kinds
    assert ModuleKind.PACKAGE in kinds
    assert ModuleKind.SERVICE in kinds
    assert ModuleKind.UNDEFINED in kinds
    assert len(kinds) == 5


def test_is_instance_of_str():
    assert isinstance(ModuleKind.PLATFORM, str)
    assert isinstance(ModuleKind.ENVIRON, str)
