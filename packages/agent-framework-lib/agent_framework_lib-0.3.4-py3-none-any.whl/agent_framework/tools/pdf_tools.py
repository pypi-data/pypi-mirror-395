"""
PDF generation tools for creating documents from Markdown and HTML.

This module provides tools for generating professional PDF documents from
Markdown or HTML content with multiple template styles and custom CSS support.
"""

import logging
from typing import Callable, Optional
from io import BytesIO

# Auto-configure WeasyPrint libraries
from agent_framework.utils.path_utils import PathDetector

from .base import AgentTool, ToolDependencyError

# Optional dependencies - will be checked at runtime
try:
    import markdown
    from markdown.extensions import extra, codehilite, tables, fenced_code
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
    WEASYPRINT_ERROR = None
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    WEASYPRINT_ERROR = str(e)

logger = logging.getLogger(__name__)


# Template styles for PDF generation
TEMPLATE_STYLES = {
    "professional": """
        @page {
            margin: 2.5cm;
            @top-center {
                content: string(doctitle);
                font-family: Georgia, serif;
                font-size: 10pt;
                color: #2c5aa0;
            }
            @bottom-center {
                content: counter(page);
                font-family: Georgia, serif;
                font-size: 10pt;
            }
        }
        body {
            font-family: Georgia, serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }
        h1 {
            string-set: doctitle content();
            color: #2c5aa0;
            font-size: 24pt;
            margin-top: 0;
            margin-bottom: 20pt;
            border-bottom: 2pt solid #2c5aa0;
            padding-bottom: 10pt;
        }
        h2 {
            color: #2c5aa0;
            font-size: 18pt;
            margin-top: 20pt;
            margin-bottom: 12pt;
        }
        h3 {
            color: #4a7ac2;
            font-size: 14pt;
            margin-top: 16pt;
            margin-bottom: 10pt;
        }
        code {
            background-color: #f5f5f5;
            padding: 2pt 4pt;
            border-radius: 3pt;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        pre {
            background-color: #f5f5f5;
            padding: 12pt;
            border-left: 3pt solid #2c5aa0;
            border-radius: 3pt;
            overflow-x: auto;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 12pt 0;
        }
        th, td {
            border: 1pt solid #ddd;
            padding: 8pt;
            text-align: left;
        }
        th {
            background-color: #2c5aa0;
            color: white;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        ul, ol {
            margin: 10pt 0;
            padding-left: 30pt;
        }
        li {
            margin: 5pt 0;
        }
        a {
            color: #2c5aa0;
            text-decoration: none;
        }
        blockquote {
            border-left: 3pt solid #2c5aa0;
            padding-left: 15pt;
            margin-left: 0;
            color: #666;
            font-style: italic;
        }
    """,
    
    "minimal": """
        @page {
            margin: 2cm;
            @bottom-center {
                content: counter(page);
                font-family: Helvetica, Arial, sans-serif;
                font-size: 9pt;
            }
        }
        body {
            font-family: Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #000;
        }
        h1 {
            font-size: 22pt;
            margin-top: 0;
            margin-bottom: 18pt;
            font-weight: bold;
        }
        h2 {
            font-size: 16pt;
            margin-top: 18pt;
            margin-bottom: 10pt;
            font-weight: bold;
        }
        h3 {
            font-size: 13pt;
            margin-top: 14pt;
            margin-bottom: 8pt;
            font-weight: bold;
        }
        code {
            background-color: #f0f0f0;
            padding: 2pt 4pt;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        pre {
            background-color: #f0f0f0;
            padding: 10pt;
            border: 1pt solid #ccc;
            overflow-x: auto;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10pt 0;
        }
        th, td {
            border: 1pt solid #000;
            padding: 6pt;
            text-align: left;
        }
        th {
            background-color: #000;
            color: white;
            font-weight: bold;
        }
        ul, ol {
            margin: 8pt 0;
            padding-left: 25pt;
        }
        li {
            margin: 4pt 0;
        }
        a {
            color: #000;
            text-decoration: underline;
        }
        blockquote {
            border-left: 2pt solid #000;
            padding-left: 12pt;
            margin-left: 0;
        }
    """,
    
    "modern": """
        @page {
            margin: 2cm;
            @top-right {
                content: counter(page);
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                font-size: 9pt;
                color: #666;
            }
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 11pt;
            line-height: 1.7;
            color: #1a1a1a;
        }
        h1 {
            font-size: 28pt;
            margin-top: 0;
            margin-bottom: 20pt;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        h2 {
            font-size: 20pt;
            margin-top: 20pt;
            margin-bottom: 12pt;
            font-weight: 600;
            color: #667eea;
        }
        h3 {
            font-size: 15pt;
            margin-top: 16pt;
            margin-bottom: 10pt;
            font-weight: 600;
            color: #764ba2;
        }
        code {
            background-color: #f6f8fa;
            padding: 2pt 5pt;
            border-radius: 4pt;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 10pt;
            color: #e83e8c;
        }
        pre {
            background-color: #f6f8fa;
            padding: 14pt;
            border-radius: 6pt;
            border: 1pt solid #e1e4e8;
            overflow-x: auto;
        }
        pre code {
            background-color: transparent;
            padding: 0;
            color: #1a1a1a;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 14pt 0;
            border-radius: 6pt;
            overflow: hidden;
        }
        th, td {
            border: 1pt solid #e1e4e8;
            padding: 10pt;
            text-align: left;
        }
        th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
        }
        tr:nth-child(even) {
            background-color: #f6f8fa;
        }
        ul, ol {
            margin: 12pt 0;
            padding-left: 28pt;
        }
        li {
            margin: 6pt 0;
        }
        a {
            color: #667eea;
            text-decoration: none;
            border-bottom: 1pt solid #667eea;
        }
        blockquote {
            border-left: 4pt solid #667eea;
            padding-left: 16pt;
            margin-left: 0;
            color: #666;
            font-style: italic;
        }
    """
}


