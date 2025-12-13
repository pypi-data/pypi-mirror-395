"""
File Storage Agent Example

This example demonstrates how to create an agent with file storage capabilities and automatic memory management.
The agent can store, retrieve, and manage files while maintaining conversation context across sessions.

Features demonstrated:
- File upload and storage with automatic processing
- File retrieval and listing with memory context
- PDF generation from Markdown content with multiple template styles
- Automatic file processing and markdown conversion
- Integration with the Agent Framework's file storage system
- Conversation memory that includes file interactions
- Reusable tools architecture with dependency injection

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

# Import reusable tools from the tools module
from agent_framework.tools import (
    CreateFileTool,
    ListFilesTool,
    ReadFileTool,
    CreatePDFFromMarkdownTool,
    CreatePDFFromHTMLTool
)


class FileStorageAgent(LlamaIndexAgent):
    """An agent with file storage capabilities and automatic memory management.
    
    This agent demonstrates the new reusable tools architecture where tools are
    instantiated as classes and have their dependencies injected via set_context().
    This approach makes tools reusable across different agents and easier to test.
    
    The agent can store, retrieve, and manage files using the framework's
    file storage system, and can also generate professional PDF documents from
    Markdown content.
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
        
        # Initialize reusable tools
        # These tools follow the AgentTool pattern where dependencies are injected
        # via set_context() rather than being passed to constructors
        self.tools = [
            CreateFileTool(),
            ListFilesTool(),
            ReadFileTool(),
            CreatePDFFromMarkdownTool(),
            CreatePDFFromHTMLTool()
        ]
    
    async def _ensure_file_storage(self):
        """Ensure file storage is initialized."""
        if self.file_storage is None:
            self.file_storage = await FileStorageFactory.create_storage_manager()
    
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """Capture session context and inject it into all tools.
        
        This method demonstrates the dependency injection pattern used by the
        reusable tools architecture. Each tool receives the file_storage instance,
        user_id, and session_id it needs to operate.
        """
        # Store user_id and session_id for tools to use
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
        
        # Ensure file storage is initialized before injecting into tools
        await self._ensure_file_storage()
        
        # Inject context into all tools
        # This is the key pattern: tools receive their dependencies here
        # rather than having them hardcoded or passed to constructors
        for tool in self.tools:
            tool.set_context(
                file_storage=self.file_storage,
                user_id=self.current_user_id,
                session_id=self.current_session_id
            )
        
        # Call parent to continue normal configuration
        await super().configure_session(session_configuration)
    
    def get_agent_prompt(self) -> str:
        """Define the agent's base system prompt.
        
        Note: Rich content capabilities (Mermaid diagrams, Chart.js charts, forms,
        option blocks, tables) are automatically injected by the framework.
        You only need to define your agent's core behavior here.
        To disable automatic rich content injection, set enable_rich_content=False
        in the session configuration.
        """
        return """You are a helpful assistant with file storage and PDF generation capabilities.

You can:
- Create, list, and read text files for users
- Generate professional PDF documents from Markdown or HTML content
- Choose from multiple PDF template styles: 'professional', 'minimal', or 'modern'

Use the provided tools to manage files and create beautiful documents."""
    
    def get_agent_tools(self) -> List[callable]:
        """Return the tool functions from the reusable tools.
        
        This method demonstrates the new architecture where tools are instantiated
        as classes and their callable functions are retrieved via get_tool_function().
        
        Benefits of this approach:
        - Tools are reusable across different agents
        - Dependencies are injected cleanly via set_context()
        - Tools can be tested independently
        - Tool implementations are centralized in agent_framework.tools
        - No need to redefine tool logic in each agent
        """
        # Get the callable function from each tool instance
        # The tools already have their context injected in configure_session()
        return [tool.get_tool_function() for tool in self.tools]
    
    async def initialize_agent(self, model_name: str, system_prompt: str, tools: List[callable], **kwargs) -> None:
        """Initialize the agent and ensure file storage is ready."""
        # Ensure file storage is ready before initializing agent
        await self._ensure_file_storage()
        
        # Call parent to create FunctionAgent with default implementation
        await super().initialize_agent(model_name, system_prompt, tools, **kwargs)



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
    print(f"🔧 Tools: create_file, list_files, read_file, create_pdf_from_markdown")
    print(f"💾 Storage: Local filesystem (default)")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"🎨 UI: http://localhost:{port}/testapp")
    print("=" * 60)
    print("\nTry asking:")
    print("  - Create a file called 'notes.txt' with some content")
    print("  - List all stored files")
    print("  - Read the file with ID <file_id>")
    print("  - Create a PDF from markdown with title 'My Report'")
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
