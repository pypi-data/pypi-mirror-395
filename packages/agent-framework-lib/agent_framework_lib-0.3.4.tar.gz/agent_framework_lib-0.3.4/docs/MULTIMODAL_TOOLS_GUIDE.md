# Multimodal Tools Guide

This guide covers the multimodal image analysis capabilities in the Agent Framework, including the ImageAnalysisTool and multimodal processing features.

## Overview

The Agent Framework provides comprehensive multimodal capabilities for analyzing images, extracting text through OCR, and providing AI-powered image descriptions and analysis. These capabilities are built on top of OpenAI's vision models and can be integrated into any agent.

## Key Components

### 1. ImageAnalysisTool

The `ImageAnalysisTool` is the primary interface for image analysis capabilities:

```python
from agent_framework.multimodal_tools import ImageAnalysisTool

# Initialize with file storage manager
image_tool = ImageAnalysisTool(file_storage_manager)

# Analyze an image with custom prompt
result = await image_tool.analyze_image(
    file_id="image_file_id",
    analysis_prompt="Describe this image in detail and identify any objects"
)

# Get basic image description
description = await image_tool.describe_image(file_id)

# Answer specific questions about image
answer = await image_tool.answer_about_image(
    file_id, 
    "What colors are prominent in this image?"
)

# Extract text from image (OCR)
text = await image_tool.extract_text_from_image(file_id)

# Check what capabilities are available
capabilities = await image_tool.get_image_capabilities(file_id)
```

### 2. Multimodal Integration

The multimodal integration handles automatic processing at upload time:

```python
from agent_framework.multimodal_integration import MultimodalProcessor

# Initialize processor
processor = MultimodalProcessor(enable_auto_analysis=False)

# Process image at upload (prepares for future analysis)
result = await processor.process_image_at_upload(
    content=image_bytes,
    mime_type="image/jpeg"
)
```

## Configuration

### Environment Variables

```bash
# Enable multimodal analysis
ENABLE_MULTIMODAL_ANALYSIS=true

# OpenAI configuration for vision models
OPENAI_API_KEY=your_api_key_here
OPENAI_API_MODEL=gpt-4o-mini  # or gpt-4-vision-preview

# Optional: Configure vision model specifically
VISION_MODEL=gpt-4o-mini
```

### Checking Multimodal Capabilities

```python
from agent_framework.multimodal_tools import get_multimodal_capabilities_summary

# Get comprehensive capability information
capabilities = get_multimodal_capabilities_summary()

print(f"Multimodal enabled: {capabilities['multimodal_enabled']}")
print(f"Supported formats: {capabilities['supported_image_types']}")
print(f"Available capabilities: {capabilities['available_capabilities']}")
```

## Supported Image Formats

The system supports the following image formats:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Usage Examples

### Basic Image Analysis

```python
import asyncio
from agent_framework.file_storages import FileStorageFactory
from agent_framework.multimodal_tools import ImageAnalysisTool

async def analyze_image_example():
    # Setup
    storage_manager = await FileStorageFactory.create_storage_manager()
    image_tool = ImageAnalysisTool(storage_manager)
    
    # Assume we have an uploaded image
    file_id = "your_image_file_id"
    
    # Get basic description
    description = await image_tool.describe_image(file_id)
    print(f"Image description: {description}")
    
    # Ask specific questions
    colors = await image_tool.answer_about_image(
        file_id, 
        "What are the main colors in this image?"
    )
    print(f"Colors: {colors}")
    
    # Extract any text
    text = await image_tool.extract_text_from_image(file_id)
    if text:
        print(f"Text found: {text}")
    
    # Detailed analysis
    analysis = await image_tool.analyze_image(
        file_id,
        "Analyze this image for any safety concerns or notable features"
    )
    
    if analysis.success:
        print(f"Analysis: {analysis.description}")
        print(f"Objects detected: {analysis.objects_detected}")
        print(f"Confidence: {analysis.confidence_scores}")
    else:
        print(f"Analysis failed: {analysis.error_message}")

# Run the example
asyncio.run(analyze_image_example())
```

