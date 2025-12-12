"""Cache-batch coordination layer for seamless integration of caching with batch operations."""

import asyncio
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple, Any

from .async_github_client import AsyncGitHubClient
from .batch_cache_manager import BatchCacheManager
from .batch_models import BatchRequest, BatchResult, BatchMetrics, BatchConfig
from .cache import CacheManager
from .cache_warming_manager import CacheWarmingManager
from .exceptions import CacheError, BatchProcessingError
from .logging_config import get_logger
from .models import Repository, FileContent

logger = get_logger(__name__)


class BatchCacheCoordinator:
    """Coordinates cache operations with batch processing for optimal performance."""
    
    def __init__(
        self,
        cache_manager: CacheManager,
        github_client: Optional[AsyncGitHubClient] = None,
        batch_config: Optional[BatchConfig] = None
    ):
        """Initialize batch cache coordinator.
        
        Args:
            cache_manager: Base cache manager instance
            github_client: Optional async GitHub client for cache warming
            batch_config: Optional batch processing configuration
        """
        self.cache_manager = cache_manager
        self.github_client = github_client
        self.batch_config = batch_config or BatchConfig()
        
        # Initialize cache components
        self.batch_cache_manager = BatchCacheManager(cache_manager)
        self.cache_warming_manager = CacheWarmingManager(
            cache_manager=cache_manager,
            github_client=github_client,
            max_warming_tasks=self.batch_config.max_batch_size * 2,
            warming_batch_size=min(10, self.batch_config.max_concurrent_requests)
        )
        
        # Coordination state
        self.active_batch_operations: Set[str] = set()
        self.coordination_stats = {
            'total_batch_operations': 0,
            'cache_optimized_operations': 0,
            'warming_triggered_operations': 0,
            'invalidation_operations': 0,
            'coordination_time_saved': 0.0
        }
        
        # Cache invalidation tracking
        self.pending_invalidations: Dict[str, datetime] = {}
        self.invalidation_lock = asyncio.Lock()
        
    async def start(self):
        """Start the cache coordination services."""
        await self.batch_cache_manager.start_cache_warming()
        await self.cache_warming_manager.start()
        logger.info("Started batch cache coordination services")
    
    async def stop(self):
        """Stop the cache coordination services."""
        await self.batch_cache_manager.stop_cache_warming()
        await self.cache_warming_manager.stop()
        logger.info("Stopped batch cache coordination services")
    
    async def coordinate_batch_operation(
        self,
        requests: List[BatchRequest],
        operation_id: Optional[str] = None
    ) -> Tuple[List[BatchResult], List[BatchRequest]]:
        """Coordinate a batch operation with intelligent cache management.
        
        Args:
            requests: List of batch requests to process
            operation_id: Optional operation identifier for tracking
            
        Returns:
            Tuple of (cached_results, uncached_requests)
        """
        if not requests:
            return [], []
        
        operation_id = operation_id or f"batch_{int(time.time() * 1000)}"
        start_time = time.time()
        
        try:
            # Mark operation as active
            self.active_batch_operations.add(operation_id)
            self.coordination_stats['total_batch_operations'] += 1
            
            logger.info(f"Coordinating batch operation {operation_id} with {len(requests)} requests")
            
            # Step 1: Pre-process requests for cache optimization
            optimized_requests = await self._optimize_requests_for_cache(requests)
            
            # Step 2: Perform batch cache lookup
            cached_results, uncached_requests = await self.batch_cache_manager.batch_cache_lookup(
                optimized_requests
            )
            
            # Step 3: Record access patterns for cache warming
            await self._record_access_patterns(requests)
            
            # Step 4: Trigger predictive cache warming if beneficial
            await self._trigger_predictive_warming(requests, cached_results)
            
            # Step 5: Handle cache invalidation coordination
            await self._coordinate_cache_invalidation(requests)
            
            # Update coordination statistics
            coordination_time = time.time() - start_time
            self.coordination_stats['coordination_time_saved'] += coordination_time
            
            if len(cached_results) > 0:
                self.coordination_stats['cache_optimized_operations'] += 1
            
            logger.info(
                f"Batch coordination completed for {operation_id}: "
                f"{len(cached_results)} cached, {len(uncached_requests)} uncached"
            )
            
            return cached_results, uncached_requests
            
        except Exception as e:
            logger.error(f"Error coordinating batch operation {operation_id}: {e}")
            raise BatchProcessingError(f"Cache coordination failed: {e}") from e
        
        finally:
            # Remove from active operations
            self.active_batch_operations.discard(operation_id)
    
    async def finalize_batch_operation(
        self,
        operation_id: str,
        results: List[BatchResult]
    ) -> None:
        """Finalize a batch operation by storing results and updating cache.
        
        Args:
            operation_id: Operation identifier
            results: List of batch results to finalize
        """
        try:
            logger.debug(f"Finalizing batch operation {operation_id} with {len(results)} results")
            
            # Store successful results in cache
            await self.batch_cache_manager.batch_cache_store(results)
            
            # Update cache warming patterns based on results
            await self._update_warming_patterns_from_results(results)
            
            # Process any pending cache invalidations
            await self._process_pending_invalidations()
            
            logger.debug(f"Batch operation {operation_id} finalized successfully")
            
        except Exception as e:
            logger.error(f"Error finalizing batch operation {operation_id}: {e}")
            raise CacheError(f"Failed to finalize batch operation: {e}") from e
    
    async def _optimize_requests_for_cache(
        self,
        requests: List[BatchRequest]
    ) -> List[BatchRequest]:
        """Optimize batch requests for better cache performance.
        
        Args:
            requests: Original batch requests
            
        Returns:
            Optimized batch requests
        """
        # For now, just return the original requests
        # In a more sophisticated implementation, we could:
        # - Reorder requests based on cache likelihood
        # - Group similar requests together
        # - Filter out requests that are definitely cached
        
        # Sort by priority to process high-priority items first
        optimized = sorted(requests, key=lambda r: r.priority, reverse=True)
        
        logger.debug(f"Optimized {len(requests)} requests for cache performance")
        return optimized
    
    async def _record_access_patterns(self, requests: List[BatchRequest]) -> None:
        """Record access patterns for cache warming predictions.
        
        Args:
            requests: Batch requests to record patterns for
        """
        try:
            for request in requests:
                await self.cache_warming_manager.record_file_access(
                    request.repo,
                    request.file_path
                )
            
            logger.debug(f"Recorded access patterns for {len(requests)} requests")
            
        except Exception as e:
            logger.warning(f"Error recording access patterns: {e}")
    
    async def _trigger_predictive_warming(
        self,
        requests: List[BatchRequest],
        cached_results: List[BatchResult]
    ) -> None:
        """Trigger predictive cache warming based on batch patterns.
        
        Args:
            requests: Original batch requests
            cached_results: Results that were served from cache
        """
        try:
            # Calculate cache hit rate for this batch
            cache_hit_rate = len(cached_results) / len(requests) if requests else 0.0
            
            # If cache hit rate is low, trigger warming for related files
            if cache_hit_rate < 0.5:  # Less than 50% hit rate
                # Get unique repositories by full_name
                repo_names = set(req.repo.full_name for req in requests)
                repositories = [req.repo for req in requests if req.repo.full_name in repo_names]
                # Remove duplicates while preserving order
                seen = set()
                unique_repositories = []
                for repo in repositories:
                    if repo.full_name not in seen:
                        seen.add(repo.full_name)
                        unique_repositories.append(repo)
                repositories = unique_repositories
                
                # Warm common files for these repositories
                for repo in repositories:
                    await self.cache_warming_manager.warm_repository_files(
                        repo, priority=0.6
                    )
                
                self.coordination_stats['warming_triggered_operations'] += 1
                logger.debug(f"Triggered predictive warming for {len(repositories)} repositories")
            
        except Exception as e:
            logger.warning(f"Error triggering predictive warming: {e}")
    
    async def _coordinate_cache_invalidation(self, requests: List[BatchRequest]) -> None:
        """Coordinate cache invalidation for batch requests.
        
        Args:
            requests: Batch requests that may need cache invalidation
        """
        try:
            async with self.invalidation_lock:
                current_time = datetime.now(timezone.utc)
                
                # Check for repositories that need invalidation
                repositories_to_invalidate = set()
                
                for request in requests:
                    repo_key = request.repo.full_name
                    
                    # Check if this repository has pending invalidation
                    if repo_key in self.pending_invalidations:
                        invalidation_time = self.pending_invalidations[repo_key]
                        
                        # If invalidation is older than 5 minutes, process it
                        if (current_time - invalidation_time).total_seconds() > 300:
                            repositories_to_invalidate.add(request.repo)
                            del self.pending_invalidations[repo_key]
                
                # Process invalidations
                if repositories_to_invalidate:
                    await self.batch_cache_manager.invalidate_batch_cache(
                        list(repositories_to_invalidate)
                    )
                    self.coordination_stats['invalidation_operations'] += 1
                    logger.debug(f"Processed cache invalidation for {len(repositories_to_invalidate)} repositories")
            
        except Exception as e:
            logger.warning(f"Error coordinating cache invalidation: {e}")
    
    async def _update_warming_patterns_from_results(self, results: List[BatchResult]) -> None:
        """Update cache warming patterns based on batch results.
        
        Args:
            results: Batch results to analyze for patterns
        """
        try:
            # Analyze successful results for warming patterns
            successful_results = [r for r in results if r.success and not r.from_cache]
            
            if successful_results:
                # Group by repository
                repo_files = {}
                for result in successful_results:
                    repo_name = result.request.repo.full_name
                    if repo_name not in repo_files:
                        repo_files[repo_name] = []
                    repo_files[repo_name].append(result.request.file_path)
                
                # Update warming patterns
                for repo_name, file_paths in repo_files.items():
                    logger.debug(f"Updated warming patterns for {repo_name}: {len(file_paths)} files")
            
        except Exception as e:
            logger.warning(f"Error updating warming patterns from results: {e}")
    
    async def _process_pending_invalidations(self) -> None:
        """Process any pending cache invalidations."""
        try:
            async with self.invalidation_lock:
                if not self.pending_invalidations:
                    return
                
                current_time = datetime.now(timezone.utc)
                expired_invalidations = []
                
                # Find expired invalidations (older than 10 minutes)
                for repo_key, invalidation_time in self.pending_invalidations.items():
                    if (current_time - invalidation_time).total_seconds() > 600:
                        expired_invalidations.append(repo_key)
                
                # Remove expired invalidations
                for repo_key in expired_invalidations:
                    del self.pending_invalidations[repo_key]
                
                if expired_invalidations:
                    logger.debug(f"Cleaned up {len(expired_invalidations)} expired invalidations")
            
        except Exception as e:
            logger.warning(f"Error processing pending invalidations: {e}")
    
    async def schedule_cache_invalidation(
        self,
        repository: Repository,
        delay_seconds: float = 0.0
    ) -> None:
        """Schedule cache invalidation for a repository.
        
        Args:
            repository: Repository to invalidate cache for
            delay_seconds: Delay before invalidation (0 for immediate)
        """
        try:
            if delay_seconds <= 0:
                # Immediate invalidation
                await self.batch_cache_manager.invalidate_batch_cache([repository])
                self.coordination_stats['invalidation_operations'] += 1
                logger.debug(f"Immediately invalidated cache for {repository.full_name}")
            else:
                # Schedule for later
                async with self.invalidation_lock:
                    invalidation_time = datetime.now(timezone.utc)
                    self.pending_invalidations[repository.full_name] = invalidation_time
                    logger.debug(f"Scheduled cache invalidation for {repository.full_name}")
            
        except Exception as e:
            logger.error(f"Error scheduling cache invalidation for {repository.full_name}: {e}")
            raise CacheError(f"Failed to schedule cache invalidation: {e}") from e
    
    async def warm_cache_for_batch_operation(
        self,
        repositories: List[Repository],
        predicted_files: Optional[List[str]] = None
    ) -> int:
        """Warm cache in preparation for a batch operation.
        
        Args:
            repositories: Repositories to warm cache for
            predicted_files: Optional list of files to prioritize
            
        Returns:
            Number of files queued for warming
        """
        try:
            if predicted_files:
                # Warm specific files
                total_queued = 0
                for repo in repositories:
                    queued = await self.cache_warming_manager.warm_repository_files(
                        repo, predicted_files, priority=0.7
                    )
                    total_queued += queued
            else:
                # Warm common files across organization
                total_queued = await self.cache_warming_manager.warm_organization_files(
                    repositories, common_files_only=True
                )
            
            self.coordination_stats['warming_triggered_operations'] += 1
            logger.info(f"Warmed cache for batch operation: {total_queued} files queued")
            return total_queued
            
        except Exception as e:
            logger.error(f"Error warming cache for batch operation: {e}")
            raise CacheError(f"Failed to warm cache: {e}") from e
    
    def get_coordination_statistics(self) -> Dict[str, Any]:
        """Get comprehensive coordination statistics.
        
        Returns:
            Dictionary containing coordination statistics
        """
        # Get statistics from sub-components
        batch_cache_stats = self.batch_cache_manager.get_batch_cache_statistics()
        warming_stats = self.cache_warming_manager.get_warming_statistics()
        cache_efficiency = self.batch_cache_manager.get_cache_efficiency_metrics()
        
        return {
            'coordination': {
                'total_batch_operations': self.coordination_stats['total_batch_operations'],
                'cache_optimized_operations': self.coordination_stats['cache_optimized_operations'],
                'warming_triggered_operations': self.coordination_stats['warming_triggered_operations'],
                'invalidation_operations': self.coordination_stats['invalidation_operations'],
                'coordination_time_saved': self.coordination_stats['coordination_time_saved'],
                'active_operations': len(self.active_batch_operations),
                'pending_invalidations': len(self.pending_invalidations)
            },
            'batch_cache': batch_cache_stats,
            'cache_warming': warming_stats,
            'cache_efficiency': cache_efficiency
        }
    
    def reset_coordination_statistics(self) -> None:
        """Reset coordination statistics."""
        self.coordination_stats = {
            'total_batch_operations': 0,
            'cache_optimized_operations': 0,
            'warming_triggered_operations': 0,
            'invalidation_operations': 0,
            'coordination_time_saved': 0.0
        }
        
        self.batch_cache_manager.reset_batch_cache_statistics()
        self.cache_warming_manager.reset_statistics()
    
    async def optimize_cache_for_scan_pattern(
        self,
        repositories: List[Repository],
        scan_pattern: str = "security_scan"
    ) -> Dict[str, Any]:
        """Optimize cache configuration for a specific scan pattern.
        
        Args:
            repositories: Repositories that will be scanned
            scan_pattern: Type of scan pattern (security_scan, dependency_audit, etc.)
            
        Returns:
            Dictionary containing optimization results
        """
        try:
            optimization_start = time.time()
            
            # Define file priorities based on scan pattern
            if scan_pattern == "security_scan":
                priority_files = [
                    'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                    'requirements.txt', 'Pipfile.lock', 'poetry.lock', 'pyproject.toml',
                    'Gemfile.lock', 'composer.lock', 'go.mod', 'go.sum', 'Cargo.lock'
                ]
            elif scan_pattern == "dependency_audit":
                priority_files = [
                    'package-lock.json', 'yarn.lock', 'Pipfile.lock', 'poetry.lock',
                    'Gemfile.lock', 'composer.lock', 'go.sum', 'Cargo.lock'
                ]
            else:
                priority_files = None
            
            # Pre-warm cache for priority files
            warmed_count = await self.warm_cache_for_batch_operation(
                repositories, priority_files
            )
            
            # Analyze current cache state
            cache_stats = self.batch_cache_manager.get_batch_cache_statistics()
            
            optimization_time = time.time() - optimization_start
            
            result = {
                'scan_pattern': scan_pattern,
                'repositories_analyzed': len(repositories),
                'files_queued_for_warming': warmed_count,
                'optimization_time': optimization_time,
                'cache_state': cache_stats,
                'recommendations': []
            }
            
            # Generate recommendations
            if cache_stats['batch_hit_rate_percent'] < 30:
                result['recommendations'].append(
                    "Consider running cache warming before large scans"
                )
            
            if warmed_count > 100:
                result['recommendations'].append(
                    "Large number of files queued - consider increasing warming batch size"
                )
            
            logger.info(f"Cache optimization completed for {scan_pattern}: {warmed_count} files queued")
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing cache for scan pattern {scan_pattern}: {e}")
            raise CacheError(f"Cache optimization failed: {e}") from e
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()