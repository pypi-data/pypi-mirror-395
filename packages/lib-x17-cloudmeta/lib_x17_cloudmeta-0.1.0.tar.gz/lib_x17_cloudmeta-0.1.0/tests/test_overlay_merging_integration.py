"""
Integration test: Configuration overlay and merging.

Tests the complete workflow of merging configurations from multiple
modules and resolving cross-references.
"""

import tempfile
from pathlib import Path

import pytest

from xcloudmeta.centre.overlay import Overlay
from xcloudmeta.module.environ import Environ
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.service import Service


class TestOverlayMerging:
    """Test end-to-end configuration overlay and merging."""

    @pytest.fixture
    def modules_with_hierarchy(self):
        """Create modules with hierarchical configuration data."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Platform with base configuration
            platform_dir = tmp_path / "platform" / "aws"
            platform_dir.mkdir(parents=True)
            (platform_dir / "platform.toml").write_text(
                """
[platform]
name = "aws"
cloud = "Amazon Web Services"
region = "us-west-2"

[database]
engine = "postgres"
version = "14"

[network]
vpc_cidr = "10.0.0.0/16"
"""
            )

            # Environ overrides some platform settings
            environ_dir = tmp_path / "environ" / "production"
            environ_dir.mkdir(parents=True)
            (environ_dir / "environ.toml").write_text(
                """
[environ]
name = "production"
stage = "prod"

[database]
instance_type = "db.r5.large"
multi_az = true

[network]
public_subnet = "10.0.1.0/24"
"""
            )

            # Service adds service-specific configuration
            service_dir = tmp_path / "service" / "api"
            service_dir.mkdir(parents=True)
            (service_dir / "service.toml").write_text(
                """
[service]
name = "api-gateway"
port = 8080

[database]
pool_size = 20
timeout = 30

[resources]
cpu = "2"
memory = "4Gi"
"""
            )

            platform = Platform(platform_dir, metafile="platform.toml")
            environ = Environ(environ_dir, metafile="environ.toml")
            service = Service(service_dir, metafile="service.toml")

            yield {
                "platform": platform,
                "environ": environ,
                "service": service,
            }

    def test_overlay_merges_all_modules(self, modules_with_hierarchy):
        """Test overlay merges configurations from all modules."""
        overlay = Overlay(
            platform=modules_with_hierarchy["platform"],
            environ=modules_with_hierarchy["environ"],
            service=modules_with_hierarchy["service"],
        )

        compose = overlay.get_compose()

        # Should have all sections
        assert "platform" in compose
        assert "environ" in compose
        assert "service" in compose
        assert "database" in compose
        assert "network" in compose
        assert "resources" in compose

    def test_overlay_merges_nested_dictionaries(self, modules_with_hierarchy):
        """Test overlay correctly merges nested dictionary structures."""
        overlay = Overlay(
            platform=modules_with_hierarchy["platform"],
            environ=modules_with_hierarchy["environ"],
            service=modules_with_hierarchy["service"],
        )

        compose = overlay.get_compose()
        db_config = compose["database"]

        # Should have all database fields merged
        assert db_config["engine"] == "postgres"  # from platform
        assert db_config["version"] == "14"  # from platform
        assert db_config["instance_type"] == "db.r5.large"  # from environ
        assert db_config["multi_az"] is True  # from environ
        assert db_config["pool_size"] == 20  # from service
        assert db_config["timeout"] == 30  # from service

    def test_overlay_environ_overrides_platform(self, modules_with_hierarchy):
        """Test environment configuration overrides platform."""
        overlay = Overlay(
            platform=modules_with_hierarchy["platform"],
            environ=modules_with_hierarchy["environ"],
        )

        compose = overlay.get_compose()
        network = compose["network"]

        # Platform values
        assert network["vpc_cidr"] == "10.0.0.0/16"
        # Environ additions
        assert network["public_subnet"] == "10.0.1.0/24"

    def test_overlay_service_overrides_environ_and_platform(self, modules_with_hierarchy):
        """Test service configuration has highest priority."""
        overlay = Overlay(
            platform=modules_with_hierarchy["platform"],
            environ=modules_with_hierarchy["environ"],
            service=modules_with_hierarchy["service"],
        )

        compose = overlay.get_compose()

        # Service-specific config should be present
        assert compose["service"]["name"] == "api-gateway"
        assert compose["service"]["port"] == 8080
        assert compose["resources"]["cpu"] == "2"

    def test_overlay_with_platform_only(self, modules_with_hierarchy):
        """Test overlay works with only platform module."""
        overlay = Overlay(platform=modules_with_hierarchy["platform"])

        compose = overlay.get_compose()

        assert "platform" in compose
        assert compose["platform"]["name"] == "aws"
        assert "database" in compose

    def test_overlay_namespace_access(self, modules_with_hierarchy):
        """Test overlay provides namespace access to merged config."""
        overlay = Overlay(
            platform=modules_with_hierarchy["platform"],
            environ=modules_with_hierarchy["environ"],
            service=modules_with_hierarchy["service"],
        )

        namespace = overlay.get_namespace()

        # Test dot-notation access
        assert namespace.platform.name == "aws"
        assert namespace.environ.name == "production"
        assert namespace.service.name == "api-gateway"
        assert namespace.database.engine == "postgres"
        assert namespace.database.pool_size == 20

    def test_overlay_get_method(self, modules_with_hierarchy):
        """Test overlay get() method for accessing values."""
        overlay = Overlay(
            platform=modules_with_hierarchy["platform"],
            environ=modules_with_hierarchy["environ"],
            service=modules_with_hierarchy["service"],
        )

        # Test get with dot notation
        assert overlay.get("platform.name") == "aws"
        assert overlay.get("database.engine") == "postgres"
        assert overlay.get("service.port") == 8080

        # Test get with default
        assert overlay.get("nonexistent.key", "default") == "default"

    def test_overlay_set_method(self, modules_with_hierarchy):
        """Test overlay set() method for updating values."""
        overlay = Overlay(platform=modules_with_hierarchy["platform"])

        # Set new value
        overlay.set("custom.setting", "value")

        assert overlay.get("custom.setting") == "value"

    def test_overlay_with_no_modules(self):
        """Test overlay with no modules provided."""
        overlay = Overlay()

        compose = overlay.get_compose()
        assert compose == {}

        namespace = overlay.get_namespace()
        assert namespace.get("any.key", None) is None
