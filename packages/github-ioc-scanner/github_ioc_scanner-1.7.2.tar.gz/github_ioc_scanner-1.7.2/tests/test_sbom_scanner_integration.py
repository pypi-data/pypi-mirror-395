"""Tests for SBOM scanner integration."""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock

from src.github_ioc_scanner.scanner import GitHubIOCScanner
from src.github_ioc_scanner.models import ScanConfig, Repository, FileContent, PackageDependency, IOCMatch
from src.github_ioc_scanner.cache import CacheManager
from src.github_ioc_scanner.github_client import GitHubClient
from src.github_ioc_scanner.ioc_loader import IOCLoader


class TestSBOMScannerIntegration:
    """Test SBOM integration with the main scanner."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = ScanConfig(
            org="test-org",
            repo="test-repo",
            enable_sbom=True
        )
        
        self.mock_github_client = Mock(spec=GitHubClient)
        self.mock_cache_manager = Mock(spec=CacheManager)
        self.mock_ioc_loader = Mock(spec=IOCLoader)
        
        # Mock IOC loader
        self.mock_ioc_loader.load_iocs.return_value = {
            "malicious-package": ["1.0.0", "2.0.0"],
            "suspicious-lib": ["*"]
        }
        self.mock_ioc_loader.get_ioc_hash.return_value = "test-hash"

    def test_scanner_initialization_with_sbom(self):
        """Test scanner initialization with SBOM enabled."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        assert scanner.enable_sbom_scanning is True
        assert scanner.SBOM_PATTERNS is not None
        assert len(scanner.SBOM_PATTERNS) > 0

    def test_get_scan_patterns_with_sbom_enabled(self):
        """Test that scan patterns include SBOM files when enabled."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        patterns = scanner._get_scan_patterns()
        
        # Should include both lockfile and SBOM patterns
        assert any("package.json" in pattern for pattern in patterns)
        assert any("sbom.json" in pattern for pattern in patterns)
        assert any("bom.json" in pattern for pattern in patterns)

    def test_get_scan_patterns_with_sbom_disabled(self):
        """Test that scan patterns exclude SBOM files when disabled."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=False
        )
        
        patterns = scanner._get_scan_patterns()
        
        # Should only include lockfile patterns
        assert any("package.json" in pattern for pattern in patterns)
        assert not any("sbom.json" in pattern for pattern in patterns)

    def test_discover_sbom_files_in_repository(self):
        """Test SBOM file discovery in repository."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        # Mock file search results
        from src.github_ioc_scanner.models import FileInfo
        mock_files = [
            FileInfo(path="sbom.json", sha="abc123", size=1024),
            FileInfo(path="frontend/bom.xml", sha="def456", size=2048)
        ]
        self.mock_github_client.search_files.return_value = mock_files
        
        sbom_files = scanner.discover_sbom_files_in_repository(repo)
        
        assert len(sbom_files) == 2
        assert "sbom.json" in sbom_files
        assert "frontend/bom.xml" in sbom_files
        
        # Verify search was called with SBOM patterns
        self.mock_github_client.search_files.assert_called_once_with(
            repo, scanner.SBOM_PATTERNS, fast_mode=False
        )

    def test_scan_sbom_file_for_iocs(self):
        """Test scanning a single SBOM file for IOCs."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        # Mock file content
        sbom_content = {
            "bomFormat": "CycloneDX",
            "components": [
                {
                    "name": "malicious-package",
                    "version": "1.0.0",
                    "purl": "pkg:npm/malicious-package@1.0.0"
                },
                {
                    "name": "safe-package",
                    "version": "2.0.0",
                    "purl": "pkg:npm/safe-package@2.0.0"
                }
            ]
        }
        
        file_content = FileContent(
            content=json.dumps(sbom_content),
            sha="abc123",
            size=len(json.dumps(sbom_content))
        )
        
        # Mock cache and file fetching
        self.mock_cache_manager.get_scan_results.return_value = None
        scanner.fetch_file_content_with_cache = Mock(return_value=file_content)
        scanner.parse_sbom_packages_with_cache = Mock(return_value=[
            PackageDependency(name="malicious-package", version="1.0.0", dependency_type="npm"),
            PackageDependency(name="safe-package", version="2.0.0", dependency_type="npm")
        ])
        scanner.match_packages_against_iocs = Mock(return_value=[
            IOCMatch(
                repo="test-org/test-repo",
                file_path="sbom.json",
                package_name="malicious-package",
                version="1.0.0",
                ioc_source="test-ioc"
            )
        ])
        
        matches = scanner.scan_sbom_file_for_iocs(repo, "sbom.json", "test-hash")
        
        assert len(matches) == 1
        assert matches[0].package_name == "malicious-package"
        assert matches[0].file_path == "sbom.json"

    def test_parse_sbom_packages_with_cache(self):
        """Test SBOM package parsing with caching."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        # Mock SBOM content
        sbom_content = {
            "spdxVersion": "SPDX-2.3",
            "packages": [
                {"name": "express", "versionInfo": "4.18.2"},
                {"name": "lodash", "versionInfo": "4.17.21"}
            ]
        }
        
        file_content = FileContent(
            content=json.dumps(sbom_content),
            sha="abc123",
            size=1024
        )
        
        # Mock cache miss
        self.mock_cache_manager.get_parsed_packages.return_value = None
        
        packages = scanner.parse_sbom_packages_with_cache(repo, "sbom.json", file_content)
        
        assert len(packages) == 2
        assert packages[0].name == "express"
        assert packages[0].version == "4.18.2"
        assert packages[0].dependency_type == "spdx"
        
        # Verify cache was called
        self.mock_cache_manager.get_parsed_packages.assert_called_once()
        self.mock_cache_manager.store_parsed_packages.assert_called_once()

    def test_scan_combined_files_for_iocs(self):
        """Test scanning both lockfiles and SBOM files."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        # Mock the individual scan methods
        scanner._scan_lockfiles_only = Mock(return_value=(
            [IOCMatch(repo="test-org/test-repo", file_path="package.json",
                     package_name="lockfile-threat", version="1.0.0", 
                     ioc_source="test-ioc")], 
            1
        ))
        
        scanner.scan_sbom_files = Mock(return_value=(
            [IOCMatch(repo="test-org/test-repo", file_path="sbom.json",
                     package_name="sbom-threat", version="2.0.0",
                     ioc_source="test-ioc")],
            1
        ))
        
        matches, files_scanned = scanner.scan_combined_files_for_iocs(repo, "test-hash")
        
        assert len(matches) == 2
        assert files_scanned == 2
        assert matches[0].package_name == "lockfile-threat"
        assert matches[1].package_name == "sbom-threat"

    def test_sbom_only_mode(self):
        """Test SBOM-only scanning mode."""
        config = ScanConfig(
            org="test-org",
            repo="test-repo",
            sbom_only=True
        )
        
        scanner = GitHubIOCScanner(
            config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        # Mock SBOM scanning
        scanner.scan_sbom_files = Mock(return_value=([], 0))
        
        matches, files_scanned = scanner.scan_repository_for_iocs(repo, "test-hash")
        
        # Should only call SBOM scanning
        scanner.scan_sbom_files.assert_called_once_with(repo, "test-hash")

    def test_disable_sbom_mode(self):
        """Test disabled SBOM scanning mode."""
        config = ScanConfig(
            org="test-org",
            repo="test-repo",
            disable_sbom=True
        )
        
        scanner = GitHubIOCScanner(
            config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=False
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        # Mock lockfile scanning
        scanner._scan_lockfiles_only = Mock(return_value=([], 0))
        
        matches, files_scanned = scanner.scan_repository_for_iocs(repo, "test-hash")
        
        # Should only call lockfile scanning
        scanner._scan_lockfiles_only.assert_called_once_with(repo, "test-hash")

    def test_get_sbom_scan_statistics(self):
        """Test SBOM scan statistics collection."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        # Mock cache stats
        mock_cache_stats = Mock()
        mock_cache_stats.cache_entries = [
            "sbom:org/repo:sbom.json",
            "sbom_packages:org/repo:bom.xml",
            "regular:org/repo:package.json"
        ]
        self.mock_cache_manager.get_cache_stats.return_value = mock_cache_stats
        
        stats = scanner.get_sbom_scan_statistics()
        
        assert "sbom_files_cached" in stats
        assert "sbom_packages_cached" in stats
        assert "sbom_scan_results_cached" in stats

    @patch('src.github_ioc_scanner.scanner.logger')
    def test_error_handling_in_sbom_scanning(self, mock_logger):
        """Test error handling during SBOM scanning."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        # Mock file discovery to raise an exception
        self.mock_github_client.search_files.side_effect = Exception("API Error")
        
        sbom_files = scanner.discover_sbom_files_in_repository(repo)
        
        assert sbom_files == []
        mock_logger.error.assert_called()


class TestSBOMCacheIntegration:
    """Test SBOM caching integration."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = ScanConfig(org="test-org", enable_sbom=True)
        self.mock_github_client = Mock(spec=GitHubClient)
        self.mock_cache_manager = Mock(spec=CacheManager)
        self.mock_ioc_loader = Mock(spec=IOCLoader)

    def test_sbom_cache_key_generation(self):
        """Test that SBOM files use proper cache keys."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        # Mock file content
        file_content = FileContent(content="{}", sha="abc123", size=2)
        scanner.fetch_file_content_with_cache = Mock(return_value=file_content)
        scanner.parse_sbom_packages_with_cache = Mock(return_value=[])
        scanner.match_packages_against_iocs = Mock(return_value=[])
        
        # Mock cache miss
        self.mock_cache_manager.get_scan_results.return_value = None
        
        scanner.scan_sbom_file_for_iocs(repo, "sbom.json", "test-hash")
        
        # Verify cache was called with SBOM-specific key
        expected_cache_key = "sbom:test-org/test-repo:sbom.json"
        self.mock_cache_manager.get_scan_results.assert_called_with(
            expected_cache_key, "sbom.json", "abc123", "test-hash"
        )

    def test_sbom_package_cache_integration(self):
        """Test SBOM package parsing cache integration."""
        scanner = GitHubIOCScanner(
            self.config,
            self.mock_github_client,
            self.mock_cache_manager,
            self.mock_ioc_loader,
            enable_sbom_scanning=True
        )
        
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=None
        )
        
        file_content = FileContent(
            content='{"packages": [{"name": "test", "version": "1.0.0"}]}',
            sha="abc123",
            size=100
        )
        
        # Test cache hit
        cached_packages = [PackageDependency(name="cached-pkg", version="1.0.0", dependency_type="generic")]
        self.mock_cache_manager.get_parsed_packages.return_value = cached_packages
        
        packages = scanner.parse_sbom_packages_with_cache(repo, "sbom.json", file_content)
        
        assert packages == cached_packages
        self.mock_cache_manager.get_parsed_packages.assert_called_once_with(
            "sbom_packages:test-org/test-repo:sbom.json", "abc123"
        )