"""
PDF generation tool with automatic image embedding from file storage.

This tool extends the PDF generation capabilities to automatically embed
images from file storage using file IDs, avoiding the need to pass large
data URIs through the LLM.
"""

import logging
import base64
import re
from typing import Callable, Optional, List

from .base import AgentTool, ToolDependencyError

# Optional dependencies
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
    WEASYPRINT_ERROR = None
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    WEASYPRINT_ERROR = str(e)

logger = logging.getLogger(__name__)


class CreatePDFWithImagesTool(AgentTool):
    """Tool for creating PDF documents from HTML with automatic image embedding."""
    
    def get_tool_function(self) -> Callable:
        """Return the PDF creation function with image support."""
        
        async def create_pdf_with_images(
            title: str,
            html_content: str,
            author: Optional[str] = None
        ) -> str:
            """
            Create a PDF document from HTML content with automatic image embedding.
            
            This tool automatically detects file_id references in img tags and
            replaces them with embedded data URIs. This avoids passing large
            base64 strings through the LLM.
            
            Args:
                title: Document title
                html_content: HTML content with special img tags using file_id
                             Format: <img src="file_id:YOUR_FILE_ID" alt="...">
                author: Optional author name
            
            Returns:
                Success message with file_id
            
            Example usage:
                1. Create a chart and get file_id: abc-123
                2. Create HTML with: <img src="file_id:abc-123" alt="Chart">
                3. Call this tool - it will automatically embed the image
            
            Example HTML:
                <h1>Report</h1>
                <p>Here is the chart:</p>
                <img src="file_id:abc-123" alt="Sales Chart">
                <p>Analysis follows...</p>
            """
            self._ensure_initialized()
            
            # Check for required dependencies
            if not WEASYPRINT_AVAILABLE:
                error_msg = "Error: WeasyPrint is not available. "
                if WEASYPRINT_ERROR and "libgobject" in WEASYPRINT_ERROR:
                    error_msg += "System dependencies are missing. Install them with:\n"
                    error_msg += "  macOS: brew install pango gdk-pixbuf libffi\n"
                    error_msg += "  Ubuntu/Debian: sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0\n"
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
                    "File storage is required but was not provided. "
                    "Ensure file_storage is set via set_context()."
                )
            
            try:
                # Find all file_id references in img tags
                # Pattern: <img src="file_id:SOME-UUID" ...>
                file_id_pattern = r'src="file_id:([a-f0-9\-]+)"'
                matches = re.findall(file_id_pattern, html_content)
                
                logger.info(f"Found {len(matches)} file_id references in HTML")
                
                # Replace each file_id with actual data URI
                processed_html = html_content
                for file_id in matches:
                    try:
                        logger.info(f"Retrieving file {file_id} for embedding")
                        
                        # Retrieve file content
                        content, metadata = await self.file_storage.retrieve_file(file_id)
                        
                        # Encode as base64
                        base64_content = base64.b64encode(content).decode('utf-8')
                        
                        # Get MIME type
                        mime_type = metadata.mime_type or "application/octet-stream"
                        
                        # Create data URI
                        data_uri = f"data:{mime_type};base64,{base64_content}"
                        
                        # Replace in HTML
                        old_src = f'src="file_id:{file_id}"'
                        new_src = f'src="{data_uri}"'
                        processed_html = processed_html.replace(old_src, new_src)
                        
                        logger.info(f"Embedded file {file_id} ({metadata.filename}, {len(base64_content)} base64 chars)")
                        
                    except Exception as e:
                        logger.error(f"Failed to embed file {file_id}: {e}")
                        return f"Error: Failed to embed image {file_id}: {str(e)}"
                
                # Wrap in complete HTML document if needed
                if not processed_html.strip().upper().startswith('<!DOCTYPE'):
                    base_css = """
                        body {
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                            font-size: 11pt;
                            line-height: 1.6;
                            color: #333;
                            margin: 2cm;
                        }
                        h1, h2, h3 { margin-top: 1em; margin-bottom: 0.5em; }
                        img { max-width: 100%; height: auto; }
                        code {
                            background-color: #f5f5f5;
                            padding: 2pt 4pt;
                            border-radius: 3pt;
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
                    """
                    
                    processed_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>{base_css}</style>
</head>
<body>
    {processed_html}
</body>
</html>"""
                
                # Generate PDF
                pdf_bytes = HTML(string=processed_html).write_pdf()
                
                # Create filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title.replace(' ', '_')
                filename = f"{safe_title}.pdf"
                
                # Store PDF
                tags = ["pdf", "generated", "html", "with-images"]
                if author:
                    tags.append(f"author:{author}")
                if matches:
                    tags.append(f"embedded-images:{len(matches)}")
                
                file_id = await self.file_storage.store_file(
                    content=pdf_bytes,
                    filename=filename,
                    user_id=self.current_user_id,
                    session_id=self.current_session_id,
                    mime_type="application/pdf",
                    tags=tags,
                    is_generated=True
                )
                
                logger.info(f"Created PDF with {len(matches)} embedded images: {filename} (file_id: {file_id})")
                return f"PDF created successfully with {len(matches)} embedded image(s)! File ID: {file_id}, Filename: {filename}"
                
            except Exception as e:
                error_msg = f"Failed to create PDF: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"Error creating PDF: {str(e)}"
        
        return create_pdf_with_images


__all__ = ["CreatePDFWithImagesTool"]
