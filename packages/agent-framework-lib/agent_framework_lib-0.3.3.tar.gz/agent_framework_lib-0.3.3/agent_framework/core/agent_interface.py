import abc
from typing import Any, Dict, AsyncGenerator, List, Union, Literal, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
import base64

# Define a type alias for the content part, which can be text or an image dictionary
# Following OpenAI/AutoGen structure: {"type": "text", "text": "..."} or {"type": "image_url", "image_url": {"url": "..."}}
# For simplicity in the interface, we accept Dict for images, specific validation happens in server/agent.
# AgentInputContent = List[Union[str, Dict[str, Any]]] # OLD TYPE, to be replaced

# --- Agent Configuration Model ---
class AgentConfig(BaseModel):
    """
    Configuration settings for agent behavior that can be set per session.
    All fields are optional to maintain backward compatibility.
    """
    # Model parameters
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Controls randomness (0.0-2.0)")
    max_tokens: Optional[int] = Field(None, ge=1, le=100000, description="Maximum tokens in response")
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0, description="Nucleus sampling parameter")
    frequency_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0, description="Reduces repetition of frequent tokens")
    presence_penalty: Optional[float] = Field(None, ge=-2.0, le=2.0, description="Reduces repetition of any tokens")
    stop_sequences: Optional[List[str]] = Field(None, description="Custom stop sequences for response termination")
    
    # Client behavior parameters
    timeout: Optional[int] = Field(None, ge=1, le=600, description="Request timeout in seconds")
    max_retries: Optional[int] = Field(None, ge=0, le=10, description="Maximum retry attempts")
    model_selection: Optional[str] = Field(None, description="Override default model for session")
    
    # Response preferences
    response_format: Optional[str] = Field(None, description="Preferred response format hints")
    
    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v):
        if v is not None and not (0.0 <= v <= 2.0):
            raise ValueError('Temperature must be between 0.0 and 2.0')
        return v
    
    @field_validator('top_p')
    @classmethod
    def validate_top_p(cls, v):
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError('Top_p must be between 0.0 and 1.0')
        return v

# --- Input Part Models ---
class TextInputPart(BaseModel):
    type: Literal["text"] = "text"
    text: str

class ImageUrlInputPart(BaseModel):
    type: Literal["image_url"] = "image_url"
    # Enhanced to support both file uploads and URLs with MIME type
    image_url: Optional[Dict[str, str]] = Field(None, json_schema_extra={"example": {"url": "data:image/png;base64,..."}})
    file: Optional[bytes] = Field(None, description="Binary file content")
    url: Optional[str] = Field(None, description="Image URL")
    mime_type: Optional[str] = Field(None, description="MIME type (e.g., image/png, image/jpeg)")
    
    @model_validator(mode='before')
    @classmethod
    def validate_at_least_one_source(cls, data: Any) -> Any:
        """Ensure at least one of image_url, file, or url is present."""
        if isinstance(data, dict):
            if not ('file' in data or 'url' in data or 'image_url' in data):
                 raise ValueError('At least one of image_url, file, or url must be present')
        return data


class FileDataInputPart(BaseModel):
    type: Literal["file_data"] = "file_data"
    filename: str
    content_base64: str # Base64 encoded file content
    mime_type: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def validate_at_least_one_source(cls, data: Any) -> Any:
        """Ensure content_base64 is present."""
        if isinstance(data, dict):
            if not ('content_base64' in data):
                raise ValueError('content_base64 must be present')
        return data
    
    def set_binary_content(self, binary_data: bytes):
        """Helper method to set binary content as base64"""
        self.content_base64 = base64.b64encode(binary_data).decode('utf-8')
    
    def get_binary_content(self) -> Optional[bytes]:
        """Helper method to get binary content from base64"""
        if self.content_base64 is None:
            return None
        try:
            return base64.b64decode(self.content_base64)
        except Exception:
            return None

# StructuredAgentInput will be defined after all part classes

# --- Output Part Models ---
# These models represent the various types of structured content an agent can produce.

class TextOutputPart(BaseModel):
    type: Literal["text_output"] = "text_output" # Changed from "text" to avoid conflict with input
    text: str # Can be markdown, plain text, etc.

class TextOutputStreamPart(BaseModel):
    type: Literal["text_output_stream"] = "text_output_stream"
    text: str # Streaming content with special markers

class JsonOutputPart(BaseModel):
    type: Literal["json_data"] = "json_data"
    data: Any # Parsed JSON data (Python dict/list)
    filename: Optional[str] = None # Optional filename if it represents a savable JSON file

class YamlOutputPart(BaseModel):
    type: Literal["yaml_data"] = "yaml_data"
    data: Any # Parsed YAML data (Python dict/list) or raw YAML string
    filename: Optional[str] = None

class FileContentOutputPart(BaseModel): # Renamed from FileDataOutputPart for clarity
    type: Literal["file_content_output"] = "file_content_output" # Changed from "file_data"
    filename: str
    content_base64: str # Base64 encoded file content
    mime_type: Optional[str] = None

