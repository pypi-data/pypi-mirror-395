"""
Test that empty repository errors are properly suppressed from normal output.
"""

import pytest
from src.github_ioc_scanner.error_message_formatter import ErrorMessageFormatter


class TestEmptyRepositoryLogging:
    """Test that empty repository errors are handled appropriately."""
    
    def test_empty_repository_error_suppression(self):
        """Test that empty repository errors are suppressed."""
        formatter = ErrorMessageFormatter()
        
        # Test various forms of normal repository state errors
        normal_repo_errors = [
            Exception("Git Repository is empty."),
            Exception("HTTP 409: Git Repository is empty."),
            Exception('{"message":"Git Repository is empty.","documentation_url":"https://docs.github.com/rest/git/trees#get-a-tree","status":"409"}'),
            Exception("Repository is empty"),
            Exception("No commits found in repository"),
            Exception("Empty repository - no files to scan"),
            Exception("Path package.json in owner/repo is a directory, not a file"),
            Exception("Access denied to repository: owner/repo - may be private or restricted"),
            Exception("Access denied to repository owner/private-repo")
        ]
        
        for error in empty_repo_errors:
            should_suppress = formatter.should_suppress_error(error)
            assert should_suppress is True, f"Should suppress error: {error}"
            print(f"✅ Suppressed: {error}")
    
    def test_real_errors_not_suppressed(self):
        """Test that real errors are not suppressed."""
        formatter = ErrorMessageFormatter()
        
        # Test real errors that should still be warnings
        real_errors = [
            Exception("Authentication failed"),
            Exception("Permission denied"),
            Exception("Internal server error"),
            Exception("Invalid API response"),
            Exception("Malformed JSON data")
        ]
        
        for error in real_errors:
            should_suppress = formatter.should_suppress_error(error)
            assert should_suppress is False, f"Should NOT suppress error: {error}"
            print(f"✅ Not suppressed: {error}")
    
    def test_rate_limit_errors_still_suppressed(self):
        """Test that rate limit errors are still suppressed."""
        formatter = ErrorMessageFormatter()
        
        # Test rate limit errors
        rate_limit_errors = [
            Exception("API rate limit exceeded"),
            Exception("Rate limit hit"),
            Exception("Forbidden - rate limit"),
            Exception("Secondary rate limit exceeded")
        ]
        
        for error in rate_limit_errors:
            should_suppress = formatter.should_suppress_error(error)
            assert should_suppress is True, f"Should suppress rate limit error: {error}"
            print(f"✅ Rate limit suppressed: {error}")
    
    def test_network_errors_still_suppressed(self):
        """Test that network errors are still suppressed."""
        formatter = ErrorMessageFormatter()
        
        # Test network errors
        network_errors = [
            Exception("Connection timeout"),
            Exception("Network unreachable"),
            Exception("Connection refused")
        ]
        
        for error in network_errors:
            should_suppress = formatter.should_suppress_error(error)
            assert should_suppress is True, f"Should suppress network error: {error}"
            print(f"✅ Network error suppressed: {error}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])