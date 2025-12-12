"""
Progress Tracker for File Processing Operations

Provides progress feedback for long-running file operations including:
- Real-time progress updates
- Operation status tracking
- User-friendly progress messages
- Cancellation support

v 0.1.9 - Performance and Scalability Enhancements
"""

import asyncio
import logging
import time
from typing import Dict, Optional, Any, List, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import weakref

logger = logging.getLogger(__name__)


class ProgressStatus(Enum):
    """Status of a progress-tracked operation"""
    PENDING = "pending"
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    COMPLETING = "completing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class ProgressUpdate:
    """A single progress update"""
    operation_id: str
    status: ProgressStatus
    progress_percent: float  # 0.0 to 100.0
    current_step: str
    total_steps: Optional[int] = None
    current_step_number: Optional[int] = None
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    estimated_completion_time: Optional[datetime] = None


@dataclass
class ProgressTracker:
    """Tracks progress for a single operation"""
    operation_id: str
    operation_name: str
    total_steps: Optional[int] = None
    current_step_number: int = 0
    current_step: str = "Starting"
    progress_percent: float = 0.0
    status: ProgressStatus = ProgressStatus.PENDING
    start_time: datetime = field(default_factory=datetime.now)
    last_update_time: datetime = field(default_factory=datetime.now)
    estimated_duration_seconds: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)
    
    # Callbacks for progress updates
    _update_callbacks: List[Callable[[ProgressUpdate], None]] = field(default_factory=list, init=False)
    _cancellation_requested: bool = field(default=False, init=False)
    
    def add_callback(self, callback: Callable[[ProgressUpdate], None]):
        """Add a callback to be called on progress updates"""
        self._update_callbacks.append(callback)
    
    def remove_callback(self, callback: Callable[[ProgressUpdate], None]):
        """Remove a progress update callback"""
        if callback in self._update_callbacks:
            self._update_callbacks.remove(callback)
    
    def request_cancellation(self):
        """Request cancellation of the operation"""
        self._cancellation_requested = True
        self.update_status(ProgressStatus.CANCELLED, "Operation cancelled by user")
    
    def is_cancellation_requested(self) -> bool:
        """Check if cancellation has been requested"""
        return self._cancellation_requested
    
    def update_progress(self, 
                       progress_percent: float, 
                       message: str = "", 
                       details: Optional[Dict[str, Any]] = None):
        """Update the progress percentage and message"""
        self.progress_percent = max(0.0, min(100.0, progress_percent))
        self.last_update_time = datetime.now()
        
        if details:
            self.details.update(details)
        
        # Estimate completion time if we have enough data
        if self.progress_percent > 0 and self.progress_percent < 100:
            elapsed_seconds = (self.last_update_time - self.start_time).total_seconds()
            if elapsed_seconds > 0:
                estimated_total_seconds = elapsed_seconds * (100.0 / self.progress_percent)
                remaining_seconds = estimated_total_seconds - elapsed_seconds
                estimated_completion = self.last_update_time.timestamp() + remaining_seconds
                estimated_completion_time = datetime.fromtimestamp(estimated_completion)
            else:
                estimated_completion_time = None
        else:
            estimated_completion_time = None
        
        self._notify_callbacks(message, estimated_completion_time)
    
    def update_step(self, 
                   step_name: str, 
                   step_number: Optional[int] = None, 
                   message: str = "",
                   details: Optional[Dict[str, Any]] = None):
        """Update the current step"""
        self.current_step = step_name
        self.last_update_time = datetime.now()
        
        if step_number is not None:
            self.current_step_number = step_number
        else:
            self.current_step_number += 1
        
        # Calculate progress based on step if total_steps is known
        if self.total_steps and self.total_steps > 0:
            self.progress_percent = (self.current_step_number / self.total_steps) * 100.0
        
        if details:
            self.details.update(details)
        
        self._notify_callbacks(message or f"Step {self.current_step_number}: {step_name}")
    
    def update_status(self, 
                     status: ProgressStatus, 
                     message: str = "",
                     details: Optional[Dict[str, Any]] = None):
        """Update the operation status"""
        self.status = status
        self.last_update_time = datetime.now()
        
        if details:
            self.details.update(details)
        
        # Set progress based on status
        if status == ProgressStatus.COMPLETED:
            self.progress_percent = 100.0
        elif status == ProgressStatus.FAILED or status == ProgressStatus.CANCELLED:
            # Keep current progress for failed/cancelled operations
            pass
        elif status == ProgressStatus.STARTING:
            self.progress_percent = 0.0
        
        self._notify_callbacks(message)
    
    def complete(self, message: str = "Operation completed successfully"):
        """Mark the operation as completed"""
        self.update_status(ProgressStatus.COMPLETED, message)
    
    def fail(self, error_message: str, details: Optional[Dict[str, Any]] = None):
        """Mark the operation as failed"""
        self.update_status(ProgressStatus.FAILED, f"Operation failed: {error_message}", details)
    
    def get_current_update(self) -> ProgressUpdate:
        """Get the current progress state as an update"""
        estimated_completion_time = None
        if self.progress_percent > 0 and self.progress_percent < 100:
            elapsed_seconds = (self.last_update_time - self.start_time).total_seconds()
            if elapsed_seconds > 0:
                estimated_total_seconds = elapsed_seconds * (100.0 / self.progress_percent)
                remaining_seconds = estimated_total_seconds - elapsed_seconds
                estimated_completion = self.last_update_time.timestamp() + remaining_seconds
                estimated_completion_time = datetime.fromtimestamp(estimated_completion)
        
        return ProgressUpdate(
            operation_id=self.operation_id,
            status=self.status,
            progress_percent=self.progress_percent,
            current_step=self.current_step,
            total_steps=self.total_steps,
            current_step_number=self.current_step_number,
            message=f"{self.operation_name}: {self.current_step}",
            details=self.details.copy(),
            timestamp=self.last_update_time,
            estimated_completion_time=estimated_completion_time
        )
    
    def _notify_callbacks(self, message: str = "", estimated_completion_time: Optional[datetime] = None):
        """Notify all registered callbacks of the progress update"""
        update = ProgressUpdate(
            operation_id=self.operation_id,
            status=self.status,
            progress_percent=self.progress_percent,
            current_step=self.current_step,
            total_steps=self.total_steps,
            current_step_number=self.current_step_number,
            message=message or f"{self.operation_name}: {self.current_step}",
            details=self.details.copy(),
            timestamp=self.last_update_time,
            estimated_completion_time=estimated_completion_time
        )
        
        # Call all callbacks (safely)
        for callback in self._update_callbacks[:]:  # Copy list to avoid modification during iteration
            try:
                callback(update)
            except Exception as e:
                logger.error(f"Error in progress callback: {e}")


