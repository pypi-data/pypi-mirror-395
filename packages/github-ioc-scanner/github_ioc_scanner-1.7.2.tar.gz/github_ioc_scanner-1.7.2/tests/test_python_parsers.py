"""Tests for Python package manager parsers."""

import pytest
from src.github_ioc_scanner.parsers.python import (
    RequirementsTxtParser,
    PipfileLockParser,
    PoetryLockParser,
    PyprojectTomlParser
)
from src.github_ioc_scanner.models import PackageDependency


class TestRequirementsTxtParser:
    """Test cases for RequirementsTxtParser."""
    
    def setup_method(self):
        """Set up parser for each test."""
        self.parser = RequirementsTxtParser()
    
    def test_can_parse_requirements_txt(self):
        """Test that parser can handle requirements.txt files."""
        assert self.parser.can_parse('requirements.txt')
        assert self.parser.can_parse('path/to/requirements.txt')
        assert self.parser.can_parse('requirements.in')
        assert not self.parser.can_parse('package.json')
        assert not self.parser.can_parse('requirements.py')
    
    def test_parse_exact_versions(self):
        """Test parsing exact version specifications."""
        content = """
requests==2.28.1
django==4.1.0
numpy==1.23.0
"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        
        requests_dep = next(d for d in dependencies if d.name == 'requests')
        assert requests_dep.version == '2.28.1'
        assert requests_dep.dependency_type == 'dependencies'
        
        django_dep = next(d for d in dependencies if d.name == 'django')
        assert django_dep.version == '4.1.0'
        
        numpy_dep = next(d for d in dependencies if d.name == 'numpy')
        assert numpy_dep.version == '1.23.0'
    
    def test_parse_version_ranges(self):
        """Test parsing various version range specifications."""
        content = """
requests>=2.28.0
django~=4.1.0
numpy>=1.20.0,<2.0.0
flask>1.0.0
pytest<=7.2.0
click<8.0.0
"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 6
        
        # Check that base versions are extracted
        requests_dep = next(d for d in dependencies if d.name == 'requests')
        assert requests_dep.version == '2.28.0'
        
        django_dep = next(d for d in dependencies if d.name == 'django')
        assert django_dep.version == '4.1.0'
        
        numpy_dep = next(d for d in dependencies if d.name == 'numpy')
        assert numpy_dep.version == '1.20.0'  # First version in range
        
        flask_dep = next(d for d in dependencies if d.name == 'flask')
        assert flask_dep.version == '1.0.0'
        
        pytest_dep = next(d for d in dependencies if d.name == 'pytest')
        assert pytest_dep.version == '7.2.0'
        
        click_dep = next(d for d in dependencies if d.name == 'click')
        assert click_dep.version == '8.0.0'
    
    def test_parse_with_extras(self):
        """Test parsing packages with extras."""
        content = """
requests[security]==2.28.1
django[bcrypt,argon2]==4.1.0
pytest[testing]>=7.0.0
"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        
        requests_dep = next(d for d in dependencies if d.name == 'requests[security]')
        assert requests_dep.version == '2.28.1'
        
        django_dep = next(d for d in dependencies if d.name == 'django[bcrypt,argon2]')
        assert django_dep.version == '4.1.0'
        
        pytest_dep = next(d for d in dependencies if d.name == 'pytest[testing]')
        assert pytest_dep.version == '7.0.0'
    
    def test_parse_editable_installs(self):
        """Test parsing editable installs."""
        content = """
-e git+https://github.com/user/repo.git
-e git+https://github.com/user/package.git@v1.0#egg=package
--editable /path/to/local/package
-e /another/local/path
"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 4
        
        # Check git URL without egg
        git_dep = next(d for d in dependencies if d.name == 'repo')
        assert git_dep.version == 'git+https://github.com/user/repo.git'
        
        # Check git URL with egg
        package_dep = next(d for d in dependencies if d.name == 'package')
        assert package_dep.version == 'git+https://github.com/user/package.git@v1.0#egg=package'
        
        # Check local paths
        local_deps = [d for d in dependencies if d.name in ['package', 'path']]
        assert len(local_deps) >= 2
    
    def test_parse_with_comments_and_blank_lines(self):
        """Test parsing with comments and blank lines."""
        content = """
# Production dependencies
requests==2.28.1  # HTTP library

# Web framework
django==4.1.0

# Skip this line
# numpy==1.23.0

# Data processing
pandas>=1.5.0  # Data analysis
"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        
        package_names = {d.name for d in dependencies}
        assert package_names == {'requests', 'django', 'pandas'}
    
    def test_parse_skip_references_and_constraints(self):
        """Test that -r and -c references are skipped."""
        content = """
