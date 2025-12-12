"""Resource management and cleanup for batch processing operations."""

import asyncio
import gc
import logging
import weakref
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Callable, AsyncIterator
from datetime import datetime, timedelta

from .memory_monitor import MemoryMonitor
from .logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class ResourceStats:
    """Statistics about resource usage and cleanup."""
    active_resources: int = 0
    total_resources_created: int = 0
    total_resources_cleaned: int = 0
    memory_cleanups_performed: int = 0
    total_memory_freed_mb: float = 0.0
    last_cleanup_time: Optional[datetime] = None
    cleanup_duration_seconds: float = 0.0


@dataclass
class ResourceConfig:
    """Configuration for resource management."""
    auto_cleanup_enabled: bool = True
    cleanup_interval_seconds: float = 30.0
    memory_cleanup_threshold: float = 0.8  # Trigger cleanup at 80% memory usage
    max_resource_age_seconds: float = 300.0  # 5 minutes
    force_gc_on_cleanup: bool = True
    track_resource_usage: bool = True


class ManagedResource:
    """Base class for managed resources that can be automatically cleaned up."""
    
    def __init__(self, resource_id: str, cleanup_callback: Optional[Callable] = None):
        """Initialize managed resource.
        
        Args:
            resource_id: Unique identifier for the resource
            cleanup_callback: Optional callback to call during cleanup
        """
        self.resource_id = resource_id
        self.created_at = datetime.now()
        self.cleanup_callback = cleanup_callback
        self._cleaned_up = False
    
    async def cleanup(self) -> None:
        """Clean up the resource."""
        if self._cleaned_up:
            return
        
        try:
            if self.cleanup_callback:
                if asyncio.iscoroutinefunction(self.cleanup_callback):
                    await self.cleanup_callback()
                else:
                    self.cleanup_callback()
            
            await self._cleanup_implementation()
            self._cleaned_up = True
            logger.debug(f"Cleaned up resource: {self.resource_id}")
            
        except Exception as e:
            logger.error(f"Error cleaning up resource {self.resource_id}: {e}")
            # Still mark as cleaned up to prevent retry loops
            self._cleaned_up = True
    
    async def _cleanup_implementation(self) -> None:
        """Override this method to implement specific cleanup logic."""
        pass
    
    @property
    def is_cleaned_up(self) -> bool:
        """Check if resource has been cleaned up."""
        return self._cleaned_up
    
    @property
    def age_seconds(self) -> float:
        """Get age of resource in seconds."""
        return (datetime.now() - self.created_at).total_seconds()


class BatchResource(ManagedResource):
    """Managed resource for batch processing operations."""
    
    def __init__(
        self, 
        resource_id: str, 
        batch_data: Any = None,
        semaphore: Optional[asyncio.Semaphore] = None,
        session: Any = None
    ):
        """Initialize batch resource.
        
        Args:
            resource_id: Unique identifier for the resource
            batch_data: Data associated with the batch
            semaphore: Asyncio semaphore for concurrency control
            session: HTTP session or similar resource
        """
        super().__init__(resource_id)
        self.batch_data = batch_data
        self.semaphore = semaphore
        self.session = session
        self.results: List[Any] = []
    
    async def _cleanup_implementation(self) -> None:
        """Clean up batch-specific resources."""
        # Clear batch data
        if self.batch_data:
            if hasattr(self.batch_data, 'clear'):
                self.batch_data.clear()
            self.batch_data = None
        
        # Clear results
        self.results.clear()
        
        # Close session if it has a close method
        if self.session and hasattr(self.session, 'close'):
            try:
                if asyncio.iscoroutinefunction(self.session.close):
                    await self.session.close()
                else:
                    self.session.close()
            except Exception as e:
                logger.warning(f"Error closing session in resource {self.resource_id}: {e}")
        
        self.session = None