class ProgressManager:
    """Manages progress tracking for multiple operations"""
    
    def __init__(self):
        self.active_trackers: Dict[str, ProgressTracker] = {}
        self.completed_trackers: List[ProgressTracker] = []
        self.max_completed_history = 100
        
        # Global callbacks for all operations
        self._global_callbacks: List[Callable[[ProgressUpdate], None]] = []
    
    def create_tracker(self, 
                      operation_id: str, 
                      operation_name: str,
                      total_steps: Optional[int] = None,
                      estimated_duration_seconds: Optional[float] = None) -> ProgressTracker:
        """Create a new progress tracker"""
        if operation_id in self.active_trackers:
            logger.warning(f"Progress tracker for operation {operation_id} already exists")
            return self.active_trackers[operation_id]
        
        tracker = ProgressTracker(
            operation_id=operation_id,
            operation_name=operation_name,
            total_steps=total_steps,
            estimated_duration_seconds=estimated_duration_seconds
        )
        
        # Add global callbacks to the tracker
        for callback in self._global_callbacks:
            tracker.add_callback(callback)
        
        self.active_trackers[operation_id] = tracker
        
        # Notify of tracker creation
        tracker.update_status(ProgressStatus.STARTING, f"Started {operation_name}")
        
        logger.debug(f"Created progress tracker for operation {operation_id}: {operation_name}")
        return tracker
    
    def get_tracker(self, operation_id: str) -> Optional[ProgressTracker]:
        """Get an active progress tracker"""
        return self.active_trackers.get(operation_id)
    
    def complete_tracker(self, operation_id: str, message: str = "Operation completed"):
        """Complete and archive a progress tracker"""
        if operation_id not in self.active_trackers:
            logger.warning(f"No active tracker found for operation {operation_id}")
            return
        
        tracker = self.active_trackers[operation_id]
        tracker.complete(message)
        
        # Move to completed trackers
        del self.active_trackers[operation_id]
        self.completed_trackers.append(tracker)
        
        # Maintain history limit
        if len(self.completed_trackers) > self.max_completed_history:
            self.completed_trackers.pop(0)
        
        logger.debug(f"Completed progress tracker for operation {operation_id}")
    
    def fail_tracker(self, operation_id: str, error_message: str, details: Optional[Dict[str, Any]] = None):
        """Fail and archive a progress tracker"""
        if operation_id not in self.active_trackers:
            logger.warning(f"No active tracker found for operation {operation_id}")
            return
        
        tracker = self.active_trackers[operation_id]
        tracker.fail(error_message, details)
        
        # Move to completed trackers
        del self.active_trackers[operation_id]
        self.completed_trackers.append(tracker)
        
        # Maintain history limit
        if len(self.completed_trackers) > self.max_completed_history:
            self.completed_trackers.pop(0)
        
        logger.debug(f"Failed progress tracker for operation {operation_id}: {error_message}")
    
    def cancel_tracker(self, operation_id: str):
        """Cancel a progress tracker"""
        if operation_id not in self.active_trackers:
            logger.warning(f"No active tracker found for operation {operation_id}")
            return
        
        tracker = self.active_trackers[operation_id]
        tracker.request_cancellation()
        
        # Move to completed trackers
        del self.active_trackers[operation_id]
        self.completed_trackers.append(tracker)
        
        # Maintain history limit
        if len(self.completed_trackers) > self.max_completed_history:
            self.completed_trackers.pop(0)
        
        logger.debug(f"Cancelled progress tracker for operation {operation_id}")
    
    def get_all_active_updates(self) -> List[ProgressUpdate]:
        """Get current progress updates for all active operations"""
        return [tracker.get_current_update() for tracker in self.active_trackers.values()]
    
    def get_recent_completed_updates(self, limit: int = 10) -> List[ProgressUpdate]:
        """Get recent completed operation updates"""
        recent_trackers = self.completed_trackers[-limit:] if self.completed_trackers else []
        return [tracker.get_current_update() for tracker in recent_trackers]
    
    def add_global_callback(self, callback: Callable[[ProgressUpdate], None]):
        """Add a global callback for all progress updates"""
        self._global_callbacks.append(callback)
        
        # Add to existing active trackers
        for tracker in self.active_trackers.values():
            tracker.add_callback(callback)
    
    def remove_global_callback(self, callback: Callable[[ProgressUpdate], None]):
        """Remove a global callback"""
        if callback in self._global_callbacks:
            self._global_callbacks.remove(callback)
        
        # Remove from existing active trackers
        for tracker in self.active_trackers.values():
            tracker.remove_callback(callback)
    
    def cleanup_old_trackers(self):
        """Clean up old completed trackers"""
        if len(self.completed_trackers) > self.max_completed_history:
            excess_count = len(self.completed_trackers) - self.max_completed_history
            self.completed_trackers = self.completed_trackers[excess_count:]
            logger.debug(f"Cleaned up {excess_count} old progress trackers")


