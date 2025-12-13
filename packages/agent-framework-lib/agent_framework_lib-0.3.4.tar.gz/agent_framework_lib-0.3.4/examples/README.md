# Agent Framework Examples

This directory contains examples demonstrating how to use the Agent Framework to build conversational AI agents with LlamaIndex.

## Quick Start

### Prerequisites

1. **Python 3.10 or higher**
2. **API Keys** - OpenAI API key (required for all examples)

For detailed installation instructions, see the [Installation Guide](../docs/installation-guide.md).

### Quick Setup

```bash
# Navigate to examples directory
cd examples/

# Install dependencies with UV (recommended)
uv sync

# Or with pip
uv add -r requirements.txt

# Set your API key
export OPENAI_API_KEY=sk-your-key-here
```

## Automatic Memory Management

**All agents in these examples have automatic conversation memory!** This is a core feature of the Agent Framework.

### What is Automatic Memory?

Every agent you create automatically:
- ✅ **Remembers previous messages** in the conversation
- ✅ **Persists memory across sessions** - reload the page, restart the server, memory stays
- ✅ **Loads conversation history** automatically when a session starts
- ✅ **Manages token limits** - keeps recent history within model context limits (default: 30,000 tokens)
- ✅ **Isolates sessions** - each user session has its own memory


## Examples Overview

| Example | Framework | Features | Port | Best For |
|---------|-----------|----------|------|----------|
| `simple_agent.py` | LlamaIndex | Basic tools, memory | 8100 | Getting started |
| `agent_with_file_storage.py` | LlamaIndex | File operations, memory | 8101 | File handling |
| `agent_with_mcp.py` | LlamaIndex | MCP servers, memory | 8102 | External tools |
| `custom_framework_agent.py` | BaseAgent | Custom framework | 8103 | Framework integration |

## Examples

### 1. Simple Agent (`simple_agent.py`)

A minimal example showing how to create a basic agent with automatic memory in less than 50 lines of code.

**Features:**
- Simple calculator with add and multiply operations
- **Automatic conversation memory** (remembers previous calculations)
- Demonstrates the minimal implementation required
- Shows how to use LlamaIndexAgent base class
- Memory persists across page reloads

**Run:**
```bash
# With UV
uv run simple_agent.py

# With Python
python simple_agent.py
```

**Access the UI:**
- Server: http://localhost:8100
- Web UI: http://localhost:8100/testapp

**Code Structure:**
```python
class CalculatorAgent(LlamaIndexAgent):
    def get_agent_prompt(self) -> str:
        return "You are a helpful calculator assistant."
    
    def get_agent_tools(self) -> List[callable]:
        return [add, multiply]
    
    async def initialize_agent(self, model_name, system_prompt, tools, **kwargs):
        llm = self.create_llm(model_name)
        self._agent_instance = FunctionAgent(
            tools=tools,
            llm=llm,
            system_prompt=system_prompt
        )
```

**What You'll Learn:**
- How to inherit from `LlamaIndexAgent`
- How to define agent prompts and tools
- How to initialize a LlamaIndex agent
- How to handle messages

---

### 2. Agent with File Storage (`agent_with_file_storage.py`)

Demonstrates how to integrate file storage capabilities with automatic memory management.

**Features:**
- Create text files
- List stored files
- Read file contents
- Automatic file storage backend management
- Memory includes file upload context

**Run:**
```bash
# With UV
uv run agent_with_file_storage.py

# With Python
python agent_with_file_storage.py
```

**Access the UI:**
- Server: http://localhost:8101
- Web UI: http://localhost:8101/testapp

**Key Concepts:**
```python
from agent_framework.storage.file_system_management import FileStorageFactory

class FileStorageAgent(LlamaIndexAgent):
    async def _ensure_file_storage(self):
        if self.file_storage is None:
            self.file_storage = await FileStorageFactory.create_storage_manager()
    
    def get_agent_tools(self):
        async def create_file(filename: str, content: str) -> str:
            await self._ensure_file_storage()
            file_id = await self.file_storage.store_file(...)
            return f"File created with ID: {file_id}"
        
        return [create_file, list_files, read_file]
```

**What You'll Learn:**
- How to integrate FileStorageManager
- How to create async tools
- How to create and read files
- How to manage file metadata
- How memory works with file operations



**Storage Backends:**
- Local filesystem (default)
- S3 (configure with AWS credentials)
- MinIO (configure with MinIO endpoint)

---

### 3. Agent with MCP (`agent_with_mcp.py`)

Shows how to configure an agent to use external MCP (Model Context Protocol) servers with automatic memory.

**Features:**
- Integration with external MCP servers
- **Automatic conversation memory** (remembers tool usage)
- Access to filesystem operations
- HTTP requests via fetch server
- Memory includes MCP tool results
- Extensible with any MCP-compatible server

**Run:**
```bash
# Install MCP server first (optional)
uvx install @modelcontextprotocol/server-filesystem

# Set workspace directory (optional)
export MCP_FILESYSTEM_DIR=~/mcp_workspace

# Run the example
uv run agent_with_mcp.py
```

**Access the UI:**
- Server: http://localhost:8102
- Web UI: http://localhost:8102/testapp

**Key Concepts:**
```python
class MCPAgent(LlamaIndexAgent):
    def get_mcp_server_params(self) -> Optional[Dict[str, Any]]:
        return {
            "command": "uvx",
            "args": [
                "@modelcontextprotocol/server-filesystem",
                "/path/to/allowed/directory"
            ],
            "env": {}
        }
```

**What You'll Learn:**
- How to configure MCP servers
- How to use external tools
- How to combine built-in and MCP tools
- How to manage MCP server lifecycle

