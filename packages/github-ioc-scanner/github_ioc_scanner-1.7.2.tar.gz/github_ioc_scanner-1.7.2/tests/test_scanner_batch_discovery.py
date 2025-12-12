"""Tests for Scanner batch repository and file discovery functionality."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from src.github_ioc_scanner.scanner import GitHubIOCScanner
from src.github_ioc_scanner.models import ScanConfig, Repository, FileInfo
from src.github_ioc_scanner.batch_models import BatchConfig, BatchStrategy
from src.github_ioc_scanner.github_client import GitHubClient
from src.github_ioc_scanner.cache_manager import CacheManager
from src.github_ioc_scanner.ioc_loader import IOCLoader


@pytest.fixture
def mock_scan_config():
    """Create a mock scan configuration."""
    return ScanConfig(
        org="test-org",
        repo=None,
        team=None,
        issues_dir="issues",
        fast_mode=False,
        include_archived=False
    )


@pytest.fixture
def mock_github_client():
    """Create a mock GitHub client."""
    client = MagicMock(spec=GitHubClient)
    client.token = "test-token"
    return client


@pytest.fixture
def mock_cache_manager():
    """Create a mock cache manager."""
    return MagicMock(spec=CacheManager)


@pytest.fixture
def mock_ioc_loader():
    """Create a mock IOC loader."""
    loader = MagicMock(spec=IOCLoader)
    loader.load_iocs.return_value = {"test-package": ["1.0.0"]}
    loader.get_ioc_hash.return_value = "test-hash"
    return loader


@pytest.fixture
def mock_batch_config():
    """Create a mock batch configuration."""
    return BatchConfig(
        max_concurrent_requests=5,
        default_batch_size=10,
        enable_cross_repo_batching=True,
        default_strategy=BatchStrategy.ADAPTIVE
    )


@pytest.fixture
def sample_repositories():
    """Create sample repositories for testing."""
    return [
        Repository(
            name="repo1",
            full_name="test-org/repo1",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(timezone.utc)
        ),
        Repository(
            name="repo2",
            full_name="test-org/repo2",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(timezone.utc)
        ),
        Repository(
            name="repo3",
            full_name="test-org/repo3",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(timezone.utc)
        )
    ]


@pytest.fixture
def sample_file_info():
    """Create sample file info objects."""
    return [
        FileInfo(path="package.json", size=1024, sha="abc123"),
        FileInfo(path="requirements.txt", size=512, sha="def456"),
        FileInfo(path="go.mod", size=256, sha="ghi789")
    ]


class TestScannerBatchRepositoryDiscovery:
    """Test batch repository discovery functionality."""
    
    @pytest.mark.asyncio
    async def test_discover_organization_repositories_batch_success(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test successful batch organization repository discovery."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock batch coordinator discovery
        scanner.batch_coordinator._discover_organization_repositories = AsyncMock(
            return_value=sample_repositories
        )
        
        # Execute
        repositories = await scanner.discover_organization_repositories_batch("test-org")
        
        # Verify
        assert len(repositories) == 3
        assert all(repo.full_name.startswith("test-org/") for repo in repositories)
        scanner.batch_coordinator._discover_organization_repositories.assert_called_once_with(
            "test-org", repository_filter=None, max_repositories=None
        )
    
    @pytest.mark.asyncio
    async def test_discover_organization_repositories_batch_fallback(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, sample_repositories
    ):
        """Test fallback to sequential discovery when batch coordinator is not available."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False  # Disable batch processing
        )
        
        # Mock sequential discovery
        with patch.object(scanner, 'discover_organization_repositories') as mock_discover:
            mock_discover.return_value = sample_repositories
            
            # Execute
            repositories = await scanner.discover_organization_repositories_batch("test-org")
            
            # Verify fallback was used
            assert len(repositories) == 3
            mock_discover.assert_called_once_with("test-org")
    
    @pytest.mark.asyncio
    async def test_discover_organization_repositories_batch_with_archived_filter(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config
    ):
        """Test batch organization discovery with archived repository filtering."""
        # Include archived repositories in config
        mock_scan_config.include_archived = False
        
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Create repositories with some archived
        repositories_with_archived = [
            Repository(name="repo1", full_name="test-org/repo1", archived=False, default_branch="main", updated_at=datetime.now(timezone.utc)),
            Repository(name="repo2", full_name="test-org/repo2", archived=True, default_branch="main", updated_at=datetime.now(timezone.utc)),
            Repository(name="repo3", full_name="test-org/repo3", archived=False, default_branch="main", updated_at=datetime.now(timezone.utc))
        ]
        
        # Mock batch coordinator discovery
        scanner.batch_coordinator._discover_organization_repositories = AsyncMock(
            return_value=repositories_with_archived
        )
        
        # Execute
        repositories = await scanner.discover_organization_repositories_batch("test-org")
        
        # Verify archived repositories are filtered out
        assert len(repositories) == 2
        assert all(not repo.archived for repo in repositories)
    
    @pytest.mark.asyncio
    async def test_discover_team_repositories_batch_success(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test successful batch team repository discovery."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock async team discovery
        with patch.object(scanner, '_discover_team_repositories_async') as mock_discover:
            mock_discover.return_value = sample_repositories
            
            # Execute
            repositories = await scanner.discover_team_repositories_batch("test-org", "test-team")
            
            # Verify
            assert len(repositories) == 3
            mock_discover.assert_called_once_with("test-org", "test-team")
    
    @pytest.mark.asyncio
    async def test_discover_team_repositories_batch_fallback(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, sample_repositories
    ):
        """Test fallback to sequential discovery for team repositories."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False
        )
        
        # Mock sequential discovery
        with patch.object(scanner, 'discover_team_repositories') as mock_discover:
            mock_discover.return_value = sample_repositories
            
            # Execute
            repositories = await scanner.discover_team_repositories_batch("test-org", "test-team")
            
            # Verify fallback was used
            assert len(repositories) == 3
            mock_discover.assert_called_once_with("test-org", "test-team")


class TestScannerBatchFileDiscovery:
    """Test batch file discovery functionality."""
    
    @pytest.mark.asyncio
    async def test_discover_files_in_repository_batch_success(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories, sample_file_info
    ):
        """Test successful batch file discovery in a single repository."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        repo = sample_repositories[0]
        
        # Mock async file discovery
        with patch.object(scanner, '_discover_files_async') as mock_discover:
            mock_discover.return_value = sample_file_info
            
            # Execute
            file_paths = await scanner.discover_files_in_repository_batch(repo)
            
            # Verify
            assert len(file_paths) == 3
            assert "package.json" in file_paths
            assert "requirements.txt" in file_paths
            assert "go.mod" in file_paths
            mock_discover.assert_called_once_with(repo)
    
    @pytest.mark.asyncio
    async def test_discover_files_in_repository_batch_fallback(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, sample_repositories
    ):
        """Test fallback to sequential file discovery."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False
        )
        
        repo = sample_repositories[0]
        expected_files = ["package.json", "requirements.txt"]
        
        # Mock sequential discovery
        with patch.object(scanner, 'discover_files_in_repository') as mock_discover:
            mock_discover.return_value = expected_files
            
            # Execute
            file_paths = await scanner.discover_files_in_repository_batch(repo)
            
            # Verify fallback was used
            assert file_paths == expected_files
            mock_discover.assert_called_once_with(repo)
    
    @pytest.mark.asyncio
    async def test_discover_files_in_repositories_batch_success(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test successful batch file discovery across multiple repositories."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock individual repository file discovery
        with patch.object(scanner, 'discover_files_in_repository_batch') as mock_discover:
            # Return different files for each repository
            mock_discover.side_effect = [
                ["package.json", "yarn.lock"],
                ["requirements.txt", "poetry.lock"],
                ["go.mod", "go.sum"]
            ]
            
            # Execute
            result = await scanner.discover_files_in_repositories_batch(sample_repositories)
            
            # Verify
            assert len(result) == 3
            assert result["test-org/repo1"] == ["package.json", "yarn.lock"]
            assert result["test-org/repo2"] == ["requirements.txt", "poetry.lock"]
            assert result["test-org/repo3"] == ["go.mod", "go.sum"]
            assert mock_discover.call_count == 3
    
    @pytest.mark.asyncio
    async def test_discover_files_in_repositories_batch_with_errors(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test batch file discovery with some repositories failing."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock individual repository file discovery with one failure
        with patch.object(scanner, 'discover_files_in_repository_batch') as mock_discover:
            mock_discover.side_effect = [
                ["package.json"],
                Exception("API error"),
                ["go.mod"]
            ]
            
            # Execute
            result = await scanner.discover_files_in_repositories_batch(sample_repositories)
            
            # Verify
            assert len(result) == 3
            assert result["test-org/repo1"] == ["package.json"]
            assert result["test-org/repo2"] == []  # Empty due to error
            assert result["test-org/repo3"] == ["go.mod"]
    
    @pytest.mark.asyncio
    async def test_discover_files_in_repositories_batch_fallback(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, sample_repositories
    ):
        """Test fallback to sequential discovery for multiple repositories."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False
        )
        
        # Mock sequential discovery
        with patch.object(scanner, 'discover_files_in_repository') as mock_discover:
            mock_discover.side_effect = [
                ["package.json"],
                ["requirements.txt"],
                ["go.mod"]
            ]
            
            # Execute
            result = await scanner.discover_files_in_repositories_batch(sample_repositories)
            
            # Verify fallback was used
            assert len(result) == 3
            assert result["test-org/repo1"] == ["package.json"]
            assert result["test-org/repo2"] == ["requirements.txt"]
            assert result["test-org/repo3"] == ["go.mod"]
            assert mock_discover.call_count == 3


