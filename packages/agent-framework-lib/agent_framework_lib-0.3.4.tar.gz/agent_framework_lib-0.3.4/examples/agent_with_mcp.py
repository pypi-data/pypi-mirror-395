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
from typing import List, Any, Dict, Optional

from agent_framework.implementations import LlamaIndexAgent
from agent_framework.core.agent_interface import StructuredAgentInput


class MCPAgent(LlamaIndexAgent):
    """An agent with MCP (Model Context Protocol) integration and automatic memory.
    
    This agent can connect to MCP servers to access external tools and services.
    """
    
    def __init__(self):
        super().__init__()
        # Define unique agent ID (required for session isolation)
        self.agent_id = "mcp_agent_v1"
        # Store session context for potential use in tools
        self.current_user_id = "default_user"
        self.current_session_id = None
        # MCP tools storage
        self.mcp_tools = []
        self.mcp_clients = {}
        self._mcp_initialized = False
    
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """Capture session context."""
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
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
        
        # Get MCP server configuration
        mcp_config = self._get_mcp_server_config()
        if not mcp_config:
            print("ℹ️ No MCP server configured")
            return
        
        try:
            print(f"🔌 Connecting to MCP server...")
            cmd = mcp_config["command"]
            args = mcp_config["args"]
            env = mcp_config.get("env", {})
            
            client = BasicMCPClient(cmd, args=args, env=env)
            self.mcp_clients["mcp_server"] = client
            
            # Use official LlamaIndex MCP approach
            mcp_tool_spec = McpToolSpec(client=client)
            function_tools = await mcp_tool_spec.to_tool_list_async()
            
            if function_tools:
                self.mcp_tools.extend(function_tools)
                print(f"✅ MCP server: {len(function_tools)} tools loaded")
            else:
                print("⚠️ No tools found from MCP server")
        except Exception as e:
            print(f"❌ Failed to connect to MCP server: {e}")
        
        self._mcp_initialized = True
        print(f"📊 MCP Tools initialized: {len(self.mcp_tools)} tools available")
    
    def _get_mcp_server_config(self) -> Optional[Dict[str, Any]]:
        """Get MCP server configuration with environment variables."""
    # This is an example with a mcp server with python 
        
        
        return [{
            "command": "uv",
            "args": [
                "run",
                "python",
                "-m",
                "iso_financial_mcp"
            ],
            "env": {}
        }]
    
    def get_agent_prompt(self) -> str:
        """Define the agent's system prompt."""
        return """You are a helpful assistant with access to external tools via MCP servers.
You can perform file system operations, make HTTP requests, and more depending on configured MCP servers.
Use the available tools to help users with their requests."""
    
    def get_agent_tools(self) -> List[callable]:
        """Define the built-in tools available to the agent.
        
        This method combines built-in tools with MCP tools.
        MCP tools are loaded asynchronously in _initialize_mcp_tools().
        """
        
        def greet(name: str) -> str:
            """Greet a user by name."""
            return f"Hello, {name}! I'm an MCP-enabled agent."
        
        # Combine built-in tools with MCP tools
        all_tools = [greet]
        
        # Add MCP tools if they've been initialized
        if self.mcp_tools:
            all_tools.extend(self.mcp_tools)
            print(f"🔧 Returning {len(all_tools)} tools ({len(self.mcp_tools)} from MCP)")
        
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
    port = int(os.getenv("AGENT_PORT", "8102"))
    
    print("=" * 60)
    print("🚀 Starting MCP Agent Server")
    print("=" * 60)
    print(f"📊 Model: {os.getenv('DEFAULT_MODEL', 'gpt-4o-mini')}")
    print(f"🔧 Built-in Tools: greet")
    print(f"🔌 MCP Server: filesystem (if configured)")
    print(f"📁 MCP Directory: {os.getenv('MCP_FILESYSTEM_DIR', '~/mcp_workspace')}")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"🎨 UI: http://localhost:{port}/testapp")
    print("=" * 60)
    print("\nMCP Setup (optional):")
    print("  1. Install: uvx install @modelcontextprotocol/server-filesystem")
    print("  2. Set: export MCP_FILESYSTEM_DIR=~/mcp_workspace")
    print("\nTry asking:")
    print("  - Greet me as Alice")
    print("  - List files in the workspace (if MCP configured)")
    print("  - Create a file called test.txt (if MCP configured)")
    print("=" * 60)
    
    # Start the server
    create_basic_agent_server(
        agent_class=MCPAgent,
        host="0.0.0.0",
        port=port,
        reload=False
    )


if __name__ == "__main__":
    asyncio.run(main())
