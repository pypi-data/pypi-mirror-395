"""Tests for BatchProgressMonitor."""

import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from src.github_ioc_scanner.batch_progress_monitor import (
    BatchProgressMonitor,
    ProgressSnapshot,
    ETACalculation
)
from src.github_ioc_scanner.batch_models import BatchMetrics, BatchResult, BatchRequest
from src.github_ioc_scanner.models import Repository, FileContent


class TestProgressSnapshot:
    """Test ProgressSnapshot functionality."""
    
    def test_progress_snapshot_initialization(self):
        """Test ProgressSnapshot initialization."""
        timestamp = datetime.now()
        snapshot = ProgressSnapshot(
            timestamp=timestamp,
            completed_operations=50,
            total_operations=100,
            success_count=45,
            failure_count=5,
            current_batch_size=10,
            processing_rate=5.0
        )
        
        assert snapshot.timestamp == timestamp
        assert snapshot.completed_operations == 50
        assert snapshot.total_operations == 100
        assert snapshot.success_count == 45
        assert snapshot.failure_count == 5
        assert snapshot.current_batch_size == 10
        assert snapshot.processing_rate == 5.0
    
    def test_completion_percentage(self):
        """Test completion percentage calculation."""
        snapshot = ProgressSnapshot(
            timestamp=datetime.now(),
            completed_operations=25,
            total_operations=100,
            success_count=20,
            failure_count=5,
            current_batch_size=5,
            processing_rate=2.5
        )
        
        assert snapshot.completion_percentage == 25.0
    
    def test_completion_percentage_zero_total(self):
        """Test completion percentage with zero total operations."""
        snapshot = ProgressSnapshot(
            timestamp=datetime.now(),
            completed_operations=0,
            total_operations=0,
            success_count=0,
            failure_count=0,
            current_batch_size=0,
            processing_rate=0.0
        )
        
        assert snapshot.completion_percentage == 0.0
    
    def test_success_rate(self):
        """Test success rate calculation."""
        snapshot = ProgressSnapshot(
            timestamp=datetime.now(),
            completed_operations=20,
            total_operations=100,
            success_count=18,
            failure_count=2,
            current_batch_size=5,
            processing_rate=2.0
        )
        
        assert snapshot.success_rate == 90.0
    
    def test_success_rate_zero_completed(self):
        """Test success rate with zero completed operations."""
        snapshot = ProgressSnapshot(
            timestamp=datetime.now(),
            completed_operations=0,
            total_operations=100,
            success_count=0,
            failure_count=0,
            current_batch_size=0,
            processing_rate=0.0
        )
        
        assert snapshot.success_rate == 0.0


class TestETACalculation:
    """Test ETACalculation functionality."""
    
    def test_eta_calculation_initialization(self):
        """Test ETACalculation initialization."""
        completion_time = datetime.now() + timedelta(minutes=30)
        eta = ETACalculation(
            estimated_seconds_remaining=1800.0,
            estimated_completion_time=completion_time,
            confidence_level=0.85,
            based_on_samples=10
        )
        
        assert eta.estimated_seconds_remaining == 1800.0
        assert eta.estimated_completion_time == completion_time
        assert eta.confidence_level == 0.85
        assert eta.based_on_samples == 10
    
    def test_estimated_time_remaining_str_seconds(self):
        """Test time remaining string for seconds."""
        eta = ETACalculation(
            estimated_seconds_remaining=45.0,
            estimated_completion_time=datetime.now(),
            confidence_level=0.8,
            based_on_samples=5
        )
        
        assert eta.estimated_time_remaining_str == "45s"
    
    def test_estimated_time_remaining_str_minutes(self):
        """Test time remaining string for minutes."""
        eta = ETACalculation(
            estimated_seconds_remaining=150.0,  # 2m 30s
            estimated_completion_time=datetime.now(),
            confidence_level=0.8,
            based_on_samples=5
        )
        
        assert eta.estimated_time_remaining_str == "2m 30s"
    
    def test_estimated_time_remaining_str_hours(self):
        """Test time remaining string for hours."""
        eta = ETACalculation(
            estimated_seconds_remaining=7320.0,  # 2h 2m
            estimated_completion_time=datetime.now(),
            confidence_level=0.8,
            based_on_samples=5
        )
        
        assert eta.estimated_time_remaining_str == "2h 2m"
    
    def test_estimated_time_remaining_str_complete(self):
        """Test time remaining string when complete."""
        eta = ETACalculation(
            estimated_seconds_remaining=0.0,
            estimated_completion_time=datetime.now(),
            confidence_level=1.0,
            based_on_samples=10
        )
        
        assert eta.estimated_time_remaining_str == "Complete"


