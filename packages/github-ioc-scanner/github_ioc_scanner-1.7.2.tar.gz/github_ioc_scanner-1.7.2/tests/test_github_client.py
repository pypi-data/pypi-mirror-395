"""Tests for the GitHub API client."""

import json
import os
import subprocess
import time
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

import httpx
import pytest

from github_ioc_scanner.github_client import GitHubClient
from github_ioc_scanner.exceptions import AuthenticationError, RateLimitError
from github_ioc_scanner.models import APIResponse, FileContent, FileInfo, Repository


class TestGitHubClientAuth:
    """Test GitHub client authentication."""

    def test_init_with_token(self):
        """Test initialization with explicit token."""
        client = GitHubClient(token="test-token")
        assert client.token == "test-token"
        assert "Bearer test-token" in client.client.headers["Authorization"]

    @patch.dict(os.environ, {"GITHUB_TOKEN": "env-token"})
    def test_discover_token_from_env(self):
        """Test token discovery from environment variable."""
        client = GitHubClient()
        assert client.token == "env-token"

    @patch.dict(os.environ, {}, clear=True)
    @patch("subprocess.run")
    def test_discover_token_from_gh_cli(self, mock_run):
        """Test token discovery from gh CLI."""
        mock_run.return_value = Mock(stdout="cli-token\n", returncode=0)
        client = GitHubClient()
        assert client.token == "cli-token"
        mock_run.assert_called_once_with(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )

    @patch.dict(os.environ, {}, clear=True)
    @patch("subprocess.run")
    def test_discover_token_failure(self, mock_run):
        """Test token discovery failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "gh")
        with pytest.raises(AuthenticationError, match="No GitHub token found"):
            GitHubClient()


class TestGitHubClientRequests:
    """Test GitHub client HTTP requests."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return GitHubClient(token="test-token")

    @pytest.fixture
    def mock_response(self):
        """Create a mock HTTP response."""
        response = Mock(spec=httpx.Response)
        response.status_code = 200
        response.headers = {
            "ETag": '"test-etag"',
            "X-RateLimit-Remaining": "4999",
            "X-RateLimit-Reset": str(int(time.time()) + 3600),
        }
        response.json.return_value = {"test": "data"}
        response.content = b'{"test": "data"}'
        response.text = '{"test": "data"}'
        return response

    def test_make_request_success(self, client, mock_response):
        """Test successful API request."""
        with patch.object(client.client, "request", return_value=mock_response):
            response = client._make_request("GET", "/test")
            
        assert response.data == {"test": "data"}
        assert response.etag == '"test-etag"'
        assert not response.not_modified
        assert response.rate_limit_remaining == 4999

    def test_make_request_with_etag(self, client, mock_response):
        """Test request with ETag header."""
        with patch.object(client.client, "request", return_value=mock_response) as mock_request:
            client._make_request("GET", "/test", etag='"existing-etag"')
            
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs["headers"]["If-None-Match"] == '"existing-etag"'

    def test_make_request_not_modified(self, client):
        """Test 304 Not Modified response."""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 304
        mock_response.headers = {
            "X-RateLimit-Remaining": "4999",
            "X-RateLimit-Reset": str(int(time.time()) + 3600),
        }
        
        with patch.object(client.client, "request", return_value=mock_response):
            response = client._make_request("GET", "/test", etag='"existing-etag"')
            
        assert response.data is None
        assert response.etag == '"existing-etag"'
        assert response.not_modified

    def test_make_request_rate_limit(self, client):
        """Test rate limit handling - should raise RateLimitError."""
        # Rate limited response
        rate_limit_response = Mock(spec=httpx.Response)
        rate_limit_response.status_code = 403
        rate_limit_response.text = "rate limit exceeded"
        rate_limit_response.headers = {
            "X-RateLimit-Reset": str(int(time.time()) + 1),  # Reset in 1 second
            "X-RateLimit-Remaining": "0",
        }
        
        with patch.object(client.client, "request", return_value=rate_limit_response):
            with pytest.raises(RateLimitError, match="rate limit exceeded"):
                client._make_request("GET", "/test")

    def test_make_request_auth_error(self, client):
        """Test authentication error handling."""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "401 Unauthorized", request=Mock(), response=mock_response
        )
        
        with patch.object(client.client, "request", return_value=mock_response):
            with pytest.raises(AuthenticationError, match="Invalid GitHub token"):
                client._make_request("GET", "/test")

    def test_make_request_not_found(self, client):
        """Test 404 Not Found handling."""
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404 Not Found", request=Mock(), response=mock_response
        )
        
        with patch.object(client.client, "request", return_value=mock_response):
            response = client._make_request("GET", "/test")
            
        assert response.data is None


