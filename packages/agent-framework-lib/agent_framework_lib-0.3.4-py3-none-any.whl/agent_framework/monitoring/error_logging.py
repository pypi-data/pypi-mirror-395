"""
Error Logging Configuration for Agent Framework

This module provides comprehensive logging configuration that integrates with
the structured error handling system to provide detailed error tracking,
monitoring, and debugging capabilities.

v 0.1.0 - Initial implementation for enhanced file management
"""

import logging
import json
import sys
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path

from .error_handling import (
    FileProcessingError,
    ProcessingIssue,
    ErrorSeverity,
    FileProcessingErrorType
)


class StructuredErrorFormatter(logging.Formatter):
    """Custom formatter for structured error logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        # Start with basic formatting
        formatted = super().format(record)
        
        # Add structured error information if available
        if hasattr(record, 'error_type'):
            error_info = {
                'error_type': record.error_type,
                'severity': getattr(record, 'severity', 'unknown'),
                'user_message': getattr(record, 'user_message', ''),
                'suggestions': getattr(record, 'suggestions', []),
                'context': getattr(record, 'context', {}),
                'technical_details': getattr(record, 'technical_details', ''),
                'timestamp': datetime.now().isoformat()
            }
            
            # Append structured information
            formatted += f"\n[STRUCTURED_ERROR] {json.dumps(error_info, indent=2)}"
        
        return formatted


class ErrorMetricsCollector:
    """Collects error metrics for monitoring and analysis"""
    
    def __init__(self):
        self.error_counts: Dict[str, int] = {}
        self.error_history: List[Dict[str, Any]] = []
        self.session_errors: Dict[str, List[Dict[str, Any]]] = {}
        self.user_errors: Dict[str, List[Dict[str, Any]]] = {}
        
    def record_error(self, error: FileProcessingError, 
                    session_id: str = None, user_id: str = None):
        """Record an error for metrics collection"""
        
        error_type_str = error.error_type.value
        self.error_counts[error_type_str] = self.error_counts.get(error_type_str, 0) + 1
        
        error_record = {
            'timestamp': error.timestamp.isoformat(),
            'error_type': error_type_str,
            'severity': error.severity.value,
            'message': error.message,
            'user_message': error.user_message,
            'context': error.context,
            'session_id': session_id,
            'user_id': user_id
        }
        
        self.error_history.append(error_record)
        
        # Track by session
        if session_id:
            if session_id not in self.session_errors:
                self.session_errors[session_id] = []
            self.session_errors[session_id].append(error_record)
        
        # Track by user
        if user_id:
            if user_id not in self.user_errors:
                self.user_errors[user_id] = []
            self.user_errors[user_id].append(error_record)
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get comprehensive error summary"""
        total_errors = sum(self.error_counts.values())
        
        # Calculate error rates by severity
        severity_counts = {}
        for error_record in self.error_history:
            severity = error_record['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Most common errors
        most_common = sorted(
            self.error_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        # Recent errors (last 100)
        recent_errors = self.error_history[-100:] if len(self.error_history) > 100 else self.error_history
        
        return {
            'total_errors': total_errors,
            'error_counts_by_type': dict(self.error_counts),
            'error_counts_by_severity': severity_counts,
            'most_common_errors': most_common,
            'recent_errors_count': len(recent_errors),
            'sessions_with_errors': len(self.session_errors),
            'users_with_errors': len(self.user_errors),
            'collection_period': {
                'start': self.error_history[0]['timestamp'] if self.error_history else None,
                'end': self.error_history[-1]['timestamp'] if self.error_history else None
            }
        }
    
    def get_session_errors(self, session_id: str) -> List[Dict[str, Any]]:
        """Get errors for a specific session"""
        return self.session_errors.get(session_id, [])
    
    def get_user_errors(self, user_id: str) -> List[Dict[str, Any]]:
        """Get errors for a specific user"""
        return self.user_errors.get(user_id, [])
    
    def clear_old_errors(self, days_to_keep: int = 30):
        """Clear errors older than specified days"""
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        
        # Filter error history
        self.error_history = [
            error for error in self.error_history
            if datetime.fromisoformat(error['timestamp']).timestamp() > cutoff_date
        ]
        
        # Recalculate counts
        self.error_counts = {}
        for error in self.error_history:
            error_type = error['error_type']
            self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Clear old session and user errors
        for session_id in list(self.session_errors.keys()):
            self.session_errors[session_id] = [
                error for error in self.session_errors[session_id]
                if datetime.fromisoformat(error['timestamp']).timestamp() > cutoff_date
            ]
            if not self.session_errors[session_id]:
                del self.session_errors[session_id]
        
        for user_id in list(self.user_errors.keys()):
            self.user_errors[user_id] = [
                error for error in self.user_errors[user_id]
                if datetime.fromisoformat(error['timestamp']).timestamp() > cutoff_date
            ]
            if not self.user_errors[user_id]:
                del self.user_errors[user_id]


class ErrorLoggingHandler(logging.Handler):
    """Custom logging handler that integrates with error metrics collection"""
    
    def __init__(self, metrics_collector: ErrorMetricsCollector):
        super().__init__()
        self.metrics_collector = metrics_collector
    
    def emit(self, record: logging.LogRecord):
        """Handle log record and extract error information"""
        
        # Check if this is a structured error log
        if hasattr(record, 'error_type') and hasattr(record, 'severity'):
            # Create a FileProcessingError from the log record
            try:
                from .error_handling import FileProcessingErrorType, ErrorSeverity
                
                error_type = FileProcessingErrorType(record.error_type)
                severity = ErrorSeverity(record.severity)
                
                error = FileProcessingError(
                    error_type=error_type,
                    severity=severity,
                    message=record.getMessage(),
                    user_message=getattr(record, 'user_message', ''),
                    suggestions=getattr(record, 'suggestions', []),
                    technical_details=getattr(record, 'technical_details', ''),
                    context=getattr(record, 'context', {})
                )
                
                # Extract session and user info from context
                context = getattr(record, 'context', {})
                session_id = context.get('session_id')
                user_id = context.get('user_id')
                
                self.metrics_collector.record_error(error, session_id, user_id)
                
            except (ValueError, AttributeError) as e:
                # If we can't parse the structured error, just log it normally
                print(f"Warning: Could not parse structured error from log record: {e}")


async def configure_error_logging(log_level: str = "INFO", 
                          log_file: Optional[str] = None,
                          enable_structured_logging: bool = True,
                          enable_metrics_collection: bool = True,
                          enable_elasticsearch: Optional[bool] = None,
                          es_index_pattern: Optional[str] = None,
                          es_batch_size: Optional[int] = None,
                          es_flush_interval: Optional[float] = None) -> Optional[ErrorMetricsCollector]:
    """
    Configure comprehensive error logging for the agent framework
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging output
        enable_structured_logging: Whether to use structured error formatting
        enable_metrics_collection: Whether to collect error metrics
        enable_elasticsearch: Whether to enable Elasticsearch logging (auto-detected if None)
        es_index_pattern: Elasticsearch index pattern (default: agent-logs-{date})
        es_batch_size: Elasticsearch batch size (default: 100)
        es_flush_interval: Elasticsearch flush interval in seconds (default: 5.0)
        
    Returns:
        ErrorMetricsCollector instance if metrics collection is enabled
    """
    
    # Get the root logger for agent_framework
    logger = logging.getLogger('agent_framework')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create metrics collector if enabled
    metrics_collector = ErrorMetricsCollector() if enable_metrics_collection else None
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    if enable_structured_logging:
        console_formatter = StructuredErrorFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        if enable_structured_logging:
            file_formatter = StructuredErrorFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        else:
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Add metrics collection handler if enabled
    if metrics_collector:
        metrics_handler = ErrorLoggingHandler(metrics_collector)
        logger.addHandler(metrics_handler)
    
    # Add Elasticsearch handler if enabled
    if enable_elasticsearch is None:
        # Auto-detect from environment
        enable_elasticsearch = os.getenv("ELASTICSEARCH_ENABLED", "false").lower() == "true"
    
    if enable_elasticsearch:
        try:
            from .elasticsearch_logging import ElasticsearchLoggingHandler
            from ..session.session_storage import get_shared_elasticsearch_client
            
            # Get shared ES client
            es_client = await get_shared_elasticsearch_client()
            
            if es_client:
                # Create Elasticsearch handler with configuration
                es_handler = ElasticsearchLoggingHandler(
                    es_client=es_client,
                    index_pattern=es_index_pattern,
                    batch_size=es_batch_size,
                    flush_interval=es_flush_interval
                )
                es_handler.setLevel(getattr(logging, log_level.upper()))
                
                # Add handler to logger
                logger.addHandler(es_handler)
                logger.info(f"Elasticsearch logging handler added successfully "
                          f"(index: {es_handler.index_pattern}, batch: {es_handler.batch_size}, "
                          f"flush: {es_handler.flush_interval}s)")
            else:
                logger.warning("Elasticsearch logging enabled but client not available")
        except Exception as e:
            logger.warning(f"Failed to add Elasticsearch logging handler: {e}")
    
    logger.info(f"Configured error logging - Level: {log_level}, Structured: {enable_structured_logging}, "
               f"Metrics: {enable_metrics_collection}, Elasticsearch: {enable_elasticsearch}")
    
    return metrics_collector


def log_structured_error(logger: logging.Logger, 
                        error: FileProcessingError,
                        session_id: str = None,
                        user_id: str = None):
    """
    Log a structured error with all relevant information
    
    Args:
        logger: Logger instance to use
        error: FileProcessingError to log
        session_id: Optional session ID for context
        user_id: Optional user ID for context
    """
    
    # Add session and user context
    context = error.context.copy()
    if session_id:
        context['session_id'] = session_id
    if user_id:
        context['user_id'] = user_id
    
    # Determine log level based on error severity
    if error.severity == ErrorSeverity.CRITICAL:
        log_level = logging.CRITICAL
    elif error.severity == ErrorSeverity.ERROR:
        log_level = logging.ERROR
    elif error.severity == ErrorSeverity.WARNING:
        log_level = logging.WARNING
    else:
        log_level = logging.INFO
    
    # Create log record with structured information
    logger.log(
        log_level,
        error.message,
        extra={
            'error_type': error.error_type.value,
            'severity': error.severity.value,
            'user_message': error.user_message,
            'suggestions': error.suggestions,
            'context': context,
            'technical_details': error.technical_details,
            'recovery_strategy': error.recovery_strategy.value
        }
    )


def log_processing_issue(logger: logging.Logger,
                        issue: ProcessingIssue,
                        session_id: str = None,
                        user_id: str = None):
    """
    Log a processing issue with structured information
    
    Args:
        logger: Logger instance to use
        issue: ProcessingIssue to log
        session_id: Optional session ID for context
        user_id: Optional user ID for context
    """
    
    # Add session and user context
    context = issue.context.copy()
    if session_id:
        context['session_id'] = session_id
    if user_id:
        context['user_id'] = user_id
    
    # Determine log level based on issue severity
    if issue.severity == ErrorSeverity.WARNING:
        log_level = logging.WARNING
    else:
        log_level = logging.INFO
    
    # Create log record with structured information
    logger.log(
        log_level,
        issue.message,
        extra={
            'error_type': issue.error_type.value,
            'severity': issue.severity.value,
            'user_message': issue.user_message,
            'suggestions': issue.suggestions,
            'context': context,
            'technical_details': issue.technical_details
        }
    )


# Global metrics collector instance
_global_metrics_collector: Optional[ErrorMetricsCollector] = None


def get_global_metrics_collector() -> Optional[ErrorMetricsCollector]:
    """Get the global metrics collector instance"""
    return _global_metrics_collector


def set_global_metrics_collector(collector: ErrorMetricsCollector):
    """Set the global metrics collector instance"""
    global _global_metrics_collector
    _global_metrics_collector = collector


# Convenience function for quick setup
async def setup_error_logging(log_file: str = "logs/agent_framework_errors.log",
                             enable_elasticsearch: Optional[bool] = None) -> ErrorMetricsCollector:
    """
    Quick setup for error logging with sensible defaults
    
    Args:
        log_file: Path to log file
        enable_elasticsearch: Whether to enable Elasticsearch logging (auto-detected if None)
        
    Returns:
        ErrorMetricsCollector instance for metrics access
    """
    metrics_collector = await configure_error_logging(
        log_level="INFO",
        log_file=log_file,
        enable_structured_logging=True,
        enable_metrics_collection=True,
        enable_elasticsearch=enable_elasticsearch
    )
    
    if metrics_collector:
        set_global_metrics_collector(metrics_collector)
    
    return metrics_collector