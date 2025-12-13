"""
Elasticsearch Logging Handler

This module provides a custom logging handler that sends logs to Elasticsearch
with batching, time-based flushing, and automatic fallback to file logging.

Key Features:
- Circular buffer with configurable max size
- Batch processing with configurable batch size
- Time-based flushing with configurable interval
- Structured log documents with context, errors, and trace correlation
- Automatic fallback to file logging on ES failure
- Daily index rotation via {date} pattern

Environment Variables:
- ELASTICSEARCH_LOG_INDEX_PATTERN: Index pattern (default: agent-logs-{date})
- ELASTICSEARCH_LOG_BATCH_SIZE: Batch size (default: 100)
- ELASTICSEARCH_LOG_FLUSH_INTERVAL: Flush interval in seconds (default: 5.0)
- ELASTICSEARCH_FALLBACK_TO_FILE: Enable file fallback (default: true)
- ELASTICSEARCH_FALLBACK_LOG_FILE: Fallback log file path (default: logs/elasticsearch_fallback.log)

Example:
    ```python
    from agent_framework.monitoring.elasticsearch_logging import ElasticsearchLoggingHandler
    from agent_framework.session.session_storage import get_shared_elasticsearch_client
    
    # Get shared ES client
    es_client = await get_shared_elasticsearch_client()
    
    # Create handler
    handler = ElasticsearchLoggingHandler(
        es_client=es_client,
        index_pattern="agent-logs-{date}",
        batch_size=100,
        flush_interval=5.0
    )
    
    # Add to logger
    logger = logging.getLogger("agent_framework")
    logger.addHandler(handler)
    ```

Version: 0.1.0
"""

import os
import logging
import asyncio
import traceback
from collections import deque
from typing import Any, Dict, Optional, Deque
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock


logger = logging.getLogger(__name__)


def get_circuit_breaker():
    """Get the circuit breaker instance lazily to avoid circular imports."""
    from agent_framework.monitoring.elasticsearch_circuit_breaker import get_elasticsearch_circuit_breaker
    return get_elasticsearch_circuit_breaker()


