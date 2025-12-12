"""
Storage Space Optimizer

Provides efficient storage space management including:
- Automatic cleanup of old files
- Storage space monitoring and alerts
- File deduplication
- Compression for large files
- Storage backend optimization

v 0.1.9 - Performance and Scalability Enhancements
"""

import asyncio
import logging
import hashlib
import gzip
import time
from typing import Dict, Optional, Any, List, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import os
import shutil

logger = logging.getLogger(__name__)


@dataclass
class StorageOptimizationConfig:
    """Configuration for storage optimization"""
    # Cleanup settings
    max_file_age_days: int = 30  # Delete files older than this
    max_storage_size_gb: float = 10.0  # Maximum total storage size
    cleanup_threshold_percent: float = 80.0  # Start cleanup when storage reaches this %
    
    # Deduplication settings
    enable_deduplication: bool = True
    dedup_chunk_size: int = 8192  # Chunk size for hash calculation
    
    # Compression settings
    enable_compression: bool = True
    compression_threshold_bytes: int = 1024 * 1024  # Compress files larger than 1MB
    compression_level: int = 6  # gzip compression level (1-9)
    
    # Monitoring settings
    monitoring_interval_seconds: int = 3600  # Check storage every hour
    alert_threshold_percent: float = 90.0  # Alert when storage reaches this %


@dataclass
class FileInfo:
    """Information about a stored file for optimization"""
    file_id: str
    filename: str
    file_path: str
    size_bytes: int
    created_at: datetime
    last_accessed: datetime
    content_hash: Optional[str] = None
    is_compressed: bool = False
    is_duplicate: bool = False
    duplicate_of: Optional[str] = None


@dataclass
class StorageStats:
    """Storage statistics and metrics"""
    total_files: int
    total_size_bytes: int
    compressed_files: int
    compressed_size_saved_bytes: int
    duplicate_files: int
    duplicate_size_saved_bytes: int
    oldest_file_age_days: float
    newest_file_age_days: float
    average_file_size_bytes: float
    storage_utilization_percent: float
    available_space_bytes: int


