"""Tests for package parser factory and base interface."""

import pytest
from typing import List

from src.github_ioc_scanner.models import PackageDependency
from src.github_ioc_scanner.parsers import (
    PackageParser, 
    PackageParserFactory, 
    get_parser_factory,
    register_parser,
    get_parser
)


class MockJavaScriptParser(PackageParser):
    """Mock parser for JavaScript package files."""
    
    def can_parse(self, file_path: str) -> bool:
        js_files = ['package.json', 'package-lock.json', 'yarn.lock']
        return any(file_path.endswith(filename) for filename in js_files)
    
    def parse(self, content: str) -> List[PackageDependency]:
        # Simple mock implementation
        if 'react' in content:
            return [PackageDependency(name='react', version='18.0.0', dependency_type='dependencies')]
        return []


class MockPythonParser(PackageParser):
    """Mock parser for Python package files."""
    
    def can_parse(self, file_path: str) -> bool:
        py_files = ['requirements.txt', 'Pipfile.lock', 'poetry.lock']
        return any(file_path.endswith(filename) for filename in py_files)
    
    def parse(self, content: str) -> List[PackageDependency]:
        # Simple mock implementation
        if 'django' in content:
            return [PackageDependency(name='django', version='4.0.0', dependency_type='requirements')]
        return []


class InvalidParser:
    """Invalid parser that doesn't inherit from PackageParser."""
    pass


class TestPackageParser:
    """Tests for the PackageParser abstract base class."""
    
    def test_cannot_instantiate_abstract_class(self):
        """Test that PackageParser cannot be instantiated directly."""
        with pytest.raises(TypeError):
            PackageParser()
    
    def test_mock_parser_implements_interface(self):
        """Test that mock parsers properly implement the interface."""
        js_parser = MockJavaScriptParser()
        py_parser = MockPythonParser()
        
        # Test can_parse method
        assert js_parser.can_parse('package.json') is True
        assert js_parser.can_parse('package-lock.json') is True
        assert js_parser.can_parse('yarn.lock') is True
        assert js_parser.can_parse('requirements.txt') is False
        
        assert py_parser.can_parse('requirements.txt') is True
        assert py_parser.can_parse('poetry.lock') is True
        assert py_parser.can_parse('package.json') is False
        
        # Test parse method
        js_deps = js_parser.parse('{"dependencies": {"react": "18.0.0"}}')
        assert len(js_deps) == 1
        assert js_deps[0].name == 'react'
        
        py_deps = py_parser.parse('django==4.0.0')
        assert len(py_deps) == 1
        assert py_deps[0].name == 'django'


class TestPackageParserFactory:
    """Tests for the PackageParserFactory class."""
    
    def setup_method(self):
        """Set up a fresh factory for each test."""
        self.factory = PackageParserFactory()
    
    def test_register_valid_parser(self):
        """Test registering a valid parser with a pattern."""
        pattern = r'package\.json$'
        self.factory.register_parser(pattern, MockJavaScriptParser)
        
        patterns = self.factory.get_supported_patterns()
        assert pattern in patterns
    
    def test_register_invalid_parser_class(self):
        """Test that registering an invalid parser class raises ValueError."""
        with pytest.raises(ValueError, match="must inherit from PackageParser"):
            self.factory.register_parser(r'test\.txt$', InvalidParser)
    
    def test_register_invalid_regex_pattern(self):
        """Test that registering an invalid regex pattern raises ValueError."""
        with pytest.raises(ValueError, match="Invalid regex pattern"):
            self.factory.register_parser(r'[invalid regex', MockJavaScriptParser)
    
    def test_get_parser_for_matching_file(self):
        """Test getting a parser for a file that matches a registered pattern."""
        self.factory.register_parser(r'package\.json$', MockJavaScriptParser)
        self.factory.register_parser(r'requirements\.txt$', MockPythonParser)
        
        js_parser = self.factory.get_parser('src/package.json')
        assert js_parser is not None
        assert isinstance(js_parser, MockJavaScriptParser)
        
        py_parser = self.factory.get_parser('requirements.txt')
        assert py_parser is not None
        assert isinstance(py_parser, MockPythonParser)
    
    def test_get_parser_for_non_matching_file(self):
        """Test getting a parser for a file that doesn't match any pattern."""
        self.factory.register_parser(r'package\.json$', MockJavaScriptParser)
        
        parser = self.factory.get_parser('unknown.txt')
        assert parser is None
    
    def test_get_parser_with_multiple_patterns(self):
        """Test that the first matching parser is returned when multiple patterns match."""
        # Register two parsers that could both match
        self.factory.register_parser(r'.*\.json$', MockJavaScriptParser)
        self.factory.register_parser(r'package\.json$', MockPythonParser)  # More specific
        
        # The first registered parser should be returned
        parser = self.factory.get_parser('package.json')
        assert parser is not None
        assert isinstance(parser, MockJavaScriptParser)
    
    def test_get_supported_patterns(self):
        """Test getting list of supported patterns."""
        patterns = ['package\\.json$', 'requirements\\.txt$', 'Cargo\\.lock$']
        
        for pattern in patterns:
            self.factory.register_parser(pattern, MockJavaScriptParser)
        
        supported = self.factory.get_supported_patterns()
        assert len(supported) == 3
        for pattern in patterns:
            assert pattern in supported
    
    def test_clear_parsers(self):
        """Test clearing all registered parsers."""
        self.factory.register_parser(r'package\.json$', MockJavaScriptParser)
        self.factory.register_parser(r'requirements\.txt$', MockPythonParser)
        
        assert len(self.factory.get_supported_patterns()) == 2
        
        self.factory.clear_parsers()
        
        assert len(self.factory.get_supported_patterns()) == 0
        assert self.factory.get_parser('package.json') is None


