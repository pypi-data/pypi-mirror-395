"""JavaScript package manager parsers."""

import json
import re
import yaml
from typing import List, Dict, Any, Optional

from .base import PackageParser
from ..models import PackageDependency


class PackageJsonParser(PackageParser):
    """Parser for package.json files."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle package.json files."""
        return file_path.endswith('package.json')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse package.json content and extract dependencies.
        
        Args:
            content: Raw package.json content
            
        Returns:
            List of PackageDependency objects
            
        Raises:
            ValueError: If JSON is malformed or invalid
        """
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in package.json: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("package.json must contain a JSON object")
        
        dependencies = []
        
        # Parse all dependency types
        dependency_types = [
            'dependencies',
            'devDependencies', 
            'peerDependencies',
            'optionalDependencies'
        ]
        
        for dep_type in dependency_types:
            if dep_type in data and isinstance(data[dep_type], dict):
                for package_name, version_spec in data[dep_type].items():
                    if isinstance(version_spec, str):
                        # Normalize semver ranges to exact versions
                        normalized_versions = self._normalize_version_range(version_spec)
                        for version in normalized_versions:
                            dependencies.append(PackageDependency(
                                name=package_name,
                                version=version,
                                dependency_type=dep_type
                            ))
        
        return dependencies
    
    def _normalize_version_range(self, version_spec: str) -> List[str]:
        """
        Normalize semver ranges to exact versions.
        
        For ranges like ^1.2.3, ~1.2.3, >=1.2.3, we extract the base version.
        For exact versions, we return as-is.
        
        Args:
            version_spec: Version specification from package.json
            
        Returns:
            List of normalized version strings
        """
        # Remove whitespace
        version_spec = version_spec.strip()
        
        # Handle exact versions (no prefix)
        if re.match(r'^\d+\.\d+\.\d+$', version_spec):
            return [version_spec]
        
        # Handle caret ranges (^1.2.3)
        caret_match = re.match(r'^\^(\d+\.\d+\.\d+)', version_spec)
        if caret_match:
            return [caret_match.group(1)]
        
        # Handle tilde ranges (~1.2.3)
        tilde_match = re.match(r'^~(\d+\.\d+\.\d+)', version_spec)
        if tilde_match:
            return [tilde_match.group(1)]
        
        # Handle >= ranges (>=1.2.3 or >= 1.2.3)
        gte_match = re.match(r'^>=\s*(\d+\.\d+\.\d+)', version_spec)
        if gte_match:
            return [gte_match.group(1)]
        
        # Handle > ranges (>1.2.3 or > 1.2.3)
        gt_match = re.match(r'^>\s*(\d+\.\d+\.\d+)', version_spec)
        if gt_match:
            return [gt_match.group(1)]
        
        # Handle <= ranges (<=1.2.3 or <= 1.2.3)
        lte_match = re.match(r'^<=\s*(\d+\.\d+\.\d+)', version_spec)
        if lte_match:
            return [lte_match.group(1)]
        
        # Handle < ranges (<1.2.3 or < 1.2.3)
        lt_match = re.match(r'^<\s*(\d+\.\d+\.\d+)', version_spec)
        if lt_match:
            return [lt_match.group(1)]
        
        # Handle version ranges (1.2.3 - 1.2.5)
        range_match = re.match(r'^(\d+\.\d+\.\d+)\s*-\s*(\d+\.\d+\.\d+)', version_spec)
        if range_match:
            # For ranges, return both endpoints
            return [range_match.group(1), range_match.group(2)]
        
        # Handle x-ranges (1.2.x, 1.x.x)
        x_range_match = re.match(r'^(\d+)\.(\d+|x)\.(\d+|x)$', version_spec)
        if x_range_match:
            major, minor, patch = x_range_match.groups()
            if minor == 'x':
                # 1.x.x -> 1.0.0
                return [f"{major}.0.0"]
            elif patch == 'x':
                # 1.2.x -> 1.2.0
                return [f"{major}.{minor}.0"]
        
        # Handle * (any version)
        if version_spec == '*' or version_spec == 'latest':
            return ['*']
        
        # Handle git URLs, file paths, etc. - return as-is
        if any(prefix in version_spec for prefix in ['git+', 'http', 'file:', '/']):
            return [version_spec]
        
        # For any other format, return as-is (might be a tag, etc.)
        return [version_spec]


class PackageLockParser(PackageParser):
    """Parser for package-lock.json files (npm lockfiles)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle package-lock.json files."""
        return file_path.endswith('package-lock.json')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse package-lock.json content and extract exact dependencies.
        
        Args:
            content: Raw package-lock.json content
            
        Returns:
            List of PackageDependency objects with exact versions
            
        Raises:
            ValueError: If JSON is malformed or invalid
        """
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in package-lock.json: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("package-lock.json must contain a JSON object")
        
        dependencies = []
        
        # Handle lockfile version 1 format
        if 'dependencies' in data:
            dependencies.extend(self._parse_v1_dependencies(data['dependencies']))
        
        # Handle lockfile version 2+ format
        if 'packages' in data:
            dependencies.extend(self._parse_v2_packages(data['packages']))
        
        return dependencies
    
    def _parse_v1_dependencies(self, deps: Dict[str, Any]) -> List[PackageDependency]:
        """Parse dependencies from lockfile v1 format."""
        dependencies = []
        
        for package_name, package_info in deps.items():
            if isinstance(package_info, dict) and 'version' in package_info:
                version = package_info['version']
                # Determine dependency type (default to dependencies)
                dep_type = 'dependencies'
                if package_info.get('dev', False):
                    dep_type = 'devDependencies'
                
                dependencies.append(PackageDependency(
                    name=package_name,
                    version=version,
                    dependency_type=dep_type
                ))
                
                # Recursively parse nested dependencies
                if 'dependencies' in package_info:
                    dependencies.extend(self._parse_v1_dependencies(package_info['dependencies']))
        
        return dependencies
    
    def _parse_v2_packages(self, packages: Dict[str, Any]) -> List[PackageDependency]:
        """Parse packages from lockfile v2+ format."""
        dependencies = []
        
        for package_path, package_info in packages.items():
            if not isinstance(package_info, dict) or 'version' not in package_info:
                continue
            
            # Skip root package (empty string key)
            if package_path == '':
                continue
            
            # Extract package name from path (node_modules/package-name)
            if package_path.startswith('node_modules/'):
                package_name = package_path[13:]  # Remove 'node_modules/' prefix
                
                # Handle scoped packages (@scope/package)
                if package_name.startswith('@'):
                    parts = package_name.split('/')
                    if len(parts) >= 2:
                        package_name = f"{parts[0]}/{parts[1]}"
                
                version = package_info['version']
                
                # Determine dependency type
                dep_type = 'dependencies'
                if package_info.get('dev', False):
                    dep_type = 'devDependencies'
                elif package_info.get('optional', False):
                    dep_type = 'optionalDependencies'
                
                dependencies.append(PackageDependency(
                    name=package_name,
                    version=version,
                    dependency_type=dep_type
                ))
        
        return dependencies

