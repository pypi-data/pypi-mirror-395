"""
Admin Services Module

This module provides service classes for admin panel operations,
including user management, KPI computation, and session listing.

Requirements: 3.1, 3.3, 3.4, 4.2, 4.3, 4.4, 4.5
"""

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Literal

from ..session.session_storage import (
    MessageData,
    get_shared_elasticsearch_client,
)
from .admin_models import (
    ConfigDetail,
    ConfigSummary,
    PaginatedUserList,
    SessionSummary,
    UserKPIs,
    UserSummary,
)


logger = logging.getLogger(__name__)


def _get_index_prefix() -> str:
    """Get the Elasticsearch index prefix from environment."""
    return os.getenv("ELASTICSEARCH_SESSION_INDEX_PREFIX", "agent-sessions")


class AdminUserService:
    """
    Service for admin user management operations.

    Provides methods to list users, compute KPIs, and retrieve session data
    using Elasticsearch aggregations for efficient querying.

    Requirements: 3.1, 3.3, 3.4, 4.2, 4.3, 4.4, 4.5
    """

    def __init__(self) -> None:
        """Initialize the admin user service."""
        self._client = None
        self._index_prefix = _get_index_prefix()

    async def _get_client(self):  # type: ignore[no-untyped-def]
        """Get or initialize the Elasticsearch client."""
        if self._client is None:
            self._client = await get_shared_elasticsearch_client()
        return self._client

    @property
    def _metadata_index(self) -> str:
        """Get the metadata index name."""
        return f"{self._index_prefix}-metadata"

    @property
    def _messages_index(self) -> str:
        """Get the messages index name."""
        return f"{self._index_prefix}-messages"

    async def list_users(
        self,
        search: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> PaginatedUserList:
        """
        List users with pagination and optional search filtering.

        Uses Elasticsearch aggregations to efficiently retrieve user summaries
        with session counts and last activity timestamps.

        Args:
            search: Optional search string for partial user_id matching (case-insensitive)
            page: Page number (1-indexed)
            page_size: Number of users per page

        Returns:
            PaginatedUserList with user summaries sorted by last activity (descending)

        Requirements: 3.1, 3.3, 3.4
        """
        client = await self._get_client()
        if client is None:
            logger.error("[ADMIN SERVICE] Elasticsearch client not available")
            return PaginatedUserList(
                users=[],
                total=0,
                page=page,
                page_size=page_size,
                total_pages=0,
            )

        try:
            # Build the query for filtering
            query: dict = {"match_all": {}}
            if search:
                # Use wildcard query for partial matching (case-insensitive)
                query = {
                    "wildcard": {
                        "user_id": {
                            "value": f"*{search.lower()}*",
                            "case_insensitive": True,
                        }
                    }
                }

            # First, get all unique users with their stats using aggregation
            agg_response = await client.search(
                index=self._metadata_index,
                body={
                    "size": 0,
                    "query": query,
                    "aggs": {
                        "users": {
                            "terms": {
                                "field": "user_id",
                                "size": 10000,  # Get all users
                                "order": {"last_activity": "desc"},
                            },
                            "aggs": {
                                "session_count": {"value_count": {"field": "session_id"}},
                                "last_activity": {"max": {"field": "updated_at"}},
                            },
                        },
                        "total_users": {"cardinality": {"field": "user_id"}},
                    },
                },
            )

            # Extract total count
            total = agg_response["aggregations"]["total_users"]["value"]

            # Extract user buckets
            user_buckets = agg_response["aggregations"]["users"]["buckets"]

            # Apply pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_buckets = user_buckets[start_idx:end_idx]

            # Build user summaries
            users = []
            for bucket in paginated_buckets:
                last_activity_ms = bucket["last_activity"]["value"]
                last_activity = None
                if last_activity_ms:
                    last_activity = datetime.fromtimestamp(last_activity_ms / 1000, tz=timezone.utc)

                users.append(
                    UserSummary(
                        user_id=bucket["key"],
                        session_count=bucket["doc_count"],
                        last_activity=last_activity,
                    )
                )

            # Calculate total pages
            total_pages = (total + page_size - 1) // page_size if total > 0 else 0

            logger.debug(
                f"[ADMIN SERVICE] Listed {len(users)} users (page {page}/{total_pages}, total: {total})"
            )

            return PaginatedUserList(
                users=users,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
            )

        except Exception as e:
            logger.error(f"[ADMIN SERVICE] Failed to list users: {e}")
            return PaginatedUserList(
                users=[],
                total=0,
                page=page,
                page_size=page_size,
                total_pages=0,
            )

    async def get_user_kpis(
        self,
        user_id: str,
        period: Literal["day", "week", "month"] = "week",
        agent_id: str | None = None,
    ) -> UserKPIs:
        """
        Get KPIs for a specific user.

        Computes message count for the specified time period and
        determines the last connection time from the most recent message.

        Args:
            user_id: User identifier
            period: Time period for message count ("day", "week", or "month")
            agent_id: Optional agent ID to filter KPIs by specific agent

        Returns:
            UserKPIs with message count and last connection timestamp

        Requirements: 4.2, 4.3, 4.4, 4.5
        """
        client = await self._get_client()
        if client is None:
            logger.error("[ADMIN SERVICE] Elasticsearch client not available")
            return UserKPIs(
                user_id=user_id,
                message_count=0,
                period=period,
                last_connection=None,
                agent_id=agent_id,
            )

        try:
            # Calculate date range based on period
            now = datetime.now(timezone.utc)
            if period == "day":
                start_date = now - timedelta(days=1)
            elif period == "week":
                start_date = now - timedelta(weeks=1)
            else:  # month
                start_date = now - timedelta(days=30)

            # Build query with optional agent_id filter
            must_clauses: list[dict] = [{"term": {"user_id": user_id}}]
            if agent_id:
                must_clauses.append({"term": {"agent_id": agent_id}})

            query = {"bool": {"must": must_clauses}}

            # Query for message count in period and last connection
            response = await client.search(
                index=self._messages_index,
                body={
                    "size": 0,
                    "query": query,
                    "aggs": {
                        "messages_in_period": {
                            "filter": {
                                "range": {
                                    "created_at": {
                                        "gte": start_date.isoformat(),
                                        "lte": now.isoformat(),
                                    }
                                }
                            }
                        },
                        "last_connection": {"max": {"field": "created_at"}},
                    },
                },
            )

            # Extract message count for the period
            message_count = response["aggregations"]["messages_in_period"]["doc_count"]

            # Extract last connection timestamp
            last_connection_ms = response["aggregations"]["last_connection"]["value"]
            last_connection = None
            if last_connection_ms:
                last_connection = datetime.fromtimestamp(last_connection_ms / 1000, tz=timezone.utc)

            logger.debug(
                f"[ADMIN SERVICE] User {user_id} KPIs (agent={agent_id}): {message_count} messages ({period}), "
                f"last connection: {last_connection}"
            )

            return UserKPIs(
                user_id=user_id,
                message_count=message_count,
                period=period,
                last_connection=last_connection,
                agent_id=agent_id,
            )

        except Exception as e:
            logger.error(f"[ADMIN SERVICE] Failed to get KPIs for user {user_id}: {e}")
            return UserKPIs(
                user_id=user_id,
                message_count=0,
                period=period,
                last_connection=None,
                agent_id=agent_id,
            )

    async def get_user_sessions(
        self, user_id: str, agent_id: str | None = None
    ) -> list[SessionSummary]:
        """
        Get all sessions for a specific user.

        Retrieves session metadata with message counts for each session.

        Args:
            user_id: User identifier
            agent_id: Optional agent ID to filter sessions

        Returns:
            List of SessionSummary objects sorted by updated_at (descending)

        Requirements: 5.1, 5.2
        """
        client = await self._get_client()
        if client is None:
            logger.error("[ADMIN SERVICE] Elasticsearch client not available")
            return []

        try:
            # Build query with optional agent_id filter
            must_clauses: list[dict] = [{"term": {"user_id": user_id}}]
            if agent_id:
                must_clauses.append({"term": {"agent_id": agent_id}})

            query = {"bool": {"must": must_clauses}}

            # Get all sessions for the user
            sessions_response = await client.search(
                index=self._metadata_index,
                body={
                    "query": query,
                    "sort": [{"updated_at": {"order": "desc"}}],
                    "size": 10000,
                },
            )

            sessions = []
            session_ids = []

            for hit in sessions_response["hits"]["hits"]:
                source = hit["_source"]
                session_ids.append(source["session_id"])
                sessions.append(
                    {
                        "session_id": source["session_id"],
                        "session_label": source.get("session_label"),
                        "created_at": source.get("created_at"),
                        "updated_at": source.get("updated_at"),
                        "agent_id": source.get("agent_id"),
                    }
                )

            # Get message counts for all sessions in one query
            if session_ids:
                msg_count_response = await client.search(
                    index=self._messages_index,
                    body={
                        "size": 0,
                        "query": {"terms": {"session_id": session_ids}},
                        "aggs": {
                            "by_session": {
                                "terms": {"field": "session_id", "size": len(session_ids)},
                            }
                        },
                    },
                )

                # Build message count lookup
                msg_counts = {}
                for bucket in msg_count_response["aggregations"]["by_session"]["buckets"]:
                    msg_counts[bucket["key"]] = bucket["doc_count"]

                # Build final session summaries
                result = []
                for session in sessions:
                    created_at = session["created_at"]
                    updated_at = session["updated_at"]

                    # Parse timestamps
                    if isinstance(created_at, str):
                        created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    if isinstance(updated_at, str):
                        updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))

                    result.append(
                        SessionSummary(
                            session_id=session["session_id"],
                            session_label=session["session_label"],
                            created_at=created_at,
                            updated_at=updated_at,
                            message_count=msg_counts.get(session["session_id"], 0),
                            agent_id=session.get("agent_id"),
                        )
                    )

                logger.debug(
                    f"[ADMIN SERVICE] Retrieved {len(result)} sessions for user {user_id} "
                    f"(agent={agent_id})"
                )
                return result

            return []

        except Exception as e:
            logger.error(f"[ADMIN SERVICE] Failed to get sessions for user {user_id}: {e}")
            return []

    async def get_user_agents(self, user_id: str) -> list[str]:
        """
        Get list of unique agent IDs used by a specific user.

        Args:
            user_id: User identifier

        Returns:
            List of unique agent IDs
        """
        client = await self._get_client()
        if client is None:
            logger.error("[ADMIN SERVICE] Elasticsearch client not available")
            return []

        try:
            # Aggregate unique agent_ids for this user
            response = await client.search(
                index=self._metadata_index,
                body={
                    "size": 0,
                    "query": {"term": {"user_id": user_id}},
                    "aggs": {
                        "agents": {
                            "terms": {
                                "field": "agent_id",
                                "size": 1000,
                            }
                        }
                    },
                },
            )

            agents = [
                bucket["key"]
                for bucket in response["aggregations"]["agents"]["buckets"]
                if bucket["key"]  # Filter out empty/null values
            ]

            logger.debug(f"[ADMIN SERVICE] Found {len(agents)} agents for user {user_id}")
            return agents

        except Exception as e:
            logger.error(f"[ADMIN SERVICE] Failed to get agents for user {user_id}: {e}")
            return []

    async def get_session_messages(self, session_id: str) -> list[MessageData]:
        """
        Get all messages for a specific session.

        Retrieves messages sorted by sequence_number in ascending order.

        Args:
            session_id: Session identifier

        Returns:
            List of MessageData objects in chronological order

        Requirements: 5.4, 7.4
        """
        client = await self._get_client()
        if client is None:
            logger.error("[ADMIN SERVICE] Elasticsearch client not available")
            return []

        try:
            response = await client.search(
                index=self._messages_index,
                body={
                    "query": {"term": {"session_id": session_id}},
                    "sort": [{"sequence_number": {"order": "asc"}}],
                    "size": 10000,
                },
            )

            messages = []
            for hit in response["hits"]["hits"]:
                source = hit["_source"]
                msg = MessageData(**source)
                logger.debug(
                    f"[ADMIN SERVICE] Message: role={msg.role}, type={msg.message_type}, "
                    f"text_content={msg.text_content[:50] if msg.text_content else None}, "
                    f"response_text_main={msg.response_text_main[:50] if msg.response_text_main else None}"
                )
                messages.append(msg)

            logger.debug(
                f"[ADMIN SERVICE] Retrieved {len(messages)} messages for session {session_id}"
            )
            return messages

        except Exception as e:
            logger.error(f"[ADMIN SERVICE] Failed to get messages for session {session_id}: {e}")
            return []


