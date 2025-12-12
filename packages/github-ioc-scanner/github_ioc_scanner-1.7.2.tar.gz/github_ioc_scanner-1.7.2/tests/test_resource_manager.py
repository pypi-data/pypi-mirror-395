"""Tests for resource management and cleanup."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from src.github_ioc_scanner.resource_manager import (
    ResourceManager, ManagedResource, BatchResource, ResourceConfig,
    ResourceStats, get_resource_manager, set_resource_manager
)


class TestManagedResource:
    """Test managed resource functionality."""
    
    @pytest.mark.asyncio
    async def test_basic_resource_creation(self):
        """Test basic resource creation and properties."""
        resource = ManagedResource("test-resource-1")
        
        assert resource.resource_id == "test-resource-1"
        assert resource.created_at is not None
        assert resource.age_seconds >= 0
        assert not resource.is_cleaned_up
    
    @pytest.mark.asyncio
    async def test_resource_cleanup_without_callback(self):
        """Test resource cleanup without callback."""
        resource = ManagedResource("test-resource-2")
        
        await resource.cleanup()
        
        assert resource.is_cleaned_up
    
    @pytest.mark.asyncio
    async def test_resource_cleanup_with_sync_callback(self):
        """Test resource cleanup with synchronous callback."""
        callback_called = False
        
        def cleanup_callback():
            nonlocal callback_called
            callback_called = True
        
        resource = ManagedResource("test-resource-3", cleanup_callback)
        
        await resource.cleanup()
        
        assert resource.is_cleaned_up
        assert callback_called
    
    @pytest.mark.asyncio
    async def test_resource_cleanup_with_async_callback(self):
        """Test resource cleanup with asynchronous callback."""
        callback_called = False
        
        async def cleanup_callback():
            nonlocal callback_called
            callback_called = True
        
        resource = ManagedResource("test-resource-4", cleanup_callback)
        
        await resource.cleanup()
        
        assert resource.is_cleaned_up
        assert callback_called
    
    @pytest.mark.asyncio
    async def test_resource_cleanup_idempotent(self):
        """Test that resource cleanup is idempotent."""
        callback_count = 0
        
        def cleanup_callback():
            nonlocal callback_count
            callback_count += 1
        
        resource = ManagedResource("test-resource-5", cleanup_callback)
        
        # Clean up multiple times
        await resource.cleanup()
        await resource.cleanup()
        await resource.cleanup()
        
        assert resource.is_cleaned_up
        assert callback_count == 1  # Should only be called once
    
    @pytest.mark.asyncio
    async def test_resource_cleanup_error_handling(self):
        """Test resource cleanup with callback error."""
        def failing_callback():
            raise Exception("Callback error")
        
        resource = ManagedResource("test-resource-6", failing_callback)
        
        # Should not raise exception
        await resource.cleanup()
        
        assert resource.is_cleaned_up
    
    def test_resource_age_calculation(self):
        """Test resource age calculation."""
        resource = ManagedResource("test-resource-7")
        
        # Age should be very small initially
        assert resource.age_seconds < 1.0
        
        # Mock older creation time
        resource.created_at = datetime.now() - timedelta(seconds=30)
        assert resource.age_seconds >= 30.0


class TestBatchResource:
    """Test batch resource functionality."""
    
    @pytest.mark.asyncio
    async def test_batch_resource_creation(self):
        """Test batch resource creation."""
        batch_data = {"key": "value"}
        semaphore = asyncio.Semaphore(5)
        session = MagicMock()
        
        resource = BatchResource(
            "batch-resource-1",
            batch_data=batch_data,
            semaphore=semaphore,
            session=session
        )
        
        assert resource.resource_id == "batch-resource-1"
        assert resource.batch_data == batch_data
        assert resource.semaphore == semaphore
        assert resource.session == session
        assert resource.results == []
    
    @pytest.mark.asyncio
    async def test_batch_resource_cleanup(self):
        """Test batch resource cleanup."""
        batch_data = {"key": "value", "items": [1, 2, 3]}
        session = MagicMock()
        session.close = MagicMock()
        
        resource = BatchResource(
            "batch-resource-2",
            batch_data=batch_data,
            session=session
        )
        
        # Add some results
        resource.results.extend([1, 2, 3])
        
        await resource.cleanup()
        
        assert resource.is_cleaned_up
        assert resource.batch_data is None
        assert resource.results == []
        assert resource.session is None
        session.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_batch_resource_cleanup_with_async_session(self):
        """Test batch resource cleanup with async session."""
        session = AsyncMock()
        
        resource = BatchResource(
            "batch-resource-3",
            session=session
        )
        
        await resource.cleanup()
        
        assert resource.is_cleaned_up
        session.close.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_batch_resource_cleanup_session_error(self):
        """Test batch resource cleanup with session close error."""
        session = MagicMock()
        session.close.side_effect = Exception("Close error")
        
        resource = BatchResource(
            "batch-resource-4",
            session=session
        )
        
        # Should not raise exception
        await resource.cleanup()
        
        assert resource.is_cleaned_up
        assert resource.session is None


class TestResourceManager:
    """Test resource manager functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = ResourceConfig(
            auto_cleanup_enabled=False,  # Disable for testing
            cleanup_interval_seconds=1.0,
            memory_cleanup_threshold=0.8,
            max_resource_age_seconds=5.0
        )
        self.manager = ResourceManager(self.config)
    
    def teardown_method(self):
        """Clean up after tests."""
        if self.manager:
            # Don't try to shutdown in teardown as there may be no event loop
            # Individual tests should handle cleanup if needed
            pass
    
    def test_manager_initialization(self):
        """Test resource manager initialization."""
        assert self.manager.config == self.config
        assert isinstance(self.manager.stats, ResourceStats)
        assert self.manager.memory_monitor is not None
        assert len(self.manager._active_resources) == 0
    
    def test_manager_initialization_without_memory_monitoring(self):
        """Test manager initialization without memory monitoring."""
        config = ResourceConfig(track_resource_usage=False, auto_cleanup_enabled=False)
        manager = ResourceManager(config)
        
        assert manager.memory_monitor is None
    
    def test_register_resource(self):
        """Test resource registration."""
        resource = ManagedResource("test-resource")
        
        self.manager.register_resource(resource)
        
        assert resource.resource_id in self.manager._active_resources
        assert self.manager.stats.total_resources_created == 1
        assert self.manager.stats.active_resources == 1
    
    def test_unregister_resource(self):
        """Test resource unregistration."""
        resource = ManagedResource("test-resource")
        self.manager.register_resource(resource)
        
        self.manager.unregister_resource("test-resource")
        
        assert "test-resource" not in self.manager._active_resources
        assert self.manager.stats.total_resources_cleaned == 1
        assert self.manager.stats.active_resources == 0
    
    @pytest.mark.asyncio
    async def test_cleanup_resource(self):
        """Test cleaning up a specific resource."""
        resource = ManagedResource("test-resource")
        self.manager.register_resource(resource)
        
        result = await self.manager.cleanup_resource("test-resource")
        
        assert result is True
        assert resource.is_cleaned_up
        assert "test-resource" not in self.manager._active_resources
    
    @pytest.mark.asyncio
    async def test_cleanup_nonexistent_resource(self):
        """Test cleaning up a nonexistent resource."""
        result = await self.manager.cleanup_resource("nonexistent")
        
        assert result is False
    
    @pytest.mark.asyncio
    async def test_cleanup_old_resources(self):
        """Test cleaning up old resources."""
        # Create resources with different ages
        old_resource = ManagedResource("old-resource")
        old_resource.created_at = datetime.now() - timedelta(seconds=10)  # Older than 5s limit
        
        new_resource = ManagedResource("new-resource")
        
        self.manager.register_resource(old_resource)
        self.manager.register_resource(new_resource)
        
        cleanup_count = await self.manager.cleanup_old_resources()
        
        assert cleanup_count == 1
        assert old_resource.is_cleaned_up
        assert not new_resource.is_cleaned_up
        assert "old-resource" not in self.manager._active_resources
        assert "new-resource" in self.manager._active_resources
    
    @pytest.mark.asyncio
    async def test_cleanup_all_resources(self):
        """Test cleaning up all resources."""
        resources = [
            ManagedResource("resource-1"),
            ManagedResource("resource-2"),
            ManagedResource("resource-3")
        ]
        
        for resource in resources:
            self.manager.register_resource(resource)
        
        cleanup_count = await self.manager.cleanup_all_resources()
        
        assert cleanup_count == 3
        assert all(resource.is_cleaned_up for resource in resources)
        assert len(self.manager._active_resources) == 0
    
    @pytest.mark.asyncio
    async def test_perform_memory_cleanup(self):
        """Test memory cleanup operations."""
        # Create some old resources
        old_resource = ManagedResource("old-resource")
        old_resource.created_at = datetime.now() - timedelta(seconds=10)
        self.manager.register_resource(old_resource)
        
        with patch.object(self.manager.memory_monitor, 'get_memory_stats') as mock_stats, \
             patch.object(self.manager.memory_monitor, 'force_garbage_collection') as mock_gc:
            
            # Mock memory stats
            mock_memory_stats = MagicMock()
            mock_memory_stats.process_mb = 100.0
            mock_stats.side_effect = [
                mock_memory_stats,  # Before cleanup
                MagicMock(process_mb=90.0)  # After cleanup
            ]
            
            mock_gc.return_value = {'objects_collected': 42, 'memory_freed_mb': 10.0}
            
            cleanup_stats = await self.manager.perform_memory_cleanup()
            
            assert 'old_resources_cleaned' in cleanup_stats
            assert cleanup_stats['old_resources_cleaned'] == 1
            assert cleanup_stats['memory_freed_mb'] == 10.0
            assert 'cleanup_duration_seconds' in cleanup_stats
            assert 'gc_stats' in cleanup_stats
            
            # Check manager stats were updated
            assert self.manager.stats.memory_cleanups_performed == 1
            assert self.manager.stats.total_memory_freed_mb == 10.0
            assert self.manager.stats.last_cleanup_time is not None
    
    def test_should_perform_cleanup_with_memory_monitoring(self):
        """Test cleanup decision with memory monitoring."""
        with patch.object(self.manager.memory_monitor, 'get_memory_stats') as mock_stats:
            # High memory usage
            mock_memory_stats = MagicMock()
            mock_memory_stats.percent_used = 0.9  # 90% > 80% threshold
            mock_stats.return_value = mock_memory_stats
            
            assert self.manager.should_perform_cleanup() is True
            
            # Low memory usage
            mock_memory_stats.percent_used = 0.5  # 50% < 80% threshold
            assert self.manager.should_perform_cleanup() is False
    
    def test_should_perform_cleanup_without_memory_monitoring(self):
        """Test cleanup decision without memory monitoring."""
        # Disable memory monitoring
        self.manager.memory_monitor = None
        
        # Few resources - no cleanup needed
        assert self.manager.should_perform_cleanup() is False
        
        # Many resources - cleanup needed
        for i in range(15):
            resource = ManagedResource(f"resource-{i}")
            self.manager.register_resource(resource)
        
        assert self.manager.should_perform_cleanup() is True
    
    @pytest.mark.asyncio
    async def test_managed_resource_context_manager(self):
        """Test managed resource context manager."""
        async with self.manager.managed_resource("context-resource") as resource:
            assert isinstance(resource, ManagedResource)
            assert resource.resource_id == "context-resource"
            assert "context-resource" in self.manager._active_resources
        
        # After context exit, resource should be cleaned up
        assert resource.is_cleaned_up
        assert "context-resource" not in self.manager._active_resources
    
    @pytest.mark.asyncio
    async def test_managed_batch_resource_context_manager(self):
        """Test managed batch resource context manager."""
        batch_data = {"test": "data"}
        
        async with self.manager.managed_batch_resource(
            "batch-context-resource",
            batch_data=batch_data
        ) as resource:
            assert isinstance(resource, BatchResource)
            assert resource.resource_id == "batch-context-resource"
            assert resource.batch_data == batch_data
            assert "batch-context-resource" in self.manager._active_resources
        
        # After context exit, resource should be cleaned up
        assert resource.is_cleaned_up
        assert "batch-context-resource" not in self.manager._active_resources
    
    def test_get_resource_stats(self):
        """Test getting resource statistics."""
        # Add some resources
        for i in range(3):
            resource = ManagedResource(f"resource-{i}")
            self.manager.register_resource(resource)
        
        with patch.object(self.manager.memory_monitor, 'get_memory_report') as mock_report:
            mock_report.return_value = {'memory_usage': '50%'}
            
            stats = self.manager.get_resource_stats()
            
            assert 'resource_stats' in stats
            assert stats['resource_stats']['active_resources'] == 3
            assert stats['resource_stats']['total_resources_created'] == 3
            
            assert 'config' in stats
            assert stats['config']['auto_cleanup_enabled'] == self.config.auto_cleanup_enabled
            
            assert 'memory_stats' in stats
            assert stats['memory_stats'] == {'memory_usage': '50%'}
    
    @pytest.mark.asyncio
    async def test_auto_cleanup_start_stop(self):
        """Test starting and stopping auto cleanup."""
        # Enable auto cleanup
        config = ResourceConfig(auto_cleanup_enabled=True, cleanup_interval_seconds=0.1)
        manager = ResourceManager(config)
        
        # Should start automatically
        assert manager._cleanup_task is not None
        assert not manager._cleanup_task.done()
        
        # Stop cleanup
        manager.stop_auto_cleanup()
        
        # Wait a bit for task to be cancelled
        await asyncio.sleep(0.05)
        
        assert manager._cleanup_task.cancelled() or manager._cleanup_task.done()
        
        await manager.shutdown()
    
    @pytest.mark.asyncio
    async def test_shutdown(self):
        """Test resource manager shutdown."""
        # Add some resources
        resources = [ManagedResource(f"resource-{i}") for i in range(3)]
        for resource in resources:
            self.manager.register_resource(resource)
        
        await self.manager.shutdown()
        
        # All resources should be cleaned up
        assert all(resource.is_cleaned_up for resource in resources)
        assert len(self.manager._active_resources) == 0


