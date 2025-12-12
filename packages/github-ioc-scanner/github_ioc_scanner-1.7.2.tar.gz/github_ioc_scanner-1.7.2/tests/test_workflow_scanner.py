"""Tests for GitHub Actions Workflow Scanner."""

import os
import pytest
from src.github_ioc_scanner.workflow_scanner import WorkflowScanner
from src.github_ioc_scanner.models import WorkflowFinding


class TestWorkflowScanner:
    """Test cases for WorkflowScanner."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scanner = WorkflowScanner()
        self.fixtures_dir = 'tests/fixtures/workflows'
        self.test_repo = 'owner/test-repo'
    
    def _read_fixture(self, filename: str) -> str:
        """Read a fixture file."""
        filepath = os.path.join(self.fixtures_dir, filename)
        with open(filepath, 'r') as f:
            return f.read()
    
    def _get_fixture_path(self, filename: str) -> str:
        """Get the workflow file path for a fixture."""
        return f'.github/workflows/{filename}'


class TestIsWorkflowFile(TestWorkflowScanner):
    """Tests for is_workflow_file method."""
    
    def test_valid_workflow_paths(self):
        """Test that valid workflow paths are recognized."""
        assert self.scanner.is_workflow_file('.github/workflows/ci.yml')
        assert self.scanner.is_workflow_file('.github/workflows/ci.yaml')
        assert self.scanner.is_workflow_file('.github/workflows/deploy.yml')
        assert self.scanner.is_workflow_file('repo/.github/workflows/test.yml')
    
    def test_invalid_workflow_paths(self):
        """Test that non-workflow paths are rejected."""
        assert not self.scanner.is_workflow_file('.github/workflows/readme.md')
        assert not self.scanner.is_workflow_file('src/workflows/ci.yml')
        assert not self.scanner.is_workflow_file('.github/ci.yml')
        assert not self.scanner.is_workflow_file('workflows/ci.yml')
        assert not self.scanner.is_workflow_file('.github/workflows/')


class TestSafeWorkflows(TestWorkflowScanner):
    """Tests for scanning safe workflow files."""
    
    def test_safe_workflow_no_findings(self):
        """Test that a safe workflow produces no findings."""
        content = self._read_fixture('safe_workflow.yml')
        file_path = self._get_fixture_path('safe_workflow.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        assert len(findings) == 0


class TestPullRequestTargetDetection(TestWorkflowScanner):
    """Tests for pull_request_target trigger detection."""
    
    def test_unsafe_pull_request_target(self):
        """Test detection of pull_request_target with unsafe checkout."""
        content = self._read_fixture('pull_request_target_unsafe.yml')
        file_path = self._get_fixture_path('pull_request_target_unsafe.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        # Should find the dangerous trigger
        trigger_findings = [f for f in findings if f.finding_type == 'dangerous_trigger']
        assert len(trigger_findings) >= 1
        
        critical_finding = next(f for f in trigger_findings if f.severity == 'critical')
        assert 'pull_request_target' in critical_finding.description
        assert 'unsafe checkout' in critical_finding.description.lower()
        assert critical_finding.recommendation is not None
    
    def test_safe_pull_request_target(self):
        """Test detection of pull_request_target without unsafe checkout."""
        content = self._read_fixture('pull_request_target_safe.yml')
        file_path = self._get_fixture_path('pull_request_target_safe.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        # Should find the trigger but with lower severity
        trigger_findings = [f for f in findings if f.finding_type == 'dangerous_trigger']
        assert len(trigger_findings) >= 1
        
        # Should be high severity, not critical (no unsafe checkout)
        high_finding = next(f for f in trigger_findings if f.severity == 'high')
        assert 'pull_request_target' in high_finding.description


class TestWorkflowRunDetection(TestWorkflowScanner):
    """Tests for workflow_run trigger detection."""
    
    def test_workflow_run_trigger(self):
        """Test detection of workflow_run trigger."""
        content = self._read_fixture('workflow_run_trigger.yml')
        file_path = self._get_fixture_path('workflow_run_trigger.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        trigger_findings = [f for f in findings if f.finding_type == 'dangerous_trigger']
        assert len(trigger_findings) >= 1
        
        workflow_run_finding = next(
            f for f in trigger_findings if 'workflow_run' in f.description
        )
        assert workflow_run_finding.severity == 'medium'
        assert 'privilege escalation' in workflow_run_finding.description.lower()


class TestMaliciousRunnerDetection(TestWorkflowScanner):
    """Tests for malicious runner detection."""
    
    def test_sha1hulud_runner(self):
        """Test detection of SHA1HULUD malicious runner."""
        content = self._read_fixture('malicious_runner.yml')
        file_path = self._get_fixture_path('malicious_runner.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        runner_findings = [f for f in findings if f.finding_type == 'malicious_runner']
        assert len(runner_findings) >= 1
        
        malicious_finding = next(
            f for f in runner_findings if f.severity == 'critical'
        )
        assert 'SHA1HULUD' in malicious_finding.description
        assert 'Shai Hulud' in malicious_finding.description
    
    def test_self_hosted_runner(self):
        """Test detection of self-hosted runner."""
        content = self._read_fixture('self_hosted_runner.yml')
        file_path = self._get_fixture_path('self_hosted_runner.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        runner_findings = [f for f in findings if f.finding_type == 'malicious_runner']
        assert len(runner_findings) >= 1
        
        self_hosted_finding = next(
            f for f in runner_findings if 'self-hosted' in f.description.lower()
        )
        assert self_hosted_finding.severity == 'medium'


class TestShaiHuludPatterns(TestWorkflowScanner):
    """Tests for Shai Hulud 2 attack pattern detection."""
    
    def test_discussion_yaml_pattern(self):
        """Test detection of discussion.yaml filename pattern."""
        content = self._read_fixture('discussion.yaml')
        file_path = self._get_fixture_path('discussion.yaml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        pattern_findings = [f for f in findings if f.finding_type == 'suspicious_pattern']
        assert len(pattern_findings) >= 1
        
        filename_finding = next(
            f for f in pattern_findings 
            if 'discussion.yaml' in f.description and 'Shai Hulud' in f.description
        )
        assert filename_finding.severity == 'critical'
    
    def test_formatter_pattern(self):
        """Test detection of formatter_NNNN.yml filename pattern."""
        content = self._read_fixture('formatter_123456789.yml')
        file_path = self._get_fixture_path('formatter_123456789.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        pattern_findings = [f for f in findings if f.finding_type == 'suspicious_pattern']
        assert len(pattern_findings) >= 1
        
        filename_finding = next(
            f for f in pattern_findings 
            if 'formatter_123456789.yml' in f.description
        )
        assert filename_finding.severity == 'critical'


class TestSuspiciousScripts(TestWorkflowScanner):
    """Tests for suspicious script pattern detection."""
    
    def test_suspicious_script_patterns(self):
        """Test detection of suspicious script patterns."""
        content = self._read_fixture('suspicious_scripts.yml')
        file_path = self._get_fixture_path('suspicious_scripts.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        script_findings = [
            f for f in findings 
            if f.finding_type == 'suspicious_pattern' and 'script' in f.description.lower()
        ]
        assert len(script_findings) >= 2  # preinstall and curl | sh
        
        # Check for preinstall detection
        preinstall_finding = next(
            (f for f in script_findings if 'preinstall' in f.description.lower()), None
        )
        assert preinstall_finding is not None
        assert preinstall_finding.severity == 'high'
        
        # Check for piped curl detection
        curl_finding = next(
            (f for f in script_findings if 'curl' in f.description.lower()), None
        )
        assert curl_finding is not None


class TestMalformedWorkflows(TestWorkflowScanner):
    """Tests for handling malformed workflow files."""
    
    def test_malformed_yaml(self):
        """Test that malformed YAML doesn't crash the scanner."""
        content = self._read_fixture('malformed.yml')
        file_path = self._get_fixture_path('malformed.yml')
        
        # Should not raise an exception
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        # May or may not have findings, but should not crash
        assert isinstance(findings, list)
    
    def test_empty_content(self):
        """Test scanning empty content."""
        findings = self.scanner.scan_workflow_file(
            self.test_repo, 
            '.github/workflows/empty.yml', 
            ''
        )
        assert findings == []
    
    def test_non_dict_yaml(self):
        """Test scanning YAML that doesn't parse to a dict."""
        content = "- item1\n- item2\n- item3"
        findings = self.scanner.scan_workflow_file(
            self.test_repo,
            '.github/workflows/list.yml',
            content
        )
        assert findings == []


