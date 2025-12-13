"""
File System Management

Comprehensive file management system for the Agent Framework.
This module provides everything needed for file processing, storage, and management:

- File Input Processing: utilities for handling FileDataInputPart
- File Storage Management: multi-backend storage with routing
- File Storage Factory: automatic configuration and setup

v 0.1.9 - Consolidated module
"""

import os
import uuid
import base64
import logging
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING
from datetime import datetime

from ..core.agent_interface import (
    StructuredAgentInput, 
    FileDataInputPart, 
    TextInputPart,
    AgentInputPartUnion
)

# Import comprehensive error handling system
from agent_framework.monitoring.error_handling import (
    ErrorHandler,
    FileProcessingError,
    FileProcessingErrorType,
    ErrorSeverity,
    StorageError,
    ConversionError,
    MultimodalProcessingError,
    ValidationError,
    ProcessingIssue,
    ErrorHandlingResult,
    UserFeedbackGenerator,
    GracefulDegradationHandler
)

# Import performance and resource management
from agent_framework.monitoring.resource_manager import (
    ResourceManager, 
    OperationType, 
    get_resource_manager,
    initialize_resource_manager
)
from agent_framework.monitoring.performance_monitor import (
    PerformanceMonitor,
    get_performance_monitor,
    initialize_performance_monitor
)
from agent_framework.monitoring.progress_tracker import (
    ProgressManager,
    ProgressStatus,
    get_progress_manager,
    track_file_upload_progress,
    track_file_conversion_progress
)
from agent_framework.storage.storage_optimizer import (
    StorageOptimizer,
    StorageOptimizationConfig,
    get_storage_optimizer,
    initialize_storage_optimizer
)

# Type checking imports to avoid circular dependencies
if TYPE_CHECKING:
    from .file_storages import FileStorageInterface, FileMetadata

logger = logging.getLogger(__name__)


# ===== FILE INPUT PROCESSING UTILITIES =====

