"""Tests for scoop-vectrade repository structure and documentation."""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
README_FILE = ROOT / "README.md"
CONTRIBUTING_FILE = ROOT / "CONTRIBUTING.md"
LICENSE_FILE = ROOT / "LICENSE"
GITIGNORE_FILE = ROOT / ".gitignore"
CI_FILE = ROOT / ".github" / "workflows" / "ci.yml"
BUCKET_DIR = ROOT / "bucket"


@pytest.fixture
def readme_content():
    """Load README content."""
    return README_FILE.read_text()


@pytest.fixture
def contributing_content():
    """Load CONTRIBUTING content."""
    return CONTRIBUTING_FILE.read_text()


@pytest.fixture
def ci_content():
    """Load CI workflow content."""
    return CI_FILE.read_text()


@pytest.fixture
def gitignore_content():
    """Load .gitignore content."""
    return GITIGNORE_FILE.read_text()


# ============================================================
# Repository structure tests
# ============================================================


class TestRepoStructure:
    """Verify repository has correct directory structure."""

    def test_bucket_directory_exists(self):
        assert BUCKET_DIR.is_dir()

    def test_github_workflows_exists(self):
        assert (ROOT / ".github" / "workflows").is_dir()

    def test_tests_directory_exists(self):
        assert (ROOT / "tests").is_dir()

    def test_readme_exists(self):
        assert README_FILE.is_file()

    def test_license_exists(self):
        assert LICENSE_FILE.is_file()

    def test_contributing_exists(self):
        assert CONTRIBUTING_FILE.is_file()

    def test_gitignore_exists(self):
        assert GITIGNORE_FILE.is_file()

    def test_ci_workflow_exists(self):
        assert CI_FILE.is_file()

    def test_no_unexpected_manifest_files(self):
        """Only vectrade.json should be in bucket/."""
        manifests = list(BUCKET_DIR.glob("*.json"))
        assert len(manifests) == 1
        assert manifests[0].name == "vectrade.json"


# ============================================================
# README tests
# ============================================================


class TestReadme:
    """Verify README is professional and complete."""

    def test_has_h1_title(self, readme_content):
        assert readme_content.startswith("# scoop-vectrade")

    def test_has_ci_badge(self, readme_content):
        assert "actions/workflows/ci.yml/badge.svg" in readme_content

    def test_has_license_badge(self, readme_content):
        assert "license" in readme_content.lower()

    def test_has_quick_start(self, readme_content):
        assert "## Quick Start" in readme_content

    def test_has_install_command(self, readme_content):
        assert "scoop install vectrade" in readme_content

    def test_has_bucket_add_command(self, readme_content):
        assert "scoop bucket add" in readme_content

    def test_has_upgrade_section(self, readme_content):
        assert "## Upgrade" in readme_content

    def test_has_uninstall_section(self, readme_content):
        assert "## Uninstall" in readme_content

    def test_has_platform_support(self, readme_content):
        assert "## Platform Support" in readme_content

    def test_mentions_windows(self, readme_content):
        assert "Windows" in readme_content

    def test_mentions_auto_update(self, readme_content):
        assert "Auto-Update" in readme_content or "autoupdate" in readme_content.lower()

    def test_has_links_section(self, readme_content):
        assert "## Links" in readme_content

    def test_links_to_vectrade_cli(self, readme_content):
        assert "VecTrade-io/vectrade-cli" in readme_content

    def test_links_to_docs(self, readme_content):
        assert "docs.vectrade.io" in readme_content

    def test_links_to_releases(self, readme_content):
        assert "releases" in readme_content

    def test_has_license_section(self, readme_content):
        assert "## License" in readme_content

    def test_mentions_goreleaser(self, readme_content):
        assert "GoReleaser" in readme_content

    def test_no_trailing_whitespace(self, readme_content):
        for i, line in enumerate(readme_content.splitlines(), 1):
            assert line == line.rstrip(), f"Trailing whitespace on line {i}"

    def test_ends_with_newline(self, readme_content):
        assert readme_content.endswith("\n")


# ============================================================
# CONTRIBUTING tests
# ============================================================


class TestContributing:
    """Verify CONTRIBUTING.md is comprehensive."""

    def test_mentions_auto_generated(self, contributing_content):
        assert "auto-generated" in contributing_content

    def test_has_repo_structure(self, contributing_content):
        assert "Structure" in contributing_content or "structure" in contributing_content

    def test_mentions_goreleaser(self, contributing_content):
        assert "GoReleaser" in contributing_content

    def test_has_test_instructions(self, contributing_content):
        assert "pytest" in contributing_content or "test" in contributing_content.lower()

    def test_warns_against_manual_edit(self, contributing_content):
        assert "Never" in contributing_content or "never" in contributing_content


# ============================================================
# CI workflow tests
# ============================================================


class TestCIWorkflow:
    """Verify CI workflow is properly configured."""

    def test_has_name(self, ci_content):
        assert "name: CI" in ci_content

    def test_triggers_on_push(self, ci_content):
        assert "push:" in ci_content

    def test_triggers_on_pr(self, ci_content):
        assert "pull_request:" in ci_content

    def test_has_permissions(self, ci_content):
        assert "permissions:" in ci_content
        assert "contents: read" in ci_content

    def test_uses_checkout_v4(self, ci_content):
        assert "actions/checkout@v4" in ci_content

    def test_validates_json(self, ci_content):
        assert "json" in ci_content.lower()

    def test_runs_pytest(self, ci_content):
        assert "pytest" in ci_content

    def test_has_lint_job(self, ci_content):
        assert "lint" in ci_content.lower() or "Validate" in ci_content

    def test_has_scoop_check(self, ci_content):
        assert "scoop" in ci_content.lower()

    def test_runs_on_windows(self, ci_content):
        assert "windows" in ci_content


# ============================================================
# .gitignore tests
# ============================================================


class TestGitignore:
    """Verify .gitignore covers necessary patterns."""

    def test_ignores_env_files(self, gitignore_content):
        assert ".env" in gitignore_content

    def test_ignores_ds_store(self, gitignore_content):
        assert ".DS_Store" in gitignore_content

    def test_ignores_pyc(self, gitignore_content):
        assert "*.pyc" in gitignore_content or "__pycache__" in gitignore_content

    def test_ignores_log_files(self, gitignore_content):
        assert "*.log" in gitignore_content


# ============================================================
# LICENSE tests
# ============================================================


class TestLicense:
    """Verify LICENSE file."""

    def test_is_mit(self):
        content = LICENSE_FILE.read_text()
        assert "MIT License" in content

    def test_mentions_vectrade(self):
        content = LICENSE_FILE.read_text()
        assert "VecTrade" in content
