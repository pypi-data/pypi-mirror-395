"""GitHub Actions Workflow Scanner for detecting dangerous configurations.

This module provides security scanning capabilities for GitHub Actions workflow files,
detecting dangerous triggers, malicious self-hosted runners, and Shai Hulud 2 attack patterns.
"""

import re
from typing import Any, Dict, List, Optional

import yaml

from .models import WorkflowFinding


class WorkflowScanner:
    """Scanner for GitHub Actions workflow files.
    
    Detects:
    - Dangerous trigger configurations (pull_request_target, workflow_run)
    - Malicious self-hosted runners (SHA1HULUD)
    - Shai Hulud 2 workflow patterns
    - Suspicious preinstall scripts
    """
    
    # Known malicious runner identifiers
    MALICIOUS_RUNNERS = {'SHA1HULUD', 'sha1hulud'}
    
    # Dangerous triggers that require careful review
    DANGEROUS_TRIGGERS = {'pull_request_target', 'workflow_run'}
    
    # Shai Hulud 2 specific workflow file patterns
    SHAI_HULUD_WORKFLOW_PATTERNS = [
        r'^discussion\.ya?ml$',
        r'^formatter_\d+\.ya?ml$',
    ]
    
    # Suspicious script patterns in workflows
    SUSPICIOUS_SCRIPT_PATTERNS = [
        r'npm\s+run\s+preinstall',
        r'yarn\s+preinstall',
        r'node\s+.*preinstall',
        r'curl\s+.*\|\s*sh',
        r'wget\s+.*\|\s*sh',
        r'eval\s*\(',
    ]
    
    def __init__(self):
        """Initialize the WorkflowScanner."""
        self._compiled_shai_hulud_patterns = [
            re.compile(pattern, re.IGNORECASE) 
            for pattern in self.SHAI_HULUD_WORKFLOW_PATTERNS
        ]
        self._compiled_script_patterns = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.SUSPICIOUS_SCRIPT_PATTERNS
        ]

    def scan_workflow_file(
        self, 
        repo: str, 
        file_path: str, 
        content: str
    ) -> List[WorkflowFinding]:
        """Scan a workflow YAML file for security issues.
        
        Args:
            repo: Repository full name (owner/repo)
            file_path: Path to the workflow file
            content: Raw YAML content of the workflow file
            
        Returns:
            List of WorkflowFinding objects with severity levels
        """
        findings: List[WorkflowFinding] = []
        
        # Check for Shai Hulud 2 workflow file patterns based on filename
        findings.extend(self._check_shai_hulud_filename(repo, file_path))
        
        # Parse YAML content
        try:
            workflow = yaml.safe_load(content)
            if not isinstance(workflow, dict):
                return findings
        except yaml.YAMLError:
            # If YAML parsing fails, we can't analyze the workflow
            return findings
        
        # Check for dangerous triggers
        findings.extend(self._check_dangerous_triggers(repo, file_path, workflow, content))
        
        # Check for self-hosted runners
        findings.extend(self._check_self_hosted_runners(repo, file_path, workflow))
        
        # Check for suspicious scripts
        findings.extend(self._check_suspicious_scripts(repo, file_path, workflow, content))
        
        return findings
    
    def _check_shai_hulud_filename(
        self, 
        repo: str, 
        file_path: str
    ) -> List[WorkflowFinding]:
        """Check if the workflow filename matches Shai Hulud 2 patterns.
        
        Args:
            repo: Repository full name
            file_path: Path to the workflow file
            
        Returns:
            List of findings for suspicious filenames
        """
        findings = []
        filename = file_path.split('/')[-1]
        
        for pattern in self._compiled_shai_hulud_patterns:
            if pattern.match(filename):
                findings.append(WorkflowFinding(
                    repo=repo,
                    file_path=file_path,
                    finding_type='suspicious_pattern',
                    severity='critical',
                    description=f"Workflow filename '{filename}' matches Shai Hulud 2 attack pattern",
                    recommendation="Immediately review this workflow file and check for signs of compromise. "
                                   "This filename pattern is associated with the Shai Hulud 2 supply chain attack."
                ))
                break
        
        return findings

    def _check_dangerous_triggers(
        self, 
        repo: str, 
        file_path: str, 
        workflow: Dict[str, Any],
        content: str
    ) -> List[WorkflowFinding]:
        """Check for dangerous workflow triggers.
        
        Args:
            repo: Repository full name
            file_path: Path to the workflow file
            workflow: Parsed workflow YAML
            content: Raw content for line number detection
            
        Returns:
            List of findings for dangerous triggers
        """
        findings = []
        
        # YAML parses 'on:' as True (boolean) because 'on' is a reserved word
        # Try both 'on' and True as keys
        triggers = workflow.get('on') or workflow.get(True, {})
        
        # Handle string trigger (e.g., on: push)
        if isinstance(triggers, str):
            triggers = {triggers: {}}
        # Handle list trigger (e.g., on: [push, pull_request])
        elif isinstance(triggers, list):
            triggers = {t: {} for t in triggers}
        
        if not isinstance(triggers, dict):
            return findings
        
        # Check for pull_request_target
        if 'pull_request_target' in triggers:
            line_num = self._find_line_number(content, 'pull_request_target')
            
            # Check if there's an unsafe checkout pattern
            has_unsafe_checkout = self._has_unsafe_checkout(workflow)
            
            if has_unsafe_checkout:
                findings.append(WorkflowFinding(
                    repo=repo,
                    file_path=file_path,
                    finding_type='dangerous_trigger',
                    severity='critical',
                    description="pull_request_target trigger with unsafe checkout detected. "
                                "This configuration can allow arbitrary code execution from untrusted PRs.",
                    line_number=line_num,
                    recommendation="Avoid checking out PR head code with pull_request_target. "
                                   "If necessary, use a separate workflow with limited permissions."
                ))
            else:
                findings.append(WorkflowFinding(
                    repo=repo,
                    file_path=file_path,
                    finding_type='dangerous_trigger',
                    severity='high',
                    description="pull_request_target trigger detected. This trigger runs with elevated "
                                "permissions and requires careful security review.",
                    line_number=line_num,
                    recommendation="Review this workflow carefully. Ensure no untrusted code from PRs "
                                   "is executed with elevated permissions."
                ))
        
        # Check for workflow_run
        if 'workflow_run' in triggers:
            line_num = self._find_line_number(content, 'workflow_run')
            findings.append(WorkflowFinding(
                repo=repo,
                file_path=file_path,
                finding_type='dangerous_trigger',
                severity='medium',
                description="workflow_run trigger detected. This trigger can access secrets from "
                            "the triggering workflow and may enable privilege escalation.",
                line_number=line_num,
                recommendation="Ensure this workflow properly validates the triggering workflow "
                               "and doesn't expose secrets to untrusted code."
            ))
        
        return findings
    
    def _has_unsafe_checkout(self, workflow: Dict[str, Any]) -> bool:
        """Check if workflow has an unsafe checkout pattern.
        
        Unsafe patterns include:
        - actions/checkout with ref: ${{ github.event.pull_request.head.sha }}
        - actions/checkout with ref: ${{ github.event.pull_request.head.ref }}
        
        Args:
            workflow: Parsed workflow YAML
            
        Returns:
            True if unsafe checkout pattern is detected
        """
        jobs = workflow.get('jobs', {})
        if not isinstance(jobs, dict):
            return False
        
        unsafe_refs = [
            'github.event.pull_request.head.sha',
            'github.event.pull_request.head.ref',
        ]
        
        for job in jobs.values():
            if not isinstance(job, dict):
                continue
            steps = job.get('steps', [])
            if not isinstance(steps, list):
                continue
            
            for step in steps:
                if not isinstance(step, dict):
                    continue
                uses = step.get('uses', '')
                if 'actions/checkout' in uses:
                    with_block = step.get('with', {})
                    if isinstance(with_block, dict):
                        ref = str(with_block.get('ref', ''))
                        for unsafe_ref in unsafe_refs:
                            if unsafe_ref in ref:
                                return True
        
        return False

    def _check_self_hosted_runners(
        self, 
        repo: str, 
        file_path: str, 
        workflow: Dict[str, Any]
    ) -> List[WorkflowFinding]:
        """Check for self-hosted runners and malicious runner identifiers.
        
        Args:
            repo: Repository full name
            file_path: Path to the workflow file
            workflow: Parsed workflow YAML
            
        Returns:
            List of findings for runner issues
        """
        findings = []
        jobs = workflow.get('jobs', {})
        
        if not isinstance(jobs, dict):
            return findings
        
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                continue
            
            runs_on = job.get('runs-on')
            if runs_on is None:
                continue
            
            # Normalize runs-on to a list
            if isinstance(runs_on, str):
                runners = [runs_on]
            elif isinstance(runs_on, list):
                runners = runs_on
            else:
                continue
            
            for runner in runners:
                runner_str = str(runner).strip()
                
                # Check for known malicious runners
                if runner_str in self.MALICIOUS_RUNNERS:
                    findings.append(WorkflowFinding(
                        repo=repo,
                        file_path=file_path,
                        finding_type='malicious_runner',
                        severity='critical',
                        description=f"Malicious runner identifier '{runner_str}' detected in job '{job_name}'. "
                                    "This is a known Shai Hulud 2 attack indicator.",
                        recommendation="Immediately remove this workflow and investigate your repository "
                                       "for signs of compromise. This runner is associated with supply chain attacks."
                    ))
                # Check for self-hosted runners
                elif runner_str.lower() == 'self-hosted' or 'self-hosted' in runner_str.lower():
                    findings.append(WorkflowFinding(
                        repo=repo,
                        file_path=file_path,
                        finding_type='malicious_runner',
                        severity='medium',
                        description=f"Self-hosted runner detected in job '{job_name}'. "
                                    "Self-hosted runners require security review.",
                        recommendation="Verify that this self-hosted runner is legitimate and properly secured. "
                                       "Ensure runner infrastructure is not compromised."
                    ))
        
        return findings
    
    def _check_suspicious_scripts(
        self, 
        repo: str, 
        file_path: str, 
        workflow: Dict[str, Any],
        content: str
    ) -> List[WorkflowFinding]:
        """Check for suspicious script patterns in workflow steps.
        
        Args:
            repo: Repository full name
            file_path: Path to the workflow file
            workflow: Parsed workflow YAML
            content: Raw content for pattern matching
            
        Returns:
            List of findings for suspicious scripts
        """
        findings = []
        
        # Check raw content for suspicious patterns
        for pattern in self._compiled_script_patterns:
            matches = pattern.finditer(content)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                findings.append(WorkflowFinding(
                    repo=repo,
                    file_path=file_path,
                    finding_type='suspicious_pattern',
                    severity='high',
                    description=f"Suspicious script pattern detected: '{match.group()}'",
                    line_number=line_num,
                    recommendation="Review this script command carefully. Preinstall scripts and "
                                   "piped shell commands can be used for malicious code execution."
                ))
        
        return findings
    
    def _find_line_number(self, content: str, search_term: str) -> Optional[int]:
        """Find the line number of a search term in content.
        
        Args:
            content: File content
            search_term: Term to search for
            
        Returns:
            Line number (1-indexed) or None if not found
        """
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_term in line:
                return i
        return None
    
    def is_workflow_file(self, file_path: str) -> bool:
        """Check if a file path is a GitHub Actions workflow file.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if the file is in .github/workflows/ and is a YAML file
        """
        normalized_path = file_path.replace('\\', '/')
        return (
            '.github/workflows/' in normalized_path and
            (normalized_path.endswith('.yml') or normalized_path.endswith('.yaml'))
        )
