"""Memory monitoring and management for batch processing."""

import gc
import logging
import psutil
from dataclasses import dataclass
from typing import Optional, Dict, Any
from threading import Lock

logger = logging.getLogger(__name__)


@dataclass
class MemoryStats:
    """Memory usage statistics."""
    total_mb: float
    available_mb: float
    used_mb: float
    percent_used: float
    process_mb: float
    process_percent: float


class MemoryMonitor:
    """Monitors memory usage and provides batch size adjustment recommendations."""
    
    def __init__(
        self,
        max_memory_threshold: float = 0.8,  # 80% of available memory
        critical_memory_threshold: float = 0.9,  # 90% of available memory
        min_batch_size: int = 1,
        max_batch_size: int = 50
    ):
        """Initialize memory monitor.
        
        Args:
            max_memory_threshold: Memory usage threshold to start reducing batch sizes
            critical_memory_threshold: Critical memory threshold for aggressive reduction
            min_batch_size: Minimum allowed batch size
            max_batch_size: Maximum allowed batch size
        """
        self.max_memory_threshold = max_memory_threshold
        self.critical_memory_threshold = critical_memory_threshold
        self.min_batch_size = min_batch_size
        self.max_batch_size = max_batch_size
        
        self._process = None  # Will be initialized in get_memory_stats
        self._lock = Lock()
        self._baseline_memory: Optional[float] = None
        self._peak_memory: float = 0.0
        
    def get_memory_stats(self) -> MemoryStats:
        """Get current memory statistics."""
        try:
            # System memory
            system_memory = psutil.virtual_memory()
            
            # Process memory - initialize process if not already done
            if self._process is None:
                self._process = psutil.Process()
            
            process_memory = self._process.memory_info()
            process_mb = process_memory.rss / 1024 / 1024
            
            # Update peak memory tracking
            with self._lock:
                self._peak_memory = max(self._peak_memory, process_mb)
            
            return MemoryStats(
                total_mb=system_memory.total / 1024 / 1024,
                available_mb=system_memory.available / 1024 / 1024,
                used_mb=system_memory.used / 1024 / 1024,
                percent_used=system_memory.percent / 100.0,
                process_mb=process_mb,
                process_percent=process_mb / (system_memory.total / 1024 / 1024)
            )
        except Exception as e:
            logger.warning(f"Failed to get memory stats: {e}")
            # Return safe defaults
            return MemoryStats(
                total_mb=8192.0,  # Assume 8GB
                available_mb=4096.0,  # Assume 4GB available
                used_mb=4096.0,
                percent_used=0.5,
                process_mb=100.0,  # Assume 100MB process
                process_percent=0.01
            )
    
    def set_baseline_memory(self) -> None:
        """Set baseline memory usage for comparison."""
        stats = self.get_memory_stats()
        with self._lock:
            self._baseline_memory = stats.process_mb
        logger.debug(f"Set baseline memory: {self._baseline_memory:.2f} MB")
    
    def get_memory_growth(self) -> float:
        """Get memory growth since baseline was set."""
        if self._baseline_memory is None:
            return 0.0
        
        current_stats = self.get_memory_stats()
        return current_stats.process_mb - self._baseline_memory
    
    def should_reduce_batch_size(self) -> bool:
        """Check if batch size should be reduced due to memory pressure."""
        stats = self.get_memory_stats()
        
        # Check system memory pressure
        if stats.percent_used > self.max_memory_threshold:
            logger.debug(f"System memory pressure detected: {stats.percent_used:.1%}")
            return True
        
        # Check process memory growth
        if self._baseline_memory is not None:
            growth = self.get_memory_growth()
            if growth > 500:  # More than 500MB growth
                logger.debug(f"Process memory growth detected: {growth:.2f} MB")
                return True
        
        return False
    
    def is_critical_memory_pressure(self) -> bool:
        """Check if we're in critical memory pressure situation."""
        stats = self.get_memory_stats()
        return stats.percent_used > self.critical_memory_threshold
    
    def calculate_adjusted_batch_size(
        self, 
        current_batch_size: int,
        memory_pressure_factor: Optional[float] = None
    ) -> int:
        """Calculate adjusted batch size based on memory pressure.
        
        Args:
            current_batch_size: Current batch size
            memory_pressure_factor: Optional override for memory pressure (0.0-1.0)
            
        Returns:
            Adjusted batch size
        """
        if memory_pressure_factor is None:
            stats = self.get_memory_stats()
            memory_pressure_factor = min(1.0, stats.percent_used)
        
        # Calculate reduction factor based on memory pressure
        if memory_pressure_factor > self.critical_memory_threshold:
            # Critical pressure: reduce to minimum
            reduction_factor = 0.1
        elif memory_pressure_factor > self.max_memory_threshold:
            # High pressure: significant reduction
            pressure_excess = memory_pressure_factor - self.max_memory_threshold
            max_excess = self.critical_memory_threshold - self.max_memory_threshold
            reduction_factor = 0.5 - (0.4 * pressure_excess / max_excess)
        else:
            # Normal pressure: no reduction needed
            reduction_factor = 1.0
        
        # Apply reduction
        adjusted_size = int(current_batch_size * reduction_factor)
        
        # Ensure within bounds
        adjusted_size = max(self.min_batch_size, min(self.max_batch_size, adjusted_size))
        
        if adjusted_size != current_batch_size:
            logger.debug(
                f"Adjusted batch size from {current_batch_size} to {adjusted_size} "
                f"due to memory pressure ({memory_pressure_factor:.1%})"
            )
        
        return adjusted_size
    
    def force_garbage_collection(self) -> Dict[str, Any]:
        """Force garbage collection and return collection stats."""
        stats_before = self.get_memory_stats()
        
        # Force garbage collection
        collected = gc.collect()
        
        stats_after = self.get_memory_stats()
        memory_freed = stats_before.process_mb - stats_after.process_mb
        
        gc_stats = {
            "objects_collected": collected,
            "memory_before_mb": stats_before.process_mb,
            "memory_after_mb": stats_after.process_mb,
            "memory_freed_mb": memory_freed
        }
        
        if memory_freed > 1.0:  # Only log if significant memory was freed
            logger.debug(f"Garbage collection freed {memory_freed:.2f} MB")
        
        return gc_stats
    
    def get_memory_report(self) -> Dict[str, Any]:
        """Get comprehensive memory usage report."""
        stats = self.get_memory_stats()
        
        report = {
            "current_stats": {
                "system_memory_mb": stats.total_mb,
                "available_memory_mb": stats.available_mb,
                "memory_usage_percent": stats.percent_used * 100,
                "process_memory_mb": stats.process_mb,
                "process_memory_percent": stats.process_percent * 100
            },
            "thresholds": {
                "max_memory_threshold_percent": self.max_memory_threshold * 100,
                "critical_memory_threshold_percent": self.critical_memory_threshold * 100
            },
            "recommendations": {
                "should_reduce_batch_size": self.should_reduce_batch_size(),
                "is_critical_pressure": self.is_critical_memory_pressure()
            }
        }
        
        if self._baseline_memory is not None:
            report["memory_tracking"] = {
                "baseline_memory_mb": self._baseline_memory,
                "memory_growth_mb": self.get_memory_growth(),
                "peak_memory_mb": self._peak_memory
            }
        
        return report