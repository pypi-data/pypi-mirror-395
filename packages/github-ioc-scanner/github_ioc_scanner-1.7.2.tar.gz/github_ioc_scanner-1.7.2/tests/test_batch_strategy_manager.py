"""Tests for batch strategy manager."""

import pytest
from unittest.mock import Mock

from src.github_ioc_scanner.batch_strategy_manager import BatchStrategyManager
from src.github_ioc_scanner.batch_models import (
    BatchConfig,
    BatchMetrics,
    BatchStrategy,
    NetworkConditions,
    PrioritizedFile,
)
from src.github_ioc_scanner.models import Repository


class TestBatchStrategyManager:
    """Test batch strategy manager functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = BatchConfig(
            default_batch_size=10,
            min_batch_size=1,
            max_batch_size=50
        )
        self.manager = BatchStrategyManager(self.config)
    
    def test_initialization(self):
        """Test manager initialization."""
        assert self.manager.config == self.config
        assert len(self.manager._performance_history) == 0
        assert len(self.manager._file_type_priorities) > 0
    
    def test_initialization_with_default_config(self):
        """Test manager initialization with default config."""
        manager = BatchStrategyManager()
        assert manager.config is not None
        assert manager.config.default_batch_size == 25  # Updated to match current default
    
    def test_calculate_optimal_batch_size_empty_files(self):
        """Test batch size calculation with empty file list."""
        result = self.manager.calculate_optimal_batch_size(
            files=[],
            file_sizes={},
            rate_limit_remaining=1000
        )
        assert result == 0
    
    def test_calculate_optimal_batch_size_small_files(self):
        """Test batch size calculation with small files."""
        files = ['file1.txt', 'file2.txt', 'file3.txt']
        file_sizes = {'file1.txt': 1000, 'file2.txt': 2000, 'file3.txt': 1500}
        
        result = self.manager.calculate_optimal_batch_size(
            files=files,
            file_sizes=file_sizes,
            rate_limit_remaining=1000
        )
        
        # Should allow larger batch size for small files
        assert result >= self.config.default_batch_size
        assert result <= self.config.max_batch_size
    
    def test_calculate_optimal_batch_size_large_files(self):
        """Test batch size calculation with large files."""
        files = ['large1.json', 'large2.json']
        file_sizes = {
            'large1.json': 2 * 1024 * 1024,  # 2MB
            'large2.json': 3 * 1024 * 1024   # 3MB
        }
        
        result = self.manager.calculate_optimal_batch_size(
            files=files,
            file_sizes=file_sizes,
            rate_limit_remaining=1000
        )
        
        # Should use smaller batch size for large files
        assert result < self.config.default_batch_size
        assert result >= self.config.min_batch_size
    
    def test_calculate_optimal_batch_size_low_rate_limit(self):
        """Test batch size calculation with low rate limit."""
        files = ['file1.txt', 'file2.txt', 'file3.txt']
        file_sizes = {'file1.txt': 1000, 'file2.txt': 2000, 'file3.txt': 1500}
        
        result = self.manager.calculate_optimal_batch_size(
            files=files,
            file_sizes=file_sizes,
            rate_limit_remaining=50  # Low rate limit
        )
        
        # Should return a reasonable batch size within bounds
        assert result >= self.config.min_batch_size
        assert result <= self.config.max_batch_size
    
    def test_calculate_optimal_batch_size_with_good_network(self):
        """Test batch size calculation with good network conditions."""
        files = ['file1.txt', 'file2.txt', 'file3.txt']
        file_sizes = {'file1.txt': 1000, 'file2.txt': 2000, 'file3.txt': 1500}
        network_conditions = NetworkConditions(
            latency_ms=50,
            bandwidth_mbps=100,
            error_rate=0.01
        )
        
        result = self.manager.calculate_optimal_batch_size(
            files=files,
            file_sizes=file_sizes,
            rate_limit_remaining=1000,
            network_conditions=network_conditions
        )
        
        # Should allow larger batch size with good network
        assert result >= self.config.default_batch_size
    
    def test_calculate_optimal_batch_size_with_poor_network(self):
        """Test batch size calculation with poor network conditions."""
        files = ['file1.txt', 'file2.txt', 'file3.txt']
        file_sizes = {'file1.txt': 1000, 'file2.txt': 2000, 'file3.txt': 1500}
        network_conditions = NetworkConditions(
            latency_ms=1000,
            bandwidth_mbps=1,
            error_rate=0.2
        )
        
        result = self.manager.calculate_optimal_batch_size(
            files=files,
            file_sizes=file_sizes,
            rate_limit_remaining=1000,
            network_conditions=network_conditions
        )
        
        # Should return a reasonable batch size within bounds
        assert result >= self.config.min_batch_size
        assert result <= self.config.max_batch_size
    
    def test_calculate_optimal_batch_size_respects_limits(self):
        """Test that batch size calculation respects configured limits."""
        files = ['file1.txt'] * 100  # Many files
        file_sizes = {f'file{i}.txt': 100 for i in range(100)}
        
        result = self.manager.calculate_optimal_batch_size(
            files=files,
            file_sizes=file_sizes,
            rate_limit_remaining=5000
        )
        
        assert result >= self.config.min_batch_size
        assert result <= self.config.max_batch_size
    
    def test_prioritize_files_empty_list(self):
        """Test file prioritization with empty list."""
        result = self.manager.prioritize_files([])
        assert result == []
    
    def test_prioritize_files_package_manager_files(self):
        """Test prioritization of package manager files."""
        files = [
            'src/main.py',
            'package.json',
            'requirements.txt',
            'README.md',
            'go.mod'
        ]
        
        result = self.manager.prioritize_files(files)
        
        # Should have all files
        assert len(result) == len(files)
        
        # Package manager files should be prioritized
        high_priority_files = [f for f in result if f.priority >= 8]
        assert len(high_priority_files) >= 3  # package.json, requirements.txt, go.mod
        
        # Should be sorted by priority (highest first)
        priorities = [f.priority for f in result]
        assert priorities == sorted(priorities, reverse=True)
    
    def test_prioritize_files_security_importance(self):
        """Test that security importance is calculated correctly."""
        files = ['package.json', 'src/main.py', 'README.md']
        
        result = self.manager.prioritize_files(files)
        
        # package.json should have highest security importance
        package_json = next(f for f in result if 'package.json' in f.path)
        main_py = next(f for f in result if 'main.py' in f.path)
        readme = next(f for f in result if 'README.md' in f.path)
        
        assert package_json.security_importance > main_py.security_importance
        assert main_py.security_importance > readme.security_importance
    
    def test_prioritize_files_estimated_sizes(self):
        """Test that file sizes are estimated correctly."""
        files = ['package.json', 'package-lock.json', 'main.py']
        
        result = self.manager.prioritize_files(files)
        
        # package-lock.json should have larger estimated size than package.json
        package_json = next(f for f in result if f.path == 'package.json')
        package_lock = next(f for f in result if f.path == 'package-lock.json')
        
        assert package_lock.estimated_size > package_json.estimated_size
    
    def test_identify_cross_repo_opportunities_empty_repos(self):
        """Test cross-repo identification with empty repositories."""
        result = self.manager.identify_cross_repo_opportunities([], {})
        assert result == []
    
    def test_identify_cross_repo_opportunities_single_repo(self):
        """Test cross-repo identification with single repository."""
        from datetime import datetime
        repo = Repository(
            full_name="owner/repo", 
            name="repo", 
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        repo_files = {"owner/repo": ["package.json", "src/main.js"]}
        
        result = self.manager.identify_cross_repo_opportunities([repo], repo_files)
        assert result == []
    
    def test_identify_cross_repo_opportunities_no_common_files(self):
        """Test cross-repo identification with no common files."""
        from datetime import datetime
        repos = [
            Repository(
                full_name="owner/repo1", 
                name="repo1", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="owner/repo2", 
                name="repo2", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            )
        ]
        repo_files = {
            "owner/repo1": ["package.json", "src/main.js"],
            "owner/repo2": ["requirements.txt", "src/main.py"]
        }
        
        result = self.manager.identify_cross_repo_opportunities(repos, repo_files)
        assert result == []
    
    def test_identify_cross_repo_opportunities_with_common_files(self):
        """Test cross-repo identification with common files."""
        from datetime import datetime
        repos = [
            Repository(
                full_name="owner/repo1", 
                name="repo1", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="owner/repo2", 
                name="repo2", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="owner/repo3", 
                name="repo3", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            )
        ]
        repo_files = {
            "owner/repo1": ["package.json", "src/main.js", "dockerfile"],
            "owner/repo2": ["package.json", "src/index.js", "dockerfile"],
            "owner/repo3": ["requirements.txt", "src/main.py"]
        }
        
        result = self.manager.identify_cross_repo_opportunities(repos, repo_files)
        
        # Should find opportunity for repo1 and repo2 (common package.json and dockerfile)
        assert len(result) > 0
        
        opportunity = result[0]
        assert len(opportunity.repositories) == 2
        assert len(opportunity.common_files) >= 2
        assert opportunity.estimated_savings > 0
    
    def test_identify_cross_repo_opportunities_disabled(self):
        """Test cross-repo identification when disabled in config."""
        from datetime import datetime
        config = BatchConfig(enable_cross_repo_batching=False)
        manager = BatchStrategyManager(config)
        
        repos = [
            Repository(
                full_name="owner/repo1", 
                name="repo1", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="owner/repo2", 
                name="repo2", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            )
        ]
        repo_files = {
            "owner/repo1": ["package.json"],
            "owner/repo2": ["package.json"]
        }
        
        result = manager.identify_cross_repo_opportunities(repos, repo_files)
        assert result == []
    
    def test_adapt_strategy_no_history(self):
        """Test strategy adaptation with no performance history."""
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=9,
            parallel_efficiency=0.8
        )
        
        result = self.manager.adapt_strategy(metrics)
        
        # Should return a valid strategy
        assert isinstance(result, BatchStrategy)
        
        # Should store the metrics
        assert len(self.manager._performance_history) == 1
    
    def test_adapt_strategy_low_success_rate(self):
        """Test strategy adaptation with low success rate."""
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=6,  # 60% success rate
            parallel_efficiency=0.5
        )
        
        result = self.manager.adapt_strategy(metrics)
        
        # Should recommend conservative strategy for low success rate
        assert result == BatchStrategy.CONSERVATIVE
    
    def test_adapt_strategy_high_performance(self):
        """Test strategy adaptation with high performance."""
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=10,  # 100% success rate
            parallel_efficiency=0.9
        )
        
        result = self.manager.adapt_strategy(metrics)
        
        # Should recommend aggressive strategy for high performance
        assert result == BatchStrategy.AGGRESSIVE
    
    def test_adapt_strategy_good_parallel_efficiency(self):
        """Test strategy adaptation with good parallel efficiency."""
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=9,  # 90% success rate
            parallel_efficiency=0.7
        )
        
        result = self.manager.adapt_strategy(metrics)
        
        # Should recommend parallel strategy for good efficiency
        assert result == BatchStrategy.PARALLEL
    
    def test_adapt_strategy_history_limit(self):
        """Test that performance history is limited."""
        # Add more than 10 metrics
        for i in range(15):
            metrics = BatchMetrics(
                total_requests=10,
                successful_requests=9,
                parallel_efficiency=0.8
            )
            self.manager.adapt_strategy(metrics)
        
        # Should keep only last 10
        assert len(self.manager._performance_history) == 10
    
    def test_file_type_priorities_initialization(self):
        """Test that file type priorities are properly initialized."""
        priorities = self.manager._file_type_priorities
        
        # Package manager files should have high priority
        assert priorities['package.json'] >= 8
        assert priorities['requirements.txt'] >= 8
        assert priorities['go.mod'] >= 8
        
        # Source code files should have lower priority
        assert priorities['python'] < priorities['package.json']
        assert priorities['javascript'] < priorities['requirements.txt']
    
    def test_calculate_size_factor(self):
        """Test size factor calculation."""
        # Small files should allow larger batches
        small_factor = self.manager._calculate_size_factor(5000)  # 5KB
        assert small_factor > 1.0
        
        # Large files should require smaller batches
        large_factor = self.manager._calculate_size_factor(2 * 1024 * 1024)  # 2MB
        assert large_factor < 1.0
        
        # Zero size should return 1.0
        zero_factor = self.manager._calculate_size_factor(0)
        assert zero_factor == 1.0
    
    def test_calculate_rate_limit_factor(self):
        """Test rate limit factor calculation."""
        # High rate limit should allow normal or higher batching
        high_factor = self.manager._calculate_rate_limit_factor(2000)
        assert high_factor >= 1.0
        
        # Low rate limit should reduce batch size
        low_factor = self.manager._calculate_rate_limit_factor(50)
        assert low_factor < high_factor
    
    def test_calculate_network_factor(self):
        """Test network factor calculation."""
        # No network conditions should return a reasonable factor
        none_factor = self.manager._calculate_network_factor(None)
        assert none_factor >= 1.0
        
        # Good network should allow larger batches
        good_network = NetworkConditions(latency_ms=50, bandwidth_mbps=50, error_rate=0.01)
        good_factor = self.manager._calculate_network_factor(good_network)
        assert good_factor >= 1.0
        
        # Poor network should reduce batch size
        poor_network = NetworkConditions(latency_ms=1000, bandwidth_mbps=1, error_rate=0.2)
        poor_factor = self.manager._calculate_network_factor(poor_network)
        assert poor_factor < 1.0
    
    def test_determine_file_type(self):
        """Test file type determination."""
        # Package manager files
        assert self.manager._determine_file_type('package.json') == 'package.json'
        assert self.manager._determine_file_type('requirements.txt') == 'requirements.txt'
        assert self.manager._determine_file_type('go.mod') == 'go.mod'
        
        # Source code files
        assert self.manager._determine_file_type('main.py') == 'python'
        assert self.manager._determine_file_type('app.js') == 'javascript'
        assert self.manager._determine_file_type('main.go') == 'go'
        
        # Unknown files
        assert self.manager._determine_file_type('unknown.xyz') == 'unknown'
    
    def test_calculate_security_importance(self):
        """Test security importance calculation."""
        # Package manager files should have high importance
        pkg_importance = self.manager._calculate_security_importance('package.json', 'package.json')
        assert pkg_importance >= 3.0
        
        # Source code files should have medium importance
        src_importance = self.manager._calculate_security_importance('main.py', 'python')
        assert 1.0 < src_importance < 3.0
        
        # Other files should have low importance
        other_importance = self.manager._calculate_security_importance('README.md', 'markdown')
        assert other_importance == 1.0
    
    def test_estimate_file_size(self):
        """Test file size estimation."""
        # Package lock files should be estimated as larger
        lock_size = self.manager._estimate_file_size('package-lock.json')
        json_size = self.manager._estimate_file_size('package.json')
        assert lock_size > json_size
        
        # Unknown files should have default size
        unknown_size = self.manager._estimate_file_size('unknown')
        assert unknown_size > 0
    
    def test_is_important_file(self):
        """Test important file identification."""
        # Package manager files should be important
        assert self.manager._is_important_file('package.json')
        assert self.manager._is_important_file('requirements.txt')
        assert self.manager._is_important_file('go.mod')
        
        # Regular source files should not be important for cross-repo batching
        assert not self.manager._is_important_file('main.py')
        assert not self.manager._is_important_file('app.js')
    
    def test_calculate_cross_repo_savings(self):
        """Test cross-repository savings calculation."""
        from datetime import datetime
        repos = [
            Repository(
                full_name="owner/repo1", 
                name="repo1", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="owner/repo2", 
                name="repo2", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            )
        ]
        
        # Common important files should yield good savings
        important_files = ['package.json', 'dockerfile']
        savings = self.manager._calculate_cross_repo_savings(repos, important_files)
        assert savings > 0.2
        
        # No files should yield no savings
        no_savings = self.manager._calculate_cross_repo_savings(repos, [])
        assert no_savings == 0.0
        
        # Single repo should yield no savings
        single_savings = self.manager._calculate_cross_repo_savings([repos[0]], important_files)
        assert single_savings == 0.0


class TestFilePrioritizationSystem:
    """Comprehensive tests for file prioritization system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = BatchStrategyManager()
    
    def test_prioritization_order_package_managers(self):
        """Test that package manager files are prioritized correctly."""
        files = [
            'src/main.py',
            'package.json',
            'requirements.txt',
            'go.mod',
            'Cargo.lock',
            'composer.lock',
            'Gemfile.lock',
            'yarn.lock',
            'README.md'
        ]
        
        result = self.manager.prioritize_files(files)
        
        # Get all package manager files from result
        package_manager_files = [f for f in result if f.priority >= 8]
        package_manager_names = [f.path for f in package_manager_files]
        
        # All package manager files should have high priority
        expected_package_files = ['package.json', 'requirements.txt', 'go.mod', 'Cargo.lock', 'composer.lock', 'Gemfile.lock', 'yarn.lock']
        for pkg_file in expected_package_files:
            assert pkg_file in package_manager_names
        
        # Non-package files should have lower priority
        non_package_files = [f for f in result if f.priority < 8]
        non_package_names = [f.path for f in non_package_files]
        assert 'src/main.py' in non_package_names
        assert 'README.md' in non_package_names
    
    def test_prioritization_within_same_type(self):
        """Test prioritization within the same file type category."""
        files = [
            'package.json',      # Priority 10
            'package-lock.json', # Priority 9
            'yarn.lock',         # Priority 9
            'requirements.txt',  # Priority 10
            'go.mod',           # Priority 10
            'go.sum'            # Priority 9
        ]
        
        result = self.manager.prioritize_files(files)
        
        # Check that the manager's priority system is working
        package_json = next(f for f in result if f.path == 'package.json')
        package_lock = next(f for f in result if f.path == 'package-lock.json')
        yarn_lock = next(f for f in result if f.path == 'yarn.lock')
        requirements = next(f for f in result if f.path == 'requirements.txt')
        go_mod = next(f for f in result if f.path == 'go.mod')
        go_sum = next(f for f in result if f.path == 'go.sum')
        
        # Verify the manager assigned the correct priorities
        assert package_json.priority == 10
        assert package_lock.priority == 9
        assert yarn_lock.priority == 9
        assert requirements.priority == 10
        assert go_mod.priority == 10
        assert go_sum.priority == 9
        
        # Files should be sorted by priority (highest first)
        priorities = [f.priority for f in result]
        assert priorities == sorted(priorities, reverse=True)
    
    def test_security_importance_calculation(self):
        """Test security importance calculation for different file types."""
        files = [
            'package.json',        # High security importance (3.0)
            'requirements.txt',    # High security importance (3.0)
            'dockerfile',          # Medium security importance (2.0)
            '.env',               # Medium security importance (2.0)
            'src/main.py',        # Lower security importance (1.5)
            'README.md',          # Minimal security importance (1.0)
        ]
        
        result = self.manager.prioritize_files(files)
        
        # Check security importance values
        package_json = next(f for f in result if 'package.json' in f.path)
        requirements = next(f for f in result if 'requirements.txt' in f.path)
        dockerfile = next(f for f in result if 'dockerfile' in f.path)
        env_file = next(f for f in result if '.env' in f.path)
        python_file = next(f for f in result if 'main.py' in f.path)
        readme = next(f for f in result if 'README.md' in f.path)
        
        assert package_json.security_importance >= 3.0
        assert requirements.security_importance >= 3.0
        assert dockerfile.security_importance >= 2.0
        assert env_file.security_importance >= 2.0
        assert python_file.security_importance >= 1.5
        assert readme.security_importance == 1.0
    
    def test_file_type_detection_comprehensive(self):
        """Test comprehensive file type detection."""
        test_cases = [
            # JavaScript ecosystem
            ('package.json', 'package.json'),
            ('package-lock.json', 'package-lock.json'),
            ('yarn.lock', 'yarn.lock'),
            ('pnpm-lock.yaml', 'pnpm-lock.yaml'),
            ('bun.lockb', 'bun.lockb'),
            ('app.js', 'javascript'),
            ('component.jsx', 'javascript'),
            ('module.mjs', 'javascript'),
            ('app.ts', 'typescript'),
            ('component.tsx', 'typescript'),
            
            # Python ecosystem
            ('requirements.txt', 'requirements.txt'),
            ('Pipfile.lock', 'pipfile.lock'),
            ('poetry.lock', 'poetry.lock'),
            ('pyproject.toml', 'pyproject.toml'),
            ('main.py', 'python'),
            ('script.pyw', 'python'),
            
            # Other languages
            ('Gemfile.lock', 'gemfile.lock'),
            ('composer.lock', 'composer.lock'),
            ('go.mod', 'go.mod'),
            ('go.sum', 'go.sum'),
            ('Cargo.lock', 'cargo.lock'),
            ('main.go', 'go'),
            ('lib.rs', 'rust'),
            ('app.rb', 'ruby'),
            ('index.php', 'php'),
            
            # Configuration files
            ('Dockerfile', 'dockerfile'),
            ('dockerfile', 'dockerfile'),
            ('Makefile', 'makefile'),
            ('makefile', 'makefile'),
            ('docker-compose.yml', 'docker-compose.yml'),
            ('config.json', 'config.json'),
            ('settings.yaml', 'yaml'),
            
            # Other files
            ('README.md', 'markdown'),
            ('CHANGELOG.markdown', 'markdown'),
            ('notes.txt', 'text'),
            ('app.log', 'text'),
            ('data.json', 'json'),
            ('unknown.xyz', 'unknown'),
        ]
        
        for filename, expected_type in test_cases:
            detected_type = self.manager._determine_file_type(filename)
            assert detected_type == expected_type, f"Failed for {filename}: expected {expected_type}, got {detected_type}"
    
    def test_priority_based_batch_ordering(self):
        """Test that files are ordered correctly for batch processing."""
        files = [
            'README.md',           # Low priority
            'src/utils.py',        # Medium priority  
            'tests/test_main.py',  # Medium priority
            'package.json',        # High priority
            'dockerfile',          # Medium-high priority
            'requirements.txt',    # High priority
            'src/main.py',         # Medium priority
            '.env.example',        # Medium priority
        ]
        
        result = self.manager.prioritize_files(files)
        
        # First few files should be high priority package manager files
        assert result[0].path in ['package.json', 'requirements.txt']
        assert result[1].path in ['package.json', 'requirements.txt']
        
        # Last file should be low priority
        assert result[-1].path == 'README.md'
        assert result[-1].priority == 1
    
    def test_estimated_file_sizes(self):
        """Test that file sizes are estimated appropriately."""
        files = [
            'package.json',      # Small config file
            'package-lock.json', # Large lock file
            'requirements.txt',  # Small requirements file
            'poetry.lock',       # Large lock file
            'go.mod',           # Small module file
            'Cargo.lock',       # Large lock file
        ]
        
        result = self.manager.prioritize_files(files)
        
        # Lock files should have larger estimated sizes than their config counterparts
        package_json = next(f for f in result if f.path == 'package.json')
        package_lock = next(f for f in result if f.path == 'package-lock.json')
        requirements = next(f for f in result if f.path == 'requirements.txt')
        poetry_lock = next(f for f in result if f.path == 'poetry.lock')
        go_mod = next(f for f in result if f.path == 'go.mod')
        cargo_lock = next(f for f in result if f.path == 'Cargo.lock')
        
        assert package_lock.estimated_size > package_json.estimated_size
        assert poetry_lock.estimated_size > requirements.estimated_size
        assert cargo_lock.estimated_size > go_mod.estimated_size
    
    def test_prioritization_with_nested_paths(self):
        """Test prioritization works with nested file paths."""
        files = [
            'frontend/package.json',
            'backend/requirements.txt',
            'services/auth/go.mod',
            'docker/Dockerfile',
            'src/main/java/App.java',
            'docs/README.md',
            'scripts/deploy.sh',
        ]
        
        result = self.manager.prioritize_files(files)
        
        # Package manager files should still be prioritized regardless of path
        top_3 = result[:3]
        top_paths = [f.path for f in top_3]
        
        assert 'frontend/package.json' in top_paths
        assert 'backend/requirements.txt' in top_paths
        assert 'services/auth/go.mod' in top_paths


