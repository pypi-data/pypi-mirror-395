"""Tests for intelligent cache warming manager."""

import asyncio
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, AsyncMock, patch

from src.github_ioc_scanner.cache_warming_manager import (
    CacheWarmingManager, AccessPattern, WarmingTask
)
from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
from src.github_ioc_scanner.cache import CacheManager
from src.github_ioc_scanner.models import Repository, FileContent


@pytest.fixture
def mock_cache_manager():
    """Create a mock cache manager."""
    cache_manager = Mock(spec=CacheManager)
    cache_manager.get_file_content = Mock(return_value=None)
    cache_manager.store_file_content = Mock()
    return cache_manager


@pytest.fixture
def mock_github_client():
    """Create a mock async GitHub client."""
    client = Mock(spec=AsyncGitHubClient)
    
    # Mock successful response
    mock_response = Mock()
    mock_response.data = FileContent(
        content='{"name": "test", "version": "1.0.0"}',
        sha="abc123",
        size=42
    )
    
    client.get_file_content_async = AsyncMock(return_value=mock_response)
    return client


@pytest.fixture
def sample_repository():
    """Create a sample repository for testing."""
    return Repository(
        name="test-repo",
        full_name="test-org/test-repo",
        archived=False,
        default_branch="main",
        updated_at=datetime.now(timezone.utc)
    )


@pytest.fixture
def cache_warming_manager(mock_cache_manager, mock_github_client):
    """Create a cache warming manager with mock dependencies."""
    return CacheWarmingManager(
        cache_manager=mock_cache_manager,
        github_client=mock_github_client,
        max_warming_tasks=10,
        warming_batch_size=3
    )


class TestAccessPattern:
    """Test cases for AccessPattern class."""
    
    def test_initialization(self):
        """Test access pattern initialization."""
        pattern = AccessPattern(
            file_path="package.json",
            repository="test-org/test-repo"
        )
        
        assert pattern.file_path == "package.json"
        assert pattern.repository == "test-org/test-repo"
        assert pattern.access_count == 0
        assert pattern.last_access is None
        assert pattern.first_access is None
        assert pattern.access_frequency == 0.0
    
    def test_record_access(self):
        """Test recording file access."""
        pattern = AccessPattern(
            file_path="package.json",
            repository="test-org/test-repo"
        )
        
        # Record first access
        pattern.record_access()
        
        assert pattern.access_count == 1
        assert pattern.last_access is not None
        assert pattern.first_access is not None
        assert pattern.first_access == pattern.last_access
        
        # Record second access
        pattern.record_access()
        
        assert pattern.access_count == 2
        assert pattern.last_access > pattern.first_access
    
    def test_warming_priority_no_accesses(self):
        """Test warming priority with no accesses."""
        pattern = AccessPattern(
            file_path="package.json",
            repository="test-org/test-repo"
        )
        
        assert pattern.warming_priority == 0.0
    
    def test_warming_priority_with_accesses(self):
        """Test warming priority calculation with accesses."""
        pattern = AccessPattern(
            file_path="package.json",
            repository="test-org/test-repo"
        )
        
        # Record multiple accesses
        for _ in range(5):
            pattern.record_access()
        
        priority = pattern.warming_priority
        assert 0.0 <= priority <= 1.0
        assert priority > 0.0  # Should have some priority with accesses


class TestWarmingTask:
    """Test cases for WarmingTask class."""
    
    def test_initialization(self, sample_repository):
        """Test warming task initialization."""
        task = WarmingTask(
            repository=sample_repository,
            file_path="package.json",
            priority=0.8
        )
        
        assert task.repository == sample_repository
        assert task.file_path == "package.json"
        assert task.priority == 0.8
        assert task.attempts == 0
        assert task.last_attempt is None
        assert task.should_retry is True
    
    def test_should_retry_max_attempts(self, sample_repository):
        """Test should_retry with max attempts reached."""
        task = WarmingTask(
            repository=sample_repository,
            file_path="package.json",
            priority=0.8
        )
        
        task.attempts = 3  # Max attempts
        assert task.should_retry is False
    
    def test_should_retry_recent_attempt(self, sample_repository):
        """Test should_retry with recent attempt."""
        task = WarmingTask(
            repository=sample_repository,
            file_path="package.json",
            priority=0.8
        )
        
        task.attempts = 1
        task.last_attempt = datetime.now(timezone.utc)  # Very recent
        assert task.should_retry is False


