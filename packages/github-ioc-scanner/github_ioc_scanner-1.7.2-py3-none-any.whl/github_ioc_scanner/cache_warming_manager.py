"""Intelligent cache warming manager for predictive cache preloading."""

import asyncio
import json
import time
from collections import defaultdict, deque
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field

from .async_github_client import AsyncGitHubClient
from .batch_models import BatchRequest, BatchResult
from .cache import CacheManager
from .exceptions import CacheError
from .logging_config import get_logger
from .models import Repository, FileContent

logger = get_logger(__name__)


@dataclass
class AccessPattern:
    """Represents an access pattern for cache warming predictions."""
    file_path: str
    repository: str
    access_count: int = 0
    last_access: Optional[datetime] = None
    first_access: Optional[datetime] = None
    access_frequency: float = 0.0  # accesses per hour
    access_times: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def record_access(self):
        """Record a new access to this file."""
        now = datetime.now(timezone.utc)
        self.access_count += 1
        self.last_access = now
        
        if self.first_access is None:
            self.first_access = now
        
        self.access_times.append(now)
        self._update_frequency()
    
    def _update_frequency(self):
        """Update access frequency based on recent access times."""
        if len(self.access_times) < 2:
            self.access_frequency = 0.0
            return
        
        # Calculate frequency based on recent accesses
        time_span = (self.access_times[-1] - self.access_times[0]).total_seconds()
        if time_span > 0:
            self.access_frequency = (len(self.access_times) - 1) / (time_span / 3600)  # per hour
    
    @property
    def warming_priority(self) -> float:
        """Calculate warming priority score (0-1, higher is more important)."""
        if self.access_count == 0:
            return 0.0
        
        # Base score on access count and frequency
        count_score = min(1.0, self.access_count / 10.0)  # Normalize to 10 accesses
        frequency_score = min(1.0, self.access_frequency / 5.0)  # Normalize to 5 per hour
        
        # Boost score for recent accesses
        recency_score = 0.0
        if self.last_access:
            hours_since_access = (datetime.now(timezone.utc) - self.last_access).total_seconds() / 3600
            recency_score = max(0.0, 1.0 - (hours_since_access / 24.0))  # Decay over 24 hours
        
        # Weighted combination
        return (count_score * 0.4 + frequency_score * 0.4 + recency_score * 0.2)


@dataclass
class WarmingTask:
    """Represents a cache warming task."""
    repository: Repository
    file_path: str
    priority: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attempts: int = 0
    last_attempt: Optional[datetime] = None
    
    @property
    def should_retry(self) -> bool:
        """Whether this task should be retried."""
        if self.attempts >= 3:  # Max 3 attempts
            return False
        
        if self.last_attempt is None:
            return True
        
        # Wait at least 5 minutes between attempts
        time_since_attempt = datetime.now(timezone.utc) - self.last_attempt
        return time_since_attempt > timedelta(minutes=5)