class TestScannerBatchDiscoveryIntegration:
    """Test integration of batch discovery methods."""
    
    @pytest.mark.asyncio
    async def test_discover_repositories_batch_organization(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test integrated batch repository discovery for organization."""
        mock_scan_config.org = "test-org"
        mock_scan_config.repo = None
        mock_scan_config.team = None
        
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock batch organization discovery
        with patch.object(scanner, 'discover_organization_repositories_batch') as mock_discover:
            mock_discover.return_value = sample_repositories
            
            # Execute
            repositories = await scanner._discover_repositories_batch()
            
            # Verify
            assert len(repositories) == 3
            mock_discover.assert_called_once_with("test-org")
    
    @pytest.mark.asyncio
    async def test_discover_repositories_batch_team(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test integrated batch repository discovery for team."""
        mock_scan_config.org = "test-org"
        mock_scan_config.team = "test-team"
        mock_scan_config.repo = None
        
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock batch team discovery
        with patch.object(scanner, 'discover_team_repositories_batch') as mock_discover:
            mock_discover.return_value = sample_repositories
            
            # Execute
            repositories = await scanner._discover_repositories_batch()
            
            # Verify
            assert len(repositories) == 3
            mock_discover.assert_called_once_with("test-org", "test-team")
    
    @pytest.mark.asyncio
    async def test_discover_repositories_batch_single_repo(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config
    ):
        """Test integrated batch repository discovery for single repository."""
        mock_scan_config.org = "test-org"
        mock_scan_config.repo = "test-repo"
        mock_scan_config.team = None
        
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Execute
        repositories = await scanner._discover_repositories_batch()
        
        # Verify
        assert len(repositories) == 1
        assert repositories[0].full_name == "test-org/test-repo"
        assert repositories[0].name == "test-repo"