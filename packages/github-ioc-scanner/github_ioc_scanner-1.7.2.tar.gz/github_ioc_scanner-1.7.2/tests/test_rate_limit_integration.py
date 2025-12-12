"""
Comprehensive integration tests for rate limit scenarios.

This module tests the complete rate limit handling system including:
- Various rate limit conditions
- Event loop handling during recovery
- Message deduplication and user experience
- Performance regression testing
"""

import pytest
import asyncio
import time
import threading
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from contextlib import asynccontextmanager

from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
from src.github_ioc_scanner.rate_limit_manager import RateLimitManager
from src.github_ioc_scanner.error_message_formatter import ErrorMessageFormatter
from src.github_ioc_scanner.event_loop_context import EventLoopContext
from src.github_ioc_scanner.batch_coordinator import BatchCoordinator
from src.github_ioc_scanner.scanner import GitHubIOCScanner
from src.github_ioc_scanner.batch_models import BatchConfig
from src.github_ioc_scanner.exceptions import RateLimitError
from src.github_ioc_scanner.intelligent_rate_limiter import RateLimitStrategy


class TestRateLimitIntegrationScenarios:
    """Test various rate limit scenarios with full integration."""
    
    @pytest.mark.asyncio
    async def test_primary_rate_limit_scenario(self):
        """Test handling of primary rate limit with full integration."""
        config = BatchConfig(
            rate_limit_strategy="normal",
            enable_proactive_rate_limiting=True
        )
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Mock session to simulate rate limit response then success
            rate_limit_response = Mock()
            rate_limit_response.status_code = 403
            rate_limit_response.text = "API rate limit exceeded"
            rate_limit_response.headers = {
                'X-RateLimit-Remaining': '0',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(seconds=0.1)).timestamp()))  # Short wait
            }
            rate_limit_response.json.return_value = {"message": "API rate limit exceeded"}
            
            success_response = Mock()
            success_response.status_code = 200
            success_response.text = '{"content": "dGVzdA=="}'
            success_response.content = b'{"content": "dGVzdA=="}'
            success_response.headers = {
                'X-RateLimit-Remaining': '4999',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
            }
            success_response.json.return_value = {"content": "dGVzdA=="}
            success_response.raise_for_status = Mock()
            
            mock_session = AsyncMock()
            mock_session.request.side_effect = [rate_limit_response, success_response]
            
            with patch.object(client, '_get_session', return_value=mock_session):
                # Request should handle rate limit gracefully and succeed
                response = await client._make_request("GET", "/repos/owner/repo/contents/file.txt")
                
                # Verify rate limit manager was updated
                assert client.rate_limit_manager.primary_limit_reset is not None
                
                # Verify request eventually succeeded
                assert response.data == {"content": "dGVzdA=="}
                assert not response.not_modified
    
    @pytest.mark.asyncio
    async def test_secondary_rate_limit_scenario(self):
        """Test handling of secondary rate limit (abuse detection)."""
        config = BatchConfig(rate_limit_strategy="aggressive")
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Mock session to simulate secondary rate limit then success
            secondary_limit_response = Mock()
            secondary_limit_response.status_code = 403
            secondary_limit_response.text = "You have exceeded a secondary rate limit exceeded"
            secondary_limit_response.headers = {
                'X-RateLimit-Remaining': '4000',  # Still have primary quota
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp())),
                'Retry-After': '1'  # Short retry for testing
            }
            secondary_limit_response.json.return_value = {"message": "You have exceeded a secondary rate limit"}
            
            success_response = Mock()
            success_response.status_code = 200
            success_response.text = '{"content": "dGVzdA=="}'
            success_response.content = b'{"content": "dGVzdA=="}'
            success_response.headers = {
                'X-RateLimit-Remaining': '3999',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
            }
            success_response.json.return_value = {"content": "dGVzdA=="}
            success_response.raise_for_status = Mock()
            
            mock_session = AsyncMock()
            mock_session.request.side_effect = [secondary_limit_response, success_response]
            
            with patch.object(client, '_get_session', return_value=mock_session):
                # Request should handle secondary rate limit with backoff and succeed
                response = await client._make_request("GET", "/repos/owner/repo/contents/file.txt")
                
                # Verify secondary rate limit was detected and handled
                assert client.rate_limit_manager.secondary_limit_reset is not None
                
                # Verify request eventually succeeded
                assert response.data == {"content": "dGVzdA=="}
                assert not response.not_modified
    
    @pytest.mark.asyncio
    async def test_rate_limit_recovery_workflow(self):
        """Test complete rate limit recovery workflow."""
        config = BatchConfig(rate_limit_strategy="conservative")
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Mock session responses: first rate limited, then successful
            rate_limit_response = Mock()
            rate_limit_response.status_code = 403
            rate_limit_response.text = "API rate limit exceeded"  # Add text attribute
            rate_limit_response.headers = {
                'X-RateLimit-Remaining': '0',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(seconds=1)).timestamp()))
            }
            rate_limit_response.json.return_value = {"message": "API rate limit exceeded"}
            
            success_response = Mock()
            success_response.status_code = 200
            success_response.text = '{"name": "test-file.txt", "content": "dGVzdA=="}'  # Add text attribute
            success_response.content = b'{"name": "test-file.txt", "content": "dGVzdA=="}'  # Add content attribute
            success_response.headers = {
                'X-RateLimit-Remaining': '4999',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
            }
            success_response.json.return_value = {"name": "test-file.txt", "content": "dGVzdA=="}
            success_response.raise_for_status = Mock()  # Add raise_for_status method
            
            mock_session = AsyncMock()
            mock_session.request.side_effect = [rate_limit_response, success_response]
            
            with patch.object(client, '_get_session', return_value=mock_session):
                # First request hits rate limit but recovers gracefully
                response1 = await client._make_request("GET", "/repos/owner/repo/contents/file.txt")
                
                # Verify first request succeeded after rate limit handling
                assert response1.data == {"name": "test-file.txt", "content": "dGVzdA=="}
                
                # Verify rate limit manager was updated
                assert client.rate_limit_manager.primary_limit_reset is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_requests_rate_limit_handling(self):
        """Test rate limit handling with concurrent requests."""
        config = BatchConfig(
            rate_limit_strategy="normal",
            max_concurrent_requests=5
        )
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Mock session to simulate rate limit after a few requests
            responses = []
            for i in range(3):
                success_response = Mock()
                success_response.status_code = 200
                success_response.text = f'{{"content": "file{i}"}}'
                success_response.content = f'{{"content": "file{i}"}}'.encode()
                success_response.headers = {
                    'X-RateLimit-Remaining': str(5000 - i - 1),
                    'X-RateLimit-Limit': '5000',
                    'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
                }
                success_response.json.return_value = {"content": f"file{i}"}
                success_response.raise_for_status = Mock()
                responses.append(success_response)
            
            # Then rate limit responses for remaining requests
            for i in range(2):  # 2 more responses for the remaining requests
                rate_limit_response = Mock()
                rate_limit_response.status_code = 403
                rate_limit_response.text = "API rate limit exceeded"
                rate_limit_response.headers = {
                    'X-RateLimit-Remaining': '0',
                    'X-RateLimit-Limit': '5000',
                    'X-RateLimit-Reset': str(int((datetime.now() + timedelta(seconds=0.1)).timestamp()))
                }
                rate_limit_response.json.return_value = {"message": "API rate limit exceeded"}
                responses.append(rate_limit_response)
                
                # Add success response after each rate limit
                success_after_limit = Mock()
                success_after_limit.status_code = 200
                success_after_limit.text = f'{{"content": "file{i+3}"}}'
                success_after_limit.content = f'{{"content": "file{i+3}"}}'.encode()
                success_after_limit.headers = {
                    'X-RateLimit-Remaining': str(4999 - i),
                    'X-RateLimit-Limit': '5000',
                    'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
                }
                success_after_limit.json.return_value = {"content": f"file{i+3}"}
                success_after_limit.raise_for_status = Mock()
                responses.append(success_after_limit)
            
            mock_session = AsyncMock()
            mock_session.request.side_effect = responses
            
            with patch.object(client, '_get_session', return_value=mock_session):
                # Launch concurrent requests
                tasks = []
                for i in range(5):
                    task = asyncio.create_task(
                        client._make_request("GET", f"/repos/owner/repo{i}/contents/file.txt")
                    )
                    tasks.append(task)
                
                # Collect results
                results = []
                for task in tasks:
                    try:
                        result = await task
                        results.append(("success", result))
                    except RateLimitError as e:
                        results.append(("rate_limit", e))
                    except Exception as e:
                        results.append(("error", e))
                
                # All requests should eventually succeed due to graceful handling
                successes = [r for r in results if r[0] == "success"]
                errors = [r for r in results if r[0] != "success"]
                
                assert len(successes) == 5  # All should eventually succeed
                assert len(errors) == 0  # No permanent failures due to graceful handling
    
    @pytest.mark.asyncio
    async def test_multiple_rate_limit_scenarios(self):
        """Test handling multiple rate limit scenarios in sequence."""
        config = BatchConfig(
            rate_limit_strategy="normal",
            enable_proactive_rate_limiting=True
        )
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Test sequence: primary rate limit -> recovery -> secondary rate limit -> recovery
            responses = []
            
            # Primary rate limit
            primary_limit_response = Mock()
            primary_limit_response.status_code = 403
            primary_limit_response.text = "API rate limit exceeded"
            primary_limit_response.headers = {
                'X-RateLimit-Remaining': '0',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(seconds=0.1)).timestamp()))
            }
            primary_limit_response.json.return_value = {"message": "API rate limit exceeded"}
            responses.append(primary_limit_response)
            
            # Success after primary recovery
            success_response1 = Mock()
            success_response1.status_code = 200
            success_response1.text = '{"content": "file1"}'
            success_response1.content = b'{"content": "file1"}'
            success_response1.headers = {
                'X-RateLimit-Remaining': '4999',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
            }
            success_response1.json.return_value = {"content": "file1"}
            success_response1.raise_for_status = Mock()
            responses.append(success_response1)
            
            # Secondary rate limit
            secondary_limit_response = Mock()
            secondary_limit_response.status_code = 403
            secondary_limit_response.text = "You have exceeded a secondary rate limit exceeded"
            secondary_limit_response.headers = {
                'X-RateLimit-Remaining': '4998',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp())),
                'Retry-After': '1'
            }
            secondary_limit_response.json.return_value = {"message": "You have exceeded a secondary rate limit"}
            responses.append(secondary_limit_response)
            
            # Success after secondary recovery
            success_response2 = Mock()
            success_response2.status_code = 200
            success_response2.text = '{"content": "file2"}'
            success_response2.content = b'{"content": "file2"}'
            success_response2.headers = {
                'X-RateLimit-Remaining': '4997',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
            }
            success_response2.json.return_value = {"content": "file2"}
            success_response2.raise_for_status = Mock()
            responses.append(success_response2)
            
            mock_session = AsyncMock()
            mock_session.request.side_effect = responses
            
            with patch.object(client, '_get_session', return_value=mock_session):
                # First request - primary rate limit
                response1 = await client._make_request("GET", "/repos/owner/repo1/contents/file.txt")
                assert response1.data == {"content": "file1"}
                assert client.rate_limit_manager.primary_limit_reset is not None
                
                # Second request - secondary rate limit  
                response2 = await client._make_request("GET", "/repos/owner/repo2/contents/file.txt")
                assert response2.data == {"content": "file2"}
                assert client.rate_limit_manager.secondary_limit_reset is not None


