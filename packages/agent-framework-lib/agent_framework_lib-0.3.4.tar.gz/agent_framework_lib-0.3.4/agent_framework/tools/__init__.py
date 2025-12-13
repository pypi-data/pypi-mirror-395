"""
Agent Framework Tools

Reusable tools for agents including file operations, PDF creation, and more.

This module provides a collection of tools that can be used across different
agents with proper dependency injection and error handling. All tools inherit
from the AgentTool base class and follow a consistent pattern for initialization
and usage.

Available Tools:
    - PDF Tools: Create professional PDFs from Markdown or HTML
    - File Tools: Create, list, and read files from storage
    - Multimodal Tools: Process images, audio, and other media

Example:
    from agent_framework.tools import CreateFileTool, CreatePDFFromMarkdownTool
    
    # Initialize tools
    file_tool = CreateFileTool()
    pdf_tool = CreatePDFFromMarkdownTool()
    
    # Inject dependencies
    file_tool.set_context(
        file_storage=storage_manager,
        user_id="user123",
        session_id="session456"
    )
    pdf_tool.set_context(
        file_storage=storage_manager,
        user_id="user123",
        session_id="session456"
    )
    
    # Get tool functions for agent use
    create_file_func = file_tool.get_tool_function()
    create_pdf_func = pdf_tool.get_tool_function()
"""

# Base classes and exceptions
from .base import AgentTool, ToolDependencyError

# File storage tools (always available)
from .file_tools import (
    CreateFileTool,
    ListFilesTool,
    ReadFileTool,
)

# PDF generation tools (optional - requires system dependencies)
try:
    from .pdf_tools import (
        CreatePDFFromMarkdownTool,
        CreatePDFFromHTMLTool,
    )
    PDF_TOOLS_AVAILABLE = True
except (ImportError, OSError) as e:
    # OSError can occur when weasyprint's system dependencies are missing
    import warnings
    
    if isinstance(e, OSError) and "libgobject" in str(e):
        warnings.warn(
            "\n" + "="*60 + "\n"
            "PDF generation tools are not available!\n"
            "System dependencies are missing. Install them with:\n\n"
            "macOS:\n"
            "  brew install pango gdk-pixbuf libffi\n"
            "  export DYLD_LIBRARY_PATH=\"/opt/homebrew/lib:$DYLD_LIBRARY_PATH\"\n\n"
            "Ubuntu/Debian:\n"
            "  sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev\n\n"
            "Fedora/RHEL:\n"
            "  sudo dnf install pango gdk-pixbuf2 libffi-devel\n"
            + "="*60,
            ImportWarning,
            stacklevel=2
        )
    elif isinstance(e, ImportError):
        warnings.warn(
            f"PDF generation tools are not available: {e}\n"
            "Install with: uv add weasyprint markdown",
            ImportWarning,
            stacklevel=2
        )
    
    PDF_TOOLS_AVAILABLE = False
    CreatePDFFromMarkdownTool = None
    CreatePDFFromHTMLTool = None

from .chart_tools import ChartToImageTool
from .mermaid_tools import MermaidToImageTool
from .tabledata_tools import TableToImageTool

# File access tools
from .file_access_tools import (
    GetFilePathTool,
    GetFileAsDataURITool,
)

# PDF with images tool
from .pdf_with_images_tool import CreatePDFWithImagesTool

__all__ = [
    # Base classes
    'AgentTool',
    'ToolDependencyError',
    
    # PDF tools (may be None if dependencies not available)
    'CreatePDFFromMarkdownTool',
    'CreatePDFFromHTMLTool',
    'PDF_TOOLS_AVAILABLE',

    # Chart Tools
    'ChartToImageTool',
    
    # File tools
    'CreateFileTool',
    'ListFilesTool',
    'ReadFileTool',
    
    # File access tools
    'GetFilePathTool',
    'GetFileAsDataURITool',
    
    # PDF with images
    'CreatePDFWithImagesTool',
    
    # Legacy exports
    'multimodal_tools',
]
