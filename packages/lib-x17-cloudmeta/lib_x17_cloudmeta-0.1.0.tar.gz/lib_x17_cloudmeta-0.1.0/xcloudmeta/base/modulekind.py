from __future__ import annotations

from enum import Enum


class ModuleKind(str, Enum):
    """
    Desc:
        Enumeration of infrastructure module types.

    Params:
        None

    Methods:
        from_str: Create ModuleKind from string value
        is_platform: Check if kind is PLATFORM
        is_environ: Check if kind is ENVIRON
        is_package: Check if kind is PACKAGE
        is_service: Check if kind is SERVICE
        is_undefined: Check if kind is UNDEFINED
    """

    PLATFORM = "platform"
    ENVIRON = "environ"
    PACKAGE = "package"
    SERVICE = "service"
    UNDEFINED = "undefined"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return ModuleKind.UNDEFINED

    @classmethod
    def from_str(cls, string: str) -> ModuleKind:
        for dkind in ModuleKind:
            if dkind.value.lower() == string.lower():
                return dkind
        return ModuleKind.UNDEFINED

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        return super().__eq__(other)

    def __ne__(self, value):
        return not self.__eq__(value)

    def is_platform(self):
        return self is ModuleKind.PLATFORM

    def is_environ(self):
        return self is ModuleKind.ENVIRON

    def is_package(self):
        return self is ModuleKind.PACKAGE

    def is_service(self):
        return self is ModuleKind.SERVICE

    def is_undefined(self):
        return self is ModuleKind.UNDEFINED
