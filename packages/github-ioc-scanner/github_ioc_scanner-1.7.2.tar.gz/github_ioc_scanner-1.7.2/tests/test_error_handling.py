"""Tests for error handling and logging functionality."""

import pytest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.github_ioc_scanner.exceptions import (
    GitHubIOCScannerError,
    AuthenticationError,
    NetworkError,
    RateLimitError,
    APIError,
    ConfigurationError,
    IOCLoaderError,
    IOCDirectoryNotFoundError,
    IOCFileError,
    ParsingError,
    UnsupportedFileFormatError,
    MalformedFileError,
    CacheError,
    CacheInitializationError,
    CacheOperationError,
    ScanError,
    RepositoryNotFoundError,
    OrganizationNotFoundError,
    TeamNotFoundError,
    ValidationError,
    wrap_exception,
    format_error_message,
    get_error_context
)
from src.github_ioc_scanner.logging_config import setup_logging, get_logger
from src.github_ioc_scanner.github_client import GitHubClient
from src.github_ioc_scanner.ioc_loader import IOCLoader
from src.github_ioc_scanner.cache import CacheManager
from src.github_ioc_scanner.parsers.factory import parse_file_safely


class TestExceptions:
    """Test custom exception classes."""
    
    def test_base_exception(self):
        """Test base GitHubIOCScannerError."""
        exc = GitHubIOCScannerError("Test message")
        assert str(exc) == "Test message"
        assert exc.message == "Test message"
        assert exc.cause is None
    
    def test_exception_with_cause(self):
        """Test exception with underlying cause."""
        cause = ValueError("Original error")
        exc = GitHubIOCScannerError("Wrapped error", cause=cause)
        assert "Wrapped error" in str(exc)
        assert "Original error" in str(exc)
        assert exc.cause == cause
    
    def test_authentication_error(self):
        """Test AuthenticationError."""
        exc = AuthenticationError()
        assert "authentication failed" in str(exc).lower()
        
        exc = AuthenticationError("Custom auth message")
        assert str(exc) == "Custom auth message"
    
    def test_network_error(self):
        """Test NetworkError."""
        exc = NetworkError("Connection failed")
        assert str(exc) == "Connection failed"
    
    def test_rate_limit_error(self):
        """Test RateLimitError with reset time."""
        exc = RateLimitError("Rate limited", reset_time=1234567890)
        assert str(exc) == "Rate limited"
        assert exc.reset_time == 1234567890
    
    def test_api_error(self):
        """Test APIError with status code."""
        exc = APIError("API failed", status_code=404)
        assert str(exc) == "API failed"
        assert exc.status_code == 404
    
    def test_ioc_file_error(self):
        """Test IOCFileError with source file."""
        exc = IOCFileError("Parse failed", source_file="test.py")
        assert str(exc) == "Parse failed"
        assert exc.source_file == "test.py"
    
    def test_parsing_error(self):
        """Test ParsingError with file path."""
        exc = ParsingError("Invalid JSON", file_path="package.json")
        assert str(exc) == "Invalid JSON"
        assert exc.file_path == "package.json"
    
    def test_unsupported_file_format_error(self):
        """Test UnsupportedFileFormatError."""
        exc = UnsupportedFileFormatError("unknown.txt")
        assert "unknown.txt" in str(exc)
        assert exc.file_path == "unknown.txt"
    
    def test_cache_initialization_error(self):
        """Test CacheInitializationError."""
        exc = CacheInitializationError("/tmp/cache.db")
        assert "/tmp/cache.db" in str(exc)
        assert exc.cache_path == "/tmp/cache.db"
    
    def test_repository_not_found_error(self):
        """Test RepositoryNotFoundError."""
        exc = RepositoryNotFoundError("owner/repo")
        assert "owner/repo" in str(exc)
        assert exc.repository == "owner/repo"
    
    def test_organization_not_found_error(self):
        """Test OrganizationNotFoundError."""
        exc = OrganizationNotFoundError("myorg")
        assert "myorg" in str(exc)
        assert exc.organization == "myorg"
    
    def test_team_not_found_error(self):
        """Test TeamNotFoundError."""
        exc = TeamNotFoundError("myorg", "myteam")
        assert "myorg/myteam" in str(exc)
        assert exc.organization == "myorg"
        assert exc.team == "myteam"
    
    def test_validation_error(self):
        """Test ValidationError with field."""
        exc = ValidationError("Invalid value", field="username")
        assert str(exc) == "Invalid value"
        assert exc.field == "username"


