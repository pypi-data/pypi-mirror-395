"""Improved rate limiting for GitHub API requests."""

import time
from datetime import datetime
from typing import Optional

from .logging_config import get_logger

logger = get_logger(__name__)


class ImprovedRateLimiter:
    """Enhanced rate limiter with proactive and adaptive strategies."""
    
    def __init__(self):
        """Initialize the rate limiter."""
        self.last_request_time = 0
        self.consecutive_low_limits = 0
        self.adaptive_delay = 0.1  # Start with minimal delay
        
    def handle_rate_limit_response(self, remaining: int, reset_time: int) -> None:
        """Handle rate limiting based on API response headers."""
        # Update adaptive delay based on remaining requests
        self._update_adaptive_delay(remaining, reset_time)
        
        # Apply proactive rate limiting
        self._apply_proactive_delay(remaining, reset_time)
        
        # Track request timing
        self.last_request_time = time.time()
    
    def _update_adaptive_delay(self, remaining: int, reset_time: int) -> None:
        """Update adaptive delay based on rate limit status."""
        current_time = int(time.time())
        time_until_reset = max(reset_time - current_time, 1)
        
        if remaining <= 10:
            self.consecutive_low_limits += 1
            # Increase delay more aggressively when consistently low
            multiplier = min(self.consecutive_low_limits * 0.5, 3.0)
            self.adaptive_delay = min(time_until_reset / max(remaining, 1) * multiplier, 30)
        else:
            self.consecutive_low_limits = 0
            # Gradually reduce delay when limits recover
            self.adaptive_delay = max(self.adaptive_delay * 0.9, 0.1)
    
    def _apply_proactive_delay(self, remaining: int, reset_time: int) -> None:
        """Apply proactive delays to prevent hitting rate limits."""
        if remaining <= 0:
            return  # Will be handled by reactive rate limiting
        
        current_time = int(time.time())
        time_until_reset = max(reset_time - current_time, 0)
        
        # Calculate delay based on remaining requests and time
        if remaining <= 3:
            # Critical - long delay
            delay = min(15, time_until_reset / max(remaining, 1))
            logger.warning(f"🚨 Rate limit critical ({remaining} remaining), waiting {delay:.1f}s")
            time.sleep(delay)
        elif remaining <= 10:
            # Very low - significant delay
            delay = min(8, self.adaptive_delay)
            logger.info(f"🐌 Rate limit very low ({remaining} remaining), waiting {delay:.1f}s")
            time.sleep(delay)
        elif remaining <= 25:
            # Low - moderate delay
            delay = min(3, self.adaptive_delay)
            logger.debug(f"⏳ Rate limit low ({remaining} remaining), waiting {delay:.1f}s")
            time.sleep(delay)
        elif remaining <= 50:
            # Getting low - small delay
            delay = min(1, self.adaptive_delay)
            logger.debug(f"⚠️  Rate limit moderate ({remaining} remaining), waiting {delay:.1f}s")
            time.sleep(delay)
    
    def handle_rate_limit_exceeded(self, reset_time: int) -> None:
        """Handle when rate limit is completely exceeded."""
        current_time = int(time.time())
        wait_time = max(reset_time - current_time, 60)  # Wait at least 1 minute
        
        logger.warning(f"💤 Rate limit exceeded. Waiting {wait_time}s until {datetime.fromtimestamp(reset_time)}")
        
        # Use exponential backoff with jitter for additional requests
        base_wait = min(wait_time, 300)  # Cap at 5 minutes
        jitter = base_wait * 0.1  # 10% jitter
        actual_wait = base_wait + (jitter * (0.5 - hash(str(time.time())) % 100 / 100))
        
        try:
            time.sleep(actual_wait)
        except KeyboardInterrupt:
            logger.info("Rate limit wait interrupted by user")
            raise
    
    def get_recommended_delay(self, remaining: int, reset_time: int) -> float:
        """Get recommended delay without applying it."""
        if remaining <= 0:
            return 0
        
        current_time = int(time.time())
        time_until_reset = max(reset_time - current_time, 1)
        
        if remaining <= 5:
            return min(10, time_until_reset / max(remaining, 1))
        elif remaining <= 20:
            return min(3, time_until_reset / max(remaining, 1))
        elif remaining <= 50:
            return 0.5
        else:
            return 0.1


# Global rate limiter instance
_rate_limiter = ImprovedRateLimiter()


def get_rate_limiter() -> ImprovedRateLimiter:
    """Get the global rate limiter instance."""
    return _rate_limiter


def handle_proactive_rate_limiting(remaining: int, reset_time: int) -> None:
    """Handle proactive rate limiting (convenience function)."""
    _rate_limiter.handle_rate_limit_response(remaining, reset_time)


def handle_rate_limit_exceeded(reset_time: int) -> None:
    """Handle rate limit exceeded (convenience function)."""
    _rate_limiter.handle_rate_limit_exceeded(reset_time)