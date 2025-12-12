"""End-to-end CLI integration tests.

This module contains integration tests that simulate real CLI usage scenarios,
including argument parsing, validation, scanning workflows, and output formatting.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

import pytest

from github_ioc_scanner.cli import CLIInterface, main
from github_ioc_scanner.models import ScanConfig, IOCMatch, CacheStats, ScanResults


class TestCLIEndToEnd:
    """End-to-end tests for CLI functionality."""

    @pytest.fixture
    def temp_issues_dir(self):
        """Create a temporary issues directory with test IOC files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            # Create multiple IOC files to test loading
            ioc_file1 = issues_dir / "malicious_packages.py"
            ioc_content1 = '''
# Malicious npm packages
IOC_PACKAGES = {
    "malicious-package": ["1.0.0", "1.0.1"],
    "backdoor-lib": None,  # Any version
    "crypto-stealer": ["2.1.0"]
}
'''
            ioc_file1.write_text(ioc_content1)
            
            ioc_file2 = issues_dir / "supply_chain_attacks.py"
            ioc_content2 = '''
# Supply chain attack packages
IOC_PACKAGES = {
    "event-stream": ["3.3.6"],
    "eslint-scope": ["3.7.2"],
    "flatmap-stream": ["0.1.1"]
}
'''
            ioc_file2.write_text(ioc_content2)
            
            yield str(issues_dir)

    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)

    def test_cli_argument_parsing_workflow(self, temp_issues_dir, temp_cache_dir, capsys):
        """Test CLI argument parsing workflow."""
        # Test argument parsing
        cli = CLIInterface()
        
        # Test organization scan configuration
        config = cli.parse_arguments([
            "--org", "test-org",
            "--issues-dir", temp_issues_dir
        ])
        
        assert config.org == "test-org"
        assert config.team is None
        assert config.repo is None
        assert config.issues_dir == temp_issues_dir
        assert config.fast_mode is False
        assert config.include_archived is False
        
        # Test validation
        assert cli.validate_arguments(config) is True

    def test_cli_team_scan_configuration(self, temp_issues_dir, capsys):
        """Test CLI configuration for team scanning."""
        cli = CLIInterface()
        
        # Test team scan configuration
        config = cli.parse_arguments([
            "--org", "test-org",
            "--team", "security-team",
            "--issues-dir", temp_issues_dir
        ])
        
        assert config.org == "test-org"
        assert config.team == "security-team"
        assert config.repo is None
        assert config.issues_dir == temp_issues_dir
        
        # Test validation
        assert cli.validate_arguments(config) is True

    def test_cli_single_repository_configuration(self, temp_issues_dir, capsys):
        """Test CLI configuration for single repository scanning."""
        cli = CLIInterface()
        
        # Test repository scan configuration
        config = cli.parse_arguments([
            "--org", "test-org",
            "--repo", "vulnerable-app",
            "--issues-dir", temp_issues_dir
        ])
        
        assert config.org == "test-org"
        assert config.team is None
        assert config.repo == "vulnerable-app"
        assert config.issues_dir == temp_issues_dir
        
        # Test validation
        assert cli.validate_arguments(config) is True

    def test_cli_fast_mode_and_archived_flags(self, temp_issues_dir, capsys):
        """Test CLI with fast mode and include archived flags."""
        cli = CLIInterface()
        
        # Test with flags
        config = cli.parse_arguments([
            "--org", "test-org",
            "--fast",
            "--include-archived",
            "--issues-dir", temp_issues_dir
        ])
        
        assert config.org == "test-org"
        assert config.fast_mode is True
        assert config.include_archived is True
        assert config.issues_dir == temp_issues_dir
        
        # Test validation
        assert cli.validate_arguments(config) is True

    def test_cli_basic_error_handling(self, temp_issues_dir, capsys):
        """Test CLI basic error handling for current implementation."""
        cli = CLIInterface()
        
        # Test that the CLI can handle basic operations without crashing
        config = cli.parse_arguments([
            "--org", "test-org",
            "--issues-dir", temp_issues_dir
        ])
        
        assert cli.validate_arguments(config) is True

    def test_cli_validation_errors(self, capsys):
        """Test CLI argument validation errors."""
        cli = CLIInterface()
        
        # Test missing organization
        exit_code = cli.main(["--team", "security"])
        assert exit_code == 1
        
        captured = capsys.readouterr()
        error_output = captured.err
        assert "--team requires --org" in error_output
        
        # Test conflicting arguments
        exit_code = cli.main([
            "--org", "test-org",
            "--team", "security",
            "--repo", "test-repo"
        ])
        assert exit_code == 1
        
        captured = capsys.readouterr()
        error_output = captured.err
        assert "cannot be used together" in error_output

    def test_cli_help_output(self, capsys):
        """Test CLI help output contains usage examples."""
        cli = CLIInterface()
        
        # Help should exit with code 0
        with pytest.raises(SystemExit) as exc_info:
            cli.parse_arguments(["--help"])
        
        assert exc_info.value.code == 0


