"""Tests for SBOM parser functionality."""

import json
import pytest
from unittest.mock import Mock, patch

from src.github_ioc_scanner.parsers.sbom import SBOMParser
from src.github_ioc_scanner.models import PackageDependency


class TestSBOMParser:
    """Test cases for SBOM parser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = SBOMParser()

    def test_can_parse_sbom_files(self):
        """Test SBOM file detection."""
        # Test exact matches
        assert self.parser.can_parse("sbom.json")
        assert self.parser.can_parse("bom.json")
        assert self.parser.can_parse("cyclonedx.json")
        assert self.parser.can_parse("spdx.json")
        assert self.parser.can_parse("sbom.xml")
        assert self.parser.can_parse("SBOM.json")
        
        # Test with paths
        assert self.parser.can_parse("path/to/sbom.json")
        assert self.parser.can_parse("frontend/bom.xml")
        
        # Test keyword detection
        assert self.parser.can_parse("my-sbom-file.json")
        assert self.parser.can_parse("project-bom.xml")
        assert self.parser.can_parse("spdx-report.json")
        
        # Test non-SBOM files
        assert not self.parser.can_parse("package.json")
        assert not self.parser.can_parse("requirements.txt")
        assert not self.parser.can_parse("random.txt")

    def test_parse_spdx_json(self):
        """Test parsing SPDX JSON format."""
        spdx_content = {
            "spdxVersion": "SPDX-2.2",
            "SPDXID": "SPDXRef-DOCUMENT",
            "packages": [
                {
                    "name": "express",
                    "SPDXID": "SPDXRef-Package-express",
                    "versionInfo": "4.18.2",
                    "downloadLocation": "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
                },
                {
                    "name": "lodash",
                    "SPDXID": "SPDXRef-Package-lodash",
                    "versionInfo": "4.17.21"
                }
            ]
        }
        
        packages = self.parser.parse(json.dumps(spdx_content), "sbom.json")
        
        assert len(packages) == 2
        assert packages[0].name == "express"
        assert packages[0].version == "4.18.2"
        assert packages[0].dependency_type == "spdx"
        assert packages[1].name == "lodash"
        assert packages[1].version == "4.17.21"

    def test_parse_cyclonedx_json(self):
        """Test parsing CycloneDX JSON format."""
        cyclonedx_content = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "components": [
                {
                    "type": "library",
                    "name": "react",
                    "version": "18.2.0",
                    "purl": "pkg:npm/react@18.2.0"
                },
                {
                    "type": "library", 
                    "name": "vue",
                    "version": "3.3.4",
                    "purl": "pkg:npm/vue@3.3.4"
                }
            ]
        }
        
        packages = self.parser.parse(json.dumps(cyclonedx_content), "bom.json")
        
        assert len(packages) == 2
        assert packages[0].name == "react"
        assert packages[0].version == "18.2.0"
        assert packages[0].dependency_type == "npm"
        assert packages[1].name == "vue"
        assert packages[1].version == "3.3.4"

    def test_parse_generic_json_sbom(self):
        """Test parsing generic JSON SBOM format."""
        generic_content = {
            "packages": [
                {"name": "django", "version": "4.2.0"},
                {"name": "requests", "version": "2.31.0"}
            ],
            "metadata": {
                "tool": "custom-sbom-generator"
            }
        }
        
        packages = self.parser.parse(json.dumps(generic_content), "custom-sbom.json")
        
        assert len(packages) == 2
        assert packages[0].name == "django"
        assert packages[0].version == "4.2.0"
        assert packages[0].dependency_type == "generic"

    def test_parse_spdx_xml(self):
        """Test parsing SPDX XML format."""
        spdx_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <spdx:SpdxDocument xmlns:spdx="http://spdx.org/rdf/terms#">
            <spdx:Package>
                <spdx:name>numpy</spdx:name>
                <spdx:versionInfo>1.24.3</spdx:versionInfo>
            </spdx:Package>
            <spdx:Package>
                <spdx:name>pandas</spdx:name>
                <spdx:versionInfo>2.0.2</spdx:versionInfo>
            </spdx:Package>
        </spdx:SpdxDocument>"""
        
        packages = self.parser.parse(spdx_xml, "spdx.xml")
        
        assert len(packages) == 2
        assert packages[0].name == "numpy"
        assert packages[0].version == "1.24.3"
        assert packages[0].dependency_type == "spdx"

    def test_parse_cyclonedx_xml(self):
        """Test parsing CycloneDX XML format."""
        cyclonedx_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <bom xmlns="http://cyclonedx.org/schema/bom/1.4">
            <components>
                <component type="library">
                    <name>spring-boot</name>
                    <version>3.1.0</version>
                    <purl>pkg:maven/org.springframework.boot/spring-boot@3.1.0</purl>
                </component>
            </components>
        </bom>"""
        
        packages = self.parser.parse(cyclonedx_xml, "bom.xml")
        
        assert len(packages) == 1
        assert packages[0].name == "spring-boot"
        assert packages[0].version == "3.1.0"
        assert packages[0].dependency_type == "maven"

    def test_extract_version_from_download_location(self):
        """Test version extraction from SPDX download locations."""
        # Test various URL patterns
        assert self.parser._extract_version_from_download_location(
            "https://registry.npmjs.org/express/-/express-4.18.2.tgz"
        ) == "4.18.2"
        
        assert self.parser._extract_version_from_download_location(
            "https://github.com/user/repo/archive/v1.2.3.tar.gz"
        ) == "1.2.3"
        
        assert self.parser._extract_version_from_download_location(
            "https://pypi.org/project/django/4.2.0/"
        ) == "4.2.0"
        
        # Test no version found
        assert self.parser._extract_version_from_download_location(
            "https://github.com/user/repo"
        ) is None

    def test_extract_dependency_type_from_purl(self):
        """Test package type extraction from Package URLs."""
        assert self.parser._extract_package_type_from_purl("pkg:npm/react@18.2.0") == "npm"
        assert self.parser._extract_package_type_from_purl("pkg:pypi/django@4.2.0") == "pypi"
        assert self.parser._extract_package_type_from_purl("pkg:maven/org.springframework/spring-core@6.0.0") == "maven"
        assert self.parser._extract_package_type_from_purl("pkg:golang/github.com/gin-gonic/gin@v1.9.1") == "golang"
        
        # Test invalid or empty purl
        assert self.parser._extract_package_type_from_purl("") is None
        assert self.parser._extract_package_type_from_purl("invalid-purl") is None

    def test_parse_invalid_json(self):
        """Test handling of invalid JSON content."""
        invalid_json = "{ invalid json content"
        packages = self.parser.parse(invalid_json, "sbom.json")
        assert packages == []

    def test_parse_invalid_xml(self):
        """Test handling of invalid XML content."""
        invalid_xml = "<invalid><xml content"
        packages = self.parser.parse(invalid_xml, "sbom.xml")
        assert packages == []

    def test_parse_empty_sbom(self):
        """Test parsing empty SBOM files."""
        empty_json = "{}"
        packages = self.parser.parse(empty_json, "sbom.json")
        assert packages == []
        
        empty_xml = "<?xml version='1.0'?><root></root>"
        packages = self.parser.parse(empty_xml, "sbom.xml")
        assert packages == []

    def test_parse_malformed_packages(self):
        """Test handling of malformed package entries."""
        malformed_content = {
            "packages": [
                {"name": "valid-package", "version": "1.0.0"},
                {"version": "2.0.0"},  # Missing name
                "invalid-entry",  # Not a dict
                {"name": "another-valid", "version": "3.0.0"}
            ]
        }
        
        packages = self.parser.parse(json.dumps(malformed_content), "sbom.json")
        
        # Should only parse valid entries
        assert len(packages) == 2
        assert packages[0].name == "valid-package"
        assert packages[1].name == "another-valid"

    def test_sbom_patterns_coverage(self):
        """Test that all SBOM patterns are covered."""
        expected_patterns = [
            "sbom.json", "bom.json", "cyclonedx.json", "spdx.json",
            "sbom.xml", "bom.xml", "cyclonedx.xml", "spdx.xml",
            "software-bill-of-materials.json", "software-bill-of-materials.xml",
            ".sbom", ".spdx", "SBOM.json", "BOM.json"
        ]
        
        for pattern in expected_patterns:
            assert pattern in SBOMParser.SBOM_PATTERNS

    @patch('src.github_ioc_scanner.parsers.sbom.logger')
    def test_logging_on_parse_errors(self, mock_logger):
        """Test that parsing errors are properly logged."""
        # Test JSON parsing error
        self.parser.parse("invalid json", "sbom.json")
        mock_logger.warning.assert_called()
        
        # Test XML parsing error
        mock_logger.reset_mock()
        self.parser.parse("<invalid xml", "sbom.xml")
        mock_logger.warning.assert_called()


class TestSBOMParserIntegration:
    """Integration tests for SBOM parser with real-world examples."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = SBOMParser()

    def test_real_world_spdx_example(self):
        """Test with a real-world SPDX example."""
        spdx_example = {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": "MyProject-SBOM",
            "documentNamespace": "https://example.com/sbom/myproject",
            "packages": [
                {
                    "SPDXID": "SPDXRef-Package-express",
                    "name": "express",
                    "versionInfo": "4.18.2",
                    "downloadLocation": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
                    "filesAnalyzed": False,
                    "copyrightText": "Copyright (c) 2009-2014 TJ Holowaychuk <tj@vision-media.ca>"
                },
                {
                    "SPDXID": "SPDXRef-Package-lodash",
                    "name": "lodash",
                    "versionInfo": "4.17.21",
                    "downloadLocation": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",
                    "filesAnalyzed": False
                }
            ]
        }
        
        packages = self.parser.parse(json.dumps(spdx_example), "project-sbom.json")
        
        assert len(packages) == 2
        assert all(pkg.dependency_type == "spdx" for pkg in packages)
        assert packages[0].name == "express"
        assert packages[1].name == "lodash"

    def test_real_world_cyclonedx_example(self):
        """Test with a real-world CycloneDX example."""
        cyclonedx_example = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "serialNumber": "urn:uuid:12345678-1234-1234-1234-123456789012",
            "version": 1,
            "metadata": {
                "timestamp": "2023-01-01T00:00:00Z",
                "tools": [
                    {
                        "vendor": "Example Corp",
                        "name": "SBOM Generator",
                        "version": "1.0.0"
                    }
                ]
            },
            "components": [
                {
                    "type": "library",
                    "bom-ref": "pkg:npm/react@18.2.0",
                    "name": "react",
                    "version": "18.2.0",
                    "purl": "pkg:npm/react@18.2.0",
                    "licenses": [
                        {
                            "license": {
                                "id": "MIT"
                            }
                        }
                    ]
                },
                {
                    "type": "library",
                    "bom-ref": "pkg:pypi/django@4.2.0",
                    "name": "django",
                    "version": "4.2.0",
                    "purl": "pkg:pypi/django@4.2.0"
                }
            ]
        }
        
        packages = self.parser.parse(json.dumps(cyclonedx_example), "cyclonedx-bom.json")
        
        assert len(packages) == 2
        assert packages[0].name == "react"
        assert packages[0].dependency_type == "npm"
        assert packages[1].name == "django"
        assert packages[1].dependency_type == "pypi"