"""Sophisticated error handling and recovery for batch operations."""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Type, Union
import httpx

from .batch_models import (
    BatchRequest, BatchResult, BatchRecoveryPlan, BatchStrategy, BatchMetrics
)
from .exceptions import (
    GitHubIOCScannerError, NetworkError, RateLimitError, APIError,
    AuthenticationError, BatchProcessingError
)


class ErrorCategory(Enum):
    """Categories of errors for different recovery strategies."""
    TRANSIENT_NETWORK = "transient_network"
    RATE_LIMIT = "rate_limit"
    AUTHENTICATION = "authentication"
    PERMISSION = "permission"
    NOT_FOUND = "not_found"
    MALFORMED_REQUEST = "malformed_request"
    SERVER_ERROR = "server_error"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


class RecoveryStrategy(Enum):
    """Different recovery strategies for error categories."""
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    RETRY_WITH_DELAY = "retry_with_delay"
    SKIP_REQUEST = "skip_request"
    FALLBACK_STRATEGY = "fallback_strategy"
    FAIL_BATCH = "fail_batch"
    REDUCE_CONCURRENCY = "reduce_concurrency"


@dataclass
class ErrorContext:
    """Context information for an error."""
    error: Exception
    request: BatchRequest
    attempt: int
    timestamp: datetime
    category: ErrorCategory
    recovery_strategy: RecoveryStrategy
    additional_info: Dict[str, any] = field(default_factory=dict)


@dataclass
class RecoveryAction:
    """Action to take for error recovery."""
    strategy: RecoveryStrategy
    delay_seconds: float = 0.0
    max_retries: int = 3
    fallback_batch_strategy: Optional[BatchStrategy] = None
    reduce_concurrency_factor: float = 0.5
    
    def should_retry(self, attempt: int) -> bool:
        """Check if request should be retried based on attempt count."""
        return attempt < self.max_retries


