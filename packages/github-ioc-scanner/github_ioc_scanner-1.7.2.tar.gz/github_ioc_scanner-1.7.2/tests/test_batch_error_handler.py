"""Tests for batch error handling and recovery strategies."""

import asyncio
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import httpx

from src.github_ioc_scanner.batch_error_handler import (
    BatchErrorHandler, ErrorCategory, RecoveryStrategy, ErrorContext,
    RecoveryAction, CircuitBreaker
)
from src.github_ioc_scanner.batch_models import (
    BatchRequest, BatchResult, BatchRecoveryPlan, BatchStrategy
)
from src.github_ioc_scanner.models import Repository
from src.github_ioc_scanner.exceptions import (
    NetworkError, RateLimitError, APIError, AuthenticationError,
    BatchProcessingError
)


@pytest.fixture
def error_handler():
    """Create a BatchErrorHandler instance for testing."""
    return BatchErrorHandler()


@pytest.fixture
def sample_repository():
    """Create a sample repository for testing."""
    return Repository(
        name="test-repo",
        full_name="owner/test-repo",
        archived=False,
        default_branch="main",
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_request(sample_repository):
    """Create a sample batch request for testing."""
    return BatchRequest(
        repo=sample_repository,
        file_path="package.json",
        priority=5,
        estimated_size=1024
    )


class TestErrorCategorization:
    """Test error categorization logic."""
    
    def test_categorize_httpx_timeout(self, error_handler, sample_request):
        """Test categorization of httpx timeout errors."""
        error = httpx.TimeoutException("Request timed out")
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.TIMEOUT
    
    def test_categorize_httpx_network_error(self, error_handler, sample_request):
        """Test categorization of httpx network errors."""
        error = httpx.NetworkError("Network unreachable")
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.TRANSIENT_NETWORK
    
    def test_categorize_httpx_http_status_errors(self, error_handler, sample_request):
        """Test categorization of various HTTP status errors."""
        # Mock response for HTTPStatusError
        mock_response = Mock()
        
        # Test 401 Unauthorized
        mock_response.status_code = 401
        error = httpx.HTTPStatusError("Unauthorized", request=Mock(), response=mock_response)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.AUTHENTICATION
        
        # Test 403 Forbidden
        mock_response.status_code = 403
        error = httpx.HTTPStatusError("Forbidden", request=Mock(), response=mock_response)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.PERMISSION
        
        # Test 404 Not Found
        mock_response.status_code = 404
        error = httpx.HTTPStatusError("Not Found", request=Mock(), response=mock_response)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.NOT_FOUND
        
        # Test 429 Rate Limited
        mock_response.status_code = 429
        error = httpx.HTTPStatusError("Rate Limited", request=Mock(), response=mock_response)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.RATE_LIMIT
        
        # Test 400 Bad Request
        mock_response.status_code = 400
        error = httpx.HTTPStatusError("Bad Request", request=Mock(), response=mock_response)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.MALFORMED_REQUEST
        
        # Test 500 Server Error
        mock_response.status_code = 500
        error = httpx.HTTPStatusError("Server Error", request=Mock(), response=mock_response)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.SERVER_ERROR
    
    def test_categorize_custom_exceptions(self, error_handler, sample_request):
        """Test categorization of custom exceptions."""
        # Test RateLimitError
        error = RateLimitError("Rate limit exceeded")
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.RATE_LIMIT
        
        # Test AuthenticationError
        error = AuthenticationError("Authentication failed")
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.AUTHENTICATION
        
        # Test NetworkError
        error = NetworkError("Network error")
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.TRANSIENT_NETWORK
        
        # Test APIError with status codes
        error = APIError("Not found", status_code=404)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.NOT_FOUND
        
        error = APIError("Forbidden", status_code=403)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.PERMISSION
        
        error = APIError("Server error", status_code=500)
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.SERVER_ERROR
    
    def test_categorize_unknown_error(self, error_handler, sample_request):
        """Test categorization of unknown errors."""
        error = ValueError("Some unknown error")
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.UNKNOWN


class TestRecoveryActions:
    """Test recovery action determination."""
    
    def test_transient_network_recovery(self, error_handler):
        """Test recovery action for transient network errors."""
        action = error_handler.get_recovery_action(ErrorCategory.TRANSIENT_NETWORK, 1)
        assert action.strategy == RecoveryStrategy.RETRY_WITH_BACKOFF
        assert action.delay_seconds == 2  # 2^1
        assert action.max_retries == 3
        
        # Test exponential backoff
        action = error_handler.get_recovery_action(ErrorCategory.TRANSIENT_NETWORK, 3)
        assert action.delay_seconds == 8  # 2^3
    
    def test_rate_limit_recovery(self, error_handler):
        """Test recovery action for rate limit errors."""
        action = error_handler.get_recovery_action(ErrorCategory.RATE_LIMIT, 1)
        assert action.strategy == RecoveryStrategy.RETRY_WITH_DELAY
        assert action.delay_seconds == 60
        assert action.max_retries == 2
        assert action.reduce_concurrency_factor == 0.5
    
    def test_authentication_recovery(self, error_handler):
        """Test recovery action for authentication errors."""
        action = error_handler.get_recovery_action(ErrorCategory.AUTHENTICATION, 1)
        assert action.strategy == RecoveryStrategy.FAIL_BATCH
        assert action.max_retries == 0
    
    def test_permission_recovery(self, error_handler):
        """Test recovery action for permission errors."""
        action = error_handler.get_recovery_action(ErrorCategory.PERMISSION, 1)
        assert action.strategy == RecoveryStrategy.SKIP_REQUEST
        assert action.max_retries == 0
    
    def test_not_found_recovery(self, error_handler):
        """Test recovery action for not found errors."""
        action = error_handler.get_recovery_action(ErrorCategory.NOT_FOUND, 1)
        assert action.strategy == RecoveryStrategy.SKIP_REQUEST
        assert action.max_retries == 0
    
    def test_server_error_recovery(self, error_handler):
        """Test recovery action for server errors."""
        action = error_handler.get_recovery_action(ErrorCategory.SERVER_ERROR, 1)
        assert action.strategy == RecoveryStrategy.RETRY_WITH_BACKOFF
        assert action.delay_seconds == 10  # 5 * 2^1
        assert action.max_retries == 2
    
    def test_timeout_recovery(self, error_handler):
        """Test recovery action for timeout errors."""
        action = error_handler.get_recovery_action(ErrorCategory.TIMEOUT, 1)
        assert action.strategy == RecoveryStrategy.RETRY_WITH_BACKOFF
        assert action.delay_seconds == 3  # 3^1
        assert action.max_retries == 2
        assert action.reduce_concurrency_factor == 0.7


class TestBatchFailureHandling:
    """Test batch failure handling."""
    
    def test_handle_batch_failure_with_retry(self, error_handler, sample_request):
        """Test handling batch failure that should be retried."""
        failed_batch = [sample_request]
        error = NetworkError("Network error")
        
        recovery_plan = error_handler.handle_batch_failure(failed_batch, error)
        
        assert len(recovery_plan.retry_requests) == 1
        assert recovery_plan.retry_requests[0] == sample_request
        assert recovery_plan.delay_seconds > 0
        assert recovery_plan.fallback_strategy == BatchStrategy.SEQUENTIAL
    
    def test_handle_batch_failure_with_skip(self, error_handler, sample_request):
        """Test handling batch failure that should be skipped."""
        failed_batch = [sample_request]
        error = APIError("Not found", status_code=404)
        
        recovery_plan = error_handler.handle_batch_failure(failed_batch, error)
        
        assert len(recovery_plan.skip_requests) == 1
        assert recovery_plan.skip_requests[0] == sample_request
        assert len(recovery_plan.retry_requests) == 0
    
    def test_handle_batch_failure_authentication_error(self, error_handler, sample_request):
        """Test handling batch failure with authentication error."""
        failed_batch = [sample_request]
        error = AuthenticationError("Authentication failed")
        
        with pytest.raises(BatchProcessingError) as exc_info:
            error_handler.handle_batch_failure(failed_batch, error, batch_id="test-batch")
        
        assert "unrecoverable error" in str(exc_info.value)
        assert exc_info.value.batch_id == "test-batch"
    
    def test_handle_empty_batch_failure(self, error_handler):
        """Test handling failure of empty batch."""
        failed_batch = []
        error = Exception("Some error")
        
        recovery_plan = error_handler.handle_batch_failure(failed_batch, error)
        
        # Should create empty recovery plan for unknown error category
        assert len(recovery_plan.retry_requests) == 0
        assert len(recovery_plan.skip_requests) == 0


class TestPartialFailureHandling:
    """Test partial failure handling."""
    
    def test_handle_partial_failure_with_retries(self, error_handler, sample_request, sample_repository):
        """Test handling partial failure where some requests should be retried."""
        # Create successful results
        successful_results = [
            BatchResult(
                request=BatchRequest(sample_repository, "success.json"),
                content=Mock(),
                processing_time=1.0
            )
        ]
        
        # Create failed requests
        failed_requests = [sample_request]
        errors = [NetworkError("Network error")]
        
        retry_requests = error_handler.handle_partial_failure(
            successful_results, failed_requests, errors
        )
        
        assert len(retry_requests) == 1
        assert retry_requests[0] == sample_request
    
    def test_handle_partial_failure_skip_requests(self, error_handler, sample_request, sample_repository):
        """Test handling partial failure where requests should be skipped."""
        successful_results = [
            BatchResult(
                request=BatchRequest(sample_repository, "success.json"),
                content=Mock(),
                processing_time=1.0
            )
        ]
        
        failed_requests = [sample_request]
        errors = [APIError("Not found", status_code=404)]
        
        retry_requests = error_handler.handle_partial_failure(
            successful_results, failed_requests, errors
        )
        
        assert len(retry_requests) == 0  # Should not retry 404 errors
    
    def test_handle_partial_failure_max_retries_exceeded(self, error_handler, sample_request, sample_repository):
        """Test handling partial failure when max retries are exceeded."""
        # Simulate previous attempts by adding error history
        for i in range(3):
            error_context = ErrorContext(
                error=NetworkError("Network error"),
                request=sample_request,
                attempt=i + 1,
                timestamp=datetime.now(),
                category=ErrorCategory.TRANSIENT_NETWORK,
                recovery_strategy=RecoveryStrategy.RETRY_WITH_BACKOFF
            )
            error_handler._error_history.append(error_context)
        
        successful_results = []
        failed_requests = [sample_request]
        errors = [NetworkError("Network error")]
        
        retry_requests = error_handler.handle_partial_failure(
            successful_results, failed_requests, errors
        )
        
        assert len(retry_requests) == 0  # Should not retry after max attempts


class TestRetryLogic:
    """Test retry decision logic."""
    
    def test_should_retry_request_within_limits(self, error_handler, sample_request):
        """Test retry decision within attempt limits."""
        error = NetworkError("Network error")
        
        # Should retry on first attempt
        assert error_handler.should_retry_request(sample_request, error, 1)
        
        # Should retry on second attempt
        assert error_handler.should_retry_request(sample_request, error, 2)
        
        # Should not retry after max attempts
        assert not error_handler.should_retry_request(sample_request, error, 4)
    
    def test_should_not_retry_authentication_error(self, error_handler, sample_request):
        """Test that authentication errors are not retried."""
        error = AuthenticationError("Authentication failed")
        
        assert not error_handler.should_retry_request(sample_request, error, 1)
    
    def test_get_retry_delay(self, error_handler, sample_request):
        """Test retry delay calculation."""
        # Network error should use exponential backoff
        error = NetworkError("Network error")
        delay = error_handler.get_retry_delay(sample_request, error, 2)
        assert delay == 4  # 2^2
        
        # Rate limit error should use fixed delay
        error = RateLimitError("Rate limited")
        delay = error_handler.get_retry_delay(sample_request, error, 1)
        assert delay == 60


class TestErrorStatistics:
    """Test error statistics and reporting."""
    
    def test_error_statistics_empty(self, error_handler):
        """Test error statistics when no errors have occurred."""
        stats = error_handler.get_error_statistics()
        
        assert stats['total_errors'] == 0
        assert stats['errors_by_category'] == {}
        assert stats['recovery_success_rates'] == {}
        assert stats['recent_errors'] == []
    
    def test_error_statistics_with_errors(self, error_handler, sample_request):
        """Test error statistics with recorded errors."""
        # Add some error contexts
        errors = [
            ErrorContext(
                error=NetworkError("Network error 1"),
                request=sample_request,
                attempt=1,
                timestamp=datetime.now(),
                category=ErrorCategory.TRANSIENT_NETWORK,
                recovery_strategy=RecoveryStrategy.RETRY_WITH_BACKOFF
            ),
            ErrorContext(
                error=NetworkError("Network error 2"),
                request=sample_request,
                attempt=1,
                timestamp=datetime.now(),
                category=ErrorCategory.TRANSIENT_NETWORK,
                recovery_strategy=RecoveryStrategy.RETRY_WITH_BACKOFF
            ),
            ErrorContext(
                error=RateLimitError("Rate limited"),
                request=sample_request,
                attempt=1,
                timestamp=datetime.now(),
                category=ErrorCategory.RATE_LIMIT,
                recovery_strategy=RecoveryStrategy.RETRY_WITH_DELAY
            )
        ]
        
        error_handler._error_history.extend(errors)
        
        stats = error_handler.get_error_statistics()
        
        assert stats['total_errors'] == 3
        assert stats['errors_by_category']['transient_network'] == 2
        assert stats['errors_by_category']['rate_limit'] == 1
        assert len(stats['recent_errors']) == 3
        
        # Check recent error format
        recent_error = stats['recent_errors'][0]
        assert 'timestamp' in recent_error
        assert 'category' in recent_error
        assert 'strategy' in recent_error
        assert 'attempt' in recent_error
        assert 'request' in recent_error
        assert 'error' in recent_error
    
    def test_clear_error_history(self, error_handler, sample_request):
        """Test clearing error history."""
        # Add an error
        error_context = ErrorContext(
            error=NetworkError("Network error"),
            request=sample_request,
            attempt=1,
            timestamp=datetime.now(),
            category=ErrorCategory.TRANSIENT_NETWORK,
            recovery_strategy=RecoveryStrategy.RETRY_WITH_BACKOFF
        )
        error_handler._error_history.append(error_context)
        
        # Verify error exists
        assert len(error_handler._error_history) == 1
        
        # Clear history
        error_handler.clear_error_history()
        
        # Verify history is cleared
        assert len(error_handler._error_history) == 0
        stats = error_handler.get_error_statistics()
        assert stats['total_errors'] == 0


class TestCircuitBreaker:
    """Test circuit breaker functionality."""
    
    def test_circuit_breaker_closed_state(self):
        """Test circuit breaker in closed state."""
        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60)
        
        # Should allow calls in closed state
        result = cb.call(lambda x: x * 2, 5)
        assert result == 10
        assert cb.state == 'closed'
        assert cb.failure_count == 0
    
    def test_circuit_breaker_opens_after_failures(self):
        """Test circuit breaker opens after threshold failures."""
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=60)
        
        # First failure
        with pytest.raises(ValueError):
            cb.call(lambda: exec('raise ValueError("test error")'))
        assert cb.state == 'closed'
        assert cb.failure_count == 1
        
        # Second failure - should open circuit
        with pytest.raises(ValueError):
            cb.call(lambda: exec('raise ValueError("test error")'))
        assert cb.state == 'open'
        assert cb.failure_count == 2
    
    def test_circuit_breaker_blocks_calls_when_open(self):
        """Test circuit breaker blocks calls when open."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=60)
        
        # Cause failure to open circuit
        with pytest.raises(ValueError):
            cb.call(lambda: exec('raise ValueError("test error")'))
        assert cb.state == 'open'
        
        # Should block subsequent calls
        with pytest.raises(Exception) as exc_info:
            cb.call(lambda: "should not execute")
        assert "Circuit breaker is open" in str(exc_info.value)
    
    def test_circuit_breaker_half_open_recovery(self):
        """Test circuit breaker recovery through half-open state."""
        cb = CircuitBreaker(failure_threshold=1, recovery_timeout=0.1)
        
        # Open the circuit
        with pytest.raises(ValueError):
            cb.call(lambda: exec('raise ValueError("test error")'))
        assert cb.state == 'open'
        
        # Wait for recovery timeout
        import time
        time.sleep(0.2)
        
        # Next call should attempt recovery (half-open)
        result = cb.call(lambda: "success")
        assert result == "success"
        assert cb.state == 'closed'
        assert cb.failure_count == 0
    
    def test_circuit_breaker_specific_exception_type(self):
        """Test circuit breaker with specific exception type."""
        cb = CircuitBreaker(failure_threshold=2, expected_exception=ValueError)
        
        # Should not count non-matching exceptions
        with pytest.raises(TypeError):
            cb.call(lambda: exec('raise TypeError("not counted")'))
        assert cb.failure_count == 0
        
        # Should count matching exceptions
        with pytest.raises(ValueError):
            cb.call(lambda: exec('raise ValueError("counted")'))
        assert cb.failure_count == 1


class TestIntegration:
    """Integration tests for error handling components."""
    
    def test_error_handler_with_circuit_breaker(self, error_handler, sample_request):
        """Test error handler integration with circuit breaker."""
        # This is a conceptual test - in practice, circuit breakers would be
        # integrated into the actual batch processing components
        
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1)
        
        def failing_operation():
            raise NetworkError("Network failure")
        
        # First failure
        with pytest.raises(NetworkError):
            cb.call(failing_operation)
        
        # Second failure - opens circuit
        with pytest.raises(NetworkError):
            cb.call(failing_operation)
        
        assert cb.state == 'open'
        
        # Error handler should still categorize the error correctly
        error = NetworkError("Network failure")
        category = error_handler.categorize_error(error, sample_request)
        assert category == ErrorCategory.TRANSIENT_NETWORK
    
    def test_comprehensive_error_handling_workflow(self, error_handler, sample_request, sample_repository):
        """Test a comprehensive error handling workflow."""
        # Simulate a batch with mixed results
        successful_results = [
            BatchResult(
                request=BatchRequest(sample_repository, "success1.json"),
                content=Mock(),
                processing_time=1.0
            ),
            BatchResult(
                request=BatchRequest(sample_repository, "success2.json"),
                content=Mock(),
                processing_time=1.5
            )
        ]
        
        failed_requests = [
            BatchRequest(sample_repository, "network_fail.json"),
            BatchRequest(sample_repository, "not_found.json"),
            BatchRequest(sample_repository, "rate_limited.json")
        ]
        
        errors = [
            NetworkError("Network error"),
            APIError("Not found", status_code=404),
            RateLimitError("Rate limited")
        ]
        
        # Handle partial failure
        retry_requests = error_handler.handle_partial_failure(
            successful_results, failed_requests, errors
        )
        
        # Should retry network error and rate limit, but not 404
        assert len(retry_requests) == 2
        
        # Check error statistics
        stats = error_handler.get_error_statistics()
        assert stats['total_errors'] == 3
        assert 'transient_network' in stats['errors_by_category']
        assert 'not_found' in stats['errors_by_category']
        assert 'rate_limit' in stats['errors_by_category']