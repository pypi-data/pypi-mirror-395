"""
Integration test: Complete Centre workflow.

Tests the complete end-to-end workflow using the Centre class
to manage infrastructure hierarchy and create overlays.
"""

import tempfile
from pathlib import Path

import pytest

from xcloudmeta.centre.centre import Centre


class TestCentreWorkflow:
    """Test end-to-end Centre management workflow."""

    @pytest.fixture
    def complete_infrastructure(self):
        """Create complete infrastructure with multiple modules."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Multiple platforms
            for platform_name in ["aws", "gcp"]:
                platform_dir = tmp_path / "platform" / platform_name
                platform_dir.mkdir(parents=True)
                region = "us-west-2" if platform_name == "aws" else "us-central1"
                (platform_dir / "platform.toml").write_text(
                    f"""
[platform]
name = "{platform_name}"
cloud = "{platform_name.upper()}"
region = "{region}"

[database]
engine = "postgres"
"""
                )

            # Multiple environments
            for env_name in ["dev", "staging", "production"]:
                env_dir = tmp_path / "environ" / env_name
                env_dir.mkdir(parents=True)
                replicas = 1 if env_name == "dev" else 3
                (env_dir / "environ.toml").write_text(
                    f"""
[environ]
name = "{env_name}"
stage = "{env_name[:4]}"

[database]
replicas = {replicas}
"""
                )

            # Multiple packages
            for pkg_name in ["auth", "data"]:
                pkg_dir = tmp_path / "package" / pkg_name
                pkg_dir.mkdir(parents=True)
                (pkg_dir / "package.toml").write_text(
                    f"""
[package]
name = "{pkg_name}"
version = "1.0.0"
"""
                )

            # Multiple services with references
            for svc_name in ["api", "worker"]:
                svc_dir = tmp_path / "service" / svc_name
                svc_dir.mkdir(parents=True)
                svc_type = "web" if svc_name == "api" else "background"
                pool_size = 20 if svc_name == "api" else 5
                toml_content = f"""
[service]
name = "{svc_name}"
type = "{svc_type}"
endpoint = "https://{{{{ ref(platform.name) }}}}.example.com/{svc_name}"

