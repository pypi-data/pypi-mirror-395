"""Tests for retry manager."""

import asyncio
import pytest
import time
from unittest.mock import AsyncMock, patch

from src.github_ioc_scanner.retry_manager import (
    RetryManager, RetryConfig, RetryStrategy, RetryAttempt, RetryStatistics,
    retry_on_error
)
from src.github_ioc_scanner.exceptions import (
    RateLimitError, NetworkError, APIError, AuthenticationError
)


@pytest.fixture
def retry_config():
    """Create a test retry configuration."""
    return RetryConfig(
        max_attempts=3,
        base_delay=0.1,  # Short delays for testing
        max_delay=10.0,  # Higher max delay for testing
        backoff_multiplier=2.0,
        jitter_range=0.1
    )


@pytest.fixture
def retry_manager(retry_config):
    """Create a retry manager for testing."""
    return RetryManager(retry_config)


class TestRetryConfig:
    """Test cases for RetryConfig."""
    
    def test_retry_config_creation(self):
        """Test RetryConfig creation with defaults."""
        config = RetryConfig()
        
        assert config.max_attempts == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.backoff_multiplier == 2.0
        assert config.jitter_range == 0.1
        assert config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF
    
    def test_retry_config_validation_valid(self):
        """Test valid retry configuration."""
        config = RetryConfig(
            max_attempts=5,
            base_delay=0.5,
            max_delay=30.0,
            backoff_multiplier=1.5,
            jitter_range=0.2
        )
        
        errors = config.validate()
        assert len(errors) == 0
    
    def test_retry_config_validation_invalid(self):
        """Test invalid retry configuration."""
        config = RetryConfig(
            max_attempts=0,  # Invalid
            base_delay=-1.0,  # Invalid
            max_delay=0.5,  # Invalid (less than base_delay when base_delay is positive)
            backoff_multiplier=1.0,  # Invalid
            jitter_range=1.5  # Invalid
        )
        
        errors = config.validate()
        assert len(errors) > 0
        assert any("max_attempts" in error for error in errors)
        assert any("base_delay" in error for error in errors)
        # Since base_delay is negative, max_delay validation might not trigger
        # Let's test with a different configuration for max_delay
        assert any("backoff_multiplier" in error for error in errors)
        assert any("jitter_range" in error for error in errors)
        
        # Test max_delay validation separately with positive base_delay
        config2 = RetryConfig(base_delay=1.0, max_delay=0.5)
        errors2 = config2.validate()
        assert any("max_delay" in error for error in errors2)


class TestRetryAttempt:
    """Test cases for RetryAttempt."""
    
    def test_retry_attempt_creation(self):
        """Test RetryAttempt creation."""
        error = NetworkError("Connection timeout")
        attempt = RetryAttempt(
            attempt_number=1,
            delay_seconds=2.5,
            error=error
        )
        
        assert attempt.attempt_number == 1
        assert attempt.delay_seconds == 2.5
        assert attempt.error == error
        assert attempt.error_type == "NetworkError"
        assert attempt.timestamp is not None


class TestRetryStatistics:
    """Test cases for RetryStatistics."""
    
    def test_retry_statistics_creation(self):
        """Test RetryStatistics creation with defaults."""
        stats = RetryStatistics()
        
        assert stats.total_operations == 0
        assert stats.successful_operations == 0
        assert stats.failed_operations == 0
        assert stats.total_retry_attempts == 0
        assert stats.total_retry_delay == 0.0
        assert stats.success_rate == 0.0
        assert stats.average_retry_delay == 0.0
        assert stats.retry_rate == 0.0
    
    def test_retry_statistics_calculations(self):
        """Test RetryStatistics calculations."""
        stats = RetryStatistics(
            total_operations=10,
            successful_operations=8,
            failed_operations=2,
            total_retry_attempts=5,
            total_retry_delay=12.5
        )
        
        assert stats.success_rate == 80.0
        assert stats.average_retry_delay == 2.5
        assert stats.retry_rate == 50.0


