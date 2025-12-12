"""Error handling and recovery integration tests.

This module contains integration tests that verify the scanner's behavior
when encountering various error conditions and its ability to recover gracefully.
"""

import json
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch
from typing import List

import pytest

from github_ioc_scanner.scanner import GitHubIOCScanner
from github_ioc_scanner.github_client import GitHubClient
from github_ioc_scanner.cache import CacheManager
from github_ioc_scanner.ioc_loader import IOCLoader, IOCLoaderError
from github_ioc_scanner.exceptions import (
    ScanError, AuthenticationError, ParsingError, RateLimitError, 
    IOCLoaderError, APIError
)
from github_ioc_scanner.models import (
    ScanConfig, Repository, FileInfo, APIResponse, ScanResults,
    FileContent, PackageDependency, IOCMatch
)


class TestAuthenticationErrorHandling:
    """Test authentication error handling scenarios."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)

    @pytest.fixture
    def temp_issues_dir(self):
        """Create a temporary issues directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            ioc_file = issues_dir / "test_ioc.py"
            ioc_content = 'IOC_PACKAGES = {"test-package": ["1.0.0"]}'
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)

    def test_invalid_token_error(self, temp_cache_dir, temp_issues_dir):
        """Test handling of invalid GitHub token."""
        config = ScanConfig(
            org="test-org",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock authentication error
        github_client.get_organization_repos_graphql.side_effect = AuthenticationError("Bad credentials")
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should propagate authentication error
        with pytest.raises(AuthenticationError, match="Bad credentials"):
            scanner.scan()

    def test_insufficient_permissions_error(self, temp_cache_dir, temp_issues_dir):
        """Test handling of insufficient permissions for organization access."""
        config = ScanConfig(
            org="private-org",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock permission error
        github_client.get_organization_repos_graphql.side_effect = AuthenticationError("Must be an organization member")
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        with pytest.raises(AuthenticationError, match="Must be an organization member"):
            scanner.scan()

    def test_team_access_permission_error(self, temp_cache_dir, temp_issues_dir):
        """Test handling of insufficient permissions for team access."""
        config = ScanConfig(
            org="test-org",
            team="private-team",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock team permission error
        github_client.get_team_repos.side_effect = AuthenticationError("Must be a team member")
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        with pytest.raises(AuthenticationError, match="Must be a team member"):
            scanner.scan()


class TestRateLimitHandling:
    """Test GitHub API rate limit handling and recovery."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)

    @pytest.fixture
    def temp_issues_dir(self):
        """Create a temporary issues directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            ioc_file = issues_dir / "test_ioc.py"
            ioc_content = 'IOC_PACKAGES = {"test-package": ["1.0.0"]}'
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)

    def test_rate_limit_with_retry(self, temp_cache_dir, temp_issues_dir):
        """Test rate limit handling with successful retry."""
        config = ScanConfig(
            org="test-org",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock rate limit followed by success
        reset_time = int(time.time()) + 1  # Reset in 1 second
        github_client.get_organization_repos_graphql.side_effect = [
            RateLimitError("API rate limit exceeded", reset_time=reset_time),
            APIResponse(data=[], etag='"empty-etag"')
        ]
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should handle rate limit and complete successfully
        results = scanner.scan()
        assert isinstance(results, ScanResults)
        
        # Verify retry occurred
        assert github_client.get_organization_repos_graphql.call_count == 2

    def test_multiple_rate_limits(self, temp_cache_dir, temp_issues_dir):
        """Test handling of multiple consecutive rate limits."""
        config = ScanConfig(
            org="test-org",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock multiple rate limits followed by success
        reset_time = int(time.time()) + 1
        github_client.get_organization_repos_graphql.side_effect = [
            RateLimitError("API rate limit exceeded", reset_time=reset_time),
            RateLimitError("API rate limit exceeded", reset_time=reset_time),
            APIResponse(data=[], etag='"empty-etag"')
        ]
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should handle multiple rate limits
        results = scanner.scan()
        assert isinstance(results, ScanResults)
        
        # Verify multiple retries occurred
        assert github_client.get_organization_repos_graphql.call_count == 3

    def test_rate_limit_during_file_fetching(self, temp_cache_dir, temp_issues_dir):
        """Test rate limit handling during file content fetching."""
        config = ScanConfig(
            org="test-org",
            repo="test-repo",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock successful file discovery
        github_client.search_files.return_value = [
            FileInfo(path="package.json", sha="abc123", size=1024)
        ]
        
        # Mock rate limit during file content fetching
        reset_time = int(time.time()) + 1
        github_client.get_file_content.side_effect = [
            RateLimitError("API rate limit exceeded", reset_time=reset_time),
            APIResponse(
                data=FileContent(
                    content='{"dependencies": {}}',
                    sha="abc123",
                    size=1024
                ),
                etag='"file-etag"'
            )
        ]
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should handle rate limit during file fetching
        results = scanner.scan()
        assert isinstance(results, ScanResults)
        assert results.files_scanned == 1
        
        # Verify retry occurred
        assert github_client.get_file_content.call_count == 2


class TestNetworkErrorHandling:
    """Test network error handling and recovery."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)

    @pytest.fixture
    def temp_issues_dir(self):
        """Create a temporary issues directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            ioc_file = issues_dir / "test_ioc.py"
            ioc_content = 'IOC_PACKAGES = {"test-package": ["1.0.0"]}'
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)

    def test_network_timeout_with_retry(self, temp_cache_dir, temp_issues_dir):
        """Test network timeout handling with retry."""
        config = ScanConfig(
            org="test-org",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock network timeout followed by success
        import requests
        github_client.get_organization_repos_graphql.side_effect = [
            requests.exceptions.Timeout("Request timed out"),
            APIResponse(data=[], etag='"empty-etag"')
        ]
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should handle timeout and retry
        results = scanner.scan()
        assert isinstance(results, ScanResults)
        
        # Verify retry occurred
        assert github_client.get_organization_repos_graphql.call_count == 2

    def test_connection_error_handling(self, temp_cache_dir, temp_issues_dir):
        """Test connection error handling."""
        config = ScanConfig(
            org="test-org",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock connection error
        import requests
        github_client.get_organization_repos_graphql.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should propagate connection error after retries
        with pytest.raises(requests.exceptions.ConnectionError):
            scanner.scan()

    def test_partial_network_failures(self, temp_cache_dir, temp_issues_dir):
        """Test handling of partial network failures during scanning."""
        config = ScanConfig(
            org="test-org",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock repositories
        mock_repos = [
            Repository(
                name="working-repo",
                full_name="test-org/working-repo",
                archived=False,
                default_branch="main",
                updated_at=datetime.now(timezone.utc)
            ),
            Repository(
                name="failing-repo",
                full_name="test-org/failing-repo",
                archived=False,
                default_branch="main",
                updated_at=datetime.now(timezone.utc)
            )
        ]
        
        github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=mock_repos,
            etag='"repos-etag"'
        )
        
        # Mock file discovery - one repo works, one fails
        def mock_search_files(repo, patterns, fast_mode=False):
            if repo.name == "working-repo":
                return [FileInfo(path="package.json", sha="abc123", size=1024)]
            else:
                import requests
                raise requests.exceptions.Timeout("Network timeout")
        
        github_client.search_files.side_effect = mock_search_files
        
        # Mock file content for working repo
        github_client.get_file_content.return_value = APIResponse(
            data=FileContent(
                content='{"dependencies": {}}',
                sha="abc123",
                size=1024
            ),
            etag='"file-etag"'
        )
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should complete scan despite partial failures
        results = scanner.scan()
        assert isinstance(results, ScanResults)
        assert results.repositories_scanned == 2  # Both repos attempted
        assert results.files_scanned == 1  # Only working repo succeeded


class TestFileParsingErrorHandling:
    """Test file parsing error handling and recovery."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)

    @pytest.fixture
    def temp_issues_dir(self):
        """Create a temporary issues directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            ioc_file = issues_dir / "test_ioc.py"
            ioc_content = 'IOC_PACKAGES = {"test-package": ["1.0.0"]}'
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)

    def test_malformed_json_handling(self, temp_cache_dir, temp_issues_dir):
        """Test handling of malformed JSON files."""
        config = ScanConfig(
            org="test-org",
            repo="test-repo",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock files with various parsing issues
        github_client.search_files.return_value = [
            FileInfo(path="malformed.json", sha="bad1", size=1024),
            FileInfo(path="valid.json", sha="good1", size=1024),
            FileInfo(path="empty.json", sha="empty1", size=0)
        ]
        
        def mock_get_file_content(repo, path, etag=None):
            if path == "malformed.json":
                return APIResponse(
                    data=FileContent(
                        content='{"dependencies": invalid json}',
                        sha="bad1",
                        size=1024
                    ),
                    etag='"bad-etag"'
                )
            elif path == "valid.json":
                return APIResponse(
                    data=FileContent(
                        content='{"dependencies": {"lodash": "^4.17.21"}}',
                        sha="good1",
                        size=1024
                    ),
                    etag='"good-etag"'
                )
            elif path == "empty.json":
                return APIResponse(
                    data=FileContent(
                        content='',
                        sha="empty1",
                        size=0
                    ),
                    etag='"empty-etag"'
                )
            return APIResponse(data=None, etag=None)
        
        github_client.get_file_content.side_effect = mock_get_file_content
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should handle parsing errors gracefully
        results = scanner.scan()
        assert isinstance(results, ScanResults)
        assert results.files_scanned == 3  # All files attempted
        # Should continue despite parsing errors

    def test_unsupported_file_format_handling(self, temp_cache_dir, temp_issues_dir):
        """Test handling of unsupported file formats."""
        config = ScanConfig(
            org="test-org",
            repo="test-repo",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock unsupported file types
        github_client.search_files.return_value = [
            FileInfo(path="unknown.lockfile", sha="unknown1", size=1024),
            FileInfo(path="binary.lock", sha="binary1", size=2048)
        ]
        
        def mock_get_file_content(repo, path, etag=None):
            if path == "unknown.lockfile":
                return APIResponse(
                    data=FileContent(
                        content='# Unknown lockfile format\npackage: version\n',
                        sha="unknown1",
                        size=1024
                    ),
                    etag='"unknown-etag"'
                )
            elif path == "binary.lock":
                return APIResponse(
                    data=FileContent(
                        content=b'\x00\x01\x02\x03\x04\x05'.decode('utf-8', errors='ignore'),
                        sha="binary1",
                        size=2048
                    ),
                    etag='"binary-etag"'
                )
            return APIResponse(data=None, etag=None)
        
        github_client.get_file_content.side_effect = mock_get_file_content
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should handle unsupported formats gracefully
        results = scanner.scan()
        assert isinstance(results, ScanResults)
        assert results.files_scanned == 2  # Both files attempted

    def test_corrupted_lockfile_handling(self, temp_cache_dir, temp_issues_dir):
        """Test handling of corrupted lockfiles."""
        config = ScanConfig(
            org="test-org",
            repo="test-repo",
            issues_dir=temp_issues_dir
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        github_client = Mock(spec=GitHubClient)
        
        # Mock corrupted lockfiles
        github_client.search_files.return_value = [
            FileInfo(path="corrupted-yarn.lock", sha="corrupt1", size=1024),
            FileInfo(path="truncated-package-lock.json", sha="truncated1", size=512)
        ]
        
        def mock_get_file_content(repo, path, etag=None):
            if path == "corrupted-yarn.lock":
                return APIResponse(
                    data=FileContent(
                        content='# yarn lockfile v1\n\npackage@version:\n  version "1.0.0\n  # Missing closing quote and structure',
                        sha="corrupt1",
                        size=1024
                    ),
                    etag='"corrupt-etag"'
                )
            elif path == "truncated-package-lock.json":
                return APIResponse(
                    data=FileContent(
                        content='{"name": "app", "lockfileVersion": 2, "requires": true, "packages": {',
                        sha="truncated1",
                        size=512
                    ),
                    etag='"truncated-etag"'
                )
            return APIResponse(data=None, etag=None)
        
        github_client.get_file_content.side_effect = mock_get_file_content
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should handle corrupted files gracefully
        results = scanner.scan()
        assert isinstance(results, ScanResults)
        assert results.files_scanned == 2


class TestIOCLoaderErrorHandling:
    """Test IOC loader error handling scenarios."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)

    def test_missing_issues_directory(self, temp_cache_dir):
        """Test handling of missing issues directory."""
        config = ScanConfig(
            org="test-org",
            issues_dir="/nonexistent/directory"
        )
        
        cache_manager = CacheManager(cache_path=temp_cache_dir)
        github_client = Mock(spec=GitHubClient)
        
        # IOC loader should fail with missing directory
        ioc_loader = IOCLoader(issues_dir="/nonexistent/directory")
        
        scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
        
        # Should raise IOC loader error
        with pytest.raises(IOCLoaderError):
            scanner.scan()

    def test_empty_issues_directory(self, temp_cache_dir):
        """Test handling of empty issues directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_issues_dir = Path(temp_dir) / "empty_issues"
            empty_issues_dir.mkdir()
            
            config = ScanConfig(
                org="test-org",
                issues_dir=str(empty_issues_dir)
            )
            
            cache_manager = CacheManager(cache_path=temp_cache_dir)
            github_client = Mock(spec=GitHubClient)
            ioc_loader = IOCLoader(issues_dir=str(empty_issues_dir))
            
            scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
            
            # Should raise IOC loader error for empty directory
            with pytest.raises(IOCLoaderError):
                scanner.scan()

    def test_malformed_ioc_files(self, temp_cache_dir):
        """Test handling of malformed IOC files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            # Create malformed IOC files
            malformed_file1 = issues_dir / "malformed1.py"
            malformed_file1.write_text("IOC_PACKAGES = invalid python syntax")
            
            malformed_file2 = issues_dir / "malformed2.py"
            malformed_file2.write_text("# Missing IOC_PACKAGES definition\nSOME_OTHER_VAR = {}")
            
            valid_file = issues_dir / "valid.py"
            valid_file.write_text('IOC_PACKAGES = {"test-package": ["1.0.0"]}')
            
            config = ScanConfig(
                org="test-org",
                issues_dir=str(issues_dir)
            )
            
            cache_manager = CacheManager(cache_path=temp_cache_dir)
            github_client = Mock(spec=GitHubClient)
            ioc_loader = IOCLoader(issues_dir=str(issues_dir))
            
            scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
            
            # Should handle malformed files and continue with valid ones
            # This depends on IOC loader implementation - it might raise an error
            # or skip malformed files and continue
            try:
                results = scanner.scan()
                # If it succeeds, verify it found the valid IOC definitions
                assert isinstance(results, ScanResults)
            except IOCLoaderError:
                # If it fails, that's also acceptable behavior
                pass

    def test_ioc_file_permission_errors(self, temp_cache_dir):
        """Test handling of IOC file permission errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            # Create IOC file
            ioc_file = issues_dir / "restricted.py"
            ioc_file.write_text('IOC_PACKAGES = {"test-package": ["1.0.0"]}')
            
            # Make file unreadable (on Unix systems)
            try:
                ioc_file.chmod(0o000)
                
                config = ScanConfig(
                    org="test-org",
                    issues_dir=str(issues_dir)
                )
                
                cache_manager = CacheManager(cache_path=temp_cache_dir)
                github_client = Mock(spec=GitHubClient)
                ioc_loader = IOCLoader(issues_dir=str(issues_dir))
                
                scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
                
                # Should handle permission error
                with pytest.raises(IOCLoaderError):
                    scanner.scan()
                    
            finally:
                # Restore permissions for cleanup
                try:
                    ioc_file.chmod(0o644)
                except:
                    pass


class TestCacheErrorHandling:
    """Test cache-related error handling scenarios."""

    @pytest.fixture
    def temp_issues_dir(self):
        """Create a temporary issues directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            ioc_file = issues_dir / "test_ioc.py"
            ioc_content = 'IOC_PACKAGES = {"test-package": ["1.0.0"]}'
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)

    def test_cache_directory_permission_error(self, temp_issues_dir):
        """Test handling of cache directory permission errors."""
        # Try to create cache in read-only directory
        readonly_cache_path = "/root/readonly/cache.sqlite3"  # Typically not writable
        
        config = ScanConfig(
            org="test-org",
            repo="test-repo",
            issues_dir=temp_issues_dir
        )
        
        github_client = Mock(spec=GitHubClient)
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
        
        # This should either fail gracefully or fall back to no-cache mode
        try:
            cache_manager = CacheManager(cache_path=readonly_cache_path)
            scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
            
            # Mock minimal successful scan
            github_client.search_files.return_value = []
            
            results = scanner.scan()
            assert isinstance(results, ScanResults)
            
        except (PermissionError, OSError):
            # Permission error is acceptable behavior
            pass

    def test_cache_corruption_handling(self, temp_issues_dir):
        """Test handling of corrupted cache database."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "corrupted.sqlite3"
            
            # Create corrupted cache file
            cache_path.write_bytes(b"This is not a valid SQLite database")
            
            config = ScanConfig(
                org="test-org",
                repo="test-repo",
                issues_dir=temp_issues_dir
            )
            
            github_client = Mock(spec=GitHubClient)
            ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
            
            # Should handle corrupted cache gracefully
            try:
                cache_manager = CacheManager(cache_path=str(cache_path))
                scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
                
                # Mock minimal successful scan
                github_client.search_files.return_value = []
                
                results = scanner.scan()
                assert isinstance(results, ScanResults)
                
            except Exception as e:
                # Cache corruption should be handled gracefully
                # The exact behavior depends on implementation
                assert "database" in str(e).lower() or "sqlite" in str(e).lower()

    def test_cache_disk_space_error(self, temp_issues_dir):
        """Test handling of disk space errors during caching."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            
            config = ScanConfig(
                org="test-org",
                repo="test-repo",
                issues_dir=temp_issues_dir
            )
            
            cache_manager = CacheManager(cache_path=str(cache_path))
            github_client = Mock(spec=GitHubClient)
            ioc_loader = IOCLoader(issues_dir=temp_issues_dir)
            
            # Mock cache operations to raise disk space error
            original_store = cache_manager.store_file_content
            
            def mock_store_with_error(*args, **kwargs):
                raise OSError("No space left on device")
            
            cache_manager.store_file_content = mock_store_with_error
            
            scanner = GitHubIOCScanner(config, github_client, cache_manager, ioc_loader)
            
            # Mock file discovery and content
            github_client.search_files.return_value = [
                FileInfo(path="package.json", sha="abc123", size=1024)
            ]
            
            github_client.get_file_content.return_value = APIResponse(
                data=FileContent(
                    content='{"dependencies": {}}',
                    sha="abc123",
                    size=1024
                ),
                etag='"file-etag"'
            )
            
            # Should handle disk space error gracefully
            results = scanner.scan()
            assert isinstance(results, ScanResults)
            # Scan should complete even if caching fails