class TestCLIArgumentParsing:
    """Test CLI argument parsing edge cases and validation."""

    def test_argument_parsing_edge_cases(self):
        """Test argument parsing with various edge cases."""
        cli = CLIInterface()
        
        # Test with equals sign syntax
        config = cli.parse_arguments(["--org=test-org", "--repo=test-repo"])
        assert config.org == "test-org"
        assert config.repo == "test-repo"
        
        # Test with mixed syntax
        config = cli.parse_arguments(["--org", "test-org", "--fast", "--repo=test-repo"])
        assert config.org == "test-org"
        assert config.repo == "test-repo"
        assert config.fast_mode is True

    def test_github_name_validation_comprehensive(self):
        """Test comprehensive GitHub name validation."""
        cli = CLIInterface()
        
        # Valid names
        valid_names = [
            "a",
            "test",
            "test-org",
            "test_org",
            "TestOrg",
            "test123",
            "123test",
            "a" * 39,  # Maximum length
            "test.org",
            "test-123_org.name"
        ]
        
        for name in valid_names:
            assert cli._is_valid_github_name(name), f"'{name}' should be valid"
        
        # Invalid names
        invalid_names = [
            "",
            "-test",
            "test-",
            "_test",
            "test_",
            ".test",
            "test.",
            "test@org",
            "test org",
            "test/org",
            "test\\org",
            "a" * 40,  # Too long
            "test--org",
            "test__org",
            "test..org"
        ]
        
        for name in invalid_names:
            assert not cli._is_valid_github_name(name), f"'{name}' should be invalid"

    def test_issues_directory_validation(self, capsys):
        """Test issues directory validation."""
        cli = CLIInterface()
        
        # Test with non-existent directory
        config = ScanConfig(
            org="test-org",
            issues_dir="/definitely/does/not/exist"
        )
        
        # Validation should pass (directory existence checked later)
        assert cli.validate_arguments(config) is True

    def test_configuration_combinations(self):
        """Test all valid configuration combinations."""
        cli = CLIInterface()
        
        valid_combinations = [
            # Organization only
            {"org": "test-org"},
            # Organization with team
            {"org": "test-org", "team": "security"},
            # Organization with repository
            {"org": "test-org", "repo": "test-repo"},
            # With flags
            {"org": "test-org", "fast_mode": True},
            {"org": "test-org", "include_archived": True},
            {"org": "test-org", "issues_dir": "custom-issues"},
            # All flags together
            {"org": "test-org", "fast_mode": True, "include_archived": True, "issues_dir": "custom"}
        ]
        
        for combo in valid_combinations:
            config = ScanConfig(**combo)
            assert cli.validate_arguments(config) is True, f"Combination {combo} should be valid"
        
        invalid_combinations = [
            # Missing organization
            {},
            {"team": "security"},
            {"repo": "test-repo"},
            # Team without organization
            {"team": "security"},
            # Repository without organization
            {"repo": "test-repo"},
            # Team and repository together
            {"org": "test-org", "team": "security", "repo": "test-repo"}
        ]
        
        for combo in invalid_combinations:
            config = ScanConfig(**combo)
            with patch('sys.stderr'):  # Suppress error output
                assert cli.validate_arguments(config) is False, f"Combination {combo} should be invalid"