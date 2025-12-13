"""
Elasticsearch Configuration Provider

Provides dynamic agent configuration retrieval from Elasticsearch with caching.

This module implements:
- Configuration retrieval from Elasticsearch
- In-memory caching with configurable TTL
- LRU eviction for memory management
- Cache invalidation on updates
- Automatic fallback to hardcoded/default configs

Environment Variables:
- ELASTICSEARCH_CONFIG_INDEX: Index name for configurations (default: "agent-configs")
- ELASTICSEARCH_CONFIG_CACHE_TTL: Cache TTL in seconds (default: 300)
- ELASTICSEARCH_CONFIG_CACHE_MAX_SIZE: Maximum cache entries (default: 100)

Example:
    ```python
    from agent_framework.core.elasticsearch_config_provider import ElasticsearchConfigProvider
    
    # Create provider
    provider = ElasticsearchConfigProvider()
    await provider.initialize()
    
    # Get configuration
    config = await provider.get_agent_config("my-agent")
    
    # Update configuration
    await provider.update_agent_config("my-agent", {"system_prompt": "..."})
    ```
"""

import os
import time
import logging
from typing import Dict, Any, Optional
from collections import OrderedDict
from datetime import datetime

logger = logging.getLogger(__name__)


def get_circuit_breaker():
    """Get the circuit breaker instance lazily to avoid circular imports."""
    from agent_framework.monitoring.elasticsearch_circuit_breaker import get_elasticsearch_circuit_breaker
    return get_elasticsearch_circuit_breaker()


