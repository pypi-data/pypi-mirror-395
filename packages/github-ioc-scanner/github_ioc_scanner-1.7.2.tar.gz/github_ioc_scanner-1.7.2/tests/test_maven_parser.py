"""Tests for Maven pom.xml parser."""

import pytest
from src.github_ioc_scanner.parsers.maven import MavenParser
from src.github_ioc_scanner.models import PackageDependency


class TestMavenParser:
    """Test cases for MavenParser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = MavenParser()
    
    def test_can_parse_pom_xml(self):
        """Test that parser correctly identifies pom.xml files."""
        assert self.parser.can_parse('pom.xml')
        assert self.parser.can_parse('path/to/pom.xml')
        assert self.parser.can_parse('/absolute/path/pom.xml')
        assert self.parser.can_parse('project/submodule/pom.xml')
        
        # Should not parse other files
        assert not self.parser.can_parse('pom.xml.bak')
        assert not self.parser.can_parse('package.json')
        assert not self.parser.can_parse('build.gradle')
        assert not self.parser.can_parse('Cargo.lock')
        assert not self.parser.can_parse('requirements.txt')
    
    def test_parse_simple_pom_with_dependencies(self):
        """Test parsing a simple pom.xml with dependencies."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.3.23</version>
        </dependency>
        <dependency>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
            <version>31.1-jre</version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 2
        
        spring_dep = next(d for d in dependencies if 'spring-core' in d.name)
        assert spring_dep.name == 'org.springframework:spring-core'
        assert spring_dep.version == '5.3.23'
        assert spring_dep.dependency_type == 'compile'
        
        guava_dep = next(d for d in dependencies if 'guava' in d.name)
        assert guava_dep.name == 'com.google.guava:guava'
        assert guava_dep.version == '31.1-jre'
        assert guava_dep.dependency_type == 'compile'
    
    def test_parse_pom_with_namespace(self):
        """Test parsing pom.xml with Maven namespace."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 1
        junit_dep = dependencies[0]
        assert junit_dep.name == 'junit:junit'
        assert junit_dep.version == '4.13.2'
        assert junit_dep.dependency_type == 'test'

    
    def test_parse_pom_with_property_resolution(self):
        """Test property resolution in versions."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>2.0.0</version>
    
    <properties>
        <spring.version>5.3.23</spring.version>
        <jackson.version>2.14.0</jackson.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>${spring.version}</version>
        </dependency>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>${jackson.version}</version>
        </dependency>
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>internal-lib</artifactId>
            <version>${project.version}</version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        
        spring_dep = next(d for d in dependencies if 'spring-core' in d.name)
        assert spring_dep.version == '5.3.23'
        
        jackson_dep = next(d for d in dependencies if 'jackson-databind' in d.name)
        assert jackson_dep.version == '2.14.0'
        
        internal_dep = next(d for d in dependencies if 'internal-lib' in d.name)
        assert internal_dep.version == '2.0.0'
    
    def test_parse_pom_with_dependency_management(self):
        """Test parsing dependencyManagement section."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>parent-pom</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>
    
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>2.7.5</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            <dependency>
                <groupId>com.google.guava</groupId>
                <artifactId>guava</artifactId>
                <version>31.1-jre</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-web</artifactId>
            <version>5.3.23</version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        # Should have 3 dependencies: 2 from dependencyManagement + 1 from dependencies
        assert len(dependencies) == 3
        
        # Check dependencyManagement dependencies
        spring_boot_dep = next(d for d in dependencies if 'spring-boot-dependencies' in d.name)
        assert spring_boot_dep.name == 'org.springframework.boot:spring-boot-dependencies'
        assert spring_boot_dep.version == '2.7.5'
        assert 'dependencyManagement' in spring_boot_dep.dependency_type
        
        guava_dep = next(d for d in dependencies if 'guava' in d.name)
        assert guava_dep.name == 'com.google.guava:guava'
        assert 'dependencyManagement' in guava_dep.dependency_type
        
        # Check regular dependency
        spring_web_dep = next(d for d in dependencies if 'spring-web' in d.name)
        assert spring_web_dep.name == 'org.springframework:spring-web'
        assert spring_web_dep.dependency_type == 'compile'
    
    def test_parse_pom_with_different_scopes(self):
        """Test parsing dependencies with different scopes."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.3.23</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.31</version>
            <scope>runtime</scope>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 4
        
        spring_dep = next(d for d in dependencies if 'spring-core' in d.name)
        assert spring_dep.dependency_type == 'compile'
        
        junit_dep = next(d for d in dependencies if 'junit' in d.name)
        assert junit_dep.dependency_type == 'test'
        
        servlet_dep = next(d for d in dependencies if 'servlet-api' in d.name)
        assert servlet_dep.dependency_type == 'provided'
        
        mysql_dep = next(d for d in dependencies if 'mysql' in d.name)
        assert mysql_dep.dependency_type == 'runtime'
    
    def test_parse_pom_with_managed_version(self):
        """Test parsing dependencies without explicit version (managed by parent)."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 1
        spring_dep = dependencies[0]
        assert spring_dep.name == 'org.springframework:spring-core'
        assert spring_dep.version == 'managed'
    
    def test_parse_empty_pom(self):
        """Test parsing empty or minimal pom.xml."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
