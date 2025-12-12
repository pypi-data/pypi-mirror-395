"""Tests for BatchConfig class and configuration validation."""

import pytest
from src.github_ioc_scanner.batch_models import BatchConfig, BatchStrategy


class TestBatchConfig:
    """Test BatchConfig class functionality."""
    
    def test_default_configuration(self):
        """Test that default configuration is valid."""
        config = BatchConfig()
        
        # Test default values (optimized for maximum speed)
        assert config.max_concurrent_requests == 50
        assert config.max_concurrent_repos == 15
        assert config.default_batch_size == 25
        assert config.max_batch_size == 100
        assert config.min_batch_size == 5
        assert config.rate_limit_buffer == 0.95
        assert config.retry_attempts == 5
        assert config.retry_delay_base == 0.5
        assert config.max_memory_usage_mb == 500
        assert config.stream_large_files_threshold == 1024 * 1024
        assert config.default_strategy == BatchStrategy.ADAPTIVE
        assert config.enable_cross_repo_batching is True
        assert config.enable_file_prioritization is True
        assert config.enable_performance_monitoring is True
        assert config.log_batch_metrics is False
        
        # Test validation passes
        errors = config.validate()
        assert len(errors) == 0
    
    def test_custom_configuration(self):
        """Test custom configuration values."""
        config = BatchConfig(
            max_concurrent_requests=20,
            max_concurrent_repos=5,
            default_batch_size=15,
            max_batch_size=100,
            min_batch_size=2,
            rate_limit_buffer=0.9,
            retry_attempts=5,
            retry_delay_base=2.0,
            max_memory_usage_mb=1000,
            stream_large_files_threshold=2 * 1024 * 1024,
            default_strategy=BatchStrategy.AGGRESSIVE,
            enable_cross_repo_batching=False,
            enable_file_prioritization=False,
            enable_performance_monitoring=False,
            log_batch_metrics=True
        )
        
        assert config.max_concurrent_requests == 20
        assert config.max_concurrent_repos == 5
        assert config.default_batch_size == 15
        assert config.max_batch_size == 100
        assert config.min_batch_size == 2
        assert config.rate_limit_buffer == 0.9
        assert config.retry_attempts == 5
        assert config.retry_delay_base == 2.0
        assert config.max_memory_usage_mb == 1000
        assert config.stream_large_files_threshold == 2 * 1024 * 1024
        assert config.default_strategy == BatchStrategy.AGGRESSIVE
        assert config.enable_cross_repo_batching is False
        assert config.enable_file_prioritization is False
        assert config.enable_performance_monitoring is False
        assert config.log_batch_metrics is True
        
        # Test validation passes
        errors = config.validate()
        assert len(errors) == 0
    
    def test_validation_max_concurrent_requests_invalid(self):
        """Test validation fails for invalid max_concurrent_requests."""
        config = BatchConfig(max_concurrent_requests=0)
        errors = config.validate()
        assert len(errors) == 1
        assert "max_concurrent_requests must be at least 1" in errors
        
        config = BatchConfig(max_concurrent_requests=-1)
        errors = config.validate()
        assert len(errors) == 1
        assert "max_concurrent_requests must be at least 1" in errors
    
    def test_validation_max_concurrent_repos_invalid(self):
        """Test validation fails for invalid max_concurrent_repos."""
        config = BatchConfig(max_concurrent_repos=0)
        errors = config.validate()
        assert len(errors) == 1
        assert "max_concurrent_repos must be at least 1" in errors
        
        config = BatchConfig(max_concurrent_repos=-1)
        errors = config.validate()
        assert len(errors) == 1
        assert "max_concurrent_repos must be at least 1" in errors
    
    def test_validation_min_batch_size_invalid(self):
        """Test validation fails for invalid min_batch_size."""
        config = BatchConfig(min_batch_size=0)
        errors = config.validate()
        assert len(errors) == 1
        assert "min_batch_size must be at least 1" in errors
        
        config = BatchConfig(min_batch_size=-1)
        errors = config.validate()
        assert len(errors) == 1
        assert "min_batch_size must be at least 1" in errors
    
    def test_validation_batch_size_relationship_invalid(self):
        """Test validation fails when max_batch_size < min_batch_size."""
        config = BatchConfig(min_batch_size=10, max_batch_size=5)
        errors = config.validate()
        assert len(errors) == 1
        assert "max_batch_size must be >= min_batch_size" in errors
    
    def test_validation_rate_limit_buffer_invalid(self):
        """Test validation fails for invalid rate_limit_buffer."""
        config = BatchConfig(rate_limit_buffer=0.05)  # Too low
        errors = config.validate()
        assert len(errors) == 1
        assert "rate_limit_buffer must be between 0.1 and 1.0" in errors
        
        config = BatchConfig(rate_limit_buffer=1.5)  # Too high
        errors = config.validate()
        assert len(errors) == 1
        assert "rate_limit_buffer must be between 0.1 and 1.0" in errors
        
        config = BatchConfig(rate_limit_buffer=0.0)  # Zero
        errors = config.validate()
        assert len(errors) == 1
        assert "rate_limit_buffer must be between 0.1 and 1.0" in errors
    
    def test_validation_retry_attempts_invalid(self):
        """Test validation fails for invalid retry_attempts."""
        config = BatchConfig(retry_attempts=-1)
        errors = config.validate()
        assert len(errors) == 1
        assert "retry_attempts must be non-negative" in errors
    
    def test_validation_multiple_errors(self):
        """Test validation returns multiple errors when multiple issues exist."""
        config = BatchConfig(
            max_concurrent_requests=0,
            max_concurrent_repos=-1,
            min_batch_size=0,
            max_batch_size=0,  # This will be equal to min_batch_size, so no batch size relationship error
            rate_limit_buffer=2.0,
            retry_attempts=-5
        )
        
        errors = config.validate()
        assert len(errors) == 5  # All validation errors should be present
        
        expected_errors = [
            "max_concurrent_requests must be at least 1",
            "max_concurrent_repos must be at least 1",
            "min_batch_size must be at least 1",
            "rate_limit_buffer must be between 0.1 and 1.0",
            "retry_attempts must be non-negative"
        ]
        
        for expected_error in expected_errors:
            assert expected_error in errors
    
    def test_validation_batch_size_relationship_with_other_errors(self):
        """Test validation includes batch size relationship error with other errors."""
        config = BatchConfig(
            max_concurrent_requests=0,
            min_batch_size=10,
            max_batch_size=5,  # This will trigger the batch size relationship error
            rate_limit_buffer=2.0
        )
        
        errors = config.validate()
        assert len(errors) == 3
        
        expected_errors = [
            "max_concurrent_requests must be at least 1",
            "max_batch_size must be >= min_batch_size",
            "rate_limit_buffer must be between 0.1 and 1.0"
        ]
        
        for expected_error in expected_errors:
            assert expected_error in errors
    
    def test_validation_edge_cases_valid(self):
        """Test validation passes for edge case valid values."""
        config = BatchConfig(
            max_concurrent_requests=1,
            max_concurrent_repos=1,
            min_batch_size=1,
            max_batch_size=1,
            rate_limit_buffer=0.1,  # Minimum valid value
            retry_attempts=0  # Zero retries is valid
        )
        
        errors = config.validate()
        assert len(errors) == 0
        
        config = BatchConfig(
            rate_limit_buffer=1.0  # Maximum valid value
        )
        
        errors = config.validate()
        assert len(errors) == 0
    
    def test_batch_strategy_enum_values(self):
        """Test that all BatchStrategy enum values work with config."""
        for strategy in BatchStrategy:
            config = BatchConfig(default_strategy=strategy)
            errors = config.validate()
            assert len(errors) == 0
            assert config.default_strategy == strategy
    
    def test_memory_and_streaming_settings(self):
        """Test memory and streaming configuration options."""
        config = BatchConfig(
            max_memory_usage_mb=1024,
            stream_large_files_threshold=5 * 1024 * 1024  # 5MB
        )
        
        assert config.max_memory_usage_mb == 1024
        assert config.stream_large_files_threshold == 5 * 1024 * 1024
        
        errors = config.validate()
        assert len(errors) == 0
    
    def test_boolean_flags(self):
        """Test boolean configuration flags."""
        config = BatchConfig(
            enable_cross_repo_batching=False,
            enable_file_prioritization=False,
            enable_performance_monitoring=False,
            log_batch_metrics=True
        )
        
        assert config.enable_cross_repo_batching is False
        assert config.enable_file_prioritization is False
        assert config.enable_performance_monitoring is False
        assert config.log_batch_metrics is True
        
        errors = config.validate()
        assert len(errors) == 0


