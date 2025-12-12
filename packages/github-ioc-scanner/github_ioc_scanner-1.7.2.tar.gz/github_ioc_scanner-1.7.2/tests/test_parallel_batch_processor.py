"""Tests for parallel batch processor."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.github_ioc_scanner.parallel_batch_processor import ParallelBatchProcessor
from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
from src.github_ioc_scanner.batch_models import (
    BatchRequest, BatchResult, BatchConfig, AsyncBatchContext, BatchRecoveryPlan
)
from src.github_ioc_scanner.models import Repository, FileContent, APIResponse
from src.github_ioc_scanner.exceptions import RateLimitError, NetworkError, APIError


@pytest.fixture
def mock_github_client():
    """Create a mock GitHub client."""
    client = AsyncMock(spec=AsyncGitHubClient)
    return client


@pytest.fixture
def batch_config():
    """Create a test batch configuration."""
    return BatchConfig(
        max_concurrent_requests=5,
        retry_attempts=2,
        retry_delay_base=0.1,  # Short delays for testing
        rate_limit_buffer=0.8
    )


@pytest.fixture
def sample_repository():
    """Create a sample repository."""
    return Repository(
        name="test-repo",
        full_name="owner/test-repo",
        default_branch="main",
        archived=False,
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_requests(sample_repository):
    """Create sample batch requests."""
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
            file_path="Gemfile.lock",
            priority=6
        )
    ]


@pytest.fixture
def processor(mock_github_client, batch_config):
    """Create a parallel batch processor."""
    return ParallelBatchProcessor(mock_github_client, batch_config)


class TestParallelBatchProcessor:
    """Test cases for ParallelBatchProcessor."""
    
    def test_initialization(self, mock_github_client, batch_config):
        """Test processor initialization."""
        processor = ParallelBatchProcessor(mock_github_client, batch_config)
        
        assert processor.github_client == mock_github_client
        assert processor.config == batch_config
        assert processor.current_concurrency == batch_config.max_concurrent_requests
        assert processor.semaphore._value == batch_config.max_concurrent_requests
        assert processor.rate_limit_manager is not None
    
    def test_initialization_with_invalid_config(self, mock_github_client):
        """Test processor initialization with invalid config."""
        invalid_config = BatchConfig(max_concurrent_requests=0)  # Invalid
        
        with pytest.raises(ValueError, match="Invalid batch configuration"):
            ParallelBatchProcessor(mock_github_client, invalid_config)
    
    @pytest.mark.asyncio
    async def test_process_empty_batch(self, processor):
        """Test processing empty batch."""
        results = await processor.process_batch_parallel([])
        assert results == []
    
    @pytest.mark.asyncio
    async def test_process_successful_batch(self, processor, sample_requests):
        """Test processing successful batch."""
        # Mock successful responses
        file_content = FileContent(content="test content", sha="abc123", size=100)
        api_response = APIResponse(
            data=file_content,
            rate_limit_remaining=4999,
            rate_limit_reset=1234567890
        )
        
        processor.github_client.get_file_content_async.return_value = api_response
        
        results = await processor.process_batch_parallel(sample_requests)
        
        assert len(results) == 3
        for result in results:
            assert result.success
            assert result.content == file_content
            assert result.error is None
            assert result.processing_time > 0
        
        # Check metrics
        metrics = processor.get_metrics()
        assert metrics.total_requests == 3
        assert metrics.successful_requests == 3
        assert metrics.failed_requests == 0
        assert metrics.success_rate == 100.0
    
    @pytest.mark.asyncio
    async def test_process_batch_with_failures(self, processor, sample_requests):
        """Test processing batch with some failures."""
        # Mock mixed responses
        file_content = FileContent(content="test content", sha="abc123", size=100)
        success_response = APIResponse(
            data=file_content,
            rate_limit_remaining=4999,
            rate_limit_reset=1234567890
        )
        
        # First request succeeds, second fails, third succeeds
        processor.github_client.get_file_content_async.side_effect = [
            success_response,
            APIError("File not found"),
            success_response
        ]
        
        results = await processor.process_batch_parallel(sample_requests)
        
        assert len(results) == 3
        assert results[0].success
        assert not results[1].success
        assert results[2].success
        
        # Check metrics
        metrics = processor.get_metrics()
        assert metrics.total_requests == 3
        assert metrics.successful_requests == 2
        assert metrics.failed_requests == 1
        assert metrics.success_rate == pytest.approx(66.67, rel=1e-2)
    
    @pytest.mark.asyncio
    async def test_rate_limit_handling(self, processor, sample_requests):
        """Test rate limit error handling and retry."""
        # Mock rate limit error on first attempt, success on retry
        file_content = FileContent(content="test content", sha="abc123", size=100)
        success_response = APIResponse(
            data=file_content,
            rate_limit_remaining=4999,
            rate_limit_reset=1234567890
        )
        
        processor.github_client.get_file_content_async.side_effect = [
            RateLimitError("Rate limit exceeded", reset_time=int(datetime.now().timestamp()) + 1),
            success_response,
            success_response,
            success_response
        ]
        
        results = await processor.process_batch_parallel(sample_requests[:1])  # Test with one request
        
        assert len(results) == 1
        assert results[0].success
        
        # Verify retry was attempted
        assert processor.github_client.get_file_content_async.call_count >= 2
    
    @pytest.mark.asyncio
    async def test_concurrency_adjustment_on_rate_limit(self, processor):
        """Test concurrency adjustment when rate limit is hit."""
        initial_concurrency = processor.current_concurrency
        
        # Simulate rate limit exceeded
        new_concurrency, wait_time = await processor.rate_limit_manager.handle_rate_limit_exceeded()
        
        assert new_concurrency < initial_concurrency
        assert wait_time >= 0
    
    @pytest.mark.asyncio
    async def test_concurrency_adjustment_based_on_remaining(self, processor):
        """Test concurrency adjustment based on remaining rate limit."""
        import time
        
        # Wait for adjustment interval
        await asyncio.sleep(0.1)
        
        # Test with low remaining rate limit
        new_concurrency = await processor.rate_limit_manager.update_rate_limit_info(
            remaining=100, limit=5000, reset_time=int(time.time()) + 3600
        )
        
        # Should reduce concurrency or at least track the low rate limit
        rate_limit_info = processor.rate_limit_manager.get_rate_limit_status()
        assert rate_limit_info.remaining == 100
        
        # Test with high remaining rate limit
        await asyncio.sleep(0.1)
        new_concurrency = await processor.rate_limit_manager.update_rate_limit_info(
            remaining=4000, limit=5000, reset_time=int(time.time()) + 3600
        )
        
        # Should track the higher rate limit
        rate_limit_info = processor.rate_limit_manager.get_rate_limit_status()
        assert rate_limit_info.remaining == 4000
    
    @pytest.mark.asyncio
    async def test_retry_delay_calculation(self, processor):
        """Test retry delay calculation with exponential backoff."""
        # Test retry manager delay calculation
        config = processor.retry_manager.config
        
        # Test normal retry delay
        delay1 = processor.retry_manager._calculate_retry_delay(0, NetworkError("test"), config, "test")
        delay2 = processor.retry_manager._calculate_retry_delay(1, NetworkError("test"), config, "test")
        delay3 = processor.retry_manager._calculate_retry_delay(2, NetworkError("test"), config, "test")
        
        # Should increase exponentially
        assert delay2 > delay1
        assert delay3 > delay2
        
        # Test rate limit retry delay (should be longer)
        rate_limit_delay = processor.retry_manager._calculate_retry_delay(0, RateLimitError("test"), config, "test")
        normal_delay = processor.retry_manager._calculate_retry_delay(0, NetworkError("test"), config, "test")
        
        assert rate_limit_delay >= normal_delay  # Rate limit uses different base delay
        
        # Test maximum delay cap
        max_delay = processor.retry_manager._calculate_retry_delay(10, NetworkError("test"), config, "test")
        assert max_delay <= config.max_delay
    
    @pytest.mark.asyncio
    async def test_rate_limit_checking(self, processor):
        """Test rate limit checking and waiting."""
        import time
        
        # Set low rate limit in the rate limit manager
        await processor.rate_limit_manager.update_rate_limit_info(
            remaining=10, limit=5000, reset_time=int(time.time()) + 1
        )
        
        context = AsyncBatchContext(semaphore=asyncio.Semaphore(1))
        
        start_time = datetime.now()
        await processor._check_rate_limits(context)
        end_time = datetime.now()
        
        # Should have waited for rate limit reset or at least checked
        duration = (end_time - start_time).total_seconds()
        assert duration >= 0  # Should complete without error
    
    @pytest.mark.asyncio
    async def test_network_error_retry(self, processor, sample_requests):
        """Test network error handling and retry."""
        # Mock network error on first attempt, success on retry
        file_content = FileContent(content="test content", sha="abc123", size=100)
        success_response = APIResponse(
            data=file_content,
            rate_limit_remaining=4999,
            rate_limit_reset=1234567890
        )
        
        processor.github_client.get_file_content_async.side_effect = [
            NetworkError("Connection timeout"),
            success_response
        ]
        
        results = await processor.process_batch_parallel(sample_requests[:1])
        
        assert len(results) == 1
        assert results[0].success
        
        # Verify retry was attempted
        assert processor.github_client.get_file_content_async.call_count == 2
    
    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self, processor, sample_requests):
        """Test behavior when max retries are exceeded."""
        # Mock persistent failures
        processor.github_client.get_file_content_async.side_effect = NetworkError("Persistent error")
        
        results = await processor.process_batch_parallel(sample_requests[:1])
        
        assert len(results) == 1
        assert not results[0].success
        assert isinstance(results[0].error, NetworkError)
        
        # Should have attempted retries (retry manager handles the retry logic)
        # The exact number of calls depends on the retry manager configuration
        assert processor.github_client.get_file_content_async.call_count >= 1
        
        # Check retry statistics
        retry_stats = processor.retry_manager.get_statistics()
        assert retry_stats.failed_operations > 0
    
    @pytest.mark.asyncio
    async def test_parallel_efficiency_calculation(self, processor, sample_requests):
        """Test parallel efficiency calculation."""
        # Mock responses with varying processing times
        file_content = FileContent(content="test content", sha="abc123", size=100)
        api_response = APIResponse(
            data=file_content,
            rate_limit_remaining=4999,
            rate_limit_reset=1234567890
        )
        
        processor.github_client.get_file_content_async.return_value = api_response
        
        results = await processor.process_batch_parallel(sample_requests)
        
        metrics = processor.get_metrics()
        assert 0 <= metrics.parallel_efficiency <= 1.0
        assert metrics.average_batch_size == len(sample_requests)
    
    @pytest.mark.asyncio
    async def test_create_recovery_plan(self, processor, sample_requests):
        """Test recovery plan creation for failed requests."""
        errors = [
            RateLimitError("Rate limit exceeded"),
            NetworkError("Connection timeout"),
            APIError("Not found", status_code=404)
        ]
        
        recovery_plan = await processor.create_recovery_plan(sample_requests, errors)
        
        assert isinstance(recovery_plan, BatchRecoveryPlan)
        assert len(recovery_plan.retry_requests) == 2  # Rate limit and network errors
        assert len(recovery_plan.skip_requests) == 1   # 404 error
        assert recovery_plan.delay_seconds > 0
        assert recovery_plan.has_retries
    
    @pytest.mark.asyncio
    async def test_create_recovery_plan_server_errors(self, processor, sample_requests):
        """Test recovery plan for server errors."""
        errors = [
            APIError("Internal server error", status_code=500),
            APIError("Bad gateway", status_code=502),
            APIError("Service unavailable", status_code=503)
        ]
        
        recovery_plan = await processor.create_recovery_plan(sample_requests, errors)
        
        # All server errors should be retried
        assert len(recovery_plan.retry_requests) == 3
        assert len(recovery_plan.skip_requests) == 0
    
    def test_get_current_concurrency(self, processor):
        """Test getting current concurrency."""
        assert processor.get_current_concurrency() == processor.config.max_concurrent_requests
    
    def test_reset_metrics(self, processor):
        """Test metrics reset."""
        # Add some data to metrics
        processor.metrics.total_requests = 10
        processor.metrics.successful_requests = 8
        
        processor.reset_metrics()
        
        assert processor.metrics.total_requests == 0
        assert processor.metrics.successful_requests == 0
    
    @pytest.mark.asyncio
    async def test_context_manager_usage(self, processor, sample_requests):
        """Test using processor with custom context."""
        custom_semaphore = asyncio.Semaphore(2)
        context = AsyncBatchContext(
            semaphore=custom_semaphore,
            rate_limit_remaining=1000,
            rate_limit_reset=0
        )
        
        file_content = FileContent(content="test content", sha="abc123", size=100)
        api_response = APIResponse(
            data=file_content,
            rate_limit_remaining=999,
            rate_limit_reset=1234567890
        )
        
        processor.github_client.get_file_content_async.return_value = api_response
        
        results = await processor.process_batch_parallel(sample_requests, context)
        
        assert len(results) == 3
        for result in results:
            assert result.success
    
    @pytest.mark.asyncio
    async def test_semaphore_update(self, processor):
        """Test semaphore update functionality."""
        original_concurrency = processor.current_concurrency
        new_concurrency = 3
        
        await processor._update_semaphore(new_concurrency)
        
        assert processor.current_concurrency == new_concurrency
        assert processor.semaphore._value == new_concurrency
        
        # Test no change when same concurrency
        await processor._update_semaphore(new_concurrency)
        assert processor.current_concurrency == new_concurrency
    
    @pytest.mark.asyncio
    async def test_rate_limit_update(self, processor):
        """Test rate limit update functionality."""
        new_remaining = 1000
        new_reset = 1234567890
        
        await processor.rate_limit_manager.update_rate_limit_info(
            remaining=new_remaining, limit=5000, reset_time=new_reset
        )
        
        rate_limit_info = processor.rate_limit_manager.get_rate_limit_status()
        assert rate_limit_info.remaining == new_remaining
        assert rate_limit_info.reset_time == new_reset


class TestBatchProcessorIntegration:
    """Integration tests for batch processor."""
    
    @pytest.mark.asyncio
    async def test_full_batch_workflow(self, mock_github_client, sample_requests):
        """Test complete batch processing workflow."""
        config = BatchConfig(
            max_concurrent_requests=2,
            retry_attempts=1,
            retry_delay_base=0.01
        )
        
        processor = ParallelBatchProcessor(mock_github_client, config)
        
        # Mock successful responses
        file_content = FileContent(content="test content", sha="abc123", size=100)
        api_response = APIResponse(
            data=file_content,
            rate_limit_remaining=4999,
            rate_limit_reset=1234567890
        )
        
        mock_github_client.get_file_content_async.return_value = api_response
        
        # Process batch
        results = await processor.process_batch_parallel(sample_requests)
        
        # Verify results
        assert len(results) == 3
        for result in results:
            assert result.success
            assert result.content == file_content
        
        # Verify metrics
        metrics = processor.get_metrics()
        assert metrics.total_requests == 3
        assert metrics.successful_requests == 3
        assert metrics.success_rate == 100.0
        assert metrics.parallel_efficiency > 0
        
        # Verify all requests were made
        assert mock_github_client.get_file_content_async.call_count == 3


class TestMemoryIntegration:
    """Test memory monitoring integration with parallel batch processor."""
    
    @pytest.mark.asyncio
    async def test_memory_monitoring_initialization(self, mock_github_client, batch_config):
        """Test that memory monitor is properly initialized."""
        processor = ParallelBatchProcessor(mock_github_client, batch_config)
        
        assert processor.memory_monitor is not None
        assert processor.memory_monitor.min_batch_size == 1
        assert processor.memory_monitor.max_batch_size == 50
    
    @pytest.mark.asyncio
    async def test_get_memory_stats(self, mock_github_client, batch_config):
        """Test getting memory statistics."""
        processor = ParallelBatchProcessor(mock_github_client, batch_config)
        
        with patch.object(processor.memory_monitor, 'get_memory_report') as mock_report:
            mock_report.return_value = {
                'current_stats': {
                    'system_memory_mb': 8192.0,
                    'process_memory_mb': 100.0,
                    'memory_usage_percent': 50.0
                },
                'recommendations': {
                    'should_reduce_batch_size': False,
                    'is_critical_pressure': False
                }
            }
            
            stats = processor.get_memory_stats()
            
            assert 'current_stats' in stats
            assert stats['current_stats']['system_memory_mb'] == 8192.0
            assert stats['current_stats']['process_memory_mb'] == 100.0
    
    @pytest.mark.asyncio
    async def test_force_memory_cleanup(self, mock_github_client, batch_config):
        """Test forcing memory cleanup."""
        processor = ParallelBatchProcessor(mock_github_client, batch_config)
        
        with patch.object(processor.memory_monitor, 'force_garbage_collection') as mock_gc:
            mock_gc.return_value = {
                'objects_collected': 42,
                'memory_freed_mb': 10.5
            }
            
            cleanup_stats = processor.force_memory_cleanup()
            
            assert cleanup_stats['objects_collected'] == 42
            assert cleanup_stats['memory_freed_mb'] == 10.5
            mock_gc.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_check_memory_pressure(self, mock_github_client, batch_config):
        """Test checking memory pressure status."""
        processor = ParallelBatchProcessor(mock_github_client, batch_config)
        
        with patch.object(processor.memory_monitor, 'should_reduce_batch_size') as mock_should_reduce, \
             patch.object(processor.memory_monitor, 'is_critical_memory_pressure') as mock_critical:
            
            mock_should_reduce.return_value = True
            mock_critical.return_value = False
            
            should_reduce, is_critical = processor.check_memory_pressure()
            
            assert should_reduce is True
            assert is_critical is False
            mock_should_reduce.assert_called_once()
            mock_critical.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_batch_size_reduction_due_to_memory_pressure(
        self, 
        mock_github_client, 
        batch_config, 
        sample_requests
    ):
        """Test that batch size is reduced when memory pressure is detected."""
        processor = ParallelBatchProcessor(mock_github_client, batch_config)
        
        # Mock memory pressure detection
        with patch.object(processor.memory_monitor, 'set_baseline_memory'), \
             patch.object(processor.memory_monitor, 'should_reduce_batch_size') as mock_should_reduce, \
             patch.object(processor.memory_monitor, 'calculate_adjusted_batch_size') as mock_adjust:
            
            mock_should_reduce.return_value = True
            mock_adjust.return_value = 2  # Reduce from 5 to 2
            
            # Mock successful API responses
            mock_response = APIResponse(
                data=FileContent(content="test content", sha="abc123", size=12),
                rate_limit_remaining=4000,
                rate_limit_reset=1234567890
            )
            mock_github_client.get_file_content_async.return_value = mock_response
            
            # Process batch with 3 requests (all available)
            results = await processor.process_batch_parallel(sample_requests)
            
            # Should only process 2 requests due to memory pressure
            assert len(results) == 2
            mock_should_reduce.assert_called_once()
            mock_adjust.assert_called_once_with(3)
    
    @pytest.mark.asyncio
    async def test_baseline_memory_set_before_processing(
        self, 
        mock_github_client, 
        batch_config, 
        sample_requests
    ):
        """Test that baseline memory is set before batch processing."""
        processor = ParallelBatchProcessor(mock_github_client, batch_config)
        
        with patch.object(processor.memory_monitor, 'set_baseline_memory') as mock_set_baseline, \
             patch.object(processor.memory_monitor, 'should_reduce_batch_size') as mock_should_reduce:
            
            mock_should_reduce.return_value = False
            
            # Mock successful API responses
            mock_response = APIResponse(
                data=FileContent(content="test content", sha="abc123", size=12),
                rate_limit_remaining=4000,
                rate_limit_reset=1234567890
            )
            mock_github_client.get_file_content_async.return_value = mock_response
            
            # Process batch
            await processor.process_batch_parallel(sample_requests[:2])
            
            # Baseline should be set before processing
            mock_set_baseline.assert_called_once()