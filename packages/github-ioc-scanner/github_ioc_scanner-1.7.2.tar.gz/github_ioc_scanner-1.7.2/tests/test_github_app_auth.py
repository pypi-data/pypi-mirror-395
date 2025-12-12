"""Tests for GitHub App authentication functionality."""

import os
import tempfile
import yaml
from unittest.mock import Mock, patch, MagicMock
import pytest

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from github_ioc_scanner.github_app_auth import GitHubAppAuth, create_github_app_auth
from github_ioc_scanner.exceptions import AuthenticationError


class TestGitHubAppAuth:
    """Test GitHub App authentication functionality."""
    
    def create_test_config(self):
        """Create a test configuration."""
        return {
            'auth': {
                'environment': 'production',
                'providers': {
                    'github': {
                        'production': {
                            'appId': 12345,
                            'clientId': 'Iv1.test123',
                            'clientSecret': 'test_secret',
                            'privateKey': '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
-----END RSA PRIVATE KEY-----'''
                        }
                    }
                }
            }
        }
    
    def test_config_loading(self):
        """Test loading configuration from file."""
        config = self.create_test_config()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            auth = GitHubAppAuth(config_path)
            assert auth.config['appId'] == 12345
            assert auth.config['clientId'] == 'Iv1.test123'
        finally:
            os.unlink(config_path)
    
    def test_missing_config_file(self):
        """Test handling of missing configuration file."""
        with pytest.raises(AuthenticationError, match="configuration file not found"):
            GitHubAppAuth("/nonexistent/path.yaml")
    
    def test_invalid_yaml(self):
        """Test handling of invalid YAML."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            config_path = f.name
        
        try:
            with pytest.raises(AuthenticationError, match="Invalid YAML"):
                GitHubAppAuth(config_path)
        finally:
            os.unlink(config_path)
    
    def test_missing_required_fields(self):
        """Test handling of missing required configuration fields."""
        config = {
            'auth': {
                'providers': {
                    'github': {
                        'production': {
                            'appId': 12345,
                            # Missing clientId, clientSecret, privateKey
                        }
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            with pytest.raises(AuthenticationError, match="Missing required.*fields"):
                GitHubAppAuth(config_path)
        finally:
            os.unlink(config_path)
    
    @patch('github_ioc_scanner.github_app_auth.jwt')
    def test_jwt_token_creation(self, mock_jwt):
        """Test JWT token creation."""
        config = self.create_test_config()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            mock_jwt.encode.return_value = 'test_jwt_token'
            
            auth = GitHubAppAuth(config_path)
            token = auth._create_jwt_token()
            
            assert token == 'test_jwt_token'
            mock_jwt.encode.assert_called_once()
        finally:
            os.unlink(config_path)
    
    @patch('httpx.Client')
    def test_get_installation_id(self, mock_client):
        """Test getting installation ID for organization."""
        config = self.create_test_config()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            # Mock HTTP response
            mock_response = Mock()
            mock_response.json.return_value = [
                {
                    'id': 123456,
                    'account': {'login': 'test-org'}
                }
            ]
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = Mock()
            mock_client_instance.get.return_value = mock_response
            mock_client.return_value.__enter__.return_value = mock_client_instance
            
            auth = GitHubAppAuth(config_path)
            installation_id = auth._get_installation_id('test-org', 'jwt_token')
            
            assert installation_id == 123456
        finally:
            os.unlink(config_path)
    
    @patch('httpx.Client')
    def test_get_installation_token(self, mock_client):
        """Test getting installation access token."""
        config = self.create_test_config()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            # Mock HTTP response
            mock_response = Mock()
            mock_response.json.return_value = {
                'token': 'ghs_test_token',
                'expires_at': '2024-01-01T12:00:00Z'
            }
            mock_response.raise_for_status.return_value = None
            
            mock_client_instance = Mock()
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value.__enter__.return_value = mock_client_instance
            
            auth = GitHubAppAuth(config_path)
            token, expires_at = auth._get_installation_token(123456, 'jwt_token')
            
            assert token == 'ghs_test_token'
            assert expires_at is not None
        finally:
            os.unlink(config_path)
    
    def test_is_available_no_jwt(self):
        """Test availability check when JWT is not available."""
        with patch('github_ioc_scanner.github_app_auth.JWT_AVAILABLE', False):
            assert not GitHubAppAuth.is_available()
    
    def test_is_available_no_config(self):
        """Test availability check when config is not available."""
        assert not GitHubAppAuth.is_available("/nonexistent/path.yaml")
    
    def test_create_github_app_auth_success(self):
        """Test successful creation of GitHub App auth."""
        config = self.create_test_config()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            auth = create_github_app_auth(config_path)
            assert auth is not None
            assert isinstance(auth, GitHubAppAuth)
        finally:
            os.unlink(config_path)
    
    def test_create_github_app_auth_failure(self):
        """Test failed creation of GitHub App auth."""
        auth = create_github_app_auth("/nonexistent/path.yaml")
        assert auth is None


class TestGitHubAppAuthIntegration:
    """Integration tests for GitHub App authentication."""
    
    def test_cli_integration(self):
        """Test CLI integration with GitHub App auth."""
        # This would require actual GitHub App credentials
        # For now, just test that the CLI accepts the parameter
        
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        
        from github_ioc_scanner.cli import CLIInterface
        
        cli = CLIInterface()
        config = cli.parse_arguments([
            '--org', 'test-org',
            '--github-app-config', '/path/to/config.yaml'
        ])
        
        assert config.org == 'test-org'
        assert config.github_app_config == '/path/to/config.yaml'
    
    def test_github_client_integration(self):
        """Test GitHub client integration with GitHub App auth."""
        # This would require actual credentials for full testing
        # For now, test the constructor accepts the parameters
        
        import sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        
        from github_ioc_scanner.github_client import GitHubClient
        
        # Should not raise an exception
        client = GitHubClient(
            token="test_token",
            github_app_config="/path/to/config.yaml",
            org="test-org"
        )
        
        assert client.token == "test_token"
        assert client.org == "test-org"


if __name__ == "__main__":
    pytest.main([__file__])