class TestGlobalFactoryFunctions:
    """Tests for global factory convenience functions."""
    
    def setup_method(self):
        """Clear global factory before each test."""
        get_parser_factory().clear_parsers()
    
    def teardown_method(self):
        """Clear global factory after each test."""
        get_parser_factory().clear_parsers()
    
    def test_get_parser_factory_singleton(self):
        """Test that get_parser_factory returns the same instance."""
        factory1 = get_parser_factory()
        factory2 = get_parser_factory()
        
        assert factory1 is factory2
    
    def test_register_parser_convenience_function(self):
        """Test the register_parser convenience function."""
        register_parser(r'package\.json$', MockJavaScriptParser)
        
        factory = get_parser_factory()
        patterns = factory.get_supported_patterns()
        assert r'package\.json$' in patterns
    
    def test_get_parser_convenience_function(self):
        """Test the get_parser convenience function."""
        register_parser(r'package\.json$', MockJavaScriptParser)
        
        parser = get_parser('src/package.json')
        assert parser is not None
        assert isinstance(parser, MockJavaScriptParser)
        
        parser = get_parser('unknown.txt')
        assert parser is None


class TestParserFactoryIntegration:
    """Integration tests for parser factory with realistic scenarios."""
    
    def setup_method(self):
        """Set up factory with realistic parsers."""
        self.factory = PackageParserFactory()
        
        # Register parsers for common package manager files
        self.factory.register_parser(r'package\.json$', MockJavaScriptParser)
        self.factory.register_parser(r'package-lock\.json$', MockJavaScriptParser)
        self.factory.register_parser(r'yarn\.lock$', MockJavaScriptParser)
        self.factory.register_parser(r'requirements\.txt$', MockPythonParser)
        self.factory.register_parser(r'Pipfile\.lock$', MockPythonParser)
        self.factory.register_parser(r'poetry\.lock$', MockPythonParser)
    
    def test_realistic_file_paths(self):
        """Test parser selection with realistic file paths."""
        test_cases = [
            ('src/frontend/package.json', MockJavaScriptParser),
            ('backend/requirements.txt', MockPythonParser),
            ('web/package-lock.json', MockJavaScriptParser),
            ('api/poetry.lock', MockPythonParser),
            ('mobile/yarn.lock', MockJavaScriptParser),
            ('services/Pipfile.lock', MockPythonParser),
            ('unknown/file.txt', None),
            ('config.yaml', None),
        ]
        
        for file_path, expected_parser_type in test_cases:
            parser = self.factory.get_parser(file_path)
            
            if expected_parser_type is None:
                assert parser is None, f"Expected no parser for {file_path}"
            else:
                assert parser is not None, f"Expected parser for {file_path}"
                assert isinstance(parser, expected_parser_type), \
                    f"Expected {expected_parser_type.__name__} for {file_path}"
    
    def test_parser_double_check_with_can_parse(self):
        """Test that factory uses parser's can_parse method as additional validation."""
        
        class StrictJavaScriptParser(PackageParser):
            """Parser that only accepts exact 'package.json' filename."""
            
            def can_parse(self, file_path: str) -> bool:
                # Only accept exact filename, not just ending
                return file_path.split('/')[-1] == 'package.json'
            
            def parse(self, content: str) -> List[PackageDependency]:
                return []
        
        # Create a fresh factory to avoid conflicts with setup_method
        factory = PackageParserFactory()
        
        # Register with broad pattern but strict can_parse
        factory.register_parser(r'\.json$', StrictJavaScriptParser)
        
        # Should match pattern but fail can_parse check
        parser = factory.get_parser('config.json')
        assert parser is None
        
        # Should match both pattern and can_parse check
        parser = factory.get_parser('package.json')
        assert parser is not None
        assert isinstance(parser, StrictJavaScriptParser)

