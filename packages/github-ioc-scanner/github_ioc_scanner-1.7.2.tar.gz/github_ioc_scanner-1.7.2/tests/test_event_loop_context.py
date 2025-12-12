"""
Tests for EventLoopContext class.
"""

import pytest
import asyncio
import threading
from unittest.mock import patch, Mock

from src.github_ioc_scanner.event_loop_context import EventLoopContext


class TestEventLoopContext:
    """Test cases for EventLoopContext."""
    
    def test_init(self):
        """Test EventLoopContext initialization."""
        context = EventLoopContext()
        assert context._loop is None
        assert hasattr(context, '_thread_local')
        
    def test_ensure_event_loop_creates_new(self):
        """Test ensuring event loop creates new one when none exists."""
        context = EventLoopContext()
        
        # Mock no running loop
        with patch('asyncio.get_running_loop', side_effect=RuntimeError):
            with patch('asyncio.get_event_loop', side_effect=RuntimeError):
                with patch('asyncio.new_event_loop') as mock_new_loop:
                    with patch('asyncio.set_event_loop') as mock_set_loop:
                        mock_loop = Mock()
                        mock_new_loop.return_value = mock_loop
                        
                        loop = context.ensure_event_loop()
                        
                        assert loop == mock_loop
                        mock_new_loop.assert_called_once()
                        mock_set_loop.assert_called_once_with(mock_loop)
                        
    def test_ensure_event_loop_uses_running(self):
        """Test ensuring event loop uses existing running loop."""
        context = EventLoopContext()
        mock_loop = Mock()
        
        with patch('asyncio.get_running_loop', return_value=mock_loop):
            loop = context.ensure_event_loop()
            assert loop == mock_loop
            
    def test_ensure_event_loop_uses_thread_default(self):
        """Test ensuring event loop uses thread's default loop."""
        context = EventLoopContext()
        mock_loop = Mock()
        mock_loop.is_closed.return_value = False
        
        with patch('asyncio.get_running_loop', side_effect=RuntimeError):
            with patch('asyncio.get_event_loop', return_value=mock_loop):
                loop = context.ensure_event_loop()
                assert loop == mock_loop
                
    def test_cleanup_event_loop_no_running_loop(self):
        """Test cleanup when no loop is running."""
        context = EventLoopContext()
        mock_loop = Mock()
        mock_loop.is_closed.return_value = False
        
        # Set up thread-local loop
        context._thread_local.loop = mock_loop
        
        with patch('asyncio.get_running_loop', side_effect=RuntimeError):
            context.cleanup_event_loop()
            
            mock_loop.close.assert_called_once()
            assert context._thread_local.loop is None
            
    def test_cleanup_event_loop_with_running_loop(self):
        """Test cleanup when a loop is running."""
        context = EventLoopContext()
        mock_loop = Mock()
        
        # Set up thread-local loop
        context._thread_local.loop = mock_loop
        
        with patch('asyncio.get_running_loop', return_value=mock_loop):
            context.cleanup_event_loop()
            
            # Should not close the running loop
            mock_loop.close.assert_not_called()
            assert context._thread_local.loop is None
            
    def test_managed_event_loop_context_manager(self):
        """Test managed event loop context manager."""
        context = EventLoopContext()
        mock_loop = Mock()
        
        with patch.object(context, 'ensure_event_loop', return_value=mock_loop):
            with patch.object(context, 'cleanup_event_loop') as mock_cleanup:
                with patch('asyncio.get_running_loop', side_effect=RuntimeError):
                    with context.managed_event_loop() as loop:
                        assert loop == mock_loop
                        
                    mock_cleanup.assert_called_once()
                    
    def test_managed_event_loop_existing_loop(self):
        """Test managed event loop with existing running loop."""
        context = EventLoopContext()
        mock_loop = Mock()
        
        with patch('asyncio.get_running_loop', return_value=mock_loop):
            with patch.object(context, 'cleanup_event_loop') as mock_cleanup:
                with context.managed_event_loop() as loop:
                    assert loop == mock_loop
                    
                # Should not cleanup existing loop
                mock_cleanup.assert_not_called()
                
    def test_is_event_loop_running_true(self):
        """Test checking if event loop is running - true case."""
        context = EventLoopContext()
        mock_loop = Mock()
        
        with patch('asyncio.get_running_loop', return_value=mock_loop):
            assert context.is_event_loop_running() is True
            
    def test_is_event_loop_running_false(self):
        """Test checking if event loop is running - false case."""
        context = EventLoopContext()
        
        with patch('asyncio.get_running_loop', side_effect=RuntimeError):
            assert context.is_event_loop_running() is False
            
    def test_get_current_loop_running(self):
        """Test getting current loop when one is running."""
        context = EventLoopContext()
        mock_loop = Mock()
        
        with patch('asyncio.get_running_loop', return_value=mock_loop):
            loop = context.get_current_loop()
            assert loop == mock_loop
            
    def test_get_current_loop_thread_default(self):
        """Test getting current loop from thread default."""
        context = EventLoopContext()
        mock_loop = Mock()
        mock_loop.is_closed.return_value = False
        
        with patch('asyncio.get_running_loop', side_effect=RuntimeError):
            with patch('asyncio.get_event_loop', return_value=mock_loop):
                loop = context.get_current_loop()
                assert loop == mock_loop
                
    def test_get_current_loop_none(self):
        """Test getting current loop when none exists."""
        context = EventLoopContext()
        
        with patch('asyncio.get_running_loop', side_effect=RuntimeError):
            with patch('asyncio.get_event_loop', side_effect=RuntimeError):
                loop = context.get_current_loop()
                assert loop is None
                
    def test_create_task_safe_with_running_loop(self):
        """Test creating task safely with running loop."""
        context = EventLoopContext()
        mock_coro = Mock()
        mock_task = Mock()
        
        with patch('asyncio.create_task', return_value=mock_task):
            task = context.create_task_safe(mock_coro)
            assert task == mock_task
            
    def test_create_task_safe_no_running_loop(self):
        """Test creating task safely without running loop."""
        context = EventLoopContext()
        mock_coro = Mock()
        mock_loop = Mock()
        mock_task = Mock()
        mock_loop.create_task.return_value = mock_task
        
        with patch('asyncio.create_task', side_effect=RuntimeError):
            with patch.object(context, 'ensure_event_loop', return_value=mock_loop):
                task = context.create_task_safe(mock_coro)
                assert task == mock_task
                mock_loop.create_task.assert_called_once_with(mock_coro)
                
    @pytest.mark.asyncio
    async def test_handle_rate_limit_async(self):
        """Test async rate limit handling."""
        context = EventLoopContext()
        
        # Test that it returns a coroutine
        coro = context.handle_rate_limit_async(0.1)
        assert asyncio.iscoroutine(coro)
        
        # Test that it actually waits
        import time
        start_time = time.time()
        await coro
        end_time = time.time()
        
        # Should have waited at least 0.1 seconds
        assert end_time - start_time >= 0.1
        
    def test_handle_rate_limit_sync(self):
        """Test sync rate limit handling."""
        context = EventLoopContext()
        
        with patch('time.sleep') as mock_sleep:
            context.handle_rate_limit_sync(5)
            mock_sleep.assert_called_once_with(5)