class FileReferenceInputPart(BaseModel):
    """Reference to a file stored in the file storage system"""
    type: Literal["file_reference"] = "file_reference"
    file_id: str  # Reference to stored file
    filename: Optional[str] = None  # Optional filename for convenience
    
class FileReferenceOutputPart(BaseModel):
    """Reference to a file stored in the file storage system"""
    type: Literal["file_reference_output"] = "file_reference_output"  
    file_id: str
    filename: str
    mime_type: Optional[str] = None
    download_url: Optional[str] = None  # API endpoint to download
    size_bytes: Optional[int] = None  # File size information

# Define the Union types after all classes are defined
AgentInputPartUnion = Union[TextInputPart, ImageUrlInputPart, FileDataInputPart, FileReferenceInputPart]

class StructuredAgentInput(BaseModel):
    """
    Represents structured input to the agent, potentially including a main query
    and a list of various content parts.
    """
    query: Optional[str] = None # Optional main text query.
                                # If parts also contain text, agent logic should decide how to combine/prioritize.
    parts: List[AgentInputPartUnion] = Field(default_factory=list)
    system_prompt: Optional[str] = None # Optional system prompt to set or override for this session
    agent_config: Optional[AgentConfig] = None # Optional configuration settings for agent behavior
    # # session_id is handled by the server and passed directly to agent methods, not part of this model.

class MediaPartType(BaseModel):
    """New output part type for images and videos from image detection"""
    type: Literal["media"] = "media"
    name: str
    mime_type: str
    content: Optional[str] = Field(None, description="Binary content as base64 string (optional)")
    url: Optional[str] = Field(None, description="Media URL (optional)")
    
    @model_validator(mode='before')
    @classmethod
    def validate_at_least_one_source(cls, data: Any) -> Any:
        """Ensure either content or url is present."""
        if isinstance(data, dict):
            if not ('content' in data or 'url' in data):
                raise ValueError('Either content or url must be present')
        return data
    
    def set_binary_content(self, binary_data: bytes):
        """Helper method to set binary content as base64"""
        self.content = base64.b64encode(binary_data).decode('utf-8')
    
    def get_binary_content(self) -> Optional[bytes]:
        """Helper method to get binary content from base64"""
        if self.content is None:
            return None
        try:
            return base64.b64decode(self.content)
        except Exception:
            return None

class MermaidOutputPart(BaseModel):
    type: Literal["mermaid_diagram"] = "mermaid_diagram"
    definition: str # The Mermaid syntax string
    width: Optional[str] = None      # e.g., "600px", "100%"
    height: Optional[str] = None     # e.g., "400px", "auto"
    max_width: Optional[str] = None  # e.g., "800px"
    max_height: Optional[str] = None # e.g., "600px"

class ChartJsOutputPart(BaseModel):
    type: Literal["chart_js"] = "chart_js"
    config: Dict[str, Any] # The Chart.js configuration object
    width: Optional[str] = None      # Suggestion for container/canvas style
    height: Optional[str] = None
    max_width: Optional[str] = None
    max_height: Optional[str] = None

class TableDataOutputPart(BaseModel):
    type: Literal["table_data"] = "table_data"
    caption: Optional[str] = None
    headers: List[str]
    rows: List[List[Any]]

class FormDefinitionOutputPart(BaseModel):
    type: Literal["form_definition"] = "form_definition"
    definition: Dict[str, Any] # The formDefinition object as expected by the frontend

class OptionsBlockOutputPart(BaseModel):
    type: Literal["options_block"] = "options_block"
    definition: Dict[str, Any] # The optionsblock JSON object as expected by the frontend

class FileDownloadLinkOutputPart(BaseModel):
    type: Literal["file_download_link"] = "file_download_link"
    file_id: str
    label: str
    action: Literal["download", "preview"] = "download"
    icon: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

AgentOutputPartUnion = Union[
    TextOutputPart,
    TextOutputStreamPart,
    JsonOutputPart,
    YamlOutputPart,
    FileContentOutputPart,
    FileReferenceOutputPart,
    MediaPartType,
    MermaidOutputPart,
    ChartJsOutputPart,
    TableDataOutputPart,
    FormDefinitionOutputPart,
    OptionsBlockOutputPart,
    FileDownloadLinkOutputPart,
]

class StructuredAgentOutput(BaseModel):
    """
    Represents structured output from the agent.
    It can contain a primary textual response and a list of additional structured parts.
    """
    # Primary text response, often the main conversational reply.
    # This can be derived from a TextOutputPart or be a separate consolidated summary.
    response_text: Optional[str] = None
    parts: List[AgentOutputPartUnion] = Field(default_factory=list)



