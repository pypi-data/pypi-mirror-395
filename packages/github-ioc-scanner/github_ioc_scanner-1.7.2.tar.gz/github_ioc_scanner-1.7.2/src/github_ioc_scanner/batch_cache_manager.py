"""Batch-aware cache manager for optimized batch operations."""

import asyncio
import hashlib
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple, Any

from .batch_models import BatchRequest, BatchResult, BatchMetrics
from .cache import CacheManager
from .exceptions import CacheError
from .logging_config import get_logger
from .models import FileContent, Repository

logger = get_logger(__name__)


class BatchCacheManager:
    """Cache manager optimized for batch operations with intelligent cache coordination."""
    
    def __init__(self, cache_manager: CacheManager):
        """Initialize batch cache manager.
        
        Args:
            cache_manager: Base cache manager instance
        """
        self.cache_manager = cache_manager
        self._batch_cache_stats = {
            'batch_hits': 0,
            'batch_misses': 0,
            'partial_hits': 0,
            'cache_warming_operations': 0,
            'batch_cache_operations': 0
        }
        
        # Cache warming patterns tracking
        self._access_patterns = {}
        self._warming_queue = asyncio.Queue()
        self._warming_task = None
        
    async def batch_cache_lookup(
        self,
        requests: List[BatchRequest]
    ) -> Tuple[List[BatchResult], List[BatchRequest]]:
        """Perform batch cache lookup and return cached results and remaining requests.
        
        Args:
            requests: List of batch requests to check cache for
            
        Returns:
            Tuple of (cached_results, uncached_requests)
        """
        if not requests:
            return [], []
        
        logger.debug(f"Performing batch cache lookup for {len(requests)} requests")
        
        cached_results = []
        uncached_requests = []
        
        # Track cache performance
        cache_hits = 0
        cache_misses = 0
        
        # Process requests in batch for better performance
        for request in requests:
            try:
                # Generate cache key for file content
                cache_key = self._generate_file_cache_key(request.repo, request.file_path)
                
                # Try to get from cache - we need the SHA to lookup content
                # For now, we'll check if we have any cached version of this file
                cached_content = await self._get_cached_file_content(request)
                
                if cached_content:
                    # Create successful result from cache
                    result = BatchResult(
                        request=request,
                        content=cached_content,
                        from_cache=True,
                        processing_time=0.001  # Minimal time for cache hit
                    )
                    cached_results.append(result)
                    cache_hits += 1
                    logger.debug(f"Cache hit for {request.repo.full_name}:{request.file_path}")
                else:
                    # Add to uncached requests
                    uncached_requests.append(request)
                    cache_misses += 1
                    logger.debug(f"Cache miss for {request.repo.full_name}:{request.file_path}")
                    
            except Exception as e:
                logger.warning(f"Error during cache lookup for {request.file_path}: {e}")
                # On cache error, treat as cache miss
                uncached_requests.append(request)
                cache_misses += 1
        
        # Update batch cache statistics
        self._batch_cache_stats['batch_cache_operations'] += 1
        self._batch_cache_stats['batch_hits'] += cache_hits
        self._batch_cache_stats['batch_misses'] += cache_misses
        
        # Track partial hits (when some requests are cached)
        if cache_hits > 0 and cache_misses > 0:
            self._batch_cache_stats['partial_hits'] += 1
        
        logger.info(
            f"Batch cache lookup completed: {cache_hits} hits, {cache_misses} misses "
            f"({cache_hits / len(requests) * 100:.1f}% hit rate)"
        )
        
        return cached_results, uncached_requests
    
    async def batch_cache_store(
        self,
        results: List[BatchResult]
    ) -> None:
        """Store batch results in cache efficiently.
        
        Args:
            results: List of batch results to store in cache
        """
        if not results:
            return
        
        logger.debug(f"Storing {len(results)} batch results in cache")
        
        successful_stores = 0
        failed_stores = 0
        
        # Store results in batch for better performance
        for result in results:
            if result.success and result.content and not result.from_cache:
                try:
                    # Store file content in cache
                    await self._store_file_content_async(result)
                    successful_stores += 1
                    
                    # Track access patterns for cache warming
                    await self._track_access_pattern(result.request)
                    
                except Exception as e:
                    logger.warning(
                        f"Failed to store cache for {result.request.file_path}: {e}"
                    )
                    failed_stores += 1
        
        logger.info(
            f"Batch cache store completed: {successful_stores} stored, {failed_stores} failed"
        )
    
    async def _get_cached_file_content(self, request: BatchRequest) -> Optional[FileContent]:
        """Get cached file content for a batch request.
        
        Args:
            request: Batch request to get cached content for
            
        Returns:
            Cached file content if available, None otherwise
        """
        try:
            repo_name = request.repo.full_name
            file_path = request.file_path
            
            # Try to get the most recent cached version
            # Since we don't have the SHA yet, we'll use a placeholder approach
            # In a real implementation, this would be more sophisticated
            cached_content = self.cache_manager.get_file_content(repo_name, file_path, "latest")
            
            if cached_content:
                return FileContent(
                    content=cached_content,
                    sha="cached",  # Placeholder SHA
                    size=len(cached_content.encode('utf-8'))
                )
            
            return None
            
        except Exception as e:
            logger.debug(f"Error getting cached content for {request.file_path}: {e}")
            return None
    
    async def _store_file_content_async(self, result: BatchResult) -> None:
        """Store file content from batch result in cache asynchronously.
        
        Args:
            result: Batch result to store in cache
        """
        if not result.content:
            return
        
        try:
            repo_name = result.request.repo.full_name
            file_path = result.request.file_path
            content = result.content.content
            sha = result.content.sha
            
            # Store in cache (this is synchronous, but we're calling it from async context)
            self.cache_manager.store_file_content(repo_name, file_path, sha, content)
            
        except Exception as e:
            logger.warning(f"Failed to store file content in cache: {e}")
            raise
    
    def _generate_file_cache_key(self, repo: Repository, file_path: str) -> str:
        """Generate cache key for file content.
        
        Args:
            repo: Repository information
            file_path: Path to the file
            
        Returns:
            Cache key string
        """
        return f"file:{repo.full_name}:{file_path}"
    
    async def _track_access_pattern(self, request: BatchRequest) -> None:
        """Track access patterns for intelligent cache warming.
        
        Args:
            request: Batch request to track
        """
        try:
            repo_name = request.repo.full_name
            file_path = request.file_path
            
            # Track access patterns
            pattern_key = f"{repo_name}:{file_path}"
            current_time = datetime.now(timezone.utc)
            
            if pattern_key not in self._access_patterns:
                self._access_patterns[pattern_key] = {
                    'count': 0,
                    'last_access': current_time,
                    'first_access': current_time,
                    'repo': repo_name,
                    'file_path': file_path
                }
            
            self._access_patterns[pattern_key]['count'] += 1
            self._access_patterns[pattern_key]['last_access'] = current_time
            
            # If this file is accessed frequently, consider it for cache warming
            if self._access_patterns[pattern_key]['count'] >= 3:
                await self._queue_for_warming(request)
                
        except Exception as e:
            logger.debug(f"Error tracking access pattern: {e}")
    
    async def _queue_for_warming(self, request: BatchRequest) -> None:
        """Queue a request for cache warming.
        
        Args:
            request: Request to queue for warming
        """
        try:
            await self._warming_queue.put(request)
            logger.debug(f"Queued {request.file_path} for cache warming")
        except Exception as e:
            logger.debug(f"Error queuing for warming: {e}")
    
    async def start_cache_warming(self) -> None:
        """Start the cache warming background task."""
        if self._warming_task is None or self._warming_task.done():
            self._warming_task = asyncio.create_task(self._cache_warming_worker())
            logger.info("Started cache warming background task")
    
    async def stop_cache_warming(self) -> None:
        """Stop the cache warming background task."""
        if self._warming_task and not self._warming_task.done():
            self._warming_task.cancel()
            try:
                await self._warming_task
            except asyncio.CancelledError:
                pass
            logger.info("Stopped cache warming background task")
    
    async def _cache_warming_worker(self) -> None:
        """Background worker for cache warming operations."""
        logger.debug("Cache warming worker started")
        
        try:
            while True:
                try:
                    # Wait for warming requests with timeout
                    request = await asyncio.wait_for(
                        self._warming_queue.get(), 
                        timeout=30.0
                    )
                    
                    # Process warming request
                    await self._process_warming_request(request)
                    self._batch_cache_stats['cache_warming_operations'] += 1
                    
                except asyncio.TimeoutError:
                    # No warming requests, continue waiting
                    continue
                except Exception as e:
                    logger.warning(f"Error in cache warming worker: {e}")
                    await asyncio.sleep(1.0)  # Brief pause on error
                    
        except asyncio.CancelledError:
            logger.debug("Cache warming worker cancelled")
            raise
        except Exception as e:
            logger.error(f"Cache warming worker failed: {e}")
    
    async def _process_warming_request(self, request: BatchRequest) -> None:
        """Process a cache warming request.
        
        Args:
            request: Request to warm cache for
        """
        try:
            # Check if already cached
            cached_content = await self._get_cached_file_content(request)
            if cached_content:
                logger.debug(f"Cache warming skipped - already cached: {request.file_path}")
                return
            
            # This would typically involve pre-fetching the content
            # For now, we'll just log the warming attempt
            logger.debug(f"Cache warming processed for {request.file_path}")
            
        except Exception as e:
            logger.debug(f"Error processing warming request: {e}")
    
    def get_batch_cache_statistics(self) -> Dict[str, Any]:
        """Get comprehensive batch cache statistics.
        
        Returns:
            Dictionary containing batch cache statistics
        """
        total_operations = (
            self._batch_cache_stats['batch_hits'] + 
            self._batch_cache_stats['batch_misses']
        )
        
        hit_rate = 0.0
        if total_operations > 0:
            hit_rate = (self._batch_cache_stats['batch_hits'] / total_operations) * 100
        
        return {
            'batch_cache_operations': self._batch_cache_stats['batch_cache_operations'],
            'total_batch_requests': total_operations,
            'batch_cache_hits': self._batch_cache_stats['batch_hits'],
            'batch_cache_misses': self._batch_cache_stats['batch_misses'],
            'batch_hit_rate_percent': hit_rate,
            'partial_batch_hits': self._batch_cache_stats['partial_hits'],
            'cache_warming_operations': self._batch_cache_stats['cache_warming_operations'],
            'tracked_access_patterns': len(self._access_patterns),
            'warming_queue_size': self._warming_queue.qsize() if self._warming_queue else 0,
            'warming_task_active': (
                self._warming_task is not None and 
                not self._warming_task.done()
            )
        }
    
    def reset_batch_cache_statistics(self) -> None:
        """Reset batch cache statistics."""
        self._batch_cache_stats = {
            'batch_hits': 0,
            'batch_misses': 0,
            'partial_hits': 0,
            'cache_warming_operations': 0,
            'batch_cache_operations': 0
        }
        self._access_patterns.clear()
    
    async def warm_cache_for_repositories(
        self,
        repositories: List[Repository],
        common_files: Optional[List[str]] = None
    ) -> int:
        """Warm cache for commonly accessed files across repositories.
        
        Args:
            repositories: List of repositories to warm cache for
            common_files: Optional list of common files to prioritize
            
        Returns:
            Number of files queued for warming
        """
        if not repositories:
            return 0
        
        # Default common files if not provided
        if common_files is None:
            common_files = [
                'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                'requirements.txt', 'Pipfile.lock', 'poetry.lock', 'pyproject.toml',
                'Gemfile.lock', 'composer.lock', 'go.mod', 'go.sum', 'Cargo.lock'
            ]
        
        queued_count = 0
        
        for repo in repositories:
            for file_path in common_files:
                # Create warming request
                warming_request = BatchRequest(
                    repo=repo,
                    file_path=file_path,
                    priority=5  # Medium priority for warming
                )
                
                try:
                    await self._queue_for_warming(warming_request)
                    queued_count += 1
                except Exception as e:
                    logger.debug(f"Failed to queue warming for {repo.full_name}:{file_path}: {e}")
        
        logger.info(f"Queued {queued_count} files for cache warming across {len(repositories)} repositories")
        return queued_count
    
    async def invalidate_batch_cache(
        self,
        repositories: Optional[List[Repository]] = None,
        file_patterns: Optional[List[str]] = None
    ) -> int:
        """Invalidate cache entries for batch operations.
        
        Args:
            repositories: Optional list of repositories to invalidate cache for
            file_patterns: Optional list of file patterns to invalidate
            
        Returns:
            Number of cache entries invalidated
        """
        invalidated_count = 0
        
        try:
            if repositories:
                for repo in repositories:
                    count = self.cache_manager.refresh_repository_files(repo.full_name)
                    invalidated_count += count
                    logger.debug(f"Invalidated {count} cache entries for {repo.full_name}")
            
            # For file patterns, we'd need more sophisticated cache key management
            # This is a simplified implementation
            if file_patterns:
                logger.debug(f"File pattern invalidation not fully implemented: {file_patterns}")
            
            logger.info(f"Batch cache invalidation completed: {invalidated_count} entries invalidated")
            return invalidated_count
            
        except Exception as e:
            logger.error(f"Error during batch cache invalidation: {e}")
            return invalidated_count
    
    def get_cache_efficiency_metrics(self) -> Dict[str, float]:
        """Calculate cache efficiency metrics for batch operations.
        
        Returns:
            Dictionary containing efficiency metrics
        """
        stats = self.get_batch_cache_statistics()
        
        total_requests = stats['total_batch_requests']
        if total_requests == 0:
            return {
                'hit_rate': 0.0,
                'miss_rate': 0.0,
                'partial_hit_rate': 0.0,
                'warming_efficiency': 0.0
            }
        
        hit_rate = stats['batch_hit_rate_percent'] / 100
        miss_rate = 1.0 - hit_rate
        partial_hit_rate = (stats['partial_batch_hits'] / stats['batch_cache_operations']) if stats['batch_cache_operations'] > 0 else 0.0
        
        # Calculate warming efficiency (warming operations vs cache hits)
        warming_efficiency = 0.0
        if stats['cache_warming_operations'] > 0:
            warming_efficiency = min(1.0, stats['batch_cache_hits'] / stats['cache_warming_operations'])
        
        return {
            'hit_rate': hit_rate,
            'miss_rate': miss_rate,
            'partial_hit_rate': partial_hit_rate,
            'warming_efficiency': warming_efficiency
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start_cache_warming()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop_cache_warming()