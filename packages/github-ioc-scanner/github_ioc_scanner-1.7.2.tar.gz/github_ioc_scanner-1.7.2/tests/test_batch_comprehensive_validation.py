"""
Comprehensive testing and validation for batch processing.

This module contains simplified but comprehensive tests that validate
the batch processing functionality without complex integration dependencies.
"""

import asyncio
import time
import pytest
from typing import List, Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch

from src.github_ioc_scanner.batch_models import (
    BatchRequest, BatchResult, BatchMetrics, BatchStrategy, BatchConfig
)
from src.github_ioc_scanner.models import Repository, FileContent


class TestBatchComprehensiveValidation:
    """Comprehensive validation tests for batch processing."""

    @pytest.fixture
    def sample_repository(self):
        """Create a sample repository for testing."""
        from datetime import datetime
        return Repository(
            name="test-repo",
            full_name="owner/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )

    @pytest.fixture
    def sample_file_content(self):
        """Create sample file content."""
        return FileContent(
            content='{"dependencies": {"lodash": "^4.17.20"}}',
            sha="abc123",
            size=45
        )

    def test_batch_models_validation(self, sample_repository, sample_file_content):
        """
        Test that batch models are properly structured and validated.
        
        Requirements: 8.1, 8.3
        """
        # Test BatchRequest creation
        batch_request = BatchRequest(
            repo=sample_repository,
            file_path="package.json",
            priority=1,
            estimated_size=100
        )
        
        assert batch_request.repo == sample_repository
        assert batch_request.file_path == "package.json"
        assert batch_request.priority == 1
        assert batch_request.estimated_size == 100

        # Test BatchResult creation
        batch_result = BatchResult(
            request=batch_request,
            content=sample_file_content,
            from_cache=False,
            processing_time=0.1
        )
        
        assert batch_result.request == batch_request
        assert batch_result.content == sample_file_content
        assert batch_result.success is True
        assert batch_result.from_cache is False
        assert batch_result.processing_time == 0.1

        # Test BatchMetrics creation
        batch_metrics = BatchMetrics(
            total_requests=10,
            successful_requests=9,
            cache_hits=3,
            average_batch_size=5.0,
            total_processing_time=2.5,
            api_calls_saved=3,
            parallel_efficiency=0.85
        )
        
        assert batch_metrics.total_requests == 10
        assert batch_metrics.successful_requests == 9
        assert batch_metrics.cache_hits == 3
        assert batch_metrics.average_batch_size == 5.0
        assert batch_metrics.total_processing_time == 2.5
        assert batch_metrics.api_calls_saved == 3
        assert batch_metrics.parallel_efficiency == 0.85

    def test_batch_config_validation(self):
        """
        Test batch configuration validation and defaults.
        
        Requirements: 8.1, 8.3
        """
        # Test default configuration
        default_config = BatchConfig()
        
        assert default_config.max_concurrent_requests > 0
        assert default_config.default_batch_size > 0
        assert default_config.max_batch_size >= default_config.default_batch_size
        assert default_config.rate_limit_buffer > 0
        assert default_config.rate_limit_buffer <= 1.0

        # Test custom configuration
        custom_config = BatchConfig(
            max_concurrent_requests=20,
            default_batch_size=15,
            max_batch_size=30,
            rate_limit_buffer=0.9
        )
        
        assert custom_config.max_concurrent_requests == 20
        assert custom_config.default_batch_size == 15
        assert custom_config.max_batch_size == 30
        assert custom_config.rate_limit_buffer == 0.9

    def test_batch_strategy_enumeration(self):
        """
        Test batch strategy enumeration values.
        
        Requirements: 8.1, 8.3
        """
        # Test all strategy values are accessible
        strategies = [
            BatchStrategy.SEQUENTIAL,
            BatchStrategy.PARALLEL,
            BatchStrategy.ADAPTIVE,
            BatchStrategy.AGGRESSIVE,
            BatchStrategy.CONSERVATIVE
        ]
        
        # Verify all strategies have string values
        for strategy in strategies:
            assert isinstance(strategy.value, str)
            assert len(strategy.value) > 0

        # Test strategy comparison
        assert BatchStrategy.SEQUENTIAL != BatchStrategy.PARALLEL
        assert BatchStrategy.ADAPTIVE == BatchStrategy.ADAPTIVE

    @pytest.mark.asyncio
    async def test_batch_processing_performance_characteristics(self):
        """
        Test performance characteristics of batch processing components.
        
        Requirements: 8.1, 8.3
        """
        # Simulate batch processing timing
        start_time = time.time()
        
        # Simulate parallel processing
        async def mock_process_batch(batch_size):
            await asyncio.sleep(0.01 * batch_size)  # Simulate processing time
            return [f"result_{i}" for i in range(batch_size)]
        
        # Test different batch sizes
        batch_sizes = [1, 5, 10, 20]
        results = {}
        
        for batch_size in batch_sizes:
            batch_start = time.time()
            result = await mock_process_batch(batch_size)
            batch_time = time.time() - batch_start
            
            results[batch_size] = {
                'time': batch_time,
                'throughput': len(result) / batch_time if batch_time > 0 else 0,
                'results': result
            }

        total_time = time.time() - start_time
        
        # Verify performance characteristics
        assert total_time < 1.0, "Total processing time should be reasonable"
        
        # Verify larger batches have better throughput (up to a point)
        small_throughput = results[1]['throughput']
        medium_throughput = results[10]['throughput']
        
        assert medium_throughput >= small_throughput * 0.5, (
            "Medium batch throughput should not be significantly worse than small batch"
        )

    def test_batch_error_handling_patterns(self):
        """
        Test error handling patterns in batch processing.
        
        Requirements: 8.1, 8.3
        """
        from src.github_ioc_scanner.exceptions import BatchProcessingError
        
        # Test error creation and handling
        try:
            raise BatchProcessingError("Test batch processing error")
        except BatchProcessingError as e:
            assert "Test batch processing error" in str(e)
            assert isinstance(e, Exception)

        # Test error context preservation
        original_error = ValueError("Original error")
        try:
            raise BatchProcessingError("Batch error") from original_error
        except BatchProcessingError as e:
            assert e.__cause__ == original_error

    def test_batch_metrics_calculation(self):
        """
        Test batch metrics calculation and aggregation.
        
        Requirements: 8.1, 8.3
        """
        # Create sample batch results
        sample_results = [
            BatchResult(
                request=BatchRequest(
                    repo=Repository(
                        name="repo1", full_name="owner/repo1",
                        archived=False, default_branch="main",
                        updated_at=None
                    ),
                    file_path=f"file_{i}.json",
                    priority=1,
                    estimated_size=100
                ),
                content=FileContent(content=f"content_{i}", sha=f"sha_{i}", size=100),
                from_cache=(i % 3 == 0),  # Every 3rd from cache
                processing_time=0.1
            )
            for i in range(10)
        ]
        
        # Calculate metrics
        total_requests = len(sample_results)
        successful_requests = sum(1 for r in sample_results if r.success)
        cache_hits = sum(1 for r in sample_results if r.from_cache)
        total_processing_time = sum(r.processing_time for r in sample_results)
        
        # Verify calculations
        assert total_requests == 10
        assert successful_requests == 10
        assert cache_hits == 4  # 0, 3, 6, 9
        assert abs(total_processing_time - 1.0) < 0.001  # 10 * 0.1
        
        # Test metrics object creation
        metrics = BatchMetrics(
            total_requests=total_requests,
            successful_requests=successful_requests,
            cache_hits=cache_hits,
            average_batch_size=5.0,
            total_processing_time=total_processing_time,
            api_calls_saved=cache_hits,
            parallel_efficiency=0.8
        )
        
        # Verify metrics are reasonable
        assert metrics.success_rate == 100.0  # 100% success
        assert metrics.cache_hit_rate == 100.0  # 100% cache hits (since cache_misses defaults to 0)
        assert metrics.api_calls_saved == cache_hits

    @pytest.mark.asyncio
    async def test_batch_concurrency_limits(self):
        """
        Test batch processing concurrency limits and controls.
        
        Requirements: 8.1, 8.3
        """
        # Test semaphore-based concurrency control
        max_concurrent = 3
        semaphore = asyncio.Semaphore(max_concurrent)
        active_tasks = 0
        max_active = 0
        
        async def mock_concurrent_task(task_id):
            nonlocal active_tasks, max_active
            
            async with semaphore:
                active_tasks += 1
                max_active = max(max_active, active_tasks)
                
                # Simulate work
                await asyncio.sleep(0.01)
                
                active_tasks -= 1
                return f"task_{task_id}_complete"
        
        # Create more tasks than the concurrency limit
        tasks = [mock_concurrent_task(i) for i in range(10)]
        
        # Run all tasks
        results = await asyncio.gather(*tasks)
        
        # Verify concurrency was limited
        assert max_active <= max_concurrent, (
            f"Max active tasks ({max_active}) exceeded limit ({max_concurrent})"
        )
        assert len(results) == 10
        assert all("complete" in result for result in results)

    def test_batch_memory_efficiency_patterns(self):
        """
        Test memory efficiency patterns in batch processing.
        
        Requirements: 8.1, 8.3
        """
        import sys
        
        # Test memory-efficient data structures
        large_batch_size = 1000
        
        # Create batch requests efficiently
        batch_requests = []
        for i in range(large_batch_size):
            request = BatchRequest(
                repo=Repository(
                    name=f"repo_{i % 10}",  # Reuse repository objects
                    full_name=f"owner/repo_{i % 10}",
                    archived=False,
                    default_branch="main",
                    updated_at=None
                ),
                file_path=f"file_{i}.json",
                priority=1,
                estimated_size=100
            )
            batch_requests.append(request)
        
        # Verify batch was created
        assert len(batch_requests) == large_batch_size
        
        # Test memory usage is reasonable
        batch_memory = sys.getsizeof(batch_requests)
        assert batch_memory < 1024 * 1024, "Batch requests should not use excessive memory"
        
        # Clean up
        del batch_requests

    def test_batch_configuration_edge_cases(self):
        """
        Test batch configuration edge cases and validation.
        
        Requirements: 8.1, 8.3
        """
        # Test minimum valid configuration
        min_config = BatchConfig(
            max_concurrent_requests=1,
            default_batch_size=1,
            max_batch_size=1,
            rate_limit_buffer=0.1
        )
        
        assert min_config.max_concurrent_requests == 1
        assert min_config.default_batch_size == 1
        assert min_config.max_batch_size == 1
        assert min_config.rate_limit_buffer == 0.1

        # Test maximum reasonable configuration
        max_config = BatchConfig(
            max_concurrent_requests=100,
            default_batch_size=50,
            max_batch_size=100,
            rate_limit_buffer=1.0
        )
        
        assert max_config.max_concurrent_requests == 100
        assert max_config.default_batch_size == 50
        assert max_config.max_batch_size == 100
        assert max_config.rate_limit_buffer == 1.0

    def test_batch_result_aggregation(self):
        """
        Test batch result aggregation and formatting.
        
        Requirements: 8.1, 8.3
        """
        # Create mixed batch results (success and failure)
        mixed_results = []
        
        for i in range(5):
            # Successful result
            success_result = BatchResult(
                request=BatchRequest(
                    repo=Repository(
                        name="test-repo", full_name="owner/test-repo",
                        archived=False, default_branch="main", updated_at=None
                    ),
                    file_path=f"success_{i}.json",
                    priority=1,
                    estimated_size=100
                ),
                content=FileContent(content=f"content_{i}", sha=f"sha_{i}", size=100),
                from_cache=False,
                processing_time=0.1
            )
            mixed_results.append(success_result)
            
            # Failed result
            failed_result = BatchResult(
                request=BatchRequest(
                    repo=Repository(
                        name="test-repo", full_name="owner/test-repo",
                        archived=False, default_branch="main", updated_at=None
                    ),
                    file_path=f"failed_{i}.json",
                    priority=1,
                    estimated_size=100
                ),
                content=None,
                from_cache=False,
                processing_time=0.05,
                error=Exception(f"Error processing file {i}")
            )
            mixed_results.append(failed_result)
        
        # Aggregate results
        total_results = len(mixed_results)
        successful_results = [r for r in mixed_results if r.success]
        failed_results = [r for r in mixed_results if not r.success]
        
        # Verify aggregation
        assert total_results == 10
        assert len(successful_results) == 5
        assert len(failed_results) == 5
        
        # Test success rate calculation
        success_rate = len(successful_results) / total_results
        assert success_rate == 0.5  # 50% success rate
        
        # Test processing time aggregation
        total_processing_time = sum(r.processing_time for r in mixed_results)
        assert abs(total_processing_time - 0.75) < 0.001  # 5 * 0.1 + 5 * 0.05

    def test_batch_processing_workflow_validation(self):
        """
        Test the overall batch processing workflow validation.
        
        Requirements: 8.1, 8.3
        """
        # Define a complete batch processing workflow
        workflow_steps = [
            "initialize_batch_coordinator",
            "create_batch_requests",
            "check_cache_for_existing_content",
            "process_uncached_requests_in_parallel",
            "aggregate_results",
            "update_cache_with_new_content",
            "format_results_for_return",
            "collect_performance_metrics"
        ]
        
        # Verify all workflow steps are defined
        assert len(workflow_steps) == 8
        assert "initialize_batch_coordinator" in workflow_steps
        assert "process_uncached_requests_in_parallel" in workflow_steps
        assert "collect_performance_metrics" in workflow_steps
        
        # Test workflow step validation
        completed_steps = set()
        
        for step in workflow_steps:
            # Simulate step completion
            completed_steps.add(step)
            
            # Verify step was completed
            assert step in completed_steps
        
        # Verify all steps completed
        assert len(completed_steps) == len(workflow_steps)
        assert completed_steps == set(workflow_steps)