class TestRetryManager:
    """Test cases for RetryManager."""
    
    def test_initialization(self, retry_manager, retry_config):
        """Test retry manager initialization."""
        assert retry_manager.config == retry_config
        assert retry_manager.statistics.total_operations == 0
        assert len(retry_manager.retry_history) == 0
        assert retry_manager.circuit_breaker_failures == 0
    
    def test_initialization_with_invalid_config(self):
        """Test retry manager initialization with invalid config."""
        invalid_config = RetryConfig(max_attempts=0)
        
        with pytest.raises(ValueError, match="Invalid retry configuration"):
            RetryManager(invalid_config)
    
    @pytest.mark.asyncio
    async def test_successful_operation_no_retry(self, retry_manager):
        """Test successful operation without retries."""
        async def successful_operation():
            return "success"
        
        result = await retry_manager.execute_with_retry(
            successful_operation,
            "test_operation"
        )
        
        assert result == "success"
        assert retry_manager.statistics.total_operations == 1
        assert retry_manager.statistics.successful_operations == 1
        assert retry_manager.statistics.failed_operations == 0
        assert retry_manager.statistics.total_retry_attempts == 0
    
    @pytest.mark.asyncio
    async def test_operation_with_retries_eventual_success(self, retry_manager):
        """Test operation that fails initially but succeeds on retry."""
        call_count = 0
        
        async def flaky_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise NetworkError("Temporary network error")
            return "success"
        
        result = await retry_manager.execute_with_retry(
            flaky_operation,
            "flaky_operation"
        )
        
        assert result == "success"
        assert call_count == 3
        assert retry_manager.statistics.total_operations == 1
        assert retry_manager.statistics.successful_operations == 1
        assert retry_manager.statistics.total_retry_attempts == 2
    
    @pytest.mark.asyncio
    async def test_operation_fails_all_retries(self, retry_manager):
        """Test operation that fails all retry attempts."""
        async def failing_operation():
            raise NetworkError("Persistent network error")
        
        with pytest.raises(NetworkError):
            await retry_manager.execute_with_retry(
                failing_operation,
                "failing_operation"
            )
        
        assert retry_manager.statistics.total_operations == 1
        assert retry_manager.statistics.successful_operations == 0
        assert retry_manager.statistics.failed_operations == 1
        assert retry_manager.statistics.total_retry_attempts == retry_manager.config.max_attempts - 1
    
    @pytest.mark.asyncio
    async def test_non_retryable_error(self, retry_manager):
        """Test operation with non-retryable error."""
        async def auth_error_operation():
            raise AuthenticationError("Invalid credentials")
        
        with pytest.raises(AuthenticationError):
            await retry_manager.execute_with_retry(
                auth_error_operation,
                "auth_operation"
            )
        
        assert retry_manager.statistics.total_operations == 1
        assert retry_manager.statistics.failed_operations == 1
        assert retry_manager.statistics.total_retry_attempts == 0  # No retries for auth errors
    
    @pytest.mark.asyncio
    async def test_rate_limit_error_with_reset_time(self, retry_manager):
        """Test rate limit error with reset time."""
        call_count = 0
        
        async def rate_limited_operation():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # First call hits rate limit
                raise RateLimitError("Rate limit exceeded", reset_time=int(time.time()) + 1)
            return "success"
        
        # Mock time.sleep to avoid actual waiting
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            result = await retry_manager.execute_with_retry(
                rate_limited_operation,
                "rate_limited_operation"
            )
        
        assert result == "success"
        assert call_count == 2
        assert mock_sleep.called
    
    def test_is_retryable_error(self, retry_manager):
        """Test retryable error detection."""
        config = retry_manager.config
        
        # Test retryable errors
        assert retry_manager._is_retryable_error(NetworkError("test"), config)
        assert retry_manager._is_retryable_error(RateLimitError("test"), config)
        assert retry_manager._is_retryable_error(APIError("test", status_code=500), config)
        
        # Test non-retryable errors
        assert not retry_manager._is_retryable_error(AuthenticationError("test"), config)
        assert not retry_manager._is_retryable_error(APIError("test", status_code=404), config)
        assert not retry_manager._is_retryable_error(ValueError("test"), config)
    
    def test_calculate_retry_delay_exponential(self, retry_manager):
        """Test exponential backoff delay calculation."""
        config = retry_manager.config
        error = NetworkError("test")
        
        delay1 = retry_manager._calculate_retry_delay(0, error, config, "test")
        delay2 = retry_manager._calculate_retry_delay(1, error, config, "test")
        delay3 = retry_manager._calculate_retry_delay(2, error, config, "test")
        
        # Should increase exponentially (accounting for jitter)
        assert delay1 < delay2 < delay3
        assert all(delay <= config.max_delay for delay in [delay1, delay2, delay3])
    
    def test_calculate_retry_delay_rate_limit(self, retry_manager):
        """Test rate limit specific delay calculation."""
        config = retry_manager.config
        
        # Rate limit error with reset time
        reset_time = int(time.time()) + 5
        rate_limit_error = RateLimitError("Rate limit exceeded", reset_time=reset_time)
        
        delay = retry_manager._calculate_retry_delay(0, rate_limit_error, config, "test")
        
        # Should use reset time for rate limit errors
        assert 4 <= delay <= 6  # Allow for small timing differences
    
    def test_fibonacci_calculation(self, retry_manager):
        """Test Fibonacci number calculation."""
        assert retry_manager._fibonacci(0) == 0
        assert retry_manager._fibonacci(1) == 1
        assert retry_manager._fibonacci(2) == 1
        assert retry_manager._fibonacci(3) == 2
        assert retry_manager._fibonacci(4) == 3
        assert retry_manager._fibonacci(5) == 5
        assert retry_manager._fibonacci(6) == 8
    
    def test_circuit_breaker_functionality(self, retry_manager):
        """Test circuit breaker functionality."""
        # Initially closed
        assert not retry_manager._is_circuit_breaker_open()
        
        # Record failures to open circuit breaker
        for _ in range(retry_manager.circuit_breaker_threshold):
            retry_manager._record_circuit_breaker_failure()
        
        # Should be open now
        assert retry_manager._is_circuit_breaker_open()
        
        # Reset circuit breaker
        retry_manager._reset_circuit_breaker()
        assert not retry_manager._is_circuit_breaker_open()
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_prevents_execution(self, retry_manager):
        """Test that open circuit breaker prevents operation execution."""
        # Force circuit breaker open
        retry_manager.circuit_breaker_failures = retry_manager.circuit_breaker_threshold
        retry_manager.circuit_breaker_reset_time = time.time() + 300
        
        async def test_operation():
            return "should not execute"
        
        with pytest.raises(APIError, match="Circuit breaker is open"):
            await retry_manager.execute_with_retry(test_operation, "test")
    
    def test_get_statistics(self, retry_manager):
        """Test getting retry statistics."""
        stats = retry_manager.get_statistics()
        assert isinstance(stats, RetryStatistics)
        assert stats.total_operations == 0
    
    def test_get_recent_retry_history(self, retry_manager):
        """Test getting recent retry history."""
        # Initially empty
        history = retry_manager.get_recent_retry_history()
        assert len(history) == 0
        
        # Add some retry attempts
        attempt1 = RetryAttempt(1, 1.0, NetworkError("test1"))
        attempt2 = RetryAttempt(2, 2.0, NetworkError("test2"))
        retry_manager.retry_history = [attempt1, attempt2]
        
        history = retry_manager.get_recent_retry_history()
        assert len(history) == 2
        assert history[0] == attempt1
        assert history[1] == attempt2
        
        # Test limit
        history_limited = retry_manager.get_recent_retry_history(limit=1)
        assert len(history_limited) == 1
        assert history_limited[0] == attempt2  # Most recent
    
    def test_reset_statistics(self, retry_manager):
        """Test resetting statistics."""
        # Add some data
        retry_manager.statistics.total_operations = 5
        retry_manager.retry_history = [RetryAttempt(1, 1.0, NetworkError("test"))]
        
        retry_manager.reset_statistics()
        
        assert retry_manager.statistics.total_operations == 0
        assert len(retry_manager.retry_history) == 0
    
    def test_create_error_specific_config(self, retry_manager):
        """Test creating error-specific configuration."""
        # Test rate limit error config
        rate_limit_config = retry_manager.create_error_specific_config(
            RateLimitError, max_attempts=5, base_delay=2.0
        )
        
        assert rate_limit_config.max_attempts == 5
        assert rate_limit_config.base_delay == 2.0
        
        # Test network error config
        network_config = retry_manager.create_error_specific_config(NetworkError)
        
        assert network_config.max_attempts == retry_manager.config.network_max_attempts
        assert network_config.base_delay == retry_manager.config.network_base_delay
    
    def test_get_circuit_breaker_status(self, retry_manager):
        """Test getting circuit breaker status."""
        status = retry_manager.get_circuit_breaker_status()
        
        assert 'is_open' in status
        assert 'failure_count' in status
        assert 'threshold' in status
        assert 'reset_time' in status
        assert 'timeout_seconds' in status
        
        assert status['is_open'] == False
        assert status['failure_count'] == 0
        assert status['threshold'] == retry_manager.circuit_breaker_threshold


