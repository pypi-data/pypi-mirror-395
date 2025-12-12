"""
Multimodal Image Analysis Tools

Provides on-demand image analysis capabilities for the Agent Framework.
This module implements tools for image description, question answering about images,
and integration with the existing file storage system.

Requirements covered:
- 3.1: Multimodal image analysis when enabled
- 3.2: Agent multimodal capabilities
- 3.4: OCR and text extraction from images
- 5.1: Enhanced agent integration
- 5.4: Comprehensive file information

v 0.1.0 - Initial implementation
"""

import os
import logging
from typing import Optional, List, Dict, Any, Union, Tuple
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import base64
from io import BytesIO

# Type checking imports to avoid circular dependencies
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from agent_framework.storage.file_system_management import FileStorageManager
    from agent_framework.storage.file_storages import FileMetadata

logger = logging.getLogger(__name__)


# ===== MULTIMODAL PROCESSING CLASSES =====

class MultimodalCapability(Enum):
    """Available multimodal capabilities"""
    IMAGE_DESCRIPTION = "image_description"
    IMAGE_QUESTION_ANSWERING = "image_qa"
    OCR_TEXT_EXTRACTION = "ocr_extraction"
    OBJECT_DETECTION = "object_detection"
    SCENE_ANALYSIS = "scene_analysis"


class MultimodalProcessingStatus(Enum):
    """Status of multimodal processing"""
    NOT_ATTEMPTED = "not_attempted"
    SUCCESS = "success"
    FAILED = "failed"
    NOT_SUPPORTED = "not_supported"
    DISABLED = "disabled"


@dataclass
class ImageAnalysisResult:
    """Result of image analysis operation"""
    success: bool
    description: Optional[str] = None
    objects_detected: List[str] = field(default_factory=list)
    text_detected: Optional[str] = None
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    error_message: Optional[str] = None
    processing_time_ms: float = 0.0
    capabilities_used: List[MultimodalCapability] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def user_friendly_summary(self) -> str:
        """Generate user-friendly summary of analysis result"""
        if self.success:
            parts = []
            if self.description:
                parts.append(f"Description: {self.description}")
            if self.objects_detected:
                parts.append(f"Objects found: {', '.join(self.objects_detected)}")
            if self.text_detected:
                parts.append(f"Text extracted: {self.text_detected[:100]}{'...' if len(self.text_detected) > 100 else ''}")
            return "✅ Image analysis completed. " + " | ".join(parts)
        else:
            return f"❌ Image analysis failed: {self.error_message or 'Unknown error'}"


@dataclass
class MultimodalProcessingResult:
    """Result of multimodal processing at upload time"""
    success: bool
    has_visual_content: bool = False
    basic_metadata: Dict[str, Any] = field(default_factory=dict)
    processing_status: MultimodalProcessingStatus = MultimodalProcessingStatus.NOT_ATTEMPTED
    error_message: Optional[str] = None
    capabilities_available: List[MultimodalCapability] = field(default_factory=list)
    processing_time_ms: float = 0.0


# ===== IMAGE ANALYSIS TOOL =====

