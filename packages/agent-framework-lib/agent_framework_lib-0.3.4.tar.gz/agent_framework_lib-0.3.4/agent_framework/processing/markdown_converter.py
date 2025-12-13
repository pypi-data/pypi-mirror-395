"""
Markdown Conversion Module

Provides automatic conversion of various file formats to Markdown using the Markitdown library.
This module integrates with the file storage system to provide seamless markdown conversion.

Enhanced with comprehensive error handling, user-friendly feedback, and partial conversion support.

v 0.2.0 - Enhanced error handling and feedback
"""

import os
import logging
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from pathlib import Path
import tempfile
from enum import Enum
from dataclasses import dataclass, field

# Auto-configure PDF tools path
from agent_framework.utils.path_utils import PathDetector

# Import comprehensive error handling system
from agent_framework.monitoring.error_handling import (
    ErrorHandler,
    FileProcessingError,
    FileProcessingErrorType,
    ErrorSeverity,
    ConversionError,
    ProcessingIssue,
    ErrorHandlingResult,
    UserFeedbackGenerator
)

try:
    from markitdown import MarkItDown
    MARKITDOWN_AVAILABLE = True
    import markitdown
    MARKITDOWN_VERSION = getattr(markitdown, '__version__', 'unknown')
except ImportError:
    MARKITDOWN_AVAILABLE = False
    MARKITDOWN_VERSION = 'not_installed'
    logging.warning("Markitdown not available. Install with 'uv add markitdown'")

logger = logging.getLogger(__name__)


# ===== ENHANCED ERROR HANDLING CLASSES =====

class ConversionErrorType(Enum):
    """Types of conversion errors"""
    FORMAT_NOT_SUPPORTED = "format_not_supported"
    FILE_TOO_LARGE = "file_too_large"
    MARKITDOWN_NOT_AVAILABLE = "markitdown_not_available"
    CONVERSION_FAILED = "conversion_failed"
    EMPTY_RESULT = "empty_result"
    FILE_CORRUPTED = "file_corrupted"
    PERMISSION_ERROR = "permission_error"
    MEMORY_ERROR = "memory_error"
    TIMEOUT_ERROR = "timeout_error"