async def process_file_inputs(
    agent_input: StructuredAgentInput,
    file_storage_manager: Optional['FileStorageManager'] = None,
    user_id: str = "default_user",
    session_id: str = "default_session",
    store_files: bool = True,
    include_text_content: bool = True,
    convert_to_markdown: bool = True,
    enable_multimodal_processing: bool = True,
    enable_progress_tracking: bool = True
) -> Tuple[StructuredAgentInput, List[Dict[str, Any]]]:
    """
    Process FileDataInputPart in agent input with enhanced dual file storage, comprehensive metadata reporting, 
    performance monitoring, and progress tracking.
    
    This enhanced utility function:
    1. Finds all FileDataInputPart in the agent input
    2. Decodes their base64 content
    3. Stores both original and markdown versions using dual file storage workflow
    4. Provides comprehensive metadata reporting including conversion status and multimodal info
    5. Implements enhanced error handling with user-friendly feedback
    6. Tracks progress and performance metrics for all operations
    7. Converts them to TextInputPart with appropriate content
    8. Returns modified input and enhanced file metadata
    
    Enhanced Features:
    - Dual file storage (original + markdown versions)
    - Comprehensive processing status reporting
    - Enhanced error handling with user-friendly messages
    - Multimodal image analysis preparation
    - Detailed capability reporting
    - Progress tracking for long-running operations
    - Performance monitoring and metrics collection
    - Resource management and concurrent processing limits
    
    Args:
        agent_input: The original StructuredAgentInput
        file_storage_manager: Optional file storage manager for persistence
        user_id: User ID for file storage
        session_id: Session ID for file storage  
        store_files: Whether to store files persistently (default: True)
        include_text_content: Whether to include text file content in the response (default: True)
        convert_to_markdown: Whether to attempt markdown conversion (default: True)
        enable_multimodal_processing: Whether to enable multimodal image processing (default: True)
        enable_progress_tracking: Whether to enable progress tracking (default: True)
        
    Returns:
        Tuple containing:
        - Modified StructuredAgentInput with FileDataInputPart converted to TextInputPart
        - List of dictionaries containing enhanced file metadata with comprehensive processing information
        
    Example:
        ```python
        # Enhanced file processing with dual storage, performance monitoring, and progress tracking
        processed_input, files = await process_file_inputs(
            agent_input, 
            self.file_storage_manager,
            user_id="user123", 
            session_id="session456",
            enable_multimodal_processing=True,
            enable_progress_tracking=True
        )
        
        # Check comprehensive processing results
        for file_info in files:
            print(f"File: {file_info['filename']}")
            print(f"  Original file ID: {file_info.get('file_id')}")
            print(f"  Markdown file ID: {file_info.get('markdown_file_id')}")
            print(f"  Conversion status: {file_info.get('conversion_status')}")
            print(f"  Processing time: {file_info.get('processing_time_ms', 0):.2f}ms")
            print(f"  Has visual content: {file_info.get('has_visual_content', False)}")
            print(f"  Available capabilities: {file_info.get('multimodal_capabilities', [])}")
            print(f"  User message: {file_info.get('user_message', '')}")
        ```
    """
    import time
    
    # Count files to process for progress tracking
    file_parts = [part for part in agent_input.parts if isinstance(part, FileDataInputPart)]
    total_files = len(file_parts)
    
    # Initialize progress tracking if enabled
    progress_manager = None
    progress_tracker = None
    if enable_progress_tracking and total_files > 0:
        progress_manager = get_progress_manager()
        operation_id = f"process_files_{session_id}_{int(time.time() * 1000)}"
        progress_tracker = progress_manager.create_tracker(
            operation_id=operation_id,
            operation_name=f"Processing {total_files} file(s)",
            total_steps=total_files + 1  # +1 for finalization
        )
        progress_tracker.update_step("Starting file processing", 0, f"Processing {total_files} files")
    
    processed_parts = []
    uploaded_files = []
    current_file_index = 0
    
    for part in agent_input.parts:
        if isinstance(part, FileDataInputPart):
            current_file_index += 1
            
            # Update progress
            if progress_tracker:
                progress_tracker.update_step(
                    f"Processing {part.filename}", 
                    current_file_index,
                    f"Processing file {current_file_index} of {total_files}: {part.filename}"
                )
                
                # Check for cancellation
                if progress_tracker.is_cancellation_requested():
                    logger.info("File processing cancelled by user")
                    if progress_manager:
                        progress_manager.cancel_tracker(progress_tracker.operation_id)
                    break
            
            try:
                # Decode base64 content
                content = base64.b64decode(part.content_base64)
                
                # Initialize comprehensive file metadata for agent context
                file_info = {
                    'filename': part.filename,
                    'content': content,
                    'mime_type': part.mime_type,
                    'size_bytes': len(content),
                    # Enhanced metadata fields
                    'file_id': None,
                    'markdown_file_id': None,
                    'conversion_status': 'not_attempted',
                    'conversion_success': False,
                    'conversion_reason': None,
                    'has_visual_content': False,
                    'multimodal_capabilities': [],
                    'multimodal_info': {},
                    'processing_errors': [],
                    'processing_warnings': [],
                    'user_message': '',
                    'capabilities_available': [],
                    'limitations': [],
                    'processing_time_ms': 0.0,
                    'storage_backend': None,
                    'versions_available': {'original': False, 'markdown': False}
                }
                uploaded_files.append(file_info)
                
                # Optionally store file persistently with enhanced dual storage and comprehensive reporting
                if store_files and file_storage_manager:
                    start_time = datetime.now()
                    try:
                        # First store the original file
                        original_file_id = await file_storage_manager.store_file(
                            content=content,
                            filename=part.filename,
                            user_id=user_id,
                            session_id=session_id,
                            mime_type=part.mime_type or "application/octet-stream",
                            is_generated=False,
                            tags=["user-uploaded", "framework-processed"]
                        )

                        if original_file_id:
                            file_info['file_id'] = original_file_id
                            file_info['versions_available']['original'] = True
                            
                            # Try markdown conversion if enabled
                            # Skip conversion if file is already markdown
                            is_already_markdown = (
                                part.mime_type in ['text/markdown', 'text/x-markdown'] or
                                part.filename.lower().endswith('.md') or
                                part.filename.lower().endswith('.markdown')
                            )
                            
                            if is_already_markdown:
                                # File is already markdown - no conversion needed
                                file_info['conversion_status'] = 'skipped'
                                file_info['conversion_reason'] = 'File is already markdown format'
                                # Store the original content as markdown_content for later use
                                try:
                                    file_info['markdown_content'] = content.decode('utf-8', errors='ignore')
                                    file_info['conversion_success'] = True  # Mark as success since we have markdown content
                                    logger.info(f"📝 File {part.filename} is already markdown, skipping conversion")
                                except Exception as decode_error:
                                    logger.warning(f"Failed to decode markdown file {part.filename}: {decode_error}")
                            elif convert_to_markdown:
                                try:
                                    # Get original content for conversion
                                    original_content, _ = await file_storage_manager.retrieve_file(original_file_id)
                                    
                                    # Convert to markdown using MarkdownConverter
                                    from agent_framework.processing.markdown_converter import markdown_converter
                                    conversion_result = await markdown_converter.convert_to_markdown(
                                        content=original_content,
                                        filename=part.filename,
                                        mime_type=part.mime_type
                                    )
                                    
                                    if conversion_result.success and conversion_result.content:
                                        # Store markdown version
                                        markdown_content = conversion_result.content.encode('utf-8')
                                        markdown_file_id = await file_storage_manager.store_file(
                                            content=markdown_content,
                                            filename=f"{part.filename}.md",
                                            user_id=user_id,
                                            session_id=session_id,
                                            mime_type="text/markdown",
                                            is_generated=True,
                                            tags=["markdown-converted", "framework-processed"]
                                        )
                                        
                                        if markdown_file_id:
                                            file_info['markdown_file_id'] = markdown_file_id
                                            file_info['versions_available']['markdown'] = True
                                            file_info['conversion_status'] = 'success'
                                            file_info['conversion_success'] = True
                                            file_info['markdown_content'] = conversion_result.content
                                    elif conversion_result.partial_content:
                                        file_info['conversion_status'] = 'partial'
                                        file_info['conversion_reason'] = "Only partial conversion possible"
                                        file_info['markdown_content'] = conversion_result.partial_content
                                    else:
                                        file_info['conversion_status'] = 'failed'
                                        file_info['conversion_reason'] = conversion_result.get_user_messages()[0] if conversion_result.get_user_messages() else "Conversion failed"
                                except Exception as md_error:
                                    logger.warning(f"Markdown conversion failed: {md_error}")
                                    file_info['conversion_status'] = 'failed'
                                    file_info['conversion_reason'] = str(md_error)
                            
                            # Try multimodal processing if enabled
                            if enable_multimodal_processing:
                                try:
                                    from agent_framework.processing.multimodal_integration import MultimodalFileStorageIntegration
                                    multimodal_integration = MultimodalFileStorageIntegration(file_storage_manager)
                                    multimodal_info = await multimodal_integration.get_multimodal_file_info(original_file_id)
                                    file_info.update({
                                        'multimodal_info': multimodal_info,
                                        'has_visual_content': multimodal_info.get('has_visual_content', False),
                                        'multimodal_capabilities': multimodal_info.get('available_capabilities', [])
                                    })
                                except ImportError:
                                    logger.warning("Multimodal integration not available")
                                except Exception as mm_error:
                                    logger.warning(f"Multimodal processing failed: {mm_error}")
                            
                            # Generate user-friendly message
                            file_info['user_message'] = _generate_processing_success_message(file_info)
                            file_info['capabilities_available'] = _get_file_capabilities(file_info)
                            
                            logger.info(f"✅ File stored successfully: {part.filename}")
                        else:
                            file_info['processing_errors'].append("Failed to store original file")
                            file_info['user_message'] = f"Failed to store {part.filename}"
                        
                        # Calculate processing time
                        processing_time = (datetime.now() - start_time).total_seconds() * 1000
                        file_info['processing_time_ms'] = processing_time
                            
                    except Exception as storage_error:
                        processing_time = (datetime.now() - start_time).total_seconds() * 1000
                        file_info['processing_time_ms'] = processing_time
                        file_info['processing_errors'].append(str(storage_error))
                        file_info['user_message'] = f"Failed to store {part.filename}: {str(storage_error)}"
                        file_info['limitations'].append("File storage failed - file not persisted")
                        logger.error(f"❌ Failed to store file {part.filename}: {storage_error}")
                        # Continue processing even if storage fails
                else:
                    if not store_files:
                        file_info['user_message'] = f"File {part.filename} processed but not stored (storage disabled)"
                        file_info['limitations'].append("File storage disabled")
                        file_info['capabilities_available'] = ["content_analysis"]
                        logger.debug(f"Skipping storage for {part.filename} (store_files=False)")
                    elif not file_storage_manager:
                        file_info['processing_errors'].append("No file storage manager provided")
                        file_info['user_message'] = f"Cannot store {part.filename}: file storage system not available"
                        file_info['limitations'].append("File storage system not available")
                        logger.error(f"❌ Cannot store {part.filename}: no file_storage_manager provided")
                
                # Convert file to enhanced text representation for the agent
                # Check if file is text-based (by mime type or extension)
                is_text_file = (
                    (part.mime_type and part.mime_type.startswith('text/')) or
                    part.filename.lower().endswith(('.md', '.markdown', '.txt', '.json', '.xml', '.csv', '.yaml', '.yml'))
                )
                
                if include_text_content and is_text_file:
                    # Text files: include content directly with enhanced metadata
                    try:
                        file_text = content.decode('utf-8', errors='ignore')
                        logger.info(f"📝 Including text content for {part.filename} ({len(file_text)} chars, mime_type={part.mime_type})")
                        
                        # Create enhanced file representation
                        file_header = f"[File: {part.filename}]"
                        if file_info.get('file_id'):
                            file_header += f" (ID: {file_info['file_id']})"
                        if file_info.get('markdown_file_id'):
                            file_header += f" (Markdown ID: {file_info['markdown_file_id']})"
                        
                        # Add processing status
                        status_info = []
                        if file_info.get('conversion_success'):
                            status_info.append("Markdown conversion: ✓")
                        elif file_info.get('conversion_status') == 'failed':
                            status_info.append(f"Markdown conversion: ❌ ({file_info.get('conversion_reason', 'unknown')})")
                        
                        if file_info.get('has_visual_content'):
                            cap_count = len(file_info.get('multimodal_capabilities', []))
                            status_info.append(f"Visual content: ✓ ({cap_count} capabilities available)")
                        
                        if status_info:
                            file_header += f"\n[Status: {' | '.join(status_info)}]"
                        
                        text_part = TextInputPart(
                            text=f"{file_header}\n{file_text}\n[End of file: {part.filename}]"
                        )
                        
                        # Add text content capability
                        if 'text_content' not in file_info['capabilities_available']:
                            file_info['capabilities_available'].append('text_content')
                            
                    except UnicodeDecodeError:
                        # Fallback if decode fails
                        file_info['processing_warnings'].append("Text content not displayable due to encoding issues")
                        text_part = TextInputPart(
                            text=f"[File uploaded: {part.filename} ({part.mime_type}, {len(content)} bytes) - content not displayable due to encoding]"
                        )
                else:
                    # Binary files or text files when include_text_content=False
                    # Check if we have markdown content to include
                    if file_info.get('conversion_success') and file_info.get('markdown_content'):
                        # Use markdown content for binary files (like PDFs)
                        file_header = f"[File: {part.filename}]"
                        if file_info.get('file_id'):
                            file_header += f" (ID: {file_info['file_id']})"
                        if file_info.get('markdown_file_id'):
                            file_header += f" (Markdown ID: {file_info['markdown_file_id']})"
                        
                        # Add processing status
                        status_info = []
                        status_info.append("Markdown conversion: ✓")
                        if file_info.get('has_visual_content'):
                            cap_count = len(file_info.get('multimodal_capabilities', []))
                            status_info.append(f"Visual content: ✓ ({cap_count} capabilities available)")
                        
                        if status_info:
                            file_header += f"\n[Status: {' | '.join(status_info)}]"
                        
                        text_part = TextInputPart(
                            text=f"{file_header}\n{file_info['markdown_content']}\n[End of file: {part.filename}]"
                        )
                        
                        # Add markdown content capability
                        if 'markdown_content' not in file_info['capabilities_available']:
                            file_info['capabilities_available'].append('markdown_content')
                        
                        logger.info(f"📄 Including markdown content for {part.filename} ({len(file_info['markdown_content'])} chars)")
                        logger.debug(f"[process_file_inputs] Created TextInputPart with {len(text_part.text)} chars for {part.filename}")
                    else:
                        # Fallback: just a reference without content
                        file_ref = f"[File uploaded: {part.filename} ({part.mime_type}, {len(content)} bytes)"
                        
                        # Add processing status to reference
                        status_parts = []
                        if file_info.get('file_id'):
                            status_parts.append(f"ID: {file_info['file_id']}")
                        if file_info.get('conversion_success'):
                            status_parts.append("Markdown: ✓")
                        elif file_info.get('conversion_status') == 'failed':
                            status_parts.append("Markdown: ❌")
                        if file_info.get('has_visual_content'):
                            status_parts.append("Visual: ✓")
                        
                        if status_parts:
                            file_ref += f" - {' | '.join(status_parts)}"
                        
                        file_ref += "]"
                        text_part = TextInputPart(text=file_ref)
                
                processed_parts.append(text_part)
                
            except Exception as e:
                logger.error(f"Failed to process file {part.filename}: {e}")
                
                # Create error file info
                error_file_info = {
                    'filename': part.filename,
                    'mime_type': part.mime_type,
                    'size_bytes': 0,
                    'file_id': None,
                    'markdown_file_id': None,
                    'conversion_status': 'error',
                    'conversion_success': False,
                    'has_visual_content': False,
                    'multimodal_capabilities': [],
                    'processing_errors': [str(e)],
                    'processing_warnings': [],
                    'user_message': f"Failed to process {part.filename}: {str(e)}",
                    'capabilities_available': [],
                    'limitations': ['File processing failed completely'],
                    'processing_time_ms': 0.0,
                    'storage_backend': None,
                    'versions_available': {'original': False, 'markdown': False}
                }
                uploaded_files.append(error_file_info)
                
                # Keep as enhanced error placeholder
                text_part = TextInputPart(
                    text=f"[File processing error: {part.filename} - {str(e)}]"
                )
                processed_parts.append(text_part)
        else:
            # Keep non-file parts as-is
            processed_parts.append(part)
    
    # Complete progress tracking
    if progress_tracker and progress_manager:
        progress_tracker.update_step(
            "Finalizing processing", 
            total_files + 1,
            f"Completed processing {len(uploaded_files)} files"
        )
        progress_manager.complete_tracker(
            progress_tracker.operation_id, 
            f"Successfully processed {len(uploaded_files)} files"
        )
    
    # Return modified agent input and file metadata
    modified_input = StructuredAgentInput(
        query=agent_input.query,
        parts=processed_parts,
        system_prompt=agent_input.system_prompt,
        agent_config=agent_input.agent_config
    )
    
    logger.info(f"[process_file_inputs] Returning modified_input with {len(processed_parts)} parts")
    for i, part in enumerate(processed_parts):
        if isinstance(part, TextInputPart):
            logger.info(f"[process_file_inputs] Part {i+1}: TextInputPart with {len(part.text)} chars")
    
    return modified_input, uploaded_files


