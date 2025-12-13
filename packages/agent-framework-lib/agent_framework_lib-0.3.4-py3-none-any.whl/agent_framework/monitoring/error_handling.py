"""
Comprehensive Error Handling System for Agent Framework

This module provides structured error handling classes and utilities for the entire
file management system, building upon the existing ConversionErrorHandler patterns
and extending them to cover all file operations.

v 0.1.0 - Initial implementation for enhanced file management
"""

import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

logger = logging.getLogger(__name__)


# ===== ERROR TYPE CLASSIFICATIONS =====

class FileProcessingErrorType(Enum):
    """Types of file processing errors"""
    # Storage errors
    STORAGE_BACKEND_UNAVAILABLE = "storage_backend_unavailable"
    STORAGE_PERMISSION_DENIED = "storage_permission_denied"
    STORAGE_QUOTA_EXCEEDED = "storage_quota_exceeded"
    STORAGE_CONNECTION_FAILED = "storage_connection_failed"
    STORAGE_WRITE_FAILED = "storage_write_failed"
    STORAGE_READ_FAILED = "storage_read_failed"
    
    # File validation errors
    FILE_TOO_LARGE = "file_too_large"
    FILE_EMPTY = "file_empty"
    FILE_CORRUPTED = "file_corrupted"
    INVALID_FILE_TYPE = "invalid_file_type"
    MALICIOUS_FILE_DETECTED = "malicious_file_detected"
    FILENAME_INVALID = "filename_invalid"
    
    # Conversion errors
    CONVERSION_FAILED = "conversion_failed"
    FORMAT_NOT_SUPPORTED = "format_not_supported"
    CONVERSION_TIMEOUT = "conversion_timeout"
    CONVERSION_LIBRARY_MISSING = "conversion_library_missing"
    
    # Multimodal processing errors
    MULTIMODAL_PROCESSING_FAILED = "multimodal_processing_failed"
    IMAGE_ANALYSIS_FAILED = "image_analysis_failed"
    OCR_FAILED = "ocr_failed"
    MULTIMODAL_LIBRARY_MISSING = "multimodal_library_missing"
    
    # System resource errors
    MEMORY_EXHAUSTED = "memory_exhausted"
    DISK_SPACE_FULL = "disk_space_full"
    PROCESSING_TIMEOUT = "processing_timeout"
    CONCURRENT_LIMIT_EXCEEDED = "concurrent_limit_exceeded"
    
    # Network and external service errors
    NETWORK_ERROR = "network_error"
    EXTERNAL_SERVICE_UNAVAILABLE = "external_service_unavailable"
    API_RATE_LIMIT_EXCEEDED = "api_rate_limit_exceeded"
    
    # Configuration and setup errors
    CONFIGURATION_ERROR = "configuration_error"
    DEPENDENCY_MISSING = "dependency_missing"
    ENVIRONMENT_ERROR = "environment_error"
    
    # Generic errors
    UNKNOWN_ERROR = "unknown_error"
    INTERNAL_ERROR = "internal_error"


