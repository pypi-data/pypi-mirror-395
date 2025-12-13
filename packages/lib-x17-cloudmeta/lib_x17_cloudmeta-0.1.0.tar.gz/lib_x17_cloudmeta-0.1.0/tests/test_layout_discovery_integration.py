"""
Integration test: Layout-based module discovery.

Tests the Layout class for discovering and listing modules
from a directory structure.
"""

import tempfile
from pathlib import Path

import pytest

from xcloudmeta.centre.layout import Layout


class TestLayoutDiscovery:
    """Test end-to-end layout creation and module discovery."""

    @pytest.fixture
    def infrastructure_root(self):
        """Create complete infrastructure directory structure."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)

            # Create multiple platforms
            for platform in ["aws", "gcp", "azure"]:
                platform_dir = tmp_path / "platform" / platform
                platform_dir.mkdir(parents=True)
                (platform_dir / "platform.toml").write_text(
                    f"""
[platform]
name = "{platform}"
"""
                )

            # Create multiple environments
            for env in ["dev", "staging", "production"]:
                env_dir = tmp_path / "environ" / env
                env_dir.mkdir(parents=True)
                (env_dir / "environ.toml").write_text(
                    f"""
[environ]
name = "{env}"
"""
                )

            # Create packages
            for pkg in ["auth-lib", "data-lib"]:
                pkg_dir = tmp_path / "package" / pkg
                pkg_dir.mkdir(parents=True)
                (pkg_dir / "package.toml").write_text(
                    f"""
[package]
name = "{pkg}"
"""
                )

            # Create services
            for svc in ["api", "worker", "scheduler"]:
                svc_dir = tmp_path / "service" / svc
                svc_dir.mkdir(parents=True)
                (svc_dir / "service.toml").write_text(
                    f"""
[service]
name = "{svc}"
"""
                )

            yield tmp_path

    def test_layout_initialization_with_defaults(self, infrastructure_root):
        """Test layout initialization discovers correct paths."""
        layout = Layout(root=str(infrastructure_root))

        assert layout.platform_path.name == "platform"
        assert layout.environ_path.name == "environ"
        assert layout.package_path.name == "package"
        assert layout.service_path.name == "service"

    def test_layout_discovers_all_platforms(self, infrastructure_root):
        """Test layout discovers all platform modules."""
        layout = Layout(root=str(infrastructure_root))

        platforms = layout.list_platforms()

        assert len(platforms) == 3
        platform_names = {p.name for p in platforms}
        assert platform_names == {"aws", "gcp", "azure"}

        for platform in platforms:
            assert platform.kind.is_platform()
            assert platform.metafile.is_exist()

    def test_layout_discovers_all_environs(self, infrastructure_root):
        """Test layout discovers all environment modules."""
        layout = Layout(root=str(infrastructure_root))

        environs = layout.list_environs()

        assert len(environs) == 3
        environ_names = {e.name for e in environs}
        assert environ_names == {"dev", "staging", "production"}

        for environ in environs:
            assert environ.kind.is_environ()

    def test_layout_discovers_all_packages(self, infrastructure_root):
        """Test layout discovers all package modules."""
        layout = Layout(root=str(infrastructure_root))

        packages = layout.list_packages()

        assert len(packages) == 2
        package_names = {p.name for p in packages}
        assert package_names == {"auth-lib", "data-lib"}

    def test_layout_discovers_all_services(self, infrastructure_root):
        """Test layout discovers all service modules."""
        layout = Layout(root=str(infrastructure_root))

        services = layout.list_services()

        assert len(services) == 3
        service_names = {s.name for s in services}
        assert service_names == {"api", "worker", "scheduler"}

    def test_layout_describe_returns_all_paths(self, infrastructure_root):
        """Test layout describe() returns complete path information."""
        layout = Layout(root=str(infrastructure_root))

        description = layout.describe()

        assert "root" in description
        assert "platform_path" in description
        assert "environ_path" in description
        assert "package_path" in description
        assert "service_path" in description

        # All paths should be strings
        for key, value in description.items():
            assert isinstance(value, str)

    def test_layout_with_custom_paths(self, infrastructure_root):
        """Test layout with custom subdirectory paths."""
        # Create custom structure
        custom_platform = infrastructure_root / "my-platforms"
        custom_platform.mkdir()
        custom_dir = custom_platform / "custom"
        custom_dir.mkdir()
        (custom_dir / "platform.toml").write_text("[platform]\nname = 'custom'")

        layout = Layout(
            root=str(infrastructure_root),
            platform="my-platforms",
        )

        assert layout.platform_path.name == "my-platforms"
        # Should still find standard paths for others
        assert layout.environ_path.name == "environ"

    def test_layout_handles_missing_directories(self, infrastructure_root):
        """Test layout handles missing module directories gracefully."""
        # Remove service directory
        service_path = infrastructure_root / "service"
        for item in service_path.iterdir():
            if item.is_dir():
                for file in item.iterdir():
                    file.unlink()
                item.rmdir()
        service_path.rmdir()

        layout = Layout(root=str(infrastructure_root))

        # Should return empty list, not error
        services = layout.list_services()
        assert services == []

        # Other modules should still work
        platforms = layout.list_platforms()
        assert len(platforms) == 3

    def test_layout_ignores_files_in_module_directories(self, infrastructure_root):
        """Test layout only lists directories, not files."""
        # Add a file in platform directory
        (infrastructure_root / "platform" / "README.md").write_text("# Platforms")

        layout = Layout(root=str(infrastructure_root))
        platforms = layout.list_platforms()

        # Should still only find 3 platforms (directories), not the file
        assert len(platforms) == 3

    def test_layout_with_empty_infrastructure(self):
        """Test layout with completely empty infrastructure."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            layout = Layout(root=tmp_dir)

            assert layout.list_platforms() == []
            assert layout.list_environs() == []
            assert layout.list_packages() == []
            assert layout.list_services() == []
