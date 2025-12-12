"""Tests for core data models."""

import pytest
from datetime import datetime

from github_ioc_scanner.models import (
    ScanConfig,
    Repository,
    FileInfo,
    PackageDependency,
    IOCMatch,
    IOCDefinition,
    CacheStats,
    ScanResults,
    FileContent,
    APIResponse,
)


def test_scan_config_defaults():
    """Test ScanConfig with default values."""
    config = ScanConfig()
    assert config.org is None
    assert config.team is None
    assert config.repo is None
    assert config.fast_mode is False
    assert config.include_archived is False
    assert config.issues_dir is None  # Default is None, not "issues"


def test_scan_config_custom():
    """Test ScanConfig with custom values."""
    config = ScanConfig(
        org="test-org",
        team="test-team",
        repo="test-repo",
        fast_mode=True,
        include_archived=True,
        issues_dir="custom-issues",
    )
    assert config.org == "test-org"
    assert config.team == "test-team"
    assert config.repo == "test-repo"
    assert config.fast_mode is True
    assert config.include_archived is True
    assert config.issues_dir == "custom-issues"


def test_repository():
    """Test Repository data class."""
    repo = Repository(
        name="test-repo",
        full_name="org/test-repo",
        archived=False,
        default_branch="main",
        updated_at=datetime(2023, 1, 1),
    )
    assert repo.name == "test-repo"
    assert repo.full_name == "org/test-repo"
    assert repo.archived is False
    assert repo.default_branch == "main"


def test_package_dependency():
    """Test PackageDependency data class."""
    dep = PackageDependency(
        name="lodash",
        version="4.17.21",
        dependency_type="dependencies",
    )
    assert dep.name == "lodash"
    assert dep.version == "4.17.21"
    assert dep.dependency_type == "dependencies"


def test_ioc_match():
    """Test IOCMatch data class."""
    match = IOCMatch(
        repo="org/repo",
        file_path="package.json",
        package_name="malicious-package",
        version="1.0.0",
        ioc_source="issues/test.py",
    )
    assert match.repo == "org/repo"
    assert match.file_path == "package.json"
    assert match.package_name == "malicious-package"
    assert match.version == "1.0.0"
    assert match.ioc_source == "issues/test.py"


def test_cache_stats_defaults():
    """Test CacheStats with default values."""
    stats = CacheStats()
    assert stats.hits == 0
    assert stats.misses == 0
    assert stats.time_saved == 0.0
    assert stats.cache_size == 0


def test_api_response_defaults():
    """Test APIResponse with default values."""
    response = APIResponse()
    assert response.data is None
    assert response.etag is None
    assert response.not_modified is False
    assert response.rate_limit_remaining == 0
    assert response.rate_limit_reset == 0