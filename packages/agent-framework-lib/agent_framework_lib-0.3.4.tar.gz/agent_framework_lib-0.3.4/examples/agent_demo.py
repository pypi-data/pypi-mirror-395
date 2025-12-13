"""
MCP Agent Example

This example demonstrates how to create an agent that integrates with MCP (Model Context Protocol) servers.
MCP allows agents to connect to external tools and services for enhanced capabilities.

Features demonstrated:
- MCP server integration with automatic memory management
- External tool access with conversation history
- Enhanced agent capabilities through MCP tools
- Automatic tool discovery and integration
- Session-based memory for tool interactions

Common MCP servers:
- filesystem: Access to local file system operations
- fetch: HTTP requests and web scraping
- github: GitHub API integration
- postgres: Database operations

Usage:
    python agent_with_mcp.py

The agent will start a web server on http://localhost:8102
Try using MCP tools, then reload - the agent remembers your previous tool interactions!

Requirements: 
- uv add agent-framework[llamaindex]
- uv add llama-index-tools-mcp
- MCP server installed (e.g., uvx install @modelcontextprotocol/server-filesystem)

Learn more about MCP: https://modelcontextprotocol.io/
"""
import asyncio
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Any, Dict, Optional

# Load environment variables from a `.env` file located at the project root (one level
# above the `agents/` directory). Fall back to default loader if no explicit .env file
# is found.
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

from agent_framework.implementations import LlamaIndexAgent
from agent_framework.core.agent_interface import StructuredAgentInput
from agent_framework.storage.file_system_management import FileStorageFactory

from agent_framework.tools import (
    CreateFileTool,
    ListFilesTool,
    ReadFileTool,
    CreatePDFFromMarkdownTool,
    CreatePDFFromHTMLTool,
    ChartToImageTool,
    GetFilePathTool,
    CreatePDFWithImagesTool,
    MermaidToImageTool,
    TableToImageTool
)

# Agent prompt - Note: Rich content capabilities (Mermaid diagrams, Chart.js charts, forms,
# option blocks, tables) are automatically injected by the framework.
# You only need to define your agent's core behavior here.
# To disable automatic rich content injection, set enable_rich_content=False in session config.
PROMPT = """You are a multi-skilled assistant with access to various tools and capabilities.

**Core Capabilities:**
- Execute Python scripts and code snippets through MCP servers
- Read, list, and create files within the session context
- Generate PDF documents from markdown or HTML sources
- By default if the user asks you to create a file, assume it's a PDF

**PDF Generation Guidelines:**
You can generate PDF files using create_pdf_from_markdown or create_pdf_from_html.
When creating PDFs, intelligently choose between markdown and HTML based on content requirements:

- **Use Markdown** for:
  - Text-heavy documents with simple formatting
  - Reports, documentation, and straightforward content
  - When readability and simplicity are priorities

- **Use HTML** for:
  - Complex layouts requiring precise control
  - Documents with advanced styling needs
  - Multi-column layouts, custom fonts, or sophisticated design elements

**Embedding Charts in PDFs:**
To include charts in PDF documents, use the workflow with create_pdf_with_images:
1. Create the chart image using save_chart_as_image tool
2. Create HTML with special file_id syntax: <img src="file_id:YOUR_FILE_ID" alt="Description">
3. Create the PDF using create_pdf_with_images (automatically embeds images from file_ids)
"""