### Agent Integration

```python
from agent_framework import AgentInterface
from agent_framework.multimodal_tools import ImageAnalysisTool

class MultimodalAgent(AgentInterface):
    def __init__(self):
        self.image_tool = None
    
    async def initialize(self):
        storage_manager = await FileStorageFactory.create_storage_manager()
        self.image_tool = ImageAnalysisTool(storage_manager)
    
    async def handle_message(self, session_id: str, agent_input: StructuredAgentInput):
        # Process any uploaded images
        if agent_input.parts:
            for part in agent_input.parts:
                if isinstance(part, FileDataInputPart):
                    if part.mime_type.startswith('image/'):
                        # Store and analyze the image
                        file_id = await self.store_file(part)
                        description = await self.image_tool.describe_image(file_id)
                        
                        return StructuredAgentOutput(
                            response_text=f"I can see the image you uploaded. {description}"
                        )
        
        return StructuredAgentOutput(
            response_text="Hello! Upload an image and I'll analyze it for you."
        )
```

### Batch Image Processing

```python
async def process_multiple_images(file_ids: list[str]):
    storage_manager = await FileStorageFactory.create_storage_manager()
    image_tool = ImageAnalysisTool(storage_manager)
    
    results = []
    for file_id in file_ids:
        try:
            # Check if file supports image analysis
            capabilities = await image_tool.get_image_capabilities(file_id)
            
            if 'image_analysis' in capabilities:
                description = await image_tool.describe_image(file_id)
                text = await image_tool.extract_text_from_image(file_id)
                
                results.append({
                    'file_id': file_id,
                    'description': description,
                    'extracted_text': text,
                    'success': True
                })
            else:
                results.append({
                    'file_id': file_id,
                    'error': 'Image analysis not supported for this file',
                    'success': False
                })
                
        except Exception as e:
            results.append({
                'file_id': file_id,
                'error': str(e),
                'success': False
            })
    
    return results
```

## Error Handling

### Common Error Scenarios

1. **Multimodal Analysis Disabled**
```python
# Check if multimodal is enabled
capabilities = get_multimodal_capabilities_summary()
if not capabilities['multimodal_enabled']:
    print("Multimodal analysis is disabled. Set ENABLE_MULTIMODAL_ANALYSIS=true")
```

2. **Unsupported File Format**
```python
try:
    result = await image_tool.analyze_image(file_id)
except Exception as e:
    if "not supported" in str(e):
        print("This file format is not supported for image analysis")
```

3. **API Key Issues**
```python
try:
    description = await image_tool.describe_image(file_id)
except Exception as e:
    if "API key" in str(e):
        print("OpenAI API key is missing or invalid")
```

### Graceful Degradation

```python
async def safe_image_analysis(file_id: str):
    try:
        # Try full analysis first
        result = await image_tool.analyze_image(file_id, "Describe this image")
        return result.description
    except Exception:
        try:
            # Fall back to basic description
            return await image_tool.describe_image(file_id)
        except Exception:
            # Fall back to OCR only
            try:
                text = await image_tool.extract_text_from_image(file_id)
                return f"Could not analyze image, but extracted text: {text}" if text else None
            except Exception:
                return "Image analysis not available"
```

## Performance Considerations

### Optimization Tips

1. **Lazy Analysis**: Only analyze images when requested, not automatically at upload
2. **Caching**: Cache analysis results to avoid repeated API calls
3. **Batch Processing**: Process multiple images in parallel when possible
4. **Size Limits**: Consider image size limits for API calls

### Resource Management

