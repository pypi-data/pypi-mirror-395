"""
Agent Framework Library

A comprehensive Python framework for building and serving conversational AI agents with FastAPI.

This framework provides:
- Abstract interfaces for building custom AI agents
- Multiple storage backends (local, S3, MinIO) for file management
- Session management with MongoDB and in-memory storage options
- Multimodal processing capabilities for text, images, and documents
- Structured input/output handling with Pydantic models
- FastAPI-based server for serving agents via REST API
- Comprehensive error handling and logging
- Support for multiple AI model providers (OpenAI, Gemini)

Key Components:
- AgentInterface: Abstract base class for implementing custom agents
- FileStorageManager: Handles file uploads, storage, and processing
- SessionStorage: Manages conversation history and agent state
- ModelConfigManager: Configures and manages AI model providers
- Server: FastAPI application for serving agents

Example Usage:
    ```python
    from agent_framework import AgentInterface, create_basic_agent_server
    
    class MyAgent(AgentInterface):
        async def handle_message(self, session_id: str, agent_input):
            return StructuredAgentOutput(response_text="Hello!")
    
    # Start server
    create_basic_agent_server(MyAgent, port=8000)
    ```

Version: 0.1.6
Author: Cinco AI Team
License: MIT
"""

import logging
import os
from typing import TYPE_CHECKING

# Create logger for this module
logger = logging.getLogger(__name__)

__version__ = "0.1.6"
__author__ = "Cinco AI Team"
__license__ = "MIT"
__email__ = "sebastian@cinco.ai"

# Core interfaces and base classes
from .core.agent_interface import (
    AgentInterface,
    StructuredAgentInput,
    StructuredAgentOutput,
    AgentConfig,
    # Input part types
    TextInputPart,
    ImageUrlInputPart,
    FileDataInputPart,
    AgentInputPartUnion,
    # Output part types
    TextOutputPart,
    TextOutputStreamPart,
    JsonOutputPart,
    YamlOutputPart,
    FileContentOutputPart,
    FileReferenceInputPart,
    FileReferenceOutputPart,
    MermaidOutputPart,
    ChartJsOutputPart,
    TableDataOutputPart,
    FormDefinitionOutputPart,
    OptionsBlockOutputPart,
    FileDownloadLinkOutputPart,
    AgentOutputPartUnion,
)

# Framework-agnostic base agent and implementations
from .core.base_agent import BaseAgent
from .implementations.llamaindex_agent import LlamaIndexAgent
from .implementations.microsoft_agent import MicrosoftAgent

# State management
from .core.state_manager import StateManager, AgentIdentity

# Agent provider
from .core.agent_provider import AgentManager

# Model configuration and clients
from .core.model_config import ModelConfigManager, ModelProvider, model_config
from .core.model_clients import ModelClientFactory, client_factory

# Session storage
from .session.session_storage import (
    SessionStorageInterface,
    SessionStorageFactory,
    SessionData,
    MessageData,
    MessageInsight,
    MessageMetadata,
    AgentLifecycleData,
    MemorySessionStorage,
    MongoDBSessionStorage,
    history_message_to_message_data,
    message_data_to_history_message,
)

# File system management (consolidated)
from .storage.file_system_management import (
    FileStorageManager, 
    FileStorageFactory, 
    process_file_inputs, 
    get_file_processing_summary, 
    FileInputMixin
)
from .storage.file_storages import (
    FileStorageInterface, 
    FileMetadata, 
    LocalFileStorage
)

# Optional file storage backends (only available if dependencies are installed)
try:
    from .storage.file_storages import S3FileStorage, S3_AVAILABLE
except ImportError:
    S3FileStorage = None
    S3_AVAILABLE = False

try:
    from .storage.file_storages import MinIOFileStorage, MINIO_AVAILABLE
except ImportError:
    MinIOFileStorage = None
    MINIO_AVAILABLE = False

# Server application
from .web.server import app, start_server