class AgentInterface(abc.ABC):
    """Abstract interface for conversational agents."""

    @abc.abstractmethod
    async def get_metadata(self) -> Dict[str, Any]:
        """Returns metadata about the agent (name, description, capabilities)."""
        pass

    @abc.abstractmethod
    async def get_state(self) -> Dict[str, Any]:
        """
        Retrieves the current state of the agent as a JSON-serializable dictionary.
        This state includes all necessary information to restore the agent later.
        """
        pass

    @abc.abstractmethod
    async def load_state(self, state: Dict[str, Any]):
        """
        Loads the agent's state from a dictionary. This method is called to restore
        the agent to a previous state.
        
        Args:
            state: A JSON-serializable dictionary representing the agent's state.
        """
        pass

    async def get_system_prompt(self) -> Optional[str]:
        """
        Returns the default system prompt for the agent.
        
        This method is optional - agents can override it to provide a default system prompt.
        If not overridden, returns None, indicating no default system prompt is configured.
        
        Returns:
            The default system prompt string, or None if no default is configured.
        """
        return None

    async def get_current_model(self, session_id: str) -> Optional[str]:
        """
        Returns the name/identifier of the model currently being used by the agent for a specific session.
        This method should return the model that would be used for the next request in that session.
        
        The implementation should account for:
        - Any session-specific model overrides
        - Agent-specific model preferences
        - Fallback to default model if none specified
        
        Args:
            session_id: The session identifier
            
        Returns:
            Optional[str]: The model identifier/name, or None if not applicable
        """
        return None

    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """
        Configure the agent with session-level settings (system prompt, model config, etc.).
        This method is called by AgentManager after agent creation but before state loading.
        
        Args:
            session_configuration: Dictionary containing:
                - system_prompt: Optional[str] - Custom system prompt for this session
                - model_name: Optional[str] - Model to use for this session
                - model_config: Optional[Dict] - Model configuration parameters
        """
        # Default implementation does nothing - agents can override to handle configuration
        pass

    async def process_file_inputs(
        self,
        agent_input: StructuredAgentInput,
        session_id: str,
        user_id: str = "default_user",
        store_files: bool = True,
        include_text_content: bool = True,
        convert_to_markdown: bool = True,
        enable_multimodal_processing: bool = True,
        enable_progress_tracking: bool = True
    ) -> tuple[StructuredAgentInput, List[Dict[str, Any]]]:
        """
        Process FileDataInputPart in agent input and optionally store files.
        
        This is a convenience method that uses the framework's file processing utilities.
        Agents can override this method to customize file processing behavior.
        
        The default implementation:
        1. Looks for a file_storage_manager attribute on the agent
        2. Uses the framework's process_file_inputs utility
        3. Converts FileDataInputPart to TextInputPart for easier agent processing
        
        Args:
            agent_input: The original StructuredAgentInput with potential FileDataInputPart
            session_id: Session ID for file storage
            user_id: User ID for file storage (default: "default_user")
            store_files: Whether to store files persistently (default: True)
            include_text_content: Whether to include text file content inline (default: True)
            
        Returns:
            Tuple containing:
            - Modified StructuredAgentInput with files converted to text
            - List of file metadata dictionaries
            
        Example:
            ```python
            # In your agent's handle_message method:
            processed_input, files = await self.process_file_inputs(agent_input, session_id)
            # Now use processed_input which has files as TextInputPart
            ```
        """
        # Import here to avoid circular imports
        from .file_system_management import process_file_inputs
        
        # Try to find file storage manager on the agent
        file_storage_manager = getattr(self, 'file_storage_manager', None) or getattr(self, '_file_storage_manager', None)
        
        return await process_file_inputs(
            agent_input=agent_input,
            file_storage_manager=file_storage_manager,
            user_id=user_id,
            session_id=session_id,
            store_files=store_files,
            include_text_content=include_text_content,
            convert_to_markdown=convert_to_markdown,
            enable_multimodal_processing=enable_multimodal_processing,
            enable_progress_tracking=enable_progress_tracking
        )

    # --- Methods that subclasses must implement ---
    @abc.abstractmethod
    async def handle_message(self, session_id: str, agent_input: StructuredAgentInput) -> StructuredAgentOutput:
        """
        Handles a user message (potentially multimodal and structured) in non-streaming mode.

        Args:
            session_id: The unique identifier for the current conversation session.
            agent_input: A StructuredAgentInput object containing the user's query and content parts.

        Returns:
            A StructuredAgentOutput object containing the agent's complete response.
        """
        pass

    async def handle_message_stream(
        self, session_id: str, agent_input: StructuredAgentInput
    ) -> AsyncGenerator[StructuredAgentOutput, None]:
        """
        Handles a user message in streaming mode, yielding responses as they become available.

        This default implementation provides a non-streaming fallback by calling
        `handle_message` and yielding its result once. Agents that support true
        streaming should override this method.

        Args:
            session_id: The unique identifier for the current conversation session.
            agent_input: A StructuredAgentInput object containing the user's query and content parts.

        Yields:
            A StructuredAgentOutput object for each part of the response.
        """
        result = await self.handle_message(session_id, agent_input)
        yield result

# Streaming functionality removed as per PRD requirements 
#TODO: Add streaming functionality under some form