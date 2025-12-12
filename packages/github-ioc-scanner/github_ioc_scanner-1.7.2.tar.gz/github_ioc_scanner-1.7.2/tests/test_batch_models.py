"""Tests for batch processing models."""

import asyncio
from datetime import datetime
from unittest.mock import Mock

import pytest

from src.github_ioc_scanner.batch_models import (
    BatchRequest,
    BatchResult,
    BatchMetrics,
    BatchConfig,
    BatchStrategy,
    NetworkConditions,
    PrioritizedFile,
    AsyncBatchContext,
    BatchRecoveryPlan
)
from src.github_ioc_scanner.models import Repository, FileContent


class TestBatchRequest:
    """Test BatchRequest model."""
    
    def test_batch_request_creation(self):
        """Test creating a batch request."""
        repo = Repository(
            name="test-repo",
            full_name="owner/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        request = BatchRequest(
            repo=repo,
            file_path="package.json",
            priority=10,
            estimated_size=1024
        )
        
        assert request.repo == repo
        assert request.file_path == "package.json"
        assert request.priority == 10
        assert request.estimated_size == 1024
        assert request.cache_key == "owner/test-repo:package.json"
    
    def test_batch_request_custom_cache_key(self):
        """Test batch request with custom cache key."""
        repo = Repository(
            name="test-repo",
            full_name="owner/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        request = BatchRequest(
            repo=repo,
            file_path="package.json",
            cache_key="custom-key"
        )
        
        assert request.cache_key == "custom-key"


