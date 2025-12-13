"""
Framework-Agnostic State Management

This module provides functionalities for managing agent state across different frameworks,
including serialization, compression, and truncation. This is separated from the generic
session storage to keep concerns separate.
"""

import os
import json
import logging
import uuid
import gzip
import sys
import hashlib
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone

# Import AgentInterface for type hinting without creating circular dependencies
from .agent_interface import AgentInterface

logger = logging.getLogger(__name__)

# Configuration for state management, can be overridden by a config file
try:
    from ..docs.mongodb_state_config import (
        MAX_STATE_SIZE_MB, MAX_CONVERSATION_HISTORY, ENABLE_STATE_COMPRESSION,
        COMPRESSION_THRESHOLD_MB, COMPRESSION_EFFICIENCY_THRESHOLD,
        AGGRESSIVE_TRUNCATION_THRESHOLD
    )
except ImportError:
    # Fallback configuration if config file is not available
    MAX_STATE_SIZE_MB = 12
    MAX_CONVERSATION_HISTORY = 100
    ENABLE_STATE_COMPRESSION = True
    COMPRESSION_THRESHOLD_MB = 1.0
    COMPRESSION_EFFICIENCY_THRESHOLD = 0.8
    AGGRESSIVE_TRUNCATION_THRESHOLD = 20