class TestBatchProgressMonitor:
    """Test BatchProgressMonitor functionality."""
    
    def test_initialization(self):
        """Test BatchProgressMonitor initialization."""
        monitor = BatchProgressMonitor()
        
        assert monitor.enable_verbose_logging is False
        assert monitor.progress_callback is None
        assert monitor.update_interval_seconds == 1.0
        assert monitor.start_time is None
        assert monitor.total_operations == 0
        assert monitor.completed_operations == 0
        assert len(monitor.progress_history) == 0
    
    def test_initialization_with_options(self):
        """Test initialization with custom options."""
        callback = MagicMock()
        monitor = BatchProgressMonitor(
            enable_verbose_logging=True,
            progress_callback=callback,
            update_interval_seconds=0.5
        )
        
        assert monitor.enable_verbose_logging is True
        assert monitor.progress_callback == callback
        assert monitor.update_interval_seconds == 0.5
    
    def test_start_monitoring(self):
        """Test starting monitoring."""
        monitor = BatchProgressMonitor()
        
        monitor.start_monitoring(100, "test_operation")
        
        assert monitor.start_time is not None
        assert monitor.total_operations == 100
        assert monitor.completed_operations == 0
        assert monitor.success_count == 0
        assert monitor.failure_count == 0
        assert monitor.current_operation_type == "test_operation"
        assert len(monitor.progress_history) == 0
    
    def test_update_progress(self):
        """Test updating progress."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)  # No delay for testing
        monitor.start_monitoring(100, "test_operation")
        
        snapshot = monitor.update_progress(
            completed=25,
            success_count=20,
            failure_count=5,
            current_batch_size=10
        )
        
        assert snapshot is not None
        assert snapshot.completed_operations == 25
        assert snapshot.success_count == 20
        assert snapshot.failure_count == 5
        assert snapshot.current_batch_size == 10
        assert snapshot.completion_percentage == 25.0
        assert len(monitor.progress_history) == 1
    
    def test_update_progress_too_soon(self):
        """Test that updates are throttled by interval."""
        monitor = BatchProgressMonitor(update_interval_seconds=1.0)
        monitor.start_monitoring(100, "test_operation")
        
        # First update should work
        snapshot1 = monitor.update_progress(10, 10, 0, 5)
        assert snapshot1 is not None
        
        # Second update immediately should be throttled
        snapshot2 = monitor.update_progress(15, 15, 0, 5)
        assert snapshot2 is None
    
    def test_update_progress_with_callback(self):
        """Test progress update with callback."""
        callback = MagicMock()
        monitor = BatchProgressMonitor(
            progress_callback=callback,
            update_interval_seconds=0.0
        )
        monitor.start_monitoring(100, "test_operation")
        
        snapshot = monitor.update_progress(25, 20, 5, 10)
        
        assert callback.called
        callback.assert_called_once_with(snapshot)
    
    def test_update_progress_callback_exception(self):
        """Test that callback exceptions don't break monitoring."""
        callback = MagicMock(side_effect=Exception("Callback error"))
        monitor = BatchProgressMonitor(
            progress_callback=callback,
            update_interval_seconds=0.0
        )
        monitor.start_monitoring(100, "test_operation")
        
        # Should not raise exception despite callback failure
        snapshot = monitor.update_progress(25, 20, 5, 10)
        assert snapshot is not None
    
    def test_record_batch_result_success(self):
        """Test recording successful batch result."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(100, "test_operation")
        
        # Create a successful result
        repo = Repository(name="test", full_name="test/repo", archived=False, default_branch="main", updated_at=datetime.now())
        request = BatchRequest(repo=repo, file_path="test.txt")
        content = FileContent(content="test", sha="abc123", size=4)
        result = BatchResult(request=request, content=content, from_cache=False, processing_time=1.0)
        
        monitor.record_batch_result(result)
        
        assert monitor.success_count == 1
        assert monitor.failure_count == 0
        assert monitor.completed_operations == 1
    
    def test_record_batch_result_failure(self):
        """Test recording failed batch result."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(100, "test_operation")
        
        # Create a failed result
        repo = Repository(name="test", full_name="test/repo", archived=False, default_branch="main", updated_at=datetime.now())
        request = BatchRequest(repo=repo, file_path="test.txt")
        result = BatchResult(request=request, error=Exception("Test error"), processing_time=1.0)
        
        monitor.record_batch_result(result)
        
        assert monitor.success_count == 0
        assert monitor.failure_count == 1
        assert monitor.completed_operations == 1
    
    def test_calculate_eta_insufficient_data(self):
        """Test ETA calculation with insufficient data."""
        monitor = BatchProgressMonitor()
        monitor.start_monitoring(100, "test_operation")
        
        eta = monitor.calculate_eta()
        assert eta is None
    
    def test_calculate_eta_completed(self):
        """Test ETA calculation when already completed."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(10, "test_operation")
        
        # Add some progress first
        monitor.update_progress(5, 5, 0, 5)
        
        # Complete all operations
        monitor.update_progress(10, 10, 0, 5)
        
        eta = monitor.calculate_eta()
        assert eta is not None
        assert eta.estimated_seconds_remaining == 0.0
        assert eta.confidence_level == 1.0
    
    def test_calculate_eta_with_progress(self):
        """Test ETA calculation with progress data."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(100, "test_operation")
        
        # Simulate progress over time
        with patch('src.github_ioc_scanner.batch_progress_monitor.datetime') as mock_datetime:
            base_time = datetime(2024, 1, 1, 12, 0, 0)
            
            # First progress update
            mock_datetime.now.return_value = base_time
            monitor.update_progress(10, 10, 0, 5)
            
            # Second progress update (10 seconds later, 10 more operations)
            mock_datetime.now.return_value = base_time + timedelta(seconds=10)
            monitor.update_progress(20, 20, 0, 5)
            
            # Calculate ETA
            mock_datetime.now.return_value = base_time + timedelta(seconds=10)
            eta = monitor.calculate_eta()
            
            assert eta is not None
            assert eta.estimated_seconds_remaining > 0
            assert 0.0 <= eta.confidence_level <= 1.0
            assert eta.based_on_samples == 2
    
    def test_get_current_status_not_started(self):
        """Test getting status when monitoring not started."""
        monitor = BatchProgressMonitor()
        
        status = monitor.get_current_status()
        
        assert status['status'] == 'not_started'
        assert 'message' in status
    
    def test_get_current_status_in_progress(self):
        """Test getting status during progress."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(100, "test_operation")
        monitor.update_progress(25, 20, 5, 10)
        
        status = monitor.get_current_status()
        
        assert status['status'] == 'in_progress'
        assert status['operation_type'] == 'test_operation'
        assert status['total_operations'] == 100
        assert status['completed_operations'] == 25
        assert status['success_count'] == 20
        assert status['failure_count'] == 5
        assert status['completion_percentage'] == 25.0
        assert status['success_rate'] == 80.0
        assert status['current_batch_size'] == 10
        assert 'elapsed_seconds' in status
        assert 'processing_rate' in status
    
    def test_get_current_status_completed(self):
        """Test getting status when completed."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(10, "test_operation")
        monitor.update_progress(10, 10, 0, 5)
        
        status = monitor.get_current_status()
        
        assert status['status'] == 'completed'
        assert status['completion_percentage'] == 100.0
    
    def test_get_current_status_with_eta(self):
        """Test getting status with ETA information."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(100, "test_operation")
        
        # Add enough progress history for ETA calculation
        with patch('src.github_ioc_scanner.batch_progress_monitor.datetime') as mock_datetime:
            base_time = datetime(2024, 1, 1, 12, 0, 0)
            
            mock_datetime.now.return_value = base_time
            monitor.update_progress(10, 10, 0, 5)
            
            mock_datetime.now.return_value = base_time + timedelta(seconds=10)
            monitor.update_progress(20, 20, 0, 5)
            
            mock_datetime.now.return_value = base_time + timedelta(seconds=10)
            status = monitor.get_current_status()
            
            assert 'eta_seconds_remaining' in status
            assert 'eta_completion_time' in status
            assert 'eta_time_remaining_str' in status
            assert 'eta_confidence' in status
    
    def test_log_batch_progress(self):
        """Test logging batch progress."""
        monitor = BatchProgressMonitor(enable_verbose_logging=True)
        
        # Should not raise any exceptions
        monitor.log_batch_progress(25, 100, 10, 120.0)
        monitor.log_batch_progress(50, 100, 15)  # Without ETA
    
    def test_finish_monitoring_not_started(self):
        """Test finishing monitoring when not started."""
        monitor = BatchProgressMonitor()
        
        stats = monitor.finish_monitoring()
        
        assert 'error' in stats
    
    def test_finish_monitoring_with_data(self):
        """Test finishing monitoring with recorded data."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(100, "test_operation")
        monitor.update_progress(75, 70, 5, 10)
        
        stats = monitor.finish_monitoring()
        
        assert stats['operation_type'] == 'test_operation'
        assert stats['total_operations'] == 100
        assert stats['completed_operations'] == 75
        assert stats['success_count'] == 70
        assert stats['failure_count'] == 5
        assert stats['success_rate'] == (70/75) * 100
        assert stats['completion_percentage'] == 75.0
        assert 'total_duration_seconds' in stats
        assert 'average_operations_per_second' in stats
    
    def test_alert_on_performance_issues_low_success_rate(self):
        """Test performance alerts for low success rate."""
        monitor = BatchProgressMonitor()
        
        metrics = BatchMetrics(
            total_requests=100,
            successful_requests=60,  # 60% success rate
            failed_requests=40,
            cache_hits=50,
            cache_misses=50
        )
        
        alerts = monitor.alert_on_performance_issues(metrics)
        
        assert len(alerts) > 0
        assert any("success rate" in alert.lower() for alert in alerts)
    
    def test_alert_on_performance_issues_slow_processing(self):
        """Test performance alerts for slow processing."""
        monitor = BatchProgressMonitor()
        
        # Create metrics with a specific duration
        from datetime import datetime, timedelta
        start_time = datetime(2024, 1, 1, 12, 0, 0)
        end_time = start_time + timedelta(seconds=20)  # 20 seconds duration
        
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=10,
            failed_requests=0,
            cache_hits=5,
            cache_misses=5,
            total_processing_time=20.0,
            start_time=start_time,
            end_time=end_time
        )
        
        alerts = monitor.alert_on_performance_issues(metrics)
        
        assert len(alerts) > 0
        assert any("slow processing" in alert.lower() for alert in alerts)
    
    def test_alert_on_performance_issues_low_cache_hit_rate(self):
        """Test performance alerts for low cache hit rate."""
        monitor = BatchProgressMonitor()
        
        metrics = BatchMetrics(
            total_requests=100,
            successful_requests=100,
            failed_requests=0,
            cache_hits=10,  # 10% cache hit rate
            cache_misses=90
        )
        
        alerts = monitor.alert_on_performance_issues(metrics)
        
        assert len(alerts) > 0
        assert any("cache hit rate" in alert.lower() for alert in alerts)
    
    def test_alert_on_performance_issues_stalled_progress(self):
        """Test performance alerts for stalled progress."""
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(100, "test_operation")
        
        # Add several snapshots with no progress
        for _ in range(5):
            monitor.update_progress(10, 10, 0, 5)  # Same progress each time
        
        metrics = BatchMetrics()
        alerts = monitor.alert_on_performance_issues(metrics)
        
        assert len(alerts) > 0
        assert any("stalled" in alert.lower() for alert in alerts)
    
    def test_alert_on_performance_issues_good_performance(self):
        """Test no alerts for good performance."""
        monitor = BatchProgressMonitor()
        
        metrics = BatchMetrics(
            total_requests=100,
            successful_requests=95,  # 95% success rate
            failed_requests=5,
            cache_hits=80,  # 80% cache hit rate
            cache_misses=20,
            total_processing_time=10.0  # 10 ops/sec
        )
        metrics.finish()
        
        alerts = monitor.alert_on_performance_issues(metrics)
        
        # Should have no alerts for good performance
        assert len(alerts) == 0
    
    def test_confidence_calculation_insufficient_data(self):
        """Test confidence calculation with insufficient data."""
        monitor = BatchProgressMonitor()
        
        # Test with empty history
        confidence = monitor._calculate_confidence([])
        assert confidence == 0.5
        
        # Test with single snapshot
        snapshot = ProgressSnapshot(
            timestamp=datetime.now(),
            completed_operations=10,
            total_operations=100,
            success_count=10,
            failure_count=0,
            current_batch_size=5,
            processing_rate=1.0
        )
        confidence = monitor._calculate_confidence([snapshot])
        assert confidence == 0.5
    
    def test_confidence_calculation_consistent_rates(self):
        """Test confidence calculation with consistent processing rates."""
        monitor = BatchProgressMonitor()
        
        # Create snapshots with consistent processing rates
        base_time = datetime(2024, 1, 1, 12, 0, 0)
        snapshots = []
        
        for i in range(5):
            snapshot = ProgressSnapshot(
                timestamp=base_time + timedelta(seconds=i*10),
                completed_operations=i*10,  # Consistent 1 op/sec rate
                total_operations=100,
                success_count=i*10,
                failure_count=0,
                current_batch_size=5,
                processing_rate=1.0
            )
            snapshots.append(snapshot)
        
        confidence = monitor._calculate_confidence(snapshots)
        assert confidence > 0.8  # Should have high confidence for consistent rates
    
    def test_confidence_calculation_variable_rates(self):
        """Test confidence calculation with variable processing rates."""
        monitor = BatchProgressMonitor()
        
        # Create snapshots with highly variable processing rates
        base_time = datetime(2024, 1, 1, 12, 0, 0)
        snapshots = []
        operations = [0, 5, 6, 20, 22]  # Highly variable progress
        
        for i, ops in enumerate(operations):
            snapshot = ProgressSnapshot(
                timestamp=base_time + timedelta(seconds=i*10),
                completed_operations=ops,
                total_operations=100,
                success_count=ops,
                failure_count=0,
                current_batch_size=5,
                processing_rate=1.0
            )
            snapshots.append(snapshot)
        
        confidence = monitor._calculate_confidence(snapshots)
        assert confidence < 0.7  # Should have lower confidence for variable rates
    
    @pytest.mark.asyncio
    async def test_concurrent_progress_updates(self):
        """Test that progress updates work correctly with concurrent access."""
        import asyncio
        
        monitor = BatchProgressMonitor(update_interval_seconds=0.0)
        monitor.start_monitoring(100, "test_operation")
        
        async def update_progress(completed: int):
            monitor.update_progress(completed, completed, 0, 5)
        
        # Update progress concurrently
        tasks = [update_progress(i*10) for i in range(1, 6)]
        await asyncio.gather(*tasks)
        
        # Should have recorded the updates
        assert len(monitor.progress_history) > 0
        assert monitor.completed_operations > 0