class TestBatchConfigIntegration:
    """Test BatchConfig integration with other components."""
    
    def test_config_for_conservative_strategy(self):
        """Test configuration suitable for conservative batching."""
        config = BatchConfig(
            max_concurrent_requests=3,
            max_concurrent_repos=1,
            default_batch_size=5,
            max_batch_size=10,
            rate_limit_buffer=0.5,
            retry_attempts=5,
            default_strategy=BatchStrategy.CONSERVATIVE
        )
        
        errors = config.validate()
        assert len(errors) == 0
        assert config.default_strategy == BatchStrategy.CONSERVATIVE
    
    def test_config_for_aggressive_strategy(self):
        """Test configuration suitable for aggressive batching."""
        config = BatchConfig(
            max_concurrent_requests=50,
            max_concurrent_repos=10,
            default_batch_size=25,
            max_batch_size=100,
            rate_limit_buffer=0.9,
            retry_attempts=2,
            default_strategy=BatchStrategy.AGGRESSIVE
        )
        
        errors = config.validate()
        assert len(errors) == 0
        assert config.default_strategy == BatchStrategy.AGGRESSIVE
    
    def test_config_for_memory_constrained_environment(self):
        """Test configuration for memory-constrained environments."""
        config = BatchConfig(
            max_memory_usage_mb=128,
            stream_large_files_threshold=256 * 1024,  # 256KB
            max_batch_size=5,
            default_batch_size=3
        )
        
        errors = config.validate()
        assert len(errors) == 0
        assert config.max_memory_usage_mb == 128
        assert config.stream_large_files_threshold == 256 * 1024
    
    def test_config_for_high_performance_environment(self):
        """Test configuration for high-performance environments."""
        config = BatchConfig(
            max_concurrent_requests=100,
            max_concurrent_repos=20,
            max_memory_usage_mb=2048,
            stream_large_files_threshold=10 * 1024 * 1024,  # 10MB
            max_batch_size=200,
            default_batch_size=50,
            rate_limit_buffer=0.95
        )
        
        errors = config.validate()
        assert len(errors) == 0
        assert config.max_concurrent_requests == 100
        assert config.max_memory_usage_mb == 2048