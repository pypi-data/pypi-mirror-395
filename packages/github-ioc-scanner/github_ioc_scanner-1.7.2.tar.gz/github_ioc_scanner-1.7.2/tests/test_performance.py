"""Performance tests for the GitHub IOC Scanner.

This module contains performance tests that verify the scanner's behavior
under various load conditions and measure performance characteristics.
"""

import json
import time
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch
from typing import List, Dict

import pytest

from github_ioc_scanner.scanner import GitHubIOCScanner
from github_ioc_scanner.github_client import GitHubClient
from github_ioc_scanner.cache import CacheManager
from github_ioc_scanner.ioc_loader import IOCLoader
from github_ioc_scanner.models import (
    ScanConfig, Repository, FileInfo, APIResponse, ScanResults,
    FileContent, PackageDependency, IOCMatch, IOCDefinition
)


class TestPerformanceScenarios:
    """Performance tests for various scanning scenarios."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)

    @pytest.fixture
    def temp_issues_dir(self):
        """Create a temporary issues directory with performance test IOCs."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            # Create IOC file with many packages for performance testing
            ioc_file = issues_dir / "performance_iocs.py"
            ioc_packages = {}
            
            # Generate 100 IOC packages for performance testing
            for i in range(100):
                package_name = f"test-package-{i:03d}"
                if i % 3 == 0:
                    ioc_packages[package_name] = None  # Any version
                else:
                    ioc_packages[package_name] = [f"1.{i}.0", f"2.{i}.0"]
            
            ioc_content = f"IOC_PACKAGES = {repr(ioc_packages)}"
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)

    def generate_mock_repositories(self, count: int) -> List[Repository]:
        """Generate a list of mock repositories for testing."""
        repos = []
        for i in range(count):
            repos.append(Repository(
                name=f"repo-{i:04d}",
                full_name=f"test-org/repo-{i:04d}",
                archived=(i % 10 == 0),  # Every 10th repo is archived
                default_branch="main",
                updated_at=datetime.now(timezone.utc)
            ))
        return repos

    def generate_mock_files(self, repo_count: int, files_per_repo: int) -> Dict[str, List[FileInfo]]:
        """Generate mock files for repositories."""
        file_patterns = [
            "package.json", "yarn.lock", "requirements.txt", "poetry.lock",
            "Gemfile.lock", "composer.lock", "go.mod", "Cargo.lock"
        ]
        
        files_by_repo = {}
        for i in range(repo_count):
            repo_name = f"test-org/repo-{i:04d}"
            files = []
            
            for j in range(files_per_repo):
                pattern = file_patterns[j % len(file_patterns)]
                files.append(FileInfo(
                    path=f"path{j}/{pattern}",
                    sha=f"sha-{i}-{j}",
                    size=1024 + (i * j)
                ))
            
            files_by_repo[repo_name] = files
        
        return files_by_repo

    def generate_mock_file_contents(self, files_by_repo: Dict[str, List[FileInfo]]) -> Dict[tuple, FileContent]:
        """Generate mock file contents."""
        contents = {}
        
        for repo_name, files in files_by_repo.items():
            for file_info in files:
                if file_info.path.endswith('.json'):
                    # Generate package.json with dependencies
                    deps = {}
                    for i in range(10):  # 10 dependencies per file
                        deps[f"dep-{i}"] = f"^{i}.0.0"
                    
                    content = json.dumps({
                        "name": f"app-{repo_name.split('/')[-1]}",
                        "dependencies": deps
                    })
                else:
                    # Generate lockfile content
                    content = f"# Lockfile for {file_info.path}\n"
                    for i in range(10):
                        content += f"package-{i}@1.0.0:\n  version: 1.0.0\n"
                
                contents[(repo_name, file_info.path)] = FileContent(
                    content=content,
                    sha=file_info.sha,
                    size=len(content)
                )
        
        return contents

    @pytest.mark.performance
    def test_large_organization_scan_performance(self, temp_cache_dir, temp_issues_dir):
        """Test performance with large organization (500 repositories)."""
        config = ScanConfig(
            org="large-org",
            issues_dir=temp_issues_dir
        )
        
        # Generate large dataset
        repo_count = 500
        files_per_repo = 3
        
        mock_repos = self.generate_mock_repositories(repo_count)
        mock_files = self.generate_mock_files(repo_count, files_per_repo)
        mock_contents = self.generate_mock_file_contents(mock_files)
        
        # Setup components
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock GitHub API responses
        github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=mock_repos,
            etag='"large-org-etag"'
        )
        
        def mock_search_files(repo, patterns, fast_mode=False):
            return mock_files.get(repo.full_name, [])
        
        github_client.search_files.side_effect = mock_search_files
        
        def mock_get_file_content(repo, path, etag=None):
            key = (repo.full_name, path)
            if key in mock_contents:
                return APIResponse(
                    data=mock_contents[key],
                    etag=f'"{path}-etag"'
                )
            return APIResponse(data=None, etag=None)
        
        github_client.get_file_content.side_effect = mock_get_file_content
        
        # Measure performance
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        start_time = time.time()
        results = scanner.scan()
        scan_time = time.time() - start_time
        
        # Performance assertions
        assert results.repositories_scanned > 0
        assert results.files_scanned > 0
        
        # Should complete within reasonable time (adjust based on system performance)
        max_time = 60.0  # 60 seconds for 500 repos
        assert scan_time < max_time, f"Large scan took {scan_time:.2f}s, expected < {max_time}s"
        
        # Memory usage should be reasonable (this is implicit - test shouldn't crash)
        print(f"Large organization scan: {repo_count} repos, {results.files_scanned} files in {scan_time:.2f}s")

    @pytest.mark.performance
    def test_cache_performance_improvement(self, temp_cache_dir, temp_issues_dir):
        """Test cache performance improvement across multiple scans."""
        config = ScanConfig(
            org="test-org",
            issues_dir=temp_issues_dir
        )
        
        # Generate moderate dataset for cache testing
        repo_count = 50
        files_per_repo = 5
        
        mock_repos = self.generate_mock_repositories(repo_count)
        mock_files = self.generate_mock_files(repo_count, files_per_repo)
        mock_contents = self.generate_mock_file_contents(mock_files)
        
        # First scan - populate cache
        cache_manager1 = CacheManager(cache_path=temp_cache_dir)
        ioc_loader1 = IOCLoader(issues_dir=temp_issues_dir)
        github_client1 = Mock(spec=GitHubClient)
        
        github_client1.get_organization_repos_graphql.return_value = APIResponse(
            data=mock_repos,
            etag='"org-etag"'
        )
        
        github_client1.search_files.side_effect = lambda repo, patterns, fast_mode=False: mock_files.get(repo.full_name, [])
        
        def mock_get_file_content1(repo, path, etag=None):
            key = (repo.full_name, path)
            if key in mock_contents:
                return APIResponse(
                    data=mock_contents[key],
                    etag=f'"{path}-etag"'
                )
            return APIResponse(data=None, etag=None)
        
        github_client1.get_file_content.side_effect = mock_get_file_content1
        
        scanner1 = GitHubIOCScanner(config, github_client1, cache_manager1, ioc_loader1)
        
        start_time = time.time()
        results1 = scanner1.scan()
        first_scan_time = time.time() - start_time
        
        # Second scan - use cache
        cache_manager2 = CacheManager(cache_path=temp_cache_dir)
        ioc_loader2 = IOCLoader(issues_dir=temp_issues_dir)
        github_client2 = Mock(spec=GitHubClient)
        
        # Return 304 Not Modified for cached content
        github_client2.get_organization_repos_graphql.return_value = APIResponse(
            data=None,
            etag='"org-etag"',
            not_modified=True
        )
        
        github_client2.search_files.side_effect = lambda repo, patterns, fast_mode=False: mock_files.get(repo.full_name, [])
        
        def mock_get_file_content2(repo, path, etag=None):
            return APIResponse(
                data=None,
                etag=f'"{path}-etag"',
                not_modified=True
            )
        
        github_client2.get_file_content.side_effect = mock_get_file_content2
        
        scanner2 = GitHubIOCScanner(config, github_client2, cache_manager2, ioc_loader2)
        
        start_time = time.time()
        results2 = scanner2.scan()
        second_scan_time = time.time() - start_time
        
        # Performance comparison
        performance_improvement = (first_scan_time - second_scan_time) / first_scan_time
        
        assert second_scan_time < first_scan_time, "Second scan should be faster"
        assert performance_improvement > 0.5, f"Cache improved performance by {performance_improvement:.1%}, expected > 50%"
        
        # Cache statistics should show hits
        assert results2.cache_stats.hits > 0
        assert results2.cache_stats.time_saved > 0
        
        print(f"Cache performance: First scan {first_scan_time:.2f}s, second scan {second_scan_time:.2f}s")
        print(f"Performance improvement: {performance_improvement:.1%}")

    @pytest.mark.performance
    def test_ioc_matching_performance(self, temp_cache_dir, temp_issues_dir):
        """Test IOC matching performance with many packages and IOCs."""
        config = ScanConfig(
            org="test-org",
            repo="test-repo",
            issues_dir=temp_issues_dir
        )
        
        # Generate file with many dependencies
        large_package_json = {
            "name": "large-app",
            "dependencies": {}
        }
        
        # Add 1000 dependencies
        for i in range(1000):
            large_package_json["dependencies"][f"package-{i:04d}"] = f"^{i % 10}.0.0"
        
        mock_file = FileInfo(path="package.json", sha="large-file", size=50000)
        mock_content = FileContent(
            content=json.dumps(large_package_json),
            sha="large-file",
            size=50000
        )
        
        # Setup components
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        github_client.search_files.return_value = [mock_file]
        github_client.get_file_content.return_value = APIResponse(
            data=mock_content,
            etag='"large-file-etag"'
        )
        
        # Measure IOC matching performance
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        start_time = time.time()
        results = scanner.scan()
        scan_time = time.time() - start_time
        
        # Should complete within reasonable time
        max_time = 10.0  # 10 seconds for 1000 packages vs 100 IOCs
        assert scan_time < max_time, f"IOC matching took {scan_time:.2f}s, expected < {max_time}s"
        
        assert results.files_scanned == 1
        print(f"IOC matching: 1000 packages vs 100 IOCs in {scan_time:.2f}s")

    @pytest.mark.performance
    def test_concurrent_file_processing_simulation(self, temp_cache_dir, temp_issues_dir):
        """Test performance characteristics that would benefit from concurrent processing."""
        config = ScanConfig(
            org="test-org",
            issues_dir=temp_issues_dir
        )
        
        # Generate many repositories with few files each (simulates concurrent processing scenario)
        repo_count = 100
        files_per_repo = 2
        
        mock_repos = self.generate_mock_repositories(repo_count)
        mock_files = self.generate_mock_files(repo_count, files_per_repo)
        mock_contents = self.generate_mock_file_contents(mock_files)
        
        # Setup components
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Add artificial delay to simulate network latency
        original_get_file_content = github_client.get_file_content
        
        def delayed_get_file_content(repo, path, etag=None):
            time.sleep(0.01)  # 10ms delay per file
            key = (repo.full_name, path)
            if key in mock_contents:
                return APIResponse(
                    data=mock_contents[key],
                    etag=f'"{path}-etag"'
                )
            return APIResponse(data=None, etag=None)
        
        github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=mock_repos,
            etag='"org-etag"'
        )
        
        github_client.search_files.side_effect = lambda repo, patterns, fast_mode=False: mock_files.get(repo.full_name, [])
        github_client.get_file_content.side_effect = delayed_get_file_content
        
        # Measure performance
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        start_time = time.time()
        results = scanner.scan()
        scan_time = time.time() - start_time
        
        total_files = sum(len(files) for files in mock_files.values())
        expected_min_time = total_files * 0.01  # Minimum time based on delays
        
        # Should complete reasonably close to minimum time (allowing for processing overhead)
        max_acceptable_time = expected_min_time * 2
        assert scan_time < max_acceptable_time, f"Scan took {scan_time:.2f}s, expected < {max_acceptable_time:.2f}s"
        
        print(f"Concurrent simulation: {total_files} files in {scan_time:.2f}s (min: {expected_min_time:.2f}s)")

    @pytest.mark.performance
    def test_memory_usage_large_scan(self, temp_cache_dir, temp_issues_dir):
        """Test memory usage characteristics during large scans."""
        import psutil
        import os
        
        config = ScanConfig(
            org="memory-test-org",
            issues_dir=temp_issues_dir
        )
        
        # Generate large dataset
        repo_count = 200
        files_per_repo = 4
        
        mock_repos = self.generate_mock_repositories(repo_count)
        mock_files = self.generate_mock_files(repo_count, files_per_repo)
        mock_contents = self.generate_mock_file_contents(mock_files)
        
        # Setup components
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=mock_repos,
            etag='"memory-org-etag"'
        )
        
        github_client.search_files.side_effect = lambda repo, patterns, fast_mode=False: mock_files.get(repo.full_name, [])
        
        def mock_get_file_content(repo, path, etag=None):
            key = (repo.full_name, path)
            if key in mock_contents:
                return APIResponse(
                    data=mock_contents[key],
                    etag=f'"{path}-etag"'
                )
            return APIResponse(data=None, etag=None)
        
        github_client.get_file_content.side_effect = mock_get_file_content
        
        # Measure memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        results = scanner.scan()
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory usage should be reasonable (less than 100MB increase for this test)
        max_memory_increase = 100  # MB
        assert memory_increase < max_memory_increase, f"Memory increased by {memory_increase:.1f}MB, expected < {max_memory_increase}MB"
        
        print(f"Memory usage: {initial_memory:.1f}MB -> {final_memory:.1f}MB (+{memory_increase:.1f}MB)")

    @pytest.mark.performance
    def test_fast_mode_performance_benefit(self, temp_cache_dir, temp_issues_dir):
        """Test that fast mode provides significant performance benefit."""
        # Test normal mode
        config_normal = ScanConfig(
            org="test-org",
            fast_mode=False,
            issues_dir=temp_issues_dir
        )
        
        # Test fast mode
        config_fast = ScanConfig(
            org="test-org",
            fast_mode=True,
            issues_dir=temp_issues_dir
        )
        
        # Generate repositories with nested files
        repo_count = 20
        mock_repos = self.generate_mock_repositories(repo_count)
        
        # Normal mode files (including nested)
        normal_files = {}
        fast_files = {}
        
        for i in range(repo_count):
            repo_name = f"test-org/repo-{i:04d}"
            
            # Normal mode: many files including nested
            normal_files[repo_name] = [
                FileInfo(path="package.json", sha=f"root-{i}", size=1024),
                FileInfo(path="nested/package.json", sha=f"nested-{i}", size=1024),
                FileInfo(path="deep/nested/yarn.lock", sha=f"deep-{i}", size=2048),
            ]
            
            # Fast mode: only root-level files
            fast_files[repo_name] = [
                FileInfo(path="package.json", sha=f"root-{i}", size=1024),
            ]
        
        # Test normal mode
        cache_manager1 = CacheManager(cache_path=temp_cache_dir + "_normal")
        ioc_loader1 = IOCLoader(issues_dir=temp_issues_dir)
        github_client1 = Mock(spec=GitHubClient)
        
        github_client1.get_organization_repos_graphql.return_value = APIResponse(data=mock_repos, etag='"org-etag"')
        github_client1.search_files.side_effect = lambda repo, patterns, fast_mode=False: normal_files.get(repo.full_name, [])
        github_client1.get_file_content.return_value = APIResponse(
            data=FileContent(content='{"dependencies": {}}', sha="mock", size=1024),
            etag='"mock-etag"'
        )
        
        scanner1 = GitHubIOCScanner(config_normal, github_client1, cache_manager1, ioc_loader1)
        
        start_time = time.time()
        results_normal = scanner1.scan()
        normal_time = time.time() - start_time
        
        # Test fast mode
        cache_manager2 = CacheManager(cache_path=temp_cache_dir + "_fast")
        ioc_loader2 = IOCLoader(issues_dir=temp_issues_dir)
        github_client2 = Mock(spec=GitHubClient)
        
        github_client2.get_organization_repos_graphql.return_value = APIResponse(data=mock_repos, etag='"org-etag"')
        github_client2.search_files.side_effect = lambda repo, patterns, fast_mode=True: fast_files.get(repo.full_name, [])
        github_client2.get_file_content.return_value = APIResponse(
            data=FileContent(content='{"dependencies": {}}', sha="mock", size=1024),
            etag='"mock-etag"'
        )
        
        scanner2 = GitHubIOCScanner(config_fast, github_client2, cache_manager2, ioc_loader2)
        
        start_time = time.time()
        results_fast = scanner2.scan()
        fast_time = time.time() - start_time
        
        # Fast mode should be significantly faster
        assert fast_time < normal_time, "Fast mode should be faster than normal mode"
        
        # Fast mode should scan fewer files
        assert results_fast.files_scanned < results_normal.files_scanned
        
        performance_improvement = (normal_time - fast_time) / normal_time
        assert performance_improvement > 0.2, f"Fast mode only improved performance by {performance_improvement:.1%}, expected > 20%"
        
        print(f"Fast mode benefit: Normal {normal_time:.2f}s ({results_normal.files_scanned} files), Fast {fast_time:.2f}s ({results_fast.files_scanned} files)")
        print(f"Performance improvement: {performance_improvement:.1%}")


