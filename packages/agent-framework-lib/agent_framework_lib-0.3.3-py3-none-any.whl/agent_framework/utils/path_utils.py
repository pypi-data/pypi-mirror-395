"""
Path utilities for automatic detection of system tools.

This module provides utilities to automatically detect and configure
system paths for external tools like PDF converters.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


class PathDetector:
    """Automatically detect and configure system tool paths"""
    
    # Common installation paths for different systems
    COMMON_PATHS = {
        'darwin': [  # macOS
            '/opt/homebrew/bin',
            '/usr/local/bin',
            '/opt/local/bin',  # MacPorts
            os.path.expanduser('~/.local/bin'),
        ],
        'linux': [
            '/usr/bin',
            '/usr/local/bin',
            '/opt/bin',
            os.path.expanduser('~/.local/bin'),
        ],
        'win32': [
            r'C:\Program Files\poppler\bin',
            r'C:\Program Files (x86)\poppler\bin',
            os.path.expanduser(r'~\AppData\Local\Programs\poppler\bin'),
        ]
    }
    
    @classmethod
    def detect_tool_path(cls, tool_name: str) -> Optional[str]:
        """
        Detect the path to a system tool.
        
        Args:
            tool_name: Name of the tool to find (e.g., 'pdftotext', 'pdfinfo')
            
        Returns:
            Full path to the tool if found, None otherwise
        """
        # First check if tool is already in PATH
        tool_path = shutil.which(tool_name)
        if tool_path:
            logger.debug(f"✓ Found {tool_name} in PATH: {tool_path}")
            return tool_path
        
        # Get platform-specific paths
        import sys
        platform = sys.platform
        search_paths = cls.COMMON_PATHS.get(platform, [])
        
        # Search in common paths
        for path in search_paths:
            if not os.path.exists(path):
                continue
                
            tool_full_path = os.path.join(path, tool_name)
            if os.path.isfile(tool_full_path) and os.access(tool_full_path, os.X_OK):
                logger.debug(f"✓ Found {tool_name} at: {tool_full_path}")
                return tool_full_path
        
        logger.debug(f"✗ Could not find {tool_name} in common paths")
        return None
    
    @classmethod
    def configure_pdf_tools_path(cls) -> bool:
        """
        Automatically detect and configure PATH for PDF tools (poppler).
        
        This function searches for PDF tools like pdftotext and pdfinfo
        in common installation locations and adds them to PATH if found.
        
        Returns:
            True if PDF tools were found and configured, False otherwise
        """
        # Tools to check for (poppler-utils)
        pdf_tools = ['pdftotext', 'pdfinfo', 'pdfimages']
        
        # Check if any tool is already available
        for tool in pdf_tools:
            if shutil.which(tool):
                logger.debug(f"✓ PDF tools already in PATH (found {tool})")
                return True
        
        # Try to find tools in common paths
        import sys
        platform = sys.platform
        search_paths = cls.COMMON_PATHS.get(platform, [])
        
        for path in search_paths:
            if not os.path.exists(path):
                continue
            
            # Check if any PDF tool exists in this path
            for tool in pdf_tools:
                tool_full_path = os.path.join(path, tool)
                if os.path.isfile(tool_full_path) and os.access(tool_full_path, os.X_OK):
                    # Found a tool, add this path to PATH
                    current_path = os.environ.get('PATH', '')
                    if path not in current_path:
                        os.environ['PATH'] = f"{path}{os.pathsep}{current_path}"
                        logger.info(f"✓ Added {path} to PATH for PDF tools")
                    
                    # Also set DYLD_LIBRARY_PATH on macOS for library dependencies
                    if platform == 'darwin':
                        lib_path = path.replace('/bin', '/lib')
                        if os.path.exists(lib_path):
                            current_dyld = os.environ.get('DYLD_LIBRARY_PATH', '')
                            if lib_path not in current_dyld:
                                os.environ['DYLD_LIBRARY_PATH'] = f"{lib_path}{os.pathsep}{current_dyld}"
                                logger.debug(f"✓ Added {lib_path} to DYLD_LIBRARY_PATH")
                    
                    return True
        
        logger.debug("✗ Could not find PDF tools in common paths")
        return False
    
    @classmethod
    def configure_weasyprint_libs(cls) -> bool:
        """
        Automatically configure library paths for WeasyPrint (pango, cairo, etc.).
        
        WeasyPrint requires system libraries like pango, cairo, gdk-pixbuf.
        This function configures the necessary environment variables.
        
        Returns:
            True if libraries were found and configured, False otherwise
        """
        import sys
        platform = sys.platform
        
        if platform == 'darwin':
            # macOS - check Homebrew paths
            homebrew_paths = [
                '/opt/homebrew/lib',  # Apple Silicon
                '/usr/local/lib',     # Intel
            ]
            
            for lib_path in homebrew_paths:
                if os.path.exists(lib_path):
                    # Check for pango library
                    pango_lib = os.path.join(lib_path, 'libpango-1.0.dylib')
                    if os.path.exists(pango_lib):
                        # Configure DYLD_LIBRARY_PATH
                        current_dyld = os.environ.get('DYLD_LIBRARY_PATH', '')
                        if lib_path not in current_dyld:
                            os.environ['DYLD_LIBRARY_PATH'] = f"{lib_path}{os.pathsep}{current_dyld}"
                            logger.info(f"✓ Added {lib_path} to DYLD_LIBRARY_PATH for WeasyPrint")
                        
                        # Also set DYLD_FALLBACK_LIBRARY_PATH
                        current_fallback = os.environ.get('DYLD_FALLBACK_LIBRARY_PATH', '')
                        if lib_path not in current_fallback:
                            os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = f"{lib_path}{os.pathsep}{current_fallback}"
                        
                        return True
            
            logger.debug("✗ WeasyPrint libraries not found in Homebrew paths")
            return False
        
        elif platform.startswith('linux'):
            # Linux - libraries are usually in standard paths
            # Check if pango is available
            lib_paths = ['/usr/lib', '/usr/local/lib', '/usr/lib/x86_64-linux-gnu']
            for lib_path in lib_paths:
                pango_lib = os.path.join(lib_path, 'libpango-1.0.so')
                if os.path.exists(pango_lib) or os.path.exists(pango_lib + '.0'):
                    logger.debug(f"✓ WeasyPrint libraries found at {lib_path}")
                    return True
            
            logger.debug("✗ WeasyPrint libraries not found")
            return False
        
        # Windows or other platforms
        return False
    
    @classmethod
    def get_installation_instructions(cls, tool_name: str = 'poppler') -> str:
        """
        Get platform-specific installation instructions for a tool.
        
        Args:
            tool_name: Name of the tool package (default: 'poppler')
            
        Returns:
            Installation instructions as a string
        """
        import sys
        platform = sys.platform
        
        instructions = {
            'darwin': f"""
