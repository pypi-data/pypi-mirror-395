"""
Elasticsearch Session Storage Backend

This module provides an Elasticsearch-based session storage implementation
for the Agent Framework, enabling scalable session management with full-text
search capabilities.

Key Features:
- Separate indices for metadata, messages, and states
- Full-text search across conversation history
- Scalable and distributed storage
- Automatic index creation and mapping

Indices:
- agent-sessions-metadata: Session metadata
- agent-sessions-messages: Individual messages
- agent-sessions-states: Agent state snapshots
- agent-sessions-insights: Message insights

Environment Variables:
- ELASTICSEARCH_ENABLED: Enable Elasticsearch integration (default: false)
- ELASTICSEARCH_URL: Elasticsearch endpoint (default: http://localhost:9200)
- ELASTICSEARCH_SESSION_INDEX_PREFIX: Index name prefix (default: agent-sessions)

Example:
    ```python
    from agent_framework.session.elasticsearch_session_storage import ElasticsearchSessionStorage
    
    # Create storage backend
    storage = ElasticsearchSessionStorage()
    await storage.initialize()
    
    # Save session
    session_data = SessionData(session_id="123", user_id="user1", ...)
    await storage.save_session("user1", "123", session_data)
    ```

Version: 0.1.0
"""

import os
import logging
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone

from .session_storage import (
    SessionStorageInterface,
    SessionData,
    MessageData,
    MessageInsight,
    MessageMetadata,
    AgentLifecycleData,
    get_shared_elasticsearch_client,
    ELASTICSEARCH_AVAILABLE
)

logger = logging.getLogger(__name__)


def get_circuit_breaker():
    """Get the circuit breaker instance lazily to avoid circular imports."""
    from agent_framework.monitoring.elasticsearch_circuit_breaker import get_elasticsearch_circuit_breaker
    return get_elasticsearch_circuit_breaker()



