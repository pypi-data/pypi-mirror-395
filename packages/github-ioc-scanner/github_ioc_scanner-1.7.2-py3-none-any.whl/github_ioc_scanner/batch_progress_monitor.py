"""Real-time batch progress monitoring and ETA calculation."""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable
from threading import Lock

from .batch_models import BatchMetrics, BatchResult


logger = logging.getLogger(__name__)


@dataclass
class ProgressSnapshot:
    """Snapshot of progress at a specific point in time."""
    timestamp: datetime
    completed_operations: int
    total_operations: int
    success_count: int
    failure_count: int
    current_batch_size: int
    processing_rate: float  # operations per second
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.completed_operations / self.total_operations) * 100
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.completed_operations == 0:
            return 0.0
        return (self.success_count / self.completed_operations) * 100


@dataclass
class ETACalculation:
    """ETA calculation result."""
    estimated_seconds_remaining: float
    estimated_completion_time: datetime
    confidence_level: float  # 0.0 to 1.0
    based_on_samples: int
    
    @property
    def estimated_time_remaining_str(self) -> str:
        """Format remaining time as human-readable string."""
        if self.estimated_seconds_remaining <= 0:
            return "Complete"
        
        seconds = int(self.estimated_seconds_remaining)
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            remaining_seconds = seconds % 60
            return f"{minutes}m {remaining_seconds}s"
        else:
            hours = seconds // 3600
            remaining_minutes = (seconds % 3600) // 60
            return f"{hours}h {remaining_minutes}m"


