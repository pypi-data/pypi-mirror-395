"""Tests for BatchPerformanceAnalyzer."""

import pytest
import statistics
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from src.github_ioc_scanner.batch_performance_analyzer import (
    BatchPerformanceAnalyzer,
    OptimizationRecommendation,
    PerformanceAnalysis,
    RecommendationPriority,
    RecommendationType
)
from src.github_ioc_scanner.batch_metrics_collector import BatchMetricsCollector, OperationMetrics
from src.github_ioc_scanner.batch_progress_monitor import BatchProgressMonitor
from src.github_ioc_scanner.batch_models import BatchStrategy


class TestOptimizationRecommendation:
    """Test OptimizationRecommendation functionality."""
    
    def test_recommendation_initialization(self):
        """Test OptimizationRecommendation initialization."""
        rec = OptimizationRecommendation(
            type=RecommendationType.CACHING,
            priority=RecommendationPriority.HIGH,
            title="Test Recommendation",
            description="Test description",
            current_value="10%",
            recommended_value="50%",
            expected_improvement="40% improvement",
            implementation_effort="Medium"
        )
        
        assert rec.type == RecommendationType.CACHING
        assert rec.priority == RecommendationPriority.HIGH
        assert rec.title == "Test Recommendation"
        assert rec.description == "Test description"
        assert rec.current_value == "10%"
        assert rec.recommended_value == "50%"
        assert rec.expected_improvement == "40% improvement"
        assert rec.implementation_effort == "Medium"
    
    def test_recommendation_to_dict(self):
        """Test converting recommendation to dictionary."""
        rec = OptimizationRecommendation(
            type=RecommendationType.BATCH_SIZE,
            priority=RecommendationPriority.MEDIUM,
            title="Increase Batch Size",
            description="Batch size is too small"
        )
        
        result = rec.to_dict()
        
        assert result['type'] == 'batch_size'
        assert result['priority'] == 'medium'
        assert result['title'] == 'Increase Batch Size'
        assert result['description'] == 'Batch size is too small'
        assert result['current_value'] is None
        assert result['recommended_value'] is None


class TestPerformanceAnalysis:
    """Test PerformanceAnalysis functionality."""
    
    def test_analysis_initialization(self):
        """Test PerformanceAnalysis initialization."""
        recommendations = [
            OptimizationRecommendation(
                type=RecommendationType.CACHING,
                priority=RecommendationPriority.HIGH,
                title="Test",
                description="Test"
            )
        ]
        
        analysis = PerformanceAnalysis(
            overall_score=85.5,
            efficiency_metrics={'cache_efficiency': 60.0},
            bottlenecks=['Low cache hit rate'],
            recommendations=recommendations,
            trend_analysis={'test_op': {'is_improving': True}},
            comparative_analysis={'vs_previous': {}}
        )
        
        assert analysis.overall_score == 85.5
        assert analysis.efficiency_metrics['cache_efficiency'] == 60.0
        assert len(analysis.bottlenecks) == 1
        assert len(analysis.recommendations) == 1
        assert 'test_op' in analysis.trend_analysis
        assert 'vs_previous' in analysis.comparative_analysis
    
    def test_analysis_to_dict(self):
        """Test converting analysis to dictionary."""
        recommendations = [
            OptimizationRecommendation(
                type=RecommendationType.CACHING,
                priority=RecommendationPriority.HIGH,
                title="Test",
                description="Test"
            )
        ]
        
        analysis = PerformanceAnalysis(
            overall_score=75.0,
            efficiency_metrics={'cache_efficiency': 50.0},
            bottlenecks=['Test bottleneck'],
            recommendations=recommendations,
            trend_analysis={},
            comparative_analysis={}
        )
        
        result = analysis.to_dict()
        
        assert result['overall_score'] == 75.0
        assert result['efficiency_metrics']['cache_efficiency'] == 50.0
        assert result['bottlenecks'] == ['Test bottleneck']
        assert len(result['recommendations']) == 1
        assert result['recommendations'][0]['type'] == 'caching'