class YarnLockParser(PackageParser):
    """Parser for yarn.lock files (both v1 and v2+ formats)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle yarn.lock files."""
        return file_path.endswith('yarn.lock')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse yarn.lock content and extract exact dependencies.
        
        Supports both Yarn v1 and Yarn v2+ (Berry) formats.
        
        Args:
            content: Raw yarn.lock content
            
        Returns:
            List of PackageDependency objects with exact versions
            
        Raises:
            ValueError: If lockfile is malformed or cannot be parsed
        """
        dependencies = []
        
        # Try to detect format and parse accordingly
        if self._is_yarn_v2_format(content):
            dependencies = self._parse_yarn_v2_format(content)
        else:
            dependencies = self._parse_yarn_v1_format(content)
        
        return dependencies
    
    def _is_yarn_v2_format(self, content: str) -> bool:
        """
        Detect if this is a Yarn v2+ (Berry) format lockfile.
        
        Yarn v2+ uses YAML format with __metadata section.
        """
        return '__metadata:' in content
    
    def _parse_yarn_v1_format(self, content: str) -> List[PackageDependency]:
        """
        Parse Yarn v1 lockfile format.
        
        Format example:
        package-name@^1.0.0:
          version "1.0.2"
          resolved "https://..."
          integrity sha512-...
        """
        dependencies = []
        lines = content.split('\n')
        
        current_package = None
        current_version = None
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Package declaration line (package@version:)
            if line.endswith(':') and not line.startswith(' '):
                # Extract package name from declaration
                package_spec = line[:-1]  # Remove trailing ':'
                current_package = self._extract_package_name_v1(package_spec)
                current_version = None
            
            # Version line (  version "1.0.2")
            elif line.startswith('version ') and current_package:
                version_match = re.search(r'version\s+"([^"]+)"', line)
                if version_match:
                    current_version = version_match.group(1)
                    
                    # Add dependency when we have both package and version
                    dependencies.append(PackageDependency(
                        name=current_package,
                        version=current_version,
                        dependency_type='dependencies'  # Yarn v1 doesn't distinguish types in lockfile
                    ))
        
        return dependencies
    
    def _parse_yarn_v2_format(self, content: str) -> List[PackageDependency]:
        """
        Parse Yarn v2+ (Berry) YAML format.
        
        Format example:
        "package-name@npm:^1.0.0":
          version: 1.0.2
          resolution: "package-name@npm:1.0.2"
        """
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in yarn.lock: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("yarn.lock must contain a YAML object")
        
        dependencies = []
        
        for package_spec, package_info in data.items():
            # Skip metadata entries
            if package_spec.startswith('__metadata'):
                continue
            
            if not isinstance(package_info, dict) or 'version' not in package_info:
                continue
            
            # Extract package name from spec (package-name@npm:^1.0.0)
            package_name = self._extract_package_name_v2(package_spec)
            if package_name:
                version = package_info['version']
                
                dependencies.append(PackageDependency(
                    name=package_name,
                    version=version,
                    dependency_type='dependencies'  # Yarn v2 doesn't distinguish types in lockfile
                ))
        
        return dependencies
    
    def _extract_package_name_v1(self, package_spec: str) -> Optional[str]:
        """
        Extract package name from Yarn v1 package specification.
        
        Examples:
        - "lodash@^4.17.21" -> "lodash"
        - "@babel/core@^7.0.0" -> "@babel/core"
        - "package@^1.0.0, package@^1.1.0" -> "package"
        """
        # Handle multiple version specs (package@^1.0.0, package@^1.1.0)
        first_spec = package_spec.split(',')[0].strip()
        
        # Handle quoted package specs
        if first_spec.startswith('"') and first_spec.endswith('"'):
            first_spec = first_spec[1:-1]
        
        # Find the last @ that separates package name from version
        # For scoped packages like @babel/core@^7.0.0, we need the last @
        at_index = first_spec.rfind('@')
        if at_index > 0:
            package_name = first_spec[:at_index]
            return package_name
        
        return None
    
    def _extract_package_name_v2(self, package_spec: str) -> Optional[str]:
        """
        Extract package name from Yarn v2+ package specification.
        
        Examples:
        - "lodash@npm:^4.17.21" -> "lodash"
        - "@babel/core@npm:^7.0.0" -> "@babel/core"
        """
        # Remove quotes if present
        if package_spec.startswith('"') and package_spec.endswith('"'):
            package_spec = package_spec[1:-1]
        
        # Split on @npm: or @workspace: etc.
        parts = re.split(r'@(?:npm|workspace|patch|file|link|portal):', package_spec)
        if len(parts) >= 2:
            return parts[0]
        
        # Fallback: find last @ (similar to v1)
        at_index = package_spec.rfind('@')
        if at_index > 0:
            return package_spec[:at_index]
        
        return None


class PnpmLockParser(PackageParser):
    """Parser for pnpm-lock.yaml files."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle pnpm-lock.yaml files."""
        return file_path.endswith('pnpm-lock.yaml')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse pnpm-lock.yaml content and extract exact dependencies.
        
        Args:
            content: Raw pnpm-lock.yaml content
            
        Returns:
            List of PackageDependency objects with exact versions
            
        Raises:
            ValueError: If YAML is malformed or invalid
        """
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in pnpm-lock.yaml: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("pnpm-lock.yaml must contain a YAML object")
        
        dependencies = []
        
        # Parse packages section (pnpm v6+)
        if 'packages' in data:
            dependencies.extend(self._parse_packages_section(data['packages']))
        
        # Parse dependencies section (older pnpm versions)
        if 'dependencies' in data:
            dependencies.extend(self._parse_dependencies_section(data['dependencies'], 'dependencies'))
        
        if 'devDependencies' in data:
            dependencies.extend(self._parse_dependencies_section(data['devDependencies'], 'devDependencies'))
        
        if 'optionalDependencies' in data:
            dependencies.extend(self._parse_dependencies_section(data['optionalDependencies'], 'optionalDependencies'))
        
        return dependencies
    
    def _parse_packages_section(self, packages: Dict[str, Any]) -> List[PackageDependency]:
        """Parse the packages section from pnpm-lock.yaml."""
        dependencies = []
        
        for package_spec, package_info in packages.items():
            if not isinstance(package_info, dict):
                continue
            
            # Extract package name and version from spec
            # Format: /package-name/1.0.0 or /@scope/package/1.0.0
            package_name, version = self._extract_package_info_from_spec(package_spec)
            if package_name and version:
                # Determine dependency type
                dep_type = 'dependencies'
                if package_info.get('dev', False):
                    dep_type = 'devDependencies'
                elif package_info.get('optional', False):
                    dep_type = 'optionalDependencies'
                
                dependencies.append(PackageDependency(
                    name=package_name,
                    version=version,
                    dependency_type=dep_type
                ))
        
        return dependencies
    
    def _parse_dependencies_section(self, deps: Dict[str, Any], dep_type: str) -> List[PackageDependency]:
        """Parse a dependencies section from pnpm-lock.yaml."""
        dependencies = []
        
        for package_name, version_spec in deps.items():
            if isinstance(version_spec, str):
                # Extract version from spec (might be like "1.0.0" or "link:../local")
                version = self._extract_version_from_spec(version_spec)
                if version:
                    dependencies.append(PackageDependency(
                        name=package_name,
                        version=version,
                        dependency_type=dep_type
                    ))
        
        return dependencies
    
    def _extract_package_info_from_spec(self, package_spec: str) -> tuple[Optional[str], Optional[str]]:
        """
        Extract package name and version from pnpm package spec.
        
        Examples:
        - "/lodash/4.17.21" -> ("lodash", "4.17.21")
        - "/@babel/core/7.20.0" -> ("@babel/core", "7.20.0")
        - "/lodash/4.17.21_dev" -> ("lodash", "4.17.21")
        """
        if not package_spec.startswith('/'):
            return None, None
        
        # Remove leading slash
        spec = package_spec[1:]
        
        # Handle scoped packages
        if spec.startswith('@'):
            # Format: @scope/package/version
            parts = spec.split('/')
            if len(parts) >= 3:
                package_name = f"{parts[0]}/{parts[1]}"  # parts[0] already includes @
                version = parts[2]
                # Remove any suffix like _dev, _optional
                version = version.split('_')[0]
                return package_name, version
        else:
            # Format: package/version
            parts = spec.split('/')
            if len(parts) >= 2:
                package_name = parts[0]
                version = parts[1]
                # Remove any suffix like _dev, _optional
                version = version.split('_')[0]
                return package_name, version
        
        return None, None
    
    def _extract_version_from_spec(self, version_spec: str) -> Optional[str]:
        """
        Extract version from pnpm version spec.
        
        Examples:
        - "1.0.0" -> "1.0.0"
        - "link:../local" -> "link:../local"
        - "file:../local" -> "file:../local"
        """
        # For link: and file: specs, return as-is
        if version_spec.startswith(('link:', 'file:')):
            return version_spec
        
        # For regular versions, return as-is
        return version_spec


class BunLockParser(PackageParser):
    """Parser for bun.lockb files (binary format)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle bun.lockb files."""
        return file_path.endswith('bun.lockb')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse bun.lockb content and extract dependencies.
        
        Note: bun.lockb is a binary format that's not easily parseable.
        This is a placeholder implementation that returns empty results.
        In a real implementation, you would need to use Bun's own tools
        or reverse-engineer the binary format.
        
        Args:
            content: Raw bun.lockb content (binary)
            
        Returns:
            Empty list (binary format not supported)
            
        Raises:
            ValueError: Always, as binary format is not supported
        """
        # Bun lockfiles are in a proprietary binary format
        # We cannot parse them without Bun's own tools
        raise ValueError(
            "bun.lockb files use a proprietary binary format that cannot be parsed directly. "
            "Consider using 'bun install --dry-run' or converting to package-lock.json format."
        )