"""Performance monitoring and metrics collection for batch operations."""

import logging
import statistics
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from .batch_models import BatchMetrics, BatchResult, BatchStrategy


logger = logging.getLogger(__name__)


@dataclass
class OperationMetrics:
    """Metrics for a specific operation type."""
    operation_type: str
    total_operations: int = 0
    total_duration: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    cache_hits: int = 0
    batch_sizes: List[int] = field(default_factory=list)
    durations: List[float] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.success_count / self.total_operations) * 100
    
    @property
    def average_duration(self) -> float:
        """Calculate average operation duration."""
        if not self.durations:
            return 0.0
        return statistics.mean(self.durations)
    
    @property
    def average_batch_size(self) -> float:
        """Calculate average batch size."""
        if not self.batch_sizes:
            return 0.0
        return statistics.mean(self.batch_sizes)
    
    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate as percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.cache_hits / self.total_operations) * 100


@dataclass
class PerformanceTrend:
    """Tracks performance trends over time."""
    window_size: int = 100
    timestamps: deque = field(default_factory=lambda: deque(maxlen=100))
    durations: deque = field(default_factory=lambda: deque(maxlen=100))
    success_rates: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def add_measurement(self, duration: float, success_rate: float):
        """Add a new measurement to the trend."""
        self.timestamps.append(datetime.now())
        self.durations.append(duration)
        self.success_rates.append(success_rate)
    
    @property
    def is_improving(self) -> bool:
        """Check if performance is improving over time."""
        if len(self.durations) < 10:
            return False
        
        # Compare recent performance to older performance
        recent = list(self.durations)[-5:]
        older = list(self.durations)[-10:-5]
        
        if not recent or not older:
            return False
        
        recent_avg = statistics.mean(recent)
        older_avg = statistics.mean(older)
        
        # Performance is improving if recent durations are shorter
        return recent_avg < older_avg * 0.95  # 5% improvement threshold


