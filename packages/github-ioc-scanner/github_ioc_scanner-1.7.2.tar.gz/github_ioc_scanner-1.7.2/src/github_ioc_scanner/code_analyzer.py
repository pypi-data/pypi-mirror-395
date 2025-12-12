"""Code analyzer utility for identifying unused modules and documentation."""

import ast
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class AnalysisReport:
    """Report of project analysis findings."""
    unused_modules: List[str] = field(default_factory=list)
    outdated_docs: List[str] = field(default_factory=list)
    unused_dependencies: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    total_files_analyzed: int = 0
    potential_savings: str = ""
    import_graph: Dict[str, Set[str]] = field(default_factory=dict)
    module_info: Dict[str, dict] = field(default_factory=dict)
    analysis_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class CodeAnalyzer:
    """Analyzes project structure to identify unused components."""
    
    def __init__(self, project_root: str):
        """
        Initialize the CodeAnalyzer.
        
        Args:
            project_root: Root directory of the project to analyze
        """
        self.project_root = Path(project_root)
        self.import_graph: Dict[str, Set[str]] = {}
        self.reverse_import_graph: Dict[str, Set[str]] = {}
        self.module_info: Dict[str, dict] = {}
        
    def analyze_project(self, src_dir: str = "src/github_ioc_scanner") -> AnalysisReport:
        """
        Analyze project structure and identify unused code.
        
        Args:
            src_dir: Source directory relative to project root
            
        Returns:
            AnalysisReport with recommendations
        """
        report = AnalysisReport()
        
        # Step 1: Scan all Python modules
        src_path = self.project_root / src_dir
        modules = self._scan_python_modules(src_path)
        report.total_files_analyzed = len(modules)
        
        # Step 2: Build import dependency graph
        self._build_import_graph(modules, src_path)
        report.import_graph = {k: set(v) for k, v in self.import_graph.items()}
        report.module_info = self.module_info
        
        # Step 3: Identify orphaned modules
        unused = self.find_unused_modules(modules)
        report.unused_modules = unused
        
        # Step 4: Analyze documentation
        docs_path = self.project_root / "docs"
        if docs_path.exists():
            outdated = self.find_outdated_docs(str(docs_path))
            report.outdated_docs = outdated
        
        # Step 5: Generate recommendations
        report.recommendations = self._generate_recommendations(report)
        
        # Calculate potential savings
        total_lines = sum(
            self.module_info.get(m, {}).get('lines', 0) 
            for m in unused
        )
        report.potential_savings = f"~{total_lines} LOC, {len(unused)} files"
        
        return report

    
    def _scan_python_modules(self, src_path: Path) -> List[str]:
        """
        Scan directory for Python modules.
        
        Args:
            src_path: Path to source directory
            
        Returns:
            List of module paths relative to src_path
        """
        modules = []
        
        for root, dirs, files in os.walk(src_path):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(src_path)
                    modules.append(str(rel_path))
                    
                    # Collect module info
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        lines = len(content.splitlines())
                        self.module_info[str(rel_path)] = {
                            'path': str(file_path),
                            'lines': lines,
                            'size': len(content),
                        }
                    except Exception:
                        self.module_info[str(rel_path)] = {
                            'path': str(file_path),
                            'lines': 0,
                            'size': 0,
                        }
        
        return modules
    
    def _build_import_graph(self, modules: List[str], src_path: Path) -> None:
        """
        Build import dependency graph for all modules.
        
        Args:
            modules: List of module paths
            src_path: Path to source directory
        """
        self.import_graph = {m: set() for m in modules}
        self.reverse_import_graph = {m: set() for m in modules}
        
        for module in modules:
            module_path = src_path / module
            try:
                content = module_path.read_text(encoding='utf-8')
                imports = self._extract_imports(content, module)
                
                for imp in imports:
                    # Normalize import to module path
                    normalized = self._normalize_import(imp, modules)
                    if normalized and normalized in self.import_graph:
                        self.import_graph[module].add(normalized)
                        self.reverse_import_graph[normalized].add(module)
                        
            except Exception:
                continue
    
    def _extract_imports(self, content: str, current_module: str) -> Set[str]:
        """
        Extract import statements from Python source code.
        
        Args:
            content: Python source code
            current_module: Current module path for relative import resolution
            
        Returns:
            Set of imported module names
        """
        imports = set()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return imports
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Handle relative imports
                    if node.level > 0:
                        # Relative import
                        base = self._resolve_relative_import(current_module, node.level)
                        if node.module:
                            imports.add(f"{base}.{node.module}" if base else node.module)
                        else:
                            imports.add(base)
                    else:
                        imports.add(node.module)
                elif node.level > 0:
                    # from . import something
                    base = self._resolve_relative_import(current_module, node.level)
                    for alias in node.names:
                        imports.add(f"{base}.{alias.name}" if base else alias.name)
        
        return imports
    
    def _resolve_relative_import(self, current_module: str, level: int) -> str:
        """
        Resolve relative import to absolute module path.
        
        Args:
            current_module: Current module path (e.g., 'parsers/python.py')
            level: Number of dots in relative import
            
        Returns:
            Base module path for the relative import
        """
        parts = current_module.replace('.py', '').split('/')
        
        # Remove filename for level 1
        if level >= 1:
            parts = parts[:-1]
        
        # Go up additional levels
        for _ in range(level - 1):
            if parts:
                parts = parts[:-1]
        
        return '/'.join(parts)
    
    def _normalize_import(self, import_name: str, modules: List[str]) -> Optional[str]:
        """
        Normalize import name to match module paths.
        
        Args:
            import_name: Import statement (e.g., 'github_ioc_scanner.models')
            modules: List of known module paths
            
        Returns:
            Normalized module path or None if not found
        """
        # Handle github_ioc_scanner imports
        if import_name.startswith('github_ioc_scanner.'):
            # Remove package prefix
            remainder = import_name[len('github_ioc_scanner.'):]
            # Convert to path
            path = remainder.replace('.', '/') + '.py'
            if path in modules:
                return path
            # Try as package __init__
            init_path = remainder.replace('.', '/') + '/__init__.py'
            if init_path in modules:
                return init_path
        
        # Handle relative imports already converted to paths
        if '/' in import_name:
            path = import_name + '.py'
            if path in modules:
                return path
            init_path = import_name + '/__init__.py'
            if init_path in modules:
                return init_path
        
        # Direct module name
        path = import_name + '.py'
        if path in modules:
            return path
        
        return None

    
    def find_unused_modules(self, modules: List[str]) -> List[str]:
        """
        Find modules that are never imported by other modules.
        
        Args:
            modules: List of module paths
            
        Returns:
            List of unused module paths
        """
        unused = []
        
        # Entry points that are expected to have no importers
        entry_points = {
            '__init__.py',
            'cli.py',
            'resume_cli.py',
        }
        
        # Modules in issues/ are IOC definitions loaded dynamically
        # Modules in parsers/ may be loaded via factory pattern
        
        for module in modules:
            # Skip entry points
            if any(module.endswith(ep) for ep in entry_points):
                continue
            
            # Skip __init__.py files (package markers)
            if module.endswith('__init__.py'):
                continue
            
            # Check if module is imported by anyone
            importers = self.reverse_import_graph.get(module, set())
            
            if not importers:
                # Check if it's a dynamically loaded module
                if not self._is_dynamically_loaded(module):
                    unused.append(module)
        
        return sorted(unused)
    
    def _is_dynamically_loaded(self, module: str) -> bool:
        """
        Check if a module is loaded dynamically (not via static imports).
        
        Args:
            module: Module path
            
        Returns:
            True if module is dynamically loaded
        """
        # Issues are loaded dynamically by ioc_loader
        if module.startswith('issues/'):
            return True
        
        # Parsers may be loaded via factory
        if module.startswith('parsers/') and not module.endswith('__init__.py'):
            return True
        
        return False
    
    def find_outdated_docs(self, docs_dir: str) -> List[str]:
        """
        Find documentation files that may be outdated.
        
        Args:
            docs_dir: Path to documentation directory
            
        Returns:
            List of potentially outdated documentation files
        """
        outdated = []
        docs_path = Path(docs_dir)
        
        # Patterns indicating potentially outdated docs
        outdated_patterns = [
            r'SUMMARY',  # Summary docs often become stale
            r'COMPLETE',  # "Complete" docs may be outdated
            r'FIX_SUMMARY',
            r'IMPLEMENTATION_SUMMARY',
        ]
        
        # Check for docs that reference removed features or old versions
        for doc_file in docs_path.glob('*.md'):
            filename = doc_file.name
            
            # Check filename patterns
            for pattern in outdated_patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    outdated.append(filename)
                    break
            else:
                # Check content for staleness indicators
                try:
                    content = doc_file.read_text(encoding='utf-8')
                    if self._check_doc_staleness(content, filename):
                        outdated.append(filename)
                except Exception:
                    continue
        
        return sorted(outdated)
    
    def _check_doc_staleness(self, content: str, filename: str) -> bool:
        """
        Check if documentation content appears stale.
        
        Args:
            content: Documentation content
            filename: Documentation filename
            
        Returns:
            True if documentation appears stale
        """
        # Check for old version references
        old_version_pattern = r'version\s*["\']?1\.[0-3]\.'
        if re.search(old_version_pattern, content, re.IGNORECASE):
            return True
        
        # Check for "TODO" or "WIP" markers
        if re.search(r'\bTODO\b|\bWIP\b|\bFIXME\b', content):
            return True
        
        # Check for very short docs (might be stubs)
        if len(content) < 500 and 'SUMMARY' in filename.upper():
            return True
        
        return False
    
    def _generate_recommendations(self, report: AnalysisReport) -> List[str]:
        """
        Generate cleanup recommendations based on analysis.
        
        Args:
            report: Analysis report with findings
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if report.unused_modules:
            recommendations.append(
                f"Consider removing {len(report.unused_modules)} unused modules: "
                f"{', '.join(report.unused_modules[:5])}"
                + ("..." if len(report.unused_modules) > 5 else "")
            )
        
        if report.outdated_docs:
            recommendations.append(
                f"Review {len(report.outdated_docs)} potentially outdated documentation files"
            )
        
        # Check for modules with no tests
        tested_modules = set()
        for module in self.module_info:
            test_name = f"test_{Path(module).stem}.py"
            # This is a simplified check
            if (self.project_root / "tests" / test_name).exists():
                tested_modules.add(module)
        
        untested = set(self.module_info.keys()) - tested_modules
        if untested:
            recommendations.append(
                f"{len(untested)} modules may lack dedicated test files"
            )
        
        return recommendations
    
    def generate_report_markdown(self, report: AnalysisReport) -> str:
        """
        Generate a markdown report from the analysis.
        
        Args:
            report: Analysis report
            
        Returns:
            Markdown formatted report
        """
        lines = [
            "# Project Cleanup Report",
            "",
            f"**Analysis Date:** {report.analysis_timestamp}",
            f"**Total Files Analyzed:** {report.total_files_analyzed}",
            f"**Potential Savings:** {report.potential_savings}",
            "",
            "## Summary",
            "",
            f"- Unused modules identified: {len(report.unused_modules)}",
            f"- Potentially outdated docs: {len(report.outdated_docs)}",
            f"- Recommendations: {len(report.recommendations)}",
            "",
        ]
        
        if report.unused_modules:
            lines.extend([
                "## Unused Modules",
                "",
                "The following modules appear to have no imports from other modules:",
                "",
            ])
            for module in report.unused_modules:
                info = report.module_info.get(module, {})
                lines.append(f"- `{module}` ({info.get('lines', 0)} lines)")
            lines.append("")
        
        if report.outdated_docs:
            lines.extend([
                "## Potentially Outdated Documentation",
                "",
                "The following documentation files may need review:",
                "",
            ])
            for doc in report.outdated_docs:
                lines.append(f"- `{doc}`")
            lines.append("")
        
        if report.recommendations:
            lines.extend([
                "## Recommendations",
                "",
            ])
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")
        
        lines.extend([
            "## Import Dependency Graph",
            "",
            "### Modules with Most Dependents",
            "",
        ])
        
        # Find most imported modules
        import_counts = [
            (module, len(importers))
            for module, importers in report.import_graph.items()
            if importers
        ]
        import_counts.sort(key=lambda x: -x[1])
        
        for module, count in import_counts[:10]:
            lines.append(f"- `{module}`: imported by {count} modules")
        
        lines.append("")
        lines.extend([
            "## Next Steps",
            "",
            "1. Review unused modules and confirm they can be safely removed",
            "2. Update or archive outdated documentation",
            "3. Run full test suite after any cleanup",
            "4. Update `__init__.py` exports if modules are removed",
            "",
        ])
        
        return "\n".join(lines)
