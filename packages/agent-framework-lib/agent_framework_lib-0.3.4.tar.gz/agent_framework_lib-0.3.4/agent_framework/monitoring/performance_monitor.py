"""
Performance Monitor for File Processing System

Provides comprehensive performance monitoring including:
- Operation timing and throughput metrics
- Resource usage tracking
- Performance bottleneck identification
- Historical performance analysis
- Storage space management

v 0.1.9 - Performance and Scalability Enhancements
"""

import asyncio
import logging
import time
import os
import shutil
from typing import Dict, Optional, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
from pathlib import Path
import json
import threading

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Performance metrics for file operations"""
    operation_type: str
    operation_count: int = 0
    total_duration_ms: float = 0.0
    min_duration_ms: float = float('inf')
    max_duration_ms: float = 0.0
    avg_duration_ms: float = 0.0
    success_count: int = 0
    failure_count: int = 0
    success_rate: float = 0.0
    total_bytes_processed: int = 0
    avg_throughput_mbps: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class StorageMetrics:
    """Storage space and usage metrics"""
    backend_name: str
    total_files: int = 0
    total_size_bytes: int = 0
    available_space_bytes: Optional[int] = None
    used_space_bytes: Optional[int] = None
    space_utilization_percent: Optional[float] = None
    largest_file_bytes: int = 0
    smallest_file_bytes: int = 0
    avg_file_size_bytes: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class SystemPerformanceSnapshot:
    """Snapshot of system performance at a point in time"""
    timestamp: datetime
    cpu_usage_percent: float
    memory_usage_mb: float
    disk_io_read_mbps: float
    disk_io_write_mbps: float
    active_operations: int
    queued_operations: int
    network_io_mbps: Optional[float] = None


@dataclass
class PerformanceAlert:
    """Performance alert for monitoring issues"""
    alert_id: str
    alert_type: str  # 'high_latency', 'low_throughput', 'high_error_rate', 'resource_exhaustion'
    severity: str  # 'info', 'warning', 'error', 'critical'
    message: str
    details: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolved_at: Optional[datetime] = None


class PerformanceMonitor:
    """Monitors and tracks performance metrics for file operations"""
    
    def __init__(self, 
                 metrics_retention_hours: int = 24,
                 snapshot_interval_seconds: int = 60,
                 alert_thresholds: Optional[Dict[str, Any]] = None):
        self.metrics_retention_hours = metrics_retention_hours
        self.snapshot_interval_seconds = snapshot_interval_seconds
        
        # Performance metrics by operation type
        self.operation_metrics: Dict[str, PerformanceMetrics] = {}
        
        # Storage metrics by backend
        self.storage_metrics: Dict[str, StorageMetrics] = {}
        
        # Historical performance snapshots
        self.performance_history: deque = deque(maxlen=int(metrics_retention_hours * 3600 / snapshot_interval_seconds))
        
        # Active performance alerts
        self.active_alerts: Dict[str, PerformanceAlert] = {}
        self.alert_history: List[PerformanceAlert] = []
        
        # Alert thresholds
        self.alert_thresholds = alert_thresholds or {
            'high_latency_ms': 5000,  # 5 seconds
            'low_throughput_mbps': 1.0,  # 1 MB/s
            'high_error_rate_percent': 10.0,  # 10%
            'high_memory_usage_percent': 90.0,  # 90%
            'high_cpu_usage_percent': 90.0,  # 90%
            'low_disk_space_percent': 10.0  # 10% remaining
        }
        
        # Background monitoring
        self._monitoring_task: Optional[asyncio.Task] = None
        self._running = False
        self._lock = threading.Lock()
        
        # Operation timing tracking
        self._operation_start_times: Dict[str, float] = {}
        
        logger.info("Initialized PerformanceMonitor")
    
    async def start_monitoring(self):
        """Start background performance monitoring"""
        if self._running:
            return
        
        self._running = True
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("Started performance monitoring")
    
    async def stop_monitoring(self):
        """Stop background performance monitoring"""
        if not self._running:
            return
        
        self._running = False
        
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Stopped performance monitoring")
    
    def start_operation_timing(self, operation_id: str):
        """Start timing an operation"""
        with self._lock:
            self._operation_start_times[operation_id] = time.time()
    
    def end_operation_timing(self, 
                           operation_id: str, 
                           operation_type: str,
                           success: bool = True,
                           bytes_processed: int = 0) -> float:
        """End timing an operation and record metrics"""
        with self._lock:
            if operation_id not in self._operation_start_times:
                logger.warning(f"No start time found for operation {operation_id}")
                return 0.0
            
            start_time = self._operation_start_times.pop(operation_id)
            duration_ms = (time.time() - start_time) * 1000
            
            # Update operation metrics
            self._update_operation_metrics(operation_type, duration_ms, success, bytes_processed)
            
            return duration_ms
    
    def _update_operation_metrics(self, 
                                operation_type: str, 
                                duration_ms: float, 
                                success: bool, 
                                bytes_processed: int):
        """Update performance metrics for an operation type"""
        if operation_type not in self.operation_metrics:
            self.operation_metrics[operation_type] = PerformanceMetrics(operation_type=operation_type)
        
        metrics = self.operation_metrics[operation_type]
        
        # Update counters
        metrics.operation_count += 1
        metrics.total_duration_ms += duration_ms
        metrics.total_bytes_processed += bytes_processed
        
        if success:
            metrics.success_count += 1
        else:
            metrics.failure_count += 1
        
        # Update timing statistics
        metrics.min_duration_ms = min(metrics.min_duration_ms, duration_ms)
        metrics.max_duration_ms = max(metrics.max_duration_ms, duration_ms)
        metrics.avg_duration_ms = metrics.total_duration_ms / metrics.operation_count
        
        # Update success rate
        metrics.success_rate = (metrics.success_count / metrics.operation_count) * 100.0
        
        # Update throughput (MB/s)
        if metrics.total_duration_ms > 0 and metrics.total_bytes_processed > 0:
            total_seconds = metrics.total_duration_ms / 1000.0
            total_mb = metrics.total_bytes_processed / (1024 * 1024)
            metrics.avg_throughput_mbps = total_mb / total_seconds
        
        metrics.last_updated = datetime.now()
        
        # Check for performance alerts
        self._check_performance_alerts(operation_type, metrics)
    
    def update_storage_metrics(self, 
                             backend_name: str, 
                             file_count: int, 
                             total_size_bytes: int,
                             file_sizes: Optional[List[int]] = None,
                             storage_path: Optional[str] = None):
        """Update storage metrics for a backend"""
        if backend_name not in self.storage_metrics:
            self.storage_metrics[backend_name] = StorageMetrics(backend_name=backend_name)
        
        metrics = self.storage_metrics[backend_name]
        
        metrics.total_files = file_count
        metrics.total_size_bytes = total_size_bytes
        
        if file_sizes:
            metrics.largest_file_bytes = max(file_sizes) if file_sizes else 0
            metrics.smallest_file_bytes = min(file_sizes) if file_sizes else 0
            metrics.avg_file_size_bytes = sum(file_sizes) / len(file_sizes) if file_sizes else 0
        
        # Get disk space information if storage path is provided
        if storage_path and os.path.exists(storage_path):
            try:
                total, used, free = shutil.disk_usage(storage_path)
                metrics.available_space_bytes = free
                metrics.used_space_bytes = used
                metrics.space_utilization_percent = (used / total) * 100.0
            except Exception as e:
                logger.warning(f"Failed to get disk usage for {storage_path}: {e}")
        
        metrics.last_updated = datetime.now()
        
        # Check for storage alerts
        self._check_storage_alerts(backend_name, metrics)
    
    def get_operation_metrics(self, operation_type: Optional[str] = None) -> Dict[str, PerformanceMetrics]:
        """Get performance metrics for operations"""
        if operation_type:
            return {operation_type: self.operation_metrics.get(operation_type)} if operation_type in self.operation_metrics else {}
        return self.operation_metrics.copy()
    
    def get_storage_metrics(self, backend_name: Optional[str] = None) -> Dict[str, StorageMetrics]:
        """Get storage metrics for backends"""
        if backend_name:
            return {backend_name: self.storage_metrics.get(backend_name)} if backend_name in self.storage_metrics else {}
        return self.storage_metrics.copy()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a comprehensive performance summary"""
        total_operations = sum(m.operation_count for m in self.operation_metrics.values())
        total_successes = sum(m.success_count for m in self.operation_metrics.values())
        total_failures = sum(m.failure_count for m in self.operation_metrics.values())
        total_bytes = sum(m.total_bytes_processed for m in self.operation_metrics.values())
        
        overall_success_rate = (total_successes / total_operations * 100.0) if total_operations > 0 else 0.0
        
        # Get latest performance snapshot
        latest_snapshot = self.performance_history[-1] if self.performance_history else None
        
        return {
            'summary': {
                'total_operations': total_operations,
                'total_successes': total_successes,
                'total_failures': total_failures,
                'overall_success_rate_percent': overall_success_rate,
                'total_bytes_processed': total_bytes,
                'active_alerts': len(self.active_alerts),
                'monitoring_since': datetime.now() - timedelta(hours=self.metrics_retention_hours)
            },
            'current_system': {
                'cpu_usage_percent': latest_snapshot.cpu_usage_percent if latest_snapshot else None,
                'memory_usage_mb': latest_snapshot.memory_usage_mb if latest_snapshot else None,
                'active_operations': latest_snapshot.active_operations if latest_snapshot else 0,
                'queued_operations': latest_snapshot.queued_operations if latest_snapshot else 0
            },
            'operation_metrics': {k: {
                'count': v.operation_count,
                'success_rate': v.success_rate,
                'avg_duration_ms': v.avg_duration_ms,
                'avg_throughput_mbps': v.avg_throughput_mbps
            } for k, v in self.operation_metrics.items()},
            'storage_metrics': {k: {
                'total_files': v.total_files,
                'total_size_mb': v.total_size_bytes / (1024 * 1024),
                'space_utilization_percent': v.space_utilization_percent,
                'avg_file_size_mb': v.avg_file_size_bytes / (1024 * 1024)
            } for k, v in self.storage_metrics.items()}
        }
    
    def get_active_alerts(self) -> List[PerformanceAlert]:
        """Get all active performance alerts"""
        return list(self.active_alerts.values())
    
    def get_alert_history(self, limit: int = 100) -> List[PerformanceAlert]:
        """Get recent alert history"""
        return self.alert_history[-limit:] if self.alert_history else []
    
    def resolve_alert(self, alert_id: str):
        """Resolve an active alert"""
        if alert_id in self.active_alerts:
            alert = self.active_alerts[alert_id]
            alert.resolved = True
            alert.resolved_at = datetime.now()
            
            # Move to history
            self.alert_history.append(alert)
            del self.active_alerts[alert_id]
            
            logger.info(f"Resolved performance alert: {alert_id}")
    
    def _check_performance_alerts(self, operation_type: str, metrics: PerformanceMetrics):
        """Check for performance-related alerts"""
        # High latency alert
        if metrics.avg_duration_ms > self.alert_thresholds['high_latency_ms']:
            alert_id = f"high_latency_{operation_type}"
            if alert_id not in self.active_alerts:
                alert = PerformanceAlert(
                    alert_id=alert_id,
                    alert_type='high_latency',
                    severity='warning',
                    message=f"High latency detected for {operation_type} operations",
                    details={
                        'operation_type': operation_type,
                        'avg_duration_ms': metrics.avg_duration_ms,
                        'threshold_ms': self.alert_thresholds['high_latency_ms']
                    }
                )
                self.active_alerts[alert_id] = alert
                logger.warning(f"Performance alert: {alert.message}")
        
        # Low throughput alert
        if metrics.avg_throughput_mbps < self.alert_thresholds['low_throughput_mbps'] and metrics.total_bytes_processed > 0:
            alert_id = f"low_throughput_{operation_type}"
            if alert_id not in self.active_alerts:
                alert = PerformanceAlert(
                    alert_id=alert_id,
                    alert_type='low_throughput',
                    severity='warning',
                    message=f"Low throughput detected for {operation_type} operations",
                    details={
                        'operation_type': operation_type,
                        'avg_throughput_mbps': metrics.avg_throughput_mbps,
                        'threshold_mbps': self.alert_thresholds['low_throughput_mbps']
                    }
                )
                self.active_alerts[alert_id] = alert
                logger.warning(f"Performance alert: {alert.message}")
        
        # High error rate alert
        if metrics.success_rate < (100.0 - self.alert_thresholds['high_error_rate_percent']) and metrics.operation_count >= 10:
            alert_id = f"high_error_rate_{operation_type}"
            if alert_id not in self.active_alerts:
                alert = PerformanceAlert(
                    alert_id=alert_id,
                    alert_type='high_error_rate',
                    severity='error',
                    message=f"High error rate detected for {operation_type} operations",
                    details={
                        'operation_type': operation_type,
                        'success_rate': metrics.success_rate,
                        'error_rate': 100.0 - metrics.success_rate,
                        'threshold_percent': self.alert_thresholds['high_error_rate_percent']
                    }
                )
                self.active_alerts[alert_id] = alert
                logger.error(f"Performance alert: {alert.message}")
    
    def _check_storage_alerts(self, backend_name: str, metrics: StorageMetrics):
        """Check for storage-related alerts"""
        # Low disk space alert
        if metrics.space_utilization_percent is not None:
            remaining_percent = 100.0 - metrics.space_utilization_percent
            if remaining_percent < self.alert_thresholds['low_disk_space_percent']:
                alert_id = f"low_disk_space_{backend_name}"
                if alert_id not in self.active_alerts:
                    alert = PerformanceAlert(
                        alert_id=alert_id,
                        alert_type='low_disk_space',
                        severity='critical' if remaining_percent < 5.0 else 'warning',
                        message=f"Low disk space on {backend_name} storage backend",
                        details={
                            'backend_name': backend_name,
                            'space_utilization_percent': metrics.space_utilization_percent,
                            'remaining_percent': remaining_percent,
                            'threshold_percent': self.alert_thresholds['low_disk_space_percent'],
                            'available_bytes': metrics.available_space_bytes
                        }
                    )
                    self.active_alerts[alert_id] = alert
                    logger.critical(f"Storage alert: {alert.message}")
    
    async def _monitoring_loop(self):
        """Background monitoring loop"""
        while self._running:
            try:
                # Take performance snapshot
                await self._take_performance_snapshot()
                
                # Clean up old alerts
                self._cleanup_old_alerts()
                
                # Sleep until next snapshot
                await asyncio.sleep(self.snapshot_interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in performance monitoring loop: {e}")
                await asyncio.sleep(5)  # Short sleep on error
    
    async def _take_performance_snapshot(self):
        """Take a snapshot of current system performance"""
        try:
            import psutil
            
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_mb = memory.used / (1024 * 1024)
            
            # Get disk I/O (if available)
            disk_io = psutil.disk_io_counters()
            disk_read_mbps = 0.0
            disk_write_mbps = 0.0
            
            if disk_io and hasattr(self, '_last_disk_io'):
                time_delta = self.snapshot_interval_seconds
                read_delta = disk_io.read_bytes - self._last_disk_io.read_bytes
                write_delta = disk_io.write_bytes - self._last_disk_io.write_bytes
                
                disk_read_mbps = (read_delta / time_delta) / (1024 * 1024)
                disk_write_mbps = (write_delta / time_delta) / (1024 * 1024)
            
            self._last_disk_io = disk_io
            
            # Create snapshot
            snapshot = SystemPerformanceSnapshot(
                timestamp=datetime.now(),
                cpu_usage_percent=cpu_percent,
                memory_usage_mb=memory_mb,
                disk_io_read_mbps=disk_read_mbps,
                disk_io_write_mbps=disk_write_mbps,
                active_operations=0,  # Will be updated by resource manager
                queued_operations=0   # Will be updated by resource manager
            )
            
            self.performance_history.append(snapshot)
            
            # Check system-level alerts
            self._check_system_alerts(snapshot)
            
        except ImportError:
            logger.warning("psutil not available for system monitoring")
        except Exception as e:
            logger.error(f"Error taking performance snapshot: {e}")
    
    def _check_system_alerts(self, snapshot: SystemPerformanceSnapshot):
        """Check for system-level performance alerts"""
        # High memory usage alert
        if snapshot.memory_usage_mb > 0:  # Only check if we have memory data
            # We need total memory to calculate percentage
            try:
                import psutil
                total_memory_mb = psutil.virtual_memory().total / (1024 * 1024)
                memory_usage_percent = (snapshot.memory_usage_mb / total_memory_mb) * 100.0
                
                if memory_usage_percent > self.alert_thresholds['high_memory_usage_percent']:
                    alert_id = "high_memory_usage"
                    if alert_id not in self.active_alerts:
                        alert = PerformanceAlert(
                            alert_id=alert_id,
                            alert_type='high_memory_usage',
                            severity='warning',
                            message="High system memory usage detected",
                            details={
                                'memory_usage_percent': memory_usage_percent,
                                'memory_usage_mb': snapshot.memory_usage_mb,
                                'threshold_percent': self.alert_thresholds['high_memory_usage_percent']
                            }
                        )
                        self.active_alerts[alert_id] = alert
                        logger.warning(f"System alert: {alert.message}")
            except ImportError:
                pass
        
        # High CPU usage alert
        if snapshot.cpu_usage_percent > self.alert_thresholds['high_cpu_usage_percent']:
            alert_id = "high_cpu_usage"
            if alert_id not in self.active_alerts:
                alert = PerformanceAlert(
                    alert_id=alert_id,
                    alert_type='high_cpu_usage',
                    severity='warning',
                    message="High system CPU usage detected",
                    details={
                        'cpu_usage_percent': snapshot.cpu_usage_percent,
                        'threshold_percent': self.alert_thresholds['high_cpu_usage_percent']
                    }
                )
                self.active_alerts[alert_id] = alert
                logger.warning(f"System alert: {alert.message}")
    
    def _cleanup_old_alerts(self):
        """Clean up old resolved alerts from history"""
        # Keep only last 1000 alerts in history
        if len(self.alert_history) > 1000:
            self.alert_history = self.alert_history[-1000:]
        
        # Auto-resolve alerts that are no longer relevant
        current_time = datetime.now()
        alerts_to_resolve = []
        
        for alert_id, alert in self.active_alerts.items():
            # Auto-resolve alerts older than 1 hour if conditions have improved
            if (current_time - alert.timestamp).total_seconds() > 3600:
                alerts_to_resolve.append(alert_id)
        
        for alert_id in alerts_to_resolve:
            self.resolve_alert(alert_id)
    
    def export_metrics(self, filepath: str):
        """Export performance metrics to a JSON file"""
        try:
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'operation_metrics': {
                    k: {
                        'operation_type': v.operation_type,
                        'operation_count': v.operation_count,
                        'total_duration_ms': v.total_duration_ms,
                        'avg_duration_ms': v.avg_duration_ms,
                        'success_rate': v.success_rate,
                        'total_bytes_processed': v.total_bytes_processed,
                        'avg_throughput_mbps': v.avg_throughput_mbps,
                        'last_updated': v.last_updated.isoformat()
                    } for k, v in self.operation_metrics.items()
                },
                'storage_metrics': {
                    k: {
                        'backend_name': v.backend_name,
                        'total_files': v.total_files,
                        'total_size_bytes': v.total_size_bytes,
                        'space_utilization_percent': v.space_utilization_percent,
                        'avg_file_size_bytes': v.avg_file_size_bytes,
                        'last_updated': v.last_updated.isoformat()
                    } for k, v in self.storage_metrics.items()
                },
                'performance_summary': self.get_performance_summary(),
                'active_alerts': [
                    {
                        'alert_id': alert.alert_id,
                        'alert_type': alert.alert_type,
                        'severity': alert.severity,
                        'message': alert.message,
                        'details': alert.details,
                        'timestamp': alert.timestamp.isoformat()
                    } for alert in self.active_alerts.values()
                ]
            }
            
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Exported performance metrics to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to export metrics to {filepath}: {e}")


# Global performance monitor instance
_global_performance_monitor: Optional[PerformanceMonitor] = None
_monitor_lock = threading.Lock()


def get_performance_monitor(**kwargs) -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    global _global_performance_monitor
    
    with _monitor_lock:
        if _global_performance_monitor is None:
            _global_performance_monitor = PerformanceMonitor(**kwargs)
        return _global_performance_monitor


async def initialize_performance_monitor(**kwargs) -> PerformanceMonitor:
    """Initialize and start the global performance monitor"""
    monitor = get_performance_monitor(**kwargs)
    await monitor.start_monitoring()
    return monitor


async def shutdown_performance_monitor():
    """Shutdown the global performance monitor"""
    global _global_performance_monitor
    
    with _monitor_lock:
        if _global_performance_monitor:
            await _global_performance_monitor.stop_monitoring()
            _global_performance_monitor = None