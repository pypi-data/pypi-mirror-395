"""
Session Storage Abstraction Layer

This module provides an extensible session storage system that supports multiple backends:
- In-memory storage (default, for development and small deployments)
- MongoDB storage (for production and distributed deployments)

The storage backend can be configured via environment variables.

Key Components:
- SessionStorageInterface: Abstract interface for storage backends
- SessionData: Session metadata and configuration
- MessageData: Individual message storage
- MessageInsight: AI-derived insights from messages
- MessageMetadata: Additional message annotations
- AgentLifecycleData: Agent lifecycle event tracking

Environment Variables:
- SESSION_STORAGE_TYPE: "memory" or "mongodb" (default: "memory")
- MONGODB_URL: MongoDB connection string (for MongoDB backend)
- MONGODB_DATABASE: Database name (default: "agent_framework")
- MONGODB_COLLECTION_PREFIX: Collection name prefix (default: "sessions")

Example:
    ```python
    from agent_framework.session_storage import SessionStorageFactory
    
    # Create storage backend
    storage = await SessionStorageFactory.create_storage()
    
    # Save session
    session_data = SessionData(session_id="123", user_id="user1", ...)
    await storage.save_session("user1", "123", session_data)
    ```

Version: 0.1.6
"""

import os
import json
import logging
import asyncio
import uuid
import gzip
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Any, Union, Final, TYPE_CHECKING
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# FastAPI/Pydantic imports
from pydantic import BaseModel

# MongoDB availability flag
MONGODB_AVAILABLE: bool = False
try:
    # We check for availability but don't import globally anymore
    import motor
    MONGODB_AVAILABLE = True
except ImportError:
    pass

# Elasticsearch availability flag
ELASTICSEARCH_AVAILABLE: bool = False
try:
    import elasticsearch
    ELASTICSEARCH_AVAILABLE = True
except ImportError:
    pass

if TYPE_CHECKING:
    from .agent_interface import AgentInterface

logger = logging.getLogger(__name__)

# Import configuration (fallback to defaults if config file not available)
# This part is being moved to autogen_state_manager.py
# try:
#     from ..docs.mongodb_state_config import (
#         MAX_STATE_SIZE_MB, MAX_CONVERSATION_HISTORY, ENABLE_STATE_COMPRESSION,
#         COMPRESSION_THRESHOLD_MB, COMPRESSION_EFFICIENCY_THRESHOLD,
#         AGGRESSIVE_TRUNCATION_THRESHOLD
#     )
# except ImportError:
#     # Fallback configuration if config file is not available
#     MAX_STATE_SIZE_MB = 12
#     MAX_CONVERSATION_HISTORY = 100
#     ENABLE_STATE_COMPRESSION = True
#     COMPRESSION_THRESHOLD_MB = 1.0
#     COMPRESSION_EFFICIENCY_THRESHOLD = 0.8
#     AGGRESSIVE_TRUNCATION_THRESHOLD = 20


@dataclass
class SessionData:
    """
    Represents session metadata only (not including message history).
    
    This class stores all session-level information including agent configuration,
    user preferences, and session-specific settings.
    
    Attributes:
        session_id: Unique identifier for the session
        user_id: Identifier for the user who owns this session
        agent_instance_config: Configuration for the agent instance
        correlation_id: Optional correlation ID for tracking across systems
        created_at: ISO timestamp when session was created
        updated_at: ISO timestamp when session was last updated
        metadata: Additional session metadata
        agent_id: Unique identifier for the agent instance (multi-agent support)
        agent_type: Agent class name for type identification
        session_configuration: Session-level agent behavior configuration
        session_label: User-defined label for the session
    """
    session_id: str
    user_id: str
    agent_instance_config: Dict[str, Any]
    correlation_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    # Agent identity fields for multi-agent support
    agent_id: Optional[str] = None  # Unique identifier for the agent instance
    agent_type: Optional[str] = None  # Agent class name
    # Session-level configuration for agent behavior
    session_configuration: Optional[Dict[str, Any]] = None  # Stores system_prompt, model_name, model_config
    # User-defined label for the session
    session_label: Optional[str] = None

    def __post_init__(self) -> None:
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def get_session_system_prompt(self) -> Optional[str]:
        """
        Extract system prompt from session configuration.
        
        Returns:
            The system prompt string if configured, None otherwise
        """
        if not self.session_configuration:
            return None
        return self.session_configuration.get("system_prompt")
    
    def get_session_model_config(self) -> Optional[Dict[str, Any]]:
        """
        Extract model configuration from session configuration.
        
        Returns:
            Dictionary of model configuration parameters, empty dict if none configured
        """
        if not self.session_configuration:
            return None
        return self.session_configuration.get("model_config", {})
    
    def get_session_model_name(self) -> Optional[str]:
        """
        Extract model name from session configuration.
        
        Returns:
            The model name string if configured, None otherwise
        """
        if not self.session_configuration:
            return None
        return self.session_configuration.get("model_name")
    
    def get_display_name(self) -> str:
        """
        Get the display name for the session (label or truncated ID).
        
        Returns:
            User-defined label if available, otherwise truncated session ID
        """
        if self.session_label and self.session_label.strip():
            return self.session_label.strip()
        # Return truncated session ID as fallback
        return f"{self.session_id[:8]}..."


@dataclass
class MessageData:
    """
    Represents an individual message (user input or agent response).
    
    This class stores all information about a single message in a conversation,
    including content, metadata, processing information, and relationships.
    
    Attributes:
        message_id: Unique identifier for this message
        session_id: Session this message belongs to
        user_id: User who owns the session
        interaction_id: Links user input with corresponding agent response
        sequence_number: Order of this message in the conversation
        message_type: Type of message ("user_input" or "agent_response")
        role: Message role for conversation context
        text_content: Main text content of the message
        parts: Structured parts of the message (multimodal content)
        response_text_main: Primary response text (for agent responses)
        created_at: ISO timestamp when message was created
        processed_at: ISO timestamp when message processing completed
        parent_message_id: ID of parent message (for threading)
        related_message_ids: IDs of related messages
        processing_time_ms: Time taken to process this message
        model_used: AI model used to generate response (for agent messages)
        token_count: Token usage statistics
        agent_id: Agent instance identifier (multi-agent support)
        agent_type: Agent class name
    """
    message_id: str
    session_id: str
    user_id: str
    interaction_id: str  # Links user input + agent response
    sequence_number: int
    message_type: str  # "user_input" or "agent_response"
    
    # Message content
    role: str
    text_content: Optional[str] = None
    parts: Optional[List[Dict[str, Any]]] = None
    response_text_main: Optional[str] = None
    
    # Timestamps
    created_at: Optional[str] = None
    processed_at: Optional[str] = None
    
    # Relationships
    parent_message_id: Optional[str] = None
    related_message_ids: List[str] = field(default_factory=list)
    
    # Processing metadata
    processing_time_ms: Optional[int] = None
    model_used: Optional[str] = None
    token_count: Optional[Dict[str, int]] = None
    # Agent identity fields for multi-agent support
    agent_id: Optional[str] = None  # Unique identifier for the agent instance
    agent_type: Optional[str] = None  # Agent class name

    def __post_init__(self) -> None:
        """Initialize created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class MessageInsight:
    """
    Represents insights derived from a message.
    
    This class stores AI-generated insights about messages, such as sentiment analysis,
    intent detection, topic extraction, or other analytical results.
    
    Attributes:
        insight_id: Unique identifier for this insight
        message_id: ID of the message this insight relates to
        session_id: Session the message belongs to
        user_id: User who owns the session
        insight_type: Type of insight ("sentiment", "intent_analysis", "topic_extraction", etc.)
        insight_data: The actual insight data and results
        created_at: ISO timestamp when insight was created
        created_by: System or agent that created this insight
        agent_id: Agent instance identifier (multi-agent support)
        agent_type: Agent class name
    """
    insight_id: str
    message_id: str
    session_id: str
    user_id: str
    insight_type: str  # "sentiment", "intent_analysis", "topic_extraction", etc.
    insight_data: Dict[str, Any]
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    # Agent identity fields for multi-agent support  
    agent_id: Optional[str] = None  # Unique identifier for the agent instance
    agent_type: Optional[str] = None  # Agent class name

    def __post_init__(self) -> None:
        """Initialize created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class MessageMetadata:
    """
    Represents additional metadata/annotations for a message.
    
    This class stores supplementary information about messages, such as user feedback,
    quality scores, debug information, or other annotations.
    
    Attributes:
        metadata_id: Unique identifier for this metadata entry
        message_id: ID of the message this metadata relates to
        session_id: Session the message belongs to
        metadata_type: Type of metadata ("user_feedback", "quality_score", "debug_info", etc.)
        metadata: The actual metadata content
        created_at: ISO timestamp when metadata was created
        created_by: System or user that created this metadata
        agent_id: Agent instance identifier (multi-agent support)
        agent_type: Agent class name
    """
    metadata_id: str
    message_id: str
    session_id: str
    metadata_type: str  # "user_feedback", "quality_score", "debug_info", etc.
    metadata: Dict[str, Any]
    created_at: Optional[str] = None
    created_by: Optional[str] = None
    # Agent identity fields for multi-agent support
    agent_id: Optional[str] = None  # Unique identifier for the agent instance  
    agent_type: Optional[str] = None  # Agent class name

    def __post_init__(self) -> None:
        """Initialize created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class AgentLifecycleData:
    """
    Tracks agent lifecycle events.
    
    This class records important events in an agent's lifecycle for monitoring,
    debugging, and analytics purposes.
    
    Attributes:
        lifecycle_id: Unique identifier for this lifecycle event
        agent_id: Unique identifier for the agent instance
        agent_type: Agent class name
        event_type: Type of event ("created", "session_started", "session_ended", "state_saved", "state_loaded")
        session_id: Session ID if event is session-related
        user_id: User ID if event is user-related
        timestamp: ISO timestamp when event occurred
        metadata: Additional event-specific metadata
    """
    lifecycle_id: str
    agent_id: str
    agent_type: str
    event_type: str  # "created", "session_started", "session_ended", "state_saved", "state_loaded"
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Generate lifecycle_id if not provided."""
        if not self.lifecycle_id:
            self.lifecycle_id = str(uuid.uuid4())