class ImageAnalysisTool:
    """
    Agent tool for on-demand image analysis using multimodal AI capabilities.
    
    This tool provides methods for:
    - Image description and scene analysis
    - Question answering about image content
    - OCR text extraction from images
    - Object detection and recognition
    
    The tool integrates with the existing file storage system to analyze stored images.
    """
    
    def __init__(self, file_storage_manager: 'FileStorageManager'):
        self.file_storage_manager = file_storage_manager
        self.supported_image_types = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
            'image/webp', 'image/bmp', 'image/tiff'
        ]
        self.multimodal_enabled = self._check_multimodal_availability()
        
        logger.info(f"ImageAnalysisTool initialized (multimodal enabled: {self.multimodal_enabled})")
    
    def _check_multimodal_availability(self) -> bool:
        """Check if multimodal capabilities are available"""
        # Check environment variable for multimodal enablement
        multimodal_env = os.getenv("ENABLE_MULTIMODAL_ANALYSIS", "false").lower()
        if multimodal_env not in ["true", "1", "yes", "on"]:
            logger.info("Multimodal analysis disabled via environment variable")
            return False
        
        # Check for required dependencies (this would be expanded based on actual multimodal library)
        try:
            # Placeholder for actual multimodal library imports
            # For example: import openai, import anthropic, etc.
            # For now, we'll simulate availability
            return True
        except ImportError as e:
            logger.warning(f"Multimodal dependencies not available: {e}")
            return False
    
    async def analyze_image(self, file_id: str, analysis_prompt: Optional[str] = None) -> ImageAnalysisResult:
        """
        Analyze image content using multimodal AI capabilities.
        
        Args:
            file_id: ID of the stored image file
            analysis_prompt: Optional specific prompt for analysis
            
        Returns:
            ImageAnalysisResult with analysis details
        """
        start_time = datetime.now()
        
        try:
            # Check if multimodal is enabled
            if not self.multimodal_enabled:
                return ImageAnalysisResult(
                    success=False,
                    error_message="Multimodal analysis is not enabled or available",
                    processing_time_ms=0.0
                )
            
            # Retrieve file and validate it's an image
            try:
                content, metadata = await self.file_storage_manager.retrieve_file(file_id)
            except Exception as e:
                return ImageAnalysisResult(
                    success=False,
                    error_message=f"Failed to retrieve file: {str(e)}",
                    processing_time_ms=0.0
                )
            
            # Validate file is an image
            if not self._is_supported_image(metadata.mime_type):
                return ImageAnalysisResult(
                    success=False,
                    error_message=f"File type {metadata.mime_type} is not a supported image format",
                    processing_time_ms=0.0
                )
            
            # Perform image analysis
            analysis_result = await self._perform_image_analysis(
                content, metadata, analysis_prompt
            )
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            analysis_result.processing_time_ms = processing_time
            
            # Update file metadata with analysis results if successful
            if analysis_result.success:
                await self._update_file_with_analysis_results(file_id, analysis_result)
            
            logger.info(f"Image analysis completed for {file_id} in {processing_time:.2f}ms")
            return analysis_result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"Image analysis failed for {file_id}: {e}")
            return ImageAnalysisResult(
                success=False,
                error_message=f"Analysis failed: {str(e)}",
                processing_time_ms=processing_time
            )
    
    async def describe_image(self, file_id: str) -> str:
        """
        Get a description of the image content.
        
        Args:
            file_id: ID of the stored image file
            
        Returns:
            String description of the image
        """
        result = await self.analyze_image(file_id, "Describe this image in detail.")
        
        if result.success and result.description:
            return result.description
        elif result.error_message:
            return f"Unable to describe image: {result.error_message}"
        else:
            return "Unable to describe image: No description available"
    
    async def answer_about_image(self, file_id: str, question: str) -> str:
        """
        Answer specific questions about an image.
        
        Args:
            file_id: ID of the stored image file
            question: Question to answer about the image
            
        Returns:
            String answer to the question
        """
        prompt = f"Answer this question about the image: {question}"
        result = await self.analyze_image(file_id, prompt)
        
        if result.success and result.description:
            return result.description
        elif result.error_message:
            return f"Unable to answer question: {result.error_message}"
        else:
            return "Unable to answer question about the image"
    
    async def extract_text_from_image(self, file_id: str) -> str:
        """
        Extract text content from an image using OCR.
        
        Args:
            file_id: ID of the stored image file
            
        Returns:
            Extracted text content
        """
        result = await self.analyze_image(file_id, "Extract all text visible in this image.")
        
        if result.success and result.text_detected:
            return result.text_detected
        elif result.error_message:
            return f"Unable to extract text: {result.error_message}"
        else:
            return "No text detected in the image"
    
    async def get_image_capabilities(self, file_id: str) -> List[MultimodalCapability]:
        """
        Get available capabilities for a specific image file.
        
        Args:
            file_id: ID of the stored image file
            
        Returns:
            List of available multimodal capabilities
        """
        if not self.multimodal_enabled:
            return []
        
        try:
            _, metadata = await self.file_storage_manager.retrieve_file(file_id)
            
            if not self._is_supported_image(metadata.mime_type):
                return []
            
            # Return all available capabilities for supported images
            return [
                MultimodalCapability.IMAGE_DESCRIPTION,
                MultimodalCapability.IMAGE_QUESTION_ANSWERING,
                MultimodalCapability.OCR_TEXT_EXTRACTION,
                MultimodalCapability.OBJECT_DETECTION,
                MultimodalCapability.SCENE_ANALYSIS
            ]
            
        except Exception as e:
            logger.error(f"Failed to get image capabilities for {file_id}: {e}")
            return []
    
    def _is_supported_image(self, mime_type: Optional[str]) -> bool:
        """Check if the file type is a supported image format"""
        if not mime_type:
            return False
        return mime_type.lower() in self.supported_image_types
    
    async def _perform_image_analysis(self, 
                                    content: bytes, 
                                    metadata: 'FileMetadata', 
                                    analysis_prompt: Optional[str] = None) -> ImageAnalysisResult:
        """
        Perform the actual image analysis using multimodal AI.
        
        This is a placeholder implementation that would be replaced with
        actual multimodal AI service calls (OpenAI Vision, Anthropic Claude Vision, etc.)
        """
        try:
            # Convert image to base64 for API calls
            image_base64 = base64.b64encode(content).decode('utf-8')
            
            # Try to use OpenAI Vision API if available
            try:
                from openai import OpenAI
                client = OpenAI()
                
                # Convert image to base64 for API
                image_base64_url = f"data:{metadata.mime_type};base64,{image_base64}"
                
                # Prepare prompt based on analysis type
                if analysis_prompt:
                    prompt = analysis_prompt
                else:
                    prompt = "Describe this image in detail, including any visible text, objects, and the overall scene."
                
                # Call Vision API
                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": image_base64_url}}
                            ]
                        }
                    ],
                    max_tokens=500
                )
                
                # Extract response
                description = response.choices[0].message.content
                
                # Try OCR if needed
                text_detected = None
                if "extract text" in prompt.lower() or "ocr" in prompt.lower():
                    # Use Vision API for OCR
                    ocr_response = client.chat.completions.create(
                        model="gpt-4-vision-preview",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Extract and list all text visible in this image, including any signs, labels, or written content."},
                                    {"type": "image_url", "image_url": {"url": image_base64_url}}
                                ]
                            }
                        ],
                        max_tokens=300
                    )
                    text_detected = ocr_response.choices[0].message.content
                
                # Return successful result
                return ImageAnalysisResult(
                    success=True,
                    description=description,
                    objects_detected=[],  # Could be enhanced with object detection API
                    text_detected=text_detected,
                    confidence_scores={"description": 0.95},
                    capabilities_used=[
                        MultimodalCapability.IMAGE_DESCRIPTION,
                        MultimodalCapability.OCR_TEXT_EXTRACTION if text_detected else None,
                        MultimodalCapability.SCENE_ANALYSIS
                    ],
                    metadata={
                        "image_size_bytes": len(content),
                        "image_format": metadata.mime_type,
                        "analysis_prompt": analysis_prompt,
                        "api_used": "openai_vision"
                    }
                )
                
            except ImportError:
                logger.warning("OpenAI package not available for vision analysis")
                return ImageAnalysisResult(
                    success=False,
                    error_message="Vision API not available - OpenAI package not installed"
                )
            except Exception as e:
                logger.error(f"Vision API error: {e}")
                return ImageAnalysisResult(
                    success=False,
                    error_message=f"Vision API error: {str(e)}"
                )
            
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            return ImageAnalysisResult(
                success=False,
                error_message=str(e)
            )
    
    async def _update_file_with_analysis_results(self, file_id: str, result: ImageAnalysisResult):
        """Update file metadata with analysis results"""
        try:
            metadata_updates = {
                'image_analysis_result': {
                    'description': result.description,
                    'objects_detected': result.objects_detected,
                    'text_detected': result.text_detected,
                    'confidence_scores': result.confidence_scores,
                    'analysis_timestamp': datetime.now().isoformat(),
                    'capabilities_used': [cap.value for cap in result.capabilities_used]
                },
                'multimodal_processing_status': 'success',
                'has_visual_content': True,
                'updated_at': datetime.now()
            }
            
            await self.file_storage_manager.update_metadata(file_id, metadata_updates)
            logger.debug(f"Updated file {file_id} with analysis results")
            
        except Exception as e:
            logger.error(f"Failed to update file metadata with analysis results: {e}")