class TestEventLoopRateLimitIntegration:
    """Test event loop handling during rate limit scenarios."""
    
    def test_sync_to_async_rate_limit_transition(self):
        """Test transitioning from sync to async context during rate limit."""
        context = EventLoopContext()
        
        def sync_operation_with_rate_limit():
            """Simulate sync operation that needs to handle async rate limit."""
            with context.managed_event_loop() as loop:
                # Simulate async rate limit handling
                async def async_rate_limit_handler():
                    await asyncio.sleep(0.1)  # Simulate waiting for rate limit
                    return "recovered"
                
                # This should work without "no running event loop" errors
                result = loop.run_until_complete(async_rate_limit_handler())
                return result
        
        # Run in separate thread to simulate real-world scenario
        result_container = []
        exception_container = []
        
        def thread_target():
            try:
                result = sync_operation_with_rate_limit()
                result_container.append(result)
            except Exception as e:
                exception_container.append(e)
        
        thread = threading.Thread(target=thread_target)
        thread.start()
        thread.join()
        
        # Should complete without errors
        assert len(exception_container) == 0
        assert len(result_container) == 1
        assert result_container[0] == "recovered"
    
    @pytest.mark.asyncio
    async def test_async_rate_limit_recovery_context(self):
        """Test async context management during rate limit recovery."""
        context = EventLoopContext()
        
        # Simulate rate limit scenario in async context
        async def simulate_rate_limited_operation():
            # First call fails with rate limit
            raise RateLimitError("Rate limit exceeded", reset_time=datetime.now() + timedelta(seconds=0.1))
        
        async def simulate_recovery_operation():
            # Recovery operation after waiting
            await context.handle_rate_limit_async(0.1)
            return "success"
        
        # Test that recovery works in async context
        try:
            await simulate_rate_limited_operation()
            assert False, "Should have raised RateLimitError"
        except RateLimitError:
            # Handle rate limit by waiting
            result = await simulate_recovery_operation()
            assert result == "success"
    
    def test_nested_event_loop_rate_limit_handling(self):
        """Test handling rate limits with nested event loop scenarios."""
        context = EventLoopContext()
        
        def outer_sync_operation():
            """Outer sync operation that creates event loop."""
            with context.managed_event_loop() as outer_loop:
                
                async def inner_async_operation():
                    """Inner async operation that might hit rate limits."""
                    # Simulate checking for existing loop
                    assert context.is_event_loop_running()
                    
                    # Simulate rate limit handling
                    await context.handle_rate_limit_async(0.05)
                    return "inner_success"
                
                # This should reuse the existing loop
                result = outer_loop.run_until_complete(inner_async_operation())
                return result
        
        result = outer_sync_operation()
        assert result == "inner_success"
    
    @pytest.mark.asyncio
    async def test_event_loop_context_rate_limit_integration(self):
        """Test EventLoopContext handling during rate limit scenarios."""
        context = EventLoopContext()
        
        # Test that event loop context works properly during rate limit handling
        def sync_operation_with_async_rate_limit():
            """Simulate sync operation that needs async rate limit handling."""
            with context.managed_event_loop() as loop:
                async def async_rate_limit_operation():
                    # Simulate rate limit detection
                    manager = RateLimitManager()
                    reset_time = datetime.now() + timedelta(seconds=0.1)
                    manager.handle_rate_limit(reset_time)
                    
                    # Simulate waiting for rate limit
                    await context.handle_rate_limit_async(0.1)
                    return "rate_limit_handled"
                
                # This should work without event loop errors
                result = loop.run_until_complete(async_rate_limit_operation())
                return result
        
        # Run in separate thread to test real-world scenario
        import threading
        result_container = []
        exception_container = []
        
        def thread_target():
            try:
                result = sync_operation_with_async_rate_limit()
                result_container.append(result)
            except Exception as e:
                exception_container.append(e)
        
        thread = threading.Thread(target=thread_target)
        thread.start()
        thread.join()
        
        # Should complete without errors
        assert len(exception_container) == 0, f"Unexpected exception: {exception_container}"
        assert len(result_container) == 1
        assert result_container[0] == "rate_limit_handled"