class TestGlobalResourceManager:
    """Test global resource manager functions."""
    
    def test_get_global_resource_manager(self):
        """Test getting global resource manager."""
        # Reset global manager first
        set_resource_manager(None)
        
        # Create with auto cleanup disabled to avoid event loop issues
        with patch('src.github_ioc_scanner.resource_manager.ResourceManager') as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager_class.return_value = mock_manager
            
            manager1 = get_resource_manager()
            manager2 = get_resource_manager()
            
            assert manager1 is manager2  # Should be same instance
            mock_manager_class.assert_called_once()
    
    def test_set_global_resource_manager(self):
        """Test setting global resource manager."""
        custom_manager = MagicMock()
        set_resource_manager(custom_manager)
        
        retrieved_manager = get_resource_manager()
        assert retrieved_manager is custom_manager


class TestResourceConfig:
    """Test resource configuration."""
    
    def test_default_config(self):
        """Test default resource configuration."""
        config = ResourceConfig()
        
        assert config.auto_cleanup_enabled is True
        assert config.cleanup_interval_seconds == 30.0
        assert config.memory_cleanup_threshold == 0.8
        assert config.max_resource_age_seconds == 300.0
        assert config.force_gc_on_cleanup is True
        assert config.track_resource_usage is True
    
    def test_custom_config(self):
        """Test custom resource configuration."""
        config = ResourceConfig(
            auto_cleanup_enabled=False,
            cleanup_interval_seconds=60.0,
            memory_cleanup_threshold=0.9,
            max_resource_age_seconds=600.0,
            force_gc_on_cleanup=False,
            track_resource_usage=False
        )
        
        assert config.auto_cleanup_enabled is False
        assert config.cleanup_interval_seconds == 60.0
        assert config.memory_cleanup_threshold == 0.9
        assert config.max_resource_age_seconds == 600.0
        assert config.force_gc_on_cleanup is False
        assert config.track_resource_usage is False


class TestResourceStats:
    """Test resource statistics."""
    
    def test_default_stats(self):
        """Test default resource statistics."""
        stats = ResourceStats()
        
        assert stats.active_resources == 0
        assert stats.total_resources_created == 0
        assert stats.total_resources_cleaned == 0
        assert stats.memory_cleanups_performed == 0
        assert stats.total_memory_freed_mb == 0.0
        assert stats.last_cleanup_time is None
        assert stats.cleanup_duration_seconds == 0.0


if __name__ == '__main__':
    pytest.main([__file__])