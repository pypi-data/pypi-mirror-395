"""
Chart.js to image conversion tool for saving charts as PNG files.
"""

import logging
from typing import Callable, Optional
import json
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


class ChartToImageTool(AgentTool):
    """Tool for converting Chart.js configurations to PNG images."""
    
    def get_tool_function(self) -> Callable:
        """Return the chart to image conversion function."""
        
        async def save_chart_as_image(
            chart_config: str,
            filename: str,
            width: int = 800,
            height: int = 600,
            background_color: str = "white"
        ) -> str:
            """
            Convert a Chart.js configuration to a PNG image and save it to file storage.
            
            Args:
                chart_config: JSON string containing the Chart.js configuration
                             (the complete chartConfig object with type, data, options)
                filename: Name for the output PNG file (without extension)
                width: Width of the chart in pixels (default: 800)
                height: Height of the chart in pixels (default: 600)
                background_color: Background color for the chart (default: "white")
            
            Returns:
                Success message with file_id
            
            Example chart_config:
            {
                "type": "bar",
                "data": {
                    "labels": ["Mon", "Tue", "Wed"],
                    "datasets": [{
                        "label": "Sales",
                        "data": [120, 150, 100],
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
            if not chart_config or not chart_config.strip():
                return "Error: chart_config cannot be empty"
            
            if not filename or not filename.strip():
                return "Error: filename cannot be empty"
            
            # Check file storage availability
            if not self.file_storage:
                raise ToolDependencyError(
                    "File storage is required but was not provided. "
                    "Ensure file_storage is set via set_context()."
                )
            
            try:
                # Parse the chart config
                try:
                    config = json.loads(chart_config)
                except json.JSONDecodeError as e:
                    return f"Error: Invalid JSON in chart_config: {str(e)}"
                
                # Validate chart config structure
                if "type" not in config:
                    return "Error: chart_config must include a 'type' field"
                if "data" not in config:
                    return "Error: chart_config must include a 'data' field"
                
                # Create HTML with Chart.js
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: {background_color};
        }}
        #chartContainer {{
            width: {width}px;
            height: {height}px;
        }}
    </style>
</head>
<body>
    <div id="chartContainer">
        <canvas id="myChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('myChart');
        const config = {json.dumps(config)};
        
        // Ensure the chart is responsive within our container
        if (!config.options) {{
            config.options = {{}};
        }}
        config.options.responsive = true;
        config.options.maintainAspectRatio = false;
        
        new Chart(ctx, config);
    </script>
</body>
</html>
"""
                
                # Use Playwright to render and capture
                async with async_playwright() as p:
                    browser = await p.chromium.launch()
                    page = await browser.new_page(
                        viewport={"width": width + 40, "height": height + 40}
                    )
                    
                    # Load the HTML
                    await page.set_content(html_content)
                    
                    # Wait for Chart.js to render
                    await page.wait_for_timeout(1000)  # Give Chart.js time to render
                    
                    # Take screenshot of the chart container
                    chart_element = await page.query_selector("#chartContainer")
                    screenshot_bytes = await chart_element.screenshot(type="png")
                    
                    await browser.close()
                
                # Create safe filename
                safe_filename = "".join(
                    c for c in filename if c.isalnum() or c in (' ', '-', '_')
                ).strip()
                safe_filename = safe_filename.replace(' ', '_')
                if not safe_filename.lower().endswith('.png'):
                    safe_filename += '.png'
                
                # Store the image
                tags = ["chart", "png", "generated", f"chart-type:{config['type']}"]
                
                file_id = await self.file_storage.store_file(
                    content=screenshot_bytes,
                    filename=safe_filename,
                    user_id=self.current_user_id,
                    session_id=self.current_session_id,
                    mime_type="image/png",
                    tags=tags,
                    is_generated=True
                )
                
                logger.info(f"Created chart image: {safe_filename} (file_id: {file_id})")
                return f"Chart saved successfully as PNG! File ID: {file_id}, Filename: {safe_filename}"
                
            except Exception as e:
                error_msg = f"Failed to create chart image: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return f"Error creating chart image: {str(e)}"
        
        return save_chart_as_image


__all__ = ["ChartToImageTool"]