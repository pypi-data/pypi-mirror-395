"""Tests for cache management utilities."""

import pytest
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

from src.github_ioc_scanner.cache import CacheManager
from src.github_ioc_scanner.cache_manager import CacheManagementService
from src.github_ioc_scanner.cli import CLIInterface
from src.github_ioc_scanner.models import (
    ScanConfig, 
    PackageDependency, 
    IOCMatch, 
    Repository
)


class TestCacheManager:
    """Test cache management functionality."""
    
    @pytest.fixture
    def temp_cache(self):
        """Create a temporary cache for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "test_cache.sqlite3"
            cache_manager = CacheManager(str(cache_path))
            yield cache_manager
    
    @pytest.fixture
    def populated_cache(self, temp_cache):
        """Create a cache with test data."""
        # Add file content
        temp_cache.store_file_content(
            "test-org/repo1", "package.json", "sha123", 
            '{"dependencies": {"test-pkg": "1.0.0"}}', "etag123"
        )
        temp_cache.store_file_content(
            "test-org/repo2", "yarn.lock", "sha456", 
            "test-pkg@1.0.0:\n  version: 1.0.0", "etag456"
        )
        
        # Add parsed packages
        packages = [
            PackageDependency("test-pkg", "1.0.0", "dependencies"),
            PackageDependency("other-pkg", "2.0.0", "devDependencies")
        ]
        temp_cache.store_parsed_packages("test-org/repo1", "package.json", "sha123", packages)
        
        # Add scan results
        matches = [
            IOCMatch("test-org/repo1", "package.json", "test-pkg", "1.0.0", "test_ioc.py")
        ]
        temp_cache.store_scan_results("test-org/repo1", "package.json", "sha123", "ioc_hash", matches)
        
        # Add repository metadata
        repos = [
            Repository("repo1", "test-org/repo1", False, "main", datetime.now(timezone.utc)),
            Repository("repo2", "test-org/repo2", True, "master", datetime.now(timezone.utc))
        ]
        temp_cache.store_repository_metadata("test-org", repos, "repo_etag")
        
        # Add ETags
        temp_cache.store_etag("test-key", "test-etag-value")
        
        return temp_cache
    
    def test_refresh_repository_files(self, populated_cache):
        """Test refreshing cache for a specific repository."""
        # Verify data exists before refresh
        content = populated_cache.get_file_content("test-org/repo1", "package.json", "sha123")
        assert content is not None
        
        packages = populated_cache.get_parsed_packages("test-org/repo1", "package.json", "sha123")
        assert packages is not None
        
        results = populated_cache.get_scan_results("test-org/repo1", "package.json", "sha123", "ioc_hash")
        assert results is not None
        
        # Refresh repository cache
        removed_count = populated_cache.refresh_repository_files("test-org/repo1")
        assert removed_count == 3  # file_cache + parsed_packages + scan_results
        
        # Verify data is removed for repo1
        content = populated_cache.get_file_content("test-org/repo1", "package.json", "sha123")
        assert content is None
        
        packages = populated_cache.get_parsed_packages("test-org/repo1", "package.json", "sha123")
        assert packages is None
        
        results = populated_cache.get_scan_results("test-org/repo1", "package.json", "sha123", "ioc_hash")
        assert results is None
        
        # Verify data still exists for repo2
        content = populated_cache.get_file_content("test-org/repo2", "yarn.lock", "sha456")
        assert content is not None
    
    def test_clear_cache_by_type(self, populated_cache):
        """Test clearing specific cache types."""
        # Clear file cache only
        populated_cache.clear_cache("file")
        
        # File content should be gone
        content = populated_cache.get_file_content("test-org/repo1", "package.json", "sha123")
        assert content is None
        
        # Other data should still exist
        packages = populated_cache.get_parsed_packages("test-org/repo1", "package.json", "sha123")
        assert packages is not None
        
        results = populated_cache.get_scan_results("test-org/repo1", "package.json", "sha123", "ioc_hash")
        assert results is not None
    
    def test_clear_all_cache(self, populated_cache):
        """Test clearing all cache data."""
        populated_cache.clear_cache()
        
        # All data should be gone
        content = populated_cache.get_file_content("test-org/repo1", "package.json", "sha123")
        assert content is None
        
        packages = populated_cache.get_parsed_packages("test-org/repo1", "package.json", "sha123")
        assert packages is None
        
        results = populated_cache.get_scan_results("test-org/repo1", "package.json", "sha123", "ioc_hash")
        assert results is None
        
        repo_data = populated_cache.get_repository_metadata("test-org")
        assert repo_data is None
        
        etag = populated_cache.get_etag("test-key")
        assert etag is None
    
    def test_cleanup_old_entries(self, temp_cache):
        """Test cleaning up old cache entries."""
        # Add entries with different timestamps
        now = datetime.now(timezone.utc)
        old_timestamp = int((now - timedelta(days=35)).timestamp())
        recent_timestamp = int((now - timedelta(days=5)).timestamp())
        
        # Manually insert entries with specific timestamps
        import sqlite3
        with sqlite3.connect(temp_cache.db_path) as conn:
            # Old entries
            conn.execute(
                "INSERT INTO file_cache (repo, path, sha, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("old-repo", "old-file", "old-sha", "old-content", old_timestamp)
            )
            conn.execute(
                "INSERT INTO parsed_packages (repo, path, sha, packages_json, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("old-repo", "old-file", "old-sha", "[]", old_timestamp)
            )
            
            # Recent entries
            conn.execute(
                "INSERT INTO file_cache (repo, path, sha, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                ("new-repo", "new-file", "new-sha", "new-content", recent_timestamp)
            )
        
        # Clean up entries older than 30 days
        removed_count = temp_cache.cleanup_old_entries(30)
        assert removed_count == 2  # 2 old entries
        
        # Verify old entries are gone
        content = temp_cache.get_file_content("old-repo", "old-file", "old-sha")
        assert content is None
        
        # Verify recent entries remain
        content = temp_cache.get_file_content("new-repo", "new-file", "new-sha")
        assert content == "new-content"
    
    def test_get_detailed_cache_info(self, populated_cache):
        """Test getting detailed cache information."""
        cache_info = populated_cache.get_detailed_cache_info()
        
        # Check basic counts
        assert cache_info['file_cache'] == 2
        assert cache_info['parsed_packages'] == 1
        assert cache_info['scan_results'] == 1
        assert cache_info['repo_metadata'] == 1
        assert cache_info['etag_cache'] == 1
        
        # Check top repositories
        assert 'top_repositories' in cache_info
        assert len(cache_info['top_repositories']) > 0
        
        # Check cache age information
        assert 'cache_age' in cache_info
        assert cache_info['cache_age']['oldest_entry'] is not None
        assert cache_info['cache_age']['newest_entry'] is not None
    
    def test_invalid_cache_type(self, temp_cache):
        """Test clearing cache with invalid type."""
        with pytest.raises(ValueError, match="Unknown cache type"):
            temp_cache.clear_cache("invalid_type")


class TestCacheManagementService:
    """Test cache management service."""
    
    @pytest.fixture
    def cache_service(self):
        """Create cache management service with mocks."""
        cache_manager = Mock(spec=CacheManager)
        cli = Mock(spec=CLIInterface)
        return CacheManagementService(cache_manager, cli)
    
    def test_handle_cache_info(self, cache_service):
        """Test handling cache info operation."""
        config = ScanConfig(cache_info=True)
        cache_service.cache_manager.get_detailed_cache_info.return_value = {
            'file_cache': 100,
            'db_size_bytes': 1024
        }
        cache_service.cache_manager.cache_path = Path("/test/cache.db")
        
        result = cache_service.handle_cache_operations(config)
        
        assert result is True  # Should exit after operation
        cache_service.cache_manager.get_detailed_cache_info.assert_called_once()
        cache_service.cli.display_cache_info.assert_called_once()
    
    def test_handle_clear_cache(self, cache_service):
        """Test handling clear cache operation."""
        config = ScanConfig(clear_cache=True)
        
        result = cache_service.handle_cache_operations(config)
        
        assert result is True
        cache_service.cache_manager.clear_cache.assert_called_once_with()
        cache_service.cli.display_cache_operation_result.assert_called_once_with("clear")
    
    def test_handle_clear_cache_type(self, cache_service):
        """Test handling clear cache type operation."""
        config = ScanConfig(clear_cache_type="file")
        
        result = cache_service.handle_cache_operations(config)
        
        assert result is True
        cache_service.cache_manager.clear_cache.assert_called_once_with("file")
        cache_service.cli.display_cache_operation_result.assert_called_once_with("clear", cache_type="file")
    
    def test_handle_refresh_repo(self, cache_service):
        """Test handling refresh repository operation."""
        config = ScanConfig(refresh_repo="test-org/test-repo")
        cache_service.cache_manager.refresh_repository_files.return_value = 42
        
        result = cache_service.handle_cache_operations(config)
        
        assert result is True
        cache_service.cache_manager.refresh_repository_files.assert_called_once_with("test-org/test-repo")
        cache_service.cli.display_cache_operation_result.assert_called_once_with("refresh", count=42)
    
    def test_handle_cleanup_cache(self, cache_service):
        """Test handling cleanup cache operation."""
        config = ScanConfig(cleanup_cache=30)
        cache_service.cache_manager.cleanup_old_entries.return_value = 15
        
        result = cache_service.handle_cache_operations(config)
        
        assert result is True
        cache_service.cache_manager.cleanup_old_entries.assert_called_once_with(30)
        cache_service.cli.display_cache_operation_result.assert_called_once_with("cleanup", count=15)
    
    def test_no_cache_operations(self, cache_service):
        """Test when no cache operations are specified."""
        config = ScanConfig()
        
        result = cache_service.handle_cache_operations(config)
        
        assert result is False  # Should continue with normal scan


class TestCLICacheValidation:
    """Test CLI cache argument validation."""
    
    @pytest.fixture
    def cli(self):
        """Create CLI interface."""
        return CLIInterface()
    
    def test_validate_refresh_repo_format(self, cli):
        """Test validation of refresh-repo format."""
        # Valid format
        config = ScanConfig(refresh_repo="test-org/test-repo")
        assert cli.validate_cache_arguments(config) is True
        
        # Invalid format - no slash
        config = ScanConfig(refresh_repo="invalid-format")
        assert cli.validate_cache_arguments(config) is False
        
        # Invalid format - invalid characters
        config = ScanConfig(refresh_repo="test@org/test-repo")
        assert cli.validate_cache_arguments(config) is False
    
    def test_validate_cleanup_cache_value(self, cli):
        """Test validation of cleanup-cache value."""
        # Valid value
        config = ScanConfig(cleanup_cache=30)
        assert cli.validate_cache_arguments(config) is True
        
        # Invalid value - negative
        config = ScanConfig(cleanup_cache=-1)
        assert cli.validate_cache_arguments(config) is False
        
        # Invalid value - zero
        config = ScanConfig(cleanup_cache=0)
        assert cli.validate_cache_arguments(config) is False
    
    def test_conflicting_cache_operations(self, cli):
        """Test validation of conflicting cache operations."""
        # Single operation - should pass
        config = ScanConfig(cache_info=True)
        assert cli.validate_cache_arguments(config) is True
        
        # Multiple operations - should fail
        config = ScanConfig(cache_info=True, clear_cache=True)
        assert cli.validate_cache_arguments(config) is False
        
        config = ScanConfig(refresh_repo="org/repo", cleanup_cache=30)
        assert cli.validate_cache_arguments(config) is False
    
    def test_parse_cache_arguments(self, cli):
        """Test parsing cache management arguments."""
        # Test cache info
        config = cli.parse_arguments(["--cache-info"])
        assert config.cache_info is True
        
        # Test clear cache
        config = cli.parse_arguments(["--clear-cache"])
        assert config.clear_cache is True
        
        # Test clear cache type
        config = cli.parse_arguments(["--clear-cache-type", "file"])
        assert config.clear_cache_type == "file"
        
        # Test refresh repo
        config = cli.parse_arguments(["--refresh-repo", "org/repo"])
        assert config.refresh_repo == "org/repo"
        
        # Test cleanup cache
        config = cli.parse_arguments(["--cleanup-cache", "30"])
        assert config.cleanup_cache == 30


class TestCLICacheDisplay:
    """Test CLI cache information display."""
    
    @pytest.fixture
    def cli(self):
        """Create CLI interface."""
        return CLIInterface()
    
    def test_display_cache_info_basic(self, cli, capsys):
        """Test displaying basic cache information."""
        cache_info = {
            'cache_path': '/test/cache.db',
            'db_size_bytes': 1048576,  # 1 MB
            'file_cache': 100,
            'parsed_packages': 50,
            'scan_results': 25,
            'repo_metadata': 10,
            'etag_cache': 75
        }
        
        cli.display_cache_info(cache_info)
        
        captured = capsys.readouterr()
        assert "Cache Information:" in captured.out
        assert "/test/cache.db" in captured.out
        assert "1.0 MB" in captured.out
        assert "File content entries: 100" in captured.out
        assert "Total entries: 260" in captured.out
    
    def test_display_cache_info_with_repos(self, cli, capsys):
        """Test displaying cache info with top repositories."""
        cache_info = {
            'cache_path': '/test/cache.db',
            'db_size_bytes': 1024,
            'file_cache': 10,
            'parsed_packages': 5,
            'scan_results': 2,
            'repo_metadata': 1,
            'etag_cache': 3,
            'top_repositories': [
                {'repo': 'org/repo1', 'files': 50},
                {'repo': 'org/repo2', 'files': 25}
            ],
            'cache_age': {
                'oldest_entry': '2024-01-01T00:00:00+00:00',
                'newest_entry': '2024-01-02T00:00:00+00:00',
                'average_age_days': 15.5
            }
        }
        
        cli.display_cache_info(cache_info)
        
        captured = capsys.readouterr()
        assert "Top Cached Repositories:" in captured.out
        assert "org/repo1: 50 files" in captured.out
        assert "org/repo2: 25 files" in captured.out
        assert "Cache Age:" in captured.out
        assert "Average age: 15.5 days" in captured.out
    
    def test_display_cache_operation_results(self, cli, capsys):
        """Test displaying cache operation results."""
        # Test clear operation
        cli.display_cache_operation_result("clear")
        captured = capsys.readouterr()
        assert "Cleared all cache data" in captured.out
        
        # Test clear with type
        cli.display_cache_operation_result("clear", cache_type="file")
        captured = capsys.readouterr()
        assert "Cleared file cache" in captured.out
        
        # Test refresh operation
        cli.display_cache_operation_result("refresh", count=42)
        captured = capsys.readouterr()
        assert "Refreshed repository cache: removed 42 entries" in captured.out
        
        # Test cleanup operation
        cli.display_cache_operation_result("cleanup", count=15)
        captured = capsys.readouterr()
        assert "Cleaned up old cache entries: removed 15 entries" in captured.out