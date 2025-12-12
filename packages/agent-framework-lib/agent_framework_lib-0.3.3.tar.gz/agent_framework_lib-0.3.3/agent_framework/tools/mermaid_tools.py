"""
Mermaid to image conversion tool for saving diagrams as PNG files.
"""

import logging
from typing import Callable, Optional
import base64

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


class MermaidToImageTool(AgentTool):
    """Tool for converting Mermaid diagrams to PNG images."""
    
    def get_tool_function(self) -> Callable:
        """Return the mermaid to image conversion function."""
        
        async def save_mermaid_as_image(
            mermaid_code: str,
            filename: str,
            width: int = 1200,
            height: int = 800,
            background_color: str = "white",
            theme: str = "default"
        ) -> str:
            """
            Convert a Mermaid diagram to a PNG image and save it to file storage.
            
            Args:
                mermaid_code: Mermaid diagram code (without ```mermaid``` markers)
                filename: Name for the output PNG file (without extension)
                width: Width of the viewport in pixels (default: 1200)
                height: Height of the viewport in pixels (default: 800)
                background_color: Background color for the diagram (default: "white")
                theme: Mermaid theme - "default", "dark", "forest", "neutral" (default: "default")
            
            Returns:
                Success message with file_id
            
            Example mermaid_code:
            graph TD
                A[Start] --> B{Decision}
                B -->|Yes| C[Process]
                B -->|No| D[End]
                C --> D
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
            if not mermaid_code or not mermaid_code.strip():
                return "Error: mermaid_code cannot be empty"
            
            if not filename or not filename.strip():
                return "Error: filename cannot be empty"
            
            # Check file storage availability
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is required but was not provided. "
                    "Ensure file_storage is set via set_context()."
                )
            
            # Clean mermaid code (remove markdown code blocks if present)
            clean_code = mermaid_code.strip()
            if clean_code.startswith("```mermaid"):
                clean_code = clean_code.replace("```mermaid", "").replace("```", "").strip()
            elif clean_code.startswith("```"):
                clean_code = clean_code.replace("```", "").strip()
            
            try:
                # Create HTML with Mermaid
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: '{theme}',
            securityLevel: 'loose'
        }});
    </script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: {background_color};
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        #diagram {{
            background-color: {background_color};
        }}
    </style>
</head>
<body>
    <div id="diagram" class="mermaid">
{clean_code}
    </div>
</body>
</html>
"""
                
                # Use Playwright to render and capture
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page(
                        viewport={"width": width, "height": height}
                    )
                    
                    # Load the HTML
                    await page.set_content(html_content)
                    
                    # Wait for Mermaid to render
                    await page.wait_for_selector("#diagram svg", timeout=5000)
                    await page.wait_for_timeout(500)  # Extra time for animations
                    
                    # Get the SVG element to capture just the diagram
                    diagram_element = await page.query_selector("#diagram")
                    screenshot_bytes = await diagram_element.screenshot(
                        type="png",
                        omit_background=(background_color.lower() == "transparent")
                    )
                    
                    await browser.close()
                
                # Create safe filename
                safe_filename = "".join(
                    c for c in filename if c.isalnum() or c in (' ', '-', '_')
                ).strip()
                safe_filename = safe_filename.replace(' ', '_')
                if not safe_filename.lower().endswith('.png'):
                    safe_filename += '.png'
                
                # Detect diagram type from mermaid code
                diagram_type = "unknown"
                first_line = clean_code.split('\n')[0].strip().lower()
                if first_line.startswith("graph"):
                    diagram_type = "flowchart"
                elif first_line.startswith("sequencediagram"):
                    diagram_type = "sequence"
                elif first_line.startswith("classDiagram"):
                    diagram_type = "class"
                elif first_line.startswith("statediagram") or first_line.startswith("state "):
                    diagram_type = "state"
                elif first_line.startswith("erdiagram"):
                    diagram_type = "er"
                elif first_line.startswith("gantt"):
                    diagram_type = "gantt"
                elif first_line.startswith("pie"):
                    diagram_type = "pie"
                elif first_line.startswith("journey"):
                    diagram_type = "journey"
                
                # Store the image
                tags = ["mermaid", "diagram", "png", "generated", f"diagram-type:{diagram_type}"]
                
                file_id = await self.file_storage.store_file(
                    content=screenshot_bytes,
                    filename=safe_filename,
                    user_id=self.current_user_id,
                    session_id=self.current_session_id,
                    mime_type="image/png",
                    tags=tags,
                    is_generated=True
                )
                
                logger.info(f"Created mermaid diagram: {safe_filename} (file_id: {file_id})")
                return f"Mermaid diagram saved successfully as PNG! File ID: {file_id}, Filename: {safe_filename}"
                
            except Exception as e:
                error_msg = f"Failed to create mermaid diagram: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"Error creating mermaid diagram: {str(e)}"
        
        return save_mermaid_as_image


__all__ = ["MermaidToImageTool"]