"""
Intelligent rate limit prevention for GitHub API requests.

This module provides proactive request throttling, budget distribution across repositories,
and adaptive request timing to maximize throughput while respecting GitHub's limits.
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field

from .logging_config import get_logger

logger = get_logger(__name__)


class RateLimitStrategy(Enum):
    """Rate limiting strategies for different use cases."""
    CONSERVATIVE = "conservative"  # Prioritize avoiding rate limits
    NORMAL = "normal"             # Balanced approach
    AGGRESSIVE = "aggressive"     # Maximize throughput


@dataclass
class RateLimitBudget:
    """Rate limit budget for a specific time window."""
    total_requests: int
    used_requests: int
    remaining_requests: int
    reset_time: datetime
    reserved_requests: int = 0  # Requests reserved for critical operations
    
    @property
    def available_requests(self) -> int:
        """Get available requests after reservations."""
        return max(0, self.remaining_requests - self.reserved_requests)
    
    @property
    def utilization_ratio(self) -> float:
        """Get current utilization ratio (0.0 to 1.0)."""
        if self.total_requests == 0:
            return 0.0
        return self.used_requests / self.total_requests
    
    @property
    def time_remaining_seconds(self) -> int:
        """Get seconds remaining until reset."""
        return max(0, int((self.reset_time - datetime.now()).total_seconds()))


@dataclass
class RepositoryBudget:
    """Budget allocation for a specific repository."""
    repo_name: str
    allocated_requests: int
    used_requests: int = 0
    priority: float = 1.0  # Higher priority gets more budget
    estimated_requests_needed: int = 0
    
    @property
    def remaining_requests(self) -> int:
        """Get remaining requests for this repository."""
        return max(0, self.allocated_requests - self.used_requests)
    
    @property
    def utilization_ratio(self) -> float:
        """Get utilization ratio for this repository."""
        if self.allocated_requests == 0:
            return 0.0
        return self.used_requests / self.allocated_requests


class IntelligentRateLimiter:
    """
    Intelligent rate limiter with proactive throttling and budget distribution.
    
    This class implements sophisticated rate limiting strategies including:
    - Proactive request throttling before hitting limits
    - Budget distribution across repositories
    - Adaptive request timing based on remaining quota
    - Multiple strategies for different use cases
    """
    
    def __init__(self, strategy: RateLimitStrategy = RateLimitStrategy.NORMAL):
        """
        Initialize the intelligent rate limiter.
        
        Args:
            strategy: Rate limiting strategy to use
        """
        self.strategy = strategy
        self.budget: Optional[RateLimitBudget] = None
        self.repository_budgets: Dict[str, RepositoryBudget] = {}
        self.request_history: List[Tuple[datetime, str]] = []  # (timestamp, repo_name)
        self.last_budget_update = datetime.now()
        self.adaptive_delay = 0.1
        self.consecutive_throttles = 0
        
        # Strategy-specific settings
        self._configure_strategy()
    
    def _configure_strategy(self) -> None:
        """Configure settings based on selected strategy."""
        if self.strategy == RateLimitStrategy.CONSERVATIVE:
            self.safety_margin = 100  # Keep 100 requests in reserve
            self.throttle_threshold = 0.6  # Start throttling at 60% usage
            self.max_burst_requests = 5
            self.base_delay = 0.5
        elif self.strategy == RateLimitStrategy.NORMAL:
            self.safety_margin = 50   # Keep 50 requests in reserve
            self.throttle_threshold = 0.75  # Start throttling at 75% usage
            self.max_burst_requests = 10
            self.base_delay = 0.2
        else:  # AGGRESSIVE
            self.safety_margin = 20   # Keep 20 requests in reserve
            self.throttle_threshold = 0.85  # Start throttling at 85% usage
            self.max_burst_requests = 20
            self.base_delay = 0.1
    
    def update_rate_limit_status(
        self, 
        remaining: int, 
        total: int, 
        reset_time: int,
        repo_name: Optional[str] = None
    ) -> None:
        """
        Update rate limit status from API response headers.
        
        Args:
            remaining: Remaining requests in current window
            total: Total requests allowed in window
            reset_time: Unix timestamp when rate limit resets
            repo_name: Name of repository making the request
        """
        reset_datetime = datetime.fromtimestamp(reset_time)
        used = total - remaining
        
        # Update global budget
        self.budget = RateLimitBudget(
            total_requests=total,
            used_requests=used,
            remaining_requests=remaining,
            reset_time=reset_datetime,
            reserved_requests=self.safety_margin
        )
        
        # Track request for this repository
        if repo_name:
            self._track_repository_request(repo_name)
        
        # Update adaptive delay based on current status
        self._update_adaptive_delay()
        
        logger.debug(
            f"Rate limit status: {remaining}/{total} remaining, "
            f"resets at {reset_datetime}, strategy: {self.strategy.value}"
        )
    
    def _track_repository_request(self, repo_name: str) -> None:
        """Track a request for a specific repository."""
        now = datetime.now()
        self.request_history.append((now, repo_name))
        
        # Clean old history (keep last hour)
        cutoff = now - timedelta(hours=1)
        self.request_history = [
            (ts, repo) for ts, repo in self.request_history 
            if ts > cutoff
        ]
        
        # Update repository budget usage
        if repo_name in self.repository_budgets:
            self.repository_budgets[repo_name].used_requests += 1
    
    def _update_adaptive_delay(self) -> None:
        """Update adaptive delay based on current rate limit status."""
        if not self.budget:
            return
        
        utilization = self.budget.utilization_ratio
        time_remaining = self.budget.time_remaining_seconds
        
        if utilization > self.throttle_threshold:
            # Increase delay as we approach limits
            excess_utilization = utilization - self.throttle_threshold
            delay_multiplier = 1 + (excess_utilization * 10)  # Scale up delay
            self.adaptive_delay = min(self.base_delay * delay_multiplier, 30.0)
            self.consecutive_throttles += 1
        else:
            # Gradually reduce delay when utilization is low
            self.adaptive_delay = max(self.adaptive_delay * 0.9, self.base_delay)
            self.consecutive_throttles = 0
        
        # Factor in time pressure
        if time_remaining < 300 and self.budget.remaining_requests > 100:
            # Less than 5 minutes left but plenty of requests - speed up
            self.adaptive_delay *= 0.5
        elif time_remaining > 1800 and self.budget.remaining_requests < 100:
            # More than 30 minutes left but few requests - slow down
            self.adaptive_delay *= 2.0
    
    def allocate_repository_budgets(self, repositories: List[str]) -> None:
        """
        Allocate rate limit budget across repositories.
        
        Args:
            repositories: List of repository names to allocate budget for
        """
        if not self.budget or not repositories:
            return
        
        available_requests = self.budget.available_requests
        
        # Calculate priorities based on historical usage and estimated needs
        repo_priorities = self._calculate_repository_priorities(repositories)
        total_priority = sum(repo_priorities.values())
        
        if total_priority == 0:
            # Equal distribution if no priority data
            requests_per_repo = available_requests // len(repositories)
            for repo in repositories:
                self.repository_budgets[repo] = RepositoryBudget(
                    repo_name=repo,
                    allocated_requests=requests_per_repo,
                    priority=1.0
                )
        else:
            # Weighted distribution based on priorities
            for repo in repositories:
                priority = repo_priorities.get(repo, 1.0)
                allocated = int((priority / total_priority) * available_requests)
                
                self.repository_budgets[repo] = RepositoryBudget(
                    repo_name=repo,
                    allocated_requests=allocated,
                    priority=priority,
                    estimated_requests_needed=self._estimate_requests_needed(repo)
                )
        
        logger.info(
            f"Allocated rate limit budget across {len(repositories)} repositories. "
            f"Available requests: {available_requests}"
        )
    
    def _calculate_repository_priorities(self, repositories: List[str]) -> Dict[str, float]:
        """Calculate priority scores for repositories based on historical data."""
        priorities = {}
        
        # Count recent requests per repository
        recent_requests = {}
        for _, repo in self.request_history:
            recent_requests[repo] = recent_requests.get(repo, 0) + 1
        
        for repo in repositories:
            # Base priority
            priority = 1.0
            
            # Boost priority for repositories with recent activity
            if repo in recent_requests:
                priority += recent_requests[repo] * 0.1
            
            # Boost priority for repositories with existing budget allocation
            if repo in self.repository_budgets:
                existing_budget = self.repository_budgets[repo]
                if existing_budget.utilization_ratio < 0.5:
                    # Under-utilized repositories get lower priority
                    priority *= 0.8
                elif existing_budget.utilization_ratio > 0.9:
                    # High-utilization repositories get higher priority
                    priority *= 1.2
            
            priorities[repo] = priority
        
        return priorities
    
    def _estimate_requests_needed(self, repo_name: str) -> int:
        """Estimate number of requests needed for a repository."""
        # This is a simplified estimation - in practice, this could be based on
        # repository size, file count, scan history, etc.
        base_estimate = 50  # Base estimate for any repository
        
        # Adjust based on historical usage
        if repo_name in self.repository_budgets:
            historical_usage = self.repository_budgets[repo_name].used_requests
            base_estimate = max(base_estimate, historical_usage)
        
        return base_estimate
    
    async def should_throttle_request(self, repo_name: Optional[str] = None) -> bool:
        """
        Determine if a request should be throttled.
        
        Args:
            repo_name: Name of repository making the request
            
        Returns:
            True if request should be throttled
        """
        if not self.budget:
            return False
        
        # Check global budget
        if self.budget.available_requests <= 0:
            return True
        
        # Check repository-specific budget
        if repo_name and repo_name in self.repository_budgets:
            repo_budget = self.repository_budgets[repo_name]
            if repo_budget.remaining_requests <= 0:
                return True
        
        # Check if we're approaching limits
        utilization = self.budget.utilization_ratio
        if utilization > self.throttle_threshold:
            return True
        
        return False
    
    async def get_throttle_delay(self, repo_name: Optional[str] = None) -> float:
        """
        Get the recommended delay before making a request.
        
        Args:
            repo_name: Name of repository making the request
            
        Returns:
            Delay in seconds
        """
        if not self.budget:
            return self.base_delay
        
        # Base delay from adaptive calculation
        delay = self.adaptive_delay
        
        # Adjust based on repository-specific budget
        if repo_name and repo_name in self.repository_budgets:
            repo_budget = self.repository_budgets[repo_name]
            if repo_budget.remaining_requests <= 5:
                # Very low repository budget - increase delay
                delay *= 2.0
            elif repo_budget.utilization_ratio > 0.8:
                # High repository utilization - moderate increase
                delay *= 1.5
        
        # Adjust based on global budget status
        if self.budget.available_requests <= 10:
            delay *= 3.0  # Critical - long delay
        elif self.budget.available_requests <= 50:
            delay *= 2.0  # Low - significant delay
        elif self.budget.utilization_ratio > 0.9:
            delay *= 1.5  # High utilization - moderate delay
        
        # Factor in consecutive throttles (exponential backoff)
        if self.consecutive_throttles > 0:
            backoff_multiplier = min(2 ** (self.consecutive_throttles - 1), 8)
            delay *= backoff_multiplier
        
        return min(delay, 60.0)  # Cap at 1 minute
    
    async def wait_for_budget_availability(self, repo_name: Optional[str] = None) -> None:
        """
        Wait until budget is available for making requests.
        
        Args:
            repo_name: Name of repository making the request
        """
        if not await self.should_throttle_request(repo_name):
            return
        
        delay = await self.get_throttle_delay(repo_name)
        
        if delay > 0:
            if repo_name:
                logger.info(
                    f"🐌 Throttling requests for {repo_name} - waiting {delay:.1f}s "
                    f"(strategy: {self.strategy.value})"
                )
            else:
                logger.info(
                    f"🐌 Throttling requests - waiting {delay:.1f}s "
                    f"(strategy: {self.strategy.value})"
                )
            
            await asyncio.sleep(delay)
    
    def redistribute_unused_budget(self) -> None:
        """Redistribute unused budget from low-activity repositories."""
        if not self.budget or not self.repository_budgets:
            return
        
        # Find repositories with unused budget
        unused_budget = 0
        active_repos = []
        
        for repo_name, repo_budget in self.repository_budgets.items():
            if repo_budget.utilization_ratio < 0.3:  # Less than 30% used
                unused = int(repo_budget.remaining_requests * 0.5)  # Reclaim 50%
                unused_budget += unused
                repo_budget.allocated_requests -= unused
            elif repo_budget.utilization_ratio > 0.8:  # More than 80% used
                active_repos.append(repo_name)
        
        # Redistribute to active repositories
        if unused_budget > 0 and active_repos:
            budget_per_active = unused_budget // len(active_repos)
            for repo_name in active_repos:
                self.repository_budgets[repo_name].allocated_requests += budget_per_active
            
            logger.debug(
                f"Redistributed {unused_budget} unused requests to {len(active_repos)} active repositories"
            )
    
    def get_budget_status(self) -> Dict[str, any]:
        """Get current budget status for monitoring."""
        status = {
            'strategy': self.strategy.value,
            'adaptive_delay': self.adaptive_delay,
            'consecutive_throttles': self.consecutive_throttles,
            'global_budget': None,
            'repository_budgets': {}
        }
        
        if self.budget:
            status['global_budget'] = {
                'total_requests': self.budget.total_requests,
                'used_requests': self.budget.used_requests,
                'remaining_requests': self.budget.remaining_requests,
                'available_requests': self.budget.available_requests,
                'utilization_ratio': self.budget.utilization_ratio,
                'time_remaining_seconds': self.budget.time_remaining_seconds,
                'reset_time': self.budget.reset_time.isoformat()
            }
        
        for repo_name, repo_budget in self.repository_budgets.items():
            status['repository_budgets'][repo_name] = {
                'allocated_requests': repo_budget.allocated_requests,
                'used_requests': repo_budget.used_requests,
                'remaining_requests': repo_budget.remaining_requests,
                'utilization_ratio': repo_budget.utilization_ratio,
                'priority': repo_budget.priority
            }
        
        return status


# Global intelligent rate limiter instance
_intelligent_limiter = IntelligentRateLimiter()


def get_intelligent_rate_limiter() -> IntelligentRateLimiter:
    """Get the global intelligent rate limiter instance."""
    return _intelligent_limiter


def set_rate_limit_strategy(strategy: RateLimitStrategy) -> None:
    """Set the global rate limiting strategy."""
    global _intelligent_limiter
    _intelligent_limiter = IntelligentRateLimiter(strategy)
    logger.info(f"Rate limiting strategy set to: {strategy.value}")