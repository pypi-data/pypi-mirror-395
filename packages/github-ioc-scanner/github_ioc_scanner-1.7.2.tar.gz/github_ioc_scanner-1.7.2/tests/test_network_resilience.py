"""Tests for network resilience and adaptive retry logic."""

import asyncio
import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch
import httpx

from src.github_ioc_scanner.network_resilience import (
    AdaptiveRetryManager, CircuitBreakerManager, NetworkResilienceManager,
    NetworkCondition, RetryConfig, NetworkMetrics
)
from src.github_ioc_scanner.batch_models import NetworkConditions
from src.github_ioc_scanner.exceptions import NetworkError, RateLimitError


class TestRetryConfig:
    """Test retry configuration."""
    
    def test_default_config(self):
        """Test default retry configuration."""
        config = RetryConfig()
        assert config.max_retries == 3
        assert config.base_delay == 1.0
        assert config.max_delay == 60.0
        assert config.exponential_base == 2.0
        assert config.jitter is True
    
    def test_calculate_delay_exponential(self):
        """Test exponential delay calculation."""
        config = RetryConfig(jitter=False)  # Disable jitter for predictable results
        
        assert config.calculate_delay(1) == 1.0  # base_delay * 2^0
        assert config.calculate_delay(2) == 2.0  # base_delay * 2^1
        assert config.calculate_delay(3) == 4.0  # base_delay * 2^2
        assert config.calculate_delay(4) == 8.0  # base_delay * 2^3
    
    def test_calculate_delay_with_max(self):
        """Test delay calculation with maximum limit."""
        config = RetryConfig(base_delay=10.0, max_delay=15.0, jitter=False)
        
        assert config.calculate_delay(1) == 10.0
        assert config.calculate_delay(2) == 15.0  # Capped at max_delay
        assert config.calculate_delay(3) == 15.0  # Still capped
    
    def test_calculate_delay_with_multiplier(self):
        """Test delay calculation with backoff multiplier."""
        config = RetryConfig(
            base_delay=1.0,
            backoff_multiplier=2.0,
            jitter=False
        )
        
        assert config.calculate_delay(1) == 2.0  # 1.0 * 2^0 * 2.0
        assert config.calculate_delay(2) == 4.0  # 1.0 * 2^1 * 2.0
        assert config.calculate_delay(3) == 8.0  # 1.0 * 2^2 * 2.0
    
    def test_calculate_delay_with_jitter(self):
        """Test delay calculation with jitter."""
        config = RetryConfig(base_delay=4.0, jitter=True)
        
        # With jitter, delay should be between 75% and 125% of base calculation
        delay = config.calculate_delay(1)
        assert 3.0 <= delay <= 5.0  # 4.0 * 0.75 to 4.0 * 1.25