macOS Installation:
  brew install {tool_name}
  brew install pango cairo gdk-pixbuf  # For WeasyPrint

After installation, the tools should be automatically detected.
If not, you may need to add to your shell profile (~/.zshrc or ~/.bash_profile):
  export PATH="/opt/homebrew/bin:$PATH"
  export DYLD_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_LIBRARY_PATH"
""",
            'linux': f"""
Linux Installation:

Ubuntu/Debian:
  sudo apt-get update
  sudo apt-get install {tool_name}-utils
  sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libcairo2  # For WeasyPrint

Fedora/RHEL:
  sudo dnf install {tool_name}-utils
  sudo dnf install pango gdk-pixbuf2 libffi-devel cairo  # For WeasyPrint

Arch Linux:
  sudo pacman -S {tool_name}
  sudo pacman -S pango cairo gdk-pixbuf2  # For WeasyPrint
""",
            'win32': f"""
Windows Installation:

1. Download {tool_name} from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract to C:\\Program Files\\{tool_name}
3. Add C:\\Program Files\\{tool_name}\\bin to your PATH environment variable

Or use Chocolatey:
  choco install {tool_name}
"""
        }
        
        return instructions.get(platform, f"Please install {tool_name} for your platform")


# Auto-configure PDF tools and WeasyPrint on module import
_pdf_tools_configured = PathDetector.configure_pdf_tools_path()
if _pdf_tools_configured:
    logger.debug("✓ PDF tools path auto-configured successfully")
else:
    logger.debug("⚠ PDF tools not found - markitdown may have limited PDF support")
    logger.debug("  Install poppler-utils for better PDF processing")

_weasyprint_configured = PathDetector.configure_weasyprint_libs()
if _weasyprint_configured:
    logger.debug("✓ WeasyPrint libraries auto-configured successfully")
else:
    logger.debug("⚠ WeasyPrint libraries not found - PDF generation may not work")
    logger.debug("  Install pango, cairo, gdk-pixbuf for WeasyPrint support")
