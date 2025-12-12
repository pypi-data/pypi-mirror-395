"""Tests for memory monitoring and batch size adjustment."""

import gc
import pytest
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass

from src.github_ioc_scanner.memory_monitor import MemoryMonitor, MemoryStats


@dataclass
class MockMemoryInfo:
    """Mock memory info for testing."""
    rss: int


@dataclass
class MockVirtualMemory:
    """Mock virtual memory for testing."""
    total: int
    available: int
    used: int
    percent: float


class TestMemoryMonitor:
    """Test memory monitoring functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.monitor = MemoryMonitor(
            max_memory_threshold=0.8,
            critical_memory_threshold=0.9,
            min_batch_size=1,
            max_batch_size=50
        )
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_get_memory_stats_success(self, mock_process_class, mock_virtual_memory):
        """Test successful memory stats retrieval."""
        # Mock system memory
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,  # 8GB
            available=4 * 1024 * 1024 * 1024,  # 4GB
            used=4 * 1024 * 1024 * 1024,  # 4GB
            percent=50.0
        )
        
        # Mock process memory
        mock_process = Mock()
        mock_process.memory_info.return_value = MockMemoryInfo(
            rss=100 * 1024 * 1024  # 100MB
        )
        mock_process_class.return_value = mock_process
        
        # Ensure process is None so it gets initialized with mock
        self.monitor._process = None
        
        stats = self.monitor.get_memory_stats()
        
        assert stats.total_mb == 8192.0
        assert stats.available_mb == 4096.0
        assert stats.used_mb == 4096.0
        assert stats.percent_used == 0.5
        assert stats.process_mb == 100.0
        assert abs(stats.process_percent - 0.01220703125) < 0.001  # 100MB / 8GB
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_get_memory_stats_exception_handling(self, mock_process_class, mock_virtual_memory):
        """Test memory stats with exception handling."""
        # Mock exception
        mock_virtual_memory.side_effect = Exception("Memory access failed")
        
        stats = self.monitor.get_memory_stats()
        
        # Should return safe defaults
        assert stats.total_mb == 8192.0
        assert stats.available_mb == 4096.0
        assert stats.used_mb == 4096.0
        assert stats.percent_used == 0.5
        assert stats.process_mb == 100.0
        assert stats.process_percent == 0.01
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_set_baseline_memory(self, mock_process_class, mock_virtual_memory):
        """Test setting baseline memory."""
        # Mock memory info
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=4 * 1024 * 1024 * 1024,
            used=4 * 1024 * 1024 * 1024,
            percent=50.0
        )
        
        mock_process = Mock()
        mock_process.memory_info.return_value = MockMemoryInfo(rss=100 * 1024 * 1024)
        mock_process_class.return_value = mock_process
        
        # Ensure process is None so it gets initialized with mock
        self.monitor._process = None
        
        # Set baseline
        self.monitor.set_baseline_memory()
        
        # Check baseline was set
        assert self.monitor._baseline_memory == 100.0
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_get_memory_growth(self, mock_process_class, mock_virtual_memory):
        """Test memory growth calculation."""
        # Mock initial memory
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=4 * 1024 * 1024 * 1024,
            used=4 * 1024 * 1024 * 1024,
            percent=50.0
        )
        
        mock_process = Mock()
        mock_process_class.return_value = mock_process
        
        # Ensure process is None so it gets initialized with mock
        self.monitor._process = None
        
        # Set baseline at 100MB
        mock_process.memory_info.return_value = MockMemoryInfo(rss=100 * 1024 * 1024)
        self.monitor.set_baseline_memory()
        
        # Increase memory to 200MB
        mock_process.memory_info.return_value = MockMemoryInfo(rss=200 * 1024 * 1024)
        
        growth = self.monitor.get_memory_growth()
        assert growth == 100.0  # 100MB growth
    
    def test_get_memory_growth_no_baseline(self):
        """Test memory growth when no baseline is set."""
        growth = self.monitor.get_memory_growth()
        assert growth == 0.0
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_should_reduce_batch_size_high_system_memory(self, mock_process_class, mock_virtual_memory):
        """Test batch size reduction due to high system memory usage."""
        # Mock high system memory usage (85%)
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=1 * 1024 * 1024 * 1024,
            used=7 * 1024 * 1024 * 1024,
            percent=85.0
        )
        
        mock_process = Mock()
        mock_process.memory_info.return_value = MockMemoryInfo(rss=100 * 1024 * 1024)
        mock_process_class.return_value = mock_process
        
        assert self.monitor.should_reduce_batch_size() is True
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_should_reduce_batch_size_high_process_growth(self, mock_process_class, mock_virtual_memory):
        """Test batch size reduction due to high process memory growth."""
        # Mock normal system memory
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=4 * 1024 * 1024 * 1024,
            used=4 * 1024 * 1024 * 1024,
            percent=50.0
        )
        
        mock_process = Mock()
        mock_process_class.return_value = mock_process
        
        # Ensure process is None so it gets initialized with mock
        self.monitor._process = None
        
        # Set baseline at 100MB
        mock_process.memory_info.return_value = MockMemoryInfo(rss=100 * 1024 * 1024)
        self.monitor.set_baseline_memory()
        
        # Increase memory to 700MB (600MB growth)
        mock_process.memory_info.return_value = MockMemoryInfo(rss=700 * 1024 * 1024)
        
        assert self.monitor.should_reduce_batch_size() is True
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_should_reduce_batch_size_normal_conditions(self, mock_process_class, mock_virtual_memory):
        """Test no batch size reduction under normal conditions."""
        # Mock normal system memory (50%)
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=4 * 1024 * 1024 * 1024,
            used=4 * 1024 * 1024 * 1024,
            percent=50.0
        )
        
        mock_process = Mock()
        mock_process.memory_info.return_value = MockMemoryInfo(rss=100 * 1024 * 1024)
        mock_process_class.return_value = mock_process
        
        assert self.monitor.should_reduce_batch_size() is False
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_is_critical_memory_pressure(self, mock_process_class, mock_virtual_memory):
        """Test critical memory pressure detection."""
        # Mock critical system memory usage (95%)
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=0.4 * 1024 * 1024 * 1024,
            used=7.6 * 1024 * 1024 * 1024,
            percent=95.0
        )
        
        mock_process = Mock()
        mock_process.memory_info.return_value = MockMemoryInfo(rss=100 * 1024 * 1024)
        mock_process_class.return_value = mock_process
        
        assert self.monitor.is_critical_memory_pressure() is True
    
    def test_calculate_adjusted_batch_size_normal_pressure(self):
        """Test batch size calculation under normal memory pressure."""
        # Normal pressure (50%)
        adjusted_size = self.monitor.calculate_adjusted_batch_size(20, 0.5)
        assert adjusted_size == 20  # No reduction
    
    def test_calculate_adjusted_batch_size_high_pressure(self):
        """Test batch size calculation under high memory pressure."""
        # High pressure (85%)
        adjusted_size = self.monitor.calculate_adjusted_batch_size(20, 0.85)
        assert adjusted_size < 20  # Should be reduced
        assert adjusted_size >= self.monitor.min_batch_size
    
    def test_calculate_adjusted_batch_size_critical_pressure(self):
        """Test batch size calculation under critical memory pressure."""
        # Critical pressure (95%)
        adjusted_size = self.monitor.calculate_adjusted_batch_size(20, 0.95)
        assert adjusted_size == 2  # Should be reduced to near minimum (20 * 0.1 = 2)
    
    def test_calculate_adjusted_batch_size_bounds(self):
        """Test batch size calculation respects bounds."""
        # Test minimum bound
        adjusted_size = self.monitor.calculate_adjusted_batch_size(1, 0.95)
        assert adjusted_size >= self.monitor.min_batch_size
        
        # Test maximum bound
        adjusted_size = self.monitor.calculate_adjusted_batch_size(100, 0.1)
        assert adjusted_size <= self.monitor.max_batch_size
    
    @patch('src.github_ioc_scanner.memory_monitor.gc.collect')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_force_garbage_collection(self, mock_process_class, mock_virtual_memory, mock_gc_collect):
        """Test forced garbage collection."""
        # Mock memory before and after GC
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=4 * 1024 * 1024 * 1024,
            used=4 * 1024 * 1024 * 1024,
            percent=50.0
        )
        
        mock_process = Mock()
        mock_process_class.return_value = mock_process
        
        # Ensure process is None so it gets initialized with mock
        self.monitor._process = None
        
        # Memory before GC: 200MB, after GC: 150MB
        mock_process.memory_info.side_effect = [
            MockMemoryInfo(rss=200 * 1024 * 1024),  # Before GC
            MockMemoryInfo(rss=150 * 1024 * 1024)   # After GC
        ]
        
        mock_gc_collect.return_value = 42  # Objects collected
        
        gc_stats = self.monitor.force_garbage_collection()
        
        assert gc_stats['objects_collected'] == 42
        assert gc_stats['memory_before_mb'] == 200.0
        assert gc_stats['memory_after_mb'] == 150.0
        assert gc_stats['memory_freed_mb'] == 50.0
        
        mock_gc_collect.assert_called_once()
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_get_memory_report(self, mock_process_class, mock_virtual_memory):
        """Test comprehensive memory report generation."""
        # Mock memory info
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=4 * 1024 * 1024 * 1024,
            used=4 * 1024 * 1024 * 1024,
            percent=50.0
        )
        
        mock_process = Mock()
        mock_process.memory_info.return_value = MockMemoryInfo(rss=100 * 1024 * 1024)
        mock_process_class.return_value = mock_process
        
        # Ensure process is None so it gets initialized with mock
        self.monitor._process = None
        
        # Set baseline for tracking
        self.monitor.set_baseline_memory()
        
        report = self.monitor.get_memory_report()
        
        # Check current stats
        assert 'current_stats' in report
        assert report['current_stats']['system_memory_mb'] == 8192.0
        assert report['current_stats']['available_memory_mb'] == 4096.0
        assert report['current_stats']['memory_usage_percent'] == 50.0
        assert report['current_stats']['process_memory_mb'] == 100.0
        
        # Check thresholds
        assert 'thresholds' in report
        assert report['thresholds']['max_memory_threshold_percent'] == 80.0
        assert report['thresholds']['critical_memory_threshold_percent'] == 90.0
        
        # Check recommendations
        assert 'recommendations' in report
        assert 'should_reduce_batch_size' in report['recommendations']
        assert 'is_critical_pressure' in report['recommendations']
        
        # Check memory tracking (should be present since baseline was set)
        assert 'memory_tracking' in report
        assert report['memory_tracking']['baseline_memory_mb'] == 100.0
        assert report['memory_tracking']['memory_growth_mb'] == 0.0
        assert report['memory_tracking']['peak_memory_mb'] == 100.0
    
    @patch('src.github_ioc_scanner.memory_monitor.psutil.virtual_memory')
    @patch('src.github_ioc_scanner.memory_monitor.psutil.Process')
    def test_get_memory_report_no_baseline(self, mock_process_class, mock_virtual_memory):
        """Test memory report without baseline set."""
        # Mock memory info
        mock_virtual_memory.return_value = MockVirtualMemory(
            total=8 * 1024 * 1024 * 1024,
            available=4 * 1024 * 1024 * 1024,
            used=4 * 1024 * 1024 * 1024,
            percent=50.0
        )
        
        mock_process = Mock()
        mock_process.memory_info.return_value = MockMemoryInfo(rss=100 * 1024 * 1024)
        mock_process_class.return_value = mock_process
        
        # Don't set baseline
        report = self.monitor.get_memory_report()
        
        # Memory tracking should not be present
        assert 'memory_tracking' not in report
    
    def test_memory_monitor_initialization(self):
        """Test memory monitor initialization with custom parameters."""
        monitor = MemoryMonitor(
            max_memory_threshold=0.7,
            critical_memory_threshold=0.85,
            min_batch_size=2,
            max_batch_size=30
        )
        
        assert monitor.max_memory_threshold == 0.7
        assert monitor.critical_memory_threshold == 0.85
        assert monitor.min_batch_size == 2
        assert monitor.max_batch_size == 30
        assert monitor._baseline_memory is None
        assert monitor._peak_memory == 0.0


class TestMemoryStats:
    """Test MemoryStats dataclass."""
    
    def test_memory_stats_creation(self):
        """Test MemoryStats creation and attributes."""
        stats = MemoryStats(
            total_mb=8192.0,
            available_mb=4096.0,
            used_mb=4096.0,
            percent_used=0.5,
            process_mb=100.0,
            process_percent=0.01
        )
        
        assert stats.total_mb == 8192.0
        assert stats.available_mb == 4096.0
        assert stats.used_mb == 4096.0
        assert stats.percent_used == 0.5
        assert stats.process_mb == 100.0
        assert stats.process_percent == 0.01


if __name__ == '__main__':
    pytest.main([__file__])