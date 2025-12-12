"""
Event loop context management for proper async/sync transitions.

This module provides utilities for managing event loops during rate limit
scenarios and preventing "no running event loop" errors.
"""

import asyncio
import threading
from contextlib import contextmanager
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class EventLoopContext:
    """
    Manages event loop context for proper async/sync transitions.
    
    This class provides event loop detection, creation, and cleanup
    functionality to prevent event loop errors during rate limit scenarios.
    """
    
    def __init__(self):
        """Initialize the EventLoopContext."""
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread_local = threading.local()
        
    def ensure_event_loop(self) -> asyncio.AbstractEventLoop:
        """
        Ensure an event loop exists and return it.
        
        Creates a new event loop if none exists, or returns the existing one.
        Uses thread-local storage to isolate event loops per thread.
        
        Returns:
            The current or newly created event loop
        """
        # Try to get the current running loop first
        try:
            loop = asyncio.get_running_loop()
            logger.debug("Using existing running event loop")
            return loop
        except RuntimeError:
            # No running loop, check if we have one stored
            pass
            
        # Check thread-local storage
        if hasattr(self._thread_local, 'loop') and self._thread_local.loop:
            if not self._thread_local.loop.is_closed():
                logger.debug("Using thread-local event loop")
                return self._thread_local.loop
                
        # Try to get the event loop for the current thread
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_closed():
                self._thread_local.loop = loop
                logger.debug("Using thread's default event loop")
                return loop
        except RuntimeError:
            pass
            
        # Create a new event loop
        logger.debug("Creating new event loop")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._thread_local.loop = loop
        
        return loop
        
    def cleanup_event_loop(self) -> None:
        """
        Clean up the current event loop if it was created by this context.
        
        This method should be called when done with async operations
        to prevent resource leaks.
        """
        if hasattr(self._thread_local, 'loop') and self._thread_local.loop:
            loop = self._thread_local.loop
            
            # Only close if we're not in a running loop
            try:
                asyncio.get_running_loop()
                # There's a running loop, don't close it
                logger.debug("Event loop is running, not closing")
            except RuntimeError:
                # No running loop, safe to close if needed
                if not loop.is_closed():
                    logger.debug("Closing event loop")
                    loop.close()
                    
            # Clear the thread-local reference
            self._thread_local.loop = None
            
    @contextmanager
    def managed_event_loop(self):
        """
        Context manager for automatic event loop management.
        
        Creates an event loop if needed and ensures proper cleanup.
        
        Yields:
            The managed event loop
        """
        loop = None
        created_new_loop = False
        
        try:
            # Check if we already have a running loop
            try:
                loop = asyncio.get_running_loop()
                logger.debug("Using existing running loop in context manager")
            except RuntimeError:
                # No running loop, create one
                loop = self.ensure_event_loop()
                created_new_loop = True
                logger.debug("Created new loop in context manager")
                
            yield loop
            
        finally:
            # Only cleanup if we created a new loop
            if created_new_loop:
                self.cleanup_event_loop()
                
    def run_async_function(self, coro):
        """
        Run an async function safely, handling event loop context.
        
        Args:
            coro: The coroutine to run
            
        Returns:
            The result of the coroutine
        """
        try:
            # Try to get the current running loop
            loop = asyncio.get_running_loop()
            # We're already in an async context, create a task
            logger.debug("Running coroutine as task in existing loop")
            return asyncio.create_task(coro)
        except RuntimeError:
            # No running loop, run with our managed loop
            logger.debug("Running coroutine with managed event loop")
            with self.managed_event_loop() as loop:
                return loop.run_until_complete(coro)
                
    def is_event_loop_running(self) -> bool:
        """
        Check if an event loop is currently running.
        
        Returns:
            True if an event loop is running, False otherwise
        """
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False
            
    def get_current_loop(self) -> Optional[asyncio.AbstractEventLoop]:
        """
        Get the current event loop if one exists.
        
        Returns:
            The current event loop or None if no loop exists
        """
        try:
            return asyncio.get_running_loop()
        except RuntimeError:
            try:
                loop = asyncio.get_event_loop()
                if not loop.is_closed():
                    return loop
            except RuntimeError:
                pass
                
        return None
        
    def create_task_safe(self, coro):
        """
        Create a task safely, ensuring proper event loop context.
        
        Args:
            coro: The coroutine to create a task for
            
        Returns:
            The created task
        """
        try:
            # Try to create task in current loop
            return asyncio.create_task(coro)
        except RuntimeError:
            # No running loop, ensure we have one
            loop = self.ensure_event_loop()
            return loop.create_task(coro)
            
    def handle_rate_limit_async(self, wait_seconds: int):
        """
        Handle rate limit waiting in async context.
        
        Args:
            wait_seconds: Number of seconds to wait
            
        Returns:
            Coroutine that waits for the specified time
        """
        async def wait_for_reset():
            logger.debug(f"Async waiting {wait_seconds} seconds for rate limit reset")
            await asyncio.sleep(wait_seconds)
            logger.debug("Rate limit wait completed")
            
        return wait_for_reset()
        
    def handle_rate_limit_sync(self, wait_seconds: int):
        """
        Handle rate limit waiting in sync context.
        
        Args:
            wait_seconds: Number of seconds to wait
        """
        import time
        logger.debug(f"Sync waiting {wait_seconds} seconds for rate limit reset")
        time.sleep(wait_seconds)
        logger.debug("Rate limit wait completed")