class TestGitHubClientMethods:
    """Test GitHub client API methods."""

    @pytest.fixture
    def client(self):
        """Create a test client."""
        return GitHubClient(token="test-token")

    @pytest.fixture
    def sample_repo_data(self):
        """Sample repository data from GitHub API."""
        return {
            "name": "test-repo",
            "full_name": "test-org/test-repo",
            "archived": False,
            "default_branch": "main",
            "updated_at": "2023-01-01T00:00:00Z",
        }

    def test_get_organization_repos(self, client, sample_repo_data):
        """Test getting organization repositories."""
        mock_response = APIResponse(
            data=[sample_repo_data],
            etag='"test-etag"',
            rate_limit_remaining=4999,
            rate_limit_reset=int(time.time()) + 3600,
        )
        
        with patch.object(client, "_make_request", return_value=mock_response):
            response = client.get_organization_repos("test-org")
            
        assert len(response.data) == 1
        repo = response.data[0]
        assert isinstance(repo, Repository)
        assert repo.name == "test-repo"
        assert repo.full_name == "test-org/test-repo"
        assert not repo.archived

    def test_get_organization_repos_exclude_archived(self, client):
        """Test excluding archived repositories."""
        archived_repo = {
            "name": "archived-repo",
            "full_name": "test-org/archived-repo",
            "archived": True,
            "default_branch": "main",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        active_repo = {
            "name": "active-repo",
            "full_name": "test-org/active-repo",
            "archived": False,
            "default_branch": "main",
            "updated_at": "2023-01-01T00:00:00Z",
        }
        
        mock_response = APIResponse(
            data=[archived_repo, active_repo],
            etag='"test-etag"',
        )
        
        with patch.object(client, "_make_request", return_value=mock_response):
            response = client.get_organization_repos("test-org", include_archived=False)
            
        assert len(response.data) == 1
        assert response.data[0].name == "active-repo"

    def test_get_team_repos(self, client, sample_repo_data):
        """Test getting team repositories."""
        mock_response = APIResponse(
            data=[sample_repo_data],
            etag='"test-etag"',
        )
        
        with patch.object(client, "_make_request", return_value=mock_response):
            response = client.get_team_repos("test-org", "test-team")
            
        assert len(response.data) == 1
        repo = response.data[0]
        assert isinstance(repo, Repository)
        assert repo.name == "test-repo"

    def test_search_files_code_api_success(self, client):
        """Test file search functionality using Code Search API."""
        search_data = {
            "items": [
                {
                    "path": "package.json",
                    "sha": "abc123",
                    "size": 1024,
                },
                {
                    "path": "src/package.json",
                    "sha": "def456",
                    "size": 512,
                },
            ]
        }
        
        mock_response = APIResponse(data=search_data)
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        with patch.object(client, "_search_files_code_api", return_value=[
            FileInfo(path="package.json", sha="abc123", size=1024),
            FileInfo(path="src/package.json", sha="def456", size=512),
        ]):
            files = client.search_files(repo, ["package.json"])
            
        assert len(files) == 2
        assert all(isinstance(f, FileInfo) for f in files)
        assert files[0].path == "package.json"
        assert files[0].sha == "abc123"

    def test_search_files_tree_api_fallback(self, client):
        """Test file search fallback to Tree API when Code Search fails."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        tree_files = [
            FileInfo(path="package.json", sha="abc123", size=1024),
            FileInfo(path="src/package.json", sha="def456", size=512),
            FileInfo(path="README.md", sha="ghi789", size=256),
        ]
        
        with patch.object(client, "_search_files_code_api", side_effect=Exception("Code Search failed")):
            with patch.object(client, "_search_files_tree_api", return_value=tree_files[:2]):
                files = client.search_files(repo, ["package.json"])
                
        assert len(files) == 2
        assert files[0].path == "package.json"

    def test_search_files_fast_mode(self, client):
        """Test file search in fast mode (root-level only)."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        # Mock Tree API response with both root and nested files
        tree_response = APIResponse(data=[
            FileInfo(path="package.json", sha="abc123", size=1024),
            FileInfo(path="src/package.json", sha="def456", size=512),
        ])
        
        with patch.object(client, "_search_files_code_api", return_value=[]):
            with patch.object(client, "get_tree", return_value=tree_response):
                files = client.search_files(repo, ["package.json"], fast_mode=True)
                
        # Should only return root-level files in fast mode
        assert len(files) == 1
        assert files[0].path == "package.json"

    def test_matches_pattern(self, client):
        """Test pattern matching functionality."""
        # Exact match
        assert client._matches_pattern("package.json", "package.json")
        assert not client._matches_pattern("package.json", "yarn.lock")
        
        # Wildcard match
        assert client._matches_pattern("package.json", "package.*")
        assert client._matches_pattern("yarn.lock", "*.lock")
        assert not client._matches_pattern("README.md", "*.lock")

    def test_search_files_code_api_method(self, client):
        """Test the Code Search API method directly."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        search_data = {
            "items": [
                {
                    "path": "package.json",
                    "sha": "abc123",
                    "size": 1024,
                },
            ]
        }
        
        mock_response = APIResponse(data=search_data)
        
        with patch.object(client, "_make_request", return_value=mock_response):
            files = client._search_files_code_api(repo, ["package.json"])
            
        assert len(files) == 1
        assert files[0].path == "package.json"
        assert files[0].sha == "abc123"

    def test_search_files_tree_api_method(self, client):
        """Test the Tree API method directly."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        tree_files = [
            FileInfo(path="package.json", sha="abc123", size=1024),
            FileInfo(path="src/package.json", sha="def456", size=512),
            FileInfo(path="yarn.lock", sha="ghi789", size=2048),
            FileInfo(path="README.md", sha="jkl012", size=256),
        ]
        
        tree_response = APIResponse(data=tree_files)
        
        with patch.object(client, "get_tree", return_value=tree_response):
            # Test normal mode
            files = client._search_files_tree_api(repo, ["package.json", "yarn.lock"], fast_mode=False)
            
        assert len(files) == 3  # Both package.json files + yarn.lock
        paths = [f.path for f in files]
        assert "package.json" in paths
        assert "src/package.json" in paths
        assert "yarn.lock" in paths

    def test_search_files_tree_api_fast_mode(self, client):
        """Test Tree API method in fast mode."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        tree_files = [
            FileInfo(path="package.json", sha="abc123", size=1024),
            FileInfo(path="src/package.json", sha="def456", size=512),
            FileInfo(path="yarn.lock", sha="ghi789", size=2048),
        ]
        
        tree_response = APIResponse(data=tree_files)
        
        with patch.object(client, "get_tree", return_value=tree_response):
            # Test fast mode - should only return root-level files
            files = client._search_files_tree_api(repo, ["package.json", "yarn.lock"], fast_mode=True)
            
        assert len(files) == 2  # Only root-level files
        paths = [f.path for f in files]
        assert "package.json" in paths
        assert "yarn.lock" in paths
        assert "src/package.json" not in paths

    def test_search_files_empty_tree(self, client):
        """Test file search with empty tree response."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        with patch.object(client, "_search_files_code_api", return_value=[]):
            with patch.object(client, "get_tree", return_value=APIResponse(data=None)):
                files = client.search_files(repo, ["package.json"])
                
        assert files == []

    def test_search_files_code_api_pagination(self, client):
        """Test Code Search API with pagination."""
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        # Mock paginated responses
        page1_data = {
            "items": [{"path": f"file{i}.json", "sha": f"sha{i}", "size": 100} for i in range(100)]
        }
        page2_data = {
            "items": [{"path": f"file{i}.json", "sha": f"sha{i}", "size": 100} for i in range(100, 150)]
        }
        
        responses = [
            APIResponse(data=page1_data),
            APIResponse(data=page2_data),
        ]
        
        with patch.object(client, "_make_request", side_effect=responses):
            files = client._search_files_code_api(repo, ["*.json"])
            
        assert len(files) == 150

    def test_get_file_content(self, client):
        """Test getting file content."""
        file_data = {
            "content": "ewogICJuYW1lIjogInRlc3QiCn0K",  # Base64 encoded JSON
            "sha": "abc123",
            "size": 20,
        }
        
        mock_response = APIResponse(data=file_data, etag='"file-etag"')
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        with patch.object(client, "_make_request", return_value=mock_response):
            response = client.get_file_content(repo, "package.json")
            
        assert isinstance(response.data, FileContent)
        assert response.data.sha == "abc123"
        assert response.data.size == 20
        assert "test" in response.data.content  # Decoded content

    def test_get_file_content_directory(self, client):
        """Test handling directory response."""
        mock_response = APIResponse(data=[{"type": "dir"}])  # Directory listing
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        with patch.object(client, "_make_request", return_value=mock_response):
            response = client.get_file_content(repo, "src")
            
        assert response.data is None

    def test_get_tree(self, client):
        """Test getting repository tree."""
        tree_data = {
            "tree": [
                {
                    "path": "package.json",
                    "type": "blob",
                    "sha": "abc123",
                    "size": 1024,
                },
                {
                    "path": "src",
                    "type": "tree",
                    "sha": "def456",
                },
                {
                    "path": "src/index.js",
                    "type": "blob",
                    "sha": "ghi789",
                    "size": 512,
                },
            ]
        }
        
        mock_response = APIResponse(data=tree_data, etag='"tree-etag"')
        repo = Repository(
            name="test-repo",
            full_name="test-org/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now(),
        )
        
        with patch.object(client, "_make_request", return_value=mock_response):
            response = client.get_tree(repo)
            
        # Should only include blobs (files), not trees (directories)
        assert len(response.data) == 2
        assert all(isinstance(f, FileInfo) for f in response.data)
        assert response.data[0].path == "package.json"
        assert response.data[1].path == "src/index.js"

    def test_context_manager(self, client):
        """Test context manager functionality."""
        with patch.object(client, "close") as mock_close:
            with client:
                pass
            mock_close.assert_called_once()


