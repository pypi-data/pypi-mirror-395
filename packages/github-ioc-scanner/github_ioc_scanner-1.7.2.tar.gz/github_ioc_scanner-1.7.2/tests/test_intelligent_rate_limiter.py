"""Tests for intelligent rate limiter functionality."""

import asyncio
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from src.github_ioc_scanner.intelligent_rate_limiter import (
    IntelligentRateLimiter,
    RateLimitStrategy,
    RateLimitBudget,
    RepositoryBudget,
    get_intelligent_rate_limiter,
    set_rate_limit_strategy
)


class TestRateLimitBudget:
    """Test RateLimitBudget data class."""
    
    def test_budget_initialization(self):
        """Test budget initialization with default values."""
        reset_time = datetime.now() + timedelta(hours=1)
        budget = RateLimitBudget(
            total_requests=5000,
            used_requests=1000,
            remaining_requests=4000,
            reset_time=reset_time
        )
        
        assert budget.total_requests == 5000
        assert budget.used_requests == 1000
        assert budget.remaining_requests == 4000
        assert budget.reserved_requests == 0
        assert budget.available_requests == 4000
        assert budget.utilization_ratio == 0.2
        assert budget.time_remaining_seconds > 0
    
    def test_budget_with_reservations(self):
        """Test budget calculations with reserved requests."""
        reset_time = datetime.now() + timedelta(hours=1)
        budget = RateLimitBudget(
            total_requests=5000,
            used_requests=1000,
            remaining_requests=4000,
            reset_time=reset_time,
            reserved_requests=500
        )
        
        assert budget.available_requests == 3500
        assert budget.utilization_ratio == 0.2
    
    def test_budget_time_remaining(self):
        """Test time remaining calculation."""
        # Future reset time
        future_reset = datetime.now() + timedelta(minutes=30)
        budget = RateLimitBudget(
            total_requests=5000,
            used_requests=1000,
            remaining_requests=4000,
            reset_time=future_reset
        )
        assert budget.time_remaining_seconds > 1700  # Approximately 30 minutes
        
        # Past reset time
        past_reset = datetime.now() - timedelta(minutes=10)
        budget.reset_time = past_reset
        assert budget.time_remaining_seconds == 0


class TestRepositoryBudget:
    """Test RepositoryBudget data class."""
    
    def test_repository_budget_initialization(self):
        """Test repository budget initialization."""
        budget = RepositoryBudget(
            repo_name="owner/repo",
            allocated_requests=100,
            priority=1.5
        )
        
        assert budget.repo_name == "owner/repo"
        assert budget.allocated_requests == 100
        assert budget.used_requests == 0
        assert budget.priority == 1.5
        assert budget.remaining_requests == 100
        assert budget.utilization_ratio == 0.0
    
    def test_repository_budget_utilization(self):
        """Test repository budget utilization calculations."""
        budget = RepositoryBudget(
            repo_name="owner/repo",
            allocated_requests=100,
            used_requests=25
        )
        
        assert budget.remaining_requests == 75
        assert budget.utilization_ratio == 0.25


