"""Tests for BatchMetricsCollector."""

import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import patch

from src.github_ioc_scanner.batch_metrics_collector import (
    BatchMetricsCollector,
    OperationMetrics,
    PerformanceTrend
)
from src.github_ioc_scanner.batch_models import BatchMetrics, BatchStrategy


class TestOperationMetrics:
    """Test OperationMetrics functionality."""
    
    def test_operation_metrics_initialization(self):
        """Test OperationMetrics initialization."""
        metrics = OperationMetrics("test_operation")
        
        assert metrics.operation_type == "test_operation"
        assert metrics.total_operations == 0
        assert metrics.success_rate == 0.0
        assert metrics.average_duration == 0.0
        assert metrics.average_batch_size == 0.0
        assert metrics.cache_hit_rate == 0.0
    
    def test_success_rate_calculation(self):
        """Test success rate calculation."""
        metrics = OperationMetrics("test")
        metrics.total_operations = 10
        metrics.success_count = 8
        
        assert metrics.success_rate == 80.0
    
    def test_average_duration_calculation(self):
        """Test average duration calculation."""
        metrics = OperationMetrics("test")
        metrics.durations = [1.0, 2.0, 3.0]
        
        assert metrics.average_duration == 2.0
    
    def test_average_batch_size_calculation(self):
        """Test average batch size calculation."""
        metrics = OperationMetrics("test")
        metrics.batch_sizes = [5, 10, 15]
        
        assert metrics.average_batch_size == 10.0
    
    def test_cache_hit_rate_calculation(self):
        """Test cache hit rate calculation."""
        metrics = OperationMetrics("test")
        metrics.total_operations = 20
        metrics.cache_hits = 15
        
        assert metrics.cache_hit_rate == 75.0


class TestPerformanceTrend:
    """Test PerformanceTrend functionality."""
    
    def test_performance_trend_initialization(self):
        """Test PerformanceTrend initialization."""
        trend = PerformanceTrend(window_size=50)
        
        assert trend.window_size == 50
        assert len(trend.timestamps) == 0
        assert len(trend.durations) == 0
        assert len(trend.success_rates) == 0
    
    def test_add_measurement(self):
        """Test adding measurements to trend."""
        trend = PerformanceTrend()
        
        trend.add_measurement(1.5, 95.0)
        
        assert len(trend.durations) == 1
        assert len(trend.success_rates) == 1
        assert trend.durations[0] == 1.5
        assert trend.success_rates[0] == 95.0
    
    def test_is_improving_insufficient_data(self):
        """Test is_improving with insufficient data."""
        trend = PerformanceTrend()
        
        # Add less than 10 measurements
        for i in range(5):
            trend.add_measurement(1.0, 90.0)
        
        assert not trend.is_improving
    
    def test_is_improving_performance_getting_better(self):
        """Test is_improving when performance is getting better."""
        trend = PerformanceTrend()
        
        # Add measurements with improving performance (decreasing duration)
        for i in range(10):
            duration = 2.0 - (i * 0.1)  # Decreasing from 2.0 to 1.1
            trend.add_measurement(duration, 90.0)
        
        assert trend.is_improving
    
    def test_is_improving_performance_getting_worse(self):
        """Test is_improving when performance is getting worse."""
        trend = PerformanceTrend()
        
        # Add measurements with degrading performance (increasing duration)
        for i in range(10):
            duration = 1.0 + (i * 0.1)  # Increasing from 1.0 to 1.9
            trend.add_measurement(duration, 90.0)
        
        assert not trend.is_improving