class ResourceManager:
    """Manages resources and performs automatic cleanup to prevent memory leaks."""
    
    def __init__(self, config: Optional[ResourceConfig] = None):
        """Initialize resource manager.
        
        Args:
            config: Resource management configuration
        """
        self.config = config or ResourceConfig()
        self.stats = ResourceStats()
        
        # Track active resources using weak references to avoid circular references
        self._active_resources: Dict[str, ManagedResource] = {}
        self._resource_refs: Set[weakref.ReferenceType] = set()
        
        # Memory monitor for cleanup decisions
        self.memory_monitor = MemoryMonitor() if self.config.track_resource_usage else None
        
        # Cleanup task
        self._cleanup_task: Optional[asyncio.Task] = None
        self._shutdown_event = asyncio.Event()
        
        # Start automatic cleanup if enabled (only if event loop is running)
        if self.config.auto_cleanup_enabled:
            try:
                self.start_auto_cleanup()
            except RuntimeError:
                # No event loop running, will start later when needed
                pass
    
    def register_resource(self, resource: ManagedResource) -> None:
        """Register a resource for management.
        
        Args:
            resource: Resource to register
        """
        self._active_resources[resource.resource_id] = resource
        
        # Create weak reference with cleanup callback
        def cleanup_ref(ref):
            self._resource_refs.discard(ref)
        
        ref = weakref.ref(resource, cleanup_ref)
        self._resource_refs.add(ref)
        
        self.stats.total_resources_created += 1
        self.stats.active_resources = len(self._active_resources)
        
        logger.debug(f"Registered resource: {resource.resource_id}")
    
    def unregister_resource(self, resource_id: str) -> None:
        """Unregister a resource from management.
        
        Args:
            resource_id: ID of resource to unregister
        """
        if resource_id in self._active_resources:
            del self._active_resources[resource_id]
            self.stats.total_resources_cleaned += 1
            self.stats.active_resources = len(self._active_resources)
            logger.debug(f"Unregistered resource: {resource_id}")
    
    async def cleanup_resource(self, resource_id: str) -> bool:
        """Clean up a specific resource.
        
        Args:
            resource_id: ID of resource to clean up
            
        Returns:
            True if resource was cleaned up, False if not found
        """
        resource = self._active_resources.get(resource_id)
        if resource:
            await resource.cleanup()
            self.unregister_resource(resource_id)
            return True
        return False
    
    async def cleanup_old_resources(self) -> int:
        """Clean up resources that are older than the configured age limit.
        
        Returns:
            Number of resources cleaned up
        """
        cleanup_count = 0
        current_time = datetime.now()
        resources_to_cleanup = []
        
        # Find old resources
        for resource_id, resource in self._active_resources.items():
            if resource.age_seconds > self.config.max_resource_age_seconds:
                resources_to_cleanup.append(resource_id)
        
        # Clean up old resources
        for resource_id in resources_to_cleanup:
            if await self.cleanup_resource(resource_id):
                cleanup_count += 1
        
        if cleanup_count > 0:
            logger.info(f"Cleaned up {cleanup_count} old resources")
        
        return cleanup_count
    
    async def cleanup_all_resources(self) -> int:
        """Clean up all registered resources.
        
        Returns:
            Number of resources cleaned up
        """
        cleanup_count = 0
        resource_ids = list(self._active_resources.keys())
        
        for resource_id in resource_ids:
            if await self.cleanup_resource(resource_id):
                cleanup_count += 1
        
        logger.info(f"Cleaned up all {cleanup_count} resources")
        return cleanup_count
    
    async def perform_memory_cleanup(self) -> Dict[str, Any]:
        """Perform memory cleanup operations.
        
        Returns:
            Dictionary containing cleanup statistics
        """
        cleanup_start = datetime.now()
        
        # Get memory stats before cleanup
        memory_before = None
        if self.memory_monitor:
            memory_before = self.memory_monitor.get_memory_stats()
        
        # Clean up old resources first
        old_resources_cleaned = await self.cleanup_old_resources()
        
        # Force garbage collection if configured
        gc_stats = {}
        if self.config.force_gc_on_cleanup:
            if self.memory_monitor:
                gc_stats = self.memory_monitor.force_garbage_collection()
            else:
                collected = gc.collect()
                gc_stats = {'objects_collected': collected}
        
        # Get memory stats after cleanup
        memory_after = None
        memory_freed = 0.0
        if self.memory_monitor:
            memory_after = self.memory_monitor.get_memory_stats()
            if memory_before:
                memory_freed = memory_before.process_mb - memory_after.process_mb
        
        # Update statistics
        cleanup_duration = (datetime.now() - cleanup_start).total_seconds()
        self.stats.memory_cleanups_performed += 1
        self.stats.total_memory_freed_mb += memory_freed
        self.stats.last_cleanup_time = cleanup_start
        self.stats.cleanup_duration_seconds = cleanup_duration
        
        cleanup_stats = {
            'old_resources_cleaned': old_resources_cleaned,
            'memory_freed_mb': memory_freed,
            'cleanup_duration_seconds': cleanup_duration,
            'gc_stats': gc_stats,
            'memory_before': memory_before,
            'memory_after': memory_after
        }
        
        logger.debug(f"Memory cleanup completed: freed {memory_freed:.2f} MB in {cleanup_duration:.2f}s")
        return cleanup_stats
    
    def should_perform_cleanup(self) -> bool:
        """Determine if cleanup should be performed based on memory pressure.
        
        Returns:
            True if cleanup should be performed
        """
        if not self.memory_monitor:
            # If no memory monitoring, clean up based on resource count
            return len(self._active_resources) > 10
        
        # Check memory pressure
        memory_stats = self.memory_monitor.get_memory_stats()
        return memory_stats.percent_used > self.config.memory_cleanup_threshold
    
    def start_auto_cleanup(self) -> None:
        """Start automatic cleanup task."""
        if self._cleanup_task is None or self._cleanup_task.done():
            try:
                # Check if there's a running event loop
                loop = asyncio.get_running_loop()
                self._cleanup_task = loop.create_task(self._auto_cleanup_loop())
                logger.info("Started automatic resource cleanup")
            except RuntimeError as e:
                if "no running event loop" in str(e) or "no current event loop" in str(e):
                    # No event loop running, task will be started later
                    logger.debug("No event loop running, auto cleanup will start later")
                else:
                    raise
    
    def stop_auto_cleanup(self) -> None:
        """Stop automatic cleanup task."""
        self._shutdown_event.set()
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()
            logger.info("Stopped automatic resource cleanup")
    
    async def _auto_cleanup_loop(self) -> None:
        """Main loop for automatic cleanup."""
        try:
            while not self._shutdown_event.is_set():
                try:
                    # Wait for cleanup interval or shutdown
                    await asyncio.wait_for(
                        self._shutdown_event.wait(),
                        timeout=self.config.cleanup_interval_seconds
                    )
                    break  # Shutdown requested
                except asyncio.TimeoutError:
                    # Timeout reached, perform cleanup check
                    pass
                
                # Check if cleanup is needed
                if self.should_perform_cleanup():
                    await self.perform_memory_cleanup()
                
        except asyncio.CancelledError:
            logger.debug("Auto cleanup loop cancelled")
        except Exception as e:
            logger.error(f"Error in auto cleanup loop: {e}")
    
    @asynccontextmanager
    async def managed_resource(
        self, 
        resource_id: str, 
        resource_type: type = ManagedResource,
        **kwargs
    ) -> AsyncIterator[ManagedResource]:
        """Context manager for automatic resource management.
        
        Args:
            resource_id: Unique identifier for the resource
            resource_type: Type of resource to create
            **kwargs: Additional arguments for resource creation
            
        Yields:
            Managed resource instance
        """
        resource = resource_type(resource_id, **kwargs)
        self.register_resource(resource)
        
        try:
            yield resource
        finally:
            await resource.cleanup()
            self.unregister_resource(resource_id)
    
    @asynccontextmanager
    async def managed_batch_resource(
        self,
        resource_id: str,
        **kwargs
    ) -> AsyncIterator[BatchResource]:
        """Context manager for batch resource management.
        
        Args:
            resource_id: Unique identifier for the batch resource
            **kwargs: Additional arguments for BatchResource creation
            
        Yields:
            Managed batch resource instance
        """
        async with self.managed_resource(resource_id, BatchResource, **kwargs) as resource:
            yield resource
    
    def get_resource_stats(self) -> Dict[str, Any]:
        """Get comprehensive resource management statistics.
        
        Returns:
            Dictionary containing resource statistics
        """
        memory_stats = None
        if self.memory_monitor:
            memory_stats = self.memory_monitor.get_memory_report()
        
        return {
            'resource_stats': {
                'active_resources': self.stats.active_resources,
                'total_resources_created': self.stats.total_resources_created,
                'total_resources_cleaned': self.stats.total_resources_cleaned,
                'memory_cleanups_performed': self.stats.memory_cleanups_performed,
                'total_memory_freed_mb': self.stats.total_memory_freed_mb,
                'last_cleanup_time': self.stats.last_cleanup_time.isoformat() if self.stats.last_cleanup_time else None,
                'cleanup_duration_seconds': self.stats.cleanup_duration_seconds
            },
            'config': {
                'auto_cleanup_enabled': self.config.auto_cleanup_enabled,
                'cleanup_interval_seconds': self.config.cleanup_interval_seconds,
                'memory_cleanup_threshold': self.config.memory_cleanup_threshold,
                'max_resource_age_seconds': self.config.max_resource_age_seconds,
                'force_gc_on_cleanup': self.config.force_gc_on_cleanup,
                'track_resource_usage': self.config.track_resource_usage
            },
            'memory_stats': memory_stats
        }
    
    async def shutdown(self) -> None:
        """Shutdown resource manager and clean up all resources."""
        logger.info("Shutting down resource manager")
        
        # Stop auto cleanup
        self.stop_auto_cleanup()
        
        # Clean up all resources
        await self.cleanup_all_resources()
        
        # Wait for cleanup task to finish
        if self._cleanup_task and not self._cleanup_task.done():
            try:
                await asyncio.wait_for(self._cleanup_task, timeout=5.0)
            except asyncio.TimeoutError:
                logger.warning("Cleanup task did not finish within timeout")
                self._cleanup_task.cancel()
        
        logger.info("Resource manager shutdown complete")


# Global resource manager instance
_global_resource_manager: Optional[ResourceManager] = None


def get_resource_manager() -> ResourceManager:
    """Get the global resource manager instance.
    
    Returns:
        Global resource manager instance
    """
    global _global_resource_manager
    if _global_resource_manager is None:
        _global_resource_manager = ResourceManager()
    return _global_resource_manager


def set_resource_manager(manager: ResourceManager) -> None:
    """Set the global resource manager instance.
    
    Args:
        manager: Resource manager to set as global
    """
    global _global_resource_manager
    _global_resource_manager = manager