class ElasticsearchConfigProvider:
    """
    Provides agent configuration from Elasticsearch with caching.
    
    This class retrieves agent configurations from Elasticsearch and caches them
    in memory with TTL-based expiration and LRU eviction.
    
    Attributes:
        client: Elasticsearch client instance
        index_name: Name of the configuration index
        cache_ttl: Time-to-live for cached entries in seconds
        cache_max_size: Maximum number of entries in cache
        _cache: OrderedDict for LRU cache implementation
        _cache_timestamps: Timestamps for TTL tracking
    """
    
    def __init__(
        self,
        es_client: Optional[Any] = None,
        index_name: Optional[str] = None,
        cache_ttl: Optional[int] = None,
        cache_max_size: Optional[int] = None
    ):
        """
        Initialize the configuration provider.
        
        Args:
            es_client: Elasticsearch client instance (if None, will get shared client)
            index_name: Name of the configuration index
            cache_ttl: Cache TTL in seconds
            cache_max_size: Maximum cache entries
        """
        self.client = es_client
        self.index_name = index_name or os.getenv("ELASTICSEARCH_CONFIG_INDEX", "agent-configs")
        self.cache_ttl = cache_ttl or int(os.getenv("ELASTICSEARCH_CONFIG_CACHE_TTL", "300"))
        self.cache_max_size = cache_max_size or int(os.getenv("ELASTICSEARCH_CONFIG_CACHE_MAX_SIZE", "100"))
        
        # LRU cache using OrderedDict
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._cache_timestamps: Dict[str, float] = {}
        
        logger.info(
            f"[ElasticsearchConfigProvider] Initialized with "
            f"index={self.index_name}, ttl={self.cache_ttl}s, max_size={self.cache_max_size}"
        )
    
    async def initialize(self) -> None:
        """
        Initialize the provider and ensure index exists.
        
        Gets the shared Elasticsearch client if not provided and creates
        the configuration index with appropriate mappings.
        """
        # Get shared client if not provided
        if self.client is None:
            from agent_framework.session.session_storage import get_shared_elasticsearch_client
            self.client = await get_shared_elasticsearch_client()
        
        if self.client is None:
            logger.warning("[ElasticsearchConfigProvider] Elasticsearch client not available")
            return
        
        try:
            # Check if index exists
            exists = await self.client.indices.exists(index=self.index_name)
            
            if not exists:
                # Create index with mappings
                mappings = {
                    "properties": {
                        "agent_id": {"type": "keyword"},
                        "agent_type": {"type": "keyword"},
                        "version": {"type": "integer"},
                        "updated_at": {"type": "date"},
                        "updated_by": {"type": "keyword"},
                        "config": {"type": "object", "enabled": True},
                        "metadata": {"type": "object", "enabled": True},
                        "active": {"type": "boolean"}
                    }
                }
                
                await self.client.indices.create(
                    index=self.index_name,
                    mappings=mappings
                )
                
                logger.info(f"[ElasticsearchConfigProvider] Created index: {self.index_name}")
            else:
                logger.debug(f"[ElasticsearchConfigProvider] Index already exists: {self.index_name}")
        
        except Exception as e:
            logger.error(f"[ElasticsearchConfigProvider] Failed to initialize index: {e}")
    
    def _check_cache(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Check if configuration is in cache and not expired.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Cached configuration if valid, None otherwise
        """
        if agent_id not in self._cache:
            logger.debug(f"[ElasticsearchConfigProvider] Cache miss for agent_id={agent_id}")
            return None
        
        # Check TTL
        timestamp = self._cache_timestamps.get(agent_id, 0)
        age = time.time() - timestamp
        
        if age > self.cache_ttl:
            logger.debug(
                f"[ElasticsearchConfigProvider] Cache expired for agent_id={agent_id} "
                f"(age={age:.1f}s, ttl={self.cache_ttl}s)"
            )
            # Remove expired entry
            self._invalidate_cache(agent_id)
            return None
        
        # Move to end (most recently used)
        self._cache.move_to_end(agent_id)
        
        logger.debug(
            f"[ElasticsearchConfigProvider] Cache hit for agent_id={agent_id} "
            f"(age={age:.1f}s, ttl={self.cache_ttl}s)"
        )
        return self._cache[agent_id]
    
    def _add_to_cache(self, agent_id: str, config: Dict[str, Any]) -> None:
        """
        Add configuration to cache with LRU eviction.
        
        Args:
            agent_id: Agent identifier
            config: Configuration to cache
        """
        # Check if cache is full
        if len(self._cache) >= self.cache_max_size and agent_id not in self._cache:
            # Evict least recently used (first item)
            evicted_id = next(iter(self._cache))
            self._cache.pop(evicted_id)
            self._cache_timestamps.pop(evicted_id, None)
            logger.debug(f"[ElasticsearchConfigProvider] Evicted LRU entry: {evicted_id}")
        
        # Add to cache
        self._cache[agent_id] = config
        self._cache_timestamps[agent_id] = time.time()
        
        # Move to end (most recently used)
        self._cache.move_to_end(agent_id)
        
        logger.debug(
            f"[ElasticsearchConfigProvider] Added to cache: agent_id={agent_id} "
            f"(cache_size={len(self._cache)}/{self.cache_max_size})"
        )
    
    def _invalidate_cache(self, agent_id: str) -> None:
        """
        Remove configuration from cache.
        
        Args:
            agent_id: Agent identifier
        """
        if agent_id in self._cache:
            self._cache.pop(agent_id)
            self._cache_timestamps.pop(agent_id, None)
            logger.debug(f"[ElasticsearchConfigProvider] Invalidated cache for agent_id={agent_id}")
    
    async def get_agent_config(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get agent configuration with cache checking.
        
        Checks cache first, then queries Elasticsearch if not found or expired.
        Only returns configurations where active=true.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Configuration dictionary if found and active, None otherwise
        """
        # Check cache first
        cached_config = self._check_cache(agent_id)
        if cached_config is not None:
            return cached_config
        
        # Query Elasticsearch
        if self.client is None:
            logger.warning("[ElasticsearchConfigProvider] Elasticsearch client not available")
            return None
        
        # Check circuit breaker
        circuit_breaker = get_circuit_breaker()
        if not circuit_breaker.is_available():
            logger.warning(
                f"[ElasticsearchConfigProvider] Circuit breaker is open, cannot get config for agent_id={agent_id} "
                f"(state={circuit_breaker.get_state().value})"
            )
            return None
        
        try:
            # Search for active configuration
            # Use agent_id.keyword for exact match (agent_id is text field with keyword subfield)
            response = await self.client.search(
                index=self.index_name,
                body={
                    "query": {
                        "bool": {
                            "must": [
                                {"term": {"agent_id.keyword": agent_id}},
                                {"term": {"active": True}}
                            ]
                        }
                    },
                    "sort": [{"version": {"order": "desc"}}],
                    "size": 1
                }
            )
            
            # Record success
            circuit_breaker.record_success()
            
            hits = response.get("hits", {}).get("hits", [])
            
            if not hits:
                logger.debug(f"[ElasticsearchConfigProvider] No active config found for agent_id={agent_id}")
                return None
            
            # Extract configuration
            doc = hits[0]["_source"]
            config = doc.get("config", {})
            
            # Add to cache
            self._add_to_cache(agent_id, config)
            
            logger.info(
                f"[ElasticsearchConfigProvider] Retrieved config for agent_id={agent_id} "
                f"(version={doc.get('version', 'unknown')})"
            )
            
            return config
        
        except Exception as e:
            logger.error(f"[ElasticsearchConfigProvider] Failed to get config for agent_id={agent_id}: {e}")
            
            # Record failure
            circuit_breaker = get_circuit_breaker()
            circuit_breaker.record_failure()
            
            return None
    
    async def update_agent_config(
        self,
        agent_id: str,
        config: Dict[str, Any],
        agent_type: Optional[str] = None,
        updated_by: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        active: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Update agent configuration with automatic versioning.
        
        Creates a new version of the configuration, deactivates old versions,
        and invalidates the cache.
        
        Args:
            agent_id: Agent identifier
            config: Configuration dictionary
            agent_type: Type of agent (optional)
            updated_by: User who updated the config (optional)
            metadata: Additional metadata (optional)
            active: Whether configuration is active
            
        Returns:
            Dictionary with doc_id, version, and agent_id if successful, None otherwise
        """
        if self.client is None:
            logger.warning("[ElasticsearchConfigProvider] Elasticsearch client not available")
            return None
        
        # Check circuit breaker
        circuit_breaker = get_circuit_breaker()
        if not circuit_breaker.is_available():
            logger.warning(
                f"[ElasticsearchConfigProvider] Circuit breaker is open, cannot update config for agent_id={agent_id} "
                f"(state={circuit_breaker.get_state().value})"
            )
            return None
        
        try:
            # Get current version
            current_version = 0
            try:
                response = await self.client.search(
                    index=self.index_name,
                    body={
                        "query": {"term": {"agent_id.keyword": agent_id}},
                        "sort": [{"version": {"order": "desc"}}],
                        "size": 1
                    }
                )
                
                hits = response.get("hits", {}).get("hits", [])
                if hits:
                    current_version = hits[0]["_source"].get("version", 0)
                    logger.debug(f"[ElasticsearchConfigProvider] Found existing version {current_version} for agent_id={agent_id}")
            except Exception as e:
                logger.debug(f"[ElasticsearchConfigProvider] No existing config found: {e}")
            
            # Deactivate all old active versions for this agent_id (always, even if current_version=0)
            try:
                result = await self.client.update_by_query(
                    index=self.index_name,
                    body={
                        "script": {"source": "ctx._source.active = false"},
                        "query": {
                            "bool": {
                                "must": [
                                    {"term": {"agent_id.keyword": agent_id}},
                                    {"term": {"active": True}}
                                ]
                            }
                        }
                    }
                )
                updated_count = result.get("updated", 0)
                if updated_count > 0:
                    logger.debug(f"[ElasticsearchConfigProvider] Deactivated {updated_count} old version(s) for agent_id={agent_id}")
            except Exception as e:
                logger.warning(f"[ElasticsearchConfigProvider] Failed to deactivate old versions: {e}")
            
            # Create new document with incremented version
            doc = {
                "agent_id": agent_id,
                "agent_type": agent_type or "unknown",
                "version": current_version + 1,
                "updated_at": datetime.utcnow().isoformat(),
                "updated_by": updated_by or "system",
                "config": config,
                "metadata": metadata or {},
                "active": active
            }
            
            # Index document (ES will generate a unique _id)
            # Use refresh=true to make the document immediately searchable
            result = await self.client.index(
                index=self.index_name,
                document=doc,
                refresh=True
            )
            
            doc_id = result.get("_id")
            
            # Record success
            circuit_breaker.record_success()
            
            # Invalidate cache
            self._invalidate_cache(agent_id)
            
            logger.info(
                f"[ElasticsearchConfigProvider] Updated config for agent_id={agent_id} "
                f"(version={doc['version']}, doc_id={doc_id}, active={active})"
            )
            
            return {
                "doc_id": doc_id,
                "version": doc["version"],
                "agent_id": agent_id
            }
        
        except Exception as e:
            logger.error(f"[ElasticsearchConfigProvider] Failed to update config for agent_id={agent_id}: {e}")
            
            # Record failure
            circuit_breaker = get_circuit_breaker()
            circuit_breaker.record_failure()
            
            return None
    
    async def get_config_versions(self, agent_id: str, limit: int = 10) -> list[Dict[str, Any]]:
        """
        Get configuration version history for an agent.
        
        Args:
            agent_id: Agent identifier
            limit: Maximum number of versions to return
            
        Returns:
            List of configuration versions in chronological order (newest first)
        """
        if self.client is None:
            logger.warning("[ElasticsearchConfigProvider] Elasticsearch client not available")
            return []
        
        try:
            response = await self.client.search(
                index=self.index_name,
                body={
                    "query": {"term": {"agent_id.keyword": agent_id}},
                    "sort": [{"version": {"order": "desc"}}],
                    "size": limit
                }
            )
            
            hits = response.get("hits", {}).get("hits", [])
            
            # Extract _id from hit metadata and include it in the returned document
            versions = []
            for hit in hits:
                version_data = hit["_source"].copy()
                version_data["_id"] = hit["_id"]
                versions.append(version_data)
            
            logger.debug(
                f"[ElasticsearchConfigProvider] Retrieved {len(versions)} versions "
                f"for agent_id={agent_id}"
            )
            
            return versions
        
        except Exception as e:
            logger.error(
                f"[ElasticsearchConfigProvider] Failed to get versions for agent_id={agent_id}: {e}"
            )
            return []
    
    async def delete_agent_config(self, agent_id: str) -> bool:
        """
        Delete all configurations for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if deletion succeeded, False otherwise
        """
        if self.client is None:
            logger.warning("[ElasticsearchConfigProvider] Elasticsearch client not available")
            return False
        
        try:
            # Delete by query
            await self.client.delete_by_query(
                index=self.index_name,
                body={
                    "query": {"term": {"agent_id.keyword": agent_id}}
                }
            )
            
            # Invalidate cache
            self._invalidate_cache(agent_id)
            
            logger.info(f"[ElasticsearchConfigProvider] Deleted configs for agent_id={agent_id}")
            
            return True
        
        except Exception as e:
            logger.error(
                f"[ElasticsearchConfigProvider] Failed to delete configs for agent_id={agent_id}: {e}"
            )
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        return {
            "size": len(self._cache),
            "max_size": self.cache_max_size,
            "ttl": self.cache_ttl,
            "entries": list(self._cache.keys())
        }