class TestRetryStrategies:
    """Test different retry strategies."""
    
    @pytest.mark.asyncio
    async def test_exponential_backoff_strategy(self):
        """Test exponential backoff strategy."""
        config = RetryConfig(
            max_attempts=4,
            base_delay=0.1,
            max_delay=10.0,  # Higher max delay
            network_base_delay=0.1,  # Override network base delay
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
            jitter_range=0.0  # No jitter for predictable testing
        )
        retry_manager = RetryManager(config)
        
        delays = []
        for attempt in range(3):
            delay = retry_manager._calculate_retry_delay(
                attempt, NetworkError("test"), config, "test"
            )
            delays.append(delay)
        
        # Should be exponentially increasing
        assert delays[0] < delays[1] < delays[2]
        assert abs(delays[0] - 0.1) < 0.01  # Base delay
        assert abs(delays[1] - 0.2) < 0.01  # Base * 2^1
        assert abs(delays[2] - 0.4) < 0.01  # Base * 2^2
    
    @pytest.mark.asyncio
    async def test_linear_backoff_strategy(self):
        """Test linear backoff strategy."""
        config = RetryConfig(
            max_attempts=4,
            base_delay=0.1,
            max_delay=10.0,  # Higher max delay
            network_base_delay=0.1,  # Override network base delay
            strategy=RetryStrategy.LINEAR_BACKOFF,
            jitter_range=0.0
        )
        retry_manager = RetryManager(config)
        
        delays = []
        for attempt in range(3):
            delay = retry_manager._calculate_retry_delay(
                attempt, NetworkError("test"), config, "test"
            )
            delays.append(delay)
        
        # Should be linearly increasing
        assert delays[0] < delays[1] < delays[2]
        assert abs(delays[0] - 0.1) < 0.01  # Base * 1
        assert abs(delays[1] - 0.2) < 0.01  # Base * 2
        assert abs(delays[2] - 0.3) < 0.01  # Base * 3
    
    @pytest.mark.asyncio
    async def test_fixed_delay_strategy(self):
        """Test fixed delay strategy."""
        config = RetryConfig(
            max_attempts=4,
            base_delay=0.5,
            max_delay=10.0,  # Higher max delay
            network_base_delay=0.5,  # Override network base delay
            strategy=RetryStrategy.FIXED_DELAY,
            jitter_range=0.0
        )
        retry_manager = RetryManager(config)
        
        delays = []
        for attempt in range(3):
            delay = retry_manager._calculate_retry_delay(
                attempt, NetworkError("test"), config, "test"
            )
            delays.append(delay)
        
        # Should all be the same
        assert all(abs(delay - 0.5) < 0.01 for delay in delays)
    
    @pytest.mark.asyncio
    async def test_fibonacci_backoff_strategy(self):
        """Test Fibonacci backoff strategy."""
        config = RetryConfig(
            max_attempts=6,
            base_delay=0.1,
            max_delay=10.0,  # Higher max delay
            network_base_delay=0.1,  # Override network base delay
            strategy=RetryStrategy.FIBONACCI_BACKOFF,
            jitter_range=0.0
        )
        retry_manager = RetryManager(config)
        
        delays = []
        for attempt in range(5):
            delay = retry_manager._calculate_retry_delay(
                attempt, NetworkError("test"), config, "test"
            )
            delays.append(delay)
        
        # Should follow Fibonacci sequence
        expected_multipliers = [1, 1, 2, 3, 5]  # Fibonacci numbers
        for i, delay in enumerate(delays):
            expected = 0.1 * expected_multipliers[i]
            assert abs(delay - expected) < 0.01


