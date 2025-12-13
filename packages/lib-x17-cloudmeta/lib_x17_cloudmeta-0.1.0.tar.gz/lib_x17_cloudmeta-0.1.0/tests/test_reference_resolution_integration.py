"""
Integration test: Configuration reference resolution.

Tests the complete workflow of resolving {{ ref() }} references
across module configurations.
"""

import tempfile
from pathlib import Path

import pytest

from xcloudmeta.centre.overlay import Overlay
from xcloudmeta.module.environ import Environ
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.service import Service


class TestReferenceResolution:
    """Test end-to-end reference resolution in configurations."""

    @pytest.fixture
    def modules_with_references(self):
        """Create modules with cross-references."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Platform with base values
            platform_dir = tmp_path / "platform" / "aws"
            platform_dir.mkdir(parents=True)
            (platform_dir / "platform.toml").write_text(
                """
[platform]
name = "aws"
region = "us-west-2"
account_id = "123456789012"
"""
            )

            # Environ references platform values
            environ_dir = tmp_path / "environ" / "production"
            environ_dir.mkdir(parents=True)
            (environ_dir / "environ.toml").write_text(
                """
[environ]
name = "production"
bucket = "{{ ref(platform.region) }}-prod-data"
domain = "{{ ref(platform.name) }}.example.com"

[metadata]
full_name = "{{ ref(platform.name) }}-{{ ref(environ.name) }}"
"""
            )

            # Service references both platform and environ
            service_dir = tmp_path / "service" / "api"
            service_dir.mkdir(parents=True)
            (service_dir / "service.toml").write_text(
                """
[service]
name = "api-gateway"
endpoint = "https://{{ ref(environ.domain) }}/api"
bucket_path = "{{ ref(environ.bucket) }}/{{ ref(service.name) }}"

[deployment]
region = "{{ ref(platform.region) }}"
environment = "{{ ref(environ.name) }}"
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

    def test_simple_reference_resolution(self, modules_with_references):
        """Test basic reference resolution in configurations."""
        overlay = Overlay(
            platform=modules_with_references["platform"],
            environ=modules_with_references["environ"],
        )

        compose = overlay.get_compose()

        # References should be resolved
        assert compose["environ"]["bucket"] == "us-west-2-prod-data"
        assert compose["environ"]["domain"] == "aws.example.com"

    def test_multi_reference_resolution(self, modules_with_references):
        """Test multiple references in single value."""
        overlay = Overlay(
            platform=modules_with_references["platform"],
            environ=modules_with_references["environ"],
        )

        compose = overlay.get_compose()

        # Multiple refs in one string
        assert compose["metadata"]["full_name"] == "aws-production"

    def test_nested_reference_resolution(self, modules_with_references):
        """Test references to nested configuration values."""
        overlay = Overlay(
            platform=modules_with_references["platform"],
            environ=modules_with_references["environ"],
            service=modules_with_references["service"],
        )

        compose = overlay.get_compose()

        # environ.domain and environ.bucket should be fully resolved
        assert compose["environ"]["domain"] == "aws.example.com"
        assert compose["environ"]["bucket"] == "us-west-2-prod-data"
        # With recursive resolution, nested refs should now be fully resolved
        assert compose["service"]["endpoint"] == "https://aws.example.com/api"
        assert compose["service"]["bucket_path"] == "us-west-2-prod-data/api-gateway"

    def test_reference_resolution_in_deployment_config(self, modules_with_references):
        """Test references work in nested deployment configuration."""
        overlay = Overlay(
            platform=modules_with_references["platform"],
            environ=modules_with_references["environ"],
            service=modules_with_references["service"],
        )

        compose = overlay.get_compose()
        deployment = compose["deployment"]

        assert deployment["region"] == "us-west-2"
        assert deployment["environment"] == "production"

    def test_reference_resolution_with_namespace_access(self, modules_with_references):
        """Test resolved references accessible via namespace."""
        overlay = Overlay(
            platform=modules_with_references["platform"],
            environ=modules_with_references["environ"],
            service=modules_with_references["service"],
        )

        ns = overlay.get_namespace()

        # Access resolved values through namespace
        assert ns.environ.bucket == "us-west-2-prod-data"
        assert ns.environ.domain == "aws.example.com"
        # With recursive resolution, service.endpoint should be fully resolved
        assert ns.service.endpoint == "https://aws.example.com/api"
        assert ns.deployment.region == "us-west-2"

    def test_reference_to_platform_from_service(self, modules_with_references):
        """Test service can reference platform values directly."""
        # Create simplified fixture without environ references
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            platform_dir = tmp_path / "platform" / "aws"
            platform_dir.mkdir(parents=True)
            (platform_dir / "platform.toml").write_text(
                """
[platform]
name = "aws"
region = "us-west-2"
"""
            )

            service_dir = tmp_path / "service" / "api"
            service_dir.mkdir(parents=True)
            (service_dir / "service.toml").write_text(
                """
[service]
name = "api"

[deployment]
region = "{{ ref(platform.region) }}"
"""
            )

            platform = Platform(platform_dir, metafile="platform.toml")
            service = Service(service_dir, metafile="service.toml")

            overlay = Overlay(platform=platform, service=service)
            compose = overlay.get_compose()

            # Platform reference should be resolved
            assert compose["deployment"]["region"] == "us-west-2"

    def test_invalid_reference_raises_error(self, modules_with_references):
        """Test invalid reference path raises KeyError."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            platform_dir = tmp_path / "platform" / "test"
            platform_dir.mkdir(parents=True)
            (platform_dir / "platform.toml").write_text(
                """