class TestIntelligentRateLimiter:
    """Test IntelligentRateLimiter class."""
    
    def test_initialization_default_strategy(self):
        """Test initialization with default strategy."""
        limiter = IntelligentRateLimiter()
        
        assert limiter.strategy == RateLimitStrategy.NORMAL
        assert limiter.safety_margin == 50
        assert limiter.throttle_threshold == 0.75
        assert limiter.max_burst_requests == 10
        assert limiter.base_delay == 0.2
    
    def test_initialization_conservative_strategy(self):
        """Test initialization with conservative strategy."""
        limiter = IntelligentRateLimiter(RateLimitStrategy.CONSERVATIVE)
        
        assert limiter.strategy == RateLimitStrategy.CONSERVATIVE
        assert limiter.safety_margin == 100
        assert limiter.throttle_threshold == 0.6
        assert limiter.max_burst_requests == 5
        assert limiter.base_delay == 0.5
    
    def test_initialization_aggressive_strategy(self):
        """Test initialization with aggressive strategy."""
        limiter = IntelligentRateLimiter(RateLimitStrategy.AGGRESSIVE)
        
        assert limiter.strategy == RateLimitStrategy.AGGRESSIVE
        assert limiter.safety_margin == 20
        assert limiter.throttle_threshold == 0.85
        assert limiter.max_burst_requests == 20
        assert limiter.base_delay == 0.1
    
    def test_update_rate_limit_status(self):
        """Test updating rate limit status."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        limiter.update_rate_limit_status(
            remaining=4000,
            total=5000,
            reset_time=reset_time,
            repo_name="owner/repo"
        )
        
        assert limiter.budget is not None
        assert limiter.budget.remaining_requests == 4000
        assert limiter.budget.total_requests == 5000
        assert limiter.budget.used_requests == 1000
        assert limiter.budget.reserved_requests == 50  # Normal strategy safety margin
        
        # Check request history
        assert len(limiter.request_history) == 1
        assert limiter.request_history[0][1] == "owner/repo"
    
    def test_allocate_repository_budgets_equal_distribution(self):
        """Test equal budget allocation when no priority data exists."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget
        limiter.update_rate_limit_status(
            remaining=1000,
            total=5000,
            reset_time=reset_time
        )
        
        repositories = ["owner/repo1", "owner/repo2", "owner/repo3"]
        limiter.allocate_repository_budgets(repositories)
        
        # Available requests = 1000 - 50 (safety margin) = 950
        # 950 / 3 = 316 per repo (integer division)
        expected_per_repo = 950 // 3
        
        assert len(limiter.repository_budgets) == 3
        for repo in repositories:
            assert repo in limiter.repository_budgets
            assert limiter.repository_budgets[repo].allocated_requests == expected_per_repo
            assert limiter.repository_budgets[repo].priority == 1.0
    
    def test_allocate_repository_budgets_with_priorities(self):
        """Test budget allocation with priority weighting."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget
        limiter.update_rate_limit_status(
            remaining=1000,
            total=5000,
            reset_time=reset_time
        )
        
        # Add some request history to create priorities
        now = datetime.now()
        limiter.request_history = [
            (now, "owner/repo1"),
            (now, "owner/repo1"),  # repo1 has more activity
            (now, "owner/repo2"),
        ]
        
        repositories = ["owner/repo1", "owner/repo2", "owner/repo3"]
        limiter.allocate_repository_budgets(repositories)
        
        # repo1 should get more budget due to higher activity
        repo1_budget = limiter.repository_budgets["owner/repo1"].allocated_requests
        repo2_budget = limiter.repository_budgets["owner/repo2"].allocated_requests
        repo3_budget = limiter.repository_budgets["owner/repo3"].allocated_requests
        
        assert repo1_budget > repo3_budget  # More activity = more budget
        assert repo2_budget > repo3_budget  # Some activity = more than no activity
    
    @pytest.mark.asyncio
    async def test_should_throttle_request_no_budget(self):
        """Test throttling decision when no budget is set."""
        limiter = IntelligentRateLimiter()
        
        should_throttle = await limiter.should_throttle_request()
        assert not should_throttle
    
    @pytest.mark.asyncio
    async def test_should_throttle_request_no_available_budget(self):
        """Test throttling when no budget is available."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget with no available requests
        limiter.update_rate_limit_status(
            remaining=0,
            total=5000,
            reset_time=reset_time
        )
        
        should_throttle = await limiter.should_throttle_request()
        assert should_throttle
    
    @pytest.mark.asyncio
    async def test_should_throttle_request_high_utilization(self):
        """Test throttling when utilization is above threshold."""
        limiter = IntelligentRateLimiter(RateLimitStrategy.NORMAL)  # 75% threshold
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget with high utilization (80%)
        limiter.update_rate_limit_status(
            remaining=1000,
            total=5000,
            reset_time=reset_time
        )
        
        should_throttle = await limiter.should_throttle_request()
        assert should_throttle
    
    @pytest.mark.asyncio
    async def test_should_throttle_request_repository_budget_exhausted(self):
        """Test throttling when repository-specific budget is exhausted."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up global budget
        limiter.update_rate_limit_status(
            remaining=2000,
            total=5000,
            reset_time=reset_time
        )
        
        # Set up repository budget with no remaining requests
        limiter.repository_budgets["owner/repo"] = RepositoryBudget(
            repo_name="owner/repo",
            allocated_requests=100,
            used_requests=100  # Fully used
        )
        
        should_throttle = await limiter.should_throttle_request("owner/repo")
        assert should_throttle
    
    @pytest.mark.asyncio
    async def test_get_throttle_delay_base_delay(self):
        """Test getting base throttle delay."""
        limiter = IntelligentRateLimiter()
        
        delay = await limiter.get_throttle_delay()
        assert delay == limiter.base_delay
    
    @pytest.mark.asyncio
    async def test_get_throttle_delay_critical_budget(self):
        """Test throttle delay when budget is critical."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up critical budget (5 requests remaining)
        limiter.update_rate_limit_status(
            remaining=5,
            total=5000,
            reset_time=reset_time
        )
        
        delay = await limiter.get_throttle_delay()
        assert delay > limiter.base_delay  # Should be increased
    
    @pytest.mark.asyncio
    async def test_get_throttle_delay_consecutive_throttles(self):
        """Test exponential backoff with consecutive throttles."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget that triggers throttling
        limiter.update_rate_limit_status(
            remaining=1000,
            total=5000,
            reset_time=reset_time
        )
        
        # Simulate consecutive throttles
        limiter.consecutive_throttles = 3
        
        delay = await limiter.get_throttle_delay()
        assert delay > limiter.base_delay * 4  # Should include backoff multiplier
    
    @pytest.mark.asyncio
    async def test_wait_for_budget_availability_no_throttling(self):
        """Test waiting when no throttling is needed."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget with low utilization
        limiter.update_rate_limit_status(
            remaining=4000,
            total=5000,
            reset_time=reset_time
        )
        
        start_time = asyncio.get_event_loop().time()
        await limiter.wait_for_budget_availability()
        end_time = asyncio.get_event_loop().time()
        
        # Should return immediately
        assert end_time - start_time < 0.1
    
    @pytest.mark.asyncio
    async def test_wait_for_budget_availability_with_throttling(self):
        """Test waiting when throttling is needed."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget that triggers throttling
        limiter.update_rate_limit_status(
            remaining=1000,
            total=5000,
            reset_time=reset_time
        )
        
        # Mock sleep to avoid actual waiting in tests
        with patch('asyncio.sleep') as mock_sleep:
            await limiter.wait_for_budget_availability()
            mock_sleep.assert_called_once()
            
            # Verify delay is reasonable
            delay_called = mock_sleep.call_args[0][0]
            assert delay_called > 0
            assert delay_called <= 60  # Should be capped at 1 minute
    
    def test_redistribute_unused_budget(self):
        """Test redistributing unused budget from low-activity repositories."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget
        limiter.update_rate_limit_status(
            remaining=1000,
            total=5000,
            reset_time=reset_time
        )
        
        # Set up repository budgets with different utilization
        limiter.repository_budgets = {
            "owner/low-usage": RepositoryBudget(
                repo_name="owner/low-usage",
                allocated_requests=200,
                used_requests=20  # 10% utilization - should lose budget
            ),
            "owner/high-usage": RepositoryBudget(
                repo_name="owner/high-usage",
                allocated_requests=200,
                used_requests=180  # 90% utilization - should gain budget
            ),
            "owner/medium-usage": RepositoryBudget(
                repo_name="owner/medium-usage",
                allocated_requests=200,
                used_requests=100  # 50% utilization - no change
            )
        }
        
        # Store original allocations
        original_low = limiter.repository_budgets["owner/low-usage"].allocated_requests
        original_high = limiter.repository_budgets["owner/high-usage"].allocated_requests
        
        limiter.redistribute_unused_budget()
        
        # Low usage repo should have less budget
        assert limiter.repository_budgets["owner/low-usage"].allocated_requests < original_low
        
        # High usage repo should have more budget
        assert limiter.repository_budgets["owner/high-usage"].allocated_requests > original_high
    
    def test_get_budget_status(self):
        """Test getting budget status for monitoring."""
        limiter = IntelligentRateLimiter(RateLimitStrategy.AGGRESSIVE)
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget and repository budgets
        limiter.update_rate_limit_status(
            remaining=3000,
            total=5000,
            reset_time=reset_time
        )
        
        limiter.repository_budgets["owner/repo"] = RepositoryBudget(
            repo_name="owner/repo",
            allocated_requests=100,
            used_requests=25,
            priority=1.5
        )
        
        status = limiter.get_budget_status()
        
        assert status['strategy'] == 'aggressive'
        assert 'adaptive_delay' in status
        assert 'consecutive_throttles' in status
        assert 'global_budget' in status
        assert 'repository_budgets' in status
        
        # Check global budget details
        global_budget = status['global_budget']
        assert global_budget['total_requests'] == 5000
        assert global_budget['remaining_requests'] == 3000
        assert global_budget['utilization_ratio'] == 0.4
        
        # Check repository budget details
        repo_budget = status['repository_budgets']['owner/repo']
        assert repo_budget['allocated_requests'] == 100
        assert repo_budget['used_requests'] == 25
        assert repo_budget['utilization_ratio'] == 0.25
        assert repo_budget['priority'] == 1.5


