"""Parallel batch processor for GitHub API requests with intelligent concurrency management."""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .async_github_client import AsyncGitHubClient
from .batch_models import (
    BatchRequest, BatchResult, BatchMetrics, BatchConfig, 
    AsyncBatchContext, NetworkConditions, BatchRecoveryPlan
)
from .exceptions import RateLimitError, NetworkError, APIError
from .logging_config import get_logger
from .memory_monitor import MemoryMonitor
from .rate_limit_manager import ParallelRateLimitManager as RateLimitManager
from .resource_manager import ResourceManager, ResourceConfig, get_resource_manager
from .retry_manager import RetryManager, RetryConfig

logger = get_logger(__name__)


class ParallelBatchProcessor:
    """Handles parallel processing of batch requests with intelligent concurrency management."""
    
    def __init__(
        self,
        github_client: AsyncGitHubClient,
        config: Optional[BatchConfig] = None
    ):
        """Initialize the parallel batch processor.
        
        Args:
            github_client: Async GitHub client for API requests
            config: Batch processing configuration
        """
        self.github_client = github_client
        self.config = config or BatchConfig()
        
        # Validate configuration
        config_errors = self.config.validate()
        if config_errors:
            raise ValueError(f"Invalid batch configuration: {', '.join(config_errors)}")
        
        # Initialize rate limit manager
        self.rate_limit_manager = RateLimitManager(
            initial_concurrency=self.config.max_concurrent_requests,
            max_concurrency=self.config.max_concurrent_requests,
            min_concurrency=1,
            buffer_percentage=self.config.rate_limit_buffer,
            adjustment_interval=10.0  # Adjust every 10 seconds minimum
        )
        
        # Initialize retry manager
        retry_config = RetryConfig(
            max_attempts=self.config.retry_attempts,
            base_delay=self.config.retry_delay_base,
            rate_limit_max_attempts=self.config.retry_attempts + 2,  # More attempts for rate limits
            network_max_attempts=self.config.retry_attempts + 1
        )
        self.retry_manager = RetryManager(retry_config)
        
        # Initialize memory monitor
        self.memory_monitor = MemoryMonitor(
            max_memory_threshold=self.config.max_memory_usage_mb / 1024 if hasattr(self.config, 'max_memory_usage_mb') else 0.8,
            critical_memory_threshold=0.9,
            min_batch_size=self.config.min_batch_size if hasattr(self.config, 'min_batch_size') else 1,
            max_batch_size=self.config.max_batch_size if hasattr(self.config, 'max_batch_size') else 50
        )
        
        # Initialize resource manager
        resource_config = ResourceConfig(
            auto_cleanup_enabled=True,
            cleanup_interval_seconds=60.0,  # Clean up every minute
            memory_cleanup_threshold=0.8,
            max_resource_age_seconds=300.0,  # 5 minutes
            force_gc_on_cleanup=True
        )
        self.resource_manager = ResourceManager(resource_config)
        
        # Initialize concurrency management
        self.current_concurrency = self.rate_limit_manager.get_current_concurrency()
        self.semaphore = asyncio.Semaphore(self.current_concurrency)
        self._concurrency_lock = asyncio.Lock()
        
        # Performance tracking
        self.metrics = BatchMetrics()
        
    async def process_batch_parallel(
        self,
        requests: List[BatchRequest],
        context: Optional[AsyncBatchContext] = None
    ) -> List[BatchResult]:
        """Process batch requests in parallel with rate limiting and error handling.
        
        Args:
            requests: List of batch requests to process
            context: Optional async batch context for coordination
            
        Returns:
            List of batch results
        """
        if not requests:
            return []
        
        # Set baseline memory before processing
        self.memory_monitor.set_baseline_memory()
        
        # Check memory pressure and adjust batch size if needed
        if self.memory_monitor.should_reduce_batch_size():
            original_size = len(requests)
            adjusted_size = self.memory_monitor.calculate_adjusted_batch_size(original_size)
            if adjusted_size < original_size:
                logger.debug(f"Reducing batch size from {original_size} to {adjusted_size} due to memory pressure")
                requests = requests[:adjusted_size]
        
        logger.info(f"Processing batch of {len(requests)} requests with concurrency {self.current_concurrency}")
        
        # Initialize metrics
        self.metrics = BatchMetrics()
        self.metrics.start_time = datetime.now()
            
        # Use provided context or create new one
        if context is None:
            rate_limit_info = self.rate_limit_manager.get_rate_limit_status()
            context = AsyncBatchContext(
                semaphore=self.semaphore,
                rate_limit_remaining=rate_limit_info.remaining if rate_limit_info else 5000,
                rate_limit_reset=rate_limit_info.reset_time if rate_limit_info else 0
            )
        
        try:
            # Create tasks for parallel processing
            tasks = []
            for request in requests:
                task = self._process_single_request(request, context)
                tasks.append(task)
            
            # Execute all tasks in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle exceptions
            batch_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    # Create error result for exceptions
                    batch_result = BatchResult(
                        request=requests[i],
                        error=result,
                        processing_time=0.0
                    )
                    logger.warning(f"Request failed with exception: {result}")
                else:
                    batch_result = result
                
                # Update metrics
                self.metrics.add_result(batch_result)
                batch_results.append(batch_result)
            
            # Update performance metrics for rate limit manager
            await self._update_performance_metrics(batch_results)
            
            # Finalize metrics
            self.metrics.finish()
            self.metrics.average_batch_size = len(requests)
            
            # Calculate parallel efficiency
            if self.metrics.total_processing_time > 0:
                sequential_time = sum(r.processing_time for r in batch_results)
                self.metrics.parallel_efficiency = min(1.0, sequential_time / self.metrics.duration_seconds)
            
            logger.info(
                f"Batch completed: {self.metrics.successful_requests}/{self.metrics.total_requests} successful, "
                f"{self.metrics.parallel_efficiency:.2%} efficiency"
            )
            
            return batch_results
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            self.metrics.finish()
            raise
    
    async def _process_single_request(
        self,
        request: BatchRequest,
        context: AsyncBatchContext
    ) -> BatchResult:
        """Process a single request with semaphore control and retry logic.
        
        Args:
            request: Batch request to process
            context: Async batch context
            
        Returns:
            Batch result
        """
        start_time = time.time()
        
        # Acquire semaphore for concurrency control
        async with context.semaphore:
            # Check and adjust for rate limits before making request
            await self._check_rate_limits(context)
            
            # Define the operation to retry
            async def api_operation():
                # Make the actual API request
                response = await self.github_client.get_file_content_async(
                    request.repo, 
                    request.file_path
                )
                
                # Update rate limit information from response
                if hasattr(response, 'rate_limit_remaining') and hasattr(response, 'rate_limit_reset'):
                    new_concurrency = await self.rate_limit_manager.update_rate_limit_info(
                        remaining=response.rate_limit_remaining,
                        limit=5000,  # GitHub default limit
                        reset_time=response.rate_limit_reset
                    )
                    
                    # Update semaphore if concurrency changed
                    if new_concurrency is not None:
                        await self._update_semaphore(new_concurrency)
                
                if response.data:
                    return response.data
                else:
                    raise APIError(f"No content returned for {request.file_path}")
            
            # Execute with retry logic
            try:
                # Create custom retry config for rate limit errors
                if isinstance(context, AsyncBatchContext) and hasattr(context, 'rate_limit_remaining'):
                    if context.rate_limit_remaining < 100:  # Low rate limit
                        custom_config = self.retry_manager.create_error_specific_config(
                            RateLimitError, 
                            max_attempts=self.config.retry_attempts + 3,
                            base_delay=self.config.retry_delay_base * 2
                        )
                    else:
                        custom_config = None
                else:
                    custom_config = None
                
                content = await self.retry_manager.execute_with_retry(
                    api_operation,
                    operation_name=f"get_file_content_{request.repo.full_name}_{request.file_path}",
                    custom_config=custom_config
                )
                
                processing_time = time.time() - start_time
                return BatchResult(
                    request=request,
                    content=content,
                    processing_time=processing_time,
                    from_cache=False  # TODO: Handle cache detection
                )
                
            except RateLimitError as e:
                # Handle rate limit exceeded at the retry manager level
                new_concurrency, wait_time = await self.rate_limit_manager.handle_rate_limit_exceeded()
                await self._update_semaphore(new_concurrency)
                
                return BatchResult(
                    request=request,
                    error=e,
                    processing_time=time.time() - start_time
                )
                
            except Exception as e:
                return BatchResult(
                    request=request,
                    error=e,
                    processing_time=time.time() - start_time
                )
        
        # This should never be reached
        return BatchResult(
            request=request,
            error=APIError("Unexpected error in request processing"),
            processing_time=time.time() - start_time
        )
    
    async def _check_rate_limits(self, context: AsyncBatchContext) -> None:
        """Check rate limits and pause if necessary.
        
        Args:
            context: Async batch context
        """
        rate_limit_info = self.rate_limit_manager.get_rate_limit_status()
        
        if rate_limit_info and rate_limit_info.is_low(threshold=self.config.rate_limit_buffer):
            wait_time = rate_limit_info.time_until_reset
            if wait_time > 0:
                logger.warning(
                    f"Rate limit low ({rate_limit_info.remaining}/{rate_limit_info.limit}), "
                    f"waiting {wait_time:.1f}s"
                )
                await asyncio.sleep(wait_time)
    
    async def _update_performance_metrics(self, results: List[BatchResult]) -> None:
        """Update performance metrics for rate limit manager.
        
        Args:
            results: List of batch results to analyze
        """
        if not results:
            return
        
        total_requests = len(results)
        successful_requests = sum(1 for r in results if r.success)
        failed_requests = total_requests - successful_requests
        
        success_rate = (successful_requests / total_requests) * 100
        error_rate = (failed_requests / total_requests) * 100
        
        # Calculate average response time
        response_times = [r.processing_time for r in results if r.processing_time > 0]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0.0
        
        await self.rate_limit_manager.update_performance_metrics(
            success_rate=success_rate,
            error_rate=error_rate,
            avg_response_time=avg_response_time
        )
    
    async def get_rate_limit_statistics(self) -> Dict[str, any]:
        """Get comprehensive rate limit and concurrency statistics.
        
        Returns:
            Dictionary containing rate limit statistics
        """
        return self.rate_limit_manager.get_statistics()
    
    async def _update_semaphore(self, new_concurrency: int) -> None:
        """Update semaphore with new concurrency limit.
        
        Args:
            new_concurrency: New concurrency limit
        """
        if new_concurrency != self.current_concurrency:
            # Create new semaphore with updated limit
            old_concurrency = self.current_concurrency
            self.current_concurrency = new_concurrency
            self.semaphore = asyncio.Semaphore(new_concurrency)
            
            logger.debug(f"Semaphore updated: {old_concurrency} -> {new_concurrency}")
    
    async def get_retry_statistics(self) -> Dict[str, Any]:
        """Get comprehensive retry statistics.
        
        Returns:
            Dictionary containing retry statistics
        """
        retry_stats = self.retry_manager.get_statistics()
        return {
            'total_operations': retry_stats.total_operations,
            'successful_operations': retry_stats.successful_operations,
            'failed_operations': retry_stats.failed_operations,
            'success_rate': retry_stats.success_rate,
            'total_retry_attempts': retry_stats.total_retry_attempts,
            'average_retry_delay': retry_stats.average_retry_delay,
            'retry_rate': retry_stats.retry_rate,
            'error_counts': retry_stats.error_counts,
            'circuit_breaker': self.retry_manager.get_circuit_breaker_status()
        }
    
    def adjust_concurrency(self, rate_limit_remaining: int, rate_limit_limit: int = 5000, reset_time: int = 0) -> None:
        """Synchronously adjust concurrency based on rate limits.
        
        Args:
            rate_limit_remaining: Current rate limit remaining
            rate_limit_limit: Total rate limit
            reset_time: Rate limit reset timestamp
        """
        # This is a synchronous wrapper for the async method
        # Used for external callers who need to adjust concurrency
        asyncio.create_task(
            self.rate_limit_manager.update_rate_limit_info(
                remaining=rate_limit_remaining,
                limit=rate_limit_limit,
                reset_time=reset_time
            )
        )
    
    def get_current_concurrency(self) -> int:
        """Get current concurrency limit.
        
        Returns:
            Current concurrency limit
        """
        return self.rate_limit_manager.get_current_concurrency()
    
    def get_metrics(self) -> BatchMetrics:
        """Get current batch processing metrics.
        
        Returns:
            Current batch metrics
        """
        return self.metrics
    
    def reset_metrics(self) -> None:
        """Reset batch processing metrics."""
        self.metrics = BatchMetrics()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get current memory statistics and recommendations.
        
        Returns:
            Dictionary containing memory statistics
        """
        return self.memory_monitor.get_memory_report()
    
    def force_memory_cleanup(self) -> Dict[str, Any]:
        """Force memory cleanup and garbage collection.
        
        Returns:
            Dictionary containing cleanup statistics
        """
        return self.memory_monitor.force_garbage_collection()
    
    def check_memory_pressure(self) -> Tuple[bool, bool]:
        """Check current memory pressure status.
        
        Returns:
            Tuple of (should_reduce_batch_size, is_critical_pressure)
        """
        return (
            self.memory_monitor.should_reduce_batch_size(),
            self.memory_monitor.is_critical_memory_pressure()
        )
    
    def get_resource_stats(self) -> Dict[str, Any]:
        """Get comprehensive resource management statistics.
        
        Returns:
            Dictionary containing resource statistics
        """
        return self.resource_manager.get_resource_stats()
    
    async def cleanup_resources(self) -> Dict[str, Any]:
        """Perform resource cleanup and return statistics.
        
        Returns:
            Dictionary containing cleanup statistics
        """
        return await self.resource_manager.perform_memory_cleanup()
    
    async def shutdown_processor(self) -> None:
        """Shutdown the processor and clean up all resources."""
        logger.info("Shutting down parallel batch processor")
        
        # Stop rate limit manager
        if hasattr(self.rate_limit_manager, 'shutdown'):
            await self.rate_limit_manager.shutdown()
        
        # Shutdown resource manager
        await self.resource_manager.shutdown()
        
        logger.info("Parallel batch processor shutdown complete")
    
    async def create_recovery_plan(
        self,
        failed_requests: List[BatchRequest],
        errors: List[Exception]
    ) -> BatchRecoveryPlan:
        """Create a recovery plan for failed requests.
        
        Args:
            failed_requests: List of failed batch requests
            errors: List of corresponding errors
            
        Returns:
            Recovery plan for handling failures
        """
        retry_requests = []
        skip_requests = []
        
        for request, error in zip(failed_requests, errors):
            if isinstance(error, RateLimitError):
                # Always retry rate limit errors
                retry_requests.append(request)
            elif isinstance(error, NetworkError):
                # Retry network errors
                retry_requests.append(request)
            elif isinstance(error, APIError) and hasattr(error, 'status_code'):
                # Retry certain API errors
                if error.status_code in [500, 502, 503, 504]:  # Server errors
                    retry_requests.append(request)
                else:
                    skip_requests.append(request)
            else:
                # Skip other errors
                skip_requests.append(request)
        
        # Calculate delay based on error types
        delay_seconds = 0.0
        if any(isinstance(e, RateLimitError) for e in errors):
            # Longer delay for rate limit errors
            delay_seconds = max(delay_seconds, 30.0)
        elif any(isinstance(e, NetworkError) for e in errors):
            # Moderate delay for network errors
            delay_seconds = max(delay_seconds, 5.0)
        
        return BatchRecoveryPlan(
            retry_requests=retry_requests,
            skip_requests=skip_requests,
            delay_seconds=delay_seconds
        )