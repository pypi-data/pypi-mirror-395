from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Dict, List, Optional

from xcloudmeta.centre.namespace import Namespace
from xcloudmeta.module.environ import Environ
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.service import Service


class Overlay:
    """
    Desc:
        Merges configurations from multiple modules and resolves cross-references.

    Params:
        platform: Optional[Platform]: Platform module
        environ: Optional[Environ]: Environment module
        service: Optional[Service]: Service module

    Methods:
        resolve_refs: Recursively resolve {{ ref(path) }} references in configuration
        get_compose: Get merged configuration dictionary
        get_namespace: Get configuration as Namespace
        get: Retrieve value by dot-separated path
        set: Set value at dot-separated path
        validate: Validate overlay structure

    Notes:
        Reference resolution is recursive with up to 10 iterations by default.
        This allows nested references (e.g., A -> B -> C) to be fully resolved.
        Circular references are detected and raise ValueError.
    """

    REF_PATTERN = re.compile(r"{{\s*ref\(([^)]+)\)\s*}}")

    def __init__(
        self,
        platform: Optional[Platform] = None,
        environ: Optional[Environ] = None,
        service: Optional[Service] = None,
    ) -> None:
        self.platform: Optional[Platform] = platform
        self.environ: Optional[Environ] = environ
        self.service: Optional[Service] = service
        self.compose: Dict[str, Any] = self._resolve_compose()
        self.namespace: Namespace = self._resolve_namespace()

    def _resolve_compose(
        self,
    ) -> Dict[str, Any]:
        raw = self._merge_all()
        compose = self.resolve_refs(raw)
        return compose

    def _resolve_namespace(self) -> Namespace:
        return Namespace.from_obj(self.compose)

    def _merge_all(
        self,
    ) -> Dict[str, Any]:
        if self.platform:
            result = self.platform.meta
        else:
            result = {}

        if self.environ:
            result = Overlay._merge(
                base=result,
                override=self.environ.meta,
            )
        if self.service:
            result = Overlay._merge(
                base=result,
                override=self.service.meta,
            )
        return result

    @staticmethod
    def _merge(
        base: Dict[str, Any],
        override: Dict[str, Any],
    ) -> Any:
        res: Dict[str, Any] = deepcopy(dict(base))
        for k, v in (override or {}).items():
            a = res.get(k)
            if isinstance(a, dict) and isinstance(v, dict):
                res[k] = Overlay._merge(a, v)
                continue
            if isinstance(a, list) and isinstance(v, list):
                combined = list(a)
                for item in v:
                    if item not in combined:
                        combined.append(deepcopy(item))
                res[k] = combined
                continue
            res[k] = deepcopy(v)
        return res

    def resolve_refs(
        self,
        compose: Dict[str, Any],
        max_iterations: int = 10,
    ) -> Dict[str, Any]:
        def get_by_path(root: Dict[str, Any], path: str) -> Any:
            cur: Any = root
            for part in path.split("."):
                part = part.strip()
                if not isinstance(cur, dict) or part not in cur:
                    raise KeyError(f"ref path '{path}' not found at '{part}'")
                cur = cur[part]
            return cur

        def has_references(value: Any) -> bool:
            if isinstance(value, str):
                return self.REF_PATTERN.search(value) is not None
            if isinstance(value, dict):
                return any(has_references(v) for v in value.values())
            if isinstance(value, (list, tuple)):
                return any(has_references(v) for v in value)
            return False

        def resolve_value(value: Any, root: Dict[str, Any]) -> Any:
            if isinstance(value, dict):
                return {k: resolve_value(v, root) for k, v in value.items()}
            if isinstance(value, list):
                return [resolve_value(v, root) for v in value]
            if isinstance(value, tuple):
                return tuple(resolve_value(v, root) for v in value)
            if isinstance(value, str):
                text = value
                m = self.REF_PATTERN.fullmatch(text.strip())
                if m:
                    path = m.group(1).strip()
                    return get_by_path(root, path)

                def _replace(match: re.Match) -> str:
                    path = match.group(1).strip()
                    v = get_by_path(root, path)
                    return str(v)

                return self.REF_PATTERN.sub(_replace, text)
            return value

        cloned = deepcopy(compose)

        for iteration in range(max_iterations):
            previous = deepcopy(cloned)
            cloned = resolve_value(cloned, cloned)
            if not has_references(cloned):
                break
            if cloned == previous:
                raise ValueError(
                    f"Circular reference detected or unresolvable references after {iteration + 1} iterations"
                )
        else:
            raise ValueError(
                f"Reference resolution exceeded max iterations ({max_iterations}). "
                "Possible circular reference or too many nested levels."
            )

        return cloned

    def get_compose(self) -> Dict[str, Any]:
        return dict(self.compose)

    def get_namespace(self) -> Namespace:
        return self.namespace

    def validate(self) -> None:
        assert "platform" in self.compose, "Missing 'platform' in compose"
        assert "environ" in self.compose, "Missing 'environ' in compose"
        assert "service" in self.compose, "Missing 'service' in compose"
        assert self.compose.get("platform", {}), "Expected valid 'platform'"
        assert self.compose.get("environ", {}), "Expected valid 'environ'"
        assert self.compose.get("service", {}), "Expected valid 'service'"

    def get(
        self,
        key: List[str] | str,
        default: Any = None,
    ) -> Any:
        return self.namespace.get(key, default)

    def set(
        self,
        key: List[str] | str,
        value: Any,
    ) -> None:
        self.namespace.set(key, value)