</project>
"""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_parse_empty_content(self):
        """Test parsing empty content."""
        dependencies = self.parser.parse('')
        assert len(dependencies) == 0
        
        dependencies = self.parser.parse('   ')
        assert len(dependencies) == 0
    
    def test_parse_malformed_xml(self):
        """Test error handling for malformed XML."""
        # Missing closing tag
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.3.23</version>
"""
        
        with pytest.raises(ValueError, match="Invalid XML"):
            self.parser.parse(content)
    
    def test_parse_invalid_xml_structure(self):
        """Test error handling for invalid XML structure."""
        content = "not xml at all"
        
        with pytest.raises(ValueError, match="Invalid XML"):
            self.parser.parse(content)
    
    def test_parse_pom_with_incomplete_dependency(self):
        """Test parsing pom.xml with incomplete dependency (missing groupId or artifactId)."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.3.23</version>
        </dependency>
        <dependency>
            <groupId>missing-artifact</groupId>
            <version>1.0.0</version>
        </dependency>
        <dependency>
            <artifactId>missing-group</artifactId>
            <version>1.0.0</version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        # Should only parse the complete dependency
        assert len(dependencies) == 1
        assert dependencies[0].name == 'org.springframework:spring-core'

    
    def test_parse_pom_with_unresolved_property(self):
        """Test parsing pom.xml with unresolved property reference."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>${undefined.property}</version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 1
        # Unresolved property should remain as-is
        assert dependencies[0].version == '${undefined.property}'
    
    def test_parse_real_world_pom(self):
        """Test parsing a real-world pom.xml example."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>spring-boot-app</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    
    <properties>
        <java.version>17</java.version>
        <spring-boot.version>3.1.5</spring-boot.version>
        <lombok.version>1.18.30</lombok.version>
    </properties>
    
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>${lombok.version}</version>
            <scope>provided</scope>
        </dependency>
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <version>2.2.224</version>
            <scope>runtime</scope>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        # Should have 6 dependencies total
        assert len(dependencies) == 6
        
        # Check dependencyManagement
        boot_deps = next(d for d in dependencies if 'spring-boot-dependencies' in d.name)
        assert boot_deps.version == '3.1.5'
        assert 'dependencyManagement' in boot_deps.dependency_type
        
        # Check regular dependencies
        web_dep = next(d for d in dependencies if 'spring-boot-starter-web' in d.name)
        assert web_dep.version == 'managed'
        assert web_dep.dependency_type == 'compile'
        
        lombok_dep = next(d for d in dependencies if 'lombok' in d.name)
        assert lombok_dep.version == '1.18.30'
        assert lombok_dep.dependency_type == 'provided'
        
        h2_dep = next(d for d in dependencies if 'h2' in d.name)
        assert h2_dep.version == '2.2.224'
        assert h2_dep.dependency_type == 'runtime'
        
        test_dep = next(d for d in dependencies if 'spring-boot-starter-test' in d.name)
        assert test_dep.version == 'managed'
        assert test_dep.dependency_type == 'test'
    
    def test_parse_pom_with_nested_properties(self):
        """Test parsing pom.xml with properties in groupId and artifactId."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <spring.group>org.springframework</spring.group>
        <spring.artifact>spring-core</spring.artifact>
        <spring.version>5.3.23</spring.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>${spring.group}</groupId>
            <artifactId>${spring.artifact}</artifactId>
            <version>${spring.version}</version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 1
        dep = dependencies[0]
        assert dep.name == 'org.springframework:spring-core'
        assert dep.version == '5.3.23'
    
    def test_parse_pom_with_project_properties(self):
        """Test parsing pom.xml using project.groupId and project.artifactId."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>parent-app</artifactId>
    <version>2.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>${project.groupId}</groupId>
            <artifactId>child-module</artifactId>
            <version>${project.version}</version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 1
        dep = dependencies[0]
        assert dep.name == 'com.example:child-module'
        assert dep.version == '2.0.0'


class TestMavenParserEdgeCases:
    """Edge case tests for MavenParser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = MavenParser()
    
    def test_parse_pom_with_comments(self):
        """Test parsing pom.xml with XML comments."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <!-- Main dependencies -->
    <dependencies>
        <!-- Spring Framework -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-core</artifactId>
            <version>5.3.23</version>
        </dependency>
        <!--
        <dependency>
            <groupId>commented.out</groupId>
            <artifactId>should-not-parse</artifactId>
            <version>1.0.0</version>
        </dependency>
        -->
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 1
        assert dependencies[0].name == 'org.springframework:spring-core'
    
    def test_parse_pom_with_whitespace_in_values(self):
        """Test parsing pom.xml with whitespace in element values."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>
                org.springframework
            </groupId>
            <artifactId>
                spring-core
            </artifactId>
            <version>
                5.3.23
            </version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 1
        dep = dependencies[0]
        assert dep.name == 'org.springframework:spring-core'
        assert dep.version == '5.3.23'
    
    def test_parse_pom_with_empty_dependencies_section(self):
        """Test parsing pom.xml with empty dependencies section."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        assert len(dependencies) == 0
    
    def test_parse_pom_with_special_characters_in_version(self):
        """Test parsing pom.xml with special characters in version."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>com.google.guava</groupId>
            <artifactId>guava</artifactId>
            <version>31.1-jre</version>
        </dependency>
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-lang3</artifactId>
            <version>3.12.0</version>
        </dependency>
        <dependency>
            <groupId>io.netty</groupId>
            <artifactId>netty-all</artifactId>
            <version>4.1.85.Final</version>
        </dependency>
    </dependencies>