@dataclass
class AgentIdentity:
    """Complete agent identity information"""
    agent_id: str
    agent_type: str
    agent_class: str
    agent_module: str
    created_at: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Ensure created_at is set if not provided"""
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert AgentIdentity to dictionary for serialization"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "agent_class": self.agent_class,
            "agent_module": self.agent_module,
            "created_at": self.created_at,
            "version": self.version,
            "metadata": self.metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentIdentity':
        """Create AgentIdentity from dictionary"""
        return cls(
            agent_id=data["agent_id"],
            agent_type=data["agent_type"],
            agent_class=data["agent_class"], 
            agent_module=data["agent_module"],
            created_at=data["created_at"],
            version=data.get("version"),
            metadata=data.get("metadata", {})
        )


class StateManager:
    """
    Framework-agnostic state management utility.
    
    Provides static methods for:
    - State compression and decompression
    - Conversation history truncation
    - Agent identity creation and validation
    """
    
    @staticmethod
    def compress_state(state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compress agent state using gzip compression for states >10KB.
        
        Args:
            state: The agent state dictionary to compress
            
        Returns:
            Compressed state dictionary with metadata, or original state if compression fails
        """
        try:
            # Convert to JSON string
            json_str = json.dumps(state, default=str)
            original_size = len(json_str)
            
            # Only compress if size exceeds threshold (10KB = 10240 bytes)
            if original_size < 10240:
                return state
            
            # Compress the JSON string
            compressed_data = gzip.compress(json_str.encode('utf-8'))
            
            # Return wrapped compressed state
            return {
                "_compressed": True,
                "_compression_type": "gzip",
                "_original_size": original_size,
                "_compressed_size": len(compressed_data),
                "data": compressed_data.hex()  # Store as hex string for JSON compatibility
            }
        except Exception as e:
            logger.warning(f"Failed to compress state: {e}")
            return state

    @staticmethod
    def decompress_state(compressed_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decompress agent state that was compressed with compress_state.
        
        Args:
            compressed_state: The compressed state dictionary
            
        Returns:
            Decompressed state dictionary, or original if not compressed or decompression fails
        """
        try:
            if not compressed_state.get("_compressed"):
                return compressed_state
                
            # Extract compressed data
            compressed_data = bytes.fromhex(compressed_state["data"])
            
            # Decompress
            json_str = gzip.decompress(compressed_data).decode('utf-8')
            
            # Parse back to dict
            return json.loads(json_str)
        except Exception as e:
            logger.error(f"Failed to decompress state: {e}")
            return compressed_state

    @staticmethod
    def truncate_history(
        state: Dict[str, Any],
        max_messages: int = MAX_CONVERSATION_HISTORY
    ) -> Dict[str, Any]:
        """
        Truncate conversation history in agent state to limit size.
        
        This method looks for common conversation history patterns across different
        frameworks and truncates them to the most recent max_messages.
        
        Args:
            state: The agent state dictionary
            max_messages: Maximum number of messages to keep (default: 100)
            
        Returns:
            State dictionary with truncated history
        """
        try:
            # Look for conversation history in various state structures
            if isinstance(state, dict):
                # Pattern 1: Direct messages list
                if "messages" in state and isinstance(state["messages"], list):
                    messages = state["messages"]
                    if len(messages) > max_messages:
                        state["messages"] = messages[-max_messages:]
                        logger.info(f"Truncated messages from {len(messages)} to {max_messages}")
                
                # Pattern 2: Nested session states
                for session_id, session_state in state.items():
                    if isinstance(session_state, dict):
                        # Handle message_thread pattern
                        if "message_thread" in session_state and isinstance(session_state["message_thread"], list):
                            thread = session_state["message_thread"]
                            if len(thread) > max_messages:
                                session_state["message_thread"] = thread[-max_messages:]
                                logger.info(f"Truncated message thread from {len(thread)} to {max_messages}")
                        
                        # Handle nested agent states with LLM context
                        if "agent_states" in session_state:
                            for agent_name, agent_state in session_state["agent_states"].items():
                                if isinstance(agent_state, dict) and "agent_state" in agent_state:
                                    inner_state = agent_state["agent_state"]
                                    if "llm_context" in inner_state and "messages" in inner_state["llm_context"]:
                                        messages = inner_state["llm_context"]["messages"]
                                        if isinstance(messages, list) and len(messages) > max_messages:
                                            inner_state["llm_context"]["messages"] = messages[-max_messages:]
                                            logger.info(f"Truncated {agent_name} LLM context from {len(messages)} to {max_messages}")
                        
                        # Handle chat_history pattern
                        if "chat_history" in session_state and isinstance(session_state["chat_history"], list):
                            history = session_state["chat_history"]
                            if len(history) > max_messages:
                                session_state["chat_history"] = history[-max_messages:]
                                logger.info(f"Truncated chat history from {len(history)} to {max_messages}")
            
            return state
        except Exception as e:
            logger.warning(f"Failed to truncate conversation history: {e}")
            return state

    @staticmethod
    def create_agent_identity(
        agent_instance: AgentInterface,
        metadata: Optional[Dict] = None
    ) -> AgentIdentity:
        """
        Generate unique identity for an agent instance based on agent metadata and configuration.
        
        Args:
            agent_instance: The agent instance to create identity for
            metadata: Optional additional metadata to include
            
        Returns:
            AgentIdentity object with unique identifier
        """
        # Try to get agent_type from environment variable first
        agent_type = os.getenv('AGENT_TYPE')
        if not agent_type:
            agent_type = agent_instance.__class__.__name__
            logger.debug(f"No AGENT_TYPE environment variable set, using class name: {agent_type}")
        else:
            logger.debug(f"Using AGENT_TYPE from environment: {agent_type}")
        
        # Get agent_id from the agent instance (required attribute)
        agent_id = StateManager._get_agent_id(agent_instance)
        logger.debug(f"Using agent ID: {agent_id} for agent type: {agent_type}")
        
        # Create complete identity with metadata
        agent_class = agent_instance.__class__.__name__
        agent_module = agent_instance.__class__.__module__
        
        # Get version from agent if available
        version = getattr(agent_instance, '__version__', None) or getattr(agent_instance, 'version', None)
        
        # Collect metadata
        default_metadata = {
            "environment_agent_type": os.getenv('AGENT_TYPE'),
            "has_save_state_method": hasattr(agent_instance, 'save_state'),
            "has_get_state_method": hasattr(agent_instance, 'get_state'),
            "python_version": sys.version,
            "creation_timestamp": time.time()
        }
        
        if metadata:
            default_metadata.update(metadata)
        
        # Check if agent already has stored identity
        if hasattr(agent_instance, '_agent_identity') and isinstance(agent_instance._agent_identity, AgentIdentity):
            # Update existing identity if needed
            stored_identity = agent_instance._agent_identity
            if stored_identity.agent_id != agent_id or stored_identity.agent_type != agent_type:
                logger.warning(f"Agent identity mismatch detected - updating stored identity")
            stored_identity.agent_id = agent_id
            stored_identity.agent_type = agent_type
            stored_identity.metadata.update(default_metadata)
            return stored_identity
        
        # Create new identity
        identity = AgentIdentity(
            agent_id=agent_id,
            agent_type=agent_type,
            agent_class=agent_class,
            agent_module=agent_module,
            created_at=datetime.now(timezone.utc).isoformat(),
            version=version,
            metadata=default_metadata
        )
        
        # Store identity on agent instance
        agent_instance._agent_identity = identity
        
        return identity

    @staticmethod
    def validate_state_compatibility(
        state: Dict[str, Any],
        agent_identity: AgentIdentity
    ) -> bool:
        """
        Validate that loaded state matches the current agent identity.
        
        Args:
            state: The state dictionary to validate
            agent_identity: The current agent identity to validate against
            
        Returns:
            True if state is compatible with agent identity, False otherwise
        """
        try:
            # Check if state has embedded agent identity
            if "_agent_identity" not in state:
                logger.debug("State has no embedded agent identity, assuming compatible")
                return True
            
            stored_identity_dict = state["_agent_identity"]
            
            # Check agent_id match
            if stored_identity_dict.get("agent_id") != agent_identity.agent_id:
                logger.warning(
                    f"Agent ID mismatch: expected {agent_identity.agent_id}, "
                    f"found {stored_identity_dict.get('agent_id')}"
                )
                return False
            
            # Check agent_type match
            if stored_identity_dict.get("agent_type") != agent_identity.agent_type:
                logger.warning(
                    f"Agent type mismatch: expected {agent_identity.agent_type}, "
                    f"found {stored_identity_dict.get('agent_type')}"
                )
                return False
            
            # Check agent_class match
            if stored_identity_dict.get("agent_class") != agent_identity.agent_class:
                logger.warning(
                    f"Agent class mismatch: expected {agent_identity.agent_class}, "
                    f"found {stored_identity_dict.get('agent_class')}"
                )
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating state compatibility: {e}")
            return False

    @staticmethod
    def _get_agent_id(agent_instance: AgentInterface) -> str:
        """
        Get the agent ID from the agent instance.
        
        The agent MUST define self.agent_id in its __init__ method.
        This ensures stable agent identity across restarts.
        
        Args:
            agent_instance: The agent instance
            
        Returns:
            Agent ID string
            
        Raises:
            ValueError: If agent_id is not defined on the agent instance
        """
        if not hasattr(agent_instance, 'agent_id'):
            raise ValueError(
                f"Agent {agent_instance.__class__.__name__} must define 'self.agent_id' in its __init__ method.\n"
                f"Example:\n"
                f"    def __init__(self):\n"
                f"        super().__init__()\n"
                f"        self.agent_id = 'my_unique_agent_id'\n"
            )
        
        agent_id = agent_instance.agent_id
        
        if not agent_id or not isinstance(agent_id, str) or not agent_id.strip():
            raise ValueError(
                f"Agent {agent_instance.__class__.__name__} has invalid agent_id: {agent_id!r}\n"
                f"agent_id must be a non-empty string."
            )
        
        return agent_id.strip()
