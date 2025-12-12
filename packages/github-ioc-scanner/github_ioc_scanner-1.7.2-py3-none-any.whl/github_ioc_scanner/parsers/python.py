"""Python package manager parsers."""

import json
import re
from typing import List, Dict, Any, Optional

# Handle tomllib import for different Python versions
try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for older Python versions
    except ImportError:
        tomllib = None

from .base import PackageParser
from ..models import PackageDependency


class RequirementsTxtParser(PackageParser):
    """Parser for requirements.txt files."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle requirements.txt files."""
        return file_path.endswith('requirements.txt') or file_path.endswith('requirements.in')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse requirements.txt content and extract dependencies.
        
        Supports various requirement formats:
        - package==1.0.0 (exact version)
        - package>=1.0.0 (minimum version)
        - package~=1.0.0 (compatible version)
        - package[extra]==1.0.0 (with extras)
        - -e git+https://... (editable installs)
        - -r other-requirements.txt (references to other files)
        - Comments and blank lines
        
        Args:
            content: Raw requirements.txt content
            
        Returns:
            List of PackageDependency objects
            
        Raises:
            ValueError: If requirements format is severely malformed
        """
        dependencies = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Strip whitespace and skip empty lines
            line = line.strip()
            if not line:
                continue
            
            # Skip comments
            if line.startswith('#'):
                continue
            
            # Skip -r (requirements file references) and -c (constraints)
            if line.startswith(('-r ', '-c ', '--requirement ', '--constraint ')):
                continue
            
            # Handle -e (editable installs)
            if line.startswith('-e ') or line.startswith('--editable '):
                editable_spec = line.split(' ', 1)[1] if ' ' in line else ''
                package_name = self._extract_package_name_from_url(editable_spec)
                if package_name:
                    dependencies.append(PackageDependency(
                        name=package_name,
                        version=editable_spec,  # Store the full URL/path
                        dependency_type='dependencies'
                    ))
                continue
            
            # Skip known non-PyPI dependency formats silently
            if self._is_non_pypi_dependency(line):
                continue
                
            # Parse regular package specifications
            try:
                package_dep = self._parse_requirement_line(line)
                if package_dep:
                    dependencies.append(package_dep)
            except ValueError as e:
                # Log warning but continue parsing other lines
                # In a real implementation, you might want to use proper logging
                print(f"Warning: Could not parse requirement on line {line_num}: {line} ({e})")
                continue
        
        return dependencies
    
    def _is_non_pypi_dependency(self, line: str) -> bool:
        """
        Check if a line contains a non-PyPI dependency that should be skipped silently.
        
        This includes:
        - Git SSH URLs: git+ssh://git@github.com/...
        - Git HTTPS URLs: git+https://github.com/...
        - Local paths: ./src, ../lib, /absolute/path
        - File URLs: file://...
        """
        line = line.strip()
        
        # Git SSH URLs
        if line.startswith('git+ssh://'):
            return True
            
        # Git HTTPS URLs  
        if line.startswith('git+https://'):
            return True
            
        # Local relative paths
        if line.startswith('./') or line.startswith('../'):
            return True
            
        # Absolute local paths (Unix/Linux)
        if line.startswith('/'):
            return True
            
        # Windows absolute paths
        if len(line) >= 3 and line[1:3] == ':\\':
            return True
            
        # File URLs
        if line.startswith('file://'):
            return True
            
        return False

    def _parse_requirement_line(self, line: str) -> Optional[PackageDependency]:
        """
        Parse a single requirement line.
        
        Examples:
        - "requests==2.28.1"
        - "django>=3.2,<4.0"
        - "pytest[testing]~=7.0"
        - "numpy>=1.20.0 # Scientific computing"
        - "colorama==0.4.6 ; sys_platform == 'win32'"
        - "package @ git+https://github.com/user/repo.git"
        """
        # Remove inline comments
        if '#' in line:
            line = line.split('#')[0].strip()
        
        if not line:
            return None
        
        # Handle environment markers (e.g., "; sys_platform == 'win32'")
        if ';' in line:
            line = line.split(';')[0].strip()
        
        # Handle direct URL references (PEP 508)
        if ' @ ' in line:
            parts = line.split(' @ ', 1)
            package_name = parts[0].strip()
            url = parts[1].strip()
            
            # Extract package name from URL if it's a git URL
            if package_name and self._is_valid_package_name(package_name):
                return PackageDependency(
                    name=package_name,
                    version=url,  # Store the URL as version
                    dependency_type='dependencies'
                )
            else:
                # Try to extract package name from URL
                extracted_name = self._extract_package_name_from_url(url)
                if extracted_name:
                    return PackageDependency(
                        name=extracted_name,
                        version=url,
                        dependency_type='dependencies'
                    )
                else:
                    raise ValueError(f"Could not extract package name from URL: {line}")
        
        # Match standard package specification pattern
        # Supports: package-name[extras]operator1.0.0,operator2.0.0
        pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?)(\[[^\]]+\])?([\s\w\d\.,<>=~!]*)?$'
        match = re.match(pattern, line)
        
        if not match:
            raise ValueError(f"Invalid requirement format: {line}")
        
        package_name = match.group(1)
        extras = match.group(3) or ''  # [extra1,extra2] or empty
        version_spec = match.group(4).strip() if match.group(4) else ''
        
        # Validate package name
        if not self._is_valid_package_name(package_name):
            raise ValueError(f"Invalid package name: {package_name}")
        
        # Include extras in package name if present
        if extras:
            package_name = f"{package_name}{extras}"
        
        # Extract version from version specification
        version = self._extract_version_from_spec(version_spec)
        
        return PackageDependency(
            name=package_name,
            version=version,
            dependency_type='dependencies'
        )
    
    def _extract_version_from_spec(self, version_spec: str) -> str:
        """
        Extract version from version specification.
        
        For exact versions (==1.0.0), return the exact version.
        For ranges (>=1.0.0, ~=1.0.0), return the base version.
        For complex specs (>=1.0.0,<2.0.0), return the first version found.
        """
        if not version_spec:
            return '*'  # No version specified
        
        # Handle exact version (==1.0.0)
        exact_match = re.search(r'==\s*([^\s,]+)', version_spec)
        if exact_match:
            return exact_match.group(1)
        
        # Handle compatible version (~=1.0.0)
        compatible_match = re.search(r'~=\s*([^\s,]+)', version_spec)
        if compatible_match:
            return compatible_match.group(1)
        
        # Handle minimum version (>=1.0.0)
        gte_match = re.search(r'>=\s*([^\s,]+)', version_spec)
        if gte_match:
            return gte_match.group(1)
        
        # Handle greater than (>1.0.0)
        gt_match = re.search(r'>\s*([^\s,]+)', version_spec)
        if gt_match:
            return gt_match.group(1)
        
        # Handle less than or equal (<=1.0.0)
        lte_match = re.search(r'<=\s*([^\s,]+)', version_spec)
        if lte_match:
            return lte_match.group(1)
        
        # Handle less than (<1.0.0)
        lt_match = re.search(r'<\s*([^\s,]+)', version_spec)
        if lt_match:
            return lt_match.group(1)
        
        # Handle version without operator (assume exact)
        version_match = re.search(r'([0-9]+(?:\.[0-9]+)*(?:[a-zA-Z0-9\-\.]*)?)', version_spec)
        if version_match:
            return version_match.group(1)
        
        # Return the spec as-is if we can't parse it
        return version_spec
    
    def _is_valid_package_name(self, name: str) -> bool:
        """Check if a package name is valid according to PEP 508."""
        if not name:
            return False
        
        # Basic validation: must start with alphanumeric, can contain hyphens, dots, underscores
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$'
        return bool(re.match(pattern, name)) and len(name) <= 214  # PyPI limit
    
    def _extract_package_name_from_url(self, url_spec: str) -> Optional[str]:
        """
        Extract package name from URL specification for editable installs.
        
        Examples:
        - "git+https://github.com/user/repo.git" -> "repo"
        - "git+https://github.com/user/package.git@v1.0#egg=package" -> "package"
        - "/path/to/local/package" -> "package"
        """
        # Check for #egg= parameter
        if '#egg=' in url_spec:
            egg_part = url_spec.split('#egg=')[1]
            # Remove any additional parameters after &
            package_name = egg_part.split('&')[0]
            return package_name
        
        # Extract from git URL
        if url_spec.startswith('git+'):
            # Remove git+ prefix and any @branch/tag
            url = url_spec[4:]  # Remove 'git+'
            if '@' in url:
                url = url.split('@')[0]
            
            # Extract repo name from URL
            if url.endswith('.git'):
                url = url[:-4]
            
            # Get the last part of the path
            parts = url.rstrip('/').split('/')
            if parts:
                return parts[-1]
        
        # Extract from local path
        if '/' in url_spec:
            parts = url_spec.rstrip('/').split('/')
            if parts:
                return parts[-1]
        
        return None


class PipfileLockParser(PackageParser):
    """Parser for Pipfile.lock files (Pipenv lockfiles)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle Pipfile.lock files."""
        return file_path.endswith('Pipfile.lock')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse Pipfile.lock content and extract exact dependencies.
        
        Pipfile.lock format:
        {
            "default": {
                "package-name": {
                    "hashes": [...],
                    "version": "==1.0.0"
                }
            },
            "develop": {
                "dev-package": {
                    "hashes": [...],
                    "version": "==2.0.0"
                }
            }
        }
        
        Args:
            content: Raw Pipfile.lock content
            
        Returns:
            List of PackageDependency objects with exact versions
            
        Raises:
            ValueError: If JSON is malformed or invalid
        """
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in Pipfile.lock: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("Pipfile.lock must contain a JSON object")
        
        dependencies = []
        
        # Parse default dependencies (production)
        if 'default' in data and isinstance(data['default'], dict):
            dependencies.extend(self._parse_pipfile_section(data['default'], 'dependencies'))
        
        # Parse develop dependencies (development)
        if 'develop' in data and isinstance(data['develop'], dict):
            dependencies.extend(self._parse_pipfile_section(data['develop'], 'devDependencies'))
        
        return dependencies
    
    def _parse_pipfile_section(self, section: Dict[str, Any], dep_type: str) -> List[PackageDependency]:
        """Parse a section (default or develop) from Pipfile.lock."""
        dependencies = []
        
        for package_name, package_info in section.items():
            if not isinstance(package_info, dict):
                continue
            
            # Extract version
            version = None
            if 'version' in package_info:
                version_spec = package_info['version']
                # Remove == prefix if present
                if version_spec.startswith('=='):
                    version = version_spec[2:]
                else:
                    version = version_spec
            
            # Handle git/VCS dependencies
            elif any(key in package_info for key in ['git', 'hg', 'svn', 'bzr']):
                # For VCS dependencies, use the VCS URL as version
                for vcs_type in ['git', 'hg', 'svn', 'bzr']:
                    if vcs_type in package_info:
                        version = f"{vcs_type}+{package_info[vcs_type]}"
                        if 'ref' in package_info:
                            version += f"@{package_info['ref']}"
                        break
            
            # Handle file/path dependencies
            elif 'file' in package_info or 'path' in package_info:
                path = package_info.get('file') or package_info.get('path')
                version = f"file:{path}"
            
            if version:
                dependencies.append(PackageDependency(
                    name=package_name,
                    version=version,
                    dependency_type=dep_type
                ))
        
        return dependencies