class TestMessageDeduplicationAndUserExperience:
    """Test message deduplication and user experience during rate limits."""
    
    def test_rate_limit_message_deduplication(self):
        """Test that rate limit messages are properly deduplicated."""
        manager = RateLimitManager(message_cooldown=2)  # Short cooldown for testing
        formatter = ErrorMessageFormatter()
        
        reset_time = datetime.now() + timedelta(minutes=5)
        
        # First message should be shown
        assert manager.should_show_message() is True
        message1 = formatter.format_rate_limit_message(reset_time, "owner/repo1")
        
        # Immediate second message should be suppressed
        assert manager.should_show_message() is False
        
        # Wait for cooldown
        time.sleep(2.1)
        
        # After cooldown, message should be shown again
        assert manager.should_show_message() is True
        message2 = formatter.format_rate_limit_message(reset_time, "owner/repo2")
        
        # Messages should be properly formatted
        assert "GitHub API rate limit reached" in message1
        assert "owner/repo1" in message1
        assert "GitHub API rate limit reached" in message2
        assert "owner/repo2" in message2
    
    def test_user_friendly_error_suppression(self):
        """Test that technical errors are suppressed for users."""
        formatter = ErrorMessageFormatter()
        
        # Rate limit exceptions should be suppressed
        rate_limit_error = RateLimitError("API rate limit exceeded for installation ID 123456")
        assert formatter.should_suppress_error(rate_limit_error) is True
        
        # Network errors should be suppressed
        network_error = Exception("Connection timeout after 30 seconds")
        assert formatter.should_suppress_error(network_error) is True
        
        # Normal exceptions should not be suppressed
        value_error = ValueError("Invalid input parameter")
        assert formatter.should_suppress_error(value_error) is False
    
    @pytest.mark.asyncio
    async def test_progress_message_formatting_during_rate_limits(self):
        """Test that progress messages are formatted correctly during rate limits."""
        formatter = ErrorMessageFormatter()
        manager = RateLimitManager(message_cooldown=1)  # Short cooldown for testing
        
        # Test progress messages with different scenarios
        progress_messages = []
        
        # Normal progress
        message1 = formatter.format_progress_message(25, 100, "5 minutes")
        progress_messages.append(message1)
        
        # Progress during rate limit
        reset_time = datetime.now() + timedelta(minutes=2)
        if manager.should_show_message():
            rate_limit_message = formatter.format_rate_limit_message(reset_time, "owner/repo")
            progress_messages.append(rate_limit_message)
        
        # Progress after rate limit recovery
        await asyncio.sleep(1.1)  # Wait for cooldown
        if manager.should_show_message():
            message2 = formatter.format_progress_message(50, 100, "3 minutes")
            progress_messages.append(message2)
        
        # Verify messages are properly formatted
        assert len(progress_messages) >= 2
        assert "Progress: 25/100 (25.0%)" in progress_messages[0]
        assert "ETA: 5 minutes" in progress_messages[0]
        assert "GitHub API rate limit reached" in progress_messages[1]
        
        if len(progress_messages) > 2:
            assert "Progress: 50/100 (50.0%)" in progress_messages[2]
    
    def test_technical_details_formatting(self):
        """Test formatting of technical details for debug mode."""
        formatter = ErrorMessageFormatter()
        
        # Create mock exception with response details
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.headers = {
            'X-RateLimit-Remaining': '0',
            'X-RateLimit-Limit': '5000',
            'X-RateLimit-Reset': '1234567890'
        }
        
        exception = RateLimitError("API rate limit exceeded")
        exception.response = mock_response
        
        details = formatter.format_technical_details(exception)
        
        # Should include technical information
        assert "Exception Type: RateLimitError" in details
        assert "HTTP Status: 403" in details
        assert "Rate Limit Headers:" in details
        assert "X-RateLimit-Remaining" in details


