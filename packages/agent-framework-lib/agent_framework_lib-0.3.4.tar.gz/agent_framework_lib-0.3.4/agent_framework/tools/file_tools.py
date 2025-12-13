"""
File storage tools for agent operations.

This module provides reusable tools for file operations including creating,
listing, and reading files from the file storage system.
"""

import logging
from typing import Callable

from .base import AgentTool, ToolDependencyError

logger = logging.getLogger(__name__)


class CreateFileTool(AgentTool):
    """Tool for creating new files in the file storage system."""
    
    def get_tool_function(self) -> Callable:
        """Return the file creation function."""
        
        async def create_file(filename: str, content: str) -> str:
            """
            Create a new text file with the given filename and content.
            
            This function creates a new file in the file storage system with the
            provided content. The file will be associated with the current user
            and session, and marked as agent-generated.
            
            Args:
                filename: Name for the new file (e.g., "report.txt", "data.json")
                content: Text content to write to the file
            
            Returns:
                Success message with the file ID, or error message if creation fails
            
            Example:
                result = await create_file("summary.txt", "This is a summary...")
                # Returns: "File 'summary.txt' created successfully with ID: abc-123"
            """
            self._ensure_initialized()
            
            # Validate inputs
            if not filename or not filename.strip():
                return "Error: Filename cannot be empty"
            
            if not content:
                return "Error: Content cannot be empty"
            
            # Check if file storage is available
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is not available. Ensure set_context() was called "
                    "with a valid file_storage instance."
                )
            
            try:
                # Encode content to bytes
                content_bytes = content.encode('utf-8')
                
                # Store file with context information
                file_id = await self.file_storage.store_file(
                    content=content_bytes,
                    filename=filename,
                    user_id=self.current_user_id,
                    session_id=self.current_session_id,
                    is_generated=True,  # Mark as agent-created
                    mime_type="text/plain",
                    tags=["agent-created"]
                )
                
                logger.info(f"Created file '{filename}' with ID: {file_id}")
                return f"File '{filename}' created successfully with ID: {file_id}"
                
            except Exception as e:
                error_msg = f"Failed to create file '{filename}': {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"
        
        return create_file


class ListFilesTool(AgentTool):
    """Tool for listing stored files."""
    
    def get_tool_function(self) -> Callable:
        """Return the file listing function."""
        
        async def list_files() -> str:
            """
            List all stored files for the current user and session.
            
            This function retrieves a list of all files stored for the current
            user and session, including both user-uploaded and agent-generated files.
            
            Returns:
                Formatted string with file information (filename, ID, size),
                or "No files found" if no files exist
            
            Example:
                result = await list_files()
                # Returns:
                # Files:
                # 1. report.txt (ID: abc-123, Size: 1.2 KB)
                # 2. data.json (ID: def-456, Size: 3.4 KB)
            """
            self._ensure_initialized()
            
            # Check if file storage is available
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is not available. Ensure set_context() was called "
                    "with a valid file_storage instance."
                )
            
            try:
                # List files for current user and session
                files = await self.file_storage.list_files(
                    user_id=self.current_user_id,
                    session_id=self.current_session_id
                )
                
                if not files:
                    return "No files found for the current session"
                
                # Format file list
                file_lines = ["Files:"]
                for i, file_metadata in enumerate(files, 1):
                    # Format file size
                    size_bytes = file_metadata.size_bytes
                    if size_bytes < 1024:
                        size_str = f"{size_bytes} B"
                    elif size_bytes < 1024 * 1024:
                        size_str = f"{size_bytes / 1024:.1f} KB"
                    else:
                        size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                    
                    file_lines.append(
                        f"{i}. {file_metadata.filename} "
                        f"(ID: {file_metadata.file_id}, Size: {size_str})"
                    )
                
                result = "\n".join(file_lines)
                logger.info(f"Listed {len(files)} files for user {self.current_user_id}")
                return result
                
            except Exception as e:
                error_msg = f"Failed to list files: {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"
        
        return list_files


class ReadFileTool(AgentTool):
    """Tool for reading file content."""
    
    def get_tool_function(self) -> Callable:
        """Return the file reading function."""
        
        async def read_file(file_id: str) -> str:
            """
            Read a file by its ID and return its content.
            
            This function retrieves a file from storage by its unique ID and
            returns the content as a string. The file must be accessible to
            the current user.
            
            Args:
                file_id: Unique identifier of the file to read
            
            Returns:
                Formatted string with filename and content, or error message if read fails
            
            Example:
                result = await read_file("abc-123")
                # Returns:
                # File: report.txt
                # Content:
                # This is the file content...
            """
            self._ensure_initialized()
            
            # Validate input
            if not file_id or not file_id.strip():
                return "Error: File ID cannot be empty"
            
            # Check if file storage is available
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is not available. Ensure set_context() was called "
                    "with a valid file_storage instance."
                )
            
            try:
                # Retrieve file from storage
                content_bytes, metadata = await self.file_storage.retrieve_file(file_id)
                
                # Decode content to string
                try:
                    content_str = content_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    return (
                        f"Error: File '{metadata.filename}' contains binary data "
                        "that cannot be displayed as text"
                    )
                
                # Format response
                result = f"File: {metadata.filename}\nContent:\n{content_str}"
                logger.info(f"Read file '{metadata.filename}' (ID: {file_id})")
                return result
                
            except Exception as e:
                error_msg = f"Failed to read file with ID '{file_id}': {str(e)}"
                logger.error(error_msg)
                return f"Error: {error_msg}"
        
        return read_file


__all__ = [
    "CreateFileTool",
    "ListFilesTool",
    "ReadFileTool",
]
