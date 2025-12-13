"""
Admin Panel Data Models

This module defines Pydantic models for the admin panel API endpoints.
These models handle request/response validation for user management,
session viewing, KPIs, and configuration management.

Requirements: 3.2, 4.2, 4.3, 5.2, 6.2
"""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class AdminAuthRequest(BaseModel):
    """Request model for admin password verification."""

    password: str = Field(..., description="Admin password to verify")


class AdminAuthResponse(BaseModel):
    """Response model for admin authentication."""

    success: bool = Field(..., description="Whether authentication was successful")
    token: str | None = Field(None, description="Admin session token if successful")
    expires_at: datetime | None = Field(None, description="Token expiration timestamp")


class UserSummary(BaseModel):
    """Summary information for a user in the admin user list."""

    user_id: str = Field(..., description="Unique user identifier")
    session_count: int = Field(..., ge=0, description="Total number of sessions for this user")
    last_activity: datetime | None = Field(
        None, description="Timestamp of the user's most recent activity"
    )


class PaginatedUserList(BaseModel):
    """Paginated list of users with metadata."""

    users: list[UserSummary] = Field(default_factory=list, description="List of user summaries")
    total: int = Field(..., ge=0, description="Total number of users matching the query")
    page: int = Field(..., ge=1, description="Current page number (1-indexed)")
    page_size: int = Field(..., ge=1, description="Number of items per page")
    total_pages: int = Field(..., ge=0, description="Total number of pages available")


class UserKPIs(BaseModel):
    """Key Performance Indicators for a specific user."""

    user_id: str = Field(..., description="User identifier")
    message_count: int = Field(..., ge=0, description="Number of messages in the selected period")
    period: Literal["day", "week", "month"] = Field(
        ..., description="Time period for the KPI calculation"
    )
    last_connection: datetime | None = Field(
        None, description="Timestamp of the user's last message"
    )
    agent_id: str | None = Field(
        None, description="Agent ID filter applied (None means all agents)"
    )


class SessionSummary(BaseModel):
    """Summary information for a session in the admin session list."""

    session_id: str = Field(..., description="Unique session identifier")
    session_label: str | None = Field(None, description="User-defined label for the session")
    created_at: datetime = Field(..., description="Session creation timestamp")
    updated_at: datetime = Field(..., description="Session last update timestamp")
    message_count: int = Field(..., ge=0, description="Number of messages in this session")
    agent_id: str | None = Field(None, description="Agent ID associated with this session")


class ConfigSummary(BaseModel):
    """Summary information for an agent configuration."""

    config_id: str = Field(..., description="Unique configuration identifier")
    agent_type: str | None = Field(None, description="Type of agent this config applies to")
    version: str | None = Field(None, description="Configuration version")
    last_updated: datetime | None = Field(
        None, description="Timestamp of the last configuration update"
    )


class ConfigDetail(BaseModel):
    """Full details of an agent configuration."""

    config_id: str = Field(..., description="Unique configuration identifier")
    agent_type: str | None = Field(None, description="Type of agent this config applies to")
    version: str | None = Field(None, description="Configuration version")
    last_updated: datetime | None = Field(
        None, description="Timestamp of the last configuration update"
    )
    config_data: dict[str, Any] = Field(
        default_factory=dict, description="Full configuration data as JSON"
    )


class AdminStatusResponse(BaseModel):
    """Status response for the admin panel availability check."""

    elasticsearch_available: bool = Field(
        ..., description="Whether Elasticsearch backend is available"
    )
    admin_enabled: bool = Field(..., description="Whether admin panel is enabled")