class BatchProgressMonitor:
    """Real-time monitoring of batch operations with progress tracking and ETA calculation."""
    
    def __init__(
        self,
        enable_verbose_logging: bool = False,
        progress_callback: Optional[Callable[[ProgressSnapshot], None]] = None,
        update_interval_seconds: float = 1.0
    ):
        """Initialize the progress monitor.
        
        Args:
            enable_verbose_logging: Whether to enable verbose progress logging
            progress_callback: Optional callback function for progress updates
            update_interval_seconds: Minimum interval between progress updates
        """
        self.enable_verbose_logging = enable_verbose_logging
        self.progress_callback = progress_callback
        self.update_interval_seconds = update_interval_seconds
        
        # Progress tracking
        self.start_time: Optional[datetime] = None
        self.last_update_time: Optional[datetime] = None
        self.total_operations = 0
        self.completed_operations = 0
        self.success_count = 0
        self.failure_count = 0
        self.current_batch_size = 0
        
        # Progress history for ETA calculation
        self.progress_history: List[ProgressSnapshot] = []
        self.max_history_size = 50
        
        # Thread safety
        self._lock = Lock()
        
        # Current operation tracking
        self.current_operation_type: Optional[str] = None
        self.current_operation_start: Optional[datetime] = None
        
        logger.info("BatchProgressMonitor initialized")
    
    def start_monitoring(self, total_operations: int, operation_type: str = "batch_operation") -> None:
        """Start monitoring a new batch operation.
        
        Args:
            total_operations: Total number of operations expected
            operation_type: Type of operation being monitored
        """
        with self._lock:
            self.start_time = datetime.now()
            self.last_update_time = self.start_time
            self.total_operations = total_operations
            self.completed_operations = 0
            self.success_count = 0
            self.failure_count = 0
            self.current_batch_size = 0
            self.current_operation_type = operation_type
            self.current_operation_start = self.start_time
            
            # Clear previous history
            self.progress_history.clear()
            
            if self.enable_verbose_logging:
                logger.info(
                    f"Started monitoring {operation_type}: {total_operations} operations expected"
                )
    
    def update_progress(
        self,
        completed: int,
        success_count: int,
        failure_count: int,
        current_batch_size: int = 0
    ) -> Optional[ProgressSnapshot]:
        """Update progress and return current snapshot.
        
        Args:
            completed: Number of completed operations
            success_count: Number of successful operations
            failure_count: Number of failed operations
            current_batch_size: Size of current batch being processed
            
        Returns:
            ProgressSnapshot if update was processed, None if too soon for update
        """
        now = datetime.now()
        
        with self._lock:
            # Check if enough time has passed for an update (skip check for first update)
            if (self.last_update_time and 
                self.last_update_time != self.start_time and
                (now - self.last_update_time).total_seconds() < self.update_interval_seconds):
                return None
            
            self.completed_operations = completed
            self.success_count = success_count
            self.failure_count = failure_count
            self.current_batch_size = current_batch_size
            
            # Calculate processing rate
            elapsed_seconds = (now - self.start_time).total_seconds() if self.start_time else 0
            processing_rate = completed / elapsed_seconds if elapsed_seconds > 0 else 0
            
            # Create progress snapshot
            snapshot = ProgressSnapshot(
                timestamp=now,
                completed_operations=completed,
                total_operations=self.total_operations,
                success_count=success_count,
                failure_count=failure_count,
                current_batch_size=current_batch_size,
                processing_rate=processing_rate
            )
            
            # Add to history
            self.progress_history.append(snapshot)
            if len(self.progress_history) > self.max_history_size:
                self.progress_history.pop(0)
            
            self.last_update_time = now
        
        # Log progress and call callback outside the lock to avoid deadlock
        if self.enable_verbose_logging:
            self._log_progress(snapshot)
        
        # Call progress callback if provided
        if self.progress_callback:
            try:
                self.progress_callback(snapshot)
            except Exception as e:
                logger.warning(f"Progress callback failed: {e}")
        
        return snapshot
    
    def record_batch_result(self, result: BatchResult) -> None:
        """Record a batch result for progress tracking.
        
        Args:
            result: BatchResult to record
        """
        with self._lock:
            if result.success:
                self.success_count += 1
            else:
                self.failure_count += 1
            
            self.completed_operations = self.success_count + self.failure_count
        
        # Update progress (call outside the lock to avoid deadlock)
        self.update_progress(
            completed=self.completed_operations,
            success_count=self.success_count,
            failure_count=self.failure_count,
            current_batch_size=self.current_batch_size
        )
    
    def calculate_eta(self) -> Optional[ETACalculation]:
        """Calculate estimated time of arrival (ETA) for completion.
        
        Returns:
            ETACalculation if enough data is available, None otherwise
        """
        with self._lock:
            if len(self.progress_history) < 2 or self.total_operations == 0:
                return None
            
            remaining_operations = self.total_operations - self.completed_operations
            if remaining_operations <= 0:
                return ETACalculation(
                    estimated_seconds_remaining=0.0,
                    estimated_completion_time=datetime.now(),
                    confidence_level=1.0,
                    based_on_samples=len(self.progress_history)
                )
            
            # Use recent history for ETA calculation
            recent_samples = min(10, len(self.progress_history))
            recent_history = self.progress_history[-recent_samples:]
            
            # Calculate average processing rate from recent samples
            if len(recent_history) < 2:
                return None
            
            time_span = (recent_history[-1].timestamp - recent_history[0].timestamp).total_seconds()
            operations_completed = recent_history[-1].completed_operations - recent_history[0].completed_operations
            
            if time_span <= 0:
                return None
            
            # If no operations completed in the time span, use a very small rate
            if operations_completed <= 0:
                avg_rate = 0.001  # Very slow rate
            else:
                avg_rate = operations_completed / time_span
            
            # Calculate ETA
            estimated_seconds = remaining_operations / avg_rate if avg_rate > 0 else float('inf')
            estimated_completion = datetime.now() + timedelta(seconds=estimated_seconds)
            
            # Calculate confidence based on consistency of recent rates
            confidence = self._calculate_confidence(recent_history)
            
            return ETACalculation(
                estimated_seconds_remaining=estimated_seconds,
                estimated_completion_time=estimated_completion,
                confidence_level=confidence,
                based_on_samples=len(recent_history)
            )
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current monitoring status.
        
        Returns:
            Dictionary with current status information
        """
        with self._lock:
            if not self.start_time:
                return {
                    'status': 'not_started',
                    'message': 'Monitoring not started'
                }
            
            elapsed_seconds = (datetime.now() - self.start_time).total_seconds()
            
            status = {
                'status': 'in_progress' if self.completed_operations < self.total_operations else 'completed',
                'operation_type': self.current_operation_type,
                'total_operations': self.total_operations,
                'completed_operations': self.completed_operations,
                'success_count': self.success_count,
                'failure_count': self.failure_count,
                'completion_percentage': (self.completed_operations / self.total_operations * 100) if self.total_operations > 0 else 0,
                'success_rate': (self.success_count / self.completed_operations * 100) if self.completed_operations > 0 else 0,
                'elapsed_seconds': elapsed_seconds,
                'current_batch_size': self.current_batch_size,
                'processing_rate': self.completed_operations / elapsed_seconds if elapsed_seconds > 0 else 0
            }
        
        # Calculate ETA outside the lock to avoid deadlock
        eta = self.calculate_eta()
        if eta:
            status.update({
                'eta_seconds_remaining': eta.estimated_seconds_remaining,
                'eta_completion_time': eta.estimated_completion_time.isoformat(),
                'eta_time_remaining_str': eta.estimated_time_remaining_str,
                'eta_confidence': eta.confidence_level
            })
        
        return status
    
    def log_batch_progress(
        self,
        completed: int,
        total: int,
        current_batch_size: int,
        eta_seconds: Optional[float] = None
    ) -> None:
        """Log current batch processing progress.
        
        Args:
            completed: Number of completed operations
            total: Total number of operations
            current_batch_size: Size of current batch
            eta_seconds: Optional ETA in seconds
        """
        percentage = (completed / total * 100) if total > 0 else 0
        
        if eta_seconds is not None and eta_seconds > 0:
            eta_str = ETACalculation(
                estimated_seconds_remaining=eta_seconds,
                estimated_completion_time=datetime.now() + timedelta(seconds=eta_seconds),
                confidence_level=0.0,
                based_on_samples=0
            ).estimated_time_remaining_str
            eta_info = f", ETA: {eta_str}"
        else:
            eta_info = ""
        
        message = (
            f"Progress: {completed}/{total} ({percentage:.1f}%), "
            f"batch size: {current_batch_size}{eta_info}"
        )
        
        if self.enable_verbose_logging:
            logger.info(message)
        else:
            logger.debug(message)
    
    def finish_monitoring(self) -> Dict[str, Any]:
        """Finish monitoring and return final statistics.
        
        Returns:
            Dictionary with final monitoring statistics
        """
        with self._lock:
            if not self.start_time:
                return {'error': 'Monitoring was not started'}
            
            end_time = datetime.now()
            total_duration = (end_time - self.start_time).total_seconds()
            
            final_stats = {
                'operation_type': self.current_operation_type,
                'total_operations': self.total_operations,
                'completed_operations': self.completed_operations,
                'success_count': self.success_count,
                'failure_count': self.failure_count,
                'total_duration_seconds': total_duration,
                'average_operations_per_second': self.completed_operations / total_duration if total_duration > 0 else 0,
                'success_rate': (self.success_count / self.completed_operations * 100) if self.completed_operations > 0 else 0,
                'completion_percentage': (self.completed_operations / self.total_operations * 100) if self.total_operations > 0 else 0
            }
            
            if self.enable_verbose_logging:
                logger.info(
                    f"Monitoring completed: {self.current_operation_type}, "
                    f"{self.completed_operations}/{self.total_operations} operations, "
                    f"{final_stats['success_rate']:.1f}% success rate, "
                    f"{total_duration:.1f}s total duration"
                )
            
            return final_stats
    
    def _log_progress(self, snapshot: ProgressSnapshot) -> None:
        """Log progress information.
        
        Args:
            snapshot: Current progress snapshot
        """
        eta = self.calculate_eta()
        eta_str = eta.estimated_time_remaining_str if eta else "calculating..."
        
        logger.info(
            f"{self.current_operation_type}: {snapshot.completed_operations}/{snapshot.total_operations} "
            f"({snapshot.completion_percentage:.1f}%) completed, "
            f"success rate: {snapshot.success_rate:.1f}%, "
            f"rate: {snapshot.processing_rate:.1f} ops/sec, "
            f"batch size: {snapshot.current_batch_size}, "
            f"ETA: {eta_str}"
        )
    
    def _calculate_confidence(self, history: List[ProgressSnapshot]) -> float:
        """Calculate confidence level for ETA based on rate consistency.
        
        Args:
            history: List of recent progress snapshots
            
        Returns:
            Confidence level between 0.0 and 1.0
        """
        if len(history) < 3:
            return 0.5  # Medium confidence with limited data
        
        # Calculate rates between consecutive snapshots
        rates = []
        for i in range(1, len(history)):
            time_diff = (history[i].timestamp - history[i-1].timestamp).total_seconds()
            ops_diff = history[i].completed_operations - history[i-1].completed_operations
            
            if time_diff > 0:
                rate = ops_diff / time_diff
                rates.append(rate)
        
        if not rates:
            return 0.3  # Low confidence
        
        # Calculate coefficient of variation (std dev / mean)
        if len(rates) == 1:
            return 0.7  # Good confidence with single rate
        
        mean_rate = sum(rates) / len(rates)
        if mean_rate == 0:
            return 0.1  # Very low confidence
        
        variance = sum((rate - mean_rate) ** 2 for rate in rates) / len(rates)
        std_dev = variance ** 0.5
        cv = std_dev / mean_rate
        
        # Convert CV to confidence (lower CV = higher confidence)
        # CV of 0 = confidence 1.0, CV of 1+ = confidence approaches 0
        confidence = max(0.1, min(1.0, 1.0 - cv))
        
        return confidence
    
    def alert_on_performance_issues(self, metrics: BatchMetrics) -> List[str]:
        """Alert when performance issues are detected.
        
        Args:
            metrics: BatchMetrics to analyze
            
        Returns:
            List of performance alerts
        """
        alerts = []
        
        # Check success rate
        if metrics.success_rate < 80:
            alerts.append(
                f"Low success rate detected: {metrics.success_rate:.1f}% "
                f"({metrics.successful_requests}/{metrics.total_requests})"
            )
        
        # Check processing speed
        if metrics.duration_seconds > 0:
            ops_per_second = metrics.total_requests / metrics.duration_seconds
            if ops_per_second < 1.0:
                alerts.append(
                    f"Slow processing detected: {ops_per_second:.2f} operations/second"
                )
        
        # Check cache efficiency
        if metrics.cache_hit_rate < 30:
            alerts.append(
                f"Low cache hit rate: {metrics.cache_hit_rate:.1f}% "
                f"({metrics.cache_hits}/{metrics.cache_hits + metrics.cache_misses})"
            )
        
        # Check for stalled progress
        with self._lock:
            if len(self.progress_history) >= 5:
                recent_snapshots = self.progress_history[-5:]
                if all(s.completed_operations == recent_snapshots[0].completed_operations 
                       for s in recent_snapshots):
                    alerts.append("Progress appears to be stalled - no operations completed recently")
        
        return alerts