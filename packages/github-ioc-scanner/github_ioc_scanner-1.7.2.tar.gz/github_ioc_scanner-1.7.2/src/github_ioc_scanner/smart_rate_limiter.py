"""Smart rate limiter that handles large team scans efficiently."""

import time
from datetime import datetime
from typing import Optional

from .logging_config import get_logger

logger = get_logger(__name__)


class SmartRateLimiter:
    """Smart rate limiter optimized for large team scans."""
    
    def __init__(self):
        """Initialize the smart rate limiter."""
        self.last_request_time = 0
        self.request_count = 0
        self.start_time = time.time()
        self.rate_limit_hit_count = 0
        
    def should_wait_before_request(self, remaining: int, reset_time: int) -> Optional[float]:
        """Determine if we should wait before making a request.
        
        Returns:
            Number of seconds to wait, or None if no wait needed
        """
        current_time = time.time()
        
        # Only wait if rate limit is completely exhausted
        if remaining <= 0:
            wait_time = max(reset_time - current_time + 1, 0)
            if wait_time > 0:
                logger.warning(f"🚨 Rate limit exhausted, waiting {wait_time:.1f}s until reset")
                return wait_time
        
        # For low rate limits, don't wait - let the caller decide to use Tree API instead
        if remaining <= 50:
            logger.info(f"⚠️  Rate limit low ({remaining} remaining), recommend using Tree API fallback")
            return None  # Don't wait, let caller handle fallback
        
        # Minimal delay for normal operation to avoid hitting limits too fast
        elif remaining <= 200:
            return 0.1  # Very short delay
        
        return None
    
    def handle_rate_limit_exceeded(self, reset_time: int) -> None:
        """Handle when rate limit is exceeded."""
        self.rate_limit_hit_count += 1
        current_time = time.time()
        wait_time = max(reset_time - current_time + 2, 0)  # Add 2s buffer
        
        logger.warning(f"🚨 Rate limit exceeded (#{self.rate_limit_hit_count}), waiting {wait_time:.1f}s")
        
        if wait_time > 0:
            time.sleep(wait_time)
    
    def log_progress(self, remaining: int, reset_time: int) -> None:
        """Log rate limiting progress."""
        current_time = time.time()
        elapsed = current_time - self.start_time
        self.request_count += 1
        
        # Log every 50 requests or when rate limit is low
        if self.request_count % 50 == 0 or remaining <= 100:
            requests_per_minute = (self.request_count / elapsed) * 60 if elapsed > 0 else 0
            time_until_reset = max(reset_time - current_time, 0)
            
            logger.info(
                f"📊 API Usage: {self.request_count} requests in {elapsed:.1f}s "
                f"({requests_per_minute:.1f}/min), {remaining} remaining, "
                f"resets in {time_until_reset:.0f}s"
            )


# Global rate limiter instance
_smart_rate_limiter = SmartRateLimiter()


def handle_smart_rate_limiting(remaining: int, reset_time: int) -> None:
    """Handle smart rate limiting for API requests."""
    wait_time = _smart_rate_limiter.should_wait_before_request(remaining, reset_time)
    
    if wait_time:
        time.sleep(wait_time)
    
    _smart_rate_limiter.log_progress(remaining, reset_time)


def handle_rate_limit_exceeded(reset_time: int) -> None:
    """Handle when rate limit is exceeded."""
    _smart_rate_limiter.handle_rate_limit_exceeded(reset_time)