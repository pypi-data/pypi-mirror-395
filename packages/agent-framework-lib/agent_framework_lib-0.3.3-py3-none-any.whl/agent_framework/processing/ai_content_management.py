"""
AI-Generated Content Detection and Storage

This module provides comprehensive detection and storage of AI-generated content
from agent responses, including text, code, charts, and other structured content.

Components:
- GeneratedContentDetector: Pattern matching and content extraction
- AIContentManager: Automatic processing and storage of detected content
- Content routing and backend separation for AI-generated content

v 0.1.0 - Initial implementation
"""

import re
import json
import uuid
import logging
import os
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


try:
    from agent_framework.core.agent_interface import StructuredAgentOutput
except ImportError:
    # For direct module testing
    from agent_interface import StructuredAgentOutput

logger = logging.getLogger(__name__)


class ContentType(Enum):
    """Types of AI-generated content that can be detected"""
    HTML = "html"
    MARKDOWN = "markdown"
    CHART_JS = "chartjs"
    MERMAID = "mermaid"
    CODE = "code"
    JSON = "json"
    CSV = "csv"
    YAML = "yaml"
    XML = "xml"
    STRUCTURED_DATA = "structured_data"
    FORM = "form"
    OPTIONS_BLOCK = "options_block"


@dataclass
class DetectedContent:
    """Represents a piece of detected AI-generated content"""
    content_type: ContentType
    content: str
    language: Optional[str] = None  # For code blocks
    metadata: Dict[str, Any] = None
    confidence: float = 1.0
    start_position: int = 0
    end_position: int = 0
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class GeneratedContentDetector:
    """
    Detects and extracts generated content from agent responses.
    
    Supports pattern matching for:
    - HTML content in code blocks
    - Markdown content in code blocks
    - Chart.js configurations
    - Mermaid diagrams
    - Code blocks with various languages
    - Structured output parts (charts, forms, options blocks)
    """
    
    def __init__(self):
        """Initialize the content detector with pattern definitions"""
        
        # Code block patterns with language detection
        self.code_block_patterns = {
            ContentType.HTML: [
                r'```html\s*\n(.*?)\n```',
                r'```htm\s*\n(.*?)\n```'
            ],
            ContentType.MARKDOWN: [
                r'```markdown\s*\n(.*?)\n```',
                r'```md\s*\n(.*?)\n```'
            ],
            ContentType.MERMAID: [
                r'```mermaid\s*\n(.*?)\n```'
            ],
            ContentType.JSON: [
                r'```json\s*\n(.*?)\n```'
            ],
            ContentType.CSV: [
                r'```csv\s*\n(.*?)\n```'
            ],
            ContentType.YAML: [
                r'```yaml\s*\n(.*?)\n```',
                r'```yml\s*\n(.*?)\n```'
            ],
            ContentType.XML: [
                r'```xml\s*\n(.*?)\n```'
            ]
        }
        
        # Generic code block pattern for any language
        self.generic_code_pattern = r'```(\w+)\s*\n(.*?)\n```'
        
        # Chart.js specific patterns
        self.chartjs_patterns = [
            r'```json\s*\n(.*?"type":\s*"(?:bar|line|pie|doughnut|radar|polarArea|bubble|scatter)".*?)\n```',
            r'```javascript\s*\n(.*?new\s+Chart\(.*?)\n```',
            r'```js\s*\n(.*?new\s+Chart\(.*?)\n```'
        ]
        
        # Structured content patterns (outside code blocks)
        self.structured_patterns = {
            ContentType.STRUCTURED_DATA: [
                r'<data[^>]*>(.*?)</data>',
                r'<table[^>]*>(.*?)</table>',
                r'\|[^|\n]*\|[^|\n]*\|'  # Simple table detection
            ],
            ContentType.FORM: [
                r'<form[^>]*>(.*?)</form>',
                r'<input[^>]*>',
                r'<select[^>]*>(.*?)</select>',
                r'<textarea[^>]*>(.*?)</textarea>'
            ]
        }
        
        # Options block patterns (for multiple choice, lists, etc.)
        self.options_patterns = [
            r'(?:^|\n)(?:\d+\.|[a-zA-Z]\.|[-*+])\s+(.+?)(?=\n(?:\d+\.|[a-zA-Z]\.|[-*+]|\n)|$)',
            r'(?:^|\n)(?:Option\s+\w+:|Choice\s+\w+:)\s*(.+?)(?=\n(?:Option|Choice|\n)|$)'
        ]
    
    async def detect_generated_content(self, response_text: str) -> List[DetectedContent]:
        """
        Detect various types of generated content in agent response text.
        
        Args:
            response_text: The text content from agent response
            
        Returns:
            List of DetectedContent objects representing found content
        """
        detected_content = []
        
        if not response_text:
            return detected_content
        
        # Detect code blocks with specific languages
        detected_content.extend(await self._detect_code_blocks(response_text))
        
        # Detect Chart.js content specifically
        detected_content.extend(await self._detect_chartjs_content(response_text))
        
        # Detect structured content outside code blocks
        detected_content.extend(await self._detect_structured_content(response_text))
        
        # Detect options blocks and lists
        detected_content.extend(await self._detect_options_blocks(response_text))
        
        # Sort by position to maintain order
        detected_content.sort(key=lambda x: x.start_position)
        
        logger.info(f"Detected {len(detected_content)} pieces of generated content")
        return detected_content
    
    async def extract_structured_content(self, agent_output: StructuredAgentOutput) -> List[DetectedContent]:
        """
        Extract content from structured output parts (charts, forms, options blocks).
        
        Args:
            agent_output: The structured agent output containing parts
            
        Returns:
            List of DetectedContent objects from structured parts
        """
        detected_content = []
        
        if not agent_output.parts:
            return detected_content
        
        for i, part in enumerate(agent_output.parts):
            try:
                # Extract content based on part type
                if hasattr(part, 'chart_config') and part.chart_config:
                    # Chart part
                    content = DetectedContent(
                        content_type=ContentType.CHART_JS,
                        content=json.dumps(part.chart_config, indent=2),
                        metadata={
                            'part_index': i,
                            'part_type': 'chart',
                            'chart_type': part.chart_config.get('type', 'unknown')
                        }
                    )
                    detected_content.append(content)
                
                elif hasattr(part, 'form_config') and part.form_config:
                    # Form part
                    content = DetectedContent(
                        content_type=ContentType.FORM,
                        content=json.dumps(part.form_config, indent=2),
                        metadata={
                            'part_index': i,
                            'part_type': 'form',
                            'form_fields': len(part.form_config.get('fields', []))
                        }
                    )
                    detected_content.append(content)
                
                elif hasattr(part, 'options') and part.options:
                    # Options part
                    options_text = '\n'.join([f"- {opt}" for opt in part.options])
                    content = DetectedContent(
                        content_type=ContentType.OPTIONS_BLOCK,
                        content=options_text,
                        metadata={
                            'part_index': i,
                            'part_type': 'options',
                            'option_count': len(part.options)
                        }
                    )
                    detected_content.append(content)
                
                elif hasattr(part, 'data') and part.data:
                    # Generic data part
                    content = DetectedContent(
                        content_type=ContentType.STRUCTURED_DATA,
                        content=json.dumps(part.data, indent=2) if isinstance(part.data, dict) else str(part.data),
                        metadata={
                            'part_index': i,
                            'part_type': 'data',
                            'data_type': type(part.data).__name__
                        }
                    )
                    detected_content.append(content)
                
            except Exception as e:
                logger.warning(f"Error extracting content from part {i}: {e}")
                continue
        
        logger.info(f"Extracted {len(detected_content)} pieces of structured content")
        return detected_content
    
    async def _detect_code_blocks(self, text: str) -> List[DetectedContent]:
        """Detect code blocks with specific languages"""
        detected = []
        
        # Check specific language patterns
        for content_type, patterns in self.code_block_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    content = DetectedContent(
                        content_type=content_type,
                        content=match.group(1).strip(),
                        language=content_type.value,
                        start_position=match.start(),
                        end_position=match.end(),
                        metadata={
                            'pattern_matched': pattern,
                            'block_type': 'code_block'
                        }
                    )
                    detected.append(content)
        
        # Check generic code blocks for other languages
        matches = re.finditer(self.generic_code_pattern, text, re.DOTALL | re.IGNORECASE)
        for match in matches:
            language = match.group(1).lower()
            code_content = match.group(2).strip()
            
            # Skip if already detected by specific patterns
            if any(d.start_position == match.start() for d in detected):
                continue
            
            content = DetectedContent(
                content_type=ContentType.CODE,
                content=code_content,
                language=language,
                start_position=match.start(),
                end_position=match.end(),
                metadata={
                    'pattern_matched': self.generic_code_pattern,
                    'block_type': 'code_block',
                    'detected_language': language
                }
            )
            detected.append(content)
        
        return detected
    
    async def _detect_chartjs_content(self, text: str) -> List[DetectedContent]:
        """Detect Chart.js specific content"""
        detected = []
        
        for pattern in self.chartjs_patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                chart_content = match.group(1).strip()
                
                # Try to parse as JSON to validate Chart.js config
                try:
                    if 'new Chart(' in chart_content:
                        # JavaScript Chart.js code
                        chart_type = 'javascript'
                    else:
                        # JSON Chart.js config
                        json.loads(chart_content)
                        chart_type = 'json'
                    
                    content = DetectedContent(
                        content_type=ContentType.CHART_JS,
                        content=chart_content,
                        language=chart_type,
                        start_position=match.start(),
                        end_position=match.end(),
                        metadata={
                            'pattern_matched': pattern,
                            'chart_format': chart_type,
                            'block_type': 'chartjs'
                        }
                    )
                    detected.append(content)
                    
                except json.JSONDecodeError:
                    # Not valid JSON, but might still be Chart.js code
                    if 'chart' in chart_content.lower() or 'type' in chart_content.lower():
                        content = DetectedContent(
                            content_type=ContentType.CHART_JS,
                            content=chart_content,
                            language='javascript',
                            start_position=match.start(),
                            end_position=match.end(),
                            confidence=0.7,  # Lower confidence for non-JSON
                            metadata={
                                'pattern_matched': pattern,
                                'chart_format': 'javascript',
                                'block_type': 'chartjs',
                                'validation_warning': 'Not valid JSON'
                            }
                        )
                        detected.append(content)
        
        return detected
    
    async def _detect_structured_content(self, text: str) -> List[DetectedContent]:
        """Detect structured content outside code blocks"""
        detected = []
        
        for content_type, patterns in self.structured_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    content = DetectedContent(
                        content_type=content_type,
                        content=match.group(0).strip(),
                        start_position=match.start(),
                        end_position=match.end(),
                        metadata={
                            'pattern_matched': pattern,
                            'block_type': 'structured_content'
                        }
                    )
                    detected.append(content)
        
        return detected
    
    async def _detect_options_blocks(self, text: str) -> List[DetectedContent]:
        """Detect options blocks and lists"""
        detected = []
        
        for pattern in self.options_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
            
            # Group consecutive matches as a single options block
            current_block = []
            last_end = -1
            
            for match in matches:
                if match.start() - last_end > 50:  # New block if gap > 50 chars
                    if current_block:
                        # Save previous block
                        block_content = '\n'.join(current_block)
                        content = DetectedContent(
                            content_type=ContentType.OPTIONS_BLOCK,
                            content=block_content,
                            metadata={
                                'pattern_matched': pattern,
                                'block_type': 'options_block',
                                'option_count': len(current_block)
                            }
                        )
                        detected.append(content)
                    
                    current_block = [match.group(1).strip()]
                else:
                    current_block.append(match.group(1).strip())
                
                last_end = match.end()
            
            # Save final block
            if current_block:
                block_content = '\n'.join(current_block)
                content = DetectedContent(
                    content_type=ContentType.OPTIONS_BLOCK,
                    content=block_content,
                    metadata={
                        'pattern_matched': pattern,
                        'block_type': 'options_block',
                        'option_count': len(current_block)
                    }
                )
                detected.append(content)
        
        return detected
    
    def classify_content(self, content: str, content_type: ContentType) -> Dict[str, Any]:
        """
        Classify and analyze detected content for additional metadata.
        
        Args:
            content: The detected content string
            content_type: The type of content detected
            
        Returns:
            Dictionary with classification results and metadata
        """
        classification = {
            'content_type': content_type.value,
            'size_bytes': len(content.encode('utf-8')),
            'line_count': len(content.split('\n')),
            'complexity_score': 0.0,
            'features': []
        }
        
        try:
            if content_type == ContentType.HTML:
                # Analyze HTML content
                tag_count = len(re.findall(r'<[^>]+>', content))
                classification.update({
                    'complexity_score': min(tag_count / 10.0, 1.0),
                    'features': ['html_tags', 'markup'],
                    'tag_count': tag_count
                })
                
                if 'script' in content.lower():
                    classification['features'].append('javascript')
                if 'style' in content.lower() or 'css' in content.lower():
                    classification['features'].append('css')
            
            elif content_type == ContentType.CHART_JS:
                # Analyze Chart.js content
                if 'type' in content:
                    chart_type_match = re.search(r'"type":\s*"([^"]+)"', content)
                    if chart_type_match:
                        classification['chart_type'] = chart_type_match.group(1)
                        classification['features'].append(f"chart_{chart_type_match.group(1)}")
                
                data_points = len(re.findall(r'"data":', content))
                classification.update({
                    'complexity_score': min(data_points / 5.0, 1.0),
                    'features': classification['features'] + ['visualization', 'interactive'],
                    'data_sections': data_points
                })
            
            elif content_type == ContentType.CODE:
                # Analyze code content
                function_count = len(re.findall(r'def |function |class ', content))
                import_count = len(re.findall(r'import |from |#include', content))
                classification.update({
                    'complexity_score': min((function_count + import_count) / 10.0, 1.0),
                    'features': ['executable', 'programming'],
                    'function_count': function_count,
                    'import_count': import_count
                })
            
            elif content_type == ContentType.MERMAID:
                # Analyze Mermaid diagrams
                diagram_type = 'unknown'
                if 'graph' in content.lower():
                    diagram_type = 'graph'
                elif 'sequenceDiagram' in content:
                    diagram_type = 'sequence'
                elif 'classDiagram' in content:
                    diagram_type = 'class'
                elif 'flowchart' in content.lower():
                    diagram_type = 'flowchart'
                
                node_count = len(re.findall(r'-->', content)) + len(re.findall(r'---', content))
                classification.update({
                    'complexity_score': min(node_count / 20.0, 1.0),
                    'features': ['diagram', 'visualization'],
                    'diagram_type': diagram_type,
                    'node_count': node_count
                })
            
        except Exception as e:
            logger.warning(f"Error classifying content: {e}")
            classification['classification_error'] = str(e)
        
        return classification


