"""Secrets Scanner for detecting exfiltrated secrets and credentials.

This module provides scanning capabilities for detecting secrets, credentials,
and Shai Hulud 2 exfiltration artifacts in repository files.
"""

import re
from typing import Dict, List, Optional, Pattern, Tuple

from .models import SecretFinding


class SecretsScanner:
    """Scanner for detecting exfiltrated secrets and credentials.
    
    Detects:
    - AWS Access Keys (AKIA...)
    - GitHub Tokens (ghp_, gho_, ghs_)
    - API Keys (various patterns)
    - Private Keys (-----BEGIN PRIVATE KEY-----)
    - Slack tokens and other common secrets
    - Shai Hulud 2 exfiltration artifacts
    """
    
    # Secret patterns with their types and descriptions
    SECRET_PATTERNS: Dict[str, Tuple[str, str, str]] = {
        # Pattern name: (regex, description, severity)
        'aws_access_key': (
            r'AKIA[0-9A-Z]{16}',
            'AWS Access Key ID detected',
            'critical'
        ),
        'aws_secret_key': (
            r'(?i)aws[_\-]?secret[_\-]?(?:access[_\-]?)?key["\']?\s*[:=]\s*["\']?([A-Za-z0-9/+=]{40})',
            'AWS Secret Access Key detected',
            'critical'
        ),
        'github_pat': (
            r'ghp_[a-zA-Z0-9]{36}',
            'GitHub Personal Access Token detected',
            'critical'
        ),
        'github_oauth': (
            r'gho_[a-zA-Z0-9]{36}',
            'GitHub OAuth Access Token detected',
            'critical'
        ),
        'github_app': (
            r'ghs_[a-zA-Z0-9]{36}',
            'GitHub App Token detected',
            'critical'
        ),
        'github_refresh': (
            r'ghr_[a-zA-Z0-9]{36}',
            'GitHub Refresh Token detected',
            'critical'
        ),
        'slack_token': (
            r'xox[baprs]-[0-9]{10,13}-[a-zA-Z0-9]{24,}',
            'Slack Token detected',
            'critical'
        ),
        'slack_webhook': (
            r'https://hooks\.slack\.com/services/T[a-zA-Z0-9_]{8,}/B[a-zA-Z0-9_]{8,}/[a-zA-Z0-9_]{24,}',
            'Slack Webhook URL detected',
            'high'
        ),
        'private_key': (
            r'-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----',
            'Private Key detected',
            'critical'
        ),
        'generic_api_key': (
            r'(?i)(?:api[_\-]?key|apikey)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{32,})',
            'Generic API Key detected',
            'high'
        ),
        'generic_secret': (
            r'(?i)(?:secret|password|passwd|pwd)["\']?\s*[:=]\s*["\']?([a-zA-Z0-9_\-!@#$%^&*]{16,})',
            'Generic Secret/Password detected',
            'high'
        ),
        'bearer_token': (
            r'(?i)bearer\s+[a-zA-Z0-9_\-\.]{20,}',
            'Bearer Token detected',
            'high'
        ),
        'npm_token': (
            r'npm_[a-zA-Z0-9]{36}',
            'NPM Access Token detected',
            'critical'
        ),
        'pypi_token': (
            r'pypi-[a-zA-Z0-9_\-]{100,}',
            'PyPI API Token detected',
            'critical'
        ),
        'stripe_key': (
            r'(?:sk|pk)_(?:live|test)_[a-zA-Z0-9]{24,}',
            'Stripe API Key detected',
            'critical'
        ),
        'sendgrid_key': (
            r'SG\.[a-zA-Z0-9_\-]{22}\.[a-zA-Z0-9_\-]{43}',
            'SendGrid API Key detected',
            'critical'
        ),
        'twilio_key': (
            r'SK[a-f0-9]{32}',
            'Twilio API Key detected',
            'critical'
        ),
        'mailchimp_key': (
            r'[a-f0-9]{32}-us[0-9]{1,2}',
            'Mailchimp API Key detected',
            'high'
        ),
        'heroku_key': (
            r'(?i)heroku[_\-]?api[_\-]?key["\']?\s*[:=]\s*["\']?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})',
            'Heroku API Key detected',
            'critical'
        ),
        'google_api_key': (
            r'AIza[0-9A-Za-z_\-]{35}',
            'Google API Key detected',
            'high'
        ),
        'firebase_key': (
            r'AAAA[A-Za-z0-9_\-]{7}:[A-Za-z0-9_\-]{140}',
            'Firebase Cloud Messaging Key detected',
            'high'
        ),
    }
    
    # Shai Hulud 2 exfiltration artifact filenames
    SHAI_HULUD_ARTIFACTS = {
        'cloud.json': 'Shai Hulud 2 AWS credentials exfiltration artifact',
        'contents.json': 'Shai Hulud 2 repository contents exfiltration artifact',
        'environment.json': 'Shai Hulud 2 environment variables exfiltration artifact',
        'truffleSecrets.json': 'Shai Hulud 2 Truffle secrets exfiltration artifact',
    }
    
    # File extensions to skip (binary files)
    BINARY_EXTENSIONS = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.zip', '.tar', '.gz', '.rar', '.7z',
        '.exe', '.dll', '.so', '.dylib',
        '.woff', '.woff2', '.ttf', '.eot',
        '.mp3', '.mp4', '.avi', '.mov', '.wav',
        '.pyc', '.pyo', '.class', '.o',
        '.lock', '.lockb',
    }
    
    # Maximum file size to scan (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    def __init__(self):
        """Initialize the SecretsScanner with compiled regex patterns."""
        self._compiled_patterns: Dict[str, Tuple[Pattern, str, str]] = {}
        for name, (pattern, description, severity) in self.SECRET_PATTERNS.items():
            self._compiled_patterns[name] = (
                re.compile(pattern),
                description,
                severity
            )
    
    def scan_for_secrets(
        self, 
        repo: str, 
        file_path: str, 
        content: str
    ) -> List[SecretFinding]:
        """Scan file content for secrets and credentials.
        
        Args:
            repo: Repository full name (owner/repo)
            file_path: Path to the file being scanned
            content: File content to scan
            
        Returns:
            List of SecretFinding objects with masked values
        """
        findings: List[SecretFinding] = []
        
        # Check for Shai Hulud 2 artifacts based on filename
        findings.extend(self._check_shai_hulud_artifacts(repo, file_path))
        
        # Skip binary files
        if self._is_binary_file(file_path):
            return findings
        
        # Skip large files
        if len(content) > self.MAX_FILE_SIZE:
            return findings
        
        # Scan for secret patterns
        findings.extend(self._scan_patterns(repo, file_path, content))
        
        return findings
    
    def _check_shai_hulud_artifacts(
        self, 
        repo: str, 
        file_path: str
    ) -> List[SecretFinding]:
        """Check if the file is a known Shai Hulud 2 exfiltration artifact.
        
        Args:
            repo: Repository full name
            file_path: Path to the file
            
        Returns:
            List of findings for Shai Hulud 2 artifacts
        """
        findings = []
        filename = file_path.split('/')[-1]
        
        if filename in self.SHAI_HULUD_ARTIFACTS:
            description = self.SHAI_HULUD_ARTIFACTS[filename]
            findings.append(SecretFinding(
                repo=repo,
                file_path=file_path,
                secret_type='shai_hulud_artifact',
                masked_value='N/A',
                line_number=0,
                severity='critical',
                description=description,
                recommendation="Immediately investigate this file. It may contain exfiltrated "
                              "credentials or sensitive data from a Shai Hulud 2 supply chain attack. "
                              "Rotate all potentially exposed credentials."
            ))
        
        return findings
    
    def _scan_patterns(
        self, 
        repo: str, 
        file_path: str, 
        content: str
    ) -> List[SecretFinding]:
        """Scan content for secret patterns.
        
        Args:
            repo: Repository full name
            file_path: Path to the file
            content: File content to scan
            
        Returns:
            List of findings for detected secrets
        """
        findings = []
        lines = content.split('\n')
        
        for pattern_name, (compiled_pattern, description, severity) in self._compiled_patterns.items():
            for line_num, line in enumerate(lines, 1):
                matches = compiled_pattern.finditer(line)
                for match in matches:
                    # Get the matched value
                    matched_value = match.group(0)
                    
                    # Check if this looks like a false positive
                    if self._is_likely_false_positive(line, matched_value, pattern_name):
                        continue
                    
                    # Mask the secret value
                    masked = self._mask_secret(matched_value)
                    
                    findings.append(SecretFinding(
                        repo=repo,
                        file_path=file_path,
                        secret_type=pattern_name,
                        masked_value=masked,
                        line_number=line_num,
                        severity=severity,
                        description=description,
                        recommendation=self._get_recommendation(pattern_name)
                    ))
        
        return findings
    
    def _is_binary_file(self, file_path: str) -> bool:
        """Check if a file is likely binary based on extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file appears to be binary
        """
        lower_path = file_path.lower()
        return any(lower_path.endswith(ext) for ext in self.BINARY_EXTENSIONS)
    
    def _is_likely_false_positive(
        self, 
        line: str, 
        matched_value: str, 
        pattern_name: str
    ) -> bool:
        """Check if a match is likely a false positive.
        
        Args:
            line: The line containing the match
            matched_value: The matched secret value
            pattern_name: Name of the pattern that matched
            
        Returns:
            True if this is likely a false positive
        """
        lower_line = line.lower()
        
        # Skip if in a comment
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('*'):
            return True
        
        # Skip example/placeholder values
        placeholder_indicators = [
            'example', 'placeholder', 'your_', 'your-', 'xxx', 
            'test', 'dummy', 'fake', 'sample', '<your', '[your',
            'replace', 'insert', 'todo', 'fixme'
        ]
        if any(indicator in lower_line for indicator in placeholder_indicators):
            return True
        
        # Skip documentation patterns
        if 'documentation' in lower_line or 'readme' in lower_line:
            return True
        
        # For generic patterns, require more context
        if pattern_name in ('generic_api_key', 'generic_secret'):
            # Skip if the value is all the same character (likely placeholder)
            if len(set(matched_value.replace('-', '').replace('_', ''))) <= 2:
                return True
        
        return False
    
    def _mask_secret(self, value: str) -> str:
        """Mask a secret value, showing only first 4 characters.
        
        Args:
            value: The secret value to mask
            
        Returns:
            Masked value (first 4 chars + '***')
        """
        if len(value) <= 4:
            return '***'
        return value[:4] + '***'
    
    def _get_recommendation(self, pattern_name: str) -> str:
        """Get remediation recommendation for a secret type.
        
        Args:
            pattern_name: Name of the secret pattern
            
        Returns:
            Recommendation string
        """
        recommendations = {
            'aws_access_key': "Rotate this AWS access key immediately. Check CloudTrail for unauthorized access.",
            'aws_secret_key': "Rotate this AWS secret key immediately. Check CloudTrail for unauthorized access.",
            'github_pat': "Revoke this GitHub Personal Access Token and create a new one with minimal permissions.",
            'github_oauth': "Revoke this GitHub OAuth token and investigate potential unauthorized access.",
            'github_app': "Revoke this GitHub App token and check for unauthorized API calls.",
            'github_refresh': "Revoke this GitHub refresh token and rotate associated credentials.",
            'slack_token': "Revoke this Slack token and check for unauthorized messages or data access.",
            'slack_webhook': "Regenerate this Slack webhook URL and update your integrations.",
            'private_key': "Rotate this private key immediately. Check for unauthorized access using this key.",
            'generic_api_key': "Rotate this API key and review access logs for unauthorized usage.",
            'generic_secret': "Change this password/secret and review access logs.",
            'bearer_token': "Revoke this bearer token and issue a new one.",
            'npm_token': "Revoke this NPM token and check for unauthorized package publications.",
            'pypi_token': "Revoke this PyPI token and check for unauthorized package uploads.",
            'stripe_key': "Rotate this Stripe key and review transaction logs for unauthorized activity.",
            'sendgrid_key': "Rotate this SendGrid key and check for unauthorized email sends.",
            'twilio_key': "Rotate this Twilio key and review usage logs.",
            'mailchimp_key': "Rotate this Mailchimp key and check for unauthorized campaign access.",
            'heroku_key': "Rotate this Heroku API key and review app access logs.",
            'google_api_key': "Rotate this Google API key and review usage in Google Cloud Console.",
            'firebase_key': "Rotate this Firebase key and review Cloud Messaging logs.",
        }
        return recommendations.get(
            pattern_name, 
            "Rotate this credential immediately and investigate potential unauthorized access."
        )
    
    def should_scan_file(self, file_path: str, file_size: int) -> bool:
        """Check if a file should be scanned for secrets.
        
        For Shai-Hulud detection, we only need to check for specific artifact files.
        Full secrets scanning of all files is optional and can be slow.
        
        Args:
            file_path: Path to the file
            file_size: Size of the file in bytes
            
        Returns:
            True if the file should be scanned
        """
        filename = file_path.split('/')[-1]
        
        # Always scan Shai-Hulud artifact files
        if filename in self.SHAI_HULUD_ARTIFACTS:
            return True
        
        # Skip binary files
        if self._is_binary_file(file_path):
            return False
        
        # Skip large files
        if file_size > self.MAX_FILE_SIZE:
            return False
        
        return True
    
    def is_shai_hulud_artifact(self, file_path: str) -> bool:
        """Check if a file is a known Shai-Hulud exfiltration artifact.
        
        This is a fast check that can be used to prioritize scanning.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if the file is a known Shai-Hulud artifact
        """
        filename = file_path.split('/')[-1]
        return filename in self.SHAI_HULUD_ARTIFACTS
