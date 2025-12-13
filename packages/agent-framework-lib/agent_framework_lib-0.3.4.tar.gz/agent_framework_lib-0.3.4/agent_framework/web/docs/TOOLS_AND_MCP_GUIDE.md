# Tools and MCP Integration Guide

This guide explains how to add tools and MCP (Model Context Protocol) servers to your agents, including the new reusable tools architecture.

**Related Documentation:**
- [Creating Agents Guide](#creating-agents) - Complete guide to creating agents
- [Simple Agent Example](#example-simple-agent) - Basic LlamaIndex agent with tools
- [File Storage Example](#example-file-storage) - Agent with reusable tools
- [MCP Integration Example](#example-mcp) - LlamaIndex agent with MCP
- [Custom Framework Example](#example-custom-framework) - BaseAgent with tools

## Table of Contents

1. [Reusable Tools Architecture](#reusable-tools-architecture)
2. [Available Tools](#available-tools)
3. [Using Reusable Tools in Your Agent](#using-reusable-tools-in-your-agent)
4. [Creating Custom Tools](#creating-custom-tools)
5. [Adding Tools to LlamaIndex Agents](#adding-tools-to-llamaindex-agents)
6. [Adding Tools to BaseAgent (Custom Framework)](#adding-tools-to-baseagent-custom-framework)
7. [Adding MCP Servers to LlamaIndex Agents](#adding-mcp-servers-to-llamaindex-agents)
8. [Adding MCP Servers to BaseAgent](#adding-mcp-servers-to-baseagent)
9. [Dependency Management](#dependency-management)
10. [Troubleshooting](#troubleshooting)
11. [Tool Best Practices](#tool-best-practices)

---

## Reusable Tools Architecture

The Agent Framework provides a reusable tools architecture that allows you to create tools once and use them across multiple agents with proper dependency injection and error handling.

### Overview

The reusable tools architecture is built around the `AgentTool` base class, which provides:

- **Dependency Injection**: Tools receive their dependencies (file storage, user context) via `set_context()`
- **Error Handling**: Consistent error handling with `ToolDependencyError` for missing dependencies
- **Type Safety**: Properly typed callable functions with complete docstrings
- **Reusability**: Tools can be used across different agents without modification
- **Testability**: Tools can be tested independently of agents

### Key Concepts

**AgentTool Base Class**: All reusable tools inherit from `AgentTool` and implement `get_tool_function()` to return the actual callable function.

**Context Injection**: Tools receive their runtime dependencies (file storage, user ID, session ID) via the `set_context()` method, which is called by the agent during session configuration.

**Tool Functions**: The actual callable functions that agents use, returned by `get_tool_function()`. These functions have complete docstrings and type hints for LLM understanding.

### Architecture Pattern

```python
from agent_framework.tools import AgentTool

class MyTool(AgentTool):
    """Tool description for LLM."""
    
    def get_tool_function(self) -> Callable:
        """Return the tool function."""
        
        async def my_function(param: str) -> str:
            """Function docstring that LLM sees."""
            # Ensure tool was initialized
            self._ensure_initialized()
            
            # Use injected dependencies
            result = await self.file_storage.some_operation(
                user_id=self.current_user_id,
                session_id=self.current_session_id
            )
            
            return "Success message"
        
        return my_function
```

---

## Available Tools

The framework provides several built-in tools that you can use immediately in your agents:

**File Storage Tools:**
- `CreateFileTool` - Create new text files
- `ListFilesTool` - List all files for user/session
- `ReadFileTool` - Read file content by ID

**Chart Generation Tools:**
- `ChartToImageTool` - Convert Chart.js configs to PNG images
- `TableToImageTool` - Convert table data to PNG images
- `MermaidToImageTool` - Convert Mermaid diagrams to PNG images

**PDF Generation Tools:**
- `CreatePDFFromMarkdownTool` - Create PDFs from Markdown
- `CreatePDFFromHTMLTool` - Create PDFs from HTML
- `CreatePDFWithImagesTool` - Create PDFs with automatic image embedding

**File Access Tools:**
- `GetFilePathTool` - Get file paths or data URIs
- `GetFileAsDataURITool` - Convert files to data URIs

### File Storage Tools

Tools for managing files in the file storage system.

#### CreateFileTool

Create new text files with specified content.

```python
from agent_framework.tools import CreateFileTool

tool = CreateFileTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
create_file = tool.get_tool_function()

# Usage by LLM
result = await create_file("report.txt", "This is my report content...")
# Returns: "File 'report.txt' created successfully with ID: abc-123"
```

**Parameters:**
- `filename` (str): Name for the new file
- `content` (str): Text content to write

**Returns:** Success message with file ID or error message

#### ListFilesTool

List all files for the current user and session.

```python
from agent_framework.tools import ListFilesTool

tool = ListFilesTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
list_files = tool.get_tool_function()

# Usage by LLM
result = await list_files()
# Returns:
# Files:
# 1. report.txt (ID: abc-123, Size: 1.2 KB)
# 2. data.json (ID: def-456, Size: 3.4 KB)
```

**Parameters:** None

**Returns:** Formatted list of files with IDs and sizes

#### ReadFileTool

Read file content by file ID.

```python
from agent_framework.tools import ReadFileTool

tool = ReadFileTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
read_file = tool.get_tool_function()

# Usage by LLM
result = await read_file("abc-123")
# Returns:
# File: report.txt
# Content:
# This is the file content...
```

**Parameters:**
- `file_id` (str): Unique identifier of the file to read

**Returns:** Formatted string with filename and content

### Chart Generation Tools

Tools for creating chart visualizations and saving them as images.

**Note:** Chart tools require Playwright. See [Dependency Management](#dependency-management) section.

#### ChartToImageTool

Convert Chart.js configurations to PNG images.

```python
from agent_framework.tools import ChartToImageTool

tool = ChartToImageTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
save_chart = tool.get_tool_function()

# Usage by LLM
chart_config = '''
{
    "type": "bar",
    "data": {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "datasets": [{
            "label": "Sales",
            "data": [120, 150, 100, 180, 200],
            "backgroundColor": "rgba(54, 162, 235, 0.6)"
        }]
    },
    "options": {
        "responsive": true,
        "plugins": {
            "title": {
                "display": true,
                "text": "Weekly Sales"
            }
        }
    }
}
'''

result = await save_chart(
    chart_config=chart_config,
    filename="weekly_sales",
    width=800,
    height=600,
    background_color="white"
)
# Returns: "Chart saved successfully as PNG! File ID: xyz-789, Filename: weekly_sales.png"
```

**Parameters:**
- `chart_config` (str): JSON string containing the complete Chart.js configuration (type, data, options)
- `filename` (str): Name for the output PNG file (without extension)
- `width` (int, optional): Width of the chart in pixels (default: 800)
- `height` (int, optional): Height of the chart in pixels (default: 600)
- `background_color` (str, optional): Background color for the chart (default: "white")

**Supported Chart Types:**
- Bar charts (`"type": "bar"`)
- Line charts (`"type": "line"`)
- Pie charts (`"type": "pie"`)
- Doughnut charts (`"type": "doughnut"`)
- Radar charts (`"type": "radar"`)
- Polar area charts (`"type": "polarArea"`)
- Bubble charts (`"type": "bubble"`)
- Scatter charts (`"type": "scatter"`)

**Returns:** Success message with file ID or error message

#### TableToImageTool

Convert table data to PNG images with styled HTML rendering.

```python
from agent_framework.tools import TableToImageTool

tool = TableToImageTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
save_table = tool.get_tool_function()

# Usage by LLM - with list of lists
table_data = [
    ["Product", "Q1", "Q2", "Q3", "Q4"],
    ["Widget A", "120", "150", "180", "200"],
    ["Widget B", "90", "110", "130", "140"],
    ["Widget C", "150", "170", "190", "210"]
]

result = await save_table(
    table_data=table_data,
    filename="quarterly_sales",
    width=800,
    height=400
)
# Returns: "Table saved successfully as PNG! File ID: xyz-789, Filename: quarterly_sales.png"

# Usage by LLM - with list of dictionaries
table_data = [
    {"Name": "Alice", "Age": 30, "City": "New York"},
    {"Name": "Bob", "Age": 25, "City": "San Francisco"},
    {"Name": "Charlie", "Age": 35, "City": "Chicago"}
]

result = await save_table(
    table_data=table_data,
    filename="employee_list"
)
```

**Parameters:**
- `table_data` (list): Table data as list of lists or list of dictionaries
- `filename` (str): Name for the output PNG file (without extension)
- `width` (int, optional): Width of the table in pixels (default: 800)
- `height` (int, optional): Height of the table in pixels (default: 600)

**Supported Data Formats:**
- **List of lists**: First row is treated as headers
- **List of dictionaries**: Dictionary keys become headers

**Styling Features:**
- Professional table styling with borders
- Alternating row colors for readability
- Header row with distinct styling
- Automatic sizing and padding

**Returns:** Success message with file ID or error message

#### MermaidToImageTool

Convert Mermaid diagram syntax to PNG images.

```python
from agent_framework.tools import MermaidToImageTool

tool = MermaidToImageTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
save_diagram = tool.get_tool_function()

# Usage by LLM - flowchart
mermaid_code = '''
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process 1]
    B -->|No| D[Process 2]
    C --> E[End]
    D --> E
'''

result = await save_diagram(
    mermaid_code=mermaid_code,
    filename="workflow_diagram",
    width=1000,
    height=800,
    background_color="white"
)
# Returns: "Mermaid diagram saved successfully as PNG! File ID: xyz-789, Filename: workflow_diagram.png"

# Usage by LLM - sequence diagram
mermaid_code = '''
sequenceDiagram
    participant User
    participant API
    participant Database
    User->>API: Request data
    API->>Database: Query
    Database-->>API: Results
    API-->>User: Response
'''

result = await save_diagram(
    mermaid_code=mermaid_code,
    filename="sequence_diagram"
)
```

**Parameters:**
- `mermaid_code` (str): Mermaid diagram syntax
- `filename` (str): Name for the output PNG file (without extension)
- `width` (int, optional): Width of the diagram in pixels (default: 1200)
- `height` (int, optional): Height of the diagram in pixels (default: 800)
- `background_color` (str, optional): Background color for the diagram (default: "white")

**Supported Diagram Types:**
- Flowcharts (`graph TD`, `graph LR`)
- Sequence diagrams (`sequenceDiagram`)
- Class diagrams (`classDiagram`)
- State diagrams (`stateDiagram`)
- Entity relationship diagrams (`erDiagram`)
- Gantt charts (`gantt`)
- Pie charts (`pie`)
- Git graphs (`gitGraph`)

**Returns:** Success message with file ID or error message

### PDF Generation Tools

Tools for creating professional PDF documents from Markdown or HTML content.

**Note:** PDF tools require system dependencies. See [Dependency Management](#dependency-management) section.

#### CreatePDFFromMarkdownTool

Create PDF documents from Markdown content with multiple template styles.

```python
from agent_framework.tools import CreatePDFFromMarkdownTool

tool = CreatePDFFromMarkdownTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
create_pdf = tool.get_tool_function()

# Usage by LLM
result = await create_pdf(
    title="My Report",
    content="# Introduction\n\nThis is **bold** text...",
    template_style="professional",
    author="John Doe"
)
# Returns: "PDF created successfully! File ID: xyz-789, Filename: My_Report.pdf"
```

**Parameters:**
- `title` (str): Document title (used for filename and header)
- `content` (str): Markdown formatted content
- `author` (str, optional): Author name
- `template_style` (str): Template style - 'professional', 'minimal', or 'modern' (default: 'professional')

**Template Styles:**
- **professional**: Georgia serif font, blue accents, formal layout with headers/footers
- **minimal**: Helvetica sans-serif, black/white, clean minimalist design
- **modern**: System fonts, gradient accents, contemporary design

**Markdown Features Supported:**
- Headers (H1-H6)
- Bold, italic, code
- Code blocks with syntax highlighting
- Tables
- Lists (ordered and unordered)
- Blockquotes
- Links

**Returns:** Success message with file ID or error message

#### CreatePDFFromHTMLTool

Create PDF documents from HTML content with optional custom CSS.

```python
from agent_framework.tools import CreatePDFFromHTMLTool

tool = CreatePDFFromHTMLTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
create_pdf_html = tool.get_tool_function()

# Usage by LLM - with HTML fragment
result = await create_pdf_html(
    title="Custom Report",
    html_content="<h1>Hello</h1><p>This is a paragraph.</p>",
    custom_css="h1 { color: red; }",
    author="Jane Doe"
)

# Usage by LLM - with complete HTML document
result = await create_pdf_html(
    title="Full Document",
    html_content="<!DOCTYPE html><html><head>...</head><body>...</body></html>",
    custom_css="body { font-family: Arial; }"
)
```

**Parameters:**
- `title` (str): Document title
- `html_content` (str): Full HTML document or HTML fragment
- `custom_css` (str, optional): Additional CSS to apply
- `author` (str, optional): Author name

**HTML Handling:**
- **Complete Documents**: If HTML contains `<!DOCTYPE>` or `<html>`, it's used as-is with optional CSS injection
- **Fragments**: HTML fragments are wrapped in a complete document structure with base styling

**Returns:** Success message with file ID or error message

#### CreatePDFWithImagesTool

Create PDF documents from HTML with automatic image embedding from file storage.

This tool is particularly powerful when combined with ChartToImageTool - create charts, get their file IDs, then embed them in PDFs without passing large base64 strings through the LLM.

```python
from agent_framework.tools import CreatePDFWithImagesTool

tool = CreatePDFWithImagesTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
create_pdf_with_images = tool.get_tool_function()

# Usage by LLM - after creating a chart with ChartToImageTool
html_content = '''
<h1>Sales Report</h1>
<p>Here is the weekly sales chart:</p>
<img src="file_id:xyz-789" alt="Weekly Sales Chart">
<p>As shown in the chart, sales increased throughout the week.</p>
'''

result = await create_pdf_with_images(
    title="Sales Report",
    html_content=html_content,
    author="Sales Team"
)
# Returns: "PDF created successfully with 1 embedded image(s)! File ID: pdf-123, Filename: Sales_Report.pdf"
```

**Parameters:**
- `title` (str): Document title
- `html_content` (str): HTML content with special img tags using `file_id:` syntax
- `author` (str, optional): Author name

**Image Embedding Syntax:**
```html
<img src="file_id:YOUR_FILE_ID" alt="Description">
```

The tool automatically:
1. Detects all `file_id:` references in img tags
2. Retrieves the files from storage
3. Converts them to base64 data URIs
4. Embeds them directly in the PDF

**Workflow Example:**
```python
# Step 1: Create a chart
chart_result = await save_chart(chart_config, "sales_chart")
# Returns: "Chart saved successfully as PNG! File ID: abc-123, ..."

# Step 2: Extract file_id from result (LLM does this)
file_id = "abc-123"

# Step 3: Create HTML with file_id reference
html = f'<h1>Report</h1><img src="file_id:{file_id}" alt="Chart">'

# Step 4: Create PDF with embedded image
pdf_result = await create_pdf_with_images("Report", html)
# PDF now contains the embedded chart image!
```

**Returns:** Success message with file ID and number of embedded images

### File Access Tools

Tools for retrieving file paths and data URIs from file storage.

These tools help bridge the gap between file storage and other tools that need to access stored files.

#### GetFilePathTool

Get an accessible path or data URI for a stored file.

```python
from agent_framework.tools import GetFilePathTool

tool = GetFilePathTool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
get_path = tool.get_tool_function()

# Usage by LLM
result = await get_path("abc-123")
# For local storage: "file:///absolute/path/to/file.png"
# For S3/MinIO: "data:image/png;base64,iVBORw0KGgoAAAANS..."
```

**Parameters:**
- `file_id` (str): The file ID returned from file storage operations

**Returns:**
- For local storage: Absolute file path with `file://` protocol
- For S3/MinIO: Base64 data URI

**Use Cases:**
- Referencing files in HTML/PDF generation
- Getting paths for external tools
- Creating portable references to stored files

#### GetFileAsDataURITool

Convert any stored file to a base64 data URI.

```python
from agent_framework.tools import GetFileAsDataURITool

tool = GetFileAsDataURITool()
tool.set_context(file_storage=storage, user_id="user123", session_id="session456")
get_data_uri = tool.get_tool_function()

# Usage by LLM
result = await get_data_uri("abc-123")
# Returns: "data:image/png;base64,iVBORw0KGgoAAAANS..."
```

**Parameters:**
- `file_id` (str): The file ID returned from file storage operations

**Returns:** Base64 data URI string (always, regardless of storage backend)

**Use Cases:**
- Embedding files directly in HTML/PDF
- Creating portable file references
- Sharing files across different contexts

---

## Using Reusable Tools in Your Agent

Here's a complete example of using reusable tools in a LlamaIndex agent:

```python
from agent_framework.implementations import LlamaIndexAgent
from agent_framework.storage.file_system_management import FileStorageFactory
from agent_framework.tools import (
    CreateFileTool,
    ListFilesTool,
    ReadFileTool,
    CreatePDFFromMarkdownTool,
    ChartToImageTool,
    CreatePDFWithImagesTool,
)

class MyAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.agent_id = "my_agent_v1"
        self.file_storage = None
        self.current_user_id = "default_user"
        self.current_session_id = None
        
        # Initialize reusable tools
        self.tools = [
            CreateFileTool(),
            ListFilesTool(),
            ReadFileTool(),
            CreatePDFFromMarkdownTool(),
            ChartToImageTool(),
            CreatePDFWithImagesTool(),
        ]
    
    async def configure_session(self, session_configuration):
        """Inject dependencies into tools during session configuration."""
        # Capture session context
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
        
        # Initialize file storage
        if self.file_storage is None:
            self.file_storage = await FileStorageFactory.create_storage_manager()
        
        # Inject context into all tools
        for tool in self.tools:
            tool.set_context(
                file_storage=self.file_storage,
                user_id=self.current_user_id,
                session_id=self.current_session_id
            )
        
        await super().configure_session(session_configuration)
    
    def get_agent_tools(self):
        """Return tool functions for the agent."""
        return [tool.get_tool_function() for tool in self.tools]
    
    def get_agent_prompt(self):
        return "You are a helpful assistant with file and PDF capabilities."
```

### Key Steps

1. **Import Tools**: Import the tool classes you need from `agent_framework.tools`
2. **Initialize Tools**: Create tool instances in `__init__()` and store them in a list
3. **Inject Context**: In `configure_session()`, call `set_context()` on each tool with file storage and session info
4. **Return Functions**: In `get_agent_tools()`, return the callable functions via `get_tool_function()`

### Benefits

- **Clean Code**: No inline tool definitions cluttering your agent
- **Reusability**: Same tools work across different agents
- **Testability**: Tools can be tested independently
- **Maintainability**: Tool implementations are centralized
- **Extensibility**: Easy to add new tools by appending to the list

---

## Creating Custom Tools

You can create your own reusable tools by inheriting from `AgentTool`.

### Basic Custom Tool

```python
from agent_framework.tools import AgentTool, ToolDependencyError
from typing import Callable

class MyCustomTool(AgentTool):
    """Tool for doing something custom."""
    
    def get_tool_function(self) -> Callable:
        """Return the custom tool function."""
        
        async def my_custom_function(param1: str, param2: int) -> str:
            """
            Do something custom with the parameters.
            
            Args:
                param1: Description of first parameter
                param2: Description of second parameter
            
            Returns:
                Success message or error
            """
            # Ensure tool was initialized
            self._ensure_initialized()
            
            # Validate inputs
            if not param1:
                return "Error: param1 cannot be empty"
            
            # Check if file storage is needed
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is required but not available"
                )
            
            try:
                # Your custom logic here
                result = f"Processed {param1} with {param2}"
                
                # Use file storage if needed
                file_id = await self.file_storage.store_file(
                    content=result.encode('utf-8'),
                    filename=f"{param1}.txt",
                    user_id=self.current_user_id,
                    session_id=self.current_session_id
                )
                
                return f"Success! File ID: {file_id}"
                
            except Exception as e:
                return f"Error: {str(e)}"
        
        return my_custom_function
```

### Custom Tool Without File Storage

If your tool doesn't need file storage, you can override `get_tool_info()`:

```python
class SimpleTool(AgentTool):
    """A simple tool that doesn't need file storage."""
    
    def get_tool_function(self) -> Callable:
        async def simple_function(text: str) -> str:
            """Process text without file storage."""
            # No need to call _ensure_initialized() if you don't use dependencies
            return text.upper()
        
        return simple_function
    
    def get_tool_info(self):
        """Override to indicate no file storage needed."""
        info = super().get_tool_info()
        info['requires_file_storage'] = False
        return info
```

### Custom Tool with External APIs

```python
import aiohttp
from agent_framework.tools import AgentTool

class WeatherTool(AgentTool):
    """Tool for fetching weather information."""
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    
    def get_tool_function(self) -> Callable:
        async def get_weather(city: str) -> str:
            """
            Get current weather for a city.
            
            Args:
                city: City name
            
            Returns:
                Weather information or error
            """
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"https://api.weather.com/v1/current?city={city}&key={self.api_key}"
                    async with session.get(url) as response:
                        data = await response.json()
                        return f"Weather in {city}: {data['temp']}°F, {data['conditions']}"
            except Exception as e:
                return f"Error fetching weather: {str(e)}"
        
        return get_weather
    
    def get_tool_info(self):
        info = super().get_tool_info()
        info['requires_file_storage'] = False
        info['requires_user_context'] = False
        return info
```

### Tool Best Practices for Custom Tools

1. **Clear Docstrings**: Write detailed docstrings for the LLM to understand
2. **Type Hints**: Use type hints for all parameters and return values
3. **Error Handling**: Catch exceptions and return user-friendly error messages
4. **Validation**: Validate inputs before processing
5. **Logging**: Use logging for debugging and monitoring
6. **Async**: Use `async def` for I/O operations

---

## Adding Tools to LlamaIndex Agents

For a complete guide on creating LlamaIndex agents, see [CREATING_AGENTS.md](CREATING_AGENTS.md).

### Basic Tool Integration

Tools for LlamaIndex agents are simple Python functions with docstrings:

```python
from agent_framework.implementations import LlamaIndexAgent

class MyAgent(LlamaIndexAgent):
    def get_agent_tools(self) -> List[callable]:
        """Define tools as regular Python functions."""
        
        def add(a: int, b: int) -> int:
            """Add two numbers together."""
            return a + b
        
        def get_weather(city: str) -> str:
            """Get the current weather for a city."""
            # Your implementation here
            return f"Weather in {city}: Sunny, 72°F"
        
        return [add, get_weather]
```

### Async Tools

LlamaIndex supports async tools natively:

```python
def get_agent_tools(self) -> List[callable]:
    async def fetch_data(url: str) -> str:
        """Fetch data from a URL."""
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    
    return [fetch_data]
```

### Tools with Session Context

Access session information in your tools:

```python
class MyAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.current_user_id = "default_user"
        self.current_session_id = None
    
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """Capture session context."""
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
        await super().configure_session(session_configuration)
    
    def get_agent_tools(self) -> List[callable]:
        def get_user_info() -> str:
            """Get information about the current user."""
            return f"User: {self.current_user_id}, Session: {self.current_session_id}"
        
        return [get_user_info]
```

### Tools with External Dependencies

Tools can use any Python library:

```python
def get_agent_tools(self) -> List[callable]:
    def analyze_sentiment(text: str) -> str:
        """Analyze the sentiment of text."""
        from textblob import TextBlob
        blob = TextBlob(text)
        return f"Sentiment: {blob.sentiment.polarity}"
    
    def search_web(query: str) -> str:
        """Search the web for information."""
        import requests
        response = requests.get(f"https://api.example.com/search?q={query}")
        return response.json()
    
    return [analyze_sentiment, search_web]
```

---

## Adding Tools to BaseAgent (Custom Framework)

For a complete guide on creating BaseAgent implementations, see [CREATING_AGENTS.md](CREATING_AGENTS.md).
For a working example, see [examples/custom_framework_agent.py](../examples/custom_framework_agent.py).

### Basic Tool Integration

For BaseAgent, you define tools the same way, but you're responsible for tool execution:

```python
from agent_framework.core.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def get_agent_tools(self) -> List[callable]:
        """Define tools as regular Python functions."""
        
        def calculate(expression: str) -> float:
            """Evaluate a mathematical expression."""
            return eval(expression)  # Use safely in production!
        
        return [calculate]
    
    async def run_agent(self, query: str, ctx: Any, stream: bool = False):
        """You handle tool calling in your framework."""
        # Your framework's logic for:
        # 1. Detecting tool calls
        # 2. Executing tools
        # 3. Passing results back to LLM
        pass
```

### Tool Execution Pattern

Here's a complete example of tool execution in BaseAgent:

```python
async def run_agent(self, query: str, ctx: Any, stream: bool = False):
    """Execute agent with tool support."""
    # Build messages
    messages = [
        {"role": "system", "content": self._system_prompt},
        {"role": "user", "content": query}
    ]
    
    # Tool execution loop
    max_iterations = 5
    for iteration in range(max_iterations):
        # Call LLM with tool schemas
        response = await self._llm_client.create(
            messages=messages,
            tools=self._get_tool_schemas()
        )
        
        message = response.choices[0].message
        
        # Check for tool calls
        if hasattr(message, 'tool_calls') and message.tool_calls:
            # Execute each tool
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                # Execute tool
                if tool_name in self._tools:
                    result = self._tools[tool_name](**tool_args)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "assistant",
                        "tool_calls": [tool_call]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            continue
        
        # No tool calls, return response
        return message.content
    
    return "Max iterations reached"
```

---

## Adding MCP Servers to LlamaIndex Agents

### What is MCP?

MCP (Model Context Protocol) allows agents to connect to external tool servers. This enables:
- File system operations
- Database access
- API integrations
- Custom tool servers

### Basic MCP Integration

```python
from agent_framework.implementations import LlamaIndexAgent

class MyMCPAgent(LlamaIndexAgent):
    def __init__(self):
        super().__init__()
        self.mcp_tools = []
        self._mcp_initialized = False
    
    async def _initialize_mcp_tools(self):
        """Initialize MCP tools from configured servers."""
        if self._mcp_initialized:
            return
        
        try:
            from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
        except ImportError:
            print("Install: uv add llama-index-tools-mcp")
            return
        
        # Connect to MCP server
        client = BasicMCPClient(
            command="uvx",
            args=["@modelcontextprotocol/server-filesystem", "/path/to/workspace"],
            env={}
        )
        
        # Load tools from server
        mcp_tool_spec = McpToolSpec(client=client)
        function_tools = await mcp_tool_spec.to_tool_list_async()
        
        self.mcp_tools.extend(function_tools)
        self._mcp_initialized = True
    
    def get_agent_tools(self) -> List[callable]:
        """Combine built-in tools with MCP tools."""
        def greet(name: str) -> str:
            """Greet a user."""
            return f"Hello, {name}!"
        
        # Combine built-in and MCP tools
        all_tools = [greet]
        if self.mcp_tools:
            all_tools.extend(self.mcp_tools)
        
        return all_tools
    
    async def initialize_agent(self, model_name: str, system_prompt: str, tools: List[callable], **kwargs):
        """Initialize MCP tools BEFORE creating agent."""
        # Load MCP tools first
        await self._initialize_mcp_tools()
        
        # Get all tools including MCP
        all_tools = self.get_agent_tools()
        
        # Call parent with all tools
        await super().initialize_agent(model_name, system_prompt, all_tools, **kwargs)
```

### Multiple MCP Servers

You can connect to multiple MCP servers:

```python
async def _initialize_mcp_tools(self):
    """Initialize tools from multiple MCP servers."""
    from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
    
    # Filesystem server
    fs_client = BasicMCPClient(
        command="uvx",
        args=["@modelcontextprotocol/server-filesystem", "/workspace"]
    )
    fs_tools = await McpToolSpec(client=fs_client).to_tool_list_async()
    self.mcp_tools.extend(fs_tools)
    
    # GitHub server
    gh_client = BasicMCPClient(
        command="uvx",
        args=["@modelcontextprotocol/server-github"],
        env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
    )
    gh_tools = await McpToolSpec(client=gh_client).to_tool_list_async()
    self.mcp_tools.extend(gh_tools)
    
    # Database server
    db_client = BasicMCPClient(
        command="uvx",
        args=["@modelcontextprotocol/server-postgres"],
        env={"DATABASE_URL": os.getenv("DATABASE_URL")}
    )
    db_tools = await McpToolSpec(client=db_client).to_tool_list_async()
    self.mcp_tools.extend(db_tools)
```

### MCP Server Configuration

Common MCP servers and their configurations:

```python
# Filesystem access
{
    "command": "uvx",
    "args": ["@modelcontextprotocol/server-filesystem", "/path/to/workspace"],
    "env": {}
}

# GitHub integration
{
    "command": "uvx",
    "args": ["@modelcontextprotocol/server-github"],
    "env": {"GITHUB_TOKEN": "your-token"}
}

# PostgreSQL database
{
    "command": "uvx",
    "args": ["@modelcontextprotocol/server-postgres"],
    "env": {"DATABASE_URL": "postgresql://..."}
}

# Web fetch/scraping
{
    "command": "uvx",
    "args": ["@modelcontextprotocol/server-fetch"]
}

# Custom Python MCP server
{
    "command": "uv",
    "args": ["run", "python", "-m", "my_mcp_server"],
    "env": {"API_KEY": "your-key"}
}
```

---

## Adding MCP Servers to BaseAgent

### Basic MCP Integration

For BaseAgent, you need to handle MCP tool loading and execution manually:

```python
from agent_framework.core.base_agent import BaseAgent

class MyCustomMCPAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.mcp_tools = []
        self._mcp_clients = {}
    
    async def _initialize_mcp_tools(self):
        """Initialize MCP tools."""
        try:
            from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
        except ImportError:
            print("Install: uv add llama-index-tools-mcp")
            return
        
        # Connect to MCP server
        client = BasicMCPClient(
            command="uvx",
            args=["@modelcontextprotocol/server-filesystem", "/workspace"]
        )
        self._mcp_clients["filesystem"] = client
        
        # Load tools
        mcp_tool_spec = McpToolSpec(client=client)
        function_tools = await mcp_tool_spec.to_tool_list_async()
        self.mcp_tools.extend(function_tools)
    
    def get_agent_tools(self) -> List[callable]:
        """Return all tools including MCP."""
        built_in_tools = [...]  # Your built-in tools
        return built_in_tools + self.mcp_tools
    
    async def initialize_agent(self, model_name: str, system_prompt: str, tools: List[callable], **kwargs):
        """Initialize agent with MCP tools."""
        # Load MCP tools first
        await self._initialize_mcp_tools()
        
        # Get all tools
        all_tools = self.get_agent_tools()
        
        # Initialize your framework with all tools
        # ... your framework initialization ...
```

### MCP Tool Execution

When executing tools in BaseAgent, MCP tools work like regular tools:

```python
async def run_agent(self, query: str, ctx: Any, stream: bool = False):
    """Execute agent with MCP tool support."""
    # MCP tools are already in self._tools
    # They're executed the same way as built-in tools
    
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        
        # Execute tool (works for both built-in and MCP tools)
        if tool_name in self._tools:
            result = await self._tools[tool_name](**tool_args)
            # ... handle result ...
```

---

## Tool Best Practices

### 1. Clear Docstrings

Tools need good docstrings for the LLM to understand them:

```python
def search_database(query: str, limit: int = 10) -> List[Dict]:
    """
    Search the database for records matching the query.
    
    Args:
        query: The search query string
        limit: Maximum number of results to return (default: 10)
    
    Returns:
        List of matching records as dictionaries
    
    Example:
        search_database("active users", limit=5)
    """
    # Implementation
```

### 2. Type Hints

Use type hints for better tool calling:

```python
def calculate_discount(price: float, discount_percent: int) -> float:
    """Calculate discounted price."""
    return price * (1 - discount_percent / 100)
```

### 3. Error Handling

Handle errors gracefully in tools:

```python
def divide(a: float, b: float) -> Union[float, str]:
    """Divide two numbers."""
    try:
        if b == 0:
            return "Error: Cannot divide by zero"
        return a / b
    except Exception as e:
        return f"Error: {str(e)}"
```

### 4. Async Tools

Use async for I/O operations:

```python
async def fetch_api_data(endpoint: str) -> Dict:
    """Fetch data from API endpoint."""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/{endpoint}") as response:
            return await response.json()
```

### 5. Tool Organization

For many tools, organize them in separate modules:

```python
# tools/database.py
def search_users(query: str) -> List[Dict]:
    """Search users in database."""
    pass

def create_user(name: str, email: str) -> Dict:
    """Create a new user."""
    pass

# tools/api.py
async def fetch_weather(city: str) -> Dict:
    """Fetch weather data."""
    pass

# agent.py
from tools import database, api

class MyAgent(LlamaIndexAgent):
    def get_agent_tools(self) -> List[callable]:
        return [
            database.search_users,
            database.create_user,
            api.fetch_weather,
        ]
```

### 6. Tool Testing

Test tools independently:

```python
# tests/test_tools.py
import pytest
from agent import MyAgent

def test_add_tool():
    agent = MyAgent()
    tools = agent.get_agent_tools()
    add_tool = next(t for t in tools if t.__name__ == "add")
    
    assert add_tool(2, 3) == 5
    assert add_tool(-1, 1) == 0

@pytest.mark.asyncio
async def test_async_tool():
    agent = MyAgent()
    tools = agent.get_agent_tools()
    fetch_tool = next(t for t in tools if t.__name__ == "fetch_data")
    
    result = await fetch_tool("https://api.example.com/data")
    assert isinstance(result, dict)
```

---

## Complete Examples

### LlamaIndex Agent with Tools and MCP

See [examples/agent_with_mcp.py](../examples/agent_with_mcp.py) for a complete working example.

For more LlamaIndex examples:
- [examples/simple_agent.py](../examples/simple_agent.py) - Basic agent with tools
- [examples/agent_with_file_storage.py](../examples/agent_with_file_storage.py) - Agent with file handling

### BaseAgent with Tools

See [examples/custom_framework_agent.py](../examples/custom_framework_agent.py) for a complete working example.

For detailed guidance on BaseAgent, see [CREATING_AGENTS.md](CREATING_AGENTS.md).

### Simple Agent with Tools

See [examples/simple_agent.py](../examples/simple_agent.py) for a minimal example.

---

## Dependency Management

### Core Dependencies

The Agent Framework core and file tools have minimal dependencies:

```bash
# Install base framework
uv add agent-framework-lib

# Or with LlamaIndex support
uv add agent-framework-lib[llamaindex]
```

**Core dependencies** (always installed):
- `aiofiles` - Async file operations
- `pydantic` - Data validation

### Chart Generation Dependencies

Chart generation tools require Playwright for browser automation.

#### Python Packages

```bash
# Install Playwright
uv add playwright

# Install browser binaries (Chromium)
playwright install chromium
```

**Note:** The `playwright install` command downloads browser binaries (~100MB for Chromium). This is a one-time setup.

#### Checking Chart Tool Availability

```python
from agent_framework.tools import ChartToImageTool

try:
    tool = ChartToImageTool()
    print("Chart tools are ready!")
except ImportError as e:
    print(f"Chart tools not available: {e}")
```

### PDF Generation Dependencies

PDF generation tools require additional Python packages and system libraries.

#### Python Packages

```bash
# Install PDF generation support
uv add weasyprint>=60.0 markdown>=3.5
```

#### System Dependencies

WeasyPrint requires system libraries for rendering. These must be installed separately:

**macOS:**
```bash
# Install with Homebrew
brew install pango gdk-pixbuf libffi

# Set library path (add to ~/.zshrc or ~/.bash_profile)
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install pango gdk-pixbuf2 libffi-devel
```

**Windows:**
```bash
# Install GTK3 runtime from https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
# Then install Python packages
uv add weasyprint markdown
```

#### Checking PDF Tool Availability

The framework will warn you if PDF tools are not available:

```python
from agent_framework.tools import PDF_TOOLS_AVAILABLE

if PDF_TOOLS_AVAILABLE:
    print("PDF tools are ready!")
else:
    print("PDF tools are not available - check dependencies")
```

You can also check at import time:

```python
try:
    from agent_framework.tools import CreatePDFFromMarkdownTool
    print("PDF tools imported successfully")
except ImportError as e:
    print(f"PDF tools not available: {e}")
```

### Optional Dependencies

Other optional dependencies for specific features:

```bash
# MongoDB session storage
uv add agent-framework-lib[mongodb]

# AWS S3 file storage
uv add agent-framework-lib[s3]

# MinIO file storage
uv add agent-framework-lib[minio]

# Multimodal processing
uv add agent-framework-lib[multimodal]

# All optional dependencies
uv add agent-framework-lib[all]
```

### Verifying Installation

Create a simple script to verify your installation:

```python
import asyncio
from agent_framework.tools import (
    CreateFileTool,
    ListFilesTool,
    ReadFileTool,
    PDF_TOOLS_AVAILABLE,
)

async def verify_tools():
    print("✓ File tools imported successfully")
    
    if PDF_TOOLS_AVAILABLE:
        from agent_framework.tools import CreatePDFFromMarkdownTool, CreatePDFFromHTMLTool
        print("✓ PDF tools available")
    else:
        print("✗ PDF tools not available - install system dependencies")
    
    # Test tool instantiation
    file_tool = CreateFileTool()
    print("✓ Tools can be instantiated")
    
    print("\nAll checks passed!")

if __name__ == "__main__":
    asyncio.run(verify_tools())
```

---

## Troubleshooting

### PDF Tools Not Available

**Symptom:** Import warning about PDF tools not being available

**Cause:** System dependencies (pango, gdk-pixbuf, libffi) are not installed

**Solution:**

1. Install system dependencies for your platform (see [Dependency Management](#dependency-management))
2. On macOS, ensure `DYLD_LIBRARY_PATH` is set:
   ```bash
   export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
   ```
3. Restart your Python environment after installing dependencies
4. Verify installation:
   ```python
   from agent_framework.tools import PDF_TOOLS_AVAILABLE
   print(PDF_TOOLS_AVAILABLE)  # Should be True
   ```

### ToolDependencyError: Tool Not Initialized

**Symptom:** `ToolDependencyError: MyTool has not been initialized. Call set_context() before using this tool.`

**Cause:** Tool was used without calling `set_context()` first

**Solution:**

Ensure you call `set_context()` in your agent's `configure_session()` method:

```python
async def configure_session(self, session_configuration):
    # Initialize file storage
    self.file_storage = await FileStorageFactory.create_storage_manager()
    
    # Inject context into tools
    for tool in self.tools:
        tool.set_context(
            file_storage=self.file_storage,
            user_id=self.current_user_id,
            session_id=self.current_session_id
        )
    
    await super().configure_session(session_configuration)
```

### ToolDependencyError: File Storage Not Available

**Symptom:** `ToolDependencyError: File storage is required but was not provided`

**Cause:** Tool requires file storage but `file_storage` was not set in `set_context()`

**Solution:**

1. Initialize file storage before setting context:
   ```python
   from agent_framework.storage.file_system_management import FileStorageFactory
   
   self.file_storage = await FileStorageFactory.create_storage_manager()
   ```

2. Pass file storage to `set_context()`:
   ```python
   tool.set_context(
       file_storage=self.file_storage,  # Don't forget this!
       user_id=self.current_user_id,
       session_id=self.current_session_id
   )
   ```

### PDF Creation Fails with "libgobject" Error

**Symptom:** Error message contains "libgobject-2.0.so.0: cannot open shared object file"

**Cause:** System libraries are installed but not in the library path

**Solution:**

**macOS:**
```bash
# Add to ~/.zshrc or ~/.bash_profile
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"

# Reload shell configuration
source ~/.zshrc  # or source ~/.bash_profile
```

**Linux:**
```bash
# Add to ~/.bashrc
export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"

# Reload shell configuration
source ~/.bashrc
```

### PDF Creation Returns "Error: Title cannot be empty"

**Symptom:** PDF creation fails with validation error

**Cause:** Empty or whitespace-only title/content was provided

**Solution:**

Ensure title and content are non-empty:
```python
result = await create_pdf_from_markdown(
    title="My Report",  # Must be non-empty
    content="# Content\n\nSome text...",  # Must be non-empty
    template_style="professional"
)
```

### PDF Template Style Not Recognized

**Symptom:** Error message "Invalid template style 'custom'"

**Cause:** Invalid template style name was provided

**Solution:**

Use one of the three supported template styles:
- `"professional"` - Georgia serif, blue accents
- `"minimal"` - Helvetica, black/white
- `"modern"` - System fonts, gradients

```python
result = await create_pdf_from_markdown(
    title="My Report",
    content="# Content",
    template_style="professional"  # Must be one of the three
)
```

### Tools Not Being Called

1. Check docstrings are clear and descriptive
2. Verify type hints are correct
3. Ensure tools are returned from `get_agent_tools()`
4. Check LLM model supports function calling (gpt-4, gpt-3.5-turbo, claude-3, etc.)

### MCP Tools Not Loading

1. Install MCP package: `uv add llama-index-tools-mcp`
2. Verify MCP server is installed: `uvx install @modelcontextprotocol/server-filesystem`
3. Check server command and args are correct
4. Ensure `_initialize_mcp_tools()` is called before agent initialization

### Async Tool Errors

1. Use `async def` for async tools
2. Use `await` when calling async tools
3. LlamaIndex handles async tools automatically
4. BaseAgent requires manual async handling

---

## Complete Example: Agent with Reusable Tools

Here's a complete, working example demonstrating the reusable tools architecture:

```python
"""
Complete example of an agent using reusable tools.

This example demonstrates:
- Importing and initializing reusable tools
- Injecting dependencies via set_context()
- Using file storage and PDF generation tools
- Proper error handling and session management
"""

import asyncio
import os
from typing import List, Any, Dict

from agent_framework.implementations import LlamaIndexAgent
from agent_framework.storage.file_system_management import FileStorageFactory
from agent_framework.tools import (
    CreateFileTool,
    ListFilesTool,
    ReadFileTool,
    CreatePDFFromMarkdownTool,
    CreatePDFFromHTMLTool,
    PDF_TOOLS_AVAILABLE,
)


class DocumentAgent(LlamaIndexAgent):
    """
    An agent with comprehensive file and PDF capabilities.
    
    This agent demonstrates the reusable tools architecture where tools
    are instantiated as classes and have their dependencies injected
    via set_context(). This makes tools reusable across agents and
    easier to test.
    """
    
    def __init__(self):
        super().__init__()
        self.agent_id = "document_agent_v1"
        self.file_storage = None
        self.current_user_id = "default_user"
        self.current_session_id = None
        
        # Initialize reusable tools
        self.tools = [
            CreateFileTool(),
            ListFilesTool(),
            ReadFileTool(),
        ]
        
        # Add PDF tools if available
        if PDF_TOOLS_AVAILABLE:
            self.tools.extend([
                CreatePDFFromMarkdownTool(),
                CreatePDFFromHTMLTool(),
            ])
            print("✓ PDF generation tools loaded")
        else:
            print("⚠ PDF tools not available - install system dependencies")
    
    async def _ensure_file_storage(self):
        """Ensure file storage is initialized."""
        if self.file_storage is None:
            self.file_storage = await FileStorageFactory.create_storage_manager()
    
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """
        Configure session and inject dependencies into tools.
        
        This is the key method where dependency injection happens.
        Each tool receives the file_storage, user_id, and session_id
        it needs to operate.
        """
        # Capture session context
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
        
        # Initialize file storage
        await self._ensure_file_storage()
        
        # Inject context into all tools
        for tool in self.tools:
            tool.set_context(
                file_storage=self.file_storage,
                user_id=self.current_user_id,
                session_id=self.current_session_id
            )
        
        # Call parent to continue configuration
        await super().configure_session(session_configuration)
    
    def get_agent_prompt(self) -> str:
        """Define the agent's system prompt."""
        base_prompt = """You are a helpful document assistant with file management capabilities.

You can:
- Create, list, and read text files
- Manage files for users across sessions"""
        
        if PDF_TOOLS_AVAILABLE:
            base_prompt += """
- Generate professional PDF documents from Markdown content
- Create PDFs from HTML with custom styling
- Choose from multiple PDF templates: 'professional', 'minimal', or 'modern'"""
        
        base_prompt += """

Use the provided tools to help users manage their documents and create beautiful PDFs."""
        
        return base_prompt
    
    def get_agent_tools(self) -> List[callable]:
        """
        Return tool functions for the agent.
        
        This method demonstrates how to get callable functions from
        tool instances. The tools already have their context injected
        in configure_session().
        """
        return [tool.get_tool_function() for tool in self.tools]
    
    async def initialize_agent(
        self,
        model_name: str,
        system_prompt: str,
        tools: List[callable],
        **kwargs
    ) -> None:
        """Initialize the agent with tools."""
        await self._ensure_file_storage()
        await super().initialize_agent(model_name, system_prompt, tools, **kwargs)
    
    def create_fresh_context(self) -> Any:
        """Create a fresh LlamaIndex Context."""
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


async def main():
    """Run the agent interactively."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        return
    
    # Create agent
    agent = DocumentAgent()
    
    # Configure session
    await agent.configure_session({
        'user_id': 'demo_user',
        'session_id': 'demo_session'
    })
    
    # Initialize agent
    model_name = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    await agent.initialize_agent(
        model_name=model_name,
        system_prompt=agent.get_agent_prompt(),
        tools=agent.get_agent_tools()
    )
    
    print("=" * 60)
    print("Document Agent Ready!")
    print("=" * 60)
    print("\nTry asking:")
    print("  - Create a file called 'notes.txt' with some content")
    print("  - List all my files")
    print("  - Read the file with ID <file_id>")
    if PDF_TOOLS_AVAILABLE:
        print("  - Create a PDF from markdown with title 'My Report'")
        print("  - Create a PDF from HTML with custom styling")
    print("\nType 'quit' to exit\n")
    
    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            # Create input
            agent_input = agent.create_agent_input(
                query=user_input,
                user_id='demo_user',
                session_id='demo_session'
            )
            
            # Run agent
            response = await agent.run(agent_input)
            print(f"\nAgent: {response.response}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nError: {e}\n")
    
    print("\nGoodbye!")


if __name__ == "__main__":
    asyncio.run(main())
```

### Running the Example

1. **Install dependencies:**
   ```bash
   uv add agent-framework-lib[llamaindex]
   uv add weasyprint markdown  # For PDF support
   ```

2. **Install system dependencies** (for PDF support):
   ```bash
   # macOS
   brew install pango gdk-pixbuf libffi
   export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
   
   # Ubuntu/Debian
   sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev
   ```

3. **Set API key:**
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```

4. **Run the agent:**
   ```bash
   python document_agent.py
   ```

### Example Interactions

**Creating a file:**
```
You: Create a file called 'meeting_notes.txt' with the content 'Discussed Q4 goals'

Agent: File 'meeting_notes.txt' created successfully with ID: abc-123-def-456
```

**Listing files:**
```
You: List all my files

Agent: Files:
1. meeting_notes.txt (ID: abc-123-def-456, Size: 23 B)
2. report.pdf (ID: xyz-789-ghi-012, Size: 45.2 KB)
```

**Creating a PDF:**
```
You: Create a professional PDF titled 'Q4 Report' with markdown content including a header and bullet points

Agent: PDF created successfully! File ID: pdf-123-456, Filename: Q4_Report.pdf
```

---

## Additional Resources

- [LlamaIndex Tools Documentation](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Server List](https://github.com/modelcontextprotocol/servers)
- [Agent Framework Examples](../examples/)
- [WeasyPrint Documentation](https://doc.courtbouillon.org/weasyprint/)
- [Python Markdown Documentation](https://python-markdown.github.io/)
