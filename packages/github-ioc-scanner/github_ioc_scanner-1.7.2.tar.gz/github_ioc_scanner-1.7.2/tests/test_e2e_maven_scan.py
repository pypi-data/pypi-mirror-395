"""End-to-end integration tests for Maven scanning functionality.

This module tests the complete Maven scanning workflow including:
- Maven parser integration with the scanner
- Maven IOC matching against pom.xml dependencies
- Real-world POM file parsing scenarios
"""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import Mock, patch

import pytest

from github_ioc_scanner.scanner import GitHubIOCScanner
from github_ioc_scanner.github_client import GitHubClient
from github_ioc_scanner.cache import CacheManager
from github_ioc_scanner.ioc_loader import IOCLoader
from github_ioc_scanner.parsers.maven import MavenParser
from github_ioc_scanner.parsers.factory import get_parser
from github_ioc_scanner.models import (
    ScanConfig, Repository, FileInfo, APIResponse, ScanResults,
    FileContent, PackageDependency, IOCMatch, IOCDefinition
)


class TestMavenParserIntegration:
    """Integration tests for Maven parser with the parser factory."""
    
    def test_maven_parser_registered_in_factory(self):
        """Test that Maven parser is properly registered in the parser factory."""
        parser = get_parser("pom.xml")
        assert parser is not None
        assert isinstance(parser, MavenParser)
    
    def test_maven_parser_for_nested_pom(self):
        """Test that Maven parser is returned for nested pom.xml paths."""
        parser = get_parser("backend/pom.xml")
        assert parser is not None
        assert isinstance(parser, MavenParser)
        
        parser = get_parser("modules/core/pom.xml")
        assert parser is not None
        assert isinstance(parser, MavenParser)
    
    def test_maven_parser_not_returned_for_other_files(self):
        """Test that Maven parser is not returned for non-pom.xml files."""
        parser = get_parser("package.json")
        assert parser is None or not isinstance(parser, MavenParser)
        
        parser = get_parser("requirements.txt")
        assert parser is None or not isinstance(parser, MavenParser)


