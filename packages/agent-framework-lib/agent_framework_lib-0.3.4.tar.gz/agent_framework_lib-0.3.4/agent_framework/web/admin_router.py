"""
Admin Panel API Router

This module provides FastAPI router for admin panel endpoints,
including user management, session viewing, KPIs, and configuration management.

The admin panel requires Elasticsearch to be enabled and available.
All endpoints (except /status and /auth/verify) require admin authentication.

Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4.1, 4.2, 5.1, 5.3, 5.4, 6.1, 6.3
"""

import logging
import os
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..session.session_storage import MessageData, get_shared_elasticsearch_client
from .admin_auth import authenticate_admin, get_admin_user
from .admin_models import (
    AdminAuthRequest,
    AdminAuthResponse,
    AdminStatusResponse,
    ConfigDetail,
    ConfigSummary,
    PaginatedUserList,
    SessionSummary,
    UserKPIs,
)
from .admin_services import AdminConfigService, AdminUserService


logger = logging.getLogger(__name__)

# Create admin router with prefix
admin_router = APIRouter(prefix="/api/admin", tags=["admin"])


async def require_elasticsearch() -> None:
    """
    FastAPI dependency to check Elasticsearch availability.

    Raises HTTPException 503 if Elasticsearch is not enabled or available.
    This dependency should be used on all admin endpoints that require ES.

    Requirements: 1.1, 1.2, 1.3
    """
    es_enabled = os.getenv("ELASTICSEARCH_ENABLED", "false").lower() == "true"

    if not es_enabled:
        logger.warning("[ADMIN ROUTER] Admin panel access denied: Elasticsearch is disabled")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin panel requires Elasticsearch to be enabled",
        )

    # Check if ES client is actually available
    client = await get_shared_elasticsearch_client()
    if client is None:
        logger.warning("[ADMIN ROUTER] Admin panel access denied: Elasticsearch client unavailable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin panel requires Elasticsearch to be available",
        )


# ============================================================================
# Status and Authentication Endpoints (No auth required)
# ============================================================================


@admin_router.get("/status", response_model=AdminStatusResponse)
async def get_admin_status() -> AdminStatusResponse:
    """
    Get admin panel availability status.

    This endpoint does not require authentication and is used by the frontend
    to determine whether to show the admin access button.

    Returns:
        AdminStatusResponse with elasticsearch_available and admin_enabled flags.

    Requirements: 1.1, 1.2
    """
    es_enabled = os.getenv("ELASTICSEARCH_ENABLED", "false").lower() == "true"

    if not es_enabled:
        return AdminStatusResponse(
            elasticsearch_available=False,
            admin_enabled=False,
        )

    # Check if ES client is actually available
    client = await get_shared_elasticsearch_client()
    es_available = client is not None

    return AdminStatusResponse(
        elasticsearch_available=es_available,
        admin_enabled=es_available,
    )


@admin_router.post("/auth/verify", response_model=AdminAuthResponse)
async def verify_admin_password(
    auth_request: AdminAuthRequest,
    _: None = Depends(require_elasticsearch),
) -> AdminAuthResponse:
    """
    Verify admin password and return authentication token.

    This endpoint requires Elasticsearch but not admin authentication
    (since it's used to obtain the authentication token).

    Args:
        auth_request: Request containing the admin password.

    Returns:
        AdminAuthResponse with success status and token if authenticated.

    Requirements: 2.1, 2.2, 2.3
    """
    logger.info("[ADMIN ROUTER] Admin password verification attempt")

    response = authenticate_admin(auth_request.password)

    if response.success:
        logger.info("[ADMIN ROUTER] Admin authentication successful")
    else:
        logger.warning("[ADMIN ROUTER] Admin authentication failed")

    return response


# ============================================================================
# User Endpoints (Auth required)
# ============================================================================