class PoetryLockParser(PackageParser):
    """Parser for poetry.lock files (Poetry lockfiles)."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle poetry.lock files."""
        return file_path.endswith('poetry.lock')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse poetry.lock content and extract exact dependencies.
        
        Poetry.lock is in TOML format with [[package]] sections.
        
        Args:
            content: Raw poetry.lock content
            
        Returns:
            List of PackageDependency objects with exact versions
            
        Raises:
            ValueError: If TOML is malformed or invalid
        """
        if tomllib is None:
            raise ValueError("TOML parsing not available. Install 'tomli' package for Python < 3.11")
        
        try:
            data = tomllib.loads(content)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Invalid TOML in poetry.lock: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("poetry.lock must contain a TOML object")
        
        dependencies = []
        
        # Parse package sections
        if 'package' in data and isinstance(data['package'], list):
            for package_info in data['package']:
                if not isinstance(package_info, dict):
                    continue
                
                package_name = package_info.get('name')
                version = package_info.get('version')
                
                if package_name and version:
                    # Determine dependency type from category
                    category = package_info.get('category', 'main')
                    dep_type = 'devDependencies' if category == 'dev' else 'dependencies'
                    
                    dependencies.append(PackageDependency(
                        name=package_name,
                        version=version,
                        dependency_type=dep_type
                    ))
        
        return dependencies


class PyprojectTomlParser(PackageParser):
    """Parser for pyproject.toml files with dependencies."""
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle pyproject.toml files."""
        return file_path.endswith('pyproject.toml')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse pyproject.toml content and extract dependencies.
        
        Supports both Poetry format and PEP 621 format:
        
        Poetry format:
        [tool.poetry.dependencies]
        python = "^3.8"
        requests = "^2.28.0"
        
        [tool.poetry.group.dev.dependencies]
        pytest = "^7.0.0"
        
        PEP 621 format:
        [project]
        dependencies = [
            "requests>=2.28.0",
            "click>=8.0.0"
        ]
        
        [project.optional-dependencies]
        dev = ["pytest>=7.0.0"]
        
        Args:
            content: Raw pyproject.toml content
            
        Returns:
            List of PackageDependency objects
            
        Raises:
            ValueError: If TOML is malformed or invalid
        """
        if tomllib is None:
            raise ValueError("TOML parsing not available. Install 'tomli' package for Python < 3.11")
        
        try:
            data = tomllib.loads(content)
        except tomllib.TOMLDecodeError as e:
            raise ValueError(f"Invalid TOML in pyproject.toml: {e}")
        
        if not isinstance(data, dict):
            raise ValueError("pyproject.toml must contain a TOML object")
        
        dependencies = []
        
        # Parse Poetry format
        dependencies.extend(self._parse_poetry_format(data))
        
        # Parse PEP 621 format
        dependencies.extend(self._parse_pep621_format(data))
        
        return dependencies
    
    def _parse_poetry_format(self, data: Dict[str, Any]) -> List[PackageDependency]:
        """Parse Poetry format dependencies from pyproject.toml."""
        dependencies = []
        
        # Parse main dependencies
        poetry_deps = data.get('tool', {}).get('poetry', {}).get('dependencies', {})
        if isinstance(poetry_deps, dict):
            for package_name, version_spec in poetry_deps.items():
                # Skip python version requirement
                if package_name == 'python':
                    continue
                
                version = self._extract_poetry_version(version_spec)
                if version:
                    dependencies.append(PackageDependency(
                        name=package_name,
                        version=version,
                        dependency_type='dependencies'
                    ))
        
        # Parse development dependencies (Poetry groups)
        poetry_groups = data.get('tool', {}).get('poetry', {}).get('group', {})
        if isinstance(poetry_groups, dict):
            for group_name, group_data in poetry_groups.items():
                if isinstance(group_data, dict) and 'dependencies' in group_data:
                    group_deps = group_data['dependencies']
                    if isinstance(group_deps, dict):
                        dep_type = 'devDependencies' if group_name == 'dev' else 'dependencies'
                        for package_name, version_spec in group_deps.items():
                            version = self._extract_poetry_version(version_spec)
                            if version:
                                dependencies.append(PackageDependency(
                                    name=package_name,
                                    version=version,
                                    dependency_type=dep_type
                                ))
        
        # Parse legacy dev-dependencies
        dev_deps = data.get('tool', {}).get('poetry', {}).get('dev-dependencies', {})
        if isinstance(dev_deps, dict):
            for package_name, version_spec in dev_deps.items():
                version = self._extract_poetry_version(version_spec)
                if version:
                    dependencies.append(PackageDependency(
                        name=package_name,
                        version=version,
                        dependency_type='devDependencies'
                    ))
        
        return dependencies
    
    def _parse_pep621_format(self, data: Dict[str, Any]) -> List[PackageDependency]:
        """Parse PEP 621 format dependencies from pyproject.toml."""
        dependencies = []
        
        project = data.get('project', {})
        if not isinstance(project, dict):
            return dependencies
        
        # Parse main dependencies
        main_deps = project.get('dependencies', [])
        if isinstance(main_deps, list):
            for dep_spec in main_deps:
                if isinstance(dep_spec, str):
                    package_dep = self._parse_pep621_requirement(dep_spec)
                    if package_dep:
                        dependencies.append(package_dep)
        
        # Parse optional dependencies
        optional_deps = project.get('optional-dependencies', {})
        if isinstance(optional_deps, dict):
            for group_name, group_deps in optional_deps.items():
                if isinstance(group_deps, list):
                    dep_type = 'devDependencies' if group_name in ['dev', 'testing'] else 'dependencies'
                    for dep_spec in group_deps:
                        if isinstance(dep_spec, str):
                            package_dep = self._parse_pep621_requirement(dep_spec)
                            if package_dep:
                                package_dep.dependency_type = dep_type
                                dependencies.append(package_dep)
        
        return dependencies
    
    def _extract_poetry_version(self, version_spec: Any) -> Optional[str]:
        """
        Extract version from Poetry version specification.
        
        Poetry versions can be:
        - String: "^1.0.0", ">=1.0.0", "1.0.0"
        - Dict: {"version": "^1.0.0", "optional": true}
        - Dict: {"git": "https://...", "branch": "main"}
        """
        if isinstance(version_spec, str):
            return self._normalize_poetry_version(version_spec)
        
        elif isinstance(version_spec, dict):
            # Handle version dict
            if 'version' in version_spec:
                return self._normalize_poetry_version(version_spec['version'])
            
            # Handle git dependencies
            elif 'git' in version_spec:
                git_url = version_spec['git']
                if 'branch' in version_spec:
                    return f"git+{git_url}@{version_spec['branch']}"
                elif 'tag' in version_spec:
                    return f"git+{git_url}@{version_spec['tag']}"
                elif 'rev' in version_spec:
                    return f"git+{git_url}@{version_spec['rev']}"
                else:
                    return f"git+{git_url}"
            
            # Handle path dependencies
            elif 'path' in version_spec:
                return f"file:{version_spec['path']}"
        
        return None
    
    def _normalize_poetry_version(self, version_spec: str) -> str:
        """
        Normalize Poetry version specification to extract base version.
        
        Examples:
        - "^1.0.0" -> "1.0.0"
        - ">=1.0.0" -> "1.0.0"
        - "~1.0.0" -> "1.0.0"
        - "1.0.0" -> "1.0.0"
        """
        # Remove Poetry version operators
        version_spec = version_spec.strip()
        
        # Handle caret (^1.0.0)
        if version_spec.startswith('^'):
            return version_spec[1:]
        
        # Handle tilde (~1.0.0)
        if version_spec.startswith('~'):
            return version_spec[1:]
        
        # Handle >= operator
        if version_spec.startswith('>='):
            return version_spec[2:].strip()
        
        # Handle > operator
        if version_spec.startswith('>'):
            return version_spec[1:].strip()
        
        # Handle <= operator
        if version_spec.startswith('<='):
            return version_spec[2:].strip()
        
        # Handle < operator
        if version_spec.startswith('<'):
            return version_spec[1:].strip()
        
        # Handle == operator
        if version_spec.startswith('=='):
            return version_spec[2:].strip()
        
        # Return as-is for exact versions
        return version_spec
    
    def _parse_pep621_requirement(self, requirement: str) -> Optional[PackageDependency]:
        """
        Parse a PEP 621 requirement string.
        
        Similar to requirements.txt format but in a list.
        """
        # Reuse the requirements.txt parser logic
        req_parser = RequirementsTxtParser()
        try:
            return req_parser._parse_requirement_line(requirement)
        except ValueError:
            return None