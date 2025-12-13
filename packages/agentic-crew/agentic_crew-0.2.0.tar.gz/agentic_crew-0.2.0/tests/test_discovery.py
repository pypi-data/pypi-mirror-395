"""Tests for the discovery module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest


class TestDiscovery:
    """Tests for package discovery functionality."""

    def test_discover_packages_finds_crewai_directories(self, temp_workspace: Path) -> None:
        """Test that discover_packages finds packages with .crewai directories."""
        from agentic_crew.core.discovery import discover_packages

        packages = discover_packages(workspace_root=temp_workspace)

        assert "otterfall" in packages
        assert packages["otterfall"].exists()

    def test_discover_packages_finds_crew_directories(self, tmp_path: Path) -> None:
        """Test that discover_packages finds framework-agnostic .crew directories."""
        from agentic_crew.core.discovery import discover_packages

        # Create packages with .crew directory
        pkg_dir = tmp_path / "packages" / "strata"
        crew_dir = pkg_dir / ".crew"
        crew_dir.mkdir(parents=True)
        (crew_dir / "manifest.yaml").write_text("name: strata\ncrews: {}")

        packages = discover_packages(workspace_root=tmp_path)

        assert "strata" in packages
        assert packages["strata"].name == ".crew"

    def test_discover_packages_prefers_crew_over_crewai(self, tmp_path: Path) -> None:
        """Test that .crew takes priority over .crewai when both exist."""
        from agentic_crew.core.discovery import discover_packages

        # Create package with both .crew and .crewai
        pkg_dir = tmp_path / "packages" / "hybrid"
        (pkg_dir / ".crew").mkdir(parents=True)
        (pkg_dir / ".crew" / "manifest.yaml").write_text("name: hybrid\ncrews: {}")
        (pkg_dir / ".crewai").mkdir(parents=True)
        (pkg_dir / ".crewai" / "manifest.yaml").write_text("name: hybrid\ncrews: {}")

        packages = discover_packages(workspace_root=tmp_path)

        assert "hybrid" in packages
        # .crew should be preferred (framework-agnostic first)
        assert packages["hybrid"].name == ".crew"

    def test_discover_packages_returns_empty_when_no_packages(self, tmp_path: Path) -> None:
        """Test that discover_packages returns empty dict when no config dirs exist."""
        from agentic_crew.core.discovery import discover_packages

        # Create empty packages directory
        packages_dir = tmp_path / "packages"
        packages_dir.mkdir()
        (packages_dir / "some_package").mkdir()

        packages = discover_packages(workspace_root=tmp_path)

        assert packages == {}

    def test_discover_all_framework_configs(self, tmp_path: Path) -> None:
        """Test discovering all framework configs for a package."""
        from agentic_crew.core.discovery import discover_all_framework_configs

        # Create package with multiple framework configs
        pkg_dir = tmp_path / "packages" / "multi"
        (pkg_dir / ".crew").mkdir(parents=True)
        (pkg_dir / ".crew" / "manifest.yaml").write_text("name: multi\ncrews: {}")
        (pkg_dir / ".crewai").mkdir(parents=True)
        (pkg_dir / ".crewai" / "manifest.yaml").write_text("name: multi\ncrews: {}")

        configs = discover_all_framework_configs(workspace_root=tmp_path)

        assert "multi" in configs
        assert None in configs["multi"]  # .crew -> None (agnostic)
        assert "crewai" in configs["multi"]

    def test_list_crews_returns_crews_from_manifest(self, temp_workspace: Path) -> None:
        """Test that list_crews returns crew definitions from manifest."""
        from agentic_crew.core.discovery import list_crews

        with patch(
            "agentic_crew.core.discovery.discover_packages",
            return_value={"otterfall": temp_workspace / "packages" / "otterfall" / ".crewai"},
        ):
            crews_by_package = list_crews()

        assert "otterfall" in crews_by_package
        crews = crews_by_package["otterfall"]
        assert len(crews) == 1
        assert crews[0]["name"] == "test_crew"

    def test_list_crews_filters_by_package_name(self, temp_workspace: Path) -> None:
        """Test that list_crews can filter to a specific package."""
        from agentic_crew.core.discovery import list_crews

        with patch(
            "agentic_crew.core.discovery.discover_packages",
            return_value={"otterfall": temp_workspace / "packages" / "otterfall" / ".crewai"},
        ):
            crews_by_package = list_crews(package_name="otterfall")

        assert "otterfall" in crews_by_package
        assert len(crews_by_package) == 1

    def test_list_crews_returns_empty_for_nonexistent_package(self, temp_workspace: Path) -> None:
        """Test that list_crews returns empty for non-existent package."""
        from agentic_crew.core.discovery import list_crews

        with patch(
            "agentic_crew.core.discovery.discover_packages",
            return_value={"otterfall": temp_workspace / "packages" / "otterfall" / ".crewai"},
        ):
            crews_by_package = list_crews(package_name="nonexistent")

        assert crews_by_package == {}

    def test_load_manifest_parses_yaml(self, temp_workspace: Path) -> None:
        """Test that load_manifest parses YAML correctly."""
        from agentic_crew.core.discovery import load_manifest

        crewai_dir = temp_workspace / "packages" / "otterfall" / ".crewai"
        manifest = load_manifest(crewai_dir)

        assert manifest is not None
        assert manifest.get("name") == "otterfall"
        assert "crews" in manifest

    def test_get_workspace_root_finds_root(self) -> None:
        """Test that get_workspace_root finds the workspace root."""
        from agentic_crew.core.discovery import get_workspace_root

        # This should find the actual workspace root
        root = get_workspace_root()

        # Verify it looks like a workspace root
        assert (root / "packages").exists() or root == Path.cwd()

    def test_get_framework_from_config_dir(self) -> None:
        """Test framework detection from directory name."""
        from agentic_crew.core.discovery import get_framework_from_config_dir

        assert get_framework_from_config_dir(Path("/some/path/.crew")) is None
        assert get_framework_from_config_dir(Path("/some/path/.crewai")) == "crewai"
        assert get_framework_from_config_dir(Path("/some/path/.langgraph")) == "langgraph"
        assert get_framework_from_config_dir(Path("/some/path/.strands")) == "strands"

    def test_get_crew_config_includes_required_framework(self, temp_workspace: Path) -> None:
        """Test that get_crew_config includes required_framework field."""
        from agentic_crew.core.discovery import get_crew_config

        crewai_dir = temp_workspace / "packages" / "otterfall" / ".crewai"
        config = get_crew_config(crewai_dir, "test_crew")

        assert config["required_framework"] == "crewai"


class TestDecomposer:
    """Tests for the decomposer module."""

    def test_is_framework_available_caches_results(self) -> None:
        """Test that framework availability is cached."""
        from agentic_crew.core.decomposer import _framework_cache, is_framework_available

        # Clear cache first
        _framework_cache.clear()

        # Check availability (will cache result)
        result1 = is_framework_available("nonexistent_framework")
        result2 = is_framework_available("nonexistent_framework")

        assert result1 is False
        assert result2 is False
        assert "nonexistent_framework" in _framework_cache

    def test_detect_framework_raises_when_none_available(self) -> None:
        """Test that detect_framework raises when no frameworks are available."""
        from agentic_crew.core.decomposer import detect_framework

        with patch("agentic_crew.core.decomposer.is_framework_available", return_value=False):
            with pytest.raises(RuntimeError, match="No AI frameworks installed"):
                detect_framework()

    def test_detect_framework_respects_priority(self) -> None:
        """Test that frameworks are detected in priority order."""
        from agentic_crew.core.decomposer import detect_framework

        def mock_available(framework):
            return framework in ["langgraph", "strands"]

        with patch(
            "agentic_crew.core.decomposer.is_framework_available",
            side_effect=mock_available,
        ):
            result = detect_framework()

        # langgraph should be preferred over strands
        assert result == "langgraph"
