"""
File access tools for retrieving file paths and data URIs.

These tools help bridge the gap between file storage and other tools
that need to access stored files (like PDF generation with images).
"""

import logging
import base64
from typing import Callable
from pathlib import Path

from .base import AgentTool, ToolDependencyError

logger = logging.getLogger(__name__)


class GetFilePathTool(AgentTool):
    """Tool for getting an accessible path or data URI for a stored file."""
    
    def get_tool_function(self) -> Callable:
        """Return the get file path function."""
        
        async def get_file_path(file_id: str) -> str:
            """
            Get an accessible path or data URI for a stored file.
            
            For local storage: Returns the absolute file path
            For S3/MinIO: Returns a base64 data URI
            
            This is useful when you need to reference a file in HTML/PDF generation.
            
            Args:
                file_id: The file ID returned from file storage operations
            
            Returns:
                Either an absolute file path or a data URI that can be used in HTML
            
            Example usage:
                1. Create a chart image and get file_id
                2. Use this tool to get the path/URI
                3. Use the path in HTML: <img src="file:///path/to/image.png">
                   or data URI: <img src="data:image/png;base64,...">
            """
            self._ensure_initialized()
            
            # Check file storage availability
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is required but was not provided. "
                    "Ensure file_storage is set via set_context()."
                )
            
            try:
                # Get file metadata
                metadata = await self.file_storage.get_file_metadata(file_id)
                
                if not metadata:
                    return f"Error: File with ID '{file_id}' not found in storage"
                
                # Check storage backend type
                backend_name = metadata.storage_backend
                
                if backend_name == "local":
                    # For local storage, return absolute path
                    storage_path = metadata.storage_path
                    
                    # Verify file exists
                    file_path = Path(storage_path)
                    if not file_path.exists():
                        return f"Error: File exists in metadata but not on disk: {storage_path}"
                    
                    # Return absolute path with file:// protocol for HTML
                    absolute_path = file_path.resolve()
                    logger.info(f"Retrieved local file path for {file_id}: {absolute_path}")
                    return f"file://{absolute_path}"
                
                else:
                    # For S3/MinIO, retrieve content and create data URI
                    logger.info(f"Retrieving file {file_id} from {backend_name} to create data URI")
                    
                    content, metadata = await self.file_storage.retrieve_file(file_id)
                    
                    # Encode as base64
                    base64_content = base64.b64encode(content).decode('utf-8')
                    
                    # Get MIME type
                    mime_type = metadata.mime_type or "application/octet-stream"
                    
                    # Create data URI
                    data_uri = f"data:{mime_type};base64,{base64_content}"
                    
                    logger.info(f"Created data URI for {file_id} ({len(base64_content)} base64 chars)")
                    return data_uri
                
            except Exception as e:
                error_msg = f"Failed to get file path: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"Error: {str(e)}"
        
        return get_file_path


class GetFileAsDataURITool(AgentTool):
    """Tool for converting any stored file to a base64 data URI."""
    
    def get_tool_function(self) -> Callable:
        """Return the get file as data URI function."""
        
        async def get_file_as_data_uri(file_id: str) -> str:
            """
            Convert a stored file to a base64 data URI.
            
            This always returns a data URI regardless of storage backend,
            which is useful for embedding files directly in HTML/PDF.
            
            Args:
                file_id: The file ID returned from file storage operations
            
            Returns:
                A data URI string: data:mime/type;base64,<encoded_content>
            
            Example usage:
                1. Create a chart image and get file_id
                2. Use this tool to get data URI
                3. Embed in HTML: <img src="data:image/png;base64,...">
            """
            self._ensure_initialized()
            
            # Check file storage availability
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is required but was not provided. "
                    "Ensure file_storage is set via set_context()."
                )
            
            try:
                # Retrieve file content
                content, metadata = await self.file_storage.retrieve_file(file_id)
                
                # Encode as base64
                base64_content = base64.b64encode(content).decode('utf-8')
                
                # Get MIME type
                mime_type = metadata.mime_type or "application/octet-stream"
                
                # Create data URI
                data_uri = f"data:{mime_type};base64,{base64_content}"
                
                logger.info(
                    f"Created data URI for {file_id} "
                    f"(filename: {metadata.filename}, size: {len(base64_content)} base64 chars)"
                )
                
                return data_uri
                
            except Exception as e:
                error_msg = f"Failed to create data URI: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"Error: {str(e)}"
        
        return get_file_as_data_uri


__all__ = [
    "GetFilePathTool",
    "GetFileAsDataURITool",
]