class AIContentManager:
    """
    Manages AI-generated content storage and lifecycle.
    
    Automatically processes agent responses to detect generated content,
    stores it with proper tagging and metadata, and associates it with
    sessions and users.
    """
    
    def __init__(self, file_storage_manager):
        """
        Initialize the AI content manager.
        
        Args:
            file_storage_manager: FileStorageManager instance for content storage
        """
        self.file_storage_manager = file_storage_manager
        self.detector = GeneratedContentDetector()
        
        # Content type to file extension mapping
        self.content_extensions = {
            ContentType.HTML: '.html',
            ContentType.MARKDOWN: '.md',
            ContentType.CHART_JS: '.json',
            ContentType.MERMAID: '.mmd',
            ContentType.CODE: '.txt',  # Will be updated based on language
            ContentType.JSON: '.json',
            ContentType.CSV: '.csv',
            ContentType.YAML: '.yaml',
            ContentType.XML: '.xml',
            ContentType.STRUCTURED_DATA: '.json',
            ContentType.FORM: '.html',
            ContentType.OPTIONS_BLOCK: '.txt'
        }
        
        # Language-specific extensions for code
        self.language_extensions = {
            'python': '.py',
            'javascript': '.js',
            'typescript': '.ts',
            'java': '.java',
            'cpp': '.cpp',
            'c': '.c',
            'csharp': '.cs',
            'php': '.php',
            'ruby': '.rb',
            'go': '.go',
            'rust': '.rs',
            'sql': '.sql',
            'bash': '.sh',
            'shell': '.sh',
            'powershell': '.ps1'
        }
    
    async def process_agent_response(self, 
                                   agent_output: StructuredAgentOutput, 
                                   session_id: str, 
                                   user_id: str,
                                   agent_id: Optional[str] = None) -> StructuredAgentOutput:
        """
        Process agent response and automatically store generated content.
        
        Args:
            agent_output: The structured agent output to process
            session_id: Session ID for content association
            user_id: User ID for content association
            agent_id: Optional agent ID for content association
            
        Returns:
            Modified StructuredAgentOutput with file references added
        """
        try:
            # Detect content in response text
            text_content = []
            if agent_output.response_text:
                text_content = await self.detector.detect_generated_content(agent_output.response_text)
            
            # Extract content from structured parts
            structured_content = await self.detector.extract_structured_content(agent_output)
            
            # Combine all detected content
            all_content = text_content + structured_content
            
            if not all_content:
                logger.debug("No AI-generated content detected in agent response")
                return agent_output
            
            # Store detected content and update response with file references
            return await self._store_and_reference_content(
                agent_output, all_content, session_id, user_id, agent_id
            )
            
        except Exception as e:
            logger.error(f"Error processing agent response for AI content: {e}")
            # Return original output if processing fails
            return agent_output
    
    async def store_generated_content(self, 
                                    content: Union[str, bytes], 
                                    content_type: ContentType,
                                    filename: str,
                                    session_id: str, 
                                    user_id: str,
                                    agent_id: Optional[str] = None,
                                    metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store AI-generated content with proper routing and metadata.
        
        Args:
            content: The content to store (string or bytes)
            content_type: Type of the generated content
            filename: Filename for the stored content
            session_id: Session ID for content association
            user_id: User ID for content association
            agent_id: Optional agent ID for content association
            metadata: Additional metadata for the content
            
        Returns:
            File ID of the stored content
        """
        try:
            # Convert content to bytes if needed
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = content
            
            # Determine MIME type and routing
            mime_type, backend_hint = self._get_content_mime_type_and_backend(content_type)
            
            # Prepare metadata with content type for enhanced routing
            storage_metadata = {
                'ai_generated': True,
                'content_type': content_type.value,  # This will be used by enhanced routing
                'generation_timestamp': datetime.now().isoformat(),
                'detection_method': 'automatic',
                'routing_hint': f"ai-generated/{content_type.value}",
                **(metadata or {})
            }
            
            # Add classification metadata
            classification = self.detector.classify_content(
                content if isinstance(content, str) else content.decode('utf-8', errors='ignore'),
                content_type
            )
            storage_metadata['classification'] = classification
            
            # Store the file with AI-generated routing
            # The enhanced _determine_backend will use is_generated=True and content_type from metadata
            file_id = await self.file_storage_manager.store_file(
                content=content_bytes,
                filename=filename,
                user_id=user_id,
                session_id=session_id,
                agent_id=agent_id,
                mime_type=mime_type,
                is_generated=True,  # This triggers AI content routing
                tags=["ai-generated", "auto-stored", content_type.value],
                custom_metadata=storage_metadata,
                backend_name=backend_hint  # Fallback if routing doesn't find a match
            )
            
            logger.info(f"✅ Stored AI-generated {content_type.value} content: {filename} (ID: {file_id})")
            return file_id
            
        except Exception as e:
            logger.error(f"❌ Failed to store AI-generated content {filename}: {e}")
            raise
    
    async def _store_and_reference_content(self, 
                                         agent_output: StructuredAgentOutput,
                                         detected_content: List[DetectedContent],
                                         session_id: str,
                                         user_id: str,
                                         agent_id: Optional[str] = None) -> StructuredAgentOutput:
        """Store detected content and add file references to the response"""
        
        stored_files = []
        response_additions = []
        
        for i, content in enumerate(detected_content):
            try:
                # Generate filename
                filename = self._generate_filename(content, i)
                
                # Store the content
                file_id = await self.store_generated_content(
                    content=content.content,
                    content_type=content.content_type,
                    filename=filename,
                    session_id=session_id,
                    user_id=user_id,
                    agent_id=agent_id,
                    metadata={
                        'detection_confidence': content.confidence,
                        'detection_metadata': content.metadata,
                        'position_in_response': {
                            'start': content.start_position,
                            'end': content.end_position
                        }
                    }
                )
                
                stored_files.append({
                    'file_id': file_id,
                    'filename': filename,
                    'content_type': content.content_type.value,
                    'size_bytes': len(content.content.encode('utf-8'))
                })
                
                # Add reference to response
                response_additions.append(f"📁 Generated content stored: {filename} (ID: {file_id})")
                
            except Exception as e:
                logger.error(f"Failed to store detected content {i}: {e}")
                continue
        
        # Update the agent output with file references
        if stored_files:
            # Add summary to response text
            summary = f"\n\n🤖 **AI Content Auto-Stored ({len(stored_files)} files):**\n" + "\n".join(response_additions)
            
            updated_response_text = (agent_output.response_text or "") + summary
            
            # Create updated output
            updated_output = StructuredAgentOutput(
                response_text=updated_response_text,
                parts=agent_output.parts
            )
            
            logger.info(f"✅ Auto-stored {len(stored_files)} pieces of AI-generated content")
            return updated_output
        
        return agent_output
    
    def _generate_filename(self, content: DetectedContent, index: int) -> str:
        """Generate appropriate filename for detected content"""
        
        # Base filename with timestamp and index
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"ai_generated_{content.content_type.value}_{timestamp}_{index:03d}"
        
        # Get appropriate extension
        if content.content_type == ContentType.CODE and content.language:
            extension = self.language_extensions.get(content.language.lower(), '.txt')
        else:
            extension = self.content_extensions.get(content.content_type, '.txt')
        
        return base_name + extension
    
    def _get_content_mime_type_and_backend(self, content_type: ContentType) -> Tuple[str, Optional[str]]:
        """Get MIME type and suggested backend for content type"""
        
        mime_types = {
            ContentType.HTML: 'text/html',
            ContentType.MARKDOWN: 'text/markdown',
            ContentType.CHART_JS: 'application/json',
            ContentType.MERMAID: 'text/plain',
            ContentType.CODE: 'text/plain',
            ContentType.JSON: 'application/json',
            ContentType.CSV: 'text/csv',
            ContentType.YAML: 'text/yaml',
            ContentType.XML: 'text/xml',
            ContentType.STRUCTURED_DATA: 'application/json',
            ContentType.FORM: 'text/html',
            ContentType.OPTIONS_BLOCK: 'text/plain'
        }
        
        # Backend suggestions based on environment variables
        backend_hints = {
            ContentType.HTML: os.getenv("AI_HTML_STORAGE_BACKEND"),
            ContentType.CHART_JS: os.getenv("AI_CHART_STORAGE_BACKEND"),
            ContentType.CODE: os.getenv("AI_CODE_STORAGE_BACKEND"),
            ContentType.STRUCTURED_DATA: os.getenv("AI_DATA_STORAGE_BACKEND")
        }
        
        mime_type = mime_types.get(content_type, 'text/plain')
        backend_hint = backend_hints.get(content_type) or os.getenv("AI_CONTENT_STORAGE_BACKEND")
        
        return mime_type, backend_hint


# Enhanced routing configuration for AI-generated content
def configure_ai_content_routing(file_storage_manager):
    """
    Configure routing rules for AI-generated content separation.
    
    This function sets up routing rules to separate AI-generated content
    from user uploads based on environment configuration.
    
    Args:
        file_storage_manager: FileStorageManager instance to configure
    """
    
    # Default routing rules for AI content
    ai_routing_rules = {
        "ai-generated/text": os.getenv("AI_TEXT_STORAGE_BACKEND", "local"),
        "ai-generated/html": os.getenv("AI_HTML_STORAGE_BACKEND", "local"),
        "ai-generated/chart": os.getenv("AI_CHART_STORAGE_BACKEND", "s3"),
        "ai-generated/code": os.getenv("AI_CODE_STORAGE_BACKEND", "local"),
        "ai-generated/data": os.getenv("AI_DATA_STORAGE_BACKEND", "local"),
        "ai-generated/image": os.getenv("AI_IMAGE_STORAGE_BACKEND", "s3"),
        "ai-generated/markdown": os.getenv("AI_MARKDOWN_STORAGE_BACKEND", "local"),
        "ai-generated/json": os.getenv("AI_JSON_STORAGE_BACKEND", "local"),
        "ai-generated/csv": os.getenv("AI_CSV_STORAGE_BACKEND", "local"),
        "ai-generated/yaml": os.getenv("AI_YAML_STORAGE_BACKEND", "local"),
        "ai-generated/xml": os.getenv("AI_XML_STORAGE_BACKEND", "local")
    }
    
    # Apply routing rules if backends are available
    configured_rules = 0
    for route_prefix, backend_name in ai_routing_rules.items():
        if backend_name and backend_name in file_storage_manager.backends:
            try:
                file_storage_manager.add_routing_rule(route_prefix, backend_name)
                logger.info(f"✅ Added AI content routing rule: {route_prefix} -> {backend_name}")
                configured_rules += 1
            except Exception as e:
                logger.warning(f"Failed to add routing rule {route_prefix} -> {backend_name}: {e}")
        else:
            logger.debug(f"Skipping routing rule {route_prefix} -> {backend_name} (backend not available)")
    
    # Log current routing configuration
    logger.info(f"AI content routing configured with {configured_rules}/{len(ai_routing_rules)} rules")
    logger.debug(f"Available backends: {list(file_storage_manager.backends.keys())}")
    
    # Log AI-specific routing rules
    ai_rules = {k: v for k, v in file_storage_manager.routing_rules.items() if k.startswith("ai-generated/")}
    if ai_rules:
        logger.info(f"Active AI content routing rules: {ai_rules}")
    else:
        logger.warning("No AI content routing rules active - AI content will use default backend")


def get_ai_content_routing_status(file_storage_manager) -> Dict[str, Any]:
    """
    Get the current status of AI content routing configuration.
    
    Args:
        file_storage_manager: FileStorageManager instance to check
        
    Returns:
        Dictionary with routing status information
    """
    
    # Check which AI routing rules are active
    ai_rules = {k: v for k, v in file_storage_manager.routing_rules.items() if k.startswith("ai-generated/")}
    
    # Check environment configuration
    env_config = {
        "AI_TEXT_STORAGE_BACKEND": os.getenv("AI_TEXT_STORAGE_BACKEND"),
        "AI_HTML_STORAGE_BACKEND": os.getenv("AI_HTML_STORAGE_BACKEND"),
        "AI_CHART_STORAGE_BACKEND": os.getenv("AI_CHART_STORAGE_BACKEND"),
        "AI_CODE_STORAGE_BACKEND": os.getenv("AI_CODE_STORAGE_BACKEND"),
        "AI_DATA_STORAGE_BACKEND": os.getenv("AI_DATA_STORAGE_BACKEND"),
        "AI_IMAGE_STORAGE_BACKEND": os.getenv("AI_IMAGE_STORAGE_BACKEND"),
        "AI_MARKDOWN_STORAGE_BACKEND": os.getenv("AI_MARKDOWN_STORAGE_BACKEND"),
        "AI_JSON_STORAGE_BACKEND": os.getenv("AI_JSON_STORAGE_BACKEND"),
        "AI_CSV_STORAGE_BACKEND": os.getenv("AI_CSV_STORAGE_BACKEND"),
        "AI_YAML_STORAGE_BACKEND": os.getenv("AI_YAML_STORAGE_BACKEND"),
        "AI_XML_STORAGE_BACKEND": os.getenv("AI_XML_STORAGE_BACKEND")
    }
    
    # Filter out None values
    env_config = {k: v for k, v in env_config.items() if v is not None}
    
    return {
        "ai_routing_enabled": len(ai_rules) > 0,
        "active_ai_rules": ai_rules,
        "environment_config": env_config,
        "available_backends": list(file_storage_manager.backends.keys()),
        "default_backend": file_storage_manager.default_backend,
        "total_routing_rules": len(file_storage_manager.routing_rules),
        "ai_routing_rules_count": len(ai_rules)
    }


# Utility functions for AI content management
async def process_agent_output_for_ai_content(agent_output: StructuredAgentOutput,
                                            file_storage_manager,
                                            session_id: str,
                                            user_id: str,
                                            agent_id: Optional[str] = None) -> StructuredAgentOutput:
    """
    Utility function to process agent output for AI-generated content.
    
    This is a convenience function that can be used by agents to automatically
    detect and store AI-generated content from their responses.
    
    Args:
        agent_output: The agent output to process
        file_storage_manager: FileStorageManager instance
        session_id: Session ID for content association
        user_id: User ID for content association
        agent_id: Optional agent ID for content association
        
    Returns:
        Modified agent output with AI content stored and referenced
    """
    
    if not file_storage_manager:
        logger.warning("No file storage manager provided, skipping AI content processing")
        return agent_output
    
    try:
        # Create AI content manager
        ai_content_manager = AIContentManager(file_storage_manager)
        
        # Process the agent output
        return await ai_content_manager.process_agent_response(
            agent_output, session_id, user_id, agent_id
        )
        
    except Exception as e:
        logger.error(f"Error processing agent output for AI content: {e}")
        return agent_output


# Export main classes and functions
__all__ = [
    'ContentType',
    'DetectedContent', 
    'GeneratedContentDetector',
    'AIContentManager',
    'configure_ai_content_routing',
    'get_ai_content_routing_status',
    'process_agent_output_for_ai_content'
]