@admin_router.get("/users", response_model=PaginatedUserList)
async def list_users(
    search: str | None = Query(None, description="Search string for partial user_id matching"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Number of users per page"),
    _es: None = Depends(require_elasticsearch),
    _admin: str = Depends(get_admin_user),
) -> PaginatedUserList:
    """
    List all users with sessions.

    Returns a paginated list of users sorted by last activity date (descending).
    Supports optional search filtering by user_id.

    Args:
        search: Optional search string for partial user_id matching (case-insensitive).
        page: Page number (1-indexed).
        page_size: Number of users per page (max 100).

    Returns:
        PaginatedUserList with user summaries.

    Requirements: 3.1, 3.2, 3.3, 3.4
    """
    logger.debug(
        f"[ADMIN ROUTER] Listing users: search={search}, page={page}, page_size={page_size}"
    )

    service = AdminUserService()
    return await service.list_users(search=search, page=page, page_size=page_size)


@admin_router.get("/users/{user_id}", response_model=UserKPIs)
async def get_user_kpis(
    user_id: str,
    period: Literal["day", "week", "month"] = Query("week", description="Time period for KPIs"),
    agent_id: str | None = Query(None, description="Filter KPIs by specific agent ID"),
    _es: None = Depends(require_elasticsearch),
    _admin: str = Depends(get_admin_user),
) -> UserKPIs:
    """
    Get KPIs for a specific user.

    Returns message count for the specified time period and last connection time.

    Args:
        user_id: User identifier.
        period: Time period for message count ("day", "week", or "month").
        agent_id: Optional agent ID to filter KPIs.

    Returns:
        UserKPIs with message count and last connection timestamp.

    Requirements: 4.1, 4.2, 4.3, 4.4, 4.5
    """
    logger.debug(f"[ADMIN ROUTER] Getting KPIs for user {user_id}, period={period}, agent={agent_id}")

    service = AdminUserService()
    return await service.get_user_kpis(user_id=user_id, period=period, agent_id=agent_id)


@admin_router.get("/users/{user_id}/sessions", response_model=list[SessionSummary])
async def get_user_sessions(
    user_id: str,
    agent_id: str | None = Query(None, description="Filter sessions by specific agent ID"),
    _es: None = Depends(require_elasticsearch),
    _admin: str = Depends(get_admin_user),
) -> list[SessionSummary]:
    """
    Get all sessions for a specific user.

    Returns a list of sessions sorted by updated_at (descending).

    Args:
        user_id: User identifier.
        agent_id: Optional agent ID to filter sessions.

    Returns:
        List of SessionSummary objects.

    Requirements: 5.1, 5.2
    """
    logger.debug(f"[ADMIN ROUTER] Getting sessions for user {user_id}, agent={agent_id}")

    service = AdminUserService()
    return await service.get_user_sessions(user_id=user_id, agent_id=agent_id)


@admin_router.get("/users/{user_id}/agents", response_model=list[str])
async def get_user_agents(
    user_id: str,
    _es: None = Depends(require_elasticsearch),
    _admin: str = Depends(get_admin_user),
) -> list[str]:
    """
    Get list of unique agent IDs used by a specific user.

    Args:
        user_id: User identifier.

    Returns:
        List of unique agent IDs.
    """
    logger.debug(f"[ADMIN ROUTER] Getting agents for user {user_id}")

    service = AdminUserService()
    return await service.get_user_agents(user_id=user_id)


# ============================================================================
# Session Endpoints (Auth required)
# ============================================================================


@admin_router.get("/sessions/{session_id}/messages", response_model=list[MessageData])
async def get_session_messages(
    session_id: str,
    _es: None = Depends(require_elasticsearch),
    _admin: str = Depends(get_admin_user),
) -> list[MessageData]:
    """
    Get all messages for a specific session (read-only).

    Returns messages sorted by sequence_number in ascending order.
    This is a read-only view for admin purposes.

    Args:
        session_id: Session identifier.

    Returns:
        List of MessageData objects in chronological order.

    Requirements: 5.3, 5.4, 7.4
    """
    logger.debug(f"[ADMIN ROUTER] Getting messages for session {session_id}")

    service = AdminUserService()
    return await service.get_session_messages(session_id=session_id)


# ============================================================================
# Config Endpoints (Auth required)
# ============================================================================


@admin_router.get("/configs", response_model=list[ConfigSummary])
async def list_configs(
    _es: None = Depends(require_elasticsearch),
    _admin: str = Depends(get_admin_user),
) -> list[ConfigSummary]:
    """
    List all agent configurations.

    Returns a list of configurations sorted by last_updated (descending).

    Returns:
        List of ConfigSummary objects.

    Requirements: 6.1, 6.2
    """
    logger.debug("[ADMIN ROUTER] Listing configurations")

    service = AdminConfigService()
    return await service.list_configs()


@admin_router.get("/configs/{config_id}", response_model=ConfigDetail)
async def get_config_detail(
    config_id: str,
    _es: None = Depends(require_elasticsearch),
    _admin: str = Depends(get_admin_user),
) -> ConfigDetail:
    """
    Get full details of a specific configuration.

    Args:
        config_id: Configuration document ID.

    Returns:
        ConfigDetail with full configuration data.

    Raises:
        HTTPException 404 if configuration not found.

    Requirements: 6.3, 6.4
    """
    logger.debug(f"[ADMIN ROUTER] Getting config detail for {config_id}")

    service = AdminConfigService()
    config = await service.get_config_detail(config_id=config_id)

    if config is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Configuration not found: {config_id}",
        )

    return config