def _generate_processing_success_message(file_info: Dict[str, Any]) -> str:
    """Generate user-friendly success message for file processing"""
    filename = file_info.get('filename', 'file')
    parts = [f"Successfully processed {filename}"]
    
    # Add storage information
    if file_info.get('file_id'):
        parts.append("stored original")
    
    # Add conversion information
    if file_info.get('conversion_success'):
        parts.append("converted to markdown")
    elif file_info.get('conversion_status') == 'failed':
        parts.append(f"markdown conversion failed ({file_info.get('conversion_reason', 'unknown reason')})")
    elif file_info.get('conversion_status') == 'disabled':
        parts.append("markdown conversion disabled")
    
    # Add multimodal information
    if file_info.get('has_visual_content'):
        capabilities_count = len(file_info.get('multimodal_capabilities', []))
        if capabilities_count > 0:
            parts.append(f"image analysis available ({capabilities_count} capabilities)")
        else:
            parts.append("image detected (analysis not available)")
    
    # Add processing time if available
    if file_info.get('processing_time_ms', 0) > 0:
        parts.append(f"processed in {file_info['processing_time_ms']:.1f}ms")
    
    return " - ".join(parts)


def _get_file_capabilities(file_info: Dict[str, Any]) -> List[str]:
    """Get list of available capabilities for a file"""
    capabilities = []
    
    # Basic file capabilities
    if file_info.get('file_id'):
        capabilities.append("file_storage")
        capabilities.append("file_retrieval")
    
    # Markdown capabilities
    if file_info.get('conversion_success'):
        capabilities.append("markdown_content")
        capabilities.append("text_analysis")
    
    # Multimodal capabilities
    if file_info.get('has_visual_content'):
        multimodal_caps = file_info.get('multimodal_capabilities', [])
        if multimodal_caps:
            capabilities.extend([f"multimodal_{cap}" for cap in multimodal_caps])
        else:
            capabilities.append("image_detected")
    
    # Text content capabilities
    mime_type = file_info.get('mime_type', '')
    if mime_type.startswith('text/'):
        capabilities.append("text_content")
    
    return capabilities


def get_file_processing_summary(uploaded_files: List[Dict[str, Any]]) -> str:
    """
    Generate a comprehensive human-readable summary of processed files with enhanced metadata.
    
    Args:
        uploaded_files: List of enhanced file metadata dictionaries from process_file_inputs
        
    Returns:
        Formatted string summarizing the files, their processing status, and capabilities
    """
    if not uploaded_files:
        return "No files uploaded."
    
    total_size = sum(f.get('size_bytes', 0) for f in uploaded_files)
    file_types = set(f.get('mime_type', 'unknown') for f in uploaded_files)
    
    # Count processing results
    successful_storage = sum(1 for f in uploaded_files if f.get('file_id'))
    multimodal_files = sum(1 for f in uploaded_files if f.get('has_visual_content', False))
    conversion_success = sum(1 for f in uploaded_files if f.get('conversion_success', False))
    conversion_failed = sum(1 for f in uploaded_files if f.get('conversion_status') == 'failed')
    processing_errors = sum(1 for f in uploaded_files if f.get('processing_errors'))
    
    # Calculate average processing time
    processing_times = [f.get('processing_time_ms', 0) for f in uploaded_files if f.get('processing_time_ms', 0) > 0]
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    
    summary_parts = [
        f"📁 {len(uploaded_files)} file(s) processed",
        f"📊 Total size: {total_size:,} bytes",
        f"🏷️ Types: {', '.join(sorted(file_types))}"
    ]
    
    # Add processing statistics
    if successful_storage > 0:
        summary_parts.append(f"💾 {successful_storage} file(s) stored successfully")
    
    if multimodal_files > 0:
        summary_parts.append(f"🖼️ {multimodal_files} file(s) with visual content")
    
    if conversion_success > 0:
        summary_parts.append(f"📝 {conversion_success} file(s) converted to markdown")
    
    if conversion_failed > 0:
        summary_parts.append(f"⚠️ {conversion_failed} file(s) failed markdown conversion")
    
    if processing_errors > 0:
        summary_parts.append(f"❌ {processing_errors} file(s) had processing errors")
    
    if avg_processing_time > 0:
        summary_parts.append(f"⏱️ Average processing time: {avg_processing_time:.1f}ms")
    
    # Show individual files if not too many
    if len(uploaded_files) <= 5:
        file_list = []
        for f in uploaded_files:
            file_desc = f"• {f['filename']} ({f.get('size_bytes', 0):,} bytes)"
            
            # Add comprehensive status indicators
            indicators = []
            
            # Storage status
            if f.get('file_id'):
                indicators.append("Stored ✓")
            else:
                indicators.append("Storage ❌")
            
            # Conversion status
            if f.get('conversion_success'):
                indicators.append("Markdown ✓")
            elif f.get('conversion_status') == 'failed':
                indicators.append("Markdown ❌")
            elif f.get('conversion_status') == 'disabled':
                indicators.append("Markdown disabled")
            
            # Multimodal status
            if f.get('has_visual_content'):
                cap_count = len(f.get('multimodal_capabilities', []))
                if cap_count > 0:
                    indicators.append(f"Visual ({cap_count} capabilities)")
                else:
                    indicators.append("Visual (no analysis)")
            
            # Versions available
            versions = f.get('versions_available', {})
            if versions.get('original') and versions.get('markdown'):
                indicators.append("Dual storage")
            elif versions.get('original'):
                indicators.append("Original only")
            
            # Processing time
            if f.get('processing_time_ms', 0) > 0:
                indicators.append(f"{f['processing_time_ms']:.1f}ms")
            
            if indicators:
                file_desc += f" [{', '.join(indicators)}]"
            
            # Add user message if available
            if f.get('user_message'):
                file_desc += f"\n    {f['user_message']}"
            
            file_list.append(file_desc)
        
        summary_parts.extend(["", "Files:"] + file_list)
    
    return "\n".join(summary_parts)


class FileInputMixin:
    """
    Mixin class that agents can inherit from to get file processing capabilities.
    
    This is an alternative to using the utility function directly.
    Agents can inherit from both AgentInterface and FileInputMixin to get
    built-in file processing.
    
    Example:
        ```python
        class MyAgent(AgentInterface, FileInputMixin):
            def __init__(self):
                self.file_storage_manager = None  # Set this up in your agent
                
            async def handle_message(self, session_id: str, agent_input: StructuredAgentInput):
                # Process files automatically
                processed_input, files = await self.process_file_inputs_mixin(
                    agent_input, session_id=session_id
                )
                # Use processed_input...
        ```
    """
    
    async def process_file_inputs_mixin(
        self,
        agent_input: StructuredAgentInput,
        session_id: str,
        user_id: str = "default_user",
        store_files: bool = True,
        include_text_content: bool = True,
        enable_multimodal_processing: bool = True
    ) -> Tuple[StructuredAgentInput, List[Dict[str, Any]]]:
        """
        Mixin method for processing file inputs.
        
        This method assumes the agent has a `file_storage_manager` attribute.
        If not available, files won't be stored but will still be processed.
        """
        file_storage_manager = getattr(self, 'file_storage_manager', None) or getattr(self, '_file_storage_manager', None)
        
        return await process_file_inputs(
            agent_input=agent_input,
            file_storage_manager=file_storage_manager,
            user_id=user_id,
            session_id=session_id,
            store_files=store_files,
            include_text_content=include_text_content,
            enable_multimodal_processing=enable_multimodal_processing
        )


# ===== FILE STORAGE MANAGER =====