```python
from agent_framework.resource_manager import ResourceManager

# Configure resource limits for image processing
resource_manager = ResourceManager(
    max_concurrent_operations=5,  # Limit concurrent image analyses
    max_memory_usage_mb=200      # Limit memory usage
)

async def managed_image_analysis(file_id: str):
    async with resource_manager.acquire_processing_slot():
        return await image_tool.analyze_image(file_id)
```

## API Reference

### ImageAnalysisTool Methods

#### `analyze_image(file_id: str, analysis_prompt: str = None) -> ImageAnalysisResult`
Performs comprehensive image analysis with optional custom prompt.

**Parameters:**
- `file_id`: ID of the stored image file
- `analysis_prompt`: Optional custom prompt for analysis

**Returns:** `ImageAnalysisResult` with description, objects, confidence scores

#### `describe_image(file_id: str) -> str`
Gets a basic description of the image content.

**Parameters:**
- `file_id`: ID of the stored image file

**Returns:** String description of the image

#### `answer_about_image(file_id: str, question: str) -> str`
Answers specific questions about an image.

**Parameters:**
- `file_id`: ID of the stored image file
- `question`: Question to ask about the image

**Returns:** String answer to the question

#### `extract_text_from_image(file_id: str) -> Optional[str]`
Extracts text from image using OCR capabilities.

**Parameters:**
- `file_id`: ID of the stored image file

**Returns:** Extracted text or None if no text found

#### `get_image_capabilities(file_id: str) -> List[str]`
Gets list of available capabilities for the image file.

**Parameters:**
- `file_id`: ID of the stored image file

**Returns:** List of capability strings

### ImageAnalysisResult Class

```python
@dataclass
class ImageAnalysisResult:
    success: bool
    description: Optional[str] = None
    objects_detected: List[str] = field(default_factory=list)
    text_detected: Optional[str] = None
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    error_message: Optional[str] = None
    user_friendly_summary: str = ""
```

## Integration with File Processing

The multimodal tools integrate seamlessly with the enhanced file processing system:

```python
from agent_framework.file_system_management import process_file_inputs

# Process files with multimodal capabilities enabled
processed_input, files = await process_file_inputs(
    agent_input,
    file_storage_manager,
    enable_multimodal_processing=True  # Enable multimodal processing
)

# Check which files support image analysis
for file_info in files:
    if file_info.get('has_visual_content'):
        print(f"File {file_info['filename']} supports image analysis")
        
        # Capabilities are already checked during processing
        capabilities = file_info.get('multimodal_capabilities', [])
        if 'image_analysis' in capabilities:
            # File is ready for analysis
            pass
```

## Troubleshooting

### Common Issues

1. **"Multimodal analysis not available"**
   - Check `ENABLE_MULTIMODAL_ANALYSIS=true` environment variable
   - Verify OpenAI API key is set and valid
   - Ensure the model supports vision (gpt-4o-mini, gpt-4-vision-preview)

2. **"Image format not supported"**
   - Check that the file is actually an image
   - Verify the MIME type is correctly detected
   - Try converting to a supported format (JPEG, PNG)

3. **"API rate limit exceeded"**
   - Implement rate limiting in your application
   - Use caching to avoid repeated analysis
   - Consider upgrading your OpenAI plan

4. **Poor analysis quality**
   - Try more specific prompts
   - Ensure image quality is good
   - Check image size (very large images may be resized)

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.getLogger('agent_framework.multimodal_tools').setLevel(logging.DEBUG)
```

## Best Practices

1. **Always check capabilities** before attempting analysis
2. **Use specific prompts** for better analysis results
3. **Implement error handling** for graceful degradation
4. **Cache results** to avoid repeated API calls
5. **Monitor API usage** to stay within limits
6. **Validate image files** before processing
7. **Provide user feedback** during long-running analyses

## See Also

- [AI Content Management Guide](./AI_CONTENT_MANAGEMENT_GUIDE.md)
- [Creating Agents Guide](./CREATING_AGENTS.md)
- [API Reference](./api-reference.md)
- [Agent Integration Examples](../examples/)