"""
Integration test: Module lifecycle and metadata loading.

Tests the complete workflow of creating modules, loading metadata,
and accessing module properties.
"""

import tempfile
from pathlib import Path

import pytest

from xcloudmeta.module.environ import Environ
from xcloudmeta.module.package import Package
from xcloudmeta.module.platform import Platform
from xcloudmeta.module.service import Service


class TestModuleLifecycle:
    """Test end-to-end module creation and metadata access."""

    @pytest.fixture
    def temp_structure(self):
        """Create temporary directory structure with metadata files."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Platform module
            platform_dir = tmp_path / "platform" / "aws"
            platform_dir.mkdir(parents=True)
            (platform_dir / "platform.toml").write_text(
                """
[platform]
name = "aws"
cloud = "Amazon Web Services"
region = "us-west-2"
account_id = "123456789012"

[features]
compute = true
storage = true
"""
            )
            (platform_dir / "makefile").write_text("deploy:\n\techo 'deploying'")

            # Environ module
            environ_dir = tmp_path / "environ" / "production"
            environ_dir.mkdir(parents=True)
            (environ_dir / "environ.toml").write_text(
                """
[environ]
name = "production"
stage = "prod"

[resources]
cpu = "4"
memory = "8Gi"
"""
            )

            # Package module
            package_dir = tmp_path / "package" / "core-lib"
            package_dir.mkdir(parents=True)
            (package_dir / "package.toml").write_text(
                """
[package]
name = "core-lib"
version = "1.0.0"
"""
            )

            # Service module
            service_dir = tmp_path / "service" / "api-gateway"
            service_dir.mkdir(parents=True)
            (service_dir / "service.toml").write_text(
                """
[service]
name = "api-gateway"
port = 8080
protocol = "http"
"""
            )

            yield {
                "root": tmp_path,
                "platform_dir": platform_dir,
                "environ_dir": environ_dir,
                "package_dir": package_dir,
                "service_dir": service_dir,
            }

    def test_platform_creation_and_metadata_access(self, temp_structure):
        """Test platform module creation and metadata parsing."""
        platform = Platform(
            path=temp_structure["platform_dir"],
            metafile="platform.toml",
            makefile="makefile",
        )

        assert platform.name == "aws"
        assert platform.kind.is_platform()
        assert platform.meta["platform"]["name"] == "aws"
        assert platform.meta["platform"]["region"] == "us-west-2"
        assert platform.meta["features"]["compute"] is True
        assert platform.metafile.is_exist()
        assert platform.makefile.is_exist()

    def test_environ_creation_and_metadata_access(self, temp_structure):
        """Test environment module creation and metadata parsing."""
        environ = Environ(
            path=temp_structure["environ_dir"],
            metafile="environ.toml",
        )

        assert environ.name == "production"
        assert environ.kind.is_environ()
        assert environ.meta["environ"]["name"] == "production"
        assert environ.meta["environ"]["stage"] == "prod"
        assert environ.meta["resources"]["cpu"] == "4"

    def test_package_creation_and_metadata_access(self, temp_structure):
        """Test package module creation and metadata parsing."""
        package = Package(
            path=temp_structure["package_dir"],
            metafile="package.toml",
        )

        assert package.name == "core-lib"
        assert package.kind.is_package()
        assert package.meta["package"]["name"] == "core-lib"
        assert package.meta["package"]["version"] == "1.0.0"

    def test_service_creation_and_metadata_access(self, temp_structure):
        """Test service module creation and metadata parsing."""
        service = Service(
            path=temp_structure["service_dir"],
            metafile="service.toml",
        )

        assert service.name == "api-gateway"
        assert service.kind.is_service()
        assert service.meta["service"]["name"] == "api-gateway"
        assert service.meta["service"]["port"] == 8080
        assert service.meta["service"]["protocol"] == "http"

    def test_module_describe_method(self, temp_structure):
        """Test module describe() method returns complete information."""
        platform = Platform(
            path=temp_structure["platform_dir"],
            metafile="platform.toml",
        )

        description = platform.describe()

        assert "path" in description
        assert "kind" in description
        assert "meta" in description
        assert description["kind"] == "platform"
        assert isinstance(description["meta"], dict)

    def test_module_without_metafile(self, temp_structure):
        """Test module creation when metafile doesn't exist."""
        empty_dir = temp_structure["root"] / "empty"
        empty_dir.mkdir()

        platform = Platform(path=empty_dir)

        assert platform.name == "empty"
        assert platform.meta == {}
        assert platform.metafile is None

    def test_module_string_representation(self, temp_structure):
        """Test module string representations."""
        platform = Platform(
            path=temp_structure["platform_dir"],
            metafile="platform.toml",
        )

        assert str(platform) == "aws"
        assert "Platform" in repr(platform)
        assert str(temp_structure["platform_dir"]) in repr(platform)