class TestBatchPerformanceAnalyzer:
    """Test BatchPerformanceAnalyzer functionality."""
    
    def test_initialization(self):
        """Test BatchPerformanceAnalyzer initialization."""
        analyzer = BatchPerformanceAnalyzer()
        
        assert len(analyzer.historical_analyses) == 0
        assert analyzer.baseline_metrics is None
        assert 'min_success_rate' in analyzer.thresholds
        assert analyzer.thresholds['min_success_rate'] == 90.0
    
    def test_calculate_overall_score_good_performance(self):
        """Test overall score calculation with good performance."""
        analyzer = BatchPerformanceAnalyzer()
        
        efficiency_metrics = {
            'cache_efficiency': 80.0,
            'batch_efficiency': 95.0,
            'time_efficiency': 8.0,  # 8 ops/sec
            'overall_efficiency': 85.0
        }
        
        performance_summary = {
            'total_operations': 100,
            'operation_metrics': {
                'test_op': {
                    'total_operations': 100,
                    'success_rate': 95.0
                }
            }
        }
        
        score = analyzer._calculate_overall_score(efficiency_metrics, performance_summary)
        
        # Should be a high score for good performance
        assert score > 80.0
        assert score <= 100.0
    
    def test_calculate_overall_score_poor_performance(self):
        """Test overall score calculation with poor performance."""
        analyzer = BatchPerformanceAnalyzer()
        
        efficiency_metrics = {
            'cache_efficiency': 20.0,
            'batch_efficiency': 60.0,
            'time_efficiency': 1.0,  # 1 ops/sec
            'overall_efficiency': 30.0
        }
        
        performance_summary = {
            'total_operations': 100,
            'operation_metrics': {
                'test_op': {
                    'total_operations': 100,
                    'success_rate': 60.0
                }
            }
        }
        
        score = analyzer._calculate_overall_score(efficiency_metrics, performance_summary)
        
        # Should be a low score for poor performance
        assert score < 60.0
        assert score >= 0.0
    
    def test_identify_bottlenecks_cache_issues(self):
        """Test bottleneck identification for cache issues."""
        analyzer = BatchPerformanceAnalyzer()
        
        efficiency_metrics = {
            'cache_efficiency': 20.0,  # Below threshold
            'batch_efficiency': 95.0,
            'time_efficiency': 5.0
        }
        
        performance_summary = {
            'operation_metrics': {},
            'strategy_performance': {}
        }
        
        bottlenecks = analyzer._identify_bottlenecks(performance_summary, efficiency_metrics)
        
        assert len(bottlenecks) > 0
        assert any('cache' in bottleneck.lower() for bottleneck in bottlenecks)
    
    def test_identify_bottlenecks_slow_operations(self):
        """Test bottleneck identification for slow operations."""
        analyzer = BatchPerformanceAnalyzer()
        
        efficiency_metrics = {
            'cache_efficiency': 80.0,
            'batch_efficiency': 95.0,
            'time_efficiency': 5.0
        }
        
        performance_summary = {
            'operation_metrics': {
                'slow_op': {
                    'average_duration': 8.0,  # Above threshold
                    'success_rate': 95.0
                }
            },
            'strategy_performance': {}
        }
        
        bottlenecks = analyzer._identify_bottlenecks(performance_summary, efficiency_metrics)
        
        assert len(bottlenecks) > 0
        assert any('slow_op' in bottleneck for bottleneck in bottlenecks)
    
    def test_identify_bottlenecks_strategy_issues(self):
        """Test bottleneck identification for strategy performance issues."""
        analyzer = BatchPerformanceAnalyzer()
        
        efficiency_metrics = {
            'cache_efficiency': 80.0,
            'batch_efficiency': 95.0,
            'time_efficiency': 5.0
        }
        
        performance_summary = {
            'operation_metrics': {},
            'strategy_performance': {
                'parallel': {'average_duration': 1.0},
                'sequential': {'average_duration': 5.0}  # Much slower
            }
        }
        
        bottlenecks = analyzer._identify_bottlenecks(performance_summary, efficiency_metrics)
        
        assert len(bottlenecks) > 0
        assert any('sequential' in bottleneck.lower() for bottleneck in bottlenecks)
    
    def test_generate_recommendations_cache_optimization(self):
        """Test recommendation generation for cache optimization."""
        analyzer = BatchPerformanceAnalyzer()
        
        performance_summary = {
            'operation_metrics': {},
            'strategy_performance': {}
        }
        
        efficiency_metrics = {
            'cache_efficiency': 25.0,  # Low cache efficiency
            'batch_efficiency': 95.0,
            'time_efficiency': 5.0
        }
        
        # Create a mock metrics collector
        metrics_collector = MagicMock()
        metrics_collector.operation_metrics = {}
        
        recommendations = analyzer._generate_recommendations(
            performance_summary, efficiency_metrics, metrics_collector
        )
        
        assert len(recommendations) > 0
        cache_recs = [r for r in recommendations if r.type == RecommendationType.CACHING]
        assert len(cache_recs) > 0
        assert cache_recs[0].priority == RecommendationPriority.HIGH
    
    def test_generate_recommendations_batch_size(self):
        """Test recommendation generation for batch size optimization."""
        analyzer = BatchPerformanceAnalyzer()
        
        performance_summary = {
            'operation_metrics': {
                'test_op': {'total_operations': 10}
            },
            'strategy_performance': {}
        }
        
        efficiency_metrics = {
            'cache_efficiency': 80.0,
            'batch_efficiency': 95.0,
            'time_efficiency': 5.0
        }
        
        # Create a mock metrics collector with small batch sizes
        metrics_collector = MagicMock()
        op_metrics = OperationMetrics('test_op')
        op_metrics.total_operations = 10
        op_metrics.batch_sizes = [2, 3, 2, 3, 2]  # Small batch sizes
        metrics_collector.operation_metrics = {'test_op': op_metrics}
        
        recommendations = analyzer._generate_recommendations(
            performance_summary, efficiency_metrics, metrics_collector
        )
        
        batch_recs = [r for r in recommendations if r.type == RecommendationType.BATCH_SIZE]
        assert len(batch_recs) > 0
        assert 'increase' in batch_recs[0].title.lower()
    
    def test_generate_recommendations_error_handling(self):
        """Test recommendation generation for error handling."""
        analyzer = BatchPerformanceAnalyzer()
        
        performance_summary = {
            'operation_metrics': {},
            'strategy_performance': {}
        }
        
        efficiency_metrics = {
            'cache_efficiency': 80.0,
            'batch_efficiency': 70.0,  # Low batch efficiency (high failure rate)
            'time_efficiency': 5.0
        }
        
        metrics_collector = MagicMock()
        metrics_collector.operation_metrics = {}
        
        recommendations = analyzer._generate_recommendations(
            performance_summary, efficiency_metrics, metrics_collector
        )
        
        error_recs = [r for r in recommendations if r.type == RecommendationType.ERROR_HANDLING]
        assert len(error_recs) > 0
        assert error_recs[0].priority == RecommendationPriority.HIGH
    
    def test_generate_recommendations_good_performance(self):
        """Test recommendation generation with good performance."""
        analyzer = BatchPerformanceAnalyzer()
        
        performance_summary = {
            'operation_metrics': {},
            'strategy_performance': {}
        }
        
        efficiency_metrics = {
            'cache_efficiency': 80.0,
            'batch_efficiency': 95.0,
            'time_efficiency': 8.0
        }
        
        metrics_collector = MagicMock()
        metrics_collector.operation_metrics = {}
        
        recommendations = analyzer._generate_recommendations(
            performance_summary, efficiency_metrics, metrics_collector
        )
        
        # Should have at least one "performance looks good" recommendation
        assert len(recommendations) > 0
        info_recs = [r for r in recommendations if r.priority == RecommendationPriority.INFO]
        assert len(info_recs) > 0
    
    def test_analyze_performance_complete_flow(self):
        """Test complete performance analysis flow."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Create mock metrics collector
        metrics_collector = MagicMock()
        metrics_collector.get_performance_summary.return_value = {
            'total_operations': 100,
            'operation_metrics': {
                'test_op': {
                    'total_operations': 100,
                    'success_rate': 90.0,
                    'average_duration': 2.0
                }
            },
            'strategy_performance': {}
        }
        metrics_collector.get_efficiency_metrics.return_value = {
            'cache_efficiency': 60.0,
            'batch_efficiency': 90.0,
            'time_efficiency': 5.0,
            'overall_efficiency': 75.0
        }
        metrics_collector.operation_metrics = {}
        
        # Create mock progress monitor
        progress_monitor = MagicMock()
        progress_monitor.performance_trends = {}
        
        analysis = analyzer.analyze_performance(metrics_collector, progress_monitor)
        
        assert isinstance(analysis, PerformanceAnalysis)
        assert 0 <= analysis.overall_score <= 100
        assert isinstance(analysis.efficiency_metrics, dict)
        assert isinstance(analysis.bottlenecks, list)
        assert isinstance(analysis.recommendations, list)
        assert len(analyzer.historical_analyses) == 1
    
    def test_analyze_trends(self):
        """Test trend analysis from progress monitor."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Create mock progress monitor with trend data
        progress_monitor = MagicMock()
        
        # Mock trend with improving performance
        mock_trend = MagicMock()
        mock_trend.is_improving = True
        mock_trend.durations = [3.0, 2.8, 2.5, 2.3, 2.0, 1.8, 1.5, 1.3, 1.0, 0.8]
        
        progress_monitor.performance_trends = {'test_op': mock_trend}
        
        trend_analysis = analyzer._analyze_trends(progress_monitor)
        
        assert 'test_op' in trend_analysis
        assert trend_analysis['test_op']['is_improving'] is True
        assert 'recent_average' in trend_analysis['test_op']
        assert 'sample_count' in trend_analysis['test_op']
    
    def test_comparative_analysis_no_history(self):
        """Test comparative analysis with no historical data."""
        analyzer = BatchPerformanceAnalyzer()
        
        current_metrics = {
            'cache_efficiency': 60.0,
            'batch_efficiency': 90.0
        }
        
        comparative_analysis = analyzer._perform_comparative_analysis(current_metrics)
        
        assert comparative_analysis['status'] == 'no_historical_data'
    
    def test_comparative_analysis_with_history(self):
        """Test comparative analysis with historical data."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Add historical analysis
        prev_analysis = PerformanceAnalysis(
            overall_score=70.0,
            efficiency_metrics={
                'cache_efficiency': 50.0,
                'batch_efficiency': 80.0
            },
            bottlenecks=[],
            recommendations=[],
            trend_analysis={},
            comparative_analysis={}
        )
        analyzer.historical_analyses.append(prev_analysis)
        
        current_metrics = {
            'cache_efficiency': 60.0,
            'batch_efficiency': 90.0
        }
        
        comparative_analysis = analyzer._perform_comparative_analysis(current_metrics)
        
        assert 'vs_previous' in comparative_analysis
        assert 'cache_efficiency' in comparative_analysis['vs_previous']
        assert comparative_analysis['vs_previous']['cache_efficiency']['trend'] == 'improving'
    
    def test_set_baseline_metrics(self):
        """Test setting baseline metrics."""
        analyzer = BatchPerformanceAnalyzer()
        
        baseline = {
            'cache_efficiency': 70.0,
            'batch_efficiency': 85.0
        }
        
        analyzer.set_baseline_metrics(baseline)
        
        assert analyzer.baseline_metrics == baseline
    
    def test_get_performance_summary_no_data(self):
        """Test performance summary with no data."""
        analyzer = BatchPerformanceAnalyzer()
        
        summary = analyzer.get_performance_summary()
        
        assert summary['status'] == 'no_data'
        assert 'message' in summary
    
    def test_get_performance_summary_with_data(self):
        """Test performance summary with historical data."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Add some historical analyses
        for i in range(5):
            analysis = PerformanceAnalysis(
                overall_score=80.0 + i,
                efficiency_metrics={'cache_efficiency': 60.0 + i},
                bottlenecks=['cache_performance'] if i % 2 == 0 else [],
                recommendations=[
                    OptimizationRecommendation(
                        type=RecommendationType.CACHING,
                        priority=RecommendationPriority.HIGH,
                        title="Test",
                        description="Test"
                    )
                ],
                trend_analysis={},
                comparative_analysis={}
            )
            analyzer.historical_analyses.append(analysis)
        
        summary = analyzer.get_performance_summary()
        
        assert summary['total_analyses'] == 5
        assert summary['recent_analyses_count'] == 5
        assert 'average_score' in summary
        assert 'score_trend' in summary
        assert 'common_bottlenecks' in summary
        assert 'recommendation_categories' in summary
    
    def test_calculate_score_trend_improving(self):
        """Test score trend calculation for improving performance."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Create analyses with improving scores
        analyses = []
        for score in [60, 65, 70, 75, 80]:
            analysis = PerformanceAnalysis(
                overall_score=score,
                efficiency_metrics={},
                bottlenecks=[],
                recommendations=[],
                trend_analysis={},
                comparative_analysis={}
            )
            analyses.append(analysis)
        
        trend = analyzer._calculate_score_trend(analyses)
        
        assert trend == 'improving'
    
    def test_calculate_score_trend_degrading(self):
        """Test score trend calculation for degrading performance."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Create analyses with degrading scores
        analyses = []
        for score in [80, 75, 70, 65, 60]:
            analysis = PerformanceAnalysis(
                overall_score=score,
                efficiency_metrics={},
                bottlenecks=[],
                recommendations=[],
                trend_analysis={},
                comparative_analysis={}
            )
            analyses.append(analysis)
        
        trend = analyzer._calculate_score_trend(analyses)
        
        assert trend == 'degrading'
    
    def test_calculate_score_trend_stable(self):
        """Test score trend calculation for stable performance."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Create analyses with stable scores
        analyses = []
        for score in [75, 76, 74, 75, 76]:
            analysis = PerformanceAnalysis(
                overall_score=score,
                efficiency_metrics={},
                bottlenecks=[],
                recommendations=[],
                trend_analysis={},
                comparative_analysis={}
            )
            analyses.append(analysis)
        
        trend = analyzer._calculate_score_trend(analyses)
        
        assert trend == 'stable'
    
    def test_identify_common_bottlenecks(self):
        """Test identification of common bottlenecks."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Create analyses with common bottlenecks
        analyses = []
        for i in range(4):
            bottlenecks = ['Low cache hit rate detected']
            if i % 2 == 0:
                bottlenecks.append('Slow processing speed detected')
            
            analysis = PerformanceAnalysis(
                overall_score=75.0,
                efficiency_metrics={},
                bottlenecks=bottlenecks,
                recommendations=[],
                trend_analysis={},
                comparative_analysis={}
            )
            analyses.append(analysis)
        
        common_bottlenecks = analyzer._identify_common_bottlenecks(analyses)
        
        # Cache performance should be common (appears in all 4 analyses)
        assert 'cache_performance' in common_bottlenecks
        # Processing speed should not be common (appears in only 2 analyses)
        assert 'processing_speed' not in common_bottlenecks
    
    def test_categorize_recommendations(self):
        """Test categorization of recommendations."""
        analyzer = BatchPerformanceAnalyzer()
        
        # Create analyses with different recommendation types
        analyses = []
        for i in range(3):
            recommendations = [
                OptimizationRecommendation(
                    type=RecommendationType.CACHING,
                    priority=RecommendationPriority.HIGH,
                    title="Cache",
                    description="Cache"
                ),
                OptimizationRecommendation(
                    type=RecommendationType.BATCH_SIZE,
                    priority=RecommendationPriority.MEDIUM,
                    title="Batch",
                    description="Batch"
                )
            ]
            
            analysis = PerformanceAnalysis(
                overall_score=75.0,
                efficiency_metrics={},
                bottlenecks=[],
                recommendations=recommendations,
                trend_analysis={},
                comparative_analysis={}
            )
            analyses.append(analysis)
        
        categories = analyzer._categorize_recommendations(analyses)
        
        assert categories['caching'] == 3  # Appears in all 3 analyses
        assert categories['batch_size'] == 3  # Appears in all 3 analyses
    
    def test_recommendation_priority_sorting(self):
        """Test that recommendations are sorted by priority."""
        analyzer = BatchPerformanceAnalyzer()
        
        performance_summary = {'operation_metrics': {}, 'strategy_performance': {}}
        efficiency_metrics = {
            'cache_efficiency': 20.0,  # Will generate HIGH priority
            'batch_efficiency': 70.0,  # Will generate HIGH priority
            'time_efficiency': 1.0     # Will generate HIGH priority
        }
        
        metrics_collector = MagicMock()
        metrics_collector.operation_metrics = {}
        
        recommendations = analyzer._generate_recommendations(
            performance_summary, efficiency_metrics, metrics_collector
        )
        
        # Check that recommendations are sorted by priority
        priorities = [rec.priority for rec in recommendations]
        priority_values = [
            0 if p == RecommendationPriority.CRITICAL else
            1 if p == RecommendationPriority.HIGH else
            2 if p == RecommendationPriority.MEDIUM else
            3 if p == RecommendationPriority.LOW else 4
            for p in priorities
        ]
        
        # Should be sorted in ascending order (CRITICAL=0, HIGH=1, etc.)
        assert priority_values == sorted(priority_values)