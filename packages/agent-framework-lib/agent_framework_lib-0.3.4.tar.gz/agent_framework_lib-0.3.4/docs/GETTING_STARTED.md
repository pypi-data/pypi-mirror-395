# Getting Started with Agent Framework

This guide will help you choose the right approach for your agent and get started quickly.

## Table of Contents

1. [Which Agent Type Should I Use?](#which-agent-type-should-i-use)
2. [Quick Start: LlamaIndex Agent](#quick-start-llamaindex-agent)
3. [Quick Start: Custom Framework Agent](#quick-start-custom-framework-agent)
4. [Adding Tools](#adding-tools)
5. [Adding MCP Servers](#adding-mcp-servers)
6. [Next Steps](#next-steps)

---

## Which Agent Type Should I Use?

### Use LlamaIndexAgent When:

✅ You want the fastest development experience  
✅ You need built-in memory management  
✅ You want automatic streaming support  
✅ You're okay with LlamaIndex as a dependency  
✅ You want to get started in 10-15 minutes

**Example use cases:**
- Chatbots with conversation history
- Agents with multiple tools
- Quick prototypes
- Production agents with standard requirements

### Use BaseAgent When:

✅ You want to use a different framework (LangChain, Haystack, etc.)  
✅ You need full control over agent execution  
✅ You have custom streaming requirements  
✅ You want minimal dependencies  
✅ You're integrating an existing agent system

**Example use cases:**
- Integrating LangChain agents
- Custom agent implementations
- Framework migration
- Specialized agent architectures

---

## Quick Start: LlamaIndex Agent

### 1. Install Dependencies

```bash
uv add agent-framework-lib[llamaindex]
```

### 2. Create Your Agent

Create a file `my_agent.py`:

```python
"""
My First LlamaIndex Agent
"""
import os
from typing import List, Any, Dict
from agent_framework.implementations import LlamaIndexAgent

class MyAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        # Required: Unique agent ID for session isolation
        self.agent_id = "my_first_agent_v1"
    
    def get_agent_prompt(self) -> str:
        """Define what your agent does."""
        return "You are a helpful assistant that can perform calculations."
    
    def get_agent_tools(self) -> List[callable]:
        """Define tools your agent can use."""
        
        def add(a: float, b: float) -> float:
            """Add two numbers together."""
            return a + b
        
        def multiply(a: float, b: float) -> float:
            """Multiply two numbers together."""
            return a * b
        
        return [add, multiply]
    
    # Optional: Override these for custom behavior
    def create_fresh_context(self) -> Any:
        """Create conversation context."""
        from llama_index.core.workflow import Context
        return Context(self._agent_instance)
    
    def serialize_context(self, ctx: Any) -> Dict[str, Any]:
        """Save conversation state."""
        from llama_index.core.workflow import JsonSerializer
        return ctx.to_dict(serializer=JsonSerializer())
    
    def deserialize_context(self, state: Dict[str, Any]) -> Any:
        """Load conversation state."""
        from llama_index.core.workflow import Context, JsonSerializer
        return Context.from_dict(self._agent_instance, state, serializer=JsonSerializer())


def main():
    """Start the agent server."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return
    
    from agent_framework import create_basic_agent_server
    
    print("🚀 Starting agent on http://localhost:8000")
    create_basic_agent_server(
        agent_class=MyAgent,
        host="0.0.0.0",
        port=8000,
        reload=False
    )


if __name__ == "__main__":
    main()
```

### 3. Set Environment Variables

```bash
export OPENAI_API_KEY=sk-your-key-here
export DEFAULT_MODEL=gpt-4o-mini
```

### 4. Run Your Agent

```bash
uv run python my_agent.py
```

### 5. Test It

Open http://localhost:8000/testapp in your browser, or use curl:

```bash
curl -X POST http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 15 + 27?"}'
```

**That's it!** You now have a fully functional agent with:
- ✅ Streaming responses
- ✅ Session management
- ✅ Tool calling
- ✅ Conversation memory
- ✅ Web interface

---

## Quick Start: Custom Framework Agent

### 1. Install Dependencies

```bash
uv add agent-framework-lib
```

### 2. Create Your Agent

Create a file `my_custom_agent.py`:

```python
"""
My Custom Framework Agent
"""
import os
from typing import List, Any, Dict, Union, AsyncGenerator
from agent_framework.core.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "my_custom_agent_v1"
        self._custom_agent = None
    
    # REQUIRED: Define agent behavior
    def get_agent_prompt(self) -> str:
        return "You are a helpful assistant."
    
    def get_agent_tools(self) -> List[callable]:
        def greet(name: str) -> str:
            """Greet a user by name."""
            return f"Hello, {name}!"
        
        return [greet]
    
    # REQUIRED: Initialize your framework
    async def initialize_agent(
        self,
        model_name: str,
        system_prompt: str,
        tools: List[callable],
        **kwargs
    ) -> None:
        """Set up your custom framework here."""
        from agent_framework.core.model_clients import ModelClientFactory
        
        # Get LLM client (handles OpenAI, Anthropic, Gemini)
        factory = ModelClientFactory()
        self._llm_client = factory.create_client(model_name=model_name)
        self._system_prompt = system_prompt
        self._tools = {tool.__name__: tool for tool in tools}
    
    # REQUIRED: Context management
    def create_fresh_context(self) -> Any:
        return {"messages": []}
    
    def serialize_context(self, ctx: Any) -> Dict[str, Any]:
        return ctx
    
    def deserialize_context(self, state: Dict[str, Any]) -> Any:
        return state
    
    # REQUIRED: Execute agent
    async def run_agent(
        self,
        query: str,
        ctx: Any,
        stream: bool = False
    ) -> Union[str, AsyncGenerator]:
        """Run your custom agent logic."""
        # Add message to context
        ctx["messages"].append({"role": "user", "content": query})
        
        # Build messages for LLM
        messages = [
            {"role": "system", "content": self._system_prompt},
            *ctx["messages"]
        ]
        
        # Call LLM
        response = await self._llm_client.create(messages=messages)
        final_response = response.choices[0].message.content
        
        # Save response
        ctx["messages"].append({"role": "assistant", "content": final_response})
        
        return final_response
    
    # OPTIONAL: Streaming support
    async def process_streaming_event(self, event: Any) -> Dict[str, Any]:
        """Convert your framework's events to unified format."""
        return {
            "type": "chunk",
            "content": str(event),
            "metadata": {}
        }


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return
    
    from agent_framework import create_basic_agent_server
    
    print("🚀 Starting custom agent on http://localhost:8000")
    create_basic_agent_server(
        agent_class=MyCustomAgent,
        host="0.0.0.0",
        port=8000,
        reload=False
    )


if __name__ == "__main__":
    main()
```

### 3. Run Your Agent

```bash
export OPENAI_API_KEY=sk-your-key-here
uv run python my_custom_agent.py
```

**You now have a custom framework agent!** This pattern works with:
- LangChain
- Haystack
- Custom implementations
- Any other AI framework

---

## Adding Tools

### For LlamaIndex Agents

Tools are simple Python functions:

```python
def get_agent_tools(self) -> List[callable]:
    def search_database(query: str) -> str:
        """Search the database for information."""
        # Your implementation
        return f"Results for: {query}"
    
    async def fetch_api(endpoint: str) -> Dict:
        """Fetch data from an API."""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.example.com/{endpoint}") as resp:
                return await resp.json()
    
    return [search_database, fetch_api]
```

### For BaseAgent

Same tool definitions, but you handle execution:

```python
async def run_agent(self, query: str, ctx: Any, stream: bool = False):
    # Your framework's tool calling logic
    # 1. Detect tool calls from LLM
    # 2. Execute tools
    # 3. Pass results back to LLM
    pass
```

**See [TOOLS_AND_MCP_GUIDE.md](TOOLS_AND_MCP_GUIDE.md) for complete details and examples.**

**Also see:**
- [CREATING_AGENTS.md](CREATING_AGENTS.md) - Full agent creation guide with tool integration
- [examples/simple_agent.py](../examples/simple_agent.py) - Working example with tools
- [examples/custom_framework_agent.py](../examples/custom_framework_agent.py) - BaseAgent tool execution

---

## Adding MCP Servers

### For LlamaIndex Agents

```python
class MyMCPAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "mcp_agent_v1"
        self.mcp_tools = []
        self._mcp_initialized = False
    
    async def _initialize_mcp_tools(self):
        """Load tools from MCP server."""
        if self._mcp_initialized:
            return
        
        from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
        
        # Connect to MCP server
        client = BasicMCPClient(
            command="uvx",
            args=["@modelcontextprotocol/server-filesystem", "/workspace"]
        )
        
        # Load tools
        mcp_tool_spec = McpToolSpec(client=client)
        function_tools = await mcp_tool_spec.to_tool_list_async()
        self.mcp_tools.extend(function_tools)
        self._mcp_initialized = True
    
    def get_agent_tools(self) -> List[callable]:
        # Combine built-in and MCP tools
        built_in = [...]  # Your tools
        return built_in + self.mcp_tools
    
    async def initialize_agent(self, model_name: str, system_prompt: str, tools: List[callable], **kwargs):
        # Load MCP tools BEFORE creating agent
        await self._initialize_mcp_tools()
        all_tools = self.get_agent_tools()
        await super().initialize_agent(model_name, system_prompt, all_tools, **kwargs)
```

### For BaseAgent

Same pattern - load MCP tools in `initialize_agent()`:

```python
async def initialize_agent(self, model_name: str, system_prompt: str, tools: List[callable], **kwargs):
    # Load MCP tools
    await self._initialize_mcp_tools()
    
    # Get all tools including MCP
    all_tools = self.get_agent_tools()
    
    # Initialize your framework with all tools
    # ...
```

**See [TOOLS_AND_MCP_GUIDE.md](TOOLS_AND_MCP_GUIDE.md) for complete MCP integration guide.**

**Also see:**
- [CREATING_AGENTS.md](CREATING_AGENTS.md) - Agent creation with MCP support
- [examples/agent_with_mcp.py](../examples/agent_with_mcp.py) - Complete MCP example

---

## Next Steps

### Learn More

#### Comprehensive Guides
- **[CREATING_AGENTS.md](CREATING_AGENTS.md)** - Complete step-by-step guide for both LlamaIndex and BaseAgent
- **[TOOLS_AND_MCP_GUIDE.md](TOOLS_AND_MCP_GUIDE.md)** - Adding tools and MCP servers to your agents
- **[AI_CONTENT_MANAGEMENT_GUIDE.md](AI_CONTENT_MANAGEMENT_GUIDE.md)** - Managing AI-generated content
- **[MULTIMODAL_TOOLS_GUIDE.md](MULTIMODAL_TOOLS_GUIDE.md)** - Working with images, audio, and video

#### Reference Documentation
- **[api-reference.md](api-reference.md)** - Complete API documentation
- **[installation-guide.md](installation-guide.md)** - Detailed installation instructions
- **[UV_TESTING_GUIDE.md](UV_TESTING_GUIDE.md)** - Testing best practices
- **[PYPI_PUBLISHING.md](PYPI_PUBLISHING.md)** - Publishing packages to PyPI

### Explore Examples

#### LlamaIndex Examples
- **[simple_agent.py](../examples/simple_agent.py)** - Basic LlamaIndex agent with tools
- **[agent_with_file_storage.py](../examples/agent_with_file_storage.py)** - File upload/download support
- **[agent_with_mcp.py](../examples/agent_with_mcp.py)** - MCP server integration

#### BaseAgent Examples
- **[custom_framework_agent.py](../examples/custom_framework_agent.py)** - Complete custom framework implementation

### Common Tasks

**Add session context to tools:**
```python
async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
    self.current_user_id = session_configuration.get('user_id')
    self.current_session_id = session_configuration.get('session_id')
    await super().configure_session(session_configuration)
```

**Change model at runtime:**
```python
# Client-side
response = client.send_message(
    "Hello",
    agent_config={"model_selection": "gpt-4"}
)
```

**Add file storage:**
```python
from agent_framework.storage.file_system_management import FileStorageFactory

async def _ensure_file_storage(self):
    if self.file_storage is None:
        self.file_storage = await FileStorageFactory.create_storage_manager()
```

**Enable MongoDB sessions:**
```bash
export SESSION_STORAGE_TYPE=mongodb
export MONGODB_CONNECTION_STRING=mongodb://localhost:27017
```

---

## Troubleshooting

### Agent not responding

1. Check API key is set: `echo $OPENAI_API_KEY`
2. Check model is valid: `curl http://localhost:8000/config/models`
3. Check logs for errors

### Tools not being called

1. Verify docstrings are clear
2. Check type hints are correct
3. Ensure model supports function calling (gpt-4, claude-3, etc.)

### MCP tools not loading

1. Install MCP package: `uv add llama-index-tools-mcp`
2. Install MCP server: `uvx install @modelcontextprotocol/server-filesystem`
3. Check `_initialize_mcp_tools()` is called before agent creation

### Import errors

```bash
# LlamaIndex agent
uv add agent-framework-lib[llamaindex]

# BaseAgent only
uv add agent-framework-lib
```

---

## Get Help

### Documentation Resources

- **[CREATING_AGENTS.md](CREATING_AGENTS.md)** - Comprehensive agent creation guide
- **[TOOLS_AND_MCP_GUIDE.md](TOOLS_AND_MCP_GUIDE.md)** - Tools and MCP integration
- **[api-reference.md](api-reference.md)** - Complete API reference
- **[All Documentation](.)** - Browse all guides

### Examples

- **[examples/](../examples/)** - All working examples
- **[simple_agent.py](../examples/simple_agent.py)** - Start here for LlamaIndex
- **[custom_framework_agent.py](../examples/custom_framework_agent.py)** - Start here for BaseAgent

### API Documentation

- **http://localhost:8000/docs** - Interactive API docs (when server is running)
- **http://localhost:8000/testapp** - Test interface
