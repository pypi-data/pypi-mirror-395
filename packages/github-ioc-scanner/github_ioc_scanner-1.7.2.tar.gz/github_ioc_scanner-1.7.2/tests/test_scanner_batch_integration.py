"""Integration tests for Scanner class with batch processing."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from src.github_ioc_scanner.scanner import GitHubIOCScanner
from src.github_ioc_scanner.models import ScanConfig, Repository, IOCMatch, FileContent
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
    client.base_url = "https://api.github.com"
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
    loader.get_all_packages.return_value = {"test-package": ["1.0.0"]}
    loader.is_package_compromised.return_value = False
    loader._ioc_definitions = {"test.py": MagicMock()}
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


class TestScannerBatchIntegration:
    """Test Scanner integration with batch processing."""
    
    def test_scanner_initialization_with_batch_processing(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config
    ):
        """Test scanner initialization with batch processing enabled."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        assert scanner.enable_batch_processing is True
        assert scanner.batch_coordinator is not None
        assert scanner.async_github_client is not None
        assert scanner.batch_coordinator.config == mock_batch_config
    
    def test_scanner_initialization_without_batch_processing(
        self, mock_scan_config, mock_github_client, mock_cache_manager, mock_ioc_loader
    ):
        """Test scanner initialization with batch processing disabled."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False
        )
        
        assert scanner.enable_batch_processing is False
        assert scanner.batch_coordinator is None
        assert scanner.async_github_client is None
    
    @patch('src.github_ioc_scanner.scanner.asyncio.run')
    def test_scan_uses_batch_processing_when_enabled(
        self, mock_asyncio_run, mock_scan_config, mock_github_client, 
        mock_cache_manager, mock_ioc_loader, mock_batch_config
    ):
        """Test that scan() uses batch processing when enabled."""
        # Setup
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock the async scan method
        mock_result = MagicMock()
        mock_asyncio_run.return_value = mock_result
        
        # Execute
        result = scanner.scan()
        
        # Verify
        assert result == mock_result
        mock_asyncio_run.assert_called_once()
        # Verify it's calling the batch processing method
        call_args = mock_asyncio_run.call_args[0][0]
        assert hasattr(call_args, '__name__') or callable(call_args)
    
    def test_scan_uses_sequential_processing_when_disabled(
        self, mock_scan_config, mock_github_client, mock_cache_manager, mock_ioc_loader
    ):
        """Test that scan() uses sequential processing when batch processing is disabled."""
        # Setup
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False
        )
        
        # Mock dependencies for sequential scan
        with patch.object(scanner, 'discover_organization_repositories') as mock_discover:
            mock_discover.return_value = []
            mock_cache_manager.get_cache_stats.return_value = MagicMock()
            
            # Execute
            result = scanner.scan()
            
            # Verify sequential processing was used
            assert result is not None
            assert result.repositories_scanned == 0
            assert result.files_scanned == 0
    
    @pytest.mark.asyncio
    async def test_discover_repositories_batch_organization(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test batch repository discovery for organization."""
        # Setup
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
        
        # Mock batch coordinator methods
        scanner.batch_coordinator._discover_organization_repositories = AsyncMock(
            return_value=sample_repositories
        )
        scanner.batch_coordinator.process_organization_repositories_batch = AsyncMock(
            return_value={}
        )
        
        # Execute
        repositories = await scanner._discover_repositories_batch()
        
        # Verify
        assert len(repositories) == 3
        assert all(repo.full_name.startswith("test-org/") for repo in repositories)
    
    @pytest.mark.asyncio
    async def test_discover_repositories_batch_single_repo(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config
    ):
        """Test batch repository discovery for single repository."""
        # Setup
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
    
    @pytest.mark.asyncio
    async def test_scan_single_repository_batch(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test batch scanning of a single repository."""
        # Setup
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        repo = sample_repositories[0]
        
        # Mock file discovery
        with patch.object(scanner, 'discover_files_in_repository') as mock_discover_files:
            mock_discover_files.return_value = ['package.json', 'requirements.txt']
            
            # Mock batch coordinator
            scanner.batch_coordinator.process_files_batch = AsyncMock(
                return_value={
                    'package.json': {'content': '{"dependencies": {"test-package": "1.0.0"}}'},
                    'requirements.txt': {'content': 'test-package==1.0.0'}
                }
            )
            
            # Mock IOC processing
            with patch.object(scanner, '_process_file_for_iocs_batch') as mock_process:
                mock_process.return_value = [
                    IOCMatch(
                        repo=repo.full_name,
                        file_path='package.json',
                        package_name='test-package',
                        version='1.0.0',
                        ioc_source='test.py'
                    )
                ]
                
                # Execute
                matches = await scanner._scan_single_repository_batch(repo, "test-hash")
                
                # Verify
                assert len(matches) == 2  # One match per file
                assert all(match.repo == repo.full_name for match in matches)
    
    def test_get_priority_files(
        self, mock_scan_config, mock_github_client, mock_cache_manager, mock_ioc_loader
    ):
        """Test priority file identification."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader
        )
        
        file_paths = [
            'src/package.json',
            'requirements.txt',
            'docs/README.md',
            'go.mod',
            'some/deep/path/Cargo.toml',
            'random-file.txt'
        ]
        
        priority_files = scanner._get_priority_files(file_paths)
        
        expected_priority = ['src/package.json', 'requirements.txt', 'go.mod', 'some/deep/path/Cargo.toml']
        assert set(priority_files) == set(expected_priority)
    
    @pytest.mark.asyncio
    async def test_process_file_for_iocs_batch(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, sample_repositories
    ):
        """Test processing a single file for IOCs in batch context."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader
        )
        
        repo = sample_repositories[0]
        
        # Mock parse_file_safely to return packages
        with patch('src.github_ioc_scanner.scanner.parse_file_safely') as mock_parse:
            mock_package = MagicMock()
            mock_package.name = "test-package"
            mock_package.version = "1.0.0"
            mock_parse.return_value = [mock_package]
            
            # Mock match_packages_against_iocs
            with patch.object(scanner, 'match_packages_against_iocs') as mock_match:
                expected_match = IOCMatch(
                    repo=repo.full_name,
                    file_path='package.json',
                    package_name='test-package',
                    version='1.0.0',
                    ioc_source='test.py'
                )
                mock_match.return_value = [expected_match]
                
                # Execute
                matches = await scanner._process_file_for_iocs_batch(
                    repo, 'package.json', '{"dependencies": {"test-package": "1.0.0"}}', "test-hash"
                )
                
                # Verify
                assert len(matches) == 1
                assert matches[0] == expected_match
                mock_parse.assert_called_once_with('package.json', '{"dependencies": {"test-package": "1.0.0"}}')
                mock_match.assert_called_once_with(repo, 'package.json', [mock_package])
    
    def test_select_batch_strategy(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, sample_repositories
    ):
        """Test batch strategy selection based on repository count."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader
        )
        
        # Test single repository
        strategy = scanner._select_batch_strategy([sample_repositories[0]])
        assert strategy == BatchStrategy.PARALLEL
        
        # Test small set (3 repos)
        strategy = scanner._select_batch_strategy(sample_repositories)
        assert strategy == BatchStrategy.ADAPTIVE
        
        # Test medium set (10 repos)
        medium_repos = sample_repositories * 4  # 12 repos
        strategy = scanner._select_batch_strategy(medium_repos)
        assert strategy == BatchStrategy.PARALLEL
        
        # Test large set (25 repos)
        large_repos = sample_repositories * 9  # 27 repos
        strategy = scanner._select_batch_strategy(large_repos)
        assert strategy == BatchStrategy.AGGRESSIVE
    
    @pytest.mark.asyncio
    async def test_scan_with_batch_processing_integration(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test complete scan workflow with batch processing."""
        # Setup
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock batch coordinator methods
        scanner.batch_coordinator.start = AsyncMock()
        scanner.batch_coordinator.stop = AsyncMock()
        scanner.batch_coordinator.get_batch_metrics = AsyncMock()
        scanner.batch_coordinator.get_batch_metrics.return_value = MagicMock(
            cache_hit_rate=75.0,
            parallel_efficiency=0.85
        )
        
        # Mock repository discovery
        with patch.object(scanner, '_discover_repositories_batch') as mock_discover:
            mock_discover.return_value = sample_repositories
            
            # Mock batch processing
            scanner.batch_coordinator.process_repositories_batch = AsyncMock(
                return_value={
                    "test-org/repo1": [
                        IOCMatch(
                            repo="test-org/repo1",
                            file_path="package.json",
                            package_name="malicious-package",
                            version="1.0.0",
                            ioc_source="test.py"
                        )
                    ],
                    "test-org/repo2": [],
                    "test-org/repo3": []
                }
            )
            
            # Mock cache stats
            mock_cache_manager.get_cache_stats.return_value = MagicMock()
            
            # Execute
            result = await scanner._scan_with_batch_processing()
            
            # Verify
            assert result is not None
            assert result.repositories_scanned == 1  # Only repo1 had matches
            assert len(result.matches) == 1
            assert result.matches[0].package_name == "malicious-package"
            
            # Verify batch coordinator was used properly
            scanner.batch_coordinator.start.assert_called_once()
            scanner.batch_coordinator.stop.assert_called_once()
            scanner.batch_coordinator.process_repositories_batch.assert_called_once()


class TestScannerBatchBackwardCompatibility:
    """Test backward compatibility when batch processing is disabled."""
    
    def test_backward_compatibility_scan_behavior(
        self, mock_scan_config, mock_github_client, mock_cache_manager, mock_ioc_loader
    ):
        """Test that disabling batch processing maintains original behavior."""
        # Setup scanner without batch processing
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False
        )
        
        # Mock the sequential scan dependencies
        with patch.object(scanner, 'discover_organization_repositories') as mock_discover:
            mock_discover.return_value = []
            mock_cache_manager.get_cache_stats.return_value = MagicMock()
            
            # Execute
            result = scanner.scan()
            
            # Verify it uses sequential processing
            assert result is not None
            assert hasattr(result, 'matches')
            assert hasattr(result, 'repositories_scanned')
            assert hasattr(result, 'files_scanned')
            
            # Verify sequential methods were called
            mock_discover.assert_called_once_with(mock_scan_config.org)
    
    def test_scan_repository_method_unchanged(
        self, mock_scan_config, mock_github_client, mock_cache_manager, mock_ioc_loader
    ):
        """Test that scan_repository method behavior is unchanged."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False
        )
        
        # Mock dependencies
        with patch.object(scanner, 'scan_repository_for_iocs') as mock_scan_repo:
            mock_scan_repo.return_value = ([], 0)
            
            # Execute
            result = scanner.scan_repository("test-org", "test-repo")
            
            # Verify
            assert result == []
            mock_scan_repo.assert_called_once()