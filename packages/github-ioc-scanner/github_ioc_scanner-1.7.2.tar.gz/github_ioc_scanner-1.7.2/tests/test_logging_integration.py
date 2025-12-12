"""Integration tests for the enhanced logging system."""

import logging
import tempfile
import os
from io import StringIO
from unittest.mock import patch, MagicMock

import pytest

from src.github_ioc_scanner.logging_config import setup_logging, log_user_message, log_rate_limit_debug
from src.github_ioc_scanner.error_message_formatter import ErrorMessageFormatter
from src.github_ioc_scanner.models import ScanConfig


class TestLoggingIntegration:
    """Test the complete logging system integration."""
    
    def setup_method(self):
        """Set up test environment."""
        # Clear any existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
    
    def test_cli_logging_configuration_verbose(self):
        """Test CLI logging configuration in verbose mode."""
        config = ScanConfig(
            verbose=True,
            debug_rate_limits=True,
            show_stack_traces=False,
            suppress_rate_limit_messages=False
        )
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as log_file:
            log_file_path = log_file.name
        
        try:
            # Configure logging as CLI would
            setup_logging(
                level="INFO",
                log_file=log_file_path,
                debug_rate_limits=config.debug_rate_limits,
                suppress_stack_traces=not config.show_stack_traces,
                separate_user_messages=not config.suppress_rate_limit_messages
            )
            
            logger = logging.getLogger("test_integration")
            
            # Test various message types
            log_user_message(logger, "Rate limit reached, waiting 60 seconds...")
            log_rate_limit_debug(logger, "Detailed rate limit info: 100 requests remaining")
            logger.info("Repository scan completed")
            
            # Verify log file contains all messages
            with open(log_file_path, 'r') as f:
                log_content = f.read()
                assert "Rate limit reached, waiting 60 seconds..." in log_content
                assert "Detailed rate limit info: 100 requests remaining" in log_content
                assert "Repository scan completed" in log_content
                
        finally:
            if os.path.exists(log_file_path):
                os.unlink(log_file_path)
    
    def test_cli_logging_configuration_quiet(self):
        """Test CLI logging configuration in quiet mode."""
        config = ScanConfig(
            quiet=True,
            debug_rate_limits=False,
            show_stack_traces=False,
            suppress_rate_limit_messages=True
        )
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as log_file:
            log_file_path = log_file.name
        
        try:
            # Configure logging as CLI would
            setup_logging(
                level="CRITICAL",
                log_file=log_file_path,
                debug_rate_limits=config.debug_rate_limits,
                suppress_stack_traces=not config.show_stack_traces,
                separate_user_messages=False  # No user messages in quiet mode
            )
            
            logger = logging.getLogger("test_integration")
            
            # Test various message types
            log_user_message(logger, "This should not appear in quiet mode")
            log_rate_limit_debug(logger, "This should not appear when debug disabled")
            logger.critical("Critical error occurred")
            
            # Verify log file behavior
            with open(log_file_path, 'r') as f:
                log_content = f.read()
                assert "Critical error occurred" in log_content
                # User messages and debug messages should not appear in console
                # but may appear in log file depending on file handler configuration
                
        finally:
            if os.path.exists(log_file_path):
                os.unlink(log_file_path)
    
    def test_rate_limit_error_handling_integration(self):
        """Test complete rate limit error handling with new logging."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as log_file:
            log_file_path = log_file.name
        
        try:
            # Setup logging with error suppression
            setup_logging(
                level="ERROR",
                log_file=log_file_path,
                suppress_stack_traces=True,
                separate_user_messages=True
            )
            
            logger = logging.getLogger("test_integration")
            
            # Simulate a rate limit error
            class MockRateLimitError(Exception):
                def __init__(self, message):
                    super().__init__(message)
                    self.response = MagicMock()
                    self.response.headers = {'X-RateLimit-Reset': '1234567890'}
            
            rate_limit_error = MockRateLimitError("API rate limit exceeded")
            
            # Test error suppression
            formatter = ErrorMessageFormatter()
            should_suppress = formatter.should_suppress_error(rate_limit_error)
            assert should_suppress is True
            
            # Test user-friendly message
            from datetime import datetime
            reset_time = datetime.fromtimestamp(1234567890)
            user_message = formatter.format_rate_limit_message(reset_time)
            assert "GitHub API rate limit reached" in user_message
            assert "Processing will resume automatically" in user_message
            
            # Log the user message
            log_user_message(logger, user_message)
            
            # Verify log file contains the message
            with open(log_file_path, 'r') as f:
                log_content = f.read()
                assert "GitHub API rate limit reached" in log_content
                
        finally:
            if os.path.exists(log_file_path):
                os.unlink(log_file_path)
    
    def test_environment_variable_override(self):
        """Test that environment variables override default settings."""
        with patch.dict(os.environ, {
            'GITHUB_IOC_SCANNER_DEBUG_RATE_LIMITS': 'true',
            'GITHUB_IOC_SCANNER_SUPPRESS_STACK_TRACES': 'false'
        }):
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as log_file:
                log_file_path = log_file.name
            
            try:
                # Setup logging (should pick up environment variables)
                setup_logging(
                    level="DEBUG",
                    log_file=log_file_path,
                    debug_rate_limits=False,  # This should be overridden by env var
                    suppress_stack_traces=True  # This should be overridden by env var
                )
                
                logger = logging.getLogger("test_integration")
                
                # Test rate limit debug message (should appear due to env var)
                log_rate_limit_debug(logger, "Environment variable test message")
                
                # Test exception with stack trace (should appear due to env var)
                try:
                    raise ValueError("Test exception")
                except ValueError as e:
                    logger.error("Test error", exc_info=True)
                
                # Verify log file contains both messages
                with open(log_file_path, 'r') as f:
                    log_content = f.read()
                    assert "Environment variable test message" in log_content
                    assert "Test error" in log_content
                    assert "ValueError: Test exception" in log_content
                    
            finally:
                if os.path.exists(log_file_path):
                    os.unlink(log_file_path)


if __name__ == "__main__":
    pytest.main([__file__])