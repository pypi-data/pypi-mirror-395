# Agent Framework Library

A comprehensive Python framework for building and serving conversational AI agents with FastAPI. Create production-ready AI agents in minutes with automatic session management, streaming responses, file storage, and easy MCP integration.

**Key Features:**
- 🚀 **Quick Setup** - Create agents in 10-15 minutes
- 🔌 **Easy MCP Integration** - Connect to external tools effortlessly
- 🛠️ **Off-the-Shelf Tools** - Pre-built tools for files, PDFs, charts, and more
- 🔄 **Multi-Provider Support** - OpenAI, Anthropic, Gemini
- 💾 **Session Management** - Automatic conversation persistence
- 📁 **File Storage** - Local, S3, MinIO support

## Installation

```bash
# Install with LlamaIndex support (recommended)
uv add agent-framework-lib[llamaindex]

# Install with MCP support
uv add agent-framework-lib[llamaindex,mcp]

# Install with all features
uv add agent-framework-lib[all]

# Or with pip
pip install agent-framework-lib[llamaindex]
```

**Available extras:** `llamaindex`, `mcp`, `mongodb`, `s3`, `minio`, `multimod`

**Optional: System Dependencies**

The framework **automatically detects and configures** system libraries. Manual installation is only needed if you encounter issues:

**For PDF Generation (WeasyPrint):**
```bash
# macOS
brew install pango gdk-pixbuf libffi cairo

# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libcairo2

# Fedora/RHEL
sudo dnf install pango gdk-pixbuf2 libffi-devel cairo
```

**For Chart/Mermaid Image Generation (Playwright):**
```bash
# Install Playwright and browser
uv add playwright
playwright install chromium

# Or with pip
pip install playwright
playwright install chromium
```

The framework handles library path configuration automatically on startup.



## 🚀 Getting Started

### Create Your First Agent

Here's a complete, working agent with LlamaIndex:

```python
from typing import List
from agent_framework import LlamaIndexAgent, create_basic_agent_server
from llama_index.core.tools import FunctionTool

class MyAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        # Required: Unique agent ID for session isolation
        self.agent_id = "my_calculator_agent"
    
    def get_agent_prompt(self) -> str:
        """Define your agent's behavior and personality."""
        return "You are a helpful calculator assistant."
  
    def get_agent_tools(self) -> List[callable]:
        """Define the tools your agent can use."""
        def add(a: float, b: float) -> float:
            """Add two numbers together."""
            return a + b
        
        def multiply(a: float, b: float) -> float:
            """Multiply two numbers together."""
            return a * b
        
        return [
            FunctionTool.from_defaults(fn=add),
            FunctionTool.from_defaults(fn=multiply)
        ]

# Start server - includes streaming, session management, web UI
create_basic_agent_server(MyAgent, port=8000)
```

**Required Methods:**
- `__init__()` - Set unique `agent_id`
- `get_agent_prompt()` - Return system prompt string
- `get_agent_tools()` - Return list of tools (can be empty)

**Optional Methods (have default implementations):**
- `create_fresh_context()` - Create new LlamaIndex Context (default provided)
- `serialize_context(ctx)` - Serialize context for persistence (default provided)
- `deserialize_context(state)` - Deserialize context from state (default provided)
- `initialize_agent()` - Customize agent creation (default: FunctionAgent)
- `configure_session()` - Add session setup logic

**That's it!** The framework provides default implementations for context management (state persistence), so you only need to implement the three core methods above.

**Run it:**
```bash
# Set your API key
export OPENAI_API_KEY=sk-your-key-here

# Run the agent
python my_agent.py

# Open http://localhost:8000/ui
```

## ⚙️ Configure Your Agent

### Environment Setup

Create a `.env` file:

```env
# Required: At least one API key
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GEMINI_API_KEY=your-gemini-key

# Model Configuration
DEFAULT_MODEL=gpt-5-mini
OPENAI_API_MODEL=gpt-5

# Session Storage (optional)
SESSION_STORAGE_TYPE=memory  # or "mongodb"
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE_NAME=agent_sessions

# File Storage (optional)
LOCAL_STORAGE_PATH=./file_storage
AWS_S3_BUCKET=my-bucket
S3_AS_DEFAULT=false
```