class TestCachePerformance:
    """Specific performance tests for cache operations."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)

    @pytest.mark.performance
    def test_cache_write_performance(self, temp_cache_dir):
        """Test cache write performance with many entries."""
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        
        # Test writing many cache entries
        num_entries = 1000
        
        start_time = time.time()
        
        for i in range(num_entries):
            cache_manager.store_file_content(
                repo=f"org/repo-{i:04d}",
                path="package.json",
                sha=f"sha-{i}",
                content=f'{{"name": "package-{i}"}}',
                etag=f'"etag-{i}"'
            )
        
        write_time = time.time() - start_time
        
        # Should complete within reasonable time
        max_time = 5.0  # 5 seconds for 1000 entries
        assert write_time < max_time, f"Cache writes took {write_time:.2f}s, expected < {max_time}s"
        
        print(f"Cache write performance: {num_entries} entries in {write_time:.2f}s ({num_entries/write_time:.0f} entries/sec)")

    @pytest.mark.performance
    def test_cache_read_performance(self, temp_cache_dir):
        """Test cache read performance with many entries."""
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        
        # Populate cache
        num_entries = 1000
        
        for i in range(num_entries):
            cache_manager.store_file_content(
                repo=f"org/repo-{i:04d}",
                path="package.json",
                sha=f"sha-{i}",
                content=f'{{"name": "package-{i}"}}',
                etag=f'"etag-{i}"'
            )
        
        # Test reading performance
        start_time = time.time()
        
        hits = 0
        for i in range(num_entries):
            result = cache_manager.get_file_content(
                repo=f"org/repo-{i:04d}",
                path="package.json",
                sha=f"sha-{i}"
            )
            if result is not None:
                hits += 1
        
        read_time = time.time() - start_time
        
        # Should find all entries
        assert hits == num_entries
        
        # Should complete within reasonable time
        max_time = 2.0  # 2 seconds for 1000 reads
        assert read_time < max_time, f"Cache reads took {read_time:.2f}s, expected < {max_time}s"
        
        print(f"Cache read performance: {num_entries} reads in {read_time:.2f}s ({num_entries/read_time:.0f} reads/sec)")

    @pytest.mark.performance
    def test_cache_size_growth(self, temp_cache_dir):
        """Test cache size growth characteristics."""
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        
        # Add entries and measure size growth
        entry_counts = [100, 500, 1000, 2000]
        sizes = []
        
        for count in entry_counts:
            # Add entries up to this count
            current_entries = len(sizes) * (entry_counts[0] if len(sizes) == 0 else entry_counts[len(sizes)-1])
            entries_to_add = count - current_entries
            
            for i in range(current_entries, current_entries + entries_to_add):
                cache_manager.store_file_content(
                    repo=f"org/repo-{i:04d}",
                    path="package.json",
                    sha=f"sha-{i}",
                    content=f'{{"name": "package-{i}", "dependencies": {{"dep-{j}": "1.0.0" for j in range(10)}}}}',
                    etag=f'"etag-{i}"'
                )
            
            # Measure cache size
            cache_info = cache_manager.get_cache_info()
            sizes.append(cache_info["db_size_bytes"])
        
        # Verify reasonable size growth (should be roughly linear)
        for i in range(1, len(sizes)):
            growth_ratio = sizes[i] / sizes[i-1]
            entry_ratio = entry_counts[i] / entry_counts[i-1]
            
            # Size growth should be proportional to entry growth (within reasonable bounds)
            assert 0.5 < growth_ratio / entry_ratio < 2.0, f"Cache size growth not proportional: {growth_ratio:.2f} vs {entry_ratio:.2f}"
        
        print(f"Cache size growth: {entry_counts} entries -> {[s//1024 for s in sizes]} KB")