"""Tests for batch cache coordinator functionality."""

import asyncio
import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock, patch

from src.github_ioc_scanner.batch_cache_coordinator import BatchCacheCoordinator
from src.github_ioc_scanner.batch_models import BatchRequest, BatchResult, BatchConfig
from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
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
def mock_github_client():
    """Create a mock async GitHub client."""
    client = Mock(spec=AsyncGitHubClient)
    
    # Mock successful response
    mock_response = Mock()
    mock_response.data = FileContent(
        content='{"name": "test", "version": "1.0.0"}',
        sha="abc123",
        size=42
    )
    
    client.get_file_content_async = AsyncMock(return_value=mock_response)
    return client


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
def batch_config():
    """Create a batch configuration for testing."""
    return BatchConfig(
        max_concurrent_requests=5,
        max_batch_size=10,
        default_batch_size=5
    )


@pytest.fixture
def batch_cache_coordinator(mock_cache_manager, mock_github_client, batch_config):
    """Create a batch cache coordinator with mock dependencies."""
    return BatchCacheCoordinator(
        cache_manager=mock_cache_manager,
        github_client=mock_github_client,
        batch_config=batch_config
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


class TestBatchCacheCoordinator:
    """Test cases for BatchCacheCoordinator."""
    
    def test_initialization(self, mock_cache_manager, mock_github_client, batch_config):
        """Test batch cache coordinator initialization."""
        coordinator = BatchCacheCoordinator(
            cache_manager=mock_cache_manager,
            github_client=mock_github_client,
            batch_config=batch_config
        )
        
        assert coordinator.cache_manager == mock_cache_manager
        assert coordinator.github_client == mock_github_client
        assert coordinator.batch_config == batch_config
        assert len(coordinator.active_batch_operations) == 0
        assert len(coordinator.pending_invalidations) == 0
    
    def test_initialization_with_defaults(self, mock_cache_manager):
        """Test initialization with default configuration."""
        coordinator = BatchCacheCoordinator(cache_manager=mock_cache_manager)
        
        assert coordinator.cache_manager == mock_cache_manager
        assert coordinator.github_client is None
        assert coordinator.batch_config is not None
        assert isinstance(coordinator.batch_config, BatchConfig)
    
    @pytest.mark.asyncio
    async def test_start_stop_lifecycle(self, batch_cache_coordinator):
        """Test start and stop lifecycle."""
        # Start coordinator
        await batch_cache_coordinator.start()
        
        # Check that sub-components are started
        # Note: We can't easily test the internal state of sub-components
        # but we can verify the methods were called without errors
        
        # Stop coordinator
        await batch_cache_coordinator.stop()
        
        # Should complete without errors
        assert True
    
    @pytest.mark.asyncio
    async def test_coordinate_batch_operation_empty_requests(self, batch_cache_coordinator):
        """Test coordinating batch operation with empty requests."""
        cached_results, uncached_requests = await batch_cache_coordinator.coordinate_batch_operation([])
        
        assert cached_results == []
        assert uncached_requests == []
    
    @pytest.mark.asyncio
    async def test_coordinate_batch_operation_with_requests(
        self, 
        batch_cache_coordinator, 
        sample_batch_requests
    ):
        """Test coordinating batch operation with requests."""
        # Mock the batch cache manager to return some cached results
        with patch.object(
            batch_cache_coordinator.batch_cache_manager, 
            'batch_cache_lookup',
            return_value=([], sample_batch_requests)  # All cache misses
        ) as mock_lookup:
            
            cached_results, uncached_requests = await batch_cache_coordinator.coordinate_batch_operation(
                sample_batch_requests, operation_id="test_op"
            )
            
            # Should have called batch cache lookup
            mock_lookup.assert_called_once()
            
            # Should return the mocked results
            assert len(cached_results) == 0
            assert len(uncached_requests) == 3
            
            # Should update statistics
            stats = batch_cache_coordinator.get_coordination_statistics()
            assert stats['coordination']['total_batch_operations'] == 1
    
    @pytest.mark.asyncio
    async def test_coordinate_batch_operation_with_cache_hits(
        self, 
        batch_cache_coordinator, 
        sample_batch_requests
    ):
        """Test coordinating batch operation with cache hits."""
        # Create mock cached results
        cached_result = BatchResult(
            request=sample_batch_requests[0],
            content=FileContent(content="cached content", sha="abc123", size=14),
            from_cache=True,
            processing_time=0.001
        )
        
        with patch.object(
            batch_cache_coordinator.batch_cache_manager, 
            'batch_cache_lookup',
            return_value=([cached_result], sample_batch_requests[1:])  # One cache hit
        ):
            
            cached_results, uncached_requests = await batch_cache_coordinator.coordinate_batch_operation(
                sample_batch_requests
            )
            
            assert len(cached_results) == 1
            assert len(uncached_requests) == 2
            assert cached_results[0].from_cache is True
            
            # Should mark as cache optimized operation
            stats = batch_cache_coordinator.get_coordination_statistics()
            assert stats['coordination']['cache_optimized_operations'] == 1
    
    @pytest.mark.asyncio
    async def test_finalize_batch_operation(
        self, 
        batch_cache_coordinator, 
        sample_batch_requests
    ):
        """Test finalizing batch operation."""
        # Create mock results
        results = [
            BatchResult(
                request=sample_batch_requests[0],
                content=FileContent(content="content", sha="abc123", size=7),
                from_cache=False,
                processing_time=0.5
            )
        ]
        
        with patch.object(
            batch_cache_coordinator.batch_cache_manager, 
            'batch_cache_store'
        ) as mock_store:
            
            await batch_cache_coordinator.finalize_batch_operation("test_op", results)
            
            # Should have called batch cache store
            mock_store.assert_called_once_with(results)
    
    @pytest.mark.asyncio
    async def test_schedule_cache_invalidation_immediate(
        self, 
        batch_cache_coordinator, 
        sample_repository
    ):
        """Test immediate cache invalidation."""
        with patch.object(
            batch_cache_coordinator.batch_cache_manager, 
            'invalidate_batch_cache'
        ) as mock_invalidate:
            
            await batch_cache_coordinator.schedule_cache_invalidation(
                sample_repository, delay_seconds=0.0
            )
            
            # Should have called immediate invalidation
            mock_invalidate.assert_called_once_with([sample_repository])
            
            # Should update statistics
            stats = batch_cache_coordinator.get_coordination_statistics()
            assert stats['coordination']['invalidation_operations'] == 1
    
    @pytest.mark.asyncio
    async def test_schedule_cache_invalidation_delayed(
        self, 
        batch_cache_coordinator, 
        sample_repository
    ):
        """Test delayed cache invalidation."""
        await batch_cache_coordinator.schedule_cache_invalidation(
            sample_repository, delay_seconds=300.0
        )
        
        # Should be added to pending invalidations
        assert sample_repository.full_name in batch_cache_coordinator.pending_invalidations
        
        # Should not have immediate invalidation
        stats = batch_cache_coordinator.get_coordination_statistics()
        assert stats['coordination']['pending_invalidations'] == 1
    
    @pytest.mark.asyncio
    async def test_warm_cache_for_batch_operation_specific_files(
        self, 
        batch_cache_coordinator, 
        sample_repository
    ):
        """Test warming cache for batch operation with specific files."""
        repositories = [sample_repository]
        predicted_files = ["package.json", "requirements.txt"]
        
        with patch.object(
            batch_cache_coordinator.cache_warming_manager, 
            'warm_repository_files',
            return_value=2
        ) as mock_warm:
            
            queued_count = await batch_cache_coordinator.warm_cache_for_batch_operation(
                repositories, predicted_files
            )
            
            assert queued_count == 2
            mock_warm.assert_called_once_with(
                sample_repository, predicted_files, priority=0.7
            )
            
            # Should update statistics
            stats = batch_cache_coordinator.get_coordination_statistics()
            assert stats['coordination']['warming_triggered_operations'] == 1
    
    @pytest.mark.asyncio
    async def test_warm_cache_for_batch_operation_common_files(
        self, 
        batch_cache_coordinator, 
        sample_repository
    ):
        """Test warming cache for batch operation with common files."""
        repositories = [sample_repository]
        
        with patch.object(
            batch_cache_coordinator.cache_warming_manager, 
            'warm_organization_files',
            return_value=5
        ) as mock_warm:
            
            queued_count = await batch_cache_coordinator.warm_cache_for_batch_operation(
                repositories
            )
            
            assert queued_count == 5
            mock_warm.assert_called_once_with(repositories, common_files_only=True)
    
    @pytest.mark.asyncio
    async def test_optimize_cache_for_scan_pattern_security(
        self, 
        batch_cache_coordinator, 
        sample_repository
    ):
        """Test cache optimization for security scan pattern."""
        repositories = [sample_repository]
        
        with patch.object(
            batch_cache_coordinator, 
            'warm_cache_for_batch_operation',
            return_value=10
        ) as mock_warm:
            
            result = await batch_cache_coordinator.optimize_cache_for_scan_pattern(
                repositories, "security_scan"
            )
            
            assert result['scan_pattern'] == "security_scan"
            assert result['repositories_analyzed'] == 1
            assert result['files_queued_for_warming'] == 10
            assert 'optimization_time' in result
            assert 'cache_state' in result
            assert 'recommendations' in result
            
            # Should have called warming with security-specific files
            mock_warm.assert_called_once()
            args, kwargs = mock_warm.call_args
            assert len(args[1]) > 0  # Should have priority files
    
    @pytest.mark.asyncio
    async def test_optimize_cache_for_scan_pattern_dependency_audit(
        self, 
        batch_cache_coordinator, 
        sample_repository
    ):
        """Test cache optimization for dependency audit pattern."""
        repositories = [sample_repository]
        
        with patch.object(
            batch_cache_coordinator, 
            'warm_cache_for_batch_operation',
            return_value=8
        ) as mock_warm:
            
            result = await batch_cache_coordinator.optimize_cache_for_scan_pattern(
                repositories, "dependency_audit"
            )
            
            assert result['scan_pattern'] == "dependency_audit"
            assert result['files_queued_for_warming'] == 8
            
            # Should have called warming with dependency-specific files
            mock_warm.assert_called_once()
            args, kwargs = mock_warm.call_args
            priority_files = args[1]
            
            # Should include lock files but not manifest files
            assert 'package-lock.json' in priority_files
            assert 'yarn.lock' in priority_files
            assert 'package.json' not in priority_files  # Manifest, not lock file
    
    def test_get_coordination_statistics(self, batch_cache_coordinator):
        """Test getting coordination statistics."""
        # Set some coordination statistics
        batch_cache_coordinator.coordination_stats.update({
            'total_batch_operations': 5,
            'cache_optimized_operations': 3,
            'warming_triggered_operations': 2,
            'invalidation_operations': 1,
            'coordination_time_saved': 1.5
        })
        
        # Add some active operations and pending invalidations
        batch_cache_coordinator.active_batch_operations.add("op1")
        batch_cache_coordinator.pending_invalidations["repo1"] = datetime.now(timezone.utc)
        
        stats = batch_cache_coordinator.get_coordination_statistics()
        
        # Check coordination stats
        coord_stats = stats['coordination']
        assert coord_stats['total_batch_operations'] == 5
        assert coord_stats['cache_optimized_operations'] == 3
        assert coord_stats['warming_triggered_operations'] == 2
        assert coord_stats['invalidation_operations'] == 1
        assert coord_stats['coordination_time_saved'] == 1.5
        assert coord_stats['active_operations'] == 1
        assert coord_stats['pending_invalidations'] == 1
        
        # Should include sub-component stats
        assert 'batch_cache' in stats
        assert 'cache_warming' in stats
        assert 'cache_efficiency' in stats
    
    def test_reset_coordination_statistics(self, batch_cache_coordinator):
        """Test resetting coordination statistics."""
        # Set some statistics
        batch_cache_coordinator.coordination_stats['total_batch_operations'] = 10
        
        batch_cache_coordinator.reset_coordination_statistics()
        
        assert batch_cache_coordinator.coordination_stats['total_batch_operations'] == 0
    
    @pytest.mark.asyncio
    async def test_optimize_requests_for_cache(self, batch_cache_coordinator, sample_batch_requests):
        """Test request optimization for cache performance."""
        # The current implementation just sorts by priority
        optimized = await batch_cache_coordinator._optimize_requests_for_cache(sample_batch_requests)
        
        # Should be sorted by priority (descending)
        assert len(optimized) == 3
        assert optimized[0].priority >= optimized[1].priority >= optimized[2].priority
        assert optimized[0].file_path == "package.json"  # Highest priority
        assert optimized[-1].file_path == "README.md"    # Lowest priority
    
    @pytest.mark.asyncio
    async def test_record_access_patterns(self, batch_cache_coordinator, sample_batch_requests):
        """Test recording access patterns."""
        with patch.object(
            batch_cache_coordinator.cache_warming_manager, 
            'record_file_access'
        ) as mock_record:
            
            await batch_cache_coordinator._record_access_patterns(sample_batch_requests)
            
            # Should have recorded access for each request
            assert mock_record.call_count == 3
    
    @pytest.mark.asyncio
    async def test_trigger_predictive_warming_low_hit_rate(
        self, 
        batch_cache_coordinator, 
        sample_batch_requests
    ):
        """Test triggering predictive warming with low cache hit rate."""
        # No cached results = 0% hit rate
        cached_results = []
        
        with patch.object(
            batch_cache_coordinator.cache_warming_manager, 
            'warm_repository_files'
        ) as mock_warm:
            
            await batch_cache_coordinator._trigger_predictive_warming(
                sample_batch_requests, cached_results
            )
            
            # Should have triggered warming due to low hit rate
            mock_warm.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_trigger_predictive_warming_high_hit_rate(
        self, 
        batch_cache_coordinator, 
        sample_batch_requests
    ):
        """Test not triggering predictive warming with high cache hit rate."""
        # All requests cached = 100% hit rate
        cached_results = [
            BatchResult(request=req, from_cache=True, processing_time=0.001)
            for req in sample_batch_requests
        ]
        
        with patch.object(
            batch_cache_coordinator.cache_warming_manager, 
            'warm_repository_files'
        ) as mock_warm:
            
            await batch_cache_coordinator._trigger_predictive_warming(
                sample_batch_requests, cached_results
            )
            
            # Should not have triggered warming due to high hit rate
            mock_warm.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_async_context_manager(self, batch_cache_coordinator):
        """Test async context manager functionality."""
        async with batch_cache_coordinator as coordinator:
            assert coordinator == batch_cache_coordinator
            # Should have started services
        
        # Should have stopped services after exiting context
        # We can't easily verify internal state, but it should complete without errors
        assert True


class TestBatchCacheCoordinatorIntegration:
    """Integration tests for batch cache coordinator."""
    
    @pytest.mark.asyncio
    async def test_full_coordination_workflow(
        self, 
        batch_cache_coordinator, 
        sample_batch_requests
    ):
        """Test complete coordination workflow."""
        operation_id = "integration_test"
        
        # Mock batch cache manager
        with patch.object(
            batch_cache_coordinator.batch_cache_manager, 
            'batch_cache_lookup',
            return_value=([], sample_batch_requests)  # All misses
        ), patch.object(
            batch_cache_coordinator.batch_cache_manager, 
            'batch_cache_store'
        ) as mock_store:
            
            # Coordinate batch operation
            cached_results, uncached_requests = await batch_cache_coordinator.coordinate_batch_operation(
                sample_batch_requests, operation_id
            )
            
            # Simulate processing results
            processed_results = [
                BatchResult(
                    request=req,
                    content=FileContent(content=f"content for {req.file_path}", sha="abc123", size=20),
                    from_cache=False,
                    processing_time=0.5
                )
                for req in uncached_requests
            ]
            
            # Finalize operation
            await batch_cache_coordinator.finalize_batch_operation(operation_id, processed_results)
            
            # Should have stored results
            mock_store.assert_called_once_with(processed_results)
            
            # Check final statistics
            stats = batch_cache_coordinator.get_coordination_statistics()
            assert stats['coordination']['total_batch_operations'] == 1
    
    @pytest.mark.asyncio
    async def test_coordination_with_cache_warming(
        self, 
        batch_cache_coordinator, 
        sample_repository
    ):
        """Test coordination with cache warming integration."""
        repositories = [sample_repository]
        
        async with batch_cache_coordinator:
            # Optimize cache for scan
            result = await batch_cache_coordinator.optimize_cache_for_scan_pattern(
                repositories, "security_scan"
            )
            
            assert result['repositories_analyzed'] == 1
            assert 'files_queued_for_warming' in result
            
            # Should have updated statistics
            stats = batch_cache_coordinator.get_coordination_statistics()
            assert stats['coordination']['warming_triggered_operations'] >= 1
    
    @pytest.mark.asyncio
    async def test_coordination_with_invalidation(
        self, 
        batch_cache_coordinator, 
        sample_repository
    ):
        """Test coordination with cache invalidation."""
        # Schedule invalidation
        await batch_cache_coordinator.schedule_cache_invalidation(sample_repository)
        
        # Check statistics
        stats = batch_cache_coordinator.get_coordination_statistics()
        assert stats['coordination']['invalidation_operations'] == 1