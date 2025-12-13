from __future__ import annotations

import json
from datetime import date, datetime, time, timedelta

from xcloudmeta.centre.namespace import Namespace


def test_init_with_kwargs():
    ns = Namespace(name="test", value=123)
    assert ns.name == "test"
    assert ns.value == 123


def test_init_empty():
    ns = Namespace()
    assert isinstance(ns, Namespace)


def test_from_obj_with_dict():
    obj = {"name": "test", "count": 5}
    ns = Namespace.from_obj(obj)
    assert isinstance(ns, Namespace)
    assert ns.name == "test"
    assert ns.count == 5


def test_from_obj_with_nested_dict():
    obj = {"user": {"name": "john", "age": 30}, "active": True}
    ns = Namespace.from_obj(obj)
    assert isinstance(ns.user, Namespace)
    assert ns.user.name == "john"
    assert ns.user.age == 30
    assert ns.active is True


def test_from_obj_with_list():
    obj = [1, 2, 3]
    result = Namespace.from_obj(obj)
    assert result == [1, 2, 3]


def test_from_obj_with_list_of_dicts():
    obj = [{"id": 1}, {"id": 2}]
    result = Namespace.from_obj(obj)
    assert isinstance(result[0], Namespace)
    assert result[0].id == 1
    assert result[1].id == 2


def test_from_obj_with_tuple():
    obj = (1, 2, 3)
    result = Namespace.from_obj(obj)
    assert result == (1, 2, 3)


def test_from_obj_with_primitives():
    assert Namespace.from_obj("string") == "string"
    assert Namespace.from_obj(123) == 123
    assert Namespace.from_obj(45.67) == 45.67
    assert Namespace.from_obj(True) is True
    assert Namespace.from_obj(None) is None


def test_resolve_key_with_string():
    ns = Namespace()
    keys = ns._resolve_key("simple")
    assert keys == ["simple"]


def test_resolve_key_with_dotted_string():
    ns = Namespace()
    keys = ns._resolve_key("a.b.c")
    assert keys == ["a", "b", "c"]


def test_resolve_key_with_leading_dot():
    ns = Namespace()
    keys = ns._resolve_key(".user.name")
    assert keys == ["user", "name"]


def test_resolve_key_with_list():
    ns = Namespace()
    keys = ns._resolve_key(["a", "b", "c"])
    assert keys == ["a", "b", "c"]


def test_resolve_key_with_spaces():
    ns = Namespace()
    keys = ns._resolve_key("  key.path  ")
    assert keys == ["key", "path"]


def test_str_returns_json():
    ns = Namespace(name="test", value=123)
    result = str(ns)
    assert isinstance(result, str)
    data = json.loads(result)
    assert data["name"] == "test"
    assert data["value"] == 123


def test_ensure_serialisable_with_primitives():
    assert Namespace.ensure_serialisable("text") == "text"
    assert Namespace.ensure_serialisable(123) == 123
    assert Namespace.ensure_serialisable(45.67) == 45.67
    assert Namespace.ensure_serialisable(True) is True
    assert Namespace.ensure_serialisable(None) is None


def test_ensure_serialisable_with_datetime():
    dt = datetime(2025, 12, 9, 10, 30, 45)
    result = Namespace.ensure_serialisable(dt)
    assert isinstance(result, str)
    assert "2025-12-09" in result


def test_ensure_serialisable_with_date():
    d = date(2025, 12, 9)
    result = Namespace.ensure_serialisable(d)
    assert result == "2025-12-09"


def test_ensure_serialisable_with_time():
    t = time(10, 30, 45)
    result = Namespace.ensure_serialisable(t)
    assert isinstance(result, str)
    assert "10:30:45" in result


def test_ensure_serialisable_with_timedelta():
    td = timedelta(days=1, hours=2)
    result = Namespace.ensure_serialisable(td)
    assert isinstance(result, str)


def test_ensure_serialisable_with_dict():
    obj = {"name": "test", "count": 5}
    result = Namespace.ensure_serialisable(obj)
    assert result == {"name": "test", "count": 5}


def test_ensure_serialisable_with_list():
    obj = [1, 2, 3]
    result = Namespace.ensure_serialisable(obj)
    assert result == [1, 2, 3]


def test_get_simple_key():
    ns = Namespace(name="test", value=123)
    assert ns.get("name") == "test"
    assert ns.get("value") == 123


def test_get_nested_key():
    ns = Namespace.from_obj({"user": {"name": "john", "age": 30}})
    assert ns.get("user.name") == "john"
    assert ns.get("user.age") == 30


def test_get_with_default():
    ns = Namespace(name="test")
    assert ns.get("missing", "default") == "default"


def test_get_nested_missing_returns_default():
    ns = Namespace(user=Namespace(name="john"))
    assert ns.get("user.missing", "N/A") == "N/A"


def test_get_with_list_key():
    ns = Namespace.from_obj({"user": {"name": "john"}})
    assert ns.get(["user", "name"]) == "john"


def test_set_simple_key():
    ns = Namespace()
    ns.set("name", "test")
    assert ns.name == "test"


def test_set_nested_key():
    ns = Namespace()
    ns.set("user.name", "john")
    assert isinstance(ns.user, Namespace)
    assert ns.user.name == "john"


def test_set_deeply_nested_key():
    ns = Namespace()
    ns.set("a.b.c", "value")
    assert ns.a.b.c == "value"


def test_set_with_list_key():
    ns = Namespace()
    ns.set(["user", "age"], 30)
    assert ns.user.age == 30


def test_set_overwrites_existing():
    ns = Namespace(name="old")
    ns.set("name", "new")
    assert ns.name == "new"


def test_describe_returns_serialisable_dict():
    ns = Namespace(name="test", count=5)
    desc = ns.describe()
    assert isinstance(desc, dict)
    assert desc["name"] == "test"
    assert desc["count"] == 5


def test_describe_with_nested_namespace():
    ns = Namespace.from_obj({"user": {"name": "john"}})
    desc = ns.describe()
    assert isinstance(desc["user"], dict)
    assert desc["user"]["name"] == "john"


def test_to_dict_simple():
    ns = Namespace(name="test", value=123)
    d = ns.to_dict()
    assert d == {"name": "test", "value": 123}


def test_to_dict_nested():
    ns = Namespace.from_obj({"user": {"name": "john", "age": 30}})
    d = ns.to_dict()
    assert isinstance(d["user"], dict)
    assert d["user"]["name"] == "john"


def test_to_dict_with_list_of_namespaces():
    ns = Namespace.from_obj({"items": [{"id": 1}, {"id": 2}]})
    d = ns.to_dict()
    assert isinstance(d["items"], list)
    assert d["items"][0] == {"id": 1}
    assert d["items"][1] == {"id": 2}


def test_to_dict_with_mixed_list():
    ns = Namespace(items=[Namespace(id=1), "plain", 123])
    d = ns.to_dict()
    assert d["items"][0] == {"id": 1}
    assert d["items"][1] == "plain"
    assert d["items"][2] == 123


def test_get_nonexistent_nested_path():
    ns = Namespace(user=Namespace(name="john"))
    assert ns.get("user.address.city") is None


def test_set_creates_intermediate_namespaces():
    ns = Namespace()
    ns.set("deep.nested.path", "value")
    assert isinstance(ns.deep, Namespace)
    assert isinstance(ns.deep.nested, Namespace)
    assert ns.deep.nested.path == "value"
