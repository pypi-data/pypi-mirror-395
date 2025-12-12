"""Tests for team-first organization scanning functionality."""

import pytest
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from github_ioc_scanner.scanner import GitHubIOCScanner
from github_ioc_scanner.models import ScanConfig, Repository, IOCMatch
from github_ioc_scanner.exceptions import AuthenticationError, OrganizationNotFoundError


class TestTeamFirstOrgScanning:
    """Test cases for team-first organization scanning."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary IOC file
        self.ioc_data = {
            "packages": [
                {
                    "name": "malicious-package",
                    "versions": ["1.0.0"],
                    "description": "Test malicious package"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.ioc_data, f)
            self.ioc_file = f.name
        
        # Create test configuration
        self.config = ScanConfig(
            org="test-org",
            team_first_org=True,
            ioc_files=[self.ioc_file],
            quiet=True,
            fast_mode=True
        )
        
        # Create mock repositories
        self.mock_repos = [
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
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            ),
            Repository(
                name="repo3",
                full_name="test-org/repo3", 
                archived=False,
                default_branch="main",
                updated_at=datetime.now()
            )
        ]
        
        # Create mock teams
        self.mock_teams = [
            {
                "id": 1,
                "name": "Team Alpha",
                "slug": "team-alpha",
                "description": "Alpha team",
                "privacy": "closed"
            },
            {
                "id": 2,
                "name": "Team Beta",
                "slug": "team-beta", 
                "description": "Beta team",
                "privacy": "closed"
            }
        ]

    def teardown_method(self):
        """Clean up test fixtures."""
        import os
        os.unlink(self.ioc_file)

    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_organization_repositories')
    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_team_repositories')
    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.scan_repository_for_iocs')
    def test_team_first_org_scan_basic(self, mock_scan_repo, mock_discover_team, mock_discover_org):
        """Test basic team-first organization scanning functionality."""
        
        # Setup mocks
        mock_discover_org.return_value = self.mock_repos
        mock_discover_team.side_effect = [
            [self.mock_repos[0]],  # Team Alpha has repo1
            [self.mock_repos[1]]   # Team Beta has repo2
        ]
        mock_scan_repo.return_value = ([], 5)  # No matches, 5 files scanned
        
        # Create scanner with mocked GitHub client
        scanner = GitHubIOCScanner(self.config)
        
        # Mock the GitHub client's get_organization_teams method
        scanner.github_client.get_organization_teams = Mock(return_value=self.mock_teams)
        
        # Execute team-first scan
        with patch.object(scanner, '_scan_team_first_organization') as mock_team_scan:
            mock_team_scan.return_value = Mock(
                matches=[],
                repositories_scanned=3,
                files_scanned=15,
                scan_duration=1.5,
                cache_stats=None
            )
            
            results = scanner.scan()
            
            # Verify the team-first scan was called
            mock_team_scan.assert_called_once()
            
            # Verify results
            assert results.repositories_scanned == 3
            assert results.files_scanned == 15
            assert len(results.matches) == 0

    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_organization_repositories')
    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_team_repositories')
    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.scan_repository_for_iocs')
    def test_team_first_org_scan_with_matches(self, mock_scan_repo, mock_discover_team, mock_discover_org):
        """Test team-first scanning with IOC matches found."""
        
        # Create mock IOC matches
        mock_matches = [
            IOCMatch(
                repository="test-org/repo1",
                file_path="package.json",
                package_name="malicious-package",
                version="1.0.0",
                line_number=10,
                context="test context"
            )
        ]
        
        # Setup mocks
        mock_discover_org.return_value = self.mock_repos
        mock_discover_team.side_effect = [
            [self.mock_repos[0]],  # Team Alpha has repo1 (with matches)
            [self.mock_repos[1]]   # Team Beta has repo2 (no matches)
        ]
        mock_scan_repo.side_effect = [
            (mock_matches, 3),  # repo1 has matches
            ([], 5),            # repo2 has no matches  
            ([], 4)             # repo3 (unassigned) has no matches
        ]
        
        # Create scanner
        scanner = GitHubIOCScanner(self.config)
        scanner.github_client.get_organization_teams = Mock(return_value=self.mock_teams)
        
        # Execute the actual team-first scan method
        import time
        start_time = time.time()
        ioc_hash = "test_hash"
        
        results = scanner._scan_team_first_organization(ioc_hash, start_time)
        
        # Verify results
        assert len(results.matches) == 1
        assert results.matches[0].repository == "test-org/repo1"
        assert results.matches[0].package_name == "malicious-package"
        assert results.repositories_scanned == 3
        assert results.files_scanned == 12  # 3 + 5 + 4

    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_organization_repositories')
    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_team_repositories')
    def test_team_first_org_scan_no_teams(self, mock_discover_team, mock_discover_org):
        """Test team-first scanning when organization has no teams."""
        
        # Setup mocks - no teams
        mock_discover_org.return_value = self.mock_repos
        
        # Create scanner
        scanner = GitHubIOCScanner(self.config)
        scanner.github_client.get_organization_teams = Mock(return_value=[])
        
        # Mock scan_repository_for_iocs to return no matches
        with patch.object(scanner, 'scan_repository_for_iocs') as mock_scan:
            mock_scan.return_value = ([], 5)
            
            # Execute team-first scan
            import time
            start_time = time.time()
            ioc_hash = "test_hash"
            
            results = scanner._scan_team_first_organization(ioc_hash, start_time)
            
            # All repositories should be scanned as "unassigned"
            assert results.repositories_scanned == 3
            assert results.files_scanned == 15  # 3 repos * 5 files each

    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_organization_repositories')
    def test_team_first_org_scan_team_discovery_failure(self, mock_discover_org):
        """Test team-first scanning when team discovery fails."""
        
        # Setup mocks
        mock_discover_org.return_value = self.mock_repos
        
        # Create scanner
        scanner = GitHubIOCScanner(self.config)
        scanner.github_client.get_organization_teams = Mock(
            side_effect=AuthenticationError("Authentication failed")
        )
        
        # Execute team-first scan - should handle the error gracefully
        import time
        start_time = time.time()
        ioc_hash = "test_hash"
        
        with pytest.raises(AuthenticationError):
            scanner._scan_team_first_organization(ioc_hash, start_time)

    def test_display_team_results_with_matches(self):
        """Test the _display_team_results method with matches."""
        
        scanner = GitHubIOCScanner(self.config)
        
        # Create mock matches
        matches = [
            IOCMatch(
                repository="test-org/repo1",
                file_path="package.json",
                package_name="malicious-package",
                version="1.0.0",
                line_number=10,
                context="test context"
            ),
            IOCMatch(
                repository="test-org/repo2",
                file_path="requirements.txt", 
                package_name="bad-package",
                version="2.0.0",
                line_number=5,
                context="test context 2"
            )
        ]
        
        # Capture output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            scanner._display_team_results("Test Team", matches, 2, 10)
            output = captured_output.getvalue()
            
            # Verify output contains expected elements
            assert "TEAM 'Test Team' - THREATS DETECTED" in output
            assert "Found 2 indicators of compromise" in output
            assert "test-org/repo1" in output
            assert "test-org/repo2" in output
            assert "malicious-package" in output
            assert "bad-package" in output
            
        finally:
            sys.stdout = sys.__stdout__

    def test_display_team_results_no_matches(self):
        """Test the _display_team_results method with no matches."""
        
        scanner = GitHubIOCScanner(self.config)
        
        # Capture output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            scanner._display_team_results("Clean Team", [], 5, 25)
            output = captured_output.getvalue()
            
            # Verify output contains expected elements
            assert "TEAM 'Clean Team' - NO THREATS DETECTED" in output
            assert "Repositories scanned: 5" in output
            assert "Files analyzed: 25" in output
            
        finally:
            sys.stdout = sys.__stdout__

    def test_config_validation_team_first_org(self):
        """Test configuration validation for team-first organization scanning."""
        
        # Test valid configuration
        valid_config = ScanConfig(
            org="test-org",
            team_first_org=True,
            ioc_files=[self.ioc_file]
        )
        
        scanner = GitHubIOCScanner(valid_config)
        # Should not raise any exceptions
        scanner._validate_scan_config()
        
        # Test invalid configuration - team_first_org without org
        invalid_config = ScanConfig(
            team_first_org=True,
            ioc_files=[self.ioc_file]
        )
        
        scanner = GitHubIOCScanner(invalid_config)
        with pytest.raises(Exception):  # Should raise configuration error
            scanner._validate_scan_config()

    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_organization_repositories')
    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.discover_team_repositories')
    @patch('github_ioc_scanner.scanner.GitHubIOCScanner.scan_repository_for_iocs')
    def test_team_first_org_scan_repository_removal(self, mock_scan_repo, mock_discover_team, mock_discover_org):
        """Test that repositories are properly removed from the remaining list after team scanning."""
        
        # Setup mocks
        mock_discover_org.return_value = self.mock_repos
        mock_discover_team.side_effect = [
            [self.mock_repos[0], self.mock_repos[1]],  # Team Alpha has repo1 and repo2
            []  # Team Beta has no repos
        ]
        mock_scan_repo.return_value = ([], 5)
        
        # Create scanner
        scanner = GitHubIOCScanner(self.config)
        scanner.github_client.get_organization_teams = Mock(return_value=self.mock_teams)
        
        # Execute team-first scan
        import time
        start_time = time.time()
        ioc_hash = "test_hash"
        
        results = scanner._scan_team_first_organization(ioc_hash, start_time)
        
        # Should scan all 3 repositories:
        # - repo1 and repo2 via Team Alpha
        # - repo3 as unassigned (since it wasn't in any team)
        assert results.repositories_scanned == 3
        
        # Verify scan_repository_for_iocs was called for each repo exactly once
        assert mock_scan_repo.call_count == 3