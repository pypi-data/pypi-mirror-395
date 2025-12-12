"""
File Storage Agent Example

This example demonstrates how to create an agent with file storage capabilities and automatic memory management.
The agent can store, retrieve, and manage files while maintaining conversation context across sessions.

Features demonstrated:
- File upload and storage with automatic processing
- File retrieval and listing with memory context
- Automatic file processing and markdown conversion
- Integration with the Agent Framework's file storage system
- Conversation memory that includes file interactions

Usage:
    uv run agent_with_file_storage.py

The agent will start a web server on http://localhost:8101
Try uploading files and discussing them, then reload - the agent remembers your file interactions!

Requirements: uv add agent-framework[llamaindex]
"""
import asyncio
import os
from typing import List, Any, Dict

from agent_framework.implementations import LlamaIndexAgent
from agent_framework.core.agent_interface import StructuredAgentInput
from agent_framework.storage.file_system_management import FileStorageFactory


class FileStorageAgent(LlamaIndexAgent):
    """An agent with file storage capabilities and automatic memory management.
    
    This agent can store, retrieve, and manage files using the framework's
    file storage system. It provides tools for file operations and maintains
    conversation context across sessions.
    """
    
    def __init__(self):
        super().__init__()
        # Define unique agent ID (required for session isolation)
        self.agent_id = "file_storage_agent_v1"
        # Initialize file storage manager
        self.file_storage = None
        # Store session context for tools
        self.current_user_id = "default_user"
        self.current_session_id = None
    
    async def _ensure_file_storage(self):
        """Ensure file storage is initialized."""
        if self.file_storage is None:
            self.file_storage = await FileStorageFactory.create_storage_manager()
    
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """Capture session context for use in tools."""
        # Store user_id and session_id for tools to use
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
        # Call parent to continue normal configuration
        await super().configure_session(session_configuration)
    
    def get_agent_prompt(self) -> str:
        """Define the agent's system prompt."""
        return """You are a helpful assistant with file storage capabilities.
You can create, list, and read files for users. Use the provided tools to manage files."""
    
    def get_agent_tools(self) -> List[callable]:
        """Define the tools available to the agent."""
        
        async def create_file(filename: str, content: str) -> str:
            """Create a new text file with the given filename and content."""
            await self._ensure_file_storage()
            try:
                # Store the file using current session context
                file_id = await self.file_storage.store_file(
                    content=content.encode('utf-8'),
                    filename=filename,
                    mime_type="text/plain",
                    user_id=self.current_user_id,
                    session_id=self.current_session_id,
                    is_generated= True
                )
                return f"File '{filename}' created successfully with ID: {file_id}"
            except Exception as e:
                return f"Error creating file: {str(e)}"
        
        async def list_files() -> str:
            """List all stored files for the current user and session."""
            await self._ensure_file_storage()
            try:
                # Get all files for the current user and session
                files = await self.file_storage.list_files(
                    user_id=self.current_user_id,
                    session_id=self.current_session_id
                )
                if not files:
                    return "No files found in this session."
                
                file_list = []
                for file_meta in files:
                    # FileMetadata is an object, not a dict - use attributes
                    filename = getattr(file_meta, 'filename', 'unknown')
                    file_id = getattr(file_meta, 'file_id', 'unknown')
                    size = getattr(file_meta, 'size_bytes', 0)
                    file_list.append(
                        f"- {filename} "
                        f"(ID: {file_id}, "
                        f"Size: {size} bytes)"
                    )
                return "Stored files:\n" + "\n".join(file_list)
            except Exception as e:
                return f"Error listing files: {str(e)}"
        
        async def read_file(file_id: str) -> str:
            """Read a file by its ID and return its content."""
            await self._ensure_file_storage()
            try:
                # Retrieve the file
                file_data, metadata = await self.file_storage.retrieve_file(file_id)
                content = file_data.decode('utf-8')
                # FileMetadata is an object, not a dict - use attributes
                filename = getattr(metadata, 'filename', 'unknown')
                return f"Content of '{filename}':\n{content}"
            except Exception as e:
                return f"Error reading file: {str(e)}"
        
        # Return the tools (note: async tools work with LlamaIndex)
        return [create_file, list_files, read_file]
    
    async def initialize_agent(self, model_name: str, system_prompt: str, tools: List[callable], **kwargs) -> None:
        """Initialize the agent and ensure file storage is ready."""
        # Ensure file storage is ready before initializing agent
        await self._ensure_file_storage()
        
        # Call parent to create FunctionAgent with default implementation
        await super().initialize_agent(model_name, system_prompt, tools, **kwargs)
    
    
    def create_fresh_context(self) -> Any:
        """Create a fresh LlamaIndex Context."""
        from llama_index.core.workflow import Context
        return Context(self._agent_instance)
    
    def serialize_context(self, ctx: Any) -> Dict[str, Any]:
        """Serialize the context for state persistence."""
        from llama_index.core.workflow import JsonSerializer
        return ctx.to_dict(serializer=JsonSerializer())
    
    def deserialize_context(self, state: Dict[str, Any]) -> Any:
        """Deserialize the context from saved state."""
        from llama_index.core.workflow import Context, JsonSerializer
        return Context.from_dict(self._agent_instance, state, serializer=JsonSerializer())


def main():
    """Start the file storage agent server with UI."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY=your-key-here")
        return
    
    # Import server function
    from agent_framework import create_basic_agent_server
    
    # Get port from environment or use default
    port = int(os.getenv("AGENT_PORT", "8101"))
    
    print("=" * 60)
    print("🚀 Starting File Storage Agent Server")
    print("=" * 60)
    print(f"📊 Model: {os.getenv('DEFAULT_MODEL', 'gpt-4o-mini')}")
    print(f"🔧 Tools: create_file, list_files, read_file")
    print(f"💾 Storage: Local filesystem (default)")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"🎨 UI: http://localhost:{port}/testapp")
    print("=" * 60)
    print("\nTry asking:")
    print("  - Create a file called 'notes.txt' with some content")
    print("  - List all stored files")
    print("  - Read the file with ID <file_id>")
    print("=" * 60)
    
    # Start the server
    create_basic_agent_server(
        agent_class=FileStorageAgent,
        host="0.0.0.0",
        port=port,
        reload=False
    )


if __name__ == "__main__":
    main()