requests==2.28.1
-r dev-requirements.txt
--requirement test-requirements.txt
-c constraints.txt
--constraint other-constraints.txt
django==4.1.0
"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 2
        package_names = {d.name for d in dependencies}
        assert package_names == {'requests', 'django'}
    
    def test_parse_no_version_specified(self):
        """Test parsing packages without version specifications."""
        content = """
requests
django
numpy
"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        for dep in dependencies:
            assert dep.version == '*'
    
    def test_parse_malformed_requirements(self):
        """Test handling of malformed requirements."""
        content = """
requests==2.28.1
invalid-line-here!!!
django==4.1.0
"""
        # Should not raise exception, but should log warning
        dependencies = self.parser.parse(content)
        
        # Should still parse valid lines
        assert len(dependencies) == 2
        package_names = {d.name for d in dependencies}
        assert package_names == {'requests', 'django'}
    
    def test_parse_empty_content(self):
        """Test parsing empty content."""
        dependencies = self.parser.parse("")
        assert len(dependencies) == 0
        
        dependencies = self.parser.parse("   \n\n  # Just comments\n  ")
        assert len(dependencies) == 0


class TestPipfileLockParser:
    """Test cases for PipfileLockParser."""
    
    def setup_method(self):
        """Set up parser for each test."""
        self.parser = PipfileLockParser()
    
    def test_can_parse_pipfile_lock(self):
        """Test that parser can handle Pipfile.lock files."""
        assert self.parser.can_parse('Pipfile.lock')
        assert self.parser.can_parse('path/to/Pipfile.lock')
        assert not self.parser.can_parse('Pipfile')
        assert not self.parser.can_parse('package.json')
    
    def test_parse_basic_pipfile_lock(self):
        """Test parsing basic Pipfile.lock format."""
        content = """{
    "_meta": {
        "hash": {
            "sha256": "abc123"
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.9"
        }
    },
    "default": {
        "requests": {
            "hashes": [
                "sha256:abc123"
            ],
            "version": "==2.28.1"
        },
        "django": {
            "hashes": [
                "sha256:def456"
            ],
            "version": "==4.1.0"
        }
    },
    "develop": {
        "pytest": {
            "hashes": [
                "sha256:ghi789"
            ],
            "version": "==7.2.0"
        }
    }
}"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        
        # Check default dependencies
        requests_dep = next(d for d in dependencies if d.name == 'requests')
        assert requests_dep.version == '2.28.1'
        assert requests_dep.dependency_type == 'dependencies'
        
        django_dep = next(d for d in dependencies if d.name == 'django')
        assert django_dep.version == '4.1.0'
        assert django_dep.dependency_type == 'dependencies'
        
        # Check develop dependencies
        pytest_dep = next(d for d in dependencies if d.name == 'pytest')
        assert pytest_dep.version == '7.2.0'
        assert pytest_dep.dependency_type == 'devDependencies'
    
    def test_parse_git_dependencies(self):
        """Test parsing git dependencies in Pipfile.lock."""
        content = """{
    "default": {
        "my-package": {
            "git": "https://github.com/user/repo.git",
            "ref": "v1.0.0"
        },
        "another-package": {
            "git": "https://github.com/user/another.git"
        }
    }
}"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 2
        
        my_package = next(d for d in dependencies if d.name == 'my-package')
        assert my_package.version == 'git+https://github.com/user/repo.git@v1.0.0'
        
        another_package = next(d for d in dependencies if d.name == 'another-package')
        assert another_package.version == 'git+https://github.com/user/another.git'
    
    def test_parse_file_dependencies(self):
        """Test parsing file/path dependencies in Pipfile.lock."""
        content = """{
    "default": {
        "local-package": {
            "file": "/path/to/local/package"
        },
        "path-package": {
            "path": "./relative/path"
        }
    }
}"""
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 2
        
        local_package = next(d for d in dependencies if d.name == 'local-package')
        assert local_package.version == 'file:/path/to/local/package'
        
        path_package = next(d for d in dependencies if d.name == 'path-package')
        assert path_package.version == 'file:./relative/path'
    
    def test_parse_invalid_json(self):
        """Test handling of invalid JSON."""
        with pytest.raises(ValueError, match="Invalid JSON in Pipfile.lock"):
            self.parser.parse("invalid json content")
    
    def test_parse_empty_sections(self):
        """Test parsing with empty or missing sections."""
        content = """{
    "_meta": {},
    "default": {},
    "develop": {}
}"""
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0


class TestPoetryLockParser:
    """Test cases for PoetryLockParser."""
    
    def setup_method(self):
        """Set up parser for each test."""
        self.parser = PoetryLockParser()
    
    def test_can_parse_poetry_lock(self):
        """Test that parser can handle poetry.lock files."""
        assert self.parser.can_parse('poetry.lock')
        assert self.parser.can_parse('path/to/poetry.lock')
        assert not self.parser.can_parse('pyproject.toml')
        assert not self.parser.can_parse('package.json')
    
    def test_parse_basic_poetry_lock(self):
        """Test parsing basic poetry.lock format."""
        content = '''# This file is automatically @generated by Poetry and should not be changed by hand.

[[package]]
name = "requests"
version = "2.28.1"
description = "Python HTTP for Humans."
category = "main"
optional = false
python-versions = ">=3.7, <4"

[[package]]
name = "pytest"
version = "7.2.0"
description = "pytest: simple powerful testing with Python"
category = "dev"
optional = false
python-versions = ">=3.7"

[metadata]
lock-version = "1.1"
python-versions = "^3.9"
content-hash = "abc123"
'''
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 2
        
        requests_dep = next(d for d in dependencies if d.name == 'requests')
        assert requests_dep.version == '2.28.1'
        assert requests_dep.dependency_type == 'dependencies'
        
        pytest_dep = next(d for d in dependencies if d.name == 'pytest')
        assert pytest_dep.version == '7.2.0'
        assert pytest_dep.dependency_type == 'devDependencies'
    
    def test_parse_invalid_toml(self):
        """Test handling of invalid TOML."""
        with pytest.raises(ValueError, match="Invalid TOML in poetry.lock"):
            self.parser.parse("invalid toml content [[[")
    
    def test_parse_empty_packages(self):
        """Test parsing with no packages."""
        content = '''[metadata]
lock-version = "1.1"
python-versions = "^3.9"
content-hash = "abc123"
'''
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0


class TestPyprojectTomlParser:
    """Test cases for PyprojectTomlParser."""
    
    def setup_method(self):
        """Set up parser for each test."""
        self.parser = PyprojectTomlParser()
    
    def test_can_parse_pyproject_toml(self):
        """Test that parser can handle pyproject.toml files."""
        assert self.parser.can_parse('pyproject.toml')
        assert self.parser.can_parse('path/to/pyproject.toml')
        assert not self.parser.can_parse('poetry.lock')
        assert not self.parser.can_parse('package.json')
    
    def test_parse_poetry_format(self):
        """Test parsing Poetry format in pyproject.toml."""
        content = '''[tool.poetry]
name = "my-project"
version = "0.1.0"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.0"
django = ">=4.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
black = "~22.0.0"

[tool.poetry.dev-dependencies]
flake8 = "^5.0.0"
'''
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 5
        
        # Check main dependencies (skip python)
        requests_dep = next(d for d in dependencies if d.name == 'requests')
        assert requests_dep.version == '2.28.0'
        assert requests_dep.dependency_type == 'dependencies'
        
        django_dep = next(d for d in dependencies if d.name == 'django')
        assert django_dep.version == '4.0.0'
        assert django_dep.dependency_type == 'dependencies'
        
        # Check dev group dependencies
        pytest_dep = next(d for d in dependencies if d.name == 'pytest')
        assert pytest_dep.version == '7.0.0'
        assert pytest_dep.dependency_type == 'devDependencies'
        
        black_dep = next(d for d in dependencies if d.name == 'black')
        assert black_dep.version == '22.0.0'
        assert black_dep.dependency_type == 'devDependencies'
        
        # Check legacy dev-dependencies
        flake8_dep = next(d for d in dependencies if d.name == 'flake8')
        assert flake8_dep.version == '5.0.0'
        assert flake8_dep.dependency_type == 'devDependencies'
    
    def test_parse_poetry_git_dependencies(self):
        """Test parsing Poetry git dependencies."""
        content = '''[tool.poetry.dependencies]
my-package = {git = "https://github.com/user/repo.git", branch = "main"}
another-package = {git = "https://github.com/user/another.git", tag = "v1.0"}
third-package = {git = "https://github.com/user/third.git", rev = "abc123"}
'''
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        
        my_package = next(d for d in dependencies if d.name == 'my-package')
        assert my_package.version == 'git+https://github.com/user/repo.git@main'
        
        another_package = next(d for d in dependencies if d.name == 'another-package')
        assert another_package.version == 'git+https://github.com/user/another.git@v1.0'
        
        third_package = next(d for d in dependencies if d.name == 'third-package')
        assert third_package.version == 'git+https://github.com/user/third.git@abc123'
    
    def test_parse_poetry_path_dependencies(self):
        """Test parsing Poetry path dependencies."""
        content = '''[tool.poetry.dependencies]
local-package = {path = "/path/to/local"}
relative-package = {path = "./relative/path"}
'''
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 2
        
        local_package = next(d for d in dependencies if d.name == 'local-package')
        assert local_package.version == 'file:/path/to/local'
        
        relative_package = next(d for d in dependencies if d.name == 'relative-package')
        assert relative_package.version == 'file:./relative/path'
    
    def test_parse_pep621_format(self):
        """Test parsing PEP 621 format in pyproject.toml."""
        content = '''[project]
name = "my-project"
version = "0.1.0"
dependencies = [
    "requests>=2.28.0",
    "django==4.1.0",
    "click~=8.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black==22.0.0"
]
test = [
    "coverage>=6.0.0"
]
'''
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 6
        
        # Check main dependencies
        requests_dep = next(d for d in dependencies if d.name == 'requests')
        assert requests_dep.version == '2.28.0'
        assert requests_dep.dependency_type == 'dependencies'
        
        django_dep = next(d for d in dependencies if d.name == 'django')
        assert django_dep.version == '4.1.0'
        assert django_dep.dependency_type == 'dependencies'
        
        # Check dev optional dependencies
        pytest_dep = next(d for d in dependencies if d.name == 'pytest')
        assert pytest_dep.version == '7.0.0'
        assert pytest_dep.dependency_type == 'devDependencies'
        
        black_dep = next(d for d in dependencies if d.name == 'black')
        assert black_dep.version == '22.0.0'
        assert black_dep.dependency_type == 'devDependencies'
        
        # Check test optional dependencies (should be dependencies, not dev)
        coverage_dep = next(d for d in dependencies if d.name == 'coverage')
        assert coverage_dep.version == '6.0.0'
        assert coverage_dep.dependency_type == 'dependencies'
    
    def test_parse_mixed_formats(self):
        """Test parsing both Poetry and PEP 621 formats in same file."""
        content = '''[project]
dependencies = [
    "requests>=2.28.0"
]

[tool.poetry.dependencies]
django = "^4.0.0"
'''
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 2
        
        requests_dep = next(d for d in dependencies if d.name == 'requests')
        assert requests_dep.version == '2.28.0'
        
        django_dep = next(d for d in dependencies if d.name == 'django')
        assert django_dep.version == '4.0.0'
    
    def test_parse_invalid_toml(self):
        """Test handling of invalid TOML."""
        with pytest.raises(ValueError, match="Invalid TOML in pyproject.toml"):
            self.parser.parse("invalid toml content [[[")
    
    def test_parse_empty_content(self):
        """Test parsing empty or minimal content."""
        content = '''[project]
name = "my-project"
version = "0.1.0"
'''
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0