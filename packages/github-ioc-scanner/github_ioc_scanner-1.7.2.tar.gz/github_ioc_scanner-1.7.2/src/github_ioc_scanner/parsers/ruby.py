"""Ruby package manager parsers."""

import re
from typing import List, Optional

from .base import PackageParser
from ..models import PackageDependency


class GemfileLockParser(PackageParser):
    """Parser for Gemfile.lock files (Bundler lockfiles)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle Gemfile.lock files."""
        return file_path.endswith('Gemfile.lock')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse Gemfile.lock content and extract gem dependencies.
        
        Gemfile.lock format:
        GEM
          remote: https://rubygems.org/
          specs:
            actioncable (7.0.4)
              actionpack (= 7.0.4)
              activesupport (= 7.0.4)
            actionpack (7.0.4)
              actionview (= 7.0.4)
              activesupport (= 7.0.4)
            gem-name (1.2.3)
              dependency1 (>= 1.0.0)
              dependency2 (~> 2.0)
        
        DEPENDENCIES
          gem-name
          other-gem (~> 1.0)
        
        Args:
            content: Raw Gemfile.lock content
            
        Returns:
            List of PackageDependency objects with exact versions
            
        Raises:
            ValueError: If Gemfile.lock format is severely malformed
        """
        dependencies = []
        lines = content.split('\n')
        
        # Parse the GEM section for installed gems with exact versions
        in_gem_section = False
        in_specs_section = False
        
        for line in lines:
            stripped_line = line.strip()
            
            # Track sections
            if stripped_line == 'GEM':
                in_gem_section = True
                in_specs_section = False
                continue
            elif stripped_line in ['DEPENDENCIES', 'PLATFORMS', 'BUNDLED WITH', 'PATH', 'GIT']:
                in_gem_section = False
                in_specs_section = False
                continue
            elif stripped_line == 'specs:' and in_gem_section:
                in_specs_section = True
                continue
            
            # Parse gem specifications in the specs section
            if in_gem_section and in_specs_section:
                gem_match = self._parse_gem_spec_line(line)
                if gem_match:
                    dependencies.append(gem_match)
        
        return dependencies
    
    def _parse_gem_spec_line(self, line: str) -> Optional[PackageDependency]:
        """
        Parse a single gem specification line.
        
        Examples:
        - "    actioncable (7.0.4)"
        - "      actionpack (= 7.0.4)"  # dependency line, indented more
        - "    gem-name (1.2.3-beta.1)"
        - "    multi_json (1.15.0)"
        """
        # Match gem name and version pattern
        # Gems are typically indented with 4 spaces, dependencies with 6+ spaces
        # We only want the main gems (4 spaces), not their dependencies
        pattern = r'^    ([a-zA-Z0-9_\-\.]+)\s+\(([^)]+)\)$'
        match = re.match(pattern, line)
        
        if match:
            gem_name = match.group(1)
            version_spec = match.group(2)
            
            # Extract exact version from version specification
            version = self._extract_version_from_spec(version_spec)
            
            return PackageDependency(
                name=gem_name,
                version=version,
                dependency_type='dependencies'
            )
        
        return None
    
    def _extract_version_from_spec(self, version_spec: str) -> str:
        """
        Extract version from Bundler version specification.
        
        In Gemfile.lock specs section, versions are typically exact:
        - "7.0.4" -> "7.0.4"
        - "1.2.3-beta.1" -> "1.2.3-beta.1"
        - "= 7.0.4" -> "7.0.4" (dependency constraint)
        - ">= 1.0.0" -> "1.0.0" (dependency constraint)
        """
        version_spec = version_spec.strip()
        
        # Handle exact version constraints (= 1.0.0)
        if version_spec.startswith('= '):
            return version_spec[2:].strip()
        
        # Handle minimum version constraints (>= 1.0.0)
        if version_spec.startswith('>= '):
            return version_spec[3:].strip()
        
        # Handle greater than constraints (> 1.0.0)
        if version_spec.startswith('> '):
            return version_spec[2:].strip()
        
        # Handle pessimistic version constraints (~> 1.0)
        if version_spec.startswith('~> '):
            return version_spec[3:].strip()
        
        # Handle less than or equal constraints (<= 1.0.0)
        if version_spec.startswith('<= '):
            return version_spec[3:].strip()
        
        # Handle less than constraints (< 1.0.0)
        if version_spec.startswith('< '):
            return version_spec[2:].strip()
        
        # Return as-is for plain versions
        return version_spec