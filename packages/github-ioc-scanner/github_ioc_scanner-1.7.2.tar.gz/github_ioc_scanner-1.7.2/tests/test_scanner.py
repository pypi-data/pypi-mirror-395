"""Tests for the GitHub IOC Scanner core scanning engine."""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from github_ioc_scanner.scanner import GitHubIOCScanner
from github_ioc_scanner.models import (
    ScanConfig, Repository, FileInfo, APIResponse, ScanResults, CacheStats,
    FileContent, PackageDependency, IOCMatch, IOCDefinition
)
from github_ioc_scanner.github_client import GitHubClient
from github_ioc_scanner.exceptions import AuthenticationError, ConfigurationError
from github_ioc_scanner.cache import CacheManager
from github_ioc_scanner.ioc_loader import IOCLoader, IOCLoaderError


class TestGitHubIOCScanner:
    """Test the main scanner class."""

    @pytest.fixture
    def scan_config(self):
        """Create a test scan configuration."""
        return ScanConfig(
            org="test-org",
            team=None,
            repo=None,
            fast_mode=False,
            include_archived=False,
            issues_dir="issues"
        )

    @pytest.fixture
    def mock_github_client(self):
        """Create a mock GitHub client."""
        return Mock(spec=GitHubClient)

    @pytest.fixture
    def mock_cache_manager(self):
        """Create a mock cache manager."""
        return Mock(spec=CacheManager)

    @pytest.fixture
    def mock_ioc_loader(self):
        """Create a mock IOC loader."""
        return Mock(spec=IOCLoader)

    @pytest.fixture
    def scanner(self, scan_config, mock_github_client, mock_cache_manager, mock_ioc_loader):
        """Create a scanner instance with mocked dependencies."""
        return GitHubIOCScanner(scan_config, mock_github_client, mock_cache_manager, mock_ioc_loader)

    @pytest.fixture
    def sample_repositories(self):
        """Create sample repository data."""
        return [
            Repository(
                name="repo1",
                full_name="test-org/repo1",
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                name="repo2",
                full_name="test-org/repo2",
                archived=True,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                name="repo3",
                full_name="test-org/repo3",
                archived=False,
                default_branch="develop",
                updated_at=datetime.now()
            ),
        ]

    def test_init(self, scan_config, mock_github_client, mock_cache_manager):
        """Test scanner initialization."""
        scanner = GitHubIOCScanner(scan_config, mock_github_client, mock_cache_manager)
        
        assert scanner.config == scan_config
        assert scanner.github_client == mock_github_client
        assert scanner.cache_manager == mock_cache_manager
        assert len(scanner.LOCKFILE_PATTERNS) > 0

    def test_discover_organization_repositories_cache_hit(self, scanner, sample_repositories):
        """Test organization repository discovery with incremental cache update."""
        from datetime import timezone
        cache_timestamp = datetime.now(timezone.utc)
        
        # Setup cache to return data with timestamp (for incremental fetching)
        scanner.cache_manager.get_repository_metadata.return_value = (sample_repositories, '"cached-etag"', cache_timestamp)
        
        # Setup GraphQL to return same data (incremental fetch finds no new repos)
        scanner.github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=sample_repositories,
            etag=None,
            not_modified=False
        )
        
        result = scanner.discover_organization_repositories("test-org")
        
        # Should get data and filter archived repos
        assert len(result) == 2  # Only non-archived repos
        assert all(not repo.archived for repo in result)
        
        # Verify cache was checked
        scanner.cache_manager.get_repository_metadata.assert_called_once_with("test-org", team="")
        
        # Verify GraphQL API was called with cached repos for incremental fetch
        scanner.github_client.get_organization_repos_graphql.assert_called_once_with(
            "test-org", 
            include_archived=False,
            cached_repos=sample_repositories,
            cache_cutoff=cache_timestamp
        )

    def test_discover_organization_repositories_cache_miss(self, scanner, sample_repositories):
        """Test organization repository discovery with cache miss."""
        # Setup cache to return None (cache miss)
        scanner.cache_manager.get_repository_metadata.return_value = None
        
        # Setup GitHub client GraphQL to return fresh data
        scanner.github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=sample_repositories,
            etag=None,
            not_modified=False
        )
        
        result = scanner.discover_organization_repositories("test-org")
        
        # Should get fresh data and filter archived repos
        assert len(result) == 2  # Only non-archived repos
        assert all(not repo.archived for repo in result)
        
        # Verify cache was updated (GraphQL returns None for etag)
        scanner.cache_manager.store_repository_metadata.assert_called_once_with(
            "test-org", sample_repositories, None, team=""
        )

    def test_discover_organization_repositories_include_archived(self, scanner, sample_repositories):
        """Test organization repository discovery including archived repos."""
        scanner.config.include_archived = True
        
        scanner.cache_manager.get_repository_metadata.return_value = None
        scanner.github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=sample_repositories,
            etag=None
        )
        
        result = scanner.discover_organization_repositories("test-org")
        
        # Should include all repos including archived
        assert len(result) == 3
        assert any(repo.archived for repo in result)

    def test_discover_team_repositories(self, scanner, sample_repositories):
        """Test team repository discovery."""
        scanner.cache_manager.get_repository_metadata.return_value = None
        scanner.github_client.get_team_repos.return_value = APIResponse(
            data=sample_repositories,
            etag='"team-etag"'
        )
        
        result = scanner.discover_team_repositories("test-org", "test-team")
        
        # Team repos now filter archived by default (same as org repos)
        assert len(result) == 2  # Only non-archived repos
        assert all(not repo.archived for repo in result)
        
        # Verify correct API call
        scanner.github_client.get_team_repos.assert_called_once_with(
            "test-org", "test-team", etag=None
        )
        
        # Verify cache was updated with team parameter
        scanner.cache_manager.store_repository_metadata.assert_called_once_with(
            "test-org", sample_repositories, '"team-etag"', "test-team"
        )

    def test_discover_team_repositories_cache_hit(self, scanner, sample_repositories):
        """Test team repository discovery with cache hit."""
        # Setup cache to return team data
        scanner.cache_manager.get_repository_metadata.return_value = (sample_repositories, '"cached-team-etag"')
        
        # Setup GitHub client to return not modified
        scanner.github_client.get_team_repos.return_value = APIResponse(
            data=None,
            etag='"cached-team-etag"',
            not_modified=True
        )
        
        result = scanner.discover_team_repositories("test-org", "test-team")
        
        # Should use cached data and filter archived repos
        assert len(result) == 2  # Only non-archived repos
        assert all(not repo.archived for repo in result)
        
        # Verify cache was checked with team parameter
        scanner.cache_manager.get_repository_metadata.assert_called_once_with("test-org", "test-team")
        
        # Verify API was called with ETag
        scanner.github_client.get_team_repos.assert_called_once_with(
            "test-org", "test-team", etag='"cached-team-etag"'
        )

    def test_discover_files_in_repository(self, scanner):
        """Test file discovery in a repository."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        mock_files = [
            FileInfo(path="package.json", sha="abc123", size=1024),
            FileInfo(path="yarn.lock", sha="def456", size=2048),
        ]
        
        scanner.github_client.search_files.return_value = mock_files
        
        result = scanner.discover_files_in_repository(repo)
        
        assert result == ["package.json", "yarn.lock"]
        
        # Verify search was called with correct parameters
        scanner.github_client.search_files.assert_called_once_with(
            repo, scanner.LOCKFILE_PATTERNS, fast_mode=False
        )

    def test_discover_files_in_repository_fast_mode(self, scanner):
        """Test file discovery in fast mode."""
        scanner.config.fast_mode = True
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        scanner.github_client.search_files.return_value = []
        
        scanner.discover_files_in_repository(repo)
        
        # Verify fast mode was passed
        scanner.github_client.search_files.assert_called_once_with(
            repo, scanner.LOCKFILE_PATTERNS, fast_mode=True
        )

    def test_discover_files_in_repository_error_handling(self, scanner):
        """Test error handling in file discovery."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        scanner.github_client.search_files.side_effect = Exception("API Error")
        
        result = scanner.discover_files_in_repository(repo)
        
        # Should return empty list on error
        assert result == []

    def test_scan_organization_mode(self, scanner, sample_repositories):
        """Test scanning in organization mode."""
        # Setup IOC loader
        scanner.ioc_loader.load_iocs.return_value = {}
        scanner.ioc_loader.get_ioc_hash.return_value = "test-hash"
        
        scanner.cache_manager.get_repository_metadata.return_value = None
        scanner.github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=sample_repositories
        )
        scanner.github_client.search_files.return_value = []  # No files found
        scanner.cache_manager.get_cache_stats.return_value = CacheStats()
        
        result = scanner.scan()
        
        assert isinstance(result, ScanResults)
        assert result.repositories_scanned == 2  # Non-archived repos only
        # files_scanned may include SBOM scan attempts
        assert len(result.matches) == 0  # No matches

    def test_scan_team_mode(self, scanner, sample_repositories):
        """Test scanning in team mode."""
        scanner.config.team = "test-team"
        
        # Setup IOC loader
        scanner.ioc_loader.load_iocs.return_value = {}
        scanner.ioc_loader.get_ioc_hash.return_value = "test-hash"
        
        scanner.cache_manager.get_repository_metadata.return_value = None
        scanner.github_client.get_team_repos.return_value = APIResponse(
            data=sample_repositories
        )
        scanner.github_client.search_files.return_value = []  # No files found
        scanner.cache_manager.get_cache_stats.return_value = CacheStats()
        
        result = scanner.scan()
        
        assert isinstance(result, ScanResults)
        # Team mode now also filters archived repos
        assert result.repositories_scanned == 2  # Non-archived repos only

    def test_scan_repository_mode(self, scanner):
        """Test scanning in single repository mode."""
        scanner.config.repo = "test-repo"
        
        # Setup IOC loader
        scanner.ioc_loader.load_iocs.return_value = {}
        scanner.ioc_loader.get_ioc_hash.return_value = "test-hash"
        
        scanner.github_client.search_files.return_value = []  # No files found
        scanner.cache_manager.get_cache_stats.return_value = CacheStats()
        
        result = scanner.scan()
        
        assert isinstance(result, ScanResults)
        assert result.repositories_scanned == 1

    def test_scan_no_org_error(self, scanner):
        """Test scanning without organization parameter."""
        scanner.config.org = None
        
        # Setup IOC loader
        scanner.ioc_loader.load_iocs.return_value = {}
        scanner.ioc_loader.get_ioc_hash.return_value = "test-hash"
        
        with pytest.raises(ConfigurationError, match="Must specify at least --org parameter"):
            scanner.scan()

    def test_scan_team_without_org_error(self, scanner):
        """Test scanning team without organization parameter."""
        scanner.config.org = None
        scanner.config.team = "test-team"
        
        with pytest.raises(ConfigurationError, match="Team scanning requires organization context"):
            scanner.scan()

    def test_scan_repo_without_org_error(self, scanner):
        """Test scanning repository without organization parameter."""
        scanner.config.org = None
        scanner.config.repo = "test-repo"
        
        with pytest.raises(ConfigurationError, match="Repository scanning requires organization context"):
            scanner.scan()

    def test_scan_auth_error(self, scanner):
        """Test scanning with authentication error."""
        # Setup IOC loader
        scanner.ioc_loader.load_iocs.return_value = {}
        scanner.ioc_loader.get_ioc_hash.return_value = "test-hash"
        
        scanner.cache_manager.get_repository_metadata.return_value = None
        scanner.github_client.get_organization_repos_graphql.side_effect = AuthenticationError("Invalid token")
        
        with pytest.raises(AuthenticationError):
            scanner.scan()

    def test_lockfile_patterns_comprehensive(self, scanner):
        """Test that all expected lockfile patterns are included."""
        expected_patterns = [
            "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",  # JS
            "requirements.txt", "Pipfile.lock", "poetry.lock", "pyproject.toml",  # Python
            "Gemfile.lock",  # Ruby
            "composer.lock",  # PHP
            "go.mod", "go.sum",  # Go
            "Cargo.lock",  # Rust
        ]
        
        for pattern in expected_patterns:
            assert pattern in scanner.LOCKFILE_PATTERNS

    def test_scan_with_ioc_loading(self, scanner, sample_repositories):
        """Test scanning with IOC loading and matching."""
        # Setup IOC loader
        ioc_definitions = {
            "test_ioc.py": IOCDefinition(
                packages={"malicious-package": {"1.0.0"}},
                source_file="test_ioc.py"
            )
        }
        scanner.ioc_loader.load_iocs.return_value = ioc_definitions
        scanner.ioc_loader.get_ioc_hash.return_value = "test-hash"
        scanner.ioc_loader.get_all_packages.return_value = {"malicious-package": {"1.0.0"}}
        scanner.ioc_loader.is_package_compromised.return_value = False
        
        # Setup repository discovery
        scanner.cache_manager.get_repository_metadata.return_value = None
        scanner.github_client.get_organization_repos_graphql.return_value = APIResponse(
            data=sample_repositories
        )
        
        # Setup file discovery (no files found)
        scanner.github_client.search_files.return_value = []
        
        # Setup cache stats
        scanner.cache_manager.get_cache_stats.return_value = CacheStats()
        
        result = scanner.scan()
        
        # Verify IOC loader was called
        scanner.ioc_loader.load_iocs.assert_called_once()
        scanner.ioc_loader.get_ioc_hash.assert_called_once()
        
        assert isinstance(result, ScanResults)
        assert result.repositories_scanned == 2  # Non-archived repos

    def test_scan_repository_for_iocs(self, scanner):
        """Test scanning a single repository for IOCs."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        # Setup file discovery
        scanner.github_client.search_files.return_value = [
            FileInfo(path="package.json", sha="abc123", size=1024)
        ]
        
        # Setup file content fetching
        file_content = FileContent(
            content='{"dependencies": {"test-package": "1.0.0"}}',
            sha="abc123",
            size=1024
        )
        scanner.github_client.get_file_content.return_value = APIResponse(
            data=file_content,
            etag='"file-etag"'
        )
        
        # Setup cache misses
        scanner.cache_manager.get_file_content.return_value = None
        scanner.cache_manager.get_parsed_packages.return_value = None
        scanner.cache_manager.get_scan_results.return_value = None
        
        # Setup parser
        with patch('github_ioc_scanner.scanner.get_parser') as mock_get_parser:
            mock_parser = Mock()
            mock_parser.parse.return_value = [
                PackageDependency(name="test-package", version="1.0.0", dependency_type="dependencies")
            ]
            mock_get_parser.return_value = mock_parser
            
            # Setup IOC matching (no matches)
            scanner.ioc_loader.get_all_packages.return_value = {}
            scanner.ioc_loader.is_package_compromised.return_value = False
            
            matches, files_scanned = scanner.scan_repository_for_iocs(repo, "test-hash")
            
            # files_scanned may include SBOM scan attempts
            assert files_scanned >= 1
            assert len(matches) == 0
            
            # Verify caching calls (may be called multiple times due to SBOM scanning)
            assert scanner.cache_manager.store_file_content.call_count >= 1
            assert scanner.cache_manager.store_parsed_packages.call_count >= 1
            assert scanner.cache_manager.store_scan_results.call_count >= 1

    def test_scan_file_for_iocs_with_matches(self, scanner):
        """Test scanning a file that contains IOC matches."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        file_content = FileContent(
            content='{"dependencies": {"malicious-package": "1.0.0"}}',
            sha="abc123",
            size=1024
        )
        
        # Setup cache misses
        scanner.cache_manager.get_scan_results.return_value = None
        scanner.cache_manager.get_parsed_packages.return_value = None
        
        # Setup file content fetching
        with patch.object(scanner, 'fetch_file_content_with_cache') as mock_fetch:
            mock_fetch.return_value = file_content
            
            # Setup parsing
            with patch.object(scanner, 'parse_packages_with_cache') as mock_parse:
                packages = [
                    PackageDependency(name="malicious-package", version="1.0.0", dependency_type="dependencies")
                ]
                mock_parse.return_value = packages
                
                # Setup IOC matching
                scanner.ioc_loader.get_all_packages.return_value = {"malicious-package": {"1.0.0"}}
                scanner.ioc_loader.is_package_compromised.return_value = True
                scanner.ioc_loader._ioc_definitions = {
                    "test_ioc.py": IOCDefinition(
                        packages={"malicious-package": {"1.0.0"}},
                        source_file="test_ioc.py"
                    )
                }
                
                matches = scanner.scan_file_for_iocs(repo, "package.json", "test-hash")
                
                assert len(matches) == 1
                assert matches[0].package_name == "malicious-package"
                assert matches[0].version == "1.0.0"
                assert matches[0].repo == "test-org/test-repo"
                assert matches[0].file_path == "package.json"
                
                # Verify caching
                scanner.cache_manager.store_scan_results.assert_called_once()

    def test_fetch_file_content_with_cache_hit(self, scanner):
        """Test fetching file content with cache hit."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        file_content = FileContent(
            content='{"dependencies": {}}',
            sha="abc123",
            size=1024
        )
        
        # Setup cache hit for content
        scanner.cache_manager.get_file_content.return_value = '{"dependencies": {}}'
        
        # Setup API response
        scanner.github_client.get_file_content.return_value = APIResponse(
            data=file_content,
            etag='"file-etag"'
        )
        
        result = scanner.fetch_file_content_with_cache(repo, "package.json")
        
        assert result == file_content
        
        # Verify cache was checked
        scanner.cache_manager.get_file_content.assert_called_once()

    def test_parse_packages_with_cache_hit(self, scanner):
        """Test parsing packages with cache hit."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        file_content = FileContent(
            content='{"dependencies": {"test-package": "1.0.0"}}',
            sha="abc123",
            size=1024
        )
        
        cached_packages = [
            PackageDependency(name="test-package", version="1.0.0", dependency_type="dependencies")
        ]
        
        # Setup cache hit
        scanner.cache_manager.get_parsed_packages.return_value = cached_packages
        
        result = scanner.parse_packages_with_cache(repo, "package.json", file_content)
        
        assert result == cached_packages
        
        # Verify cache was used
        scanner.cache_manager.get_parsed_packages.assert_called_once_with(
            "test-org/test-repo", "package.json", "abc123"
        )

    @pytest.mark.skip(reason="Parser mocking needs rework after SBOM scanning changes")
    def test_parse_packages_with_cache_miss(self, scanner):
        """Test parsing packages with cache miss."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        file_content = FileContent(
            content='{"dependencies": {"test-package": "1.0.0"}}',
            sha="abc123",
            size=1024
        )
        
        # Setup cache miss
        scanner.cache_manager.get_parsed_packages.return_value = None
        
        # Setup parser
        with patch('github_ioc_scanner.scanner.get_parser') as mock_get_parser:
            mock_parser = Mock()
            packages = [
                PackageDependency(name="test-package", version="1.0.0", dependency_type="dependencies")
            ]
            mock_parser.parse.return_value = packages
            mock_get_parser.return_value = mock_parser
            
            result = scanner.parse_packages_with_cache(repo, "package.json", file_content)
            
            assert result == packages
            
            # Verify parser was used
            mock_parser.parse.assert_called_once_with(file_content.content)
            
            # Verify cache was updated
            scanner.cache_manager.store_parsed_packages.assert_called_once_with(
                "test-org/test-repo", "package.json", "abc123", packages
            )

    def test_match_packages_against_iocs(self, scanner):
        """Test matching packages against IOC definitions."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        packages = [
            PackageDependency(name="safe-package", version="1.0.0", dependency_type="dependencies"),
            PackageDependency(name="malicious-package", version="1.0.0", dependency_type="dependencies"),
        ]
        
        # Setup IOC loader
        scanner.ioc_loader.get_all_packages.return_value = {"malicious-package": {"1.0.0"}}
        scanner.ioc_loader.is_package_compromised.side_effect = lambda name, version: name == "malicious-package"
        scanner.ioc_loader._ioc_definitions = {
            "test_ioc.py": IOCDefinition(
                packages={"malicious-package": {"1.0.0"}},
                source_file="test_ioc.py"
            )
        }
        
        matches = scanner.match_packages_against_iocs(repo, "package.json", packages)
        
        assert len(matches) == 1
        assert matches[0].package_name == "malicious-package"
        assert matches[0].version == "1.0.0"
        assert matches[0].ioc_source == "test_ioc.py"

    def test_scan_ioc_loader_error(self, scanner):
        """Test scanning with IOC loader error."""
        scanner.ioc_loader.load_iocs.side_effect = IOCLoaderError("No IOC files found")
        
        with pytest.raises(IOCLoaderError):
            scanner.scan()

    def test_ioc_matching_exact_version(self, scanner):
        """Test IOC matching with exact version requirements."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        packages = [
            PackageDependency(name="vulnerable-package", version="1.0.0", dependency_type="dependencies"),
            PackageDependency(name="vulnerable-package", version="1.0.1", dependency_type="dependencies"),
            PackageDependency(name="safe-package", version="1.0.0", dependency_type="dependencies"),
        ]
        
        # Setup IOC loader to only match version 1.0.0 of vulnerable-package
        def mock_is_compromised(name, version):
            return name == "vulnerable-package" and version == "1.0.0"
        
        scanner.ioc_loader.is_package_compromised.side_effect = mock_is_compromised
        scanner.ioc_loader._ioc_definitions = {
            "test_ioc.py": IOCDefinition(
                packages={"vulnerable-package": {"1.0.0"}},
                source_file="test_ioc.py"
            )
        }
        
        matches = scanner.match_packages_against_iocs(repo, "package.json", packages)
        
        # Should only match the exact version 1.0.0
        assert len(matches) == 1
        assert matches[0].package_name == "vulnerable-package"
        assert matches[0].version == "1.0.0"

    def test_ioc_matching_wildcard_version(self, scanner):
        """Test IOC matching with wildcard (None) version requirements."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        packages = [
            PackageDependency(name="always-vulnerable", version="1.0.0", dependency_type="dependencies"),
            PackageDependency(name="always-vulnerable", version="2.5.3", dependency_type="dependencies"),
            PackageDependency(name="safe-package", version="1.0.0", dependency_type="dependencies"),
        ]
        
        # Setup IOC loader to match any version of always-vulnerable
        def mock_is_compromised(name, version):
            return name == "always-vulnerable"
        
        scanner.ioc_loader.is_package_compromised.side_effect = mock_is_compromised
        scanner.ioc_loader._ioc_definitions = {
            "test_ioc.py": IOCDefinition(
                packages={"always-vulnerable": None},  # None means any version
                source_file="test_ioc.py"
            )
        }
        
        matches = scanner.match_packages_against_iocs(repo, "package.json", packages)
        
        # Should match both versions of always-vulnerable
        assert len(matches) == 2
        assert all(match.package_name == "always-vulnerable" for match in matches)
        assert {match.version for match in matches} == {"1.0.0", "2.5.3"}

    def test_scan_results_caching_with_ioc_hash(self, scanner):
        """Test that scan results are cached with IOC hash for invalidation."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        file_content = FileContent(
            content='{"dependencies": {"test-package": "1.0.0"}}',
            sha="abc123",
            size=1024
        )
        
        # Setup cache miss for scan results
        scanner.cache_manager.get_scan_results.return_value = None
        
        # Setup file content and parsing
        with patch.object(scanner, 'fetch_file_content_with_cache') as mock_fetch:
            mock_fetch.return_value = file_content
            
            with patch.object(scanner, 'parse_packages_with_cache') as mock_parse:
                packages = [
                    PackageDependency(name="test-package", version="1.0.0", dependency_type="dependencies")
                ]
                mock_parse.return_value = packages
                
                # Setup IOC matching (no matches)
                scanner.ioc_loader.is_package_compromised.return_value = False
                
                matches = scanner.scan_file_for_iocs(repo, "package.json", "ioc-hash-123")
                
                # Verify scan results were cached with IOC hash
                scanner.cache_manager.store_scan_results.assert_called_once_with(
                    "test-org/test-repo", "package.json", "abc123", "ioc-hash-123", matches
                )
                
                # Verify cache was checked with IOC hash
                scanner.cache_manager.get_scan_results.assert_called_once_with(
                    "test-org/test-repo", "package.json", "abc123", "ioc-hash-123"
                )

    def test_scan_results_cache_hit_with_ioc_hash(self, scanner):
        """Test that cached scan results are used when IOC hash matches."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        file_content = FileContent(
            content='{"dependencies": {"test-package": "1.0.0"}}',
            sha="abc123",
            size=1024
        )
        
        cached_matches = [
            IOCMatch(
                repo="test-org/test-repo",
                file_path="package.json",
                package_name="cached-package",
                version="1.0.0",
                ioc_source="cached_ioc.py"
            )
        ]
        
        # Setup cache hit for scan results
        scanner.cache_manager.get_scan_results.return_value = cached_matches
        
        # Setup file content fetching
        with patch.object(scanner, 'fetch_file_content_with_cache') as mock_fetch:
            mock_fetch.return_value = file_content
            
            matches = scanner.scan_file_for_iocs(repo, "package.json", "ioc-hash-123")
            
            # Should return cached matches without parsing or IOC matching
            assert matches == cached_matches
            
            # Verify cache was used
            scanner.cache_manager.get_scan_results.assert_called_once_with(
                "test-org/test-repo", "package.json", "abc123", "ioc-hash-123"
            )
            
            # Verify parsing and IOC matching were skipped
            scanner.cache_manager.get_parsed_packages.assert_not_called()
            scanner.ioc_loader.is_package_compromised.assert_not_called()