### LlamaIndex Agent Configuration

Control model behavior in your agent:

```python
class MyAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "my_agent"
        # Default model config (can be overridden per session)
        self.default_temperature = 0.7
        self.default_model = "gpt-5-mini"
```

**Runtime Configuration:**

Users can override settings per session via the API or web UI:
- Model selection (gpt-5, claude-4.5-sonnet, gemini-pro)
- Temperature (0.0 - 1.0)
- Max tokens
- System prompt override

## 🛠️ Off-the-Shelf Tools

The framework provides ready-to-use tools for common tasks. Import from `agent_framework.tools`:

### File Management Tools

```python
from agent_framework.tools import (
    CreateFileTool,      # Create text files
    ListFilesTool,       # List stored files
    ReadFileTool,        # Read file contents
    GetFilePathTool      # Get file system path
)
```

### PDF Generation Tools

```python
from agent_framework.tools import (
    CreatePDFFromMarkdownTool,  # Generate PDF from markdown
    CreatePDFFromHTMLTool,      # Generate PDF from HTML
    CreatePDFWithImagesTool     # Generate PDF with embedded images
)
```

### Chart & Visualization Tools

```python
from agent_framework.tools import (
    ChartToImageTool,    # Convert Chart.js config to PNG
    MermaidToImageTool,  # Convert Mermaid diagram to PNG
    TableToImageTool     # Convert table data to PNG
)
```

### Using Off-the-Shelf Tools

```python
from agent_framework import LlamaIndexAgent
from agent_framework.storage.file_system_management import FileStorageFactory
from agent_framework.tools import CreateFileTool, ListFilesTool, CreatePDFFromMarkdownTool

class MyAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "my_agent"
        self.file_storage = None
        
        # Initialize tools
        self.tools = [
            CreateFileTool(),
            ListFilesTool(),
            CreatePDFFromMarkdownTool()
        ]
    
    async def _ensure_file_storage(self):
        if self.file_storage is None:
            self.file_storage = await FileStorageFactory.create_storage_manager()
    
    async def configure_session(self, session_configuration):
        user_id = session_configuration.get('user_id', 'default_user')
        session_id = session_configuration.get('session_id')
        
        await self._ensure_file_storage()
        
        # Inject dependencies into tools
        for tool in self.tools:
            tool.set_context(
                file_storage=self.file_storage,
                user_id=user_id,
                session_id=session_id
            )
        
        await super().configure_session(session_configuration)
    
    def get_agent_tools(self):
        return [tool.get_tool_function() for tool in self.tools]
```

**Key Pattern:**
1. Instantiate tools in `__init__()`
2. Initialize file storage in `configure_session()`
3. Inject context with `tool.set_context()`
4. Return tool functions in `get_agent_tools()`

## 🔧 Create Custom Tools

Custom tools extend your agent's capabilities. The tool name and docstring are crucial - they tell the agent when and how to use the tool.

### Basic Custom Tool

```python
from llama_index.core.tools import FunctionTool

def get_weather(city: str) -> str:
    """Get the current weather for a specific city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A description of the current weather
    """
    # Your implementation here
    return f"The weather in {city} is sunny, 22°C"

# Add to your agent
class MyAgent(LlamaIndexAgent):
    def get_agent_tools(self):
        return [FunctionTool.from_defaults(fn=get_weather)]
```

**Important:**
- **Function name** should be explicit and descriptive (e.g., `get_weather`, not `weather`)
- **Docstring** is added as the tool description - the agent uses this to understand when to call the tool
- **Type hints** help the agent understand parameters
- **Args/Returns documentation** provides additional context

### Custom Tool with Dependencies

For tools that need file storage or other dependencies:

```python
from agent_framework.tools.base_tool import AgentTool

class MyCustomTool(AgentTool):
    """Base class handles dependency injection."""
    
    def execute(self, param1: str, param2: int) -> str:
        """Process data and store results.
        
        Args:
            param1: Description of first parameter
            param2: Description of second parameter
            
        Returns:
            Result description
        """
        # Access injected dependencies
        user_id = self.user_id
        session_id = self.session_id
        file_storage = self.file_storage
        
        # Your logic here
        result = f"Processed {param1} with {param2}"
        
        # Store file if needed
        file_id = await file_storage.store_file(
            user_id=user_id,
            session_id=session_id,
            filename="result.txt",
            content=result.encode()
        )
        
        return f"Result stored with ID: {file_id}"

# Use in your agent
class MyAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "my_agent"
        self.custom_tool = MyCustomTool()
    
    async def configure_session(self, session_configuration):
        # Inject dependencies
        self.custom_tool.set_context(
            file_storage=self.file_storage,
            user_id=session_configuration.get('user_id'),
            session_id=session_configuration.get('session_id')
        )
        await super().configure_session(session_configuration)
    
    def get_agent_tools(self):
        return [self.custom_tool.get_tool_function()]
```

### Tool Naming Best Practices

```python
# ✅ GOOD - Explicit and clear
def calculate_mortgage_payment(principal: float, rate: float, years: int) -> float:
    """Calculate monthly mortgage payment."""
    pass

def send_email_notification(recipient: str, subject: str, body: str) -> bool:
    """Send an email notification to a recipient."""
    pass

# ❌ BAD - Too vague
def calculate(x: float, y: float) -> float:
    """Do calculation."""
    pass

def send(data: str) -> bool:
    """Send something."""
    pass
```

## 🔌 Adding MCP Servers

MCP (Model Context Protocol) allows your agent to connect to external tools and services.

### Basic MCP Setup

```python
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

class MyAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "my_agent"
        self.mcp_tools = []
        self._mcp_initialized = False
    
    async def _initialize_mcp_tools(self):
        """Load tools from MCP servers."""
        if self._mcp_initialized:
            return
        
        # Configure your MCP server
        mcp_configs = [
            {
                "command": "uvx",
                "args": ["mcp-server-filesystem"],
                "env": {"FILESYSTEM_ROOT": "/path/to/workspace"}
            }
        ]
        
        for config in mcp_configs:
            client = BasicMCPClient(
                config["command"],
                args=config["args"],
                env=config.get("env", {})
            )
            
            # Load tools from the MCP server
            mcp_tool_spec = McpToolSpec(client=client)
            tools = await mcp_tool_spec.to_tool_list_async()
            self.mcp_tools.extend(tools)
        
        self._mcp_initialized = True
    
    async def initialize_agent(self, model_name, system_prompt, tools, **kwargs):
        # Load MCP tools before initializing agent
        await self._initialize_mcp_tools()
        
        # Combine with other tools
        all_tools = self.get_agent_tools()
        await super().initialize_agent(model_name, system_prompt, all_tools, **kwargs)
    
    def get_agent_tools(self):
        # Return built-in tools + MCP tools
        return self.mcp_tools
```

### Multiple MCP Servers

```python
def _get_mcp_configs(self):
    """Configure multiple MCP servers."""
    return [
        {
            "name": "filesystem",
            "command": "uvx",
            "args": ["mcp-server-filesystem"],
            "env": {"FILESYSTEM_ROOT": "/workspace"}
        },
        {
            "name": "github",
            "command": "uvx",
            "args": ["mcp-server-github"],
            "env": {
                "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")
            }
        },
        {
            "name": "python",
            "command": "uvx",
            "args": ["mcp-run-python", "stdio"]
        }
    ]
```

### Popular MCP Servers

```bash
# Filesystem operations
uvx mcp-server-filesystem

# GitHub integration
uvx mcp-server-github

# Python code execution
uvx mcp-run-python

# Database access
uvx mcp-neo4j-cypher
uvx mcp-server-postgres
```

**Installation:**
```bash
# Install with MCP support
uv add agent-framework-lib[llamaindex,mcp]

# Or add MCP to existing installation
uv add agent-framework-lib[mcp]

# MCP servers are run via uvx (no separate install needed)
```

