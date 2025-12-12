"""GitHub App authentication support for the GitHub IOC Scanner."""

import json
import time
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any
import logging

try:
    import jwt
    from cryptography.hazmat.primitives import serialization
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

from .exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class GitHubAppAuth:
    """Handles GitHub App authentication using JWT tokens."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize GitHub App authentication.
        
        Args:
            config_path: Path to the GitHub App configuration file
        """
        if not JWT_AVAILABLE:
            raise AuthenticationError(
                "GitHub App authentication requires 'pyjwt' and 'cryptography' packages. "
                "Install with: pip install pyjwt cryptography"
            )
        
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
        self._installation_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        
    def _find_config_file(self) -> str:
        """Find the GitHub App configuration file."""
        # Check common locations
        possible_paths = [
            "~/github/apps.yaml",
            "~/.github/apps.yaml", 
            "./github-apps.yaml",
            "./apps.yaml"
        ]
        
        for path_str in possible_paths:
            path = Path(path_str).expanduser()
            if path.exists():
                logger.debug(f"Found GitHub App config at: {path}")
                return str(path)
        
        raise AuthenticationError(
            f"GitHub App configuration file not found. Checked: {possible_paths}"
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Load GitHub App configuration from YAML file."""
        try:
            config_path = Path(self.config_path).expanduser()
            
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Navigate to the GitHub production config
            github_config = config.get('auth', {}).get('providers', {}).get('github', {}).get('production', {})
            
            if not github_config:
                raise AuthenticationError(
                    "GitHub App configuration not found in auth.providers.github.production"
                )
            
            required_fields = ['appId', 'clientId', 'clientSecret', 'privateKey']
            missing_fields = [field for field in required_fields if field not in github_config]
            
            if missing_fields:
                raise AuthenticationError(
                    f"Missing required GitHub App configuration fields: {missing_fields}"
                )
            
            logger.debug(f"Loaded GitHub App config for app ID: {github_config['appId']}")
            return github_config
            
        except FileNotFoundError:
            raise AuthenticationError(f"GitHub App configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise AuthenticationError(f"Invalid YAML in GitHub App configuration: {e}")
        except Exception as e:
            raise AuthenticationError(f"Error loading GitHub App configuration: {e}")
    
    def _create_jwt_token(self) -> str:
        """Create a JWT token for GitHub App authentication."""
        try:
            # Parse the private key
            private_key_pem = self.config['privateKey']
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode('utf-8'),
                password=None
            )
            
            # Create JWT payload
            now = int(time.time())
            payload = {
                'iat': now - 60,  # Issued at (60 seconds ago to account for clock skew)
                'exp': now + (10 * 60),  # Expires in 10 minutes
                'iss': int(self.config['appId'])  # Issuer (GitHub App ID)
            }
            
            # Create and sign the JWT
            token = jwt.encode(payload, private_key, algorithm='RS256')
            
            logger.debug("Created JWT token for GitHub App authentication")
            return token
            
        except Exception as e:
            raise AuthenticationError(f"Failed to create JWT token: {e}")
    
    def _get_installation_id(self, org: str, jwt_token: str) -> int:
        """Get the installation ID for the organization."""
        import httpx
        
        try:
            headers = {
                'Authorization': f'Bearer {jwt_token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'github-ioc-scanner'
            }
            
            # Get installations for this app
            with httpx.Client() as client:
                response = client.get(
                    'https://api.github.com/app/installations',
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                
                installations = response.json()
                
                # Find installation for the organization
                for installation in installations:
                    if installation.get('account', {}).get('login') == org:
                        installation_id = installation['id']
                        logger.debug(f"Found installation ID {installation_id} for org {org}")
                        return installation_id
                
                raise AuthenticationError(
                    f"No GitHub App installation found for organization '{org}'. "
                    f"Please install the GitHub App in the organization."
                )
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("GitHub App JWT token is invalid")
            elif e.response.status_code == 403:
                raise AuthenticationError("GitHub App does not have permission to list installations")
            else:
                raise AuthenticationError(f"Failed to get installations: {e}")
        except Exception as e:
            raise AuthenticationError(f"Error getting installation ID: {e}")
    
    def _get_installation_token(self, installation_id: int, jwt_token: str) -> tuple[str, datetime]:
        """Get an installation access token."""
        import httpx
        
        try:
            headers = {
                'Authorization': f'Bearer {jwt_token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'github-ioc-scanner'
            }
            
            with httpx.Client() as client:
                response = client.post(
                    f'https://api.github.com/app/installations/{installation_id}/access_tokens',
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                
                token_data = response.json()
                token = token_data['token']
                expires_at = datetime.fromisoformat(token_data['expires_at'].replace('Z', '+00:00'))
                
                logger.debug(f"Got installation token, expires at: {expires_at}")
                return token, expires_at
                
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("GitHub App JWT token is invalid")
            elif e.response.status_code == 404:
                raise AuthenticationError(f"Installation {installation_id} not found")
            else:
                raise AuthenticationError(f"Failed to get installation token: {e}")
        except Exception as e:
            raise AuthenticationError(f"Error getting installation token: {e}")
    
    def get_token(self, org: str) -> str:
        """Get a valid GitHub App installation token for the organization.
        
        Args:
            org: Organization name
            
        Returns:
            Valid GitHub API token
        """
        # Check if we have a valid cached token
        if (self._installation_token and 
            self._token_expires_at and 
            datetime.now().replace(tzinfo=None) < self._token_expires_at.replace(tzinfo=None) - timedelta(minutes=5)):
            logger.debug("Using cached installation token")
            return self._installation_token
        
        # Create new JWT token
        jwt_token = self._create_jwt_token()
        
        # Get installation ID for the organization
        installation_id = self._get_installation_id(org, jwt_token)
        
        # Get installation access token
        token, expires_at = self._get_installation_token(installation_id, jwt_token)
        
        # Cache the token
        self._installation_token = token
        self._token_expires_at = expires_at
        
        logger.info(f"Successfully authenticated as GitHub App for organization '{org}'")
        return token
    
    @classmethod
    def is_available(cls, config_path: Optional[str] = None) -> bool:
        """Check if GitHub App authentication is available.
        
        Args:
            config_path: Optional path to configuration file
            
        Returns:
            True if GitHub App auth is available
        """
        if not JWT_AVAILABLE:
            return False
        
        try:
            # Try to find and load config
            auth = cls(config_path)
            return True
        except AuthenticationError:
            return False
        except Exception:
            return False


def create_github_app_auth(config_path: Optional[str] = None) -> Optional[GitHubAppAuth]:
    """Create a GitHub App authentication instance if available.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        GitHubAppAuth instance or None if not available
    """
    try:
        if GitHubAppAuth.is_available(config_path):
            return GitHubAppAuth(config_path)
    except Exception as e:
        logger.debug(f"GitHub App authentication not available: {e}")
    
    return None