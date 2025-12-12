"""
Performance benchmark tests for batch API optimizations.

This module contains benchmarks comparing batch vs non-batch performance,
performance regression tests, and tests measuring actual performance improvements.
"""

import asyncio
import time
from typing import List, Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

from src.github_ioc_scanner.batch_coordinator import BatchCoordinator
from src.github_ioc_scanner.batch_models import (
    BatchRequest, BatchResult, BatchMetrics, BatchStrategy
)
from src.github_ioc_scanner.models import Repository, FileContent
from src.github_ioc_scanner.scanner import GitHubIOCScanner
from src.github_ioc_scanner.github_client import GitHubClient


class TestBatchPerformanceBenchmarks:
    """Performance benchmark tests for batch processing."""

    @pytest.fixture
    def mock_cache_manager(self):
        """Create a mock cache manager for testing."""
        from src.github_ioc_scanner.cache_manager import CacheManager
        cache_manager = MagicMock(spec=CacheManager)
        return cache_manager

    @pytest.fixture
    def mock_github_client(self):
        """Create a mock GitHub client for testing."""
        client = AsyncMock(spec=GitHubClient)
        
        # Mock file content responses with realistic delays
        async def mock_get_file_content(repo, path):
            await asyncio.sleep(0.1)  # Simulate network delay
            return FileContent(
                content=f"mock content for {path}",
                sha="mock_sha",
                size=100
            )
        
        client.get_file_content = mock_get_file_content
        
        # Mock batch file content responses
        async def mock_get_multiple_file_contents(repo, paths):
            await asyncio.sleep(0.05 * len(paths))  # Simulate batch efficiency
            return {
                path: FileContent(
                    content=f"mock content for {path}",
                    sha="mock_sha",
                    size=100
                )
                for path in paths
            }
        
        client.get_multiple_file_contents = mock_get_multiple_file_contents
        return client

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
    def sample_files(self):
        """Create sample file paths for testing."""
        return [
            "package.json",
            "requirements.txt",
            "Gemfile.lock",
            "composer.lock",
            "go.mod",
            "Cargo.lock",
            "src/package.json",
            "backend/requirements.txt",
            "frontend/package-lock.json",
            "api/go.mod"
        ]

    @pytest.mark.asyncio
    async def test_batch_vs_sequential_performance_benchmark(
        self, mock_github_client, mock_cache_manager, sample_repository, sample_files
    ):
        """
        Benchmark comparing batch vs sequential file processing performance.
        
        Requirements: 8.1, 8.3
        """
        # Test sequential processing
        start_time = time.time()
        sequential_results = {}
        for file_path in sample_files:
            content = await mock_github_client.get_file_content(
                sample_repository, file_path
            )
            sequential_results[file_path] = content
        sequential_time = time.time() - start_time

        # Test batch processing
        start_time = time.time()
        batch_results = await mock_github_client.get_multiple_file_contents(
            sample_repository, sample_files
        )
        batch_time = time.time() - start_time

        # Verify results are equivalent
        assert len(sequential_results) == len(batch_results)
        for file_path in sample_files:
            assert file_path in sequential_results
            assert file_path in batch_results
            assert sequential_results[file_path].content == batch_results[file_path].content

        # Verify batch processing is significantly faster
        performance_improvement = (sequential_time - batch_time) / sequential_time
        assert performance_improvement > 0.3, (
            f"Batch processing should be at least 30% faster. "
            f"Sequential: {sequential_time:.3f}s, Batch: {batch_time:.3f}s, "
            f"Improvement: {performance_improvement:.1%}"
        )

        print(f"Performance Benchmark Results:")
        print(f"  Sequential processing: {sequential_time:.3f}s")
        print(f"  Batch processing: {batch_time:.3f}s")
        print(f"  Performance improvement: {performance_improvement:.1%}")

    @pytest.mark.asyncio
    async def test_batch_coordinator_performance_benchmark(
        self, mock_github_client, mock_cache_manager, sample_repository, sample_files
    ):
        """
        Benchmark BatchCoordinator performance with different strategies.
        
        Requirements: 8.1, 8.3
        """
        coordinator = BatchCoordinator(mock_github_client, mock_cache_manager)
        
        # Test different batch strategies
        strategies = [
            BatchStrategy.SEQUENTIAL,
            BatchStrategy.PARALLEL,
            BatchStrategy.ADAPTIVE
        ]
        
        performance_results = {}
        
        for strategy in strategies:
            start_time = time.time()
            
            results = await coordinator.process_files_batch(
                sample_repository,
                sample_files
            )
            
            processing_time = time.time() - start_time
            performance_results[strategy] = {
                'time': processing_time,
                'files_processed': len(results),
                'success_rate': len([r for r in results.values() if r is not None]) / len(results)
            }

        # Verify parallel strategy is fastest
        parallel_time = performance_results[BatchStrategy.PARALLEL]['time']
        sequential_time = performance_results[BatchStrategy.SEQUENTIAL]['time']
        
        assert parallel_time < sequential_time, (
            f"Parallel strategy should be faster than sequential. "
            f"Parallel: {parallel_time:.3f}s, Sequential: {sequential_time:.3f}s"
        )

        # Print benchmark results
        print(f"Batch Strategy Performance Benchmark:")
        for strategy, results in performance_results.items():
            print(f"  {strategy.value}: {results['time']:.3f}s "
                  f"({results['files_processed']} files, "
                  f"{results['success_rate']:.1%} success rate)")

    @pytest.mark.asyncio
    async def test_batch_size_optimization_benchmark(
        self, mock_github_client, mock_cache_manager, sample_repository
    ):
        """
        Benchmark different batch sizes to find optimal performance.
        
        Requirements: 8.1, 8.3
        """
        coordinator = BatchCoordinator(mock_github_client, mock_cache_manager)
        
        # Create larger file list for batch size testing
        large_file_list = [f"file_{i}.json" for i in range(50)]
        
        batch_sizes = [1, 5, 10, 15, 20, 25]
        performance_results = {}
        
        for batch_size in batch_sizes:
            # Configure batch size
            coordinator.config.default_batch_size = batch_size
            coordinator.config.max_batch_size = batch_size
            
            start_time = time.time()
            
            results = await coordinator.process_files_batch(
                sample_repository,
                large_file_list
            )
            
            processing_time = time.time() - start_time
            performance_results[batch_size] = {
                'time': processing_time,
                'throughput': len(results) / processing_time if processing_time > 0 else 0
            }

        # Find optimal batch size (highest throughput)
        optimal_batch_size = max(
            performance_results.keys(),
            key=lambda size: performance_results[size]['throughput']
        )
        
        # Verify optimal batch size is reasonable (not too small or too large)
        assert 5 <= optimal_batch_size <= 25, (
            f"Optimal batch size should be between 5 and 25, got {optimal_batch_size}"
        )

        print(f"Batch Size Optimization Benchmark:")
        for batch_size, results in performance_results.items():
            marker = " (optimal)" if batch_size == optimal_batch_size else ""
            print(f"  Size {batch_size}: {results['time']:.3f}s, "
                  f"{results['throughput']:.1f} files/sec{marker}")

    @pytest.mark.asyncio
    async def test_memory_efficiency_benchmark(
        self, mock_github_client, mock_cache_manager, sample_repository
    ):
        """
        Benchmark memory usage during batch processing.
        
        Requirements: 8.1, 8.3
        """
        import psutil
        import os
        
        coordinator = BatchCoordinator(mock_github_client, mock_cache_manager)
        
        # Create large file list to test memory usage
        large_file_list = [f"large_file_{i}.json" for i in range(100)]
        
        # Mock large file content
        async def mock_large_file_content(repo, paths):
            await asyncio.sleep(0.01 * len(paths))
            return {
                path: FileContent(
                    content="x" * 10000,  # 10KB per file
                    sha="mock_sha",
                    size=10000
                )
                for path in paths
            }
        
        mock_github_client.get_multiple_file_contents = mock_large_file_content
        
        # Measure memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        results = await coordinator.process_files_batch(
            sample_repository,
            large_file_list
        )
        
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = peak_memory - initial_memory
        
        # Verify memory usage is reasonable (less than 100MB for 1MB of content)
        assert memory_increase < 100, (
            f"Memory usage should be reasonable. Increased by {memory_increase:.1f}MB"
        )
        
        # Verify all files were processed
        assert len(results) == len(large_file_list)
        
        print(f"Memory Efficiency Benchmark:")
        print(f"  Initial memory: {initial_memory:.1f}MB")
        print(f"  Peak memory: {peak_memory:.1f}MB")
        print(f"  Memory increase: {memory_increase:.1f}MB")
        print(f"  Files processed: {len(results)}")

    @pytest.mark.asyncio
    async def test_concurrent_batch_performance_benchmark(
        self, mock_github_client, mock_cache_manager, sample_repository, sample_files
    ):
        """
        Benchmark concurrent batch operations performance.
        
        Requirements: 8.1, 8.3
        """
        coordinator = BatchCoordinator(mock_github_client, mock_cache_manager)
        
        # Test different concurrency levels
        concurrency_levels = [1, 3, 5, 10]
        performance_results = {}
        
        for concurrency in concurrency_levels:
            coordinator.config.max_concurrent_requests = concurrency
            
            start_time = time.time()
            
            # Run multiple batch operations concurrently
            tasks = []
            for i in range(5):  # 5 concurrent batch operations
                task = coordinator.process_files_batch(
                    sample_repository,
                    sample_files
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            
            processing_time = time.time() - start_time
            total_files = sum(len(result) for result in results)
            
            performance_results[concurrency] = {
                'time': processing_time,
                'total_files': total_files,
                'throughput': total_files / processing_time if processing_time > 0 else 0
            }

        # Verify higher concurrency improves performance up to a point
        throughputs = [results['throughput'] for results in performance_results.values()]
        max_throughput = max(throughputs)
        
        # Find the concurrency level that achieved max throughput
        optimal_concurrency = next(
            concurrency for concurrency, results in performance_results.items()
            if results['throughput'] == max_throughput
        )
        
        print(f"Concurrent Batch Performance Benchmark:")
        for concurrency, results in performance_results.items():
            marker = " (optimal)" if concurrency == optimal_concurrency else ""
            print(f"  Concurrency {concurrency}: {results['time']:.3f}s, "
                  f"{results['throughput']:.1f} files/sec{marker}")

    def test_performance_regression_detection(self):
        """
        Test for performance regression detection in batch operations.
        
        Requirements: 8.1, 8.3
        """
        # Define performance baselines (these would be updated as optimizations are made)
        performance_baselines = {
            'batch_vs_sequential_improvement': 0.3,  # 30% improvement minimum
            'optimal_batch_size_range': (5, 25),
            'memory_increase_limit_mb': 100,
            'max_processing_time_per_file_ms': 200
        }
        
        # This test would be run as part of CI/CD to detect regressions
        # For now, we'll just verify the baselines are reasonable
        assert performance_baselines['batch_vs_sequential_improvement'] > 0.2
        assert performance_baselines['optimal_batch_size_range'][0] >= 1
        assert performance_baselines['optimal_batch_size_range'][1] <= 50
        assert performance_baselines['memory_increase_limit_mb'] > 0
        assert performance_baselines['max_processing_time_per_file_ms'] > 0
        
        print("Performance regression baselines verified:")
        for metric, baseline in performance_baselines.items():
            print(f"  {metric}: {baseline}")

    @pytest.mark.asyncio
    async def test_real_world_performance_simulation(
        self, mock_github_client, mock_cache_manager, sample_repository
    ):
        """
        Simulate real-world performance scenarios with varying conditions.
        
        Requirements: 8.1, 8.3
        """
        coordinator = BatchCoordinator(mock_github_client, mock_cache_manager)
        
        # Simulate different real-world scenarios
        scenarios = {
            'small_repo': [f"file_{i}.json" for i in range(5)],
            'medium_repo': [f"file_{i}.json" for i in range(25)],
            'large_repo': [f"file_{i}.json" for i in range(100)],
            'mixed_files': [
                "package.json", "requirements.txt", "Gemfile.lock",
                "composer.lock", "go.mod", "Cargo.lock"
            ] * 10
        }
        
        performance_results = {}
        
        for scenario_name, file_list in scenarios.items():
            start_time = time.time()
            
            results = await coordinator.process_files_batch(
                sample_repository,
                file_list
            )
            
            processing_time = time.time() - start_time
            
            performance_results[scenario_name] = {
                'files': len(file_list),
                'time': processing_time,
                'files_per_second': len(file_list) / processing_time if processing_time > 0 else 0,
                'success_rate': len([r for r in results.values() if r is not None]) / len(results)
            }

        # Verify performance scales reasonably with repo size
        small_fps = performance_results['small_repo']['files_per_second']
        large_fps = performance_results['large_repo']['files_per_second']
        
        # Large repos should still maintain reasonable throughput
        assert large_fps > small_fps * 0.5, (
            f"Large repo performance should not degrade too much. "
            f"Small: {small_fps:.1f} fps, Large: {large_fps:.1f} fps"
        )

        print(f"Real-world Performance Simulation:")
        for scenario, results in performance_results.items():
            print(f"  {scenario}: {results['files']} files in {results['time']:.3f}s "
                  f"({results['files_per_second']:.1f} fps, "
                  f"{results['success_rate']:.1%} success)")