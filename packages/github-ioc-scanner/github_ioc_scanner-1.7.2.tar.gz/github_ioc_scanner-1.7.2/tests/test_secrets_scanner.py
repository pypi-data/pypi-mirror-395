"""Tests for Secrets Scanner."""

import os
import pytest
from src.github_ioc_scanner.secrets_scanner import SecretsScanner
from src.github_ioc_scanner.models import SecretFinding


class TestSecretsScanner:
    """Test cases for SecretsScanner."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scanner = SecretsScanner()
        self.fixtures_dir = 'tests/fixtures/secrets'
        self.test_repo = 'owner/test-repo'
    
    def _read_fixture(self, filename: str) -> str:
        """Read a fixture file."""
        filepath = os.path.join(self.fixtures_dir, filename)
        with open(filepath, 'r') as f:
            return f.read()


class TestAWSKeyDetection(TestSecretsScanner):
    """Tests for AWS access key detection."""
    
    def test_detect_aws_access_key(self):
        """Test detection of AWS access keys."""
        content = self._read_fixture('aws_credentials.txt')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config/aws.txt', content
        )
        
        aws_findings = [f for f in findings if f.secret_type == 'aws_access_key']
        assert len(aws_findings) >= 2
        
        for finding in aws_findings:
            assert finding.severity == 'critical'
            assert finding.masked_value.startswith('AKIA')
            assert '***' in finding.masked_value
    
    def test_aws_key_inline(self):
        """Test detection of inline AWS access key."""
        content = "AWS_KEY=AKIAIOSFODNN7PRODKEY"
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config.txt', content
        )
        
        aws_findings = [f for f in findings if f.secret_type == 'aws_access_key']
        assert len(aws_findings) == 1
        assert aws_findings[0].line_number == 1


class TestGitHubTokenDetection(TestSecretsScanner):
    """Tests for GitHub token detection."""
    
    def test_detect_github_pat(self):
        """Test detection of GitHub Personal Access Token."""
        content = self._read_fixture('github_tokens.txt')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, '.env', content
        )
        
        pat_findings = [f for f in findings if f.secret_type == 'github_pat']
        assert len(pat_findings) >= 1
        assert pat_findings[0].severity == 'critical'
        assert pat_findings[0].masked_value.startswith('ghp_')
    
    def test_detect_github_oauth(self):
        """Test detection of GitHub OAuth token."""
        content = self._read_fixture('github_tokens.txt')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, '.env', content
        )
        
        oauth_findings = [f for f in findings if f.secret_type == 'github_oauth']
        assert len(oauth_findings) >= 1
        assert oauth_findings[0].masked_value.startswith('gho_')
    
    def test_detect_github_app_token(self):
        """Test detection of GitHub App token."""
        content = self._read_fixture('github_tokens.txt')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, '.env', content
        )
        
        app_findings = [f for f in findings if f.secret_type == 'github_app']
        assert len(app_findings) >= 1
        assert app_findings[0].masked_value.startswith('ghs_')
    
    def test_detect_github_refresh_token(self):
        """Test detection of GitHub refresh token."""
        content = self._read_fixture('github_tokens.txt')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, '.env', content
        )
        
        refresh_findings = [f for f in findings if f.secret_type == 'github_refresh']
        assert len(refresh_findings) >= 1
        assert refresh_findings[0].masked_value.startswith('ghr_')


class TestShaiHuludArtifacts(TestSecretsScanner):
    """Tests for Shai Hulud 2 artifact detection."""
    
    def test_detect_cloud_json(self):
        """Test detection of cloud.json artifact."""
        content = self._read_fixture('cloud.json')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'cloud.json', content
        )
        
        artifact_findings = [f for f in findings if f.secret_type == 'shai_hulud_artifact']
        assert len(artifact_findings) >= 1
        assert artifact_findings[0].severity == 'critical'
        assert 'AWS credentials' in artifact_findings[0].description
    
    def test_detect_environment_json(self):
        """Test detection of environment.json artifact."""
        content = self._read_fixture('environment.json')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'environment.json', content
        )
        
        artifact_findings = [f for f in findings if f.secret_type == 'shai_hulud_artifact']
        assert len(artifact_findings) >= 1
        assert 'environment variables' in artifact_findings[0].description
    
    def test_detect_truffle_secrets_json(self):
        """Test detection of truffleSecrets.json artifact."""
        content = self._read_fixture('truffleSecrets.json')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'truffleSecrets.json', content
        )
        
        artifact_findings = [f for f in findings if f.secret_type == 'shai_hulud_artifact']
        assert len(artifact_findings) >= 1
        assert 'Truffle secrets' in artifact_findings[0].description
    
    def test_detect_contents_json(self):
        """Test detection of contents.json artifact."""
        content = self._read_fixture('contents.json')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'contents.json', content
        )
        
        artifact_findings = [f for f in findings if f.secret_type == 'shai_hulud_artifact']
        assert len(artifact_findings) >= 1
        assert 'repository contents' in artifact_findings[0].description


class TestSecretMasking(TestSecretsScanner):
    """Tests for proper secret masking."""
    
    def test_mask_secret_shows_first_four_chars(self):
        """Test that masking shows first 4 characters."""
        masked = self.scanner._mask_secret('AKIAIOSFODNN7EXAMPLE')
        assert masked == 'AKIA***'
    
    def test_mask_short_secret(self):
        """Test masking of short secrets."""
        masked = self.scanner._mask_secret('abc')
        assert masked == '***'
    
    def test_mask_exactly_four_chars(self):
        """Test masking of exactly 4 character secret."""
        masked = self.scanner._mask_secret('abcd')
        assert masked == '***'
    
    def test_findings_have_masked_values(self):
        """Test that all findings have properly masked values."""
        content = "GITHUB_TOKEN=ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890"
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config.env', content
        )
        
        assert len(findings) >= 1
        for finding in findings:
            # Masked value should not contain the full secret
            assert len(finding.masked_value) <= 7  # 4 chars + '***'
            assert '***' in finding.masked_value


class TestPrivateKeyDetection(TestSecretsScanner):
    """Tests for private key detection."""
    
    def test_detect_rsa_private_key(self):
        """Test detection of RSA private key."""
        content = self._read_fixture('private_key.pem')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'key.pem', content
        )
        
        key_findings = [f for f in findings if f.secret_type == 'private_key']
        assert len(key_findings) >= 1
        assert key_findings[0].severity == 'critical'
    
    def test_detect_ec_private_key(self):
        """Test detection of EC private key."""
        content = "-----BEGIN EC PRIVATE KEY-----\nMHQCAQEE..."
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'ec_key.pem', content
        )
        
        key_findings = [f for f in findings if f.secret_type == 'private_key']
        assert len(key_findings) >= 1


class TestSlackTokenDetection(TestSecretsScanner):
    """Tests for Slack token detection."""
    
    def test_detect_slack_bot_token(self):
        """Test detection of Slack bot token."""
        content = self._read_fixture('slack_tokens.txt')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config.txt', content
        )
        
        slack_findings = [f for f in findings if f.secret_type == 'slack_token']
        assert len(slack_findings) >= 1
        assert slack_findings[0].severity == 'critical'
    
    def test_detect_slack_webhook(self):
        """Test detection of Slack webhook URL."""
        content = self._read_fixture('slack_tokens.txt')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config.txt', content
        )
        
        webhook_findings = [f for f in findings if f.secret_type == 'slack_webhook']
        assert len(webhook_findings) >= 1


class TestFalsePositiveHandling(TestSecretsScanner):
    """Tests for false positive handling."""
    
    def test_skip_comments(self):
        """Test that secrets in comments are skipped."""
        content = "# AWS_KEY=AKIAIOSFODNN7EXAMPLE"
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config.txt', content
        )
        
        assert len(findings) == 0
    
    def test_skip_placeholder_values(self):
        """Test that placeholder values are skipped."""
        content = "api_key = your_api_key_here"
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config.txt', content
        )
        
        assert len(findings) == 0
    
    def test_skip_example_values(self):
        """Test that example values are skipped."""
        content = "# Example: AKIAIOSFODNN7EXAMPLE"
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'readme.md', content
        )
        
        assert len(findings) == 0
    
    def test_safe_file_no_findings(self):
        """Test that safe files produce no findings."""
        content = self._read_fixture('safe_file.txt')
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'safe.txt', content
        )
        
        assert len(findings) == 0


class TestBinaryFileHandling(TestSecretsScanner):
    """Tests for binary file handling."""
    
    def test_skip_binary_files(self):
        """Test that binary files are skipped."""
        assert self.scanner._is_binary_file('image.png')
        assert self.scanner._is_binary_file('archive.zip')
        assert self.scanner._is_binary_file('binary.exe')
        assert not self.scanner._is_binary_file('config.txt')
        assert not self.scanner._is_binary_file('script.py')
    
    def test_should_scan_file(self):
        """Test should_scan_file method."""
        assert self.scanner.should_scan_file('config.txt', 1000)
        assert not self.scanner.should_scan_file('image.png', 1000)
        assert not self.scanner.should_scan_file('config.txt', 20 * 1024 * 1024)


class TestSecretFindingModel(TestSecretsScanner):
    """Tests for SecretFinding data model."""
    
    def test_finding_has_required_fields(self):
        """Test that findings have all required fields."""
        content = "GITHUB_TOKEN=ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890"
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config.env', content
        )
        
        assert len(findings) > 0
        finding = findings[0]
        
        assert finding.repo == self.test_repo
        assert finding.file_path == 'config.env'
        assert finding.secret_type is not None
        assert finding.masked_value is not None
        assert finding.line_number >= 1
        assert finding.severity in ['critical', 'high', 'medium', 'low']
    
    def test_finding_has_recommendation(self):
        """Test that findings include recommendations."""
        content = "GITHUB_TOKEN=ghp_aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890"
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'config.env', content
        )
        
        assert len(findings) > 0
        assert findings[0].recommendation is not None
        assert len(findings[0].recommendation) > 0


class TestEmptyAndEdgeCases(TestSecretsScanner):
    """Tests for empty and edge cases."""
    
    def test_empty_content(self):
        """Test scanning empty content."""
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'empty.txt', ''
        )
        assert findings == []
    
    def test_large_file_skipped(self):
        """Test that large files are skipped."""
        # Create content larger than MAX_FILE_SIZE
        large_content = 'x' * (11 * 1024 * 1024)  # 11MB
        
        findings = self.scanner.scan_for_secrets(
            self.test_repo, 'large.txt', large_content
        )
        
        assert findings == []