class TestWorkflowFindingModel(TestWorkflowScanner):
    """Tests for WorkflowFinding data model."""
    
    def test_finding_has_required_fields(self):
        """Test that findings have all required fields."""
        content = self._read_fixture('malicious_runner.yml')
        file_path = self._get_fixture_path('malicious_runner.yml')
        
        findings = self.scanner.scan_workflow_file(self.test_repo, file_path, content)
        
        assert len(findings) > 0
        finding = findings[0]
        
        assert finding.repo == self.test_repo
        assert finding.file_path == file_path
        assert finding.finding_type in ['dangerous_trigger', 'malicious_runner', 'suspicious_pattern']
        assert finding.severity in ['critical', 'high', 'medium', 'low']
        assert finding.description is not None
        assert len(finding.description) > 0


class TestInlineWorkflows(TestWorkflowScanner):
    """Tests using inline workflow content."""
    
    def test_simple_trigger_formats(self):
        """Test various trigger format styles."""
        # String trigger format
        content_string = """
name: Test
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "test"
"""
        findings = self.scanner.scan_workflow_file(
            self.test_repo, '.github/workflows/test.yml', content_string
        )
        assert len(findings) == 0
        
        # List trigger format
        content_list = """
name: Test
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "test"
"""
        findings = self.scanner.scan_workflow_file(
            self.test_repo, '.github/workflows/test.yml', content_list
        )
        assert len(findings) == 0
    
    def test_runner_list_format(self):
        """Test detection with runs-on as a list."""
        content = """
name: Test
on: push
jobs:
  build:
    runs-on: [self-hosted, linux]
    steps:
      - run: echo "test"
"""
        findings = self.scanner.scan_workflow_file(
            self.test_repo, '.github/workflows/test.yml', content
        )
        
        runner_findings = [f for f in findings if f.finding_type == 'malicious_runner']
        assert len(runner_findings) >= 1
    
    def test_checkout_with_head_ref(self):
        """Test detection of checkout with head.ref (also unsafe)."""
        content = """
name: PR Target
on:
  pull_request_target:
    types: [opened]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.ref }}
      - run: npm test
"""
        findings = self.scanner.scan_workflow_file(
            self.test_repo, '.github/workflows/test.yml', content
        )
        
        trigger_findings = [f for f in findings if f.finding_type == 'dangerous_trigger']
        critical_findings = [f for f in trigger_findings if f.severity == 'critical']
        assert len(critical_findings) >= 1
