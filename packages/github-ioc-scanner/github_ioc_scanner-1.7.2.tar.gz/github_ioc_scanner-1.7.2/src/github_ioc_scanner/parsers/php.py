"""PHP package manager parsers."""

import json
from typing import List, Dict, Any

from .base import PackageParser
from ..models import PackageDependency


class ComposerLockParser(PackageParser):
    """Parser for composer.lock files (Composer lockfiles)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle composer.lock files."""
        return file_path.endswith('composer.lock')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse composer.lock content and extract package dependencies.
        
        Composer.lock format:
        {
            "packages": [
                {
                    "name": "vendor/package",
                    "version": "1.0.0",
                    "type": "library",
                    "source": {...},
                    "dist": {...},
                    "require": {...}
                }
            ],
            "packages-dev": [
                {
                    "name": "vendor/dev-package",
                    "version": "2.0.0",
                    "type": "library"
                }
            ]
        }
        
        Args:
            content: Raw composer.lock content
            
        Returns:
            List of PackageDependency objects with exact versions
            
        Raises:
            ValueError: If JSON is malformed or invalid
        """
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in composer.lock: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("composer.lock must contain a JSON object")
        
        dependencies = []
        
        # Parse production packages
        if 'packages' in data and isinstance(data['packages'], list):
            dependencies.extend(self._parse_composer_packages(data['packages'], 'dependencies'))
        
        # Parse development packages
        if 'packages-dev' in data and isinstance(data['packages-dev'], list):
            dependencies.extend(self._parse_composer_packages(data['packages-dev'], 'devDependencies'))
        
        return dependencies
    
    def _parse_composer_packages(self, packages: List[Dict[str, Any]], dep_type: str) -> List[PackageDependency]:
        """Parse a list of Composer packages."""
        dependencies = []
        
        for package_info in packages:
            if not isinstance(package_info, dict):
                continue
            
            package_name = package_info.get('name')
            version = package_info.get('version')
            
            if package_name and version:
                # Clean up version string (remove 'v' prefix if present)
                if version.startswith('v'):
                    version = version[1:]
                
                dependencies.append(PackageDependency(
                    name=package_name,
                    version=version,
                    dependency_type=dep_type
                ))
        
        return dependencies