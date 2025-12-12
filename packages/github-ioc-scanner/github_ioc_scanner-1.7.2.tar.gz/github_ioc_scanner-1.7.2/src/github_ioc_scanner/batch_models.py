"""Core data models for batch processing operations."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from .models import Repository, FileContent, IOCMatch


class BatchStrategy(Enum):
    """Different batching strategies."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    ADAPTIVE = "adaptive"
    AGGRESSIVE = "aggressive"
    CONSERVATIVE = "conservative"


@dataclass
class BatchRequest:
    """Represents a single request in a batch."""
    repo: Repository
    file_path: str
    priority: int = 0
    estimated_size: int = 0
    cache_key: Optional[str] = None
    
    def __post_init__(self):
        """Generate cache key if not provided."""
        if self.cache_key is None:
            self.cache_key = f"{self.repo.full_name}:{self.file_path}"


@dataclass
class BatchResult:
    """Result of a batch request."""
    request: BatchRequest
    content: Optional[FileContent] = None
    error: Optional[Exception] = None
    from_cache: bool = False
    processing_time: float = 0.0
    
    @property
    def success(self) -> bool:
        """Whether the request was successful."""
        return self.error is None and self.content is not None


@dataclass
class RepositoryBatchResult:
    """Result of processing a repository in batch mode."""
    repository_name: str
    ioc_matches: List[IOCMatch] = field(default_factory=list)
    files_analyzed: int = 0
    files_with_errors: int = 0
    processing_time: float = 0.0


@dataclass
class CrossRepoBatch:
    """Represents a cross-repository batch opportunity."""
    repositories: List[Repository]
    common_files: List[str]
    estimated_savings: float


@dataclass
class BatchMetrics:
    """Performance metrics for batch operations."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    average_batch_size: float = 0.0
    total_processing_time: float = 0.0
    api_calls_saved: int = 0
    parallel_efficiency: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def __post_init__(self):
        """Initialize start time if not provided."""
        if self.start_time is None:
            self.start_time = datetime.now()
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as a percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate as a percentage."""
        total_cache_requests = self.cache_hits + self.cache_misses
        if total_cache_requests == 0:
            return 0.0
        return (self.cache_hits / total_cache_requests) * 100
    
    @property
    def duration_seconds(self) -> float:
        """Calculate total duration in seconds."""
        if self.start_time is None:
            return 0.0
        end = self.end_time or datetime.now()
        return (end - self.start_time).total_seconds()
    
    def finish(self):
        """Mark the batch operation as finished."""
        self.end_time = datetime.now()
    
    def add_result(self, result: BatchResult):
        """Add a batch result to the metrics."""
        self.total_requests += 1
        if result.success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        
        if result.from_cache:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        
        self.total_processing_time += result.processing_time


@dataclass
class NetworkConditions:
    """Current network conditions affecting batch performance."""
    latency_ms: float = 0.0
    bandwidth_mbps: float = 0.0
    error_rate: float = 0.0
    
    @property
    def is_good(self) -> bool:
        """Whether network conditions are good for aggressive batching."""
        return (
            self.latency_ms < 200 and
            self.bandwidth_mbps > 10 and
            self.error_rate < 0.05
        )


@dataclass
class PrioritizedFile:
    """File with priority information."""
    path: str
    priority: int
    file_type: str
    estimated_size: int
    security_importance: float = 1.0
    
    def __post_init__(self):
        """Calculate priority based on file type and security importance."""
        # Only set default priority if not already set (priority == 0)
        if self.priority == 0:
            # High priority files (package managers)
            high_priority_files = {
                'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                'requirements.txt', 'Pipfile.lock', 'poetry.lock', 'pyproject.toml',
                'Gemfile.lock', 'composer.lock', 'go.mod', 'go.sum', 'Cargo.lock'
            }
            
            filename = self.path.split('/')[-1]
            if filename in high_priority_files:
                self.priority = 10
                self.security_importance = max(self.security_importance, 2.0)
            else:
                self.priority = 1  # Default priority for other files


@dataclass
class BatchConfig:
    """Configuration for batch processing."""
    
    # Concurrency settings - maximized for speed (not local resource conservation)
    max_concurrent_requests: int = 50  # Significantly increased for maximum throughput
    max_concurrent_repos: int = 15     # Increased for maximum parallel processing
    
    # Batch size settings - optimized for maximum speed
    default_batch_size: int = 25      # Increased from 10 for better throughput
    max_batch_size: int = 100         # Increased from 50 for maximum speed
    min_batch_size: int = 5           # Increased from 1 to maintain efficiency
    
    # Performance settings - optimized for maximum speed
    rate_limit_buffer: float = 0.95  # Use 95% of available rate limit (very aggressive)
    retry_attempts: int = 5          # More retries for resilience at high speed
    retry_delay_base: float = 0.5    # Faster retries for maximum speed
    
    # Rate limiting settings - optimized for speed over safety
    enable_proactive_rate_limiting: bool = True
    rate_limit_safety_margin: int = 20   # Minimal safety margin for maximum speed
    adaptive_delay_enabled: bool = True
    
    # Intelligent rate limiting settings
    rate_limit_strategy: str = "normal"  # Options: conservative, normal, aggressive
    enable_budget_distribution: bool = True
    enable_adaptive_timing: bool = True
    budget_redistribution_interval: int = 300  # Seconds between budget redistributions
    
    # Memory settings
    max_memory_usage_mb: int = 500
    stream_large_files_threshold: int = 1024 * 1024  # 1MB
    
    # Strategy settings
    default_strategy: BatchStrategy = BatchStrategy.ADAPTIVE
    enable_cross_repo_batching: bool = True
    enable_file_prioritization: bool = True
    
    # Monitoring settings
    enable_performance_monitoring: bool = True
    log_batch_metrics: bool = False
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        if self.max_concurrent_requests < 1:
            errors.append("max_concurrent_requests must be at least 1")
        
        if self.max_concurrent_repos < 1:
            errors.append("max_concurrent_repos must be at least 1")
        
        if self.min_batch_size < 1:
            errors.append("min_batch_size must be at least 1")
        
        if self.max_batch_size < self.min_batch_size:
            errors.append("max_batch_size must be >= min_batch_size")
        
        if not 0.1 <= self.rate_limit_buffer <= 1.0:
            errors.append("rate_limit_buffer must be between 0.1 and 1.0")
        
        if self.retry_attempts < 0:
            errors.append("retry_attempts must be non-negative")
        
        return errors


@dataclass
class BatchRecoveryPlan:
    """Plan for recovering from batch failures."""
    retry_requests: List[BatchRequest] = field(default_factory=list)
    skip_requests: List[BatchRequest] = field(default_factory=list)
    fallback_strategy: Optional[BatchStrategy] = None
    delay_seconds: float = 0.0
    
    @property
    def has_retries(self) -> bool:
        """Whether there are requests to retry."""
        return len(self.retry_requests) > 0
    
    @property
    def total_requests(self) -> int:
        """Total number of requests in the recovery plan."""
        return len(self.retry_requests) + len(self.skip_requests)


@dataclass
class AsyncBatchContext:
    """Context for async batch operations."""
    semaphore: asyncio.Semaphore
    session: Optional[Any] = None  # Will be httpx.AsyncClient
    rate_limit_remaining: int = 5000
    rate_limit_reset: int = 0
    current_strategy: BatchStrategy = BatchStrategy.ADAPTIVE
    
    def __post_init__(self):
        """Initialize semaphore if not provided."""
        if not hasattr(self, 'semaphore') or self.semaphore is None:
            self.semaphore = asyncio.Semaphore(10)  # Default concurrency