class TestNetworkMetrics:
    """Test network metrics tracking."""
    
    def test_initial_state(self):
        """Test initial metrics state."""
        metrics = NetworkMetrics()
        assert metrics.error_count == 0
        assert metrics.success_count == 0
        assert metrics.total_requests == 0
        assert metrics.average_latency == 0.0
        assert metrics.error_rate == 0.0
        assert metrics.success_rate == 0.0
    
    def test_add_success(self):
        """Test adding successful requests."""
        metrics = NetworkMetrics()
        
        metrics.add_success(100.0)
        assert metrics.success_count == 1
        assert metrics.total_requests == 1
        assert metrics.average_latency == 100.0
        assert metrics.success_rate == 1.0
        assert metrics.consecutive_errors == 0
        
        metrics.add_success(200.0)
        assert metrics.success_count == 2
        assert metrics.total_requests == 2
        assert metrics.average_latency == 150.0  # (100 + 200) / 2
        assert metrics.success_rate == 1.0
    
    def test_add_error(self):
        """Test adding failed requests."""
        metrics = NetworkMetrics()
        
        metrics.add_error()
        assert metrics.error_count == 1
        assert metrics.total_requests == 1
        assert metrics.error_rate == 1.0
        assert metrics.consecutive_errors == 1
        assert metrics.last_error_time is not None
        
        metrics.add_error()
        assert metrics.error_count == 2
        assert metrics.total_requests == 2
        assert metrics.error_rate == 1.0
        assert metrics.consecutive_errors == 2
    
    def test_mixed_requests(self):
        """Test mixed successful and failed requests."""
        metrics = NetworkMetrics()
        
        metrics.add_success(100.0)
        metrics.add_error()
        metrics.add_success(200.0)
        
        assert metrics.success_count == 2
        assert metrics.error_count == 1
        assert metrics.total_requests == 3
        assert metrics.success_rate == 2/3
        assert metrics.error_rate == 1/3
        assert metrics.consecutive_errors == 0  # Reset by last success
    
    def test_latency_sample_limit(self):
        """Test that latency samples are limited."""
        metrics = NetworkMetrics()
        
        # Add more than 100 samples
        for i in range(150):
            metrics.add_success(float(i))
        
        # Should keep only the last 100 samples
        assert len(metrics.latency_samples) == 100
        assert metrics.latency_samples[0] == 50.0  # First of the last 100
        assert metrics.latency_samples[-1] == 149.0  # Last sample
    
    def test_network_condition_excellent(self):
        """Test excellent network condition detection."""
        metrics = NetworkMetrics()
        
        # Add samples for excellent condition
        for _ in range(10):
            metrics.add_success(50.0)  # Low latency
        
        condition = metrics.get_network_condition()
        assert condition == NetworkCondition.EXCELLENT
    
    def test_network_condition_poor(self):
        """Test poor network condition detection."""
        metrics = NetworkMetrics()
        
        # Add samples for poor condition
        for _ in range(5):
            metrics.add_success(800.0)  # High latency
        for _ in range(2):
            metrics.add_error()  # Some errors
        
        condition = metrics.get_network_condition()
        assert condition == NetworkCondition.POOR
    
    def test_network_condition_critical(self):
        """Test critical network condition detection."""
        metrics = NetworkMetrics()
        
        # Add samples for critical condition
        for _ in range(3):
            metrics.add_success(2000.0)  # Very high latency
        for _ in range(4):
            metrics.add_error()  # High error rate
        
        condition = metrics.get_network_condition()
        assert condition == NetworkCondition.CRITICAL
    
    def test_network_condition_insufficient_data(self):
        """Test network condition with insufficient data."""
        metrics = NetworkMetrics()
        
        # Add only a few samples
        metrics.add_success(100.0)
        metrics.add_success(200.0)
        
        condition = metrics.get_network_condition()
        assert condition == NetworkCondition.GOOD  # Default for insufficient data


