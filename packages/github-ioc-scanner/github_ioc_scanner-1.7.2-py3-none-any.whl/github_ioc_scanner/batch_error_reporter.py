"""Detailed error reporting and diagnostics for batch operations."""

import json
import logging
import traceback
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union
import httpx

from .batch_models import BatchRequest, BatchResult, BatchMetrics
from .batch_error_handler import ErrorCategory, ErrorContext
from .exceptions import (
    GitHubIOCScannerError, NetworkError, RateLimitError, APIError,
    AuthenticationError
)


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DiagnosticLevel(Enum):
    """Diagnostic detail levels."""
    BASIC = "basic"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"


@dataclass
class ErrorDiagnostic:
    """Detailed diagnostic information for an error."""
    error_id: str
    timestamp: datetime
    severity: ErrorSeverity
    category: ErrorCategory
    error_type: str
    error_message: str
    request_context: Dict[str, Any]
    system_context: Dict[str, Any]
    stack_trace: Optional[str] = None
    recovery_attempted: bool = False
    recovery_successful: bool = False
    related_errors: List[str] = field(default_factory=list)
    diagnostic_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert diagnostic to dictionary."""
        data = asdict(self)
        # Convert datetime to ISO string
        data['timestamp'] = self.timestamp.isoformat()
        # Convert enums to strings
        data['severity'] = self.severity.value
        data['category'] = self.category.value
        return data


@dataclass
class BatchErrorSummary:
    """Summary of errors in a batch operation."""
    batch_id: str
    start_time: datetime
    end_time: Optional[datetime]
    total_requests: int
    successful_requests: int
    failed_requests: int
    error_categories: Dict[str, int] = field(default_factory=dict)
    severity_distribution: Dict[str, int] = field(default_factory=dict)
    most_common_errors: List[Dict[str, Any]] = field(default_factory=list)
    recovery_statistics: Dict[str, Any] = field(default_factory=dict)
    performance_impact: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def duration_seconds(self) -> float:
        """Calculate batch duration."""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary."""
        data = asdict(self)
        data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        data['success_rate'] = self.success_rate
        data['duration_seconds'] = self.duration_seconds
        return data