class ElasticsearchLoggingHandler(logging.Handler):
    """
    Custom logging handler that sends logs to Elasticsearch with batching and fallback.
    
    This handler accumulates log records in a circular buffer and sends them to
    Elasticsearch in batches. It supports time-based flushing and automatic fallback
    to file logging when Elasticsearch is unavailable.
    
    Attributes:
        es_client: Elasticsearch client instance
        index_pattern: Index pattern with optional {date} placeholder
        batch_size: Number of logs to accumulate before sending
        flush_interval: Seconds between automatic flushes
        max_buffer_size: Maximum buffer size (circular buffer)
        fallback_to_file: Whether to fallback to file logging on ES failure
        fallback_log_file: Path to fallback log file
    """
    
    def __init__(
        self,
        es_client: Optional[Any] = None,
        index_pattern: Optional[str] = None,
        batch_size: Optional[int] = None,
        flush_interval: Optional[float] = None,
        max_buffer_size: int = 10000,
        fallback_to_file: Optional[bool] = None,
        fallback_log_file: Optional[str] = None
    ):
        """
        Initialize the Elasticsearch logging handler.
        
        Args:
            es_client: Elasticsearch client instance (if None, will be retrieved from shared client)
            index_pattern: Index pattern with optional {date} placeholder
            batch_size: Number of logs to accumulate before sending
            flush_interval: Seconds between automatic flushes
            max_buffer_size: Maximum buffer size (circular buffer)
            fallback_to_file: Whether to fallback to file logging on ES failure
            fallback_log_file: Path to fallback log file
        """
        super().__init__()
        
        # Elasticsearch client
        self.es_client = es_client
        
        # Configuration from environment or parameters
        self.index_pattern = index_pattern or os.getenv(
            "ELASTICSEARCH_LOG_INDEX_PATTERN", "agent-logs-{date}"
        )
        self.batch_size = batch_size or int(os.getenv("ELASTICSEARCH_LOG_BATCH_SIZE", "100"))
        self.flush_interval = flush_interval or float(os.getenv("ELASTICSEARCH_LOG_FLUSH_INTERVAL", "5.0"))
        self.max_buffer_size = max_buffer_size
        
        # Fallback configuration
        self.fallback_to_file = (
            fallback_to_file 
            if fallback_to_file is not None 
            else os.getenv("ELASTICSEARCH_FALLBACK_TO_FILE", "true").lower() == "true"
        )
        self.fallback_log_file = fallback_log_file or os.getenv(
            "ELASTICSEARCH_FALLBACK_LOG_FILE", "logs/elasticsearch_fallback.log"
        )
        
        # Circular buffer for log records
        self.buffer: Deque[Dict[str, Any]] = deque(maxlen=self.max_buffer_size)
        self.buffer_lock = Lock()
        
        # Fallback file handler
        self.fallback_handler: Optional[logging.FileHandler] = None
        if self.fallback_to_file:
            self._setup_fallback_handler()
        
        # Flush timer
        self.last_flush_time = datetime.now(timezone.utc)
        self.flush_task: Optional[asyncio.Task] = None
        self._closed = False
        
        logger.debug(
            f"Initialized ElasticsearchLoggingHandler: "
            f"index_pattern={self.index_pattern}, batch_size={self.batch_size}, "
            f"flush_interval={self.flush_interval}s, max_buffer_size={self.max_buffer_size}"
        )
    
    def _setup_fallback_handler(self) -> None:
        """Set up fallback file handler."""
        try:
            log_path = Path(self.fallback_log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.fallback_handler = logging.FileHandler(self.fallback_log_file)
            self.fallback_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            logger.debug(f"Fallback file handler configured: {self.fallback_log_file}")
        except Exception as e:
            logger.error(f"Failed to setup fallback file handler: {e}")
            self.fallback_handler = None
    
    def _get_index_name(self) -> str:
        """
        Get the index name with date substitution.
        
        Returns:
            Index name with {date} replaced by current date in YYYY-MM-DD format
        """
        if "{date}" in self.index_pattern:
            current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            return self.index_pattern.replace("{date}", current_date)
        return self.index_pattern
    
    def _format_log_document(self, record: logging.LogRecord) -> Dict[str, Any]:
        """
        Format a log record as an Elasticsearch document.
        
        Args:
            record: Log record to format
            
        Returns:
            Dictionary containing all required fields for Elasticsearch
        """
        # Basic log information
        document = {
            "@timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger_name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line_number": record.lineno,
        }
        
        # Add structured context if available
        if hasattr(record, 'context') and record.context:
            document["context"] = record.context
        
        # Add error information if available
        if hasattr(record, 'error_type'):
            document["error"] = {
                "type": getattr(record, 'error_type', None),
                "severity": getattr(record, 'severity', None),
                "technical_details": getattr(record, 'technical_details', None),
            }
        
        # Add trace context if available (OpenTelemetry)
        if hasattr(record, 'trace_id') and hasattr(record, 'span_id'):
            document["trace"] = {
                "trace_id": record.trace_id,
                "span_id": record.span_id,
            }
        
        # Add exception information if present
        if record.exc_info:
            document["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "stack_trace": ''.join(traceback.format_exception(*record.exc_info)),
            }
        
        return document
    
    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log record by adding it to the buffer.
        
        Args:
            record: Log record to emit
        """
        try:
            # Format the log document
            document = self._format_log_document(record)
            
            # Add to buffer
            with self.buffer_lock:
                self.buffer.append(document)
                buffer_size = len(self.buffer)
            
            # Check if we should flush
            if buffer_size >= self.batch_size:
                # Trigger batch flush
                self._schedule_flush()
            else:
                # Check time-based flush
                time_since_flush = (datetime.now(timezone.utc) - self.last_flush_time).total_seconds()
                if time_since_flush >= self.flush_interval:
                    self._schedule_flush()
        
        except Exception as e:
            # Don't let logging errors break the application
            self.handleError(record)
    
    def _schedule_flush(self) -> None:
        """Schedule an async flush operation."""
        try:
            # Get or create event loop
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                # No running loop, create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Schedule flush
            if not self._closed:
                loop.create_task(self._flush_buffer())
        except Exception as e:
            logger.error(f"Failed to schedule flush: {e}")
    
    async def _flush_buffer(self) -> None:
        """
        Flush buffered logs to Elasticsearch using bulk API.
        """
        if self._closed:
            return
        
        # Get documents from buffer
        with self.buffer_lock:
            if not self.buffer:
                return
            
            documents = list(self.buffer)
            self.buffer.clear()
        
        # Update last flush time
        self.last_flush_time = datetime.now(timezone.utc)
        
        # Check circuit breaker before attempting ES operation
        circuit_breaker = get_circuit_breaker()
        
        # Try to send to Elasticsearch
        if self.es_client and circuit_breaker.is_available():
            try:
                # Get index name with date substitution
                index_name = self._get_index_name()
                
                # Prepare bulk operations
                operations = []
                for doc in documents:
                    operations.append({"index": {"_index": index_name}})
                    operations.append(doc)
                
                # Send bulk request
                response = await self.es_client.bulk(operations=operations)
                
                # Record success with circuit breaker
                circuit_breaker.record_success()
                
                # Check for errors
                if response.get("errors"):
                    error_count = sum(1 for item in response["items"] if "error" in item.get("index", {}))
                    logger.warning(f"Elasticsearch bulk operation had {error_count} errors")
                    
                    # Fallback to file for failed documents
                    if self.fallback_handler:
                        logger.warning(
                            f"Activating fallback logging due to Elasticsearch bulk errors "
                            f"(circuit_breaker_state={circuit_breaker.get_state().value})"
                        )
                        self._write_to_fallback(documents)
                else:
                    logger.debug(f"Successfully sent {len(documents)} logs to Elasticsearch")
            
            except Exception as e:
                logger.error(f"Failed to send logs to Elasticsearch: {e}")
                
                # Record failure with circuit breaker
                circuit_breaker.record_failure()
                
                # Fallback to file
                if self.fallback_handler:
                    logger.warning(
                        f"Activating fallback logging due to Elasticsearch failure: {e} "
                        f"(circuit_breaker_state={circuit_breaker.get_state().value})"
                    )
                    self._write_to_fallback(documents)
        else:
            # Circuit breaker is open or no ES client, use fallback immediately
            if not circuit_breaker.is_available():
                logger.warning(
                    f"Circuit breaker is open, using fallback logging "
                    f"(state={circuit_breaker.get_state().value})"
                )
            
            if self.fallback_handler:
                self._write_to_fallback(documents)
    
    def _write_to_fallback(self, documents: list) -> None:
        """
        Write documents to fallback file.
        
        Args:
            documents: List of log documents to write
        """
        if not self.fallback_handler:
            return
        
        try:
            for doc in documents:
                # Create a log record for the fallback handler
                record = logging.LogRecord(
                    name=doc.get("logger_name", "unknown"),
                    level=getattr(logging, doc.get("level", "INFO")),
                    pathname="",
                    lineno=doc.get("line_number", 0),
                    msg=doc.get("message", ""),
                    args=(),
                    exc_info=None
                )
                self.fallback_handler.emit(record)
            
            logger.debug(f"Wrote {len(documents)} logs to fallback file")
        except Exception as e:
            logger.error(f"Failed to write to fallback file: {e}")
    
    def flush(self) -> None:
        """
        Manually flush all buffered logs.
        """
        try:
            # Create event loop if needed
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run flush
            if not self._closed:
                loop.run_until_complete(self._flush_buffer())
        except Exception as e:
            logger.error(f"Failed to flush buffer: {e}")
    
    def close(self) -> None:
        """
        Close the handler and flush remaining logs.
        """
        if self._closed:
            return
        
        self._closed = True
        
        # Flush remaining logs
        self.flush()
        
        # Close fallback handler
        if self.fallback_handler:
            self.fallback_handler.close()
        
        # Call parent close
        super().close()
        
        logger.debug("ElasticsearchLoggingHandler closed")


async def setup_elasticsearch_logging(
    logger_instance: Optional[logging.Logger] = None,
    log_level: str = "INFO",
    es_client: Optional[Any] = None
) -> Optional[ElasticsearchLoggingHandler]:
    """
    Set up Elasticsearch logging for the agent framework.
    
    This is a convenience function that creates and configures an
    ElasticsearchLoggingHandler and adds it to the specified logger.
    
    Args:
        logger_instance: Logger to add handler to (default: agent_framework root logger)
        log_level: Logging level (default: INFO)
        es_client: Elasticsearch client (if None, will use shared client)
        
    Returns:
        ElasticsearchLoggingHandler instance if successful, None otherwise
        
    Example:
        ```python
        from agent_framework.monitoring.elasticsearch_logging import setup_elasticsearch_logging
        
        # Set up ES logging
        handler = await setup_elasticsearch_logging(log_level="DEBUG")
        ```
    """
    try:
        # Get ES client if not provided
        if es_client is None:
            from agent_framework.session.session_storage import get_shared_elasticsearch_client
            es_client = await get_shared_elasticsearch_client()
        
        # Check if ES is available
        if es_client is None:
            logger.info("Elasticsearch logging not enabled (client not available)")
            return None
        
        # Create handler
        handler = ElasticsearchLoggingHandler(es_client=es_client)
        handler.setLevel(getattr(logging, log_level.upper()))
        
        # Get logger
        if logger_instance is None:
            logger_instance = logging.getLogger("agent_framework")
        
        # Add handler
        logger_instance.addHandler(handler)
        
        logger.info("Elasticsearch logging handler configured successfully")
        return handler
    
    except Exception as e:
        logger.error(f"Failed to setup Elasticsearch logging: {e}")
        return None
