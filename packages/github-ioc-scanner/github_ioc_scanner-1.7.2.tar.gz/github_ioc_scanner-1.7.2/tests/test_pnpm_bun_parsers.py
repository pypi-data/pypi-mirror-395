"""Tests for pnpm and Bun lockfile parsers."""

import pytest
from src.github_ioc_scanner.parsers.javascript import PnpmLockParser, BunLockParser


class TestPnpmLockParser:
    """Tests for PnpmLockParser."""
    
    def setup_method(self):
        """Set up parser for each test."""
        self.parser = PnpmLockParser()
    
    def test_can_parse_pnpm_lock_yaml(self):
        """Test that parser correctly identifies pnpm-lock.yaml files."""
        assert self.parser.can_parse('pnpm-lock.yaml') is True
        assert self.parser.can_parse('src/pnpm-lock.yaml') is True
        assert self.parser.can_parse('frontend/pnpm-lock.yaml') is True
        
        # Should not parse other files
        assert self.parser.can_parse('package.json') is False
        assert self.parser.can_parse('yarn.lock') is False
        assert self.parser.can_parse('requirements.txt') is False
    
    def test_parse_pnpm_v6_packages_format(self):
        """Test parsing pnpm v6+ packages format."""
        content = '''lockfileVersion: 5.4

specifiers:
  lodash: ^4.17.21
  react: ^18.2.0

packages:
  /lodash/4.17.21:
    resolution: {integrity: sha512-v2kDEe57lecTulaDIuNTPy3Ry4gLGJ6Z1O3vE1krgXZNrsQ+LFTGHVxVjcXPs17LhbZVGedAJv8XZ1tvj5FvSg==}
    dev: false

  /react/18.2.0:
    resolution: {integrity: sha512-/3IjMdb2L9QbBdWiW5e3P2/npwMBaU9mHCSCUzNln0ZCYbcfTsGbTJrU/kGemdH2IWmB2ioZ+zkxtmq6g09fGQ==}
    engines: {node: '>=0.10.0'}
    dependencies:
      loose-envify: 1.4.0
    dev: false

  /jest/29.0.0:
    resolution: {integrity: sha512-...}
    dev: true
'''
        
        deps = self.parser.parse(content)
        assert len(deps) == 3
        
        lodash_dep = next(d for d in deps if d.name == 'lodash')
        assert lodash_dep.version == '4.17.21'
        assert lodash_dep.dependency_type == 'dependencies'
        
        react_dep = next(d for d in deps if d.name == 'react')
        assert react_dep.version == '18.2.0'
        assert react_dep.dependency_type == 'dependencies'
        
        jest_dep = next(d for d in deps if d.name == 'jest')
        assert jest_dep.version == '29.0.0'
        assert jest_dep.dependency_type == 'devDependencies'
    
    def test_parse_pnpm_scoped_packages(self):
        """Test parsing scoped packages in pnpm format."""
        content = '''lockfileVersion: 5.4

packages:
  /@babel/core/7.20.12:
    resolution: {integrity: sha512-XsMfHovsUYHFMdrIHkZphTN/2Hzzi78R08NuHfDBehym2VsPDL6Zn/JAD/JQdnRvbSsbQc4mVaU1m6JgtTEElg==}
    dev: false

  /@types/node/18.11.18:
    resolution: {integrity: sha512-DHQpWGjyQKSHj3ebjFI/wRKcqQcdR+MoFBygntYOZytCqNfkd2ZC4ARDJ2DQqhjH5p85Nnd3jhUJIXrszFX/JA==}
    dev: true
'''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        babel_dep = next(d for d in deps if d.name == '@babel/core')
        assert babel_dep.version == '7.20.12'
        assert babel_dep.dependency_type == 'dependencies'
        
        types_dep = next(d for d in deps if d.name == '@types/node')
        assert types_dep.version == '18.11.18'
        assert types_dep.dependency_type == 'devDependencies'
    
    def test_parse_pnpm_dependencies_section(self):
        """Test parsing older pnpm format with dependencies sections."""
        content = '''lockfileVersion: 5.3

dependencies:
  lodash: 4.17.21
  react: 18.2.0

devDependencies:
  jest: 29.0.0
  typescript: 4.9.0

optionalDependencies:
  fsevents: 2.3.2
'''
        
        deps = self.parser.parse(content)
        assert len(deps) == 5
        
        # Check dependency types
        dep_types = {d.dependency_type for d in deps}
        expected_types = {'dependencies', 'devDependencies', 'optionalDependencies'}
        assert dep_types == expected_types
        
        # Check specific packages
        lodash_dep = next(d for d in deps if d.name == 'lodash')
        assert lodash_dep.dependency_type == 'dependencies'
        
        jest_dep = next(d for d in deps if d.name == 'jest')
        assert jest_dep.dependency_type == 'devDependencies'
        
        fsevents_dep = next(d for d in deps if d.name == 'fsevents')
        assert fsevents_dep.dependency_type == 'optionalDependencies'
    
    def test_parse_pnpm_with_suffixes(self):
        """Test parsing pnpm packages with version suffixes."""
        content = '''lockfileVersion: 5.4

packages:
  /lodash/4.17.21_dev:
    resolution: {integrity: sha512-...}
    dev: true

  /react/18.2.0_optional:
    resolution: {integrity: sha512-...}
    optional: true
'''
        
        deps = self.parser.parse(content)
        assert len(deps) == 2
        
        lodash_dep = next(d for d in deps if d.name == 'lodash')
        assert lodash_dep.version == '4.17.21'  # Suffix should be removed
        assert lodash_dep.dependency_type == 'devDependencies'
        
        react_dep = next(d for d in deps if d.name == 'react')
        assert react_dep.version == '18.2.0'  # Suffix should be removed
        assert react_dep.dependency_type == 'optionalDependencies'
    
    def test_extract_package_info_from_spec(self):
        """Test package info extraction from pnpm specs."""
        test_cases = [
            ('/lodash/4.17.21', ('lodash', '4.17.21')),
            ('/@babel/core/7.20.0', ('@babel/core', '7.20.0')),
            ('/@types/node/18.11.0', ('@types/node', '18.11.0')),
            ('/react/18.2.0_dev', ('react', '18.2.0')),
            ('/invalid-spec', (None, None)),
            ('no-leading-slash/1.0.0', (None, None)),
        ]
        
        for spec, expected in test_cases:
            result = self.parser._extract_package_info_from_spec(spec)
            assert result == expected, f"Failed for {spec}: got {result}, expected {expected}"
    
    def test_extract_version_from_spec(self):
        """Test version extraction from pnpm version specs."""
        test_cases = [
            ('1.0.0', '1.0.0'),
            ('link:../local-package', 'link:../local-package'),
            ('file:../local-package', 'file:../local-package'),
            ('18.2.0', '18.2.0'),
        ]
        
        for spec, expected in test_cases:
            result = self.parser._extract_version_from_spec(spec)
            assert result == expected, f"Failed for {spec}: got {result}, expected {expected}"
    
    def test_parse_invalid_yaml(self):
        """Test that invalid YAML raises ValueError."""
        content = '''lockfileVersion: 5.4

packages:
  /lodash/4.17.21:
    resolution: {integrity: sha512-...
    # Invalid YAML structure
'''
        
        with pytest.raises(ValueError, match="Invalid YAML"):
            self.parser.parse(content)
    
    def test_parse_empty_pnpm_lock(self):
        """Test parsing empty pnpm-lock.yaml file."""
        content = '''lockfileVersion: 5.4
'''
        
        deps = self.parser.parse(content)
        assert len(deps) == 0