# Convenience imports for common use cases
__all__ = [
    # Version info
    "__version__",
    "__author__",
    
    # Core interfaces
    "AgentInterface",
    "StructuredAgentInput", 
    "StructuredAgentOutput",
    "AgentConfig",
    
    # Base implementations
    "BaseAgent",
    "LlamaIndexAgent",
    "MicrosoftAgent",
    "StateManager",
    "AgentIdentity",
    "AgentManager",
    
    # Input/Output types
    "TextInputPart",
    "ImageUrlInputPart", 
    "FileDataInputPart",
    "AgentInputPartUnion",
    "TextOutputPart",
    "TextOutputStreamPart",
    "JsonOutputPart",
    "YamlOutputPart", 
    "FileContentOutputPart",
    "FileReferenceInputPart",
    "FileReferenceOutputPart",
    "MermaidOutputPart",
    "ChartJsOutputPart",
    "TableDataOutputPart",
    "FormDefinitionOutputPart",
    "OptionsBlockOutputPart",
    "FileDownloadLinkOutputPart",
    "AgentOutputPartUnion",
    
    # Model configuration
    "ModelConfigManager",
    "ModelProvider", 
    "model_config",
    "ModelClientFactory",
    "client_factory",
    
    # Session storage
    "SessionStorageInterface",
    "SessionStorageFactory",
    "SessionData",
    "MessageData",
    "MessageInsight", 
    "MessageMetadata",
    "AgentLifecycleData",
    "MemorySessionStorage",
    "MongoDBSessionStorage",
    "history_message_to_message_data",
    "message_data_to_history_message",
    
    # File storage implementations (consolidated)
    "FileStorageInterface",
    "FileMetadata", 
    "LocalFileStorage",
    "S3FileStorage",
    "MinIOFileStorage",
    "S3_AVAILABLE",
    "MINIO_AVAILABLE",
    
    # File system management (consolidated)
    "FileStorageManager",
    "FileStorageFactory", 
    "process_file_inputs",
    "get_file_processing_summary",
    "FileInputMixin",
    
    # Server
    "app",
    "start_server",
    
    # Convenience functions
    "create_basic_agent_server",
]

# Quick start function for convenience
def create_basic_agent_server(
    agent_class: type[AgentInterface], 
    host: str = "0.0.0.0", 
    port: int = 8000, 
    reload: bool = False
) -> None:
    """
    Quick start function to create and run an agent server.
    
    This function allows external projects to quickly start an agent server
    without needing to create their own server.py file or set environment variables.
    
    Args:
        agent_class: The agent class that implements AgentInterface
        host: Host to bind the server to (default: "0.0.0.0")
        port: Port to run the server on (default: 8000)
        reload: Whether to enable auto-reload for development (default: False)
                Note: When reload=True, the agent class is temporarily stored in an 
                environment variable to survive module reloads.
    
    Returns:
        None (starts the server and blocks)
    
    Raises:
        ImportError: If uvicorn is not available
        ValueError: If agent_class does not implement AgentInterface
    
    Example:
        >>> from agent_framework import create_basic_agent_server, AgentInterface
        >>> from my_agent import MyAgent
        >>> create_basic_agent_server(MyAgent, port=8001)
    """
    try:
        import uvicorn
    except ImportError as e:
        raise ImportError(
            "uvicorn is required to run the server. Install it with: uv add uvicorn"
        ) from e
    
    # Validate that agent_class implements AgentInterface
    if not issubclass(agent_class, AgentInterface):
        raise ValueError(
            f"agent_class must implement AgentInterface, got {agent_class.__name__}"
        )
    
    # Store the agent class globally for immediate use
    from .web import server
    server._GLOBAL_AGENT_CLASS = agent_class
    
    # If reload is enabled, also store in environment variable to survive reloads
    # We use the class's module and name to recreate the import path
    if reload:
        module_name = agent_class.__module__
        class_name = agent_class.__name__
        agent_class_path = f"{module_name}:{class_name}"
        os.environ["AGENT_CLASS_PATH"] = agent_class_path
        logger.info(f"[create_basic_agent_server] Reload enabled. Set AGENT_CLASS_PATH={agent_class_path}")
    
    logger.info(f"[create_basic_agent_server] Starting server for {agent_class.__name__} on {host}:{port}")
    logger.info(f"[create_basic_agent_server] Reload: {reload}")
    
    # When reload=True, uvicorn requires an import string, not the app object directly
    if reload:
        # Use the agent_framework.web.server:app import string for reload mode
        uvicorn.run(
            "agent_framework.web.server:app",
            host=host,
            port=port,
            reload=reload
        )
    else:
        # Import the app after setting the global variable for non-reload mode
        from .web.server import app
        # For non-reload mode, we can pass the app object directly
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=reload
        ) 