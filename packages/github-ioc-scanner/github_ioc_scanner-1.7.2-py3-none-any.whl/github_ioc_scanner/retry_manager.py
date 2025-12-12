"""Retry manager with exponential backoff and jitter for robust error handling."""

import asyncio
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union

from .exceptions import RateLimitError, NetworkError, APIError, AuthenticationError
from .logging_config import get_logger

logger = get_logger(__name__)


class RetryStrategy(Enum):
    """Different retry strategies."""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    FIXED_DELAY = "fixed_delay"
    FIBONACCI_BACKOFF = "fibonacci_backoff"


@dataclass
class RetryAttempt:
    """Information about a retry attempt."""
    attempt_number: int
    delay_seconds: float
    error: Exception
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def error_type(self) -> str:
        """Get the error type as a string."""
        return type(self.error).__name__


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    backoff_multiplier: float = 2.0
    jitter_range: float = 0.1  # 10% jitter
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    
    # Error-specific configurations
    rate_limit_max_attempts: int = 5
    rate_limit_base_delay: float = 2.0
    network_max_attempts: int = 4
    network_base_delay: float = 1.0
    
    # Retryable error types
    retryable_errors: List[Type[Exception]] = field(default_factory=lambda: [
        RateLimitError, NetworkError, APIError
    ])
    
    # Non-retryable error types
    non_retryable_errors: List[Type[Exception]] = field(default_factory=lambda: [
        AuthenticationError
    ])
    
    def validate(self) -> List[str]:
        """Validate retry configuration."""
        errors = []
        
        if self.max_attempts < 1:
            errors.append("max_attempts must be at least 1")
        
        if self.base_delay < 0:
            errors.append("base_delay must be non-negative")
        
        if self.max_delay < self.base_delay:
            errors.append("max_delay must be >= base_delay")
        
        if self.backoff_multiplier <= 1.0:
            errors.append("backoff_multiplier must be > 1.0")
        
        if not 0 <= self.jitter_range <= 1.0:
            errors.append("jitter_range must be between 0 and 1")
        
        return errors


@dataclass
class RetryStatistics:
    """Statistics about retry operations."""
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    total_retry_attempts: int = 0
    total_retry_delay: float = 0.0
    
    # Error type statistics
    error_counts: Dict[str, int] = field(default_factory=dict)
    retry_counts_by_error: Dict[str, int] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.successful_operations / self.total_operations) * 100
    
    @property
    def average_retry_delay(self) -> float:
        """Calculate average retry delay."""
        if self.total_retry_attempts == 0:
            return 0.0
        return self.total_retry_delay / self.total_retry_attempts
    
    @property
    def retry_rate(self) -> float:
        """Calculate retry rate percentage."""
        if self.total_operations == 0:
            return 0.0
        return (self.total_retry_attempts / self.total_operations) * 100