class TestMavenIOCMatching:
    """Integration tests for Maven IOC matching."""
    
    @pytest.fixture
    def temp_issues_dir_with_maven_iocs(self):
        """Create a temporary issues directory with Maven IOC definitions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            # Create test IOC file with Maven packages
            ioc_file = issues_dir / "test_maven_ioc.py"
            ioc_content = '''
# Test Maven IOC definitions
IOC_PACKAGES = {
    "malicious-npm-package": ["1.0.0", "1.0.1"],
}

MAVEN_IOC_PACKAGES = {
    "org.malicious:evil-lib": {"1.0.0", "1.0.1", "2.0.0"},
    "com.attacker:backdoor": {"3.5.0"},
    "io.compromised:data-stealer": None,  # Any version
}
'''
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)
    
    def test_ioc_loader_loads_maven_packages(self, temp_issues_dir_with_maven_iocs):
        """Test that IOC loader correctly loads Maven IOC packages."""
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir_with_maven_iocs)
        ioc_definitions = ioc_loader.load_iocs()
        
        assert len(ioc_definitions) == 1
        
        maven_packages = ioc_loader.get_all_maven_packages()
        assert len(maven_packages) == 3
        assert "org.malicious:evil-lib" in maven_packages
        assert "com.attacker:backdoor" in maven_packages
        assert "io.compromised:data-stealer" in maven_packages
        
        # Check version sets
        assert maven_packages["org.malicious:evil-lib"] == {"1.0.0", "1.0.1", "2.0.0"}
        assert maven_packages["com.attacker:backdoor"] == {"3.5.0"}
        assert maven_packages["io.compromised:data-stealer"] is None  # Any version
    
    def test_is_package_compromised_maven(self, temp_issues_dir_with_maven_iocs):
        """Test checking if Maven packages are compromised."""
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir_with_maven_iocs)
        ioc_loader.load_iocs()
        
        # Test specific version match
        assert ioc_loader.is_package_compromised(
            "org.malicious:evil-lib", "1.0.0", package_type="maven"
        )
        assert ioc_loader.is_package_compromised(
            "org.malicious:evil-lib", "2.0.0", package_type="maven"
        )
        
        # Test version not in IOC list
        assert not ioc_loader.is_package_compromised(
            "org.malicious:evil-lib", "3.0.0", package_type="maven"
        )
        
        # Test any version match (None)
        assert ioc_loader.is_package_compromised(
            "io.compromised:data-stealer", "1.0.0", package_type="maven"
        )
        assert ioc_loader.is_package_compromised(
            "io.compromised:data-stealer", "999.999.999", package_type="maven"
        )
        
        # Test non-existent package
        assert not ioc_loader.is_package_compromised(
            "org.safe:good-lib", "1.0.0", package_type="maven"
        )
    
    def test_ioc_hash_includes_maven_packages(self, temp_issues_dir_with_maven_iocs):
        """Test that IOC hash calculation includes Maven packages."""
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir_with_maven_iocs)
        ioc_loader.load_iocs()
        
        hash1 = ioc_loader.get_ioc_hash()
        assert hash1 is not None
        assert len(hash1) == 64  # SHA-256 hex digest
        
        # Modify Maven IOCs and verify hash changes
        ioc_file = Path(temp_issues_dir_with_maven_iocs) / "test_maven_ioc.py"
        new_content = '''
IOC_PACKAGES = {
    "malicious-npm-package": ["1.0.0", "1.0.1"],
}

MAVEN_IOC_PACKAGES = {
    "org.malicious:evil-lib": {"1.0.0", "1.0.1", "2.0.0", "3.0.0"},  # Added version
    "com.attacker:backdoor": {"3.5.0"},
}
'''
        ioc_file.write_text(new_content)
        
        # Reload and check hash changed
        ioc_loader2 = IOCLoader(issues_dir=temp_issues_dir_with_maven_iocs)
        ioc_loader2.load_iocs()
        hash2 = ioc_loader2.get_ioc_hash()
        
        assert hash2 != hash1


class TestMavenScanningWorkflow:
    """End-to-end tests for Maven scanning workflow."""
    
    @pytest.fixture
    def temp_cache_dir(self):
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_path = Path(temp_dir) / "cache.sqlite3"
            yield str(cache_path)
    
    @pytest.fixture
    def temp_issues_dir_with_maven_iocs(self):
        """Create a temporary issues directory with Maven IOC definitions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            ioc_file = issues_dir / "test_maven_ioc.py"
            ioc_content = '''
IOC_PACKAGES = {
    "malicious-npm-package": ["1.0.0"],
}

MAVEN_IOC_PACKAGES = {
    "org.springframework:spring-core": {"5.3.23"},  # Matches fixture
    "com.google.guava:guava": {"31.1-jre"},  # Matches fixture
    "org.malicious:evil-lib": {"1.0.0"},
}
'''
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)
    
    @pytest.fixture
    def mock_maven_repository(self):
        """Create mock data for a Maven repository."""
        return {
            "repository": Repository(
                name="java-backend",
                full_name="test-org/java-backend",
                archived=False,
                default_branch="main",
                updated_at=datetime.now(timezone.utc)
            ),
            "files": [
                FileInfo(path="pom.xml", sha="maven123", size=2048),
            ],
            "file_contents": {
                "pom.xml": FileContent(
                    content='''<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>java-backend</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.3.23</version>
        </dependency>
        <dependency>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
            <version>31.1-jre</version>
        </dependency>
        <dependency>
            <groupId>org.safe</groupId>
            <artifactId>safe-lib</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
</project>
''',
                    sha="maven123",
                    size=2048
                )
            }
        }
    
    def test_maven_parser_extracts_dependencies_correctly(self):
        """Test that Maven parser correctly extracts dependencies from pom.xml."""
        parser = MavenParser()
        
        pom_content = '''<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>test-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.3.23</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
'''
        
        dependencies = parser.parse(pom_content)
        
        assert len(dependencies) == 2
        
        spring_dep = next(d for d in dependencies if 'spring-core' in d.name)
        assert spring_dep.name == 'org.springframework:spring-core'
        assert spring_dep.version == '5.3.23'
        assert spring_dep.dependency_type == 'compile'
        
        junit_dep = next(d for d in dependencies if 'junit' in d.name)
        assert junit_dep.name == 'junit:junit'
        assert junit_dep.version == '4.13.2'
        assert junit_dep.dependency_type == 'test'