class BatchMetricsCollector:
    """Collects and analyzes batch performance metrics."""
    
    def __init__(self, enable_detailed_tracking: bool = True):
        """Initialize the metrics collector.
        
        Args:
            enable_detailed_tracking: Whether to track detailed per-operation metrics
        """
        self.enable_detailed_tracking = enable_detailed_tracking
        self.start_time = datetime.now()
        
        # Overall metrics
        self.total_operations = 0
        self.total_api_calls = 0
        self.total_cache_hits = 0
        self.total_processing_time = 0.0
        
        # Per-operation type metrics
        self.operation_metrics: Dict[str, OperationMetrics] = {}
        
        # Performance trends
        self.performance_trends: Dict[str, PerformanceTrend] = {}
        
        # Recent batch metrics for analysis
        self.recent_batches: deque = deque(maxlen=50)
        
        # Strategy performance tracking
        self.strategy_performance: Dict[BatchStrategy, OperationMetrics] = {
            strategy: OperationMetrics(operation_type=strategy.value)
            for strategy in BatchStrategy
        }
        
        logger.info("BatchMetricsCollector initialized")
    
    def record_batch_operation(
        self,
        operation_type: str,
        duration: float,
        batch_size: int,
        success_count: int,
        total_count: int,
        cache_hits: int = 0,
        strategy: Optional[BatchStrategy] = None
    ) -> None:
        """Record metrics for a batch operation.
        
        Args:
            operation_type: Type of operation (e.g., 'file_batch', 'repo_batch')
            duration: Duration of the operation in seconds
            batch_size: Size of the batch processed
            success_count: Number of successful operations
            total_count: Total number of operations attempted
            cache_hits: Number of cache hits in this batch
            strategy: Batch strategy used for this operation
        """
        self.total_operations += 1
        self.total_processing_time += duration
        self.total_cache_hits += cache_hits
        
        # Update operation-specific metrics
        if operation_type not in self.operation_metrics:
            self.operation_metrics[operation_type] = OperationMetrics(operation_type)
        op_metrics = self.operation_metrics[operation_type]
        op_metrics.total_operations += 1
        op_metrics.total_duration += duration
        op_metrics.success_count += success_count
        op_metrics.failure_count += (total_count - success_count)
        op_metrics.cache_hits += cache_hits
        op_metrics.batch_sizes.append(batch_size)
        op_metrics.durations.append(duration)
        
        # Update strategy performance if provided
        if strategy:
            strategy_metrics = self.strategy_performance[strategy]
            strategy_metrics.total_operations += 1
            strategy_metrics.total_duration += duration
            strategy_metrics.success_count += success_count
            strategy_metrics.failure_count += (total_count - success_count)
            strategy_metrics.cache_hits += cache_hits
            strategy_metrics.batch_sizes.append(batch_size)
            strategy_metrics.durations.append(duration)
        
        # Update performance trends
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
        if operation_type not in self.performance_trends:
            self.performance_trends[operation_type] = PerformanceTrend()
        self.performance_trends[operation_type].add_measurement(duration, success_rate)
        
        # Store recent batch for analysis
        if self.enable_detailed_tracking:
            batch_info = {
                'timestamp': datetime.now(),
                'operation_type': operation_type,
                'duration': duration,
                'batch_size': batch_size,
                'success_count': success_count,
                'total_count': total_count,
                'cache_hits': cache_hits,
                'strategy': strategy.value if strategy else None
            }
            self.recent_batches.append(batch_info)
        
        logger.debug(
            f"Recorded batch operation: {operation_type}, "
            f"duration={duration:.2f}s, batch_size={batch_size}, "
            f"success_rate={success_rate:.1f}%"
        )
    
    def record_batch_metrics(self, metrics: BatchMetrics) -> None:
        """Record metrics from a BatchMetrics object.
        
        Args:
            metrics: BatchMetrics object containing operation results
        """
        operation_type = "batch_operation"
        duration = metrics.duration_seconds
        
        self.record_batch_operation(
            operation_type=operation_type,
            duration=duration,
            batch_size=int(metrics.average_batch_size) if metrics.average_batch_size > 0 else 1,
            success_count=metrics.successful_requests,
            total_count=metrics.total_requests,
            cache_hits=metrics.cache_hits
        )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary.
        
        Returns:
            Dictionary containing performance metrics and analysis
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        summary = {
            'uptime_seconds': uptime,
            'total_operations': self.total_operations,
            'total_processing_time': self.total_processing_time,
            'total_cache_hits': self.total_cache_hits,
            'operations_per_second': self.total_operations / uptime if uptime > 0 else 0,
            'average_operation_time': (
                self.total_processing_time / self.total_operations 
                if self.total_operations > 0 else 0
            ),
            'cache_efficiency': (
                self.total_cache_hits / self.total_operations * 100 
                if self.total_operations > 0 else 0
            )
        }
        
        # Add per-operation metrics
        summary['operation_metrics'] = {}
        for op_type, metrics in self.operation_metrics.items():
            summary['operation_metrics'][op_type] = {
                'total_operations': metrics.total_operations,
                'success_rate': metrics.success_rate,
                'average_duration': metrics.average_duration,
                'average_batch_size': metrics.average_batch_size,
                'cache_hit_rate': metrics.cache_hit_rate
            }
        
        # Add strategy performance
        summary['strategy_performance'] = {}
        for strategy, metrics in self.strategy_performance.items():
            if metrics.total_operations > 0:
                summary['strategy_performance'][strategy.value] = {
                    'total_operations': metrics.total_operations,
                    'success_rate': metrics.success_rate,
                    'average_duration': metrics.average_duration,
                    'average_batch_size': metrics.average_batch_size
                }
        
        # Add performance trends
        summary['performance_trends'] = {}
        for op_type, trend in self.performance_trends.items():
            if len(trend.durations) > 0:
                summary['performance_trends'][op_type] = {
                    'is_improving': trend.is_improving,
                    'recent_average_duration': statistics.mean(list(trend.durations)[-10:]),
                    'sample_count': len(trend.durations)
                }
        
        return summary
    
    def get_efficiency_metrics(self) -> Dict[str, float]:
        """Get efficiency-focused metrics.
        
        Returns:
            Dictionary with efficiency measurements
        """
        if self.total_operations == 0:
            return {
                'overall_efficiency': 0.0,
                'cache_efficiency': 0.0,
                'time_efficiency': 0.0,
                'batch_efficiency': 0.0
            }
        
        # Calculate various efficiency metrics
        cache_efficiency = (self.total_cache_hits / self.total_operations) * 100
        
        # Time efficiency: operations per second
        uptime = (datetime.now() - self.start_time).total_seconds()
        time_efficiency = self.total_operations / uptime if uptime > 0 else 0
        
        # Batch efficiency: average success rate across all operations
        total_success = sum(metrics.success_count for metrics in self.operation_metrics.values())
        total_attempts = sum(
            metrics.success_count + metrics.failure_count 
            for metrics in self.operation_metrics.values()
        )
        batch_efficiency = (total_success / total_attempts * 100) if total_attempts > 0 else 0
        
        # Overall efficiency score (weighted combination)
        overall_efficiency = (
            cache_efficiency * 0.3 +
            min(time_efficiency * 10, 100) * 0.3 +  # Cap time efficiency at 10 ops/sec = 100%
            batch_efficiency * 0.4
        )
        
        return {
            'overall_efficiency': overall_efficiency,
            'cache_efficiency': cache_efficiency,
            'time_efficiency': time_efficiency,
            'batch_efficiency': batch_efficiency
        }
    
    def identify_optimization_opportunities(self) -> List[str]:
        """Identify areas for performance optimization.
        
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        # Check cache efficiency
        efficiency = self.get_efficiency_metrics()
        if efficiency['cache_efficiency'] < 30:
            recommendations.append(
                "Low cache hit rate detected. Consider implementing cache warming "
                "or adjusting cache invalidation policies."
            )
        
        # Check batch efficiency
        if efficiency['batch_efficiency'] < 80:
            recommendations.append(
                "High failure rate detected. Consider implementing better error "
                "handling or adjusting batch sizes."
            )
        
        # Check for slow operations
        for op_type, metrics in self.operation_metrics.items():
            if metrics.average_duration > 5.0:  # 5 seconds threshold
                recommendations.append(
                    f"Operation '{op_type}' is slow (avg: {metrics.average_duration:.1f}s). "
                    "Consider optimizing batch sizes or implementing parallel processing."
                )
        
        # Check performance trends
        for op_type, trend in self.performance_trends.items():
            if len(trend.durations) >= 10 and not trend.is_improving:
                recent_avg = statistics.mean(list(trend.durations)[-5:])
                if recent_avg > 3.0:  # 3 seconds threshold
                    recommendations.append(
                        f"Performance for '{op_type}' is not improving and may be degrading. "
                        "Consider reviewing recent changes or system resources."
                    )
        
        # Check strategy performance
        if len(self.strategy_performance) > 1:
            best_strategy = min(
                self.strategy_performance.items(),
                key=lambda x: x[1].average_duration if x[1].total_operations > 0 else float('inf')
            )
            worst_strategy = max(
                self.strategy_performance.items(),
                key=lambda x: x[1].average_duration if x[1].total_operations > 0 else 0
            )
            
            if (best_strategy[1].total_operations > 0 and 
                worst_strategy[1].total_operations > 0 and
                worst_strategy[1].average_duration > best_strategy[1].average_duration * 1.5):
                recommendations.append(
                    f"Strategy '{best_strategy[0].value}' performs significantly better "
                    f"than '{worst_strategy[0].value}'. Consider using it more frequently."
                )
        
        # Check batch sizes
        all_batch_sizes = []
        for metrics in self.operation_metrics.values():
            all_batch_sizes.extend(metrics.batch_sizes)
        
        if all_batch_sizes:
            avg_batch_size = statistics.mean(all_batch_sizes)
            if avg_batch_size < 5:
                recommendations.append(
                    "Average batch size is small. Consider increasing batch sizes "
                    "to improve throughput (while respecting rate limits)."
                )
            elif avg_batch_size > 50:
                recommendations.append(
                    "Average batch size is large. Consider reducing batch sizes "
                    "to improve responsiveness and reduce memory usage."
                )
        
        if not recommendations:
            recommendations.append("Performance metrics look good. No specific optimizations needed.")
        
        return recommendations
    
    def get_recent_performance(self, minutes: int = 10) -> Dict[str, Any]:
        """Get performance metrics for recent operations.
        
        Args:
            minutes: Number of minutes to look back
        
        Returns:
            Dictionary with recent performance data
        """
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_batches = [
            batch for batch in self.recent_batches
            if batch['timestamp'] >= cutoff_time
        ]
        
        if not recent_batches:
            return {
                'period_minutes': minutes,
                'total_operations': 0,
                'average_duration': 0.0,
                'success_rate': 0.0,
                'operations_per_minute': 0.0
            }
        
        total_ops = len(recent_batches)
        total_duration = sum(batch['duration'] for batch in recent_batches)
        total_success = sum(batch['success_count'] for batch in recent_batches)
        total_attempts = sum(batch['total_count'] for batch in recent_batches)
        
        return {
            'period_minutes': minutes,
            'total_operations': total_ops,
            'average_duration': total_duration / total_ops,
            'success_rate': (total_success / total_attempts * 100) if total_attempts > 0 else 0,
            'operations_per_minute': total_ops / minutes,
            'total_cache_hits': sum(batch['cache_hits'] for batch in recent_batches)
        }
    
    def reset_metrics(self) -> None:
        """Reset all collected metrics."""
        self.start_time = datetime.now()
        self.total_operations = 0
        self.total_api_calls = 0
        self.total_cache_hits = 0
        self.total_processing_time = 0.0
        
        self.operation_metrics.clear()
        self.performance_trends.clear()
        self.recent_batches.clear()
        
        # Reset strategy performance
        self.strategy_performance = {
            strategy: OperationMetrics(operation_type=strategy.value)
            for strategy in BatchStrategy
        }
        
        logger.info("BatchMetricsCollector metrics reset")