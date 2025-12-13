"""
Resource Manager for File Processing

Manages system resources for file processing operations including:
- Concurrent operation limits
- Memory usage monitoring
- Processing queue management
- Performance metrics tracking

v 0.1.9 - Performance and Scalability Enhancements
"""

import asyncio
import logging
import time
import psutil
from typing import Dict, Optional, Any, List, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from enum import Enum
import threading
import weakref

logger = logging.getLogger(__name__)


class OperationType(Enum):
    """Types of file operations for resource management"""
    UPLOAD = "upload"
    CONVERSION = "conversion"
    ANALYSIS = "analysis"
    STORAGE = "storage"
    RETRIEVAL = "retrieval"
    DELETION = "deletion"


@dataclass
class OperationMetrics:
    """Metrics for a file operation"""
    operation_id: str
    operation_type: OperationType
    file_id: Optional[str]
    filename: Optional[str]
    file_size_bytes: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: Optional[float] = None
    memory_used_mb: Optional[float] = None
    success: bool = True
    error_message: Optional[str] = None
    backend_name: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class ResourceLimits:
    """Resource limits configuration"""
    max_concurrent_operations: int = 10
    max_memory_usage_mb: int = 500
    max_file_size_mb: int = 100
    max_queue_size: int = 50
    operation_timeout_seconds: int = 300  # 5 minutes
    memory_check_interval_seconds: int = 30


@dataclass
class SystemMetrics:
    """Current system resource metrics"""
    active_operations: int
    queued_operations: int
    memory_usage_mb: float
    cpu_usage_percent: float
    disk_usage_percent: float
    total_operations_completed: int
    total_operations_failed: int
    average_operation_time_ms: float
    timestamp: datetime = field(default_factory=datetime.now)


