"""Tests for streaming batch processor."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.github_ioc_scanner.streaming_batch_processor import (
    StreamingBatchProcessor, StreamingConfig
)
from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
from src.github_ioc_scanner.batch_models import BatchRequest, BatchConfig
from src.github_ioc_scanner.models import Repository, FileContent, APIResponse


@pytest.fixture
def mock_github_client():
    """Create a mock GitHub client."""
    client = AsyncMock(spec=AsyncGitHubClient)
    return client


@pytest.fixture
def streaming_config():
    """Create a test streaming configuration."""
    return StreamingConfig(
        chunk_size=5,
        max_memory_per_chunk_mb=50.0,
        enable_memory_monitoring=True,
        stream_threshold=10,
        max_concurrent_chunks=2
    )


@pytest.fixture
def batch_config():
    """Create a test batch configuration."""
    return BatchConfig(
        max_concurrent_requests=5,
        retry_attempts=2
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
            file_path=f"file_{i}.txt",
            priority=1,
            estimated_size=1024 * i  # Varying sizes
        )
        for i in range(1, 16)  # 15 requests
    ]


class TestStreamingBatchProcessor:
    """Test streaming batch processor functionality."""
    
    def test_initialization(self, mock_github_client, streaming_config, batch_config):
        """Test processor initialization."""
        processor = StreamingBatchProcessor(
            mock_github_client,
            streaming_config,
            batch_config
        )
        
        assert processor.github_client == mock_github_client
        assert processor.config == streaming_config
        assert processor.batch_config == batch_config
        assert processor.memory_monitor is not None
        assert processor.chunk_semaphore._value == streaming_config.max_concurrent_chunks
    
    def test_initialization_without_memory_monitoring(self, mock_github_client):
        """Test processor initialization with memory monitoring disabled."""
        config = StreamingConfig(enable_memory_monitoring=False)
        processor = StreamingBatchProcessor(mock_github_client, config)
        
        assert processor.memory_monitor is None
    
    @pytest.mark.asyncio
    async def test_should_use_streaming_large_batch(self, mock_github_client, streaming_config, sample_requests):
        """Test streaming decision for large batches."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Large batch (15 requests > 10 threshold)
        should_stream = await processor.should_use_streaming(sample_requests)
        assert should_stream is True
    
    @pytest.mark.asyncio
    async def test_should_use_streaming_small_batch(self, mock_github_client, streaming_config, sample_requests):
        """Test streaming decision for small batches."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Small batch (5 requests < 10 threshold)
        small_batch = sample_requests[:5]
        should_stream = await processor.should_use_streaming(small_batch)
        assert should_stream is False
    
    @pytest.mark.asyncio
    async def test_should_use_streaming_memory_pressure(self, mock_github_client, streaming_config, sample_requests):
        """Test streaming decision due to memory pressure."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        with patch.object(processor.memory_monitor, 'should_reduce_batch_size') as mock_should_reduce:
            mock_should_reduce.return_value = True
            
            # Small batch but with memory pressure
            small_batch = sample_requests[:5]
            should_stream = await processor.should_use_streaming(small_batch)
            assert should_stream is True
    
    @pytest.mark.asyncio
    async def test_should_use_streaming_high_memory_estimate(self, mock_github_client, streaming_config):
        """Test streaming decision due to high estimated memory usage."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Create requests with large estimated sizes
        large_requests = [
            BatchRequest(
                repo=Repository("test", "test/test", False, "main", datetime.now()),
                file_path=f"large_file_{i}.txt",
                estimated_size=50 * 1024 * 1024  # 50MB each
            )
            for i in range(3)  # 3 requests = ~150MB total
        ]
        
        should_stream = await processor.should_use_streaming(large_requests)
        assert should_stream is True
    
    def test_create_chunks_normal(self, mock_github_client, streaming_config, sample_requests):
        """Test chunk creation under normal conditions."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        chunks = processor.create_chunks(sample_requests)  # 15 requests, chunk_size=5
        
        assert len(chunks) == 3  # 15 / 5 = 3 chunks
        assert len(chunks[0]) == 5
        assert len(chunks[1]) == 5
        assert len(chunks[2]) == 5
    
    def test_create_chunks_memory_pressure(self, mock_github_client, streaming_config, sample_requests):
        """Test chunk creation with memory pressure."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        with patch.object(processor.memory_monitor, 'should_reduce_batch_size') as mock_should_reduce, \
             patch.object(processor.memory_monitor, 'calculate_adjusted_batch_size') as mock_adjust:
            
            mock_should_reduce.return_value = True
            mock_adjust.return_value = 3  # Reduce chunk size to 3
            
            chunks = processor.create_chunks(sample_requests)  # 15 requests, adjusted chunk_size=3
            
            assert len(chunks) == 5  # 15 / 3 = 5 chunks
            assert all(len(chunk) <= 3 for chunk in chunks)
            mock_adjust.assert_called_once_with(5)
    
    @pytest.mark.asyncio
    async def test_process_single_request_streaming_success(self, mock_github_client, streaming_config, sample_requests):
        """Test processing a single request successfully."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Mock successful response
        mock_response = APIResponse(
            data=FileContent(content="test content", sha="abc123", size=12)
        )
        mock_github_client.get_file_content_async.return_value = mock_response
        
        request = sample_requests[0]
        result = await processor._process_single_request_streaming(request)
        
        assert result.request == request
        assert result.content == mock_response.data
        assert result.error is None
        assert result.processing_time > 0
        assert result.from_cache is False
    
    @pytest.mark.asyncio
    async def test_process_single_request_streaming_error(self, mock_github_client, streaming_config, sample_requests):
        """Test processing a single request with error."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Mock error response
        mock_github_client.get_file_content_async.side_effect = Exception("API Error")
        
        request = sample_requests[0]
        result = await processor._process_single_request_streaming(request)
        
        assert result.request == request
        assert result.content is None
        assert result.error is not None
        assert str(result.error) == "API Error"
        assert result.processing_time > 0
    
    @pytest.mark.asyncio
    async def test_process_chunk_streaming(self, mock_github_client, streaming_config, sample_requests):
        """Test processing a chunk with streaming."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Mock successful responses
        mock_response = APIResponse(
            data=FileContent(content="test content", sha="abc123", size=12)
        )
        mock_github_client.get_file_content_async.return_value = mock_response
        
        chunk = sample_requests[:3]  # Process 3 requests
        results = []
        
        async for result in processor.process_chunk_streaming(chunk, 0):
            results.append(result)
        
        assert len(results) == 3
        assert all(result.error is None for result in results)
        assert all(result.content is not None for result in results)
    
    @pytest.mark.asyncio
    async def test_process_chunk_streaming_with_memory_monitoring(self, mock_github_client, streaming_config, sample_requests):
        """Test chunk processing with memory monitoring."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Mock responses and memory monitoring
        mock_response = APIResponse(
            data=FileContent(content="test content", sha="abc123", size=12)
        )
        mock_github_client.get_file_content_async.return_value = mock_response
        
        with patch.object(processor.memory_monitor, 'set_baseline_memory') as mock_set_baseline, \
             patch.object(processor.memory_monitor, 'is_critical_memory_pressure') as mock_critical, \
             patch.object(processor.memory_monitor, 'force_garbage_collection') as mock_gc:
            
            mock_critical.return_value = True  # Simulate critical memory pressure
            mock_gc.return_value = {'objects_collected': 10, 'memory_freed_mb': 5.0}
            
            chunk = sample_requests[:2]
            results = []
            
            async for result in processor.process_chunk_streaming(chunk, 0):
                results.append(result)
            
            assert len(results) == 2
            mock_set_baseline.assert_called_once()
            # GC should be called for each result due to critical pressure
            assert mock_gc.call_count == 2
    
    @pytest.mark.asyncio
    async def test_process_batch_streaming_small_batch(self, mock_github_client, streaming_config, sample_requests):
        """Test streaming processing with small batch (no streaming needed)."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Mock successful responses
        mock_response = APIResponse(
            data=FileContent(content="test content", sha="abc123", size=12)
        )
        mock_github_client.get_file_content_async.return_value = mock_response
        
        small_batch = sample_requests[:5]  # Below streaming threshold
        results = []
        
        async for result in processor.process_batch_streaming(small_batch):
            results.append(result)
        
        assert len(results) == 5
        assert all(result.error is None for result in results)
    
    @pytest.mark.asyncio
    async def test_process_batch_streaming_large_batch(self, mock_github_client, streaming_config, sample_requests):
        """Test streaming processing with large batch."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Mock successful responses
        mock_response = APIResponse(
            data=FileContent(content="test content", sha="abc123", size=12)
        )
        mock_github_client.get_file_content_async.return_value = mock_response
        
        results = []
        async for result in processor.process_batch_streaming(sample_requests):  # 15 requests
            results.append(result)
        
        assert len(results) == 15
        assert all(result.error is None for result in results)
    
    @pytest.mark.asyncio
    async def test_process_batch_streaming_collect(self, mock_github_client, streaming_config, sample_requests):
        """Test streaming processing with result collection."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        # Mock successful responses
        mock_response = APIResponse(
            data=FileContent(content="test content", sha="abc123", size=12)
        )
        mock_github_client.get_file_content_async.return_value = mock_response
        
        results = await processor.process_batch_streaming_collect(sample_requests[:8])
        
        assert len(results) == 8
        assert all(result.error is None for result in results)
        assert all(result.content is not None for result in results)
    
    @pytest.mark.asyncio
    async def test_estimate_memory_usage(self, mock_github_client, streaming_config, sample_requests):
        """Test memory usage estimation."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        estimated_mb = await processor.estimate_memory_usage(sample_requests[:5])
        
        # Should be > 0 and reasonable
        assert estimated_mb > 0
        assert estimated_mb < 100  # Should be reasonable for small test files
    
    def test_get_memory_stats_with_monitoring(self, mock_github_client, streaming_config):
        """Test getting memory stats when monitoring is enabled."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        with patch.object(processor.memory_monitor, 'get_memory_report') as mock_report:
            mock_report.return_value = {'memory_usage': '50%'}
            
            stats = processor.get_memory_stats()
            assert stats == {'memory_usage': '50%'}
            mock_report.assert_called_once()
    
    def test_get_memory_stats_without_monitoring(self, mock_github_client):
        """Test getting memory stats when monitoring is disabled."""
        config = StreamingConfig(enable_memory_monitoring=False)
        processor = StreamingBatchProcessor(mock_github_client, config)
        
        stats = processor.get_memory_stats()
        assert stats is None
    
    def test_force_memory_cleanup_with_monitoring(self, mock_github_client, streaming_config):
        """Test forcing memory cleanup when monitoring is enabled."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        with patch.object(processor.memory_monitor, 'force_garbage_collection') as mock_gc:
            mock_gc.return_value = {'objects_collected': 42}
            
            stats = processor.force_memory_cleanup()
            assert stats == {'objects_collected': 42}
            mock_gc.assert_called_once()
    
    def test_force_memory_cleanup_without_monitoring(self, mock_github_client):
        """Test forcing memory cleanup when monitoring is disabled."""
        config = StreamingConfig(enable_memory_monitoring=False)
        processor = StreamingBatchProcessor(mock_github_client, config)
        
        stats = processor.force_memory_cleanup()
        assert stats is None
    
    def test_get_streaming_stats(self, mock_github_client, streaming_config):
        """Test getting streaming statistics."""
        processor = StreamingBatchProcessor(mock_github_client, streaming_config)
        
        with patch.object(processor, 'get_memory_stats') as mock_memory_stats:
            mock_memory_stats.return_value = {'memory_usage': '50%'}
            
            stats = processor.get_streaming_stats()
            
            assert 'config' in stats
            assert stats['config']['chunk_size'] == streaming_config.chunk_size
            assert stats['config']['max_memory_per_chunk_mb'] == streaming_config.max_memory_per_chunk_mb
            assert stats['config']['stream_threshold'] == streaming_config.stream_threshold
            assert stats['config']['max_concurrent_chunks'] == streaming_config.max_concurrent_chunks
            assert stats['config']['memory_monitoring_enabled'] == streaming_config.enable_memory_monitoring
            
            assert 'memory_stats' in stats
            assert stats['memory_stats'] == {'memory_usage': '50%'}


class TestStreamingConfig:
    """Test streaming configuration."""
    
    def test_default_config(self):
        """Test default streaming configuration."""
        config = StreamingConfig()
        
        assert config.chunk_size == 10
        assert config.max_memory_per_chunk_mb == 100.0
        assert config.enable_memory_monitoring is True
        assert config.stream_threshold == 50
        assert config.max_concurrent_chunks == 3
    
    def test_custom_config(self):
        """Test custom streaming configuration."""
        config = StreamingConfig(
            chunk_size=5,
            max_memory_per_chunk_mb=50.0,
            enable_memory_monitoring=False,
            stream_threshold=20,
            max_concurrent_chunks=2
        )
        
        assert config.chunk_size == 5
        assert config.max_memory_per_chunk_mb == 50.0
        assert config.enable_memory_monitoring is False
        assert config.stream_threshold == 20
        assert config.max_concurrent_chunks == 2


if __name__ == '__main__':
    pytest.main([__file__])