# Global progress manager instance
_global_progress_manager: Optional[ProgressManager] = None


def get_progress_manager() -> ProgressManager:
    """Get the global progress manager instance"""
    global _global_progress_manager
    
    if _global_progress_manager is None:
        _global_progress_manager = ProgressManager()
    
    return _global_progress_manager


# Convenience functions for common progress tracking patterns

async def track_file_upload_progress(operation_id: str, 
                                    filename: str, 
                                    file_size_bytes: int,
                                    upload_func: Callable[[], Any]) -> Any:
    """Track progress for a file upload operation"""
    manager = get_progress_manager()
    tracker = manager.create_tracker(
        operation_id=operation_id,
        operation_name=f"Uploading {filename}",
        total_steps=4  # Upload, Store, Process, Complete
    )
    
    try:
        tracker.update_step("Preparing upload", 1, f"Preparing to upload {filename} ({file_size_bytes} bytes)")
        
        # Check for cancellation
        if tracker.is_cancellation_requested():
            manager.cancel_tracker(operation_id)
            return None
        
        tracker.update_step("Uploading file", 2, "Transferring file data")
        
        # Perform the actual upload
        result = await upload_func()
        
        # Check for cancellation
        if tracker.is_cancellation_requested():
            manager.cancel_tracker(operation_id)
            return None
        
        tracker.update_step("Processing file", 3, "Processing uploaded file")
        
        tracker.update_step("Finalizing", 4, "Completing upload process")
        
        manager.complete_tracker(operation_id, f"Successfully uploaded {filename}")
        return result
        
    except Exception as e:
        manager.fail_tracker(operation_id, str(e), {"filename": filename, "file_size": file_size_bytes})
        raise


async def track_file_conversion_progress(operation_id: str, 
                                       filename: str,
                                       conversion_func: Callable[[], Any]) -> Any:
    """Track progress for a file conversion operation"""
    manager = get_progress_manager()
    tracker = manager.create_tracker(
        operation_id=operation_id,
        operation_name=f"Converting {filename}",
        total_steps=3  # Analyze, Convert, Finalize
    )
    
    try:
        tracker.update_step("Analyzing file", 1, f"Analyzing {filename} for conversion")
        
        # Check for cancellation
        if tracker.is_cancellation_requested():
            manager.cancel_tracker(operation_id)
            return None
        
        tracker.update_step("Converting content", 2, "Converting file to markdown")
        
        # Perform the actual conversion
        result = await conversion_func()
        
        # Check for cancellation
        if tracker.is_cancellation_requested():
            manager.cancel_tracker(operation_id)
            return None
        
        tracker.update_step("Finalizing conversion", 3, "Completing conversion process")
        
        manager.complete_tracker(operation_id, f"Successfully converted {filename}")
        return result
        
    except Exception as e:
        manager.fail_tracker(operation_id, str(e), {"filename": filename})
        raise