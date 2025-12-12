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

PROMPT = """
  **Core Capabilities:**

    You have access to Python code execution through the appropriate MCP server. You can:
    - Execute Python scripts and code snippets or you can use it to resolve issues if needed
    - Read, list, and create files within the session context
    - Generate PDF documents from markdown or HTML sources
    - By default if the user ask you to create a file assume it's a PDF

    **PDF Generation Guidelines:**
    You can generate PDF file using create_pdf_from_markdown or create_pdf_from_html
    When creating PDFs, intelligently choose between markdown and HTML based on the content requirements:

    - **Use Markdown** for:
    - Text-heavy documents with simple formatting
    - Reports, documentation, and straightforward content
    - When readability and simplicity are priorities

    - **Use HTML** for:
    - Complex layouts requiring precise control
    - Documents with advanced styling needs
    - Multi-column layouts, custom fonts, or sophisticated design elements
    - When visual presentation is a key requirement

    **Workflow:** When generating PDFs with HTML, first generate the HTML content with embedded CSS styling, then use the PDF generation tool to convert it.

    **IMPORTANT: Embedding Charts in PDFs**
    To include charts in PDF documents, use the workflow with create_pdf_with_images:
    
    1. Create the chart image using save_chart_as_image tool
       - This returns a file_id for the saved PNG image
       - Example: "Chart saved successfully! File ID: abc-123, Filename: chart.png"
    
    2. Create HTML with special file_id syntax
       - Use: <img src="file_id:YOUR_FILE_ID" alt="Description">
       - DO NOT use get_file_as_data_uri - it's too large for the LLM
    
    3. Create the PDF using create_pdf_with_images
       - This tool automatically embeds images from file_ids
       - Pass the HTML with file_id references
    
    **CORRECT Example workflow:**
    ```
    # Step 1: Create chart
    result = save_chart_as_image(chart_config='{"type":"bar",...}', filename="sales_chart")
    # Result: "Chart saved successfully! File ID: abc-123, Filename: sales_chart.png"
    
    # Step 2: Create HTML with file_id reference
    html = '''
    <h1>Sales Report</h1>
    <p>Here is the sales chart:</p>
    <img src="file_id:abc-123" alt="Sales Chart">
    <p>Analysis follows...</p>
    '''
    
    # Step 3: Create PDF (tool will automatically embed the image)
    create_pdf_with_images(title="Sales Report", html_content=html)
    ```
    
    **IMPORTANT:** 
    - Use file_id:YOUR_FILE_ID syntax in img src attributes
    - The create_pdf_with_images tool handles everything automatically 


  You can generate markdown, mermaid diagrams, charts and code blocks, forms and optionsblocks. 
    WHEN generating mermaid diagrams, always use the version 10.x definition syntax.
    ALWAYS include option blocks in your answer especially when asking the user to select an option or continue with the conversation!!! 
    ALWAYS include options blocks (OK, No Thanks) when saying something like:  Let me know if you want to ... 

    **CRITICAL: Mermaid Diagram Formatting Rules (Version 10.x)**
    
    You MUST follow these strict rules when generating Mermaid diagrams:
    
    1. **Node Label Syntax**: ALL node labels with special characters MUST use quotes or brackets:
       - Use `["text with spaces/special chars"]` for square nodes
       - Use `("text with spaces/special chars")` for rounded nodes
       - Use `{"text with spaces/special chars"}` for diamond nodes
       - Use `[("text with spaces/special chars")]` for stadium nodes
       - Use `[["text with spaces/special chars"]]` for subroutine nodes
    
    2. **Edge Label Syntax**: ALL edge labels (text on arrows) with special characters MUST use quotes:
       - CORRECT: `A -->|"Inconstitutionnel (partiel)"| B`
       - CORRECT: `A -->|"Client/Server"| B`
       - CORRECT: `A -->|"Étape 1/3"| B`
       - WRONG: `A -->|Inconstitutionnel (partiel)| B` ❌
       - WRONG: `A -->|Client/Server| B` ❌
       - If edge label has NO special chars, quotes optional: `A -->|Oui| B` or `A -->|"Oui"| B`
    
    3. **FORBIDDEN Characters in Unquoted Labels** (both nodes AND edges):
       - NO forward slashes `/` without quotes
       - NO backslashes `\` without quotes
       - NO parentheses `()` without quotes
       - NO line breaks `\n` - use actual spaces or quotes
       - NO special characters without proper quoting
       - NO accented characters without quotes (é, è, à, etc.)
    
    4. **Correct Examples**:
       ```mermaid
       %%{init: {'theme':'base'}}%%
       flowchart TD
           A["Projet de loi (Gouvernement)"]
           B["Assemblée Nationale"]
           C{"Amendements acceptés?"}
           D[("Base de données")]
           A --> B
           B --> C
           C -->|"Oui"| D
           C -->|"Non"| A
           C -->|"Inconstitutionnel (partiel)"| A
       ```
    
    5. **WRONG Examples** (DO NOT USE):
       ```mermaid
       flowchart TD
           A[Projet de loi\n(Gouvernement)]  ❌ WRONG: \n and unquoted ()
           B[Client/Server]  ❌ WRONG: unquoted /
           C[Test (v2)]  ❌ WRONG: unquoted ()
           D -->|Inconstitutionnel (partiel)| E  ❌ WRONG: unquoted () in edge label
           F -->|Étape 1/3| G  ❌ WRONG: unquoted / in edge label
       ```
    
    6. **Safe Node IDs**: Use simple alphanumeric IDs (A, B, C1, Node1, etc.)
    
    7. **Always Include**:
       - Version directive: `%%{init: {'theme':'base'}}%%`
       - Diagram type: `flowchart TD`, `sequenceDiagram`, `classDiagram`, etc.
       - Proper closing with triple backticks
    
    8. **Complete Valid Example with Edge Labels**:
       ```mermaid
       %%{init: {'theme':'base'}}%%
       flowchart TD
           A["Projet de loi (Gouvernement)"]
           B["Assemblée Nationale"]
           C["Sénat"]
           D{"Conseil Constitutionnel"}
           E["Promulgation"]
           
           A -->|"Dépôt"| B
           B -->|"Vote favorable"| C
           C -->|"Approuvé"| D
           D -->|"Constitutionnel"| E
           D -->|"Inconstitutionnel (total ou partiel)"| A
           B -->|"Rejeté (1ère lecture)"| C
       ```
    
    9. **Sequence Diagram Example**:
       ```mermaid
       %%{init: {'theme':'base'}}%%
       sequenceDiagram
           participant User as ["Utilisateur"]
           participant Browser as ["Navigateur Web"]
           participant Server as ["Serveur API"]
           User->>Browser: Envoie requête
           Browser->>Server: HTTP POST /api
           Server-->>Browser: Réponse JSON
           Browser-->>User: Affiche résultat
       ```
    
    **MANDATORY**: After generating a Mermaid diagram, ALWAYS offer to save it as an image using the save button.
    
    **CRITICAL RULE**: When in doubt, ALWAYS use quotes around ALL labels (nodes and edges). It's safer to over-quote than under-quote.
    
    **TESTING CHECKLIST** - Before outputting, mentally verify:
    - ✓ All node labels with spaces/special chars are in brackets with quotes
    - ✓ All edge labels with special chars are in quotes: `-->|"text"|`
    - ✓ No `/`, `\`, `()` in unquoted labels (nodes OR edges)
    - ✓ No `\n` characters anywhere
    - ✓ No accented characters without quotes
    - ✓ Proper init directive included
    - ✓ Valid diagram type specified 

    **Crucial for Display: Formatting Charts and Tables**
            To ensure charts are displayed correctly as interactive graphics, you MUST format your chart output using a fenced code block explicitly marked as `chart`. The content of this block must be a JSON object with **EXACTLY** the following top-level structure:
            ```json
            {
            "type": "chartjs",
            "chartConfig": { /* Your actual Chart.js configuration object goes here */ }
            }
            ```
            Inside the `chartConfig` object, you will then specify the Chart.js `type` (e.g., `bar`, `line`), `data`, and `options`.

            **CRITICAL: NO JAVASCRIPT FUNCTIONS ALLOWED**
            The `chartConfig` must be PURE JSON - NO JavaScript functions, callbacks, or executable code are allowed. This means:
            - NO `function(context) { ... }` in tooltip callbacks
            - NO `function(value, index, values) { ... }` in formatting callbacks
            - NO arrow functions like `(ctx) => { ... }`
            - NO executable JavaScript code of any kind
            
            Instead, use only Chart.js's built-in configuration options that accept simple values:
            - For tooltips: Use Chart.js default formatting or simple string templates
            - For labels: Use static strings or Chart.js built-in formatters
            - For colors: Use static color arrays or predefined color schemes
            
            **Valid Chart.js Options (JSON-only):**
            ```json
            "options": {
            "responsive": true,
            "maintainAspectRatio": false,
            "plugins": {
                "title": {
                "display": true,
                "text": "Your Chart Title"
                },
                "legend": {
                "display": true,
                "position": "top"
                }
            },
            "scales": {
                "y": {
                "beginAtZero": true,
                "title": {
                    "display": true,
                    "text": "Y Axis Label"
                }
                },
                "x": {
                "title": {
                    "display": true,
                    "text": "X Axis Label"
                }
                }
            }
            }
            ```

            Example of a complete ````chart ```` block:
            ```chart
            {
            "type": "chartjs",
            "chartConfig": {
                "type": "bar",
                "data": {
                "labels": ["Mon", "Tue", "Wed"],
                "datasets": [{
                    "label": "Sales",
                    "data": [120, 150, 100],
                    "backgroundColor": ["rgba(255, 99, 132, 0.6)", "rgba(54, 162, 235, 0.6)", "rgba(255, 206, 86, 0.6)"],
                    "borderColor": ["rgba(255, 99, 132, 1)", "rgba(54, 162, 235, 1)", "rgba(255, 206, 86, 1)"],
                    "borderWidth": 1
                }]
                },
                "options": {
                "responsive": true,
                "plugins": {
                    "title": {
                    "display": true,
                    "text": "Weekly Sales Data"
                    }
                }
                }
            }
            }
            ```

            **When generating `chartConfig` for Chart.js, you MUST use only the following core supported chart types within the `chartConfig.type` field: `bar`, `line`, `pie`, `doughnut`, `polarArea`, `radar`, `scatter`, or `bubble`.**
            **Do NOT use any other chart types, especially complex ones like `heatmap`, `treemap`, `sankey`, `matrix`, `wordCloud`, `gantt`, or any other type not explicitly listed as supported, as they typically require plugins not available in the environment.**
            For data that represents counts across two categories (which might seem like a heatmap), a `bar` chart (e.g., a grouped or stacked bar chart) is a more appropriate choice for standard Chart.js.

            **Never** output chart data as plain JSON, or within a code block marked as `json` or any other type if you intend for it to be a graphical chart. Only use the ````chart ```` block.
            
            Similarly, to ensure tables are displayed correctly as formatted tables (not just code), you MUST format your table output using a fenced code block explicitly marked as `tabledata`. The content of this block must be the JSON structure for headers and rows as shown.
            Example:
            ```tabledata
            {
            "caption": "Your Table Title",
            "headers": ["Column 1", "Column 2"],
            "rows": [
                ["Data1A", "Data1B"],
                ["Data2A", "Data2B"]
            ]
            }
            ```
            **Never** output table data intended for graphical display within a code block marked as `json` or any other type. Only use the ````tabledata ```` block.

            If you need to present a form to the user to gather structured information,
            you MUST format your entire response as a single JSON string. 
            This JSON object should contain a top-level key `"formDefinition"`, and its value should be an object describing the form. 

            The `formDefinition` object should have the following structure:
            - `title` (optional string): A title for the form.
            - `description` (optional string): A short description displayed above the form fields.
            - `fields` (array of objects): Each object represents a field in the form.
            - `submitButton` (optional object): Customizes the submit button.

            Each `field` object in the `fields` array must have:
            - `name` (string): A unique identifier for the field (used for data submission).
            - `label` (string): Text label displayed to the user for this field.
            - `fieldType` (string): Type of the input field. Supported types include:
                - `"text"`: Single-line text input.
                - `"number"`: Input for numerical values.
                - `"email"`: Input for email addresses.
                - `"password"`: Password input field (masked).
                - `"textarea"`: Multi-line text input.
                - `"select"`: Dropdown list.
                - `"checkbox"`: A single checkbox.
                - `"radio"`: Radio buttons (group by `name`).
                - `"date"`: Date picker.
            - `placeholder` (optional string): Placeholder text within the input field.
            - `required` (optional boolean): Set to `true` if the field is mandatory.
            - `defaultValue` (optional string/boolean/number): A default value for the field.

            Type-specific properties for fields:
            - For `fieldType: "number"`:
                - `min` (optional number): Minimum allowed value.
                - `max` (optional number): Maximum allowed value.
                - `step` (optional number): Increment step.
            - For `fieldType: "textarea"`:
                - `rows` (optional number): Number of visible text lines.
            - For `fieldType: "select"` or `"radio"`:
                - `options` (array of objects): Each option object must have:
                    - `value` (string): The actual value submitted if this option is chosen.
                    - `text` (string): The display text for the option.

            For `fieldType: "radio"`, all radio buttons intended to be part of the same group MUST share the same `name` attribute.

            The `submitButton` object (optional) can have:
            - `text` (string): Text for the submit button (e.g., "Submit", "Send").
            - `id` (optional string): A custom ID for the submit button element.

            Example of a form definition:
            ```json
            {
            "formDefinition": {
                "title": "User Feedback Form",
                "description": "Please provide your valuable feedback.",
                "fields": [
                {
                    "name": "user_email",
                    "label": "Your Email:",
                    "fieldType": "email",
                    "placeholder": "name@example.com",
                    "required": true
                },
                {
                    "name": "rating",
                    "label": "Overall Rating:",
                    "fieldType": "select",
                    "options": [
                    {"value": "5", "text": "Excellent"},
                    {"value": "4", "text": "Good"},
                    {"value": "3", "text": "Average"},
                    {"value": "2", "text": "Fair"},
                    {"value": "1", "text": "Poor"}
                    ],
                    "required": true
                },
                {
                    "name": "comments",
                    "label": "Additional Comments:",
                    "fieldType": "textarea",
                    "rows": 4,
                    "placeholder": "Let us know your thoughts..."
                },
                {
                    "name": "subscribe_newsletter",
                    "label": "Subscribe to our newsletter",
                    "fieldType": "checkbox",
                    "defaultValue": true
                }
                ],
                "submitButton": {
                "text": "Send Feedback"
                }
            }
            }
            ```

            If you are NOT generating a form, respond with a normal text string (or markdown, etc.) as usual.
            Only use the `formDefinition` JSON structure when you intend to present a fillable form to the user.

            If you need to ask a single question with a small, fixed set of answers, you can present these as clickable options to the user.
            
            **CRITICAL: You MUST use a fenced code block with triple backticks (```) and the language identifier `optionsblock`.**
            
            Format: Start with ```optionsblock on its own line, then the JSON object, then ``` to close.
            The user's selection (the 'value' of the chosen option) will be sent back as their next message.
            
            The JSON object must have the following structure:
            - `question` (string, optional): The question text displayed to the user above the options.
            - `options` (array of objects): Each object represents a clickable option.
            - `text` (string): The text displayed on the button for the user.
            - `value` (string): The actual value that will be sent back to you if this option is chosen. This is what your system should process.
            - `id` (string, optional): A unique identifier for this set of options (e.g., for context or logging).

            **CRITICAL JSON VALIDITY NOTE**: All JSON generated for `optionsblock` (and `formDefinition`) MUST be strictly valid. A common error is including a trailing comma after the last item in an array or the last property in an object. For example, in an `options` array, the last option object should NOT be followed by a comma.

            **CRITICAL FORMATTING NOTE**: You MUST wrap the optionsblock JSON in a fenced code block with triple backticks. DO NOT output raw JSON without the code block markers.

            Example of a correctly formatted optionsblock (note the triple backticks):
            ```optionsblock
            {
            "question": "Which topic are you interested in?",
            "options": [
                {"text": "Weather Updates", "value": "get_weather"},
                {"text": "Stock Prices", "value": "get_stocks"},
                {"text": "General Knowledge", "value": "ask_general_knowledge"}
            ],
            "id": "topic_selection_dialog_001"
            }
            ```
            This is an alternative to using a full formDefinition for simple, single-question scenarios.
        Do NOT use this if multiple inputs are needed or if free-form text is expected.
"""



class MCPAgent(LlamaIndexAgent):
    """An agent with MCP (Model Context Protocol) integration and automatic memory.
    
    This agent can connect to MCP servers to access external tools and services.
    """
    
    def __init__(self):
        super().__init__()
        # Define unique agent ID (required for session isolation)
        self.agent_id = "test-agent-v1"
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