class TestBatchMetricsCollector:
    """Test BatchMetricsCollector functionality."""
    
    def test_initialization(self):
        """Test BatchMetricsCollector initialization."""
        collector = BatchMetricsCollector()
        
        assert collector.enable_detailed_tracking is True
        assert collector.total_operations == 0
        assert collector.total_cache_hits == 0
        assert collector.total_processing_time == 0.0
        assert len(collector.operation_metrics) == 0
        assert len(collector.strategy_performance) == len(BatchStrategy)
    
    def test_initialization_without_detailed_tracking(self):
        """Test initialization without detailed tracking."""
        collector = BatchMetricsCollector(enable_detailed_tracking=False)
        
        assert collector.enable_detailed_tracking is False
    
    def test_record_batch_operation(self):
        """Test recording a batch operation."""
        collector = BatchMetricsCollector()
        
        collector.record_batch_operation(
            operation_type="test_batch",
            duration=2.5,
            batch_size=10,
            success_count=8,
            total_count=10,
            cache_hits=3,
            strategy=BatchStrategy.PARALLEL
        )
        
        assert collector.total_operations == 1
        assert collector.total_processing_time == 2.5
        assert collector.total_cache_hits == 3
        
        # Check operation metrics
        op_metrics = collector.operation_metrics["test_batch"]
        assert op_metrics.total_operations == 1
        assert op_metrics.success_count == 8
        assert op_metrics.failure_count == 2
        assert op_metrics.cache_hits == 3
        assert op_metrics.batch_sizes == [10]
        assert op_metrics.durations == [2.5]
        
        # Check strategy metrics
        strategy_metrics = collector.strategy_performance[BatchStrategy.PARALLEL]
        assert strategy_metrics.total_operations == 1
        assert strategy_metrics.success_count == 8
        assert strategy_metrics.failure_count == 2
    
    def test_record_batch_operation_without_strategy(self):
        """Test recording batch operation without strategy."""
        collector = BatchMetricsCollector()
        
        collector.record_batch_operation(
            operation_type="test_batch",
            duration=1.0,
            batch_size=5,
            success_count=5,
            total_count=5
        )
        
        assert collector.total_operations == 1
        
        # Strategy metrics should not be updated
        for strategy_metrics in collector.strategy_performance.values():
            assert strategy_metrics.total_operations == 0
    
    def test_record_batch_metrics(self):
        """Test recording BatchMetrics object."""
        collector = BatchMetricsCollector()
        
        metrics = BatchMetrics(
            total_requests=15,
            successful_requests=12,
            failed_requests=3,
            cache_hits=8,
            cache_misses=7,
            average_batch_size=7.5,
            total_processing_time=3.0
        )
        metrics.finish()
        
        collector.record_batch_metrics(metrics)
        
        assert collector.total_operations == 1
        assert collector.total_cache_hits == 8
        
        op_metrics = collector.operation_metrics["batch_operation"]
        assert op_metrics.success_count == 12
        assert op_metrics.failure_count == 3
    
    def test_get_performance_summary_empty(self):
        """Test performance summary with no operations."""
        collector = BatchMetricsCollector()
        
        summary = collector.get_performance_summary()
        
        assert summary['total_operations'] == 0
        assert summary['operations_per_second'] == 0
        assert summary['average_operation_time'] == 0
        assert summary['cache_efficiency'] == 0
        assert len(summary['operation_metrics']) == 0
        assert len(summary['strategy_performance']) == 0
    
    def test_get_performance_summary_with_data(self):
        """Test performance summary with recorded operations."""
        collector = BatchMetricsCollector()
        
        # Record some operations
        collector.record_batch_operation("test1", 1.0, 5, 5, 5, 2, BatchStrategy.PARALLEL)
        collector.record_batch_operation("test2", 2.0, 10, 8, 10, 3, BatchStrategy.ADAPTIVE)
        
        summary = collector.get_performance_summary()
        
        assert summary['total_operations'] == 2
        assert summary['total_processing_time'] == 3.0
        assert summary['total_cache_hits'] == 5
        assert summary['average_operation_time'] == 1.5
        assert summary['cache_efficiency'] == 250.0  # 5 hits / 2 operations * 100
        
        # Check operation metrics
        assert 'test1' in summary['operation_metrics']
        assert 'test2' in summary['operation_metrics']
        
        # Check strategy performance
        assert 'parallel' in summary['strategy_performance']
        assert 'adaptive' in summary['strategy_performance']
    
    def test_get_efficiency_metrics_empty(self):
        """Test efficiency metrics with no operations."""
        collector = BatchMetricsCollector()
        
        efficiency = collector.get_efficiency_metrics()
        
        assert efficiency['overall_efficiency'] == 0.0
        assert efficiency['cache_efficiency'] == 0.0
        assert efficiency['time_efficiency'] == 0.0
        assert efficiency['batch_efficiency'] == 0.0
    
    def test_get_efficiency_metrics_with_data(self):
        """Test efficiency metrics with recorded operations."""
        collector = BatchMetricsCollector()
        
        # Record operations with good performance
        collector.record_batch_operation("test", 0.5, 10, 10, 10, 8)
        collector.record_batch_operation("test", 0.3, 8, 7, 8, 6)
        
        efficiency = collector.get_efficiency_metrics()
        
        assert efficiency['cache_efficiency'] == 700.0  # 14 hits / 2 operations * 100
        # 17 success / 18 total * 100 = 94.44% (10+7 success / 10+8 total)
        assert abs(efficiency['batch_efficiency'] - 94.44) < 0.1
        assert efficiency['time_efficiency'] > 0  # Should be positive
        assert efficiency['overall_efficiency'] > 0  # Should be positive
    
    def test_identify_optimization_opportunities_good_performance(self):
        """Test optimization recommendations with good performance."""
        collector = BatchMetricsCollector()
        
        # Record operations with good performance
        for _ in range(10):
            collector.record_batch_operation("test", 0.5, 10, 10, 10, 8)
        
        recommendations = collector.identify_optimization_opportunities()
        
        # Should have the "no optimizations needed" message
        assert any("Performance metrics look good" in rec for rec in recommendations)
    
    def test_identify_optimization_opportunities_low_cache_efficiency(self):
        """Test optimization recommendations with low cache efficiency."""
        collector = BatchMetricsCollector()
        
        # Record operations with low cache hits
        for _ in range(10):
            collector.record_batch_operation("test", 1.0, 10, 10, 10, 0)  # No cache hits
        
        recommendations = collector.identify_optimization_opportunities()
        
        # Should recommend cache improvements
        assert any("cache hit rate" in rec.lower() for rec in recommendations)
    
    def test_identify_optimization_opportunities_high_failure_rate(self):
        """Test optimization recommendations with high failure rate."""
        collector = BatchMetricsCollector()
        
        # Record operations with high failure rate
        for _ in range(10):
            collector.record_batch_operation("test", 1.0, 10, 5, 10, 5)  # 50% success rate
        
        recommendations = collector.identify_optimization_opportunities()
        
        # Should recommend error handling improvements
        assert any("failure rate" in rec.lower() for rec in recommendations)
    
    def test_identify_optimization_opportunities_slow_operations(self):
        """Test optimization recommendations with slow operations."""
        collector = BatchMetricsCollector()
        
        # Record slow operations
        for _ in range(5):
            collector.record_batch_operation("slow_test", 8.0, 10, 10, 10, 5)
        
        recommendations = collector.identify_optimization_opportunities()
        
        # Should recommend optimization for slow operations
        assert any("slow" in rec.lower() for rec in recommendations)
    
    def test_identify_optimization_opportunities_small_batch_sizes(self):
        """Test optimization recommendations with small batch sizes."""
        collector = BatchMetricsCollector()
        
        # Record operations with small batch sizes
        for _ in range(10):
            collector.record_batch_operation("test", 1.0, 2, 2, 2, 1)  # Small batches
        
        recommendations = collector.identify_optimization_opportunities()
        
        # Should recommend increasing batch sizes
        assert any("batch size is small" in rec.lower() for rec in recommendations)
    
    def test_identify_optimization_opportunities_large_batch_sizes(self):
        """Test optimization recommendations with large batch sizes."""
        collector = BatchMetricsCollector()
        
        # Record operations with large batch sizes
        for _ in range(10):
            collector.record_batch_operation("test", 1.0, 60, 60, 60, 30)  # Large batches
        
        recommendations = collector.identify_optimization_opportunities()
        
        # Should recommend reducing batch sizes
        assert any("batch size is large" in rec.lower() for rec in recommendations)
    
    def test_identify_optimization_opportunities_strategy_comparison(self):
        """Test optimization recommendations comparing strategies."""
        collector = BatchMetricsCollector()
        
        # Record operations with different strategy performance
        for _ in range(5):
            collector.record_batch_operation("test", 1.0, 10, 10, 10, 5, BatchStrategy.PARALLEL)
        for _ in range(5):
            collector.record_batch_operation("test", 3.0, 10, 10, 10, 5, BatchStrategy.SEQUENTIAL)
        
        recommendations = collector.identify_optimization_opportunities()
        
        # Should recommend using the better strategy
        assert any("parallel" in rec.lower() and "better" in rec.lower() for rec in recommendations)
    
    def test_get_recent_performance_empty(self):
        """Test recent performance with no operations."""
        collector = BatchMetricsCollector()
        
        recent = collector.get_recent_performance(minutes=10)
        
        assert recent['total_operations'] == 0
        assert recent['average_duration'] == 0.0
        assert recent['success_rate'] == 0.0
        assert recent['operations_per_minute'] == 0.0
    
    def test_get_recent_performance_with_data(self):
        """Test recent performance with recorded operations."""
        collector = BatchMetricsCollector(enable_detailed_tracking=True)
        
        # Mock datetime to control timestamps
        with patch('src.github_ioc_scanner.batch_metrics_collector.datetime') as mock_datetime:
            base_time = datetime(2024, 1, 1, 12, 0, 0)
            mock_datetime.now.return_value = base_time
            
            # Record some operations
            collector.record_batch_operation("test", 1.0, 10, 9, 10, 5)
            collector.record_batch_operation("test", 2.0, 8, 7, 8, 3)
            
            # Move time forward and get recent performance
            mock_datetime.now.return_value = base_time + timedelta(minutes=5)
            recent = collector.get_recent_performance(minutes=10)
            
            assert recent['total_operations'] == 2
            assert recent['average_duration'] == 1.5
            assert recent['success_rate'] == (16/18) * 100  # (9+7)/(10+8) * 100
            assert recent['operations_per_minute'] == 0.2  # 2 operations / 10 minutes
            assert recent['total_cache_hits'] == 8
    
    def test_get_recent_performance_old_data_excluded(self):
        """Test that old data is excluded from recent performance."""
        collector = BatchMetricsCollector(enable_detailed_tracking=True)
        
        with patch('src.github_ioc_scanner.batch_metrics_collector.datetime') as mock_datetime:
            base_time = datetime(2024, 1, 1, 12, 0, 0)
            
            # Record old operation
            mock_datetime.now.return_value = base_time
            collector.record_batch_operation("test", 1.0, 10, 10, 10, 5)
            
            # Record recent operation
            mock_datetime.now.return_value = base_time + timedelta(minutes=5)
            collector.record_batch_operation("test", 2.0, 8, 8, 8, 3)
            
            # Get recent performance (only last 3 minutes)
            mock_datetime.now.return_value = base_time + timedelta(minutes=6)
            recent = collector.get_recent_performance(minutes=3)
            
            # Should only include the recent operation
            assert recent['total_operations'] == 1
            assert recent['average_duration'] == 2.0
    
    def test_reset_metrics(self):
        """Test resetting all metrics."""
        collector = BatchMetricsCollector()
        
        # Record some operations
        collector.record_batch_operation("test", 1.0, 10, 10, 10, 5, BatchStrategy.PARALLEL)
        
        # Verify data exists
        assert collector.total_operations == 1
        assert len(collector.operation_metrics) == 1
        assert collector.strategy_performance[BatchStrategy.PARALLEL].total_operations == 1
        
        # Reset metrics
        collector.reset_metrics()
        
        # Verify everything is reset
        assert collector.total_operations == 0
        assert collector.total_cache_hits == 0
        assert collector.total_processing_time == 0.0
        assert len(collector.operation_metrics) == 0
        assert len(collector.recent_batches) == 0
        
        # Strategy performance should be reset but still exist
        assert len(collector.strategy_performance) == len(BatchStrategy)
        for strategy_metrics in collector.strategy_performance.values():
            assert strategy_metrics.total_operations == 0
    
    def test_performance_trends_tracking(self):
        """Test that performance trends are properly tracked."""
        collector = BatchMetricsCollector()
        
        # Record operations to build trend data
        for i in range(15):
            # Gradually improving performance (decreasing duration)
            duration = 2.0 - (i * 0.05)
            collector.record_batch_operation("test", duration, 10, 10, 10, 5)
        
        # Check that trend is tracked
        assert "test" in collector.performance_trends
        trend = collector.performance_trends["test"]
        assert len(trend.durations) == 15
        assert trend.is_improving  # Should detect improvement
    
    def test_detailed_tracking_disabled(self):
        """Test behavior when detailed tracking is disabled."""
        collector = BatchMetricsCollector(enable_detailed_tracking=False)
        
        collector.record_batch_operation("test", 1.0, 10, 10, 10, 5)
        
        # Basic metrics should still be tracked
        assert collector.total_operations == 1
        assert len(collector.operation_metrics) == 1
        
        # Recent batches should not be stored
        assert len(collector.recent_batches) == 0
    
    @pytest.mark.asyncio
    async def test_concurrent_metric_recording(self):
        """Test that metrics can be recorded concurrently."""
        import asyncio
        
        collector = BatchMetricsCollector()
        
        async def record_operation(op_id: int):
            collector.record_batch_operation(
                f"test_{op_id}",
                1.0,
                10,
                10,
                10,
                5
            )
        
        # Record operations concurrently
        tasks = [record_operation(i) for i in range(10)]
        await asyncio.gather(*tasks)
        
        # All operations should be recorded
        assert collector.total_operations == 10
        assert len(collector.operation_metrics) == 10