[database]
pool_size = {pool_size}
"""
                # Replace escaped braces with single braces for TOML
                toml_content = toml_content.replace("{{{{", "{{").replace("}}}}", "}}")
                (svc_dir / "service.toml").write_text(toml_content)

            yield tmp_path

    def test_centre_initialization(self, complete_infrastructure):
        """Test Centre initialization and module discovery."""
        centre = Centre(root=str(complete_infrastructure))

        assert len(centre.platforms) == 2
        assert len(centre.environs) == 3
        assert len(centre.packages) == 2
        assert len(centre.services) == 2

    def test_centre_get_platform_by_name(self, complete_infrastructure):
        """Test retrieving specific platform by name."""
        centre = Centre(root=str(complete_infrastructure))

        aws = centre.get_platform("aws")
        gcp = centre.get_platform("gcp")

        assert aws is not None
        assert aws.name == "aws"
        assert aws.meta["platform"]["cloud"] == "AWS"

        assert gcp is not None
        assert gcp.name == "gcp"
        assert gcp.meta["platform"]["cloud"] == "GCP"

    def test_centre_get_environ_by_name(self, complete_infrastructure):
        """Test retrieving specific environment by name."""
        centre = Centre(root=str(complete_infrastructure))

        dev = centre.get_environ("dev")
        prod = centre.get_environ("production")

        assert dev is not None
        assert dev.name == "dev"
        assert dev.meta["environ"]["stage"] == "dev"

        assert prod is not None
        assert prod.name == "production"
        assert prod.meta["environ"]["stage"] == "prod"

    def test_centre_get_service_by_name(self, complete_infrastructure):
        """Test retrieving specific service by name."""
        centre = Centre(root=str(complete_infrastructure))

        api = centre.get_service("api")
        worker = centre.get_service("worker")

        assert api is not None
        assert api.name == "api"
        assert api.meta["service"]["type"] == "web"

        assert worker is not None
        assert worker.name == "worker"
        assert worker.meta["service"]["type"] == "background"

    def test_centre_get_package_by_name(self, complete_infrastructure):
        """Test retrieving specific package by name."""
        centre = Centre(root=str(complete_infrastructure))

        auth = centre.get_package("auth")
        data = centre.get_package("data")

        assert auth is not None
        assert auth.name == "auth"

        assert data is not None
        assert data.name == "data"

    def test_centre_create_overlay(self, complete_infrastructure):
        """Test creating overlay from Centre."""
        centre = Centre(root=str(complete_infrastructure))

        overlay = centre.overlay(
            platform="aws",
            environ="production",
            service="api",
        )

        assert overlay is not None
        compose = overlay.get_compose()

        assert compose["platform"]["name"] == "aws"
        assert compose["environ"]["name"] == "production"
        assert compose["service"]["name"] == "api"

    def test_centre_overlay_merges_configurations(self, complete_infrastructure):
        """Test overlay correctly merges configurations from Centre modules."""
        centre = Centre(root=str(complete_infrastructure))

        overlay = centre.overlay(
            platform="aws",
            environ="production",
            service="api",
        )

        compose = overlay.get_compose()
        db_config = compose["database"]

        # Should merge database config from all modules
        assert db_config["engine"] == "postgres"  # from platform
        assert db_config["replicas"] == 3  # from production environ
        assert db_config["pool_size"] == 20  # from api service

    def test_centre_overlay_resolves_references(self, complete_infrastructure):
        """Test overlay resolves references in Centre workflow."""
        centre = Centre(root=str(complete_infrastructure))

        overlay = centre.overlay(
            platform="aws",
            environ="production",
            service="api",
        )

        compose = overlay.get_compose()

        # Reference should be resolved
        expected_endpoint = "https://aws.example.com/api"
        assert compose["service"]["endpoint"] == expected_endpoint

    def test_centre_overlay_with_different_combinations(self, complete_infrastructure):
        """Test creating overlays with different module combinations."""
        centre = Centre(root=str(complete_infrastructure))

        # AWS + dev + worker
        overlay1 = centre.overlay(platform="aws", environ="dev", service="worker")
        compose1 = overlay1.get_compose()
        assert compose1["platform"]["name"] == "aws"
        assert compose1["environ"]["name"] == "dev"
        assert compose1["service"]["name"] == "worker"
        assert compose1["database"]["replicas"] == 1  # dev has 1 replica

        # GCP + production + api
        overlay2 = centre.overlay(platform="gcp", environ="production", service="api")
        compose2 = overlay2.get_compose()
        assert compose2["platform"]["name"] == "gcp"
        assert compose2["environ"]["name"] == "production"
        assert compose2["service"]["endpoint"] == "https://gcp.example.com/api"

    def test_centre_overlay_without_service(self, complete_infrastructure):
        """Test creating overlay with only platform and environ."""
        centre = Centre(root=str(complete_infrastructure))

        overlay = centre.overlay(platform="aws", environ="production")

        compose = overlay.get_compose()
        assert "platform" in compose
        assert "environ" in compose
        assert compose["platform"]["name"] == "aws"
        assert compose["environ"]["name"] == "production"

    def test_centre_overlay_raises_on_invalid_platform(self, complete_infrastructure):
        """Test overlay raises error when platform not found."""
        centre = Centre(root=str(complete_infrastructure))

        with pytest.raises(ValueError, match="Platform.*not found"):
            centre.overlay(platform="nonexistent")

    def test_centre_overlay_raises_on_invalid_environ(self, complete_infrastructure):
        """Test overlay raises error when environ not found."""
        centre = Centre(root=str(complete_infrastructure))

        with pytest.raises(ValueError, match="Environ.*not found"):
            centre.overlay(platform="aws", environ="nonexistent")

    def test_centre_overlay_raises_on_invalid_service(self, complete_infrastructure):
        """Test overlay raises error when service not found."""
        centre = Centre(root=str(complete_infrastructure))

        with pytest.raises(ValueError, match="Service.*not found"):
            centre.overlay(platform="aws", service="nonexistent")

    def test_centre_describe(self, complete_infrastructure):
        """Test Centre describe() returns complete information."""
        centre = Centre(root=str(complete_infrastructure))

        description = centre.describe()

        assert "layout" in description
        assert "platforms" in description
        assert "environs" in description
        assert "packages" in description
        assert "services" in description

        assert set(description["platforms"]) == {"aws", "gcp"}
        assert set(description["environs"]) == {"dev", "staging", "production"}
        assert set(description["packages"]) == {"auth", "data"}
        assert set(description["services"]) == {"api", "worker"}

    def test_centre_string_representation(self, complete_infrastructure):
        """Test Centre string representations."""
        centre = Centre(root=str(complete_infrastructure))

        assert complete_infrastructure.name in str(centre)
        assert "Centre" in repr(centre)

    def test_centre_get_single_platform_without_name(self):
        """Test get_platform returns single platform when name not provided."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create only one platform
            platform_dir = tmp_path / "platform" / "aws"
            platform_dir.mkdir(parents=True)
            (platform_dir / "platform.toml").write_text('[platform]\nname = "aws"')

            centre = Centre(root=str(tmp_path))

            # Should return the single platform
            platform = centre.get_platform()
            assert platform is not None
            assert platform.name == "aws"

    def test_centre_returns_none_for_missing_module(self, complete_infrastructure):
        """Test Centre returns None for non-existent modules."""
        centre = Centre(root=str(complete_infrastructure))

        assert centre.get_platform("nonexistent") is None
        assert centre.get_environ("nonexistent") is None
        assert centre.get_package("nonexistent") is None
        assert centre.get_service("nonexistent") is None
