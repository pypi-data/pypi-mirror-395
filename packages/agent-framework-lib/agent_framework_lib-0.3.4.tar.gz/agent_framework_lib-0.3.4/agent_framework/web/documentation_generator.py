"""Documentation generator for serving comprehensive documentation via web endpoint."""

import logging
from pathlib import Path
from typing import Optional, List, Dict
import markdown


logger = logging.getLogger(__name__)


# Documentation sections configuration
DOCUMENTATION_SECTIONS = [
    {
        "id": "readme",
        "title": "README",
        "filename": "README.md",
        "order": 1
    },
    {
        "id": "api-reference",
        "title": "API Reference",
        "filename": "api-reference.md",
        "order": 2
    },
    {
        "id": "configuratio-guide",
        "title": "Configuration Guide",
        "filename": "configuration.md",
        "order": 3
    },
    {
        "id": "creating-agents",
        "title": "Creating Agents",
        "filename": "CREATING_AGENTS.md",
        "order": 4
    },
    {
        "id": "tools-and-mcp",
        "title": "Tools and MCP Guide",
        "filename": "TOOLS_AND_MCP_GUIDE.md",
        "order": 5
    },
    {
        "id": "installation-guide",
        "title": "Installation Guide",
        "filename": "installation-guide.md",
        "order": 6
    },
    {
        "id": "example-simple-agent",
        "title": "Example: Simple Agent",
        "filename": "examples/simple_agent.py",
        "order": 7,
        "is_code": True
    },
    {
        "id": "example-file-storage",
        "title": "Example: File Storage",
        "filename": "examples/agent_with_file_storage.py",
        "order": 8,
        "is_code": True
    },
    {
        "id": "example-mcp",
        "title": "Example: MCP Integration",
        "filename": "examples/agent_with_mcp.py",
        "order": 9,
        "is_code": True
    },
    {
        "id": "example-multi-skills",
        "title": "Example: Multi-Skills Agent",
        "filename": "examples/agent_example_multi_skills.py",
        "order": 10,
        "is_code": True
    },
    {
        "id": "example-custom-framework",
        "title": "Example: Custom Framework",
        "filename": "examples/custom_framework_agent.py",
        "order": 11,
        "is_code": True
    }
]


