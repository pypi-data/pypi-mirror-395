"""Streaming batch processor for memory-efficient processing of large batches."""

import asyncio
import logging
from typing import AsyncIterator, List, Optional, Dict, Any
from dataclasses import dataclass

from .async_github_client import AsyncGitHubClient
from .batch_models import BatchRequest, BatchResult, BatchConfig
from .memory_monitor import MemoryMonitor
from .logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class StreamingConfig:
    """Configuration for streaming batch processing."""
    chunk_size: int = 10  # Number of requests per chunk
    max_memory_per_chunk_mb: float = 100.0  # Maximum memory per chunk
    enable_memory_monitoring: bool = True
    stream_threshold: int = 50  # Start streaming for batches larger than this
    max_concurrent_chunks: int = 3  # Maximum concurrent chunks


class StreamingBatchProcessor:
    """Processes large batches using streaming and chunked processing to minimize memory usage."""
    
    def __init__(
        self,
        github_client: AsyncGitHubClient,
        config: Optional[StreamingConfig] = None,
        batch_config: Optional[BatchConfig] = None
    ):
        """Initialize streaming batch processor.
        
        Args:
            github_client: Async GitHub client for API requests
            config: Streaming configuration
            batch_config: General batch configuration
        """
        self.github_client = github_client
        self.config = config or StreamingConfig()
        self.batch_config = batch_config or BatchConfig()
        
        # Initialize memory monitor if enabled
        if self.config.enable_memory_monitoring:
            self.memory_monitor = MemoryMonitor(
                max_memory_threshold=0.8,
                critical_memory_threshold=0.9,
                min_batch_size=1,
                max_batch_size=self.config.chunk_size
            )
        else:
            self.memory_monitor = None
        
        # Semaphore for controlling concurrent chunks
        self.chunk_semaphore = asyncio.Semaphore(self.config.max_concurrent_chunks)
    
    async def should_use_streaming(self, requests: List[BatchRequest]) -> bool:
        """Determine if streaming should be used for the given batch.
        
        Args:
            requests: List of batch requests
            
        Returns:
            True if streaming should be used
        """
        # Use streaming for large batches
        if len(requests) >= self.config.stream_threshold:
            return True
        
        # Use streaming if memory pressure is detected
        if self.memory_monitor and self.memory_monitor.should_reduce_batch_size():
            logger.debug("Using streaming due to memory pressure")
            return True
        
        # Estimate memory usage based on request sizes
        estimated_memory_mb = sum(
            getattr(req, 'estimated_size', 1024) for req in requests
        ) / (1024 * 1024)
        
        if estimated_memory_mb > self.config.max_memory_per_chunk_mb * 2:
            logger.debug(f"Using streaming due to estimated memory usage: {estimated_memory_mb:.1f} MB")
            return True
        
        return False
    
    def create_chunks(self, requests: List[BatchRequest]) -> List[List[BatchRequest]]:
        """Split requests into chunks for processing.
        
        Args:
            requests: List of batch requests
            
        Returns:
            List of request chunks
        """
        chunk_size = self.config.chunk_size
        
        # Adjust chunk size based on memory pressure
        if self.memory_monitor and self.memory_monitor.should_reduce_batch_size():
            chunk_size = self.memory_monitor.calculate_adjusted_batch_size(chunk_size)
            logger.debug(f"Adjusted chunk size to {chunk_size} due to memory pressure")
        
        # Create chunks
        chunks = []
        for i in range(0, len(requests), chunk_size):
            chunk = requests[i:i + chunk_size]
            chunks.append(chunk)
        
        logger.info(f"Created {len(chunks)} chunks with average size {len(requests) / len(chunks):.1f}")
        return chunks
    
    async def process_chunk_streaming(
        self,
        chunk: List[BatchRequest],
        chunk_index: int
    ) -> AsyncIterator[BatchResult]:
        """Process a single chunk and yield results as they complete.
        
        Args:
            chunk: List of requests in the chunk
            chunk_index: Index of the chunk for logging
            
        Yields:
            BatchResult objects as they complete
        """
        async with self.chunk_semaphore:
            logger.debug(f"Processing chunk {chunk_index} with {len(chunk)} requests")
            
            # Set memory baseline for this chunk
            if self.memory_monitor:
                self.memory_monitor.set_baseline_memory()
            
            # Process requests in the chunk concurrently
            tasks = []
            for request in chunk:
                task = self._process_single_request_streaming(request)
                tasks.append(task)
            
            # Yield results as they complete
            for completed_task in asyncio.as_completed(tasks):
                try:
                    result = await completed_task
                    yield result
                    
                    # Check memory pressure after each result
                    if self.memory_monitor and self.memory_monitor.is_critical_memory_pressure():
                        logger.warning("Critical memory pressure detected, forcing garbage collection")
                        self.memory_monitor.force_garbage_collection()
                        
                except Exception as e:
                    logger.error(f"Error processing request in chunk {chunk_index}: {e}")
                    # Create error result
                    error_result = BatchResult(
                        request=chunk[0] if chunk else BatchRequest(None, "unknown"),  # Best effort
                        error=e,
                        processing_time=0.0
                    )
                    yield error_result
            
            logger.debug(f"Completed chunk {chunk_index}")
    
    async def _process_single_request_streaming(self, request: BatchRequest) -> BatchResult:
        """Process a single request with memory-efficient handling.
        
        Args:
            request: Batch request to process
            
        Returns:
            Batch result
        """
        import time
        start_time = time.time()
        
        try:
            # Make API request
            response = await self.github_client.get_file_content_async(
                request.repo,
                request.file_path
            )
            
            if response.data:
                # For large files, we might want to process content in chunks
                # but for now, we'll just return the result
                processing_time = time.time() - start_time
                return BatchResult(
                    request=request,
                    content=response.data,
                    processing_time=processing_time,
                    from_cache=False
                )
            else:
                raise Exception(f"No content returned for {request.file_path}")
                
        except Exception as e:
            processing_time = time.time() - start_time
            return BatchResult(
                request=request,
                error=e,
                processing_time=processing_time
            )
    
    async def process_batch_streaming(
        self,
        requests: List[BatchRequest]
    ) -> AsyncIterator[BatchResult]:
        """Process batch requests using streaming approach.
        
        Args:
            requests: List of batch requests to process
            
        Yields:
            BatchResult objects as they complete
        """
        if not requests:
            return
        
        logger.info(f"Starting streaming processing of {len(requests)} requests")
        
        # Check if streaming should be used
        use_streaming = await self.should_use_streaming(requests)
        if not use_streaming:
            logger.info("Streaming not needed, using regular processing")
            # Fall back to regular processing (could delegate to ParallelBatchProcessor)
            # For now, we'll still use chunked processing but with larger chunks
            chunks = [requests]  # Single chunk
        else:
            # Create chunks for streaming
            chunks = self.create_chunks(requests)
        
        # Process chunks and yield results
        chunk_tasks = []
        for i, chunk in enumerate(chunks):
            chunk_task = self.process_chunk_streaming(chunk, i)
            chunk_tasks.append(chunk_task)
        
        # Yield results from all chunks as they complete
        async def process_all_chunks():
            for chunk_task in chunk_tasks:
                async for result in chunk_task:
                    yield result
        
        async for result in process_all_chunks():
            yield result
        
        logger.info(f"Completed streaming processing of {len(requests)} requests")
    
    async def process_batch_streaming_collect(
        self,
        requests: List[BatchRequest]
    ) -> List[BatchResult]:
        """Process batch requests using streaming and collect all results.
        
        This is a convenience method that collects all streaming results into a list.
        Use process_batch_streaming() for true streaming behavior.
        
        Args:
            requests: List of batch requests to process
            
        Returns:
            List of all batch results
        """
        results = []
        async for result in self.process_batch_streaming(requests):
            results.append(result)
        return results
    
    def get_memory_stats(self) -> Optional[Dict[str, Any]]:
        """Get current memory statistics.
        
        Returns:
            Memory statistics if monitoring is enabled, None otherwise
        """
        if self.memory_monitor:
            return self.memory_monitor.get_memory_report()
        return None
    
    def force_memory_cleanup(self) -> Optional[Dict[str, Any]]:
        """Force memory cleanup and garbage collection.
        
        Returns:
            Cleanup statistics if monitoring is enabled, None otherwise
        """
        if self.memory_monitor:
            return self.memory_monitor.force_garbage_collection()
        return None
    
    async def estimate_memory_usage(self, requests: List[BatchRequest]) -> float:
        """Estimate memory usage for processing the given requests.
        
        Args:
            requests: List of batch requests
            
        Returns:
            Estimated memory usage in MB
        """
        # Base memory per request (rough estimate)
        base_memory_per_request = 0.1  # 100KB base
        
        # Add estimated file sizes
        total_estimated_size = sum(
            getattr(req, 'estimated_size', 1024) for req in requests
        )
        
        # Convert to MB and add overhead
        estimated_mb = (total_estimated_size / (1024 * 1024)) + (len(requests) * base_memory_per_request)
        
        return estimated_mb
    
    def get_streaming_stats(self) -> Dict[str, Any]:
        """Get statistics about streaming configuration and performance.
        
        Returns:
            Dictionary containing streaming statistics
        """
        return {
            'config': {
                'chunk_size': self.config.chunk_size,
                'max_memory_per_chunk_mb': self.config.max_memory_per_chunk_mb,
                'stream_threshold': self.config.stream_threshold,
                'max_concurrent_chunks': self.config.max_concurrent_chunks,
                'memory_monitoring_enabled': self.config.enable_memory_monitoring
            },
            'memory_stats': self.get_memory_stats() if self.memory_monitor else None
        }