class TestGitHubClientIntegration:
    """Integration tests for GitHub client."""

    def test_pagination_handling(self):
        """Test handling of paginated responses."""
        client = GitHubClient(token="test-token")
        
        # Mock responses for multiple pages
        page1_data = [{"name": f"repo-{i}", "full_name": f"org/repo-{i}", "archived": False, "default_branch": "main", "updated_at": "2023-01-01T00:00:00Z"} for i in range(100)]
        page2_data = [{"name": f"repo-{i}", "full_name": f"org/repo-{i}", "archived": False, "default_branch": "main", "updated_at": "2023-01-01T00:00:00Z"} for i in range(100, 150)]
        
        responses = [
            APIResponse(data=page1_data, etag='"page1-etag"'),
            APIResponse(data=page2_data, etag='"page2-etag"'),
        ]
        
        with patch.object(client, "_make_request", side_effect=responses):
            response = client.get_organization_repos("test-org")
            
        assert len(response.data) == 150

    def test_error_recovery(self):
        """Test error recovery and retry logic."""
        client = GitHubClient(token="test-token")
        
        # First call fails with network error, second succeeds
        network_error = httpx.RequestError("Network error")
        success_response = APIResponse(data=[], etag='"success-etag"')
        
        with patch.object(client, "_make_request", side_effect=[network_error, success_response]):
            # This would normally retry in a real implementation
            with pytest.raises(httpx.RequestError):
                client.get_organization_repos("test-org")