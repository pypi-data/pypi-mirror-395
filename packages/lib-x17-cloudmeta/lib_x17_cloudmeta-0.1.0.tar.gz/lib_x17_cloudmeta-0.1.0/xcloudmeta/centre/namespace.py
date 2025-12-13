from __future__ import annotations

import json
from datetime import date, datetime, time, timedelta
from types import SimpleNamespace
from typing import Any, Dict, List, Mapping, Union


class Namespace(SimpleNamespace):
    """
    Desc:
        Hierarchical namespace for configuration access with dot notation.

    Params:
        **kwargs: Arbitrary keyword arguments to initialize namespace

    Methods:
        from_obj: Create Namespace from mapping or nested structure
        get: Retrieve value by dot-separated path
        set: Set value at dot-separated path
        describe: Return namespace as serializable dictionary
        to_dict: Convert namespace to dictionary
    """

    @classmethod
    def from_obj(cls, obj: Any) -> Any:
        if isinstance(obj, Mapping):
            res = {k: cls.from_obj(v) for k, v in obj.items()}
            return cls(**res)
        if isinstance(obj, list):
            return [cls.from_obj(v) for v in obj]
        if isinstance(obj, tuple):
            return tuple(cls.from_obj(v) for v in obj)
        return obj

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

    def _resolve_key(
        self,
        key: Union[List[str], str],
    ) -> List[str]:
        if isinstance(key, list):
            return key
        key = key.strip()
        if key.startswith("."):
            key = key[1:]
        if "." in key:
            return [p for p in key.split(".") if p]
        return [key]

    def __repr__(self) -> str:
        return super().__repr__()

    def __str__(self) -> str:
        return json.dumps(self.describe(), ensure_ascii=False, indent=2)

    @staticmethod
    def ensure_serialisable(value: Any) -> Any:
        natives = (str, int, float, bool, type(None))
        dts = (datetime, date, time)
        durs = (timedelta,)
        if isinstance(value, natives):
            return value
        if isinstance(value, dts):
            return value.isoformat()
        if isinstance(value, durs):
            return str(value)
        if isinstance(value, dict):
            return {str(k): Namespace.ensure_serialisable(v) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [Namespace.ensure_serialisable(v) for v in value]
        return str(value)

    def get(
        self,
        key: str | List[str],
        default: Any = None,
    ) -> Any:
        path = self._resolve_key(key)
        current: Any = self
        for part in path:
            not_ns = not isinstance(current, Namespace)
            not_in = not hasattr(current, part)
            if not_ns or not_in:
                return default
            current = getattr(current, part)
        return current

    def set(
        self,
        key: List[str] | str,
        value: Any,
    ) -> None:
        path = self._resolve_key(key)
        if len(path) == 1:
            setattr(self, path[0], value)
        else:
            current = self
            for part in path[:-1]:
                if not hasattr(current, part):
                    setattr(current, part, Namespace())
                current = getattr(current, part)
            setattr(current, path[-1], value)

    def describe(self) -> Dict[str, Any]:
        return Namespace.ensure_serialisable(self.to_dict())

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for k, v in self.__dict__.items():
            if isinstance(v, Namespace):
                out[k] = v.to_dict()
            elif isinstance(v, list):
                items = []
                for item in v:
                    if isinstance(item, Namespace):
                        items.append(item.to_dict())
                    else:
                        items.append(item)
                out[k] = items
            else:
                out[k] = v
        return out
