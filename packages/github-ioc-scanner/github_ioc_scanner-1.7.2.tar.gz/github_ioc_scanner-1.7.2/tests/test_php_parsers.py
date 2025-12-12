"""Tests for PHP package manager parsers."""

import pytest
from src.github_ioc_scanner.parsers.php import ComposerLockParser
from src.github_ioc_scanner.models import PackageDependency


class TestComposerLockParser:
    """Test cases for ComposerLockParser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = ComposerLockParser()
    
    def test_can_parse_composer_lock(self):
        """Test that parser correctly identifies composer.lock files."""
        assert self.parser.can_parse('composer.lock')
        assert self.parser.can_parse('path/to/composer.lock')
        assert self.parser.can_parse('/absolute/path/composer.lock')
        
        # Should not parse other files
        assert not self.parser.can_parse('composer.json')
        assert not self.parser.can_parse('Composer.lock')
        assert not self.parser.can_parse('package.json')
        assert not self.parser.can_parse('Gemfile.lock')
    
    def test_parse_basic_composer_lock(self):
        """Test parsing a basic composer.lock file."""
        content = """{
    "_readme": [
        "This file locks the dependencies of your project to a known state"
    ],
    "content-hash": "abc123",
    "packages": [
        {
            "name": "symfony/console",
            "version": "v5.4.15",
            "source": {
                "type": "git",
                "url": "https://github.com/symfony/console.git",
                "reference": "abc123"
            },
            "dist": {
                "type": "zip",
                "url": "https://api.github.com/repos/symfony/console/zipball/abc123",
                "reference": "abc123",
                "shasum": ""
            },
            "require": {
                "php": ">=7.2.5",
                "symfony/deprecation-contracts": "^2.1|^3",
                "symfony/polyfill-mbstring": "~1.0",
                "symfony/polyfill-php73": "^1.9",
                "symfony/polyfill-php80": "^1.16",
                "symfony/service-contracts": "^1.1|^2|^3",
                "symfony/string": "^5.1|^6.0"
            },
            "type": "library"
        },
        {
            "name": "guzzlehttp/guzzle",
            "version": "7.5.0",
            "source": {
                "type": "git",
                "url": "https://github.com/guzzle/guzzle.git",
                "reference": "def456"
            },
            "type": "library"
        }
    ],
    "packages-dev": [
        {
            "name": "phpunit/phpunit",
            "version": "9.5.26",
            "source": {
                "type": "git",
                "url": "https://github.com/sebastianbergmann/phpunit.git",
                "reference": "ghi789"
            },
            "type": "library"
        }
    ],
    "aliases": [],
    "minimum-stability": "stable",
    "stability-flags": [],
    "prefer-stable": false,
    "prefer-lowest": false,
    "platform": {
        "php": ">=7.4"
    },
    "platform-dev": []
}"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='symfony/console', version='5.4.15', dependency_type='dependencies'),
            PackageDependency(name='guzzlehttp/guzzle', version='7.5.0', dependency_type='dependencies'),
            PackageDependency(name='phpunit/phpunit', version='9.5.26', dependency_type='devDependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_composer_lock_with_version_prefixes(self):
        """Test parsing composer.lock with 'v' version prefixes."""
        content = """{
    "packages": [
        {
            "name": "laravel/framework",
            "version": "v9.43.0",
            "type": "library"
        },
        {
            "name": "doctrine/dbal",
            "version": "3.5.1",
            "type": "library"
        }
    ],
    "packages-dev": [
        {
            "name": "mockery/mockery",
            "version": "v1.5.1",
            "type": "library"
        }
    ]
}"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='laravel/framework', version='9.43.0', dependency_type='dependencies'),
            PackageDependency(name='doctrine/dbal', version='3.5.1', dependency_type='dependencies'),
            PackageDependency(name='mockery/mockery', version='1.5.1', dependency_type='devDependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_composer_lock_with_complex_package_names(self):
        """Test parsing packages with complex vendor/package names."""
        content = """{
    "packages": [
        {
            "name": "symfony/http-foundation",
            "version": "5.4.15",
            "type": "library"
        },
        {
            "name": "psr/http-message",
            "version": "1.0.1",
            "type": "library"
        },
        {
            "name": "league/flysystem",
            "version": "3.12.0",
            "type": "library"
        },
        {
            "name": "nesbot/carbon",
            "version": "2.63.0",
            "type": "library"
        }
    ]
}"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='symfony/http-foundation', version='5.4.15', dependency_type='dependencies'),
            PackageDependency(name='psr/http-message', version='1.0.1', dependency_type='dependencies'),
            PackageDependency(name='league/flysystem', version='3.12.0', dependency_type='dependencies'),
            PackageDependency(name='nesbot/carbon', version='2.63.0', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 4
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_composer_lock_only_production_packages(self):
        """Test parsing composer.lock with only production packages."""
        content = """{
    "packages": [
        {
            "name": "monolog/monolog",
            "version": "2.8.0",
            "type": "library"
        },
        {
            "name": "psr/log",
            "version": "3.0.0",
            "type": "library"
        }
    ]
}"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='monolog/monolog', version='2.8.0', dependency_type='dependencies'),
            PackageDependency(name='psr/log', version='3.0.0', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_composer_lock_only_dev_packages(self):
        """Test parsing composer.lock with only development packages."""
        content = """{
    "packages": [],
    "packages-dev": [
        {
            "name": "phpunit/phpunit",
            "version": "9.5.26",
            "type": "library"
        },
        {
            "name": "squizlabs/php_codesniffer",
            "version": "3.7.1",
            "type": "library"
        }
    ]
}"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='phpunit/phpunit', version='9.5.26', dependency_type='devDependencies'),
            PackageDependency(name='squizlabs/php_codesniffer', version='3.7.1', dependency_type='devDependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_empty_composer_lock(self):
        """Test parsing an empty composer.lock file."""
        content = """{
    "packages": [],
    "packages-dev": []
}"""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_parse_composer_lock_missing_sections(self):
        """Test parsing composer.lock with missing packages sections."""
        content = """{
    "_readme": ["This file locks the dependencies"],
    "content-hash": "abc123"
}"""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_parse_composer_lock_with_incomplete_packages(self):
        """Test parsing composer.lock with incomplete package information."""
        content = """{
    "packages": [
        {
            "name": "complete/package",
            "version": "1.0.0",
            "type": "library"
        },
        {
            "name": "missing-version/package",
            "type": "library"
        },
        {
            "version": "2.0.0",
            "type": "library"
        },
        {
            "name": "another/complete",
            "version": "3.0.0",
            "type": "library"
        }
    ]
}"""
        
        dependencies = self.parser.parse(content)
        
        # Should only parse packages with both name and version
        expected_deps = [
            PackageDependency(name='complete/package', version='1.0.0', dependency_type='dependencies'),
            PackageDependency(name='another/complete', version='3.0.0', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_malformed_composer_lock(self):
        """Test parsing malformed composer.lock content."""
        # Invalid JSON
        with pytest.raises(ValueError, match="Invalid JSON in composer.lock"):
            self.parser.parse('{"packages": [invalid json}')
        
        # Non-object JSON
        with pytest.raises(ValueError, match="composer.lock must contain a JSON object"):
            self.parser.parse('["not", "an", "object"]')
        
        # String instead of object
        with pytest.raises(ValueError, match="composer.lock must contain a JSON object"):
            self.parser.parse('"just a string"')
    
    def test_parse_composer_packages_with_invalid_data(self):
        """Test parsing composer.lock with invalid package data."""
        content = """{
    "packages": [
        "not an object",
        {
            "name": "valid/package",
            "version": "1.0.0"
        },
        null,
        {
            "name": "another/valid",
            "version": "2.0.0"
        }
    ],
    "packages-dev": "not an array"
}"""
        
        dependencies = self.parser.parse(content)
        
        # Should only parse valid package objects
        expected_deps = [
            PackageDependency(name='valid/package', version='1.0.0', dependency_type='dependencies'),
            PackageDependency(name='another/valid', version='2.0.0', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_real_world_composer_lock(self):
        """Test parsing a real-world composer.lock example."""
        content = """{
    "_readme": [
        "This file locks the dependencies of your project to a known state",
        "Read more about it at https://getcomposer.org/doc/01-basic-usage.md#installing-dependencies"
    ],
    "content-hash": "abc123def456",
    "packages": [
        {
            "name": "doctrine/inflector",
            "version": "2.0.6",
            "source": {
                "type": "git",
                "url": "https://github.com/doctrine/inflector.git",
                "reference": "d9d313a36c872fd6ee06d9a6cbcf713eaa40f024"
            },
            "dist": {
                "type": "zip",
                "url": "https://api.github.com/repos/doctrine/inflector/zipball/d9d313a36c872fd6ee06d9a6cbcf713eaa40f024",
                "reference": "d9d313a36c872fd6ee06d9a6cbcf713eaa40f024",
                "shasum": ""
            },
            "require": {
                "php": "^7.2 || ^8.0"
            },
            "type": "library"
        },
        {
            "name": "guzzlehttp/guzzle",
            "version": "7.5.0",
            "source": {
                "type": "git",
                "url": "https://github.com/guzzle/guzzle.git",
                "reference": "b50a2a1251152e43f6a37f0fa053e730a67d25ba"
            },
            "dist": {
                "type": "zip",
                "url": "https://api.github.com/repos/guzzle/guzzle/zipball/b50a2a1251152e43f6a37f0fa053e730a67d25ba",
                "reference": "b50a2a1251152e43f6a37f0fa053e730a67d25ba",
                "shasum": ""
            },
            "require": {
                "ext-json": "*",
                "guzzlehttp/promises": "^1.5",
                "guzzlehttp/psr7": "^1.9 || ^2.0",
                "php": "^7.2.5 || ^8.0",
                "psr/http-client": "^1.0"
            },
            "type": "library"
        },
        {
            "name": "laravel/framework",
            "version": "v9.43.0",
            "source": {
                "type": "git",
                "url": "https://github.com/laravel/framework.git",
                "reference": "76c8ed1b4d9ac0c0d9d8e6e7c8c0b8c8c0b8c8c0"
            },
            "type": "library"
        },
        {
            "name": "monolog/monolog",
            "version": "2.8.0",
            "source": {
                "type": "git",
                "url": "https://github.com/Seldaek/monolog.git",
                "reference": "720488632c590286b88b80e62aa3d3d551ad4a50"
            },
            "type": "library"
        },
        {
            "name": "nesbot/carbon",
            "version": "2.63.0",
            "source": {
                "type": "git",
                "url": "https://github.com/briannesbitt/Carbon.git",
                "reference": "ad35dd71a6a212b98e4b87e97389b6fa85f0e347"
            },
            "type": "library"
        },
        {
            "name": "psr/container",
            "version": "2.0.2",
            "source": {
                "type": "git",
                "url": "https://github.com/php-fig/container.git",
                "reference": "c71ecc56dfe541dbd90c5360474fbc405f8d5963"
            },
            "type": "library"
        },
        {
            "name": "symfony/console",
            "version": "v6.2.0",
            "source": {
                "type": "git",
                "url": "https://github.com/symfony/console.git",
                "reference": "ef69e17f88e9b109b6c36e4be8b6f8c4d5ac6e3c"
            },
            "type": "library"
        },
        {
            "name": "symfony/http-foundation",
            "version": "v6.2.0",
            "source": {
                "type": "git",
                "url": "https://github.com/symfony/http-foundation.git",
                "reference": "e8dd1f502bc2b3371d05092aa233b064b03ce7ed"
            },
            "type": "library"
        }
    ],
    "packages-dev": [
        {
            "name": "fakerphp/faker",
            "version": "v1.20.0",
            "source": {
                "type": "git",
                "url": "https://github.com/FakerPHP/Faker.git",
                "reference": "37f751c67a5372d4e26353bd9384bc03744ec77b"
            },
            "type": "library"
        },
        {
            "name": "mockery/mockery",
            "version": "1.5.1",
            "source": {
                "type": "git",
                "url": "https://github.com/mockery/mockery.git",
                "reference": "e92dcc83d5a51851baf5f5591d32cb2b16e3684e"
            },
            "type": "library"
        },
        {
            "name": "phpunit/phpunit",
            "version": "9.5.26",
            "source": {
                "type": "git",
                "url": "https://github.com/sebastianbergmann/phpunit.git",
                "reference": "851867efcbb6a1b992ec515c71cdcf20d895e9d2"
            },
            "type": "library"
        }
    ],
    "aliases": [],
    "minimum-stability": "stable",
    "stability-flags": [],
    "prefer-stable": false,
    "prefer-lowest": false,
    "platform": {
        "php": "^8.0.2"
    },
    "platform-dev": []
}"""
        
        dependencies = self.parser.parse(content)
        
        # Should extract all packages from both sections
        package_names = [dep.name for dep in dependencies]
        
        # Check for some key packages
        assert 'laravel/framework' in package_names
        assert 'guzzlehttp/guzzle' in package_names
        assert 'symfony/console' in package_names
        assert 'phpunit/phpunit' in package_names
        assert 'mockery/mockery' in package_names
        
        # Check specific versions (with v prefix removed)
        laravel_dep = next(dep for dep in dependencies if dep.name == 'laravel/framework')
        assert laravel_dep.version == '9.43.0'  # v prefix removed
        
        symfony_dep = next(dep for dep in dependencies if dep.name == 'symfony/console')
        assert symfony_dep.version == '6.2.0'  # v prefix removed
        
        # Check dependency types
        production_deps = [dep for dep in dependencies if dep.dependency_type == 'dependencies']
        dev_deps = [dep for dep in dependencies if dep.dependency_type == 'devDependencies']
        
        assert len(production_deps) == 8
        assert len(dev_deps) == 3
        assert len(dependencies) == 11