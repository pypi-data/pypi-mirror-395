"""
Elasticsearch Circuit Breaker

This module provides a circuit breaker pattern implementation for Elasticsearch
operations to prevent cascading failures when Elasticsearch is unavailable.

The circuit breaker has three states:
- CLOSED: Normal operation, requests pass through
- OPEN: ES unavailable, requests immediately fail/fallback
- HALF_OPEN: Testing recovery, limited requests allowed

Key Features:
- Automatic failure detection and circuit opening
- Configurable failure threshold
- Recovery timeout with automatic half-open transition
- Thread-safe state management
- Metrics for monitoring

Environment Variables:
- ELASTICSEARCH_CIRCUIT_BREAKER_THRESHOLD: Consecutive failures before opening (default: 5)
- ELASTICSEARCH_CIRCUIT_BREAKER_TIMEOUT: Recovery timeout in seconds (default: 60)

Example:
    ```python
    from agent_framework.monitoring.elasticsearch_circuit_breaker import ElasticsearchCircuitBreaker
    
    # Create circuit breaker
    circuit_breaker = ElasticsearchCircuitBreaker(
        failure_threshold=5,
        recovery_timeout=60
    )
    
    # Check if ES operations should be attempted
    if circuit_breaker.is_available():
        try:
            # Perform ES operation
            result = await es_client.index(...)
            circuit_breaker.record_success()
        except Exception as e:
            circuit_breaker.record_failure()
            # Use fallback
    else:
        # Circuit is open, use fallback immediately
        pass
    ```

Version: 0.1.0
"""

import os
import logging
import time
from enum import Enum
from threading import Lock
from typing import Optional
from datetime import datetime, timezone


logger = logging.getLogger(__name__)


class CircuitBreakerState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, use fallback
    HALF_OPEN = "half_open"  # Testing recovery


