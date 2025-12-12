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
        """Define the agent's system prompt."""
        return """You are a helpful assistant with file storage and PDF generation capabilities.

You can:
- Create, list, and read text files for users
- Generate professional PDF documents from Markdown content
- Choose from multiple PDF template styles: 'professional', 'minimal', or 'modern'

Use the provided tools to manage files and create beautiful documents.

You are a helpful  assistant. Use the provided tools to perform calculations.
        You are an assistant helping with a user's requests.
        
   You can generate markdown, mermaid diagrams, charts and code blocks, forms and optionsblocks. 
ALWAYS include option blocks in your answer especially when asking the user to select an option or continue with the conversation!!! 
ALWAYS include options blocks (OK, No Thanks) when saying something like:  Let me know if you want to ... 

NEVER propose to export data, charts or tables or generate pdf files. You are not capable YET.



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
        Use the ```optionsblock``` for this. The user's selection (the 'value' of the chosen option) will be sent back as their next message.
        Format this block as a JSON object with the following structure:
        - `question` (string, optional): The question text displayed to the user above the options.
        - `options` (array of objects): Each object represents a clickable option.
          - `text` (string): The text displayed on the button for the user.
          - `value` (string): The actual value that will be sent back to you if this option is chosen. This is what your system should process.
        - `id` (string, optional): A unique identifier for this set of options (e.g., for context or logging).

        **CRITICAL JSON VALIDITY NOTE**: All JSON generated for `optionsblock` (and `formDefinition`) MUST be strictly valid. A common error is including a trailing comma after the last item in an array or the last property in an object. For example, in an `options` array, the last option object should NOT be followed by a comma.

        Example of an optionsblock:
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
        
        ALWAYS generate the optionsblock as the last thing in your response!!!! YOU MUST DO THIS!!!"""
    
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