class TestCacheWarmingManager:
    """Test cases for CacheWarmingManager."""
    
    def test_initialization(self, mock_cache_manager, mock_github_client):
        """Test cache warming manager initialization."""
        manager = CacheWarmingManager(
            cache_manager=mock_cache_manager,
            github_client=mock_github_client,
            max_warming_tasks=50,
            warming_batch_size=10
        )
        
        assert manager.cache_manager == mock_cache_manager
        assert manager.github_client == mock_github_client
        assert manager.max_warming_tasks == 50
        assert manager.warming_batch_size == 10
        assert len(manager.access_patterns) == 0
        assert manager.warming_queue.qsize() == 0
    
    @pytest.mark.asyncio
    async def test_start_stop_lifecycle(self, cache_warming_manager):
        """Test start and stop lifecycle."""
        # Start warming manager
        await cache_warming_manager.start()
        
        assert cache_warming_manager.warming_worker_task is not None
        assert not cache_warming_manager.warming_worker_task.done()
        assert cache_warming_manager.pattern_analysis_task is not None
        assert not cache_warming_manager.pattern_analysis_task.done()
        
        # Stop warming manager
        await cache_warming_manager.stop()
        
        assert cache_warming_manager.warming_worker_task.done()
        assert cache_warming_manager.pattern_analysis_task.done()
    
    @pytest.mark.asyncio
    async def test_record_file_access(self, cache_warming_manager, sample_repository):
        """Test recording file access."""
        file_path = "package.json"
        
        # Record access
        await cache_warming_manager.record_file_access(sample_repository, file_path)
        
        # Check that pattern was created
        pattern_key = f"{sample_repository.full_name}:{file_path}"
        assert pattern_key in cache_warming_manager.access_patterns
        
        pattern = cache_warming_manager.access_patterns[pattern_key]
        assert pattern.access_count == 1
        assert pattern.file_path == file_path
        assert pattern.repository == sample_repository.full_name
    
    @pytest.mark.asyncio
    async def test_record_multiple_accesses(self, cache_warming_manager, sample_repository):
        """Test recording multiple accesses to same file."""
        file_path = "package.json"
        
        # Record multiple accesses
        for _ in range(3):
            await cache_warming_manager.record_file_access(sample_repository, file_path)
        
        pattern_key = f"{sample_repository.full_name}:{file_path}"
        pattern = cache_warming_manager.access_patterns[pattern_key]
        assert pattern.access_count == 3
    
    @pytest.mark.asyncio
    async def test_warm_repository_files_specific(self, cache_warming_manager, sample_repository):
        """Test warming specific repository files."""
        file_paths = ["package.json", "requirements.txt"]
        
        await cache_warming_manager.start()
        try:
            queued_count = await cache_warming_manager.warm_repository_files(
                sample_repository, file_paths, priority=0.8
            )
            
            assert queued_count == 2
            assert cache_warming_manager.warming_queue.qsize() == 2
        finally:
            await cache_warming_manager.stop()
    
    @pytest.mark.asyncio
    async def test_warm_repository_files_predicted(self, cache_warming_manager, sample_repository):
        """Test warming repository files with prediction."""
        await cache_warming_manager.start()
        try:
            # Should predict files based on project type
            queued_count = await cache_warming_manager.warm_repository_files(
                sample_repository, priority=0.5
            )
            
            assert queued_count > 0
            assert cache_warming_manager.warming_queue.qsize() > 0
        finally:
            await cache_warming_manager.stop()
    
    @pytest.mark.asyncio
    async def test_warm_organization_files(self, cache_warming_manager, sample_repository):
        """Test warming files across organization repositories."""
        repositories = [sample_repository]
        
        await cache_warming_manager.start()
        try:
            queued_count = await cache_warming_manager.warm_organization_files(
                repositories, common_files_only=True
            )
            
            assert queued_count > 0
            assert cache_warming_manager.warming_queue.qsize() > 0
        finally:
            await cache_warming_manager.stop()
    
    @pytest.mark.asyncio
    async def test_queue_warming_task_duplicate(self, cache_warming_manager, sample_repository):
        """Test that duplicate warming tasks are not queued."""
        file_path = "package.json"
        
        await cache_warming_manager.start()
        try:
            # Queue first task
            result1 = await cache_warming_manager._queue_warming_task(
                sample_repository, file_path, 0.8
            )
            assert result1 is True
            
            # Try to queue duplicate
            result2 = await cache_warming_manager._queue_warming_task(
                sample_repository, file_path, 0.8
            )
            assert result2 is False  # Should be rejected as duplicate
            
            assert cache_warming_manager.warming_queue.qsize() == 1
        finally:
            await cache_warming_manager.stop()
    
    @pytest.mark.asyncio
    async def test_queue_full_rejection(self, cache_warming_manager, sample_repository):
        """Test that tasks are rejected when queue is full."""
        # Set very small queue size
        cache_warming_manager.max_warming_tasks = 2
        
        await cache_warming_manager.start()
        try:
            # Fill the queue
            result1 = await cache_warming_manager._queue_warming_task(
                sample_repository, "file1.json", 0.8
            )
            result2 = await cache_warming_manager._queue_warming_task(
                sample_repository, "file2.json", 0.8
            )
            
            assert result1 is True
            assert result2 is True
            assert cache_warming_manager.warming_queue.qsize() == 2
            
            # Try to add one more (should be rejected)
            result3 = await cache_warming_manager._queue_warming_task(
                sample_repository, "file3.json", 0.8
            )
            assert result3 is False
            assert cache_warming_manager.warming_queue.qsize() == 2
        finally:
            await cache_warming_manager.stop()
    
    @pytest.mark.asyncio
    async def test_process_warming_task_already_cached(self, cache_warming_manager, sample_repository):
        """Test processing warming task when file is already cached."""
        # Mock cache to return content (already cached)
        cache_warming_manager.cache_manager.get_file_content.return_value = "cached content"
        
        task = WarmingTask(
            repository=sample_repository,
            file_path="package.json",
            priority=0.8
        )
        
        await cache_warming_manager._process_warming_task(task)
        
        # Should not call GitHub client since file is cached
        cache_warming_manager.github_client.get_file_content_async.assert_not_called()
        
        # Should increment cache hits stat
        stats = cache_warming_manager.get_warming_statistics()
        assert stats['cache_hits_from_warming'] == 1
    
    @pytest.mark.asyncio
    async def test_process_warming_task_fetch_and_cache(self, cache_warming_manager, sample_repository):
        """Test processing warming task that fetches and caches content."""
        # Mock cache to return None (not cached)
        cache_warming_manager.cache_manager.get_file_content.return_value = None
        
        task = WarmingTask(
            repository=sample_repository,
            file_path="package.json",
            priority=0.8
        )
        
        await cache_warming_manager._process_warming_task(task)
        
        # Should call GitHub client to fetch content
        cache_warming_manager.github_client.get_file_content_async.assert_called_once_with(
            sample_repository, "package.json"
        )
        
        # Should store in cache
        cache_warming_manager.cache_manager.store_file_content.assert_called_once()
        
        # Should increment files warmed stat
        stats = cache_warming_manager.get_warming_statistics()
        assert stats['files_warmed'] == 1
    
    @pytest.mark.asyncio
    async def test_process_warming_task_github_error(self, cache_warming_manager, sample_repository):
        """Test processing warming task when GitHub client fails."""
        # Mock cache to return None (not cached)
        cache_warming_manager.cache_manager.get_file_content.return_value = None
        
        # Mock GitHub client to raise exception
        cache_warming_manager.github_client.get_file_content_async.side_effect = Exception("API error")
        
        task = WarmingTask(
            repository=sample_repository,
            file_path="package.json",
            priority=0.8
        )
        
        await cache_warming_manager._process_warming_task(task)
        
        # Should not store in cache
        cache_warming_manager.cache_manager.store_file_content.assert_not_called()
        
        # Should increment failed tasks stat
        stats = cache_warming_manager.get_warming_statistics()
        assert stats['tasks_failed'] == 1
    
    def test_detect_project_type_by_name(self, cache_warming_manager):
        """Test project type detection by repository name."""
        # Test JavaScript detection
        js_repo = Repository(
            name="my-react-app",
            full_name="org/my-react-app",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(timezone.utc)
        )
        
        # Use asyncio.run for async method
        project_type = asyncio.run(cache_warming_manager._detect_project_type(js_repo))
        assert project_type == "javascript"
        
        # Test Python detection
        py_repo = Repository(
            name="my-python-app",
            full_name="org/my-python-app",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(timezone.utc)
        )
        
        project_type = asyncio.run(cache_warming_manager._detect_project_type(py_repo))
        assert project_type == "python"
    
    def test_detect_project_type_by_patterns(self, cache_warming_manager, sample_repository):
        """Test project type detection by access patterns."""
        # Add JavaScript-related access patterns
        cache_warming_manager.access_patterns = {
            f"{sample_repository.full_name}:package.json": AccessPattern(
                file_path="package.json",
                repository=sample_repository.full_name
            ),
            f"{sample_repository.full_name}:src/index.js": AccessPattern(
                file_path="src/index.js",
                repository=sample_repository.full_name
            )
        }
        
        project_type = asyncio.run(cache_warming_manager._detect_project_type(sample_repository))
        assert project_type == "javascript"
    
    def test_get_warming_statistics(self, cache_warming_manager):
        """Test getting warming statistics."""
        # Set some statistics
        cache_warming_manager.warming_stats.update({
            'tasks_completed': 10,
            'tasks_failed': 2,
            'files_warmed': 8,
            'cache_hits_from_warming': 3,
            'total_warming_time': 5.0
        })
        
        # Add some access patterns
        cache_warming_manager.access_patterns = {
            'repo1:file1': AccessPattern('file1', 'repo1'),
            'repo1:file2': AccessPattern('file2', 'repo1')
        }
        cache_warming_manager.access_patterns['repo1:file1'].access_count = 10  # High priority
        
        stats = cache_warming_manager.get_warming_statistics()
        
        assert stats['total_access_patterns'] == 2
        assert stats['high_priority_patterns'] >= 0
        assert stats['tasks_completed'] == 10
        assert stats['tasks_failed'] == 2
        assert stats['files_warmed'] == 8
        assert stats['cache_hits_from_warming'] == 3
        assert stats['average_warming_time'] == 0.5  # 5.0 / 10
    
    def test_reset_statistics(self, cache_warming_manager):
        """Test resetting warming statistics."""
        # Set some statistics
        cache_warming_manager.warming_stats['tasks_completed'] = 10
        cache_warming_manager.warming_stats['files_warmed'] = 5
        
        cache_warming_manager.reset_statistics()
        
        assert cache_warming_manager.warming_stats['tasks_completed'] == 0
        assert cache_warming_manager.warming_stats['files_warmed'] == 0
    
    @pytest.mark.asyncio
    async def test_async_context_manager(self, cache_warming_manager):
        """Test async context manager functionality."""
        async with cache_warming_manager as manager:
            assert manager == cache_warming_manager
            assert cache_warming_manager.warming_worker_task is not None
            assert not cache_warming_manager.warming_worker_task.done()
        
        # After exiting context, should be stopped
        assert cache_warming_manager.warming_worker_task.done()
    
    @pytest.mark.asyncio
    async def test_predict_important_files_common_patterns(self, cache_warming_manager, sample_repository):
        """Test predicting important files with common patterns."""
        # Mock project type detection
        with patch.object(cache_warming_manager, '_detect_project_type', return_value='javascript'):
            predicted_files = await cache_warming_manager._predict_important_files(sample_repository)
        
        # Should include JavaScript common files
        assert 'package.json' in predicted_files
        assert 'package-lock.json' in predicted_files
        
        # Should include general files
        assert 'README.md' in predicted_files
    
    @pytest.mark.asyncio
    async def test_predict_important_files_with_patterns(self, cache_warming_manager, sample_repository):
        """Test predicting important files with access patterns."""
        # Add access patterns for this repository
        pattern1 = AccessPattern('custom-file.json', sample_repository.full_name)
        pattern1.access_count = 5  # High priority
        
        pattern2 = AccessPattern('low-priority.txt', sample_repository.full_name)
        pattern2.access_count = 1  # Low priority
        
        cache_warming_manager.access_patterns = {
            f"{sample_repository.full_name}:custom-file.json": pattern1,
            f"{sample_repository.full_name}:low-priority.txt": pattern2
        }
        
        with patch.object(cache_warming_manager, '_detect_project_type', return_value='general'):
            predicted_files = await cache_warming_manager._predict_important_files(sample_repository)
        
        # Should include high-priority pattern file
        assert 'custom-file.json' in predicted_files
        
        # Should include general common files
        assert 'README.md' in predicted_files