**Available MCP Servers:**
- `@modelcontextprotocol/server-filesystem` - File system operations
- `@modelcontextprotocol/server-fetch` - HTTP requests
- `@modelcontextprotocol/server-github` - GitHub API
- `@modelcontextprotocol/server-postgres` - Database operations

Learn more: https://modelcontextprotocol.io/

---

### 4. Custom Framework Agent (`custom_framework_agent.py`)

Demonstrates how to integrate a custom AI framework (LangChain, Haystack, etc.) using BaseAgent.

**Features:**
- Direct BaseAgent implementation
- Custom agent initialization
- Manual tool execution
- Framework-agnostic approach
- Shows integration pattern for any framework

**Run:**
```bash
# With UV
uv run custom_framework_agent.py

# With Python
python custom_framework_agent.py
```

**Access the UI:**
- Server: http://localhost:8103
- Web UI: http://localhost:8103/testapp

**Key Concepts:**
```python
from agent_framework.core.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    async def initialize_agent(self, model_name, system_prompt, tools, **kwargs):
        # Initialize YOUR framework here
        # Examples: LangChain, Haystack, custom implementation
        from agent_framework.core.model_clients import client_factory
        self._llm_client = client_factory.create_client(model_name=model_name)
        self._tools = {tool.__name__: tool for tool in tools}
    
    async def run_agent(self, query: str, ctx: Any, stream: bool = False):
        # Your framework's execution logic
        # Handle tool calling, streaming, etc.
        pass
```

**What You'll Learn:**
- How to use BaseAgent for custom frameworks
- How to integrate any AI framework
- How to handle tool execution manually
- How to implement streaming
- How to manage conversation context

**Use This Pattern For:**
- LangChain integration
- Haystack integration
- Custom agent implementations
- Framework migration
- Specialized agent architectures

---

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-openai-key-here

# Optional: Model Selection
OPENAI_API_MODEL=gpt-4o-mini

# Optional: File Storage (for agent_with_file_storage.py)
# Local storage is used by default
# For S3:
AWS_S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1

# For MinIO:
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=agent-files

# Optional: MCP Configuration (for agent_with_mcp.py)
MCP_FILESYSTEM_DIR=~/mcp_workspace
```

### Agent Configuration

You can customize agent behavior by modifying the configuration:

```python
from agent_framework.core.agent_interface import AgentConfig

# Create custom configuration
agent_config = AgentConfig(
    temperature=0.7,
    max_tokens=1000,
    model_selection="gpt-4"
)

# Use in agent initialization
agent = MyAgent()
# Configuration is applied automatically based on environment
```

## Development

### Running with Different Models

```bash
# Use GPT-4
export OPENAI_API_MODEL=gpt-4
uv run simple_agent.py

# Use GPT-3.5
export OPENAI_API_MODEL=gpt-3.5-turbo
uv run simple_agent.py
```

### Running Examples

Each example starts a web server with an interactive UI:

```bash
# Start simple agent (port 8100)
uv run simple_agent.py

# Start file storage agent (port 8101)
uv run agent_with_file_storage.py

# Start MCP agent (port 8102)
uv run agent_with_mcp.py
```

**Access the Web UI:**
- Simple Agent: http://localhost:8100/testapp
- File Storage Agent: http://localhost:8101/testapp
- MCP Agent: http://localhost:8102/testapp

**Using the UI:**
1. Open the URL in your browser
2. Type your message in the chat input
3. Press Enter or click Send
4. Watch the agent respond with tool calls and results

### Debugging

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Common Issues

### Issue: "OPENAI_API_KEY not set"
**Solution:** Create a `.env` file with your OpenAI API key:
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Issue: "Module not found: agent_framework"
**Solution:** Install the framework in editable mode:
```bash
uv add --editable ../
# or
uv add -e ../
```

### Issue: "MCP server not found"
**Solution:** Install the MCP server:
```bash
uvx install @modelcontextprotocol/server-filesystem
```

### Issue: "File storage error"
**Solution:** Ensure you have write permissions in the storage directory:
```bash
mkdir -p ~/.agent_framework/storage
chmod 755 ~/.agent_framework/storage
```

### Issue: "Agent doesn't remember previous messages"
**Solution:** Check the server logs for memory-related messages:
```
Look for these emoji indicators:
🆕 Creating new memory for session X - New memory created
✅ Using cached memory for session X - Memory reused from cache
📚 Loaded X messages into memory - History loaded from storage
🧠 Passing memory to agent - Memory passed to LlamaIndex
🔄 Session changed to X - Session switch detected
```

**Troubleshooting steps:**
1. Check that the session ID is consistent (same browser session)
2. Verify storage is working (check web interface history)
3. Look for error messages in server logs
4. Ensure the agent server hasn't been restarted (memory cache clears but reloads from storage)

### Issue: "Memory not persisting across page reloads"
**Solution:** This usually means storage isn't working properly:
```bash
# Check storage directory exists and is writable
ls -la ~/.agent_framework/storage/

# Check server logs for storage errors
# Look for messages about loading/saving session data
```

## Next Steps

1. **Customize the examples** - Modify the prompts and tools to fit your use case
2. **Add more tools** - Create custom tools for your specific needs
3. **Deploy your agent** - Use the web server to expose your agent via HTTP
4. **Explore advanced features** - Check the main documentation for streaming, state management, and more

## Additional Resources

- [Main Documentation](../docs/)
- [API Reference](../docs/api-reference.md)
- [Creating Agents Guide](../docs/creating-agents.md)
- [Architecture Overview](../ARCHITECTURE.md)

## Support

For issues and questions:
- Check the [main documentation](../docs/)
- Review the [API reference](../docs/api-reference.md)
- Open an issue on GitHub