## 📝 Rich Content Capabilities (Automatic)

All agents automatically support rich content generation including:
- 📊 **Mermaid diagrams** (version 10.x syntax)
- 📈 **Chart.js charts** (bar, line, pie, doughnut, polarArea, radar, scatter, bubble)
- 📋 **Interactive forms** (formDefinition JSON)
- 🔘 **Clickable option buttons** (optionsblock)
- 📑 **Formatted tables** (tabledata)

**This is automatic!** The framework injects rich content instructions into all agent system prompts by default. You don't need to add anything to your `get_agent_prompt()`.

### Disabling Rich Content

If you need to disable automatic rich content injection for a specific agent or session:

**Via Session Configuration (UI or API):**
```python
# When initializing a session
session_config = {
    "user_id": "user123",
    "session_id": "session456",
    "enable_rich_content": False  # Disable rich content
}
```

**Via Web UI:**
Uncheck the "Enable rich content capabilities" checkbox when creating a session.

### Format Examples

**Chart:**
````markdown
```chart
{
  "type": "chartjs",
  "chartConfig": {
    "type": "bar",
    "data": {
      "labels": ["Mon", "Tue", "Wed"],
      "datasets": [{
        "label": "Sales",
        "data": [120, 150, 100]
      }]
    }
  }
}
```
````

**Options Block:**
````markdown
```optionsblock
{
  "question": "What would you like to do?",
  "options": [
    {"text": "Continue", "value": "continue"},
    {"text": "Cancel", "value": "cancel"}
  ]
}
```
````

**Table:**
````markdown
```tabledata
{
  "caption": "Sales Data",
  "headers": ["Month", "Revenue"],
  "rows": [["Jan", "$1000"], ["Feb", "$1200"]]
}
```
````

## 🎯 All Together: Complete Multi-Skills Agent

Here's a complete example combining all features - MCP, off-the-shelf tools, custom tools, and format support:

```python
import os
from typing import List, Any, Dict
from agent_framework import LlamaIndexAgent, create_basic_agent_server
from agent_framework.storage.file_system_management import FileStorageFactory
from agent_framework.tools import (
    CreateFileTool, ListFilesTool, ReadFileTool,
    CreatePDFFromMarkdownTool, CreatePDFFromHTMLTool,
    ChartToImageTool, MermaidToImageTool, CreatePDFWithImagesTool, TableToImageTool
)
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

class MultiSkillsAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "multi_skills_agent_v1"
        self.file_storage = None
        self.mcp_tools = []
        self._mcp_initialized = False
        
        # Off-the-shelf tools
        self.file_tools = [
            CreateFileTool(),
            ListFilesTool(),
            ReadFileTool(),
            CreatePDFFromMarkdownTool(),
            CreatePDFFromHTMLTool(),
            ChartToImageTool(),
            MermaidToImageTool(),
            TableToImageTool(),
            CreatePDFWithImagesTool()
        ]
    
    async def _ensure_file_storage(self):
        if self.file_storage is None:
            self.file_storage = await FileStorageFactory.create_storage_manager()
    
    async def configure_session(self, session_configuration: Dict[str, Any]):
        user_id = session_configuration.get('user_id', 'default_user')
        session_id = session_configuration.get('session_id')
        
        await self._ensure_file_storage()
        
        # Inject context into file tools
        for tool in self.file_tools:
            tool.set_context(
                file_storage=self.file_storage,
                user_id=user_id,
                session_id=session_id
            )
        
        await super().configure_session(session_configuration)
    
    async def _initialize_mcp_tools(self):
        if self._mcp_initialized:
            return
        
        try:
            from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
        except ImportError:
            return
        
        # Configure MCP servers
        mcp_configs = [
            {
                "command": "uvx",
                "args": ["mcp-run-python", "stdio"]
            }
        ]
        
        for config in mcp_configs:
            try:
                client = BasicMCPClient(config["command"], args=config["args"])
                mcp_tool_spec = McpToolSpec(client=client)
                tools = await mcp_tool_spec.to_tool_list_async()
                self.mcp_tools.extend(tools)
            except Exception as e:
                print(f"MCP initialization failed: {e}")
        
        self._mcp_initialized = True
    
    def get_agent_prompt(self) -> str:
        return """You are a helpful assistant with multiple capabilities:
        
        - Execute Python code via MCP
        - Create, read, and list files
        - Generate PDF documents from markdown or HTML
        - Create charts, mermaid diagrams, and tables
        - Present forms and option blocks to users
        
        You can generate markdown, mermaid diagrams, charts, code blocks, forms and optionsblocks.
        ALWAYS include option blocks when asking the user to select an option!
        
        ... See the format section above
        """
    
    def get_agent_tools(self) -> List[callable]:
        # Combine all tools
        all_tools = []
        all_tools.extend([tool.get_tool_function() for tool in self.file_tools])
        all_tools.extend(self.mcp_tools)
        return all_tools
    
    async def initialize_agent(self, model_name, system_prompt, tools, **kwargs):
        await self._initialize_mcp_tools()
        all_tools = self.get_agent_tools()
        await super().initialize_agent(model_name, system_prompt, all_tools, **kwargs)

# Start the server
if __name__ == "__main__":
    create_basic_agent_server(MultiSkillsAgent, port=8000)
```

