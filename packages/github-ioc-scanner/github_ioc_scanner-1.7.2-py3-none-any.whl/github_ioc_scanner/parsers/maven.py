"""Maven package manager parser for pom.xml files."""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

from .base import PackageParser
from ..models import PackageDependency


class MavenParser(PackageParser):
    """
    Parser for Maven pom.xml files.
    
    Extracts dependencies from Maven POM files, supporting:
    - <dependencies> section
    - <dependencyManagement> section
    - Basic property resolution (${project.version}, ${property.name})
    - Different dependency scopes (compile, test, provided, runtime)
    
    Limitations:
    - Parent POM inheritance is not resolved (requires network access)
    - Complex property resolution (e.g., from parent POMs) is not supported
    - Profile-specific dependencies are not extracted
    - Import-scoped dependencies in dependencyManagement are not resolved
    """
    
    # Maven POM namespace
    MAVEN_NS = {'m': 'http://maven.apache.org/POM/4.0.0'}
    
    def can_parse(self, file_path: str) -> bool:
        """Check if this parser can handle pom.xml files."""
        return file_path.endswith('pom.xml')
    
    def parse(self, content: str) -> List[PackageDependency]:
        """
        Parse pom.xml content and extract Maven dependencies.
        
        Extracts:
        - groupId:artifactId as package identifier
        - version from <version> tag
        - dependency scope (compile, test, provided, runtime)
        
        Args:
            content: Raw pom.xml content
            
        Returns:
            List of PackageDependency objects with Maven format
            
        Raises:
            ValueError: If pom.xml format is severely malformed
        """
        if not content or not content.strip():
            return []
        
        try:
            # Parse XML content
            root = ET.fromstring(content)
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML in pom.xml: {e}")
        
        # Detect namespace usage
        ns = self._detect_namespace(root)
        
        # Extract properties for variable resolution
        properties = self._extract_properties(root, ns)
        
        # Extract project-level properties
        project_version = self._get_text(root, 'version', ns)
        project_group_id = self._get_text(root, 'groupId', ns)
        project_artifact_id = self._get_text(root, 'artifactId', ns)
        
        # Add project properties to the properties dict
        if project_version:
            properties['project.version'] = project_version
        if project_group_id:
            properties['project.groupId'] = project_group_id
        if project_artifact_id:
            properties['project.artifactId'] = project_artifact_id
        
        dependencies = []
        
        # Extract from <dependencies> section
        deps_from_dependencies = self._extract_dependencies(root, ns, properties, 'dependencies')
        dependencies.extend(deps_from_dependencies)
        
        # Extract from <dependencyManagement><dependencies> section
        deps_from_mgmt = self._extract_dependencies(root, ns, properties, 'dependencyManagement/dependencies')
        dependencies.extend(deps_from_mgmt)
        
        return dependencies
    
    def _detect_namespace(self, root: ET.Element) -> Dict[str, str]:
        """
        Detect if the POM uses Maven namespace.
        
        Args:
            root: Root XML element
            
        Returns:
            Namespace dict for XPath queries, empty if no namespace
        """
        # Check if root tag includes namespace
        if root.tag.startswith('{http://maven.apache.org/POM/4.0.0}'):
            return self.MAVEN_NS
        return {}
    
    def _get_xpath_prefix(self, ns: Dict[str, str]) -> str:
        """Get XPath prefix based on namespace."""
        return 'm:' if ns else ''
    
    def _extract_properties(self, root: ET.Element, ns: Dict[str, str]) -> Dict[str, str]:
        """
        Extract properties from <properties> section.
        
        Args:
            root: Root XML element
            ns: Namespace dict
            
        Returns:
            Dict mapping property names to values
        """
        properties = {}
        prefix = self._get_xpath_prefix(ns)
        
        # Find properties element
        props_path = f'{prefix}properties' if prefix else 'properties'
        props_elem = root.find(props_path, ns) if ns else root.find('properties')
        
        if props_elem is not None:
            for prop in props_elem:
                # Remove namespace from tag name
                tag_name = prop.tag
                if tag_name.startswith('{'):
                    tag_name = tag_name.split('}')[1]
                if prop.text:
                    properties[tag_name] = prop.text.strip()
        
        return properties
    
    def _get_text(self, element: ET.Element, tag: str, ns: Dict[str, str]) -> Optional[str]:
        """
        Get text content of a child element.
        
        Args:
            element: Parent element
            tag: Child tag name
            ns: Namespace dict
            
        Returns:
            Text content or None
        """
        prefix = self._get_xpath_prefix(ns)
        path = f'{prefix}{tag}' if prefix else tag
        child = element.find(path, ns) if ns else element.find(tag)
        
        if child is not None and child.text:
            return child.text.strip()
        return None
    
    def _resolve_property(self, value: Optional[str], properties: Dict[str, str]) -> Optional[str]:
        """
        Resolve Maven property references in a value.
        
        Handles:
        - ${property.name} references
        - ${project.version} and similar project properties
        
        Args:
            value: String that may contain property references
            properties: Dict of available properties
            
        Returns:
            Resolved value or original if no properties found
        """
        if not value:
            return value
        
        # Pattern to match ${property.name}
        pattern = r'\$\{([^}]+)\}'
        
        def replace_property(match):
            prop_name = match.group(1)
            return properties.get(prop_name, match.group(0))
        
        resolved = re.sub(pattern, replace_property, value)
        return resolved
    
    def _extract_dependencies(
        self, 
        root: ET.Element, 
        ns: Dict[str, str], 
        properties: Dict[str, str],
        section_path: str
    ) -> List[PackageDependency]:
        """
        Extract dependencies from a specific section.
        
        Args:
            root: Root XML element
            ns: Namespace dict
            properties: Properties for variable resolution
            section_path: Path to dependencies section (e.g., 'dependencies' or 'dependencyManagement/dependencies')
            
        Returns:
            List of PackageDependency objects
        """
        dependencies = []
        prefix = self._get_xpath_prefix(ns)
        
        # Build XPath for the section
        if prefix:
            xpath_parts = section_path.split('/')
            full_path = '/'.join(f'{prefix}{part}' for part in xpath_parts)
        else:
            full_path = section_path
        
        # Find the dependencies container
        deps_container = root.find(full_path, ns) if ns else root.find(section_path)
        
        if deps_container is None:
            return dependencies
        
        # Find all dependency elements
        dep_tag = f'{prefix}dependency' if prefix else 'dependency'
        for dep_elem in deps_container.findall(dep_tag, ns) if ns else deps_container.findall('dependency'):
            dep = self._parse_dependency(dep_elem, ns, properties, section_path)
            if dep:
                dependencies.append(dep)
        
        return dependencies
    
    def _parse_dependency(
        self, 
        dep_elem: ET.Element, 
        ns: Dict[str, str], 
        properties: Dict[str, str],
        section_path: str
    ) -> Optional[PackageDependency]:
        """
        Parse a single dependency element.
        
        Args:
            dep_elem: Dependency XML element
            ns: Namespace dict
            properties: Properties for variable resolution
            section_path: Source section for dependency type
            
        Returns:
            PackageDependency or None if invalid
        """
        group_id = self._get_text(dep_elem, 'groupId', ns)
        artifact_id = self._get_text(dep_elem, 'artifactId', ns)
        version = self._get_text(dep_elem, 'version', ns)
        scope = self._get_text(dep_elem, 'scope', ns) or 'compile'
        
        # Both groupId and artifactId are required
        if not group_id or not artifact_id:
            return None
        
        # Resolve property references
        group_id = self._resolve_property(group_id, properties)
        artifact_id = self._resolve_property(artifact_id, properties)
        version = self._resolve_property(version, properties)
        
        # Version might be managed elsewhere (dependencyManagement)
        # Use 'managed' as placeholder if not specified
        if not version:
            version = 'managed'
        
        # Create package name in Maven format: groupId:artifactId
        package_name = f"{group_id}:{artifact_id}"
        
        # Determine dependency type based on scope and section
        if 'dependencyManagement' in section_path:
            dep_type = f'dependencyManagement-{scope}'
        else:
            dep_type = scope
        
        return PackageDependency(
            name=package_name,
            version=version,
            dependency_type=dep_type
        )
