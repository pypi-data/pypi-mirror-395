"""
Base classes and exceptions for agent tools.

This module provides the foundation for creating reusable tools that can be
used across different agents with proper dependency injection and error handling.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional


class ToolDependencyError(Exception):
    """
    Raised when a tool's dependencies are not available.
    
    This exception is raised when:
    - A tool is used without proper initialization via set_context()
    - Required dependencies (like file_storage) are missing
    - Optional packages required by the tool are not installed
    """
    pass


class AgentTool(ABC):
    """
    Base class for agent tools that require dependencies like file storage.
    
    Tools should inherit from this class and implement get_tool_function().
    The agent will inject dependencies via set_context() before using the tool.
    
    Example:
        class MyTool(AgentTool):
            def get_tool_function(self) -> Callable:
                async def my_function(param: str) -> str:
                    self._ensure_initialized()
                    # Use self.file_storage, self.current_user_id, etc.
                    return "result"
                return my_function
        
        # Usage in agent
        tool = MyTool()
        tool.set_context(
            file_storage=storage_manager,
            user_id="user123",
            session_id="session456"
        )
        func = tool.get_tool_function()
        result = await func("test")
    """
    
    def __init__(self):
        """Initialize the tool with default values."""
        self.file_storage: Optional[Any] = None
        self.current_user_id: str = "default_user"
        self.current_session_id: Optional[str] = None
        self._initialized: bool = False
    
    def set_context(
        self,
        file_storage: Optional[Any] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> None:
        """
        Set the context/dependencies for this tool.
        
        This method should be called by the agent after tool instantiation
        and before using the tool function. It injects the runtime dependencies
        that the tool needs to operate.
        
        Args:
            file_storage: FileStorageManager instance for file operations
            user_id: Current user identifier
            session_id: Current session identifier
        
        Example:
            tool.set_context(
                file_storage=self.file_storage,
                user_id=self.current_user_id,
                session_id=self.current_session_id
            )
        """
        if file_storage is not None:
            self.file_storage = file_storage
        if user_id is not None:
            self.current_user_id = user_id
        if session_id is not None:
            self.current_session_id = session_id
        self._initialized = True
    
    def _ensure_initialized(self) -> None:
        """
        Check that the tool has been properly initialized.
        
        This method should be called at the beginning of tool functions
        to ensure that set_context() was called before use.
        
        Raises:
            ToolDependencyError: If the tool has not been initialized via set_context()
        
        Example:
            async def my_tool_function(self, param: str) -> str:
                self._ensure_initialized()
                # Rest of implementation
        """
        if not self._initialized:
            raise ToolDependencyError(
                f"{self.__class__.__name__} has not been initialized. "
                "Call set_context() before using this tool."
            )
    
    @abstractmethod
    def get_tool_function(self) -> Callable:
        """
        Return the actual tool function that the agent will use.
        
        This method must be implemented by subclasses to provide the
        callable function that performs the tool's operation.
        
        The returned function should:
        - Be async (async def)
        - Have a complete docstring with parameter descriptions
        - Call self._ensure_initialized() at the start
        - Use self.file_storage, self.current_user_id, etc. as needed
        - Return a string result or error message
        
        Returns:
            Callable: The tool function that can be called by the agent/LLM
        
        Example:
            def get_tool_function(self) -> Callable:
                async def create_file(filename: str, content: str) -> str:
                    '''Create a new file with the given content.'''
                    self._ensure_initialized()
                    # Implementation
                    return "File created successfully"
                return create_file
        """
        pass
    
    def get_tool_info(self) -> Dict[str, Any]:
        """
        Get metadata about this tool.
        
        Returns a dictionary containing information about the tool including
        its name, description, and dependency requirements.
        
        Returns:
            dict: Tool metadata with the following keys:
                - name (str): Tool class name
                - description (str): Tool description from docstring
                - requires_file_storage (bool): Whether tool needs file storage
                - requires_user_context (bool): Whether tool needs user/session IDs
        
        Example:
            info = tool.get_tool_info()
            print(f"Tool: {info['name']}")
            print(f"Requires storage: {info['requires_file_storage']}")
        """
        return {
            "name": self.__class__.__name__,
            "description": self.__class__.__doc__.strip() if self.__class__.__doc__ else "",
            "requires_file_storage": True,  # Most tools require file storage
            "requires_user_context": True,  # Most tools require user context
        }


__all__ = [
    "AgentTool",
    "ToolDependencyError",
]