class BatchErrorReporter:
    """Comprehensive error reporting and diagnostics for batch operations."""
    
    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        diagnostic_level: DiagnosticLevel = DiagnosticLevel.DETAILED
    ):
        """
        Initialize the error reporter.
        
        Args:
            logger: Optional logger for error reporting
            diagnostic_level: Level of diagnostic detail to collect
        """
        self.logger = logger or logging.getLogger(__name__)
        self.diagnostic_level = diagnostic_level
        self.error_diagnostics: Dict[str, ErrorDiagnostic] = {}
        self.batch_summaries: Dict[str, BatchErrorSummary] = {}
        self._error_counter = 0
    
    def create_error_diagnostic(
        self,
        error: Exception,
        request: BatchRequest,
        batch_id: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> ErrorDiagnostic:
        """
        Create detailed diagnostic information for an error.
        
        Args:
            error: The exception that occurred
            request: The batch request that failed
            batch_id: Optional batch identifier
            additional_context: Additional context information
            
        Returns:
            ErrorDiagnostic with detailed information
        """
        self._error_counter += 1
        error_id = f"batch_error_{self._error_counter}_{int(datetime.now().timestamp())}"
        
        # Determine error severity
        severity = self._determine_error_severity(error)
        
        # Categorize error
        category = self._categorize_error(error)
        
        # Collect request context
        request_context = {
            'repository': request.repo.full_name,
            'file_path': request.file_path,
            'priority': request.priority,
            'estimated_size': request.estimated_size,
            'cache_key': request.cache_key
        }
        
        # Collect system context
        system_context = {
            'batch_id': batch_id,
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_module': type(error).__module__
        }
        
        # Add additional context if provided
        if additional_context:
            system_context.update(additional_context)
        
        # Collect diagnostic data based on level
        diagnostic_data = self._collect_diagnostic_data(error, request)
        
        # Get stack trace if detailed diagnostics are enabled
        stack_trace = None
        if self.diagnostic_level in [DiagnosticLevel.DETAILED, DiagnosticLevel.COMPREHENSIVE]:
            stack_trace = traceback.format_exc()
        
        diagnostic = ErrorDiagnostic(
            error_id=error_id,
            timestamp=datetime.now(),
            severity=severity,
            category=category,
            error_type=type(error).__name__,
            error_message=str(error),
            request_context=request_context,
            system_context=system_context,
            stack_trace=stack_trace,
            diagnostic_data=diagnostic_data
        )
        
        self.error_diagnostics[error_id] = diagnostic
        
        # Log the error with appropriate level
        self._log_error_diagnostic(diagnostic)
        
        return diagnostic
    
    def record_recovery_attempt(
        self,
        error_id: str,
        recovery_strategy: str,
        successful: bool,
        additional_info: Optional[Dict[str, Any]] = None
    ):
        """
        Record a recovery attempt for an error.
        
        Args:
            error_id: ID of the error being recovered
            recovery_strategy: Strategy used for recovery
            successful: Whether recovery was successful
            additional_info: Additional recovery information
        """
        if error_id in self.error_diagnostics:
            diagnostic = self.error_diagnostics[error_id]
            diagnostic.recovery_attempted = True
            diagnostic.recovery_successful = successful
            
            recovery_info = {
                'strategy': recovery_strategy,
                'successful': successful,
                'timestamp': datetime.now().isoformat()
            }
            
            if additional_info:
                recovery_info.update(additional_info)
            
            diagnostic.diagnostic_data['recovery_info'] = recovery_info
            
            self.logger.info(
                f"Recovery {'succeeded' if successful else 'failed'} for error {error_id} "
                f"using strategy: {recovery_strategy}"
            )
    
    def create_batch_summary(
        self,
        batch_id: str,
        batch_results: List[BatchResult],
        batch_metrics: BatchMetrics,
        start_time: datetime,
        end_time: Optional[datetime] = None
    ) -> BatchErrorSummary:
        """
        Create a comprehensive summary of batch errors.
        
        Args:
            batch_id: Batch identifier
            batch_results: Results from the batch operation
            batch_metrics: Batch performance metrics
            start_time: When the batch started
            end_time: When the batch ended
            
        Returns:
            BatchErrorSummary with comprehensive error analysis
        """
        # Count successful and failed requests
        successful_requests = sum(1 for result in batch_results if result.success)
        failed_requests = len(batch_results) - successful_requests
        
        # Analyze error categories
        error_categories = {}
        severity_distribution = {}
        error_details = []
        
        for result in batch_results:
            if not result.success and result.error:
                # Find diagnostic for this error
                diagnostic = self._find_diagnostic_for_error(result.error, result.request)
                
                if diagnostic:
                    category = diagnostic.category.value
                    severity = diagnostic.severity.value
                    
                    error_categories[category] = error_categories.get(category, 0) + 1
                    severity_distribution[severity] = severity_distribution.get(severity, 0) + 1
                    
                    error_details.append({
                        'error_id': diagnostic.error_id,
                        'error_type': diagnostic.error_type,
                        'error_message': diagnostic.error_message,
                        'category': category,
                        'severity': severity,
                        'file_path': result.request.file_path,
                        'repository': result.request.repo.full_name
                    })
        
        # Find most common errors
        error_counts = {}
        for detail in error_details:
            key = f"{detail['error_type']}: {detail['error_message']}"
            if key not in error_counts:
                error_counts[key] = {
                    'error_type': detail['error_type'],
                    'error_message': detail['error_message'],
                    'count': 0,
                    'category': detail['category'],
                    'severity': detail['severity']
                }
            error_counts[key]['count'] += 1
        
        most_common_errors = sorted(
            error_counts.values(),
            key=lambda x: x['count'],
            reverse=True
        )[:5]  # Top 5 most common errors
        
        # Calculate recovery statistics
        recovery_stats = self._calculate_recovery_statistics(batch_id)
        
        # Calculate performance impact
        performance_impact = self._calculate_performance_impact(
            batch_metrics, failed_requests, len(batch_results)
        )
        
        summary = BatchErrorSummary(
            batch_id=batch_id,
            start_time=start_time,
            end_time=end_time or datetime.now(),
            total_requests=len(batch_results),
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            error_categories=error_categories,
            severity_distribution=severity_distribution,
            most_common_errors=most_common_errors,
            recovery_statistics=recovery_stats,
            performance_impact=performance_impact
        )
        
        self.batch_summaries[batch_id] = summary
        
        # Log batch summary
        self._log_batch_summary(summary)
        
        return summary
    
    def generate_diagnostic_report(
        self,
        batch_id: Optional[str] = None,
        include_resolved: bool = True,
        format_type: str = "json"
    ) -> Union[str, Dict[str, Any]]:
        """
        Generate a comprehensive diagnostic report.
        
        Args:
            batch_id: Optional batch ID to filter by
            include_resolved: Whether to include resolved errors
            format_type: Output format ("json" or "dict")
            
        Returns:
            Diagnostic report in requested format
        """
        # Filter diagnostics
        diagnostics = self.error_diagnostics
        if batch_id:
            diagnostics = {
                k: v for k, v in diagnostics.items()
                if v.system_context.get('batch_id') == batch_id
            }
        
        if not include_resolved:
            diagnostics = {
                k: v for k, v in diagnostics.items()
                if not v.recovery_successful
            }
        
        # Filter summaries
        summaries = self.batch_summaries
        if batch_id:
            summaries = {k: v for k, v in summaries.items() if k == batch_id}
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'diagnostic_level': self.diagnostic_level.value,
            'total_errors': len(diagnostics),
            'total_batches': len(summaries),
            'error_diagnostics': [diag.to_dict() for diag in diagnostics.values()],
            'batch_summaries': [summary.to_dict() for summary in summaries.values()],
            'overall_statistics': self._generate_overall_statistics(diagnostics, summaries)
        }
        
        if format_type == "json":
            return json.dumps(report, indent=2, default=str)
        else:
            return report
    
    def get_troubleshooting_suggestions(
        self,
        error_diagnostic: ErrorDiagnostic
    ) -> List[str]:
        """
        Get troubleshooting suggestions for a specific error.
        
        Args:
            error_diagnostic: Error diagnostic to analyze
            
        Returns:
            List of troubleshooting suggestions
        """
        suggestions = []
        
        category = error_diagnostic.category
        error_type = error_diagnostic.error_type
        
        # Category-based suggestions
        if category == ErrorCategory.TRANSIENT_NETWORK:
            suggestions.extend([
                "Check network connectivity and stability",
                "Consider increasing retry delays or maximum retry attempts",
                "Verify DNS resolution is working correctly",
                "Check for network proxy or firewall issues"
            ])
        elif category == ErrorCategory.RATE_LIMIT:
            suggestions.extend([
                "Reduce batch size or concurrency limits",
                "Implement longer delays between requests",
                "Check GitHub API rate limit status",
                "Consider using multiple API tokens for higher limits"
            ])
        elif category == ErrorCategory.AUTHENTICATION:
            suggestions.extend([
                "Verify GitHub API token is valid and not expired",
                "Check token permissions and scopes",
                "Ensure token has access to the target repositories",
                "Consider regenerating the API token"
            ])
        elif category == ErrorCategory.PERMISSION:
            suggestions.extend([
                "Verify repository access permissions",
                "Check if repository is private and token has appropriate access",
                "Ensure organization membership if accessing org repositories",
                "Review repository-specific access controls"
            ])
        elif category == ErrorCategory.NOT_FOUND:
            suggestions.extend([
                "Verify repository and file paths are correct",
                "Check if repository has been renamed or deleted",
                "Ensure file exists in the specified branch",
                "Verify branch name is correct (default branch may have changed)"
            ])
        elif category == ErrorCategory.SERVER_ERROR:
            suggestions.extend([
                "Check GitHub API status page for service issues",
                "Implement exponential backoff with longer delays",
                "Consider reducing request frequency temporarily",
                "Monitor for service recovery and retry later"
            ])
        
        # Error type specific suggestions
        if "timeout" in error_type.lower():
            suggestions.extend([
                "Increase request timeout values",
                "Reduce batch sizes for large file operations",
                "Check network latency to GitHub servers"
            ])
        
        if "connection" in error_type.lower():
            suggestions.extend([
                "Verify internet connectivity",
                "Check for DNS resolution issues",
                "Consider connection pooling settings"
            ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_suggestions = []
        for suggestion in suggestions:
            if suggestion not in seen:
                seen.add(suggestion)
                unique_suggestions.append(suggestion)
        
        return unique_suggestions
    
    def _determine_error_severity(self, error: Exception) -> ErrorSeverity:
        """Determine the severity of an error."""
        if isinstance(error, httpx.HTTPStatusError):
            status_code = error.response.status_code
            if status_code == 401:
                return ErrorSeverity.CRITICAL  # Authentication issues are critical
            elif status_code == 403:
                return ErrorSeverity.HIGH  # Permission issues are high severity
            elif status_code == 404:
                return ErrorSeverity.MEDIUM  # Not found is medium severity
            elif status_code >= 500:
                return ErrorSeverity.HIGH  # Server errors are high severity
            elif status_code == 429:
                return ErrorSeverity.MEDIUM  # Rate limits are medium severity
        
        if isinstance(error, (httpx.TimeoutException, httpx.NetworkError)):
            return ErrorSeverity.MEDIUM  # Network issues are medium severity
        
        if isinstance(error, GitHubIOCScannerError):
            # Custom exceptions can have their own severity logic
            return ErrorSeverity.MEDIUM
        
        return ErrorSeverity.LOW  # Default to low severity
    
    def _categorize_error(self, error: Exception) -> ErrorCategory:
        """Categorize an error (reuse logic from error handler)."""
        # Handle httpx specific errors
        if isinstance(error, httpx.TimeoutException):
            return ErrorCategory.TIMEOUT
        elif isinstance(error, httpx.NetworkError):
            return ErrorCategory.TRANSIENT_NETWORK
        elif isinstance(error, httpx.HTTPStatusError):
            status_code = error.response.status_code
            if status_code == 401:
                return ErrorCategory.AUTHENTICATION
            elif status_code == 403:
                return ErrorCategory.PERMISSION
            elif status_code == 404:
                return ErrorCategory.NOT_FOUND
            elif status_code == 429:
                return ErrorCategory.RATE_LIMIT
            elif 400 <= status_code < 500:
                return ErrorCategory.MALFORMED_REQUEST
            elif 500 <= status_code < 600:
                return ErrorCategory.SERVER_ERROR
        
        # Handle custom exceptions
        if isinstance(error, RateLimitError):
            return ErrorCategory.RATE_LIMIT
        elif isinstance(error, AuthenticationError):
            return ErrorCategory.AUTHENTICATION
        elif isinstance(error, NetworkError):
            return ErrorCategory.TRANSIENT_NETWORK
        elif isinstance(error, APIError):
            if error.status_code:
                if error.status_code == 404:
                    return ErrorCategory.NOT_FOUND
                elif error.status_code == 403:
                    return ErrorCategory.PERMISSION
                elif 500 <= error.status_code < 600:
                    return ErrorCategory.SERVER_ERROR
        
        return ErrorCategory.UNKNOWN
    
    def _collect_diagnostic_data(
        self,
        error: Exception,
        request: BatchRequest
    ) -> Dict[str, Any]:
        """Collect diagnostic data based on diagnostic level."""
        data = {}
        
        if self.diagnostic_level == DiagnosticLevel.BASIC:
            data['basic_info'] = {
                'error_class': type(error).__name__,
                'request_file': request.file_path
            }
        elif self.diagnostic_level == DiagnosticLevel.DETAILED:
            data.update({
                'error_details': {
                    'error_class': type(error).__name__,
                    'error_module': type(error).__module__,
                    'error_args': getattr(error, 'args', [])
                },
                'request_details': {
                    'file_path': request.file_path,
                    'repository': request.repo.full_name,
                    'priority': request.priority,
                    'estimated_size': request.estimated_size
                }
            })
            
            # Add HTTP-specific details
            if isinstance(error, httpx.HTTPStatusError):
                data['http_details'] = {
                    'status_code': error.response.status_code,
                    'reason_phrase': getattr(error.response, 'reason_phrase', 'Unknown'),
                    'headers': dict(error.response.headers) if hasattr(error.response.headers, 'items') else {},
                    'url': str(error.request.url) if hasattr(error.request, 'url') else 'Unknown'
                }
        elif self.diagnostic_level == DiagnosticLevel.COMPREHENSIVE:
            # Include everything from detailed level first
            data.update({
                'error_details': {
                    'error_class': type(error).__name__,
                    'error_module': type(error).__module__,
                    'error_args': getattr(error, 'args', [])
                },
                'request_details': {
                    'file_path': request.file_path,
                    'repository': request.repo.full_name,
                    'priority': request.priority,
                    'estimated_size': request.estimated_size
                }
            })
            
            # Add HTTP-specific details
            if isinstance(error, httpx.HTTPStatusError):
                data['http_details'] = {
                    'status_code': error.response.status_code,
                    'reason_phrase': getattr(error.response, 'reason_phrase', 'Unknown'),
                    'headers': dict(error.response.headers) if hasattr(error.response.headers, 'items') else {},
                    'url': str(error.request.url) if hasattr(error.request, 'url') else 'Unknown'
                }
            
            # Add comprehensive info
            data['comprehensive_info'] = {
                'system_info': {
                    'timestamp': datetime.now().isoformat(),
                    'diagnostic_level': self.diagnostic_level.value
                },
                'repository_info': {
                    'name': request.repo.name,
                    'full_name': request.repo.full_name,
                    'archived': request.repo.archived,
                    'default_branch': request.repo.default_branch,
                    'updated_at': request.repo.updated_at.isoformat()
                }
            }
        
        return data
    
    def _find_diagnostic_for_error(
        self,
        error: Exception,
        request: BatchRequest
    ) -> Optional[ErrorDiagnostic]:
        """Find existing diagnostic for an error."""
        # This is a simplified approach - in practice you might want more sophisticated matching
        for diagnostic in self.error_diagnostics.values():
            if (diagnostic.error_message == str(error) and
                diagnostic.request_context.get('file_path') == request.file_path and
                diagnostic.request_context.get('repository') == request.repo.full_name):
                return diagnostic
        return None
    
    def _calculate_recovery_statistics(self, batch_id: str) -> Dict[str, Any]:
        """Calculate recovery statistics for a batch."""
        batch_diagnostics = [
            diag for diag in self.error_diagnostics.values()
            if diag.system_context.get('batch_id') == batch_id
        ]
        
        total_errors = len(batch_diagnostics)
        recovery_attempted = sum(1 for diag in batch_diagnostics if diag.recovery_attempted)
        recovery_successful = sum(1 for diag in batch_diagnostics if diag.recovery_successful)
        
        return {
            'total_errors': total_errors,
            'recovery_attempted': recovery_attempted,
            'recovery_successful': recovery_successful,
            'recovery_success_rate': (recovery_successful / recovery_attempted * 100) if recovery_attempted > 0 else 0
        }
    
    def _calculate_performance_impact(
        self,
        batch_metrics: BatchMetrics,
        failed_requests: int,
        total_requests: int
    ) -> Dict[str, Any]:
        """Calculate performance impact of errors."""
        return {
            'failure_rate_percent': (failed_requests / total_requests * 100) if total_requests > 0 else 0,
            'total_processing_time': batch_metrics.total_processing_time,
            'average_processing_time': batch_metrics.total_processing_time / total_requests if total_requests > 0 else 0,
            'cache_hit_rate': batch_metrics.cache_hit_rate,
            'estimated_time_lost_to_errors': failed_requests * 2.0  # Rough estimate
        }
    
    def _generate_overall_statistics(
        self,
        diagnostics: Dict[str, ErrorDiagnostic],
        summaries: Dict[str, BatchErrorSummary]
    ) -> Dict[str, Any]:
        """Generate overall statistics across all errors and batches."""
        if not diagnostics and not summaries:
            return {}
        
        # Error statistics
        error_categories = {}
        severity_counts = {}
        
        for diagnostic in diagnostics.values():
            category = diagnostic.category.value
            severity = diagnostic.severity.value
            
            error_categories[category] = error_categories.get(category, 0) + 1
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Batch statistics
        total_requests = sum(summary.total_requests for summary in summaries.values())
        total_successful = sum(summary.successful_requests for summary in summaries.values())
        total_failed = sum(summary.failed_requests for summary in summaries.values())
        
        return {
            'error_categories': error_categories,
            'severity_distribution': severity_counts,
            'overall_success_rate': (total_successful / total_requests * 100) if total_requests > 0 else 0,
            'total_requests_processed': total_requests,
            'total_successful_requests': total_successful,
            'total_failed_requests': total_failed,
            'average_batch_size': total_requests / len(summaries) if summaries else 0
        }
    
    def _log_error_diagnostic(self, diagnostic: ErrorDiagnostic):
        """Log error diagnostic with appropriate level."""
        severity_to_log_level = {
            ErrorSeverity.LOW: logging.INFO,
            ErrorSeverity.MEDIUM: logging.WARNING,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL
        }
        
        log_level = severity_to_log_level.get(diagnostic.severity, logging.WARNING)
        
        message = (
            f"Batch error [{diagnostic.error_id}] - {diagnostic.error_type}: "
            f"{diagnostic.error_message} (Category: {diagnostic.category.value}, "
            f"Severity: {diagnostic.severity.value}, "
            f"Repository: {diagnostic.request_context['repository']}, "
            f"File: {diagnostic.request_context['file_path']})"
        )
        
        self.logger.log(log_level, message)
    
    def _log_batch_summary(self, summary: BatchErrorSummary):
        """Log batch summary."""
        message = (
            f"Batch [{summary.batch_id}] completed - "
            f"Success rate: {summary.success_rate:.1f}% "
            f"({summary.successful_requests}/{summary.total_requests}), "
            f"Duration: {summary.duration_seconds:.1f}s"
        )
        
        if summary.failed_requests > 0:
            message += f", Failed: {summary.failed_requests}"
            if summary.error_categories:
                top_category = max(summary.error_categories.items(), key=lambda x: x[1])
                message += f", Top error: {top_category[0]} ({top_category[1]} occurrences)"
        
        log_level = logging.WARNING if summary.failed_requests > 0 else logging.INFO
        self.logger.log(log_level, message)
    
    def clear_diagnostics(self, older_than_hours: Optional[int] = None):
        """
        Clear diagnostic data.
        
        Args:
            older_than_hours: Only clear diagnostics older than this many hours
        """
        if older_than_hours is None:
            self.error_diagnostics.clear()
            self.batch_summaries.clear()
        else:
            cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
            
            # Clear old diagnostics
            self.error_diagnostics = {
                k: v for k, v in self.error_diagnostics.items()
                if v.timestamp > cutoff_time
            }
            
            # Clear old summaries
            self.batch_summaries = {
                k: v for k, v in self.batch_summaries.items()
                if v.start_time > cutoff_time
            }