[platform]
name = "test"
"""
            )

            service_dir = tmp_path / "service" / "bad"
            service_dir.mkdir(parents=True)
            (service_dir / "service.toml").write_text(
                """
[service]
invalid = "{{ ref(nonexistent.path) }}"
"""
            )

            platform = Platform(platform_dir, metafile="platform.toml")
            service = Service(service_dir, metafile="service.toml")

            with pytest.raises(KeyError):
                Overlay(platform=platform, service=service)

    def test_reference_with_whitespace(self, modules_with_references):
        """Test references work with various whitespace formats."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            platform_dir = tmp_path / "platform" / "test"
            platform_dir.mkdir(parents=True)
            (platform_dir / "platform.toml").write_text(
                """
[platform]
name = "test"
value = "myvalue"
"""
            )

            service_dir = tmp_path / "service" / "test"
            service_dir.mkdir(parents=True)
            (service_dir / "service.toml").write_text(
                """
[service]
# Various whitespace formats
ref1 = "{{ref(platform.value)}}"
ref2 = "{{ ref(platform.value) }}"
ref3 = "{{  ref(platform.value)  }}"
"""
            )

            platform = Platform(platform_dir, metafile="platform.toml")
            service = Service(service_dir, metafile="service.toml")
            overlay = Overlay(platform=platform, service=service)

            compose = overlay.get_compose()

            # All formats should resolve correctly
            assert compose["service"]["ref1"] == "myvalue"
            assert compose["service"]["ref2"] == "myvalue"
            assert compose["service"]["ref3"] == "myvalue"

    def test_partial_string_reference_resolution(self, modules_with_references):
        """Test references embedded in larger strings."""
        overlay = Overlay(
            platform=modules_with_references["platform"],
            environ=modules_with_references["environ"],
        )

        compose = overlay.get_compose()

        # Reference embedded in URL
        assert compose["environ"]["bucket"] == "us-west-2-prod-data"
        assert "us-west-2" in compose["environ"]["bucket"]
        assert "prod-data" in compose["environ"]["bucket"]

    def test_circular_reference_detection(self):
        """Test that circular references are detected and raise an error."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create circular reference: A -> B -> A
            platform_dir = tmp_path / "platform" / "test"
            platform_dir.mkdir(parents=True)
            (platform_dir / "platform.toml").write_text(
                """
[platform]
name = "test"
value_a = "{{ ref(environ.value_b) }}"
"""
            )

            environ_dir = tmp_path / "environ" / "test"
            environ_dir.mkdir(parents=True)
            (environ_dir / "environ.toml").write_text(
                """
[environ]
name = "test"
value_b = "{{ ref(platform.value_a) }}"
"""
            )

            platform = Platform(platform_dir, metafile="platform.toml")
            environ = Environ(environ_dir, metafile="environ.toml")

            with pytest.raises(ValueError, match="Circular reference|unresolvable references"):
                Overlay(platform=platform, environ=environ)

    def test_deeply_nested_references_resolve(self):
        """Test that deeply nested references are resolved correctly."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create a chain: level1 -> level2 -> level3 -> level4 -> level5
            platform_dir = tmp_path / "platform" / "test"
            platform_dir.mkdir(parents=True)

            # Build a chain of references
            toml_content = '[platform]\nname = "test"\n'
            toml_content += 'level5 = "final_value"\n'
            for i in range(4, 0, -1):
                toml_content += f'level{i} = "{{{{ ref(platform.level{i + 1}) }}}}"\n'

            (platform_dir / "platform.toml").write_text(toml_content)

            platform = Platform(platform_dir, metafile="platform.toml")
            overlay = Overlay(platform=platform)
            compose = overlay.get_compose()

            # All levels should resolve to final_value
            assert compose["platform"]["level1"] == "final_value"
            assert compose["platform"]["level2"] == "final_value"
            assert compose["platform"]["level3"] == "final_value"
            assert compose["platform"]["level4"] == "final_value"
            assert compose["platform"]["level5"] == "final_value"