class ElasticsearchCircuitBreaker:
    """
    Circuit breaker for Elasticsearch operations.
    
    Prevents cascading failures by opening the circuit after a threshold of
    consecutive failures. After a recovery timeout, the circuit transitions
    to half-open state to test if Elasticsearch has recovered.
    
    Attributes:
        failure_threshold: Number of consecutive failures before opening circuit
        recovery_timeout: Seconds to wait before attempting recovery
        state: Current circuit breaker state
        failure_count: Current count of consecutive failures
        last_failure_time: Timestamp of last failure
        last_state_change: Timestamp of last state change
    """
    
    def __init__(
        self,
        failure_threshold: Optional[int] = None,
        recovery_timeout: Optional[int] = None
    ):
        """
        Initialize the circuit breaker.
        
        Args:
            failure_threshold: Consecutive failures before opening (default: 5)
            recovery_timeout: Seconds before attempting recovery (default: 60)
        """
        # Configuration from environment or parameters
        self.failure_threshold = failure_threshold or int(
            os.getenv("ELASTICSEARCH_CIRCUIT_BREAKER_THRESHOLD", "5")
        )
        self.recovery_timeout = recovery_timeout or int(
            os.getenv("ELASTICSEARCH_CIRCUIT_BREAKER_TIMEOUT", "60")
        )
        
        # State management
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.last_state_change: float = time.time()
        
        # Thread safety
        self._lock = Lock()
        
        logger.info(
            f"Initialized ElasticsearchCircuitBreaker: "
            f"failure_threshold={self.failure_threshold}, "
            f"recovery_timeout={self.recovery_timeout}s"
        )
    
    def record_failure(self) -> None:
        """
        Record a failure and potentially open the circuit.
        
        Increments the failure count and opens the circuit if the threshold
        is reached. Thread-safe.
        """
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            # Check if we should open the circuit
            if self.state == CircuitBreakerState.CLOSED:
                if self.failure_count >= self.failure_threshold:
                    self._transition_to_open()
            
            elif self.state == CircuitBreakerState.HALF_OPEN:
                # Failed during recovery test, reopen circuit
                self._transition_to_open()
            
            logger.debug(
                f"Circuit breaker recorded failure: "
                f"count={self.failure_count}, state={self.state.value}"
            )
    
    def record_success(self) -> None:
        """
        Record a successful operation and potentially close the circuit.
        
        Resets the failure count and closes the circuit if in half-open state.
        Thread-safe.
        """
        with self._lock:
            # Reset failure count
            previous_count = self.failure_count
            self.failure_count = 0
            self.last_failure_time = None
            
            # Close circuit if in half-open state
            if self.state == CircuitBreakerState.HALF_OPEN:
                self._transition_to_closed()
            
            if previous_count > 0:
                logger.debug(
                    f"Circuit breaker recorded success: "
                    f"reset failure count from {previous_count}, state={self.state.value}"
                )
    
    def is_available(self) -> bool:
        """
        Check if Elasticsearch operations should be attempted.
        
        Returns False if circuit is open, True otherwise. Also handles
        automatic transition to half-open state after recovery timeout.
        Thread-safe.
        
        Returns:
            True if operations should be attempted, False otherwise
        """
        with self._lock:
            # Check if we should transition to half-open
            if self.state == CircuitBreakerState.OPEN:
                if self._should_attempt_recovery():
                    self._transition_to_half_open()
            
            # Return availability based on state
            return self.state != CircuitBreakerState.OPEN
    
    def _should_attempt_recovery(self) -> bool:
        """
        Check if enough time has passed to attempt recovery.
        
        Returns:
            True if recovery timeout has elapsed, False otherwise
        """
        if self.last_failure_time is None:
            return False
        
        time_since_failure = time.time() - self.last_failure_time
        return time_since_failure >= self.recovery_timeout
    
    def _transition_to_open(self) -> None:
        """
        Transition circuit breaker to OPEN state.
        
        Should be called with lock held.
        """
        previous_state = self.state
        self.state = CircuitBreakerState.OPEN
        self.last_state_change = time.time()
        
        logger.warning(
            f"Circuit breaker opened: "
            f"previous_state={previous_state.value}, "
            f"failure_count={self.failure_count}, "
            f"threshold={self.failure_threshold}"
        )
    
    def _transition_to_half_open(self) -> None:
        """
        Transition circuit breaker to HALF_OPEN state.
        
        Should be called with lock held.
        """
        previous_state = self.state
        self.state = CircuitBreakerState.HALF_OPEN
        self.last_state_change = time.time()
        
        logger.info(
            f"Circuit breaker transitioning to half-open: "
            f"previous_state={previous_state.value}, "
            f"attempting recovery after {self.recovery_timeout}s"
        )
    
    def _transition_to_closed(self) -> None:
        """
        Transition circuit breaker to CLOSED state.
        
        Should be called with lock held.
        """
        previous_state = self.state
        self.state = CircuitBreakerState.CLOSED
        self.last_state_change = time.time()
        
        logger.info(
            f"Circuit breaker closed: "
            f"previous_state={previous_state.value}, "
            f"Elasticsearch recovered"
        )
    
    def get_state(self) -> CircuitBreakerState:
        """
        Get the current circuit breaker state.
        
        Thread-safe.
        
        Returns:
            Current circuit breaker state
        """
        with self._lock:
            return self.state
    
    def get_failure_count(self) -> int:
        """
        Get the current failure count.
        
        Thread-safe.
        
        Returns:
            Current consecutive failure count
        """
        with self._lock:
            return self.failure_count
    
    def get_metrics(self) -> dict:
        """
        Get circuit breaker metrics for monitoring.
        
        Thread-safe.
        
        Returns:
            Dictionary containing current metrics
        """
        with self._lock:
            return {
                "state": self.state.value,
                "failure_count": self.failure_count,
                "failure_threshold": self.failure_threshold,
                "recovery_timeout": self.recovery_timeout,
                "last_failure_time": (
                    datetime.fromtimestamp(self.last_failure_time, tz=timezone.utc).isoformat()
                    if self.last_failure_time
                    else None
                ),
                "last_state_change": datetime.fromtimestamp(
                    self.last_state_change, tz=timezone.utc
                ).isoformat(),
                "time_since_last_failure": (
                    time.time() - self.last_failure_time
                    if self.last_failure_time
                    else None
                ),
            }
    
    def reset(self) -> None:
        """
        Manually reset the circuit breaker to CLOSED state.
        
        This can be used by administrators to force recovery attempts.
        Thread-safe.
        """
        with self._lock:
            previous_state = self.state
            self.state = CircuitBreakerState.CLOSED
            self.failure_count = 0
            self.last_failure_time = None
            self.last_state_change = time.time()
            
            logger.info(
                f"Circuit breaker manually reset: "
                f"previous_state={previous_state.value}"
            )


# Global circuit breaker instance (singleton)
_global_circuit_breaker: Optional[ElasticsearchCircuitBreaker] = None
_circuit_breaker_lock = Lock()


def get_elasticsearch_circuit_breaker() -> ElasticsearchCircuitBreaker:
    """
    Get the global Elasticsearch circuit breaker instance.
    
    Creates a singleton circuit breaker instance on first call.
    Thread-safe.
    
    Returns:
        Global ElasticsearchCircuitBreaker instance
        
    Example:
        ```python
        from agent_framework.monitoring.elasticsearch_circuit_breaker import (
            get_elasticsearch_circuit_breaker
        )
        
        circuit_breaker = get_elasticsearch_circuit_breaker()
        
        if circuit_breaker.is_available():
            # Perform ES operation
            pass
        ```
    """
    global _global_circuit_breaker
    
    with _circuit_breaker_lock:
        if _global_circuit_breaker is None:
            _global_circuit_breaker = ElasticsearchCircuitBreaker()
        
        return _global_circuit_breaker