class ElasticsearchSessionStorage(SessionStorageInterface):
    """
    Session storage backend using Elasticsearch for scalable and searchable storage.
    
    This implementation uses separate Elasticsearch indices for different data types:
    - Metadata: Session-level information
    - Messages: Individual conversation messages
    - States: Agent state snapshots
    - Insights: AI-derived insights from messages
    
    All operations are async and use the shared Elasticsearch client for
    efficient connection pooling.
    """

    def __init__(self, index_prefix: str = None):
        """
        Initialize Elasticsearch session storage.
        
        Args:
            index_prefix: Prefix for index names (default: from env or "agent-sessions")
        """
        if not ELASTICSEARCH_AVAILABLE:
            raise ImportError("Elasticsearch dependencies are not installed. "
                            "Install with: pip install elasticsearch>=8.11.0")
        
        self.index_prefix = index_prefix or os.getenv("ELASTICSEARCH_SESSION_INDEX_PREFIX", "agent-sessions")
        self.metadata_index = f"{self.index_prefix}-metadata"
        self.messages_index = f"{self.index_prefix}-messages"
        self.states_index = f"{self.index_prefix}-states"
        self.insights_index = f"{self.index_prefix}-insights"
        self.lifecycle_index = f"{self.index_prefix}-lifecycle"
        
        self.client = None
        self._initialized = False

    async def initialize(self) -> bool:
        """
        Initialize the Elasticsearch connection and create indices with mappings.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Get shared Elasticsearch client
            self.client = await get_shared_elasticsearch_client()
            
            if self.client is None:
                logger.error("Failed to get Elasticsearch client")
                return False
            
            # Create indices with mappings
            await self._create_indices()
            
            self._initialized = True
            logger.info(f"Elasticsearch session storage initialized with prefix: {self.index_prefix}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Elasticsearch session storage: {e}")
            return False

    async def _create_indices(self):
        """Create Elasticsearch indices with appropriate mappings."""
        try:
            # Metadata index mapping
            metadata_mapping = {
                "mappings": {
                    "properties": {
                        "session_id": {"type": "keyword"},
                        "user_id": {"type": "keyword"},
                        "agent_id": {"type": "keyword"},
                        "agent_type": {"type": "keyword"},
                        "agent_instance_config": {"type": "object", "enabled": False},
                        "session_configuration": {"type": "object", "enabled": False},
                        "correlation_id": {"type": "keyword"},
                        "session_label": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"},
                        "metadata": {"type": "object", "enabled": False}
                    }
                }
            }
            
            # Messages index mapping
            messages_mapping = {
                "mappings": {
                    "properties": {
                        "message_id": {"type": "keyword"},
                        "session_id": {"type": "keyword"},
                        "user_id": {"type": "keyword"},
                        "agent_id": {"type": "keyword"},
                        "agent_type": {"type": "keyword"},
                        "interaction_id": {"type": "keyword"},
                        "sequence_number": {"type": "integer"},
                        "message_type": {"type": "keyword"},
                        "role": {"type": "keyword"},
                        "text_content": {"type": "text"},
                        "parts": {"type": "object", "enabled": False},
                        "response_text_main": {"type": "text"},
                        "created_at": {"type": "date"},
                        "processed_at": {"type": "date"},
                        "parent_message_id": {"type": "keyword"},
                        "related_message_ids": {"type": "keyword"},
                        "processing_time_ms": {"type": "integer"},
                        "model_used": {"type": "keyword"},
                        "token_count": {"type": "object", "enabled": False}
                    }
                }
            }
            
            # States index mapping
            states_mapping = {
                "mappings": {
                    "properties": {
                        "session_id": {"type": "keyword"},
                        "state": {"type": "object", "enabled": False},
                        "updated_at": {"type": "date"}
                    }
                }
            }
            
            # Insights index mapping
            insights_mapping = {
                "mappings": {
                    "properties": {
                        "insight_id": {"type": "keyword"},
                        "message_id": {"type": "keyword"},
                        "session_id": {"type": "keyword"},
                        "user_id": {"type": "keyword"},
                        "agent_id": {"type": "keyword"},
                        "agent_type": {"type": "keyword"},
                        "insight_type": {"type": "keyword"},
                        "insight_data": {"type": "object", "enabled": False},
                        "created_at": {"type": "date"},
                        "created_by": {"type": "keyword"}
                    }
                }
            }
            
            # Lifecycle index mapping
            lifecycle_mapping = {
                "mappings": {
                    "properties": {
                        "lifecycle_id": {"type": "keyword"},
                        "agent_id": {"type": "keyword"},
                        "agent_type": {"type": "keyword"},
                        "event_type": {"type": "keyword"},
                        "session_id": {"type": "keyword"},
                        "user_id": {"type": "keyword"},
                        "timestamp": {"type": "date"},
                        "metadata": {"type": "object", "enabled": False}
                    }
                }
            }
            
            # Create indices if they don't exist
            indices = [
                (self.metadata_index, metadata_mapping),
                (self.messages_index, messages_mapping),
                (self.states_index, states_mapping),
                (self.insights_index, insights_mapping),
                (self.lifecycle_index, lifecycle_mapping)
            ]
            
            for index_name, mapping in indices:
                if not await self.client.indices.exists(index=index_name):
                    await self.client.indices.create(index=index_name, body=mapping)
                    logger.debug(f"Created Elasticsearch index: {index_name}")
                else:
                    logger.debug(f"Elasticsearch index already exists: {index_name}")
                    
        except Exception as e:
            logger.error(f"Failed to create Elasticsearch indices: {e}")
            raise


    async def save_session(self, user_id: str, session_id: str, session_data: SessionData) -> bool:
        """
        Save session metadata to Elasticsearch.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            session_data: Session data to save
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
            # Check circuit breaker
            circuit_breaker = get_circuit_breaker()
            if not circuit_breaker.is_available():
                logger.warning(
                    f"Circuit breaker is open, cannot save session {session_id} "
                    f"(state={circuit_breaker.get_state().value})"
                )
                return False
            
            # Update timestamp
            session_data.updated_at = datetime.now(timezone.utc).isoformat()
            
            # Convert SessionData to document
            doc = {
                "session_id": session_data.session_id,
                "user_id": session_data.user_id,
                "agent_id": session_data.agent_id,
                "agent_type": session_data.agent_type,
                "agent_instance_config": session_data.agent_instance_config,
                "session_configuration": session_data.session_configuration,
                "correlation_id": session_data.correlation_id,
                "session_label": session_data.session_label,
                "created_at": session_data.created_at,
                "updated_at": session_data.updated_at,
                "metadata": session_data.metadata
            }
            
            # Use session_id as document ID for idempotent updates
            doc_id = f"{user_id}_{session_id}"
            
            await self.client.index(
                index=self.metadata_index,
                id=doc_id,
                document=doc,
                refresh='wait_for'  # Make data immediately available for search
            )
            
            # Record success
            circuit_breaker.record_success()
            
            logger.debug(f"Saved session {session_id} for user {user_id} to Elasticsearch")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save session {session_id} to Elasticsearch: {e}")
            
            # Record failure
            circuit_breaker = get_circuit_breaker()
            circuit_breaker.record_failure()
            
            return False

    async def load_session(self, user_id: str, session_id: str) -> Optional[SessionData]:
        """
        Load session metadata from Elasticsearch.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            SessionData if found, None otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return None
            
            # Check circuit breaker
            circuit_breaker = get_circuit_breaker()
            if not circuit_breaker.is_available():
                logger.warning(
                    f"Circuit breaker is open, cannot load session {session_id} "
                    f"(state={circuit_breaker.get_state().value})"
                )
                return None
            
            doc_id = f"{user_id}_{session_id}"
            
            response = await self.client.get(
                index=self.metadata_index,
                id=doc_id
            )
            
            # Record success
            circuit_breaker.record_success()
            
            if response and response.get("found"):
                source = response["_source"]
                session_data = SessionData(**source)
                logger.debug(f"Loaded session {session_id} for user {user_id} from Elasticsearch")
                return session_data
            
            return None
            
        except Exception as e:
            if "not_found" not in str(e).lower():
                logger.error(f"Failed to load session {session_id} from Elasticsearch: {e}")
                
                # Record failure
                circuit_breaker = get_circuit_breaker()
                circuit_breaker.record_failure()
            
            return None

    async def delete_session(self, user_id: str, session_id: str) -> bool:
        """
        Delete session and all related data from Elasticsearch.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
            # Delete session metadata
            doc_id = f"{user_id}_{session_id}"
            await self.client.delete(
                index=self.metadata_index,
                id=doc_id,
                ignore=[404]
            )
            
            # Delete all messages for this session
            await self.client.delete_by_query(
                index=self.messages_index,
                body={"query": {"term": {"session_id": session_id}}}
            )
            
            # Delete all insights for this session
            await self.client.delete_by_query(
                index=self.insights_index,
                body={"query": {"term": {"session_id": session_id}}}
            )
            
            # Delete agent state
            await self.client.delete_by_query(
                index=self.states_index,
                body={"query": {"term": {"session_id": session_id}}}
            )
            
            logger.debug(f"Deleted session {session_id} for user {user_id} from Elasticsearch")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete session {session_id} from Elasticsearch: {e}")
            return False

    async def list_user_sessions(self, user_id: str) -> List[str]:
        """
        List all session IDs for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of session IDs sorted by updated_at (most recent first)
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            response = await self.client.search(
                index=self.metadata_index,
                body={
                    "query": {"term": {"user_id": user_id}},
                    "sort": [{"updated_at": {"order": "desc"}}],
                    "_source": ["session_id"],
                    "size": 10000
                }
            )
            
            sessions = [hit["_source"]["session_id"] for hit in response["hits"]["hits"]]
            return sessions
            
        except Exception as e:
            logger.error(f"Failed to list sessions for user {user_id} from Elasticsearch: {e}")
            return []

    async def list_all_users_with_sessions(self) -> List[str]:
        """
        List all user IDs who have at least one session.
        
        Returns:
            List of user IDs
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            response = await self.client.search(
                index=self.metadata_index,
                body={
                    "size": 0,
                    "aggs": {
                        "unique_users": {
                            "terms": {"field": "user_id", "size": 10000}
                        }
                    }
                }
            )
            
            users = [bucket["key"] for bucket in response["aggregations"]["unique_users"]["buckets"]]
            return users
            
        except Exception as e:
            logger.error(f"Failed to list all users from Elasticsearch: {e}")
            return []


    async def add_message(self, message_data: MessageData) -> bool:
        """
        Add a message to Elasticsearch.
        
        Args:
            message_data: Message data to store
            
        Returns:
            True if addition successful, False otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
            # Check circuit breaker
            circuit_breaker = get_circuit_breaker()
            if not circuit_breaker.is_available():
                logger.warning(
                    f"Circuit breaker is open, cannot add message {message_data.message_id} "
                    f"(state={circuit_breaker.get_state().value})"
                )
                return False
            
            # Auto-increment sequence number
            if message_data.sequence_number == 0:
                # Get the highest sequence number for this session
                response = await self.client.search(
                    index=self.messages_index,
                    body={
                        "query": {"term": {"session_id": message_data.session_id}},
                        "sort": [{"sequence_number": {"order": "desc"}}],
                        "size": 1,
                        "_source": ["sequence_number"]
                    }
                )
                
                if response["hits"]["hits"]:
                    last_seq = response["hits"]["hits"][0]["_source"]["sequence_number"]
                    message_data.sequence_number = last_seq + 1
                else:
                    message_data.sequence_number = 1
            
            # Convert MessageData to document
            doc = {
                "message_id": message_data.message_id,
                "session_id": message_data.session_id,
                "user_id": message_data.user_id,
                "agent_id": message_data.agent_id,
                "agent_type": message_data.agent_type,
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
                "token_count": message_data.token_count
            }
            
            await self.client.index(
                index=self.messages_index,
                id=message_data.message_id,
                document=doc,
                refresh='wait_for'  # Make data immediately available for search
            )
            
            # Record success
            circuit_breaker.record_success()
            
            logger.debug(f"Added message {message_data.message_id} to Elasticsearch")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add message {message_data.message_id} to Elasticsearch: {e}")
            
            # Record failure
            circuit_breaker = get_circuit_breaker()
            circuit_breaker.record_failure()
            
            return False

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
            List of MessageData objects sorted by sequence_number
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            body = {
                "query": {"term": {"session_id": session_id}},
                "sort": [{"sequence_number": {"order": "asc"}}],
                "size": limit or 10000
            }
            
            if offset:
                body["from"] = offset
            
            response = await self.client.search(
                index=self.messages_index,
                body=body
            )
            
            messages = []
            for hit in response["hits"]["hits"]:
                source = hit["_source"]
                messages.append(MessageData(**source))
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to get conversation history for session {session_id}: {e}")
            return []

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
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            # Use aggregation to group by interaction_id
            response = await self.client.search(
                index=self.messages_index,
                body={
                    "query": {"term": {"session_id": session_id}},
                    "size": 0,
                    "aggs": {
                        "interactions": {
                            "terms": {
                                "field": "interaction_id",
                                "size": limit,
                                "order": {"max_sequence": "desc"}
                            },
                            "aggs": {
                                "max_sequence": {"max": {"field": "sequence_number"}},
                                "messages": {
                                    "top_hits": {
                                        "size": 100,
                                        "sort": [{"sequence_number": {"order": "asc"}}]
                                    }
                                }
                            }
                        }
                    }
                }
            )
            
            exchanges = []
            for bucket in response["aggregations"]["interactions"]["buckets"]:
                exchange_messages = []
                for hit in bucket["messages"]["hits"]["hits"]:
                    source = hit["_source"]
                    exchange_messages.append(MessageData(**source))
                exchanges.append(exchange_messages)
            
            return exchanges
            
        except Exception as e:
            logger.error(f"Failed to get conversation exchanges for session {session_id}: {e}")
            return []

    async def search_messages(
        self,
        query: str,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        limit: int = 100
    ) -> List[MessageData]:
        """
        Full-text search across messages.
        
        Args:
            query: Search query string
            user_id: Optional user filter
            session_id: Optional session filter
            limit: Maximum number of results
            
        Returns:
            List of matching MessageData objects
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            # Build query
            must_clauses = [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["text_content", "response_text_main"]
                    }
                }
            ]
            
            if user_id:
                must_clauses.append({"term": {"user_id": user_id}})
            if session_id:
                must_clauses.append({"term": {"session_id": session_id}})
            
            response = await self.client.search(
                index=self.messages_index,
                body={
                    "query": {"bool": {"must": must_clauses}},
                    "sort": [{"created_at": {"order": "desc"}}],
                    "size": limit
                }
            )
            
            messages = []
            for hit in response["hits"]["hits"]:
                source = hit["_source"]
                messages.append(MessageData(**source))
            
            return messages
            
        except Exception as e:
            logger.error(f"Failed to search messages: {e}")
            return []


    async def add_insight(self, insight: MessageInsight) -> bool:
        """
        Add an insight for a message.
        
        Args:
            insight: Insight data to store
            
        Returns:
            True if addition successful, False otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
            doc = {
                "insight_id": insight.insight_id,
                "message_id": insight.message_id,
                "session_id": insight.session_id,
                "user_id": insight.user_id,
                "agent_id": insight.agent_id,
                "agent_type": insight.agent_type,
                "insight_type": insight.insight_type,
                "insight_data": insight.insight_data,
                "created_at": insight.created_at,
                "created_by": insight.created_by
            }
            
            await self.client.index(
                index=self.insights_index,
                id=insight.insight_id,
                document=doc
            )
            
            logger.debug(f"Added insight {insight.insight_id} to Elasticsearch")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add insight {insight.insight_id} to Elasticsearch: {e}")
            return False

    async def add_metadata(self, metadata: MessageMetadata) -> bool:
        """
        Add metadata for a message.
        
        Args:
            metadata: Metadata to store
            
        Returns:
            True if addition successful, False otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
            # Store metadata as part of the message document
            # Update the message with additional metadata field
            doc = {
                "metadata_id": metadata.metadata_id,
                "message_id": metadata.message_id,
                "session_id": metadata.session_id,
                "agent_id": metadata.agent_id,
                "agent_type": metadata.agent_type,
                "metadata_type": metadata.metadata_type,
                "metadata": metadata.metadata,
                "created_at": metadata.created_at,
                "created_by": metadata.created_by
            }
            
            # Store in insights index (can be used for both insights and metadata)
            await self.client.index(
                index=self.insights_index,
                id=metadata.metadata_id,
                document=doc
            )
            
            logger.debug(f"Added metadata {metadata.metadata_id} to Elasticsearch")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add metadata {metadata.metadata_id} to Elasticsearch: {e}")
            return False

    async def get_message_with_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get message with all its insights and metadata.
        
        Args:
            message_id: Message identifier
            
        Returns:
            Dictionary containing message, insights, and metadata, or None if not found
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return None
            
            # Get message
            message_response = await self.client.get(
                index=self.messages_index,
                id=message_id
            )
            
            if not message_response.get("found"):
                return None
            
            message = MessageData(**message_response["_source"])
            
            # Get insights and metadata
            insights_response = await self.client.search(
                index=self.insights_index,
                body={
                    "query": {"term": {"message_id": message_id}},
                    "size": 1000
                }
            )
            
            insights = []
            metadata_list = []
            
            for hit in insights_response["hits"]["hits"]:
                source = hit["_source"]
                if "insight_type" in source:
                    insights.append(MessageInsight(**source))
                elif "metadata_type" in source:
                    metadata_list.append(MessageMetadata(**source))
            
            return {
                "message": message,
                "insights": insights,
                "metadata": metadata_list
            }
            
        except Exception as e:
            logger.error(f"Failed to get message details for {message_id}: {e}")
            return None

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
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
            doc_id = f"{user_id}_{session_id}"
            
            update_doc = {
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            if correlation_id is not None:
                update_doc["correlation_id"] = correlation_id
            
            if metadata is not None:
                # Merge with existing metadata
                existing = await self.load_session(user_id, session_id)
                if existing and existing.metadata:
                    update_doc["metadata"] = {**existing.metadata, **metadata}
                else:
                    update_doc["metadata"] = metadata
            
            await self.client.update(
                index=self.metadata_index,
                id=doc_id,
                body={"doc": update_doc}
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update session metadata for {session_id}: {e}")
            return False

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
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
            doc_id = f"{user_id}_{session_id}"
            
            await self.client.update(
                index=self.metadata_index,
                id=doc_id,
                body={
                    "doc": {
                        "session_label": label,
                        "updated_at": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update session label for {session_id}: {e}")
            return False

    async def list_user_sessions_with_info(self, user_id: str) -> List[Dict[str, Any]]:
        """
        List all sessions for a user with metadata including labels.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of dictionaries containing session information
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            response = await self.client.search(
                index=self.metadata_index,
                body={
                    "query": {"term": {"user_id": user_id}},
                    "sort": [{"updated_at": {"order": "desc"}}],
                    "size": 10000
                }
            )
            
            sessions_info = []
            for hit in response["hits"]["hits"]:
                source = hit["_source"]
                sessions_info.append({
                    "session_id": source.get("session_id"),
                    "session_label": source.get("session_label"),
                    "created_at": source.get("created_at"),
                    "updated_at": source.get("updated_at"),
                    "correlation_id": source.get("correlation_id"),
                    "metadata": source.get("metadata"),
                    "agent_id": source.get("agent_id"),
                    "agent_type": source.get("agent_type"),
                    "session_configuration": source.get("session_configuration")
                })
            
            return sessions_info
            
        except Exception as e:
            logger.error(f"Failed to list user sessions with info for {user_id}: {e}")
            return []


    async def list_sessions_by_agent_id(self, agent_id: str) -> List[str]:
        """
        List all session IDs for a specific agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of session IDs
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            response = await self.client.search(
                index=self.metadata_index,
                body={
                    "query": {"term": {"agent_id": agent_id}},
                    "sort": [{"updated_at": {"order": "desc"}}],
                    "_source": ["session_id"],
                    "size": 10000
                }
            )
            
            sessions = [hit["_source"]["session_id"] for hit in response["hits"]["hits"]]
            return sessions
            
        except Exception as e:
            logger.error(f"Failed to list sessions for agent {agent_id}: {e}")
            return []

    async def list_sessions_by_agent_type(self, agent_type: str) -> List[str]:
        """
        List all session IDs for a specific agent type.
        
        Args:
            agent_type: Agent type identifier
            
        Returns:
            List of session IDs
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            response = await self.client.search(
                index=self.metadata_index,
                body={
                    "query": {"term": {"agent_type": agent_type}},
                    "sort": [{"updated_at": {"order": "desc"}}],
                    "_source": ["session_id"],
                    "size": 10000
                }
            )
            
            sessions = [hit["_source"]["session_id"] for hit in response["hits"]["hits"]]
            return sessions
            
        except Exception as e:
            logger.error(f"Failed to list sessions for agent type {agent_type}: {e}")
            return []

    async def get_user_sessions_by_agent(
        self, 
        user_id: str, 
        agent_id: Optional[str] = None, 
        agent_type: Optional[str] = None
    ) -> List[str]:
        """
        Get user sessions filtered by agent identity.
        
        Args:
            user_id: User identifier
            agent_id: Optional agent ID filter
            agent_type: Optional agent type filter
            
        Returns:
            List of session IDs
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            # Build query
            must_clauses = [{"term": {"user_id": user_id}}]
            
            if agent_id:
                must_clauses.append({"term": {"agent_id": agent_id}})
            if agent_type:
                must_clauses.append({"term": {"agent_type": agent_type}})
            
            response = await self.client.search(
                index=self.metadata_index,
                body={
                    "query": {"bool": {"must": must_clauses}},
                    "sort": [{"updated_at": {"order": "desc"}}],
                    "_source": ["session_id"],
                    "size": 10000
                }
            )
            
            sessions = [hit["_source"]["session_id"] for hit in response["hits"]["hits"]]
            return sessions
            
        except Exception as e:
            logger.error(f"Failed to get user sessions by agent for {user_id}: {e}")
            return []

    async def save_agent_state(self, session_id: str, agent_state: Dict[str, Any]) -> bool:
        """
        Save the agent's state to Elasticsearch.
        
        Args:
            session_id: Session identifier
            agent_state: Agent state to save
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
            doc = {
                "session_id": session_id,
                "state": agent_state,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            await self.client.index(
                index=self.states_index,
                id=session_id,
                document=doc,
                refresh='wait_for'  # Make data immediately available for search
            )
            
            logger.debug(f"Saved agent state for session {session_id} to Elasticsearch")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save agent state for session {session_id}: {e}")
            return False

    async def load_agent_state(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load the agent's state from Elasticsearch.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Agent state dictionary if found, None otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return None
            
            response = await self.client.get(
                index=self.states_index,
                id=session_id
            )
            
            if response and response.get("found"):
                return response["_source"].get("state")
            
            return None
            
        except Exception as e:
            if "not_found" not in str(e).lower():
                logger.error(f"Failed to load agent state for session {session_id}: {e}")
            return None

    async def load_session_configuration(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Load session configuration for a session.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            
        Returns:
            Session configuration dictionary if found, None otherwise
        """
        try:
            session_data = await self.load_session(user_id, session_id)
            if session_data:
                return session_data.session_configuration
            return None
            
        except Exception as e:
            logger.error(f"Failed to load session configuration for {session_id}: {e}")
            return None

    async def add_agent_lifecycle_event(self, lifecycle_data: AgentLifecycleData) -> bool:
        """
        Add an agent lifecycle event to Elasticsearch.
        
        Args:
            lifecycle_data: Lifecycle event data
            
        Returns:
            True if addition successful, False otherwise
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return False
            
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
            
            await self.client.index(
                index=self.lifecycle_index,
                id=lifecycle_data.lifecycle_id,
                document=doc
            )
            
            logger.debug(f"Added lifecycle event {lifecycle_data.event_type} for agent {lifecycle_data.agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add lifecycle event to Elasticsearch: {e}")
            return False

    async def get_agent_lifecycle_events(self, agent_id: str) -> List[AgentLifecycleData]:
        """
        Get lifecycle events for a specific agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of lifecycle events
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return []
            
            response = await self.client.search(
                index=self.lifecycle_index,
                body={
                    "query": {"term": {"agent_id": agent_id}},
                    "sort": [{"timestamp": {"order": "desc"}}],
                    "size": 10000
                }
            )
            
            events = []
            for hit in response["hits"]["hits"]:
                source = hit["_source"]
                events.append(AgentLifecycleData(**source))
            
            return events
            
        except Exception as e:
            logger.error(f"Failed to get lifecycle events for agent {agent_id}: {e}")
            return []

    async def get_agent_usage_statistics(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get usage statistics by agent type.
        
        Args:
            agent_type: Optional agent type filter
            
        Returns:
            Dictionary containing usage statistics
        """
        try:
            if not self._initialized:
                logger.error("Elasticsearch session storage not initialized")
                return {}
            
            # Build aggregation query
            agg_query = {
                "size": 0,
                "aggs": {
                    "by_agent_type": {
                        "terms": {"field": "agent_type", "size": 100},
                        "aggs": {
                            "unique_agents": {
                                "cardinality": {"field": "agent_id"}
                            }
                        }
                    },
                    "total_sessions": {"value_count": {"field": "session_id"}},
                    "unique_agents": {"cardinality": {"field": "agent_id"}}
                }
            }
            
            if agent_type:
                agg_query["query"] = {"term": {"agent_type": agent_type}}
            
            response = await self.client.search(
                index=self.metadata_index,
                body=agg_query
            )
            
            # Count messages
            message_count_response = await self.client.count(index=self.messages_index)
            
            # Count lifecycle events by type
            lifecycle_response = await self.client.search(
                index=self.lifecycle_index,
                body={
                    "size": 0,
                    "aggs": {
                        "by_event_type": {
                            "terms": {"field": "event_type", "size": 100}
                        }
                    }
                }
            )
            
            stats = {
                "total_agents": response["aggregations"]["unique_agents"]["value"],
                "total_sessions": response["aggregations"]["total_sessions"]["value"],
                "total_messages": message_count_response["count"],
                "agent_types": {},
                "lifecycle_events": {}
            }
            
            # Process agent type statistics
            for bucket in response["aggregations"]["by_agent_type"]["buckets"]:
                stats["agent_types"][bucket["key"]] = {
                    "session_count": bucket["doc_count"],
                    "unique_agents": bucket["unique_agents"]["value"]
                }
            
            # Process lifecycle events
            for bucket in lifecycle_response["aggregations"]["by_event_type"]["buckets"]:
                stats["lifecycle_events"][bucket["key"]] = bucket["doc_count"]
            
            # Filter by specific agent type if requested
            if agent_type and agent_type in stats["agent_types"]:
                return {
                    "agent_type": agent_type,
                    **stats["agent_types"][agent_type]
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get usage statistics from Elasticsearch: {e}")
            return {}

    async def cleanup(self) -> None:
        """
        Clean up resources.
        
        Note: The Elasticsearch client is shared and managed globally,
        so we don't close it here.
        """
        logger.debug("Elasticsearch session storage cleanup (client is shared)")
        self._initialized = False
