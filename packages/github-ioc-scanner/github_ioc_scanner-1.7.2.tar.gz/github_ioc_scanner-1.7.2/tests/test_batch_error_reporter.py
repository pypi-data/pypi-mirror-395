"""Tests for batch error reporting and diagnostics."""

import json
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import httpx

from src.github_ioc_scanner.batch_error_reporter import (
    BatchErrorReporter, ErrorDiagnostic, BatchErrorSummary,
    ErrorSeverity, DiagnosticLevel
)
from src.github_ioc_scanner.batch_error_handler import ErrorCategory
from src.github_ioc_scanner.batch_models import BatchRequest, BatchResult, BatchMetrics
from src.github_ioc_scanner.models import Repository
from src.github_ioc_scanner.exceptions import NetworkError, RateLimitError


@pytest.fixture
def error_reporter():
    """Create a BatchErrorReporter instance for testing."""
    return BatchErrorReporter(diagnostic_level=DiagnosticLevel.DETAILED)


@pytest.fixture
def sample_repository():
    """Create a sample repository for testing."""
    return Repository(
        name="test-repo",
        full_name="owner/test-repo",
        archived=False,
        default_branch="main",
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_request(sample_repository):
    """Create a sample batch request for testing."""
    return BatchRequest(
        repo=sample_repository,
        file_path="package.json",
        priority=5,
        estimated_size=1024
    )


@pytest.fixture
def sample_batch_results(sample_repository):
    """Create sample batch results for testing."""
    return [
        BatchResult(
            request=BatchRequest(sample_repository, "success1.json"),
            content=Mock(),
            processing_time=1.0
        ),
        BatchResult(
            request=BatchRequest(sample_repository, "success2.json"),
            content=Mock(),
            processing_time=1.5
        ),
        BatchResult(
            request=BatchRequest(sample_repository, "failed1.json"),
            error=NetworkError("Network error"),
            processing_time=0.5
        ),
        BatchResult(
            request=BatchRequest(sample_repository, "failed2.json"),
            error=httpx.HTTPStatusError(
                "Not Found",
                request=Mock(url="https://api.github.com/test"),
                response=Mock(status_code=404, reason_phrase="Not Found", headers={})
            ),
            processing_time=0.3
        )
    ]


class TestErrorDiagnostic:
    """Test ErrorDiagnostic functionality."""
    
    def test_error_diagnostic_creation(self):
        """Test creating an error diagnostic."""
        diagnostic = ErrorDiagnostic(
            error_id="test_error_1",
            timestamp=datetime.now(),
            severity=ErrorSeverity.HIGH,
            category=ErrorCategory.TRANSIENT_NETWORK,
            error_type="NetworkError",
            error_message="Connection failed",
            request_context={"file": "test.json"},
            system_context={"batch_id": "batch_1"}
        )
        
        assert diagnostic.error_id == "test_error_1"
        assert diagnostic.severity == ErrorSeverity.HIGH
        assert diagnostic.category == ErrorCategory.TRANSIENT_NETWORK
        assert diagnostic.error_type == "NetworkError"
        assert diagnostic.error_message == "Connection failed"
    
    def test_error_diagnostic_to_dict(self):
        """Test converting error diagnostic to dictionary."""
        timestamp = datetime.now()
        diagnostic = ErrorDiagnostic(
            error_id="test_error_1",
            timestamp=timestamp,
            severity=ErrorSeverity.MEDIUM,
            category=ErrorCategory.RATE_LIMIT,
            error_type="RateLimitError",
            error_message="Rate limit exceeded",
            request_context={"file": "test.json"},
            system_context={"batch_id": "batch_1"}
        )
        
        data = diagnostic.to_dict()
        
        assert data['error_id'] == "test_error_1"
        assert data['timestamp'] == timestamp.isoformat()
        assert data['severity'] == "medium"
        assert data['category'] == "rate_limit"
        assert data['error_type'] == "RateLimitError"
        assert data['error_message'] == "Rate limit exceeded"


class TestBatchErrorSummary:
    """Test BatchErrorSummary functionality."""
    
    def test_batch_summary_creation(self):
        """Test creating a batch error summary."""
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=30)
        
        summary = BatchErrorSummary(
            batch_id="test_batch_1",
            start_time=start_time,
            end_time=end_time,
            total_requests=10,
            successful_requests=7,
            failed_requests=3
        )
        
        assert summary.batch_id == "test_batch_1"
        assert summary.total_requests == 10
        assert summary.successful_requests == 7
        assert summary.failed_requests == 3
        assert summary.success_rate == 70.0
        assert summary.duration_seconds == 30.0
    
    def test_batch_summary_to_dict(self):
        """Test converting batch summary to dictionary."""
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=45)
        
        summary = BatchErrorSummary(
            batch_id="test_batch_1",
            start_time=start_time,
            end_time=end_time,
            total_requests=5,
            successful_requests=3,
            failed_requests=2
        )
        
        data = summary.to_dict()
        
        assert data['batch_id'] == "test_batch_1"
        assert data['start_time'] == start_time.isoformat()
        assert data['end_time'] == end_time.isoformat()
        assert data['success_rate'] == 60.0
        assert data['duration_seconds'] == 45.0


