"""
Simple Agent Example

This example demonstrates how to create a basic conversational agent using the Agent Framework.
The agent uses LlamaIndex with OpenAI's GPT models and includes automatic memory management.

Features demonstrated:
- Basic agent setup with LlamaIndex
- Automatic conversation memory (remembers previous messages)
- Automatic model configuration from environment
- Session-based memory persistence
- Web server integration with memory support

Usage:
    python simple_agent.py

The agent will start a web server on http://localhost:8100
Try having a conversation, then reload the page - the agent will remember your previous messages!

Requirements: pip install agent-framework[llamaindex]
"""
import asyncio
import os
from typing import List, Any, Dict

from agent_framework.implementations import LlamaIndexAgent
from agent_framework.core.agent_interface import StructuredAgentInput


class CalculatorAgent(LlamaIndexAgent):
    """A simple calculator agent with basic math operations and automatic memory.
    """
    
    def __init__(self):
        super().__init__()
        # Define unique agent ID (required for session isolation)
        self.agent_id = "calculator_agent_v1"
        # Store session context (not used by calculator tools, but good practice)
        self.current_user_id = "default_user"
        self.current_session_id = None
    
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """Capture session context."""
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
        await super().configure_session(session_configuration)
    
    def get_agent_prompt(self) -> str:
        """Define the agent's base system prompt.
        
        Note: Rich content capabilities (Mermaid diagrams, Chart.js charts, forms,
        option blocks, tables) are automatically injected by the framework.
        You only need to define your agent's core behavior here.
        To disable automatic rich content injection, set enable_rich_content=False
        in the session configuration.
        """
        return """You are a helpful calculator assistant. Use the provided tools to perform calculations.
Always be helpful and explain your calculations clearly."""
    
    def get_agent_tools(self) -> List[callable]:
        """Define the tools available to the agent."""
        def add(a: int, b: int) -> int:
            """Add two numbers together."""
            return a + b
        
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers together."""
            return a * b
        
        return [add, multiply]




def main():
    """Start the calculator agent server with UI."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY=your-key-here")
        return
    
    # Import server function
    from agent_framework import create_basic_agent_server
    
    # Get port from environment or use default
    port = int(os.getenv("AGENT_PORT", "8100"))
    
    print("=" * 60)
    print("🚀 Starting Simple Calculator Agent Server")
    print("=" * 60)
    print(f"📊 Model: {os.getenv('DEFAULT_MODEL', 'gpt-4o-mini')}")
    print(f"🔧 Tools: add, multiply")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"🎨 UI: http://localhost:{port}/testapp")
    print("=" * 60)
    
    # Start the server
    create_basic_agent_server(
        agent_class=CalculatorAgent,
        host="0.0.0.0",
        port=port,
        reload=False
    )


if __name__ == "__main__":
    main()