class CacheWarmingManager:
    """Manages intelligent cache warming based on access patterns and predictions."""
    
    def __init__(
        self,
        cache_manager: CacheManager,
        github_client: Optional[AsyncGitHubClient] = None,
        max_warming_tasks: int = 100,
        warming_batch_size: int = 5
    ):
        """Initialize cache warming manager.
        
        Args:
            cache_manager: Cache manager instance
            github_client: Optional async GitHub client for preloading
            max_warming_tasks: Maximum number of warming tasks to queue
            warming_batch_size: Number of files to warm in parallel
        """
        self.cache_manager = cache_manager
        self.github_client = github_client
        self.max_warming_tasks = max_warming_tasks
        self.warming_batch_size = warming_batch_size
        
        # Access pattern tracking
        self.access_patterns: Dict[str, AccessPattern] = {}
        self.pattern_lock = asyncio.Lock()
        
        # Warming task management
        self.warming_queue = asyncio.PriorityQueue()
        self.active_warming_tasks: Set[str] = set()
        self.warming_stats = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'files_warmed': 0,
            'cache_hits_from_warming': 0,
            'total_warming_time': 0.0
        }
        
        # Background tasks
        self.warming_worker_task: Optional[asyncio.Task] = None
        self.pattern_analysis_task: Optional[asyncio.Task] = None
        self._shutdown_event = asyncio.Event()
        
        # Common file patterns for different project types
        self.common_file_patterns = {
            'javascript': [
                'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                'bun.lockb', '.nvmrc', 'tsconfig.json'
            ],
            'python': [
                'requirements.txt', 'Pipfile.lock', 'poetry.lock', 'pyproject.toml',
                'setup.py', 'setup.cfg', 'requirements-dev.txt'
            ],
            'ruby': ['Gemfile.lock', 'Gemfile', '.ruby-version'],
            'php': ['composer.lock', 'composer.json'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.lock', 'Cargo.toml'],
            'general': ['README.md', 'LICENSE', '.gitignore', 'Dockerfile']
        }
    
    async def start(self):
        """Start cache warming background tasks."""
        if self.warming_worker_task is None or self.warming_worker_task.done():
            self._shutdown_event.clear()
            self.warming_worker_task = asyncio.create_task(self._warming_worker())
            self.pattern_analysis_task = asyncio.create_task(self._pattern_analysis_worker())
            logger.info("Started cache warming background tasks")
    
    async def stop(self):
        """Stop cache warming background tasks."""
        self._shutdown_event.set()
        
        if self.warming_worker_task and not self.warming_worker_task.done():
            self.warming_worker_task.cancel()
            try:
                await self.warming_worker_task
            except asyncio.CancelledError:
                pass
        
        if self.pattern_analysis_task and not self.pattern_analysis_task.done():
            self.pattern_analysis_task.cancel()
            try:
                await self.pattern_analysis_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Stopped cache warming background tasks")
    
    async def record_file_access(self, repository: Repository, file_path: str):
        """Record access to a file for pattern analysis.
        
        Args:
            repository: Repository containing the file
            file_path: Path to the accessed file
        """
        pattern_key = f"{repository.full_name}:{file_path}"
        
        async with self.pattern_lock:
            if pattern_key not in self.access_patterns:
                self.access_patterns[pattern_key] = AccessPattern(
                    file_path=file_path,
                    repository=repository.full_name
                )
            
            self.access_patterns[pattern_key].record_access()
            
            # Queue for warming if it meets criteria
            pattern = self.access_patterns[pattern_key]
            if pattern.warming_priority > 0.5:  # High priority threshold
                await self._queue_warming_task(repository, file_path, pattern.warming_priority)
    
    async def warm_repository_files(
        self,
        repository: Repository,
        file_paths: Optional[List[str]] = None,
        priority: float = 0.5
    ) -> int:
        """Warm cache for specific repository files.
        
        Args:
            repository: Repository to warm files for
            file_paths: Optional list of specific files to warm
            priority: Priority for warming tasks
            
        Returns:
            Number of warming tasks queued
        """
        if file_paths is None:
            file_paths = await self._predict_important_files(repository)
        
        queued_count = 0
        for file_path in file_paths:
            if await self._queue_warming_task(repository, file_path, priority):
                queued_count += 1
        
        logger.info(f"Queued {queued_count} files for warming in {repository.full_name}")
        return queued_count
    
    async def warm_organization_files(
        self,
        repositories: List[Repository],
        common_files_only: bool = True
    ) -> int:
        """Warm cache for common files across an organization.
        
        Args:
            repositories: List of repositories to warm
            common_files_only: Whether to only warm common package manager files
            
        Returns:
            Number of warming tasks queued
        """
        total_queued = 0
        
        for repo in repositories:
            if common_files_only:
                # Detect project type and warm relevant files
                project_type = await self._detect_project_type(repo)
                file_paths = self.common_file_patterns.get(project_type, [])
                file_paths.extend(self.common_file_patterns['general'])
            else:
                file_paths = await self._predict_important_files(repo)
            
            queued = await self.warm_repository_files(repo, file_paths, priority=0.3)
            total_queued += queued
        
        logger.info(f"Queued {total_queued} files for warming across {len(repositories)} repositories")
        return total_queued
    
    async def _queue_warming_task(
        self,
        repository: Repository,
        file_path: str,
        priority: float
    ) -> bool:
        """Queue a warming task if not already active.
        
        Args:
            repository: Repository containing the file
            file_path: Path to the file
            priority: Priority for the warming task
            
        Returns:
            True if task was queued, False if already active or queue full
        """
        task_key = f"{repository.full_name}:{file_path}"
        
        # Check if already active or queued
        if task_key in self.active_warming_tasks:
            return False
        
        # Check if queue is full
        if self.warming_queue.qsize() >= self.max_warming_tasks:
            logger.debug("Warming queue is full, skipping task")
            return False
        
        # Create warming task (negative priority for max-heap behavior)
        task = WarmingTask(
            repository=repository,
            file_path=file_path,
            priority=priority
        )
        
        try:
            await self.warming_queue.put((-priority, task_key, task))
            self.active_warming_tasks.add(task_key)
            logger.debug(f"Queued warming task for {task_key} with priority {priority}")
            return True
        except Exception as e:
            logger.warning(f"Failed to queue warming task for {task_key}: {e}")
            return False
    
    async def _warming_worker(self):
        """Background worker that processes warming tasks."""
        logger.debug("Cache warming worker started")
        
        try:
            while not self._shutdown_event.is_set():
                try:
                    # Wait for warming tasks with timeout
                    priority, task_key, task = await asyncio.wait_for(
                        self.warming_queue.get(),
                        timeout=5.0
                    )
                    
                    # Process the warming task
                    await self._process_warming_task(task)
                    
                    # Remove from active tasks
                    self.active_warming_tasks.discard(task_key)
                    
                except asyncio.TimeoutError:
                    # No tasks available, continue waiting
                    continue
                except Exception as e:
                    logger.warning(f"Error in warming worker: {e}")
                    await asyncio.sleep(1.0)
        
        except asyncio.CancelledError:
            logger.debug("Cache warming worker cancelled")
            raise
        except Exception as e:
            logger.error(f"Cache warming worker failed: {e}")
    
    async def _process_warming_task(self, task: WarmingTask):
        """Process a single warming task.
        
        Args:
            task: Warming task to process
        """
        start_time = time.time()
        task.attempts += 1
        task.last_attempt = datetime.now(timezone.utc)
        
        try:
            # Check if already cached
            cached_content = self.cache_manager.get_file_content(
                task.repository.full_name,
                task.file_path,
                "latest"  # Placeholder SHA
            )
            
            if cached_content:
                logger.debug(f"File already cached, skipping: {task.file_path}")
                self.warming_stats['cache_hits_from_warming'] += 1
                return
            
            # If we have a GitHub client, pre-fetch the content
            if self.github_client:
                try:
                    content = await self.github_client.get_file_content_async(
                        task.repository,
                        task.file_path
                    )
                    
                    if content.data:
                        # Store in cache
                        self.cache_manager.store_file_content(
                            task.repository.full_name,
                            task.file_path,
                            content.data.sha,
                            content.data.content
                        )
                        
                        self.warming_stats['files_warmed'] += 1
                        logger.debug(f"Successfully warmed cache for {task.file_path}")
                    
                except Exception as e:
                    logger.debug(f"Failed to warm {task.file_path}: {e}")
                    self.warming_stats['tasks_failed'] += 1
                    
                    # Retry if appropriate
                    if task.should_retry:
                        await self._queue_warming_task(
                            task.repository,
                            task.file_path,
                            task.priority * 0.8  # Reduce priority on retry
                        )
            else:
                logger.debug(f"No GitHub client available for warming {task.file_path}")
            
            self.warming_stats['tasks_completed'] += 1
            
        except Exception as e:
            logger.warning(f"Error processing warming task for {task.file_path}: {e}")
            self.warming_stats['tasks_failed'] += 1
        
        finally:
            processing_time = time.time() - start_time
            self.warming_stats['total_warming_time'] += processing_time
    
    async def _pattern_analysis_worker(self):
        """Background worker that analyzes access patterns for predictive warming."""
        logger.debug("Pattern analysis worker started")
        
        try:
            while not self._shutdown_event.is_set():
                try:
                    # Run pattern analysis every 5 minutes
                    await asyncio.sleep(300)
                    
                    if self._shutdown_event.is_set():
                        break
                    
                    await self._analyze_patterns_and_predict()
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.warning(f"Error in pattern analysis worker: {e}")
                    await asyncio.sleep(60)  # Wait a minute on error
        
        except asyncio.CancelledError:
            logger.debug("Pattern analysis worker cancelled")
            raise
        except Exception as e:
            logger.error(f"Pattern analysis worker failed: {e}")
    
    async def _analyze_patterns_and_predict(self):
        """Analyze access patterns and predict files to warm."""
        async with self.pattern_lock:
            high_priority_patterns = []
            
            for pattern_key, pattern in self.access_patterns.items():
                if pattern.warming_priority > 0.7:  # Very high priority
                    high_priority_patterns.append((pattern_key, pattern))
            
            # Sort by priority
            high_priority_patterns.sort(key=lambda x: x[1].warming_priority, reverse=True)
            
            # Queue top patterns for warming
            for pattern_key, pattern in high_priority_patterns[:20]:  # Top 20
                repo_name, file_path = pattern_key.split(':', 1)
                
                # Create a minimal repository object for warming
                repo = Repository(
                    name=repo_name.split('/')[-1],
                    full_name=repo_name,
                    archived=False,
                    default_branch="main",
                    updated_at=datetime.now(timezone.utc)
                )
                
                await self._queue_warming_task(repo, file_path, pattern.warming_priority)
            
            logger.debug(f"Pattern analysis completed, found {len(high_priority_patterns)} high-priority patterns")
    
    async def _predict_important_files(self, repository: Repository) -> List[str]:
        """Predict important files for a repository based on patterns.
        
        Args:
            repository: Repository to predict files for
            
        Returns:
            List of predicted important file paths
        """
        # Start with common files
        project_type = await self._detect_project_type(repository)
        predicted_files = list(self.common_file_patterns.get(project_type, []))
        predicted_files.extend(self.common_file_patterns['general'])
        
        # Add files from access patterns
        repo_patterns = [
            pattern for pattern in self.access_patterns.values()
            if pattern.repository == repository.full_name
        ]
        
        # Sort by access count (simpler than warming priority for now)
        repo_patterns.sort(key=lambda p: p.access_count, reverse=True)
        for pattern in repo_patterns[:10]:  # Top 10 from patterns
            if pattern.file_path not in predicted_files and pattern.access_count > 0:
                predicted_files.append(pattern.file_path)
        
        return predicted_files
    
    async def _detect_project_type(self, repository: Repository) -> str:
        """Detect project type based on repository name and patterns.
        
        Args:
            repository: Repository to analyze
            
        Returns:
            Detected project type
        """
        repo_name = repository.name.lower()
        
        # Simple heuristics based on repository name
        if any(keyword in repo_name for keyword in ['js', 'node', 'react', 'vue', 'angular']):
            return 'javascript'
        elif any(keyword in repo_name for keyword in ['py', 'python', 'django', 'flask']):
            return 'python'
        elif any(keyword in repo_name for keyword in ['rb', 'ruby', 'rails']):
            return 'ruby'
        elif any(keyword in repo_name for keyword in ['php', 'laravel', 'symfony']):
            return 'php'
        elif any(keyword in repo_name for keyword in ['go', 'golang']):
            return 'go'
        elif any(keyword in repo_name for keyword in ['rs', 'rust']):
            return 'rust'
        
        # Check access patterns for this repository
        repo_patterns = [
            pattern for pattern in self.access_patterns.values()
            if pattern.repository == repository.full_name
        ]
        
        # Count file types in patterns
        type_counts = defaultdict(int)
        for pattern in repo_patterns:
            file_path = pattern.file_path.lower()
            if any(js_file in file_path for js_file in ['package.json', '.js', '.ts']):
                type_counts['javascript'] += 1
            elif any(py_file in file_path for py_file in ['requirements.txt', '.py', 'pyproject.toml']):
                type_counts['python'] += 1
            elif any(rb_file in file_path for rb_file in ['gemfile', '.rb']):
                type_counts['ruby'] += 1
            elif any(php_file in file_path for php_file in ['composer.json', '.php']):
                type_counts['php'] += 1
            elif any(go_file in file_path for go_file in ['go.mod', '.go']):
                type_counts['go'] += 1
            elif any(rs_file in file_path for rs_file in ['cargo.toml', '.rs']):
                type_counts['rust'] += 1
        
        if type_counts:
            return max(type_counts.items(), key=lambda x: x[1])[0]
        
        return 'general'
    
    def get_warming_statistics(self) -> Dict[str, Any]:
        """Get comprehensive cache warming statistics.
        
        Returns:
            Dictionary containing warming statistics
        """
        total_patterns = len(self.access_patterns)
        high_priority_patterns = sum(
            1 for p in self.access_patterns.values() 
            if p.warming_priority > 0.5
        )
        
        avg_warming_time = 0.0
        if self.warming_stats['tasks_completed'] > 0:
            avg_warming_time = (
                self.warming_stats['total_warming_time'] / 
                self.warming_stats['tasks_completed']
            )
        
        return {
            'total_access_patterns': total_patterns,
            'high_priority_patterns': high_priority_patterns,
            'warming_queue_size': self.warming_queue.qsize(),
            'active_warming_tasks': len(self.active_warming_tasks),
            'tasks_completed': self.warming_stats['tasks_completed'],
            'tasks_failed': self.warming_stats['tasks_failed'],
            'files_warmed': self.warming_stats['files_warmed'],
            'cache_hits_from_warming': self.warming_stats['cache_hits_from_warming'],
            'average_warming_time': avg_warming_time,
            'worker_active': (
                self.warming_worker_task is not None and 
                not self.warming_worker_task.done()
            ),
            'pattern_analysis_active': (
                self.pattern_analysis_task is not None and 
                not self.pattern_analysis_task.done()
            )
        }
    
    def reset_statistics(self):
        """Reset warming statistics."""
        self.warming_stats = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'files_warmed': 0,
            'cache_hits_from_warming': 0,
            'total_warming_time': 0.0
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.stop()