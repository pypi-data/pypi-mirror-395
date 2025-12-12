"""Logging configuration for the GitHub IOC Scanner."""

import logging
import sys
from typing import Optional, Dict, Any
import os


# Custom log levels for user messages
USER_MESSAGE_LEVEL = 25  # Between INFO (20) and WARNING (30)
RATE_LIMIT_DEBUG_LEVEL = 15  # Between DEBUG (10) and INFO (20)

# Add custom log levels
logging.addLevelName(USER_MESSAGE_LEVEL, "USER")
logging.addLevelName(RATE_LIMIT_DEBUG_LEVEL, "RATE_LIMIT_DEBUG")


class UserMessageFilter(logging.Filter):
    """Filter to separate user messages from technical logs."""
    
    def __init__(self, show_user_messages: bool = True):
        super().__init__()
        self.show_user_messages = show_user_messages
    
    def filter(self, record: logging.LogRecord) -> bool:
        # Allow user messages if enabled
        if record.levelno == USER_MESSAGE_LEVEL:
            return self.show_user_messages
        
        # Allow all other messages
        return True


class TechnicalLogFilter(logging.Filter):
    """Filter to show only technical logs (no user messages)."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        # Block user messages from technical logs
        return record.levelno != USER_MESSAGE_LEVEL


class RateLimitDebugFilter(logging.Filter):
    """Filter for rate limit debug messages."""
    
    def __init__(self, debug_rate_limits: bool = False):
        super().__init__()
        self.debug_rate_limits = debug_rate_limits
    
    def filter(self, record: logging.LogRecord) -> bool:
        # Show rate limit debug messages only if enabled
        if record.levelno == RATE_LIMIT_DEBUG_LEVEL:
            return self.debug_rate_limits
        
        # Allow all other messages
        return True


class ErrorSuppressionFilter(logging.Filter):
    """Filter to suppress technical stack traces for known error types."""
    
    def __init__(self, suppress_stack_traces: bool = True):
        super().__init__()
        self.suppress_stack_traces = suppress_stack_traces
    
    def filter(self, record: logging.LogRecord) -> bool:
        if not self.suppress_stack_traces:
            return True
            
        # Check if this is a rate limit or network error that should be suppressed
        if hasattr(record, 'exc_info') and record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            if exc_value and self._should_suppress_error(exc_value):
                # Remove stack trace info for suppressed errors
                record.exc_info = None
                record.exc_text = None
                
        return True
    
    def _should_suppress_error(self, exception: Exception) -> bool:
        """Determine if an error should have its stack trace suppressed."""
        from .error_message_formatter import ErrorMessageFormatter
        return ErrorMessageFormatter.should_suppress_error(exception)


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    include_timestamp: bool = True,
    log_file: Optional[str] = None,
    debug_rate_limits: bool = False,
    suppress_stack_traces: bool = True,
    separate_user_messages: bool = True
) -> None:
    """
    Configure logging for the GitHub IOC Scanner with enhanced user message separation.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        include_timestamp: Whether to include timestamps in log messages
        log_file: Optional file path to write logs to (in addition to console)
        debug_rate_limits: Enable detailed rate limit debugging
        suppress_stack_traces: Suppress stack traces for known error types
        separate_user_messages: Separate user messages from technical logs
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Check environment variables for configuration
    debug_rate_limits = debug_rate_limits or os.getenv('GITHUB_IOC_SCANNER_DEBUG_RATE_LIMITS', '').lower() == 'true'
    suppress_stack_traces = suppress_stack_traces and os.getenv('GITHUB_IOC_SCANNER_SUPPRESS_STACK_TRACES', 'true').lower() != 'false'
    
    # Clear any existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Set root logger level
    root_logger.setLevel(logging.DEBUG)  # Allow all messages, filter at handler level
    
    # Create formatters
    if format_string is None:
        if include_timestamp:
            technical_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            user_format = "%(message)s"  # Simple format for user messages
        else:
            technical_format = "%(name)s - %(levelname)s - %(message)s"
            user_format = "%(message)s"
    else:
        technical_format = format_string
        user_format = "%(message)s"
    
    technical_formatter = logging.Formatter(technical_format, datefmt="%Y-%m-%d %H:%M:%S")
    user_formatter = logging.Formatter(user_format)
    
    # Create console handler for user messages
    if separate_user_messages:
        user_console_handler = logging.StreamHandler(sys.stdout)
        user_console_handler.setLevel(USER_MESSAGE_LEVEL)
        user_console_handler.setFormatter(user_formatter)
        user_console_handler.addFilter(UserMessageFilter(show_user_messages=True))
        root_logger.addHandler(user_console_handler)
    
    # Create console handler for technical logs
    tech_console_handler = logging.StreamHandler(sys.stderr)
    tech_console_handler.setLevel(numeric_level)
    tech_console_handler.setFormatter(technical_formatter)
    
    # Add filters
    if separate_user_messages:
        tech_console_handler.addFilter(TechnicalLogFilter())
    
    tech_console_handler.addFilter(RateLimitDebugFilter(debug_rate_limits=debug_rate_limits))
    tech_console_handler.addFilter(ErrorSuppressionFilter(suppress_stack_traces=suppress_stack_traces))
    
    root_logger.addHandler(tech_console_handler)
    
    # Add file handler if specified
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)  # File gets all messages
            file_handler.setFormatter(technical_formatter)
            
            # File handler gets rate limit debug messages if enabled
            file_handler.addFilter(RateLimitDebugFilter(debug_rate_limits=debug_rate_limits))
            
            # File handler can optionally suppress stack traces
            if suppress_stack_traces:
                file_handler.addFilter(ErrorSuppressionFilter(suppress_stack_traces=False))  # Keep full details in file
            
            root_logger.addHandler(file_handler)
        except (OSError, PermissionError) as e:
            logging.warning(f"Could not create log file {log_file}: {e}")
    
    # Set specific logger levels for external libraries to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def set_log_level(level: str) -> None:
    """
    Change the log level for all loggers.
    
    Args:
        level: New logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Update root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Update all handlers
    for handler in root_logger.handlers:
        handler.setLevel(numeric_level)


def log_user_message(logger: logging.Logger, message: str) -> None:
    """
    Log a user-friendly message that will be displayed to the user.
    
    Args:
        logger: Logger instance to use
        message: User-friendly message to display
    """
    logger.log(USER_MESSAGE_LEVEL, message)


def log_rate_limit_debug(logger: logging.Logger, message: str) -> None:
    """
    Log detailed rate limit debugging information.
    
    Args:
        logger: Logger instance to use
        message: Rate limit debug message
    """
    logger.log(RATE_LIMIT_DEBUG_LEVEL, message)


def log_exception(logger: logging.Logger, message: str, exc: Exception, 
                 suppress_stack_trace: bool = None) -> None:
    """
    Log an exception with optional stack trace suppression.
    
    Args:
        logger: Logger instance to use
        message: Descriptive message about the error context
        exc: Exception instance to log
        suppress_stack_trace: Override stack trace suppression for this exception
    """
    if suppress_stack_trace is None:
        # Use the ErrorMessageFormatter to determine if we should suppress
        from .error_message_formatter import ErrorMessageFormatter
        suppress_stack_trace = ErrorMessageFormatter.should_suppress_error(exc)
    
    if suppress_stack_trace:
        # Log without stack trace
        logger.error(f"{message}: {exc}")
        # Log technical details at debug level
        technical_details = _format_technical_details(exc)
        logger.debug(f"Technical details for '{message}': {technical_details}")
    else:
        # Log with full stack trace
        logger.error(f"{message}: {exc}", exc_info=True)


def log_exception_with_user_message(logger: logging.Logger, user_message: str, 
                                   technical_message: str, exc: Exception) -> None:
    """
    Log an exception with both user-friendly and technical messages.
    
    Args:
        logger: Logger instance to use
        user_message: User-friendly message to display
        technical_message: Technical message for logs
        exc: Exception instance to log
    """
    # Log user-friendly message
    log_user_message(logger, user_message)
    
    # Log technical details
    log_exception(logger, technical_message, exc)


def _format_technical_details(exception: Exception) -> str:
    """
    Format technical details for an exception.
    
    Args:
        exception: The exception to format
        
    Returns:
        Formatted technical details string
    """
    from .error_message_formatter import ErrorMessageFormatter
    return ErrorMessageFormatter.format_technical_details(exception)


def log_performance(logger: logging.Logger, operation: str, duration: float, **kwargs) -> None:
    """
    Log performance information for operations.
    
    Args:
        logger: Logger instance to use
        operation: Name of the operation
        duration: Duration in seconds
        **kwargs: Additional context information
    """
    context = " ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"Performance: {operation} completed in {duration:.3f}s {context}".strip())


def log_rate_limit(logger: logging.Logger, remaining: int, reset_time: int) -> None:
    """
    Log GitHub API rate limit information only when relevant (low or exhausted).
    
    Args:
        logger: Logger instance to use
        remaining: Number of requests remaining
        reset_time: Unix timestamp when rate limit resets
    """
    from datetime import datetime
    
    # Only log rate limit info when it's getting low or critical
    # Skip logging if reset_time is invalid (0 or None - happens with GraphQL)
    if reset_time is None or reset_time <= 0:
        if remaining is not None and remaining <= 0:
            logger.warning(f"⚠️  Rate limit exhausted! (reset time unknown)")
        return
    
    if remaining <= 0:
        # Rate limit exhausted - critical warning
        reset_datetime = datetime.fromtimestamp(reset_time)
        logger.warning(f"⚠️  Rate limit exhausted! Resets at {reset_datetime}")
    elif remaining <= 100:
        # Rate limit getting low - warning
        reset_datetime = datetime.fromtimestamp(reset_time)
        logger.warning(f"⚠️  Rate limit low: {remaining} requests remaining, resets at {reset_datetime}")
    elif remaining <= 500:
        # Rate limit moderately low - info only in verbose mode
        reset_datetime = datetime.fromtimestamp(reset_time)
        logger.info(f"Rate limit: {remaining} requests remaining, resets at {reset_datetime}")
    # For remaining > 500, don't log anything (normal operation)


def log_cache_stats(logger: logging.Logger, hits: int, misses: int, hit_rate: float) -> None:
    """
    Log cache performance statistics.
    
    Args:
        logger: Logger instance to use
        hits: Number of cache hits
        misses: Number of cache misses
        hit_rate: Cache hit rate as percentage
    """
    logger.info(f"Cache stats: {hits} hits, {misses} misses, {hit_rate:.1f}% hit rate")