class TestBunLockParser:
    """Tests for BunLockParser."""
    
    def setup_method(self):
        """Set up parser for each test."""
        self.parser = BunLockParser()
    
    def test_can_parse_bun_lockb(self):
        """Test that parser correctly identifies bun.lockb files."""
        assert self.parser.can_parse('bun.lockb') is True
        assert self.parser.can_parse('src/bun.lockb') is True
        assert self.parser.can_parse('frontend/bun.lockb') is True
        
        # Should not parse other files
        assert self.parser.can_parse('package.json') is False
        assert self.parser.can_parse('yarn.lock') is False
        assert self.parser.can_parse('pnpm-lock.yaml') is False
    
    def test_parse_bun_lockb_raises_error(self):
        """Test that parsing bun.lockb raises ValueError due to binary format."""
        binary_content = b'\x00\x01\x02\x03\x04\x05'  # Mock binary content
        
        with pytest.raises(ValueError, match="proprietary binary format"):
            self.parser.parse(binary_content.decode('latin-1'))
    
    def test_parse_bun_lockb_with_text_content(self):
        """Test that parsing any content raises ValueError."""
        text_content = "This is not a valid bun.lockb file"
        
        with pytest.raises(ValueError, match="proprietary binary format"):
            self.parser.parse(text_content)