**Run it:**
```bash
export OPENAI_API_KEY=sk-your-key
python multi_skills_agent.py
# Open http://localhost:8000/ui
```

**Full example:** See `examples/agent_example_multi_skills.py` for the complete implementation with full format support prompt.

## 🌐 Web Interface

The framework includes a built-in web UI for testing and interacting with your agent.

**Access:** `http://localhost:8000/ui`

**Features:**
- 💬 Real-time message streaming
- 🎨 Rich format rendering (charts, tables, mermaid diagrams)
- 📁 File upload and management
- ⚙️ Model and parameter configuration
- 💾 Session management
- 📊 Conversation history
- 🎯 Interactive option blocks and forms

**Quick Test:**
```bash
# Start your agent
python my_agent.py

# Open in browser
open http://localhost:8000/ui
```

The UI automatically detects and renders:
- Chart.js visualizations from `chart` blocks
- Mermaid diagrams from `mermaid` blocks
- Tables from `tabledata` blocks
- Interactive forms from `formDefinition` JSON
- Clickable options from `optionsblock`

**API Documentation:** `http://localhost:8000/docs` (Swagger UI)

## 📚 Additional Resources

### Documentation
- **[Installation Guide](#installation-guide)** - Detailed setup instructions
- **[Configuration Guide](#configuratio-guide)** - Environment and settings configuration
- **[Creating Agents Guide](#creating-agents)** - Guide to building custom agents
- **[Tools and MCP Guide](#tools-and-mcp)** - Tools and MCP integration
- **[API Reference](#api-reference)** - Complete API documentation

### Examples
- **[Simple Agent](#example-simple-agent)** - Basic calculator agent
- **[File Storage Agent](#example-file-storage)** - File management
- **[MCP Integration](#example-mcp)** - MCP integration
- **[Multi-Skills Agent](#example-multi-skills)** - Complete multi-skills agent
- **[Custom Framework Agent](#example-custom-framework)** - Custom framework implementation

### API Endpoints

**Core:**
- `POST /message` - Send message to agent
- `POST /init` - Initialize session
- `POST /end` - End session
- `GET /sessions` - List sessions

**Files:**
- `POST /files/upload` - Upload file
- `GET /files/{file_id}/download` - Download file
- `GET /files` - List files

**Full API docs:** `http://localhost:8000/docs`

### Authentication

```env
# API Key Authentication
REQUIRE_AUTH=true
API_KEYS=sk-key-1,sk-key-2
```

```bash
curl -H "Authorization: Bearer sk-key-1" \
  http://localhost:8000/message \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!"}'
```

---

**Quick Links:**
- 🎨 [Web UI](http://localhost:8000/ui)
- 📖 [API Docs](http://localhost:8000/docs)
- ⚙️ [Config Test](http://localhost:8000/config/models)