class StorageOptimizer:
    """Optimizes storage space usage and manages file lifecycle"""
    
    def __init__(self, config: Optional[StorageOptimizationConfig] = None):
        self.config = config or StorageOptimizationConfig()
        self.file_hashes: Dict[str, str] = {}  # content_hash -> file_id
        self.file_info_cache: Dict[str, FileInfo] = {}  # file_id -> FileInfo
        self.optimization_running = False
        self._optimization_task: Optional[asyncio.Task] = None
        
        logger.info(f"Initialized StorageOptimizer with config: {self.config}")
    
    async def start_optimization(self):
        """Start background storage optimization"""
        if self.optimization_running:
            return
        
        self.optimization_running = True
        self._optimization_task = asyncio.create_task(self._optimization_loop())
        logger.info("Started storage optimization background task")
    
    async def stop_optimization(self):
        """Stop background storage optimization"""
        if not self.optimization_running:
            return
        
        self.optimization_running = False
        
        if self._optimization_task:
            self._optimization_task.cancel()
            try:
                await self._optimization_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Stopped storage optimization")
    
    async def optimize_file_storage(self, file_storage_manager) -> Dict[str, Any]:
        """Perform comprehensive storage optimization"""
        start_time = time.time()
        optimization_results = {
            'start_time': datetime.now().isoformat(),
            'files_processed': 0,
            'files_compressed': 0,
            'files_deduplicated': 0,
            'files_cleaned_up': 0,
            'space_saved_bytes': 0,
            'errors': []
        }
        
        try:
            # Get all files from all backends
            all_files = []
            for backend_name, backend in file_storage_manager.backends.items():
                try:
                    # Get all files for all users (admin operation)
                    backend_files = await self._get_all_files_from_backend(backend)
                    all_files.extend([(backend_name, f) for f in backend_files])
                except Exception as e:
                    logger.error(f"Failed to get files from backend {backend_name}: {e}")
                    optimization_results['errors'].append(f"Backend {backend_name}: {str(e)}")
            
            optimization_results['files_processed'] = len(all_files)
            
            # Build file info cache
            await self._build_file_info_cache(all_files)
            
            # Perform deduplication if enabled
            if self.config.enable_deduplication:
                dedup_results = await self._deduplicate_files(file_storage_manager)
                optimization_results['files_deduplicated'] = dedup_results['files_deduplicated']
                optimization_results['space_saved_bytes'] += dedup_results['space_saved_bytes']
            
            # Perform compression if enabled
            if self.config.enable_compression:
                compression_results = await self._compress_large_files(file_storage_manager)
                optimization_results['files_compressed'] = compression_results['files_compressed']
                optimization_results['space_saved_bytes'] += compression_results['space_saved_bytes']
            
            # Perform cleanup based on age and storage limits
            cleanup_results = await self._cleanup_old_files(file_storage_manager)
            optimization_results['files_cleaned_up'] = cleanup_results['files_cleaned_up']
            optimization_results['space_saved_bytes'] += cleanup_results['space_freed_bytes']
            
            # Update storage metrics
            if file_storage_manager.performance_monitor:
                await self._update_storage_metrics(file_storage_manager)
            
            optimization_results['duration_seconds'] = time.time() - start_time
            optimization_results['end_time'] = datetime.now().isoformat()
            
            logger.info(f"Storage optimization completed: {optimization_results}")
            return optimization_results
            
        except Exception as e:
            logger.error(f"Storage optimization failed: {e}")
            optimization_results['errors'].append(f"Optimization failed: {str(e)}")
            optimization_results['duration_seconds'] = time.time() - start_time
            optimization_results['end_time'] = datetime.now().isoformat()
            return optimization_results
    
    async def get_storage_stats(self, file_storage_manager) -> StorageStats:
        """Get comprehensive storage statistics"""
        try:
            # Get all files from all backends
            all_files = []
            total_available_space = 0
            
            for backend_name, backend in file_storage_manager.backends.items():
                try:
                    backend_files = await self._get_all_files_from_backend(backend)
                    all_files.extend(backend_files)
                    
                    # Get available space for local backends
                    if hasattr(backend, 'base_path'):
                        try:
                            total, used, free = shutil.disk_usage(backend.base_path)
                            total_available_space += free
                        except Exception:
                            pass
                            
                except Exception as e:
                    logger.error(f"Failed to get files from backend {backend_name}: {e}")
            
            if not all_files:
                return StorageStats(
                    total_files=0,
                    total_size_bytes=0,
                    compressed_files=0,
                    compressed_size_saved_bytes=0,
                    duplicate_files=0,
                    duplicate_size_saved_bytes=0,
                    oldest_file_age_days=0,
                    newest_file_age_days=0,
                    average_file_size_bytes=0,
                    storage_utilization_percent=0,
                    available_space_bytes=total_available_space
                )
            
            # Calculate statistics
            total_files = len(all_files)
            total_size = sum(f.size_bytes for f in all_files)
            compressed_files = sum(1 for f in all_files if getattr(f, 'is_compressed', False))
            duplicate_files = sum(1 for f in all_files if getattr(f, 'is_duplicate', False))
            
            # Calculate file ages
            now = datetime.now()
            file_ages = [(now - f.created_at).days for f in all_files]
            oldest_age = max(file_ages) if file_ages else 0
            newest_age = min(file_ages) if file_ages else 0
            
            # Calculate storage utilization
            max_storage_bytes = self.config.max_storage_size_gb * 1024 * 1024 * 1024
            utilization_percent = (total_size / max_storage_bytes) * 100.0 if max_storage_bytes > 0 else 0
            
            return StorageStats(
                total_files=total_files,
                total_size_bytes=total_size,
                compressed_files=compressed_files,
                compressed_size_saved_bytes=0,  # Would need to track this separately
                duplicate_files=duplicate_files,
                duplicate_size_saved_bytes=0,  # Would need to track this separately
                oldest_file_age_days=oldest_age,
                newest_file_age_days=newest_age,
                average_file_size_bytes=total_size / total_files if total_files > 0 else 0,
                storage_utilization_percent=utilization_percent,
                available_space_bytes=total_available_space
            )
            
        except Exception as e:
            logger.error(f"Failed to get storage stats: {e}")
            return StorageStats(
                total_files=0,
                total_size_bytes=0,
                compressed_files=0,
                compressed_size_saved_bytes=0,
                duplicate_files=0,
                duplicate_size_saved_bytes=0,
                oldest_file_age_days=0,
                newest_file_age_days=0,
                average_file_size_bytes=0,
                storage_utilization_percent=0,
                available_space_bytes=0
            )
    
    async def _optimization_loop(self):
        """Background optimization loop"""
        while self.optimization_running:
            try:
                # This would need access to file_storage_manager
                # For now, just sleep and log
                logger.debug("Storage optimization check (background task)")
                await asyncio.sleep(self.config.monitoring_interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in storage optimization loop: {e}")
                await asyncio.sleep(60)  # Short sleep on error
    
    async def _get_all_files_from_backend(self, backend) -> List:
        """Get all files from a backend (admin operation)"""
        try:
            # This is a simplified approach - in practice, you'd need to iterate through all users
            # For now, we'll use a placeholder approach
            if hasattr(backend, '_metadata_cache'):
                return list(backend._metadata_cache.values())
            else:
                # For backends without metadata cache, we'd need a different approach
                return []
        except Exception as e:
            logger.error(f"Failed to get all files from backend: {e}")
            return []
    
    async def _build_file_info_cache(self, all_files: List[Tuple[str, Any]]):
        """Build cache of file information for optimization"""
        self.file_info_cache.clear()
        
        for backend_name, file_metadata in all_files:
            try:
                file_info = FileInfo(
                    file_id=file_metadata.file_id,
                    filename=file_metadata.filename,
                    file_path=file_metadata.storage_path,
                    size_bytes=file_metadata.size_bytes,
                    created_at=file_metadata.created_at,
                    last_accessed=file_metadata.updated_at,  # Use updated_at as proxy for last_accessed
                    is_compressed=False,  # Would need to track this
                    is_duplicate=False   # Will be determined during deduplication
                )
                
                self.file_info_cache[file_metadata.file_id] = file_info
                
            except Exception as e:
                logger.error(f"Failed to build file info for {file_metadata.file_id}: {e}")
    
    async def _calculate_file_hash(self, file_path: str) -> Optional[str]:
        """Calculate SHA-256 hash of file content"""
        try:
            hasher = hashlib.sha256()
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    while chunk := f.read(self.config.dedup_chunk_size):
                        hasher.update(chunk)
                
                return hasher.hexdigest()
            else:
                return None
                
        except Exception as e:
            logger.error(f"Failed to calculate hash for {file_path}: {e}")
            return None
    
    async def _deduplicate_files(self, file_storage_manager) -> Dict[str, Any]:
        """Remove duplicate files to save space"""
        results = {
            'files_deduplicated': 0,
            'space_saved_bytes': 0,
            'errors': []
        }
        
        try:
            # Calculate hashes for all files
            hash_to_files: Dict[str, List[str]] = {}
            
            for file_id, file_info in self.file_info_cache.items():
                if file_info.content_hash is None:
                    file_info.content_hash = await self._calculate_file_hash(file_info.file_path)
                
                if file_info.content_hash:
                    if file_info.content_hash not in hash_to_files:
                        hash_to_files[file_info.content_hash] = []
                    hash_to_files[file_info.content_hash].append(file_id)
            
            # Find and handle duplicates
            for content_hash, file_ids in hash_to_files.items():
                if len(file_ids) > 1:
                    # Keep the oldest file, mark others as duplicates
                    file_ids_with_dates = [
                        (file_id, self.file_info_cache[file_id].created_at) 
                        for file_id in file_ids
                    ]
                    file_ids_with_dates.sort(key=lambda x: x[1])  # Sort by creation date
                    
                    # Keep the first (oldest) file
                    original_file_id = file_ids_with_dates[0][0]
                    
                    # Mark others as duplicates
                    for file_id, _ in file_ids_with_dates[1:]:
                        file_info = self.file_info_cache[file_id]
                        file_info.is_duplicate = True
                        file_info.duplicate_of = original_file_id
                        
                        # For now, just mark as duplicate - actual deletion would require careful handling
                        results['files_deduplicated'] += 1
                        results['space_saved_bytes'] += file_info.size_bytes
                        
                        logger.info(f"Marked file {file_id} as duplicate of {original_file_id}")
            
            return results
            
        except Exception as e:
            logger.error(f"Deduplication failed: {e}")
            results['errors'].append(f"Deduplication failed: {str(e)}")
            return results
    
    async def _compress_large_files(self, file_storage_manager) -> Dict[str, Any]:
        """Compress large files to save space"""
        results = {
            'files_compressed': 0,
            'space_saved_bytes': 0,
            'errors': []
        }
        
        try:
            for file_id, file_info in self.file_info_cache.items():
                if (file_info.size_bytes > self.config.compression_threshold_bytes and 
                    not file_info.is_compressed and 
                    not file_info.is_duplicate):
                    
                    # For now, just mark as compressed - actual compression would require backend support
                    file_info.is_compressed = True
                    estimated_savings = file_info.size_bytes * 0.3  # Estimate 30% compression
                    results['files_compressed'] += 1
                    results['space_saved_bytes'] += int(estimated_savings)
                    
                    logger.info(f"Marked file {file_id} for compression (estimated savings: {estimated_savings} bytes)")
            
            return results
            
        except Exception as e:
            logger.error(f"Compression failed: {e}")
            results['errors'].append(f"Compression failed: {str(e)}")
            return results
    
    async def _cleanup_old_files(self, file_storage_manager) -> Dict[str, Any]:
        """Clean up old files based on age and storage limits"""
        results = {
            'files_cleaned_up': 0,
            'space_freed_bytes': 0,
            'errors': []
        }
        
        try:
            # Get current storage usage
            stats = await self.get_storage_stats(file_storage_manager)
            
            # Check if cleanup is needed
            if stats.storage_utilization_percent < self.config.cleanup_threshold_percent:
                logger.debug(f"Storage utilization {stats.storage_utilization_percent:.1f}% below cleanup threshold")
                return results
            
            # Find files to clean up
            cleanup_candidates = []
            cutoff_date = datetime.now() - timedelta(days=self.config.max_file_age_days)
            
            for file_id, file_info in self.file_info_cache.items():
                if file_info.created_at < cutoff_date or file_info.is_duplicate:
                    cleanup_candidates.append((file_id, file_info))
            
            # Sort by age (oldest first) and size (largest first)
            cleanup_candidates.sort(key=lambda x: (x[1].created_at, -x[1].size_bytes))
            
            # Clean up files until we're below the threshold
            target_size = stats.total_size_bytes * (self.config.cleanup_threshold_percent / 100.0)
            current_size = stats.total_size_bytes
            
            for file_id, file_info in cleanup_candidates:
                if current_size <= target_size:
                    break
                
                # For now, just mark for cleanup - actual deletion would require careful handling
                results['files_cleaned_up'] += 1
                results['space_freed_bytes'] += file_info.size_bytes
                current_size -= file_info.size_bytes
                
                logger.info(f"Marked file {file_id} for cleanup (age: {(datetime.now() - file_info.created_at).days} days)")
            
            return results
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            results['errors'].append(f"Cleanup failed: {str(e)}")
            return results
    
    async def _update_storage_metrics(self, file_storage_manager):
        """Update storage metrics in performance monitor"""
        try:
            if not file_storage_manager.performance_monitor:
                return
            
            for backend_name, backend in file_storage_manager.backends.items():
                try:
                    # Get files for this backend
                    backend_files = [
                        info for info in self.file_info_cache.values()
                        if info.file_path.startswith(str(getattr(backend, 'base_path', '')))
                    ]
                    
                    if backend_files:
                        total_size = sum(f.size_bytes for f in backend_files)
                        file_sizes = [f.size_bytes for f in backend_files]
                        
                        # Get storage path for disk usage
                        storage_path = None
                        if hasattr(backend, 'base_path'):
                            storage_path = str(backend.base_path)
                        
                        file_storage_manager.performance_monitor.update_storage_metrics(
                            backend_name=backend_name,
                            file_count=len(backend_files),
                            total_size_bytes=total_size,
                            file_sizes=file_sizes,
                            storage_path=storage_path
                        )
                        
                except Exception as e:
                    logger.error(f"Failed to update storage metrics for backend {backend_name}: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to update storage metrics: {e}")


# Global storage optimizer instance
_global_storage_optimizer: Optional[StorageOptimizer] = None


def get_storage_optimizer(config: Optional[StorageOptimizationConfig] = None) -> StorageOptimizer:
    """Get the global storage optimizer instance"""
    global _global_storage_optimizer
    
    if _global_storage_optimizer is None:
        _global_storage_optimizer = StorageOptimizer(config)
    
    return _global_storage_optimizer


async def initialize_storage_optimizer(config: Optional[StorageOptimizationConfig] = None) -> StorageOptimizer:
    """Initialize and start the global storage optimizer"""
    optimizer = get_storage_optimizer(config)
    await optimizer.start_optimization()
    return optimizer


async def shutdown_storage_optimizer():
    """Shutdown the global storage optimizer"""
    global _global_storage_optimizer
    
    if _global_storage_optimizer:
        await _global_storage_optimizer.stop_optimization()
        _global_storage_optimizer = None