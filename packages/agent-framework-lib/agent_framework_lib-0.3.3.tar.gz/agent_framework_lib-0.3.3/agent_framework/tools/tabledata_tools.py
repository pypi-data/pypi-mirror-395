"""
Table data to image conversion tool for saving tables as PNG files.
"""

import logging
from typing import Callable, Optional
import json

from .base import AgentTool, ToolDependencyError

# Optional dependencies
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
    PLAYWRIGHT_ERROR = None
except ImportError as e:
    PLAYWRIGHT_AVAILABLE = False
    PLAYWRIGHT_ERROR = str(e)

logger = logging.getLogger(__name__)


class TableToImageTool(AgentTool):
    """Tool for converting table data to PNG images."""
    
    def get_tool_function(self) -> Callable:
        """Return the table to image conversion function."""
        
        async def save_table_as_image(
            table_data: str,
            filename: str,
            width: int = 1000,
            theme: str = "default",
            font_size: int = 14,
            show_index: bool = False
        ) -> str:
            """
            Convert table data to a PNG image and save it to file storage.
            
            Args:
                table_data: JSON string containing table data with 'headers', 'rows', and optional 'caption'
                filename: Name for the output PNG file (without extension)
                width: Width of the table in pixels (default: 1000, height auto-adjusts)
                theme: Color theme - "default", "dark", "blue", "green", "minimal" (default: "default")
                font_size: Font size in pixels (default: 14)
                show_index: Show row numbers (default: False)
            
            Returns:
                Success message with file_id
            
            Example table_data format:
            {
                "caption": "Sales Report Q4 2024",
                "headers": ["Name", "Age", "City"],
                "rows": [
                    ["Alice", 30, "Paris"],
                    ["Bob", 25, "London"],
                    ["Charlie", 35, "Berlin"]
                ]
            }
            
            Note: 'caption' is optional. If not provided, no title will be shown.
            """
            self._ensure_initialized()
            
            # Check for required dependencies
            if not PLAYWRIGHT_AVAILABLE:
                return (
                    "Error: Playwright is not installed. Install with:\n"
                    "  uv add playwright\n"
                    "  playwright install chromium"
                )
            
            # Validate inputs
            if not table_data or not table_data.strip():
                return "Error: table_data cannot be empty"
            
            if not filename or not filename.strip():
                return "Error: filename cannot be empty"
            
            # Check file storage availability
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is required but was not provided. "
                    "Ensure file_storage is set via set_context()."
                )
            
            try:
                # Parse the table data
                try:
                    data = json.loads(table_data)
                except json.JSONDecodeError as e:
                    return f"Error: Invalid JSON in table_data: {str(e)}"
                
                # Extract data
                if not isinstance(data, dict):
                    return "Error: table_data must be a JSON object"
                
                if "headers" not in data:
                    return "Error: table_data must include 'headers' field"
                
                if "rows" not in data:
                    return "Error: table_data must include 'rows' field"
                
                headers = data["headers"]
                rows = data["rows"]
                caption = data.get("caption", "")  # Optional caption
                
                if not headers:
                    return "Error: headers cannot be empty"
                if not rows:
                    return "Error: rows cannot be empty"
                
                # Add index column if requested
                if show_index:
                    headers = ["#"] + headers
                    rows = [[i + 1] + row for i, row in enumerate(rows)]
                
                # Theme configurations
                themes = {
                    "default": {
                        "bg": "#ffffff",
                        "header_bg": "#f8f9fa",
                        "header_color": "#212529",
                        "row_bg": "#ffffff",
                        "row_alt_bg": "#f8f9fa",
                        "border": "#dee2e6",
                        "text": "#212529"
                    },
                    "dark": {
                        "bg": "#1a1a1a",
                        "header_bg": "#2d2d2d",
                        "header_color": "#ffffff",
                        "row_bg": "#1a1a1a",
                        "row_alt_bg": "#252525",
                        "border": "#404040",
                        "text": "#e0e0e0"
                    },
                    "blue": {
                        "bg": "#ffffff",
                        "header_bg": "#0d6efd",
                        "header_color": "#ffffff",
                        "row_bg": "#ffffff",
                        "row_alt_bg": "#e7f1ff",
                        "border": "#0d6efd",
                        "text": "#212529"
                    },
                    "green": {
                        "bg": "#ffffff",
                        "header_bg": "#198754",
                        "header_color": "#ffffff",
                        "row_bg": "#ffffff",
                        "row_alt_bg": "#d1e7dd",
                        "border": "#198754",
                        "text": "#212529"
                    },
                    "minimal": {
                        "bg": "#ffffff",
                        "header_bg": "#ffffff",
                        "header_color": "#212529",
                        "row_bg": "#ffffff",
                        "row_alt_bg": "#ffffff",
                        "border": "#e0e0e0",
                        "text": "#212529"
                    }
                }
                
                theme_colors = themes.get(theme, themes["default"])
                
                # Build HTML table
                table_html = '<table>'
                
                # Add caption if provided
                if caption:
                    # Escape HTML in caption
                    safe_caption = caption.replace('<', '&lt;').replace('>', '&gt;')
                    table_html += f'<caption>{safe_caption}</caption>'
                
                # Add headers
                table_html += '<thead><tr>'
                for header in headers:
                    # Escape HTML in headers
                    safe_header = str(header).replace('<', '&lt;').replace('>', '&gt;')
                    table_html += f'<th>{safe_header}</th>'
                table_html += '</tr></thead>'
                
                # Add rows
                table_html += '<tbody>'
                for i, row in enumerate(rows):
                    table_html += '<tr>'
                    for cell in row:
                        # Escape HTML in cells
                        safe_cell = str(cell).replace('<', '&lt;').replace('>', '&gt;')
                        table_html += f'<td>{safe_cell}</td>'
                    table_html += '</tr>'
                table_html += '</tbody></table>'
                
                # Create HTML
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 30px;
            background-color: {theme_colors['bg']};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        }}
        #tableContainer {{
            width: {width}px;
            background-color: {theme_colors['bg']};
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: {font_size}px;
            color: {theme_colors['text']};
        }}
        caption {{
            font-size: {font_size + 4}px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: left;
            color: {theme_colors['header_color']};
        }}
        th {{
            background-color: {theme_colors['header_bg']};
            color: {theme_colors['header_color']};
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            border: 1px solid {theme_colors['border']};
        }}
        td {{
            padding: 10px 15px;
            border: 1px solid {theme_colors['border']};
        }}
        tbody tr:nth-child(even) {{
            background-color: {theme_colors['row_alt_bg']};
        }}
        tbody tr:nth-child(odd) {{
            background-color: {theme_colors['row_bg']};
        }}
        tbody tr:hover {{
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div id="tableContainer">
        {table_html}
    </div>
</body>
</html>
"""
                
                # Use Playwright to render and capture
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page(
                        viewport={"width": width + 60, "height": 2000}
                    )
                    
                    # Load the HTML
                    await page.set_content(html_content)
                    
                    # Wait for content to render
                    await page.wait_for_timeout(500)
                    
                    # Take screenshot of the table container
                    table_element = await page.query_selector("#tableContainer")
                    screenshot_bytes = await table_element.screenshot(type="png")
                    
                    await browser.close()
                
                # Create safe filename
                safe_filename = "".join(
                    c for c in filename if c.isalnum() or c in (' ', '-', '_')
                ).strip()
                safe_filename = safe_filename.replace(' ', '_')
                if not safe_filename.lower().endswith('.png'):
                    safe_filename += '.png'
                
                # Store the image
                tags = [
                    "table", 
                    "png", 
                    "generated", 
                    f"rows:{len(rows)}", 
                    f"columns:{len(headers)}",
                    f"theme:{theme}"
                ]
                
                if caption:
                    tags.append("with-caption")
                
                file_id = await self.file_storage.store_file(
                    content=screenshot_bytes,
                    filename=safe_filename,
                    user_id=self.current_user_id,
                    session_id=self.current_session_id,
                    mime_type="image/png",
                    tags=tags,
                    is_generated=True
                )
                
                logger.info(f"Created table image: {safe_filename} (file_id: {file_id})")
                caption_info = f" with caption '{caption}'" if caption else ""
                return f"Table saved successfully as PNG{caption_info}! File ID: {file_id}, Filename: {safe_filename} ({len(rows)} rows, {len(headers)} columns)"
                
            except Exception as e:
                error_msg = f"Failed to create table image: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"Error creating table image: {str(e)}"
        
        return save_table_as_image


__all__ = ["TableToImageTool"]