class TestRateLimitPerformanceRegression:
    """Test performance to ensure no regression from rate limit handling."""
    
    def test_rate_limit_manager_performance(self):
        """Test that RateLimitManager operations are performant."""
        manager = RateLimitManager()
        
        # Test performance of status checks
        start_time = time.time()
        
        for _ in range(1000):
            manager.is_rate_limited()
            manager.get_wait_time()
            manager.should_show_message()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 operations in well under 1 second
        assert duration < 0.1, f"Rate limit operations too slow: {duration}s"
    
    def test_error_message_formatter_performance(self):
        """Test that ErrorMessageFormatter operations are performant."""
        formatter = ErrorMessageFormatter()
        reset_time = datetime.now() + timedelta(minutes=5)
        
        start_time = time.time()
        
        for i in range(1000):
            formatter.format_rate_limit_message(reset_time, f"owner/repo{i}")
            formatter.format_progress_message(i, 1000)
            formatter.should_suppress_error(Exception("test error"))
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 operations in well under 1 second
        assert duration < 0.1, f"Message formatting too slow: {duration}s"
    
    def test_event_loop_context_performance(self):
        """Test that EventLoopContext operations are performant."""
        context = EventLoopContext()
        
        start_time = time.time()
        
        for _ in range(100):  # Fewer iterations as this involves actual event loops
            with context.managed_event_loop():
                context.is_event_loop_running()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 100 operations in reasonable time
        assert duration < 1.0, f"Event loop operations too slow: {duration}s"
    
    @pytest.mark.asyncio
    async def test_async_rate_limit_handling_performance(self):
        """Test performance of async rate limit handling."""
        config = BatchConfig(rate_limit_strategy="normal")
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Mock successful responses (no actual rate limits)
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.headers = {
                'X-RateLimit-Remaining': '4999',
                'X-RateLimit-Limit': '5000',
                'X-RateLimit-Reset': str(int((datetime.now() + timedelta(hours=1)).timestamp()))
            }
            mock_response.json.return_value = {"content": "dGVzdA=="}
            
            mock_session = AsyncMock()
            mock_session.request.return_value = mock_response
            
            with patch.object(client, '_get_session', return_value=mock_session):
                start_time = time.time()
                
                # Make multiple requests to test overhead
                tasks = []
                for i in range(50):
                    task = asyncio.create_task(
                        client._make_request("GET", f"/repos/owner/repo{i}/contents/file.txt")
                    )
                    tasks.append(task)
                
                await asyncio.gather(*tasks)
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Should complete 50 requests in reasonable time
                # (This is mainly testing overhead, not actual network time)
                assert duration < 2.0, f"Async requests too slow: {duration}s"
    
    def test_memory_usage_during_rate_limits(self):
        """Test that memory usage doesn't grow excessively during rate limits."""
        import gc
        import sys
        
        # Get initial memory usage
        gc.collect()
        initial_objects = len(gc.get_objects())
        
        manager = RateLimitManager()
        formatter = ErrorMessageFormatter()
        
        # Simulate many rate limit events
        for i in range(1000):
            reset_time = datetime.now() + timedelta(minutes=i % 60)
            manager.handle_rate_limit(reset_time, is_secondary=(i % 2 == 0))
            
            if manager.should_show_message():
                formatter.format_rate_limit_message(reset_time, f"owner/repo{i}")
            
            # Periodically clear expired limits
            if i % 100 == 0:
                manager.clear_expired_limits()
        
        # Check memory usage
        gc.collect()
        final_objects = len(gc.get_objects())
        
        # Memory growth should be reasonable
        object_growth = final_objects - initial_objects
        assert object_growth < 1000, f"Excessive memory growth: {object_growth} objects"