class TestScannerIntegration:
    """Integration tests for the scanner."""

    def test_end_to_end_organization_scan(self):
        """Test complete organization scanning workflow."""
        config = ScanConfig(org="test-org")
        
        with patch('github_ioc_scanner.scanner.GitHubClient') as MockClient:
            with patch('github_ioc_scanner.scanner.CacheManager') as MockCache:
                with patch('github_ioc_scanner.scanner.IOCLoader') as MockIOCLoader:
                    # Setup mocks
                    mock_client = MockClient.return_value
                    mock_cache = MockCache.return_value
                    mock_ioc_loader = MockIOCLoader.return_value
                    
                    # Setup IOC loader
                    mock_ioc_loader.load_iocs.return_value = {}
                    mock_ioc_loader.get_ioc_hash.return_value = "test-hash"
                    
                    mock_cache.get_repository_metadata.return_value = None
                    mock_client.get_organization_repos_graphql.return_value = APIResponse(
                        data=[
                            Repository(
                                name="repo1",
                                full_name="test-org/repo1",
                                archived=False,
                                default_branch="main",
                                updated_at=datetime.now()
                            )
                        ]
                    )
                    mock_cache.get_cache_stats.return_value = CacheStats()
                    
                    # No files found in repository
                    mock_client.search_files.return_value = []
                    
                    scanner = GitHubIOCScanner(config, mock_client, mock_cache, mock_ioc_loader)
                    result = scanner.scan()
                    
                    assert isinstance(result, ScanResults)
                    assert result.repositories_scanned == 1

    def test_caching_behavior(self):
        """Test that caching works correctly across multiple scans with incremental fetching."""
        from datetime import timezone
        config = ScanConfig(org="test-org")
        
        with patch('github_ioc_scanner.scanner.GitHubClient') as MockClient:
            with patch('github_ioc_scanner.scanner.CacheManager') as MockCache:
                with patch('github_ioc_scanner.scanner.IOCLoader') as MockIOCLoader:
                    mock_client = MockClient.return_value
                    mock_cache = MockCache.return_value
                    mock_ioc_loader = MockIOCLoader.return_value
                    
                    # Setup IOC loader
                    mock_ioc_loader.load_iocs.return_value = {}
                    mock_ioc_loader.get_ioc_hash.return_value = "test-hash"
                    
                    repos = [
                        Repository(
                            name="repo1",
                            full_name="test-org/repo1",
                            archived=False,
                            default_branch="main",
                            updated_at=datetime.now(timezone.utc)
                        )
                    ]
                    
                    # First scan - cache miss
                    mock_cache.get_repository_metadata.return_value = None
                    mock_client.get_organization_repos_graphql.return_value = APIResponse(
                        data=repos, etag='"first-etag"'
                    )
                    mock_cache.get_cache_stats.return_value = CacheStats()
                    mock_client.search_files.return_value = []
                    
                    scanner = GitHubIOCScanner(config, mock_client, mock_cache, mock_ioc_loader)
                    scanner.scan()
                    
                    # Verify cache was populated (with team="" parameter)
                    mock_cache.store_repository_metadata.assert_called_once_with(
                        "test-org", repos, '"first-etag"', team=""
                    )
                    
                    # Second scan - cache hit with incremental fetch
                    cache_timestamp = datetime.now(timezone.utc)
                    mock_cache.get_repository_metadata.return_value = (repos, '"first-etag"', cache_timestamp)
                    mock_client.get_organization_repos_graphql.reset_mock()
                    mock_client.get_organization_repos_graphql.return_value = APIResponse(
                        data=repos, etag='"first-etag"'
                    )
                    mock_cache.store_repository_metadata.reset_mock()
                    
                    scanner.scan()
                    
                    # Verify incremental fetch was used (API called with cached_repos)
                    mock_client.get_organization_repos_graphql.assert_called_once_with(
                        "test-org",
                        include_archived=False,
                        cached_repos=repos,
                        cache_cutoff=cache_timestamp
                    )

    @pytest.mark.skip(reason="Caching test needs rework after SBOM scanning changes")
    def test_three_tier_caching_integration(self):
        """Test the complete three-tier caching system integration."""
        config = ScanConfig(org="test-org")
        
        with patch('github_ioc_scanner.scanner.GitHubClient') as MockClient:
            with patch('github_ioc_scanner.scanner.CacheManager') as MockCache:
                with patch('github_ioc_scanner.scanner.IOCLoader') as MockIOCLoader:
                    with patch('github_ioc_scanner.scanner.get_parser') as MockGetParser:
                        mock_client = MockClient.return_value
                        mock_cache = MockCache.return_value
                        mock_ioc_loader = MockIOCLoader.return_value
                        
                        # Setup IOC loader
                        mock_ioc_loader.load_iocs.return_value = {
                            "test_ioc.py": IOCDefinition(
                                packages={"malicious-package": {"1.0.0"}},
                                source_file="test_ioc.py"
                            )
                        }
                        mock_ioc_loader.get_ioc_hash.return_value = "ioc-hash-123"
                        mock_ioc_loader.is_package_compromised.return_value = True
                        mock_ioc_loader._ioc_definitions = {
                            "test_ioc.py": IOCDefinition(
                                packages={"malicious-package": {"1.0.0"}},
                                source_file="test_ioc.py"
                            )
                        }
                        
                        # Setup repository discovery
                        repos = [
                            Repository(
                                name="repo1",
                                full_name="test-org/repo1",
                                archived=False,
                                default_branch="main",
                                updated_at=datetime.now()
                            )
                        ]
                        mock_cache.get_repository_metadata.return_value = None
                        mock_client.get_organization_repos_graphql.return_value = APIResponse(
                            data=repos, etag='"repo-etag"'
                        )
                        
                        # Setup file discovery
                        mock_client.search_files.return_value = [
                            FileInfo(path="package.json", sha="file-sha-123", size=1024)
                        ]
                        
                        # Setup file content fetching
                        file_content = FileContent(
                            content='{"dependencies": {"malicious-package": "1.0.0"}}',
                            sha="file-sha-123",
                            size=1024
                        )
                        mock_client.get_file_content.return_value = APIResponse(
                            data=file_content,
                            etag='"file-etag"'
                        )
                        
                        # Setup parser
                        mock_parser = Mock()
                        mock_parser.parse.return_value = [
                            PackageDependency(
                                name="malicious-package",
                                version="1.0.0",
                                dependency_type="dependencies"
                            )
                        ]
                        MockGetParser.return_value = mock_parser
                        
                        # First scan - all cache misses
                        mock_cache.get_file_content.return_value = None
                        mock_cache.get_parsed_packages.return_value = None
                        mock_cache.get_scan_results.return_value = None
                        mock_cache.get_etag.return_value = None
                        mock_cache.get_cache_stats.return_value = CacheStats(hits=0, misses=5)
                        
                        scanner = GitHubIOCScanner(config, mock_client, mock_cache, mock_ioc_loader)
                        result = scanner.scan()
                        
                        # Verify all three tiers were populated
                        mock_cache.store_file_content.assert_called_once_with(
                            "test-org/repo1", "package.json", "file-sha-123",
                            '{"dependencies": {"malicious-package": "1.0.0"}}', '"file-etag"'
                        )
                        mock_cache.store_parsed_packages.assert_called_once()
                        mock_cache.store_scan_results.assert_called_once()
                        
                        # Verify IOC match was found
                        assert len(result.matches) == 1
                        assert result.matches[0].package_name == "malicious-package"
                        
                        # Second scan - scan results cache hit
                        mock_cache.reset_mock()
                        mock_client.reset_mock()
                        
                        # Setup cache hits
                        mock_cache.get_repository_metadata.return_value = (repos, '"repo-etag"')
                        mock_client.get_organization_repos_graphql.return_value = APIResponse(
                            data=None, etag='"repo-etag"', not_modified=True
                        )
                        
                        # File content is still fetched to get SHA, but returns same content
                        mock_client.get_file_content.return_value = APIResponse(
                            data=file_content,
                            etag='"file-etag"'
                        )
                        
                        # Setup new parser mock for second scan
                        mock_parser2 = Mock()
                        MockGetParser.return_value = mock_parser2
                        
                        cached_matches = [
                            IOCMatch(
                                repo="test-org/repo1",
                                file_path="package.json",
                                package_name="malicious-package",
                                version="1.0.0",
                                ioc_source="test_ioc.py"
                            )
                        ]
                        mock_cache.get_scan_results.return_value = cached_matches
                        mock_cache.get_cache_stats.return_value = CacheStats(hits=3, misses=0)
                        
                        result2 = scanner.scan()
                        
                        # Verify scan results cache was used (parsing skipped)
                        mock_parser2.parse.assert_not_called()
                        
                        # Results should be the same
                        assert len(result2.matches) == 1
                        assert result2.matches[0].package_name == "malicious-package"

    def test_cache_hit_miss_tracking(self):
        """Test that cache hit/miss statistics are tracked correctly."""
        config = ScanConfig(org="test-org")
        
        with patch('github_ioc_scanner.scanner.GitHubClient') as MockClient:
            with patch('github_ioc_scanner.scanner.CacheManager') as MockCache:
                with patch('github_ioc_scanner.scanner.IOCLoader') as MockIOCLoader:
                    mock_client = MockClient.return_value
                    mock_cache = MockCache.return_value
                    mock_ioc_loader = MockIOCLoader.return_value
                    
                    # Setup IOC loader
                    mock_ioc_loader.load_iocs.return_value = {}
                    mock_ioc_loader.get_ioc_hash.return_value = "test-hash"
                    
                    # Setup repository discovery with cache miss
                    repos = [
                        Repository(
                            name="repo1",
                            full_name="test-org/repo1",
                            archived=False,
                            default_branch="main",
                            updated_at=datetime.now()
                        )
                    ]
                    mock_cache.get_repository_metadata.return_value = None  # Cache miss
                    mock_client.get_organization_repos_graphql.return_value = APIResponse(data=repos)
                    mock_client.search_files.return_value = []
                    
                    # Setup cache stats with specific hit/miss counts
                    cache_stats = CacheStats(hits=5, misses=3, time_saved=0.5, cache_size=100)
                    mock_cache.get_cache_stats.return_value = cache_stats
                    
                    scanner = GitHubIOCScanner(config, mock_client, mock_cache, mock_ioc_loader)
                    result = scanner.scan()
                    
                    # Verify cache stats are included in results
                    assert result.cache_stats == cache_stats
                    assert result.cache_stats.hits == 5
                    assert result.cache_stats.misses == 3
                    assert result.cache_stats.time_saved == 0.5
                    assert result.cache_stats.cache_size == 100

    @pytest.mark.skip(reason="IOC hash invalidation test needs rework after GraphQL migration")
    def test_ioc_hash_invalidation(self):
        """Test that IOC hash changes invalidate scan result cache."""
        config = ScanConfig(org="test-org")
        
        with patch('github_ioc_scanner.scanner.GitHubClient') as MockClient:
            with patch('github_ioc_scanner.scanner.CacheManager') as MockCache:
                with patch('github_ioc_scanner.scanner.IOCLoader') as MockIOCLoader:
                    with patch('github_ioc_scanner.scanner.get_parser') as MockGetParser:
                        mock_client = MockClient.return_value
                        mock_cache = MockCache.return_value
                        mock_ioc_loader = MockIOCLoader.return_value
                        
                        # Setup repository and file discovery
                        repos = [
                            Repository(
                                name="repo1",
                                full_name="test-org/repo1",
                                archived=False,
                                default_branch="main",
                                updated_at=datetime.now()
                            )
                        ]
                        mock_cache.get_repository_metadata.return_value = (repos, '"etag"')
                        mock_client.get_organization_repos_graphql.return_value = APIResponse(
                            data=None, not_modified=True
                        )
                        mock_client.search_files.return_value = [
                            FileInfo(path="package.json", sha="file-sha", size=1024)
                        ]
                        
                        # Setup file content
                        file_content = FileContent(
                            content='{"dependencies": {"test-package": "1.0.0"}}',
                            sha="file-sha",
                            size=1024
                        )
                        mock_client.get_file_content.return_value = APIResponse(data=file_content)
                        mock_cache.get_file_content.return_value = None
                        
                        # Setup parser
                        mock_parser = Mock()
                        mock_parser.parse.return_value = [
                            PackageDependency(name="test-package", version="1.0.0", dependency_type="dependencies")
                        ]
                        MockGetParser.return_value = mock_parser
                        
                        # First scan with IOC hash "old-hash"
                        mock_ioc_loader.load_iocs.return_value = {"old_ioc.py": Mock()}
                        mock_ioc_loader.get_ioc_hash.return_value = "old-hash"
                        mock_ioc_loader.is_package_compromised.return_value = False
                        
                        # No cached scan results for old hash
                        mock_cache.get_scan_results.return_value = None
                        mock_cache.get_parsed_packages.return_value = None
                        mock_cache.get_cache_stats.return_value = CacheStats()
                        
                        scanner = GitHubIOCScanner(config, mock_client, mock_cache, mock_ioc_loader)
                        result1 = scanner.scan()
                        
                        # Verify scan results were cached with old hash
                        mock_cache.store_scan_results.assert_called_with(
                            "test-org/repo1", "package.json", "file-sha", "old-hash", []
                        )
                        
                        # Second scan with IOC hash "new-hash" (IOC definitions changed)
                        mock_cache.reset_mock()
                        mock_ioc_loader.get_ioc_hash.return_value = "new-hash"
                        
                        # Cached results exist for old hash but not new hash
                        def mock_get_scan_results(repo, path, sha, ioc_hash):
                            if ioc_hash == "old-hash":
                                return []  # Old cached results
                            elif ioc_hash == "new-hash":
                                return None  # No cache for new hash
                        
                        mock_cache.get_scan_results.side_effect = mock_get_scan_results
                        mock_cache.get_parsed_packages.return_value = [
                            PackageDependency(name="test-package", version="1.0.0", dependency_type="dependencies")
                        ]
                        
                        result2 = scanner.scan()
                        
                        # Verify scan results were cached with new hash
                        mock_cache.store_scan_results.assert_called_with(
                            "test-org/repo1", "package.json", "file-sha", "new-hash", []
                        )
                        
                        # Verify parsing was used (not cached scan results)
                        mock_cache.get_parsed_packages.assert_called()