class TestGlobalFunctions:
    """Test global utility functions."""
    
    def test_get_intelligent_rate_limiter(self):
        """Test getting global rate limiter instance."""
        limiter1 = get_intelligent_rate_limiter()
        limiter2 = get_intelligent_rate_limiter()
        
        # Should return the same instance
        assert limiter1 is limiter2
    
    def test_set_rate_limit_strategy(self):
        """Test setting global rate limiting strategy."""
        original_limiter = get_intelligent_rate_limiter()
        original_strategy = original_limiter.strategy
        
        # Set new strategy
        set_rate_limit_strategy(RateLimitStrategy.CONSERVATIVE)
        
        new_limiter = get_intelligent_rate_limiter()
        assert new_limiter.strategy == RateLimitStrategy.CONSERVATIVE
        
        # Should be a new instance
        assert new_limiter is not original_limiter
        
        # Reset to original strategy
        set_rate_limit_strategy(original_strategy)


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_typical_scan_workflow(self):
        """Test a typical scanning workflow with intelligent rate limiting."""
        limiter = IntelligentRateLimiter(RateLimitStrategy.NORMAL)
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Initial rate limit status
        limiter.update_rate_limit_status(
            remaining=4500,
            total=5000,
            reset_time=reset_time
        )
        
        # Allocate budgets for repositories
        repositories = ["owner/repo1", "owner/repo2", "owner/repo3"]
        limiter.allocate_repository_budgets(repositories)
        
        # Simulate requests for different repositories
        for i in range(10):
            repo = repositories[i % 3]
            
            # Check if we should throttle
            should_throttle = await limiter.should_throttle_request(repo)
            
            if should_throttle:
                # Get delay and simulate waiting
                delay = await limiter.get_throttle_delay(repo)
                assert delay >= 0
                # In real scenario, we would await asyncio.sleep(delay)
            
            # Simulate API response with updated rate limit
            remaining = 4500 - (i * 50)  # Simulate decreasing rate limit
            limiter.update_rate_limit_status(
                remaining=remaining,
                total=5000,
                reset_time=reset_time,
                repo_name=repo
            )
        
        # Check final status
        status = limiter.get_budget_status()
        assert status['global_budget']['remaining_requests'] == 4050  # 4500 - (9 * 50)
        
        # All repositories should have some budget allocated
        for repo in repositories:
            assert repo in status['repository_budgets']
            repo_budget = status['repository_budgets'][repo]
            assert repo_budget['allocated_requests'] > 0
    
    @pytest.mark.asyncio
    async def test_rate_limit_exhaustion_scenario(self):
        """Test behavior when rate limits are exhausted."""
        limiter = IntelligentRateLimiter(RateLimitStrategy.CONSERVATIVE)
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up near-exhausted rate limit
        limiter.update_rate_limit_status(
            remaining=10,
            total=5000,
            reset_time=reset_time
        )
        
        # All requests should be throttled
        should_throttle = await limiter.should_throttle_request()
        assert should_throttle
        
        # Delay should be significant
        delay = await limiter.get_throttle_delay()
        assert delay > 1.0  # Should be more than base delay
        
        # Simulate complete exhaustion
        limiter.update_rate_limit_status(
            remaining=0,
            total=5000,
            reset_time=reset_time
        )
        
        should_throttle = await limiter.should_throttle_request()
        assert should_throttle
        
        delay = await limiter.get_throttle_delay()
        assert delay > 5.0  # Should be much higher for exhausted limits
    
    def test_budget_redistribution_scenario(self):
        """Test realistic budget redistribution scenario."""
        limiter = IntelligentRateLimiter()
        reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
        
        # Set up budget
        limiter.update_rate_limit_status(
            remaining=2000,
            total=5000,
            reset_time=reset_time
        )
        
        # Create repositories with different usage patterns
        repositories = [
            "owner/active-repo",
            "owner/inactive-repo",
            "owner/moderate-repo"
        ]
        limiter.allocate_repository_budgets(repositories)
        
        # Simulate different usage patterns
        # First, let's see what the initial allocations are
        initial_allocation = limiter.repository_budgets["owner/active-repo"].allocated_requests
        
        # Set usage that creates the right utilization ratios
        limiter.repository_budgets["owner/active-repo"].used_requests = int(initial_allocation * 0.9)  # 90% usage - high
        limiter.repository_budgets["owner/inactive-repo"].used_requests = int(initial_allocation * 0.1)  # 10% usage - low
        limiter.repository_budgets["owner/moderate-repo"].used_requests = int(initial_allocation * 0.5)  # 50% usage - moderate
        
        # Store original allocations
        original_allocations = {
            repo: budget.allocated_requests 
            for repo, budget in limiter.repository_budgets.items()
        }
        
        # Redistribute budget
        limiter.redistribute_unused_budget()
        
        # Active repo should get more budget (high utilization > 80%)
        assert (limiter.repository_budgets["owner/active-repo"].allocated_requests >= 
                original_allocations["owner/active-repo"])
        
        # Inactive repo should lose some budget (low utilization < 30%)
        assert (limiter.repository_budgets["owner/inactive-repo"].allocated_requests < 
                original_allocations["owner/inactive-repo"])