class TestExceptionUtilities:
    """Test exception utility functions."""
    
    def test_wrap_exception_with_scanner_error(self):
        """Test wrapping an existing scanner error."""
        original = AuthenticationError("Auth failed")
        wrapped = wrap_exception(original, "Wrapper message")
        assert wrapped is original  # Should return the original
    
    def test_wrap_exception_with_generic_error(self):
        """Test wrapping a generic exception."""
        original = ValueError("Generic error")
        wrapped = wrap_exception(original, "Wrapper message")
        assert isinstance(wrapped, GitHubIOCScannerError)
        assert wrapped.cause == original
        assert "Wrapper message" in str(wrapped)
    
    def test_wrap_exception_with_custom_class(self):
        """Test wrapping with custom exception class."""
        original = ValueError("Generic error")
        wrapped = wrap_exception(original, "Network issue", NetworkError)
        assert isinstance(wrapped, NetworkError)
        assert wrapped.cause == original
    
    def test_format_error_message_scanner_error(self):
        """Test formatting scanner error message."""
        cause = ValueError("Original")
        exc = NetworkError("Network failed", cause=cause)
        
        message = format_error_message(exc, include_cause=True)
        assert "Network failed" in message
        assert "Original" in message
        
        message = format_error_message(exc, include_cause=False)
        assert "Network failed" in message
        assert "Original" not in message
    
    def test_format_error_message_generic_error(self):
        """Test formatting generic error message."""
        exc = ValueError("Generic error")
        message = format_error_message(exc)
        assert message == "Generic error"
    
    def test_get_error_context(self):
        """Test extracting error context."""
        exc = IOCFileError("Parse failed", source_file="test.py")
        context = get_error_context(exc)
        
        assert context["error_type"] == "IOCFileError"
        assert context["error_message"] == "Parse failed"
        assert context["source_file"] == "test.py"
    
    def test_get_error_context_parsing_error(self):
        """Test context extraction for parsing error."""
        exc = ParsingError("Invalid JSON", file_path="package.json")
        context = get_error_context(exc)
        
        assert context["file_path"] == "package.json"
    
    def test_get_error_context_api_error(self):
        """Test context extraction for API error."""
        exc = APIError("Not found", status_code=404)
        context = get_error_context(exc)
        
        assert context["status_code"] == 404


class TestLoggingConfiguration:
    """Test logging configuration."""
    
    def test_setup_logging_basic(self):
        """Test basic logging setup."""
        setup_logging(level="DEBUG")
        logger = get_logger("test")
        assert logger.level <= 10  # DEBUG level
    
    def test_setup_logging_with_file(self):
        """Test logging setup with file output."""
        import logging
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            tmp_path = tmp.name
            
        setup_logging(level="INFO", log_file=tmp_path)
        logger = get_logger("test")
        logger.info("Test message")
        
        # Force flush of all handlers on root logger
        root_logger = logging.getLogger()
        for handler in root_logger.handlers:
            handler.flush()
        
        # Check that file was created and contains message
        with open(tmp_path, 'r') as f:
            content = f.read()
            assert "Test message" in content
        
        # Clean up
        os.unlink(tmp_path)


class TestGitHubClientErrorHandling:
    """Test error handling in GitHub client."""
    
    @patch('src.github_ioc_scanner.github_client.httpx.Client')
    def test_authentication_error_on_401(self, mock_client_class):
        """Test authentication error on 401 response."""
        import httpx
        
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock 401 response with proper headers
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.headers = {
            "X-RateLimit-Remaining": "100",
            "X-RateLimit-Reset": "1234567890"
        }
        mock_response.text = "Unauthorized"
        
        # Create proper HTTPStatusError
        http_error = httpx.HTTPStatusError("401 Unauthorized", request=Mock(), response=mock_response)
        mock_response.raise_for_status.side_effect = http_error
        mock_client.request.return_value = mock_response
        
        with patch('os.getenv', return_value="fake_token"):
            client = GitHubClient()
            
            with pytest.raises(AuthenticationError):
                client._make_request("GET", "/test")
    
    @patch('src.github_ioc_scanner.github_client.httpx.Client')
    def test_rate_limit_error_on_403(self, mock_client_class):
        """Test rate limit error on 403 response."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock rate limit response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "API rate limit exceeded"
        mock_response.headers = {
            "X-RateLimit-Reset": "1234567890",
            "X-RateLimit-Remaining": "0"
        }
        mock_client.request.return_value = mock_response
        
        with patch('os.getenv', return_value="fake_token"):
            client = GitHubClient()
            
            with pytest.raises(RateLimitError) as exc_info:
                client._make_request("GET", "/test")
            
            assert exc_info.value.reset_time == 1234567890
    
    @patch('src.github_ioc_scanner.github_client.httpx.Client')
    def test_organization_not_found_error(self, mock_client_class):
        """Test organization not found error."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock empty response for organization repos
        mock_response = Mock()
        mock_response.data = None
        mock_response.not_modified = False
        mock_client.request.return_value = mock_response
        
        with patch('os.getenv', return_value="fake_token"):
            client = GitHubClient()
            client._make_request = Mock(return_value=mock_response)
            
            with pytest.raises(OrganizationNotFoundError):
                client.get_organization_repos("nonexistent-org")