class ErrorSeverity(Enum):
    """Severity levels for file processing errors"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorRecoveryStrategy(Enum):
    """Recovery strategies for different error types"""
    RETRY = "retry"
    FALLBACK = "fallback"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    USER_INTERVENTION = "user_intervention"
    SYSTEM_RESTART = "system_restart"
    NO_RECOVERY = "no_recovery"


# ===== ERROR DATA STRUCTURES =====

@dataclass
class FileProcessingError(Exception):
    """Base exception for file processing errors with structured information"""
    error_type: FileProcessingErrorType
    severity: ErrorSeverity
    message: str
    user_message: str
    suggestions: List[str] = field(default_factory=list)
    recovery_strategy: ErrorRecoveryStrategy = ErrorRecoveryStrategy.NO_RECOVERY
    technical_details: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        return f"{self.error_type.value}: {self.message}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/serialization"""
        return {
            'error_type': self.error_type.value,
            'severity': self.severity.value,
            'message': self.message,
            'user_message': self.user_message,
            'suggestions': self.suggestions,
            'recovery_strategy': self.recovery_strategy.value,
            'technical_details': self.technical_details,
            'context': self.context,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class ProcessingIssue:
    """Represents a processing issue (error or warning) that doesn't stop execution"""
    severity: ErrorSeverity
    error_type: FileProcessingErrorType
    message: str
    user_message: str
    suggestions: List[str] = field(default_factory=list)
    technical_details: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert issue to dictionary for logging/serialization"""
        return {
            'severity': self.severity.value,
            'error_type': self.error_type.value,
            'message': self.message,
            'user_message': self.user_message,
            'suggestions': self.suggestions,
            'technical_details': self.technical_details,
            'context': self.context,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class ErrorHandlingResult:
    """Result of error handling operations"""
    success: bool
    handled_errors: List[FileProcessingError] = field(default_factory=list)
    issues: List[ProcessingIssue] = field(default_factory=list)
    recovery_actions_taken: List[str] = field(default_factory=list)
    user_messages: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    
    @property
    def has_critical_errors(self) -> bool:
        """Check if there are any critical errors"""
        return any(error.severity == ErrorSeverity.CRITICAL for error in self.handled_errors)
    
    @property
    def has_errors(self) -> bool:
        """Check if there are any errors (ERROR or CRITICAL)"""
        return any(error.severity in [ErrorSeverity.ERROR, ErrorSeverity.CRITICAL] 
                  for error in self.handled_errors)
    
    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings"""
        return any(issue.severity == ErrorSeverity.WARNING for issue in self.issues)
    
    def get_all_user_messages(self) -> List[str]:
        """Get all user messages from errors and issues"""
        messages = self.user_messages.copy()
        messages.extend([error.user_message for error in self.handled_errors if error.user_message])
        messages.extend([issue.user_message for issue in self.issues if issue.user_message])
        return messages
    
    def get_all_suggestions(self) -> List[str]:
        """Get all suggestions from errors and issues"""
        suggestions = self.suggestions.copy()
        for error in self.handled_errors:
            suggestions.extend(error.suggestions)
        for issue in self.issues:
            suggestions.extend(issue.suggestions)
        return list(set(suggestions))  # Remove duplicates


# ===== SPECIALIZED ERROR CLASSES =====

class StorageError(FileProcessingError):
    """Storage-related errors"""
    def __init__(self, error_type: FileProcessingErrorType, message: str, 
                 backend_name: str = None, **kwargs):
        super().__init__(error_type=error_type, message=message, **kwargs)
        if backend_name:
            self.context['backend_name'] = backend_name


class ConversionError(FileProcessingError):
    """File conversion-related errors"""
    def __init__(self, error_type: FileProcessingErrorType, message: str,
                 source_format: str = None, target_format: str = None, **kwargs):
        super().__init__(error_type=error_type, message=message, **kwargs)
        if source_format:
            self.context['source_format'] = source_format
        if target_format:
            self.context['target_format'] = target_format


class MultimodalProcessingError(FileProcessingError):
    """Multimodal processing-related errors"""
    def __init__(self, error_type: FileProcessingErrorType, message: str,
                 processing_type: str = None, **kwargs):
        super().__init__(error_type=error_type, message=message, **kwargs)
        if processing_type:
            self.context['processing_type'] = processing_type


class ValidationError(FileProcessingError):
    """File validation-related errors"""
    def __init__(self, error_type: FileProcessingErrorType, message: str,
                 validation_rule: str = None, **kwargs):
        super().__init__(error_type=error_type, message=message, **kwargs)
        if validation_rule:
            self.context['validation_rule'] = validation_rule


# ===== ERROR HANDLER CLASS =====

class ErrorHandler:
    """Centralized error handling for file operations"""
    
    # Error message templates and recovery strategies
    ERROR_TEMPLATES = {
        FileProcessingErrorType.STORAGE_BACKEND_UNAVAILABLE: {
            'message': "Storage backend is not available",
            'user_message': "File storage system is temporarily unavailable",
            'suggestions': [
                "Try again in a few moments",
                "Contact support if the problem persists",
                "Files may be stored locally as a fallback"
            ],
            'recovery_strategy': ErrorRecoveryStrategy.FALLBACK,
            'severity': ErrorSeverity.ERROR
        },
        FileProcessingErrorType.FILE_TOO_LARGE: {
            'message': "File exceeds maximum size limit",
            'user_message': "File is too large to process",
            'suggestions': [
                "Try splitting the file into smaller parts",
                "Compress the file to reduce its size",
                "Contact support for larger file limits"
            ],
            'recovery_strategy': ErrorRecoveryStrategy.USER_INTERVENTION,
            'severity': ErrorSeverity.ERROR
        },
        FileProcessingErrorType.FORMAT_NOT_SUPPORTED: {
            'message': "File format is not supported",
            'user_message': "This file type is not supported for processing",
            'suggestions': [
                "Try converting to a supported format (PDF, DOCX, TXT, etc.)",
                "The file will still be stored in its original format",
                "Contact support to request support for this format"
            ],
            'recovery_strategy': ErrorRecoveryStrategy.GRACEFUL_DEGRADATION,
            'severity': ErrorSeverity.WARNING
        },
        FileProcessingErrorType.CONVERSION_FAILED: {
            'message': "File conversion failed",
            'user_message': "Could not convert file to markdown format",
            'suggestions': [
                "The original file is still available",
                "Try uploading a different version of the file",
                "Manual conversion may be needed"
            ],
            'recovery_strategy': ErrorRecoveryStrategy.GRACEFUL_DEGRADATION,
            'severity': ErrorSeverity.WARNING
        },
        FileProcessingErrorType.MULTIMODAL_PROCESSING_FAILED: {
            'message': "Multimodal processing failed",
            'user_message': "Could not analyze visual content in the file",
            'suggestions': [
                "The file is still stored and accessible",
                "Try uploading a clearer image",
                "Manual analysis may be needed"
            ],
            'recovery_strategy': ErrorRecoveryStrategy.GRACEFUL_DEGRADATION,
            'severity': ErrorSeverity.WARNING
        },
        FileProcessingErrorType.MEMORY_EXHAUSTED: {
            'message': "System memory exhausted during processing",
            'user_message': "File is too large for current system resources",
            'suggestions': [
                "Try processing a smaller file",
                "Wait for system resources to become available",
                "Contact support for resource limits"
            ],
            'recovery_strategy': ErrorRecoveryStrategy.RETRY,
            'severity': ErrorSeverity.ERROR
        },
        FileProcessingErrorType.STORAGE_QUOTA_EXCEEDED: {
            'message': "Storage quota exceeded",
            'user_message': "Storage space limit has been reached",
            'suggestions': [
                "Delete some old files to free up space",
                "Contact support to increase storage quota",
                "Consider using file compression"
            ],
            'recovery_strategy': ErrorRecoveryStrategy.USER_INTERVENTION,
            'severity': ErrorSeverity.ERROR
        }
    }
    
    def __init__(self, enable_logging: bool = True):
        self.enable_logging = enable_logging
        self.error_counts = {}
        self.recovery_attempts = {}
    
    def create_error(self, 
                    error_type: FileProcessingErrorType,
                    message: str = None,
                    user_message: str = None,
                    context: Dict[str, Any] = None,
                    technical_details: str = None,
                    exception: Exception = None) -> FileProcessingError:
        """Create a structured error with appropriate defaults"""
        
        # Get template information
        template = self.ERROR_TEMPLATES.get(error_type, {})
        
        # Use provided message or template message
        final_message = message or template.get('message', f"Error of type {error_type.value}")
        final_user_message = user_message or template.get('user_message', "An error occurred during file processing")
        
        # Create error with context
        error_context = context or {}
        if exception:
            error_context['original_exception'] = str(exception)
            error_context['exception_type'] = type(exception).__name__
        
        error = FileProcessingError(
            error_type=error_type,
            severity=template.get('severity', ErrorSeverity.ERROR),
            message=final_message,
            user_message=final_user_message,
            suggestions=template.get('suggestions', []),
            recovery_strategy=template.get('recovery_strategy', ErrorRecoveryStrategy.NO_RECOVERY),
            technical_details=technical_details,
            context=error_context
        )
        
        # Log error if enabled
        if self.enable_logging:
            self._log_error(error)
        
        # Track error counts
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        return error
    
    def create_issue(self,
                    error_type: FileProcessingErrorType,
                    severity: ErrorSeverity,
                    message: str = None,
                    user_message: str = None,
                    context: Dict[str, Any] = None,
                    technical_details: str = None) -> ProcessingIssue:
        """Create a processing issue (non-fatal error/warning)"""
        
        template = self.ERROR_TEMPLATES.get(error_type, {})
        
        final_message = message or template.get('message', f"Issue of type {error_type.value}")
        final_user_message = user_message or template.get('user_message', "A processing issue occurred")
        
        issue = ProcessingIssue(
            severity=severity,
            error_type=error_type,
            message=final_message,
            user_message=final_user_message,
            suggestions=template.get('suggestions', []),
            technical_details=technical_details,
            context=context or {}
        )
        
        if self.enable_logging:
            self._log_issue(issue)
        
        return issue
    
    def handle_exception(self,
                        exception: Exception,
                        operation: str,
                        filename: str = None,
                        context: Dict[str, Any] = None) -> FileProcessingError:
        """Handle a generic exception and convert it to a structured error"""
        
        # Determine error type based on exception type
        error_type = self._classify_exception(exception)
        
        # Create context with operation details
        error_context = context or {}
        error_context.update({
            'operation': operation,
            'filename': filename,
            'exception_type': type(exception).__name__
        })
        
        return self.create_error(
            error_type=error_type,
            message=f"Exception during {operation}: {str(exception)}",
            context=error_context,
            technical_details=str(exception),
            exception=exception
        )
    
    def _classify_exception(self, exception: Exception) -> FileProcessingErrorType:
        """Classify an exception into a FileProcessingErrorType"""
        
        exception_type = type(exception).__name__
        exception_message = str(exception).lower()
        
        # Storage-related exceptions
        if 'permission' in exception_message or 'access' in exception_message:
            return FileProcessingErrorType.STORAGE_PERMISSION_DENIED
        elif 'space' in exception_message or 'quota' in exception_message:
            return FileProcessingErrorType.STORAGE_QUOTA_EXCEEDED
        elif 'connection' in exception_message or 'network' in exception_message:
            return FileProcessingErrorType.STORAGE_CONNECTION_FAILED
        
        # Memory-related exceptions
        elif exception_type == 'MemoryError' or 'memory' in exception_message:
            return FileProcessingErrorType.MEMORY_EXHAUSTED
        
        # File-related exceptions
        elif exception_type == 'FileNotFoundError':
            return FileProcessingErrorType.STORAGE_READ_FAILED
        elif 'corrupt' in exception_message or 'invalid' in exception_message:
            return FileProcessingErrorType.FILE_CORRUPTED
        
        # Timeout exceptions
        elif 'timeout' in exception_message or exception_type == 'TimeoutError':
            return FileProcessingErrorType.PROCESSING_TIMEOUT
        
        # Import/dependency exceptions
        elif exception_type == 'ImportError' or exception_type == 'ModuleNotFoundError':
            return FileProcessingErrorType.DEPENDENCY_MISSING
        
        # Default to unknown error
        else:
            return FileProcessingErrorType.UNKNOWN_ERROR
    
    def _log_error(self, error: FileProcessingError):
        """Log an error with appropriate level"""
        log_data = error.to_dict()
        
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"CRITICAL ERROR: {error.message}", extra=log_data)
        elif error.severity == ErrorSeverity.ERROR:
            logger.error(f"ERROR: {error.message}", extra=log_data)
        elif error.severity == ErrorSeverity.WARNING:
            logger.warning(f"WARNING: {error.message}", extra=log_data)
        else:
            logger.info(f"INFO: {error.message}", extra=log_data)
    
    def _log_issue(self, issue: ProcessingIssue):
        """Log a processing issue"""
        log_data = issue.to_dict()
        
        if issue.severity == ErrorSeverity.WARNING:
            logger.warning(f"PROCESSING WARNING: {issue.message}", extra=log_data)
        else:
            logger.info(f"PROCESSING INFO: {issue.message}", extra=log_data)
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics for monitoring"""
        return {
            'total_errors': sum(self.error_counts.values()),
            'error_counts_by_type': dict(self.error_counts),
            'most_common_errors': sorted(
                self.error_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5]
        }


# ===== USER FEEDBACK GENERATOR =====

class UserFeedbackGenerator:
    """Generates user-friendly feedback for file operations"""
    
    @staticmethod
    def generate_error_summary(errors: List[FileProcessingError]) -> str:
        """Generate a comprehensive error summary for users"""
        if not errors:
            return "No errors occurred."
        
        if len(errors) == 1:
            error = errors[0]
            return f"❌ {error.user_message}"
        
        # Multiple errors
        critical_errors = [e for e in errors if e.severity == ErrorSeverity.CRITICAL]
        regular_errors = [e for e in errors if e.severity == ErrorSeverity.ERROR]
        warnings = [e for e in errors if e.severity == ErrorSeverity.WARNING]
        
        summary_parts = []
        
        if critical_errors:
            summary_parts.append(f"🚨 {len(critical_errors)} critical error(s)")
        if regular_errors:
            summary_parts.append(f"❌ {len(regular_errors)} error(s)")
        if warnings:
            summary_parts.append(f"⚠️ {len(warnings)} warning(s)")
        
        return f"Multiple issues occurred: {', '.join(summary_parts)}"
    
    @staticmethod
    def generate_processing_feedback(result: ErrorHandlingResult, 
                                   operation: str = "file processing") -> str:
        """Generate comprehensive processing feedback"""
        if result.success and not result.has_warnings:
            return f"✅ {operation.capitalize()} completed successfully"
        
        feedback_parts = []
        
        if result.success:
            feedback_parts.append(f"✅ {operation.capitalize()} completed")
        else:
            feedback_parts.append(f"❌ {operation.capitalize()} failed")
        
        if result.has_critical_errors:
            critical_count = sum(1 for e in result.handled_errors 
                               if e.severity == ErrorSeverity.CRITICAL)
            feedback_parts.append(f"🚨 {critical_count} critical issue(s)")
        
        if result.has_errors and not result.has_critical_errors:
            error_count = sum(1 for e in result.handled_errors 
                            if e.severity == ErrorSeverity.ERROR)
            feedback_parts.append(f"❌ {error_count} error(s)")
        
        if result.has_warnings:
            warning_count = sum(1 for i in result.issues 
                              if i.severity == ErrorSeverity.WARNING)
            feedback_parts.append(f"⚠️ {warning_count} warning(s)")
        
        if result.recovery_actions_taken:
            feedback_parts.append(f"🔧 {len(result.recovery_actions_taken)} recovery action(s) taken")
        
        return " - ".join(feedback_parts)
    
    @staticmethod
    def generate_suggestions_list(suggestions: List[str]) -> str:
        """Generate a formatted list of suggestions"""
        if not suggestions:
            return ""
        
        if len(suggestions) == 1:
            return f"💡 Suggestion: {suggestions[0]}"
        
        formatted_suggestions = []
        for i, suggestion in enumerate(suggestions[:5], 1):  # Limit to 5 suggestions
            formatted_suggestions.append(f"  {i}. {suggestion}")
        
        result = "💡 Suggestions:\n" + "\n".join(formatted_suggestions)
        
        if len(suggestions) > 5:
            result += f"\n  ... and {len(suggestions) - 5} more"
        
        return result


# ===== GRACEFUL DEGRADATION UTILITIES =====

class GracefulDegradationHandler:
    """Handles graceful degradation scenarios"""
    
    @staticmethod
    def create_fallback_result(operation: str, 
                             original_error: FileProcessingError,
                             fallback_data: Any = None) -> Dict[str, Any]:
        """Create a fallback result when primary operation fails"""
        return {
            'success': False,
            'fallback_used': True,
            'original_error': original_error.to_dict(),
            'fallback_data': fallback_data,
            'user_message': f"{operation} failed, but fallback data is available",
            'limitations': [
                f"Primary {operation} failed",
                "Using fallback approach with limited functionality"
            ]
        }
    
    @staticmethod
    def should_attempt_recovery(error: FileProcessingError, 
                              max_attempts: int = 3) -> bool:
        """Determine if recovery should be attempted for an error"""
        if error.recovery_strategy == ErrorRecoveryStrategy.NO_RECOVERY:
            return False
        
        if error.severity == ErrorSeverity.CRITICAL:
            return False
        
        # Check if we've already tried too many times
        # This would need to be tracked externally
        return True