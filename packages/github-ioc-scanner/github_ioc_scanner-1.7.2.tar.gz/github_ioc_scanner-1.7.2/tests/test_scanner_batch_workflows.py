"""Tests for Scanner end-to-end batch scanning workflows."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from src.github_ioc_scanner.scanner import GitHubIOCScanner
from src.github_ioc_scanner.models import ScanConfig, ScanResults, Repository, IOCMatch
from src.github_ioc_scanner.batch_models import BatchConfig, BatchStrategy, BatchMetrics
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
    manager = MagicMock(spec=CacheManager)
    manager.get_cache_stats.return_value = MagicMock()
    return manager


@pytest.fixture
def mock_ioc_loader():
    """Create a mock IOC loader."""
    loader = MagicMock(spec=IOCLoader)
    loader.load_iocs.return_value = {"malicious-package": ["1.0.0"]}
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
def sample_ioc_matches():
    """Create sample IOC matches for testing."""
    return [
        IOCMatch(
            repo="test-org/repo1",
            file_path="package.json",
            package_name="malicious-package",
            version="1.0.0",
            ioc_source="test.py"
        ),
        IOCMatch(
            repo="test-org/repo2",
            file_path="requirements.txt",
            package_name="malicious-package",
            version="1.0.0",
            ioc_source="test.py"
        )
    ]


@pytest.fixture
def mock_batch_metrics():
    """Create mock batch metrics."""
    return BatchMetrics(
        total_requests=100,
        successful_requests=95,
        failed_requests=5,
        cache_hits=60,
        cache_misses=40,
        average_batch_size=8.5,
        total_processing_time=45.2,
        api_calls_saved=60,
        parallel_efficiency=0.85
    )


class TestEndToEndBatchWorkflows:
    """Test complete end-to-end batch scanning workflows."""
    
    @pytest.mark.asyncio
    async def test_execute_end_to_end_batch_scan_success(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories, 
        sample_ioc_matches, mock_batch_metrics
    ):
        """Test successful end-to-end batch scan execution."""
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
        scanner.batch_coordinator.execute_end_to_end_batch_workflow = AsyncMock(
            return_value={
                'processing_results': {
                    'test-org/repo1': [sample_ioc_matches[0]],
                    'test-org/repo2': [sample_ioc_matches[1]],
                    'test-org/repo3': []
                },
                'workflow_metrics': {'total_repositories': 3},
                'operation_id': 'test-op-123'
            }
        )
        scanner.batch_coordinator.get_batch_metrics = AsyncMock(return_value=mock_batch_metrics)
        
        # Mock repository and file discovery
        with patch.object(scanner, '_discover_repositories_batch') as mock_discover_repos:
            mock_discover_repos.return_value = sample_repositories
            
            with patch.object(scanner, 'discover_files_in_repositories_batch') as mock_discover_files:
                mock_discover_files.return_value = {
                    'test-org/repo1': ['package.json'],
                    'test-org/repo2': ['requirements.txt'],
                    'test-org/repo3': ['go.mod']
                }
                
                # Execute
                result = await scanner.execute_end_to_end_batch_scan()
                
                # Verify
                assert isinstance(result, ScanResults)
                assert len(result.matches) == 2
                assert result.repositories_scanned == 2  # Only repos with matches
                assert result.files_scanned == 3
                
                # Verify batch coordinator was used properly
                scanner.batch_coordinator.start.assert_called_once()
                scanner.batch_coordinator.stop.assert_called_once()
                scanner.batch_coordinator.execute_end_to_end_batch_workflow.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_execute_end_to_end_batch_scan_no_repositories(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config
    ):
        """Test end-to-end batch scan with no repositories found."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock batch coordinator
        scanner.batch_coordinator.start = AsyncMock()
        scanner.batch_coordinator.stop = AsyncMock()
        
        # Mock empty repository discovery
        with patch.object(scanner, '_discover_repositories_batch') as mock_discover:
            mock_discover.return_value = []
            
            # Execute
            result = await scanner.execute_end_to_end_batch_scan()
            
            # Verify
            assert isinstance(result, ScanResults)
            assert len(result.matches) == 0
            assert result.repositories_scanned == 0
            assert result.files_scanned == 0
    
    @pytest.mark.asyncio
    async def test_execute_end_to_end_batch_scan_with_workflow_config(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories, mock_batch_metrics
    ):
        """Test end-to-end batch scan with custom workflow configuration."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock batch coordinator
        scanner.batch_coordinator.start = AsyncMock()
        scanner.batch_coordinator.stop = AsyncMock()
        scanner.batch_coordinator.execute_end_to_end_batch_workflow = AsyncMock(
            return_value={
                'processing_results': {},
                'workflow_metrics': {'total_repositories': 3},
                'operation_id': 'test-op-456'
            }
        )
        scanner.batch_coordinator.get_batch_metrics = AsyncMock(return_value=mock_batch_metrics)
        
        # Mock discovery methods
        with patch.object(scanner, '_discover_repositories_batch') as mock_discover_repos:
            mock_discover_repos.return_value = sample_repositories
            
            with patch.object(scanner, 'discover_files_in_repositories_batch') as mock_discover_files:
                mock_discover_files.return_value = {'test-org/repo1': ['package.json']}
                
                # Custom workflow configuration
                workflow_config = {
                    'scan_pattern': 'custom_scan',
                    'enable_progress_tracking': False,
                    'enable_performance_monitoring': True
                }
                
                # Execute
                result = await scanner.execute_end_to_end_batch_scan(workflow_config)
                
                # Verify workflow config was passed correctly
                call_args = scanner.batch_coordinator.execute_end_to_end_batch_workflow.call_args
                assert call_args[0][0] == sample_repositories  # repositories
                workflow_params = call_args[0][1]  # workflow_params
                assert workflow_params['scan_pattern'] == 'custom_scan'
                assert workflow_params['enable_progress_tracking'] is False
                assert workflow_params['enable_performance_monitoring'] is True
    
    @pytest.mark.asyncio
    async def test_execute_organization_batch_scan(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_ioc_matches
    ):
        """Test organization-level batch scan execution."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock the end-to-end batch scan
        with patch.object(scanner, 'execute_end_to_end_batch_scan') as mock_execute:
            mock_result = ScanResults(
                matches=sample_ioc_matches,
                cache_stats=MagicMock(),
                repositories_scanned=2,
                files_scanned=5
            )
            mock_execute.return_value = mock_result
            
            # Execute
            result = await scanner.execute_organization_batch_scan("test-org")
            
            # Verify
            assert result == mock_result
            assert scanner.config.org == "test-org"  # Config was updated
            
            # Verify workflow config was passed
            call_args = mock_execute.call_args[0][0]  # workflow_config
            assert call_args['scan_pattern'] == 'organization_security_scan'
            assert call_args['enable_progress_tracking'] is True
    
    @pytest.mark.asyncio
    async def test_execute_team_batch_scan(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_ioc_matches
    ):
        """Test team-level batch scan execution."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Store original config values
        original_org = scanner.config.org
        original_team = scanner.config.team
        
        # Mock the end-to-end batch scan to capture config during execution
        config_during_execution = {}
        
        async def mock_execute_with_config_capture(workflow_config):
            # Capture config values during execution
            config_during_execution['org'] = scanner.config.org
            config_during_execution['team'] = scanner.config.team
            return ScanResults(
                matches=sample_ioc_matches,
                cache_stats=MagicMock(),
                repositories_scanned=2,
                files_scanned=3
            )
        
        with patch.object(scanner, 'execute_end_to_end_batch_scan', side_effect=mock_execute_with_config_capture):
            # Execute
            result = await scanner.execute_team_batch_scan("test-org", "test-team")
            
            # Verify result
            assert len(result.matches) == 2
            assert result.repositories_scanned == 2
            
            # Verify config was set correctly during execution
            assert config_during_execution['org'] == "test-org"
            assert config_during_execution['team'] == "test-team"
            
            # Verify config was restored after execution
            assert scanner.config.org == original_org
            assert scanner.config.team == original_team
    
    @pytest.mark.asyncio
    async def test_execute_repository_batch_scan(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_ioc_matches
    ):
        """Test repository-level batch scan execution."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Store original config values
        original_org = scanner.config.org
        original_repo = scanner.config.repo
        
        # Mock the end-to-end batch scan to capture config during execution
        config_during_execution = {}
        
        async def mock_execute_with_config_capture(workflow_config):
            # Capture config values during execution
            config_during_execution['org'] = scanner.config.org
            config_during_execution['repo'] = scanner.config.repo
            return ScanResults(
                matches=[sample_ioc_matches[0]],
                cache_stats=MagicMock(),
                repositories_scanned=1,
                files_scanned=2
            )
        
        with patch.object(scanner, 'execute_end_to_end_batch_scan', side_effect=mock_execute_with_config_capture):
            # Execute
            result = await scanner.execute_repository_batch_scan("test-org", "test-repo")
            
            # Verify result
            assert len(result.matches) == 1
            assert result.repositories_scanned == 1
            
            # Verify config was set correctly during execution
            assert config_during_execution['org'] == "test-org"
            assert config_during_execution['repo'] == "test-repo"
            
            # Verify config was restored after execution
            assert scanner.config.org == original_org
            assert scanner.config.repo == original_repo
    
    @pytest.mark.asyncio
    async def test_process_batch_results_for_iocs(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, sample_ioc_matches
    ):
        """Test processing of batch results to extract IOC matches."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False
        )
        
        # Prepare batch results
        batch_results = {
            'test-org/repo1': [sample_ioc_matches[0]],
            'test-org/repo2': [sample_ioc_matches[1]],
            'test-org/repo3': [],  # No matches
            'test-org/repo4': ["invalid-match"]  # Invalid match format
        }
        
        # Execute
        matches = await scanner._process_batch_results_for_iocs(batch_results, "test-hash")
        
        # Verify
        assert len(matches) == 2  # Only valid IOCMatch objects
        assert all(isinstance(match, IOCMatch) for match in matches)
        assert matches[0] == sample_ioc_matches[0]
        assert matches[1] == sample_ioc_matches[1]


class TestBatchWorkflowErrorHandling:
    """Test error handling in batch workflows."""
    
    @pytest.mark.asyncio
    async def test_execute_end_to_end_batch_scan_no_batch_coordinator(
        self, mock_scan_config, mock_github_client, mock_cache_manager, mock_ioc_loader
    ):
        """Test end-to-end batch scan without batch coordinator."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            enable_batch_processing=False  # No batch coordinator
        )
        
        # Execute and expect ConfigurationError
        with pytest.raises(Exception):  # Should raise ConfigurationError wrapped in ScanError
            await scanner.execute_end_to_end_batch_scan()
    
    @pytest.mark.asyncio
    async def test_execute_end_to_end_batch_scan_coordinator_failure(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories
    ):
        """Test end-to-end batch scan with batch coordinator failure."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock batch coordinator to fail
        scanner.batch_coordinator.start = AsyncMock()
        scanner.batch_coordinator.stop = AsyncMock()
        scanner.batch_coordinator.execute_end_to_end_batch_workflow = AsyncMock(
            side_effect=Exception("Batch coordinator failure")
        )
        
        # Mock repository discovery
        with patch.object(scanner, '_discover_repositories_batch') as mock_discover:
            mock_discover.return_value = sample_repositories
            
            with patch.object(scanner, 'discover_files_in_repositories_batch') as mock_discover_files:
                mock_discover_files.return_value = {'test-org/repo1': ['package.json']}
                
                # Execute and expect ScanError
                with pytest.raises(Exception):  # Should raise wrapped ScanError
                    await scanner.execute_end_to_end_batch_scan()
                
                # Verify coordinator was still stopped
                scanner.batch_coordinator.stop.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_organization_batch_scan_config_restoration(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config
    ):
        """Test that organization batch scan restores original configuration on error."""
        original_org = "original-org"
        mock_scan_config.org = original_org
        
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock the end-to-end batch scan to fail
        with patch.object(scanner, 'execute_end_to_end_batch_scan') as mock_execute:
            mock_execute.side_effect = Exception("Scan failed")
            
            # Execute and expect exception
            with pytest.raises(Exception):
                await scanner.execute_organization_batch_scan("test-org")
            
            # Verify original configuration was restored
            assert scanner.config.org == original_org


class TestBatchWorkflowIntegration:
    """Test integration aspects of batch workflows."""
    
    @pytest.mark.asyncio
    async def test_complete_workflow_integration(
        self, mock_scan_config, mock_github_client, mock_cache_manager, 
        mock_ioc_loader, mock_batch_config, sample_repositories, 
        sample_ioc_matches, mock_batch_metrics
    ):
        """Test complete integration of all workflow components."""
        scanner = GitHubIOCScanner(
            config=mock_scan_config,
            github_client=mock_github_client,
            cache_manager=mock_cache_manager,
            ioc_loader=mock_ioc_loader,
            batch_config=mock_batch_config,
            enable_batch_processing=True
        )
        
        # Mock all components
        scanner.batch_coordinator.start = AsyncMock()
        scanner.batch_coordinator.stop = AsyncMock()
        scanner.batch_coordinator.execute_end_to_end_batch_workflow = AsyncMock(
            return_value={
                'processing_results': {
                    'test-org/repo1': [sample_ioc_matches[0]],
                    'test-org/repo2': [sample_ioc_matches[1]]
                },
                'workflow_metrics': {
                    'total_repositories': 2,
                    'total_ioc_matches': 2,
                    'batch_metrics': mock_batch_metrics.__dict__
                },
                'operation_id': 'integration-test-123'
            }
        )
        scanner.batch_coordinator.get_batch_metrics = AsyncMock(return_value=mock_batch_metrics)
        
        # Mock discovery methods
        with patch.object(scanner, '_discover_repositories_batch') as mock_discover_repos:
            mock_discover_repos.return_value = sample_repositories[:2]  # Only 2 repos
            
            with patch.object(scanner, 'discover_files_in_repositories_batch') as mock_discover_files:
                mock_discover_files.return_value = {
                    'test-org/repo1': ['package.json', 'yarn.lock'],
                    'test-org/repo2': ['requirements.txt', 'poetry.lock']
                }
                
                # Execute complete workflow
                result = await scanner.execute_end_to_end_batch_scan({
                    'scan_pattern': 'integration_test',
                    'enable_progress_tracking': True,
                    'enable_performance_monitoring': True
                })
                
                # Verify comprehensive results
                assert isinstance(result, ScanResults)
                assert len(result.matches) == 2
                assert result.repositories_scanned == 2
                assert result.files_scanned == 4  # 2 files per repo
                
                # Verify all components were called
                mock_discover_repos.assert_called_once()
                mock_discover_files.assert_called_once_with(sample_repositories[:2])
                scanner.batch_coordinator.execute_end_to_end_batch_workflow.assert_called_once()
                
                # Verify workflow parameters
                call_args = scanner.batch_coordinator.execute_end_to_end_batch_workflow.call_args
                workflow_params = call_args[0][1]
                assert workflow_params['scan_pattern'] == 'integration_test'
                assert workflow_params['enable_progress_tracking'] is True
                assert workflow_params['enable_performance_monitoring'] is True