class FileStorageManager:
    """Manages multiple file storage backends with intelligent routing, resource management, and performance monitoring"""
    
    def __init__(self, 
                 enable_performance_monitoring: bool = True, 
                 enable_resource_management: bool = True,
                 enable_storage_optimization: bool = True,
                 storage_optimization_config: Optional[StorageOptimizationConfig] = None):
        self.backends: Dict[str, 'FileStorageInterface'] = {}
        self.default_backend: Optional[str] = None
        self.routing_rules: Dict[str, str] = {}  # mime_type_prefix -> backend_name
        self.initialized = False
        
        # Performance and resource management
        self.enable_performance_monitoring = enable_performance_monitoring
        self.enable_resource_management = enable_resource_management
        self.enable_storage_optimization = enable_storage_optimization
        self.resource_manager: Optional[ResourceManager] = None
        self.performance_monitor: Optional[PerformanceMonitor] = None
        self.storage_optimizer: Optional[StorageOptimizer] = None
        self.progress_manager: ProgressManager = get_progress_manager()
        self.storage_optimization_config = storage_optimization_config
        
        logger.info(f"Initialized FileStorageManager (performance_monitoring={enable_performance_monitoring}, resource_management={enable_resource_management}, storage_optimization={enable_storage_optimization})")
    
    async def initialize_performance_systems(self):
        """Initialize performance monitoring, resource management, and storage optimization systems"""
        try:
            if self.enable_resource_management and not self.resource_manager:
                self.resource_manager = await initialize_resource_manager()
                logger.info("Initialized resource management system")
            
            if self.enable_performance_monitoring and not self.performance_monitor:
                self.performance_monitor = await initialize_performance_monitor()
                logger.info("Initialized performance monitoring system")
            
            if self.enable_storage_optimization and not self.storage_optimizer:
                self.storage_optimizer = await initialize_storage_optimizer(self.storage_optimization_config)
                logger.info("Initialized storage optimization system")
            
            self.initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize performance systems: {e}")
            raise
    
    async def shutdown_performance_systems(self):
        """Shutdown performance monitoring, resource management, and storage optimization systems"""
        try:
            if self.resource_manager:
                await self.resource_manager.stop()
                self.resource_manager = None
            
            if self.performance_monitor:
                await self.performance_monitor.stop_monitoring()
                self.performance_monitor = None
            
            if self.storage_optimizer:
                await self.storage_optimizer.stop_optimization()
                self.storage_optimizer = None
            
            logger.info("Shutdown performance systems")
            
        except Exception as e:
            logger.error(f"Error shutting down performance systems: {e}")

    async def register_backend(self, name: str, backend: 'FileStorageInterface', is_default: bool = False):
        """Register a storage backend"""
        try:
            await backend.initialize()
            self.backends[name] = backend
            
            if is_default or not self.default_backend:
                self.default_backend = name
            
            # Initialize performance systems if this is the first backend
            if not self.initialized:
                await self.initialize_performance_systems()
            
            logger.info(f"Registered file storage backend '{name}' (default: {is_default})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register backend '{name}': {e}")
            return False
    
    def add_routing_rule(self, mime_type_prefix: str, backend_name: str):
        """Add routing rule for specific MIME types"""
        if backend_name not in self.backends:
            raise ValueError(f"Backend '{backend_name}' not registered")
        
        self.routing_rules[mime_type_prefix] = backend_name
        logger.debug(f"Added routing rule: {mime_type_prefix} -> {backend_name}")
    
    async def store_file(self, 
                        content: bytes, 
                        filename: str, 
                        user_id: str,
                        session_id: Optional[str] = None,
                        agent_id: Optional[str] = None,
                        is_generated: bool = False,
                        mime_type: Optional[str] = None,
                        backend_name: Optional[str] = None,
                        tags: Optional[List[str]] = None,
                        custom_metadata: Optional[Dict] = None) -> str:
        """Store file using appropriate backend with comprehensive error handling, resource management, and performance monitoring"""
        
        error_handler = ErrorHandler()
        
        # Validate inputs
        if not content:
            raise ValidationError(
                error_type=FileProcessingErrorType.FILE_EMPTY,
                severity=ErrorSeverity.ERROR,
                message="Cannot store empty file content",
                user_message=f"File {filename} is empty and cannot be stored"
            )
        
        if not filename or not filename.strip():
            raise ValidationError(
                error_type=FileProcessingErrorType.FILENAME_INVALID,
                severity=ErrorSeverity.ERROR,
                message="Invalid filename provided",
                user_message="Filename is required for file storage"
            )
        
        if not user_id or not user_id.strip():
            raise ValidationError(
                error_type=FileProcessingErrorType.CONFIGURATION_ERROR,
                severity=ErrorSeverity.ERROR,
                message="User ID is required for file storage",
                user_message="User identification is required"
            )
        
        # Check if backends are available
        if not self.backends:
            raise StorageError(
                error_type=FileProcessingErrorType.STORAGE_BACKEND_UNAVAILABLE,
                severity=ErrorSeverity.CRITICAL,
                message="No storage backends registered",
                user_message="File storage system is not available",
                context={'available_backends': list(self.backends.keys())}
            )
        
        # Determine backend to use
        if not backend_name:
            # Extract content type from custom metadata if available for AI-generated content
            content_type = None
            if is_generated and custom_metadata:
                content_type = custom_metadata.get('content_type')
            backend_name = self._determine_backend(mime_type, is_generated, content_type)
        
        if backend_name not in self.backends:
            raise StorageError(
                error_type=FileProcessingErrorType.STORAGE_BACKEND_UNAVAILABLE,
                severity=ErrorSeverity.ERROR,
                message=f"Backend '{backend_name}' not found",
                user_message="Requested storage backend is not available",
                context={
                    'requested_backend': backend_name,
                    'available_backends': list(self.backends.keys())
                }
            )
        
        # Use resource management if enabled
        if self.enable_resource_management and self.resource_manager:
            async with self.resource_manager.acquire_operation_slot(
                operation_type=OperationType.STORAGE,
                file_size_bytes=len(content),
                filename=filename,
                user_id=user_id,
                session_id=session_id,
                backend_name=backend_name
            ) as operation_id:
                return await self._store_file_with_monitoring(
                    content, filename, user_id, session_id, agent_id, is_generated,
                    mime_type, backend_name, tags, custom_metadata, operation_id
                )
        else:
            # Store without resource management
            return await self._store_file_with_monitoring(
                content, filename, user_id, session_id, agent_id, is_generated,
                mime_type, backend_name, tags, custom_metadata, None
            )
    
    async def _store_file_with_monitoring(self,
                                        content: bytes,
                                        filename: str,
                                        user_id: str,
                                        session_id: Optional[str],
                                        agent_id: Optional[str],
                                        is_generated: bool,
                                        mime_type: Optional[str],
                                        backend_name: str,
                                        tags: Optional[List[str]],
                                        custom_metadata: Optional[Dict],
                                        operation_id: Optional[str]) -> str:
        """Store file with performance monitoring and progress tracking"""
        
        error_handler = ErrorHandler()
        
        # Start performance monitoring
        perf_operation_id = operation_id or f"store_{int(time.time() * 1000)}"
        if self.performance_monitor:
            self.performance_monitor.start_operation_timing(perf_operation_id)
        
        try:
            backend = self.backends[backend_name]
            
            # Import here to avoid circular import
            from .file_storages import FileMetadata
            import time
            
            # Create metadata
            file_id = str(uuid.uuid4())
            
            metadata = FileMetadata(
                file_id=file_id,
                filename=filename,
                mime_type=mime_type,
                size_bytes=len(content),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                user_id=user_id,
                session_id=session_id,
                agent_id=agent_id,
                is_generated=is_generated,
                tags=tags or [],
                custom_metadata=custom_metadata or {},
                storage_backend=backend_name,
                storage_path=""  # Will be set by the backend
            )
            
            # Store file with backend-specific error handling
            try:
                returned_file_id = await backend.store_file(content, filename, metadata)
                
                # End performance monitoring - success
                if self.performance_monitor:
                    self.performance_monitor.end_operation_timing(
                        perf_operation_id, 
                        "file_storage", 
                        success=True, 
                        bytes_processed=len(content)
                    )
                
                # Update storage metrics
                if self.performance_monitor:
                    # Get current file count and size for this backend
                    try:
                        files = await backend.list_files(user_id)
                        total_size = sum(f.size_bytes for f in files)
                        file_sizes = [f.size_bytes for f in files]
                        
                        # Get storage path for disk usage calculation
                        storage_path = None
                        if hasattr(backend, 'base_path'):
                            storage_path = str(backend.base_path)
                        
                        self.performance_monitor.update_storage_metrics(
                            backend_name=backend_name,
                            file_count=len(files),
                            total_size_bytes=total_size,
                            file_sizes=file_sizes,
                            storage_path=storage_path
                        )
                    except Exception as e:
                        logger.warning(f"Failed to update storage metrics for {backend_name}: {e}")
                
                if returned_file_id:
                    logger.info(f"✅ Successfully stored file {filename} with ID: {returned_file_id} in backend '{backend_name}'")
                    return returned_file_id
                else:
                    # Backend returned None/empty - this is unusual but not necessarily an error
                    logger.warning(f"⚠️ Backend '{backend_name}' returned empty file_id for {filename}, using generated ID")
                    return file_id  # Return the generated ID as fallback
                
            except (StorageError, ValidationError, FileProcessingError):
                # End performance monitoring - failure
                if self.performance_monitor:
                    self.performance_monitor.end_operation_timing(
                        perf_operation_id, 
                        "file_storage", 
                        success=False, 
                        bytes_processed=len(content)
                    )
                # Re-raise structured errors from backend
                raise
            except Exception as backend_error:
                # End performance monitoring - failure
                if self.performance_monitor:
                    self.performance_monitor.end_operation_timing(
                        perf_operation_id, 
                        "file_storage", 
                        success=False, 
                        bytes_processed=len(content)
                    )
                
                # Handle unexpected backend errors
                structured_error = error_handler.handle_exception(
                    exception=backend_error,
                    operation="backend_storage",
                    filename=filename,
                    context={
                        'backend_name': backend_name,
                        'file_id': file_id,
                        'file_size': len(content),
                        'user_id': user_id,
                        'is_generated': is_generated
                    }
                )
                logger.error(f"❌ Backend '{backend_name}' storage failed for {filename}: {structured_error}")
                raise structured_error
                
        except (StorageError, ValidationError, FileProcessingError):
            # Re-raise our structured errors
            raise
        except Exception as e:
            # End performance monitoring - failure
            if self.performance_monitor:
                self.performance_monitor.end_operation_timing(
                    perf_operation_id, 
                    "file_storage", 
                    success=False, 
                    bytes_processed=len(content)
                )
            
            # Handle any other unexpected errors
            structured_error = error_handler.handle_exception(
                exception=e,
                operation="file_storage_management",
                filename=filename,
                context={
                    'backend_name': backend_name,
                    'file_size': len(content) if content else 0,
                    'user_id': user_id,
                    'is_generated': is_generated
                }
            )
            logger.error(f"❌ Unexpected error in file storage management for {filename}: {structured_error}")
            raise structured_error
    
    async def retrieve_file(self, file_id: str) -> Tuple[bytes, 'FileMetadata']:
        """Retrieve file from appropriate backend with comprehensive error handling, resource management, and performance monitoring"""
        
        error_handler = ErrorHandler()
        
        # Validate file_id
        if not file_id or not file_id.strip():
            raise ValidationError(
                error_type=FileProcessingErrorType.FILENAME_INVALID,
                severity=ErrorSeverity.ERROR,
                message="Invalid file ID provided",
                user_message="File ID is required for retrieval"
            )
        
        # First, try to find the file in any backend by checking metadata
        backend_name = await self._find_file_backend(file_id)
        
        if not backend_name:
            raise StorageError(
                error_type=FileProcessingErrorType.STORAGE_READ_FAILED,
                severity=ErrorSeverity.ERROR,
                message=f"File {file_id} not found in any backend",
                user_message="File not found in storage system",
                context={
                    'file_id': file_id,
                    'available_backends': list(self.backends.keys())
                }
            )
        
        # Get file metadata to determine size for resource management
        backend = self.backends[backend_name]
        file_metadata = await backend.get_file_metadata(file_id)
        file_size = file_metadata.size_bytes if file_metadata else 0
        
        # Use resource management if enabled
        if self.enable_resource_management and self.resource_manager:
            async with self.resource_manager.acquire_operation_slot(
                operation_type=OperationType.RETRIEVAL,
                file_size_bytes=file_size,
                filename=file_metadata.filename if file_metadata else None,
                file_id=file_id,
                backend_name=backend_name
            ) as operation_id:
                return await self._retrieve_file_with_monitoring(file_id, backend_name, operation_id)
        else:
            # Retrieve without resource management
            return await self._retrieve_file_with_monitoring(file_id, backend_name, None)
    
    async def _retrieve_file_with_monitoring(self, 
                                           file_id: str, 
                                           backend_name: str, 
                                           operation_id: Optional[str]) -> Tuple[bytes, 'FileMetadata']:
        """Retrieve file with performance monitoring"""
        
        error_handler = ErrorHandler()
        
        # Start performance monitoring
        perf_operation_id = operation_id or f"retrieve_{int(time.time() * 1000)}"
        if self.performance_monitor:
            self.performance_monitor.start_operation_timing(perf_operation_id)
        
        try:
            backend = self.backends[backend_name]
            
            try:
                import time
                content, metadata = await backend.retrieve_file(file_id)
                
                # End performance monitoring - success
                if self.performance_monitor:
                    self.performance_monitor.end_operation_timing(
                        perf_operation_id, 
                        "file_retrieval", 
                        success=True, 
                        bytes_processed=len(content)
                    )
                
                logger.debug(f"✅ Retrieved file {file_id} from backend '{backend_name}' ({len(content)} bytes)")
                return content, metadata
                
            except (StorageError, ValidationError, FileProcessingError):
                # End performance monitoring - failure
                if self.performance_monitor:
                    self.performance_monitor.end_operation_timing(
                        perf_operation_id, 
                        "file_retrieval", 
                        success=False, 
                        bytes_processed=0
                    )
                # Re-raise structured errors from backend
                raise
            except Exception as backend_error:
                # End performance monitoring - failure
                if self.performance_monitor:
                    self.performance_monitor.end_operation_timing(
                        perf_operation_id, 
                        "file_retrieval", 
                        success=False, 
                        bytes_processed=0
                    )
                
                # Handle unexpected backend errors
                structured_error = error_handler.handle_exception(
                    exception=backend_error,
                    operation="backend_retrieval",
                    context={
                        'file_id': file_id,
                        'backend_name': backend_name
                    }
                )
                logger.error(f"❌ Backend '{backend_name}' retrieval failed for {file_id}: {structured_error}")
                raise structured_error
                
        except (StorageError, ValidationError, FileProcessingError):
            # Re-raise our structured errors
            raise
        except Exception as e:
            # End performance monitoring - failure
            if self.performance_monitor:
                self.performance_monitor.end_operation_timing(
                    perf_operation_id, 
                    "file_retrieval", 
                    success=False, 
                    bytes_processed=0
                )
            
            # Handle any other unexpected errors
            structured_error = error_handler.handle_exception(
                exception=e,
                operation="file_retrieval_management",
                context={'file_id': file_id}
            )
            logger.error(f"❌ Unexpected error in file retrieval management for {file_id}: {structured_error}")
            raise structured_error
    
    async def delete_file(self, file_id: str) -> bool:
        """Delete file from appropriate backend"""
        
        backend_name = await self._find_file_backend(file_id)
        
        if not backend_name:
            logger.warning(f"File {file_id} not found in any backend for deletion")
            return False
        
        backend = self.backends[backend_name]
        
        try:
            result = await backend.delete_file(file_id)
            if result:
                logger.debug(f"Deleted file {file_id} from backend '{backend_name}'")
            return result
            
        except Exception as e:
            logger.error(f"Failed to delete file {file_id} from backend '{backend_name}': {e}")
            return False
    
    async def list_files(self, 
                        user_id: str, 
                        session_id: Optional[str] = None,
                        agent_id: Optional[str] = None,
                        is_generated: Optional[bool] = None,
                        backend_name: Optional[str] = None) -> List['FileMetadata']:
        """List files with filtering across backends"""
        
        all_files = []
        
        # Determine which backends to search
        backends_to_search = []
        if backend_name:
            if backend_name in self.backends:
                backends_to_search = [backend_name]
            else:
                logger.warning(f"Backend '{backend_name}' not found")
                return []
        else:
            backends_to_search = list(self.backends.keys())
        
        # Search across specified backends
        for name in backends_to_search:
            backend = self.backends[name]
            try:
                files = await backend.list_files(user_id, session_id, agent_id, is_generated)
                all_files.extend(files)
            except Exception as e:
                logger.error(f"Failed to list files from backend '{name}': {e}")
        
        # Sort by created_at descending
        all_files.sort(key=lambda x: x.created_at, reverse=True)
        return all_files
    
    async def update_metadata(self, file_id: str, metadata_updates: Dict) -> bool:
        """Update file metadata in appropriate backend"""
        
        backend_name = await self._find_file_backend(file_id)
        
        if not backend_name:
            logger.warning(f"File {file_id} not found in any backend for metadata update")
            return False
        
        backend = self.backends[backend_name]
        
        try:
            result = await backend.update_metadata(file_id, metadata_updates)
            if result:
                logger.debug(f"Updated metadata for file {file_id} in backend '{backend_name}'")
            return result
            
        except Exception as e:
            logger.error(f"Failed to update metadata for file {file_id} in backend '{backend_name}': {e}")
            return False
    
    async def file_exists(self, file_id: str) -> bool:
        """Check if file exists in any backend"""
        
        for backend in self.backends.values():
            try:
                if await backend.file_exists(file_id):
                    return True
            except Exception as e:
                logger.debug(f"Error checking file existence in backend: {e}")
        
        return False
    
    async def get_file_metadata(self, file_id: str) -> Optional['FileMetadata']:
        """Get file metadata from appropriate backend"""
        
        backend_name = await self._find_file_backend(file_id)
        
        if not backend_name:
            return None
        
        backend = self.backends[backend_name]
        
        try:
            metadata = await backend.get_file_metadata(file_id)
            if metadata:
                logger.debug(f"Retrieved metadata for file {file_id} from backend '{backend_name}'")
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to get metadata for file {file_id} from backend '{backend_name}': {e}")
            return None
    
    async def convert_file_to_markdown(self, file_id: str) -> Optional[str]:
        """Convert file to markdown using appropriate backend (legacy method)"""
        
        backend_name = await self._find_file_backend(file_id)
        
        if not backend_name:
            logger.warning(f"File {file_id} not found in any backend for markdown conversion")
            return None
        
        backend = self.backends[backend_name]
        
        try:
            markdown_content = await backend.convert_file_to_markdown(file_id)
            if markdown_content:
                logger.info(f"✅ Successfully converted file {file_id} to markdown using backend '{backend_name}'")
            return markdown_content
            
        except Exception as e:
            logger.error(f"Failed to convert file {file_id} to markdown using backend '{backend_name}': {e}")
            return None
    
    async def get_file_processing_summary(self, file_id: str) -> Dict[str, Any]:
        """Get comprehensive processing summary for a file including conversion details"""
        
        backend_name = await self._find_file_backend(file_id)
        
        if not backend_name:
            return {
                'file_id': file_id,
                'exists': False,
                'error': 'File not found in any backend'
            }
        
        backend = self.backends[backend_name]
        
        try:
            # Get comprehensive processing status from backend
            processing_status = await backend.get_processing_status(file_id)
            
            # Add manager-level information
            processing_status.update({
                'backend_name': backend_name,
                'manager_info': {
                    'available_backends': list(self.backends.keys()),
                    'routing_rules': self.routing_rules,
                    'default_backend': self.default_backend
                }
            })
            
            return processing_status
            
        except Exception as e:
            logger.error(f"Error getting processing summary for file {file_id}: {e}")
            return {
                'file_id': file_id,
                'exists': False,
                'error': str(e),
                'backend_name': backend_name
            }

    async def store_file_with_markdown_conversion(self, 
                                                content: bytes, 
                                                filename: str, 
                                                user_id: str,
                                                session_id: Optional[str] = None,
                                                agent_id: Optional[str] = None,
                                                is_generated: bool = False,
                                                mime_type: Optional[str] = None,
                                                backend_name: Optional[str] = None,
                                                tags: Optional[List[str]] = None,
                                                custom_metadata: Optional[Dict] = None) -> Tuple[str, Optional[str]]:
        """
        Store file and automatically attempt markdown conversion, storing both versions.
        
        Returns:
            Tuple of (original_file_id, markdown_file_id) where markdown_file_id is None if conversion failed
        """
        
        # First store the original file
        original_file_id = await self.store_file(
            content=content,
            filename=filename,
            user_id=user_id,
            session_id=session_id,
            agent_id=agent_id,
            is_generated=is_generated,
            mime_type=mime_type,
            backend_name=backend_name,
            tags=tags,
            custom_metadata=custom_metadata
        )
        
        if not original_file_id:
            logger.error(f"Failed to store original file {filename}")
            return original_file_id, None
        
        # Attempt markdown conversion and storage
        markdown_file_id = await self.convert_and_store_markdown(original_file_id)
        
        return original_file_id, markdown_file_id

    async def convert_and_store_markdown(self, original_file_id: str) -> Optional[str]:
        """
        Convert a file to markdown and store the markdown version as a separate file.
        
        Args:
            original_file_id: ID of the original file to convert
            
        Returns:
            File ID of the stored markdown version, or None if conversion failed
        """
        
        backend_name = await self._find_file_backend(original_file_id)
        
        if not backend_name:
            logger.warning(f"File {original_file_id} not found in any backend for markdown conversion")
            return None
        
        backend = self.backends[backend_name]
        
        try:
            # Get file metadata to check if conversion is appropriate
            metadata = await backend.get_file_metadata(original_file_id)
            if not metadata:
                logger.error(f"Could not retrieve metadata for file {original_file_id}")
                return None
            
            # Skip conversion if already converted
            if metadata.markdown_file_id:
                logger.debug(f"File {original_file_id} already has markdown version: {metadata.markdown_file_id}")
                return metadata.markdown_file_id
            
            # Import here to avoid circular import
            from agent_framework.processing.markdown_converter import markdown_converter
            
            # Check if format is supported for conversion
            if not markdown_converter.is_supported_format(metadata.mime_type or ""):
                logger.debug(f"File format {metadata.mime_type} not supported for markdown conversion")
                # Update metadata to indicate conversion not supported
                await backend.update_metadata(original_file_id, {
                    'conversion_status': 'not_supported',
                    'conversion_timestamp': datetime.now(),
                    'conversion_error': f'Format not supported: {metadata.mime_type}'
                })
                return None
            
            # Retrieve file content for conversion
            content, _ = await backend.retrieve_file(original_file_id)
            
            # Use enhanced conversion with detailed results
            conversion_result = await markdown_converter.convert_to_markdown(
                content, metadata.filename, metadata.mime_type or ""
            )
            
            # Update metadata with comprehensive conversion results
            metadata_updates = {
                'conversion_timestamp': datetime.now(),
                'total_processing_time_ms': conversion_result.conversion_time_ms
            }
            
            if conversion_result.success:
                # Store successful markdown version as separate file
                markdown_file_id = await backend.store_markdown_version(original_file_id, conversion_result.content)
                
                if markdown_file_id:
                    # Update metadata with success information
                    metadata_updates.update({
                        'conversion_status': 'success',
                        'conversion_error': None,
                        'processing_errors': [],
                        'processing_warnings': [issue.user_message for issue in conversion_result.issues 
                                              if issue.severity.value in ['warning', 'info']]
                    })
                    
                    await backend.update_metadata(original_file_id, metadata_updates)
                    logger.info(f"✅ Successfully converted and stored markdown version of {metadata.filename} ({conversion_result.converted_size_chars:,} characters)")
                    return markdown_file_id
                else:
                    # Conversion succeeded but storage failed
                    metadata_updates.update({
                        'conversion_status': 'failed',
                        'conversion_error': 'Failed to store markdown version',
                        'processing_errors': ['Storage of markdown version failed']
                    })
                    await backend.update_metadata(original_file_id, metadata_updates)
                    logger.error(f"Failed to store markdown version of {metadata.filename}")
                    return None
                    
            elif conversion_result.partial_content:
                # Store partial conversion result
                markdown_file_id = await backend.store_markdown_version(original_file_id, conversion_result.partial_content)
                
                if markdown_file_id:
                    # Update metadata with partial success information
                    error_messages = [issue.user_message for issue in conversion_result.issues 
                                    if issue.severity.value == 'error']
                    warning_messages = [issue.user_message for issue in conversion_result.issues 
                                      if issue.severity.value in ['warning', 'info']]
                    
                    metadata_updates.update({
                        'conversion_status': 'partial',
                        'conversion_error': '; '.join(error_messages) if error_messages else 'Partial conversion only',
                        'processing_errors': error_messages,
                        'processing_warnings': warning_messages
                    })
                    
                    await backend.update_metadata(original_file_id, metadata_updates)
                    logger.warning(f"⚠️ Partial conversion and storage completed for {metadata.filename} ({len(conversion_result.partial_content):,} characters)")
                    return markdown_file_id
                else:
                    # Partial conversion succeeded but storage failed
                    metadata_updates.update({
                        'conversion_status': 'failed',
                        'conversion_error': 'Failed to store partial markdown version',
                        'processing_errors': ['Storage of partial markdown version failed']
                    })
                    await backend.update_metadata(original_file_id, metadata_updates)
                    logger.error(f"Failed to store partial markdown version of {metadata.filename}")
                    return None
            else:
                # Conversion failed completely
                error_messages = [issue.user_message for issue in conversion_result.issues 
                                if issue.severity.value in ['error', 'critical']]
                warning_messages = [issue.user_message for issue in conversion_result.issues 
                                  if issue.severity.value in ['warning', 'info']]
                
                metadata_updates.update({
                    'conversion_status': 'failed',
                    'conversion_error': '; '.join(error_messages) if error_messages else 'Conversion failed',
                    'processing_errors': error_messages,
                    'processing_warnings': warning_messages
                })
                
                await backend.update_metadata(original_file_id, metadata_updates)
                logger.error(f"❌ Failed to convert {metadata.filename} to markdown: {metadata_updates['conversion_error']}")
                return None
                
        except Exception as e:
            logger.error(f"Error during markdown conversion and storage for file {original_file_id}: {e}")
            
            # Update metadata to indicate error
            try:
                await backend.update_metadata(original_file_id, {
                    'conversion_status': 'failed',
                    'conversion_timestamp': datetime.now(),
                    'conversion_error': str(e)
                })
            except Exception as meta_error:
                logger.error(f"Failed to update metadata after conversion error: {meta_error}")
            
            return None

    async def retrieve_file_with_versions(self, file_id: str) -> Dict[str, Any]:
        """
        Retrieve file with information about both original and markdown versions.
        
        Returns:
            Dictionary containing original file info and markdown version if available
        """
        
        backend_name = await self._find_file_backend(file_id)
        
        if not backend_name:
            raise FileNotFoundError(f"File {file_id} not found in any backend")
        
        backend = self.backends[backend_name]
        
        try:
            # Get original file
            original_content, original_metadata = await backend.retrieve_file(file_id)
            
            result = {
                'original': {
                    'file_id': file_id,
                    'content': original_content,
                    'metadata': original_metadata,
                    'filename': original_metadata.filename,
                    'mime_type': original_metadata.mime_type,
                    'size_bytes': original_metadata.size_bytes
                },
                'markdown': None,
                'conversion_status': original_metadata.conversion_status,
                'conversion_error': original_metadata.conversion_error
            }
            
            # Get markdown version if available
            if original_metadata.markdown_file_id:
                try:
                    markdown_result = await backend.retrieve_markdown_version(file_id)
                    if markdown_result:
                        markdown_content, markdown_metadata = markdown_result
                        result['markdown'] = {
                            'file_id': original_metadata.markdown_file_id,
                            'content': markdown_content,
                            'metadata': markdown_metadata,
                            'filename': markdown_metadata.filename,
                            'size_bytes': markdown_metadata.size_bytes
                        }
                except Exception as e:
                    logger.error(f"Failed to retrieve markdown version for file {file_id}: {e}")
                    result['conversion_error'] = f"Failed to retrieve markdown version: {str(e)}"
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to retrieve file with versions {file_id}: {e}")
            raise

    async def get_file_processing_summary(self, file_id: str) -> Dict[str, Any]:
        """
        Get comprehensive processing summary for a file including both versions.
        
        Returns:
            Dictionary with processing status, available versions, and metadata
        """
        
        backend_name = await self._find_file_backend(file_id)
        
        if not backend_name:
            return {
                'file_id': file_id,
                'exists': False,
                'error': 'File not found in any backend'
            }
        
        backend = self.backends[backend_name]
        
        try:
            # Get comprehensive processing status from backend
            status = await backend.get_processing_status(file_id)
            
            # Add manager-level information
            status.update({
                'backend_name': backend_name,
                'dual_storage_enabled': True,
                'versions_available': {
                    'original': True,
                    'markdown': status.get('has_markdown_version', False)
                }
            })
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get processing summary for file {file_id}: {e}")
            return {
                'file_id': file_id,
                'exists': False,
                'error': str(e)
            }
    
    # ===== PERFORMANCE AND RESOURCE MONITORING METHODS =====
    
    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get comprehensive system metrics including resource usage and performance"""
        metrics = {
            'resource_management_enabled': self.enable_resource_management,
            'performance_monitoring_enabled': self.enable_performance_monitoring,
            'backends': list(self.backends.keys()),
            'default_backend': self.default_backend,
            'routing_rules': self.routing_rules.copy()
        }
        
        # Add resource manager metrics
        if self.resource_manager:
            resource_metrics = await self.resource_manager.get_system_metrics()
            metrics['resource_usage'] = {
                'active_operations': resource_metrics.active_operations,
                'queued_operations': resource_metrics.queued_operations,
                'memory_usage_mb': resource_metrics.memory_usage_mb,
                'cpu_usage_percent': resource_metrics.cpu_usage_percent,
                'disk_usage_percent': resource_metrics.disk_usage_percent,
                'total_operations_completed': resource_metrics.total_operations_completed,
                'total_operations_failed': resource_metrics.total_operations_failed,
                'average_operation_time_ms': resource_metrics.average_operation_time_ms
            }
        
        # Add performance monitor metrics
        if self.performance_monitor:
            perf_summary = self.performance_monitor.get_performance_summary()
            metrics['performance'] = perf_summary
            
            # Add active alerts
            active_alerts = self.performance_monitor.get_active_alerts()
            metrics['active_alerts'] = [
                {
                    'alert_id': alert.alert_id,
                    'alert_type': alert.alert_type,
                    'severity': alert.severity,
                    'message': alert.message,
                    'timestamp': alert.timestamp.isoformat()
                } for alert in active_alerts
            ]
        
        return metrics
    
    async def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for file operations"""
        if not self.performance_monitor:
            return {'error': 'Performance monitoring not enabled'}
        
        return self.performance_monitor.get_performance_summary()
    
    async def get_storage_metrics(self) -> Dict[str, Any]:
        """Get storage metrics for all backends"""
        if not self.performance_monitor:
            return {'error': 'Performance monitoring not enabled'}
        
        return self.performance_monitor.get_storage_metrics()
    
    async def get_active_operations(self) -> List[Dict[str, Any]]:
        """Get information about currently active operations"""
        if not self.resource_manager:
            return []
        
        active_ops = []
        async with self.resource_manager._operation_lock:
            for op_id, metrics in self.resource_manager.active_operations.items():
                active_ops.append({
                    'operation_id': op_id,
                    'operation_type': metrics.operation_type.value,
                    'file_id': metrics.file_id,
                    'filename': metrics.filename,
                    'file_size_bytes': metrics.file_size_bytes,
                    'start_time': metrics.start_time.isoformat(),
                    'duration_so_far_ms': (datetime.now() - metrics.start_time).total_seconds() * 1000,
                    'backend_name': metrics.backend_name,
                    'user_id': metrics.user_id,
                    'session_id': metrics.session_id
                })
        
        return active_ops
    
    async def export_performance_metrics(self, filepath: str) -> bool:
        """Export performance metrics to a file"""
        if not self.performance_monitor:
            logger.warning("Performance monitoring not enabled, cannot export metrics")
            return False
        
        try:
            self.performance_monitor.export_metrics(filepath)
            return True
        except Exception as e:
            logger.error(f"Failed to export performance metrics: {e}")
            return False
    
    # ===== STORAGE OPTIMIZATION METHODS =====
    
    async def optimize_storage(self) -> Dict[str, Any]:
        """Perform comprehensive storage optimization"""
        if not self.storage_optimizer:
            return {'error': 'Storage optimization not enabled'}
        
        try:
            return await self.storage_optimizer.optimize_file_storage(self)
        except Exception as e:
            logger.error(f"Storage optimization failed: {e}")
            return {'error': str(e)}
    
    async def get_storage_optimization_stats(self) -> Dict[str, Any]:
        """Get storage optimization statistics"""
        if not self.storage_optimizer:
            return {'error': 'Storage optimization not enabled'}
        
        try:
            stats = await self.storage_optimizer.get_storage_stats(self)
            return {
                'total_files': stats.total_files,
                'total_size_mb': stats.total_size_bytes / (1024 * 1024),
                'compressed_files': stats.compressed_files,
                'duplicate_files': stats.duplicate_files,
                'oldest_file_age_days': stats.oldest_file_age_days,
                'newest_file_age_days': stats.newest_file_age_days,
                'average_file_size_mb': stats.average_file_size_bytes / (1024 * 1024),
                'storage_utilization_percent': stats.storage_utilization_percent,
                'available_space_mb': stats.available_space_bytes / (1024 * 1024)
            }
        except Exception as e:
            logger.error(f"Failed to get storage optimization stats: {e}")
            return {'error': str(e)}
    
    async def schedule_storage_cleanup(self, max_age_days: Optional[int] = None) -> Dict[str, Any]:
        """Schedule storage cleanup with optional custom age limit"""
        if not self.storage_optimizer:
            return {'error': 'Storage optimization not enabled'}
        
        try:
            # Temporarily override max age if provided
            original_max_age = self.storage_optimizer.config.max_file_age_days
            if max_age_days is not None:
                self.storage_optimizer.config.max_file_age_days = max_age_days
            
            # Perform optimization (which includes cleanup)
            result = await self.storage_optimizer.optimize_file_storage(self)
            
            # Restore original max age
            if max_age_days is not None:
                self.storage_optimizer.config.max_file_age_days = original_max_age
            
            return result
            
        except Exception as e:
            logger.error(f"Storage cleanup failed: {e}")
            return {'error': str(e)}
    
    def _determine_backend(self, mime_type: Optional[str], is_generated: bool = False, content_type: Optional[str] = None) -> str:
        """Determine which backend to use based on routing rules, generation status, and content type"""
        
        # For AI-generated content, check AI-specific routing first
        if is_generated and content_type:
            ai_prefix = f"ai-generated/{content_type}"
            if ai_prefix in self.routing_rules:
                return self.routing_rules[ai_prefix]
        
        # For AI-generated content without specific content type, use general AI routing
        if is_generated:
            # Try to map MIME type to AI content type
            ai_content_type = self._map_mime_to_ai_content_type(mime_type)
            if ai_content_type:
                ai_prefix = f"ai-generated/{ai_content_type}"
                if ai_prefix in self.routing_rules:
                    return self.routing_rules[ai_prefix]
        
        # Standard MIME type routing
        if mime_type:
            # Check routing rules for exact matches or prefixes
            for prefix, backend_name in self.routing_rules.items():
                if not prefix.startswith("ai-generated/") and mime_type.startswith(prefix):
                    return backend_name
        
        # Fall back to default backend
        if not self.default_backend:
            raise RuntimeError("No default backend configured")
        
        return self.default_backend
    
    def _map_mime_to_ai_content_type(self, mime_type: Optional[str]) -> Optional[str]:
        """Map MIME type to AI content type for routing"""
        if not mime_type:
            return None
        
        mime_to_ai_type = {
            'text/html': 'html',
            'text/markdown': 'markdown',
            'application/json': 'json',
            'text/csv': 'csv',
            'text/yaml': 'yaml',
            'text/xml': 'xml',
            'text/plain': 'text',
            'application/javascript': 'code',
            'text/javascript': 'code'
        }
        
        # Check exact matches first
        if mime_type in mime_to_ai_type:
            return mime_to_ai_type[mime_type]
        
        # Check prefix matches
        for mime_prefix, ai_type in mime_to_ai_type.items():
            if mime_prefix.endswith('/') and mime_type.startswith(mime_prefix):
                return ai_type
        
        # Special handling for image types
        if mime_type.startswith('image/'):
            return 'image'
        
        return 'data'  # Default AI content type
    
    async def _find_file_backend(self, file_id: str) -> Optional[str]:
        """Find which backend contains the specified file"""
        
        logger.info(f"🔍 FIND BACKEND - Looking for file {file_id} across {len(self.backends)} backends")
        
        for name, backend in self.backends.items():
            try:
                logger.info(f"🔍 FIND BACKEND - Checking backend '{name}' for file {file_id}")
                metadata = await backend.get_file_metadata(file_id)
                if metadata:
                    logger.info(f"✅ FIND BACKEND - Found file {file_id} in backend '{name}'")
                    return name
                else:
                    logger.info(f"❌ FIND BACKEND - File {file_id} not found in backend '{name}'")
            except Exception as e:
                logger.error(f"❌ FIND BACKEND - Error checking file {file_id} in backend '{name}': {e}")
        
        logger.error(f"❌ FIND BACKEND - File {file_id} not found in any backend")
        return None
    
    def get_backend_info(self) -> Dict[str, Dict]:
        """Get information about registered backends"""
        
        info = {
            "backends": list(self.backends.keys()),
            "default_backend": self.default_backend,
            "routing_rules": self.routing_rules
        }
        
        return info