class TestBatchResult:
    """Test BatchResult model."""
    
    def test_batch_result_success(self):
        """Test successful batch result."""
        repo = Repository(
            name="test-repo",
            full_name="owner/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        request = BatchRequest(repo=repo, file_path="package.json")
        content = FileContent(content='{"name": "test"}', sha="abc123", size=15)
        
        result = BatchResult(
            request=request,
            content=content,
            processing_time=0.5
        )
        
        assert result.success is True
        assert result.content == content
        assert result.error is None
        assert result.processing_time == 0.5
    
    def test_batch_result_failure(self):
        """Test failed batch result."""
        repo = Repository(
            name="test-repo",
            full_name="owner/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        request = BatchRequest(repo=repo, file_path="package.json")
        error = Exception("Network error")
        
        result = BatchResult(
            request=request,
            error=error,
            processing_time=1.0
        )
        
        assert result.success is False
        assert result.content is None
        assert result.error == error
        assert result.processing_time == 1.0


class TestBatchMetrics:
    """Test BatchMetrics model."""
    
    def test_batch_metrics_initialization(self):
        """Test batch metrics initialization."""
        metrics = BatchMetrics()
        
        assert metrics.total_requests == 0
        assert metrics.successful_requests == 0
        assert metrics.failed_requests == 0
        assert metrics.cache_hits == 0
        assert metrics.cache_misses == 0
        assert metrics.start_time is not None
        assert metrics.end_time is None
    
    def test_batch_metrics_success_rate(self):
        """Test success rate calculation."""
        metrics = BatchMetrics()
        metrics.total_requests = 10
        metrics.successful_requests = 8
        
        assert metrics.success_rate == 80.0
    
    def test_batch_metrics_cache_hit_rate(self):
        """Test cache hit rate calculation."""
        metrics = BatchMetrics()
        metrics.cache_hits = 7
        metrics.cache_misses = 3
        
        assert metrics.cache_hit_rate == 70.0
    
    def test_batch_metrics_add_result(self):
        """Test adding results to metrics."""
        repo = Repository(
            name="test-repo",
            full_name="owner/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        request = BatchRequest(repo=repo, file_path="package.json")
        content = FileContent(content='{"name": "test"}', sha="abc123", size=15)
        
        # Successful result
        success_result = BatchResult(
            request=request,
            content=content,
            from_cache=True,
            processing_time=0.5
        )
        
        # Failed result
        failed_result = BatchResult(
            request=request,
            error=Exception("Error"),
            processing_time=1.0
        )
        
        metrics = BatchMetrics()
        metrics.add_result(success_result)
        metrics.add_result(failed_result)
        
        assert metrics.total_requests == 2
        assert metrics.successful_requests == 1
        assert metrics.failed_requests == 1
        assert metrics.cache_hits == 1
        assert metrics.cache_misses == 1
        assert metrics.total_processing_time == 1.5


class TestBatchConfig:
    """Test BatchConfig model."""
    
    def test_batch_config_defaults(self):
        """Test default batch configuration."""
        config = BatchConfig()
        
        # Updated defaults optimized for maximum speed
        assert config.max_concurrent_requests == 50
        assert config.max_concurrent_repos == 15
        assert config.default_batch_size == 25
        assert config.max_batch_size == 100
        assert config.min_batch_size == 5
        assert config.rate_limit_buffer == 0.95
        assert config.retry_attempts == 5
        assert config.default_strategy == BatchStrategy.ADAPTIVE
    
    def test_batch_config_validation_success(self):
        """Test successful batch config validation."""
        config = BatchConfig()
        errors = config.validate()
        
        assert len(errors) == 0
    
    def test_batch_config_validation_errors(self):
        """Test batch config validation with errors."""
        config = BatchConfig(
            max_concurrent_requests=0,
            min_batch_size=0,
            max_batch_size=5,
            rate_limit_buffer=1.5,
            retry_attempts=-1
        )
        config.min_batch_size = 10  # Make max < min
        
        errors = config.validate()
        
        assert len(errors) > 0
        assert any("max_concurrent_requests" in error for error in errors)
        assert any("min_batch_size" in error for error in errors)
        assert any("max_batch_size" in error for error in errors)
        assert any("rate_limit_buffer" in error for error in errors)
        assert any("retry_attempts" in error for error in errors)


class TestNetworkConditions:
    """Test NetworkConditions model."""
    
    def test_network_conditions_good(self):
        """Test good network conditions."""
        conditions = NetworkConditions(
            latency_ms=50,
            bandwidth_mbps=50,
            error_rate=0.01
        )
        
        assert conditions.is_good is True
    
    def test_network_conditions_bad(self):
        """Test bad network conditions."""
        conditions = NetworkConditions(
            latency_ms=500,
            bandwidth_mbps=1,
            error_rate=0.1
        )
        
        assert conditions.is_good is False


class TestPrioritizedFile:
    """Test PrioritizedFile model."""
    
    def test_prioritized_file_high_priority(self):
        """Test high priority file detection when priority is 0."""
        file = PrioritizedFile(
            path="package.json",
            priority=0,  # Priority 0 triggers auto-detection
            file_type="json",
            estimated_size=1024
        )
        
        assert file.priority >= 10  # Should be upgraded to high priority
        assert file.security_importance >= 2.0
    
    def test_prioritized_file_normal_priority(self):
        """Test normal priority file."""
        file = PrioritizedFile(
            path="src/main.py",
            priority=5,
            file_type="python",
            estimated_size=2048
        )
        
        assert file.priority == 5  # Should remain unchanged
        assert file.security_importance == 1.0


class TestAsyncBatchContext:
    """Test AsyncBatchContext model."""
    
    def test_async_batch_context_creation(self):
        """Test creating async batch context."""
        context = AsyncBatchContext(
            semaphore=asyncio.Semaphore(5)
        )
        
        assert context.semaphore._value == 5
        assert context.rate_limit_remaining == 5000
        assert context.current_strategy == BatchStrategy.ADAPTIVE


class TestBatchRecoveryPlan:
    """Test BatchRecoveryPlan model."""
    
    def test_batch_recovery_plan_empty(self):
        """Test empty recovery plan."""
        plan = BatchRecoveryPlan()
        
        assert plan.has_retries is False
        assert plan.total_requests == 0
    
    def test_batch_recovery_plan_with_retries(self):
        """Test recovery plan with retries."""
        repo = Repository(
            name="test-repo",
            full_name="owner/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        retry_request = BatchRequest(repo=repo, file_path="package.json")
        skip_request = BatchRequest(repo=repo, file_path="README.md")
        
        plan = BatchRecoveryPlan(
            retry_requests=[retry_request],
            skip_requests=[skip_request],
            fallback_strategy=BatchStrategy.SEQUENTIAL,
            delay_seconds=5.0
        )
        
        assert plan.has_retries is True
        assert plan.total_requests == 2
        assert plan.fallback_strategy == BatchStrategy.SEQUENTIAL
        assert plan.delay_seconds == 5.0