class ResourceManager:
    """Manages system resources for file processing operations"""
    
    def __init__(self, limits: Optional[ResourceLimits] = None):
        self.limits = limits or ResourceLimits()
        self.active_operations: Dict[str, OperationMetrics] = {}
        self.operation_queue: asyncio.Queue = asyncio.Queue(maxsize=self.limits.max_queue_size)
        self.completed_operations: List[OperationMetrics] = []
        self.max_completed_history = 1000  # Keep last 1000 operations
        
        # Synchronization
        self._operation_lock = asyncio.Lock()
        self._metrics_lock = asyncio.Lock()
        
        # Background tasks
        self._monitor_task: Optional[asyncio.Task] = None
        self._cleanup_task: Optional[asyncio.Task] = None
        self._running = False
        
        # Performance tracking
        self._total_operations = 0
        self._total_failed_operations = 0
        self._total_processing_time_ms = 0.0
        
        # Memory monitoring
        self._last_memory_check = datetime.now()
        self._memory_usage_history: List[float] = []
        
        logger.info(f"Initialized ResourceManager with limits: {self.limits}")
    
    async def start(self):
        """Start the resource manager background tasks"""
        if self._running:
            return
        
        self._running = True
        
        # Start background monitoring tasks
        self._monitor_task = asyncio.create_task(self._monitor_resources())
        self._cleanup_task = asyncio.create_task(self._cleanup_completed_operations())
        
        logger.info("ResourceManager started")
    
    async def stop(self):
        """Stop the resource manager and cleanup"""
        if not self._running:
            return
        
        self._running = False
        
        # Cancel background tasks
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
        
        # Wait for active operations to complete (with timeout)
        if self.active_operations:
            logger.info(f"Waiting for {len(self.active_operations)} active operations to complete...")
            timeout = 30  # 30 seconds timeout
            start_time = time.time()
            
            while self.active_operations and (time.time() - start_time) < timeout:
                await asyncio.sleep(1)
            
            if self.active_operations:
                logger.warning(f"Forcibly stopping with {len(self.active_operations)} operations still active")
        
        logger.info("ResourceManager stopped")
    
    @asynccontextmanager
    async def acquire_operation_slot(self, 
                                   operation_type: OperationType,
                                   file_size_bytes: int = 0,
                                   filename: Optional[str] = None,
                                   file_id: Optional[str] = None,
                                   user_id: Optional[str] = None,
                                   session_id: Optional[str] = None,
                                   backend_name: Optional[str] = None):
        """
        Context manager to acquire a processing slot for an operation
        
        Usage:
            async with resource_manager.acquire_operation_slot(
                OperationType.UPLOAD, file_size_bytes=1024, filename="test.txt"
            ) as operation_id:
                # Perform file operation
                pass
        """
        # Validate file size
        if file_size_bytes > self.limits.max_file_size_mb * 1024 * 1024:
            raise ValueError(f"File size {file_size_bytes} bytes exceeds limit of {self.limits.max_file_size_mb}MB")
        
        # Check if we can acquire a slot immediately
        can_proceed = await self._can_start_operation(file_size_bytes)
        
        if not can_proceed:
            # Add to queue and wait
            logger.debug(f"Operation queued: {operation_type.value} for {filename or file_id}")
            await self.operation_queue.put((operation_type, file_size_bytes, filename, file_id, user_id, session_id, backend_name))
            
            # Wait for our turn (this will block until resources are available)
            queued_item = await self.operation_queue.get()
            operation_type, file_size_bytes, filename, file_id, user_id, session_id, backend_name = queued_item
        
        # Create operation metrics
        operation_id = f"{operation_type.value}_{int(time.time() * 1000)}_{id(asyncio.current_task())}"
        
        metrics = OperationMetrics(
            operation_id=operation_id,
            operation_type=operation_type,
            file_id=file_id,
            filename=filename,
            file_size_bytes=file_size_bytes,
            start_time=datetime.now(),
            backend_name=backend_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Acquire the slot
        async with self._operation_lock:
            self.active_operations[operation_id] = metrics
        
        start_memory = self._get_memory_usage()
        
        try:
            logger.debug(f"Started operation {operation_id}: {operation_type.value} for {filename or file_id}")
            yield operation_id
            
            # Operation completed successfully
            metrics.success = True
            
        except Exception as e:
            # Operation failed
            metrics.success = False
            metrics.error_message = str(e)
            logger.error(f"Operation {operation_id} failed: {e}")
            raise
            
        finally:
            # Complete the operation
            end_time = datetime.now()
            metrics.end_time = end_time
            metrics.duration_ms = (end_time - metrics.start_time).total_seconds() * 1000
            metrics.memory_used_mb = self._get_memory_usage() - start_memory
            
            # Move to completed operations
            async with self._operation_lock:
                if operation_id in self.active_operations:
                    del self.active_operations[operation_id]
            
            async with self._metrics_lock:
                self.completed_operations.append(metrics)
                self._total_operations += 1
                if not metrics.success:
                    self._total_failed_operations += 1
                if metrics.duration_ms:
                    self._total_processing_time_ms += metrics.duration_ms
            
            logger.debug(f"Completed operation {operation_id}: {metrics.duration_ms:.2f}ms, success={metrics.success}")
    
    async def _can_start_operation(self, file_size_bytes: int) -> bool:
        """Check if we can start a new operation based on current resource usage"""
        async with self._operation_lock:
            # Check concurrent operation limit
            if len(self.active_operations) >= self.limits.max_concurrent_operations:
                return False
        
        # Check memory usage
        current_memory = self._get_memory_usage()
        estimated_additional_memory = file_size_bytes / (1024 * 1024) * 2  # Estimate 2x file size for processing
        
        if current_memory + estimated_additional_memory > self.limits.max_memory_usage_mb:
            return False
        
        return True
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            return memory_info.rss / (1024 * 1024)  # Convert to MB
        except Exception as e:
            logger.warning(f"Failed to get memory usage: {e}")
            return 0.0
    
    def _get_cpu_usage(self) -> float:
        """Get current CPU usage percentage"""
        try:
            return psutil.cpu_percent(interval=0.1)
        except Exception as e:
            logger.warning(f"Failed to get CPU usage: {e}")
            return 0.0
    
    def _get_disk_usage(self) -> float:
        """Get current disk usage percentage"""
        try:
            disk_usage = psutil.disk_usage('/')
            return (disk_usage.used / disk_usage.total) * 100
        except Exception as e:
            logger.warning(f"Failed to get disk usage: {e}")
            return 0.0
    
    async def get_system_metrics(self) -> SystemMetrics:
        """Get current system metrics"""
        async with self._operation_lock:
            active_count = len(self.active_operations)
        
        queued_count = self.operation_queue.qsize()
        
        async with self._metrics_lock:
            total_completed = len(self.completed_operations)
            avg_time = (self._total_processing_time_ms / self._total_operations) if self._total_operations > 0 else 0.0
        
        return SystemMetrics(
            active_operations=active_count,
            queued_operations=queued_count,
            memory_usage_mb=self._get_memory_usage(),
            cpu_usage_percent=self._get_cpu_usage(),
            disk_usage_percent=self._get_disk_usage(),
            total_operations_completed=self._total_operations,
            total_operations_failed=self._total_failed_operations,
            average_operation_time_ms=avg_time
        )
    
    async def get_operation_metrics(self, operation_id: str) -> Optional[OperationMetrics]:
        """Get metrics for a specific operation"""
        # Check active operations
        async with self._operation_lock:
            if operation_id in self.active_operations:
                return self.active_operations[operation_id]
        
        # Check completed operations
        async with self._metrics_lock:
            for metrics in self.completed_operations:
                if metrics.operation_id == operation_id:
                    return metrics
        
        return None
    
    async def get_recent_operations(self, limit: int = 100) -> List[OperationMetrics]:
        """Get recent completed operations"""
        async with self._metrics_lock:
            return self.completed_operations[-limit:] if self.completed_operations else []
    
    async def get_operations_by_type(self, operation_type: OperationType, limit: int = 100) -> List[OperationMetrics]:
        """Get recent operations of a specific type"""
        async with self._metrics_lock:
            filtered_ops = [op for op in self.completed_operations if op.operation_type == operation_type]
            return filtered_ops[-limit:] if filtered_ops else []
    
    async def _monitor_resources(self):
        """Background task to monitor system resources"""
        while self._running:
            try:
                # Update memory usage history
                current_memory = self._get_memory_usage()
                self._memory_usage_history.append(current_memory)
                
                # Keep only last 100 measurements
                if len(self._memory_usage_history) > 100:
                    self._memory_usage_history.pop(0)
                
                # Check for resource issues
                if current_memory > self.limits.max_memory_usage_mb * 0.9:  # 90% of limit
                    logger.warning(f"High memory usage: {current_memory:.2f}MB (limit: {self.limits.max_memory_usage_mb}MB)")
                
                # Check for stuck operations
                current_time = datetime.now()
                timeout_threshold = timedelta(seconds=self.limits.operation_timeout_seconds)
                
                async with self._operation_lock:
                    stuck_operations = []
                    for op_id, metrics in self.active_operations.items():
                        if current_time - metrics.start_time > timeout_threshold:
                            stuck_operations.append((op_id, metrics))
                    
                    for op_id, metrics in stuck_operations:
                        logger.error(f"Operation {op_id} has been running for {current_time - metrics.start_time}, marking as failed")
                        metrics.success = False
                        metrics.error_message = "Operation timeout"
                        metrics.end_time = current_time
                        metrics.duration_ms = (current_time - metrics.start_time).total_seconds() * 1000
                        
                        # Move to completed operations
                        del self.active_operations[op_id]
                        async with self._metrics_lock:
                            self.completed_operations.append(metrics)
                            self._total_operations += 1
                            self._total_failed_operations += 1
                
                await asyncio.sleep(self.limits.memory_check_interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in resource monitoring: {e}")
                await asyncio.sleep(5)  # Short sleep on error
    
    async def _cleanup_completed_operations(self):
        """Background task to cleanup old completed operations"""
        while self._running:
            try:
                async with self._metrics_lock:
                    if len(self.completed_operations) > self.max_completed_history:
                        # Remove oldest operations
                        excess_count = len(self.completed_operations) - self.max_completed_history
                        self.completed_operations = self.completed_operations[excess_count:]
                        logger.debug(f"Cleaned up {excess_count} old operation records")
                
                # Run cleanup every hour
                await asyncio.sleep(3600)
                
            except Exception as e:
                logger.error(f"Error in operation cleanup: {e}")
                await asyncio.sleep(300)  # 5 minutes on error


# Global resource manager instance
_global_resource_manager: Optional[ResourceManager] = None
_manager_lock = threading.Lock()


def get_resource_manager(limits: Optional[ResourceLimits] = None) -> ResourceManager:
    """Get the global resource manager instance"""
    global _global_resource_manager
    
    with _manager_lock:
        if _global_resource_manager is None:
            _global_resource_manager = ResourceManager(limits)
        return _global_resource_manager


async def initialize_resource_manager(limits: Optional[ResourceLimits] = None) -> ResourceManager:
    """Initialize and start the global resource manager"""
    manager = get_resource_manager(limits)
    await manager.start()
    return manager


async def shutdown_resource_manager():
    """Shutdown the global resource manager"""
    global _global_resource_manager
    
    with _manager_lock:
        if _global_resource_manager:
            await _global_resource_manager.stop()
            _global_resource_manager = None