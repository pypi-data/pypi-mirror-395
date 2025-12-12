"""Integration tests for cache management functionality."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.github_ioc_scanner.cache import CacheManager
from src.github_ioc_scanner.cache_manager import CacheManagementService
from src.github_ioc_scanner.cli import CLIInterface
from src.github_ioc_scanner.models import ScanConfig


class TestCacheManagementIntegration:
    """Integration tests for cache management."""
    
    @pytest.fixture
    def temp_cache_setup(self):
        """Set up temporary cache with real data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "integration_cache.sqlite3"
            cache_manager = CacheManager(str(cache_path))
            cli = CLIInterface()
            service = CacheManagementService(cache_manager, cli)
            
            # Add some test data
            cache_manager.store_file_content(
                "test-org/repo1", "package.json", "sha123", 
                '{"dependencies": {"lodash": "4.17.21"}}', "etag123"
            )
            cache_manager.store_file_content(
                "test-org/repo2", "requirements.txt", "sha456", 
                "requests==2.28.1\nnumpy==1.21.0", "etag456"
            )
            
            yield cache_manager, cli, service
    
    def test_cache_info_integration(self, temp_cache_setup, capsys):
        """Test cache info display integration."""
        cache_manager, cli, service = temp_cache_setup
        
        config = ScanConfig(cache_info=True)
        result = service.handle_cache_operations(config)
        
        assert result is True
        captured = capsys.readouterr()
        assert "Cache Information:" in captured.out
        assert "File content entries: 2" in captured.out
        assert "integration_cache.sqlite3" in captured.out
    
    def test_clear_cache_integration(self, temp_cache_setup, capsys):
        """Test clear cache integration."""
        cache_manager, cli, service = temp_cache_setup
        
        # Verify data exists
        content = cache_manager.get_file_content("test-org/repo1", "package.json", "sha123")
        assert content is not None
        
        # Clear cache
        config = ScanConfig(clear_cache=True)
        result = service.handle_cache_operations(config)
        
        assert result is True
        captured = capsys.readouterr()
        assert "Cleared all cache data" in captured.out
        
        # Verify data is gone
        content = cache_manager.get_file_content("test-org/repo1", "package.json", "sha123")
        assert content is None
    
    def test_refresh_repo_integration(self, temp_cache_setup, capsys):
        """Test refresh repository integration."""
        cache_manager, cli, service = temp_cache_setup
        
        # Verify data exists for both repos
        content1 = cache_manager.get_file_content("test-org/repo1", "package.json", "sha123")
        content2 = cache_manager.get_file_content("test-org/repo2", "requirements.txt", "sha456")
        assert content1 is not None
        assert content2 is not None
        
        # Refresh only repo1
        config = ScanConfig(refresh_repo="test-org/repo1")
        result = service.handle_cache_operations(config)
        
        assert result is True
        captured = capsys.readouterr()
        assert "Refreshed repository cache: removed 1 entries" in captured.out
        
        # Verify repo1 data is gone, repo2 data remains
        content1 = cache_manager.get_file_content("test-org/repo1", "package.json", "sha123")
        content2 = cache_manager.get_file_content("test-org/repo2", "requirements.txt", "sha456")
        assert content1 is None
        assert content2 is not None
    
    def test_cli_argument_parsing_integration(self):
        """Test CLI argument parsing for cache management."""
        cli = CLIInterface()
        
        # Test cache info
        config = cli.parse_arguments(["--cache-info"])
        assert config.cache_info is True
        assert cli.validate_arguments(config) is True
        
        # Test clear cache with type
        config = cli.parse_arguments(["--clear-cache-type", "file"])
        assert config.clear_cache_type == "file"
        assert cli.validate_arguments(config) is True
        
        # Test refresh repo
        config = cli.parse_arguments(["--refresh-repo", "myorg/myrepo"])
        assert config.refresh_repo == "myorg/myrepo"
        assert cli.validate_arguments(config) is True
        
        # Test cleanup cache
        config = cli.parse_arguments(["--cleanup-cache", "30"])
        assert config.cleanup_cache == 30
        assert cli.validate_arguments(config) is True
    
    def test_cli_validation_integration(self):
        """Test CLI validation for cache management."""
        cli = CLIInterface()
        
        # Test invalid refresh repo format
        config = ScanConfig(refresh_repo="invalid-format")
        assert cli.validate_cache_arguments(config) is False
        
        # Test invalid cleanup value
        config = ScanConfig(cleanup_cache=-1)
        assert cli.validate_cache_arguments(config) is False
        
        # Test conflicting operations
        config = ScanConfig(cache_info=True, clear_cache=True)
        assert cli.validate_cache_arguments(config) is False
    
    def test_error_handling_integration(self, temp_cache_setup, capsys):
        """Test error handling in cache operations."""
        cache_manager, cli, service = temp_cache_setup
        
        # Test with invalid cache operation (simulate error)
        with patch.object(cache_manager, 'clear_cache', side_effect=Exception("Test error")):
            config = ScanConfig(clear_cache=True)
            result = service.handle_cache_operations(config)
            
            assert result is True  # Should still return True to exit
            captured = capsys.readouterr()
            assert "Unexpected error in cache operation" in captured.err
    
    def test_no_cache_operations_integration(self, temp_cache_setup):
        """Test when no cache operations are specified."""
        cache_manager, cli, service = temp_cache_setup
        
        config = ScanConfig(org="test-org")  # Normal scan config
        result = service.handle_cache_operations(config)
        
        assert result is False  # Should continue with normal scan