class TestAgent(LlamaIndexAgent):
    """An agent with MCP (Model Context Protocol) integration and automatic memory.
    
    This agent can connect to MCP servers to access external tools and services.
    """
    
    def __init__(self):
        super().__init__()
        # Define unique agent ID (required for session isolation)
        self.agent_id = "owliance-bot"
        # Store session context for potential use in tools
        self.current_user_id = "default_user"
        self.current_session_id = None
        # MCP tools storage
        self.mcp_tools = []
        self.mcp_clients = {}
        self._mcp_initialized = False
        self.file_storage = None
        self.tools_files_storage= [
            CreateFileTool(),
            ListFilesTool(),
            ReadFileTool(),
            CreatePDFFromMarkdownTool(),
            CreatePDFFromHTMLTool(),
            ChartToImageTool(),
            GetFilePathTool(),
            CreatePDFWithImagesTool(),
            MermaidToImageTool(),
            TableToImageTool()
        ]
    async def _ensure_file_storage(self):
        """Ensure file storage is initialized."""
        if self.file_storage is None:
            self.file_storage = await FileStorageFactory.create_storage_manager()
    
    
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """Capture session context."""
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
         # Ensure file storage is initialized before injecting into tools
        await self._ensure_file_storage()
        #Initialize file storage tools
        for tool in self.tools_files_storage:
            tool.set_context(file_storage=self.file_storage,
                            user_id=self.current_user_id,
                            session_id=self.current_session_id)
        # Call parent to continue normal configuration                
        await super().configure_session(session_configuration)
    
    async def _initialize_mcp_tools(self):
        """Initialize MCP tools from configured servers."""
        if self._mcp_initialized:
            return
        
        try:
            from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
        except ImportError:
            print("⚠️ llama-index-tools-mcp not available. Install with: uv add llama-index-tools-mcp")
            self.mcp_tools = []
            return
        
        print("🔌 Initializing MCP tools...")
        self.mcp_tools = []
        
        # Get MCP server configuration (returns a list of configs)
        mcp_configs = self._get_mcp_server_config()
        if not mcp_configs:
            print("ℹ️ No MCP server configured")
            return
        
        # Iterate over all MCP server configurations
        for idx, mcp_config in enumerate(mcp_configs):
            try:
                server_name = mcp_config.get("name", f"mcp_server_{idx}")
                print(f"🔌 Connecting to MCP server: {server_name}...")
                cmd = mcp_config["command"]
                args = mcp_config["args"]
                env = mcp_config.get("env", {})
                
                client = BasicMCPClient(cmd, args=args, env=env)
                self.mcp_clients[server_name] = client
                
                # Use official LlamaIndex MCP approach
                mcp_tool_spec = McpToolSpec(client=client)
                function_tools = await mcp_tool_spec.to_tool_list_async()
                
                if function_tools:
                    self.mcp_tools.extend(function_tools)
                    print(f"✅ MCP server '{server_name}': {len(function_tools)} tools loaded")
                else:
                    print(f"⚠️ No tools found from MCP server '{server_name}'")
            except Exception as e:
                print(f"❌ Failed to connect to MCP server '{server_name}': {e}")
        
        self._mcp_initialized = True
        print(f"📊 MCP Tools initialized: {len(self.mcp_tools)} tools available")
    
    def _get_mcp_server_config(self) -> Optional[List[Dict[str, Any]]]:
        """Get MCP server configuration with environment variables.
        
        Returns a list of MCP server configurations. Each configuration is a dict with:
        - command: The command to run (e.g., "uvx")
        - args: List of arguments
        - env: Dictionary of environment variables
        """
        # This is an example with a mcp server with python 
        return [{
            "command": "uvx",
            "args": [
                "mcp-neo4j-cypher@0.5.1", "--transport", "stdio" 
            ],
            "env": {
                "NEO4J_URI": "neo4j+s://92c380c6.databases.neo4j.io",
                "NEO4J_USERNAME": os.getenv("NEO4J_USERNAME", "neo4j"),
                "NEO4J_PASSWORD": os.getenv("NEO4J_PASSWORD","Sd6JI1bMVGG6kqFM6uox3FwtZ8dH_Sci4-vUx31-wsI"),
                "NEO4J_DATABASE": os.getenv("NEO4J_DATABASE", "neo4j")
            }
        },
            {
                "command": "uvx",
                "args": ["mcp-run-python","stdio"],
            }]
    


    def get_agent_prompt(self) -> str:
        """Define the agent's system prompt."""
        return PROMPT
    
    def get_agent_tools(self) -> List[callable]:
        """Define the built-in tools available to the agent.
        
        This method combines built-in tools with MCP tools.
        MCP tools are loaded asynchronously in _initialize_mcp_tools().
        """
        all_tools = []
        
        # Add MCP tools if they've been initialized
        if self.mcp_tools:
            all_tools.extend(self.mcp_tools)
            print(f"🔧 Returning {len(all_tools)} tools ({len(self.mcp_tools)} from MCP)")
        all_tools.extend([tool.get_tool_function() for tool in self.tools_files_storage])  
        return all_tools
    
    async def initialize_agent(self, model_name: str, system_prompt: str, tools: List[callable], **kwargs) -> None:
        """Initialize the agent and load MCP tools first."""
        # Load MCP tools BEFORE creating the agent
        await self._initialize_mcp_tools()
        
        # Get all tools including MCP
        all_tools = self.get_agent_tools()
        
        # Call parent with all tools
        await super().initialize_agent(model_name, system_prompt, all_tools, **kwargs)



def main():
    """Start the MCP agent server with UI."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY=your-key-here")
        return
    
    # Import server function
    from agent_framework import create_basic_agent_server
    
    # Get port from environment or use default
    port = int(os.getenv("AGENT_PORT", "8200"))
    
    print("=" * 60)
    print("🚀 Starting MCP multi skills Server")
    print("=" * 60)
    print(f"📊 Model: {os.getenv('DEFAULT_MODEL', 'gpt-5-mini')}")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"🎨 UI: http://localhost:{port}/testapp")
    print("=" * 60)
    
    # Start the server
    create_basic_agent_server(
        agent_class=TestAgent,
        host="0.0.0.0",
        port=port,
        reload=False
    )


if __name__ == "__main__":
    asyncio.run(main())
