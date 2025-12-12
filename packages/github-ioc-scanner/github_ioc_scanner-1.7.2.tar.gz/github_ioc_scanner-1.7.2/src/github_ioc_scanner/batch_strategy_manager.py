"""Batch strategy manager for intelligent batching decisions."""

import math
from typing import Dict, List, Optional, Tuple

from .batch_models import (
    BatchConfig,
    BatchMetrics,
    BatchRequest,
    BatchStrategy,
    CrossRepoBatch,
    NetworkConditions,
    PrioritizedFile,
)
from .models import Repository


class BatchStrategyManager:
    """Manages intelligent batching strategies and optimizations."""
    
    def __init__(self, config: Optional[BatchConfig] = None):
        """Initialize the batch strategy manager.
        
        Args:
            config: Batch configuration settings
        """
        self.config = config or BatchConfig()
        self._performance_history: List[BatchMetrics] = []
        self._file_type_priorities = self._initialize_file_priorities()
    
    def calculate_optimal_batch_size(
        self,
        files: List[str],
        file_sizes: Dict[str, int],
        rate_limit_remaining: int,
        network_conditions: Optional[NetworkConditions] = None
    ) -> int:
        """Calculate optimal batch size based on multiple factors.
        
        Args:
            files: List of file paths to batch
            file_sizes: Dictionary mapping file paths to their sizes in bytes
            rate_limit_remaining: Number of API calls remaining
            network_conditions: Current network conditions
            
        Returns:
            Optimal batch size for the given conditions
        """
        if not files:
            return 0
        
        # Start with base batch size
        base_size = self.config.default_batch_size
        
        # Calculate file size factor
        total_size = sum(file_sizes.get(f, 0) for f in files)
        avg_size = total_size / len(files) if files else 0
        
        # Adjust for file sizes (smaller batches for larger files)
        size_factor = self._calculate_size_factor(avg_size)
        
        # Adjust for rate limits
        rate_limit_factor = self._calculate_rate_limit_factor(rate_limit_remaining)
        
        # Adjust for network conditions
        network_factor = self._calculate_network_factor(network_conditions)
        
        # Adjust based on performance history
        performance_factor = self._calculate_performance_factor()
        
        # Calculate optimal size
        optimal_size = int(
            base_size * 
            size_factor * 
            rate_limit_factor * 
            network_factor * 
            performance_factor
        )
        
        # Clamp to configured limits
        return max(
            self.config.min_batch_size,
            min(self.config.max_batch_size, optimal_size)
        )
    
    def prioritize_files(self, files: List[str]) -> List[PrioritizedFile]:
        """Prioritize files based on security importance and file type.
        
        Args:
            files: List of file paths to prioritize
            
        Returns:
            List of prioritized files sorted by priority (highest first)
        """
        prioritized = []
        
        for file_path in files:
            filename = file_path.split('/')[-1].lower()
            file_type = self._determine_file_type(filename)
            
            # Get base priority from file type
            base_priority = self._file_type_priorities.get(file_type, 1)
            
            # Calculate security importance
            security_importance = self._calculate_security_importance(filename, file_type)
            
            # Estimate file size (rough estimate based on file type)
            estimated_size = self._estimate_file_size(file_type)
            
            prioritized_file = PrioritizedFile(
                path=file_path,
                priority=base_priority,
                file_type=file_type,
                estimated_size=estimated_size,
                security_importance=security_importance
            )
            
            prioritized.append(prioritized_file)
        
        # Sort by priority (highest first), then by security importance
        prioritized.sort(
            key=lambda f: (f.priority, f.security_importance),
            reverse=True
        )
        
        return prioritized
    
    def identify_cross_repo_opportunities(
        self, 
        repositories: List[Repository],
        repo_files: Dict[str, List[str]]
    ) -> List[CrossRepoBatch]:
        """Identify opportunities for cross-repository batching.
        
        Args:
            repositories: List of repositories to analyze
            repo_files: Dictionary mapping repo names to their file lists
            
        Returns:
            List of cross-repository batching opportunities
        """
        if not self.config.enable_cross_repo_batching or len(repositories) < 2:
            return []
        
        opportunities = []
        
        # Find common files across repositories
        common_files_map = self._find_common_files(repo_files)
        
        # Group repositories by common files
        for common_files, repo_names in common_files_map.items():
            if len(repo_names) < 2:
                continue
            
            # Get repository objects
            batch_repos = [r for r in repositories if r.full_name in repo_names]
            
            if len(batch_repos) < 2:
                continue
            
            # Calculate estimated savings
            estimated_savings = self._calculate_cross_repo_savings(
                batch_repos, 
                list(common_files)
            )
            
            # Only include if savings are significant
            if estimated_savings > 0.2:  # At least 20% savings
                opportunity = CrossRepoBatch(
                    repositories=batch_repos,
                    common_files=list(common_files),
                    estimated_savings=estimated_savings
                )
                opportunities.append(opportunity)
        
        # Sort by estimated savings (highest first)
        opportunities.sort(key=lambda o: o.estimated_savings, reverse=True)
        
        return opportunities
    
    def select_strategy(
        self,
        repositories: List[Repository],
        total_files: int,
        rate_limit_remaining: int,
        network_conditions: Optional[NetworkConditions] = None
    ) -> BatchStrategy:
        """Select optimal batching strategy based on scan characteristics.
        
        Args:
            repositories: List of repositories to scan
            total_files: Total number of files to process
            rate_limit_remaining: Number of API calls remaining
            network_conditions: Current network conditions
            
        Returns:
            Recommended batching strategy
        """
        # Start with configured default strategy
        if self.config.default_strategy != BatchStrategy.ADAPTIVE:
            return self.config.default_strategy
        
        # Analyze scan characteristics
        repo_count = len(repositories)
        
        # Conservative strategy for limited resources
        if rate_limit_remaining < 200 or (network_conditions and not network_conditions.is_good):
            return BatchStrategy.CONSERVATIVE
        
        # Sequential strategy for small scans
        if repo_count == 1 and total_files < 5:
            return BatchStrategy.SEQUENTIAL
        
        # Aggressive strategy for large scans with good conditions
        if (repo_count > 10 or total_files > 100) and rate_limit_remaining > 2000:
            if network_conditions is None or network_conditions.is_good:
                return BatchStrategy.AGGRESSIVE
        
        # Parallel strategy for medium scans
        if repo_count > 1 or total_files > 10:
            return BatchStrategy.PARALLEL
        
        # Default to adaptive for other cases
        return BatchStrategy.ADAPTIVE
    
    def adapt_strategy(self, performance_metrics: BatchMetrics) -> BatchStrategy:
        """Adapt batching strategy based on performance data.
        
        Args:
            performance_metrics: Recent performance metrics
            
        Returns:
            Recommended batching strategy
        """
        # Store performance history
        self._performance_history.append(performance_metrics)
        
        # Keep only recent history (last 10 batches)
        if len(self._performance_history) > 10:
            self._performance_history = self._performance_history[-10:]
        
        # Analyze current performance
        success_rate = performance_metrics.success_rate
        parallel_efficiency = performance_metrics.parallel_efficiency
        cache_hit_rate = performance_metrics.cache_hit_rate
        
        # Analyze performance trends if we have history
        trend_analysis = self._analyze_performance_trends()
        
        # Decision matrix based on multiple factors
        strategy_scores = {
            BatchStrategy.CONSERVATIVE: 0,
            BatchStrategy.SEQUENTIAL: 0,
            BatchStrategy.PARALLEL: 0,
            BatchStrategy.AGGRESSIVE: 0,
            BatchStrategy.ADAPTIVE: 0
        }
        
        # Score based on success rate
        if success_rate < 70:
            strategy_scores[BatchStrategy.CONSERVATIVE] += 3
            strategy_scores[BatchStrategy.SEQUENTIAL] += 2
        elif success_rate < 85:
            strategy_scores[BatchStrategy.CONSERVATIVE] += 1
            strategy_scores[BatchStrategy.PARALLEL] += 1
        elif success_rate > 95:
            strategy_scores[BatchStrategy.AGGRESSIVE] += 2
            strategy_scores[BatchStrategy.PARALLEL] += 1
        
        # Score based on parallel efficiency
        if parallel_efficiency > 0.8:
            strategy_scores[BatchStrategy.AGGRESSIVE] += 2
            strategy_scores[BatchStrategy.PARALLEL] += 1
        elif parallel_efficiency > 0.6:
            strategy_scores[BatchStrategy.PARALLEL] += 2
            strategy_scores[BatchStrategy.ADAPTIVE] += 1
        elif parallel_efficiency < 0.3:
            strategy_scores[BatchStrategy.SEQUENTIAL] += 2
            strategy_scores[BatchStrategy.CONSERVATIVE] += 1
        
        # Score based on cache hit rate
        if cache_hit_rate > 80:
            # High cache hit rate allows for more aggressive strategies
            strategy_scores[BatchStrategy.AGGRESSIVE] += 1
            strategy_scores[BatchStrategy.PARALLEL] += 1
        elif cache_hit_rate < 20:
            # Low cache hit rate suggests network-heavy operations
            strategy_scores[BatchStrategy.CONSERVATIVE] += 1
        
        # Score based on performance trends
        if trend_analysis['improving']:
            strategy_scores[BatchStrategy.AGGRESSIVE] += 1
            strategy_scores[BatchStrategy.PARALLEL] += 1
        elif trend_analysis['degrading']:
            strategy_scores[BatchStrategy.CONSERVATIVE] += 2
            strategy_scores[BatchStrategy.SEQUENTIAL] += 1
        
        # Score based on error patterns
        if trend_analysis['high_error_rate']:
            strategy_scores[BatchStrategy.CONSERVATIVE] += 2
            strategy_scores[BatchStrategy.SEQUENTIAL] += 1
        
        # Always give adaptive strategy a base score
        strategy_scores[BatchStrategy.ADAPTIVE] += 1
        
        # Select strategy with highest score
        best_strategy = max(strategy_scores.items(), key=lambda x: x[1])[0]
        
        return best_strategy
    
    def adapt_strategy_runtime(
        self,
        current_strategy: BatchStrategy,
        current_metrics: BatchMetrics,
        rate_limit_remaining: int,
        error_count: int
    ) -> BatchStrategy:
        """Adapt strategy during runtime based on immediate feedback.
        
        Args:
            current_strategy: Currently active strategy
            current_metrics: Real-time performance metrics
            rate_limit_remaining: Current rate limit remaining
            error_count: Number of recent errors
            
        Returns:
            Adapted strategy for immediate use
        """
        # Emergency fallback conditions
        if error_count > 5:
            return BatchStrategy.CONSERVATIVE
        
        if rate_limit_remaining < 50:
            return BatchStrategy.CONSERVATIVE
        
        # Quick adaptation based on immediate performance
        success_rate = current_metrics.success_rate
        
        # If current strategy is failing, step down
        if success_rate < 60:
            if current_strategy == BatchStrategy.AGGRESSIVE:
                return BatchStrategy.PARALLEL
            elif current_strategy == BatchStrategy.PARALLEL:
                return BatchStrategy.CONSERVATIVE
            elif current_strategy == BatchStrategy.ADAPTIVE:
                return BatchStrategy.CONSERVATIVE
        
        # If current strategy is working well, consider stepping up
        elif success_rate > 95 and rate_limit_remaining > 1000:
            if current_strategy == BatchStrategy.CONSERVATIVE:
                return BatchStrategy.PARALLEL
            elif current_strategy == BatchStrategy.PARALLEL:
                return BatchStrategy.AGGRESSIVE
        
        # No change needed
        return current_strategy
    
    def get_strategy_config(self, strategy: BatchStrategy) -> Dict[str, any]:
        """Get configuration parameters for a specific strategy.
        
        Args:
            strategy: The batching strategy
            
        Returns:
            Dictionary of configuration parameters for the strategy
        """
        base_config = {
            'max_concurrent_requests': self.config.max_concurrent_requests,
            'max_concurrent_repos': self.config.max_concurrent_repos,
            'default_batch_size': self.config.default_batch_size,
            'max_batch_size': self.config.max_batch_size,
            'retry_attempts': self.config.retry_attempts,
            'rate_limit_buffer': self.config.rate_limit_buffer
        }
        
        # Adjust configuration based on strategy
        if strategy == BatchStrategy.CONSERVATIVE:
            base_config.update({
                'max_concurrent_requests': min(3, self.config.max_concurrent_requests),
                'max_concurrent_repos': 1,
                'default_batch_size': max(1, self.config.default_batch_size // 2),
                'max_batch_size': min(10, self.config.max_batch_size),
                'retry_attempts': self.config.retry_attempts + 2,
                'rate_limit_buffer': max(0.5, self.config.rate_limit_buffer - 0.2)
            })
        
        elif strategy == BatchStrategy.SEQUENTIAL:
            base_config.update({
                'max_concurrent_requests': 1,
                'max_concurrent_repos': 1,
                'default_batch_size': 1,
                'max_batch_size': 1,
                'retry_attempts': self.config.retry_attempts + 1
            })
        
        elif strategy == BatchStrategy.AGGRESSIVE:
            base_config.update({
                'max_concurrent_requests': min(50, self.config.max_concurrent_requests * 2),
                'max_concurrent_repos': min(10, self.config.max_concurrent_repos * 2),
                'default_batch_size': min(self.config.max_batch_size, self.config.default_batch_size * 2),
                'max_batch_size': min(100, self.config.max_batch_size * 2),
                'retry_attempts': max(1, self.config.retry_attempts - 1),
                'rate_limit_buffer': min(0.95, self.config.rate_limit_buffer + 0.1)
            })
        
        elif strategy == BatchStrategy.PARALLEL:
            base_config.update({
                'max_concurrent_requests': self.config.max_concurrent_requests,
                'max_concurrent_repos': self.config.max_concurrent_repos,
                'default_batch_size': self.config.default_batch_size,
                'max_batch_size': self.config.max_batch_size
            })
        
        # ADAPTIVE strategy uses base config as-is
        
        return base_config
    
    def _analyze_performance_trends(self) -> Dict[str, bool]:
        """Analyze performance trends from history.
        
        Returns:
            Dictionary with trend analysis results
        """
        if len(self._performance_history) < 3:
            return {
                'improving': False,
                'degrading': False,
                'stable': True,
                'high_error_rate': False
            }
        
        recent_metrics = self._performance_history[-3:]
        
        # Analyze success rate trend
        success_rates = [m.success_rate for m in recent_metrics]
        success_improving = all(
            success_rates[i] <= success_rates[i + 1] 
            for i in range(len(success_rates) - 1)
        )
        success_degrading = all(
            success_rates[i] >= success_rates[i + 1] 
            for i in range(len(success_rates) - 1)
        )
        
        # Analyze efficiency trend
        efficiencies = [m.parallel_efficiency for m in recent_metrics]
        efficiency_improving = all(
            efficiencies[i] <= efficiencies[i + 1] 
            for i in range(len(efficiencies) - 1)
        )
        efficiency_degrading = all(
            efficiencies[i] >= efficiencies[i + 1] 
            for i in range(len(efficiencies) - 1)
        )
        
        # Check for high error rate
        avg_success_rate = sum(success_rates) / len(success_rates)
        high_error_rate = avg_success_rate < 75
        
        return {
            'improving': success_improving and efficiency_improving,
            'degrading': success_degrading or efficiency_degrading,
            'stable': not (success_improving or success_degrading or efficiency_improving or efficiency_degrading),
            'high_error_rate': high_error_rate
        }
    
    def _initialize_file_priorities(self) -> Dict[str, int]:
        """Initialize file type priorities."""
        return {
            # Package manager files (highest priority)
            'package.json': 10,
            'package-lock.json': 9,
            'yarn.lock': 9,
            'pnpm-lock.yaml': 9,
            'bun.lockb': 9,
            'requirements.txt': 10,
            'pipfile.lock': 9,
            'poetry.lock': 9,
            'pyproject.toml': 8,
            'gemfile.lock': 9,
            'composer.lock': 9,
            'go.mod': 10,
            'go.sum': 9,
            'cargo.lock': 9,
            
            # Configuration files (medium priority)
            'dockerfile': 6,
            'docker-compose.yml': 6,
            'makefile': 5,
            '.env': 7,
            'config.json': 5,
            
            # Source code files (lower priority)
            'python': 3,
            'javascript': 3,
            'typescript': 3,
            'go': 3,
            'rust': 3,
            'ruby': 3,
            'php': 3,
            
            # Other files (lowest priority)
            'text': 1,
            'markdown': 1,
            'unknown': 1,
        }
    
    def _calculate_size_factor(self, avg_size: float) -> float:
        """Calculate batch size adjustment factor based on file sizes."""
        if avg_size == 0:
            return 1.0
        
        # Smaller batches for larger files
        # Files > 1MB: reduce batch size significantly
        # Files > 100KB: reduce batch size moderately
        # Files < 10KB: can use larger batches
        
        if avg_size > 1024 * 1024:  # > 1MB
            return 0.3
        elif avg_size > 100 * 1024:  # > 100KB
            return 0.6
        elif avg_size > 10 * 1024:  # > 10KB
            return 0.8
        else:  # <= 10KB
            return 1.2
    
    def _calculate_rate_limit_factor(self, rate_limit_remaining: int) -> float:
        """Calculate batch size adjustment factor based on rate limits.
        
        Optimized for maximum speed - only reduce batch size when absolutely necessary.
        """
        # Only reduce batch size when rate limits are critically low
        if rate_limit_remaining < 50:
            return 0.7  # Still aggressive - only 30% reduction when critically low
        elif rate_limit_remaining < 200:
            return 0.85  # Minimal reduction - only 15% when low
        elif rate_limit_remaining < 500:
            return 0.95  # Tiny reduction - only 5% when moderate
        else:
            return 1.2  # Actually INCREASE batch size when we have plenty of rate limit
    
    def _calculate_network_factor(
        self, 
        network_conditions: Optional[NetworkConditions]
    ) -> float:
        """Calculate batch size adjustment factor based on network conditions.
        
        Optimized for maximum speed - assume good network and push harder.
        """
        if network_conditions is None:
            return 1.3  # Assume good network and be aggressive
        
        # Good network conditions allow much larger batches
        if network_conditions.is_good:
            return 1.5  # Very aggressive with good network
        
        # Even with poor conditions, stay more aggressive for speed
        if network_conditions.error_rate > 0.2:  # Only reduce for very high error rates
            return 0.8
        elif network_conditions.latency_ms > 1000:  # Only reduce for very high latency
            return 0.9
        elif network_conditions.bandwidth_mbps < 2:  # Only reduce for very low bandwidth
            return 0.9
        else:
            return 1.2  # Still aggressive for moderate conditions
    
    def _calculate_performance_factor(self) -> float:
        """Calculate batch size adjustment factor based on performance history.
        
        Optimized for maximum speed - push harder when performing well.
        """
        if not self._performance_history:
            return 1.2  # Start aggressive without history
        
        # Calculate average success rate from recent history
        recent_metrics = self._performance_history[-5:]  # Look at more history for stability
        avg_success_rate = sum(m.success_rate for m in recent_metrics) / len(recent_metrics)
        
        # Be more aggressive with good performance
        if avg_success_rate > 98:
            return 1.4  # Very aggressive increase for excellent performance
        elif avg_success_rate > 90:
            return 1.2  # Aggressive increase for good performance
        elif avg_success_rate > 75:
            return 1.0  # Maintain size for acceptable performance
        else:
            return 0.9  # Only small reduction for poor performance
    
    def _determine_file_type(self, filename: str) -> str:
        """Determine file type from filename."""
        filename = filename.lower()
        
        # Package manager files
        if filename in ['package.json', 'package-lock.json', 'yarn.lock', 
                       'pnpm-lock.yaml', 'bun.lockb']:
            return filename
        elif filename in ['requirements.txt', 'pipfile.lock', 'poetry.lock', 
                         'pyproject.toml']:
            return filename
        elif filename in ['gemfile.lock', 'composer.lock', 'go.mod', 'go.sum', 
                         'cargo.lock']:
            return filename
        
        # File extensions
        elif filename.endswith(('.py', '.pyw')):
            return 'python'
        elif filename.endswith(('.js', '.jsx', '.mjs')):
            return 'javascript'
        elif filename.endswith(('.ts', '.tsx')):
            return 'typescript'
        elif filename.endswith('.go'):
            return 'go'
        elif filename.endswith('.rs'):
            return 'rust'
        elif filename.endswith('.rb'):
            return 'ruby'
        elif filename.endswith('.php'):
            return 'php'
        elif filename.endswith(('.md', '.markdown')):
            return 'markdown'
        elif filename.endswith(('.txt', '.log')):
            return 'text'
        elif filename in ['dockerfile', 'makefile']:
            return filename
        elif filename.endswith(('.yml', '.yaml')):
            if 'docker-compose' in filename:
                return 'docker-compose.yml'
            return 'yaml'
        elif filename.endswith('.json'):
            if 'config' in filename:
                return 'config.json'
            return 'json'
        else:
            return 'unknown'
    
    def _calculate_security_importance(self, filename: str, file_type: str) -> float:
        """Calculate security importance score for a file."""
        # Package manager files have highest security importance
        high_security_files = {
            'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
            'requirements.txt', 'pipfile.lock', 'poetry.lock', 'pyproject.toml',
            'gemfile.lock', 'composer.lock', 'go.mod', 'go.sum', 'cargo.lock'
        }
        
        if file_type in high_security_files:
            return 3.0
        
        # Configuration files have medium security importance
        config_files = {'dockerfile', 'docker-compose.yml', '.env', 'config.json'}
        if file_type in config_files or '.env' in filename:
            return 2.0
        
        # Source code files have lower security importance
        source_files = {'python', 'javascript', 'typescript', 'go', 'rust', 'ruby', 'php'}
        if file_type in source_files:
            return 1.5
        
        # Other files have minimal security importance
        return 1.0
    
    def _estimate_file_size(self, file_type: str) -> int:
        """Estimate file size based on file type."""
        # Rough estimates in bytes
        size_estimates = {
            # Package manager files (usually small to medium)
            'package.json': 2048,
            'package-lock.json': 50000,
            'yarn.lock': 30000,
            'pnpm-lock.yaml': 25000,
            'requirements.txt': 1024,
            'pipfile.lock': 20000,
            'poetry.lock': 25000,
            'pyproject.toml': 2048,
            'gemfile.lock': 15000,
            'composer.lock': 20000,
            'go.mod': 1024,
            'go.sum': 10000,
            'cargo.lock': 30000,
            
            # Source code files (variable, use conservative estimate)
            'python': 5000,
            'javascript': 4000,
            'typescript': 4000,
            'go': 3000,
            'rust': 4000,
            'ruby': 3000,
            'php': 3000,
            
            # Configuration files
            'dockerfile': 1024,
            'docker-compose.yml': 2048,
            'config.json': 1024,
            
            # Other files
            'markdown': 2000,
            'text': 1000,
            'unknown': 2000,
        }
        
        return size_estimates.get(file_type, 2000)
    
    def _find_common_files(
        self, 
        repo_files: Dict[str, List[str]]
    ) -> Dict[Tuple[str, ...], List[str]]:
        """Find common files across repositories.
        
        Returns:
            Dictionary mapping common file tuples to repository names
        """
        if len(repo_files) < 2:
            return {}
        
        # Extract important files from each repository (normalize filenames)
        repo_important_files = {}
        for repo_name, files in repo_files.items():
            important_files = []
            for f in files:
                filename = f.split('/')[-1].lower()
                if self._is_important_file(filename):
                    important_files.append(filename)
            
            if important_files:
                repo_important_files[repo_name] = set(important_files)
        
        if len(repo_important_files) < 2:
            return {}
        
        # Find all possible combinations of common files
        common_file_groups = {}
        repo_names = list(repo_important_files.keys())
        
        # For each pair of repositories, find common files
        for i in range(len(repo_names)):
            for j in range(i + 1, len(repo_names)):
                repo1, repo2 = repo_names[i], repo_names[j]
                common_files = repo_important_files[repo1] & repo_important_files[repo2]
                
                if common_files:
                    # Check if other repos also have these files
                    repos_with_files = [repo1, repo2]
                    for k, other_repo in enumerate(repo_names):
                        if k != i and k != j:
                            if common_files.issubset(repo_important_files[other_repo]):
                                repos_with_files.append(other_repo)
                    
                    if len(repos_with_files) >= 2:
                        file_tuple = tuple(sorted(common_files))
                        if file_tuple not in common_file_groups or len(repos_with_files) > len(common_file_groups[file_tuple]):
                            common_file_groups[file_tuple] = repos_with_files
        
        # Also find individual file commonalities
        all_files = set()
        for files in repo_important_files.values():
            all_files.update(files)
        
        for file in all_files:
            repos_with_file = [
                repo for repo, files in repo_important_files.items()
                if file in files
            ]
            
            if len(repos_with_file) >= 2:
                file_tuple = (file,)
                if file_tuple not in common_file_groups or len(repos_with_file) > len(common_file_groups[file_tuple]):
                    common_file_groups[file_tuple] = repos_with_file
        
        return common_file_groups
    
    def _is_important_file(self, filename: str) -> bool:
        """Check if a file is important for cross-repo batching."""
        filename = filename.lower()
        
        important_files = {
            'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
            'requirements.txt', 'pipfile.lock', 'poetry.lock', 'pyproject.toml',
            'gemfile.lock', 'composer.lock', 'go.mod', 'go.sum', 'cargo.lock',
            'dockerfile', 'docker-compose.yml'
        }
        
        return filename in important_files
    
    def _calculate_cross_repo_savings(
        self, 
        repositories: List[Repository], 
        common_files: List[str]
    ) -> float:
        """Calculate estimated savings from cross-repository batching."""
        if len(repositories) < 2 or not common_files:
            return 0.0
        
        # Estimate savings based on:
        # 1. Number of repositories that can be batched together
        # 2. Number of common files
        # 3. Potential for request consolidation
        
        repo_count = len(repositories)
        file_count = len(common_files)
        
        # Base savings from batching multiple repos
        base_savings = min(0.5, (repo_count - 1) * 0.15)
        
        # Additional savings from common files
        file_savings = min(0.3, file_count * 0.05)
        
        # Bonus for high-priority files
        priority_bonus = 0.0
        for file_path in common_files:
            filename = file_path.split('/')[-1].lower()
            if self._is_important_file(filename):
                priority_bonus += 0.1
        
        priority_bonus = min(0.2, priority_bonus)
        
        total_savings = base_savings + file_savings + priority_bonus
        return min(0.79, total_savings)  # Cap just under 80% savings