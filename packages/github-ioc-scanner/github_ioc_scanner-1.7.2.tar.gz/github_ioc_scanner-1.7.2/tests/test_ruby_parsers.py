"""Tests for Ruby package manager parsers."""

import pytest
from src.github_ioc_scanner.parsers.ruby import GemfileLockParser
from src.github_ioc_scanner.models import PackageDependency


class TestGemfileLockParser:
    """Test cases for GemfileLockParser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = GemfileLockParser()
    
    def test_can_parse_gemfile_lock(self):
        """Test that parser correctly identifies Gemfile.lock files."""
        assert self.parser.can_parse('Gemfile.lock')
        assert self.parser.can_parse('path/to/Gemfile.lock')
        assert self.parser.can_parse('/absolute/path/Gemfile.lock')
        
        # Should not parse other files
        assert not self.parser.can_parse('Gemfile')
        assert not self.parser.can_parse('gemfile.lock')
        assert not self.parser.can_parse('package.json')
        assert not self.parser.can_parse('requirements.txt')
    
    def test_parse_basic_gemfile_lock(self):
        """Test parsing a basic Gemfile.lock file."""
        content = """GEM
  remote: https://rubygems.org/
  specs:
    actioncable (7.0.4)
      actionpack (= 7.0.4)
      activesupport (= 7.0.4)
    actionpack (7.0.4)
      actionview (= 7.0.4)
      activesupport (= 7.0.4)
    rails (7.0.4)
      actioncable (= 7.0.4)
      actionpack (= 7.0.4)

DEPENDENCIES
  rails (~> 7.0.0)

PLATFORMS
  ruby

BUNDLED WITH
   2.3.26
"""
        
        dependencies = self.parser.parse(content)
        
        # Should extract main gems with exact versions
        expected_deps = [
            PackageDependency(name='actioncable', version='7.0.4', dependency_type='dependencies'),
            PackageDependency(name='actionpack', version='7.0.4', dependency_type='dependencies'),
            PackageDependency(name='rails', version='7.0.4', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_gemfile_lock_with_prerelease_versions(self):
        """Test parsing Gemfile.lock with prerelease versions."""
        content = """GEM
  remote: https://rubygems.org/
  specs:
    rails (7.1.0.beta1)
      actioncable (= 7.1.0.beta1)
    nokogiri (1.13.8-x86_64-linux)
    multi_json (1.15.0)