class SessionStorageInterface(ABC):
    """
    Abstract interface for session storage backends.
    
    This interface defines the contract that all session storage implementations
    must follow. It supports session management, message storage, insights,
    metadata, and multi-agent scenarios.
    
    Implementations should handle:
    - Session lifecycle management
    - Message storage and retrieval
    - Conversation history with pagination
    - Insights and metadata storage
    - Multi-agent support
    - User and session management
    """

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Initialize the storage backend.
        
        Returns:
            True if initialization successful, False otherwise
        """
        pass

    @abstractmethod
    async def save_session(self, user_id: str, session_id: str, session_data: SessionData) -> bool:
        """
        Save session metadata.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            session_data: Session data to save
            
        Returns:
            True if save successful, False otherwise
        """
        pass

    @abstractmethod
    async def load_session(self, user_id: str, session_id: str) -> Optional[SessionData]:
        """
        Load session metadata.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            SessionData if found, None otherwise
        """
        pass

    @abstractmethod
    async def delete_session(self, user_id: str, session_id: str) -> bool:
        """
        Delete session and all related messages.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            True if deletion successful, False otherwise
        """
        pass

    @abstractmethod
    async def list_user_sessions(self, user_id: str) -> List[str]:
        """
        List all session IDs for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of session IDs
        """
        pass

    @abstractmethod
    async def list_all_users_with_sessions(self) -> List[str]:
        """
        List all user IDs who have at least one session.
        
        Returns:
            List of user IDs
        """
        pass

    @abstractmethod
    async def add_message(self, message_data: MessageData) -> bool:
        """
        Add a message to the storage.
        
        Args:
            message_data: Message data to store
            
        Returns:
            True if addition successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_conversation_history(
        self, 
        session_id: str, 
        limit: Optional[int] = None, 
        offset: Optional[int] = None
    ) -> List[MessageData]:
        """
        Get conversation history with pagination.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of messages to return
            offset: Number of messages to skip
            
        Returns:
            List of MessageData objects
        """
        pass

    @abstractmethod
    async def get_last_conversation_exchanges(
        self, 
        session_id: str, 
        limit: int = 10
    ) -> List[List[MessageData]]:
        """
        Get last N conversation exchanges (grouped by interaction_id).
        
        Args:
            session_id: Session identifier
            limit: Number of exchanges to return
            
        Returns:
            List of exchanges, each exchange is a list of related messages
        """
        pass

    @abstractmethod
    async def add_insight(self, insight: MessageInsight) -> bool:
        """
        Add an insight for a message.
        
        Args:
            insight: Insight data to store
            
        Returns:
            True if addition successful, False otherwise
        """
        pass

    @abstractmethod
    async def add_metadata(self, metadata: MessageMetadata) -> bool:
        """
        Add metadata for a message.
        
        Args:
            metadata: Metadata to store
            
        Returns:
            True if addition successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_message_with_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get message with all its insights and metadata.
        
        Args:
            message_id: Message identifier
            
        Returns:
            Dictionary containing message, insights, and metadata, or None if not found
        """
        pass

    @abstractmethod
    async def update_session_metadata(
        self, 
        user_id: str, 
        session_id: str, 
        correlation_id: Optional[str] = None, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update session metadata.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            correlation_id: Optional correlation ID to set
            metadata: Optional metadata to update
            
        Returns:
            True if update successful, False otherwise
        """
        pass

    @abstractmethod
    async def update_session_label(self, user_id: str, session_id: str, label: str) -> bool:
        """
        Update the session label.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            label: New label for the session
            
        Returns:
            True if update successful, False otherwise
        """
        pass

    @abstractmethod
    async def list_user_sessions_with_info(self, user_id: str) -> List[Dict[str, Any]]:
        """
        List all sessions for a user with metadata including labels.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of dictionaries containing session information
        """
        pass

    # Agent identity query methods
    @abstractmethod
    async def list_sessions_by_agent_id(self, agent_id: str) -> List[str]:
        """List all session IDs for a specific agent."""
        pass

    @abstractmethod
    async def list_sessions_by_agent_type(self, agent_type: str) -> List[str]:
        """List all session IDs for a specific agent type."""
        pass

    @abstractmethod
    async def get_user_sessions_by_agent(self, user_id: str, agent_id: Optional[str] = None, 
                                       agent_type: Optional[str] = None) -> List[str]:
        """Get user sessions filtered by agent identity."""
        pass

    @abstractmethod
    async def save_agent_state(self, session_id: str, agent_state: Dict[str, Any]) -> bool:
        """Saves the agent's state, separate from session metadata."""
        pass

    @abstractmethod
    async def load_agent_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Loads the agent's state."""
        pass

    @abstractmethod
    async def load_session_configuration(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session configuration (system_prompt, model_name, model_config) for a session."""
        pass

    @abstractmethod
    async def add_agent_lifecycle_event(self, lifecycle_data: AgentLifecycleData) -> bool:
        """Add an agent lifecycle event to storage"""
        pass

    @abstractmethod
    async def get_agent_lifecycle_events(self, agent_id: str) -> List[AgentLifecycleData]:
        """Get lifecycle events for a specific agent"""
        pass

    @abstractmethod
    async def get_agent_usage_statistics(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """Get usage statistics by agent type"""
        pass

    async def cleanup(self) -> None:
        """Clean up resources."""
        pass


class MemorySessionStorage(SessionStorageInterface):
    """
    In-memory session storage for development and single-instance deployments.
    """

    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}  # {user_id_session_id: SessionData}
        self.messages: Dict[str, MessageData] = {}  # {message_id: MessageData}
        self.insights: Dict[str, List[MessageInsight]] = {}  # {message_id: [MessageInsight]}
        self.metadata: Dict[str, List[MessageMetadata]] = {}  # {message_id: [MessageMetadata]}
        self.sequence_counters: Dict[str, int] = {}  # {session_id: current_sequence}
        self.agent_states: Dict[str, Dict[str, Any]] = {} # {session_id: agent_state}

    async def initialize(self) -> bool:
        """Initialize memory storage."""
        logger.debug("Initialized MemorySessionStorage with message-per-document structure")
        return True

    def _session_key(self, user_id: str, session_id: str) -> str:
        return f"{user_id}_{session_id}"

    async def save_session(self, user_id: str, session_id: str, session_data: SessionData) -> bool:
        """Save session metadata."""
        try:
            session_key = self._session_key(user_id, session_id)
            session_data.updated_at = datetime.now(timezone.utc).isoformat()
            self.sessions[session_key] = session_data
            logger.debug(f"Saved session {session_id} for user {user_id} to memory")
            return True
        except Exception as e:
            logger.error(f"Failed to save session {session_id} for user {user_id} to memory: {e}")
            return False

    async def load_session(self, user_id: str, session_id: str) -> Optional[SessionData]:
        """Load session metadata."""
        try:
            session_key = self._session_key(user_id, session_id)
            return self.sessions.get(session_key)
        except Exception as e:
            logger.error(f"Failed to load session {session_id} for user {user_id} from memory: {e}")
            return None

    async def delete_session(self, user_id: str, session_id: str) -> bool:
        """Delete session and all related messages."""
        try:
            session_key = self._session_key(user_id, session_id)
            if session_key in self.sessions:
                del self.sessions[session_key]
            
            # Delete all messages for this session
            messages_to_delete = [msg_id for msg_id, msg in self.messages.items() 
                                if msg.session_id == session_id]
            for msg_id in messages_to_delete:
                del self.messages[msg_id]
                self.insights.pop(msg_id, None)
                self.metadata.pop(msg_id, None)
            
            # Clean up sequence counter
            self.sequence_counters.pop(session_id, None)
            
            # Delete agent state
            self.agent_states.pop(session_id, None)

            logger.debug(f"Deleted session {session_id} for user {user_id} from memory")
            return True
        except Exception as e:
            logger.error(f"Failed to delete session {session_id} for user {user_id} from memory: {e}")
            return False

    async def list_user_sessions(self, user_id: str) -> List[str]:
        """List all session IDs for a user."""
        try:
            sessions = []
            for session_key, session_data in self.sessions.items():
                if session_data.user_id == user_id:
                    sessions.append(session_data.session_id)
            return sorted(sessions, key=lambda sid: self.sessions[self._session_key(user_id, sid)].updated_at, reverse=True)
        except Exception as e:
            logger.error(f"Failed to list sessions for user {user_id} from memory: {e}")
            return []

    async def list_all_users_with_sessions(self) -> List[str]:
        """List all user IDs who have at least one session."""
        return list(set(session_data.user_id for session_data in self.sessions.values()))

    async def add_message(self, message_data: MessageData) -> bool:
        """Add a message to storage."""
        try:
            # Auto-increment sequence number
            if message_data.session_id not in self.sequence_counters:
                self.sequence_counters[message_data.session_id] = 0
            self.sequence_counters[message_data.session_id] += 1
            message_data.sequence_number = self.sequence_counters[message_data.session_id]
            
            self.messages[message_data.message_id] = message_data
            logger.debug(f"Added message {message_data.message_id} to session {message_data.session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add message {message_data.message_id}: {e}")
            return False

    async def get_conversation_history(self, session_id: str, limit: Optional[int] = None, 
                                     offset: Optional[int] = None) -> List[MessageData]:
        """Get conversation history with pagination."""
        try:
            messages = [msg for msg in self.messages.values() if msg.session_id == session_id]
            messages.sort(key=lambda m: m.sequence_number)
            
            if offset:
                messages = messages[offset:]
            if limit:
                messages = messages[:limit]
            
            return messages
        except Exception as e:
            logger.error(f"Failed to get conversation history for session {session_id}: {e}")
            return []

    async def get_last_conversation_exchanges(self, session_id: str, limit: int = 10) -> List[List[MessageData]]:
        """Get last N conversation exchanges (grouped by interaction_id)."""
        try:
            messages = [msg for msg in self.messages.values() if msg.session_id == session_id]
            
            # Group by interaction_id
            exchanges = {}
            for msg in messages:
                if msg.interaction_id not in exchanges:
                    exchanges[msg.interaction_id] = []
                exchanges[msg.interaction_id].append(msg)
            
            # Sort exchanges by latest message in each exchange
            sorted_exchanges = sorted(
                exchanges.values(),
                key=lambda exchange: max(msg.sequence_number for msg in exchange),
                reverse=True
            )
            
            return sorted_exchanges[:limit]
        except Exception as e:
            logger.error(f"Failed to get conversation exchanges for session {session_id}: {e}")
            return []

    async def add_insight(self, insight: MessageInsight) -> bool:
        """Add an insight for a message."""
        try:
            if insight.message_id not in self.insights:
                self.insights[insight.message_id] = []
            self.insights[insight.message_id].append(insight)
            return True
        except Exception as e:
            logger.error(f"Failed to add insight {insight.insight_id}: {e}")
            return False

    async def add_metadata(self, metadata: MessageMetadata) -> bool:
        """Add metadata for a message."""
        try:
            if metadata.message_id not in self.metadata:
                self.metadata[metadata.message_id] = []
            self.metadata[metadata.message_id].append(metadata)
            return True
        except Exception as e:
            logger.error(f"Failed to add metadata {metadata.metadata_id}: {e}")
            return False

    async def get_message_with_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get message with all its insights and metadata."""
        try:
            message = self.messages.get(message_id)
            if not message:
                return None
            
            return {
                "message": message,
                "insights": self.insights.get(message_id, []),
                "metadata": self.metadata.get(message_id, [])
            }
        except Exception as e:
            logger.error(f"Failed to get message details for {message_id}: {e}")
            return None

    async def update_session_metadata(self, user_id: str, session_id: str, 
                                    correlation_id: Optional[str] = None, 
                                    metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update session metadata."""
        try:
            session_key = self._session_key(user_id, session_id)
            session_data = self.sessions.get(session_key)
            if not session_data:
                return False
            
            session_data.updated_at = datetime.now(timezone.utc).isoformat()
            
            if correlation_id is not None:
                session_data.correlation_id = correlation_id
            
            if metadata is not None:
                if session_data.metadata is None:
                    session_data.metadata = {}
                session_data.metadata.update(metadata)
            
            return True
        except Exception as e:
            logger.error(f"Failed to update session metadata for {session_id}: {e}")
            return False

    async def update_session_label(self, user_id: str, session_id: str, label: str) -> bool:
        """Update the session label."""
        try:
            session_key = self._session_key(user_id, session_id)
            session_data = self.sessions.get(session_key)
            if not session_data:
                return False
            session_data.session_label = label
            session_data.updated_at = datetime.now(timezone.utc).isoformat()
            return True
        except Exception as e:
            logger.error(f"Failed to update session label for {session_id}: {e}")
            return False

    async def list_user_sessions_with_info(self, user_id: str) -> List[Dict[str, Any]]:
        """List all sessions for a user with metadata including labels."""
        sessions_info = []
        for session_key, session_data in self.sessions.items():
            if session_data.user_id == user_id:
                sessions_info.append({
                    "session_id": session_data.session_id,
                    "session_label": session_data.session_label,
                    "created_at": session_data.created_at,
                    "updated_at": session_data.updated_at,
                    "correlation_id": session_data.correlation_id,
                    "metadata": session_data.metadata,
                    "agent_id": session_data.agent_id,
                    "agent_type": session_data.agent_type,
                    "session_configuration": session_data.session_configuration
                })
        return sorted(sessions_info, key=lambda s: s["updated_at"], reverse=True)

    # Agent identity query methods
    async def list_sessions_by_agent_id(self, agent_id: str) -> List[str]:
        """List all session IDs for a specific agent."""
        matching_sessions = []
        for session_data in self.sessions.values():
            if hasattr(session_data, 'agent_id') and session_data.agent_id == agent_id:
                matching_sessions.append(session_data.session_id)
        return matching_sessions

    async def list_sessions_by_agent_type(self, agent_type: str) -> List[str]:
        """List all session IDs for a specific agent type."""
        matching_sessions = []
        for session_data in self.sessions.values():
            if hasattr(session_data, 'agent_type') and session_data.agent_type == agent_type:
                matching_sessions.append(session_data.session_id)
        return matching_sessions

    async def get_user_sessions_by_agent(self, user_id: str, agent_id: Optional[str] = None, 
                                       agent_type: Optional[str] = None) -> List[str]:
        """Get user sessions filtered by agent identity."""
        matching_sessions = []
        for session_data in self.sessions.values():
            if session_data.user_id != user_id:
                continue
            
            if agent_id and hasattr(session_data, 'agent_id') and session_data.agent_id != agent_id:
                continue
                
            if agent_type and hasattr(session_data, 'agent_type') and session_data.agent_type != agent_type:
                continue
                
            matching_sessions.append(session_data.session_id)
        return matching_sessions

    async def save_agent_state(self, session_id: str, agent_state: Dict[str, Any]) -> bool:
        """Saves the agent's state in memory."""
        try:
            self.agent_states[session_id] = agent_state
            logger.debug(f"Saved agent state for session {session_id} to memory.")
            return True
        except Exception as e:
            logger.error(f"Failed to save agent state for session {session_id} to memory: {e}")
            return False

    async def load_agent_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Loads the agent's state from memory."""
        try:
            return self.agent_states.get(session_id)
        except Exception as e:
            logger.error(f"Failed to load agent state for session {session_id} from memory: {e}")
            return None

    async def load_session_configuration(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session configuration (system_prompt, model_name, model_config) for a session."""
        session_key = self._session_key(user_id, session_id)
        session_data = self.sessions.get(session_key)
        if not session_data:
            return None
        return session_data.session_configuration

    async def add_agent_lifecycle_event(self, lifecycle_data: AgentLifecycleData) -> bool:
        """Add an agent lifecycle event to storage"""
        try:
            if not hasattr(self, 'lifecycle_events'):
                self.lifecycle_events: Dict[str, List[AgentLifecycleData]] = {}
            
            agent_id = lifecycle_data.agent_id
            if agent_id not in self.lifecycle_events:
                self.lifecycle_events[agent_id] = []
            
            self.lifecycle_events[agent_id].append(lifecycle_data)
            logger.debug(f"Added lifecycle event: {lifecycle_data.event_type} for agent {agent_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding lifecycle event: {e}")
            return False

    async def get_agent_lifecycle_events(self, agent_id: str) -> List[AgentLifecycleData]:
        """Get lifecycle events for a specific agent"""
        if not hasattr(self, 'lifecycle_events'):
            self.lifecycle_events: Dict[str, List[AgentLifecycleData]] = {}
        
        return self.lifecycle_events.get(agent_id, [])

    async def get_agent_usage_statistics(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """Get usage statistics by agent type"""
        stats = {
            "total_agents": 0,
            "total_sessions": 0,
            "total_messages": 0,
            "agent_types": {},
            "lifecycle_events": {}
        }
        
        # Count sessions by agent type
        for session_data in self.sessions.values():
            if session_data.agent_type:
                if session_data.agent_type not in stats["agent_types"]:
                    stats["agent_types"][session_data.agent_type] = {
                        "session_count": 0,
                        "unique_agents": set()
                    }
                stats["agent_types"][session_data.agent_type]["session_count"] += 1
                if session_data.agent_id:
                    stats["agent_types"][session_data.agent_type]["unique_agents"].add(session_data.agent_id)
        
        # Convert sets to counts
        for agent_type_data in stats["agent_types"].values():
            agent_type_data["unique_agents"] = len(agent_type_data["unique_agents"])
        
        # Count lifecycle events
        if hasattr(self, 'lifecycle_events'):
            for agent_id, events in self.lifecycle_events.items():
                for event in events:
                    event_type = event.event_type
                    if event_type not in stats["lifecycle_events"]:
                        stats["lifecycle_events"][event_type] = 0
                    stats["lifecycle_events"][event_type] += 1
        
        stats["total_sessions"] = len(self.sessions)
        stats["total_messages"] = len(self.messages)
        stats["total_agents"] = len(set(session_data.agent_id for session_data in self.sessions.values() if session_data.agent_id))
        
        # Filter by agent type if specified
        if agent_type and agent_type in stats["agent_types"]:
            return {
                "agent_type": agent_type,
                "session_count": stats["agent_types"][agent_type]["session_count"],
                "unique_agents": stats["agent_types"][agent_type]["unique_agents"]
            }
        
        return stats

    async def cleanup(self) -> None:
        """Clear all in-memory data."""
        self.sessions = {}
        self.messages = {}
        self.insights = {}
        self.metadata = {}
        self.agent_states = {}
        if hasattr(self, 'lifecycle_events'):
            self.lifecycle_events = {}
        logger.info("In-memory session storage cleared")


class MongoDBSessionStorage(SessionStorageInterface):
    """
    Session storage backend using MongoDB for persistent and scalable storage.
    """

    def __init__(self, connection_string: str = None, database_name: str = None):
        """
        Initialize MongoDB session storage.
        """
        if not MONGODB_AVAILABLE:
            raise ImportError("MongoDB dependencies (motor, pymongo) are not installed.")
        
        # Dynamic imports are now inside the method that needs them
        self.connection_string = connection_string or os.getenv("MONGODB_CONNECTION_STRING")
        self.database_name = database_name or os.getenv("MONGODB_DATABASE_NAME", "agent_sessions_db")
        
        if not self.connection_string:
            raise ValueError("MongoDB connection string is required.")
            
        self.client = None
        self.db = None
        self.sessions_collection = None
        self.messages_collection = None
        self.insights_collection = None
        self.metadata_collection = None
        self.agent_states_collection = None

    async def initialize(self) -> bool:
        """
        Initialize the MongoDB connection and collections.
        """
        # Import here to ensure it's only done when this class is used
        from motor.motor_asyncio import AsyncIOMotorClient
        from pymongo.errors import ConnectionFailure

        try:
            logger.debug(f"Connecting to MongoDB at {self.connection_string}...")
            self.client = AsyncIOMotorClient(self.connection_string)
            self.db = self.client[self.database_name]
            
            await self.client.admin.command('ping')
            
            self.sessions_collection = self.db["sessions"]
            self.messages_collection = self.db["messages"]
            self.insights_collection = self.db["insights"]
            self.metadata_collection = self.db["metadata"]
            self.agent_states_collection = self.db["agent_states"]
            
            logger.info(f"MongoDB connected: {self.database_name}")
            await self._create_indexes()
            return True
        except ConnectionFailure as e:
            logger.error(f"MongoDB connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during MongoDB initialization: {e}")
            return False

    async def _create_indexes(self):
        """Create indexes for optimal query performance."""
        try:
            # Sessions collection indexes
            await self.sessions_collection.create_index([("user_id", 1), ("session_id", 1)], unique=True)
            await self.sessions_collection.create_index([("correlation_id", 1)])
            await self.sessions_collection.create_index([("updated_at", -1)])
            # Agent identity indexes
            await self.sessions_collection.create_index([("agent_id", 1)])
            await self.sessions_collection.create_index([("agent_type", 1)])
            await self.sessions_collection.create_index([("user_id", 1), ("agent_id", 1)])
            await self.sessions_collection.create_index([("user_id", 1), ("agent_type", 1)])

            # Messages collection indexes
            await self.messages_collection.create_index([("session_id", 1), ("sequence_number", 1)])
            await self.messages_collection.create_index([("user_id", 1), ("created_at", -1)])
            await self.messages_collection.create_index([("interaction_id", 1)])
            await self.messages_collection.create_index([("message_id", 1)], unique=True)
            await self.messages_collection.create_index([("message_type", 1), ("session_id", 1)])
            # Agent identity indexes for messages
            await self.messages_collection.create_index([("agent_id", 1)])
            await self.messages_collection.create_index([("agent_type", 1)])
            await self.messages_collection.create_index([("user_id", 1), ("agent_id", 1), ("created_at", -1)])

            # Insights collection indexes
            await self.insights_collection.create_index([("message_id", 1), ("insight_type", 1)])
            await self.insights_collection.create_index([("session_id", 1), ("insight_type", 1)])
            await self.insights_collection.create_index([("user_id", 1), ("created_at", -1)])
            # Agent identity indexes for insights
            await self.insights_collection.create_index([("agent_id", 1)])
            await self.insights_collection.create_index([("agent_type", 1)])

            # Metadata collection indexes
            await self.metadata_collection.create_index([("message_id", 1), ("metadata_type", 1)])
            await self.metadata_collection.create_index([("session_id", 1), ("metadata_type", 1)])
            # Agent identity indexes for metadata
            await self.metadata_collection.create_index([("agent_id", 1)])
            await self.metadata_collection.create_index([("agent_type", 1)])

            # Agent states collection indexes
            await self.agent_states_collection.create_index([("session_id", 1)], unique=True)

            # Agent lifecycle collection indexes (create collection if it doesn't exist)
            lifecycle_collection = self.db["agent_lifecycle"]
            await lifecycle_collection.create_index([("agent_id", 1), ("timestamp", -1)])
            await lifecycle_collection.create_index([("agent_type", 1), ("event_type", 1)])
            await lifecycle_collection.create_index([("event_type", 1), ("timestamp", -1)])
            await lifecycle_collection.create_index([("session_id", 1)])
            await lifecycle_collection.create_index([("user_id", 1), ("timestamp", -1)])

            logger.debug("MongoDB indexes created successfully")
        except Exception as e:
            logger.debug(f"Some indexes already exist: {e}")

    def _session_document_id(self, user_id: str, session_id: str, agent_id: str) -> str:
        """
        Generate unique document ID for a session.
        Includes agent_id to prevent conflicts when multiple agents use the same session_id.
        """
        return f"{user_id}_{agent_id}_{session_id}"

    async def save_session(self, user_id: str, session_id: str, session_data: SessionData) -> bool:
        """Save session metadata to MongoDB."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return False

            doc_id = self._session_document_id(user_id, session_id, session_data.agent_id)
            
            # Convert SessionData to dict for MongoDB
            doc = {
                "session_id": session_data.session_id,
                "user_id": session_data.user_id,
                "agent_instance_config": session_data.agent_instance_config,
                "correlation_id": session_data.correlation_id,
                "created_at": session_data.created_at,
                "updated_at": session_data.updated_at,
                "metadata": session_data.metadata,
                "agent_id": session_data.agent_id,
                "agent_type": session_data.agent_type,
                "session_configuration": session_data.session_configuration,
                "session_label": session_data.session_label
            }

            result = await self.sessions_collection.replace_one(
                {"_id": doc_id}, 
                doc, 
                upsert=True
            )
            
            if result.acknowledged:
                logger.debug(f"Session saved: {session_id} (agent: {session_data.agent_id})")
                return True
            else:
                logger.error(f"Failed to save session {session_id}: operation not acknowledged")
                return False
                
        except Exception as e:
            logger.error(f"❌ [MONGODB DEBUG] Failed to save session {session_id} for user {user_id} to MongoDB: {e}")
            import traceback
            logger.error(f"   📜 Traceback: {traceback.format_exc()}")
            return False

    async def load_session(self, user_id: str, session_id: str) -> Optional[SessionData]:
        """Load session metadata from MongoDB."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return None

            # Find the session by user_id and session_id
            session_query = {"user_id": user_id, "session_id": session_id}
            doc = await self.sessions_collection.find_one(session_query)
            
            if doc:
                agent_id = doc.get("agent_id")
                logger.debug(f"Session loaded: {session_id} (agent: {agent_id})")
                
                # Remove MongoDB _id before creating SessionData
                doc.pop("_id", None)
                session_data = SessionData(**doc)
                return session_data
            else:
                logger.debug(f"Session not found: {session_id} for user {user_id}")
                return None
                
        except Exception as e:
            logger.error(f"❌ [MONGODB DEBUG] Failed to load session {session_id} for user {user_id} from MongoDB: {e}")
            import traceback
            logger.error(f"   📜 Traceback: {traceback.format_exc()}")
            return None

    async def delete_session(self, user_id: str, session_id: str) -> bool:
        """Delete session and all related messages from MongoDB."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return False

            # Delete session - use query instead of doc_id to handle any agent_id
            await self.sessions_collection.delete_one({"user_id": user_id, "session_id": session_id})
            
            # Delete all messages for this session
            await self.messages_collection.delete_many({"session_id": session_id})
            
            # Delete all insights for this session
            await self.insights_collection.delete_many({"session_id": session_id})
            
            # Delete all metadata for this session
            await self.metadata_collection.delete_many({"session_id": session_id})
            
            # Delete agent state
            await self.agent_states_collection.delete_one({"session_id": session_id})

            logger.debug(f"Deleted session {session_id} for user {user_id} from MongoDB")
            return True
        except Exception as e:
            logger.error(f"Failed to delete session {session_id} for user {user_id} from MongoDB: {e}")
            return False

    async def list_user_sessions(self, user_id: str) -> List[str]:
        """List all session IDs for a user."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            cursor = self.sessions_collection.find(
                {"user_id": user_id}, 
                {"session_id": 1}
            ).sort("updated_at", -1)
            
            sessions = []
            async for doc in cursor:
                sessions.append(doc["session_id"])
            
            return sessions
        except Exception as e:
            logger.error(f"Failed to list sessions for user {user_id} from MongoDB: {e}")
            return []

    async def list_all_users_with_sessions(self) -> List[str]:
        """List all user IDs who have at least one session."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            user_ids = await self.sessions_collection.distinct("user_id", {})
            
            return user_ids
        except Exception as e:
            logger.error(f"Failed to list all users with sessions from MongoDB: {e}")
            return []

    async def add_message(self, message_data: MessageData) -> bool:
        """Add a message to MongoDB."""
        try:
            if self.messages_collection is None:
                logger.error("MongoDB not initialized")
                return False

            # Auto-increment sequence number
            last_message = await self.messages_collection.find_one(
                {"session_id": message_data.session_id},
                sort=[("sequence_number", -1)]
            )
            
            sequence_number = (last_message["sequence_number"] + 1) if last_message else 1
            message_data.sequence_number = sequence_number

            doc = {
                "message_id": message_data.message_id,
                "session_id": message_data.session_id,
                "user_id": message_data.user_id,
                "interaction_id": message_data.interaction_id,
                "sequence_number": message_data.sequence_number,
                "message_type": message_data.message_type,
                "role": message_data.role,
                "text_content": message_data.text_content,
                "parts": message_data.parts,
                "response_text_main": message_data.response_text_main,
                "created_at": message_data.created_at,
                "processed_at": message_data.processed_at,
                "parent_message_id": message_data.parent_message_id,
                "related_message_ids": message_data.related_message_ids,
                "processing_time_ms": message_data.processing_time_ms,
                "model_used": message_data.model_used,
                "token_count": message_data.token_count,
                # Agent identity fields
                "agent_id": message_data.agent_id,
                "agent_type": message_data.agent_type
            }

            await self.messages_collection.insert_one(doc)
            logger.debug(f"Added message {message_data.message_id} to MongoDB")
            return True
        except Exception as e:
            logger.error(f"Failed to add message {message_data.message_id} to MongoDB: {e}")
            return False

    async def get_conversation_history(self, session_id: str, limit: Optional[int] = None, 
                                     offset: Optional[int] = None) -> List[MessageData]:
        """Get conversation history with pagination."""
        try:
            if self.messages_collection is None:
                logger.error("MongoDB not initialized")
                return []

            query = {"session_id": session_id}
            cursor = self.messages_collection.find(query).sort("sequence_number", 1)
            
            if offset:
                cursor = cursor.skip(offset)
            if limit:
                cursor = cursor.limit(limit)

            messages = []
            async for doc in cursor:
                doc.pop("_id", None)
                messages.append(MessageData(**doc))
            
            return messages
        except Exception as e:
            logger.error(f"Failed to get conversation history for session {session_id}: {e}")
            return []

    async def get_last_conversation_exchanges(self, session_id: str, limit: int = 10) -> List[List[MessageData]]:
        """Get last N conversation exchanges (grouped by interaction_id)."""
        try:
            if self.messages_collection is None:
                logger.error("MongoDB not initialized")
                return []

            pipeline = [
                {"$match": {"session_id": session_id}},
                {"$sort": {"sequence_number": 1}},
                {"$group": {
                    "_id": "$interaction_id",
                    "messages": {"$push": "$$ROOT"},
                    "max_sequence": {"$max": "$sequence_number"}
                }},
                {"$sort": {"max_sequence": -1}},
                {"$limit": limit}
            ]

            exchanges = []
            async for doc in self.messages_collection.aggregate(pipeline):
                exchange_messages = []
                for msg_doc in doc["messages"]:
                    msg_doc.pop("_id", None)
                    exchange_messages.append(MessageData(**msg_doc))
                exchanges.append(exchange_messages)
            
            return exchanges
        except Exception as e:
            logger.error(f"Failed to get conversation exchanges for session {session_id}: {e}")
            return []

    async def add_insight(self, insight: MessageInsight) -> bool:
        """Add an insight for a message."""
        try:
            if self.insights_collection is None:
                logger.error("MongoDB not initialized")
                return False

            doc = {
                "insight_id": insight.insight_id,
                "message_id": insight.message_id,
                "session_id": insight.session_id,
                "user_id": insight.user_id,
                "insight_type": insight.insight_type,
                "insight_data": insight.insight_data,
                "created_at": insight.created_at,
                "created_by": insight.created_by,
                # Agent identity fields
                "agent_id": insight.agent_id,
                "agent_type": insight.agent_type
            }

            await self.insights_collection.insert_one(doc)
            return True
        except Exception as e:
            logger.error(f"Failed to add insight {insight.insight_id}: {e}")
            return False

    async def add_metadata(self, metadata: MessageMetadata) -> bool:
        """Add metadata for a message."""
        try:
            if self.metadata_collection is None:
                logger.error("MongoDB not initialized")
                return False

            doc = {
                "metadata_id": metadata.metadata_id,
                "message_id": metadata.message_id,
                "session_id": metadata.session_id,
                "metadata_type": metadata.metadata_type,
                "metadata": metadata.metadata,
                "created_at": metadata.created_at,
                "created_by": metadata.created_by,
                # Agent identity fields
                "agent_id": metadata.agent_id,
                "agent_type": metadata.agent_type
            }

            await self.metadata_collection.insert_one(doc)
            return True
        except Exception as e:
            logger.error(f"Failed to add metadata {metadata.metadata_id}: {e}")
            return False

    async def get_message_with_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """Get message with all its insights and metadata."""
        try:
            if self.messages_collection is None:
                logger.error("MongoDB not initialized")
                return None

            pipeline = [
                {"$match": {"message_id": message_id}},
                {"$lookup": {
                    "from": "insights",
                    "localField": "message_id", 
                    "foreignField": "message_id",
                    "as": "insights"
                }},
                {"$lookup": {
                    "from": "metadata",
                    "localField": "message_id",
                    "foreignField": "message_id", 
                    "as": "metadata"
                }}
            ]

            async for doc in self.messages_collection.aggregate(pipeline):
                doc.pop("_id", None)
                
                # Convert insights
                insights = []
                for insight_doc in doc.pop("insights", []):
                    insight_doc.pop("_id", None)
                    insights.append(MessageInsight(**insight_doc))
                
                # Convert metadata
                metadata_list = []
                for metadata_doc in doc.pop("metadata", []):
                    metadata_doc.pop("_id", None)
                    metadata_list.append(MessageMetadata(**metadata_doc))
                
                return {
                    "message": MessageData(**doc),
                    "insights": insights,
                    "metadata": metadata_list
                }
            
            return None
        except Exception as e:
            logger.error(f"Failed to get message details for {message_id}: {e}")
            return None

    async def update_session_metadata(self, user_id: str, session_id: str, 
                                    correlation_id: Optional[str] = None, 
                                    metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update session metadata."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return False

            update_doc = {"$set": {"updated_at": datetime.now(timezone.utc).isoformat()}}
            
            if correlation_id is not None:
                update_doc["$set"]["correlation_id"] = correlation_id
            
            if metadata is not None:
                for key, value in metadata.items():
                    update_doc["$set"][f"metadata.{key}"] = value

            # Use query instead of doc_id to handle any agent_id
            result = await self.sessions_collection.update_one(
                {"user_id": user_id, "session_id": session_id}, 
                update_doc
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update metadata for session {session_id}: {e}")
            return False

    async def update_session_label(self, user_id: str, session_id: str, label: str) -> bool:
        """Update the session label."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return False

            update_doc = {"$set": {"session_label": label, "updated_at": datetime.now(timezone.utc).isoformat()}}
            # Use query instead of doc_id to handle any agent_id
            result = await self.sessions_collection.update_one(
                {"user_id": user_id, "session_id": session_id}, 
                update_doc
            )
            
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Failed to update session label for {session_id}: {e}")
            return False

    async def list_user_sessions_with_info(self, user_id: str) -> List[Dict[str, Any]]:
        """List all sessions for a user with metadata including labels."""
        sessions_info = []
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            cursor = self.sessions_collection.find(
                {"user_id": user_id},
                {"session_id": 1, "session_label": 1, "created_at": 1, "updated_at": 1, "correlation_id": 1, "metadata": 1, "agent_id": 1, "agent_type": 1, "session_configuration": 1}
            ).sort("updated_at", -1)
            
            async for doc in cursor:
                doc.pop("_id", None)
                sessions_info.append(doc)
            
            return sessions_info
        except Exception as e:
            logger.error(f"Failed to list user sessions with info for user {user_id} from MongoDB: {e}")
            return []

    # Agent identity query methods
    async def list_sessions_by_agent_id(self, agent_id: str) -> List[str]:
        """List all session IDs for a specific agent."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            cursor = self.sessions_collection.find(
                {"agent_id": agent_id}, 
                {"session_id": 1}
            ).sort("updated_at", -1)
            
            sessions = []
            async for doc in cursor:
                sessions.append(doc["session_id"])
            
            return sessions
        except Exception as e:
            logger.error(f"Failed to list sessions for agent {agent_id} from MongoDB: {e}")
            return []

    async def list_sessions_by_agent_type(self, agent_type: str) -> List[str]:
        """List all session IDs for a specific agent type."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            cursor = self.sessions_collection.find(
                {"agent_type": agent_type}, 
                {"session_id": 1}
            ).sort("updated_at", -1)
            
            sessions = []
            async for doc in cursor:
                sessions.append(doc["session_id"])
            
            return sessions
        except Exception as e:
            logger.error(f"Failed to list sessions for agent type {agent_type} from MongoDB: {e}")
            return []

    async def get_user_sessions_by_agent(self, user_id: str, agent_id: Optional[str] = None, 
                                       agent_type: Optional[str] = None) -> List[str]:
        """Get user sessions filtered by agent identity."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            # Build query
            query = {"user_id": user_id}
            if agent_id:
                query["agent_id"] = agent_id
            if agent_type:
                query["agent_type"] = agent_type

            cursor = self.sessions_collection.find(
                query, 
                {"session_id": 1}
            ).sort("updated_at", -1)
            
            sessions = []
            async for doc in cursor:
                sessions.append(doc["session_id"])
            
            return sessions
        except Exception as e:
            logger.error(f"Failed to get user sessions by agent for user {user_id} from MongoDB: {e}")
            return []

    async def save_agent_state(self, session_id: str, agent_state: Dict[str, Any]) -> bool:
        """Saves the agent's state to MongoDB."""
        try:
            if self.agent_states_collection is None:
                logger.error("MongoDB not initialized")
                return False

            doc = {"session_id": session_id, "state": agent_state, "updated_at": datetime.now(timezone.utc).isoformat()}
            
            await self.agent_states_collection.replace_one({"session_id": session_id}, doc, upsert=True)
            logger.debug(f"Saved agent state for session {session_id} to MongoDB.")
            return True
        except Exception as e:
            logger.error(f"Failed to save agent state for session {session_id} to MongoDB: {e}")
            return False

    async def load_agent_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Loads the agent's state from MongoDB."""
        try:
            if self.agent_states_collection is None:
                logger.error("MongoDB not initialized")
                return None

            doc = await self.agent_states_collection.find_one({"session_id": session_id})
            
            if doc and "state" in doc:
                return doc["state"]
            return None
        except Exception as e:
            logger.error(f"Failed to load agent state for session {session_id} from MongoDB: {e}")
            return None

    async def load_session_configuration(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session configuration (system_prompt, model_name, model_config) for a session."""
        # Use query instead of doc_id to handle any agent_id
        doc = await self.sessions_collection.find_one({"user_id": user_id, "session_id": session_id})
        if not doc:
            return None
        return doc.get("session_configuration")

    # Agent identity query methods
    async def list_sessions_by_agent_id(self, agent_id: str) -> List[str]:
        """List all session IDs for a specific agent."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            cursor = self.sessions_collection.find(
                {"agent_id": agent_id}, 
                {"session_id": 1}
            ).sort("updated_at", -1)
            
            sessions = []
            async for doc in cursor:
                sessions.append(doc["session_id"])
            
            return sessions
        except Exception as e:
            logger.error(f"Failed to list sessions for agent {agent_id} from MongoDB: {e}")
            return []

    async def list_sessions_by_agent_type(self, agent_type: str) -> List[str]:
        """List all session IDs for a specific agent type."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            cursor = self.sessions_collection.find(
                {"agent_type": agent_type}, 
                {"session_id": 1}
            ).sort("updated_at", -1)
            
            sessions = []
            async for doc in cursor:
                sessions.append(doc["session_id"])
            
            return sessions
        except Exception as e:
            logger.error(f"Failed to list sessions for agent type {agent_type} from MongoDB: {e}")
            return []

    async def get_user_sessions_by_agent(self, user_id: str, agent_id: Optional[str] = None, 
                                       agent_type: Optional[str] = None) -> List[str]:
        """Get user sessions filtered by agent identity."""
        try:
            if self.sessions_collection is None:
                logger.error("MongoDB not initialized")
                return []

            # Build query
            query = {"user_id": user_id}
            if agent_id:
                query["agent_id"] = agent_id
            if agent_type:
                query["agent_type"] = agent_type

            cursor = self.sessions_collection.find(
                query, 
                {"session_id": 1}
            ).sort("updated_at", -1)
            
            sessions = []
            async for doc in cursor:
                sessions.append(doc["session_id"])
            
            return sessions
        except Exception as e:
            logger.error(f"Failed to get user sessions by agent for user {user_id} from MongoDB: {e}")
            return []

    async def cleanup(self) -> None:
        """Close MongoDB connection."""
        if self.client is not None:
            self.client.close()
            logger.info("Closed MongoDB connection")

    async def get_response_times_for_session(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Calculate response times for agent responses by measuring the time delta
        between user input and agent response messages in the same conversation.
        
        Returns a list of dictionaries with response time information.
        """
        try:
            pipeline = [
                # Match messages for this session
                {"$match": {"session_id": session_id}},
                
                # Sort by sequence number to ensure proper ordering
                {"$sort": {"sequence_number": 1}},
                
                # Add a field with the previous message in the sequence
                {"$setWindowFields": {
                    "sortBy": {"sequence_number": 1},
                    "output": {
                        "prev_message": {
                            "$shift": {
                                "output": "$$ROOT",
                                "by": -1
                            }
                        }
                    }
                }},
                
                # Only keep agent responses that have a previous message
                {"$match": {
                    "message_type": "agent_response",
                    "prev_message": {"$ne": None}
                }},
                
                # Add calculated response time
                {"$addFields": {
                    "response_time_ms": {
                        "$divide": [
                            {"$subtract": [
                                {"$dateFromString": {"dateString": "$created_at"}},
                                {"$dateFromString": {"dateString": "$prev_message.created_at"}}
                            ]},
                            1  # Convert to milliseconds
                        ]
                    },
                    "user_request_text": "$prev_message.text_content",
                    "user_request_created_at": "$prev_message.created_at"
                }},
                
                # Project relevant fields
                {"$project": {
                    "message_id": 1,
                    "interaction_id": 1,
                    "sequence_number": 1,
                    "response_text_main": 1,
                    "created_at": 1,
                    "user_request_text": 1,
                    "user_request_created_at": 1,
                    "response_time_ms": 1,
                    "response_time_seconds": {"$divide": ["$response_time_ms", 1000]}
                }}
            ]
            
            results = []
            async for doc in self.messages_collection.aggregate(pipeline):
                results.append(doc)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error calculating response times for session {session_id}: {e}")
            return []

    async def get_response_times_for_interaction(self, interaction_id: str) -> Dict[str, Any]:
        """
        Calculate response time for a specific interaction (user input + agent response pair).
        
        Returns response time information for the interaction.
        """
        try:
            pipeline = [
                # Match messages for this interaction
                {"$match": {"interaction_id": interaction_id}},
                
                # Sort by sequence number
                {"$sort": {"sequence_number": 1}},
                
                # Group by interaction to get both user input and agent response
                {"$group": {
                    "_id": "$interaction_id",
                    "messages": {"$push": "$$ROOT"}
                }},
                
                # Add calculated response time
                {"$addFields": {
                    "user_message": {
                        "$arrayElemAt": [
                            {"$filter": {
                                "input": "$messages",
                                "cond": {"$eq": ["$$this.message_type", "user_input"]}
                            }},
                            0
                        ]
                    },
                    "agent_message": {
                        "$arrayElemAt": [
                            {"$filter": {
                                "input": "$messages", 
                                "cond": {"$eq": ["$$this.message_type", "agent_response"]}
                            }},
                            0
                        ]
                    }
                }},
                
                # Calculate response time
                {"$addFields": {
                    "response_time_ms": {
                        "$cond": {
                            "if": {"$and": ["$user_message", "$agent_message"]},
                            "then": {
                                "$divide": [
                                    {"$subtract": [
                                        {"$dateFromString": {"dateString": "$agent_message.created_at"}},
                                        {"$dateFromString": {"dateString": "$user_message.created_at"}}
                                    ]},
                                    1
                                ]
                            },
                            "else": null
                        }
                    }
                }},
                
                # Project result
                {"$project": {
                    "interaction_id": "$_id",
                    "user_request": {
                        "message_id": "$user_message.message_id",
                        "text_content": "$user_message.text_content", 
                        "created_at": "$user_message.created_at"
                    },
                    "agent_response": {
                        "message_id": "$agent_message.message_id",
                        "response_text_main": "$agent_message.response_text_main",
                        "created_at": "$agent_message.created_at"
                    },
                    "response_time_ms": 1,
                    "response_time_seconds": {"$divide": ["$response_time_ms", 1000]}
                }}
            ]
            
            result = None
            async for doc in self.messages_collection.aggregate(pipeline):
                result = doc
                break
            
            return result or {}
            
        except Exception as e:
            self.logger.error(f"Error calculating response time for interaction {interaction_id}: {e}")
            return {}

    async def add_agent_lifecycle_event(self, lifecycle_data: AgentLifecycleData) -> bool:
        """Add an agent lifecycle event to MongoDB"""
        try:
            if not hasattr(self, 'lifecycle_collection'):
                self.lifecycle_collection = self.db["agent_lifecycle"]
            
            doc = {
                "lifecycle_id": lifecycle_data.lifecycle_id,
                "agent_id": lifecycle_data.agent_id,
                "agent_type": lifecycle_data.agent_type,
                "event_type": lifecycle_data.event_type,
                "session_id": lifecycle_data.session_id,
                "user_id": lifecycle_data.user_id,
                "timestamp": lifecycle_data.timestamp,
                "metadata": lifecycle_data.metadata
            }
            
            await self.lifecycle_collection.insert_one(doc)
            logger.debug(f"Added lifecycle event: {lifecycle_data.event_type} for agent {lifecycle_data.agent_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding lifecycle event to MongoDB: {e}")
            return False

    async def get_agent_lifecycle_events(self, agent_id: str) -> List[AgentLifecycleData]:
        """Get lifecycle events for a specific agent from MongoDB"""
        try:
            if not hasattr(self, 'lifecycle_collection'):
                self.lifecycle_collection = self.db["agent_lifecycle"]
            
            events = []
            cursor = self.lifecycle_collection.find(
                {"agent_id": agent_id}
            ).sort("timestamp", -1)
            
            async for doc in cursor:
                doc.pop("_id", None)  # Remove MongoDB _id
                events.append(AgentLifecycleData(**doc))
            
            return events
        except Exception as e:
            logger.error(f"Error getting lifecycle events from MongoDB: {e}")
            return []

    async def get_agent_usage_statistics(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """Get usage statistics by agent type from MongoDB"""
        try:
            stats = {
                "total_agents": 0,
                "total_sessions": 0,
                "total_messages": 0,
                "agent_types": {},
                "lifecycle_events": {}
            }
            
            # Count sessions by agent type
            pipeline = [
                {"$group": {
                    "_id": "$agent_type",
                    "session_count": {"$sum": 1},
                    "unique_agents": {"$addToSet": "$agent_id"}
                }},
                {"$addFields": {
                    "unique_agent_count": {"$size": "$unique_agents"}
                }}
            ]
            
            if agent_type:
                pipeline.insert(0, {"$match": {"agent_type": agent_type}})
            
            if hasattr(self, 'sessions_collection'):
                async for doc in self.sessions_collection.aggregate(pipeline):
                    agent_type_key = doc["_id"] or "unknown"
                    stats["agent_types"][agent_type_key] = {
                        "session_count": doc["session_count"],
                        "unique_agents": doc["unique_agent_count"]
                    }
            
            # Count messages
            if hasattr(self, 'messages_collection'):
                stats["total_messages"] = await self.messages_collection.count_documents({})
            
            # Count lifecycle events
            if hasattr(self, 'lifecycle_collection'):
                lifecycle_pipeline = [
                    {"$group": {
                        "_id": "$event_type",
                        "count": {"$sum": 1}
                    }}
                ]
                async for doc in self.lifecycle_collection.aggregate(lifecycle_pipeline):
                    stats["lifecycle_events"][doc["_id"]] = doc["count"]
            
            # Calculate totals
            stats["total_sessions"] = sum(data["session_count"] for data in stats["agent_types"].values())
            stats["total_agents"] = sum(data["unique_agents"] for data in stats["agent_types"].values())
            
            # Filter by specific agent type if requested
            if agent_type and agent_type in stats["agent_types"]:
                return {
                    "agent_type": agent_type,
                    **stats["agent_types"][agent_type]
                }
            
            return stats
        except Exception as e:
            logger.error(f"Error getting usage statistics from MongoDB: {e}")
            return {}


# Singleton Elasticsearch client instance
_elasticsearch_client: Optional[Any] = None
_elasticsearch_client_lock = asyncio.Lock()


async def get_shared_elasticsearch_client() -> Optional[Any]:
    """
    Get or create a singleton Elasticsearch client instance.
    
    This function provides a shared Elasticsearch client across all framework components
    for efficient connection pooling and centralized configuration.
    
    Configuration is read from environment variables:
    - ELASTICSEARCH_ENABLED: Enable/disable Elasticsearch integration (default: false)
    - ELASTICSEARCH_URL: Elasticsearch endpoint (default: http://localhost:9200)
    - ELASTICSEARCH_USERNAME: Username for basic auth (optional)
    - ELASTICSEARCH_PASSWORD: Password for basic auth (optional)
    - ELASTICSEARCH_API_KEY: API key for authentication (optional, preferred over basic auth)
    - ELASTICSEARCH_VERIFY_CERTS: Verify SSL certificates (default: true)
    - ELASTICSEARCH_CA_CERTS: Path to CA certificate file (optional)
    - ELASTICSEARCH_TIMEOUT: Request timeout in seconds (default: 30)
    - ELASTICSEARCH_MAX_RETRIES: Maximum number of retries (default: 3)
    - ELASTICSEARCH_RETRY_ON_TIMEOUT: Retry on timeout (default: true)
    
    Returns:
        Elasticsearch client instance if enabled and available, None otherwise
        
    Example:
        ```python
        es_client = await get_shared_elasticsearch_client()
        if es_client:
            await es_client.index(index="my-index", document={"field": "value"})
        ```
    """
    global _elasticsearch_client
    
    # Check if Elasticsearch is enabled
    es_enabled = os.getenv("ELASTICSEARCH_ENABLED", "false").lower() == "true"
    if not es_enabled:
        logger.debug("Elasticsearch integration is disabled (ELASTICSEARCH_ENABLED=false)")
        return None
    
    # Check if Elasticsearch package is available
    if not ELASTICSEARCH_AVAILABLE:
        logger.warning("Elasticsearch integration is enabled but elasticsearch package is not installed. "
                      "Install with: pip install elasticsearch>=8.11.0")
        return None
    
    # Return existing client if already created
    if _elasticsearch_client is not None:
        return _elasticsearch_client
    
    # Use lock to ensure only one client is created
    async with _elasticsearch_client_lock:
        # Double-check after acquiring lock
        if _elasticsearch_client is not None:
            return _elasticsearch_client
        
        try:
            from elasticsearch import AsyncElasticsearch
            
            # Read configuration from environment
            es_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
            es_username = os.getenv("ELASTICSEARCH_USERNAME")
            es_password = os.getenv("ELASTICSEARCH_PASSWORD")
            es_api_key = os.getenv("ELASTICSEARCH_API_KEY")
            es_verify_certs = os.getenv("ELASTICSEARCH_VERIFY_CERTS", "true").lower() == "true"
            es_ca_certs = os.getenv("ELASTICSEARCH_CA_CERTS")
            es_timeout = int(os.getenv("ELASTICSEARCH_TIMEOUT", "30"))
            es_max_retries = int(os.getenv("ELASTICSEARCH_MAX_RETRIES", "3"))
            es_retry_on_timeout = os.getenv("ELASTICSEARCH_RETRY_ON_TIMEOUT", "true").lower() == "true"
            
            # Build client configuration
            client_config = {
                "hosts": [es_url],
                "request_timeout": es_timeout,
                "max_retries": es_max_retries,
                "retry_on_timeout": es_retry_on_timeout,
            }
            
            # Add authentication
            if es_api_key:
                # API key authentication (preferred)
                client_config["api_key"] = es_api_key
                logger.debug("Using Elasticsearch API key authentication")
            elif es_username and es_password:
                # Basic authentication
                client_config["basic_auth"] = (es_username, es_password)
                logger.debug("Using Elasticsearch basic authentication")
            else:
                logger.debug("No Elasticsearch authentication configured")
            
            # Add SSL/TLS configuration
            if es_url.startswith("https://"):
                client_config["verify_certs"] = es_verify_certs
                if es_ca_certs:
                    client_config["ca_certs"] = es_ca_certs
                    logger.debug(f"Using CA certificate: {es_ca_certs}")
                if not es_verify_certs:
                    logger.warning("SSL certificate verification is disabled. "
                                 "This is insecure and should only be used in development.")
            
            # Create client
            _elasticsearch_client = AsyncElasticsearch(**client_config)
            
            # Test connection
            try:
                info = await _elasticsearch_client.info()
                logger.info(f"Connected to Elasticsearch cluster: {info['cluster_name']} "
                          f"(version {info['version']['number']})")
            except Exception as e:
                logger.error(f"Failed to connect to Elasticsearch: {e}")
                await _elasticsearch_client.close()
                _elasticsearch_client = None
                return None
            
            return _elasticsearch_client
            
        except Exception as e:
            logger.error(f"Failed to create Elasticsearch client: {e}")
            _elasticsearch_client = None
            return None


class SessionStorageFactory:
    """
    Factory class to create session storage instances based on configuration.
    
    Supports automatic fallback chain with connection testing:
    - Elasticsearch → MongoDB → Memory (if Elasticsearch fails)
    - MongoDB → Memory (if MongoDB fails)
    - Memory (always works)
    
    The factory tests each backend's connection before returning it, ensuring
    that the returned storage instance is fully operational.
    """
    
    @staticmethod
    async def get_elasticsearch_client() -> Optional[Any]:
        """
        Get the shared Elasticsearch client instance.
        
        This method provides access to the singleton Elasticsearch client
        for use by other components that need direct ES access.
        
        Returns:
            Elasticsearch client if available and enabled, None otherwise
        """
        return await get_shared_elasticsearch_client()
    
    @staticmethod
    async def _test_elasticsearch_connection(storage_instance: 'ElasticsearchSessionStorage') -> bool:
        """
        Test Elasticsearch connection by attempting a simple operation.
        
        Args:
            storage_instance: Elasticsearch storage instance to test
            
        Returns:
            True if connection is working, False otherwise
        """
        try:
            if storage_instance.client is None:
                return False
            
            # Test connection with a simple ping
            await storage_instance.client.ping()
            logger.debug("Elasticsearch connection test successful")
            return True
        except Exception as e:
            logger.warning(f"Elasticsearch connection test failed: {e}")
            return False
    
    @staticmethod
    async def _test_mongodb_connection(storage_instance: MongoDBSessionStorage) -> bool:
        """
        Test MongoDB connection by attempting a simple operation.
        
        Args:
            storage_instance: MongoDB storage instance to test
            
        Returns:
            True if connection is working, False otherwise
        """
        try:
            if storage_instance.client is None:
                return False
            
            # Test connection with a simple ping
            await storage_instance.client.admin.command('ping')
            logger.debug("MongoDB connection test successful")
            return True
        except Exception as e:
            logger.warning(f"MongoDB connection test failed: {e}")
            return False
    
    @staticmethod
    async def create_storage() -> SessionStorageInterface:
        """
        Create and initialize a session storage backend based on environment variables.
        
        Priority order (when multiple backends are configured):
        1. Elasticsearch (if ELASTICSEARCH_ENABLED=true)
        2. MongoDB (if SESSION_STORAGE_TYPE=mongodb)
        3. Memory (default fallback)
        
        Each backend is tested for connectivity before being returned. If a backend
        fails initialization or connection testing, the factory automatically falls
        back to the next option in the priority chain.
        
        Logging is provided at each step to track backend selection and fallback reasons.
        
        Returns:
            Initialized SessionStorageInterface instance
            
        Example:
            ```python
            storage = await SessionStorageFactory.create_storage()
            # storage will be Elasticsearch, MongoDB, or Memory depending on config and availability
            ```
        """
        storage_type = os.getenv("SESSION_STORAGE_TYPE", "memory").lower()
        es_enabled = os.getenv("ELASTICSEARCH_ENABLED", "false").lower() == "true"
        
        # Try Elasticsearch first if enabled (highest priority)
        if es_enabled:
            if not ELASTICSEARCH_AVAILABLE:
                logger.warning("Elasticsearch integration is enabled (ELASTICSEARCH_ENABLED=true) but "
                             "elasticsearch package is not installed. Install with: pip install elasticsearch>=8.11.0. "
                             "Falling back to next storage option.")
            else:
                logger.info("Attempting to create Elasticsearch session storage (priority 1)")
                try:
                    from .elasticsearch_session_storage import ElasticsearchSessionStorage
                    storage_instance = ElasticsearchSessionStorage()
                    initialized = await storage_instance.initialize()
                    
                    if initialized:
                        # Test connection before returning
                        connection_ok = await SessionStorageFactory._test_elasticsearch_connection(storage_instance)
                        if connection_ok:
                            logger.info("✓ Successfully initialized Elasticsearch session storage")
                            return storage_instance
                        else:
                            logger.warning("Elasticsearch storage initialized but connection test failed. "
                                         "Falling back to next storage option.")
                    else:
                        logger.warning("Failed to initialize Elasticsearch storage (initialization returned False). "
                                     "Falling back to next storage option.")
                except ImportError as e:
                    logger.warning(f"Failed to import Elasticsearch storage module: {e}. "
                                 "Falling back to next storage option.")
                except Exception as e:
                    logger.warning(f"Failed to create Elasticsearch storage: {e}. "
                                 "Falling back to next storage option.")
        
        # Try MongoDB if configured (second priority)
        if storage_type == "mongodb":
            if not MONGODB_AVAILABLE:
                logger.warning("MongoDB storage type configured (SESSION_STORAGE_TYPE=mongodb) but "
                             "required packages (motor, pymongo) are not installed. "
                             "Install with: pip install motor pymongo. "
                             "Falling back to memory storage.")
            else:
                logger.info("Attempting to create MongoDB session storage (priority 2)")
                try:
                    storage_instance = MongoDBSessionStorage()
                    initialized = await storage_instance.initialize()
                    
                    if initialized:
                        # Test connection before returning
                        connection_ok = await SessionStorageFactory._test_mongodb_connection(storage_instance)
                        if connection_ok:
                            logger.info("✓ Successfully initialized MongoDB session storage")
                            return storage_instance
                        else:
                            logger.warning("MongoDB storage initialized but connection test failed. "
                                         "Falling back to memory storage.")
                    else:
                        logger.warning("Failed to initialize MongoDB storage (initialization returned False). "
                                     "Falling back to memory storage.")
                except Exception as e:
                    logger.warning(f"Failed to create MongoDB storage: {e}. "
                                 "Falling back to memory storage.")
        
        # Fall back to memory storage (always works, lowest priority)
        logger.info("Using in-memory session storage (priority 3 - fallback)")
        storage_instance = MemorySessionStorage()
        await storage_instance.initialize()
        logger.info("✓ Successfully initialized in-memory session storage")
        return storage_instance


# Helper functions for backward compatibility have been moved to autogen_state_manager.py
def history_message_to_message_data(history_message, session_id: str, user_id: str, 
                                  interaction_id: str, message_type: str, 
                                  agent_id: Optional[str] = None, agent_type: Optional[str] = None) -> MessageData:
    """Convert HistoryMessage to MessageData."""
    # Convert Pydantic parts to dictionaries for MongoDB storage
    parts = getattr(history_message, 'parts', None)
    if parts:
        serializable_parts = []
        for part in parts:
            if hasattr(part, 'model_dump'):
                serializable_parts.append(part.model_dump())
            elif hasattr(part, 'dict'):
                serializable_parts.append(part.dict())
            else:
                # Fallback for non-Pydantic objects
                serializable_parts.append(str(part))
        parts = serializable_parts
    
    return MessageData(
        message_id=str(uuid.uuid4()),
        session_id=session_id,
        user_id=user_id,
        interaction_id=interaction_id,
        sequence_number=0,  # Will be set by storage
        message_type=message_type,
        role=getattr(history_message, 'role', ''),
        text_content=getattr(history_message, 'text_content', None),
        parts=parts,
        response_text_main=getattr(history_message, 'response_text_main', None),
        created_at=getattr(history_message, 'timestamp', None),
        processing_time_ms=getattr(history_message, 'processing_time_ms', None),
        processed_at=getattr(history_message, 'processed_at', None),
        model_used=getattr(history_message, 'model_used', None),
        # Agent identity fields
        agent_id=agent_id,
        agent_type=agent_type,
    )

def message_data_to_history_message(message_data: MessageData, history_message_class):
    """Convert MessageData back to HistoryMessage object."""
    # Note: Parts are stored as dictionaries in MongoDB, they would need to be 
    # reconstructed into Pydantic objects if needed by the application
    # For now, we'll keep them as dictionaries since the API can handle both formats
    return history_message_class(
        role=message_data.role,
        text_content=message_data.text_content,
        parts=message_data.parts,  # These are now dictionaries, not Pydantic objects
        response_text_main=message_data.response_text_main,
        timestamp=message_data.created_at,
        interaction_id=message_data.interaction_id,
        processing_time_ms=message_data.processing_time_ms,
        processed_at=message_data.processed_at,
        model_used=message_data.model_used
    ) 