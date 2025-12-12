"""Tests for Go package manager parsers."""

import pytest
from src.github_ioc_scanner.parsers.go import GoModParser, GoSumParser
from src.github_ioc_scanner.models import PackageDependency


class TestGoModParser:
    """Test cases for GoModParser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = GoModParser()
    
    def test_can_parse_go_mod(self):
        """Test that parser correctly identifies go.mod files."""
        assert self.parser.can_parse('go.mod')
        assert self.parser.can_parse('path/to/go.mod')
        assert self.parser.can_parse('/absolute/path/go.mod')
        
        # Should not parse other files
        assert not self.parser.can_parse('go.sum')
        assert not self.parser.can_parse('Go.mod')
        assert not self.parser.can_parse('package.json')
        assert not self.parser.can_parse('Cargo.toml')
    
    def test_parse_basic_go_mod(self):
        """Test parsing a basic go.mod file."""
        content = """module example.com/mymodule

go 1.19

require (
    github.com/gorilla/mux v1.8.0
    github.com/lib/pq v1.10.7
    golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d
)
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies'),
            PackageDependency(name='github.com/lib/pq', version='1.10.7', dependency_type='dependencies'),
            PackageDependency(name='golang.org/x/crypto', version='0.0.0-20220622213112-05595931fe9d', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_go_mod_with_single_requires(self):
        """Test parsing go.mod with single require statements."""
        content = """module example.com/mymodule

go 1.19

require github.com/gorilla/mux v1.8.0
require github.com/lib/pq v1.10.7

require (
    golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d
)
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies'),
            PackageDependency(name='github.com/lib/pq', version='1.10.7', dependency_type='dependencies'),
            PackageDependency(name='golang.org/x/crypto', version='0.0.0-20220622213112-05595931fe9d', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_go_mod_with_comments(self):
        """Test parsing go.mod with comments."""
        content = """module example.com/mymodule

go 1.19

require (
    github.com/gorilla/mux v1.8.0 // HTTP router
    github.com/lib/pq v1.10.7 // PostgreSQL driver
    // This is a comment line
    golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d // Crypto utilities
)
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies'),
            PackageDependency(name='github.com/lib/pq', version='1.10.7', dependency_type='dependencies'),
            PackageDependency(name='golang.org/x/crypto', version='0.0.0-20220622213112-05595931fe9d', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_go_mod_with_indirect_dependencies(self):
        """Test parsing go.mod with indirect dependencies."""
        content = """module example.com/mymodule

go 1.19

require (
    github.com/gorilla/mux v1.8.0
    github.com/lib/pq v1.10.7 // indirect
    golang.org/x/sys v0.0.0-20220715151400-c0bba94af5f8 // indirect
)
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies'),
            PackageDependency(name='github.com/lib/pq', version='1.10.7', dependency_type='dependencies'),
            PackageDependency(name='golang.org/x/sys', version='0.0.0-20220715151400-c0bba94af5f8', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_go_mod_with_complex_module_paths(self):
        """Test parsing go.mod with complex module paths."""
        content = """module example.com/mymodule

go 1.19

require (
    cloud.google.com/go/storage v1.27.0
    github.com/aws/aws-sdk-go-v2 v1.17.1
    k8s.io/api v0.25.4
    sigs.k8s.io/controller-runtime v0.13.1
    go.uber.org/zap v1.24.0
)
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='cloud.google.com/go/storage', version='1.27.0', dependency_type='dependencies'),
            PackageDependency(name='github.com/aws/aws-sdk-go-v2', version='1.17.1', dependency_type='dependencies'),
            PackageDependency(name='k8s.io/api', version='0.25.4', dependency_type='dependencies'),
            PackageDependency(name='sigs.k8s.io/controller-runtime', version='0.13.1', dependency_type='dependencies'),
            PackageDependency(name='go.uber.org/zap', version='1.24.0', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 5
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_go_mod_with_pseudo_versions(self):
        """Test parsing go.mod with pseudo-versions."""
        content = """module example.com/mymodule

go 1.19

require (
    github.com/example/module v0.0.0-20220622213112-05595931fe9d
    github.com/another/module v1.2.3-0.20220622213112-05595931fe9d
    github.com/third/module v2.0.0-20220622213112-05595931fe9d+incompatible
)
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='github.com/example/module', version='0.0.0-20220622213112-05595931fe9d', dependency_type='dependencies'),
            PackageDependency(name='github.com/another/module', version='1.2.3-0.20220622213112-05595931fe9d', dependency_type='dependencies'),
            PackageDependency(name='github.com/third/module', version='2.0.0-20220622213112-05595931fe9d+incompatible', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_empty_go_mod(self):
        """Test parsing an empty or minimal go.mod file."""
        content = """module example.com/mymodule

go 1.19
"""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_parse_go_mod_without_require_block(self):
        """Test parsing go.mod without require statements."""
        content = """module example.com/mymodule

go 1.19

replace github.com/old/module => github.com/new/module v1.2.3
"""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_parse_require_line(self):
        """Test parsing individual require lines."""
        parser = GoModParser()
        
        # Valid require lines
        dep1 = parser._parse_require_line('github.com/gorilla/mux v1.8.0')
        assert dep1 == PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies')
        
        dep2 = parser._parse_require_line('golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d')
        assert dep2 == PackageDependency(name='golang.org/x/crypto', version='0.0.0-20220622213112-05595931fe9d', dependency_type='dependencies')
        
        dep3 = parser._parse_require_line('github.com/lib/pq v1.10.7 // indirect')
        assert dep3 == PackageDependency(name='github.com/lib/pq', version='1.10.7', dependency_type='dependencies')
        
        # Invalid lines
        assert parser._parse_require_line('') is None
        assert parser._parse_require_line('// just a comment') is None
        assert parser._parse_require_line('module example.com/mymodule') is None
        assert parser._parse_require_line('go 1.19') is None
    
    def test_parse_malformed_go_mod(self):
        """Test parsing malformed go.mod content."""
        # Malformed require lines
        content = """module example.com/mymodule

go 1.19

require (
    github.com/gorilla/mux  # Missing version
    v1.8.0  # Missing module path
    github.com/lib/pq v1.10.7
)
"""
        
        dependencies = self.parser.parse(content)
        
        # Should only parse valid lines
        expected_deps = [
            PackageDependency(name='github.com/lib/pq', version='1.10.7', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 1
        for expected_dep in expected_deps:
            assert expected_dep in dependencies


class TestGoSumParser:
    """Test cases for GoSumParser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = GoSumParser()
    
    def test_can_parse_go_sum(self):
        """Test that parser correctly identifies go.sum files."""
        assert self.parser.can_parse('go.sum')
        assert self.parser.can_parse('path/to/go.sum')
        assert self.parser.can_parse('/absolute/path/go.sum')
        
        # Should not parse other files
        assert not self.parser.can_parse('go.mod')
        assert not self.parser.can_parse('Go.sum')
        assert not self.parser.can_parse('package.json')
        assert not self.parser.can_parse('Cargo.lock')
    
    def test_parse_basic_go_sum(self):
        """Test parsing a basic go.sum file."""
        content = """github.com/gorilla/mux v1.8.0 h1:i40aqfkR1h2SlN9hojwV5ZA91wcXFOvkdNIeFDP5koI=
github.com/gorilla/mux v1.8.0/go.mod h1:DVbg23sWSpFRCP0SfiEN6jmj59UnW/n46BH5rLB71So=
github.com/lib/pq v1.10.7 h1:p7ZhMD+KsSRozJr34udlUrhboJwWAgCg34+/ZZNvZZw=
github.com/lib/pq v1.10.7/go.mod h1:AlVN5x4E4T544tWzH6hKfbfQvm3HdbOxrmggDNAPY9o=
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies'),
            PackageDependency(name='github.com/lib/pq', version='1.10.7', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_go_sum_with_pseudo_versions(self):
        """Test parsing go.sum with pseudo-versions."""
        content = """golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d h1:RgqCarRHycqFkrqbBQqQQmhNRZqD3JlVHfgp1/RMvfA=
golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d/go.mod h1:IxCIyHEi3zRg3s0A5j5BB6A9Jmi73HwBIUl50j+osU4=
github.com/example/module v1.2.3-0.20220622213112-05595931fe9d h1:abc123def456=
github.com/example/module v1.2.3-0.20220622213112-05595931fe9d/go.mod h1:xyz789=
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='golang.org/x/crypto', version='0.0.0-20220622213112-05595931fe9d', dependency_type='dependencies'),
            PackageDependency(name='github.com/example/module', version='1.2.3-0.20220622213112-05595931fe9d', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_go_sum_deduplication(self):
        """Test that go.sum parser deduplicates entries."""
        content = """github.com/gorilla/mux v1.8.0 h1:i40aqfkR1h2SlN9hojwV5ZA91wcXFOvkdNIeFDP5koI=
github.com/gorilla/mux v1.8.0/go.mod h1:DVbg23sWSpFRCP0SfiEN6jmj59UnW/n46BH5rLB71So=
github.com/gorilla/mux v1.8.0 h1:different_hash_but_same_module=
"""
        
        dependencies = self.parser.parse(content)
        
        # Should only have one entry for github.com/gorilla/mux v1.8.0
        assert len(dependencies) == 1
        assert dependencies[0] == PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies')
    
    def test_parse_go_sum_with_complex_module_paths(self):
        """Test parsing go.sum with complex module paths."""
        content = """cloud.google.com/go/storage v1.27.0 h1:YOO045NZI9RKfCj1c5A/ZtuuENUc8OAW+gHdGnDgyMQ=
cloud.google.com/go/storage v1.27.0/go.mod h1:x9DOL8TK/ygDUMieqwfhdpQryTeEkhGKMi80i/iqR2s=
k8s.io/api v0.25.4 h1:3YO8J4RtmG7elEgaWMb4HgmpS2CfY1QlaOz9nwB+ZSs=
k8s.io/api v0.25.4/go.mod h1:ttceV1ht+DfB7XWJGNs2FgwfgwQAjbwFhKqE8YCBvbg=
sigs.k8s.io/controller-runtime v0.13.1 h1:tUsRCSJVM1QQOOeViGeX3GMT3dQF1eePPw6sEE3xSlg=
sigs.k8s.io/controller-runtime v0.13.1/go.mod h1:Zbz+el8Yg31jubvAEyglRZGdLAjplZl+PgtYNI6WNTI=
"""
        
        dependencies = self.parser.parse(content)
        
        expected_deps = [
            PackageDependency(name='cloud.google.com/go/storage', version='1.27.0', dependency_type='dependencies'),
            PackageDependency(name='k8s.io/api', version='0.25.4', dependency_type='dependencies'),
            PackageDependency(name='sigs.k8s.io/controller-runtime', version='0.13.1', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 3
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_empty_go_sum(self):
        """Test parsing an empty go.sum file."""
        content = ""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_parse_sum_line(self):
        """Test parsing individual go.sum lines."""
        parser = GoSumParser()
        
        # Valid sum lines
        dep1 = parser._parse_sum_line('github.com/gorilla/mux v1.8.0 h1:i40aqfkR1h2SlN9hojwV5ZA91wcXFOvkdNIeFDP5koI=')
        assert dep1 == PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies')
        
        dep2 = parser._parse_sum_line('github.com/gorilla/mux v1.8.0/go.mod h1:DVbg23sWSpFRCP0SfiEN6jmj59UnW/n46BH5rLB71So=')
        assert dep2 == PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies')
        
        dep3 = parser._parse_sum_line('golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d h1:RgqCarRHycqFkrqbBQqQQmhNRZqD3JlVHfgp1/RMvfA=')
        assert dep3 == PackageDependency(name='golang.org/x/crypto', version='0.0.0-20220622213112-05595931fe9d', dependency_type='dependencies')
        
        # Invalid lines
        assert parser._parse_sum_line('') is None
        assert parser._parse_sum_line('invalid line') is None
        assert parser._parse_sum_line('github.com/module') is None  # Missing version and hash
        assert parser._parse_sum_line('github.com/module 1.0.0') is None  # Version without 'v' prefix
    
    def test_parse_malformed_go_sum(self):
        """Test parsing malformed go.sum content."""
        content = """github.com/gorilla/mux v1.8.0 h1:i40aqfkR1h2SlN9hojwV5ZA91wcXFOvkdNIeFDP5koI=
invalid line without proper format
github.com/lib/pq v1.10.7 h1:p7ZhMD+KsSRozJr34udlUrhboJwWAgCg34+/ZZNvZZw=
another invalid line
"""
        
        dependencies = self.parser.parse(content)
        
        # Should only parse valid lines
        expected_deps = [
            PackageDependency(name='github.com/gorilla/mux', version='1.8.0', dependency_type='dependencies'),
            PackageDependency(name='github.com/lib/pq', version='1.10.7', dependency_type='dependencies'),
        ]
        
        assert len(dependencies) == 2
        for expected_dep in expected_deps:
            assert expected_dep in dependencies
    
    def test_parse_real_world_go_sum(self):
        """Test parsing a real-world go.sum example."""
        content = """cloud.google.com/go v0.26.0/go.mod h1:aQUYkXzVsufM+DwF1aE+0xfcU+56JwCaLick0ClmMTw=
github.com/BurntSushi/toml v0.3.1/go.mod h1:xHWCNGjB5oqiDr8zfno3MHue2Ht5sIBksp03qcyfWMU=
github.com/census-instrumentation/opencensus-proto v0.2.1/go.mod h1:f6KPmirojxKA12rnyqOA5BBL4O983OfeGPqjHWSTneU=
github.com/client9/misspell v0.3.4/go.mod h1:qj6jICC3Q7zFZvVWo7KLAzC3yx5G7kyvSDkc90ppPyw=
github.com/golang/glog v0.0.0-20160126235308-23def4e6c14b/go.mod h1:SBH7ygxi8pfUlaOkMMuAQtPIUF8ecWP5IEl/CR7VP2Q=
github.com/golang/mock v1.1.1/go.mod h1:oTYuIxOrZwtPieC+H1uAHpcLFnEyAGVDL/k47Jfbm0A=
github.com/golang/protobuf v1.2.0/go.mod h1:6lQm79b+lXiMfvg/cZm0SGofjICqVBUtrP5yJMmIC1U=
github.com/golang/protobuf v1.3.2/go.mod h1:6lQm79b+lXiMfvg/cZm0SGofjICqVBUtrP5yJMmIC1U=
github.com/google/go-cmp v0.2.0/go.mod h1:oXzfMopK8JAjlY9xF4vHSVASa0yLyX7SntLO5aqRK0M=
github.com/gorilla/mux v1.8.0 h1:i40aqfkR1h2SlN9hojwV5ZA91wcXFOvkdNIeFDP5koI=
github.com/gorilla/mux v1.8.0/go.mod h1:DVbg23sWSpFRCP0SfiEN6jmj59UnW/n46BH5rLB71So=
github.com/lib/pq v1.10.7 h1:p7ZhMD+KsSRozJr34udlUrhboJwWAgCg34+/ZZNvZZw=
github.com/lib/pq v1.10.7/go.mod h1:AlVN5x4E4T544tWzH6hKfbfQvm3HdbOxrmggDNAPY9o=
golang.org/x/crypto v0.0.0-20190308221718-c2843e01d9a2/go.mod h1:djNgcEr1/C05ACkg1iLfiJU5Ep61QUkGW8qpdssI0+w=
golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d h1:RgqCarRHycqFkrqbBQqQQmhNRZqD3JlVHfgp1/RMvfA=
golang.org/x/crypto v0.0.0-20220622213112-05595931fe9d/go.mod h1:IxCIyHEi3zRg3s0A5j5BB6A9Jmi73HwBIUl50j+osU4=
golang.org/x/net v0.0.0-20190603091049-60506f45cf65/go.mod h1:HSz+uSET+XFnRR8LxR5pz3Of3rY3CfYBVs4xY44aLks=
golang.org/x/sys v0.0.0-20190215142949-d0b11bdaac8a/go.mod h1:STP8DvDyc/dI5b8T5hshtkjS+E42TnysNCUPdjciGhY=
golang.org/x/text v0.3.0/go.mod h1:NqM8EUOU14njkJ3fqMW+pc6Ldnwhi/IjpwHt7yyuwOQ=
golang.org/x/text v0.3.2/go.mod h1:bEr9sfX3Q8Zfm5fL9x+3itogRgK3+ptLWKqgva+5dAk=
golang.org/x/tools v0.0.0-20180917221912-90fa682c2a6e/go.mod h1:n7NCudcB/nEzxVGmLbDWY5pfWTLqBcC2KZ6jyYvM4mQ=
"""
        
        dependencies = self.parser.parse(content)
        
        # Should extract unique modules
        module_names = [dep.name for dep in dependencies]
        
        # Check for some key modules
        assert 'github.com/gorilla/mux' in module_names
        assert 'github.com/lib/pq' in module_names
        assert 'golang.org/x/crypto' in module_names
        
        # Check specific versions
        gorilla_dep = next(dep for dep in dependencies if dep.name == 'github.com/gorilla/mux')
        assert gorilla_dep.version == '1.8.0'
        
        crypto_dep = next(dep for dep in dependencies if dep.name == 'golang.org/x/crypto')
        # Should pick the first version encountered (0.0.0-20190308221718-c2843e01d9a2)
        assert crypto_dep.version == '0.0.0-20190308221718-c2843e01d9a2'
        
        # Should have multiple dependencies but deduplicated
        assert len(dependencies) > 5