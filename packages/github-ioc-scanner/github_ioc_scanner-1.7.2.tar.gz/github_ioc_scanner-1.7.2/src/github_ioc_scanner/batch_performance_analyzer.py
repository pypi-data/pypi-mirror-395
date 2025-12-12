"""Performance analysis and optimization recommendations for batch operations."""

import logging
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
from enum import Enum

from .batch_models import BatchMetrics, BatchStrategy
from .batch_metrics_collector import BatchMetricsCollector, OperationMetrics
from .batch_progress_monitor import BatchProgressMonitor, ProgressSnapshot


logger = logging.getLogger(__name__)


class RecommendationPriority(Enum):
    """Priority levels for optimization recommendations."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class RecommendationType(Enum):
    """Types of optimization recommendations."""
    BATCH_SIZE = "batch_size"
    CONCURRENCY = "concurrency"
    CACHING = "caching"
    STRATEGY = "strategy"
    ERROR_HANDLING = "error_handling"
    RESOURCE_USAGE = "resource_usage"
    NETWORK = "network"
    CONFIGURATION = "configuration"


@dataclass
class OptimizationRecommendation:
    """A specific optimization recommendation."""
    type: RecommendationType
    priority: RecommendationPriority
    title: str
    description: str
    current_value: Optional[Union[str, float, int]] = None
    recommended_value: Optional[Union[str, float, int]] = None
    expected_improvement: Optional[str] = None
    implementation_effort: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert recommendation to dictionary."""
        return {
            'type': self.type.value,
            'priority': self.priority.value,
            'title': self.title,
            'description': self.description,
            'current_value': self.current_value,
            'recommended_value': self.recommended_value,
            'expected_improvement': self.expected_improvement,
            'implementation_effort': self.implementation_effort
        }