class TestAdaptiveRetryManager:
    """Test adaptive retry manager."""
    
    @pytest.fixture
    def retry_manager(self):
        """Create a retry manager for testing."""
        return AdaptiveRetryManager()
    
    @pytest.mark.asyncio
    async def test_successful_operation_no_retry(self, retry_manager):
        """Test successful operation that doesn't need retry."""
        async def successful_operation():
            return "success"
        
        result = await retry_manager.execute_with_retry(
            successful_operation,
            operation_name="test_op"
        )
        
        assert result == "success"
        assert retry_manager.network_metrics.success_count == 1
        assert retry_manager.network_metrics.error_count == 0
    
    @pytest.mark.asyncio
    async def test_operation_with_retries(self, retry_manager):
        """Test operation that succeeds after retries."""
        call_count = 0
        
        async def flaky_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise httpx.NetworkError("Network error")
            return "success"
        
        result = await retry_manager.execute_with_retry(
            flaky_operation,
            operation_name="flaky_op"
        )
        
        assert result == "success"
        assert call_count == 3
        assert retry_manager.network_metrics.success_count == 1
        assert retry_manager.network_metrics.error_count == 2
    
    @pytest.mark.asyncio
    async def test_operation_fails_after_max_retries(self, retry_manager):
        """Test operation that fails after maximum retries."""
        async def failing_operation():
            raise httpx.NetworkError("Persistent network error")
        
        with pytest.raises(httpx.NetworkError):
            await retry_manager.execute_with_retry(
                failing_operation,
                operation_name="failing_op"
            )
        
        # Should have tried max_retries + 1 times (initial + retries)
        condition = retry_manager.network_metrics.get_network_condition()
        config = retry_manager.retry_configs[condition]
        assert retry_manager.network_metrics.error_count == config.max_retries
    
    @pytest.mark.asyncio
    async def test_non_retryable_error(self, retry_manager):
        """Test that non-retryable errors are not retried."""
        async def operation_with_auth_error():
            raise httpx.HTTPStatusError(
                "Unauthorized",
                request=Mock(),
                response=Mock(status_code=401)
            )
        
        with pytest.raises(httpx.HTTPStatusError):
            await retry_manager.execute_with_retry(
                operation_with_auth_error,
                operation_name="auth_error_op"
            )
        
        # Should not retry authentication errors
        assert retry_manager.network_metrics.error_count == 1
    
    @pytest.mark.asyncio
    async def test_retryable_http_errors(self, retry_manager):
        """Test that retryable HTTP errors are retried."""
        call_count = 0
        
        async def server_error_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise httpx.HTTPStatusError(
                    "Server Error",
                    request=Mock(),
                    response=Mock(status_code=500)
                )
            return "success"
        
        result = await retry_manager.execute_with_retry(
            server_error_operation,
            operation_name="server_error_op"
        )
        
        assert result == "success"
        assert call_count == 2
    
    def test_should_retry_exception(self, retry_manager):
        """Test retry decision for different exception types."""
        # Retryable exceptions
        assert retry_manager._should_retry_exception(httpx.TimeoutException("timeout"))
        assert retry_manager._should_retry_exception(httpx.NetworkError("network"))
        assert retry_manager._should_retry_exception(NetworkError("custom network"))
        assert retry_manager._should_retry_exception(RateLimitError("rate limited"))
        
        # Server errors should be retried
        server_error = httpx.HTTPStatusError(
            "Server Error",
            request=Mock(),
            response=Mock(status_code=500)
        )
        assert retry_manager._should_retry_exception(server_error)
        
        # Rate limit errors should be retried
        rate_limit_error = httpx.HTTPStatusError(
            "Rate Limited",
            request=Mock(),
            response=Mock(status_code=429)
        )
        assert retry_manager._should_retry_exception(rate_limit_error)
        
        # Non-retryable exceptions
        auth_error = httpx.HTTPStatusError(
            "Unauthorized",
            request=Mock(),
            response=Mock(status_code=401)
        )
        assert not retry_manager._should_retry_exception(auth_error)
        
        assert not retry_manager._should_retry_exception(ValueError("not retryable"))
    
    def test_get_current_network_conditions(self, retry_manager):
        """Test getting current network conditions."""
        # Add some metrics
        retry_manager.network_metrics.add_success(150.0)
        retry_manager.network_metrics.add_success(200.0)
        retry_manager.network_metrics.add_error()
        
        conditions = retry_manager.get_current_network_conditions()
        
        assert isinstance(conditions, NetworkConditions)
        assert conditions.latency_ms == 175.0  # Average of 150 and 200
        assert conditions.error_rate == 1/3  # 1 error out of 3 total requests
        assert conditions.bandwidth_mbps > 0
    
    def test_adaptive_retry_config_selection(self, retry_manager):
        """Test that retry config adapts to network conditions."""
        # Simulate excellent network conditions
        for _ in range(10):
            retry_manager.network_metrics.add_success(50.0)
        
        condition = retry_manager.network_metrics.get_network_condition()
        assert condition == NetworkCondition.EXCELLENT
        
        config = retry_manager.retry_configs[condition]
        assert config.max_retries == 2  # Fewer retries for excellent conditions
        assert config.base_delay == 0.5  # Shorter delays
        
        # Simulate poor network conditions
        retry_manager.reset_metrics()
        for _ in range(5):
            retry_manager.network_metrics.add_success(800.0)
        for _ in range(2):
            retry_manager.network_metrics.add_error()
        
        condition = retry_manager.network_metrics.get_network_condition()
        assert condition == NetworkCondition.POOR
        
        config = retry_manager.retry_configs[condition]
        assert config.max_retries == 5  # More retries for poor conditions
        assert config.base_delay == 5.0  # Longer delays
    
    def test_get_retry_statistics(self, retry_manager):
        """Test getting retry statistics."""
        # Add some metrics
        retry_manager.network_metrics.add_success(100.0)
        retry_manager.network_metrics.add_error()
        
        stats = retry_manager.get_retry_statistics()
        
        assert 'network_condition' in stats
        assert 'total_requests' in stats
        assert 'success_count' in stats
        assert 'error_count' in stats
        assert 'success_rate' in stats
        assert 'error_rate' in stats
        assert 'average_latency_ms' in stats
        assert 'current_retry_config' in stats
        
        assert stats['total_requests'] == 2
        assert stats['success_count'] == 1
        assert stats['error_count'] == 1
    
    def test_reset_metrics(self, retry_manager):
        """Test resetting metrics."""
        # Add some metrics
        retry_manager.network_metrics.add_success(100.0)
        retry_manager.network_metrics.add_error()
        
        assert retry_manager.network_metrics.total_requests == 2
        
        retry_manager.reset_metrics()
        
        assert retry_manager.network_metrics.total_requests == 0
        assert retry_manager.network_metrics.success_count == 0
        assert retry_manager.network_metrics.error_count == 0