class TestRetryDecorator:
    """Test retry decorator functionality."""
    
    @pytest.mark.asyncio
    async def test_retry_decorator_success(self):
        """Test retry decorator with successful operation."""
        @retry_on_error(max_attempts=3, base_delay=0.1)
        async def successful_operation():
            return "success"
        
        result = await successful_operation()
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_retry_decorator_with_retries(self):
        """Test retry decorator with retries."""
        call_count = 0
        
        @retry_on_error(max_attempts=3, base_delay=0.1)
        async def flaky_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise NetworkError("Temporary error")
            return "success"
        
        result = await flaky_operation()
        assert result == "success"
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_retry_decorator_failure(self):
        """Test retry decorator with persistent failure."""
        @retry_on_error(max_attempts=2, base_delay=0.1)
        async def failing_operation():
            raise NetworkError("Persistent error")
        
        with pytest.raises(NetworkError):
            await failing_operation()


class TestRetryManagerIntegration:
    """Integration tests for retry manager."""
    
    @pytest.mark.asyncio
    async def test_complex_retry_scenario(self):
        """Test complex retry scenario with multiple error types."""
        retry_manager = RetryManager(RetryConfig(
            max_attempts=5,
            base_delay=0.1,
            rate_limit_max_attempts=3,
            network_max_attempts=4
        ))
        
        call_count = 0
        
        async def complex_operation():
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                raise NetworkError("Network timeout")
            elif call_count == 2:
                raise RateLimitError("Rate limit exceeded")
            elif call_count == 3:
                raise APIError("Server error", status_code=500)
            else:
                return "finally_success"
        
        result = await retry_manager.execute_with_retry(
            complex_operation,
            "complex_operation"
        )
        
        assert result == "finally_success"
        assert call_count == 4
        
        # Check statistics
        stats = retry_manager.get_statistics()
        assert stats.total_operations == 1
        assert stats.successful_operations == 1
        assert stats.total_retry_attempts == 3
        assert len(stats.error_counts) == 3  # Three different error types