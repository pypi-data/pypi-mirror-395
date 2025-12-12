"""Tests for the CLI interface."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch

from github_ioc_scanner.cli import CLIInterface
from github_ioc_scanner.models import ScanConfig, IOCMatch, CacheStats


class TestCLIInterface:
    """Test cases for the CLIInterface class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cli = CLIInterface()

    def test_parse_arguments_org_only(self):
        """Test parsing arguments for organization-only scan."""
        args = ["--org", "myorg"]
        config = self.cli.parse_arguments(args)
        
        assert config.org == "myorg"
        assert config.team is None
        assert config.repo is None
        assert config.fast_mode is False
        assert config.include_archived is False
        assert config.issues_dir is None  # Default is None, not "issues"

    def test_parse_arguments_org_and_team(self):
        """Test parsing arguments for organization and team scan."""
        args = ["--org", "myorg", "--team", "security"]
        config = self.cli.parse_arguments(args)
        
        assert config.org == "myorg"
        assert config.team == "security"
        assert config.repo is None
        assert config.fast_mode is False
        assert config.include_archived is False

    def test_parse_arguments_org_and_repo(self):
        """Test parsing arguments for specific repository scan."""
        args = ["--org", "myorg", "--repo", "myrepo"]
        config = self.cli.parse_arguments(args)
        
        assert config.org == "myorg"
        assert config.team is None
        assert config.repo == "myrepo"
        assert config.fast_mode is False
        assert config.include_archived is False

    def test_parse_arguments_with_flags(self):
        """Test parsing arguments with optional flags."""
        args = ["--org", "myorg", "--fast", "--include-archived", "--issues-dir", "custom-issues"]
        config = self.cli.parse_arguments(args)
        
        assert config.org == "myorg"
        assert config.fast_mode is True
        assert config.include_archived is True
        assert config.issues_dir == "custom-issues"

    def test_validate_arguments_valid_org_only(self):
        """Test validation of valid organization-only configuration."""
        config = ScanConfig(org="myorg")
        assert self.cli.validate_arguments(config) is True

    def test_validate_arguments_valid_org_and_team(self):
        """Test validation of valid organization and team configuration."""
        config = ScanConfig(org="myorg", team="security")
        assert self.cli.validate_arguments(config) is True

    def test_validate_arguments_valid_org_and_repo(self):
        """Test validation of valid organization and repository configuration."""
        config = ScanConfig(org="myorg", repo="myrepo")
        assert self.cli.validate_arguments(config) is True

    def test_validate_arguments_missing_org(self):
        """Test validation fails when organization is missing."""
        config = ScanConfig()
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = self.cli.validate_arguments(config)
            assert result is False
            assert "--org is required" in mock_stderr.getvalue()

    def test_validate_arguments_team_without_org(self):
        """Test validation fails when team is specified without organization."""
        config = ScanConfig(team="security")
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = self.cli.validate_arguments(config)
            assert result is False
            assert "--team requires --org" in mock_stderr.getvalue()

    def test_validate_arguments_repo_without_org(self):
        """Test validation fails when repository is specified without organization."""
        config = ScanConfig(repo="myrepo")
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = self.cli.validate_arguments(config)
            assert result is False
            assert "--repo requires --org" in mock_stderr.getvalue()

    def test_validate_arguments_team_and_repo_together(self):
        """Test validation fails when both team and repository are specified."""
        config = ScanConfig(org="myorg", team="security", repo="myrepo")
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = self.cli.validate_arguments(config)
            assert result is False
            assert "cannot be used together" in mock_stderr.getvalue()

    def test_validate_arguments_invalid_org_name(self):
        """Test validation fails for invalid organization name."""
        config = ScanConfig(org="invalid-org-")
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = self.cli.validate_arguments(config)
            assert result is False
            assert "Invalid organization name" in mock_stderr.getvalue()

    def test_validate_arguments_invalid_team_name(self):
        """Test validation fails for invalid team name."""
        config = ScanConfig(org="myorg", team="-invalid")
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = self.cli.validate_arguments(config)
            assert result is False
            assert "Invalid team name" in mock_stderr.getvalue()

    def test_validate_arguments_invalid_repo_name(self):
        """Test validation fails for invalid repository name."""
        config = ScanConfig(org="myorg", repo="invalid-repo-")
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            result = self.cli.validate_arguments(config)
            assert result is False
            assert "Invalid repository name" in mock_stderr.getvalue()

    def test_is_valid_github_name_valid_names(self):
        """Test validation of valid GitHub names."""
        valid_names = [
            "myorg",
            "my-org",
            "my_org",
            "MyOrg123",
            "org.name",
            "a",
            "123",
        ]
        
        for name in valid_names:
            assert self.cli._is_valid_github_name(name), f"'{name}' should be valid"

    def test_is_valid_github_name_invalid_names(self):
        """Test validation of invalid GitHub names."""
        invalid_names = [
            "",
            "-invalid",
            "invalid-",
            "invalid@name",
            "invalid name",
            "invalid/name",
            "a" * 101,  # Too long
        ]
        
        for name in invalid_names:
            assert not self.cli._is_valid_github_name(name), f"'{name}' should be invalid"

    def test_display_results_with_matches(self):
        """Test displaying results when IOC matches are found."""
        matches = [
            IOCMatch(
                repo="myorg/repo1",
                file_path="package.json",
                package_name="malicious-package",
                version="1.0.0",
                ioc_source="test_ioc.py"
            ),
            IOCMatch(
                repo="myorg/repo2",
                file_path="requirements.txt",
                package_name="bad-package",
                version="2.1.0",
                ioc_source="test_ioc.py"
            ),
        ]
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_results(matches)
            output = mock_stdout.getvalue()
            
            assert "myorg/repo1 | package.json | malicious-package | 1.0.0" in output
            assert "myorg/repo2 | requirements.txt | bad-package | 2.1.0" in output

    def test_display_results_no_matches(self):
        """Test displaying results when no IOC matches are found."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_results([])
            output = mock_stdout.getvalue()
            
            assert "Keine Treffer gefunden." in output

    def test_display_results_sorted(self):
        """Test that results are displayed in sorted order."""
        matches = [
            IOCMatch(
                repo="myorg/repo2",
                file_path="package.json",
                package_name="z-package",
                version="1.0.0",
                ioc_source="test_ioc.py"
            ),
            IOCMatch(
                repo="myorg/repo1",
                file_path="requirements.txt",
                package_name="a-package",
                version="2.1.0",
                ioc_source="test_ioc.py"
            ),
        ]
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_results(matches)
            output = mock_stdout.getvalue()
            lines = output.strip().split('\n')
            
            # Should be sorted by repo, then file, then package
            assert "myorg/repo1" in lines[0]
            assert "myorg/repo2" in lines[1]

    def test_display_results_with_header(self):
        """Test displaying results with header."""
        matches = [
            IOCMatch(
                repo="myorg/repo1",
                file_path="package.json",
                package_name="malicious-package",
                version="1.0.0",
                ioc_source="test_ioc.py"
            ),
        ]
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_results_with_header(matches)
            output = mock_stdout.getvalue()
            
            assert "Found 1 IOC match:" in output
            assert "Repository | File | Package | Version" in output
            assert "myorg/repo1 | package.json | malicious-package | 1.0.0" in output

    def test_display_results_with_header_multiple(self):
        """Test displaying multiple results with header."""
        matches = [
            IOCMatch(
                repo="myorg/repo1",
                file_path="package.json",
                package_name="malicious-package",
                version="1.0.0",
                ioc_source="test_ioc.py"
            ),
            IOCMatch(
                repo="myorg/repo2",
                file_path="requirements.txt",
                package_name="bad-package",
                version="2.1.0",
                ioc_source="test_ioc.py"
            ),
        ]
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_results_with_header(matches)
            output = mock_stdout.getvalue()
            
            assert "Found 2 IOC matches:" in output

    def test_display_results_with_header_no_matches(self):
        """Test displaying header with no matches."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_results_with_header([])
            output = mock_stdout.getvalue()
            
            assert "Keine Treffer gefunden." in output

    def test_display_cache_stats(self):
        """Test displaying cache statistics."""
        stats = CacheStats(
            hits=150,
            misses=50,
            time_saved=45.67,
            cache_size=1000
        )
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_cache_stats(stats)
            output = mock_stdout.getvalue()
            
            assert "Cache Statistics:" in output
            assert "Hits: 150" in output
            assert "Misses: 50" in output
            assert "Hit rate: 75.0%" in output
            assert "Time saved: 45.67s" in output
            assert "Cache size: 1000 entries" in output
            assert "Cache saved 45.7 seconds" in output

    def test_display_cache_stats_no_operations(self):
        """Test displaying cache statistics when no cache operations occurred."""
        stats = CacheStats(hits=0, misses=0, time_saved=0.0, cache_size=0)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_cache_stats(stats)
            output = mock_stdout.getvalue()
            
            assert "Cache Statistics:" in output
            assert "Hits: 0" in output
            assert "Misses: 0" in output
            assert "Hit rate:" not in output  # Should not show hit rate when no operations
            assert "Time saved: 0.00s" in output

    def test_display_cache_stats_first_scan(self):
        """Test displaying cache statistics for first scan (no hits)."""
        stats = CacheStats(hits=0, misses=100, time_saved=0.0, cache_size=50)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_cache_stats(stats)
            output = mock_stdout.getvalue()
            
            assert "First scan - building cache" in output

    def test_display_error(self):
        """Test displaying error messages."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            self.cli.display_error("Test error message")
            output = mock_stderr.getvalue()
            
            assert "Error: Test error message" in output

    def test_display_warning(self):
        """Test displaying warning messages."""
        with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
            self.cli.display_warning("Test warning message")
            output = mock_stderr.getvalue()
            
            assert "Warning: Test warning message" in output

    def test_display_scan_summary(self):
        """Test displaying scan summary."""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_scan_summary(repositories_scanned=25, files_scanned=150)
            output = mock_stdout.getvalue()
            
            assert "Scan Summary:" in output
            assert "Repositories scanned: 25" in output
            assert "Files scanned: 150" in output

    def test_display_progress(self):
        """Test displaying progress messages."""
        config = ScanConfig(org="myorg")
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_progress(1, 10, "test-repo", config)
            output = mock_stdout.getvalue()
            
            # Progress display should show repository info
            assert "test-repo" in output or "1" in output

    def test_display_scan_start_org_only(self):
        """Test displaying scan start for organization-only scan."""
        config = ScanConfig(org="myorg")
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_scan_start(config)
            output = mock_stdout.getvalue()
            
            assert "Scanning organization: myorg" in output
            # IOC definitions directory is only shown in verbose mode

    def test_display_scan_start_team(self):
        """Test displaying scan start for team scan."""
        config = ScanConfig(org="myorg", team="security")
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_scan_start(config)
            output = mock_stdout.getvalue()
            
            assert "Scanning team repositories: myorg/security" in output

    def test_display_scan_start_repo(self):
        """Test displaying scan start for repository scan."""
        config = ScanConfig(org="myorg", repo="myrepo")
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_scan_start(config)
            output = mock_stdout.getvalue()
            
            assert "Scanning repository: myorg/myrepo" in output

    def test_display_scan_start_with_flags(self):
        """Test displaying scan start with optional flags."""
        config = ScanConfig(org="myorg", fast_mode=True, include_archived=True, issues_dir="custom", verbose=True)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.cli.display_scan_start(config)
            output = mock_stdout.getvalue()
            
            # Check for scan mode indicators
            assert "fast mode" in output
            assert "including archived" in output
            # IOC definitions directory is shown in verbose mode
            assert "IOC definitions directory: custom" in output

    def test_format_file_size(self):
        """Test file size formatting."""
        assert self.cli.format_file_size(500) == "500 B"
        assert self.cli.format_file_size(1536) == "1.5 KB"
        assert self.cli.format_file_size(2097152) == "2.0 MB"

    def test_format_duration(self):
        """Test duration formatting."""
        assert self.cli.format_duration(0.5) == "500ms"
        assert self.cli.format_duration(5.7) == "5.7s"
        assert self.cli.format_duration(125.3) == "2m 5.3s"

    def test_parse_arguments_help_text(self):
        """Test that help text includes usage examples."""
        with pytest.raises(SystemExit):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                self.cli.parse_arguments(["--help"])
                
        # Note: argparse exits before we can capture output in this test
        # The help text format is tested implicitly through the epilog in parse_arguments

    def test_parse_arguments_invalid_flag(self):
        """Test parsing with invalid command-line flag."""
        with pytest.raises(SystemExit):
            with patch('sys.stderr', new_callable=StringIO):
                self.cli.parse_arguments(["--invalid-flag"])


class TestCLIIntegration:
    """Integration tests for CLI functionality."""

    def test_full_validation_workflow_success(self):
        """Test complete argument parsing and validation workflow for success case."""
        cli = CLIInterface()
        
        # Test successful org-only scan
        config = cli.parse_arguments(["--org", "myorg", "--fast"])
        assert cli.validate_arguments(config) is True
        
        # Test successful team scan
        config = cli.parse_arguments(["--org", "myorg", "--team", "security"])
        assert cli.validate_arguments(config) is True
        
        # Test successful repo scan
        config = cli.parse_arguments(["--org", "myorg", "--repo", "myrepo"])
        assert cli.validate_arguments(config) is True

    def test_full_validation_workflow_failure(self):
        """Test complete argument parsing and validation workflow for failure cases."""
        cli = CLIInterface()
        
        # Test missing org
        config = cli.parse_arguments(["--team", "security"])
        with patch('sys.stderr', new_callable=StringIO):
            assert cli.validate_arguments(config) is False
        
        # Test conflicting team and repo
        config = cli.parse_arguments(["--org", "myorg", "--team", "security", "--repo", "myrepo"])
        with patch('sys.stderr', new_callable=StringIO):
            assert cli.validate_arguments(config) is False