class TestCircuitBreakerManager:
    """Test circuit breaker manager."""
    
    @pytest.fixture
    def circuit_breaker(self):
        """Create a circuit breaker for testing."""
        return CircuitBreakerManager(failure_threshold=2, recovery_timeout=1)
    
    @pytest.mark.asyncio
    async def test_closed_state_allows_calls(self, circuit_breaker):
        """Test that closed circuit breaker allows calls."""
        async def successful_operation():
            return "success"
        
        result = await circuit_breaker.call(successful_operation)
        assert result == "success"
        assert circuit_breaker.state == 'closed'
        assert circuit_breaker.failure_count == 0
    
    @pytest.mark.asyncio
    async def test_circuit_opens_after_failures(self, circuit_breaker):
        """Test that circuit breaker opens after threshold failures."""
        async def failing_operation():
            raise Exception("Operation failed")
        
        # First failure
        with pytest.raises(Exception):
            await circuit_breaker.call(failing_operation)
        assert circuit_breaker.state == 'closed'
        assert circuit_breaker.failure_count == 1
        
        # Second failure - should open circuit
        with pytest.raises(Exception):
            await circuit_breaker.call(failing_operation)
        assert circuit_breaker.state == 'open'
        assert circuit_breaker.failure_count == 2
    
    @pytest.mark.asyncio
    async def test_open_circuit_blocks_calls(self, circuit_breaker):
        """Test that open circuit breaker blocks calls."""
        async def failing_operation():
            raise Exception("Operation failed")
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(Exception):
                await circuit_breaker.call(failing_operation)
        
        assert circuit_breaker.state == 'open'
        
        # Should block subsequent calls
        async def should_not_execute():
            return "should not reach here"
        
        with pytest.raises(Exception) as exc_info:
            await circuit_breaker.call(should_not_execute)
        assert "Circuit breaker is open" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_half_open_recovery(self, circuit_breaker):
        """Test circuit breaker recovery through half-open state."""
        async def failing_operation():
            raise Exception("Operation failed")
        
        async def successful_operation():
            return "success"
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(Exception):
                await circuit_breaker.call(failing_operation)
        assert circuit_breaker.state == 'open'
        
        # Wait for recovery timeout
        await asyncio.sleep(1.1)
        
        # Next calls should attempt recovery (half-open)
        for _ in range(3):  # half_open_max_calls
            result = await circuit_breaker.call(successful_operation)
            assert result == "success"
        
        assert circuit_breaker.state == 'closed'
        assert circuit_breaker.failure_count == 0
    
    @pytest.mark.asyncio
    async def test_half_open_failure_reopens_circuit(self, circuit_breaker):
        """Test that failure in half-open state reopens circuit."""
        async def failing_operation():
            raise Exception("Operation failed")
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(Exception):
                await circuit_breaker.call(failing_operation)
        assert circuit_breaker.state == 'open'
        
        # Wait for recovery timeout
        await asyncio.sleep(1.1)
        
        # Failure in half-open should reopen circuit
        with pytest.raises(Exception):
            await circuit_breaker.call(failing_operation)
        assert circuit_breaker.state == 'open'
    
    @pytest.mark.asyncio
    async def test_half_open_call_limit(self, circuit_breaker):
        """Test half-open call limit and transition to closed."""
        async def failing_operation():
            raise Exception("Operation failed")
        
        async def successful_operation():
            return "success"
        
        # Open the circuit
        for _ in range(2):
            with pytest.raises(Exception):
                await circuit_breaker.call(failing_operation)
        
        assert circuit_breaker.state == 'open'
        
        # Wait for recovery timeout
        await asyncio.sleep(1.1)
        
        # Make maximum allowed half-open calls - should succeed and close circuit
        for i in range(3):  # half_open_max_calls
            result = await circuit_breaker.call(successful_operation)
            assert result == "success"
            if i < 2:
                assert circuit_breaker.state == 'half-open'
        
        # After 3 successful calls, circuit should be closed
        assert circuit_breaker.state == 'closed'
        
        # Additional calls should work normally now
        result = await circuit_breaker.call(successful_operation)
        assert result == "success"
    
    def test_get_status(self, circuit_breaker):
        """Test getting circuit breaker status."""
        status = circuit_breaker.get_status()
        
        assert 'state' in status
        assert 'failure_count' in status
        assert 'success_count' in status
        assert 'failure_threshold' in status
        assert 'recovery_timeout' in status
        assert 'time_until_retry' in status
        assert 'half_open_calls' in status
        assert 'half_open_max_calls' in status
        
        assert status['state'] == 'closed'
        assert status['failure_count'] == 0
        assert status['failure_threshold'] == 2
        assert status['recovery_timeout'] == 1


