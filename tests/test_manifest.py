"""Tests for scoop-vectrade manifest validation."""

import json
import re
from pathlib import Path

import pytest

BUCKET_DIR = Path(__file__).parent.parent / "bucket"
MANIFEST_FILE = BUCKET_DIR / "vectrade.json"


@pytest.fixture
def manifest():
    """Load and parse the manifest."""
    return json.loads(MANIFEST_FILE.read_text())


@pytest.fixture
def manifest_text():
    """Load manifest as raw text."""
    return MANIFEST_FILE.read_text()


class TestManifestExists:
    """Verify manifest file exists and is valid JSON."""

    def test_bucket_directory_exists(self):
        assert BUCKET_DIR.is_dir(), "bucket/ directory must exist"

    def test_manifest_file_exists(self):
        assert MANIFEST_FILE.is_file(), "bucket/vectrade.json must exist"

    def test_manifest_not_empty(self, manifest_text):
        assert len(manifest_text.strip()) > 0

    def test_manifest_valid_json(self, manifest_text):
        try:
            json.loads(manifest_text)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON: {e}")

    def test_manifest_is_object(self, manifest):
        assert isinstance(manifest, dict), "Manifest root must be a JSON object"


class TestRequiredFields:
    """Verify all required Scoop manifest fields are present."""

    def test_has_version(self, manifest):
        assert "version" in manifest

    def test_has_description(self, manifest):
        assert "description" in manifest

    def test_has_homepage(self, manifest):
        assert "homepage" in manifest

    def test_has_license(self, manifest):
        assert "license" in manifest

    def test_has_architecture(self, manifest):
        assert "architecture" in manifest

    def test_has_bin(self, manifest):
        assert "bin" in manifest

    def test_has_checkver(self, manifest):
        assert "checkver" in manifest

    def test_has_autoupdate(self, manifest):
        assert "autoupdate" in manifest


class TestMetadata:
    """Verify metadata values are correct."""

    def test_version_is_semver(self, manifest):
        assert re.match(r"^\d+\.\d+\.\d+$", manifest["version"])

    def test_description_mentions_vectrade(self, manifest):
        assert "vectrade" in manifest["description"].lower() or "VecTrade" in manifest["description"]

    def test_homepage_is_vectrade_cli(self, manifest):
        assert "VecTrade-io/vectrade-cli" in manifest["homepage"]

    def test_license_is_mit(self, manifest):
        assert manifest["license"] == "MIT"

    def test_bin_is_vectrade_exe(self, manifest):
        assert manifest["bin"] == "vectrade.exe"


class TestArchitecture:
    """Verify architecture configuration."""

    def test_has_64bit(self, manifest):
        assert "64bit" in manifest["architecture"]

    def test_has_arm64(self, manifest):
        assert "arm64" in manifest["architecture"]

    def test_64bit_has_url(self, manifest):
        assert "url" in manifest["architecture"]["64bit"]

    def test_64bit_has_hash(self, manifest):
        assert "hash" in manifest["architecture"]["64bit"]

    def test_arm64_has_url(self, manifest):
        assert "url" in manifest["architecture"]["arm64"]

    def test_arm64_has_hash(self, manifest):
        assert "hash" in manifest["architecture"]["arm64"]


class TestURLs:
    """Verify download URLs are correct."""

    def test_64bit_url_points_to_releases(self, manifest):
        url = manifest["architecture"]["64bit"]["url"]
        assert "github.com/VecTrade-io/vectrade-cli/releases" in url

    def test_arm64_url_points_to_releases(self, manifest):
        url = manifest["architecture"]["arm64"]["url"]
        assert "github.com/VecTrade-io/vectrade-cli/releases" in url

    def test_64bit_url_is_zip(self, manifest):
        url = manifest["architecture"]["64bit"]["url"]
        assert url.endswith(".zip")

    def test_arm64_url_is_zip(self, manifest):
        url = manifest["architecture"]["arm64"]["url"]
        assert url.endswith(".zip")

    def test_64bit_url_contains_version(self, manifest):
        url = manifest["architecture"]["64bit"]["url"]
        assert manifest["version"] in url

    def test_arm64_url_contains_version(self, manifest):
        url = manifest["architecture"]["arm64"]["url"]
        assert manifest["version"] in url

    def test_64bit_url_has_windows_amd64(self, manifest):
        url = manifest["architecture"]["64bit"]["url"]
        assert "windows_amd64" in url

    def test_arm64_url_has_windows_arm64(self, manifest):
        url = manifest["architecture"]["arm64"]["url"]
        assert "windows_arm64" in url


class TestCheckver:
    """Verify checkver configuration for auto-updates."""

    def test_checkver_has_github(self, manifest):
        assert "github" in manifest["checkver"]

    def test_checkver_github_url(self, manifest):
        assert "VecTrade-io/vectrade-cli" in manifest["checkver"]["github"]


class TestAutoupdate:
    """Verify autoupdate configuration."""

    def test_autoupdate_has_architecture(self, manifest):
        assert "architecture" in manifest["autoupdate"]

    def test_autoupdate_has_64bit(self, manifest):
        assert "64bit" in manifest["autoupdate"]["architecture"]

    def test_autoupdate_has_arm64(self, manifest):
        assert "arm64" in manifest["autoupdate"]["architecture"]

    def test_autoupdate_64bit_url_template(self, manifest):
        url = manifest["autoupdate"]["architecture"]["64bit"]["url"]
        assert "$version" in url
        assert "windows_amd64" in url

    def test_autoupdate_arm64_url_template(self, manifest):
        url = manifest["autoupdate"]["architecture"]["arm64"]["url"]
        assert "$version" in url
        assert "windows_arm64" in url

    def test_autoupdate_has_hash(self, manifest):
        assert "hash" in manifest["autoupdate"]

    def test_autoupdate_hash_uses_checksums(self, manifest):
        hash_config = manifest["autoupdate"]["hash"]
        assert "checksums.txt" in hash_config.get("url", "")


class TestManifestFormatting:
    """Verify JSON formatting conventions."""

    def test_uses_2_space_indent(self, manifest_text):
        # Check that indentation uses 2 spaces (Scoop convention)
        lines = manifest_text.splitlines()
        for i, line in enumerate(lines, 1):
            stripped = line.lstrip()
            if stripped and line != stripped:
                indent = line[: len(line) - len(stripped)]
                assert indent.replace("  ", "") == "", f"Non-2-space indent on line {i}"

    def test_no_trailing_whitespace(self, manifest_text):
        for i, line in enumerate(manifest_text.splitlines(), 1):
            assert line == line.rstrip(), f"Trailing whitespace on line {i}"

    def test_ends_with_newline(self, manifest_text):
        assert manifest_text.endswith("\n")

    def test_no_bom(self, manifest_text):
        assert not manifest_text.startswith("\ufeff"), "File must not have BOM"
