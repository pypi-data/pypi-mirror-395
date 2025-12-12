"""Tests for batch cache manager functionality."""

import asyncio
import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch

from src.github_ioc_scanner.batch_cache_manager import BatchCacheManager
from src.github_ioc_scanner.batch_models import BatchRequest, BatchResult
from src.github_ioc_scanner.cache import CacheManager
from src.github_ioc_scanner.models import Repository, FileContent


@pytest.fixture
def mock_cache_manager():
    """Create a mock cache manager."""
    cache_manager = Mock(spec=CacheManager)
    cache_manager.get_file_content = Mock(return_value=None)
    cache_manager.store_file_content = Mock()
    cache_manager.refresh_repository_files = Mock(return_value=5)
    return cache_manager


@pytest.fixture
def batch_cache_manager(mock_cache_manager):
    """Create a batch cache manager with mock dependencies."""
    return BatchCacheManager(mock_cache_manager)


@pytest.fixture
def sample_repository():
    """Create a sample repository for testing."""
    return Repository(
        name="test-repo",
        full_name="test-org/test-repo",
        archived=False,
        default_branch="main",
        updated_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def sample_batch_requests(sample_repository):
    """Create sample batch requests for testing."""
    return [
        BatchRequest(
            repo=sample_repository,
            file_path="package.json",
            priority=10
        ),
        BatchRequest(
            repo=sample_repository,
            file_path="requirements.txt",
            priority=8
        ),
        BatchRequest(
            repo=sample_repository,
            file_path="README.md",
            priority=1
        )
    ]


@pytest.fixture
def sample_file_content():
    """Create sample file content for testing."""
    return FileContent(
        content='{"name": "test-package", "version": "1.0.0"}',
        sha="abc123",
        size=42
    )


class TestBatchCacheManager:
    """Test cases for BatchCacheManager."""
    
    @pytest.mark.asyncio
    async def test_initialization(self, mock_cache_manager):
        """Test batch cache manager initialization."""
        manager = BatchCacheManager(mock_cache_manager)
        
        assert manager.cache_manager == mock_cache_manager
        assert manager._batch_cache_stats['batch_hits'] == 0
        assert manager._batch_cache_stats['batch_misses'] == 0
        assert len(manager._access_patterns) == 0
    
    @pytest.mark.asyncio
    async def test_batch_cache_lookup_empty_requests(self, batch_cache_manager):
        """Test batch cache lookup with empty requests."""
        cached_results, uncached_requests = await batch_cache_manager.batch_cache_lookup([])
        
        assert cached_results == []
        assert uncached_requests == []
    
    @pytest.mark.asyncio
    async def test_batch_cache_lookup_all_misses(self, batch_cache_manager, sample_batch_requests):
        """Test batch cache lookup with all cache misses."""
        # Mock cache manager to return None (cache miss)
        batch_cache_manager.cache_manager.get_file_content.return_value = None
        
        cached_results, uncached_requests = await batch_cache_manager.batch_cache_lookup(
            sample_batch_requests
        )
        
        assert len(cached_results) == 0
        assert len(uncached_requests) == 3
        assert uncached_requests == sample_batch_requests
        
        # Check statistics
        stats = batch_cache_manager.get_batch_cache_statistics()
        assert stats['batch_cache_misses'] == 3
        assert stats['batch_cache_hits'] == 0
        assert stats['batch_hit_rate_percent'] == 0.0
    
    @pytest.mark.asyncio
    async def test_batch_cache_lookup_all_hits(self, batch_cache_manager, sample_batch_requests):
        """Test batch cache lookup with all cache hits."""
        # Mock cache manager to return content (cache hit)
        mock_content = '{"name": "test", "version": "1.0.0"}'
        batch_cache_manager.cache_manager.get_file_content.return_value = mock_content
        
        cached_results, uncached_requests = await batch_cache_manager.batch_cache_lookup(
            sample_batch_requests
        )
        
        assert len(cached_results) == 3
        assert len(uncached_requests) == 0
        
        # Check that all results are from cache
        for result in cached_results:
            assert result.from_cache is True
            assert result.content is not None
            assert result.content.content == mock_content
            assert result.processing_time == 0.001
        
        # Check statistics
        stats = batch_cache_manager.get_batch_cache_statistics()
        assert stats['batch_cache_hits'] == 3
        assert stats['batch_cache_misses'] == 0
        assert stats['batch_hit_rate_percent'] == 100.0
    
    @pytest.mark.asyncio
    async def test_batch_cache_lookup_partial_hits(self, batch_cache_manager, sample_batch_requests):
        """Test batch cache lookup with partial cache hits."""
        # Mock cache manager to return content for some files
        def mock_get_file_content(repo, path, sha):
            if path == "package.json":
                return '{"name": "test", "version": "1.0.0"}'
            return None
        
        batch_cache_manager.cache_manager.get_file_content.side_effect = mock_get_file_content
        
        cached_results, uncached_requests = await batch_cache_manager.batch_cache_lookup(
            sample_batch_requests
        )
        
        assert len(cached_results) == 1
        assert len(uncached_requests) == 2
        assert cached_results[0].request.file_path == "package.json"
        
        # Check statistics
        stats = batch_cache_manager.get_batch_cache_statistics()
        assert stats['batch_cache_hits'] == 1
        assert stats['batch_cache_misses'] == 2
        assert stats['partial_batch_hits'] == 1
        assert abs(stats['batch_hit_rate_percent'] - 33.3) < 0.1
    
    @pytest.mark.asyncio
    async def test_batch_cache_store_empty_results(self, batch_cache_manager):
        """Test batch cache store with empty results."""
        await batch_cache_manager.batch_cache_store([])
        
        # Should not call store_file_content
        batch_cache_manager.cache_manager.store_file_content.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_batch_cache_store_successful_results(
        self, 
        batch_cache_manager, 
        sample_batch_requests, 
        sample_file_content
    ):
        """Test batch cache store with successful results."""
        # Create successful batch results
        results = [
            BatchResult(
                request=sample_batch_requests[0],
                content=sample_file_content,
                from_cache=False,
                processing_time=0.5
            ),
            BatchResult(
                request=sample_batch_requests[1],
                content=FileContent(
                    content="requests==2.28.0",
                    sha="def456",
                    size=16
                ),
                from_cache=False,
                processing_time=0.3
            )
        ]
        
        await batch_cache_manager.batch_cache_store(results)
        
        # Check that store_file_content was called for each successful result
        assert batch_cache_manager.cache_manager.store_file_content.call_count == 2
    
    @pytest.mark.asyncio
    async def test_batch_cache_store_skip_cached_results(
        self, 
        batch_cache_manager, 
        sample_batch_requests, 
        sample_file_content
    ):
        """Test that batch cache store skips results that came from cache."""
        # Create result that came from cache
        cached_result = BatchResult(
            request=sample_batch_requests[0],
            content=sample_file_content,
            from_cache=True,  # This should be skipped
            processing_time=0.001
        )
        
        await batch_cache_manager.batch_cache_store([cached_result])
        
        # Should not store results that came from cache
        batch_cache_manager.cache_manager.store_file_content.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_batch_cache_store_skip_failed_results(
        self, 
        batch_cache_manager, 
        sample_batch_requests
    ):
        """Test that batch cache store skips failed results."""
        # Create failed result
        failed_result = BatchResult(
            request=sample_batch_requests[0],
            error=Exception("API error"),
            processing_time=0.5
        )
        
        await batch_cache_manager.batch_cache_store([failed_result])
        
        # Should not store failed results
        batch_cache_manager.cache_manager.store_file_content.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_cache_warming_lifecycle(self, batch_cache_manager):
        """Test cache warming start and stop lifecycle."""
        # Start cache warming
        await batch_cache_manager.start_cache_warming()
        assert batch_cache_manager._warming_task is not None
        assert not batch_cache_manager._warming_task.done()
        
        # Stop cache warming
        await batch_cache_manager.stop_cache_warming()
        assert batch_cache_manager._warming_task.done()
    
    @pytest.mark.asyncio
    async def test_warm_cache_for_repositories(self, batch_cache_manager, sample_repository):
        """Test warming cache for repositories."""
        repositories = [sample_repository]
        common_files = ["package.json", "requirements.txt"]
        
        # Start cache warming to initialize the queue
        await batch_cache_manager.start_cache_warming()
        
        try:
            queued_count = await batch_cache_manager.warm_cache_for_repositories(
                repositories, common_files
            )
            
            assert queued_count == 2  # 1 repo * 2 files
            assert batch_cache_manager._warming_queue.qsize() == 2
            
        finally:
            await batch_cache_manager.stop_cache_warming()
    
    @pytest.mark.asyncio
    async def test_warm_cache_for_repositories_default_files(
        self, 
        batch_cache_manager, 
        sample_repository
    ):
        """Test warming cache with default common files."""
        repositories = [sample_repository]
        
        await batch_cache_manager.start_cache_warming()
        
        try:
            queued_count = await batch_cache_manager.warm_cache_for_repositories(repositories)
            
            # Should queue default common files
            assert queued_count > 0
            assert batch_cache_manager._warming_queue.qsize() > 0
            
        finally:
            await batch_cache_manager.stop_cache_warming()
    
    @pytest.mark.asyncio
    async def test_invalidate_batch_cache(self, batch_cache_manager, sample_repository):
        """Test batch cache invalidation."""
        repositories = [sample_repository]
        
        # Mock refresh_repository_files to return count
        batch_cache_manager.cache_manager.refresh_repository_files.return_value = 5
        
        invalidated_count = await batch_cache_manager.invalidate_batch_cache(repositories)
        
        assert invalidated_count == 5
        batch_cache_manager.cache_manager.refresh_repository_files.assert_called_once_with(
            sample_repository.full_name
        )
    
    def test_get_batch_cache_statistics(self, batch_cache_manager):
        """Test getting batch cache statistics."""
        # Manually set some statistics
        batch_cache_manager._batch_cache_stats['batch_hits'] = 10
        batch_cache_manager._batch_cache_stats['batch_misses'] = 5
        batch_cache_manager._batch_cache_stats['batch_cache_operations'] = 3
        batch_cache_manager._batch_cache_stats['partial_hits'] = 1
        
        stats = batch_cache_manager.get_batch_cache_statistics()
        
        assert stats['batch_cache_hits'] == 10
        assert stats['batch_cache_misses'] == 5
        assert stats['total_batch_requests'] == 15
        assert abs(stats['batch_hit_rate_percent'] - 66.7) < 0.1
        assert stats['partial_batch_hits'] == 1
        assert stats['batch_cache_operations'] == 3
    
    def test_reset_batch_cache_statistics(self, batch_cache_manager):
        """Test resetting batch cache statistics."""
        # Set some statistics
        batch_cache_manager._batch_cache_stats['batch_hits'] = 10
        batch_cache_manager._access_patterns['test'] = {'count': 5}
        
        batch_cache_manager.reset_batch_cache_statistics()
        
        assert batch_cache_manager._batch_cache_stats['batch_hits'] == 0
        assert len(batch_cache_manager._access_patterns) == 0
    
    def test_get_cache_efficiency_metrics(self, batch_cache_manager):
        """Test getting cache efficiency metrics."""
        # Set up statistics for metrics calculation
        batch_cache_manager._batch_cache_stats.update({
            'batch_hits': 8,
            'batch_misses': 2,
            'batch_cache_operations': 5,
            'partial_hits': 1,
            'cache_warming_operations': 4
        })
        
        metrics = batch_cache_manager.get_cache_efficiency_metrics()
        
        assert metrics['hit_rate'] == 0.8  # 8/10
        assert abs(metrics['miss_rate'] - 0.2) < 0.001  # 2/10
        assert metrics['partial_hit_rate'] == 0.2  # 1/5
        assert metrics['warming_efficiency'] == 1.0  # min(1.0, 8/4)
    
    def test_get_cache_efficiency_metrics_no_data(self, batch_cache_manager):
        """Test getting cache efficiency metrics with no data."""
        metrics = batch_cache_manager.get_cache_efficiency_metrics()
        
        assert metrics['hit_rate'] == 0.0
        assert metrics['miss_rate'] == 0.0
        assert metrics['partial_hit_rate'] == 0.0
        assert metrics['warming_efficiency'] == 0.0
    
    @pytest.mark.asyncio
    async def test_async_context_manager(self, batch_cache_manager):
        """Test async context manager functionality."""
        async with batch_cache_manager as manager:
            assert manager == batch_cache_manager
            assert batch_cache_manager._warming_task is not None
            assert not batch_cache_manager._warming_task.done()
        
        # After exiting context, warming should be stopped
        assert batch_cache_manager._warming_task.done()
    
    @pytest.mark.asyncio
    async def test_cache_lookup_with_exception(self, batch_cache_manager, sample_batch_requests):
        """Test batch cache lookup handles exceptions gracefully."""
        # Mock cache manager to raise exception
        batch_cache_manager.cache_manager.get_file_content.side_effect = Exception("Cache error")
        
        cached_results, uncached_requests = await batch_cache_manager.batch_cache_lookup(
            sample_batch_requests
        )
        
        # Should treat exceptions as cache misses
        assert len(cached_results) == 0
        assert len(uncached_requests) == 3
        
        stats = batch_cache_manager.get_batch_cache_statistics()
        assert stats['batch_cache_misses'] == 3
        assert stats['batch_cache_hits'] == 0
    
    @pytest.mark.asyncio
    async def test_store_with_exception(self, batch_cache_manager, sample_batch_requests, sample_file_content):
        """Test batch cache store handles exceptions gracefully."""
        # Mock store_file_content to raise exception
        batch_cache_manager.cache_manager.store_file_content.side_effect = Exception("Store error")
        
        result = BatchResult(
            request=sample_batch_requests[0],
            content=sample_file_content,
            from_cache=False,
            processing_time=0.5
        )
        
        # Should not raise exception
        await batch_cache_manager.batch_cache_store([result])
        
        # Should have attempted to store
        batch_cache_manager.cache_manager.store_file_content.assert_called_once()


class TestBatchCacheIntegration:
    """Integration tests for batch cache functionality."""
    
    @pytest.mark.asyncio
    async def test_full_batch_cache_workflow(self, batch_cache_manager, sample_batch_requests):
        """Test complete batch cache workflow."""
        # Start with cache misses
        batch_cache_manager.cache_manager.get_file_content.return_value = None
        
        # First lookup - should be all misses
        cached_results, uncached_requests = await batch_cache_manager.batch_cache_lookup(
            sample_batch_requests
        )
        
        assert len(cached_results) == 0
        assert len(uncached_requests) == 3
        
        # Simulate processing and storing results
        processed_results = []
        for request in uncached_requests:
            result = BatchResult(
                request=request,
                content=FileContent(
                    content=f"content for {request.file_path}",
                    sha="abc123",
                    size=20
                ),
                from_cache=False,
                processing_time=0.5
            )
            processed_results.append(result)
        
        # Store results in cache
        await batch_cache_manager.batch_cache_store(processed_results)
        
        # Verify store was called
        assert batch_cache_manager.cache_manager.store_file_content.call_count == 3
        
        # Check final statistics
        stats = batch_cache_manager.get_batch_cache_statistics()
        assert stats['batch_cache_operations'] == 1
        assert stats['batch_cache_misses'] == 3
        assert stats['batch_cache_hits'] == 0
    
    @pytest.mark.asyncio
    async def test_cache_warming_integration(self, batch_cache_manager, sample_repository):
        """Test cache warming integration."""
        repositories = [sample_repository]
        
        async with batch_cache_manager:
            # Queue files for warming
            queued_count = await batch_cache_manager.warm_cache_for_repositories(repositories)
            assert queued_count > 0
            
            # Allow some time for warming worker to process
            await asyncio.sleep(0.1)
            
            # Check statistics
            stats = batch_cache_manager.get_batch_cache_statistics()
            assert stats['warming_task_active'] is True