class TestNetworkResilienceManager:
    """Test comprehensive network resilience manager."""
    
    @pytest.fixture
    def resilience_manager(self):
        """Create a resilience manager for testing."""
        return NetworkResilienceManager()
    
    def test_get_circuit_breaker(self, resilience_manager):
        """Test getting circuit breakers by name."""
        cb1 = resilience_manager.get_circuit_breaker("service1")
        cb2 = resilience_manager.get_circuit_breaker("service2")
        cb1_again = resilience_manager.get_circuit_breaker("service1")
        
        assert cb1 is not cb2  # Different services get different breakers
        assert cb1 is cb1_again  # Same service gets same breaker
    
    @pytest.mark.asyncio
    async def test_execute_with_resilience_success(self, resilience_manager):
        """Test successful execution with resilience."""
        async def successful_operation():
            return "success"
        
        result = await resilience_manager.execute_with_resilience(
            successful_operation,
            operation_name="test_op"
        )
        
        assert result == "success"
    
    @pytest.mark.asyncio
    async def test_execute_with_resilience_retry_and_circuit_breaker(self, resilience_manager):
        """Test execution with both retry and circuit breaker."""
        call_count = 0
        
        async def flaky_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise httpx.NetworkError("Network error")
            return "success"
        
        result = await resilience_manager.execute_with_resilience(
            flaky_operation,
            operation_name="flaky_op",
            circuit_breaker_name="test_service"
        )
        
        assert result == "success"
        assert call_count == 3
    
    @pytest.mark.asyncio
    async def test_execute_with_resilience_circuit_breaker_opens(self, resilience_manager):
        """Test that circuit breaker opens after repeated failures."""
        async def failing_operation():
            # Use a non-retryable error to ensure circuit breaker gets the failures
            raise httpx.HTTPStatusError(
                "Unauthorized",
                request=Mock(),
                response=Mock(status_code=401)
            )
        
        cb = resilience_manager.get_circuit_breaker("failing_service")
        
        # Make enough calls to open the circuit breaker
        for _ in range(cb.failure_threshold):
            with pytest.raises(httpx.HTTPStatusError):
                await resilience_manager.execute_with_resilience(
                    failing_operation,
                    operation_name="failing_op",
                    circuit_breaker_name="failing_service"
                )
        
        # Circuit breaker should be open
        assert cb.state == 'open'
    
    def test_get_network_conditions(self, resilience_manager):
        """Test getting network conditions."""
        conditions = resilience_manager.get_network_conditions()
        assert isinstance(conditions, NetworkConditions)
    
    def test_get_resilience_status(self, resilience_manager):
        """Test getting comprehensive resilience status."""
        # Create some circuit breakers
        resilience_manager.get_circuit_breaker("service1")
        resilience_manager.get_circuit_breaker("service2")
        
        status = resilience_manager.get_resilience_status()
        
        assert 'retry_statistics' in status
        assert 'circuit_breakers' in status
        assert 'default' in status['circuit_breakers']
        assert 'service1' in status['circuit_breakers']
        assert 'service2' in status['circuit_breakers']
    
    def test_reset_all_metrics(self, resilience_manager):
        """Test resetting all metrics."""
        # Add some data
        resilience_manager.retry_manager.network_metrics.add_success(100.0)
        resilience_manager.get_circuit_breaker("test_service")
        
        assert resilience_manager.retry_manager.network_metrics.total_requests == 1
        assert len(resilience_manager.circuit_breakers) == 1
        
        resilience_manager.reset_all_metrics()
        
        assert resilience_manager.retry_manager.network_metrics.total_requests == 0
        assert len(resilience_manager.circuit_breakers) == 0