# ===== MULTIMODAL PROCESSOR =====

class MultimodalProcessor:
    """
    Handles automatic multimodal processing at upload time.
    
    This processor prepares images for future analysis without performing
    expensive operations immediately. It extracts basic metadata and
    indicates multimodal capabilities available.
    """
    
    def __init__(self, enable_auto_analysis: bool = False):
        self.enable_auto_analysis = enable_auto_analysis  # Usually disabled for performance
        self.supported_image_types = [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
            'image/webp', 'image/bmp', 'image/tiff'
        ]
        self.multimodal_enabled = self._check_multimodal_availability()
        
        logger.info(f"MultimodalProcessor initialized (auto-analysis: {enable_auto_analysis}, enabled: {self.multimodal_enabled})")
    
    def _check_multimodal_availability(self) -> bool:
        """Check if multimodal capabilities are available"""
        multimodal_env = os.getenv("ENABLE_MULTIMODAL_ANALYSIS", "false").lower()
        return multimodal_env in ["true", "1", "yes", "on"]
    
    async def process_image_at_upload(self, 
                                    content: bytes, 
                                    mime_type: str, 
                                    filename: str) -> MultimodalProcessingResult:
        """
        Process image at upload time.
        
        This method:
        1. Checks if the file is an image
        2. Extracts basic metadata without expensive operations
        3. Prepares the image for future analysis
        4. Updates file metadata to indicate multimodal capabilities
        
        Args:
            content: Image file content
            mime_type: MIME type of the file
            filename: Original filename
            
        Returns:
            MultimodalProcessingResult with processing status
        """
        start_time = datetime.now()
        
        try:
            # Check if file is an image
            if not self._is_supported_image(mime_type):
                return MultimodalProcessingResult(
                    success=True,
                    has_visual_content=False,
                    processing_status=MultimodalProcessingStatus.NOT_SUPPORTED,
                    processing_time_ms=0.0
                )
            
            # Extract basic image metadata
            basic_metadata = await self._extract_basic_image_metadata(content, mime_type, filename)
            
            # Determine available capabilities
            capabilities_available = []
            if self.multimodal_enabled:
                capabilities_available = [
                    MultimodalCapability.IMAGE_DESCRIPTION,
                    MultimodalCapability.IMAGE_QUESTION_ANSWERING,
                    MultimodalCapability.OCR_TEXT_EXTRACTION,
                    MultimodalCapability.OBJECT_DETECTION,
                    MultimodalCapability.SCENE_ANALYSIS
                ]
            
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return MultimodalProcessingResult(
                success=True,
                has_visual_content=True,
                basic_metadata=basic_metadata,
                processing_status=MultimodalProcessingStatus.SUCCESS if self.multimodal_enabled else MultimodalProcessingStatus.DISABLED,
                capabilities_available=capabilities_available,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.error(f"Multimodal processing failed for {filename}: {e}")
            
            return MultimodalProcessingResult(
                success=False,
                has_visual_content=False,
                processing_status=MultimodalProcessingStatus.FAILED,
                error_message=str(e),
                processing_time_ms=processing_time
            )
    
    def _is_supported_image(self, mime_type: str) -> bool:
        """Check if the file type is a supported image format"""
        return mime_type.lower() in self.supported_image_types
    
    async def _extract_basic_image_metadata(self, 
                                          content: bytes, 
                                          mime_type: str, 
                                          filename: str) -> Dict[str, Any]:
        """
        Extract basic image metadata without expensive operations.
        
        This method extracts lightweight metadata that can be used
        to prepare for future analysis.
        """
        try:
            metadata = {
                'file_size_bytes': len(content),
                'mime_type': mime_type,
                'filename': filename,
                'is_image': True,
                'multimodal_ready': self.multimodal_enabled,
                'processing_timestamp': datetime.now().isoformat()
            }
            
            # Try to extract basic image properties (width, height, etc.)
            # This would use a lightweight image library like Pillow
            try:
                from PIL import Image
                with BytesIO(content) as img_buffer:
                    with Image.open(img_buffer) as img:
                        metadata.update({
                            'width': img.width,
                            'height': img.height,
                            'format': img.format,
                            'mode': img.mode,
                            'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                        })
            except ImportError:
                logger.debug("PIL not available for image metadata extraction")
            except Exception as e:
                logger.debug(f"Failed to extract image properties: {e}")
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to extract basic image metadata: {e}")
            return {
                'file_size_bytes': len(content),
                'mime_type': mime_type,
                'filename': filename,
                'is_image': True,
                'error': str(e)
            }


# ===== UTILITY FUNCTIONS =====

def get_multimodal_capabilities_summary() -> Dict[str, Any]:
    """Get summary of available multimodal capabilities"""
    multimodal_enabled = os.getenv("ENABLE_MULTIMODAL_ANALYSIS", "false").lower() in ["true", "1", "yes", "on"]
    
    return {
        'multimodal_enabled': multimodal_enabled,
        'supported_image_types': [
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
            'image/webp', 'image/bmp', 'image/tiff'
        ],
        'available_capabilities': [cap.value for cap in MultimodalCapability] if multimodal_enabled else [],
        'environment_variable': 'ENABLE_MULTIMODAL_ANALYSIS',
        'current_setting': os.getenv("ENABLE_MULTIMODAL_ANALYSIS", "false")
    }


def is_multimodal_enabled() -> bool:
    """Check if multimodal analysis is enabled"""
    return os.getenv("ENABLE_MULTIMODAL_ANALYSIS", "false").lower() in ["true", "1", "yes", "on"]


def get_supported_image_types() -> List[str]:
    """Get list of supported image MIME types"""
    return [
        'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
        'image/webp', 'image/bmp', 'image/tiff'
    ]