class TestMavenWithRealWorldPOMs:
    """Tests using real-world POM file fixtures."""
    
    @pytest.fixture
    def fixtures_dir(self):
        """Return path to Maven fixtures directory."""
        return Path(__file__).parent / "fixtures" / "maven"
    
    def _read_fixture(self, fixtures_dir: Path, filename: str) -> str:
        """Read a fixture file."""
        filepath = fixtures_dir / filename
        with open(filepath, 'r') as f:
            return f.read()
    
    def test_parse_simple_pom_fixture(self, fixtures_dir):
        """Test parsing simple_pom.xml fixture."""
        parser = MavenParser()
        content = self._read_fixture(fixtures_dir, 'simple_pom.xml')
        
        dependencies = parser.parse(content)
        
        assert len(dependencies) == 3
        
        # Verify all expected dependencies are present
        dep_names = [d.name for d in dependencies]
        assert 'org.springframework:spring-core' in dep_names
        assert 'com.google.guava:guava' in dep_names
        assert 'junit:junit' in dep_names
        
        # Verify versions
        spring_dep = next(d for d in dependencies if 'spring-core' in d.name)
        assert spring_dep.version == '5.3.23'
        
        guava_dep = next(d for d in dependencies if 'guava' in d.name)
        assert guava_dep.version == '31.1-jre'
        
        junit_dep = next(d for d in dependencies if 'junit' in d.name)
        assert junit_dep.version == '4.13.2'
        assert junit_dep.dependency_type == 'test'
    
    def test_parse_pom_with_properties_fixture(self, fixtures_dir):
        """Test parsing pom_with_properties.xml fixture with property resolution."""
        parser = MavenParser()
        content = self._read_fixture(fixtures_dir, 'pom_with_properties.xml')
        
        dependencies = parser.parse(content)
        
        assert len(dependencies) == 5
        
        # Verify property resolution worked
        spring_core = next(d for d in dependencies if 'spring-core' in d.name)
        assert spring_core.version == '5.3.23'  # Resolved from ${spring.version}
        
        spring_web = next(d for d in dependencies if 'spring-web' in d.name)
        assert spring_web.version == '5.3.23'  # Same property
        
        jackson = next(d for d in dependencies if 'jackson-databind' in d.name)
        assert jackson.version == '2.14.0'  # Resolved from ${jackson.version}
        
        lombok = next(d for d in dependencies if 'lombok' in d.name)
        assert lombok.version == '1.18.30'  # Resolved from ${lombok.version}
        assert lombok.dependency_type == 'provided'
        
        internal = next(d for d in dependencies if 'internal-lib' in d.name)
        assert internal.version == '2.0.0'  # Resolved from ${project.version}
    
    def test_parse_pom_with_dependency_management_fixture(self, fixtures_dir):
        """Test parsing pom_with_dependency_management.xml fixture."""
        parser = MavenParser()
        content = self._read_fixture(fixtures_dir, 'pom_with_dependency_management.xml')
        
        dependencies = parser.parse(content)
        
        # Should have dependencies from both dependencyManagement and dependencies sections
        assert len(dependencies) == 5
        
        # Check dependencyManagement entries
        spring_boot_deps = next(d for d in dependencies if 'spring-boot-dependencies' in d.name)
        assert spring_boot_deps.version == '3.1.5'  # Resolved from ${spring-boot.version}
        assert 'dependencyManagement' in spring_boot_deps.dependency_type
        
        # Check regular dependencies with managed versions
        starter_web = next(d for d in dependencies if 'spring-boot-starter-web' in d.name)
        assert starter_web.version == 'managed'  # No explicit version
        assert starter_web.dependency_type == 'compile'
    
    def test_parse_malformed_pom_fixture(self, fixtures_dir):
        """Test that malformed POM raises appropriate error."""
        parser = MavenParser()
        content = self._read_fixture(fixtures_dir, 'malformed_pom.xml')
        
        with pytest.raises(ValueError, match="Invalid XML"):
            parser.parse(content)


class TestMavenIOCStatistics:
    """Tests for Maven IOC statistics."""
    
    @pytest.fixture
    def temp_issues_dir_with_maven_iocs(self):
        """Create a temporary issues directory with Maven IOC definitions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            issues_dir = Path(temp_dir) / "issues"
            issues_dir.mkdir()
            
            ioc_file = issues_dir / "test_ioc.py"
            ioc_content = '''
IOC_PACKAGES = {
    "npm-package-1": ["1.0.0"],
    "npm-package-2": ["2.0.0"],
    "npm-package-3": None,
}

MAVEN_IOC_PACKAGES = {
    "org.malicious:lib1": {"1.0.0"},
    "org.malicious:lib2": {"2.0.0"},
}
'''
            ioc_file.write_text(ioc_content)
            
            yield str(issues_dir)
    
    def test_ioc_statistics_include_maven(self, temp_issues_dir_with_maven_iocs):
        """Test that IOC statistics include Maven package counts."""
        ioc_loader = IOCLoader(issues_dir=temp_issues_dir_with_maven_iocs)
        ioc_loader.load_iocs()
        
        stats = ioc_loader.get_ioc_statistics()
        
        assert stats["npm_packages"] == 3
        assert stats["maven_packages"] == 2
        assert stats["total_packages"] == 5
        assert stats["source_files"] == 1