BASE_HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        {css}
    </style>
</head>
<body>
    {content}
</body>
</html>
"""


class CreatePDFFromMarkdownTool(AgentTool):
    """Tool for creating PDF documents from Markdown content."""
    
    def get_tool_function(self) -> Callable:
        """Return the PDF from Markdown creation function."""
        
        async def create_pdf_from_markdown(
            title: str,
            content: str,
            author: Optional[str] = None,
            template_style: str = "professional"
        ) -> str:
            """
            Create a PDF document from Markdown content.
            
            Args:
                title: Document title (used for filename and header)
                content: Markdown formatted content
                author: Optional author name
                template_style: 'professional', 'minimal', or 'modern'
            
            Returns:
                Success message with file_id
            """
            self._ensure_initialized()
            
            # Check for required dependencies
            if not MARKDOWN_AVAILABLE:
                return "Error: markdown package is not installed. Install with: uv add markdown"
            
            if not WEASYPRINT_AVAILABLE:
                error_msg = "Error: WeasyPrint is not available. "
                if WEASYPRINT_ERROR and "libgobject" in WEASYPRINT_ERROR:
                    error_msg += "System dependencies are missing. Install them with:\n"
                    error_msg += "  macOS: brew install pango gdk-pixbuf libffi && export DYLD_LIBRARY_PATH=\"/opt/homebrew/lib:$DYLD_LIBRARY_PATH\"\n"
                    error_msg += "  Ubuntu/Debian: sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev\n"
                    error_msg += "  Fedora/RHEL: sudo dnf install pango gdk-pixbuf2 libffi-devel"
                else:
                    error_msg += "Install with: uv add weasyprint"
                return error_msg
            
            # Validate inputs
            if not title or not title.strip():
                return "Error: Title cannot be empty"
            
            if not content or not content.strip():
                return "Error: Content cannot be empty"
            
            if template_style not in TEMPLATE_STYLES:
                return f"Error: Invalid template style '{template_style}'. Use 'professional', 'minimal', or 'modern'."
            
            # Check file storage availability
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is required for PDF creation but was not provided. "
                    "Ensure file_storage is set via set_context()."
                )
            
            try:
                # Convert Markdown to HTML
                md = markdown.Markdown(extensions=[
                    'extra',
                    'codehilite',
                    'tables',
                    'fenced_code'
                ])
                html_content = md.convert(content)
                
                # Get template CSS
                css = TEMPLATE_STYLES[template_style]
                
                # Create complete HTML document
                html_doc = BASE_HTML_TEMPLATE.format(
                    title=title,
                    css=css,
                    content=html_content
                )
                
                # Generate PDF
                pdf_bytes = HTML(string=html_doc).write_pdf()
                
                # Create filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title.replace(' ', '_')
                filename = f"{safe_title}.pdf"
                
                # Store PDF
                tags = ["pdf", "generated", "markdown", f"template:{template_style}"]
                if author:
                    tags.append(f"author:{author}")
                
                file_id = await self.file_storage.store_file(
                    content=pdf_bytes,
                    filename=filename,
                    user_id=self.current_user_id,
                    session_id=self.current_session_id,
                    mime_type="application/pdf",
                    tags=tags,
                    is_generated=True
                )
                
                logger.info(f"Created PDF from Markdown: {filename} (file_id: {file_id})")
                return f"PDF created successfully! File ID: {file_id}, Filename: {filename}"
                
            except Exception as e:
                error_msg = f"Failed to create PDF: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"Error creating PDF: {str(e)}"
        
        return create_pdf_from_markdown


class CreatePDFFromHTMLTool(AgentTool):
    """Tool for creating PDF documents from HTML content."""
    
    def get_tool_function(self) -> Callable:
        """Return the PDF from HTML creation function."""
        
        async def create_pdf_from_html(
            title: str,
            html_content: str,
            custom_css: Optional[str] = None,
            author: Optional[str] = None
        ) -> str:
            """
            Create a PDF document from HTML content with optional custom CSS.
            
            Args:
                title: Document title
                html_content: Full HTML document or HTML fragment
                custom_css: Optional additional CSS to apply
                author: Optional author name
            
            Returns:
                Success message with file_id
            """
            self._ensure_initialized()
            
            # Check for required dependencies
            if not WEASYPRINT_AVAILABLE:
                error_msg = "Error: WeasyPrint is not available. "
                if WEASYPRINT_ERROR and "libgobject" in WEASYPRINT_ERROR:
                    error_msg += "System dependencies are missing. Install them with:\n"
                    error_msg += "  macOS: brew install pango gdk-pixbuf libffi && export DYLD_LIBRARY_PATH=\"/opt/homebrew/lib:$DYLD_LIBRARY_PATH\"\n"
                    error_msg += "  Ubuntu/Debian: sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev\n"
                    error_msg += "  Fedora/RHEL: sudo dnf install pango gdk-pixbuf2 libffi-devel"
                else:
                    error_msg += "Install with: uv add weasyprint"
                return error_msg
            
            # Validate inputs
            if not title or not title.strip():
                return "Error: Title cannot be empty"
            
            if not html_content or not html_content.strip():
                return "Error: HTML content cannot be empty"
            
            # Check file storage availability
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is required for PDF creation but was not provided. "
                    "Ensure file_storage is set via set_context()."
                )
            
            try:
                # Detect if HTML is a complete document or fragment
                is_complete_doc = (
                    '<!DOCTYPE' in html_content.upper() or
                    '<HTML' in html_content.upper()
                )
                
                if is_complete_doc:
                    # Use HTML as-is, optionally inject custom CSS
                    if custom_css:
                        # Try to inject CSS before </head> or at the beginning
                        css_tag = f"<style>{custom_css}</style>"
                        if '</head>' in html_content.lower():
                            html_doc = html_content.replace('</head>', f"{css_tag}</head>", 1)
                        else:
                            html_doc = css_tag + html_content
                    else:
                        html_doc = html_content
                else:
                    # Wrap fragment in complete document structure
                    base_css = """
                        body {
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                            font-size: 11pt;
                            line-height: 1.6;
                            color: #333;
                            margin: 2cm;
                        }
                        h1, h2, h3, h4, h5, h6 {
                            margin-top: 1em;
                            margin-bottom: 0.5em;
                        }
                        code {
                            background-color: #f5f5f5;
                            padding: 2pt 4pt;
                            border-radius: 3pt;
                            font-family: 'Courier New', monospace;
                        }
                        pre {
                            background-color: #f5f5f5;
                            padding: 12pt;
                            border-radius: 3pt;
                            overflow-x: auto;
                        }
                        table {
                            border-collapse: collapse;
                            width: 100%;
                            margin: 12pt 0;
                        }
                        th, td {
                            border: 1pt solid #ddd;
                            padding: 8pt;
                            text-align: left;
                        }
                        th {
                            background-color: #f0f0f0;
                            font-weight: bold;
                        }
                    """
                    
                    combined_css = base_css
                    if custom_css:
                        combined_css += "\n" + custom_css
                    
                    html_doc = BASE_HTML_TEMPLATE.format(
                        title=title,
                        css=combined_css,
                        content=html_content
                    )
                
                # Generate PDF
                pdf_bytes = HTML(string=html_doc).write_pdf()
                
                # Create filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title.replace(' ', '_')
                filename = f"{safe_title}.pdf"
                
                # Store PDF
                tags = ["pdf", "generated", "html"]
                if custom_css:
                    tags.append("custom-css")
                if author:
                    tags.append(f"author:{author}")
                
                file_id = await self.file_storage.store_file(
                    content=pdf_bytes,
                    filename=filename,
                    user_id=self.current_user_id,
                    session_id=self.current_session_id,
                    mime_type="application/pdf",
                    tags=tags,
                    is_generated=True
                )
                
                logger.info(f"Created PDF from HTML: {filename} (file_id: {file_id})")
                return f"PDF created successfully! File ID: {file_id}, Filename: {filename}"
                
            except Exception as e:
                error_msg = f"Failed to create PDF from HTML: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"Error creating PDF: {str(e)}"
        
        return create_pdf_from_html


__all__ = [
    "CreatePDFFromMarkdownTool",
    "CreatePDFFromHTMLTool",
]
