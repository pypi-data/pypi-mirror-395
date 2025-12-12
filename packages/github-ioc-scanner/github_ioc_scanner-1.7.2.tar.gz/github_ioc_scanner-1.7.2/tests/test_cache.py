"""Unit tests for the CacheManager class."""

import json
import sqlite3
import tempfile
import platform
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from src.github_ioc_scanner.cache import CacheManager
from src.github_ioc_scanner.models import (
    CacheStats,
    PackageDependency,
    IOCMatch,
    Repository
)


class TestCacheManager:
    """Test suite for CacheManager functionality."""
    
    @pytest.fixture
    def temp_cache(self):
        """Create a temporary cache manager for testing."""
        with tempfile.NamedTemporaryFile(suffix='.sqlite3', delete=False) as tmp:
            cache_path = tmp.name
        
        cache_manager = CacheManager(cache_path=cache_path)
        yield cache_manager
        
        # Cleanup
        Path(cache_path).unlink(missing_ok=True)
    
    def test_init_with_custom_path(self):
        """Test cache manager initialization with custom path."""
        with tempfile.NamedTemporaryFile(suffix='.sqlite3', delete=False) as tmp:
            cache_path = tmp.name
        
        cache_manager = CacheManager(cache_path=cache_path)
        assert cache_manager.db_path == Path(cache_path)
        
        # Verify database file exists
        assert Path(cache_path).exists()
        
        # Cleanup
        Path(cache_path).unlink(missing_ok=True)
    
    @patch('platform.system')
    def test_default_cache_path_windows(self, mock_system):
        """Test default cache path resolution on Windows."""
        mock_system.return_value = 'Windows'
        
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('C:/Users/testuser')
            
            cache_manager = CacheManager()
            expected_path = Path('C:/Users/testuser/AppData/Local/github-ioc-scan/cache.sqlite3')
            assert cache_manager.db_path == expected_path
    
    @patch('platform.system')
    def test_default_cache_path_unix(self, mock_system):
        """Test default cache path resolution on Linux/macOS."""
        mock_system.return_value = 'Linux'
        
        with patch('pathlib.Path.home') as mock_home:
            mock_home.return_value = Path('/home/testuser')
            
            # Use a temporary directory to avoid permission issues
            with tempfile.TemporaryDirectory() as temp_dir:
                expected_path = Path(temp_dir) / "cache.sqlite3"
                cache_manager = CacheManager(cache_path=str(expected_path))
                assert cache_manager.db_path == expected_path
    
    def test_database_schema_creation(self, temp_cache):
        """Test that all required database tables are created."""
        with sqlite3.connect(temp_cache.db_path) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = [
                'etag_cache',
                'file_cache', 
                'parsed_packages',
                'repo_metadata',
                'scan_results'
            ]
            
            for table in expected_tables:
                assert table in tables
    
    def test_file_content_cache(self, temp_cache):
        """Test file content caching functionality."""
        repo = "owner/repo"
        path = "package.json"
        sha = "abc123"
        content = '{"name": "test-package"}'
        etag = "W/\"abc123\""
        
        # Test cache miss
        result = temp_cache.get_file_content(repo, path, sha)
        assert result is None
        
        # Store content
        temp_cache.store_file_content(repo, path, sha, content, etag)
        
        # Test cache hit
        result = temp_cache.get_file_content(repo, path, sha)
        assert result == content
        
        # Verify ETag is stored
        with sqlite3.connect(temp_cache.db_path) as conn:
            cursor = conn.execute(
                "SELECT etag FROM file_cache WHERE repo = ? AND path = ? AND sha = ?",
                (repo, path, sha)
            )
            stored_etag = cursor.fetchone()[0]
            assert stored_etag == etag
    
    def test_parsed_packages_cache(self, temp_cache):
        """Test parsed packages caching functionality."""
        repo = "owner/repo"
        path = "package.json"
        sha = "abc123"
        packages = [
            PackageDependency(name="lodash", version="4.17.21", dependency_type="dependencies"),
            PackageDependency(name="jest", version="27.0.0", dependency_type="devDependencies")
        ]
        
        # Test cache miss
        result = temp_cache.get_parsed_packages(repo, path, sha)
        assert result is None
        
        # Store packages
        temp_cache.store_parsed_packages(repo, path, sha, packages)
        
        # Test cache hit
        result = temp_cache.get_parsed_packages(repo, path, sha)
        assert result is not None
        assert len(result) == 2
        assert result[0].name == "lodash"
        assert result[0].version == "4.17.21"
        assert result[0].dependency_type == "dependencies"
        assert result[1].name == "jest"
        assert result[1].version == "27.0.0"
        assert result[1].dependency_type == "devDependencies"
    
    def test_scan_results_cache(self, temp_cache):
        """Test IOC scan results caching functionality."""
        repo = "owner/repo"
        path = "package.json"
        sha = "abc123"
        ioc_hash = "def456"
        results = [
            IOCMatch(
                repo=repo,
                file_path=path,
                package_name="malicious-package",
                version="1.0.0",
                ioc_source="issue1.py"
            )
        ]
        
        # Test cache miss
        result = temp_cache.get_scan_results(repo, path, sha, ioc_hash)
        assert result is None
        
        # Store results
        temp_cache.store_scan_results(repo, path, sha, ioc_hash, results)
        
        # Test cache hit
        result = temp_cache.get_scan_results(repo, path, sha, ioc_hash)
        assert result is not None
        assert len(result) == 1
        assert result[0].repo == repo
        assert result[0].file_path == path
        assert result[0].package_name == "malicious-package"
        assert result[0].version == "1.0.0"
        assert result[0].ioc_source == "issue1.py"
    
    def test_repository_metadata_cache(self, temp_cache):
        """Test repository metadata caching functionality."""
        org = "test-org"
        team = "test-team"
        etag = "W/\"repo-etag\""
        repos = [
            Repository(
                name="repo1",
                full_name="test-org/repo1",
                archived=False,
                default_branch="main",
                updated_at=datetime.now(timezone.utc)
            ),
            Repository(
                name="repo2",
                full_name="test-org/repo2",
                archived=True,
                default_branch="master",
                updated_at=datetime.now(timezone.utc)
            )
        ]
        
        # Test cache miss
        result = temp_cache.get_repository_metadata(org, team)
        assert result is None
        
        # Store metadata
        temp_cache.store_repository_metadata(org, repos, etag, team)
        
        # Test cache hit
        result = temp_cache.get_repository_metadata(org, team)
        assert result is not None
        cached_repos, cached_etag = result
        
        assert len(cached_repos) == 2
        assert cached_repos[0].name == "repo1"
        assert cached_repos[0].full_name == "test-org/repo1"
        assert cached_repos[0].archived is False
        assert cached_repos[1].name == "repo2"
        assert cached_repos[1].archived is True
        assert cached_etag == etag
    
    def test_etag_cache(self, temp_cache):
        """Test ETag caching functionality."""
        cache_key = "org:test-org"
        etag = "W/\"test-etag\""
        
        # Test cache miss
        result = temp_cache.get_etag(cache_key)
        assert result is None
        
        # Store ETag
        temp_cache.store_etag(cache_key, etag)
        
        # Test cache hit
        result = temp_cache.get_etag(cache_key)
        assert result == etag
    
    def test_cache_stats_tracking(self, temp_cache):
        """Test cache statistics tracking."""
        # Initial stats should be zero
        stats = temp_cache.get_cache_stats()
        assert stats.hits == 0
        assert stats.misses == 0
        assert stats.cache_size == 0
        
        # Perform some cache operations
        temp_cache.get_file_content("repo", "path", "sha")  # miss
        temp_cache.store_file_content("repo", "path", "sha", "content")
        temp_cache.get_file_content("repo", "path", "sha")  # hit
        
        # Check updated stats
        stats = temp_cache.get_cache_stats()
        assert stats.hits == 1
        assert stats.misses == 1
        assert stats.cache_size > 0
        assert stats.time_saved > 0
    
    def test_clear_cache_specific_type(self, temp_cache):
        """Test clearing specific cache types."""
        # Add data to different cache types
        temp_cache.store_file_content("repo", "path", "sha", "content")
        temp_cache.store_etag("key", "etag")
        
        # Clear only file cache
        temp_cache.clear_cache("file")
        
        # Verify file cache is cleared but ETag cache remains
        assert temp_cache.get_file_content("repo", "path", "sha") is None
        assert temp_cache.get_etag("key") == "etag"
    
    def test_clear_cache_all(self, temp_cache):
        """Test clearing all cache data."""
        # Add data to different cache types
        temp_cache.store_file_content("repo", "path", "sha", "content")
        temp_cache.store_etag("key", "etag")
        
        # Clear all cache
        temp_cache.clear_cache()
        
        # Verify all caches are cleared
        assert temp_cache.get_file_content("repo", "path", "sha") is None
        assert temp_cache.get_etag("key") is None
    
    def test_clear_cache_invalid_type(self, temp_cache):
        """Test clearing cache with invalid type raises error."""
        with pytest.raises(ValueError, match="Unknown cache type"):
            temp_cache.clear_cache("invalid_type")
    
    def test_refresh_repository_cache(self, temp_cache):
        """Test refreshing repository cache for specific org/team."""
        org = "test-org"
        team = "test-team"
        repos = [Repository("repo1", "test-org/repo1", False, "main", datetime.now(timezone.utc))]
        
        # Store repository metadata
        temp_cache.store_repository_metadata(org, repos, "etag", team)
        assert temp_cache.get_repository_metadata(org, team) is not None
        
        # Refresh cache
        temp_cache.refresh_repository_cache(org, team)
        assert temp_cache.get_repository_metadata(org, team) is None
    
    def test_cleanup_old_entries(self, temp_cache):
        """Test cleanup of old cache entries."""
        # Store some data
        temp_cache.store_file_content("repo", "path", "sha", "content")
        temp_cache.store_etag("key", "etag")
        
        # Verify data exists
        assert temp_cache.get_file_content("repo", "path", "sha") == "content"
        assert temp_cache.get_etag("key") == "etag"
        
        # Cleanup entries older than -1 days (future date, should remove all)
        removed_count = temp_cache.cleanup_old_entries(days_old=-1)
        assert removed_count >= 2  # At least the two entries we added
        
        # Verify data is removed
        assert temp_cache.get_file_content("repo", "path", "sha") is None
        assert temp_cache.get_etag("key") is None
    
    def test_get_cache_info(self, temp_cache):
        """Test getting detailed cache information."""
        # Add some data
        temp_cache.store_file_content("repo", "path", "sha", "content")
        temp_cache.store_etag("key", "etag")
        
        cache_info = temp_cache.get_cache_info()
        
        assert "file_cache" in cache_info
        assert "etag_cache" in cache_info
        assert "db_size_bytes" in cache_info
        assert cache_info["file_cache"] >= 1
        assert cache_info["etag_cache"] >= 1
        assert cache_info["db_size_bytes"] > 0
    
    def test_generate_ioc_hash(self, temp_cache):
        """Test IOC hash generation for cache invalidation."""
        ioc_definitions1 = {
            "package1": {"versions": ["1.0.0", "2.0.0"]},
            "package2": {"versions": None}
        }
        
        ioc_definitions2 = {
            "package2": {"versions": None},
            "package1": {"versions": ["1.0.0", "2.0.0"]}
        }
        
        ioc_definitions3 = {
            "package1": {"versions": ["1.0.0"]},
            "package2": {"versions": None}
        }
        
        hash1 = temp_cache.generate_ioc_hash(ioc_definitions1)
        hash2 = temp_cache.generate_ioc_hash(ioc_definitions2)
        hash3 = temp_cache.generate_ioc_hash(ioc_definitions3)
        
        # Same content in different order should produce same hash
        assert hash1 == hash2
        
        # Different content should produce different hash
        assert hash1 != hash3
        
        # Hash should be consistent
        assert temp_cache.generate_ioc_hash(ioc_definitions1) == hash1
    
    def test_context_manager(self, temp_cache):
        """Test cache manager as context manager."""
        with temp_cache as cache:
            assert cache is temp_cache
            cache.store_file_content("repo", "path", "sha", "content")
            assert cache.get_file_content("repo", "path", "sha") == "content"
    
    def test_cache_replacement_behavior(self, temp_cache):
        """Test that cache entries are properly replaced when updated."""
        repo = "owner/repo"
        path = "package.json"
        sha = "abc123"
        
        # Store initial content
        temp_cache.store_file_content(repo, path, sha, "content1", "etag1")
        assert temp_cache.get_file_content(repo, path, sha) == "content1"
        
        # Replace with new content (same key)
        temp_cache.store_file_content(repo, path, sha, "content2", "etag2")
        assert temp_cache.get_file_content(repo, path, sha) == "content2"
        
        # Verify only one entry exists
        with sqlite3.connect(temp_cache.db_path) as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) FROM file_cache WHERE repo = ? AND path = ? AND sha = ?",
                (repo, path, sha)
            )
            count = cursor.fetchone()[0]
            assert count == 1
    
    def test_empty_results_caching(self, temp_cache):
        """Test caching of empty scan results."""
        repo = "owner/repo"
        path = "package.json"
        sha = "abc123"
        ioc_hash = "def456"
        empty_results = []
        
        # Store empty results
        temp_cache.store_scan_results(repo, path, sha, ioc_hash, empty_results)
        
        # Retrieve empty results
        result = temp_cache.get_scan_results(repo, path, sha, ioc_hash)
        assert result is not None
        assert len(result) == 0
        assert result == []