</project>
"""
        
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        
        guava_dep = next(d for d in dependencies if 'guava' in d.name)
        assert guava_dep.version == '31.1-jre'
        
        netty_dep = next(d for d in dependencies if 'netty' in d.name)
        assert netty_dep.version == '4.1.85.Final'



class TestMavenParserWithFixtures:
    """Tests using fixture files."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = MavenParser()
        self.fixtures_dir = 'tests/fixtures/maven'
    
    def _read_fixture(self, filename: str) -> str:
        """Read a fixture file."""
        import os
        filepath = os.path.join(self.fixtures_dir, filename)
        with open(filepath, 'r') as f:
            return f.read()
    
    def test_parse_simple_pom_fixture(self):
        """Test parsing simple_pom.xml fixture."""
        content = self._read_fixture('simple_pom.xml')
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 3
        
        names = [d.name for d in dependencies]
        assert 'org.springframework:spring-core' in names
        assert 'com.google.guava:guava' in names
        assert 'junit:junit' in names
        
        junit_dep = next(d for d in dependencies if 'junit' in d.name)
        assert junit_dep.dependency_type == 'test'
    
    def test_parse_pom_with_properties_fixture(self):
        """Test parsing pom_with_properties.xml fixture."""
        content = self._read_fixture('pom_with_properties.xml')
        dependencies = self.parser.parse(content)
        
        assert len(dependencies) == 5
        
        # Check property resolution
        spring_core = next(d for d in dependencies if 'spring-core' in d.name)
        assert spring_core.version == '5.3.23'
        
        jackson = next(d for d in dependencies if 'jackson-databind' in d.name)
        assert jackson.version == '2.14.0'
        
        internal = next(d for d in dependencies if 'internal-lib' in d.name)
        assert internal.version == '2.0.0'  # project.version
    
    def test_parse_dependency_management_fixture(self):
        """Test parsing pom_with_dependency_management.xml fixture."""
        content = self._read_fixture('pom_with_dependency_management.xml')
        dependencies = self.parser.parse(content)
        
        # 3 from dependencyManagement + 2 from dependencies
        assert len(dependencies) == 5
        
        # Check dependencyManagement entries
        spring_boot_deps = next(d for d in dependencies if 'spring-boot-dependencies' in d.name)
        assert spring_boot_deps.version == '3.1.5'
        assert 'dependencyManagement' in spring_boot_deps.dependency_type
        
        # Check regular dependencies (version managed)
        starter_web = next(d for d in dependencies if 'spring-boot-starter-web' in d.name)
        assert starter_web.version == 'managed'
        assert starter_web.dependency_type == 'compile'
    
    def test_parse_malformed_pom_fixture(self):
        """Test parsing malformed_pom.xml fixture raises error."""
        content = self._read_fixture('malformed_pom.xml')
        
        with pytest.raises(ValueError, match="Invalid XML"):
            self.parser.parse(content)