# ===== FILE STORAGE FACTORY =====

class FileStorageFactory:
    """Factory for creating file storage backends and managers"""
    
    @staticmethod
    async def create_storage_manager() -> FileStorageManager:
        """Create and configure file storage manager based on environment"""
        manager = FileStorageManager()
        
        # Always register local storage as fallback
        local_path = os.getenv("LOCAL_STORAGE_PATH", "./file_storage")
        # Import here to avoid circular import
        from .file_storages import LocalFileStorage
        
        local_storage = LocalFileStorage(base_path=local_path)
        success = await manager.register_backend("local", local_storage, is_default=True)
        
        if not success:
            logger.error("Failed to register local storage backend")
            raise RuntimeError("Failed to initialize local file storage")
        
        # Register S3 if configured
        await FileStorageFactory._register_s3_if_configured(manager)
        
        # Register MinIO if configured  
        await FileStorageFactory._register_minio_if_configured(manager)
        
        # Set up routing rules
        FileStorageFactory._configure_routing_rules(manager)
        
        logger.info(f"File storage manager initialized with backends: {list(manager.backends.keys())}")
        return manager
    
    @staticmethod
    async def _register_s3_if_configured(manager: FileStorageManager) -> bool:
        """Register S3 backend if environment variables are configured"""
        s3_bucket = os.getenv("AWS_S3_BUCKET")
        
        if not s3_bucket:
            logger.debug("S3 storage not configured (no AWS_S3_BUCKET)")
            return False
        
        try:
            from .file_storages import S3FileStorage, S3_AVAILABLE
            
            if not S3_AVAILABLE:
                logger.warning("S3 storage configured but boto3 not available")
                return False
            
            s3_storage = S3FileStorage(
                bucket=s3_bucket,
                region=os.getenv("AWS_REGION", "us-east-1"),
                prefix=os.getenv("S3_FILE_PREFIX", "agent-files/")
            )
            
            success = await manager.register_backend("s3", s3_storage)
            
            if success:
                logger.info(f"Registered S3 storage backend for bucket {s3_bucket}")
                
                # Set S3 as default for large files if configured
                if os.getenv("S3_AS_DEFAULT", "false").lower() == "true":
                    manager.default_backend = "s3"
                    logger.info("Set S3 as default storage backend")
                
            return success
            
        except ImportError as e:
            logger.warning(f"S3 storage configured but import failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to register S3 storage: {e}")
            return False
    
    @staticmethod
    async def _register_minio_if_configured(manager: FileStorageManager) -> bool:
        """Register MinIO backend if environment variables are configured"""
        minio_endpoint = os.getenv("MINIO_ENDPOINT")
        minio_access_key = os.getenv("MINIO_ACCESS_KEY")
        minio_secret_key = os.getenv("MINIO_SECRET_KEY")
        
        if not all([minio_endpoint, minio_access_key, minio_secret_key]):
            logger.debug("MinIO storage not configured (missing required environment variables)")
            return False
        
        try:
            from .file_storages import MinIOFileStorage, MINIO_AVAILABLE
            
            if not MINIO_AVAILABLE:
                logger.warning("MinIO storage configured but minio package not available")
                return False
            
            minio_storage = MinIOFileStorage(
                endpoint=minio_endpoint,
                access_key=minio_access_key,
                secret_key=minio_secret_key,
                bucket=os.getenv("MINIO_BUCKET", "agent-files"),
                secure=os.getenv("MINIO_SECURE", "true").lower() == "true",
                prefix=os.getenv("MINIO_FILE_PREFIX", "agent-files/")
            )
            
            success = await manager.register_backend("minio", minio_storage)
            
            if success:
                logger.info(f"Registered MinIO storage backend for {minio_endpoint}")
                
                # Set MinIO as default if configured
                if os.getenv("MINIO_AS_DEFAULT", "false").lower() == "true":
                    manager.default_backend = "minio"
                    logger.info("Set MinIO as default storage backend")
                
            return success
            
        except ImportError as e:
            logger.warning(f"MinIO storage configured but import failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to register MinIO storage: {e}")
            return False
    
    @staticmethod
    def _configure_routing_rules(manager: FileStorageManager):
        """Configure routing rules based on environment variables"""
        
        # Configure default routing rules for user uploads
        default_rules = {
            "image/": os.getenv("IMAGE_STORAGE_BACKEND", "local"),
            "video/": os.getenv("VIDEO_STORAGE_BACKEND", "local"),
            "application/pdf": os.getenv("PDF_STORAGE_BACKEND", "local"),
            "text/": os.getenv("TEXT_STORAGE_BACKEND", "local"),
        }
        
        # Configure AI-generated content routing rules
        ai_content_rules = {
            "ai-generated/text": os.getenv("AI_TEXT_STORAGE_BACKEND", "local"),
            "ai-generated/html": os.getenv("AI_HTML_STORAGE_BACKEND", "local"),
            "ai-generated/chart": os.getenv("AI_CHART_STORAGE_BACKEND", "s3"),
            "ai-generated/code": os.getenv("AI_CODE_STORAGE_BACKEND", "local"),
            "ai-generated/data": os.getenv("AI_DATA_STORAGE_BACKEND", "local"),
            "ai-generated/image": os.getenv("AI_IMAGE_STORAGE_BACKEND", "s3"),
            "ai-generated/markdown": os.getenv("AI_MARKDOWN_STORAGE_BACKEND", "local"),
            "ai-generated/json": os.getenv("AI_JSON_STORAGE_BACKEND", "local"),
            "ai-generated/csv": os.getenv("AI_CSV_STORAGE_BACKEND", "local"),
            "ai-generated/yaml": os.getenv("AI_YAML_STORAGE_BACKEND", "local"),
            "ai-generated/xml": os.getenv("AI_XML_STORAGE_BACKEND", "local"),
        }
        
        # Combine all default rules
        all_default_rules = {**default_rules, **ai_content_rules}
        
        # Apply routing rules if backends exist
        for mime_prefix, backend_name in all_default_rules.items():
            if backend_name and backend_name in manager.backends:
                try:
                    manager.add_routing_rule(mime_prefix, backend_name)
                    logger.debug(f"Added routing rule: {mime_prefix} -> {backend_name}")
                except Exception as e:
                    logger.warning(f"Failed to add routing rule {mime_prefix} -> {backend_name}: {e}")
        
        # Custom routing rules from environment
        custom_rules_env = os.getenv("FILE_ROUTING_RULES")
        if custom_rules_env:
            try:
                # Format: "image/:s3,video/:minio,application/pdf:local,ai-generated/chart:s3"
                rules = custom_rules_env.split(",")
                for rule in rules:
                    if ":" in rule:
                        mime_prefix, backend_name = rule.strip().split(":", 1)
                        if backend_name in manager.backends:
                            manager.add_routing_rule(mime_prefix, backend_name)
                            logger.debug(f"Added custom routing rule: {mime_prefix} -> {backend_name}")
                        else:
                            logger.warning(f"Custom routing rule references unknown backend: {backend_name}")
            except Exception as e:
                logger.error(f"Failed to parse custom routing rules: {e}")
        
        # Log final configuration
        if manager.routing_rules:
            logger.info(f"Configured routing rules: {manager.routing_rules}")
            # Log AI content routing specifically
            ai_rules = {k: v for k, v in manager.routing_rules.items() if k.startswith("ai-generated/")}
            if ai_rules:
                logger.info(f"AI content routing rules: {ai_rules}")
        else:
            logger.info("No routing rules configured, using default backend for all files")
    
    @staticmethod
    def get_configuration_template() -> str:
        """Get a template for environment variable configuration"""
        return """
# File Storage Configuration Template

# Local Storage (always enabled as fallback)
LOCAL_STORAGE_PATH=./file_storage

# AWS S3 Storage (optional)
AWS_S3_BUCKET=my-agent-files-bucket
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_FILE_PREFIX=agent-files/
S3_AS_DEFAULT=false

# MinIO Storage (optional)
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=agent-files
MINIO_SECURE=false
MINIO_FILE_PREFIX=agent-files/
MINIO_AS_DEFAULT=false

# Routing Rules for User Uploads (optional)
IMAGE_STORAGE_BACKEND=s3
VIDEO_STORAGE_BACKEND=s3
PDF_STORAGE_BACKEND=local
TEXT_STORAGE_BACKEND=local

# AI-Generated Content Routing Rules (optional)
AI_TEXT_STORAGE_BACKEND=local
AI_HTML_STORAGE_BACKEND=local
AI_CHART_STORAGE_BACKEND=s3
AI_CODE_STORAGE_BACKEND=local
AI_DATA_STORAGE_BACKEND=local
AI_IMAGE_STORAGE_BACKEND=s3
AI_MARKDOWN_STORAGE_BACKEND=local
AI_JSON_STORAGE_BACKEND=local
AI_CSV_STORAGE_BACKEND=local
AI_YAML_STORAGE_BACKEND=local
AI_XML_STORAGE_BACKEND=local

# Custom routing rules (optional)
# Format: "mime_prefix:backend,mime_prefix:backend"
# Supports both user uploads and AI-generated content routing
FILE_ROUTING_RULES=image/:s3,video/:minio,application/pdf:local,ai-generated/chart:s3

# File Management Settings
MAX_FILE_SIZE_MB=100
ENABLE_FILE_COMPRESSION=false
FILE_CLEANUP_ENABLED=true
FILE_CLEANUP_DAYS=30
""" 