class TestCacheWarmingIntegration:
    """Integration tests for cache warming functionality."""
    
    @pytest.mark.asyncio
    async def test_full_warming_workflow(self, cache_warming_manager, sample_repository):
        """Test complete cache warming workflow."""
        file_path = "package.json"
        
        async with cache_warming_manager:
            # Record access to trigger warming
            await cache_warming_manager.record_file_access(sample_repository, file_path)
            
            # Manually queue warming task
            queued = await cache_warming_manager._queue_warming_task(
                sample_repository, file_path, 0.8
            )
            assert queued is True
            
            # Allow some time for processing
            await asyncio.sleep(0.1)
            
            # Check statistics
            stats = cache_warming_manager.get_warming_statistics()
            assert stats['total_access_patterns'] == 1
    
    @pytest.mark.asyncio
    async def test_warming_with_high_priority_access(self, cache_warming_manager, sample_repository):
        """Test that high-priority access patterns trigger automatic warming."""
        file_path = "package.json"
        
        async with cache_warming_manager:
            # Record multiple accesses to make it high priority
            for _ in range(10):
                await cache_warming_manager.record_file_access(sample_repository, file_path)
            
            # Allow some time for processing
            await asyncio.sleep(0.1)
            
            # Should have queued warming task automatically
            stats = cache_warming_manager.get_warming_statistics()
            assert stats['total_access_patterns'] == 1