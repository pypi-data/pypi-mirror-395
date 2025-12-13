# Creating Agents Guide

This comprehensive guide explains how to create custom agents with the Agent Framework. Whether you're using LlamaIndex or integrating a custom AI framework, this guide provides everything you need to build production-ready agents.

## Table of Contents

- [Quick Start](#quick-start)
- [Choosing Your Approach](#choosing-your-approach)
- [LlamaIndex Agent Creation](#llamaindex-agent-creation)
- [BaseAgent (Custom Framework) Creation](#baseagent-custom-framework-creation)
- [Streaming Architecture](#streaming-architecture)
- [Tool Integration](#tool-integration)
- [Best Practices](#best-practices)
- [Examples](#examples)

## Quick Start

The fastest way to create an agent is to inherit from `LlamaIndexAgent`:

```python
from agent_framework import LlamaIndexAgent, create_basic_agent_server
from typing import List

class MyAgent(LlamaIndexAgent):
    def get_agent_prompt(self) -> str:
        return "You are a helpful assistant."
  
    def get_agent_tools(self) -> List[callable]:
        return []

# Start the server
create_basic_agent_server(MyAgent, port=8000)
```

That's it! You now have a fully functional agent with automatic conversation memory, session management, streaming responses, and a web interface.

## Choosing Your Approach

The Agent Framework provides two ways to create agents:

### Decision Tree

```
Do you want to use LlamaIndex?
│
├─ YES → Use LlamaIndexAgent
│   ├─ ✅ Fastest to implement (3 required methods)
│   ├─ ✅ Automatic memory management
│   ├─ ✅ Built-in streaming support
│   ├─ ✅ Rich ecosystem of tools
│   └─ 📖 See: LlamaIndex Agent Creation
│
└─ NO → Use BaseAgent
    ├─ ✅ Framework-agnostic (LangChain, Haystack, custom, etc.)
    ├─ ✅ Full control over agent behavior
    ├─ ✅ Custom streaming implementation
    ├─ ⚠️  More methods to implement (7 required)
    └─ 📖 See: BaseAgent Creation
```

### Comparison Table

| Feature | LlamaIndexAgent | BaseAgent |
|---------|----------------|-----------|
| **Required Methods** | 3 | 7 |
| **Complexity** | Low | Medium |
| **Framework** | LlamaIndex only | Any framework |
| **Memory** | Automatic | Manual |
| **Streaming** | Built-in | Custom implementation |
| **Best For** | Quick prototypes, LlamaIndex users | Custom frameworks, full control |

---

## LlamaIndex Agent Creation

### Overview

`LlamaIndexAgent` is a concrete implementation that provides LlamaIndex-specific functionality with automatic memory management and streaming support.

### Required Methods

You must implement these 3 methods:

#### 1. `get_agent_prompt() -> str`

Define the agent's system prompt.

```python
def get_agent_prompt(self) -> str:
    """Return the system prompt for the agent."""
    return """You are a helpful calculator assistant.
    You can perform basic arithmetic operations.
    Always show your work and explain the calculation steps."""
```

**Purpose**: Defines the agent's behavior, personality, and capabilities.

**Note**: Rich content capabilities (Mermaid diagrams, Chart.js charts, forms, options blocks, tables) are automatically injected into all agent system prompts. You don't need to add these instructions manually.

**Tips**:
- Be specific about the agent's role
- List available capabilities
- Provide behavioral guidelines
- Include examples if helpful

#### 2. `get_agent_tools() -> List[callable]`

Define the tools available to the agent.

```python
def get_agent_tools(self) -> List[callable]:
    """Return list of tools for the agent."""
    
    def add(a: float, b: float) -> float:
        """Add two numbers together."""
        return a + b
    
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers together."""
        return a * b
    
    return [add, multiply]
```

**Purpose**: Extends the agent's capabilities beyond text generation.

**Requirements**:
- Each tool must have a clear function name
- Docstring (LLM reads this to understand the tool)
- Type hints (helps LLM understand parameters)
- Return value (sent back to LLM)

#### 3. `initialize_agent(model_name, system_prompt, tools, **kwargs) -> None`

Initialize the LlamaIndex agent.

```python
async def initialize_agent(
    self,
    model_name: str,
    system_prompt: str,
    tools: List[callable],
    **kwargs
) -> None:
    """Initialize the LlamaIndex agent."""
    from llama_index.core.agent.workflow import FunctionAgent
    
    # Create LLM using helper method
    llm = self.create_llm(model_name)
    
    # Create agent
    self._agent_instance = FunctionAgent(
        tools=tools,
        llm=llm,
        system_prompt=system_prompt,
        verbose=kwargs.get('verbose', True)
    )
```

**Purpose**: Sets up the LlamaIndex agent with your configuration.

**Helper Method**: Use `self.create_llm(model_name)` to automatically create the correct LLM client (OpenAI, Anthropic, or Gemini) based on the model name.

### Optional Methods

Override these methods for advanced customization:

#### Context Management

```python
def create_fresh_context(self) -> Any:
    """Create a new conversation context."""
    from llama_index.core.workflow import Context
    return Context(self._agent_instance)

def serialize_context(self, ctx: Any) -> Dict[str, Any]:
    """Serialize context for persistence."""
    from llama_index.core.workflow import JsonSerializer
    return ctx.to_dict(serializer=JsonSerializer())

def deserialize_context(self, state: Dict[str, Any]) -> Any:
    """Deserialize context from saved state."""
    from llama_index.core.workflow import Context, JsonSerializer
    return Context.from_dict(
        self._agent_instance, 
        state, 
        serializer=JsonSerializer()
    )
```

**When to override**: If you need custom context management or state persistence.

#### MCP Tools

```python
def get_mcp_server_params(self) -> List[StdioServerParams]:
    """Configure external MCP tools."""
    from autogen_ext.tools.mcp import StdioServerParams
    
    return [
        StdioServerParams(
            command='deno',
            args=['run', '-N', 'jsr:@pydantic/mcp-run-python', 'stdio'],
            read_timeout_seconds=120
        )
    ]
```

**When to override**: If you want to add Model Context Protocol tools (Python execution, file system access, etc.).

### Rich Content Configuration

All agents automatically receive rich content capabilities (Mermaid diagrams, Chart.js charts, forms, options blocks, tables). This is enabled by default.

To disable rich content for a specific session:

```python
# Via session configuration
session_config = {
    "user_id": "user123",
    "session_id": "session456",
    "enable_rich_content": False  # Disable rich content
}
```

Or via the Web UI by unchecking the "Enable rich content capabilities" checkbox.

### Complete Example

See [examples/simple_agent.py](../examples/simple_agent.py) for a complete working example.

```python
from agent_framework import LlamaIndexAgent, create_basic_agent_server
from typing import List

class CalculatorAgent(LlamaIndexAgent):
    """A simple calculator agent."""
    
    def __init__(self):
        super().__init__()
        self.agent_id = "calculator_agent_v1"
    
    def get_agent_prompt(self) -> str:
        return """You are a helpful calculator assistant.
        Use the provided tools to perform calculations."""
    
    def get_agent_tools(self) -> List[callable]:
        def add(a: int, b: int) -> int:
            """Add two numbers together."""
            return a + b
        
        def multiply(a: int, b: int) -> int:
            """Multiply two numbers together."""
            return a * b
        
        return [add, multiply]
    
    async def initialize_agent(
        self,
        model_name: str,
        system_prompt: str,
        tools: List[callable],
        **kwargs
    ) -> None:
        from llama_index.core.agent.workflow import FunctionAgent
        
        llm = self.create_llm(model_name)
        self._agent_instance = FunctionAgent(
            tools=tools,
            llm=llm,
            system_prompt=system_prompt,
            verbose=True
        )

if __name__ == "__main__":
    create_basic_agent_server(CalculatorAgent, port=8000)
```

---

## BaseAgent (Custom Framework) Creation

### Overview

`BaseAgent` is a framework-agnostic base class that allows you to integrate ANY AI framework (LangChain, Haystack, custom implementations, etc.) with the Agent Framework.

### Required Methods

You must implement these 7 methods:

#### 1. `get_agent_prompt() -> str`

Same as LlamaIndex - define the agent's system prompt.

```python
def get_agent_prompt(self) -> str:
    """Return the system prompt for the agent."""
    return "You are a helpful assistant with calculator capabilities."
```

#### 2. `get_agent_tools() -> List[callable]`

Same as LlamaIndex - define the tools available to the agent.

```python
def get_agent_tools(self) -> List[callable]:
    """Return list of tools for the agent."""
    
    def add(a: float, b: float) -> float:
        """Add two numbers together."""
        return a + b
    
    return [add]
```

#### 3. `initialize_agent(model_name, system_prompt, tools, **kwargs) -> None`

Initialize your custom framework's agent.

```python
async def initialize_agent(
    self,
    model_name: str,
    system_prompt: str,
    tools: List[callable],
    **kwargs
) -> None:
    """Initialize your custom framework's agent."""
    from agent_framework.core.model_clients import client_factory
    
    # Get LLM client (handles OpenAI, Anthropic, Gemini automatically)
    self._llm_client = client_factory.create_client(model_name=model_name)
    
    # Store configuration
    self._system_prompt = system_prompt
    self._tools = {tool.__name__: tool for tool in tools}
    
    # Initialize your framework here
    # Example for LangChain:
    # from langchain.agents import create_openai_functions_agent
    # self._agent = create_openai_functions_agent(...)
    
    # Example for Haystack:
    # from haystack.agents import Agent
    # self._agent = Agent(...)
```

**Purpose**: Set up your framework's agent with the provided configuration.

**Key Points**:
- Use `client_factory.create_client()` for automatic LLM provider detection
- Store system prompt and tools for use in `run_agent()`
- Initialize your framework's agent instance

#### 4. `create_fresh_context() -> Any`

Create a new conversation context.

```python
def create_fresh_context(self) -> Any:
    """Create a new conversation context."""
    return {
        "messages": [],  # Conversation history
        "metadata": {
            "session_id": self.current_session_id,
            "user_id": self.current_user_id,
        }
    }
```

**Purpose**: Initialize context for a new conversation.

**Return**: Any object your framework needs for context (dict, list, custom class, etc.).

**Examples**:
- LangChain: `return []` (list of messages)
- Haystack: `return {"conversation_history": [], "documents": []}`
- Custom: `return MyCustomContext()`

#### 5. `serialize_context(ctx) -> Dict[str, Any]`

Serialize context to dictionary for persistence.

```python
def serialize_context(self, ctx: Any) -> Dict[str, Any]:
    """Serialize context for persistence."""
    # For dict context, return as-is
    return ctx
    
    # For custom objects, extract data:
    # return {
    #     "messages": [msg.to_dict() for msg in ctx.messages],
    #     "metadata": ctx.metadata
    # }
```

**Purpose**: Convert context to JSON-serializable format for saving to database.

**Requirements**:
- Must return JSON-serializable dict (str, int, float, bool, None, list, dict)
- No custom objects, functions, or lambdas
- Convert datetime to ISO string if needed

#### 6. `deserialize_context(state) -> Any`

Deserialize dictionary to context object.

```python
def deserialize_context(self, state: Dict[str, Any]) -> Any:
    """Deserialize context from saved state."""
    # For dict context, return as-is
    return state
    
    # For custom objects, reconstruct:
    # ctx = MyCustomContext()
    # ctx.messages = [Message.from_dict(m) for m in state["messages"]]
    # return ctx
```

**Purpose**: Reconstruct context object from saved dictionary.

**Requirements**:
- Must return same type as `create_fresh_context()`
- Reconstruct any custom objects from the dict

#### 7. `run_agent(query, ctx, stream=False) -> Union[str, AsyncGenerator]`

Execute the agent with a query.

```python
async def run_agent(
    self,
    query: str,
    ctx: Any,
    stream: bool = False
) -> Union[str, AsyncGenerator]:
    """Execute the agent with a query."""
    if stream:
        return self._run_streaming(query, ctx)
    else:
        return await self._run_non_streaming(query, ctx)
```

**Purpose**: Main execution method that runs your framework's agent.

**Modes**:
- **Non-streaming** (`stream=False`): Return final response as string
- **Streaming** (`stream=True`): Return AsyncGenerator yielding RAW framework events

**Important**: When streaming, yield RAW framework-specific events. They will be converted to unified format via `process_streaming_event()`.

### Optional Methods

#### `process_streaming_event(event) -> Optional[Dict[str, Any]]`

Convert framework-specific streaming events to unified format.

```python
async def process_streaming_event(self, event: Any) -> Optional[Dict[str, Any]]:
    """Convert framework events to unified format."""
    # For dict events already in unified format
    if isinstance(event, dict) and "type" in event:
        return event
    
    # For LangChain events
    # if isinstance(event, dict) and event.get("type") == "llm_new_token":
    #     return {
    #         "type": "chunk",
    #         "content": event["token"],
    #         "metadata": {"source": "langchain"}
    #     }
    
    # Skip unknown events
    return None
```

**Purpose**: Normalize framework-specific events to standard format.

**Unified Format**:
```python
{
    "type": "chunk" | "tool_call" | "tool_result" | "activity" | "error",
    "content": str,
    "metadata": {...}  # Optional
}
```

**When to override**: Always override this when implementing streaming support.

### Complete Example

See [examples/custom_framework_agent.py](../examples/custom_framework_agent.py) for a complete working example with extensive comments.

```python
from agent_framework.core.base_agent import BaseAgent
from typing import List, Any, Dict, Union, AsyncGenerator

class CustomFrameworkAgent(BaseAgent):
    """Agent using custom AI framework."""
    
    def __init__(self):
        super().__init__()
        self.agent_id = "custom_agent_v1"
    
    def get_agent_prompt(self) -> str:
        return "You are a helpful assistant."
    
    def get_agent_tools(self) -> List[callable]:
        def add(a: float, b: float) -> float:
            """Add two numbers."""
            return a + b
        return [add]
    
    async def initialize_agent(
        self,
        model_name: str,
        system_prompt: str,
        tools: List[callable],
        **kwargs
    ) -> None:
        from agent_framework.core.model_clients import client_factory
        
        self._llm_client = client_factory.create_client(model_name=model_name)
        self._system_prompt = system_prompt
        self._tools = {tool.__name__: tool for tool in tools}
    
    def create_fresh_context(self) -> Any:
        return {"messages": []}
    
    def serialize_context(self, ctx: Any) -> Dict[str, Any]:
        return ctx
    
    def deserialize_context(self, state: Dict[str, Any]) -> Any:
        return state
    
    async def run_agent(
        self,
        query: str,
        ctx: Any,
        stream: bool = False
    ) -> Union[str, AsyncGenerator]:
        # Add user message to context
        ctx["messages"].append({"role": "user", "content": query})
        
        # Build messages for LLM
        messages = [
            {"role": "system", "content": self._system_prompt},
            *ctx["messages"]
        ]
        
        if stream:
            # Return streaming generator
            return self._stream_response(messages, ctx)
        else:
            # Return final response
            response = await self._llm_client.create(messages=messages)
            final_text = response.choices[0].message.content
            ctx["messages"].append({"role": "assistant", "content": final_text})
            return final_text
    
    async def _stream_response(self, messages, ctx):
        """Stream response chunks."""
        stream = await self._llm_client.create(messages=messages, stream=True)
        accumulated = ""
        
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content:
                accumulated += delta.content
                yield {
                    "type": "chunk",
                    "content": delta.content,
                    "metadata": {}
                }
        
        ctx["messages"].append({"role": "assistant", "content": accumulated})
    
    async def process_streaming_event(self, event: Any) -> Optional[Dict[str, Any]]:
        """Convert events to unified format."""
        if isinstance(event, dict) and "type" in event:
            return event
        return None
```

---

## Streaming Architecture

### Overview

The Agent Framework uses a clear separation of concerns for streaming:

```
┌─────────────────────────────────────────────────────────────┐
│  Your Agent Implementation                                  │
│                                                             │
│  run_agent(stream=True)                                     │
│    └─> Yields RAW framework-specific events                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  BaseAgent.handle_message_stream() [FINAL - DO NOT OVERRIDE]│
│                                                             │
│  Orchestrates the streaming flow:                           │
│    1. Calls run_agent(stream=True)                          │
│    2. For each event, calls process_streaming_event()       │
│    3. Converts to StructuredAgentOutput                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Your Agent Implementation                                  │
│                                                             │
│  process_streaming_event(event)                             │
│    └─> Converts framework event to unified format          │
└─────────────────────────────────────────────────────────────┘
```

### Key Principles

1. **`run_agent()`** = Framework-specific logic, yields RAW events
2. **`process_streaming_event()`** = Conversion layer, framework-specific
3. **`handle_message_stream()`** = Orchestration, framework-agnostic (DO NOT OVERRIDE)

### Event Flow

```
Your Framework          BaseAgent                    Client
───────────────         ─────────                    ──────
      │                     │                          │
      │  run_agent(stream)  │                          │
      │◄────────────────────│                          │
      │                     │                          │
      │  yield raw_event_1  │                          │
      ├────────────────────►│                          │
      │                     │                          │
      │                     │ process_streaming_event()│
      │                     │ (converts to unified)    │
      │                     │                          │
      │                     │  StructuredAgentOutput   │
      │                     ├─────────────────────────►│
      │                     │                          │
      │  yield raw_event_2  │                          │
      ├────────────────────►│                          │
      │                     │                          │
```

### Unified Event Format

All streaming events must be converted to this format:

```python
{
    "type": "chunk" | "tool_call" | "tool_result" | "activity" | "error",
    "content": str,
    "metadata": {...}  # Optional additional data
}
```

**Event Types**:
- **chunk**: Text content being streamed to the user
- **tool_call**: Agent is calling a tool
- **tool_result**: Result from a tool execution
- **activity**: General activity message (e.g., "thinking", "processing")
- **error**: Error occurred during processing

### Implementation Examples

#### Non-Streaming Mode

```python
async def run_agent(self, query, ctx, stream=False):
    if not stream:
        # Call your framework
        response = await my_framework.chat(query, ctx)
        # Return final response as string
        return response.text
```

#### Streaming Mode

```python
async def run_agent(self, query, ctx, stream=False):
    if stream:
        # Return async generator
        async def event_generator():
            async for event in my_framework.stream_chat(query, ctx):
                # Yield RAW framework events
                # DO NOT convert here - that happens in process_streaming_event()
                yield event
        return event_generator()
```

#### Event Conversion

```python
async def process_streaming_event(self, event):
    # Convert framework events to unified format
    if event.type == "text_chunk":
        return {
            "type": "chunk",
            "content": event.text,
            "metadata": {"source": "my_framework"}
        }
    elif event.type == "tool_request":
        return {
            "type": "tool_call",
            "content": "",
            "metadata": {
                "tool_name": event.tool_name,
                "tool_arguments": event.arguments
            }
        }
    # Skip unknown events
    return None
```

---

## Tool Integration

### Basic Tools

Tools are Python functions with clear docstrings and type hints:

```python
def calculate_total(items: List[Dict[str, float]]) -> float:
    """Calculate the total price of items.
    
    Args:
        items: List of items with 'price' and 'quantity' keys
    
    Returns:
        Total price
    """
    return sum(item['price'] * item['quantity'] for item in items)
```

### Tool Requirements

Each tool must have:
1. **Clear function name** (becomes tool name for LLM)
2. **Docstring** (LLM reads this to understand the tool)
3. **Type hints** (helps LLM understand parameters)
4. **Return value** (sent back to LLM)

### Accessing Session Context

Tools can access session context via `self`:

```python
def get_user_data(self) -> dict:
    """Get current user's data."""
    user_id = self.current_user_id
    session_id = self.current_session_id
    return {"user_id": user_id, "session_id": session_id}
```

### MCP Tools (Model Context Protocol)

Add external tools via MCP servers:

```python
def get_mcp_server_params(self) -> List[StdioServerParams]:
    """Configure external MCP tools."""
    from autogen_ext.tools.mcp import StdioServerParams
    
    return [
        # Python execution
        StdioServerParams(
            command='deno',
            args=['run', '-N', 'jsr:@pydantic/mcp-run-python', 'stdio'],
            read_timeout_seconds=120
        ),
        # File system access
        StdioServerParams(
            command='npx',
            args=['-y', '@modelcontextprotocol/server-filesystem', '/tmp'],
            read_timeout_seconds=60
        )
    ]
```

See [agent_with_mcp.py](../examples/agent_with_mcp.py) for a complete example.

---

## Best Practices

### 1. System Prompts

**Good System Prompt**:
```python
def get_agent_prompt(self) -> str:
    return """You are a financial advisor assistant.

    Your capabilities:
    - Calculate investment returns
    - Analyze portfolio risk
    - Provide market insights
    
    Your guidelines:
    - Always show calculations step-by-step
    - Explain financial terms when used
    - Provide disclaimers for investment advice
    
    Your personality:
    - Professional but friendly
    - Patient and educational
    """
```

### 2. Tool Design

**Good Tool Design**:
```python
def calculate_roi(
    initial_investment: float,
    final_value: float,
    years: int
) -> Dict[str, float]:
    """Calculate return on investment with annualized rate.
    
    Args:
        initial_investment: Initial investment amount in dollars
        final_value: Final value in dollars
        years: Number of years invested
    
    Returns:
        Dictionary with 'total_return' and 'annualized_return'
    
    Example:
        >>> calculate_roi(1000, 1500, 5)
        {'total_return': 50.0, 'annualized_return': 8.45}
    """
    total_return = ((final_value - initial_investment) / initial_investment) * 100
    annualized_return = ((final_value / initial_investment) ** (1/years) - 1) * 100
    
    return {
        "total_return": round(total_return, 2),
        "annualized_return": round(annualized_return, 2)
    }
```

### 3. Error Handling

**Good Error Handling**:
```python
def divide(a: float, b: float) -> Union[float, str]:
    """Divide a by b with error handling."""
    try:
        if b == 0:
            return "Error: Cannot divide by zero"
        return a / b
    except Exception as e:
        logger.error(f"Division error: {e}")
        return f"Error: {str(e)}"
```

### 4. State Management

**Good State Management**:
```python
async def get_state(self) -> Dict[str, Any]:
    """Save only necessary state."""
    state = await super().get_state()
    
    # Save only what's needed
    state['user_preferences'] = self.user_preferences
    state['session_stats'] = {
        'messages': self.message_count,
        'tools_used': self.tools_used
    }
    
    # Don't save large temporary data
    # state['large_cache'] = self.cache  # ❌ Bad
    
    return state
```

---

## Examples

### LlamaIndex Examples

- **[simple_agent.py](../examples/simple_agent.py)** - Basic calculator agent
- **[agent_with_file_storage.py](../examples/agent_with_file_storage.py)** - Agent with file upload/download
- **[agent_with_mcp.py](../examples/agent_with_mcp.py)** - Agent with MCP tools

### BaseAgent Examples

- **[custom_framework_agent.py](../examples/custom_framework_agent.py)** - Complete custom framework integration with extensive comments

### Running Examples

```bash
# Install dependencies
uv add agent-framework[llamaindex]

# Set API key
export OPENAI_API_KEY=your-key-here

# Run an example
python examples/simple_agent.py

# Open browser to http://localhost:8100/testapp
```

---

## Next Steps

- **[Tools and MCP Guide](TOOLS_AND_MCP_GUIDE.md)** - Advanced tool integration
- **[API Reference](api-reference.md)** - Complete API documentation
- **[Architecture](../ARCHITECTURE.md)** - System architecture details
- **[Testing Guide](UV_TESTING_GUIDE.md)** - Testing best practices

---

**Need Help?**

- Review the [examples](../examples/) directory
- Check the [API Reference](api-reference.md)
- Open an issue on GitHub