DEPENDENCIES
  rails (>= 7.1.0.beta1)
  nokogiri
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='rails', version='7.1.0.beta1', dependency_type='dependencies'),
            PackageDependency(name='nokogiri', version='1.13.8-x86_64-linux', dependency_type='dependencies'),
            PackageDependency(name='multi_json', version='1.15.0', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_gemfile_lock_with_git_dependencies(self):
        """Test parsing Gemfile.lock with git dependencies."""
        content = """GIT
  remote: https://github.com/rails/rails.git
  revision: 1234567890abcdef
  specs:
    rails (7.1.0.alpha)

GEM
  remote: https://rubygems.org/
  specs:
    actionpack (7.0.4)
    nokogiri (1.13.8)

DEPENDENCIES
  rails!
  actionpack
"""
        
        dependencies = self.parser.parse(content)
        
        # Should only parse GEM section, not GIT section
        expected_deps = [
            PackageDependency(name='actionpack', version='7.0.4', dependency_type='dependencies'),
            PackageDependency(name='nokogiri', version='1.13.8', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_gemfile_lock_with_path_dependencies(self):
        """Test parsing Gemfile.lock with path dependencies."""
        content = """PATH
  remote: ../my_gem
  specs:
    my_gem (1.0.0)

GEM
  remote: https://rubygems.org/
  specs:
    rails (7.0.4)
    nokogiri (1.13.8)

DEPENDENCIES
  my_gem!
  rails
"""
        
        dependencies = self.parser.parse(content)
        
        # Should only parse GEM section, not PATH section
        expected_deps = [
            PackageDependency(name='rails', version='7.0.4', dependency_type='dependencies'),
            PackageDependency(name='nokogiri', version='1.13.8', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_gemfile_lock_with_complex_gem_names(self):
        """Test parsing gems with complex names (underscores, hyphens, dots)."""
        content = """GEM
  remote: https://rubygems.org/
  specs:
    active_model_serializers (0.10.13)
    dry-validation (1.8.1)
    google-api-client (0.53.0)
    jwt_sessions (2.7.0)
    rack-cors (1.1.1)
    rspec-rails (5.1.2)

DEPENDENCIES
  active_model_serializers
  dry-validation
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='active_model_serializers', version='0.10.13', dependency_type='dependencies'),
            PackageDependency(name='dry-validation', version='1.8.1', dependency_type='dependencies'),
            PackageDependency(name='google-api-client', version='0.53.0', dependency_type='dependencies'),
            PackageDependency(name='jwt_sessions', version='2.7.0', dependency_type='dependencies'),
            PackageDependency(name='rack-cors', version='1.1.1', dependency_type='dependencies'),
            PackageDependency(name='rspec-rails', version='5.1.2', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 6
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_empty_gemfile_lock(self):
        """Test parsing an empty or minimal Gemfile.lock."""
        content = """GEM
  remote: https://rubygems.org/
  specs:

DEPENDENCIES

PLATFORMS
  ruby

BUNDLED WITH
   2.3.26
"""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_parse_gemfile_lock_without_gem_section(self):
        """Test parsing Gemfile.lock without GEM section."""
        content = """DEPENDENCIES
  rails

PLATFORMS
  ruby
"""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_extract_version_from_spec(self):
        """Test version extraction from various specifications."""
        parser = GemfileLockParser()
        
        # Exact versions
        assert parser._extract_version_from_spec('7.0.4') == '7.0.4'
        assert parser._extract_version_from_spec('1.2.3-beta.1') == '1.2.3-beta.1'
        
        # Version constraints (from dependency lines)
        assert parser._extract_version_from_spec('= 7.0.4') == '7.0.4'
        assert parser._extract_version_from_spec('>= 1.0.0') == '1.0.0'
        assert parser._extract_version_from_spec('> 1.0.0') == '1.0.0'
        assert parser._extract_version_from_spec('~> 1.0') == '1.0'
        assert parser._extract_version_from_spec('<= 2.0.0') == '2.0.0'
        assert parser._extract_version_from_spec('< 2.0.0') == '2.0.0'
    
    def test_parse_gem_spec_line(self):
        """Test parsing individual gem specification lines."""
        parser = GemfileLockParser()
        
        # Valid gem lines (4 spaces indentation)
        gem1 = parser._parse_gem_spec_line('    actioncable (7.0.4)')
        assert gem1 == PackageDependency(name='actioncable', version='7.0.4', dependency_type='dependencies')
        
        gem2 = parser._parse_gem_spec_line('    rails (7.1.0.beta1)')
        assert gem2 == PackageDependency(name='rails', version='7.1.0.beta1', dependency_type='dependencies')
        
        gem3 = parser._parse_gem_spec_line('    multi_json (1.15.0)')
        assert gem3 == PackageDependency(name='multi_json', version='1.15.0', dependency_type='dependencies')
        
        # Invalid lines (should return None)
        assert parser._parse_gem_spec_line('      actionpack (= 7.0.4)') is None  # dependency line (6 spaces)
        assert parser._parse_gem_spec_line('  remote: https://rubygems.org/') is None
        assert parser._parse_gem_spec_line('  specs:') is None
        assert parser._parse_gem_spec_line('') is None
        assert parser._parse_gem_spec_line('DEPENDENCIES') is None
    
    def test_parse_malformed_gemfile_lock(self):
        """Test parsing malformed Gemfile.lock content."""
        # Missing specs section
        content1 = """GEM
  remote: https://rubygems.org/
    actioncable (7.0.4)

DEPENDENCIES
  actioncable
"""
        
        dependencies1 = self.parser.parse(content1)
        assert len(dependencies1) == 0  # Should not parse without specs: section
        
        # Malformed gem lines
        content2 = """GEM
  remote: https://rubygems.org/
  specs:
    actioncable 7.0.4  # Missing parentheses
    rails (  # Missing version
    nokogiri () # Empty version

DEPENDENCIES
  actioncable
"""
        
        dependencies2 = self.parser.parse(content2)
        assert len(dependencies2) == 0  # Should skip malformed lines
    
    def test_parse_real_world_gemfile_lock(self):
        """Test parsing a real-world Gemfile.lock example."""
        content = """GEM
  remote: https://rubygems.org/
  specs:
    actioncable (7.0.4)
      actionpack (= 7.0.4)
      activesupport (= 7.0.4)
      nio4r (~> 2.0)
      websocket-driver (>= 0.6.1)
    actionmailbox (7.0.4)
      actionpack (= 7.0.4)
      activejob (= 7.0.4)
      activerecord (= 7.0.4)
      activestorage (= 7.0.4)
      activesupport (= 7.0.4)
      mail (>= 2.7.1)
    bootsnap (1.13.0)
      msgpack (~> 1.2)
    concurrent-ruby (1.1.10)
    crass (1.0.6)
    debug (1.6.2)
      irb (>= 1.3.6)
      reline (>= 0.3.1)
    globalid (1.0.0)
      activesupport (>= 5.0)
    i18n (1.12.0)
      concurrent-ruby (~> 1.0)
    importmap-rails (1.1.5)
      actionpack (>= 6.0.0)
      railties (>= 6.0.0)
    io-console (0.5.11)
    irb (1.4.1)
      reline (>= 0.3.0)
    loofah (2.18.0)
      crass (~> 1.0.2)
      nokogiri (>= 1.5.9)
    mail (2.7.1)
      mini_mime (>= 0.1.1)
    marcel (1.0.2)
    method_source (1.0.0)
    mini_mime (1.1.2)
    minitest (5.16.3)
    msgpack (1.5.6)
    net-imap (0.2.3)
      digest
      net-protocol
      strscan
    net-pop (0.1.1)
      digest
      net-protocol
      timeout
    net-protocol (0.1.3)
      timeout
    net-smtp (0.3.1)
      digest
      net-protocol
      timeout
    nio4r (2.5.8)
    nokogiri (1.13.8-x86_64-linux)
      racc (~> 1.4)
    puma (5.6.5)
      nio4r (~> 2.0)
    racc (1.6.0)
    rack (2.2.4)
    rack-test (2.0.2)
      rack (>= 1.3)
    rails (7.0.4)
      actioncable (= 7.0.4)
      actionmailbox (= 7.0.4)
      actionmailer (= 7.0.4)
      actionpack (= 7.0.4)
      actiontext (= 7.0.4)
      actionview (= 7.0.4)
      activejob (= 7.0.4)
      activemodel (= 7.0.4)
      activerecord (= 7.0.4)
      activestorage (= 7.0.4)
      activesupport (= 7.0.4)
      bundler (>= 1.15.0)
      railties (= 7.0.4)
    reline (0.3.1)
      io-console (~> 0.5)
    sprockets (4.1.1)
      concurrent-ruby (~> 1.0)
      rack (> 1, < 3)
    sprockets-rails (3.4.2)
      actionpack (>= 5.2)
      activesupport (>= 5.2)
      sprockets (>= 3.0.0)
    sqlite3 (1.4.4)
    stimulus-rails (1.1.0)
      railties (>= 6.0.0)
    strscan (3.0.4)
    timeout (0.3.0)
    turbo-rails (1.1.1)
      actionpack (>= 6.0.0)
      activejob (>= 6.0.0)
      railties (>= 6.0.0)
    tzinfo (2.0.5)
      concurrent-ruby (~> 1.0)
    web-console (4.2.0)
      actionview (>= 6.0.0)
      activemodel (>= 6.0.0)
      bindex (>= 0.4.0)
      railties (>= 6.0.0)
    websocket-driver (0.7.5)
      websocket-extensions (>= 0.1.0)
    websocket-extensions (0.1.5)
    zeitwerk (2.6.0)

DEPENDENCIES
  bootsnap
  debug
  importmap-rails
  jbuilder
  puma (~> 5.0)
  rails (~> 7.0.4)
  redis (~> 4.0)
  sassc-rails
  sprockets-rails
  sqlite3 (~> 1.4)
  stimulus-rails
  turbo-rails
  tzinfo-data
  web-console

PLATFORMS
  x86_64-linux

BUNDLED WITH
   2.3.26
"""
        
        dependencies = self.parser.parse(content)
        
        # Should extract all gems from specs section
        gem_names = [dep.name for dep in dependencies]
        
        # Check for some key gems
        assert 'rails' in gem_names
        assert 'actioncable' in gem_names
        assert 'nokogiri' in gem_names
        assert 'puma' in gem_names
        assert 'sqlite3' in gem_names
        
        # Check specific versions
        rails_dep = next(dep for dep in dependencies if dep.name == 'rails')
        assert rails_dep.version == '7.0.4'
        
        nokogiri_dep = next(dep for dep in dependencies if dep.name == 'nokogiri')
        assert nokogiri_dep.version == '1.13.8-x86_64-linux'
        
        # Should have many dependencies
        assert len(dependencies) > 40