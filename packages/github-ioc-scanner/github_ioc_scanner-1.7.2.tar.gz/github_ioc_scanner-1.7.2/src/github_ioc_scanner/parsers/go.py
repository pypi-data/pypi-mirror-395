"""Go package manager parsers."""

import re
from typing import List, Optional, Set

from .base import PackageParser
from ..models import PackageDependency


class GoModParser(PackageParser):
    """Parser for go.mod files (Go modules)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle go.mod files."""
        return file_path.endswith('go.mod')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse go.mod content and extract module dependencies.
        
        Go.mod format:
        module example.com/mymodule
        
        go 1.19
        
        require (
            github.com/gorilla/mux v1.8.0
            github.com/lib/pq v1.10.7
            golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d
        )
        
        require github.com/single/module v1.0.0
        
        replace github.com/old/module => github.com/new/module v1.2.3
        
        Args:
            content: Raw go.mod content
            
        Returns:
            List of PackageDependency objects
            
        Raises:
            ValueError: If go.mod format is severely malformed
        """
        dependencies = []
        lines = content.split('\n')
        
        in_require_block = False
        
        for line in lines:
            stripped_line = line.strip()
            
            # Skip empty lines and comments
            if not stripped_line or stripped_line.startswith('//'):
                continue
            
            # Handle require block start
            if stripped_line.startswith('require ('):
                in_require_block = True
                continue
            
            # Handle require block end
            if in_require_block and stripped_line == ')':
                in_require_block = False
                continue
            
            # Parse require statements
            if in_require_block:
                # Inside require block: "github.com/module v1.0.0"
                dep = self._parse_require_line(stripped_line)
                if dep:
                    dependencies.append(dep)
            elif stripped_line.startswith('require '):
                # Single require statement: "require github.com/module v1.0.0"
                require_content = stripped_line[8:].strip()  # Remove "require "
                dep = self._parse_require_line(require_content)
                if dep:
                    dependencies.append(dep)
        
        return dependencies
    
    def _parse_require_line(self, line: str) -> Optional[PackageDependency]:
        """
        Parse a single require line.
        
        Examples:
        - "github.com/gorilla/mux v1.8.0"
        - "golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d"
        - "github.com/lib/pq v1.10.7 // indirect"
        """
        # Remove inline comments
        if '//' in line:
            line = line.split('//')[0].strip()
        
        if not line:
            return None
        
        # Match module path and version
        # Go module paths can contain dots, slashes, hyphens
        # Versions start with 'v' and can include pseudo-versions
        pattern = r'^([a-zA-Z0-9\-\./_]+)\s+(v[^\s]+)$'
        match = re.match(pattern, line)
        
        if match:
            module_path = match.group(1)
            version = match.group(2)
            
            # Remove 'v' prefix from version for consistency
            if version.startswith('v'):
                version = version[1:]
            
            return PackageDependency(
                name=module_path,
                version=version,
                dependency_type='dependencies'
            )
        
        return None


class GoSumParser(PackageParser):
    """Parser for go.sum files (Go module checksums)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle go.sum files."""
        return file_path.endswith('go.sum')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse go.sum content and extract module dependencies.
        
        Go.sum format:
        github.com/gorilla/mux v1.8.0 h1:i40aqfkR1h2SlN9hojwV5ZA91wcXFOvkdNIeFDP5koI=
        github.com/gorilla/mux v1.8.0/go.mod h1:DVbg23sWSpFRCP0SfiEN6jmj59UnW/n46BH5rLB71So=
        github.com/lib/pq v1.10.7 h1:p7ZhMD+KsSRozJr34udlUrhboJwWAgCg34+/ZZNvZZw=
        github.com/lib/pq v1.10.7/go.mod h1:AlVN5x4E4T544tWzH6hKfbfQvm3HdbOxrmggDNAPY9o=
        
        Args:
            content: Raw go.sum content
            
        Returns:
            List of PackageDependency objects (deduplicated)
            
        Raises:
            ValueError: If go.sum format is severely malformed
        """
        dependencies = []
        seen_modules: Set[str] = set()
        lines = content.split('\n')
        
        for line in lines:
            stripped_line = line.strip()
            
            # Skip empty lines
            if not stripped_line:
                continue
            
            dep = self._parse_sum_line(stripped_line)
            if dep:
                # Use module path + version as key to avoid duplicates
                module_key = f"{dep.name}@{dep.version}"
                if module_key not in seen_modules:
                    dependencies.append(dep)
                    seen_modules.add(module_key)
        
        return dependencies
    
    def _parse_sum_line(self, line: str) -> Optional[PackageDependency]:
        """
        Parse a single go.sum line.
        
        Examples:
        - "github.com/gorilla/mux v1.8.0 h1:i40aqfkR1h2SlN9hojwV5ZA91wcXFOvkdNIeFDP5koI="
        - "github.com/gorilla/mux v1.8.0/go.mod h1:DVbg23sWSpFRCP0SfiEN6jmj59UnW/n46BH5rLB71So="
        - "golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d h1:RgqCarRHycqFkrqbBQqQQmhNRZqD3JlVHfgp1/RMvfA="
        """
        # Split by spaces to get module, version, and hash
        parts = line.split(' ')
        if len(parts) < 3:
            return None
        
        module_path = parts[0]
        version_part = parts[1]
        # parts[2] is the hash, which we don't need
        
        # Handle /go.mod suffix in module path
        if module_path.endswith('/go.mod'):
            module_path = module_path[:-7]  # Remove '/go.mod'
        
        # Handle /go.mod suffix in version part
        if version_part.endswith('/go.mod'):
            version_part = version_part[:-7]  # Remove '/go.mod'
        
        # Validate version format (should start with 'v')
        if not version_part.startswith('v'):
            return None
        
        # Remove 'v' prefix from version for consistency
        version = version_part[1:]
        
        return PackageDependency(
            name=module_path,
            version=version,
            dependency_type='dependencies'
        )