class RetryManager:
    """Manages retry logic with exponential backoff and jitter."""
    
    def __init__(self, config: Optional[RetryConfig] = None):
        """Initialize retry manager.
        
        Args:
            config: Retry configuration
        """
        self.config = config or RetryConfig()
        
        # Validate configuration
        config_errors = self.config.validate()
        if config_errors:
            raise ValueError(f"Invalid retry configuration: {', '.join(config_errors)}")
        
        # Statistics tracking
        self.statistics = RetryStatistics()
        self.retry_history: List[RetryAttempt] = []
        
        # Circuit breaker state (simple implementation)
        self.circuit_breaker_failures = 0
        self.circuit_breaker_threshold = 10
        self.circuit_breaker_reset_time = 0.0
        self.circuit_breaker_timeout = 300.0  # 5 minutes
    
    async def execute_with_retry(
        self,
        operation: Callable[[], Any],
        operation_name: str = "operation",
        custom_config: Optional[RetryConfig] = None
    ) -> Any:
        """Execute an operation with retry logic.
        
        Args:
            operation: Async function to execute
            operation_name: Name of the operation for logging
            custom_config: Custom retry configuration for this operation
            
        Returns:
            Result of the operation
            
        Raises:
            Exception: The last exception if all retries fail
        """
        config = custom_config or self.config
        self.statistics.total_operations += 1
        
        # Check circuit breaker
        if self._is_circuit_breaker_open():
            logger.warning(f"Circuit breaker open, skipping {operation_name}")
            raise APIError("Circuit breaker is open, too many recent failures")
        
        last_exception = None
        retry_attempts = []
        
        for attempt in range(config.max_attempts):
            try:
                # Execute the operation
                result = await operation()
                
                # Success - update statistics and reset circuit breaker
                self.statistics.successful_operations += 1
                self._reset_circuit_breaker()
                
                # Log retry statistics if there were retries
                if retry_attempts:
                    total_delay = sum(r.delay_seconds for r in retry_attempts)
                    logger.info(
                        f"{operation_name} succeeded after {len(retry_attempts)} retries "
                        f"(total delay: {total_delay:.2f}s)"
                    )
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # Check if error is retryable
                if not self._is_retryable_error(e, config):
                    logger.debug(f"{operation_name} failed with non-retryable error: {e}")
                    self.statistics.failed_operations += 1
                    self._record_circuit_breaker_failure()
                    raise e
                
                # Don't retry on last attempt
                if attempt == config.max_attempts - 1:
                    break
                
                # Calculate delay for retry
                delay = self._calculate_retry_delay(
                    attempt, e, config, operation_name
                )
                
                # Record retry attempt
                retry_attempt = RetryAttempt(
                    attempt_number=attempt + 1,
                    delay_seconds=delay,
                    error=e
                )
                retry_attempts.append(retry_attempt)
                self.retry_history.append(retry_attempt)
                
                # Update statistics
                self.statistics.total_retry_attempts += 1
                self.statistics.total_retry_delay += delay
                
                error_type = type(e).__name__
                self.statistics.error_counts[error_type] = (
                    self.statistics.error_counts.get(error_type, 0) + 1
                )
                self.statistics.retry_counts_by_error[error_type] = (
                    self.statistics.retry_counts_by_error.get(error_type, 0) + 1
                )
                
                logger.debug(
                    f"{operation_name} attempt {attempt + 1} failed: {e}. "
                    f"Retrying in {delay:.2f}s"
                )
                
                # Wait before retry
                await asyncio.sleep(delay)
        
        # All retries failed
        self.statistics.failed_operations += 1
        self._record_circuit_breaker_failure()
        
        logger.warning(
            f"{operation_name} failed after {config.max_attempts} attempts. "
            f"Last error: {last_exception}"
        )
        
        raise last_exception
    
    def _is_retryable_error(self, error: Exception, config: RetryConfig) -> bool:
        """Check if an error is retryable.
        
        Args:
            error: Exception to check
            config: Retry configuration
            
        Returns:
            True if error is retryable
        """
        # Check non-retryable errors first
        for non_retryable_type in config.non_retryable_errors:
            if isinstance(error, non_retryable_type):
                return False
        
        # Check retryable errors
        for retryable_type in config.retryable_errors:
            if isinstance(error, retryable_type):
                # For API errors, check status code if available
                if isinstance(error, APIError) and hasattr(error, 'status_code'):
                    # Retry server errors (5xx) but not client errors (4xx)
                    return 500 <= error.status_code < 600
                return True
        
        return False
    
    def _calculate_retry_delay(
        self,
        attempt: int,
        error: Exception,
        config: RetryConfig,
        operation_name: str
    ) -> float:
        """Calculate delay before retry.
        
        Args:
            attempt: Current attempt number (0-based)
            error: Exception that occurred
            config: Retry configuration
            operation_name: Name of operation for logging
            
        Returns:
            Delay in seconds
        """
        # Use error-specific configuration if available
        if isinstance(error, RateLimitError):
            base_delay = config.rate_limit_base_delay
            # For rate limit errors, use the reset time if available
            if hasattr(error, 'reset_time') and error.reset_time:
                reset_delay = max(0, error.reset_time - time.time())
                if reset_delay > 0:
                    logger.debug(f"Using rate limit reset time: {reset_delay:.2f}s")
                    return min(reset_delay, config.max_delay)
        elif isinstance(error, NetworkError):
            base_delay = config.network_base_delay
        else:
            base_delay = config.base_delay
        
        # Calculate delay based on strategy
        if config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = base_delay * (config.backoff_multiplier ** attempt)
        elif config.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = base_delay * (attempt + 1)
        elif config.strategy == RetryStrategy.FIXED_DELAY:
            delay = base_delay
        elif config.strategy == RetryStrategy.FIBONACCI_BACKOFF:
            delay = base_delay * self._fibonacci(attempt + 1)
        else:
            delay = base_delay * (config.backoff_multiplier ** attempt)
        
        # Apply jitter to prevent thundering herd
        if config.jitter_range > 0:
            jitter = random.uniform(-config.jitter_range, config.jitter_range)
            delay = delay * (1 + jitter)
        
        # Ensure minimum delay
        delay = max(delay, 0.1)
        
        # Apply maximum delay limit
        delay = min(delay, config.max_delay)
        
        return delay
    
    def _fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def _is_circuit_breaker_open(self) -> bool:
        """Check if circuit breaker is open."""
        if self.circuit_breaker_failures < self.circuit_breaker_threshold:
            return False
        
        # Check if timeout has passed
        if time.time() > self.circuit_breaker_reset_time:
            self._reset_circuit_breaker()
            return False
        
        return True
    
    def _record_circuit_breaker_failure(self) -> None:
        """Record a failure for circuit breaker."""
        self.circuit_breaker_failures += 1
        if self.circuit_breaker_failures >= self.circuit_breaker_threshold:
            self.circuit_breaker_reset_time = time.time() + self.circuit_breaker_timeout
            logger.warning(
                f"Circuit breaker opened due to {self.circuit_breaker_failures} failures. "
                f"Will reset in {self.circuit_breaker_timeout}s"
            )
    
    def _reset_circuit_breaker(self) -> None:
        """Reset circuit breaker state."""
        if self.circuit_breaker_failures > 0:
            logger.info("Circuit breaker reset after successful operation")
        self.circuit_breaker_failures = 0
        self.circuit_breaker_reset_time = 0.0
    
    def get_statistics(self) -> RetryStatistics:
        """Get retry statistics.
        
        Returns:
            Current retry statistics
        """
        return self.statistics
    
    def get_recent_retry_history(self, limit: int = 10) -> List[RetryAttempt]:
        """Get recent retry attempts.
        
        Args:
            limit: Maximum number of attempts to return
            
        Returns:
            List of recent retry attempts
        """
        return self.retry_history[-limit:] if self.retry_history else []
    
    def reset_statistics(self) -> None:
        """Reset retry statistics."""
        self.statistics = RetryStatistics()
        self.retry_history.clear()
    
    def create_error_specific_config(
        self,
        error_type: Type[Exception],
        max_attempts: Optional[int] = None,
        base_delay: Optional[float] = None
    ) -> RetryConfig:
        """Create error-specific retry configuration.
        
        Args:
            error_type: Type of error to configure for
            max_attempts: Maximum retry attempts for this error type
            base_delay: Base delay for this error type
            
        Returns:
            Customized retry configuration
        """
        config = RetryConfig(
            max_attempts=max_attempts or self.config.max_attempts,
            base_delay=base_delay or self.config.base_delay,
            max_delay=self.config.max_delay,
            backoff_multiplier=self.config.backoff_multiplier,
            jitter_range=self.config.jitter_range,
            strategy=self.config.strategy,
            retryable_errors=self.config.retryable_errors.copy(),
            non_retryable_errors=self.config.non_retryable_errors.copy()
        )
        
        # Apply error-specific defaults
        if error_type == RateLimitError:
            config.max_attempts = max_attempts or self.config.rate_limit_max_attempts
            config.base_delay = base_delay or self.config.rate_limit_base_delay
        elif error_type == NetworkError:
            config.max_attempts = max_attempts or self.config.network_max_attempts
            config.base_delay = base_delay or self.config.network_base_delay
        
        return config
    
    def get_circuit_breaker_status(self) -> Dict[str, Any]:
        """Get circuit breaker status.
        
        Returns:
            Dictionary with circuit breaker information
        """
        return {
            'is_open': self._is_circuit_breaker_open(),
            'failure_count': self.circuit_breaker_failures,
            'threshold': self.circuit_breaker_threshold,
            'reset_time': self.circuit_breaker_reset_time,
            'timeout_seconds': self.circuit_breaker_timeout
        }


# Decorator for easy retry functionality
def retry_on_error(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF,
    retryable_errors: Optional[List[Type[Exception]]] = None
):
    """Decorator to add retry functionality to async functions.
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Base delay between retries
        strategy: Retry strategy to use
        retryable_errors: List of retryable error types
        
    Returns:
        Decorated function with retry capability
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            config = RetryConfig(
                max_attempts=max_attempts,
                base_delay=base_delay,
                strategy=strategy,
                retryable_errors=retryable_errors or [RateLimitError, NetworkError, APIError]
            )
            
            retry_manager = RetryManager(config)
            
            async def operation():
                return await func(*args, **kwargs)
            
            return await retry_manager.execute_with_retry(
                operation, 
                operation_name=func.__name__
            )
        
        return wrapper
    return decorator