@dataclass
class PerformanceAnalysis:
    """Complete performance analysis results."""
    overall_score: float  # 0-100 score
    efficiency_metrics: Dict[str, float]
    bottlenecks: List[str]
    recommendations: List[OptimizationRecommendation]
    trend_analysis: Dict[str, Any]
    comparative_analysis: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to dictionary."""
        return {
            'overall_score': self.overall_score,
            'efficiency_metrics': self.efficiency_metrics,
            'bottlenecks': self.bottlenecks,
            'recommendations': [rec.to_dict() for rec in self.recommendations],
            'trend_analysis': self.trend_analysis,
            'comparative_analysis': self.comparative_analysis
        }


class BatchPerformanceAnalyzer:
    """Analyzes batch performance and provides optimization recommendations."""
    
    def __init__(self):
        """Initialize the performance analyzer."""
        self.historical_analyses: List[PerformanceAnalysis] = []
        self.baseline_metrics: Optional[Dict[str, float]] = None
        
        # Performance thresholds
        self.thresholds = {
            'min_success_rate': 90.0,
            'min_cache_hit_rate': 50.0,
            'max_avg_duration': 5.0,
            'min_ops_per_second': 2.0,
            'max_failure_rate': 10.0,
            'min_batch_efficiency': 80.0
        }
        
        logger.info("BatchPerformanceAnalyzer initialized")
    
    def analyze_performance(
        self,
        metrics_collector: BatchMetricsCollector,
        progress_monitor: Optional[BatchProgressMonitor] = None
    ) -> PerformanceAnalysis:
        """Perform comprehensive performance analysis.
        
        Args:
            metrics_collector: BatchMetricsCollector with performance data
            progress_monitor: Optional BatchProgressMonitor for trend analysis
            
        Returns:
            PerformanceAnalysis with recommendations
        """
        logger.info("Starting comprehensive performance analysis")
        
        # Get current performance metrics
        performance_summary = metrics_collector.get_performance_summary()
        efficiency_metrics = metrics_collector.get_efficiency_metrics()
        
        # Calculate overall performance score
        overall_score = self._calculate_overall_score(efficiency_metrics, performance_summary)
        
        # Identify bottlenecks
        bottlenecks = self._identify_bottlenecks(performance_summary, efficiency_metrics)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            performance_summary, 
            efficiency_metrics, 
            metrics_collector
        )
        
        # Analyze trends from metrics collector
        trend_analysis = self._analyze_trends(metrics_collector)
        
        # Comparative analysis with historical data
        comparative_analysis = self._perform_comparative_analysis(efficiency_metrics)
        
        analysis = PerformanceAnalysis(
            overall_score=overall_score,
            efficiency_metrics=efficiency_metrics,
            bottlenecks=bottlenecks,
            recommendations=recommendations,
            trend_analysis=trend_analysis,
            comparative_analysis=comparative_analysis
        )
        
        # Store for historical comparison
        self.historical_analyses.append(analysis)
        if len(self.historical_analyses) > 50:  # Keep last 50 analyses
            self.historical_analyses.pop(0)
        
        logger.info(f"Performance analysis completed. Overall score: {overall_score:.1f}/100")
        return analysis
    
    def _calculate_overall_score(
        self, 
        efficiency_metrics: Dict[str, float], 
        performance_summary: Dict[str, Any]
    ) -> float:
        """Calculate overall performance score (0-100).
        
        Args:
            efficiency_metrics: Efficiency metrics from collector
            performance_summary: Performance summary from collector
            
        Returns:
            Overall performance score
        """
        scores = []
        weights = []
        
        # Cache efficiency (weight: 20%)
        cache_score = min(100, efficiency_metrics.get('cache_efficiency', 0))
        scores.append(cache_score)
        weights.append(0.2)
        
        # Batch efficiency (weight: 30%)
        batch_score = min(100, efficiency_metrics.get('batch_efficiency', 0))
        scores.append(batch_score)
        weights.append(0.3)
        
        # Time efficiency (weight: 25%)
        time_eff = efficiency_metrics.get('time_efficiency', 0)
        time_score = min(100, (time_eff / 10) * 100)  # 10 ops/sec = 100%
        scores.append(time_score)
        weights.append(0.25)
        
        # Operation success rate (weight: 25%)
        total_ops = performance_summary.get('total_operations', 0)
        if total_ops > 0:
            success_ops = sum(
                metrics.get('total_operations', 0) * (metrics.get('success_rate', 0) / 100)
                for metrics in performance_summary.get('operation_metrics', {}).values()
            )
            success_rate = (success_ops / total_ops) * 100
        else:
            success_rate = 0
        
        scores.append(min(100, success_rate))
        weights.append(0.25)
        
        # Calculate weighted average
        if not scores:
            return 0.0
        
        weighted_score = sum(score * weight for score, weight in zip(scores, weights))
        return max(0.0, min(100.0, weighted_score))
    
    def _identify_bottlenecks(
        self, 
        performance_summary: Dict[str, Any], 
        efficiency_metrics: Dict[str, float]
    ) -> List[str]:
        """Identify performance bottlenecks.
        
        Args:
            performance_summary: Performance summary from collector
            efficiency_metrics: Efficiency metrics from collector
            
        Returns:
            List of identified bottlenecks
        """
        bottlenecks = []
        
        # Check cache efficiency
        cache_eff = efficiency_metrics.get('cache_efficiency', 0)
        if cache_eff < self.thresholds['min_cache_hit_rate']:
            bottlenecks.append(
                f"Low cache hit rate ({cache_eff:.1f}%) - consider cache warming or optimization"
            )
        
        # Check batch efficiency
        batch_eff = efficiency_metrics.get('batch_efficiency', 0)
        if batch_eff < self.thresholds['min_batch_efficiency']:
            bottlenecks.append(
                f"Low batch success rate ({batch_eff:.1f}%) - high failure rate detected"
            )
        
        # Check processing speed
        time_eff = efficiency_metrics.get('time_efficiency', 0)
        if time_eff < self.thresholds['min_ops_per_second']:
            bottlenecks.append(
                f"Slow processing speed ({time_eff:.2f} ops/sec) - consider parallel processing"
            )
        
        # Check individual operation performance
        op_metrics = performance_summary.get('operation_metrics', {})
        for op_type, metrics in op_metrics.items():
            avg_duration = metrics.get('average_duration', 0)
            if avg_duration > self.thresholds['max_avg_duration']:
                bottlenecks.append(
                    f"Slow operation '{op_type}' ({avg_duration:.1f}s avg) - needs optimization"
                )
            
            success_rate = metrics.get('success_rate', 0)
            if success_rate < self.thresholds['min_success_rate']:
                bottlenecks.append(
                    f"High failure rate in '{op_type}' ({100-success_rate:.1f}% failures)"
                )
        
        # Check strategy performance
        strategy_perf = performance_summary.get('strategy_performance', {})
        if len(strategy_perf) > 1:
            # Find best and worst performing strategies
            best_strategy = min(strategy_perf.items(), 
                              key=lambda x: x[1].get('average_duration', float('inf')))
            worst_strategy = max(strategy_perf.items(), 
                               key=lambda x: x[1].get('average_duration', 0))
            
            if (best_strategy[1].get('average_duration', 0) > 0 and
                worst_strategy[1].get('average_duration', 0) > 
                best_strategy[1].get('average_duration', 0) * 2):
                bottlenecks.append(
                    f"Strategy '{worst_strategy[0]}' performs poorly compared to '{best_strategy[0]}'"
                )
        
        return bottlenecks
    
    def _generate_recommendations(
        self,
        performance_summary: Dict[str, Any],
        efficiency_metrics: Dict[str, float],
        metrics_collector: BatchMetricsCollector
    ) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations.
        
        Args:
            performance_summary: Performance summary from collector
            efficiency_metrics: Efficiency metrics from collector
            metrics_collector: The metrics collector instance
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        # Cache optimization recommendations
        cache_eff = efficiency_metrics.get('cache_efficiency', 0)
        if cache_eff < 30:
            recommendations.append(OptimizationRecommendation(
                type=RecommendationType.CACHING,
                priority=RecommendationPriority.HIGH,
                title="Implement Cache Warming",
                description="Cache hit rate is very low. Implement cache warming strategies to pre-load frequently accessed data.",
                current_value=f"{cache_eff:.1f}%",
                recommended_value="60%+",
                expected_improvement="30-50% performance improvement",
                implementation_effort="Medium"
            ))
        elif cache_eff < 50:
            recommendations.append(OptimizationRecommendation(
                type=RecommendationType.CACHING,
                priority=RecommendationPriority.MEDIUM,
                title="Optimize Cache Strategy",
                description="Cache hit rate could be improved. Review cache invalidation policies and consider increasing cache size.",
                current_value=f"{cache_eff:.1f}%",
                recommended_value="60%+",
                expected_improvement="15-25% performance improvement",
                implementation_effort="Low"
            ))
        
        # Batch size recommendations
        all_batch_sizes = []
        for op_metrics in performance_summary.get('operation_metrics', {}).values():
            if hasattr(metrics_collector, 'operation_metrics'):
                op_name = None
                for name, metrics in metrics_collector.operation_metrics.items():
                    if metrics.total_operations == op_metrics.get('total_operations', 0):
                        all_batch_sizes.extend(metrics.batch_sizes)
                        break
        
        if all_batch_sizes:
            avg_batch_size = statistics.mean(all_batch_sizes)
            if avg_batch_size < 5:
                recommendations.append(OptimizationRecommendation(
                    type=RecommendationType.BATCH_SIZE,
                    priority=RecommendationPriority.MEDIUM,
                    title="Increase Batch Size",
                    description="Average batch size is small. Increasing batch size can improve throughput while respecting rate limits.",
                    current_value=f"{avg_batch_size:.1f}",
                    recommended_value="10-20",
                    expected_improvement="20-40% throughput improvement",
                    implementation_effort="Low"
                ))
            elif avg_batch_size > 50:
                recommendations.append(OptimizationRecommendation(
                    type=RecommendationType.BATCH_SIZE,
                    priority=RecommendationPriority.MEDIUM,
                    title="Reduce Batch Size",
                    description="Average batch size is large. Reducing batch size can improve responsiveness and reduce memory usage.",
                    current_value=f"{avg_batch_size:.1f}",
                    recommended_value="20-30",
                    expected_improvement="Better responsiveness and lower memory usage",
                    implementation_effort="Low"
                ))
        
        # Strategy recommendations
        strategy_perf = performance_summary.get('strategy_performance', {})
        if len(strategy_perf) > 1:
            best_strategy = min(strategy_perf.items(), 
                              key=lambda x: x[1].get('average_duration', float('inf')))
            worst_strategy = max(strategy_perf.items(), 
                               key=lambda x: x[1].get('average_duration', 0))
            
            if (best_strategy[1].get('average_duration', 0) > 0 and
                worst_strategy[1].get('average_duration', 0) > 
                best_strategy[1].get('average_duration', 0) * 1.5):
                recommendations.append(OptimizationRecommendation(
                    type=RecommendationType.STRATEGY,
                    priority=RecommendationPriority.HIGH,
                    title="Optimize Batch Strategy",
                    description=f"Strategy '{best_strategy[0]}' performs significantly better than '{worst_strategy[0]}'. Consider using it more frequently.",
                    current_value=f"Mixed strategies",
                    recommended_value=f"Prefer {best_strategy[0]}",
                    expected_improvement="25-40% performance improvement",
                    implementation_effort="Low"
                ))
        
        # Error handling recommendations
        batch_eff = efficiency_metrics.get('batch_efficiency', 0)
        if batch_eff < 80:
            recommendations.append(OptimizationRecommendation(
                type=RecommendationType.ERROR_HANDLING,
                priority=RecommendationPriority.HIGH,
                title="Improve Error Handling",
                description="High failure rate detected. Implement better error handling, retry logic, and fallback strategies.",
                current_value=f"{batch_eff:.1f}% success rate",
                recommended_value="90%+ success rate",
                expected_improvement="Reduced failures and better reliability",
                implementation_effort="Medium"
            ))
        
        # Concurrency recommendations
        time_eff = efficiency_metrics.get('time_efficiency', 0)
        if time_eff < 2.0:
            recommendations.append(OptimizationRecommendation(
                type=RecommendationType.CONCURRENCY,
                priority=RecommendationPriority.HIGH,
                title="Increase Concurrency",
                description="Processing speed is low. Consider increasing concurrent request limits while respecting API rate limits.",
                current_value=f"{time_eff:.2f} ops/sec",
                recommended_value="5+ ops/sec",
                expected_improvement="2-3x performance improvement",
                implementation_effort="Medium"
            ))
        
        # Resource usage recommendations
        total_ops = performance_summary.get('total_operations', 0)
        if total_ops > 1000:  # For large operations
            recommendations.append(OptimizationRecommendation(
                type=RecommendationType.RESOURCE_USAGE,
                priority=RecommendationPriority.MEDIUM,
                title="Monitor Memory Usage",
                description="Large number of operations detected. Monitor memory usage and implement streaming for large batches.",
                current_value=f"{total_ops} operations",
                recommended_value="Streaming for 500+ operations",
                expected_improvement="Reduced memory usage and better scalability",
                implementation_effort="Medium"
            ))
        
        # Configuration recommendations
        if not recommendations:
            recommendations.append(OptimizationRecommendation(
                type=RecommendationType.CONFIGURATION,
                priority=RecommendationPriority.INFO,
                title="Performance Looks Good",
                description="Current performance metrics are within acceptable ranges. Continue monitoring for any degradation.",
                expected_improvement="Maintain current performance levels",
                implementation_effort="None"
            ))
        
        # Sort recommendations by priority
        priority_order = {
            RecommendationPriority.CRITICAL: 0,
            RecommendationPriority.HIGH: 1,
            RecommendationPriority.MEDIUM: 2,
            RecommendationPriority.LOW: 3,
            RecommendationPriority.INFO: 4
        }
        recommendations.sort(key=lambda x: priority_order[x.priority])
        
        return recommendations
    
    def _analyze_trends(self, metrics_collector: BatchMetricsCollector) -> Dict[str, Any]:
        """Analyze performance trends from metrics collector.
        
        Args:
            metrics_collector: BatchMetricsCollector with trend data
            
        Returns:
            Dictionary with trend analysis
        """
        trend_analysis = {}
        
        # Analyze performance trends for each operation type
        for op_type, trend in metrics_collector.performance_trends.items():
            if len(trend.durations) >= 5:
                recent_durations = list(trend.durations)[-10:]  # Last 10 measurements
                older_durations = list(trend.durations)[:-10] if len(trend.durations) > 10 else []
                
                trend_info = {
                    'is_improving': trend.is_improving,
                    'sample_count': len(trend.durations),
                    'recent_average': statistics.mean(recent_durations),
                }
                
                if older_durations:
                    older_average = statistics.mean(older_durations)
                    trend_info['improvement_percentage'] = (
                        (older_average - trend_info['recent_average']) / older_average * 100
                    )
                
                trend_analysis[op_type] = trend_info
        
        return trend_analysis
    
    def _perform_comparative_analysis(
        self, 
        current_metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """Perform comparative analysis with historical data.
        
        Args:
            current_metrics: Current efficiency metrics
            
        Returns:
            Dictionary with comparative analysis
        """
        comparative_analysis = {}
        
        if not self.historical_analyses:
            comparative_analysis['status'] = 'no_historical_data'
            return comparative_analysis
        
        # Compare with previous analysis
        if len(self.historical_analyses) >= 1:
            prev_metrics = self.historical_analyses[-1].efficiency_metrics
            
            comparisons = {}
            for metric, current_value in current_metrics.items():
                prev_value = prev_metrics.get(metric, 0)
                if prev_value > 0:
                    change_percentage = ((current_value - prev_value) / prev_value) * 100
                    comparisons[metric] = {
                        'current': current_value,
                        'previous': prev_value,
                        'change_percentage': change_percentage,
                        'trend': 'improving' if change_percentage > 5 else 'degrading' if change_percentage < -5 else 'stable'
                    }
            
            comparative_analysis['vs_previous'] = comparisons
        
        # Compare with baseline if available
        if self.baseline_metrics:
            baseline_comparisons = {}
            for metric, current_value in current_metrics.items():
                baseline_value = self.baseline_metrics.get(metric, 0)
                if baseline_value > 0:
                    change_percentage = ((current_value - baseline_value) / baseline_value) * 100
                    baseline_comparisons[metric] = {
                        'current': current_value,
                        'baseline': baseline_value,
                        'change_percentage': change_percentage
                    }
            
            comparative_analysis['vs_baseline'] = baseline_comparisons
        
        # Calculate average performance over time
        if len(self.historical_analyses) >= 3:
            avg_metrics = {}
            for metric in current_metrics.keys():
                values = [analysis.efficiency_metrics.get(metric, 0) 
                         for analysis in self.historical_analyses[-10:]]  # Last 10 analyses
                if values:
                    avg_metrics[metric] = statistics.mean(values)
            
            comparative_analysis['vs_recent_average'] = {
                metric: {
                    'current': current_metrics[metric],
                    'average': avg_value,
                    'vs_average': ((current_metrics[metric] - avg_value) / avg_value * 100) if avg_value > 0 else 0
                }
                for metric, avg_value in avg_metrics.items()
            }
        
        return comparative_analysis
    
    def set_baseline_metrics(self, metrics: Dict[str, float]) -> None:
        """Set baseline metrics for comparison.
        
        Args:
            metrics: Baseline efficiency metrics
        """
        self.baseline_metrics = metrics.copy()
        logger.info("Baseline metrics set for performance comparison")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of recent performance analyses.
        
        Returns:
            Dictionary with performance summary
        """
        if not self.historical_analyses:
            return {'status': 'no_data', 'message': 'No performance analyses available'}
        
        recent_analyses = self.historical_analyses[-5:]  # Last 5 analyses
        
        summary = {
            'total_analyses': len(self.historical_analyses),
            'recent_analyses_count': len(recent_analyses),
            'average_score': statistics.mean([a.overall_score for a in recent_analyses]),
            'score_trend': self._calculate_score_trend(recent_analyses),
            'common_bottlenecks': self._identify_common_bottlenecks(recent_analyses),
            'recommendation_categories': self._categorize_recommendations(recent_analyses)
        }
        
        return summary
    
    def _calculate_score_trend(self, analyses: List[PerformanceAnalysis]) -> str:
        """Calculate trend in performance scores.
        
        Args:
            analyses: List of recent performance analyses
            
        Returns:
            Trend description
        """
        if len(analyses) < 2:
            return 'insufficient_data'
        
        scores = [a.overall_score for a in analyses]
        
        # Simple trend calculation
        first_half = scores[:len(scores)//2]
        second_half = scores[len(scores)//2:]
        
        if not first_half or not second_half:
            return 'stable'
        
        first_avg = statistics.mean(first_half)
        second_avg = statistics.mean(second_half)
        
        change = ((second_avg - first_avg) / first_avg) * 100 if first_avg > 0 else 0
        
        if change > 10:
            return 'improving'
        elif change < -10:
            return 'degrading'
        else:
            return 'stable'
    
    def _identify_common_bottlenecks(self, analyses: List[PerformanceAnalysis]) -> List[str]:
        """Identify commonly occurring bottlenecks.
        
        Args:
            analyses: List of recent performance analyses
            
        Returns:
            List of common bottlenecks
        """
        bottleneck_counts = {}
        
        for analysis in analyses:
            for bottleneck in analysis.bottlenecks:
                # Extract the main issue type from the bottleneck description
                if 'cache' in bottleneck.lower():
                    key = 'cache_performance'
                elif 'slow' in bottleneck.lower():
                    key = 'processing_speed'
                elif 'failure' in bottleneck.lower() or 'error' in bottleneck.lower():
                    key = 'error_rate'
                elif 'strategy' in bottleneck.lower():
                    key = 'strategy_optimization'
                else:
                    key = 'other'
                
                bottleneck_counts[key] = bottleneck_counts.get(key, 0) + 1
        
        # Return bottlenecks that appear in more than half of the analyses
        threshold = len(analyses) / 2
        common_bottlenecks = [
            bottleneck for bottleneck, count in bottleneck_counts.items()
            if count > threshold
        ]
        
        return common_bottlenecks
    
    def _categorize_recommendations(self, analyses: List[PerformanceAnalysis]) -> Dict[str, int]:
        """Categorize recommendations by type.
        
        Args:
            analyses: List of recent performance analyses
            
        Returns:
            Dictionary with recommendation counts by category
        """
        category_counts = {}
        
        for analysis in analyses:
            for recommendation in analysis.recommendations:
                category = recommendation.type.value
                category_counts[category] = category_counts.get(category, 0) + 1
        
        return category_counts