class TestPackageJsonParser:
    """Tests for PackageJsonParser."""
    
    def setup_method(self):
        """Set up parser for each test."""
        from src.github_ioc_scanner.parsers.javascript import PackageJsonParser
        self.parser = PackageJsonParser()
    
    def test_can_parse_package_json(self):
        """Test that parser correctly identifies package.json files."""
        assert self.parser.can_parse('package.json') is True
        assert self.parser.can_parse('src/package.json') is True
        assert self.parser.can_parse('frontend/package.json') is True
        
        # Should not parse other files
        assert self.parser.can_parse('package-lock.json') is False
        assert self.parser.can_parse('yarn.lock') is False
        assert self.parser.can_parse('requirements.txt') is False
    
    def test_parse_basic_dependencies(self):
        """Test parsing basic dependencies section."""
        content = '''
        {
            "name": "test-app",
            "version": "1.0.0",
            "dependencies": {
                "react": "18.2.0",
                "lodash": "4.17.21"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        react_dep = next(d for d in deps if d.name == 'react')
        assert react_dep.version == '18.2.0'
        assert react_dep.dependency_type == 'dependencies'
        
        lodash_dep = next(d for d in deps if d.name == 'lodash')
        assert lodash_dep.version == '4.17.21'
        assert lodash_dep.dependency_type == 'dependencies'
    
    def test_parse_all_dependency_types(self):
        """Test parsing all types of dependencies."""
        content = '''
        {
            "dependencies": {
                "react": "18.2.0"
            },
            "devDependencies": {
                "jest": "29.0.0"
            },
            "peerDependencies": {
                "react-dom": "18.2.0"
            },
            "optionalDependencies": {
                "fsevents": "2.3.2"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 4
        
        dep_types = {d.dependency_type for d in deps}
        expected_types = {'dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies'}
        assert dep_types == expected_types
    
    def test_normalize_caret_ranges(self):
        """Test normalization of caret ranges (^1.2.3)."""
        content = '''
        {
            "dependencies": {
                "react": "^18.2.0",
                "lodash": "^4.17.21"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        react_dep = next(d for d in deps if d.name == 'react')
        assert react_dep.version == '18.2.0'
        
        lodash_dep = next(d for d in deps if d.name == 'lodash')
        assert lodash_dep.version == '4.17.21'
    
    def test_normalize_tilde_ranges(self):
        """Test normalization of tilde ranges (~1.2.3)."""
        content = '''
        {
            "dependencies": {
                "express": "~4.18.2",
                "moment": "~2.29.4"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        express_dep = next(d for d in deps if d.name == 'express')
        assert express_dep.version == '4.18.2'
        
        moment_dep = next(d for d in deps if d.name == 'moment')
        assert moment_dep.version == '2.29.4'
    
    def test_normalize_gte_ranges(self):
        """Test normalization of >= ranges."""
        content = '''
        {
            "dependencies": {
                "node": ">=16.0.0",
                "npm": ">= 8.0.0"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        node_dep = next(d for d in deps if d.name == 'node')
        assert node_dep.version == '16.0.0'
        
        npm_dep = next(d for d in deps if d.name == 'npm')
        assert npm_dep.version == '8.0.0'
    
    def test_normalize_version_ranges(self):
        """Test normalization of version ranges (1.2.3 - 1.2.5)."""
        content = '''
        {
            "dependencies": {
                "test-pkg": "1.0.0 - 1.2.0"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2  # Should return both endpoints
        
        versions = {d.version for d in deps if d.name == 'test-pkg'}
        assert versions == {'1.0.0', '1.2.0'}
    
    def test_normalize_x_ranges(self):
        """Test normalization of x-ranges (1.x.x, 1.2.x)."""
        content = '''
        {
            "dependencies": {
                "pkg1": "1.x.x",
                "pkg2": "2.3.x"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        pkg1_dep = next(d for d in deps if d.name == 'pkg1')
        assert pkg1_dep.version == '1.0.0'
        
        pkg2_dep = next(d for d in deps if d.name == 'pkg2')
        assert pkg2_dep.version == '2.3.0'
    
    def test_normalize_wildcard_versions(self):
        """Test handling of wildcard versions (* and latest)."""
        content = '''
        {
            "dependencies": {
                "pkg1": "*",
                "pkg2": "latest"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        pkg1_dep = next(d for d in deps if d.name == 'pkg1')
        assert pkg1_dep.version == '*'
        
        pkg2_dep = next(d for d in deps if d.name == 'pkg2')
        assert pkg2_dep.version == '*'
    
    def test_handle_git_urls(self):
        """Test handling of git URLs and file paths."""
        content = '''
        {
            "dependencies": {
                "pkg1": "git+https://github.com/user/repo.git",
                "pkg2": "file:../local-package",
                "pkg3": "https://registry.npmjs.org/package/-/package-1.0.0.tgz"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 3
        
        # Git URLs and file paths should be preserved as-is
        versions = {d.version for d in deps}
        expected_versions = {
            'git+https://github.com/user/repo.git',
            'file:../local-package',
            'https://registry.npmjs.org/package/-/package-1.0.0.tgz'
        }
        assert versions == expected_versions
    
    def test_parse_empty_dependencies(self):
        """Test parsing package.json with empty or missing dependencies."""
        content = '''
        {
            "name": "test-app",
            "version": "1.0.0",
            "dependencies": {},
            "devDependencies": {}
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 0
    
    def test_parse_no_dependencies_section(self):
        """Test parsing package.json without dependencies sections."""
        content = '''
        {
            "name": "test-app",
            "version": "1.0.0",
            "scripts": {
                "start": "node index.js"
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 0
    
    def test_parse_invalid_json(self):
        """Test that invalid JSON raises ValueError."""
        content = '''
        {
            "name": "test-app",
            "version": "1.0.0"
            "dependencies": {
                "react": "18.2.0"
            }
        '''  # Missing comma after version
        
        with pytest.raises(ValueError, match="Invalid JSON"):
            self.parser.parse(content)
    
    def test_parse_non_object_json(self):
        """Test that non-object JSON raises ValueError."""
        content = '["not", "an", "object"]'
        
        with pytest.raises(ValueError, match="must contain a JSON object"):
            self.parser.parse(content)
    
    def test_parse_invalid_dependency_values(self):
        """Test handling of invalid dependency values."""
        content = '''
        {
            "dependencies": {
                "valid-pkg": "1.0.0",
                "invalid-pkg": 123,
                "null-pkg": null
            }
        }
        '''
        
        deps = self.parser.parse(content)
        # Should only parse valid string versions
        assert len(deps) == 1
        assert deps[0].name == 'valid-pkg'
        assert deps[0].version == '1.0.0'


class TestPackageLockParser:
    """Tests for PackageLockParser."""
    
    def setup_method(self):
        """Set up parser for each test."""
        from src.github_ioc_scanner.parsers.javascript import PackageLockParser
        self.parser = PackageLockParser()
    
    def test_can_parse_package_lock_json(self):
        """Test that parser correctly identifies package-lock.json files."""
        assert self.parser.can_parse('package-lock.json') is True
        assert self.parser.can_parse('src/package-lock.json') is True
        assert self.parser.can_parse('frontend/package-lock.json') is True
        
        # Should not parse other files
        assert self.parser.can_parse('package.json') is False
        assert self.parser.can_parse('yarn.lock') is False
        assert self.parser.can_parse('requirements.txt') is False
    
    def test_parse_lockfile_v1_format(self):
        """Test parsing npm lockfile v1 format."""
        content = '''
        {
            "name": "test-app",
            "version": "1.0.0",
            "lockfileVersion": 1,
            "dependencies": {
                "react": {
                    "version": "18.2.0",
                    "resolved": "https://registry.npmjs.org/react/-/react-18.2.0.tgz",
                    "integrity": "sha512-..."
                },
                "lodash": {
                    "version": "4.17.21",
                    "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",
                    "integrity": "sha512-...",
                    "dev": true
                }
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        react_dep = next(d for d in deps if d.name == 'react')
        assert react_dep.version == '18.2.0'
        assert react_dep.dependency_type == 'dependencies'
        
        lodash_dep = next(d for d in deps if d.name == 'lodash')
        assert lodash_dep.version == '4.17.21'
        assert lodash_dep.dependency_type == 'devDependencies'
    
    def test_parse_lockfile_v2_format(self):
        """Test parsing npm lockfile v2+ format."""
        content = '''
        {
            "name": "test-app",
            "version": "1.0.0",
            "lockfileVersion": 2,
            "packages": {
                "": {
                    "name": "test-app",
                    "version": "1.0.0"
                },
                "node_modules/react": {
                    "version": "18.2.0",
                    "resolved": "https://registry.npmjs.org/react/-/react-18.2.0.tgz",
                    "integrity": "sha512-..."
                },
                "node_modules/jest": {
                    "version": "29.0.0",
                    "resolved": "https://registry.npmjs.org/jest/-/jest-29.0.0.tgz",
                    "integrity": "sha512-...",
                    "dev": true
                },
                "node_modules/fsevents": {
                    "version": "2.3.2",
                    "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.2.tgz",
                    "integrity": "sha512-...",
                    "optional": true
                }
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 3
        
        react_dep = next(d for d in deps if d.name == 'react')
        assert react_dep.version == '18.2.0'
        assert react_dep.dependency_type == 'dependencies'
        
        jest_dep = next(d for d in deps if d.name == 'jest')
        assert jest_dep.version == '29.0.0'
        assert jest_dep.dependency_type == 'devDependencies'
        
        fsevents_dep = next(d for d in deps if d.name == 'fsevents')
        assert fsevents_dep.version == '2.3.2'
        assert fsevents_dep.dependency_type == 'optionalDependencies'
    
    def test_parse_scoped_packages_v2(self):
        """Test parsing scoped packages in v2 format."""
        content = '''
        {
            "lockfileVersion": 2,
            "packages": {
                "node_modules/@babel/core": {
                    "version": "7.20.0"
                },
                "node_modules/@types/node": {
                    "version": "18.11.0",
                    "dev": true
                }
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        babel_dep = next(d for d in deps if d.name == '@babel/core')
        assert babel_dep.version == '7.20.0'
        assert babel_dep.dependency_type == 'dependencies'
        
        types_dep = next(d for d in deps if d.name == '@types/node')
        assert types_dep.version == '18.11.0'
        assert types_dep.dependency_type == 'devDependencies'
    
    def test_parse_nested_dependencies_v1(self):
        """Test parsing nested dependencies in v1 format."""
        content = '''
        {
            "lockfileVersion": 1,
            "dependencies": {
                "react": {
                    "version": "18.2.0",
                    "dependencies": {
                        "loose-envify": {
                            "version": "1.4.0"
                        }
                    }
                }
            }
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        package_names = {d.name for d in deps}
        assert package_names == {'react', 'loose-envify'}
    
    def test_parse_invalid_lockfile_json(self):
        """Test that invalid JSON raises ValueError."""
        content = '''
        {
            "lockfileVersion": 1,
            "dependencies": {
                "react": {
                    "version": "18.2.0"
                }
            }
        '''  # Missing closing brace
        
        with pytest.raises(ValueError, match="Invalid JSON"):
            self.parser.parse(content)
    
    def test_parse_empty_lockfile(self):
        """Test parsing empty lockfile."""
        content = '''
        {
            "name": "test-app",
            "version": "1.0.0",
            "lockfileVersion": 1
        }
        '''
        
        deps = self.parser.parse(content)
        assert len(deps) == 0