class TestBatchErrorReporter:
    """Test BatchErrorReporter functionality."""
    
    def test_create_error_diagnostic(self, error_reporter, sample_request):
        """Test creating error diagnostics."""
        error = NetworkError("Connection failed")
        
        diagnostic = error_reporter.create_error_diagnostic(
            error=error,
            request=sample_request,
            batch_id="test_batch",
            additional_context={"retry_count": 2}
        )
        
        assert diagnostic.error_type == "NetworkError"
        assert diagnostic.error_message == "Connection failed"
        assert diagnostic.severity == ErrorSeverity.MEDIUM
        assert diagnostic.category == ErrorCategory.TRANSIENT_NETWORK
        assert diagnostic.request_context['repository'] == "owner/test-repo"
        assert diagnostic.request_context['file_path'] == "package.json"
        assert diagnostic.system_context['batch_id'] == "test_batch"
        assert diagnostic.system_context['retry_count'] == 2
        
        # Should be stored in reporter
        assert diagnostic.error_id in error_reporter.error_diagnostics
    
    def test_determine_error_severity(self, error_reporter):
        """Test error severity determination."""
        # Test HTTP status errors
        auth_error = httpx.HTTPStatusError(
            "Unauthorized",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=401, reason_phrase="Unauthorized", headers={})
        )
        assert error_reporter._determine_error_severity(auth_error) == ErrorSeverity.CRITICAL
        
        permission_error = httpx.HTTPStatusError(
            "Forbidden",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=403, reason_phrase="Forbidden", headers={})
        )
        assert error_reporter._determine_error_severity(permission_error) == ErrorSeverity.HIGH
        
        not_found_error = httpx.HTTPStatusError(
            "Not Found",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=404, reason_phrase="Not Found", headers={})
        )
        assert error_reporter._determine_error_severity(not_found_error) == ErrorSeverity.MEDIUM
        
        server_error = httpx.HTTPStatusError(
            "Server Error",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=500, reason_phrase="Server Error", headers={})
        )
        assert error_reporter._determine_error_severity(server_error) == ErrorSeverity.HIGH
        
        rate_limit_error = httpx.HTTPStatusError(
            "Rate Limited",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=429, reason_phrase="Rate Limited", headers={})
        )
        assert error_reporter._determine_error_severity(rate_limit_error) == ErrorSeverity.MEDIUM
        
        # Test network errors
        network_error = httpx.NetworkError("Network error")
        assert error_reporter._determine_error_severity(network_error) == ErrorSeverity.MEDIUM
        
        timeout_error = httpx.TimeoutException("Timeout")
        assert error_reporter._determine_error_severity(timeout_error) == ErrorSeverity.MEDIUM
        
        # Test generic errors
        generic_error = ValueError("Some error")
        assert error_reporter._determine_error_severity(generic_error) == ErrorSeverity.LOW
    
    def test_categorize_error(self, error_reporter):
        """Test error categorization."""
        # Test timeout
        timeout_error = httpx.TimeoutException("Timeout")
        assert error_reporter._categorize_error(timeout_error) == ErrorCategory.TIMEOUT
        
        # Test network error
        network_error = httpx.NetworkError("Network error")
        assert error_reporter._categorize_error(network_error) == ErrorCategory.TRANSIENT_NETWORK
        
        # Test HTTP status errors
        auth_error = httpx.HTTPStatusError(
            "Unauthorized",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=401, reason_phrase="Unauthorized", headers={})
        )
        assert error_reporter._categorize_error(auth_error) == ErrorCategory.AUTHENTICATION
        
        not_found_error = httpx.HTTPStatusError(
            "Not Found",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=404, reason_phrase="Not Found", headers={})
        )
        assert error_reporter._categorize_error(not_found_error) == ErrorCategory.NOT_FOUND
        
        # Test unknown error
        unknown_error = ValueError("Unknown error")
        assert error_reporter._categorize_error(unknown_error) == ErrorCategory.UNKNOWN
    
    def test_collect_diagnostic_data_levels(self, sample_request):
        """Test diagnostic data collection at different levels."""
        error = NetworkError("Network error")
        
        # Basic level
        reporter_basic = BatchErrorReporter(diagnostic_level=DiagnosticLevel.BASIC)
        data_basic = reporter_basic._collect_diagnostic_data(error, sample_request)
        
        assert 'basic_info' in data_basic
        assert data_basic['basic_info']['error_class'] == 'NetworkError'
        assert 'error_details' not in data_basic
        
        # Detailed level
        reporter_detailed = BatchErrorReporter(diagnostic_level=DiagnosticLevel.DETAILED)
        data_detailed = reporter_detailed._collect_diagnostic_data(error, sample_request)
        
        assert 'error_details' in data_detailed
        assert 'request_details' in data_detailed
        assert data_detailed['error_details']['error_class'] == 'NetworkError'
        assert data_detailed['request_details']['file_path'] == 'package.json'
        
        # Comprehensive level
        reporter_comprehensive = BatchErrorReporter(diagnostic_level=DiagnosticLevel.COMPREHENSIVE)
        data_comprehensive = reporter_comprehensive._collect_diagnostic_data(error, sample_request)
        
        assert 'comprehensive_info' in data_comprehensive
        assert 'repository_info' in data_comprehensive['comprehensive_info']
    
    def test_collect_diagnostic_data_http_error(self, sample_request):
        """Test diagnostic data collection for HTTP errors."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.reason_phrase = "Not Found"
        mock_response.headers = {"Content-Type": "application/json"}
        
        mock_request = Mock()
        mock_request.url = "https://api.github.com/repos/owner/test-repo/contents/package.json"
        
        error = httpx.HTTPStatusError("Not Found", request=mock_request, response=mock_response)
        
        reporter = BatchErrorReporter(diagnostic_level=DiagnosticLevel.DETAILED)
        data = reporter._collect_diagnostic_data(error, sample_request)
        
        assert 'http_details' in data
        assert data['http_details']['status_code'] == 404
        assert data['http_details']['reason_phrase'] == "Not Found"
        assert data['http_details']['headers']['Content-Type'] == "application/json"
    
    def test_record_recovery_attempt(self, error_reporter, sample_request):
        """Test recording recovery attempts."""
        error = NetworkError("Network error")
        diagnostic = error_reporter.create_error_diagnostic(error, sample_request)
        
        # Record successful recovery
        error_reporter.record_recovery_attempt(
            error_id=diagnostic.error_id,
            recovery_strategy="retry_with_backoff",
            successful=True,
            additional_info={"attempts": 3}
        )
        
        updated_diagnostic = error_reporter.error_diagnostics[diagnostic.error_id]
        assert updated_diagnostic.recovery_attempted is True
        assert updated_diagnostic.recovery_successful is True
        assert 'recovery_info' in updated_diagnostic.diagnostic_data
        assert updated_diagnostic.diagnostic_data['recovery_info']['strategy'] == "retry_with_backoff"
        assert updated_diagnostic.diagnostic_data['recovery_info']['successful'] is True
        assert updated_diagnostic.diagnostic_data['recovery_info']['attempts'] == 3
    
    def test_create_batch_summary(self, error_reporter, sample_batch_results):
        """Test creating batch summary."""
        # Create diagnostics for failed results
        for result in sample_batch_results:
            if not result.success and result.error:
                error_reporter.create_error_diagnostic(
                    error=result.error,
                    request=result.request,
                    batch_id="test_batch"
                )
        
        batch_metrics = BatchMetrics(
            total_requests=4,
            successful_requests=2,
            failed_requests=2,
            cache_hits=1,
            cache_misses=3,
            total_processing_time=3.3
        )
        
        start_time = datetime.now() - timedelta(seconds=30)
        end_time = datetime.now()
        
        summary = error_reporter.create_batch_summary(
            batch_id="test_batch",
            batch_results=sample_batch_results,
            batch_metrics=batch_metrics,
            start_time=start_time,
            end_time=end_time
        )
        
        assert summary.batch_id == "test_batch"
        assert summary.total_requests == 4
        assert summary.successful_requests == 2
        assert summary.failed_requests == 2
        assert summary.success_rate == 50.0
        assert len(summary.error_categories) > 0
        assert len(summary.most_common_errors) > 0
        
        # Should be stored in reporter
        assert "test_batch" in error_reporter.batch_summaries
    
    def test_generate_diagnostic_report_json(self, error_reporter, sample_request):
        """Test generating diagnostic report in JSON format."""
        # Create some diagnostics
        error1 = NetworkError("Network error 1")
        error2 = httpx.HTTPStatusError(
            "Not Found",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=404, reason_phrase="Not Found", headers={})
        )
        
        error_reporter.create_error_diagnostic(error1, sample_request, batch_id="batch1")
        error_reporter.create_error_diagnostic(error2, sample_request, batch_id="batch1")
        
        # Generate report
        report_json = error_reporter.generate_diagnostic_report(format_type="json")
        
        assert isinstance(report_json, str)
        report_data = json.loads(report_json)
        
        assert 'report_generated' in report_data
        assert 'diagnostic_level' in report_data
        assert 'total_errors' in report_data
        assert 'error_diagnostics' in report_data
        assert 'overall_statistics' in report_data
        
        assert report_data['total_errors'] == 2
        assert report_data['diagnostic_level'] == 'detailed'
        assert len(report_data['error_diagnostics']) == 2
    
    def test_generate_diagnostic_report_dict(self, error_reporter, sample_request):
        """Test generating diagnostic report in dictionary format."""
        error = NetworkError("Network error")
        error_reporter.create_error_diagnostic(error, sample_request, batch_id="batch1")
        
        report_dict = error_reporter.generate_diagnostic_report(format_type="dict")
        
        assert isinstance(report_dict, dict)
        assert 'report_generated' in report_dict
        assert 'total_errors' in report_dict
        assert report_dict['total_errors'] == 1
    
    def test_generate_diagnostic_report_filtered(self, error_reporter, sample_request):
        """Test generating filtered diagnostic report."""
        # Create diagnostics for different batches
        error1 = NetworkError("Error in batch1")
        error2 = NetworkError("Error in batch2")
        
        error_reporter.create_error_diagnostic(error1, sample_request, batch_id="batch1")
        error_reporter.create_error_diagnostic(error2, sample_request, batch_id="batch2")
        
        # Filter by batch_id
        report = error_reporter.generate_diagnostic_report(
            batch_id="batch1",
            format_type="dict"
        )
        
        assert report['total_errors'] == 1
        assert len(report['error_diagnostics']) == 1
        assert report['error_diagnostics'][0]['system_context']['batch_id'] == "batch1"
    
    def test_get_troubleshooting_suggestions(self, error_reporter, sample_request):
        """Test getting troubleshooting suggestions."""
        # Test network error suggestions
        network_error = NetworkError("Network error")
        diagnostic = error_reporter.create_error_diagnostic(network_error, sample_request)
        
        suggestions = error_reporter.get_troubleshooting_suggestions(diagnostic)
        
        assert len(suggestions) > 0
        assert any("network connectivity" in suggestion.lower() for suggestion in suggestions)
        assert any("retry" in suggestion.lower() for suggestion in suggestions)
        
        # Test authentication error suggestions
        auth_error = httpx.HTTPStatusError(
            "Unauthorized",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=401, reason_phrase="Unauthorized", headers={})
        )
        auth_diagnostic = error_reporter.create_error_diagnostic(auth_error, sample_request)
        
        auth_suggestions = error_reporter.get_troubleshooting_suggestions(auth_diagnostic)
        
        assert len(auth_suggestions) > 0
        assert any("token" in suggestion.lower() for suggestion in auth_suggestions)
        assert any("api token" in suggestion.lower() for suggestion in auth_suggestions)
        
        # Test rate limit error suggestions
        rate_limit_error = httpx.HTTPStatusError(
            "Rate Limited",
            request=Mock(url="https://api.github.com/test"),
            response=Mock(status_code=429, reason_phrase="Rate Limited", headers={})
        )
        rate_limit_diagnostic = error_reporter.create_error_diagnostic(rate_limit_error, sample_request)
        
        rate_limit_suggestions = error_reporter.get_troubleshooting_suggestions(rate_limit_diagnostic)
        
        assert len(rate_limit_suggestions) > 0
        assert any("batch size" in suggestion.lower() for suggestion in rate_limit_suggestions)
        assert any("rate limit" in suggestion.lower() for suggestion in rate_limit_suggestions)
    
    def test_clear_diagnostics_all(self, error_reporter, sample_request):
        """Test clearing all diagnostics."""
        # Create some diagnostics
        error1 = NetworkError("Error 1")
        error2 = NetworkError("Error 2")
        
        error_reporter.create_error_diagnostic(error1, sample_request)
        error_reporter.create_error_diagnostic(error2, sample_request)
        
        assert len(error_reporter.error_diagnostics) == 2
        
        # Clear all
        error_reporter.clear_diagnostics()
        
        assert len(error_reporter.error_diagnostics) == 0
        assert len(error_reporter.batch_summaries) == 0
    
    def test_clear_diagnostics_by_age(self, error_reporter, sample_request):
        """Test clearing diagnostics by age."""
        # Create old diagnostic
        old_error = NetworkError("Old error")
        old_diagnostic = error_reporter.create_error_diagnostic(old_error, sample_request)
        old_diagnostic.timestamp = datetime.now() - timedelta(hours=25)  # 25 hours ago
        
        # Create recent diagnostic
        recent_error = NetworkError("Recent error")
        recent_diagnostic = error_reporter.create_error_diagnostic(recent_error, sample_request)
        
        assert len(error_reporter.error_diagnostics) == 2
        
        # Clear diagnostics older than 24 hours
        error_reporter.clear_diagnostics(older_than_hours=24)
        
        assert len(error_reporter.error_diagnostics) == 1
        assert recent_diagnostic.error_id in error_reporter.error_diagnostics
        assert old_diagnostic.error_id not in error_reporter.error_diagnostics


class TestIntegration:
    """Integration tests for error reporting components."""
    
    def test_comprehensive_error_reporting_workflow(self, sample_repository):
        """Test a comprehensive error reporting workflow."""
        reporter = BatchErrorReporter(diagnostic_level=DiagnosticLevel.COMPREHENSIVE)
        
        # Simulate a batch operation with various errors
        batch_id = "integration_test_batch"
        start_time = datetime.now()
        
        requests = [
            BatchRequest(sample_repository, "success1.json"),
            BatchRequest(sample_repository, "network_fail.json"),
            BatchRequest(sample_repository, "not_found.json"),
            BatchRequest(sample_repository, "rate_limited.json"),
            BatchRequest(sample_repository, "success2.json")
        ]
        
        results = []
        
        # Process requests and create diagnostics for failures
        for i, request in enumerate(requests):
            if "success" in request.file_path:
                result = BatchResult(
                    request=request,
                    content=Mock(),
                    processing_time=1.0
                )
            else:
                if "network_fail" in request.file_path:
                    error = httpx.NetworkError("Network connection failed")
                elif "not_found" in request.file_path:
                    error = httpx.HTTPStatusError(
                        "Not Found",
                        request=Mock(url="https://api.github.com/test"),
                        response=Mock(status_code=404, reason_phrase="Not Found", headers={})
                    )
                elif "rate_limited" in request.file_path:
                    error = httpx.HTTPStatusError(
                        "Rate Limited",
                        request=Mock(url="https://api.github.com/test"),
                        response=Mock(status_code=429, reason_phrase="Rate Limited", headers={})
                    )
                else:
                    error = Exception("Unknown error")
                
                # Create diagnostic
                diagnostic = reporter.create_error_diagnostic(
                    error=error,
                    request=request,
                    batch_id=batch_id
                )
                
                # Simulate recovery attempt
                if "network_fail" in request.file_path:
                    reporter.record_recovery_attempt(
                        error_id=diagnostic.error_id,
                        recovery_strategy="retry_with_backoff",
                        successful=True
                    )
                
                result = BatchResult(
                    request=request,
                    error=error,
                    processing_time=0.5
                )
            
            results.append(result)
        
        # Create batch metrics
        batch_metrics = BatchMetrics(
            total_requests=len(requests),
            successful_requests=2,
            failed_requests=3,
            cache_hits=1,
            cache_misses=4,
            total_processing_time=4.0
        )
        
        end_time = datetime.now()
        
        # Create batch summary
        summary = reporter.create_batch_summary(
            batch_id=batch_id,
            batch_results=results,
            batch_metrics=batch_metrics,
            start_time=start_time,
            end_time=end_time
        )
        
        # Verify comprehensive reporting
        assert len(reporter.error_diagnostics) == 3  # 3 failed requests
        assert batch_id in reporter.batch_summaries
        
        # Verify summary details
        assert summary.total_requests == 5
        assert summary.successful_requests == 2
        assert summary.failed_requests == 3
        assert summary.success_rate == 40.0
        assert len(summary.error_categories) > 0
        assert len(summary.most_common_errors) > 0
        
        # Generate comprehensive report
        report = reporter.generate_diagnostic_report(format_type="dict")
        
        assert report['total_errors'] == 3
        assert report['total_batches'] == 1
        assert len(report['error_diagnostics']) == 3
        assert len(report['batch_summaries']) == 1
        assert 'overall_statistics' in report
        
        # Verify overall statistics
        stats = report['overall_statistics']
        assert stats['total_requests_processed'] == 5
        assert stats['total_successful_requests'] == 2
        assert stats['total_failed_requests'] == 3
        assert stats['overall_success_rate'] == 40.0
        
        # Test troubleshooting suggestions for each error
        for diagnostic in reporter.error_diagnostics.values():
            suggestions = reporter.get_troubleshooting_suggestions(diagnostic)
            assert len(suggestions) > 0
    
    def test_error_reporting_with_different_diagnostic_levels(self, sample_repository):
        """Test error reporting with different diagnostic levels."""
        request = BatchRequest(sample_repository, "test.json")
        error = NetworkError("Network error")
        
        # Test basic level
        reporter_basic = BatchErrorReporter(diagnostic_level=DiagnosticLevel.BASIC)
        diagnostic_basic = reporter_basic.create_error_diagnostic(error, request)
        
        assert 'basic_info' in diagnostic_basic.diagnostic_data
        assert 'error_details' not in diagnostic_basic.diagnostic_data
        assert diagnostic_basic.stack_trace is None
        
        # Test detailed level
        reporter_detailed = BatchErrorReporter(diagnostic_level=DiagnosticLevel.DETAILED)
        diagnostic_detailed = reporter_detailed.create_error_diagnostic(error, request)
        
        assert 'error_details' in diagnostic_detailed.diagnostic_data
        assert 'request_details' in diagnostic_detailed.diagnostic_data
        assert diagnostic_detailed.stack_trace is not None
        
        # Test comprehensive level
        reporter_comprehensive = BatchErrorReporter(diagnostic_level=DiagnosticLevel.COMPREHENSIVE)
        diagnostic_comprehensive = reporter_comprehensive.create_error_diagnostic(error, request)
        
        assert 'comprehensive_info' in diagnostic_comprehensive.diagnostic_data
        assert 'repository_info' in diagnostic_comprehensive.diagnostic_data['comprehensive_info']
        assert diagnostic_comprehensive.stack_trace is not None