"""Tests for async GitHub client functionality."""

import asyncio
import base64
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest
import httpx

from src.github_ioc_scanner.async_github_client import AsyncGitHubClient
from src.github_ioc_scanner.batch_models import BatchRequest, BatchConfig, AsyncBatchContext, BatchResult
from src.github_ioc_scanner.models import Repository, FileContent, APIResponse
from src.github_ioc_scanner.exceptions import AuthenticationError, NetworkError


class TestAsyncGitHubClient:
    """Test AsyncGitHubClient functionality."""
    
    @pytest.fixture
    def mock_repo(self):
        """Create a mock repository."""
        return Repository(
            name="test-repo",
            full_name="owner/test-repo",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
    
    @pytest.fixture
    def client(self):
        """Create an async GitHub client with mocked token."""
        with patch.dict('os.environ', {'GITHUB_TOKEN': 'test-token'}):
            return AsyncGitHubClient()
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, client):
        """Test client initialization."""
        assert client.token == 'test-token'
        assert isinstance(client.config, BatchConfig)
        assert client.client is None  # Should be None until first use
    
    @pytest.mark.asyncio
    async def test_get_session(self, client):
        """Test getting async session."""
        session = await client._get_session()
        
        assert isinstance(session, httpx.AsyncClient)
        assert session.base_url == "https://api.github.com"
        assert "Authorization" in session.headers
        assert session.headers["Authorization"] == "Bearer test-token"
        
        # Test that same session is returned on subsequent calls
        session2 = await client._get_session()
        assert session is session2
        
        await client.close()
    
    @pytest.mark.asyncio
    async def test_get_tree_async(self, client, mock_repo):
        """Test async tree retrieval."""
        mock_response_data = {
            "tree": [
                {
                    "path": "package.json",
                    "type": "blob",
                    "sha": "abc123",
                    "size": 1024
                },
                {
                    "path": "src",
                    "type": "tree",
                    "sha": "def456"
                },
                {
                    "path": "README.md",
                    "type": "blob",
                    "sha": "ghi789",
                    "size": 512
                }
            ]
        }
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = APIResponse(
                data=mock_response_data,
                etag="test-etag",
                rate_limit_remaining=4999,
                rate_limit_reset=1234567890
            )
            
            response = await client.get_tree_async(mock_repo)
            
            assert response.data is not None
            assert len(response.data) == 2  # Only blobs, not trees
            assert response.data[0].path == "package.json"
            assert response.data[0].sha == "abc123"
            assert response.data[1].path == "README.md"
            
            mock_request.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_blob_content_async(self, client, mock_repo):
        """Test async blob content retrieval."""
        mock_blob_data = {
            "content": "eyJuYW1lIjogInRlc3QifQ==",  # base64 encoded '{"name": "test"}'
            "encoding": "base64"
        }
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = APIResponse(data=mock_blob_data)
            
            content = await client.get_blob_content_async(mock_repo, "abc123")
            
            assert content == '{"name": "test"}'
            mock_request.assert_called_once_with("GET", "/repos/owner/test-repo/git/blobs/abc123")
    
    @pytest.mark.asyncio
    async def test_get_multiple_file_contents_parallel(self, client, mock_repo):
        """Test parallel file content retrieval."""
        # Mock tree response
        mock_tree_data = [
            Mock(path="package.json", sha="abc123", size=1024),
            Mock(path="README.md", sha="def456", size=512)
        ]
        
        # Mock blob responses
        mock_blob_responses = {
            "abc123": '{"name": "test-package"}',
            "def456": "# Test Repository"
        }
        
        with patch.object(client, 'get_tree_async', new_callable=AsyncMock) as mock_tree:
            mock_tree.return_value = APIResponse(data=mock_tree_data)
            
            with patch.object(client, 'get_blob_content_async', new_callable=AsyncMock) as mock_blob:
                mock_blob.side_effect = lambda repo, sha: mock_blob_responses.get(sha)
                
                file_paths = ["package.json", "README.md"]
                result = await client.get_multiple_file_contents_parallel(
                    mock_repo, file_paths, max_concurrent=2
                )
                
                assert len(result) == 2
                assert "package.json" in result
                assert "README.md" in result
                assert result["package.json"].content == '{"name": "test-package"}'
                assert result["README.md"].content == "# Test Repository"
                
                # Verify tree was called once
                mock_tree.assert_called_once_with(mock_repo)
                
                # Verify blob was called for each file
                assert mock_blob.call_count == 2
    
    @pytest.mark.asyncio
    async def test_get_multiple_file_contents_parallel_with_missing_files(self, client, mock_repo):
        """Test parallel file content retrieval with missing files."""
        # Mock tree response with only one file
        mock_tree_data = [
            Mock(path="package.json", sha="abc123", size=1024)
        ]
        
        with patch.object(client, 'get_tree_async', new_callable=AsyncMock) as mock_tree:
            mock_tree.return_value = APIResponse(data=mock_tree_data)
            
            with patch.object(client, 'get_blob_content_async', new_callable=AsyncMock) as mock_blob:
                mock_blob.return_value = '{"name": "test-package"}'
                
                # Request both existing and non-existing files
                file_paths = ["package.json", "nonexistent.json"]
                result = await client.get_multiple_file_contents_parallel(
                    mock_repo, file_paths, max_concurrent=2
                )
                
                # Should only return the existing file
                assert len(result) == 1
                assert "package.json" in result
                assert "nonexistent.json" not in result
                
                # Verify blob was only called for existing file
                assert mock_blob.call_count == 1
    
    @pytest.mark.asyncio
    async def test_get_multiple_file_contents_parallel_with_errors(self, client, mock_repo):
        """Test parallel file content retrieval with blob fetch errors."""
        from src.github_ioc_scanner.exceptions import NetworkError
        
        # Mock tree response
        mock_tree_data = [
            Mock(path="package.json", sha="abc123", size=1024),
            Mock(path="README.md", sha="def456", size=512)
        ]
        
        async def mock_blob_side_effect(repo, sha):
            if sha == "abc123":
                return '{"name": "test-package"}'
            else:
                raise NetworkError("Network error")
        
        with patch.object(client, 'get_tree_async', new_callable=AsyncMock) as mock_tree:
            mock_tree.return_value = APIResponse(data=mock_tree_data)
            
            with patch.object(client, 'get_blob_content_async', new_callable=AsyncMock) as mock_blob:
                mock_blob.side_effect = mock_blob_side_effect
                
                # Mock sleep to avoid actual delays in tests
                with patch('asyncio.sleep', new_callable=AsyncMock):
                    file_paths = ["package.json", "README.md"]
                    result = await client.get_multiple_file_contents_parallel(
                        mock_repo, file_paths, max_concurrent=2
                    )
                    
                    # Should only return the successful file
                    assert len(result) == 1
                    assert "package.json" in result
                    assert "README.md" not in result
                    
                    # Verify blob was called for each file (no retry in _fetch_blob_with_semaphore)
                    # 1 call for package.json + 1 call for README.md
                    assert mock_blob.call_count == 2
    
    @pytest.mark.asyncio
    async def test_get_multiple_file_contents_parallel_empty_input(self, client, mock_repo):
        """Test parallel file content retrieval with empty input."""
        result = await client.get_multiple_file_contents_parallel(
            mock_repo, [], max_concurrent=2
        )
        
        assert result == {}
    
    @pytest.mark.asyncio
    async def test_fetch_blob_with_semaphore_success(self, client, mock_repo):
        """Test blob fetching with semaphore - successful case."""
        from src.github_ioc_scanner.models import FileInfo
        
        file_info = FileInfo(path="test.json", sha="abc123", size=100)
        semaphore = asyncio.Semaphore(1)
        
        with patch.object(client, 'get_blob_content_async', new_callable=AsyncMock) as mock_blob:
            mock_blob.return_value = '{"test": "content"}'
            
            result = await client._fetch_blob_with_semaphore(
                semaphore, mock_repo, "test.json", file_info
            )
            
            assert result is not None
            file_path, file_content = result
            assert file_path == "test.json"
            assert file_content.content == '{"test": "content"}'
            
            # Verify blob was called once
            assert mock_blob.call_count == 1
    
    @pytest.mark.asyncio
    async def test_fetch_blob_with_semaphore_rate_limit_error(self, client, mock_repo):
        """Test blob fetching when rate limit error occurs - error is re-raised."""
        from src.github_ioc_scanner.exceptions import RateLimitError
        from src.github_ioc_scanner.models import FileInfo
        
        file_info = FileInfo(path="test.json", sha="abc123", size=100)
        semaphore = asyncio.Semaphore(1)
        
        # Always raise rate limit error
        async def mock_blob_side_effect(repo, sha):
            raise RateLimitError("Rate limit exceeded", reset_time=1234567890)
        
        with patch.object(client, 'get_blob_content_async', new_callable=AsyncMock) as mock_blob:
            mock_blob.side_effect = mock_blob_side_effect
            
            # Rate limit errors are re-raised (no retry in _fetch_blob_with_semaphore)
            with pytest.raises(RateLimitError):
                await client._fetch_blob_with_semaphore(
                    semaphore, mock_repo, "test.json", file_info
                )
            
            # Verify only one call was made (no retry in this method)
            assert mock_blob.call_count == 1
    
    @pytest.mark.asyncio
    async def test_process_batch_requests(self, client, mock_repo):
        """Test batch request processing."""
        # Create batch requests
        requests = [
            BatchRequest(repo=mock_repo, file_path="package.json"),
            BatchRequest(repo=mock_repo, file_path="README.md")
        ]
        
        # Mock file content responses
        mock_file_content = FileContent(
            content='{"name": "test"}',
            sha="abc123",
            size=15
        )
        
        with patch.object(client, 'get_file_content_async', new_callable=AsyncMock) as mock_get_file:
            mock_get_file.return_value = APIResponse(data=mock_file_content)
            
            results = await client.process_batch_requests(requests)
            
            assert len(results) == 2
            assert all(result.success for result in results)
            assert all(result.content == mock_file_content for result in results)
            
            # Verify get_file_content_async was called for each request
            assert mock_get_file.call_count == 2
    
    @pytest.mark.asyncio
    async def test_process_batch_requests_with_errors(self, client, mock_repo):
        """Test batch request processing with errors."""
        # Create batch requests
        requests = [
            BatchRequest(repo=mock_repo, file_path="package.json"),
            BatchRequest(repo=mock_repo, file_path="nonexistent.json")
        ]
        
        mock_file_content = FileContent(
            content='{"name": "test"}',
            sha="abc123",
            size=15
        )
        
        async def mock_get_file_side_effect(repo, path, etag=None):
            if path == "package.json":
                return APIResponse(data=mock_file_content)
            else:
                raise NetworkError("File not found")
        
        with patch.object(client, 'get_file_content_async', new_callable=AsyncMock) as mock_get_file:
            mock_get_file.side_effect = mock_get_file_side_effect
            
            results = await client.process_batch_requests(requests)
            
            assert len(results) == 2
            assert results[0].success is True
            assert results[0].content == mock_file_content
            assert results[1].success is False
            assert isinstance(results[1].error, NetworkError)
    
    @pytest.mark.asyncio
    async def test_context_manager(self, client):
        """Test async context manager functionality."""
        async with client as c:
            assert c is client
            session = await c._get_session()
            assert isinstance(session, httpx.AsyncClient)
        
        # Client should be closed after context exit
        assert client.client.is_closed
    
    @pytest.mark.asyncio
    async def test_close(self, client):
        """Test client close functionality."""
        # Get session to initialize client
        await client._get_session()
        assert client.client is not None
        assert not client.client.is_closed
        
        # Close client
        await client.close()
        assert client.client.is_closed
    
    @pytest.mark.asyncio
    async def test_batch_context_integration(self, client, mock_repo):
        """Test integration with AsyncBatchContext."""
        context = AsyncBatchContext(
            semaphore=asyncio.Semaphore(2),
            rate_limit_remaining=1000
        )
        
        requests = [
            BatchRequest(repo=mock_repo, file_path="package.json"),
            BatchRequest(repo=mock_repo, file_path="README.md")
        ]
        
        mock_file_content = FileContent(
            content='{"name": "test"}',
            sha="abc123",
            size=15
        )
        
        with patch.object(client, 'get_file_content_async', new_callable=AsyncMock) as mock_get_file:
            mock_get_file.return_value = APIResponse(data=mock_file_content)
            
            results = await client.process_batch_requests(requests, context)
            
            assert len(results) == 2
            assert all(result.success for result in results)
            
            # Verify semaphore was used (indirectly through successful execution)
            assert mock_get_file.call_count == 2
    
    @pytest.mark.asyncio
    async def test_get_cross_repo_file_contents(self, client):
        """Test cross-repository file content retrieval."""
        from src.github_ioc_scanner.models import Repository
        from datetime import datetime
        
        # Create mock repositories
        repo1 = Repository(
            name="repo1",
            full_name="owner/repo1",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        repo2 = Repository(
            name="repo2", 
            full_name="owner/repo2",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        repo_files = {
            "owner/repo1": (repo1, ["package.json", "README.md"]),
            "owner/repo2": (repo2, ["requirements.txt", "setup.py"])
        }
        
        # Mock file contents for each repository
        mock_repo1_contents = {
            "package.json": FileContent(content='{"name": "repo1"}', sha="abc123", size=20),
            "README.md": FileContent(content="# Repo 1", sha="def456", size=8)
        }
        
        mock_repo2_contents = {
            "requirements.txt": FileContent(content="requests==2.25.1", sha="ghi789", size=16),
            "setup.py": FileContent(content="from setuptools import setup", sha="jkl012", size=26)
        }
        
        async def mock_get_multiple_files(repo, file_paths, max_concurrent=None):
            if repo.full_name == "owner/repo1":
                return {path: mock_repo1_contents[path] for path in file_paths if path in mock_repo1_contents}
            elif repo.full_name == "owner/repo2":
                return {path: mock_repo2_contents[path] for path in file_paths if path in mock_repo2_contents}
            return {}
        
        with patch.object(client, 'get_multiple_file_contents_parallel', new_callable=AsyncMock) as mock_get_files:
            mock_get_files.side_effect = mock_get_multiple_files
            
            result = await client.get_cross_repo_file_contents(repo_files, max_concurrent=2)
            
            assert len(result) == 2
            assert "owner/repo1" in result
            assert "owner/repo2" in result
            
            # Verify repo1 contents
            repo1_contents = result["owner/repo1"]
            assert len(repo1_contents) == 2
            assert "package.json" in repo1_contents
            assert "README.md" in repo1_contents
            assert repo1_contents["package.json"].content == '{"name": "repo1"}'
            
            # Verify repo2 contents
            repo2_contents = result["owner/repo2"]
            assert len(repo2_contents) == 2
            assert "requirements.txt" in repo2_contents
            assert "setup.py" in repo2_contents
            assert repo2_contents["requirements.txt"].content == "requests==2.25.1"
            
            # Verify both repositories were processed
            assert mock_get_files.call_count == 2
    
    @pytest.mark.asyncio
    async def test_process_cross_repo_batch_requests(self, client):
        """Test cross-repository batch request processing."""
        from src.github_ioc_scanner.models import Repository
        from datetime import datetime
        
        # Create mock repositories
        repo1 = Repository(
            name="repo1",
            full_name="owner/repo1", 
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        repo2 = Repository(
            name="repo2",
            full_name="owner/repo2",
            archived=False, 
            default_branch="main",
            updated_at=datetime.now()
        )
        
        # Create batch requests
        requests = [
            BatchRequest(repo=repo1, file_path="package.json"),
            BatchRequest(repo=repo1, file_path="README.md"),
            BatchRequest(repo=repo2, file_path="requirements.txt"),
            BatchRequest(repo=repo2, file_path="setup.py")
        ]
        
        # Mock successful batch results
        mock_file_content = FileContent(
            content='{"test": "content"}',
            sha="abc123",
            size=20
        )
        
        async def mock_process_batch(batch_requests, context=None):
            results = []
            for request in batch_requests:
                results.append(BatchResult(
                    request=request,
                    content=mock_file_content,
                    processing_time=0.1
                ))
            return results
        
        with patch.object(client, 'process_batch_requests', new_callable=AsyncMock) as mock_process:
            mock_process.side_effect = mock_process_batch
            
            result = await client.process_cross_repo_batch_requests(requests)
            
            assert len(result) == 2
            assert "owner/repo1" in result
            assert "owner/repo2" in result
            
            # Verify repo1 results
            repo1_results = result["owner/repo1"]
            assert len(repo1_results) == 2
            assert all(r.success for r in repo1_results)
            
            # Verify repo2 results  
            repo2_results = result["owner/repo2"]
            assert len(repo2_results) == 2
            assert all(r.success for r in repo2_results)
            
            # Verify batch processing was called for each repository
            assert mock_process.call_count == 2
    
    @pytest.mark.asyncio
    async def test_get_cross_repo_file_contents_empty_input(self, client):
        """Test cross-repository file content retrieval with empty input."""
        result = await client.get_cross_repo_file_contents({})
        assert result == {}
    
    @pytest.mark.asyncio
    async def test_get_cross_repo_file_contents_with_errors(self, client):
        """Test cross-repository file content retrieval with repository errors."""
        from src.github_ioc_scanner.models import Repository
        from src.github_ioc_scanner.exceptions import NetworkError
        from datetime import datetime
        
        # Create mock repositories
        repo1 = Repository(
            name="repo1",
            full_name="owner/repo1",
            archived=False,
            default_branch="main", 
            updated_at=datetime.now()
        )
        
        repo2 = Repository(
            name="repo2",
            full_name="owner/repo2",
            archived=False,
            default_branch="main",
            updated_at=datetime.now()
        )
        
        repo_files = {
            "owner/repo1": (repo1, ["package.json"]),
            "owner/repo2": (repo2, ["requirements.txt"])
        }
        
        async def mock_get_multiple_files_with_error(repo, file_paths, max_concurrent=None):
            if repo.full_name == "owner/repo1":
                return {"package.json": FileContent(content='{"name": "repo1"}', sha="abc123", size=20)}
            else:
                raise NetworkError("Network error for repo2")
        
        with patch.object(client, 'get_multiple_file_contents_parallel', new_callable=AsyncMock) as mock_get_files:
            mock_get_files.side_effect = mock_get_multiple_files_with_error
            
            result = await client.get_cross_repo_file_contents(repo_files, max_concurrent=2)
            
            assert len(result) == 2
            assert "owner/repo1" in result
            assert "owner/repo2" in result
            
            # Verify successful repo
            assert len(result["owner/repo1"]) == 1
            assert "package.json" in result["owner/repo1"]
            
            # Verify failed repo returns empty dict
            assert len(result["owner/repo2"]) == 0
    
    @pytest.mark.asyncio
    async def test_stream_large_file_content_small_file(self, client, mock_repo):
        """Test streaming for small files (should return content directly)."""
        # Mock small file response
        mock_file_data = {
            "content": "eyJuYW1lIjogInRlc3QifQ==",  # base64 encoded '{"name": "test"}'
            "size": 100,  # Small file
            "sha": "abc123"
        }
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = APIResponse(data=mock_file_data)
            
            chunks = []
            async for chunk in client.stream_large_file_content(mock_repo, "small.json"):
                chunks.append(chunk)
            
            # Should return content in one chunk for small files
            assert len(chunks) == 1
            assert chunks[0] == '{"name": "test"}'
    
    @pytest.mark.asyncio
    async def test_stream_large_file_content_large_file(self, client, mock_repo):
        """Test streaming for large files (above threshold)."""
        # File size must be above stream_large_files_threshold (default 1MB)
        # to trigger streaming behavior
        mock_file_data = {
            "size": 2 * 1024 * 1024,  # 2MB - above 1MB threshold
            "sha": "def456"
        }
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = APIResponse(data=mock_file_data)
            
            # Mock _stream_blob_content as an async generator
            async def mock_stream_generator(repo, sha, chunk_size):
                yield "chunk1"
                yield "chunk2"
                yield "chunk3"
            
            with patch.object(client, '_stream_blob_content', side_effect=mock_stream_generator) as mock_stream:
                chunks = []
                async for chunk in client.stream_large_file_content(mock_repo, "large.json", chunk_size=1024):
                    chunks.append(chunk)
                
                # Should return content in multiple chunks
                assert len(chunks) == 3
                assert chunks == ["chunk1", "chunk2", "chunk3"]
                
                # Verify streaming was called
                mock_stream.assert_called_once_with(mock_repo, "def456", 1024)
    
    @pytest.mark.asyncio
    async def test_get_file_content_chunked_small_file(self, client, mock_repo):
        """Test chunked file content retrieval for small files."""
        # Mock file metadata response (small file below threshold)
        mock_file_data = {
            "size": 15,  # Small file
            "sha": "abc123",
            "content": base64.b64encode(b'{"name": "test"}').decode()
        }
        
        mock_file_content = FileContent(
            content='{"name": "test"}',
            sha="abc123",
            size=15
        )
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = APIResponse(data=mock_file_data)
            
            with patch.object(client, 'get_file_content_async', new_callable=AsyncMock) as mock_get_file:
                mock_get_file.return_value = APIResponse(data=mock_file_content)
                
                result = await client.get_file_content_chunked(mock_repo, "small.json")
                
                assert result is not None
                assert result.content == '{"name": "test"}'
                assert result.size == 15
                
                # Should use regular method for small files
                mock_get_file.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_file_content_chunked_large_file(self, client, mock_repo):
        """Test chunked file content retrieval for large files."""
        large_content = '{"name": "test", "data": "' + 'x' * 2000 + '"}'
        
        # Mock file metadata response - must be above stream_large_files_threshold (1MB)
        mock_file_data = {
            "size": 2 * 1024 * 1024,  # 2MB - above threshold
            "sha": "def456"
        }
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = APIResponse(data=mock_file_data)
            
            # Mock streaming as an async generator
            async def mock_stream_generator(repo, file_path, chunk_size=8192):
                content = large_content
                for i in range(0, len(content), chunk_size):
                    yield content[i:i + chunk_size]
            
            with patch.object(client, 'stream_large_file_content', side_effect=mock_stream_generator) as mock_stream:
                result = await client.get_file_content_chunked(mock_repo, "large.json")
                
                assert result is not None
                assert result.content == large_content
                assert result.size == 2 * 1024 * 1024
                
                # Should use streaming for large files
                mock_stream.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_file_content_chunked_too_large(self, client, mock_repo):
        """Test chunked file content retrieval for files that are too large."""
        # Mock very large file metadata - larger than max_memory_usage_mb (500MB default)
        mock_file_data = {
            "size": 600 * 1024 * 1024,  # 600MB - larger than default max (500MB)
            "sha": "huge123"
        }
        
        with patch.object(client, '_make_request', new_callable=AsyncMock) as mock_request:
            mock_request.return_value = APIResponse(data=mock_file_data)
            
            result = await client.get_file_content_chunked(mock_repo, "huge.json")
            
            # Should return None for files that are too large
            assert result is None