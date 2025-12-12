"""
Rate limit management for GitHub API requests.

This module provides centralized rate limit tracking, status management,
and message deduplication to improve user experience during rate limiting scenarios.
"""

from datetime import datetime, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class RateLimitManager:
    """
    Manages rate limit status tracking and message deduplication.
    
    This class tracks both primary and secondary rate limits, implements
    message cooldown logic to prevent spam, and provides methods for
    checking rate limit status and calculating wait times.
    """
    
    def __init__(self, message_cooldown: int = 60):
        """
        Initialize the RateLimitManager.
        
        Args:
            message_cooldown: Seconds between rate limit messages to prevent spam
        """
        self.primary_limit_reset: Optional[datetime] = None
        self.secondary_limit_reset: Optional[datetime] = None
        self.last_rate_limit_message: Optional[datetime] = None
        self.message_cooldown = message_cooldown
        
    def handle_rate_limit(self, reset_time: datetime, is_secondary: bool = False) -> None:
        """
        Handle a rate limit event by updating internal state.
        
        Args:
            reset_time: When the rate limit will reset
            is_secondary: Whether this is a secondary rate limit
        """
        if is_secondary:
            self.secondary_limit_reset = reset_time
            logger.debug(f"Secondary rate limit hit, resets at {reset_time}")
        else:
            self.primary_limit_reset = reset_time
            logger.debug(f"Primary rate limit hit, resets at {reset_time}")
            
    def should_show_message(self) -> bool:
        """
        Determine if a rate limit message should be shown to the user.
        
        Implements cooldown logic to prevent message spam.
        
        Returns:
            True if a message should be displayed
        """
        now = datetime.now()
        
        if self.last_rate_limit_message is None:
            self.last_rate_limit_message = now
            return True
            
        time_since_last = (now - self.last_rate_limit_message).total_seconds()
        if time_since_last >= self.message_cooldown:
            self.last_rate_limit_message = now
            return True
            
        return False
        
    def get_wait_time(self) -> int:
        """
        Calculate the number of seconds to wait before the next request.
        
        Returns:
            Seconds to wait, or 0 if no rate limit is active
        """
        now = datetime.now()
        wait_times = []
        
        if self.primary_limit_reset and self.primary_limit_reset > now:
            wait_times.append((self.primary_limit_reset - now).total_seconds())
            
        if self.secondary_limit_reset and self.secondary_limit_reset > now:
            wait_times.append((self.secondary_limit_reset - now).total_seconds())
            
        return int(max(wait_times)) if wait_times else 0
        
    def is_rate_limited(self) -> bool:
        """
        Check if any rate limit is currently active.
        
        Returns:
            True if rate limited, False otherwise
        """
        now = datetime.now()
        
        primary_limited = (
            self.primary_limit_reset is not None and 
            self.primary_limit_reset > now
        )
        
        secondary_limited = (
            self.secondary_limit_reset is not None and 
            self.secondary_limit_reset > now
        )
        
        return primary_limited or secondary_limited
        
    def clear_expired_limits(self) -> None:
        """
        Clear any rate limits that have expired.
        
        This method should be called periodically to clean up expired limits.
        """
        now = datetime.now()
        
        if self.primary_limit_reset and self.primary_limit_reset <= now:
            logger.debug("Primary rate limit has expired")
            self.primary_limit_reset = None
            
        if self.secondary_limit_reset and self.secondary_limit_reset <= now:
            logger.debug("Secondary rate limit has expired")
            self.secondary_limit_reset = None
            
    def get_status_summary(self) -> dict:
        """
        Get a summary of current rate limit status.
        
        Returns:
            Dictionary with rate limit status information
        """
        now = datetime.now()
        
        return {
            'is_rate_limited': self.is_rate_limited(),
            'wait_time_seconds': self.get_wait_time(),
            'primary_limit_active': (
                self.primary_limit_reset is not None and 
                self.primary_limit_reset > now
            ),
            'secondary_limit_active': (
                self.secondary_limit_reset is not None and 
                self.secondary_limit_reset > now
            ),
            'primary_reset_time': self.primary_limit_reset,
            'secondary_reset_time': self.secondary_limit_reset
        }


# Compatibility class for ParallelBatchProcessor
# This is a temporary stub to avoid breaking existing code
class ParallelRateLimitManager:
    """
    Compatibility rate limit manager for ParallelBatchProcessor.
    
    This is a stub implementation to maintain compatibility with existing code
    while the new RateLimitManager is being integrated.
    """
    
    def __init__(self, initial_concurrency=5, max_concurrency=10, min_concurrency=1, 
                 buffer_percentage=0.1, adjustment_interval=10.0):
        """Initialize with compatibility parameters."""
        self.initial_concurrency = initial_concurrency
        self.max_concurrency = max_concurrency
        self.min_concurrency = min_concurrency
        self.buffer_percentage = buffer_percentage
        self.adjustment_interval = adjustment_interval
        self.current_concurrency = initial_concurrency
        
    def get_current_concurrency(self):
        """Get current concurrency level."""
        return self.current_concurrency
        
    def get_rate_limit_status(self):
        """Get rate limit status."""
        return None  # Stub implementation
        
    async def update_rate_limit_info(self, remaining, limit, reset_time=None):
        """Update rate limit information."""
        return self.current_concurrency  # Stub implementation
        
    async def handle_rate_limit_exceeded(self):
        """Handle rate limit exceeded."""
        return self.current_concurrency, 60  # Stub implementation
        
    async def update_performance_metrics(self, success_rate, error_rate, avg_response_time):
        """Update performance metrics."""
        pass  # Stub implementation
        
    def get_statistics(self):
        """Get statistics."""
        return {}  # Stub implementation