class DocumentationGenerator:
    """Generates HTML documentation from Markdown files."""
    
    def __init__(self, docs_path: Optional[Path] = None):
        """
        Initialize the documentation generator.
        
        Args:
            docs_path: Path to the docs directory. If None, will auto-detect
                      using importlib.resources.
        """
        if docs_path is None:
            docs_path = self._find_docs_directory()
        
        self.docs_path = docs_path
        self.markdown_converter = markdown.Markdown(
            extensions=[
                'fenced_code',
                'tables',
                'toc',
                'codehilite',
                'nl2br'
            ]
        )
        logger.info(f"DocumentationGenerator initialized with docs_path: {self.docs_path}")
    
    def _find_docs_directory(self) -> Path:
        """
        Find the docs directory using importlib.resources.
        
        Returns:
            Path to docs directory (agent_framework/web/docs/)
        
        Raises:
            FileNotFoundError: If docs directory cannot be found
        """
        try:
            # Python 3.9+ approach: access package data
            import importlib.resources as pkg_resources
            
            # Get reference to agent_framework.web.docs
            docs_ref = pkg_resources.files('agent_framework.web').joinpath('docs')
            
            if docs_ref.is_dir():
                # Convert to Path (works for both filesystem and zip)
                return Path(str(docs_ref))
            
            raise FileNotFoundError(f"docs directory not found in package: {docs_ref}")
            
        except Exception as e:
            logger.critical(f"Failed to locate documentation directory: {e}")
            raise FileNotFoundError(
                f"Could not locate documentation directory in agent_framework.web.docs. "
                f"Error: {e}. "
                f"Please ensure the package is properly installed with documentation files."
            )
    
    def _read_markdown_file(self, filename: str) -> str:
        """
        Read a markdown file from docs directory.
        
        Args:
            filename: Name of the markdown file to read
            
        Returns:
            Content of the markdown file as string
            
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If the file exceeds size limit
        """
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        
        file_path = self.docs_path / filename
        
        if not file_path.exists():
            logger.error(f"Documentation file not found: {filename}")
            raise FileNotFoundError(f"Documentation file '{filename}' not found at {file_path}")
        
        # Check file size
        file_size = file_path.stat().st_size
        if file_size > MAX_FILE_SIZE:
            logger.warning(f"File {filename} exceeds size limit: {file_size} bytes")
            raise ValueError(f"File '{filename}' is too large to display ({file_size} bytes > {MAX_FILE_SIZE} bytes)")
        
        # Read file with UTF-8 encoding
        try:
            content = file_path.read_text(encoding='utf-8')
            logger.debug(f"Successfully read file {filename} ({file_size} bytes)")
            return content
        except UnicodeDecodeError as e:
            logger.error(f"Failed to decode file {filename} as UTF-8: {e}")
            raise ValueError(f"File '{filename}' contains invalid UTF-8 encoding")
    
    def _convert_markdown_to_html(self, markdown_content: str) -> str:
        """
        Convert markdown content to HTML.
        
        Args:
            markdown_content: Markdown content as string
            
        Returns:
            HTML content as string
            
        Raises:
            ValueError: If conversion fails
        """
        try:
            # Reset the markdown converter to clear any previous state
            self.markdown_converter.reset()
            
            # Convert markdown to HTML
            html_content = self.markdown_converter.convert(markdown_content)
            
            logger.debug(f"Successfully converted markdown to HTML ({len(html_content)} chars)")
            return html_content
            
        except Exception as e:
            logger.error(f"Failed to convert markdown to HTML: {e}")
            raise ValueError(f"Markdown conversion failed: {e}")
    
    def _convert_code_to_html(self, code_content: str, language: str = "python") -> str:
        """
        Convert code content to HTML with syntax highlighting.
        
        Args:
            code_content: Code content as string
            language: Programming language for syntax highlighting
            
        Returns:
            HTML content as string with code block
        """
        # Escape HTML special characters
        import html
        escaped_code = html.escape(code_content)
        
        # Wrap in pre/code tags with language class for Prism.js
        html_content = f'<pre><code class="language-{language}">{escaped_code}</code></pre>'
        
        logger.debug(f"Successfully converted code to HTML ({len(html_content)} chars)")
        return html_content
    
    def _generate_navigation(self, sections: List[Dict]) -> str:
        """
        Generate navigation menu HTML.
        
        Args:
            sections: List of section dictionaries with 'id', 'title', and 'order' keys
            
        Returns:
            HTML string for navigation menu
        """
        # Sort sections by order
        sorted_sections = sorted(sections, key=lambda s: s['order'])
        
        nav_items = []
        for section in sorted_sections:
            section_id = section['id']
            section_title = section['title']
            nav_items.append(f'<a href="#{section_id}" class="nav-link">{section_title}</a>')
        
        nav_html = '\n'.join(nav_items)
        
        logger.debug(f"Generated navigation with {len(sorted_sections)} links")
        return nav_html
    
    def _generate_section_html(self, section: Dict) -> str:
        """
        Generate HTML for a documentation section.
        
        Args:
            section: Dictionary with 'id', 'title', and 'content' keys
            
        Returns:
            HTML string for the section
        """
        section_id = section['id']
        section_title = section['title']
        section_content = section['content']
        
        # Add an anchor div at the very top of the section to ensure navigation works
        # This prevents conflicts with auto-generated IDs from markdown headers
        section_html = f'''
        <div id="{section_id}" class="section-anchor"></div>
        <section class="doc-section">
            <h1 class="section-title">{section_title}</h1>
            <div class="section-content">
                {section_content}
            </div>
        </section>
        '''
        
        logger.debug(f"Generated section HTML for '{section_title}'")
        return section_html
    
    def generate_documentation_html(self) -> str:
        """
        Generate complete documentation HTML.
        
        Returns:
            Complete HTML string with all documentation
            
        Raises:
            FileNotFoundError: If documentation files cannot be found
            ValueError: If markdown conversion fails
        """
        logger.info("Generating complete documentation HTML")
        
        # Read and convert all documentation files
        sections_with_content = []
        for section_config in DOCUMENTATION_SECTIONS:
            try:
                # Read file content
                file_content = self._read_markdown_file(section_config['filename'])
                
                # Check if this is a code file
                is_code = section_config.get('is_code', False)
                
                # Convert to HTML
                if is_code:
                    html_content = self._convert_code_to_html(file_content, language="python")
                else:
                    html_content = self._convert_markdown_to_html(file_content)
                
                # Add to sections list
                sections_with_content.append({
                    'id': section_config['id'],
                    'title': section_config['title'],
                    'order': section_config['order'],
                    'content': html_content
                })
                
                logger.debug(f"Processed section: {section_config['title']}")
                
            except FileNotFoundError as e:
                # Log error and create placeholder section
                logger.error(f"Documentation file not found: {section_config['filename']}")
                error_content = f"<p><strong>Error:</strong> Documentation file '{section_config['filename']}' not found.</p>"
                sections_with_content.append({
                    'id': section_config['id'],
                    'title': section_config['title'],
                    'order': section_config['order'],
                    'content': error_content
                })
            except Exception as e:
                # Log error and create placeholder section
                logger.error(f"Error processing {section_config['filename']}: {e}")
                error_content = f"<p><strong>Error:</strong> Failed to process '{section_config['filename']}': {e}</p>"
                sections_with_content.append({
                    'id': section_config['id'],
                    'title': section_config['title'],
                    'order': section_config['order'],
                    'content': error_content
                })
        
        # Generate navigation
        navigation_html = self._generate_navigation(sections_with_content)
        
        # Generate section HTML
        sections_html = '\n'.join([
            self._generate_section_html(section) 
            for section in sorted(sections_with_content, key=lambda s: s['order'])
        ])
        
        # Combine into complete HTML document
        complete_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agent Framework Documentation</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            display: flex;
            min-height: 100vh;
        }}
        
        .sidebar {{
            width: 250px;
            background-color: #2c3e50;
            color: white;
            padding: 2rem 1rem;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }}
        
        .sidebar h2 {{
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
            color: #ecf0f1;
        }}
        
        .nav-link {{
            display: block;
            padding: 0.75rem 1rem;
            color: #ecf0f1;
            text-decoration: none;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            transition: background-color 0.2s;
        }}
        
        .nav-link:hover {{
            background-color: #34495e;
        }}
        
        .nav-link.active {{
            background-color: #3498db;
        }}
        
        .content {{
            margin-left: 250px;
            flex: 1;
            padding: 2rem;
            max-width: 1200px;
        }}
        
        .section-anchor {{
            display: block;
            position: relative;
            top: -80px;
            visibility: hidden;
        }}
        
        .doc-section {{
            background-color: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .section-title {{
            color: #2c3e50;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #3498db;
        }}
        
        .section-content h1,
        .section-content h2,
        .section-content h3,
        .section-content h4,
        .section-content h5,
        .section-content h6 {{
            color: #2c3e50;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        .section-content h1 {{ font-size: 2rem; }}
        .section-content h2 {{ font-size: 1.75rem; }}
        .section-content h3 {{ font-size: 1.5rem; }}
        .section-content h4 {{ font-size: 1.25rem; }}
        .section-content h5 {{ font-size: 1.1rem; }}
        .section-content h6 {{ font-size: 1rem; }}
        
        .section-content p {{
            margin-bottom: 1rem;
        }}
        
        .section-content ul,
        .section-content ol {{
            margin-bottom: 1rem;
            padding-left: 2rem;
        }}
        
        .section-content li {{
            margin-bottom: 0.5rem;
        }}
        
        .section-content a {{
            color: #3498db;
            text-decoration: none;
        }}
        
        .section-content a:hover {{
            text-decoration: underline;
        }}
        
        .section-content code {{
            background-color: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9em;
        }}
        
        .section-content pre {{
            background-color: #2d2d2d;
            color: #f8f8f2;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
            margin-bottom: 1rem;
        }}
        
        .section-content pre code {{
            background-color: transparent;
            padding: 0;
            color: inherit;
        }}
        
        .section-content table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
        }}
        
        .section-content table th,
        .section-content table td {{
            padding: 0.75rem;
            border: 1px solid #ddd;
            text-align: left;
        }}
        
        .section-content table th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        
        .section-content table tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        .section-content blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 1rem;
            margin: 1rem 0;
            color: #555;
            font-style: italic;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .sidebar {{
                width: 100%;
                position: relative;
                height: auto;
            }}
            
            .content {{
                margin-left: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="sidebar">
            <h2>Documentation</h2>
            {navigation_html}
        </nav>
        <main class="content">
            {sections_html}
        </main>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>
    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('.nav-link').forEach(link => {{
            link.addEventListener('click', function(e) {{
                e.preventDefault();
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {{
                    // Scroll to the anchor element
                    targetElement.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    
                    // Update active link
                    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Update URL hash without jumping
                    history.pushState(null, null, '#' + targetId);
                }}
            }});
        }});
        
        // Highlight active section on scroll
        let ticking = false;
        window.addEventListener('scroll', function() {{
            if (!ticking) {{
                window.requestAnimationFrame(function() {{
                    const anchors = document.querySelectorAll('.section-anchor');
                    const navLinks = document.querySelectorAll('.nav-link');
                    
                    let currentSection = '';
                    anchors.forEach(anchor => {{
                        const rect = anchor.getBoundingClientRect();
                        // Check if anchor is in viewport (with some offset for better UX)
                        if (rect.top <= 150 && rect.top >= -window.innerHeight) {{
                            currentSection = anchor.getAttribute('id');
                        }}
                    }});
                    
                    // Update active nav link
                    navLinks.forEach(link => {{
                        link.classList.remove('active');
                        if (link.getAttribute('href') === '#' + currentSection) {{
                            link.classList.add('active');
                        }}
                    }});
                    
                    ticking = false;
                }});
                ticking = true;
            }}
        }});
        
        // Set initial active link based on URL hash
        window.addEventListener('load', function() {{
            const hash = window.location.hash;
            if (hash) {{
                const targetLink = document.querySelector('.nav-link[href="' + hash + '"]');
                if (targetLink) {{
                    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                    targetLink.classList.add('active');
                }}
            }} else {{
                // Set first link as active by default
                const firstLink = document.querySelector('.nav-link');
                if (firstLink) {{
                    firstLink.classList.add('active');
                }}
            }}
        }});
    </script>
</body>
</html>'''
        
        logger.info(f"Generated complete documentation HTML ({len(complete_html)} chars)")
        return complete_html
