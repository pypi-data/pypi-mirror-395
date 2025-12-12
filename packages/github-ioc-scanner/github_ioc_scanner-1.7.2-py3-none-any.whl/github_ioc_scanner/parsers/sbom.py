"""SBOM (Software Bill of Materials) parser for various formats."""

import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass

from ..logging_config import get_logger
from ..models import PackageDependency

logger = get_logger(__name__)


@dataclass
class SBOMComponent:
    """Represents a component in an SBOM."""
    name: str
    version: Optional[str] = None
    purl: Optional[str] = None  # Package URL
    cpe: Optional[str] = None   # Common Platform Enumeration
    supplier: Optional[str] = None
    licenses: List[str] = None
    hashes: Dict[str, str] = None
    
    def __post_init__(self):
        if self.licenses is None:
            self.licenses = []
        if self.hashes is None:
            self.hashes = {}


class SBOMParser:
    """Parser for SBOM files in various formats (SPDX, CycloneDX)."""
    
    # Common SBOM file patterns
    SBOM_PATTERNS = [
        "sbom.json",
        "bom.json", 
        "cyclonedx.json",
        "spdx.json",
        "sbom.xml",
        "bom.xml",
        "cyclonedx.xml",
        "spdx.xml",
        "software-bill-of-materials.json",
        "software-bill-of-materials.xml",
        ".sbom",
        ".spdx",
        "SBOM.json",
        "BOM.json"
    ]
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle the given file."""
        file_path_lower = file_path.lower()
        
        # Check exact matches
        filename = file_path_lower.split('/')[-1]
        if filename in [p.lower() for p in self.SBOM_PATTERNS]:
            return True
            
        # Check if filename contains sbom/bom keywords
        sbom_keywords = ['sbom', 'bom', 'spdx', 'cyclonedx']
        for keyword in sbom_keywords:
            if keyword in filename and (filename.endswith('.json') or filename.endswith('.xml')):
                return True
                
        return False
    
    def parse(self, content: str, file_path: str) -> List[PackageDependency]:
        """Parse SBOM content and extract packages."""
        try:
            # Determine format based on content and file extension
            if file_path.lower().endswith('.xml'):
                return self._parse_xml_sbom(content, file_path)
            else:
                return self._parse_json_sbom(content, file_path)
                
        except Exception as e:
            logger.warning(f"Failed to parse SBOM file {file_path}: {e}")
            return []
    
    def _parse_json_sbom(self, content: str, file_path: str) -> List[PackageDependency]:
        """Parse JSON-based SBOM formats (SPDX JSON, CycloneDX JSON)."""
        try:
            data = json.loads(content)
            
            # Handle GitHub API SBOM format (nested under 'sbom' key)
            if 'sbom' in data and isinstance(data['sbom'], dict):
                logger.debug(f"Detected GitHub API SBOM format in {file_path}")
                data = data['sbom']
            
            # Detect SBOM format
            if self._is_spdx_json(data):
                return self._parse_spdx_json(data, file_path)
            elif self._is_cyclonedx_json(data):
                return self._parse_cyclonedx_json(data, file_path)
            else:
                # Try generic JSON SBOM parsing
                return self._parse_generic_json_sbom(data, file_path)
                
        except json.JSONDecodeError as e:
            logger.warning(f"Invalid JSON in SBOM file {file_path}: {e}")
            return []
        except Exception as e:
            logger.warning(f"Error parsing JSON SBOM {file_path}: {e}")
            return []
    
    def _parse_xml_sbom(self, content: str, file_path: str) -> List[PackageDependency]:
        """Parse XML-based SBOM formats (SPDX XML, CycloneDX XML)."""
        try:
            root = ET.fromstring(content)
            
            # Detect SBOM format by namespace or root element
            if self._is_spdx_xml(root):
                return self._parse_spdx_xml(root, file_path)
            elif self._is_cyclonedx_xml(root):
                return self._parse_cyclonedx_xml(root, file_path)
            else:
                # Try generic XML SBOM parsing
                return self._parse_generic_xml_sbom(root, file_path)
                
        except ET.ParseError as e:
            logger.warning(f"Invalid XML in SBOM file {file_path}: {e}")
            return []
        except Exception as e:
            logger.warning(f"Error parsing XML SBOM {file_path}: {e}")
            return []
    
    def _is_spdx_json(self, data: Dict[str, Any]) -> bool:
        """Check if JSON data is SPDX format."""
        return (
            isinstance(data, dict) and
            (data.get('spdxVersion') is not None or 
             data.get('SPDXID') is not None)
        )
    
    def _is_cyclonedx_json(self, data: Dict[str, Any]) -> bool:
        """Check if JSON data is CycloneDX format."""
        return (
            isinstance(data, dict) and
            (data.get('bomFormat') == 'CycloneDX' or
             data.get('specVersion') is not None or
             'components' in data)
        )
    
    def _is_spdx_xml(self, root: ET.Element) -> bool:
        """Check if XML root is SPDX format."""
        return (
            'spdx' in root.tag.lower() or
            'spdx' in str(root.tag)
        )
    
    def _is_cyclonedx_xml(self, root: ET.Element) -> bool:
        """Check if XML root is CycloneDX format."""
        return (
            'bom' in root.tag.lower() or
            'cyclonedx' in str(root.tag).lower()
        )
    
    def _parse_spdx_json(self, data: Dict[str, Any], file_path: str) -> List[PackageDependency]:
        """Parse SPDX JSON format."""
        packages = []
        
        try:
            # SPDX packages are in the 'packages' array
            spdx_packages = data.get('packages', [])
            
            for pkg_data in spdx_packages:
                if not isinstance(pkg_data, dict):
                    continue
                    
                name = pkg_data.get('name')
                if not name:
                    continue
                
                # Extract version from versionInfo or downloadLocation
                version = (
                    pkg_data.get('versionInfo') or
                    self._extract_version_from_download_location(pkg_data.get('downloadLocation', ''))
                )
                
                # Create package
                package = PackageDependency(
                    name=name,
                    version=version,
                    dependency_type='spdx'
                )
                packages.append(package)
                
            logger.debug(f"Parsed {len(packages)} packages from SPDX JSON {file_path}")
            
        except Exception as e:
            logger.warning(f"Error parsing SPDX JSON packages in {file_path}: {e}")
            
        return packages
    
    def _parse_cyclonedx_json(self, data: Dict[str, Any], file_path: str) -> List[PackageDependency]:
        """Parse CycloneDX JSON format."""
        packages = []
        
        try:
            # CycloneDX components are in the 'components' array
            components = data.get('components', [])
            
            for comp_data in components:
                if not isinstance(comp_data, dict):
                    continue
                    
                name = comp_data.get('name')
                if not name:
                    continue
                
                version = comp_data.get('version')
                purl = comp_data.get('purl', '')
                
                # Extract package type from purl or type field
                package_type = self._extract_package_type_from_purl(purl) or comp_data.get('type', 'cyclonedx')
                
                package = PackageDependency(
                    name=name,
                    version=version,
                    dependency_type=package_type
                )
                packages.append(package)
                
            logger.debug(f"Parsed {len(packages)} components from CycloneDX JSON {file_path}")
            
        except Exception as e:
            logger.warning(f"Error parsing CycloneDX JSON components in {file_path}: {e}")
            
        return packages
    
    def _parse_generic_json_sbom(self, data: Dict[str, Any], file_path: str) -> List[PackageDependency]:
        """Parse generic JSON SBOM format."""
        packages = []
        
        try:
            # Look for common package/component arrays
            for key in ['packages', 'components', 'dependencies', 'libraries']:
                if key in data and isinstance(data[key], list):
                    for item in data[key]:
                        if isinstance(item, dict) and 'name' in item:
                            package = PackageDependency(
                                name=item['name'],
                                version=item.get('version'),
                                dependency_type='generic'
                            )
                            packages.append(package)
                            
            logger.debug(f"Parsed {len(packages)} packages from generic JSON SBOM {file_path}")
            
        except Exception as e:
            logger.warning(f"Error parsing generic JSON SBOM {file_path}: {e}")
            
        return packages
    
    def _parse_spdx_xml(self, root: ET.Element, file_path: str) -> List[PackageDependency]:
        """Parse SPDX XML format."""
        packages = []
        
        try:
            # Find package elements (namespace-aware)
            for pkg_elem in root.iter():
                if 'package' in pkg_elem.tag.lower():
                    # Look for name and version in child elements
                    name = None
                    version = None
                    
                    for child in pkg_elem:
                        if 'name' in child.tag.lower():
                            name = child.text
                        elif 'versioninfo' in child.tag.lower():
                            version = child.text
                    
                    if name:
                        package = PackageDependency(
                            name=name,
                            version=version,
                            dependency_type='spdx'
                        )
                        packages.append(package)
                        
            logger.debug(f"Parsed {len(packages)} packages from SPDX XML {file_path}")
            
        except Exception as e:
            logger.warning(f"Error parsing SPDX XML {file_path}: {e}")
            
        return packages
    
    def _parse_cyclonedx_xml(self, root: ET.Element, file_path: str) -> List[PackageDependency]:
        """Parse CycloneDX XML format."""
        packages = []
        
        try:
            # Find component elements
            for comp_elem in root.iter():
                if 'component' in comp_elem.tag.lower():
                    # Look for name, version, and purl in child elements
                    name = None
                    version = None
                    purl = None
                    
                    for child in comp_elem:
                        if 'name' in child.tag.lower():
                            name = child.text
                        elif 'version' in child.tag.lower():
                            version = child.text
                        elif 'purl' in child.tag.lower():
                            purl = child.text
                    
                    if name:
                        package_type = self._extract_package_type_from_purl(purl) if purl else 'cyclonedx'
                        
                        package = PackageDependency(
                            name=name,
                            version=version,
                            dependency_type=package_type
                        )
                        packages.append(package)
                        
            logger.debug(f"Parsed {len(packages)} components from CycloneDX XML {file_path}")
            
        except Exception as e:
            logger.warning(f"Error parsing CycloneDX XML {file_path}: {e}")
            
        return packages
    
    def _parse_generic_xml_sbom(self, root: ET.Element, file_path: str) -> List[PackageDependency]:
        """Parse generic XML SBOM format."""
        packages = []
        
        try:
            # Look for common element names
            for elem in root.iter():
                tag_lower = elem.tag.lower()
                if any(keyword in tag_lower for keyword in ['package', 'component', 'dependency', 'library']):
                    # Try to find name and version in attributes or child elements
                    name = elem.get('name') or elem.get('id')
                    version = elem.get('version')
                    
                    # If not in attributes, look in child elements
                    if not name:
                        name_elem = elem.find('.//*[local-name()="name"]')
                        name = name_elem.text if name_elem is not None else None
                    
                    if not version:
                        version_elem = elem.find('.//*[local-name()="version"]')
                        version = version_elem.text if version_elem is not None else None
                    
                    if name:
                        package = PackageDependency(
                            name=name,
                            version=version,
                            dependency_type='generic'
                        )
                        packages.append(package)
                        
            logger.debug(f"Parsed {len(packages)} packages from generic XML SBOM {file_path}")
            
        except Exception as e:
            logger.warning(f"Error parsing generic XML SBOM {file_path}: {e}")
            
        return packages
    
    def _extract_version_from_download_location(self, download_location: str) -> Optional[str]:
        """Extract version from SPDX download location URL."""
        if not download_location:
            return None
            
        # Common patterns in download URLs
        import re
        
        # Look for version patterns like v1.2.3, 1.2.3, etc.
        version_patterns = [
            r'[-/]v?(\d+\.\d+\.\d+(?:\.\d+)?)',
            r'@(\d+\.\d+\.\d+(?:\.\d+)?)',
            r'=(\d+\.\d+\.\d+(?:\.\d+)?)',
            r'/(\d+\.\d+\.\d+(?:\.\d+)?)/',
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, download_location)
            if match:
                return match.group(1)
                
        return None
    
    def _extract_package_type_from_purl(self, purl: str) -> Optional[str]:
        """Extract package type from Package URL (purl)."""
        if not purl:
            return None
            
        # PURL format: pkg:type/namespace/name@version
        if purl.startswith('pkg:'):
            parts = purl.split('/')
            if len(parts) > 0:
                type_part = parts[0][4:]  # Remove 'pkg:' prefix
                return type_part
                
        return None


# Note: SBOM parser is used directly in the scanner rather than through the factory
# since it has different patterns and use cases than traditional lockfile parsers