class TestIntegration:
    """Integration tests for network resilience components."""
    
    @pytest.mark.asyncio
    async def test_comprehensive_resilience_workflow(self):
        """Test a comprehensive resilience workflow."""
        resilience_manager = NetworkResilienceManager()
        
        # Simulate a service that fails initially but recovers within retry limits
        call_count = 0
        
        async def recovering_service():
            nonlocal call_count
            call_count += 1
            
            if call_count <= 1:
                raise httpx.NetworkError("Network error")
            elif call_count <= 2:
                raise httpx.HTTPStatusError(
                    "Server Error",
                    request=Mock(),
                    response=Mock(status_code=500)
                )
            else:
                return f"success_call_{call_count}"
        
        # Should eventually succeed with retries
        result = await resilience_manager.execute_with_resilience(
            recovering_service,
            operation_name="recovering_service",
            circuit_breaker_name="test_service"
        )
        
        assert "success" in result
        assert call_count == 3  # Should succeed on third attempt
        
        # Check that metrics were recorded
        status = resilience_manager.get_resilience_status()
        assert status['retry_statistics']['total_requests'] > 0
        assert status['retry_statistics']['error_count'] > 0
        assert status['retry_statistics']['success_count'] > 0
    
    @pytest.mark.asyncio
    async def test_network_condition_adaptation(self):
        """Test that retry behavior adapts to network conditions."""
        retry_manager = AdaptiveRetryManager()
        
        # Start with excellent conditions
        for _ in range(10):
            retry_manager.network_metrics.add_success(50.0)
        
        condition = retry_manager.network_metrics.get_network_condition()
        assert condition == NetworkCondition.EXCELLENT
        
        config = retry_manager.retry_configs[condition]
        assert config.max_retries == 2  # Fewer retries for excellent conditions
        
        # Degrade to poor conditions
        for _ in range(10):
            retry_manager.network_metrics.add_success(800.0)
            retry_manager.network_metrics.add_error()
        
        condition = retry_manager.network_metrics.get_network_condition()
        assert condition in [NetworkCondition.POOR, NetworkCondition.CRITICAL]
        
        config = retry_manager.retry_configs[condition]
        assert config.max_retries >= 3  # More retries for poor conditions
    
    @pytest.mark.asyncio
    async def test_circuit_breaker_prevents_cascading_failures(self):
        """Test that circuit breaker prevents cascading failures."""
        cb = CircuitBreakerManager(failure_threshold=3, recovery_timeout=0.1)
        
        async def always_failing():
            raise Exception("Always fails")
        
        # Cause failures to open circuit
        for _ in range(3):
            with pytest.raises(Exception):
                await cb.call(always_failing)
        
        assert cb.state == 'open'
        
        # Subsequent calls should be blocked immediately
        start_time = time.time()
        with pytest.raises(Exception) as exc_info:
            await cb.call(always_failing)
        end_time = time.time()
        
        # Should fail immediately without calling the operation
        assert (end_time - start_time) < 0.01  # Very fast failure
        assert "Circuit breaker is open" in str(exc_info.value)