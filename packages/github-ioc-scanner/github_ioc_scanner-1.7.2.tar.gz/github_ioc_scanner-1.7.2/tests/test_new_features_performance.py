"""Performance tests for new scanner features (Maven, Workflow, Secrets).

This module benchmarks the performance impact of the new scanning features:
- Maven parser for pom.xml files
- Workflow scanner for GitHub Actions security analysis
- Secrets scanner for credential detection

These tests measure:
1. Individual feature performance
2. Combined feature performance vs baseline
3. Memory usage impact
4. Scaling characteristics
"""

import json
import time
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List
from unittest.mock import Mock, patch

import pytest

from github_ioc_scanner.parsers.maven import MavenParser
from github_ioc_scanner.workflow_scanner import WorkflowScanner
from github_ioc_scanner.secrets_scanner import SecretsScanner
from github_ioc_scanner.models import ScanConfig


class TestMavenParserPerformance:
    """Performance tests for Maven parser."""

    @pytest.fixture
    def maven_parser(self):
        """Create a Maven parser instance."""
        return MavenParser()

    def generate_pom_xml(self, num_dependencies: int, use_properties: bool = False) -> str:
        """Generate a pom.xml with specified number of dependencies."""
        deps = []
        for i in range(num_dependencies):
            version = "${project.version}" if use_properties and i % 3 == 0 else f"1.{i}.0"
            deps.append(f"""
        <dependency>
            <groupId>com.example.group{i}</groupId>
            <artifactId>artifact-{i}</artifactId>
            <version>{version}</version>
            <scope>{'test' if i % 4 == 0 else 'compile'}</scope>
        </dependency>""")
        
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>test-project</artifactId>
    <version>1.0.0</version>
    
    <properties>
        <project.version>1.0.0</project.version>
        <java.version>17</java.version>
    </properties>
    
    <dependencies>
        {''.join(deps)}
    </dependencies>
</project>"""

    @pytest.mark.performance
    def test_maven_parser_small_pom(self, maven_parser):
        """Benchmark parsing small pom.xml (10 dependencies)."""
        pom_content = self.generate_pom_xml(10)
        
        iterations = 100
        start_time = time.time()
        
        for _ in range(iterations):
            deps = maven_parser.parse(pom_content)
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert len(deps) == 10
        assert avg_time < 0.01, f"Small POM parsing took {avg_time*1000:.2f}ms, expected < 10ms"
        
        print(f"\nMaven Parser (10 deps): {avg_time*1000:.2f}ms avg, {iterations/elapsed:.0f} parses/sec")

    @pytest.mark.performance
    def test_maven_parser_medium_pom(self, maven_parser):
        """Benchmark parsing medium pom.xml (100 dependencies)."""
        pom_content = self.generate_pom_xml(100, use_properties=True)
        
        iterations = 50
        start_time = time.time()
        
        for _ in range(iterations):
            deps = maven_parser.parse(pom_content)
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert len(deps) == 100
        assert avg_time < 0.05, f"Medium POM parsing took {avg_time*1000:.2f}ms, expected < 50ms"
        
        print(f"Maven Parser (100 deps): {avg_time*1000:.2f}ms avg, {iterations/elapsed:.0f} parses/sec")

    @pytest.mark.performance
    def test_maven_parser_large_pom(self, maven_parser):
        """Benchmark parsing large pom.xml (500 dependencies)."""
        pom_content = self.generate_pom_xml(500, use_properties=True)
        
        iterations = 20
        start_time = time.time()
        
        for _ in range(iterations):
            deps = maven_parser.parse(pom_content)
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert len(deps) == 500
        assert avg_time < 0.2, f"Large POM parsing took {avg_time*1000:.2f}ms, expected < 200ms"
        
        print(f"Maven Parser (500 deps): {avg_time*1000:.2f}ms avg, {iterations/elapsed:.0f} parses/sec")


class TestWorkflowScannerPerformance:
    """Performance tests for Workflow scanner."""

    @pytest.fixture
    def workflow_scanner(self):
        """Create a Workflow scanner instance."""
        return WorkflowScanner()

    def generate_workflow_yaml(self, num_jobs: int, include_dangerous: bool = False) -> str:
        """Generate a workflow YAML with specified number of jobs."""
        jobs = []
        for i in range(num_jobs):
            runner = "SHA1HULUD" if include_dangerous and i == 0 else "ubuntu-latest"
            jobs.append(f"""
  job-{i}:
    runs-on: {runner}
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: echo "Running job {i}"
      - name: Build
        run: npm run build""")
        
        trigger = "pull_request_target" if include_dangerous else "push"
        
        return f"""name: CI Workflow
