"""
Load testing for batch processing scalability.

This module contains load tests for high-volume batch processing,
stress tests for concurrent batch operations, and tests for batch
processing under resource constraints.
"""

import asyncio
import time
import pytest
import psutil
import os
from typing import List, Dict, Any, Optional
from unittest.mock import AsyncMock, MagicMock, patch
from concurrent.futures import ThreadPoolExecutor
import threading
import gc

from src.github_ioc_scanner.batch_coordinator import BatchCoordinator
from src.github_ioc_scanner.batch_models import (
    BatchRequest, BatchResult, BatchMetrics, BatchStrategy, BatchConfig
)
from src.github_ioc_scanner.models import Repository, FileContent
from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
from src.github_ioc_scanner.exceptions import APIError, RateLimitError


class TestBatchLoadScalability:
    """Load and scalability tests for batch processing."""

    @pytest.fixture
    def mock_cache_manager(self):
        """Create a mock cache manager for testing."""
        from src.github_ioc_scanner.cache_manager import CacheManager
        cache_manager = MagicMock(spec=CacheManager)
        return cache_manager

    @pytest.fixture
    def scalable_mock_client(self):
        """Create a mock client that can handle high-volume requests."""
        client = AsyncMock(spec=AsyncGitHubClient)
        
        # Track request statistics
        client._request_count = 0
        client._concurrent_requests = 0
        client._max_concurrent = 0
        client._request_times = []
        
        async def mock_get_multiple_file_contents(repo, paths):
            client._request_count += 1
            client._concurrent_requests += 1
            client._max_concurrent = max(client._max_concurrent, client._concurrent_requests)
            
            start_time = time.time()
            
            # Simulate realistic processing time based on batch size
            base_delay = 0.01  # 10ms base delay
            size_factor = len(paths) * 0.005  # 5ms per file
            total_delay = base_delay + size_factor
            
            await asyncio.sleep(total_delay)
            
            # Create mock file contents
            results = {}
            for path in paths:
                results[path] = FileContent(
                    content=f"mock content for {path}",
                    sha=f"sha_{hash(path) % 1000000}",
                    size=len(path) * 10
                )
            
            processing_time = time.time() - start_time
            client._request_times.append(processing_time)
            client._concurrent_requests -= 1
            
            return results
        
        async def mock_get_repository(full_name):
            from datetime import datetime
            return Repository(
                name=full_name.split('/')[-1],
                full_name=full_name,
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            )
        
        async def mock_list_repository_files(repo, extensions=None):
            # Generate a realistic number of files
            base_files = [
                "package.json", "requirements.txt", "Gemfile.lock",
                "composer.lock", "go.mod", "Cargo.lock"
            ]
            
            # Add more files to simulate larger repositories
            additional_files = [
                f"src/module_{i}/package.json" for i in range(10)
            ] + [
                f"services/service_{i}/requirements.txt" for i in range(5)
            ] + [
                f"libs/lib_{i}/go.mod" for i in range(3)
            ]
            
            all_files = base_files + additional_files
            
            if extensions:
                all_files = [f for f in all_files if any(f.endswith(ext) for ext in extensions)]
            
            return all_files
        
        client.get_multiple_file_contents = mock_get_multiple_file_contents
        client.get_repository = mock_get_repository
        client.list_repository_files = mock_list_repository_files
        
        return client

    @pytest.fixture
    def load_test_config(self):
        """Create configuration optimized for load testing."""
        return BatchConfig(
            max_concurrent_requests=10,
            max_concurrent_repos=5,
            default_batch_size=15,
            max_batch_size=30,
            rate_limit_buffer=0.9,
            retry_attempts=2,
            max_memory_usage_mb=200,
            enable_performance_monitoring=True
        )

    @pytest.mark.asyncio
    async def test_high_volume_single_repository_load(
        self, scalable_mock_client, mock_cache_manager, load_test_config
    ):
        """
        Test high-volume batch processing for a single large repository.
        
        Requirements: 10.1, 10.2, 10.4
        """
        coordinator = BatchCoordinator(scalable_mock_client, mock_cache_manager, load_test_config)
        
        # Create a large repository simulation
        repo = await scalable_mock_client.get_repository("large-org/massive-repo")
        
        # Generate a large number of files
        large_file_list = []
        for i in range(500):  # 500 files
            file_type = ["package.json", "requirements.txt", "go.mod", "Cargo.lock"][i % 4]
            large_file_list.append(f"module_{i}/{file_type}")
        
        # Monitor system resources
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        initial_cpu_percent = process.cpu_percent()
        
        start_time = time.time()
        
        # Process large batch
        results = await coordinator.process_files_batch(
            repo,
            large_file_list,
            strategy=BatchStrategy.PARALLEL
        )
        
        processing_time = time.time() - start_time
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Verify results
        assert len(results) == len(large_file_list)
        assert all(isinstance(content, FileContent) for content in results.values())
        
        # Verify performance metrics
        throughput = len(large_file_list) / processing_time
        assert throughput > 10, f"Throughput too low: {throughput:.1f} files/sec"
        
        # Verify memory usage is reasonable
        assert memory_increase < load_test_config.max_memory_usage_mb * 1.5, (
            f"Memory usage too high: {memory_increase:.1f}MB"
        )
        
        # Get detailed metrics
        metrics = coordinator.get_batch_metrics()
        assert metrics.total_requests > 0
        assert metrics.successful_requests == len(large_file_list)
        
        print(f"High-volume load test results:")
        print(f"  Files processed: {len(large_file_list)}")
        print(f"  Processing time: {processing_time:.2f}s")
        print(f"  Throughput: {throughput:.1f} files/sec")
        print(f"  Memory increase: {memory_increase:.1f}MB")
        print(f"  API requests: {scalable_mock_client._request_count}")
        print(f"  Max concurrent: {scalable_mock_client._max_concurrent}")

    @pytest.mark.asyncio
    async def test_concurrent_batch_operations_stress(
        self, scalable_mock_client, mock_cache_manager, load_test_config
    ):
        """
        Test concurrent batch operations under stress conditions.
        
        Requirements: 10.1, 10.2, 10.4
        """
        coordinator = BatchCoordinator(scalable_mock_client, mock_cache_manager, load_test_config)
        
        # Create multiple repositories
        repos = []
        for i in range(10):
            repo = await scalable_mock_client.get_repository(f"org/repo-{i}")
            repos.append(repo)
        
        # Create concurrent batch operations
        concurrent_operations = 20
        files_per_operation = 50
        
        async def single_batch_operation(operation_id):
            """Single batch operation for stress testing."""
            repo = repos[operation_id % len(repos)]
            files = [f"file_{operation_id}_{i}.json" for i in range(files_per_operation)]
            
            start_time = time.time()
            results = await coordinator.process_files_batch(repo, files)
            processing_time = time.time() - start_time
            
            return {
                'operation_id': operation_id,
                'files_processed': len(results),
                'processing_time': processing_time,
                'success': len(results) == len(files)
            }
        
        # Monitor system resources
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        
        # Run concurrent operations
        tasks = [
            single_batch_operation(i) 
            for i in range(concurrent_operations)
        ]
        
        operation_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Analyze results
        successful_operations = [
            r for r in operation_results 
            if isinstance(r, dict) and r.get('success', False)
        ]
        
        failed_operations = [
            r for r in operation_results 
            if not isinstance(r, dict) or not r.get('success', False)
        ]
        
        # Verify stress test results
        success_rate = len(successful_operations) / len(operation_results)
        assert success_rate > 0.8, f"Success rate too low: {success_rate:.1%}"
        
        total_files = sum(r['files_processed'] for r in successful_operations)
        overall_throughput = total_files / total_time
        
        # Verify reasonable performance under stress
        assert overall_throughput > 50, f"Throughput under stress too low: {overall_throughput:.1f} files/sec"
        
        print(f"Concurrent stress test results:")
        print(f"  Concurrent operations: {concurrent_operations}")
        print(f"  Successful operations: {len(successful_operations)}")
        print(f"  Failed operations: {len(failed_operations)}")
        print(f"  Success rate: {success_rate:.1%}")
        print(f"  Total files processed: {total_files}")
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Overall throughput: {overall_throughput:.1f} files/sec")
        print(f"  Memory increase: {memory_increase:.1f}MB")

    @pytest.mark.asyncio
    async def test_memory_constrained_batch_processing(
        self, scalable_mock_client, mock_cache_manager
    ):
        """
        Test batch processing under memory constraints.
        
        Requirements: 10.1, 10.2, 10.4
        """
        # Configure with strict memory limits
        constrained_config = BatchConfig(
            max_concurrent_requests=3,
            default_batch_size=5,
            max_batch_size=10,
            max_memory_usage_mb=50,  # Very strict limit
            stream_large_files_threshold=1024
        )
        
        coordinator = BatchCoordinator(scalable_mock_client, mock_cache_manager, constrained_config)
        
        # Create large file simulation
        async def mock_large_file_contents(repo, paths):
            # Simulate large files
            results = {}
            for path in paths:
                large_content = "x" * 10000  # 10KB per file
                results[path] = FileContent(
                    content=large_content,
                    sha=f"sha_{hash(path)}",
                    size=len(large_content)
                )
            return results
        
        scalable_mock_client.get_multiple_file_contents = mock_large_file_contents
        
        repo = await scalable_mock_client.get_repository("org/memory-test-repo")
        
        # Process many large files
        large_files = [f"large_file_{i}.json" for i in range(100)]
        
        # Monitor memory usage throughout processing
        process = psutil.Process(os.getpid())
        memory_samples = []
        
        async def memory_monitor():
            """Monitor memory usage during processing."""
            while True:
                memory_mb = process.memory_info().rss / 1024 / 1024
                memory_samples.append(memory_mb)
                await asyncio.sleep(0.1)
        
        # Start memory monitoring
        monitor_task = asyncio.create_task(memory_monitor())
        
        try:
            start_time = time.time()
            results = await coordinator.process_files_batch(repo, large_files)
            processing_time = time.time() - start_time
        finally:
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass
        
        # Analyze memory usage
        if memory_samples:
            initial_memory = memory_samples[0]
            peak_memory = max(memory_samples)
            final_memory = memory_samples[-1]
            memory_increase = peak_memory - initial_memory
        else:
            memory_increase = 0
        
        # Verify processing completed successfully
        assert len(results) == len(large_files)
        
        # Verify memory usage stayed within reasonable bounds
        # Allow some overhead but should not exceed limits dramatically
        assert memory_increase < constrained_config.max_memory_usage_mb * 2, (
            f"Memory usage exceeded limits: {memory_increase:.1f}MB"
        )
        
        print(f"Memory-constrained test results:")
        print(f"  Files processed: {len(large_files)}")
        print(f"  Processing time: {processing_time:.2f}s")
        print(f"  Memory increase: {memory_increase:.1f}MB")
        print(f"  Memory limit: {constrained_config.max_memory_usage_mb}MB")

    @pytest.mark.asyncio
    async def test_scalability_with_increasing_load(
        self, scalable_mock_client, mock_cache_manager, load_test_config
    ):
        """
        Test batch processing scalability with increasing load.
        
        Requirements: 10.1, 10.2, 10.4
        """
        coordinator = BatchCoordinator(scalable_mock_client, mock_cache_manager, load_test_config)
        
        # Test with increasing numbers of files
        file_counts = [10, 50, 100, 200, 500]
        scalability_results = {}
        
        for file_count in file_counts:
            # Reset client statistics
            scalable_mock_client._request_count = 0
            scalable_mock_client._request_times = []
            
            repo = await scalable_mock_client.get_repository(f"org/scale-test-{file_count}")
            files = [f"file_{i}.json" for i in range(file_count)]
            
            start_time = time.time()
            results = await coordinator.process_files_batch(repo, files)
            processing_time = time.time() - start_time
            
            throughput = len(results) / processing_time if processing_time > 0 else 0
            avg_request_time = (
                sum(scalable_mock_client._request_times) / len(scalable_mock_client._request_times)
                if scalable_mock_client._request_times else 0
            )
            
            scalability_results[file_count] = {
                'processing_time': processing_time,
                'throughput': throughput,
                'api_requests': scalable_mock_client._request_count,
                'avg_request_time': avg_request_time,
                'files_processed': len(results)
            }
            
            # Verify all files were processed
            assert len(results) == file_count

        # Analyze scalability
        print(f"Scalability test results:")
        print(f"{'Files':<8} {'Time':<8} {'Throughput':<12} {'API Calls':<10} {'Avg Req Time':<12}")
        print("-" * 60)
        
        for file_count, results in scalability_results.items():
            print(f"{file_count:<8} {results['processing_time']:<8.2f} "
                  f"{results['throughput']:<12.1f} {results['api_requests']:<10} "
                  f"{results['avg_request_time']:<12.3f}")
        
        # Verify throughput doesn't degrade significantly with scale
        small_throughput = scalability_results[file_counts[0]]['throughput']
        large_throughput = scalability_results[file_counts[-1]]['throughput']
        
        # Allow some degradation but not too much
        throughput_ratio = large_throughput / small_throughput if small_throughput > 0 else 1
        assert throughput_ratio > 0.3, (
            f"Throughput degraded too much with scale: {throughput_ratio:.2f}"
        )

    @pytest.mark.asyncio
    async def test_error_resilience_under_load(
        self, scalable_mock_client, mock_cache_manager, load_test_config
    ):
        """
        Test error resilience during high-load batch processing.
        
        Requirements: 10.1, 10.2, 10.4
        """
        coordinator = BatchCoordinator(scalable_mock_client, mock_cache_manager, load_test_config)
        
        # Inject failures into the mock client
        failure_rate = 0.1  # 10% failure rate
        call_count = 0
        
        original_get_multiple = scalable_mock_client.get_multiple_file_contents
        
        async def failing_get_multiple(repo, paths):
            nonlocal call_count
            call_count += 1
            
            # Simulate various types of failures
            if call_count % 10 == 0:  # 10% rate limit errors
                raise RateLimitError("Rate limit exceeded", reset_time=1)
            elif call_count % 15 == 0:  # ~7% network errors
                raise APIError("Network timeout")
            else:
                return await original_get_multiple(repo, paths)
        
        scalable_mock_client.get_multiple_file_contents = failing_get_multiple
        
        # Process large batch with failures
        repo = await scalable_mock_client.get_repository("org/error-test-repo")
        files = [f"file_{i}.json" for i in range(200)]
        
        start_time = time.time()
        results = await coordinator.process_files_batch(repo, files)
        processing_time = time.time() - start_time
        
        # Verify resilience
        success_rate = len([r for r in results.values() if r is not None]) / len(files)
        
        # Should handle most failures gracefully
        assert success_rate > 0.7, f"Success rate too low under load with errors: {success_rate:.1%}"
        
        # Get error metrics
        metrics = coordinator.get_batch_metrics()
        
        print(f"Error resilience test results:")
        print(f"  Files attempted: {len(files)}")
        print(f"  Files processed: {len([r for r in results.values() if r is not None])}")
        print(f"  Success rate: {success_rate:.1%}")
        print(f"  Processing time: {processing_time:.2f}s")
        print(f"  Total API calls: {call_count}")
        print(f"  Retry attempts: {metrics.total_requests - len(files) if metrics.total_requests > len(files) else 0}")

    @pytest.mark.asyncio
    async def test_resource_cleanup_under_load(
        self, scalable_mock_client, mock_cache_manager, load_test_config
    ):
        """
        Test proper resource cleanup during high-load processing.
        
        Requirements: 10.1, 10.2, 10.4
        """
        coordinator = BatchCoordinator(scalable_mock_client, mock_cache_manager, load_test_config)
        
        # Track resource usage over multiple batch operations
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Run multiple batch operations
        for batch_round in range(10):
            repo = await scalable_mock_client.get_repository(f"org/cleanup-test-{batch_round}")
            files = [f"batch_{batch_round}_file_{i}.json" for i in range(50)]
            
            results = await coordinator.process_files_batch(repo, files)
            
            # Verify batch completed
            assert len(results) == len(files)
            
            # Force garbage collection
            gc.collect()
            
            # Check memory usage
            current_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = current_memory - initial_memory
            
            # Memory should not grow unbounded
            assert memory_increase < 100, (
                f"Memory leak detected after batch {batch_round}: {memory_increase:.1f}MB increase"
            )
        
        # Final memory check
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        total_memory_increase = final_memory - initial_memory
        
        print(f"Resource cleanup test results:")
        print(f"  Batch rounds: 10")
        print(f"  Files per batch: 50")
        print(f"  Initial memory: {initial_memory:.1f}MB")
        print(f"  Final memory: {final_memory:.1f}MB")
        print(f"  Total memory increase: {total_memory_increase:.1f}MB")
        
        # Verify reasonable memory usage after all operations
        assert total_memory_increase < 150, (
            f"Excessive memory usage after load test: {total_memory_increase:.1f}MB"
        )

    @pytest.mark.asyncio
    async def test_batch_processing_performance_limits(
        self, scalable_mock_client, mock_cache_manager, load_test_config
    ):
        """
        Test batch processing at performance limits.
        
        Requirements: 10.1, 10.2, 10.4
        """
        # Push configuration to limits
        extreme_config = BatchConfig(
            max_concurrent_requests=50,  # Very high concurrency
            max_concurrent_repos=20,
            default_batch_size=100,      # Large batches
            max_batch_size=200,
            rate_limit_buffer=0.95,      # Aggressive rate limit usage
            max_memory_usage_mb=500
        )
        
        coordinator = BatchCoordinator(scalable_mock_client, mock_cache_manager, extreme_config)
        
        # Create extreme load scenario
        repos = []
        for i in range(20):
            repo = await scalable_mock_client.get_repository(f"extreme-org/repo-{i}")
            repos.append(repo)
        
        # Process multiple repositories simultaneously
        start_time = time.time()
        
        results = await coordinator.process_repositories_batch(
            repos,
            strategy=BatchStrategy.PARALLEL
        )
        
        processing_time = time.time() - start_time
        
        # Verify extreme load handling
        assert len(results) > 0
        successful_repos = len([r for r in results.values() if len(r) >= 0])
        success_rate = successful_repos / len(repos)
        
        # Should handle most repositories even under extreme load
        assert success_rate > 0.6, f"Success rate too low under extreme load: {success_rate:.1%}"
        
        # Calculate performance metrics
        total_files = sum(len(repo_results) for repo_results in results.values())
        throughput = total_files / processing_time if processing_time > 0 else 0
        
        print(f"Performance limits test results:")
        print(f"  Repositories: {len(repos)}")
        print(f"  Successful repositories: {successful_repos}")
        print(f"  Success rate: {success_rate:.1%}")
        print(f"  Total files processed: {total_files}")
        print(f"  Processing time: {processing_time:.2f}s")
        print(f"  Throughput: {throughput:.1f} files/sec")
        print(f"  Max concurrent requests: {scalable_mock_client._max_concurrent}")
        
        # Verify reasonable performance even at limits
        assert throughput > 20, f"Throughput too low at performance limits: {throughput:.1f} files/sec"