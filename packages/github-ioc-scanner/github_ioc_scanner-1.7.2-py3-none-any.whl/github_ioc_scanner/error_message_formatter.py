"""
Error message formatting for user-friendly error display.

This module provides utilities for converting technical exceptions into
clean, user-friendly messages while preserving technical details for debug logging.
"""

from datetime import datetime, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ErrorMessageFormatter:
    """
    Formats error messages for user-friendly display.
    
    This class provides static methods for formatting rate limit messages,
    progress updates, and determining when to suppress technical error details.
    """
    
    @staticmethod
    def format_rate_limit_message(reset_time: datetime, repo_name: Optional[str] = None) -> str:
        """
        Format a user-friendly rate limit message.
        
        Args:
            reset_time: When the rate limit will reset
            repo_name: Optional repository name being processed
            
        Returns:
            Formatted user-friendly message
        """
        now = datetime.now()
        wait_time = reset_time - now
        
        # Format wait time in a human-readable way
        if wait_time.total_seconds() < 60:
            time_str = f"{int(wait_time.total_seconds())} seconds"
        elif wait_time.total_seconds() < 3600:
            minutes = int(wait_time.total_seconds() / 60)
            time_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
        else:
            hours = int(wait_time.total_seconds() / 3600)
            minutes = int((wait_time.total_seconds() % 3600) / 60)
            if minutes > 0:
                time_str = f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
            else:
                time_str = f"{hours} hour{'s' if hours != 1 else ''}"
        
        # Format reset time
        reset_time_str = reset_time.strftime("%H:%M:%S")
        
        # Build the message
        if repo_name:
            message = f"GitHub API rate limit reached while processing {repo_name}. "
        else:
            message = "GitHub API rate limit reached. "
            
        message += f"Waiting {time_str} until reset at {reset_time_str}. "
        message += "Processing will resume automatically."
        
        return message
        
    @staticmethod
    def format_progress_message(current: int, total: int, eta: Optional[str] = None) -> str:
        """
        Format a progress message with ETA updates.
        
        Args:
            current: Current number of items processed
            total: Total number of items to process
            eta: Estimated time of arrival string
            
        Returns:
            Formatted progress message
        """
        percentage = (current / total * 100) if total > 0 else 0
        
        message = f"Progress: {current}/{total} ({percentage:.1f}%)"
        
        if eta:
            message += f" - ETA: {eta}"
            
        return message
        
    @staticmethod
    def format_waiting_message(wait_seconds: int) -> str:
        """
        Format a message indicating the system is waiting for rate limit reset.
        
        Args:
            wait_seconds: Number of seconds to wait
            
        Returns:
            Formatted waiting message
        """
        if wait_seconds < 60:
            time_str = f"{wait_seconds} seconds"
        elif wait_seconds < 3600:
            minutes = wait_seconds // 60
            time_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
        else:
            hours = wait_seconds // 3600
            minutes = (wait_seconds % 3600) // 60
            if minutes > 0:
                time_str = f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
            else:
                time_str = f"{hours} hour{'s' if hours != 1 else ''}"
                
        return f"Waiting {time_str} for rate limit reset..."
        
    @staticmethod
    def should_suppress_error(exception: Exception) -> bool:
        """
        Determine if an error should be suppressed from user display.
        
        Rate limit errors and certain network errors should be handled
        gracefully without showing technical stack traces to users.
        
        Args:
            exception: The exception to evaluate
            
        Returns:
            True if the error should be suppressed from user display
        """
        # Get the exception class name and message
        exception_name = exception.__class__.__name__
        exception_message = str(exception).lower()
        
        # Rate limit related exceptions
        rate_limit_indicators = [
            'ratelimiterror',
            'rate limit',
            'api rate limit exceeded',
            'forbidden',
            'abuse detection',
            'secondary rate limit'
        ]
        
        # Check exception name
        if any(indicator in exception_name.lower() for indicator in rate_limit_indicators):
            return True
            
        # Check exception message
        if any(indicator in exception_message for indicator in rate_limit_indicators):
            return True
            
        # Network-related errors that should be handled gracefully
        network_indicators = [
            'connection',
            'timeout',
            'network',
            'unreachable'
        ]
        
        if any(indicator in exception_message for indicator in network_indicators):
            return True
            
        # Repository state errors that are normal conditions
        repository_state_indicators = [
            'git repository is empty',
            'repository is empty',
            'no commits found',
            'empty repository',
            'is a directory, not a file',
            'may be private or restricted',
            'access denied to repository'
        ]
        
        if any(indicator in exception_message for indicator in repository_state_indicators):
            return True
            
        return False
        
    @staticmethod
    def extract_reset_time_from_exception(exception: Exception) -> Optional[datetime]:
        """
        Extract rate limit reset time from an exception if available.
        
        Args:
            exception: The exception to examine
            
        Returns:
            Reset time if found, None otherwise
        """
        # This is a placeholder implementation
        # In practice, this would examine the exception or its attributes
        # to extract rate limit reset time information
        
        # Check if exception has rate limit information
        if hasattr(exception, 'reset_time'):
            reset_time = exception.reset_time
            if isinstance(reset_time, int):
                # Convert timestamp to datetime
                return datetime.fromtimestamp(reset_time)
            elif isinstance(reset_time, datetime):
                return reset_time
            
        if hasattr(exception, 'response') and hasattr(exception.response, 'headers'):
            # Try to extract from X-RateLimit-Reset header
            headers = exception.response.headers
            if 'X-RateLimit-Reset' in headers:
                try:
                    reset_timestamp = int(headers['X-RateLimit-Reset'])
                    return datetime.fromtimestamp(reset_timestamp)
                except (ValueError, TypeError):
                    pass
                    
        return None
        
    @staticmethod
    def format_technical_details(exception: Exception) -> str:
        """
        Format technical details for debug logging.
        
        Args:
            exception: The exception to format
            
        Returns:
            Formatted technical details string
        """
        details = [
            f"Exception Type: {exception.__class__.__name__}",
            f"Exception Message: {str(exception)}"
        ]
        
        if hasattr(exception, 'response'):
            response = exception.response
            details.append(f"HTTP Status: {getattr(response, 'status_code', 'Unknown')}")
            
            if hasattr(response, 'headers'):
                rate_limit_headers = {
                    k: v for k, v in response.headers.items() 
                    if 'rate' in k.lower() or 'limit' in k.lower()
                }
                if rate_limit_headers:
                    details.append(f"Rate Limit Headers: {rate_limit_headers}")
                    
        return " | ".join(details)