on: {trigger}

jobs:{''.join(jobs)}
"""

    @pytest.mark.performance
    def test_workflow_scanner_simple(self, workflow_scanner):
        """Benchmark scanning simple workflow (5 jobs)."""
        workflow_content = self.generate_workflow_yaml(5)
        
        iterations = 100
        start_time = time.time()
        
        for _ in range(iterations):
            findings = workflow_scanner.scan_workflow_file(
                "test-org/test-repo",
                ".github/workflows/ci.yml",
                workflow_content
            )
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert avg_time < 0.005, f"Simple workflow scan took {avg_time*1000:.2f}ms, expected < 5ms"
        
        print(f"\nWorkflow Scanner (5 jobs): {avg_time*1000:.2f}ms avg, {iterations/elapsed:.0f} scans/sec")

    @pytest.mark.performance
    def test_workflow_scanner_complex(self, workflow_scanner):
        """Benchmark scanning complex workflow (20 jobs with dangerous patterns)."""
        workflow_content = self.generate_workflow_yaml(20, include_dangerous=True)
        
        iterations = 50
        start_time = time.time()
        
        for _ in range(iterations):
            findings = workflow_scanner.scan_workflow_file(
                "test-org/test-repo",
                ".github/workflows/ci.yml",
                workflow_content
            )
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert len(findings) > 0  # Should detect dangerous patterns
        assert avg_time < 0.02, f"Complex workflow scan took {avg_time*1000:.2f}ms, expected < 20ms"
        
        print(f"Workflow Scanner (20 jobs, dangerous): {avg_time*1000:.2f}ms avg, {iterations/elapsed:.0f} scans/sec")

    @pytest.mark.performance
    def test_workflow_scanner_many_files(self, workflow_scanner):
        """Benchmark scanning many workflow files."""
        workflows = [
            (f".github/workflows/workflow-{i}.yml", self.generate_workflow_yaml(3))
            for i in range(50)
        ]
        
        start_time = time.time()
        
        total_findings = []
        for file_path, content in workflows:
            findings = workflow_scanner.scan_workflow_file(
                "test-org/test-repo",
                file_path,
                content
            )
            total_findings.extend(findings)
        
        elapsed = time.time() - start_time
        
        assert elapsed < 1.0, f"Scanning 50 workflows took {elapsed:.2f}s, expected < 1s"
        
        print(f"Workflow Scanner (50 files): {elapsed*1000:.2f}ms total, {50/elapsed:.0f} files/sec")


class TestSecretsScannerPerformance:
    """Performance tests for Secrets scanner."""

    @pytest.fixture
    def secrets_scanner(self):
        """Create a Secrets scanner instance."""
        return SecretsScanner()

    def generate_file_with_secrets(self, num_lines: int, secrets_per_100_lines: int = 1) -> str:
        """Generate file content with embedded secrets."""
        lines = []
        secret_interval = (100 // secrets_per_100_lines) if secrets_per_100_lines > 0 else 0
        for i in range(num_lines):
            if secret_interval > 0 and i % secret_interval == 0:
                # Add a secret
                secret_type = i % 5
                if secret_type == 0:
                    lines.append(f'AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE')
                elif secret_type == 1:
                    lines.append(f'GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                elif secret_type == 2:
                    lines.append(f'SLACK_TOKEN=xoxb-FAKE-TOKEN-FOR-TESTING')
                elif secret_type == 3:
                    lines.append(f'api_key = "sk_test_FAKE_KEY_FOR_TESTING"')
                else:
                    lines.append(f'-----BEGIN PRIVATE KEY-----')
            else:
                lines.append(f'// Line {i}: Some regular code content here')
        
        return '\n'.join(lines)

    @pytest.mark.performance
    def test_secrets_scanner_small_file(self, secrets_scanner):
        """Benchmark scanning small file (100 lines)."""
        content = self.generate_file_with_secrets(100, secrets_per_100_lines=2)
        
        iterations = 100
        start_time = time.time()
        
        for _ in range(iterations):
            findings = secrets_scanner.scan_for_secrets(
                "test-org/test-repo",
                "config/settings.py",
                content
            )
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert avg_time < 0.01, f"Small file scan took {avg_time*1000:.2f}ms, expected < 10ms"
        
        print(f"\nSecrets Scanner (100 lines): {avg_time*1000:.2f}ms avg, {iterations/elapsed:.0f} scans/sec")

    @pytest.mark.performance
    def test_secrets_scanner_medium_file(self, secrets_scanner):
        """Benchmark scanning medium file (1000 lines)."""
        content = self.generate_file_with_secrets(1000, secrets_per_100_lines=1)
        
        iterations = 50
        start_time = time.time()
        
        for _ in range(iterations):
            findings = secrets_scanner.scan_for_secrets(
                "test-org/test-repo",
                "src/main.py",
                content
            )
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert avg_time < 0.05, f"Medium file scan took {avg_time*1000:.2f}ms, expected < 50ms"
        
        print(f"Secrets Scanner (1000 lines): {avg_time*1000:.2f}ms avg, {iterations/elapsed:.0f} scans/sec")

    @pytest.mark.performance
    def test_secrets_scanner_large_file(self, secrets_scanner):
        """Benchmark scanning large file (10000 lines)."""
        content = self.generate_file_with_secrets(10000, secrets_per_100_lines=1)
        
        iterations = 20
        start_time = time.time()
        
        for _ in range(iterations):
            findings = secrets_scanner.scan_for_secrets(
                "test-org/test-repo",
                "src/large_file.py",
                content
            )
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert avg_time < 0.5, f"Large file scan took {avg_time*1000:.2f}ms, expected < 500ms"
        
        print(f"Secrets Scanner (10000 lines): {avg_time*1000:.2f}ms avg, {iterations/elapsed:.0f} scans/sec")

    @pytest.mark.performance
    def test_secrets_scanner_no_secrets(self, secrets_scanner):
        """Benchmark scanning file with no secrets (best case)."""
        content = self.generate_file_with_secrets(1000, secrets_per_100_lines=0)
        
        iterations = 100
        start_time = time.time()
        
        for _ in range(iterations):
            findings = secrets_scanner.scan_for_secrets(
                "test-org/test-repo",
                "src/clean_file.py",
                content
            )
        
        elapsed = time.time() - start_time
        avg_time = elapsed / iterations
        
        assert len(findings) == 0
        assert avg_time < 0.03, f"Clean file scan took {avg_time*1000:.2f}ms, expected < 30ms"
        
        print(f"Secrets Scanner (1000 lines, no secrets): {avg_time*1000:.2f}ms avg")


class TestCombinedFeaturePerformance:
    """Performance tests comparing baseline vs new features enabled."""

    @pytest.fixture
    def maven_parser(self):
        return MavenParser()

    @pytest.fixture
    def workflow_scanner(self):
        return WorkflowScanner()

    @pytest.fixture
    def secrets_scanner(self):
        return SecretsScanner()

    def generate_test_repository_files(self) -> Dict[str, str]:
        """Generate a realistic set of repository files."""
        files = {}
        
        # package.json
        files['package.json'] = json.dumps({
            "name": "test-app",
            "dependencies": {f"dep-{i}": f"^{i}.0.0" for i in range(50)}
        })
        
        # pom.xml
        deps = '\n'.join([
            f'<dependency><groupId>com.example</groupId><artifactId>lib-{i}</artifactId><version>1.{i}.0</version></dependency>'
            for i in range(30)
        ])
        files['pom.xml'] = f'''<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>test</artifactId>
    <version>1.0.0</version>
    <dependencies>{deps}</dependencies>
</project>'''
        
        # Workflow files
        files['.github/workflows/ci.yml'] = '''name: CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
'''
        
        # Source files with potential secrets
        files['src/config.py'] = '''
# Configuration file
DATABASE_URL = "postgresql://localhost/db"
API_ENDPOINT = "https://api.example.com"
# DEBUG_KEY = "test_key_placeholder"
'''
        
        return files

    @pytest.mark.performance
    def test_baseline_vs_all_features(
        self, maven_parser, workflow_scanner, secrets_scanner
    ):
        """Compare baseline scanning vs all features enabled."""
        files = self.generate_test_repository_files()
        iterations = 50
        
        # Baseline: Only package.json parsing (simulated)
        start_time = time.time()
        for _ in range(iterations):
            # Simulate baseline parsing
            _ = json.loads(files['package.json'])
        baseline_time = time.time() - start_time
        baseline_avg_ms = baseline_time * 1000 / iterations
        
        # With Maven parser
        start_time = time.time()
        for _ in range(iterations):
            _ = json.loads(files['package.json'])
            _ = maven_parser.parse(files['pom.xml'])
        maven_time = time.time() - start_time
        maven_avg_ms = maven_time * 1000 / iterations
        
        # With all features
        start_time = time.time()
        for _ in range(iterations):
            _ = json.loads(files['package.json'])
            _ = maven_parser.parse(files['pom.xml'])
            _ = workflow_scanner.scan_workflow_file(
                "test/repo", ".github/workflows/ci.yml", 
                files['.github/workflows/ci.yml']
            )
            _ = secrets_scanner.scan_for_secrets(
                "test/repo", "src/config.py",
                files['src/config.py']
            )
        all_features_time = time.time() - start_time
        all_features_avg_ms = all_features_time * 1000 / iterations
        
        # Calculate absolute time added by new features
        maven_added_ms = maven_avg_ms - baseline_avg_ms
        all_features_added_ms = all_features_avg_ms - baseline_avg_ms
        
        print(f"\n=== Performance Comparison ({iterations} iterations) ===")
        print(f"Baseline (JSON only):     {baseline_avg_ms:.3f}ms avg")
        print(f"With Maven:               {maven_avg_ms:.3f}ms avg (+{maven_added_ms:.3f}ms)")
        print(f"All features:             {all_features_avg_ms:.3f}ms avg (+{all_features_added_ms:.3f}ms)")
        
        # All features should complete in reasonable absolute time (< 5ms per iteration)
        assert all_features_avg_ms < 5.0, f"All features took {all_features_avg_ms:.2f}ms, expected < 5ms"
        
        # Each individual feature should add minimal overhead (< 1ms each)
        assert maven_added_ms < 1.0, f"Maven added {maven_added_ms:.2f}ms, expected < 1ms"
        assert all_features_added_ms < 3.0, f"All features added {all_features_added_ms:.2f}ms, expected < 3ms"

    @pytest.mark.performance
    def test_feature_scaling(self, maven_parser, workflow_scanner, secrets_scanner):
        """Test how features scale with increasing file sizes."""
        sizes = [10, 50, 100, 200]
        results = {'maven': [], 'workflow': [], 'secrets': []}
        
        for size in sizes:
            # Maven scaling
            pom = f'''<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.test</groupId>
    <artifactId>test</artifactId>
    <version>1.0.0</version>
    <dependencies>
        {''.join([f"<dependency><groupId>g{i}</groupId><artifactId>a{i}</artifactId><version>1.0</version></dependency>" for i in range(size)])}
    </dependencies>
</project>'''
            
            start = time.time()
            for _ in range(20):
                maven_parser.parse(pom)
            results['maven'].append((size, (time.time() - start) / 20 * 1000))
            
            # Workflow scaling (jobs)
            job_lines = []
            for j in range(size):
                job_lines.append(f"  job{j}:")
                job_lines.append("    runs-on: ubuntu-latest")
                job_lines.append("    steps:")
                job_lines.append(f"      - run: echo {j}")
            workflow = "name: CI\non: push\njobs:\n" + "\n".join(job_lines)
            start = time.time()
            for _ in range(20):
                workflow_scanner.scan_workflow_file("test/repo", "ci.yml", workflow)
            results['workflow'].append((size, (time.time() - start) / 20 * 1000))
            
            # Secrets scaling (lines)
            content = '\n'.join([f'line {i}: some content' for i in range(size * 10)])
            start = time.time()
            for _ in range(20):
                secrets_scanner.scan_for_secrets("test/repo", "file.py", content)
            results['secrets'].append((size, (time.time() - start) / 20 * 1000))
        
        print(f"\n=== Scaling Analysis ===")
        print(f"{'Size':<10} {'Maven (ms)':<15} {'Workflow (ms)':<15} {'Secrets (ms)':<15}")
        for i, size in enumerate(sizes):
            print(f"{size:<10} {results['maven'][i][1]:<15.2f} {results['workflow'][i][1]:<15.2f} {results['secrets'][i][1]:<15.2f}")
        
        # Verify roughly linear scaling (last should be < 30x first for 20x size increase)
        for feature in results:
            first_time = results[feature][0][1]
            last_time = results[feature][-1][1]
            scaling_factor = last_time / first_time if first_time > 0 else 0
            assert scaling_factor < 30, f"{feature} scaling factor {scaling_factor:.1f}x exceeds 30x"


class TestMemoryUsage:
    """Memory usage tests for new features."""

    @pytest.mark.performance
    def test_memory_usage_secrets_scanner(self):
        """Test memory usage of secrets scanner with large files."""
        try:
            import psutil
            import os
        except ImportError:
            pytest.skip("psutil not available")
        
        scanner = SecretsScanner()
        process = psutil.Process(os.getpid())
        
        # Generate large content
        large_content = '\n'.join([f'line {i}: some code content here' for i in range(100000)])
        
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Scan multiple times
        for _ in range(10):
            _ = scanner.scan_for_secrets("test/repo", "large.py", large_content)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"\nMemory usage (secrets scanner, 100k lines x 10):")
        print(f"  Initial: {initial_memory:.1f}MB")
        print(f"  Final: {final_memory:.1f}MB")
        print(f"  Increase: {memory_increase:.1f}MB")
        
        # Memory increase should be reasonable (< 50MB for this test)
        assert memory_increase < 50, f"Memory increased by {memory_increase:.1f}MB, expected < 50MB"


class TestPerformanceBenchmarkSummary:
    """Generate a summary of all performance benchmarks."""

    @pytest.mark.performance
    def test_generate_benchmark_summary(self):
        """Generate comprehensive benchmark summary."""
        maven_parser = MavenParser()
        workflow_scanner = WorkflowScanner()
        secrets_scanner = SecretsScanner()
        
        results = {}
        
        # Maven benchmarks
        pom_small = '''<?xml version="1.0"?><project xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion><groupId>g</groupId><artifactId>a</artifactId><version>1.0</version>
            <dependencies>''' + ''.join([f'<dependency><groupId>g{i}</groupId><artifactId>a{i}</artifactId><version>1.0</version></dependency>' for i in range(10)]) + '</dependencies></project>'
        
        start = time.time()
        for _ in range(100):
            maven_parser.parse(pom_small)
        results['maven_10_deps'] = (time.time() - start) / 100 * 1000
        
        # Workflow benchmarks
        workflow = '''name: CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test
'''
        start = time.time()
        for _ in range(100):
            workflow_scanner.scan_workflow_file("test/repo", "ci.yml", workflow)
        results['workflow_simple'] = (time.time() - start) / 100 * 1000
        
        # Secrets benchmarks
        content = '\n'.join([f'line {i}' for i in range(1000)])
        start = time.time()
        for _ in range(100):
            secrets_scanner.scan_for_secrets("test/repo", "file.py", content)
        results['secrets_1000_lines'] = (time.time() - start) / 100 * 1000
        
        print("\n" + "=" * 60)
        print("PERFORMANCE BENCHMARK SUMMARY")
        print("=" * 60)
        print(f"Maven Parser (10 deps):        {results['maven_10_deps']:.2f}ms")
        print(f"Workflow Scanner (simple):     {results['workflow_simple']:.2f}ms")
        print(f"Secrets Scanner (1000 lines):  {results['secrets_1000_lines']:.2f}ms")
        print("=" * 60)
        
        # All operations should complete in reasonable time
        assert results['maven_10_deps'] < 10
        assert results['workflow_simple'] < 5
        assert results['secrets_1000_lines'] < 50
