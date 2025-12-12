"""Custom exceptions for the GitHub IOC Scanner."""

from typing import Optional


class GitHubIOCScannerError(Exception):
    """Base exception for all GitHub IOC Scanner errors."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        """
        Initialize the exception.
        
        Args:
            message: Human-readable error message
            cause: Optional underlying exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.cause = cause
    
    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.cause:
            return f"{self.message} (caused by: {self.cause})"
        return self.message


class AuthenticationError(GitHubIOCScannerError):
    """Raised when GitHub authentication fails."""
    
    def __init__(self, message: str = "GitHub authentication failed", cause: Optional[Exception] = None):
        super().__init__(message, cause)


class NetworkError(GitHubIOCScannerError):
    """Raised when network operations fail."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message, cause)


class RateLimitError(GitHubIOCScannerError):
    """Raised when GitHub API rate limits are exceeded."""
    
    def __init__(self, message: str, reset_time: Optional[int] = None, cause: Optional[Exception] = None):
        super().__init__(message, cause)
        self.reset_time = reset_time


class APIError(GitHubIOCScannerError):
    """Raised when GitHub API returns an error response."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, cause: Optional[Exception] = None):
        super().__init__(message, cause)
        self.status_code = status_code


class ConfigurationError(GitHubIOCScannerError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message, cause)


class IOCLoaderError(GitHubIOCScannerError):
    """Base exception for IOC loader errors."""
    
    def __init__(self, message: str, source_file: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(message, cause)
        self.source_file = source_file


class IOCDirectoryNotFoundError(IOCLoaderError):
    """Raised when the IOC definitions directory is not found."""
    
    def __init__(self, directory_path: str, cause: Optional[Exception] = None):
        message = f"IOC definitions directory not found: {directory_path}"
        super().__init__(message, cause=cause)
        self.directory_path = directory_path


class IOCFileError(IOCLoaderError):
    """Raised when an IOC definition file cannot be loaded or parsed."""
    
    def __init__(self, message: str, source_file: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(message, source_file, cause)


class ParsingError(GitHubIOCScannerError):
    """Base exception for file parsing errors."""
    
    def __init__(self, message: str, file_path: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(message, cause)
        self.file_path = file_path


class UnsupportedFileFormatError(ParsingError):
    """Raised when a file format is not supported by any parser."""
    
    def __init__(self, file_path: str, cause: Optional[Exception] = None):
        message = f"Unsupported file format: {file_path}"
        super().__init__(message, file_path, cause)


class MalformedFileError(ParsingError):
    """Raised when a file is malformed and cannot be parsed."""
    
    def __init__(self, message: str, file_path: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(message, file_path, cause)


class CacheError(GitHubIOCScannerError):
    """Base exception for cache-related errors."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message, cause)


class CacheInitializationError(CacheError):
    """Raised when cache initialization fails."""
    
    def __init__(self, cache_path: str, cause: Optional[Exception] = None):
        message = f"Failed to initialize cache at {cache_path}"
        super().__init__(message, cause)
        self.cache_path = cache_path


class CacheOperationError(CacheError):
    """Raised when a cache operation fails."""
    
    def __init__(self, operation: str, cause: Optional[Exception] = None):
        message = f"Cache operation failed: {operation}"
        super().__init__(message, cause)
        self.operation = operation


class ScanError(GitHubIOCScannerError):
    """Base exception for scanning operation errors."""
    
    def __init__(self, message: str, repository: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(message, cause)
        self.repository = repository


class RepositoryNotFoundError(ScanError):
    """Raised when a repository cannot be found or accessed."""
    
    def __init__(self, repository: str, cause: Optional[Exception] = None):
        message = f"Repository not found or inaccessible: {repository}"
        super().__init__(message, repository, cause)


class OrganizationNotFoundError(ScanError):
    """Raised when an organization cannot be found or accessed."""
    
    def __init__(self, organization: str, cause: Optional[Exception] = None):
        message = f"Organization not found or inaccessible: {organization}"
        super().__init__(message, cause=cause)
        self.organization = organization


class TeamNotFoundError(ScanError):
    """Raised when a team cannot be found or accessed."""
    
    def __init__(self, organization: str, team: str, cause: Optional[Exception] = None):
        message = f"Team not found or inaccessible: {organization}/{team}"
        super().__init__(message, cause=cause)
        self.organization = organization
        self.team = team


class ValidationError(GitHubIOCScannerError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(message, cause)
        self.field = field


class BatchProcessingError(GitHubIOCScannerError):
    """Raised when batch processing operations fail."""
    
    def __init__(self, message: str, batch_id: Optional[str] = None, cause: Optional[Exception] = None):
        super().__init__(message, cause)
        self.batch_id = batch_id


def wrap_exception(exc: Exception, message: str, exception_class: type = GitHubIOCScannerError) -> GitHubIOCScannerError:
    """
    Wrap a generic exception in a more specific scanner exception.
    
    Args:
        exc: Original exception to wrap
        message: Descriptive message for the new exception
        exception_class: Type of exception to create
        
    Returns:
        New exception instance with the original as the cause
    """
    if isinstance(exc, GitHubIOCScannerError):
        return exc
    
    return exception_class(message, cause=exc)


def format_error_message(exc: Exception, include_cause: bool = True) -> str:
    """
    Format an exception into a user-friendly error message.
    
    Args:
        exc: Exception to format
        include_cause: Whether to include the underlying cause
        
    Returns:
        Formatted error message
    """
    if isinstance(exc, GitHubIOCScannerError):
        message = exc.message
        if include_cause and exc.cause:
            message += f" (Details: {exc.cause})"
        return message
    else:
        return str(exc)


def get_error_context(exc: Exception) -> dict:
    """
    Extract context information from an exception for logging.
    
    Args:
        exc: Exception to extract context from
        
    Returns:
        Dictionary with context information
    """
    context = {
        "error_type": type(exc).__name__,
        "error_message": str(exc)
    }
    
    # Add specific context for known exception types
    if isinstance(exc, IOCFileError) and exc.source_file:
        context["source_file"] = exc.source_file
    elif isinstance(exc, ParsingError) and exc.file_path:
        context["file_path"] = exc.file_path
    elif isinstance(exc, ScanError) and exc.repository:
        context["repository"] = exc.repository
    elif isinstance(exc, APIError) and exc.status_code:
        context["status_code"] = exc.status_code
    elif isinstance(exc, RateLimitError) and exc.reset_time:
        context["reset_time"] = exc.reset_time
    elif isinstance(exc, ValidationError) and exc.field:
        context["field"] = exc.field
    
    return context