class TestIOCLoaderErrorHandling:
    """Test error handling in IOC loader."""
    
    def test_directory_not_found_error(self):
        """Test error when issues directory doesn't exist."""
        loader = IOCLoader("nonexistent_directory")
        
        with pytest.raises(IOCDirectoryNotFoundError) as exc_info:
            loader.load_iocs()
        
        assert "nonexistent_directory" in str(exc_info.value)
    
    def test_no_python_files_error(self):
        """Test error when no Python files found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = IOCLoader(tmpdir)
            
            with pytest.raises(IOCLoaderError) as exc_info:
                loader.load_iocs()
            
            assert "No Python files found" in str(exc_info.value)
    
    def test_malformed_python_file_error(self):
        """Test error handling for malformed Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a malformed Python file
            malformed_file = Path(tmpdir) / "malformed.py"
            malformed_file.write_text("invalid python syntax !!!")
            
            loader = IOCLoader(tmpdir)
            
            with pytest.raises(IOCLoaderError):
                loader.load_iocs()
    
    def test_missing_ioc_packages_warning(self):
        """Test warning when IOC_PACKAGES is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a valid Python file without IOC_PACKAGES
            valid_file = Path(tmpdir) / "empty.py"
            valid_file.write_text("# Empty file\nprint('hello')")
            
            loader = IOCLoader(tmpdir)
            
            with pytest.raises(IOCLoaderError):
                loader.load_iocs()
    
    def test_invalid_ioc_packages_structure(self):
        """Test error for invalid IOC_PACKAGES structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file with invalid IOC_PACKAGES
            invalid_file = Path(tmpdir) / "invalid.py"
            invalid_file.write_text("IOC_PACKAGES = 'not a dict'")
            
            loader = IOCLoader(tmpdir)
            
            with pytest.raises(IOCLoaderError):
                loader.load_iocs()


class TestCacheErrorHandling:
    """Test error handling in cache manager."""
    
    def test_cache_initialization_with_invalid_path(self):
        """Test cache initialization error with invalid path."""
        # Try to create cache in a read-only location
        with pytest.raises(CacheInitializationError):
            CacheManager("/root/readonly/cache.db")
    
    def test_cache_operation_with_corrupted_database(self):
        """Test cache operations with corrupted database."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            # Create a corrupted database file
            tmp.write(b"not a sqlite database")
            tmp.flush()
            
            # This should raise CacheInitializationError
            with pytest.raises(CacheInitializationError):
                CacheManager(tmp.name)


class TestParserErrorHandling:
    """Test error handling in parsers."""
    
    def test_unsupported_file_format(self):
        """Test error for unsupported file format."""
        with pytest.raises(UnsupportedFileFormatError):
            parse_file_safely("unknown.xyz", "content")
    
    def test_malformed_json_file(self):
        """Test error for malformed JSON file."""
        with pytest.raises(ParsingError):
            parse_file_safely("package.json", "invalid json content")
    
    def test_empty_file_content(self):
        """Test handling of empty file content."""
        # This should raise a ParsingError for empty JSON
        with pytest.raises(ParsingError):
            parse_file_safely("package.json", "")


class TestScannerErrorHandling:
    """Test error handling in scanner."""
    
    def test_configuration_validation_error(self):
        """Test configuration validation errors."""
        from src.github_ioc_scanner.scanner import GitHubIOCScanner
        from src.github_ioc_scanner.models import ScanConfig
        
        # Create scanner with invalid config
        config = ScanConfig(team="myteam")  # team without org
        
        with patch('src.github_ioc_scanner.github_client.GitHubClient'):
            with patch('src.github_ioc_scanner.cache.CacheManager'):
                scanner = GitHubIOCScanner(config, Mock(), Mock())
                
                with pytest.raises(ConfigurationError):
                    scanner._validate_scan_config()
    
    def test_ioc_loader_error_propagation(self):
        """Test that IOC loader errors are properly propagated."""
        from src.github_ioc_scanner.scanner import GitHubIOCScanner
        from src.github_ioc_scanner.models import ScanConfig
        
        config = ScanConfig(org="myorg")
        
        # Mock IOC loader that raises error
        mock_ioc_loader = Mock()
        mock_ioc_loader.load_iocs.side_effect = IOCLoaderError("IOC load failed")
        
        with patch('src.github_ioc_scanner.github_client.GitHubClient'):
            with patch('src.github_ioc_scanner.cache.CacheManager'):
                scanner = GitHubIOCScanner(config, Mock(), Mock(), mock_ioc_loader)
                
                with pytest.raises(IOCLoaderError):
                    scanner.scan()


if __name__ == "__main__":
    pytest.main([__file__])