"""
LlamaIndex Memory Adapter

This module provides an adapter between the framework's SessionStorage
and LlamaIndex's Memory system, allowing seamless integration of conversation
history into LlamaIndex agents.

The adapter:
- Loads conversation history from SessionStorage
- Converts MessageData to LlamaIndex ChatMessage format
- Creates a Memory object that can be used with LlamaIndex agents
- Keeps memory synchronized with SessionStorage

Version: 0.1.0
"""

import logging
from typing import Optional, List
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.memory import ChatMemoryBuffer

from ..session.session_storage import SessionStorageInterface, MessageData

logger = logging.getLogger(__name__)

# Global memory cache shared across all adapter instances
_GLOBAL_MEMORY_CACHE: dict[str, ChatMemoryBuffer] = {}



class LlamaIndexMemoryAdapter:
    """
    Adapter that bridges SessionStorage and LlamaIndex Memory.
    
    This adapter loads conversation history from SessionStorage and creates
    a LlamaIndex Memory object that can be used with agents.
    """
    
    def __init__(self, session_storage: SessionStorageInterface):
        """
        Initialize the memory adapter.
        
        Args:
            session_storage: The session storage backend to use
        """
        self.session_storage = session_storage
        # Use global cache instead of instance cache
        self._memory_cache = _GLOBAL_MEMORY_CACHE
    
    async def get_memory_for_session(
        self, 
        session_id: str,
        user_id: str,
        token_limit: int = 30000
    ) -> ChatMemoryBuffer:
        """
        Get or create a Memory object for a session.
        
        This method:
        1. Checks if memory is already cached
        2. If not, loads conversation history from SessionStorage
        3. Converts messages to LlamaIndex format
        4. Creates a Memory object with the history
        
        Args:
            session_id: The session identifier
            user_id: The user identifier
            token_limit: Maximum tokens for short-term memory
            
        Returns:
            Memory object ready to use with LlamaIndex agents
        """
        # Check cache first
        cache_key = f"{user_id}:{session_id}"
        if cache_key in self._memory_cache:
            logger.info(f"✅ Using cached memory for session {session_id}")
            return self._memory_cache[cache_key]
        
        # Create new memory
        logger.info(f"🆕 Creating new memory for session {session_id}")
        memory = ChatMemoryBuffer.from_defaults(
            token_limit=token_limit,
        )
        
        # Load conversation history from SessionStorage
        try:
            message_history = await self.session_storage.get_conversation_history(
                session_id=session_id,
                limit=100  # Load last 100 messages
            )
            
            if message_history:
                # Convert to LlamaIndex ChatMessage format
                chat_messages = self._convert_to_chat_messages(message_history)
                
                # Put messages into memory
                if chat_messages:
                    memory.put_messages(chat_messages)
                    logger.info(f"📚 Loaded {len(chat_messages)} messages into memory for session {session_id}")
                    logger.info(f"📝 First message: {chat_messages[0].content[:50]}..." if chat_messages else "")
            else:
                logger.info(f"⚠️ No existing history for session {session_id}, starting fresh")
                
        except Exception as e:
            logger.error(f"Error loading conversation history for session {session_id}: {e}")
            # Continue with empty memory rather than failing
        
        # Cache the memory
        self._memory_cache[cache_key] = memory
        
        return memory
    
    def _convert_to_chat_messages(self, message_data_list: List[MessageData]) -> List[ChatMessage]:
        """
        Convert MessageData objects to LlamaIndex ChatMessage objects.
        
        Args:
            message_data_list: List of MessageData from SessionStorage
            
        Returns:
            List of ChatMessage objects for LlamaIndex
        """
        chat_messages = []
        
        for msg_data in message_data_list:
            # Determine role
            if msg_data.role == "user":
                role = MessageRole.USER
            elif msg_data.role == "assistant":
                role = MessageRole.ASSISTANT
            elif msg_data.role == "system":
                role = MessageRole.SYSTEM
            else:
                logger.warning(f"Unknown role '{msg_data.role}', defaulting to USER")
                role = MessageRole.USER
            
            # Get content - prefer text_content, fallback to response_text_main
            content = msg_data.text_content or msg_data.response_text_main or ""
            
            # Create ChatMessage
            chat_message = ChatMessage(
                role=role,
                content=content
            )
            
            chat_messages.append(chat_message)
        
        return chat_messages
    
    def clear_cache(self, session_id: Optional[str] = None, user_id: Optional[str] = None):
        """
        Clear memory cache.
        
        Args:
            session_id: If provided, clear only this session
            user_id: If provided, clear all sessions for this user
        """
        if session_id and user_id:
            cache_key = f"{user_id}:{session_id}"
            if cache_key in self._memory_cache:
                del self._memory_cache[cache_key]
                logger.info(f"Cleared memory cache for session {session_id}")
        elif user_id:
            # Clear all sessions for user
            keys_to_remove = [k for k in self._memory_cache.keys() if k.startswith(f"{user_id}:")]
            for key in keys_to_remove:
                del self._memory_cache[key]
            logger.info(f"Cleared memory cache for user {user_id} ({len(keys_to_remove)} sessions)")
        else:
            # Clear all
            self._memory_cache.clear()
            logger.info("Cleared all memory cache")
