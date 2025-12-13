"""
Integration test: Namespace operations.

Tests complete namespace workflows including creation, access,
modification, and serialization.
"""

import json
from datetime import date, datetime, time, timedelta

import pytest

from xcloudmeta.centre.namespace import Namespace


class TestNamespaceOperations:
    """Test end-to-end namespace operations."""

    def test_namespace_from_complex_dict(self):
        """Test creating namespace from complex nested dictionary."""
        config = {
            "application": {
                "name": "my-app",
                "version": "1.0.0",
                "settings": {
                    "debug": True,
                    "timeout": 30,
                },
            },
            "database": {
                "connections": [
                    {"host": "db1.example.com", "port": 5432},
                    {"host": "db2.example.com", "port": 5432},
                ],
            },
            "features": ["auth", "logging", "metrics"],
        }

        ns = Namespace.from_obj(config)

        # Test nested access
        assert ns.application.name == "my-app"
        assert ns.application.settings.debug is True
        assert ns.application.settings.timeout == 30

        # Test list access
        assert len(ns.database.connections) == 2
        assert ns.database.connections[0].host == "db1.example.com"
        assert ns.features == ["auth", "logging", "metrics"]

    def test_namespace_get_with_dot_notation(self):
        """Test get() method with various dot notation patterns."""
        ns = Namespace.from_obj(
            {
                "level1": {
                    "level2": {"level3": {"value": "deep_value"}},
                },
            }
        )

        # Various ways to access nested value
        assert ns.get("level1.level2.level3.value") == "deep_value"
        assert ns.get(".level1.level2.level3.value") == "deep_value"
        assert ns.get(["level1", "level2", "level3", "value"]) == "deep_value"

    def test_namespace_get_with_defaults(self):
        """Test get() method with default values."""
        ns = Namespace.from_obj({"existing": "value"})

        # Existing key
        assert ns.get("existing") == "value"

        # Non-existing key with default
        assert ns.get("missing", "default") == "default"
        assert ns.get("deep.missing.path", None) is None
        assert ns.get("missing", 42) == 42

    def test_namespace_set_creates_nested_structure(self):
        """Test set() method automatically creates nested namespaces."""
        ns = Namespace()

        # Set deeply nested value
        ns.set("app.config.database.host", "localhost")
        ns.set("app.config.database.port", 5432)
        ns.set("app.name", "my-app")

        # Verify structure was created
        assert ns.app.name == "my-app"
        assert ns.app.config.database.host == "localhost"
        assert ns.app.config.database.port == 5432

    def test_namespace_set_overwrites_existing(self):
        """Test set() method overwrites existing values."""
        ns = Namespace.from_obj({"key": "old_value"})

        ns.set("key", "new_value")

        assert ns.get("key") == "new_value"

    def test_namespace_to_dict_conversion(self):
        """Test converting namespace back to dictionary."""
        original = {
            "app": {"name": "test", "port": 8080},
            "features": ["a", "b"],
        }

        ns = Namespace.from_obj(original)
        result = ns.to_dict()

        assert result == original
        assert isinstance(result, dict)
        assert isinstance(result["app"], dict)

    def test_namespace_describe_with_datetime_objects(self):
        """Test describe() serializes datetime objects."""
        now = datetime(2025, 12, 9, 10, 30, 0)
        today = date(2025, 12, 9)
        current_time = time(10, 30, 0)
        duration = timedelta(hours=2, minutes=30)

        ns = Namespace(
            timestamp=now,
            date=today,
            time=current_time,
            duration=duration,
        )

        description = ns.describe()

        # Should be serializable
        assert isinstance(description["timestamp"], str)
        assert "2025-12-09" in description["timestamp"]
        assert description["date"] == "2025-12-09"
        assert "10:30" in description["time"]
        assert description["duration"] == "2:30:00"

    def test_namespace_str_returns_json(self):
        """Test str() returns formatted JSON."""
        ns = Namespace.from_obj({"key": "value", "nested": {"inner": 123}})

        json_str = str(ns)

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed["key"] == "value"
        assert parsed["nested"]["inner"] == 123

    def test_namespace_with_list_of_dicts(self):
        """Test namespace handles list of dictionaries."""
        data = {
            "servers": [
                {"name": "server1", "port": 8001},
                {"name": "server2", "port": 8002},
            ],
        }

        ns = Namespace.from_obj(data)

        # List should contain Namespace objects
        assert len(ns.servers) == 2
        assert ns.servers[0].name == "server1"
        assert ns.servers[0].port == 8001
        assert ns.servers[1].name == "server2"
        assert ns.servers[1].port == 8002

    def test_namespace_to_dict_with_nested_namespaces(self):
        """Test to_dict() handles nested Namespace objects."""
        ns = Namespace.from_obj(
            {
                "outer": {
                    "inner": {"deep": "value"},
                },
                "list": [{"item": "one"}, {"item": "two"}],
            }
        )

        result = ns.to_dict()

        # Should convert all nested Namespaces to dicts
        assert isinstance(result, dict)
        assert isinstance(result["outer"], dict)
        assert isinstance(result["outer"]["inner"], dict)
        assert isinstance(result["list"], list)
        assert isinstance(result["list"][0], dict)
        assert result["outer"]["inner"]["deep"] == "value"

    def test_namespace_ensure_serializable_with_mixed_types(self):
        """Test ensure_serialisable handles various data types."""
        data = {
            "string": "text",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "none": None,
            "datetime": datetime(2025, 12, 9),
            "list": [1, 2, 3],
            "nested": {"key": "value"},
        }

        serialized = Namespace.ensure_serialisable(data)

        assert serialized["string"] == "text"
        assert serialized["integer"] == 42
        assert serialized["float"] == 3.14
        assert serialized["boolean"] is True
        assert serialized["none"] is None
        assert isinstance(serialized["datetime"], str)
        assert serialized["list"] == [1, 2, 3]
        assert serialized["nested"]["key"] == "value"

    def test_namespace_with_tuple_data(self):
        """Test namespace handles tuple data structures."""
        data = {"coordinates": (10, 20, 30)}

        ns = Namespace.from_obj(data)

        # Tuples should be preserved
        assert isinstance(ns.coordinates, tuple)
        assert ns.coordinates == (10, 20, 30)

    def test_namespace_complex_nested_operations(self):
        """Test complex operations on deeply nested namespace."""
        ns = Namespace()

        # Build complex structure
        ns.set("app.database.primary.host", "db1.example.com")
        ns.set("app.database.primary.port", 5432)
        ns.set("app.database.replica.host", "db2.example.com")
        ns.set("app.database.replica.port", 5432)
        ns.set("app.cache.redis.host", "cache.example.com")
        ns.set("app.cache.redis.port", 6379)

        # Test various access patterns
        assert ns.get("app.database.primary.host") == "db1.example.com"
        assert ns.app.database.replica.port == 5432
        assert ns.get("app.cache.redis.port") == 6379

        # Modify nested value
        ns.set("app.database.primary.port", 5433)
        assert ns.app.database.primary.port == 5433

    def test_namespace_attribute_access_vs_get(self):
        """Test both attribute access and get() method work consistently."""
        ns = Namespace.from_obj({"level1": {"level2": {"value": "test"}}})

        # Both should work
        assert ns.level1.level2.value == "test"
        assert ns.get("level1.level2.value") == "test"

        # Missing keys
        with pytest.raises(AttributeError):
            _ = ns.missing.attribute

        assert ns.get("missing.attribute", "default") == "default"

    def test_namespace_empty_initialization(self):
        """Test creating empty namespace and adding values."""
        ns = Namespace()

        # Should be empty
        assert ns.to_dict() == {}

        # Add values
        ns.set("key", "value")
        assert ns.get("key") == "value"

    def test_namespace_with_special_characters_in_keys(self):
        """Test namespace handles keys with special characters."""
        data = {
            "app-name": "my-app",
            "database_host": "localhost",
            "feature.flag": "enabled",
        }

        ns = Namespace.from_obj(data)

        # Access with special characters (via attribute may not work for all)
        assert ns.to_dict()["app-name"] == "my-app"
        assert ns.to_dict()["database_host"] == "localhost"
        assert ns.to_dict()["feature.flag"] == "enabled"
