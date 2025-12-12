"""Cache management utilities for GitHub IOC Scanner."""

from typing import Dict, Optional

from .cache import CacheManager
from .cli import CLIInterface
from .exceptions import CacheError
from .logging_config import get_logger
from .models import ScanConfig

logger = get_logger(__name__)


class CacheManagementService:
    """Service for handling cache management operations."""
    
    def __init__(self, cache_manager: CacheManager, cli: CLIInterface):
        """Initialize cache management service.
        
        Args:
            cache_manager: The cache manager instance
            cli: CLI interface for displaying results
        """
        self.cache_manager = cache_manager
        self.cli = cli
    
    def handle_cache_operations(self, config: ScanConfig) -> bool:
        """Handle cache management operations based on configuration.
        
        Args:
            config: Scan configuration with cache management options
            
        Returns:
            True if a cache operation was performed (and app should exit)
            False if no cache operation was performed (continue with scan)
        """
        try:
            # Display cache information
            if config.cache_info:
                self._display_cache_info()
                return True
            
            # Clear cache operations
            if config.clear_cache:
                self._clear_all_cache()
                return True
            
            if config.clear_cache_type:
                self._clear_cache_type(config.clear_cache_type)
                return True
            
            # Refresh repository cache
            if config.refresh_repo:
                self._refresh_repository(config.refresh_repo)
                return True
            
            # Cleanup old cache entries
            if config.cleanup_cache is not None:
                self._cleanup_old_entries(config.cleanup_cache)
                return True
            
            return False
            
        except CacheError as e:
            self.cli.display_error(f"Cache operation failed: {e}")
            return True
        except Exception as e:
            logger.error(f"Unexpected error in cache operation: {e}", exc_info=True)
            self.cli.display_error(f"Unexpected error in cache operation: {e}")
            return True
    
    def _display_cache_info(self) -> None:
        """Display detailed cache information."""
        cache_info = self.cache_manager.get_detailed_cache_info()
        cache_info['cache_path'] = str(self.cache_manager.cache_path)
        self.cli.display_cache_info(cache_info)
    
    def _clear_all_cache(self) -> None:
        """Clear all cache data."""
        self.cache_manager.clear_cache()
        self.cli.display_cache_operation_result("clear")
        logger.info("Cleared all cache data")
    
    def _clear_cache_type(self, cache_type: str) -> None:
        """Clear specific type of cache data.
        
        Args:
            cache_type: Type of cache to clear (file, packages, results, repos, etags)
        """
        self.cache_manager.clear_cache(cache_type)
        self.cli.display_cache_operation_result("clear", cache_type=cache_type)
        logger.info(f"Cleared {cache_type} cache data")
    
    def _refresh_repository(self, repo_name: str) -> None:
        """Refresh cache for a specific repository.
        
        Args:
            repo_name: Repository name in format 'org/repo'
        """
        count = self.cache_manager.refresh_repository_files(repo_name)
        self.cli.display_cache_operation_result("refresh", count=count)
        logger.info(f"Refreshed cache for repository {repo_name}: removed {count} entries")
    
    def _cleanup_old_entries(self, days_old: int) -> None:
        """Clean up cache entries older than specified days.
        
        Args:
            days_old: Number of days - entries older than this will be removed
        """
        count = self.cache_manager.cleanup_old_entries(days_old)
        self.cli.display_cache_operation_result("cleanup", count=count)
        logger.info(f"Cleaned up cache entries older than {days_old} days: removed {count} entries")