"""
Tests for ErrorMessageFormatter class.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock

from src.github_ioc_scanner.error_message_formatter import ErrorMessageFormatter


class TestErrorMessageFormatter:
    """Test cases for ErrorMessageFormatter."""
    
    def test_format_rate_limit_message_seconds(self):
        """Test formatting rate limit message with seconds."""
        reset_time = datetime.now() + timedelta(seconds=30)
        
        message = ErrorMessageFormatter.format_rate_limit_message(reset_time)
        
        assert "seconds" in message
        assert "Processing will resume automatically" in message
        assert "GitHub API rate limit reached" in message
        
    def test_format_rate_limit_message_minutes(self):
        """Test formatting rate limit message with minutes."""
        reset_time = datetime.now() + timedelta(minutes=5)
        
        message = ErrorMessageFormatter.format_rate_limit_message(reset_time)
        
        assert "minutes" in message
        assert "Processing will resume automatically" in message
        
    def test_format_rate_limit_message_hours(self):
        """Test formatting rate limit message with hours."""
        reset_time = datetime.now() + timedelta(hours=2, minutes=30)
        
        message = ErrorMessageFormatter.format_rate_limit_message(reset_time)
        
        assert "hours" in message and "minutes" in message
        assert "Processing will resume automatically" in message
        
    def test_format_rate_limit_message_with_repo(self):
        """Test formatting rate limit message with repository name."""
        reset_time = datetime.now() + timedelta(minutes=5)
        repo_name = "test-org/test-repo"
        
        message = ErrorMessageFormatter.format_rate_limit_message(reset_time, repo_name)
        
        assert repo_name in message
        assert "while processing" in message
        
    def test_format_progress_message_basic(self):
        """Test basic progress message formatting."""
        message = ErrorMessageFormatter.format_progress_message(50, 100)
        
        assert "Progress: 50/100 (50.0%)" in message
        
    def test_format_progress_message_with_eta(self):
        """Test progress message formatting with ETA."""
        message = ErrorMessageFormatter.format_progress_message(25, 100, "5 minutes")
        
        assert "Progress: 25/100 (25.0%)" in message
        assert "ETA: 5 minutes" in message
        
    def test_format_progress_message_zero_total(self):
        """Test progress message with zero total."""
        message = ErrorMessageFormatter.format_progress_message(0, 0)
        
        assert "Progress: 0/0 (0.0%)" in message
        
    def test_format_waiting_message_seconds(self):
        """Test waiting message with seconds."""
        message = ErrorMessageFormatter.format_waiting_message(45)
        
        assert "Waiting 45 seconds" in message
        assert "for rate limit reset" in message
        
    def test_format_waiting_message_minutes(self):
        """Test waiting message with minutes."""
        message = ErrorMessageFormatter.format_waiting_message(300)  # 5 minutes
        
        assert "Waiting 5 minutes" in message
        
    def test_format_waiting_message_hours(self):
        """Test waiting message with hours."""
        message = ErrorMessageFormatter.format_waiting_message(7800)  # 2 hours 10 minutes
        
        assert "Waiting 2 hours and 10 minutes" in message
        
    def test_should_suppress_error_rate_limit_exception(self):
        """Test suppressing rate limit exceptions."""
        # Test with exception name
        class RateLimitError(Exception):
            pass
            
        exception = RateLimitError("Rate limit exceeded")
        assert ErrorMessageFormatter.should_suppress_error(exception) is True
        
    def test_should_suppress_error_rate_limit_message(self):
        """Test suppressing exceptions with rate limit in message."""
        exception = Exception("API rate limit exceeded")
        assert ErrorMessageFormatter.should_suppress_error(exception) is True
        
        exception = Exception("Forbidden due to rate limiting")
        assert ErrorMessageFormatter.should_suppress_error(exception) is True
        
    def test_should_suppress_error_network_errors(self):
        """Test suppressing network-related errors."""
        exception = Exception("Connection timeout")
        assert ErrorMessageFormatter.should_suppress_error(exception) is True
        
        exception = Exception("Network unreachable")
        assert ErrorMessageFormatter.should_suppress_error(exception) is True
        
    def test_should_suppress_error_normal_exception(self):
        """Test not suppressing normal exceptions."""
        exception = ValueError("Invalid input")
        assert ErrorMessageFormatter.should_suppress_error(exception) is False
        
        exception = KeyError("Missing key")
        assert ErrorMessageFormatter.should_suppress_error(exception) is False
        
    def test_extract_reset_time_from_exception_with_attribute(self):
        """Test extracting reset time from exception with reset_time attribute."""
        reset_time = datetime.now() + timedelta(minutes=5)
        
        exception = Exception("Rate limit exceeded")
        exception.reset_time = reset_time
        
        extracted_time = ErrorMessageFormatter.extract_reset_time_from_exception(exception)
        assert extracted_time == reset_time
        
    def test_extract_reset_time_from_exception_with_headers(self):
        """Test extracting reset time from exception with response headers."""
        reset_timestamp = int((datetime.now() + timedelta(minutes=5)).timestamp())
        
        mock_response = Mock()
        mock_response.headers = {'X-RateLimit-Reset': str(reset_timestamp)}
        
        exception = Exception("Rate limit exceeded")
        exception.response = mock_response
        
        extracted_time = ErrorMessageFormatter.extract_reset_time_from_exception(exception)
        assert extracted_time is not None
        assert abs((extracted_time - datetime.fromtimestamp(reset_timestamp)).total_seconds()) < 1
        
    def test_extract_reset_time_from_exception_no_info(self):
        """Test extracting reset time when no information is available."""
        exception = Exception("Some error")
        
        extracted_time = ErrorMessageFormatter.extract_reset_time_from_exception(exception)
        assert extracted_time is None
        
    def test_format_technical_details_basic(self):
        """Test formatting basic technical details."""
        exception = ValueError("Invalid value")
        
        details = ErrorMessageFormatter.format_technical_details(exception)
        
        assert "Exception Type: ValueError" in details
        assert "Exception Message: Invalid value" in details
        
    def test_format_technical_details_with_response(self):
        """Test formatting technical details with HTTP response."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.headers = {
            'X-RateLimit-Remaining': '0',
            'X-RateLimit-Reset': '1234567890'
        }
        
        exception = Exception("Forbidden")
        exception.response = mock_response
        
        details = ErrorMessageFormatter.format_technical_details(exception)
        
        assert "HTTP Status: 403" in details
        assert "Rate Limit Headers:" in details
        assert "X-RateLimit-Remaining" in details