class ConversionSeverity(Enum):
    """Severity levels for conversion issues"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ConversionIssue:
    """Represents a conversion issue (error or warning)"""
    severity: ConversionSeverity
    error_type: ConversionErrorType
    message: str
    user_message: str
    suggestions: List[str] = field(default_factory=list)
    technical_details: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ConversionResult:
    """Enhanced result of markdown conversion attempt"""
    success: bool
    content: Optional[str] = None
    partial_content: Optional[str] = None  # Partial conversion if available
    issues: List[ConversionIssue] = field(default_factory=list)
    format_supported: bool = True
    conversion_time_ms: float = 0.0
    original_size_bytes: int = 0
    converted_size_chars: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def has_errors(self) -> bool:
        """Check if result has any errors"""
        return any(issue.severity == ConversionSeverity.ERROR for issue in self.issues)
    
    @property
    def has_warnings(self) -> bool:
        """Check if result has any warnings"""
        return any(issue.severity == ConversionSeverity.WARNING for issue in self.issues)
    
    @property
    def user_friendly_summary(self) -> str:
        """Generate user-friendly summary of conversion result"""
        if self.success:
            summary = f"✅ Successfully converted to markdown ({self.converted_size_chars:,} characters)"
            if self.has_warnings:
                warning_count = sum(1 for issue in self.issues if issue.severity == ConversionSeverity.WARNING)
                summary += f" with {warning_count} warning(s)"
        elif self.partial_content:
            summary = f"⚠️ Partial conversion completed ({len(self.partial_content):,} characters)"
        else:
            summary = "❌ Conversion failed"
        
        return summary
    
    def get_user_messages(self) -> List[str]:
        """Get all user-friendly messages from issues"""
        return [issue.user_message for issue in self.issues if issue.user_message]
    
    def get_suggestions(self) -> List[str]:
        """Get all suggestions from issues"""
        suggestions = []
        for issue in self.issues:
            suggestions.extend(issue.suggestions)
        return list(set(suggestions))  # Remove duplicates


class ConversionErrorHandler:
    """Handles conversion errors and generates user-friendly feedback"""
    
    ERROR_MESSAGES = {
        ConversionErrorType.FORMAT_NOT_SUPPORTED: {
            'message': "File format is not supported for markdown conversion",
            'user_message': "This file type cannot be converted to markdown",
            'suggestions': [
                "Try uploading a supported format (PDF, DOCX, TXT, HTML, etc.)",
                "The file will still be stored and available for download",
                "Consider converting the file manually to a supported format"
            ]
        },
        ConversionErrorType.FILE_TOO_LARGE: {
            'message': "File exceeds maximum size limit for conversion",
            'user_message': "File is too large to convert to markdown",
            'suggestions': [
                "Try splitting the file into smaller parts",
                "The original file is still stored and accessible",
                "Consider using a file compression tool"
            ]
        },
        ConversionErrorType.MARKITDOWN_NOT_AVAILABLE: {
            'message': "Markitdown library is not installed",
            'user_message': "Markdown conversion is not available on this system",
            'suggestions': [
                "Contact your administrator to install the markitdown library",
                "Files will still be stored in their original format",
                "You can download and convert files manually"
            ]
        },
        ConversionErrorType.CONVERSION_FAILED: {
            'message': "Conversion process failed due to an error",
            'user_message': "Failed to convert file to markdown",
            'suggestions': [
                "Check if the file is corrupted or password-protected",
                "Try uploading the file again",
                "The original file is still available for download"
            ]
        },
        ConversionErrorType.EMPTY_RESULT: {
            'message': "Conversion completed but produced no content",
            'user_message': "File appears to be empty or contains no extractable text",
            'suggestions': [
                "Check if the file contains readable content",
                "The file might be an image-only document (OCR not available)",
                "Try a different file format if possible"
            ]
        },
        ConversionErrorType.FILE_CORRUPTED: {
            'message': "File appears to be corrupted or unreadable",
            'user_message': "File seems to be damaged or corrupted",
            'suggestions': [
                "Try uploading the file again",
                "Check if you can open the file in its native application",
                "The file might have been corrupted during upload"
            ]
        },
        ConversionErrorType.PERMISSION_ERROR: {
            'message': "Permission denied while processing file",
            'user_message': "System permissions prevent file processing",
            'suggestions': [
                "Contact your administrator about file processing permissions",
                "The file is stored but cannot be converted",
                "Try again later"
            ]
        },
        ConversionErrorType.MEMORY_ERROR: {
            'message': "Insufficient memory to process file",
            'user_message': "File is too complex to process with available memory",
            'suggestions': [
                "Try a smaller or simpler file",
                "The original file is still stored and accessible",
                "Contact support if this persists"
            ]
        },
        ConversionErrorType.TIMEOUT_ERROR: {
            'message': "Conversion process timed out",
            'user_message': "File processing took too long and was cancelled",
            'suggestions': [
                "Try a smaller or simpler file",
                "The original file is still stored",
                "Contact support for complex document processing"
            ]
        }
    }
    
    @classmethod
    def create_issue(cls, 
                    error_type: ConversionErrorType, 
                    severity: ConversionSeverity = ConversionSeverity.ERROR,
                    technical_details: Optional[str] = None,
                    custom_suggestions: Optional[List[str]] = None) -> ConversionIssue:
        """Create a conversion issue with appropriate messaging"""
        
        error_info = cls.ERROR_MESSAGES.get(error_type, {
            'message': f"Unknown error: {error_type.value}",
            'user_message': "An unexpected error occurred during conversion",
            'suggestions': ["Try uploading the file again", "Contact support if the problem persists"]
        })
        
        suggestions = custom_suggestions or error_info['suggestions']
        
        return ConversionIssue(
            severity=severity,
            error_type=error_type,
            message=error_info['message'],
            user_message=error_info['user_message'],
            suggestions=suggestions,
            technical_details=technical_details
        )
    
    @classmethod
    def handle_exception(cls, 
                        exception: Exception, 
                        filename: str,
                        operation: str = "conversion") -> ConversionIssue:
        """Handle exceptions and convert to appropriate conversion issues"""
        
        exception_type = type(exception).__name__
        exception_message = str(exception)
        
        # Map common exceptions to error types
        if isinstance(exception, FileNotFoundError):
            error_type = ConversionErrorType.FILE_CORRUPTED
        elif isinstance(exception, PermissionError):
            error_type = ConversionErrorType.PERMISSION_ERROR
        elif isinstance(exception, MemoryError):
            error_type = ConversionErrorType.MEMORY_ERROR
        elif isinstance(exception, TimeoutError):
            error_type = ConversionErrorType.TIMEOUT_ERROR
        elif "corrupted" in exception_message.lower() or "invalid" in exception_message.lower():
            error_type = ConversionErrorType.FILE_CORRUPTED
        else:
            error_type = ConversionErrorType.CONVERSION_FAILED
        
        technical_details = f"{exception_type}: {exception_message} (during {operation} of {filename})"
        
        return cls.create_issue(
            error_type=error_type,
            severity=ConversionSeverity.ERROR,
            technical_details=technical_details
        )

# Debug log to track module loading
logger.info(f"🔧 MarkdownConverter module loaded - Markitdown available: {MARKITDOWN_AVAILABLE}, version: {MARKITDOWN_VERSION}")


class MarkdownConverter:
    """Enhanced markdown converter with comprehensive error handling and feedback"""
    
    # Supported MIME types for conversion with detailed information
    # Based on markitdown v0.1.0+ source code analysis
    SUPPORTED_MIME_TYPES = {
        # PDF Documents
        'application/pdf': {
            'name': 'PDF',
            'description': 'Portable Document Format',
            'typical_issues': ['Password-protected files', 'Image-only content', 'Complex layouts', 'Scanned documents without OCR']
        },
        'application/x-pdf': {
            'name': 'PDF',
            'description': 'PDF (alternative MIME type)',
            'typical_issues': ['Password-protected files', 'Image-only content', 'Complex layouts']
        },
        
        # Microsoft Word Documents
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': {
            'name': 'DOCX',
            'description': 'Microsoft Word Document (Office Open XML)',
            'typical_issues': ['Complex formatting', 'Embedded objects', 'Track changes', 'Comments', 'Headers/footers']
        },
        
        # Microsoft PowerPoint Presentations
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': {
            'name': 'PPTX',
            'description': 'Microsoft PowerPoint Presentation',
            'typical_issues': ['Slide layouts', 'Animations', 'Speaker notes', 'Embedded media', 'Complex graphics']
        },
        
        # Microsoft Excel Spreadsheets
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': {
            'name': 'XLSX',
            'description': 'Microsoft Excel Spreadsheet (Office Open XML)',
            'typical_issues': ['Multiple sheets', 'Formulas', 'Charts', 'Pivot tables', 'Macros']
        },
        'application/vnd.ms-excel': {
            'name': 'XLS',
            'description': 'Legacy Microsoft Excel Spreadsheet',
            'typical_issues': ['Older format compatibility', 'Complex formulas', 'Multiple worksheets', 'Charts']
        },
        
        # HTML and Web Content
        'text/html': {
            'name': 'HTML',
            'description': 'HyperText Markup Language',
            'typical_issues': ['Complex CSS styling', 'JavaScript content', 'External resources', 'Embedded media']
        },
        'application/xhtml+xml': {
            'name': 'XHTML',
            'description': 'XHTML Document',
            'typical_issues': ['XML namespaces', 'Strict formatting', 'External stylesheets']
        },
        
        # Plain Text and Markdown
        'text/plain': {
            'name': 'TXT',
            'description': 'Plain Text',
            'typical_issues': ['Encoding issues', 'Line ending differences', 'Character set problems']
        },
        'text/markdown': {
            'name': 'MD',
            'description': 'Markdown',
            'typical_issues': ['Already in markdown format', 'Dialect differences', 'Extension syntax']
        },
        'application/markdown': {
            'name': 'MD',
            'description': 'Markdown (alternative MIME type)',
            'typical_issues': ['Already in markdown format', 'Dialect differences']
        },
        
        # Structured Data Formats
        'application/json': {
            'name': 'JSON',
            'description': 'JavaScript Object Notation',
            'typical_issues': ['Complex nested structures', 'Large data sets', 'Binary data encoding']
        },
        'text/csv': {
            'name': 'CSV',
            'description': 'Comma-Separated Values',
            'typical_issues': ['Delimiter variations', 'Quoted fields', 'Encoding issues', 'Large datasets']
        },
        'application/csv': {
            'name': 'CSV',
            'description': 'CSV (alternative MIME type)',
            'typical_issues': ['Delimiter variations', 'Quoted fields', 'Encoding issues']
        },
        
        # XML Documents
        'application/xml': {
            'name': 'XML',
            'description': 'Extensible Markup Language',
            'typical_issues': ['Complex structure', 'Namespace issues', 'Schema validation', 'Large documents']
        },
        'text/xml': {
            'name': 'XML',
            'description': 'XML Text',
            'typical_issues': ['Complex structure', 'Namespace issues', 'Encoding declarations']
        },
        
        # Image Formats (with OCR and metadata extraction)
        'image/jpeg': {
            'name': 'JPEG',
            'description': 'JPEG Image',
            'typical_issues': ['OCR accuracy', 'Image quality', 'Text orientation', 'Handwritten text', 'Complex layouts']
        },
        'image/png': {
            'name': 'PNG',
            'description': 'PNG Image',
            'typical_issues': ['OCR accuracy', 'Transparent backgrounds', 'Text clarity', 'Complex graphics']
        },
        
        # Audio Formats (with transcription)
        'audio/x-wav': {
            'name': 'WAV',
            'description': 'WAV Audio',
            'typical_issues': ['Audio quality', 'Background noise', 'Multiple speakers', 'Accents', 'Technical terms']
        },
        'audio/mpeg': {
            'name': 'MP3',
            'description': 'MP3 Audio',
            'typical_issues': ['Compression artifacts', 'Audio quality', 'Speech recognition accuracy', 'Music vs speech']
        },
        'video/mp4': {
            'name': 'MP4',
            'description': 'MP4 Video (audio extraction)',
            'typical_issues': ['Audio track extraction', 'Video compression', 'Multiple audio tracks', 'Background noise']
        },
        
        # E-book Formats
        'application/epub+zip': {
            'name': 'EPUB',
            'description': 'Electronic Publication',
            'typical_issues': ['DRM protection', 'Complex layouts', 'Embedded fonts', 'Interactive elements', 'Multiple chapters']
        },
        'application/epub': {
            'name': 'EPUB',
            'description': 'EPUB E-book',
            'typical_issues': ['DRM protection', 'Complex layouts', 'Embedded media']
        },
        'application/x-epub+zip': {
            'name': 'EPUB',
            'description': 'EPUB (alternative MIME type)',
            'typical_issues': ['DRM protection', 'Complex layouts', 'Embedded media']
        },
        
        # Email Formats
        'application/vnd.ms-outlook': {
            'name': 'MSG',
            'description': 'Outlook Email Message',
            'typical_issues': ['Embedded attachments', 'Rich formatting', 'Email headers', 'Encrypted content', 'Embedded images']
        },
        
        # Archive Formats
        'application/zip': {
            'name': 'ZIP',
            'description': 'ZIP Archive',
            'typical_issues': ['Password protection', 'Large archives', 'Nested archives', 'Binary files', 'File extraction limits']
        },
        
        # Jupyter Notebooks
        'application/x-ipynb+json': {
            'name': 'IPYNB',
            'description': 'Jupyter Notebook',
            'typical_issues': ['Code execution output', 'Rich media outputs', 'Cell metadata', 'Kernel-specific content']
        },
        
        # Additional text formats supported by PlainTextConverter
        'text/': {  # Prefix match for all text/* MIME types
            'name': 'Text',
            'description': 'Generic Text Format',
            'typical_issues': ['Encoding detection', 'Character set issues', 'Line endings']
        }
    }
    
    def __init__(self, 
                 max_file_size_mb: int = 50,
                 conversion_timeout_seconds: int = 300,
                 enable_partial_conversion: bool = True):
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024
        self.conversion_timeout_seconds = conversion_timeout_seconds
        self.enable_partial_conversion = enable_partial_conversion
        
        if not MARKITDOWN_AVAILABLE:
            logger.warning("Markitdown not available - conversion will be disabled")
        else:
            logger.info(f"✅ MarkdownConverter initialized with Markitdown {MARKITDOWN_VERSION}")
            logger.info(f"📊 Configuration: max_size={max_file_size_mb}MB, timeout={conversion_timeout_seconds}s, partial_conversion={enable_partial_conversion}")
    
    def is_supported_format(self, mime_type: str) -> bool:
        """Check if the MIME type is supported for conversion"""
        if not mime_type:
            return False
        
        mime_type_lower = mime_type.lower()
        
        # Check for exact matches first
        if mime_type_lower in self.SUPPORTED_MIME_TYPES:
            return True
        
        # Check for prefix matches (e.g., text/* for all text types)
        for supported_type in self.SUPPORTED_MIME_TYPES:
            if supported_type.endswith('/') and mime_type_lower.startswith(supported_type):
                return True
        
        return False
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported MIME types"""
        return list(self.SUPPORTED_MIME_TYPES.keys())
    
    def get_supported_formats_summary(self) -> Dict[str, List[str]]:
        """Get a categorized summary of supported formats"""
        categories = {
            'Documents': [],
            'Spreadsheets': [],
            'Presentations': [],
            'Images': [],
            'Audio/Video': [],
            'Web/Markup': [],
            'Data': [],
            'Archives': [],
            'E-books': [],
            'Email': [],
            'Code/Text': []
        }
        
        for mime_type, info in self.SUPPORTED_MIME_TYPES.items():
            format_name = info['name']
            
            if mime_type.startswith('application/pdf') or 'word' in mime_type.lower() or mime_type.endswith('document'):
                categories['Documents'].append(f"{format_name} ({mime_type})")
            elif 'excel' in mime_type.lower() or 'spreadsheet' in mime_type.lower():
                categories['Spreadsheets'].append(f"{format_name} ({mime_type})")
            elif 'powerpoint' in mime_type.lower() or 'presentation' in mime_type.lower():
                categories['Presentations'].append(f"{format_name} ({mime_type})")
            elif mime_type.startswith('image/'):
                categories['Images'].append(f"{format_name} ({mime_type})")
            elif mime_type.startswith('audio/') or mime_type.startswith('video/'):
                categories['Audio/Video'].append(f"{format_name} ({mime_type})")
            elif mime_type.startswith('text/html') or mime_type.startswith('application/xhtml'):
                categories['Web/Markup'].append(f"{format_name} ({mime_type})")
            elif mime_type in ['application/json', 'text/csv', 'application/csv', 'application/xml', 'text/xml']:
                categories['Data'].append(f"{format_name} ({mime_type})")
            elif mime_type.startswith('application/zip'):
                categories['Archives'].append(f"{format_name} ({mime_type})")
            elif 'epub' in mime_type.lower():
                categories['E-books'].append(f"{format_name} ({mime_type})")
            elif 'outlook' in mime_type.lower():
                categories['Email'].append(f"{format_name} ({mime_type})")
            elif mime_type.startswith('text/') or 'ipynb' in mime_type.lower():
                categories['Code/Text'].append(f"{format_name} ({mime_type})")
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def get_format_info(self, mime_type: str) -> Dict[str, Any]:
        """Get detailed information about a format"""
        if not mime_type:
            return {
                'name': 'Unknown',
                'description': 'Unknown format',
                'typical_issues': ['Format not recognized']
            }
        
        mime_type_lower = mime_type.lower()
        
        # Check for exact matches first
        if mime_type_lower in self.SUPPORTED_MIME_TYPES:
            return self.SUPPORTED_MIME_TYPES[mime_type_lower]
        
        # Check for prefix matches (e.g., text/* for all text types)
        for supported_type, info in self.SUPPORTED_MIME_TYPES.items():
            if supported_type.endswith('/') and mime_type_lower.startswith(supported_type):
                # Create a customized info for the specific subtype
                custom_info = info.copy()
                custom_info['name'] = f"{info['name']} ({mime_type_lower})"
                custom_info['description'] = f"{info['description']} - {mime_type_lower}"
                return custom_info
        
        return {
            'name': 'Unknown',
            'description': f'Unknown format: {mime_type}',
            'typical_issues': ['Format not recognized by markitdown']
        }
    
    def get_format_name(self, mime_type: str) -> str:
        """Get human-readable format name for MIME type"""
        return self.get_format_info(mime_type)['name']
    
    def validate_conversion_request(self, 
                                  content: bytes, 
                                  filename: str, 
                                  mime_type: str) -> List[ConversionIssue]:
        """Validate conversion request and return any issues"""
        issues = []
        
        # Check if markitdown is available
        if not MARKITDOWN_AVAILABLE:
            issues.append(ConversionErrorHandler.create_issue(
                ConversionErrorType.MARKITDOWN_NOT_AVAILABLE,
                ConversionSeverity.CRITICAL
            ))
            return issues
        
        # Check format support
        if not self.is_supported_format(mime_type):
            format_info = self.get_format_info(mime_type)
            
            # Get a sample of supported formats for suggestions
            format_categories = self.get_supported_formats_summary()
            popular_formats = []
            for category, formats in format_categories.items():
                if category in ['Documents', 'Web/Markup', 'Code/Text', 'Data']:
                    popular_formats.extend([f.split(' (')[0] for f in formats[:2]])  # Take first 2 from each category
            
            issues.append(ConversionErrorHandler.create_issue(
                ConversionErrorType.FORMAT_NOT_SUPPORTED,
                ConversionSeverity.ERROR,
                technical_details=f"MIME type: {mime_type}, Format: {format_info['name']}",
                custom_suggestions=[
                    f"Popular supported formats: {', '.join(popular_formats[:8])}",
                    "The file will still be stored in its original format",
                    "Consider converting to PDF, DOCX, HTML, or plain text format",
                    "Check the documentation for the complete list of supported formats"
                ]
            ))
        
        # Check file size
        if len(content) > self.max_file_size_bytes:
            size_mb = len(content) / (1024 * 1024)
            max_mb = self.max_file_size_bytes / (1024 * 1024)
            issues.append(ConversionErrorHandler.create_issue(
                ConversionErrorType.FILE_TOO_LARGE,
                ConversionSeverity.ERROR,
                technical_details=f"File size: {size_mb:.1f}MB, Maximum: {max_mb:.1f}MB",
                custom_suggestions=[
                    f"File size ({size_mb:.1f}MB) exceeds limit ({max_mb:.1f}MB)",
                    "Try compressing the file or splitting it into smaller parts",
                    "The original file is still stored and accessible"
                ]
            ))
        
        # Check for empty content
        if len(content) == 0:
            issues.append(ConversionErrorHandler.create_issue(
                ConversionErrorType.EMPTY_RESULT,
                ConversionSeverity.WARNING,
                technical_details="File content is empty"
            ))
        
        # Add format-specific warnings
        format_info = self.get_format_info(mime_type)
        if format_info['typical_issues']:
            issues.append(ConversionIssue(
                severity=ConversionSeverity.INFO,
                error_type=ConversionErrorType.CONVERSION_FAILED,  # Reusing enum value
                message=f"Format {format_info['name']} may have conversion challenges",
                user_message=f"Note: {format_info['name']} files may have some conversion limitations",
                suggestions=[f"Common issues with {format_info['name']}: {', '.join(format_info['typical_issues'])}"],
                technical_details=f"Typical issues for {mime_type}: {format_info['typical_issues']}"
            ))
        
        return issues
    
    async def convert_to_markdown(self, 
                                content: bytes, 
                                filename: str, 
                                mime_type: str) -> ConversionResult:
        """
        Convert file content to Markdown with comprehensive error handling
        
        Args:
            content: File content as bytes
            filename: Original filename
            mime_type: MIME type of the file
            
        Returns:
            ConversionResult with detailed information about the conversion
        """
        start_time = datetime.now()
        
        # Initialize result
        result = ConversionResult(
            success=False,
            format_supported=self.is_supported_format(mime_type),
            original_size_bytes=len(content),
            metadata={
                'filename': filename,
                'mime_type': mime_type,
                'converter_version': MARKITDOWN_VERSION,
                'conversion_settings': {
                    'max_file_size_mb': self.max_file_size_bytes / (1024 * 1024),
                    'timeout_seconds': self.conversion_timeout_seconds,
                    'partial_conversion_enabled': self.enable_partial_conversion
                }
            }
        )
        
        # Validate conversion request
        validation_issues = self.validate_conversion_request(content, filename, mime_type)
        result.issues.extend(validation_issues)
        
        # Check for critical issues that prevent conversion
        critical_issues = [issue for issue in validation_issues if issue.severity == ConversionSeverity.CRITICAL]
        error_issues = [issue for issue in validation_issues if issue.severity == ConversionSeverity.ERROR]
        
        if critical_issues:
            logger.error(f"❌ Critical issues prevent conversion of {filename}: {[issue.message for issue in critical_issues]}")
            result.conversion_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            return result
        
        if error_issues:
            logger.warning(f"⚠️ Error issues found for {filename}, skipping conversion: {[issue.message for issue in error_issues]}")
            result.conversion_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            return result
        
        # Attempt conversion
        temp_file_path = None
        try:
            # Convert to markdown using MarkItDown's stream interface
            from io import BytesIO
            content_stream = BytesIO(content)
            content_stream.name = filename  # Set name for mime type detection
            
            logger.debug(f"🔄 Starting conversion of {filename} ({mime_type}) using stream interface")
            
            # Convert using MarkItDown
            converter = MarkItDown()
            conversion_result = converter.convert_stream(content_stream)
            
            # Extract markdown content from the result object
            if hasattr(conversion_result, 'markdown') and conversion_result.markdown:
                markdown_content = conversion_result.markdown.strip()
                
                if markdown_content:
                    result.success = True
                    result.content = markdown_content
                    result.converted_size_chars = len(markdown_content)
                    
                    # Add success metadata
                    result.metadata.update({
                        'conversion_method': 'markitdown',
                        'content_preview': markdown_content[:200] + '...' if len(markdown_content) > 200 else markdown_content,
                        'line_count': markdown_content.count('\n') + 1,
                        'word_count_estimate': len(markdown_content.split())
                    })
                    
                    logger.info(f"✅ Successfully converted {filename} to markdown ({result.converted_size_chars:,} characters)")
                    
                    # Check for potential quality issues
                    self._analyze_conversion_quality(result, markdown_content, filename)
                    
                else:
                    # Empty content after conversion
                    issue = ConversionErrorHandler.create_issue(
                        ConversionErrorType.EMPTY_RESULT,
                        ConversionSeverity.ERROR,
                        technical_details=f"Markitdown returned empty content for {filename}"
                    )
                    result.issues.append(issue)
                    logger.warning(f"⚠️ Conversion of {filename} returned empty content")
                    
                    # Try to provide partial content if available
                    if self.enable_partial_conversion:
                        partial_content = self._attempt_partial_conversion(content, filename, mime_type)
                        if partial_content:
                            result.partial_content = partial_content
                            logger.info(f"📝 Extracted partial content for {filename} ({len(partial_content)} characters)")
            else:
                # No markdown attribute or empty result
                issue = ConversionErrorHandler.create_issue(
                    ConversionErrorType.CONVERSION_FAILED,
                    ConversionSeverity.ERROR,
                    technical_details=f"Markitdown result object missing markdown attribute for {filename}"
                )
                result.issues.append(issue)
                logger.error(f"❌ Markitdown result object invalid for {filename}")
                
        except Exception as e:
            # Handle conversion exceptions
            issue = ConversionErrorHandler.handle_exception(e, filename, "markdown conversion")
            result.issues.append(issue)
            logger.error(f"❌ Exception during conversion of {filename}: {type(e).__name__}: {str(e)}")
            
            # Try partial conversion on error if enabled
            if self.enable_partial_conversion and not result.partial_content:
                try:
                    partial_content = self._attempt_partial_conversion(content, filename, mime_type)
                    if partial_content:
                        result.partial_content = partial_content
                        logger.info(f"📝 Extracted partial content after error for {filename} ({len(partial_content)} characters)")
                except Exception as partial_error:
                    logger.debug(f"Partial conversion also failed for {filename}: {partial_error}")
            
        finally:
            # No cleanup needed with stream interface
            pass
        
        # Calculate final timing
        result.conversion_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Log final result
        if result.success:
            logger.info(f"✅ Conversion completed for {filename} in {result.conversion_time_ms:.1f}ms")
        elif result.partial_content:
            logger.warning(f"⚠️ Partial conversion completed for {filename} in {result.conversion_time_ms:.1f}ms")
        else:
            logger.error(f"❌ Conversion failed for {filename} after {result.conversion_time_ms:.1f}ms")
        
        return result
    
    def _get_file_extension(self, filename: str) -> str:
        """Get file extension from filename"""
        return Path(filename).suffix
    
    def _analyze_conversion_quality(self, result: ConversionResult, markdown_content: str, filename: str):
        """Analyze conversion quality and add warnings if needed"""
        
        # Check for very short content (might indicate poor conversion)
        if len(markdown_content) < 50:
            result.issues.append(ConversionIssue(
                severity=ConversionSeverity.WARNING,
                error_type=ConversionErrorType.EMPTY_RESULT,
                message="Converted content is very short",
                user_message="The converted text is quite short - the original file might contain mostly images or complex formatting",
                suggestions=[
                    "Check if the original file contains readable text",
                    "The file might be image-heavy or have complex layouts",
                    "Consider using OCR tools for image-based content"
                ],
                technical_details=f"Converted content length: {len(markdown_content)} characters"
            ))
        
        # Check for potential encoding issues
        if '�' in markdown_content or '\ufffd' in markdown_content:
            result.issues.append(ConversionIssue(
                severity=ConversionSeverity.WARNING,
                error_type=ConversionErrorType.FILE_CORRUPTED,
                message="Potential encoding issues detected",
                user_message="Some characters may not have converted correctly",
                suggestions=[
                    "The original file might have encoding issues",
                    "Try saving the original file with UTF-8 encoding",
                    "Some special characters may appear as question marks"
                ],
                technical_details="Unicode replacement characters found in converted content"
            ))
        
        # Check for very repetitive content (might indicate conversion error)
        lines = markdown_content.split('\n')
        if len(lines) > 10:
            unique_lines = set(line.strip() for line in lines if line.strip())
            if len(unique_lines) < len(lines) * 0.3:  # Less than 30% unique lines
                result.issues.append(ConversionIssue(
                    severity=ConversionSeverity.WARNING,
                    error_type=ConversionErrorType.CONVERSION_FAILED,
                    message="Highly repetitive content detected",
                    user_message="The converted content appears very repetitive - this might indicate a conversion issue",
                    suggestions=[
                        "Check if the original file has unusual formatting",
                        "The file might have tables or structured data that didn't convert well",
                        "Consider manually reviewing the converted content"
                    ],
                    technical_details=f"Only {len(unique_lines)} unique lines out of {len(lines)} total lines"
                ))
        
        # Check for successful table conversion indicators
        if '|' in markdown_content and markdown_content.count('|') > 10:
            result.issues.append(ConversionIssue(
                severity=ConversionSeverity.INFO,
                error_type=ConversionErrorType.CONVERSION_FAILED,  # Reusing enum
                message="Tables detected in conversion",
                user_message="Tables were found and converted to markdown format",
                suggestions=[
                    "Review table formatting in the converted content",
                    "Complex tables might need manual adjustment"
                ],
                technical_details=f"Detected {markdown_content.count('|')} table separators"
            ))
    
    def _attempt_partial_conversion(self, content: bytes, filename: str, mime_type: str) -> Optional[str]:
        """Attempt to extract partial content when full conversion fails"""
        
        try:
            # For text-based files, try direct text extraction
            if mime_type.startswith('text/'):
                try:
                    text_content = content.decode('utf-8', errors='ignore')
                    if text_content.strip():
                        return f"# Partial Content from {filename}\n\n```\n{text_content[:2000]}\n```\n\n*Note: This is raw text content as markdown conversion failed.*"
                except Exception:
                    pass
            
            # For HTML files, try basic text extraction
            if mime_type in ['text/html', 'application/xhtml+xml']:
                try:
                    html_content = content.decode('utf-8', errors='ignore')
                    # Very basic HTML tag removal
                    import re
                    text_content = re.sub(r'<[^>]+>', '', html_content)
                    text_content = re.sub(r'\s+', ' ', text_content).strip()
                    if text_content:
                        return f"# Partial Content from {filename}\n\n{text_content[:2000]}\n\n*Note: Basic text extraction from HTML as full conversion failed.*"
                except Exception:
                    pass
            
            # For other formats, provide basic file information
            return f"# File Information: {filename}\n\n- **File Type**: {mime_type}\n- **File Size**: {len(content):,} bytes\n- **Status**: Conversion failed, but file is stored and accessible\n\n*Note: Full content conversion was not possible for this file type.*"
            
        except Exception as e:
            logger.debug(f"Partial conversion attempt failed for {filename}: {e}")
            return None
    
    async def convert_file_with_metadata(self, 
                                       content: bytes, 
                                       filename: str, 
                                       mime_type: str) -> Dict[str, Any]:
        """
        Convert file to markdown with detailed metadata (legacy method for backward compatibility)
        
        Returns:
            Dictionary with conversion results and metadata
        """
        # Use the new enhanced conversion method
        conversion_result = await self.convert_to_markdown(content, filename, mime_type)
        
        # Convert to legacy format for backward compatibility
        result = {
            'success': conversion_result.success,
            'markdown_content': conversion_result.content,
            'partial_content': conversion_result.partial_content,
            'conversion_time_ms': conversion_result.conversion_time_ms,
            'format_supported': conversion_result.format_supported,
            'file_size_bytes': conversion_result.original_size_bytes,
            'original_mime_type': mime_type,
            'converted_size_chars': conversion_result.converted_size_chars,
            
            # Enhanced error information
            'error': None,
            'errors': [issue.message for issue in conversion_result.issues if issue.severity == ConversionSeverity.ERROR],
            'warnings': [issue.message for issue in conversion_result.issues if issue.severity == ConversionSeverity.WARNING],
            'user_messages': conversion_result.get_user_messages(),
            'suggestions': conversion_result.get_suggestions(),
            'user_friendly_summary': conversion_result.user_friendly_summary,
            
            # Additional metadata
            'has_errors': conversion_result.has_errors,
            'has_warnings': conversion_result.has_warnings,
            'issues_count': len(conversion_result.issues),
            'metadata': conversion_result.metadata
        }
        
        # Set legacy error field for backward compatibility
        if conversion_result.has_errors:
            error_messages = [issue.message for issue in conversion_result.issues if issue.severity == ConversionSeverity.ERROR]
            result['error'] = '; '.join(error_messages) if error_messages else "Conversion failed"
        elif not conversion_result.success and not conversion_result.partial_content:
            result['error'] = "Conversion failed without specific error"
        
        # Add markdown length for backward compatibility
        if conversion_result.content:
            result['markdown_length'] = len(conversion_result.content)
        elif conversion_result.partial_content:
            result['markdown_length'] = len(conversion_result.partial_content)
        
        return result
    
    async def convert_to_markdown_legacy(self, 
                                       content: bytes, 
                                       filename: str, 
                                       mime_type: str) -> Optional[str]:
        """
        Legacy method that returns just the markdown content (for backward compatibility)
        
        Returns:
            Markdown content as string, or None if conversion failed
        """
        conversion_result = await self.convert_to_markdown(content, filename, mime_type)
        
        # Return content if successful, partial content if available, or None
        if conversion_result.success and conversion_result.content:
            return conversion_result.content
        elif conversion_result.partial_content:
            return conversion_result.partial_content
        else:
            return None


# Global converter instance
markdown_converter = MarkdownConverter(
    max_file_size_mb=int(os.getenv("MAX_MARKDOWN_FILE_SIZE_MB", "50")),
    conversion_timeout_seconds=int(os.getenv("MARKDOWN_CONVERSION_TIMEOUT_SECONDS", "300")),
    enable_partial_conversion=os.getenv("ENABLE_PARTIAL_CONVERSION", "true").lower() == "true"
) 