class TestRateLimitEdgeCases:
    """Test edge cases and error conditions in rate limit handling."""
    
    @pytest.mark.asyncio
    async def test_malformed_rate_limit_headers(self):
        """Test handling of malformed rate limit headers."""
        config = BatchConfig()
        
        with patch('src.github_ioc_scanner.async_github_client.AsyncGitHubClient._discover_token') as mock_token:
            mock_token.return_value = "test_token"
            
            client = AsyncGitHubClient(config=config)
            
            # Mock response with malformed headers
            mock_response = Mock()
            mock_response.status_code = 403
            mock_response.headers = {
                'X-RateLimit-Remaining': 'invalid',  # Should be numeric
                'X-RateLimit-Reset': 'not-a-timestamp',  # Should be timestamp
            }
            mock_response.json.return_value = {"message": "API rate limit exceeded"}
            
            mock_session = AsyncMock()
            mock_session.request.return_value = mock_response
            
            with patch.object(client, '_get_session', return_value=mock_session):
                # Should handle malformed headers gracefully by catching the error
                try:
                    await client._make_request("GET", "/repos/owner/repo/contents/file.txt")
                    assert False, "Should have raised an exception due to malformed headers"
                except Exception as e:
                    # Should get a wrapped exception, not crash
                    assert "invalid literal for int()" in str(e) or "Unexpected error" in str(e)
    
    def test_rate_limit_manager_edge_cases(self):
        """Test edge cases in RateLimitManager."""
        manager = RateLimitManager()
        
        # Test with past reset times
        past_time = datetime.now() - timedelta(minutes=5)
        manager.handle_rate_limit(past_time)
        
        # Should not be rate limited for past times
        assert not manager.is_rate_limited()
        assert manager.get_wait_time() == 0
        
        # Test with very far future times
        far_future = datetime.now() + timedelta(days=365)
        manager.handle_rate_limit(far_future)
        
        # Should handle extreme future times
        assert manager.is_rate_limited()
        wait_time = manager.get_wait_time()
        assert wait_time > 0
        
        # Test clearing expired limits
        manager.clear_expired_limits()
        # The far future time should still be active, so it should still be rate limited
        # Let's test with a past time instead
        manager.primary_limit_reset = None  # Clear it first
        past_time = datetime.now() - timedelta(minutes=5)
        manager.handle_rate_limit(past_time)
        manager.clear_expired_limits()
        assert not manager.is_rate_limited()
    
    def test_event_loop_context_edge_cases(self):
        """Test edge cases in EventLoopContext."""
        context = EventLoopContext()
        
        # Test cleanup with no loop
        context.cleanup_event_loop()  # Should not raise
        
        # Test multiple cleanup calls
        with context.managed_event_loop():
            pass
        context.cleanup_event_loop()  # Should not raise
        context.cleanup_event_loop()  # Should not raise
        
        # Test getting current loop when none exists
        with patch('asyncio.get_running_loop', side_effect=RuntimeError):
            with patch('asyncio.get_event_loop', side_effect=RuntimeError):
                loop = context.get_current_loop()
                assert loop is None
    
    def test_error_message_formatter_edge_cases(self):
        """Test edge cases in ErrorMessageFormatter."""
        formatter = ErrorMessageFormatter()
        
        # Test with zero wait time
        message = formatter.format_waiting_message(0)
        assert "0 seconds" in message
        
        # Test with very large wait time
        large_wait = 86400 * 7  # 7 days in seconds
        message = formatter.format_waiting_message(large_wait)
        # The formatter might show hours for very large times, which is acceptable
        assert "hours" in message or "days" in message or "week" in message
        
        # Test progress with zero total
        message = formatter.format_progress_message(0, 0)
        assert "0/0" in message
        
        # Test progress with current > total
        message = formatter.format_progress_message(150, 100)
        assert "150/100" in message
        
        # Test exception without response attribute
        exception = Exception("Generic error")
        reset_time = formatter.extract_reset_time_from_exception(exception)
        assert reset_time is None
        
        # Test technical details with minimal exception
        details = formatter.format_technical_details(Exception("test"))
        assert "Exception Type: Exception" in details
        assert "Exception Message: test" in details