class BatchErrorHandler:
    """Sophisticated error handler for batch operations."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the error handler.
        
        Args:
            logger: Optional logger for error reporting
        """
        self.logger = logger or logging.getLogger(__name__)
        self._error_history: List[ErrorContext] = []
        self._recovery_stats: Dict[ErrorCategory, Dict[str, int]] = {}
        self._circuit_breakers: Dict[str, 'CircuitBreaker'] = {}
        
        # Initialize recovery stats
        for category in ErrorCategory:
            self._recovery_stats[category] = {
                'total': 0,
                'successful_recoveries': 0,
                'failed_recoveries': 0
            }
    
    def categorize_error(self, error: Exception, request: BatchRequest) -> ErrorCategory:
        """
        Categorize an error to determine appropriate recovery strategy.
        
        Args:
            error: The exception that occurred
            request: The batch request that failed
            
        Returns:
            Error category for recovery strategy selection
        """
        # Handle httpx specific errors
        if isinstance(error, httpx.TimeoutException):
            return ErrorCategory.TIMEOUT
        elif isinstance(error, httpx.NetworkError):
            return ErrorCategory.TRANSIENT_NETWORK
        elif isinstance(error, httpx.HTTPStatusError):
            status_code = error.response.status_code
            if status_code == 401:
                return ErrorCategory.AUTHENTICATION
            elif status_code == 403:
                return ErrorCategory.PERMISSION
            elif status_code == 404:
                return ErrorCategory.NOT_FOUND
            elif status_code == 429:
                return ErrorCategory.RATE_LIMIT
            elif 400 <= status_code < 500:
                return ErrorCategory.MALFORMED_REQUEST
            elif 500 <= status_code < 600:
                return ErrorCategory.SERVER_ERROR
        
        # Handle custom exceptions
        if isinstance(error, RateLimitError):
            return ErrorCategory.RATE_LIMIT
        elif isinstance(error, AuthenticationError):
            return ErrorCategory.AUTHENTICATION
        elif isinstance(error, NetworkError):
            return ErrorCategory.TRANSIENT_NETWORK
        elif isinstance(error, APIError):
            if error.status_code:
                if error.status_code == 404:
                    return ErrorCategory.NOT_FOUND
                elif error.status_code == 403:
                    return ErrorCategory.PERMISSION
                elif 500 <= error.status_code < 600:
                    return ErrorCategory.SERVER_ERROR
        
        return ErrorCategory.UNKNOWN
    
    def get_recovery_action(self, category: ErrorCategory, attempt: int) -> RecoveryAction:
        """
        Get the appropriate recovery action for an error category.
        
        Args:
            category: Error category
            attempt: Current attempt number
            
        Returns:
            Recovery action to take
        """
        recovery_actions = {
            ErrorCategory.TRANSIENT_NETWORK: RecoveryAction(
                strategy=RecoveryStrategy.RETRY_WITH_BACKOFF,
                delay_seconds=min(2 ** attempt, 60),  # Exponential backoff, max 60s
                max_retries=3
            ),
            ErrorCategory.RATE_LIMIT: RecoveryAction(
                strategy=RecoveryStrategy.RETRY_WITH_DELAY,
                delay_seconds=60,  # Wait 1 minute for rate limit reset
                max_retries=2,
                reduce_concurrency_factor=0.5
            ),
            ErrorCategory.AUTHENTICATION: RecoveryAction(
                strategy=RecoveryStrategy.FAIL_BATCH,
                max_retries=0
            ),
            ErrorCategory.PERMISSION: RecoveryAction(
                strategy=RecoveryStrategy.SKIP_REQUEST,
                max_retries=0
            ),
            ErrorCategory.NOT_FOUND: RecoveryAction(
                strategy=RecoveryStrategy.SKIP_REQUEST,
                max_retries=0
            ),
            ErrorCategory.MALFORMED_REQUEST: RecoveryAction(
                strategy=RecoveryStrategy.SKIP_REQUEST,
                max_retries=0
            ),
            ErrorCategory.SERVER_ERROR: RecoveryAction(
                strategy=RecoveryStrategy.RETRY_WITH_BACKOFF,
                delay_seconds=min(5 * (2 ** attempt), 300),  # Longer backoff for server errors
                max_retries=2
            ),
            ErrorCategory.TIMEOUT: RecoveryAction(
                strategy=RecoveryStrategy.RETRY_WITH_BACKOFF,
                delay_seconds=min(3 ** attempt, 120),
                max_retries=2,
                reduce_concurrency_factor=0.7
            ),
            ErrorCategory.UNKNOWN: RecoveryAction(
                strategy=RecoveryStrategy.RETRY_WITH_BACKOFF,
                delay_seconds=min(2 ** attempt, 30),
                max_retries=1
            )
        }
        
        return recovery_actions.get(category, RecoveryAction(
            strategy=RecoveryStrategy.SKIP_REQUEST,
            max_retries=0
        ))
    
    def handle_batch_failure(
        self,
        failed_batch: List[BatchRequest],
        error: Exception,
        batch_id: Optional[str] = None
    ) -> BatchRecoveryPlan:
        """
        Create recovery plan for a complete batch failure.
        
        Args:
            failed_batch: List of requests that failed
            error: The exception that caused the batch failure
            batch_id: Optional batch identifier for tracking
            
        Returns:
            Recovery plan for the failed batch
        """
        self.logger.error(f"Batch failure for {len(failed_batch)} requests: {error}")
        
        # Categorize the error
        if failed_batch:
            category = self.categorize_error(error, failed_batch[0])
        else:
            category = ErrorCategory.UNKNOWN
        
        # Get recovery action
        recovery_action = self.get_recovery_action(category, 1)
        
        # Create recovery plan based on strategy
        recovery_plan = BatchRecoveryPlan()
        
        if recovery_action.strategy == RecoveryStrategy.RETRY_WITH_BACKOFF:
            recovery_plan.retry_requests = failed_batch.copy()
            recovery_plan.delay_seconds = recovery_action.delay_seconds
            recovery_plan.fallback_strategy = BatchStrategy.SEQUENTIAL
        elif recovery_action.strategy == RecoveryStrategy.RETRY_WITH_DELAY:
            recovery_plan.retry_requests = failed_batch.copy()
            recovery_plan.delay_seconds = recovery_action.delay_seconds
        elif recovery_action.strategy == RecoveryStrategy.FALLBACK_STRATEGY:
            recovery_plan.retry_requests = failed_batch.copy()
            recovery_plan.fallback_strategy = BatchStrategy.SEQUENTIAL
        elif recovery_action.strategy == RecoveryStrategy.SKIP_REQUEST:
            recovery_plan.skip_requests = failed_batch.copy()
        elif recovery_action.strategy == RecoveryStrategy.FAIL_BATCH:
            # Re-raise the error to fail the entire operation
            raise BatchProcessingError(
                f"Batch processing failed with unrecoverable error: {error}",
                batch_id=batch_id,
                cause=error
            )
        
        # Record error context
        for request in failed_batch:
            error_context = ErrorContext(
                error=error,
                request=request,
                attempt=1,
                timestamp=datetime.now(),
                category=category,
                recovery_strategy=recovery_action.strategy
            )
            self._error_history.append(error_context)
        
        return recovery_plan
    
    def handle_partial_failure(
        self,
        successful_results: List[BatchResult],
        failed_requests: List[BatchRequest],
        errors: List[Exception]
    ) -> List[BatchRequest]:
        """
        Handle partial batch failures where some requests succeeded.
        
        Args:
            successful_results: Results that succeeded
            failed_requests: Requests that failed
            errors: Corresponding errors for failed requests
            
        Returns:
            List of requests to retry
        """
        retry_requests = []
        
        for request, error in zip(failed_requests, errors):
            category = self.categorize_error(error, request)
            
            # Get current attempt count for this request
            attempt = self._get_attempt_count(request) + 1
            recovery_action = self.get_recovery_action(category, attempt)
            
            # Record error context
            error_context = ErrorContext(
                error=error,
                request=request,
                attempt=attempt,
                timestamp=datetime.now(),
                category=category,
                recovery_strategy=recovery_action.strategy,
                additional_info={
                    'successful_in_batch': len(successful_results),
                    'failed_in_batch': len(failed_requests)
                }
            )
            self._error_history.append(error_context)
            
            # Decide whether to retry
            if recovery_action.should_retry(attempt):
                if recovery_action.strategy in [
                    RecoveryStrategy.RETRY_WITH_BACKOFF,
                    RecoveryStrategy.RETRY_WITH_DELAY
                ]:
                    retry_requests.append(request)
                    self.logger.info(
                        f"Will retry request {request.cache_key} "
                        f"(attempt {attempt}) after {recovery_action.delay_seconds}s"
                    )
            else:
                self.logger.warning(
                    f"Skipping request {request.cache_key} after {attempt} attempts"
                )
        
        return retry_requests
    
    def should_retry_request(
        self,
        request: BatchRequest,
        error: Exception,
        attempt: int
    ) -> bool:
        """
        Determine if a specific request should be retried.
        
        Args:
            request: The batch request that failed
            error: The exception that occurred
            attempt: Current attempt number
            
        Returns:
            True if the request should be retried
        """
        category = self.categorize_error(error, request)
        recovery_action = self.get_recovery_action(category, attempt)
        
        return recovery_action.should_retry(attempt)
    
    def get_retry_delay(
        self,
        request: BatchRequest,
        error: Exception,
        attempt: int
    ) -> float:
        """
        Get the delay before retrying a request.
        
        Args:
            request: The batch request that failed
            error: The exception that occurred
            attempt: Current attempt number
            
        Returns:
            Delay in seconds before retry
        """
        category = self.categorize_error(error, request)
        recovery_action = self.get_recovery_action(category, attempt)
        
        return recovery_action.delay_seconds
    
    def _get_attempt_count(self, request: BatchRequest) -> int:
        """Get the current attempt count for a request."""
        count = 0
        for error_context in self._error_history:
            if error_context.request.cache_key == request.cache_key:
                count = max(count, error_context.attempt)
        return count
    
    def get_error_statistics(self) -> Dict[str, any]:
        """
        Get statistics about errors and recovery attempts.
        
        Returns:
            Dictionary with error statistics
        """
        stats = {
            'total_errors': len(self._error_history),
            'errors_by_category': {},
            'recovery_success_rates': {},
            'recent_errors': []
        }
        
        # Count errors by category
        for error_context in self._error_history:
            category = error_context.category.value
            if category not in stats['errors_by_category']:
                stats['errors_by_category'][category] = 0
            stats['errors_by_category'][category] += 1
        
        # Calculate recovery success rates
        for category, recovery_stats in self._recovery_stats.items():
            if recovery_stats['total'] > 0:
                success_rate = recovery_stats['successful_recoveries'] / recovery_stats['total']
                stats['recovery_success_rates'][category.value] = success_rate
        
        # Get recent errors (last 10)
        recent_errors = self._error_history[-10:] if self._error_history else []
        stats['recent_errors'] = [
            {
                'timestamp': error_context.timestamp.isoformat(),
                'category': error_context.category.value,
                'strategy': error_context.recovery_strategy.value,
                'attempt': error_context.attempt,
                'request': error_context.request.cache_key,
                'error': str(error_context.error)
            }
            for error_context in recent_errors
        ]
        
        return stats
    
    def clear_error_history(self):
        """Clear the error history (useful for testing or memory management)."""
        self._error_history.clear()
        for category in ErrorCategory:
            self._recovery_stats[category] = {
                'total': 0,
                'successful_recoveries': 0,
                'failed_recoveries': 0
            }


class CircuitBreaker:
    """Circuit breaker pattern for preventing cascading failures."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: Type[Exception] = Exception
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Seconds to wait before attempting recovery
            expected_exception: Type of exception to monitor
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self._failure_count = 0
        self._last_failure_time: Optional[datetime] = None
        self._state = 'closed'  # closed, open, half-open
    
    def call(self, func, *args, **kwargs):
        """
        Call a function through the circuit breaker.
        
        Args:
            func: Function to call
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            Exception: If circuit is open or function fails
        """
        if self._state == 'open':
            if self._should_attempt_reset():
                self._state = 'half-open'
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self._last_failure_time is None:
            return True
        
        return (
            datetime.now() - self._last_failure_time
        ).total_seconds() >= self.recovery_timeout
    
    def _on_success(self):
        """Handle successful call."""
        self._failure_count = 0
        self._state = 'closed'
    
    def _on_failure(self):
        """Handle failed call."""
        self._failure_count += 1
        self._last_failure_time = datetime.now()
        
        if self._failure_count >= self.failure_threshold:
            self._state = 'open'
    
    @property
    def state(self) -> str:
        """Get current circuit breaker state."""
        return self._state
    
    @property
    def failure_count(self) -> int:
        """Get current failure count."""
        return self._failure_count