def _get_config_index() -> str:
    """Get the Elasticsearch config index from environment."""
    return os.getenv("ELASTICSEARCH_CONFIG_INDEX", "agent-configs")


class AdminConfigService:
    """
    Service for admin configuration management operations.

    Provides methods to list and retrieve agent configurations
    from Elasticsearch.

    Requirements: 6.1, 6.2, 6.3, 6.4
    """

    def __init__(self) -> None:
        """Initialize the admin config service."""
        self._client = None
        self._config_index = _get_config_index()

    async def _get_client(self):  # type: ignore[no-untyped-def]
        """Get or initialize the Elasticsearch client."""
        if self._client is None:
            self._client = await get_shared_elasticsearch_client()
        return self._client

    async def list_configs(self) -> list[ConfigSummary]:
        """
        List all agent configurations from Elasticsearch.

        Retrieves all configurations with their summary fields,
        showing only the latest active version for each agent.

        Returns:
            List of ConfigSummary objects sorted by last_updated (descending)

        Requirements: 6.1, 6.2
        """
        client = await self._get_client()
        if client is None:
            logger.error("[ADMIN CONFIG SERVICE] Elasticsearch client not available")
            return []

        try:
            # Query all configurations, sorted by updated_at descending
            response = await client.search(
                index=self._config_index,
                body={
                    "query": {"match_all": {}},
                    "sort": [{"updated_at": {"order": "desc"}}],
                    "size": 10000,
                },
            )

            configs = []
            for hit in response["hits"]["hits"]:
                source = hit["_source"]
                doc_id = hit["_id"]

                # Parse updated_at timestamp
                updated_at = source.get("updated_at")
                if isinstance(updated_at, str):
                    try:
                        updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                    except ValueError:
                        updated_at = None

                # Use doc_id as config_id for unique identification
                configs.append(
                    ConfigSummary(
                        config_id=doc_id,
                        agent_type=source.get("agent_type"),
                        version=str(source.get("version", "")) if source.get("version") else None,
                        last_updated=updated_at,
                    )
                )

            logger.debug(f"[ADMIN CONFIG SERVICE] Listed {len(configs)} configurations")
            return configs

        except Exception as e:
            logger.error(f"[ADMIN CONFIG SERVICE] Failed to list configs: {e}")
            return []

    async def get_config_detail(self, config_id: str) -> ConfigDetail | None:
        """
        Get full details of a specific configuration.

        Retrieves the complete configuration document including
        all configuration data as JSON.

        Args:
            config_id: Configuration document ID

        Returns:
            ConfigDetail with full configuration data, or None if not found

        Requirements: 6.3, 6.4
        """
        client = await self._get_client()
        if client is None:
            logger.error("[ADMIN CONFIG SERVICE] Elasticsearch client not available")
            return None

        try:
            # Get document by ID
            response = await client.get(
                index=self._config_index,
                id=config_id,
            )

            source = response["_source"]

            # Parse updated_at timestamp
            updated_at = source.get("updated_at")
            if isinstance(updated_at, str):
                try:
                    updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                except ValueError:
                    updated_at = None

            # Build config_data from the full document
            # Include the nested config object and other relevant fields
            config_data = {
                "agent_id": source.get("agent_id"),
                "config": source.get("config", {}),
                "metadata": source.get("metadata", {}),
                "active": source.get("active", False),
                "updated_by": source.get("updated_by"),
            }

            logger.debug(f"[ADMIN CONFIG SERVICE] Retrieved config detail for {config_id}")

            return ConfigDetail(
                config_id=config_id,
                agent_type=source.get("agent_type"),
                version=str(source.get("version", "")) if source.get("version") else None,
                last_updated=updated_at,
                config_data=config_data,
            )

        except Exception as e:
            # Check if it's a not found error
            error_str = str(e).lower()
            if "not found" in error_str or "404" in error_str:
                logger.debug(f"[ADMIN CONFIG SERVICE] Config not found: {config_id}")
                return None
            logger.error(f"[ADMIN CONFIG SERVICE] Failed to get config detail for {config_id}: {e}")
            return None