class TestCrossRepositoryBatchingAnalysis:
    """Comprehensive tests for cross-repository batching analysis."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.manager = BatchStrategyManager()
        
        # Create test repositories
        from datetime import datetime
        self.repos = [
            Repository(
                full_name="org/frontend-app", 
                name="frontend-app", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="org/backend-api", 
                name="backend-api", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="org/mobile-app", 
                name="mobile-app", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="org/data-service", 
                name="data-service", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                full_name="org/legacy-system", 
                name="legacy-system", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            )
        ]
    
    def test_identify_simple_cross_repo_opportunity(self):
        """Test identification of simple cross-repository batching opportunity."""
        repo_files = {
            "org/frontend-app": ["package.json", "src/app.js", "README.md"],
            "org/backend-api": ["package.json", "src/server.js", "README.md"],
            "org/mobile-app": ["package.json", "src/main.js", "README.md"]
        }
        
        opportunities = self.manager.identify_cross_repo_opportunities(
            self.repos[:3], repo_files
        )
        
        # Should find opportunity for all three repos (common package.json)
        assert len(opportunities) > 0
        
        opportunity = opportunities[0]
        assert len(opportunity.repositories) == 3
        assert "package.json" in opportunity.common_files
        assert opportunity.estimated_savings > 0.2
    
    def test_identify_multiple_cross_repo_opportunities(self):
        """Test identification of multiple cross-repository opportunities."""
        repo_files = {
            "org/frontend-app": ["package.json", "dockerfile", "src/app.js"],
            "org/backend-api": ["package.json", "dockerfile", "src/server.js"],
            "org/mobile-app": ["package.json", "src/main.js"],
            "org/data-service": ["requirements.txt", "dockerfile", "src/main.py"],
            "org/legacy-system": ["requirements.txt", "src/legacy.py"]
        }
        
        opportunities = self.manager.identify_cross_repo_opportunities(
            self.repos, repo_files
        )
        
        # Should find at least one opportunity
        assert len(opportunities) >= 1
        
        # Check for specific opportunities
        has_package_json_opp = any(
            "package.json" in opp.common_files for opp in opportunities
        )
        has_dockerfile_opp = any(
            "dockerfile" in opp.common_files for opp in opportunities
        )
        has_requirements_opp = any(
            "requirements.txt" in opp.common_files for opp in opportunities
        )
        
        # Should find at least package.json opportunity (3 repos have it)
        assert has_package_json_opp
        
        # Check that opportunities are sorted by estimated savings
        if len(opportunities) > 1:
            for i in range(len(opportunities) - 1):
                assert opportunities[i].estimated_savings >= opportunities[i + 1].estimated_savings
    
    def test_cross_repo_with_no_common_files(self):
        """Test cross-repo analysis when repositories have no common files."""
        repo_files = {
            "org/frontend-app": ["package.json", "src/app.js"],
            "org/backend-api": ["requirements.txt", "src/server.py"],
            "org/mobile-app": ["go.mod", "src/main.go"]
        }
        
        opportunities = self.manager.identify_cross_repo_opportunities(
            self.repos[:3], repo_files
        )
        
        # Should find no opportunities since no common important files
        assert len(opportunities) == 0
    
    def test_cross_repo_with_mixed_file_types(self):
        """Test cross-repo analysis with mixed file types."""
        repo_files = {
            "org/frontend-app": ["package.json", "dockerfile", "src/app.js", "README.md"],
            "org/backend-api": ["requirements.txt", "dockerfile", "src/server.py", "README.md"],
            "org/mobile-app": ["go.mod", "dockerfile", "src/main.go", "README.md"],
            "org/data-service": ["package.json", "requirements.txt", "src/main.py"]
        }
        
        opportunities = self.manager.identify_cross_repo_opportunities(
            self.repos[:4], repo_files
        )
        
        # Should find at least one opportunity
        assert len(opportunities) >= 1
        
        # Check for dockerfile opportunity (first 3 repos have it)
        dockerfile_opportunity = None
        for opp in opportunities:
            if "dockerfile" in opp.common_files:
                dockerfile_opportunity = opp
                break
        
        # Should find dockerfile opportunity
        assert dockerfile_opportunity is not None
        assert len(dockerfile_opportunity.repositories) == 3  # First 3 repos have dockerfile
        assert dockerfile_opportunity.estimated_savings > 0
    
    def test_cross_repo_savings_calculation(self):
        """Test cross-repository savings calculation accuracy."""
        # Test with 2 repos and 1 common file
        repos_2_1 = self.repos[:2]
        savings_2_1 = self.manager._calculate_cross_repo_savings(repos_2_1, ["package.json"])
        
        # Test with 3 repos and 2 common files
        repos_3_2 = self.repos[:3]
        savings_3_2 = self.manager._calculate_cross_repo_savings(repos_3_2, ["package.json", "dockerfile"])
        
        # Test with 4 repos and 3 common files (high-priority files)
        repos_4_3 = self.repos[:4]
        savings_4_3 = self.manager._calculate_cross_repo_savings(repos_4_3, ["package.json", "dockerfile", "requirements.txt"])
        
        # More repos and files should yield higher savings
        assert savings_3_2 > savings_2_1
        assert savings_4_3 > savings_3_2
        
        # All savings should be reasonable (between 0 and 0.79)
        assert 0 < savings_2_1 <= 0.79
        assert 0 < savings_3_2 <= 0.79
        assert 0 < savings_4_3 <= 0.79
    
    def test_cross_repo_with_nested_paths(self):
        """Test cross-repo analysis with nested file paths."""
        repo_files = {
            "org/frontend-app": ["frontend/package.json", "docker/dockerfile", "src/app.js"],
            "org/backend-api": ["api/package.json", "docker/dockerfile", "src/server.js"],
            "org/mobile-app": ["mobile/package.json", "docker/dockerfile", "src/main.js"]
        }
        
        opportunities = self.manager.identify_cross_repo_opportunities(
            self.repos[:3], repo_files
        )
        
        # Should find opportunities despite different paths (normalized by filename)
        assert len(opportunities) > 0
        
        # Should find package.json opportunity (all 3 repos have it)
        package_json_opp = None
        for opp in opportunities:
            if "package.json" in opp.common_files:
                package_json_opp = opp
                break
        
        assert package_json_opp is not None
        assert len(package_json_opp.repositories) == 3
        
        # Should also find dockerfile opportunity
        dockerfile_opp = None
        for opp in opportunities:
            if "dockerfile" in opp.common_files:
                dockerfile_opp = opp
                break
        
        assert dockerfile_opp is not None
        assert len(dockerfile_opp.repositories) == 3
    
    def test_cross_repo_disabled_in_config(self):
        """Test that cross-repo analysis respects configuration."""
        config = BatchConfig(enable_cross_repo_batching=False)
        manager = BatchStrategyManager(config)
        
        repo_files = {
            "org/frontend-app": ["package.json", "dockerfile"],
            "org/backend-api": ["package.json", "dockerfile"],
            "org/mobile-app": ["package.json", "dockerfile"]
        }
        
        opportunities = manager.identify_cross_repo_opportunities(
            self.repos[:3], repo_files
        )
        
        # Should find no opportunities when disabled
        assert len(opportunities) == 0
    
    def test_cross_repo_minimum_savings_threshold(self):
        """Test that only opportunities with significant savings are returned."""
        # Create scenario with minimal savings (single repo, single file)
        repo_files = {
            "org/frontend-app": ["package.json"],
            "org/backend-api": ["package.json"]  # Only 2 repos, 1 file
        }
        
        opportunities = self.manager.identify_cross_repo_opportunities(
            self.repos[:2], repo_files
        )
        
        # Should still find opportunity but verify savings threshold
        if opportunities:
            assert opportunities[0].estimated_savings >= 0.2  # Minimum 20% savings
    
    def test_cross_repo_with_large_number_of_repos(self):
        """Test cross-repo analysis with many repositories."""
        # Create many repos with same files
        from datetime import datetime
        many_repos = []
        repo_files = {}
        
        for i in range(10):
            repo = Repository(
                full_name=f"org/service-{i}", 
                name=f"service-{i}", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            )
            many_repos.append(repo)
            repo_files[f"org/service-{i}"] = ["package.json", "dockerfile", "requirements.txt"]
        
        opportunities = self.manager.identify_cross_repo_opportunities(
            many_repos, repo_files
        )
        
        # Should find significant opportunity with many repos
        assert len(opportunities) > 0
        
        best_opportunity = opportunities[0]
        assert len(best_opportunity.repositories) == 10
        assert len(best_opportunity.common_files) == 3
        assert best_opportunity.estimated_savings > 0.5  # Should be high with many repos
    
    def test_find_common_files_algorithm(self):
        """Test the common files finding algorithm."""
        repo_files = {
            "org/repo1": ["package.json", "dockerfile", "src/main.js"],
            "org/repo2": ["package.json", "dockerfile", "src/app.js"],
            "org/repo3": ["package.json", "src/index.js"],
            "org/repo4": ["requirements.txt", "dockerfile", "src/main.py"],
            "org/repo5": ["requirements.txt", "src/app.py"]
        }
        
        common_files_map = self.manager._find_common_files(repo_files)
        
        # Should group repos by their common important files
        assert len(common_files_map) > 0
        
        # Check that repos with package.json are grouped
        package_json_groups = [
            repos for files, repos in common_files_map.items()
            if "package.json" in files
        ]
        assert len(package_json_groups) > 0
        
        # Check that repos with dockerfile are grouped
        dockerfile_groups = [
            repos for files, repos in common_files_map.items()
            if "dockerfile" in files
        ]
        assert len(dockerfile_groups) > 0
    
    def test_important_file_identification(self):
        """Test identification of important files for cross-repo batching."""
        # Important files should be identified correctly
        assert self.manager._is_important_file("package.json")
        assert self.manager._is_important_file("requirements.txt")
        assert self.manager._is_important_file("dockerfile")
        assert self.manager._is_important_file("go.mod")
        assert self.manager._is_important_file("Cargo.lock")
        
        # Non-important files should not be identified
        assert not self.manager._is_important_file("main.js")
        assert not self.manager._is_important_file("README.md")
        assert not self.manager._is_important_file("test.py")
        assert not self.manager._is_important_file("config.yaml")


class TestBatchStrategyManagerIntegration:
    """Integration tests for batch strategy manager."""
    
    def test_end_to_end_batch_optimization(self):
        """Test complete batch optimization workflow."""
        config = BatchConfig(
            default_batch_size=10,
            min_batch_size=2,
            max_batch_size=20
        )
        manager = BatchStrategyManager(config)
        
        # Simulate a realistic scenario
        files = [
            'package.json',
            'package-lock.json',
            'src/main.js',
            'src/utils.js',
            'tests/test.js',
            'README.md'
        ]
        
        file_sizes = {
            'package.json': 2048,
            'package-lock.json': 50000,
            'src/main.js': 5000,
            'src/utils.js': 3000,
            'tests/test.js': 2000,
            'README.md': 1500
        }
        
        network_conditions = NetworkConditions(
            latency_ms=100,
            bandwidth_mbps=20,
            error_rate=0.02
        )
        
        # Calculate optimal batch size
        batch_size = manager.calculate_optimal_batch_size(
            files=files,
            file_sizes=file_sizes,
            rate_limit_remaining=1000,
            network_conditions=network_conditions
        )
        
        # Prioritize files
        prioritized_files = manager.prioritize_files(files)
        
        # Verify results
        assert 2 <= batch_size <= 20
        assert len(prioritized_files) == len(files)
        
        # Package manager files should be first
        assert prioritized_files[0].path in ['package.json', 'package-lock.json']
        assert prioritized_files[0].priority >= 8
    
    def test_adaptive_strategy_with_performance_feedback(self):
        """Test adaptive strategy with performance feedback loop."""
        manager = BatchStrategyManager()
        
        # Simulate poor performance
        poor_metrics = BatchMetrics(
            total_requests=20,
            successful_requests=12,  # 60% success
            parallel_efficiency=0.4
        )
        
        strategy1 = manager.adapt_strategy(poor_metrics)
        assert strategy1 == BatchStrategy.CONSERVATIVE
        
        # Simulate improved performance
        good_metrics = BatchMetrics(
            total_requests=20,
            successful_requests=19,  # 95% success
            parallel_efficiency=0.8
        )
        
        strategy2 = manager.adapt_strategy(good_metrics)
        assert strategy2 == BatchStrategy.PARALLEL
        
        # Simulate excellent performance
        excellent_metrics = BatchMetrics(
            total_requests=20,
            successful_requests=20,  # 100% success
            parallel_efficiency=0.9
        )
        
        strategy3 = manager.adapt_strategy(excellent_metrics)
        assert strategy3 == BatchStrategy.AGGRESSIVE


class TestStrategySelectionAndAdaptation:
    """Test strategy selection and adaptation logic."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = BatchConfig(default_strategy=BatchStrategy.ADAPTIVE)
        self.manager = BatchStrategyManager(self.config)
    
    def test_select_strategy_conservative_for_low_rate_limit(self):
        """Test that conservative strategy is selected for low rate limits."""
        from datetime import datetime
        repos = [Repository(
            full_name="owner/repo", 
            name="repo", 
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )]
        
        strategy = self.manager.select_strategy(
            repositories=repos,
            total_files=10,
            rate_limit_remaining=150  # Low rate limit
        )
        
        assert strategy == BatchStrategy.CONSERVATIVE
    
    def test_select_strategy_conservative_for_poor_network(self):
        """Test that conservative strategy is selected for poor network conditions."""
        from datetime import datetime
        repos = [Repository(
            full_name="owner/repo", 
            name="repo", 
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )]
        
        poor_network = NetworkConditions(
            latency_ms=1000,
            bandwidth_mbps=1,
            error_rate=0.2
        )
        
        strategy = self.manager.select_strategy(
            repositories=repos,
            total_files=10,
            rate_limit_remaining=1000,
            network_conditions=poor_network
        )
        
        assert strategy == BatchStrategy.CONSERVATIVE
    
    def test_select_strategy_sequential_for_small_scans(self):
        """Test that sequential strategy is selected for small scans."""
        from datetime import datetime
        repos = [Repository(
            full_name="owner/repo", 
            name="repo", 
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )]
        
        strategy = self.manager.select_strategy(
            repositories=repos,
            total_files=3,  # Small number of files
            rate_limit_remaining=1000
        )
        
        assert strategy == BatchStrategy.SEQUENTIAL
    
    def test_select_strategy_aggressive_for_large_scans(self):
        """Test that aggressive strategy is selected for large scans with good conditions."""
        from datetime import datetime
        repos = [Repository(
            full_name=f"owner/repo{i}", 
            name=f"repo{i}", 
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ) for i in range(15)]  # Many repositories
        
        good_network = NetworkConditions(
            latency_ms=50,
            bandwidth_mbps=100,
            error_rate=0.01
        )
        
        strategy = self.manager.select_strategy(
            repositories=repos,
            total_files=150,  # Many files
            rate_limit_remaining=3000,  # High rate limit
            network_conditions=good_network
        )
        
        assert strategy == BatchStrategy.AGGRESSIVE
    
    def test_select_strategy_parallel_for_medium_scans(self):
        """Test that parallel strategy is selected for medium scans."""
        from datetime import datetime
        repos = [Repository(
            full_name=f"owner/repo{i}", 
            name=f"repo{i}", 
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        ) for i in range(3)]
        
        strategy = self.manager.select_strategy(
            repositories=repos,
            total_files=25,
            rate_limit_remaining=1000
        )
        
        assert strategy == BatchStrategy.PARALLEL
    
    def test_select_strategy_respects_configured_default(self):
        """Test that configured default strategy is respected when not adaptive."""
        config = BatchConfig(default_strategy=BatchStrategy.CONSERVATIVE)
        manager = BatchStrategyManager(config)
        
        from datetime import datetime
        repos = [Repository(
            full_name="owner/repo", 
            name="repo", 
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )]
        
        strategy = manager.select_strategy(
            repositories=repos,
            total_files=50,
            rate_limit_remaining=5000  # Even with good conditions
        )
        
        assert strategy == BatchStrategy.CONSERVATIVE
    
    def test_adapt_strategy_with_performance_trends(self):
        """Test strategy adaptation based on performance trends."""
        # Add improving performance history
        for i in range(3):
            metrics = BatchMetrics(
                total_requests=10,
                successful_requests=7 + i,  # Improving success rate
                parallel_efficiency=0.6 + i * 0.1  # Improving efficiency
            )
            self.manager._performance_history.append(metrics)
        
        # Current good performance
        current_metrics = BatchMetrics(
            total_requests=10,
            successful_requests=10,
            parallel_efficiency=0.9,
            cache_hits=8,
            cache_misses=2
        )
        
        strategy = self.manager.adapt_strategy(current_metrics)
        
        # Should recommend aggressive strategy for improving performance
        assert strategy == BatchStrategy.AGGRESSIVE
    
    def test_adapt_strategy_with_degrading_performance(self):
        """Test strategy adaptation with degrading performance."""
        # Add degrading performance history
        for i in range(3):
            metrics = BatchMetrics(
                total_requests=10,
                successful_requests=10 - i,  # Degrading success rate
                parallel_efficiency=0.9 - i * 0.1  # Degrading efficiency
            )
            self.manager._performance_history.append(metrics)
        
        # Current poor performance
        current_metrics = BatchMetrics(
            total_requests=10,
            successful_requests=6,  # 60% success rate
            parallel_efficiency=0.4
        )
        
        strategy = self.manager.adapt_strategy(current_metrics)
        
        # Should recommend conservative strategy for degrading performance
        assert strategy == BatchStrategy.CONSERVATIVE
    
    def test_adapt_strategy_with_high_cache_hit_rate(self):
        """Test strategy adaptation with high cache hit rate."""
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=9,
            parallel_efficiency=0.7,
            cache_hits=9,  # 90% cache hit rate
            cache_misses=1
        )
        
        strategy = self.manager.adapt_strategy(metrics)
        
        # High cache hit rate should favor more aggressive strategies
        assert strategy in [BatchStrategy.AGGRESSIVE, BatchStrategy.PARALLEL]
    
    def test_adapt_strategy_runtime_emergency_fallback(self):
        """Test runtime strategy adaptation with emergency conditions."""
        current_strategy = BatchStrategy.AGGRESSIVE
        metrics = BatchMetrics(total_requests=10, successful_requests=8)
        
        # High error count should trigger conservative strategy
        adapted_strategy = self.manager.adapt_strategy_runtime(
            current_strategy=current_strategy,
            current_metrics=metrics,
            rate_limit_remaining=1000,
            error_count=6  # High error count
        )
        
        assert adapted_strategy == BatchStrategy.CONSERVATIVE
    
    def test_adapt_strategy_runtime_low_rate_limit(self):
        """Test runtime strategy adaptation with low rate limit."""
        current_strategy = BatchStrategy.AGGRESSIVE
        metrics = BatchMetrics(total_requests=10, successful_requests=9)
        
        adapted_strategy = self.manager.adapt_strategy_runtime(
            current_strategy=current_strategy,
            current_metrics=metrics,
            rate_limit_remaining=30,  # Very low rate limit
            error_count=1
        )
        
        assert adapted_strategy == BatchStrategy.CONSERVATIVE
    
    def test_adapt_strategy_runtime_step_down(self):
        """Test runtime strategy adaptation stepping down from aggressive."""
        current_strategy = BatchStrategy.AGGRESSIVE
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=5  # 50% success rate
        )
        
        adapted_strategy = self.manager.adapt_strategy_runtime(
            current_strategy=current_strategy,
            current_metrics=metrics,
            rate_limit_remaining=1000,
            error_count=2
        )
        
        # Should step down from aggressive to parallel
        assert adapted_strategy == BatchStrategy.PARALLEL
    
    def test_adapt_strategy_runtime_step_up(self):
        """Test runtime strategy adaptation stepping up from conservative."""
        current_strategy = BatchStrategy.CONSERVATIVE
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=10  # 100% success rate
        )
        
        adapted_strategy = self.manager.adapt_strategy_runtime(
            current_strategy=current_strategy,
            current_metrics=metrics,
            rate_limit_remaining=2000,  # High rate limit
            error_count=0
        )
        
        # Should step up from conservative to parallel
        assert adapted_strategy == BatchStrategy.PARALLEL
    
    def test_adapt_strategy_runtime_no_change_needed(self):
        """Test runtime strategy adaptation when no change is needed."""
        current_strategy = BatchStrategy.PARALLEL
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=9  # 90% success rate - good but not exceptional
        )
        
        adapted_strategy = self.manager.adapt_strategy_runtime(
            current_strategy=current_strategy,
            current_metrics=metrics,
            rate_limit_remaining=1000,
            error_count=1
        )
        
        # Should keep current strategy
        assert adapted_strategy == current_strategy
    
    def test_get_strategy_config_conservative(self):
        """Test configuration for conservative strategy."""
        config = self.manager.get_strategy_config(BatchStrategy.CONSERVATIVE)
        
        # Conservative strategy should have reduced concurrency and batch sizes
        assert config['max_concurrent_requests'] <= 3
        assert config['max_concurrent_repos'] == 1
        assert config['default_batch_size'] <= self.config.default_batch_size
        assert config['max_batch_size'] <= 10
        assert config['retry_attempts'] > self.config.retry_attempts
        assert config['rate_limit_buffer'] < self.config.rate_limit_buffer
    
    def test_get_strategy_config_sequential(self):
        """Test configuration for sequential strategy."""
        config = self.manager.get_strategy_config(BatchStrategy.SEQUENTIAL)
        
        # Sequential strategy should have minimal concurrency
        assert config['max_concurrent_requests'] == 1
        assert config['max_concurrent_repos'] == 1
        assert config['default_batch_size'] == 1
        assert config['max_batch_size'] == 1
        assert config['retry_attempts'] > self.config.retry_attempts
    
    def test_get_strategy_config_aggressive(self):
        """Test configuration for aggressive strategy."""
        config = self.manager.get_strategy_config(BatchStrategy.AGGRESSIVE)
        
        # Aggressive strategy should have reasonable concurrency and batch sizes
        assert config['max_concurrent_requests'] > 0
        assert config['max_concurrent_repos'] > 0
        assert config['default_batch_size'] > 0
        assert config['max_batch_size'] > 0
        assert config['retry_attempts'] >= 0
        assert config['rate_limit_buffer'] > 0
    
    def test_get_strategy_config_parallel(self):
        """Test configuration for parallel strategy."""
        config = self.manager.get_strategy_config(BatchStrategy.PARALLEL)
        
        # Parallel strategy should use base configuration
        assert config['max_concurrent_requests'] == self.config.max_concurrent_requests
        assert config['max_concurrent_repos'] == self.config.max_concurrent_repos
        assert config['default_batch_size'] == self.config.default_batch_size
        assert config['max_batch_size'] == self.config.max_batch_size
    
    def test_get_strategy_config_adaptive(self):
        """Test configuration for adaptive strategy."""
        config = self.manager.get_strategy_config(BatchStrategy.ADAPTIVE)
        
        # Adaptive strategy should use base configuration
        assert config['max_concurrent_requests'] == self.config.max_concurrent_requests
        assert config['max_concurrent_repos'] == self.config.max_concurrent_repos
        assert config['default_batch_size'] == self.config.default_batch_size
        assert config['max_batch_size'] == self.config.max_batch_size
    
    def test_analyze_performance_trends_improving(self):
        """Test performance trend analysis for improving performance."""
        # Add improving performance history
        for i in range(3):
            metrics = BatchMetrics(
                total_requests=10,
                successful_requests=7 + i,  # 70%, 80%, 90%
                parallel_efficiency=0.5 + i * 0.1  # 0.5, 0.6, 0.7
            )
            self.manager._performance_history.append(metrics)
        
        trends = self.manager._analyze_performance_trends()
        
        assert trends['improving'] is True
        assert trends['degrading'] is False
        assert trends['stable'] is False
        assert trends['high_error_rate'] is False
    
    def test_analyze_performance_trends_degrading(self):
        """Test performance trend analysis for degrading performance."""
        # Add degrading performance history
        for i in range(3):
            metrics = BatchMetrics(
                total_requests=10,
                successful_requests=9 - i,  # 90%, 80%, 70%
                parallel_efficiency=0.8 - i * 0.1  # 0.8, 0.7, 0.6
            )
            self.manager._performance_history.append(metrics)
        
        trends = self.manager._analyze_performance_trends()
        
        assert trends['improving'] is False
        assert trends['degrading'] is True
        assert trends['stable'] is False
    
    def test_analyze_performance_trends_high_error_rate(self):
        """Test performance trend analysis for high error rate."""
        # Add history with high error rate
        for i in range(3):
            metrics = BatchMetrics(
                total_requests=10,
                successful_requests=6,  # 60% success rate (high error rate)
                parallel_efficiency=0.5
            )
            self.manager._performance_history.append(metrics)
        
        trends = self.manager._analyze_performance_trends()
        
        assert trends['high_error_rate'] is True
    
    def test_analyze_performance_trends_insufficient_history(self):
        """Test performance trend analysis with insufficient history."""
        # Add only 2 metrics (less than required 3)
        for i in range(2):
            metrics = BatchMetrics(
                total_requests=10,
                successful_requests=8,
                parallel_efficiency=0.7
            )
            self.manager._performance_history.append(metrics)
        
        trends = self.manager._analyze_performance_trends()
        
        # Should return stable defaults
        assert trends['improving'] is False
        assert trends['degrading'] is False
        assert trends['stable'] is True
        assert trends['high_error_rate'] is False
    
    def test_strategy_adaptation_scoring_system(self):
        """Test the scoring system used in strategy adaptation."""
        # Test with metrics that should favor aggressive strategy
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=10,  # 100% success rate
            parallel_efficiency=0.9,  # High efficiency
            cache_hits=9,  # High cache hit rate
            cache_misses=1
        )
        
        # Add improving trend history
        for i in range(3):
            trend_metrics = BatchMetrics(
                total_requests=10,
                successful_requests=8 + i,
                parallel_efficiency=0.7 + i * 0.05
            )
            self.manager._performance_history.append(trend_metrics)
        
        strategy = self.manager.adapt_strategy(metrics)
        
        # Should score highest for aggressive strategy
        assert strategy == BatchStrategy.AGGRESSIVE
    
    def test_strategy_adaptation_with_mixed_signals(self):
        """Test strategy adaptation with mixed performance signals."""
        # Medium success rate and low parallel efficiency
        metrics = BatchMetrics(
            total_requests=10,
            successful_requests=8,  # 80% success rate (medium)
            parallel_efficiency=0.3,  # Low efficiency
            cache_hits=3,  # Low cache hit rate
            cache_misses=7
        )
        
        strategy = self.manager.adapt_strategy(metrics)
        
        # Should balance the mixed signals - likely conservative, adaptive, or sequential
        assert strategy in [BatchStrategy.CONSERVATIVE, BatchStrategy.ADAPTIVE, BatchStrategy.SEQUENTIAL]