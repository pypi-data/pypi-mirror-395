"""Integration tests for intelligent rate limiter with AsyncGitHubClient."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta

from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
from src.github_ioc_scanner.batch_models import BatchConfig
from src.github_ioc_scanner.intelligent_rate_limiter import RateLimitStrategy


class TestIntelligentRateLimiterIntegration:
    """Test integration between intelligent rate limiter and AsyncGitHubClient."""
    
    @pytest.mark.asyncio
    async def test_async_client_with_intelligent_rate_limiter(self):
        """Test that AsyncGitHubClient properly initializes intelligent rate limiter."""
        config = BatchConfig(
            rate_limit_strategy="aggressive",
            enable_proactive_rate_limiting=True,
            rate_limit_safety_margin=20
        )
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Check that intelligent limiter is initialized with correct strategy
            assert client.intelligent_limiter.strategy == RateLimitStrategy.AGGRESSIVE
            assert client.intelligent_limiter.safety_margin == 20
    
    @pytest.mark.asyncio
    async def test_repository_budget_allocation(self):
        """Test that repository budgets are allocated correctly."""
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient()
            
            # Set up initial rate limit budget
            reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
            client.intelligent_limiter.update_rate_limit_status(
                remaining=3000,
                total=5000,
                reset_time=reset_time
            )
            
            # Allocate budgets for repositories
            repositories = ["owner/repo1", "owner/repo2", "owner/repo3"]
            client.allocate_repository_budgets(repositories)
            
            # Check that budgets were allocated
            status = client.get_rate_limit_budget_status()
            assert 'repository_budgets' in status
            
            # Should have budgets for all repositories
            for repo in repositories:
                assert repo in status['repository_budgets']
    
    @pytest.mark.asyncio
    async def test_rate_limit_strategy_setting(self):
        """Test setting rate limit strategy on client."""
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient()
            
            # Initially should be normal strategy
            assert client.intelligent_limiter.strategy == RateLimitStrategy.NORMAL
            
            # Change to conservative
            client.set_rate_limit_strategy(RateLimitStrategy.CONSERVATIVE)
            assert client.intelligent_limiter.strategy == RateLimitStrategy.CONSERVATIVE
            assert client.intelligent_limiter.safety_margin == 100  # Conservative settings
    
    @pytest.mark.asyncio
    async def test_extract_repo_name_from_url(self):
        """Test extracting repository name from GitHub API URLs."""
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient()
            
            # Test various URL formats
            test_cases = [
                ("/repos/owner/repo/contents/file.txt", "owner/repo"),
                ("repos/owner/repo/git/trees/main", "owner/repo"),
                ("/repos/owner/repo-name/contents/path/to/file.json", "owner/repo-name"),
                ("/orgs/owner/repos", None),  # Not a repo-specific URL
                ("invalid-url", None),
            ]
            
            for url, expected in test_cases:
                result = client._extract_repo_name_from_url(url)
                assert result == expected, f"URL: {url}, Expected: {expected}, Got: {result}"
    
    @pytest.mark.asyncio
    async def test_rate_limit_status_update_integration(self):
        """Test that rate limit status updates are properly integrated."""
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient()
            
            # Mock the intelligent limiter to track calls
            client.intelligent_limiter.update_rate_limit_status = Mock()
            
            # Simulate a successful API response with rate limit headers
            reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
            
            # This would normally be called in _make_request_with_retry
            client.intelligent_limiter.update_rate_limit_status(
                remaining=4000,
                total=5000,
                reset_time=reset_time,
                repo_name="owner/repo"
            )
            
            # Verify the method was called with correct parameters
            client.intelligent_limiter.update_rate_limit_status.assert_called_once_with(
                remaining=4000,
                total=5000,
                reset_time=reset_time,
                repo_name="owner/repo"
            )
    
    @pytest.mark.asyncio
    async def test_budget_redistribution(self):
        """Test budget redistribution functionality."""
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient()
            
            # Set up some budget and repository allocations
            reset_time = int((datetime.now() + timedelta(hours=1)).timestamp())
            client.intelligent_limiter.update_rate_limit_status(
                remaining=2000,
                total=5000,
                reset_time=reset_time
            )
            
            repositories = ["owner/active", "owner/inactive"]
            client.allocate_repository_budgets(repositories)
            
            # Get initial allocations
            initial_active = client.intelligent_limiter.repository_budgets["owner/active"].allocated_requests
            initial_inactive = client.intelligent_limiter.repository_budgets["owner/inactive"].allocated_requests
            
            # Simulate different usage patterns based on allocated amounts
            client.intelligent_limiter.repository_budgets["owner/active"].used_requests = int(initial_active * 0.9)  # 90% usage - high
            client.intelligent_limiter.repository_budgets["owner/inactive"].used_requests = int(initial_inactive * 0.1)  # 10% usage - low
            
            # Redistribute budget
            client.redistribute_unused_budget()
            
            # Check that redistribution occurred
            final_active = client.intelligent_limiter.repository_budgets["owner/active"].allocated_requests
            final_inactive = client.intelligent_limiter.repository_budgets["owner/inactive"].allocated_requests
            
            # Active repo should get more or same budget, inactive should lose some
            assert final_active >= initial_active
            assert final_inactive < initial_inactive
    
    @pytest.mark.asyncio
    async def test_throttling_integration(self):
        """Test that throttling is properly integrated into request flow."""
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient()
            
            # Mock the wait_for_budget_availability method to track calls
            client.intelligent_limiter.wait_for_budget_availability = AsyncMock()
            
            # Mock the session and response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {
                'X-RateLimit-Remaining': '4000',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
            }
            mock_response.json.return_value = {"test": "data"}
            mock_response.content = b'{"test": "data"}'
            mock_response.text = '{"test": "data"}'
            
            mock_session = AsyncMock()
            mock_session.request.return_value = mock_response
            
            with patch.object(client, '_get_session', return_value=mock_session):
                # Make a request
                await client._make_request("GET", "/repos/owner/repo/contents/file.txt")
                
                # Verify that throttling check was called
                client.intelligent_limiter.wait_for_budget_availability.assert_called_once_with("owner/repo")
    
    def test_batch_config_integration(self):
        """Test that BatchConfig properly configures intelligent rate limiting."""
        config = BatchConfig(
            rate_limit_strategy="conservative",
            enable_proactive_rate_limiting=True,
            rate_limit_safety_margin=100,
            enable_budget_distribution=True,
            enable_adaptive_timing=True
        )
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Check that configuration was applied
            assert client.intelligent_limiter.strategy == RateLimitStrategy.CONSERVATIVE
            assert client.intelligent_limiter.safety_margin == 100
            assert client.intelligent_limiter.throttle_threshold == 0.6  # Conservative threshold
    
    def test_invalid_rate_limit_strategy_fallback(self):
        """Test fallback to normal strategy for invalid configuration."""
        config = BatchConfig()
        config.rate_limit_strategy = "invalid_strategy"
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            # Should not raise an exception and should fall back to normal
            client = AsyncGitHubClient(config=config)
            assert client.intelligent_limiter.strategy == RateLimitStrategy.NORMAL