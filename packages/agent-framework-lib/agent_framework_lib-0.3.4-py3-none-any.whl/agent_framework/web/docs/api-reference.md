# API Reference

## Table of Contents

- [Authentication](#authentication)
- [Session Management](#session-management)
- [Messaging](#messaging)
- [File Storage](#file-storage)
- [Configuration Management](#configuration-management)
- [Feedback](#feedback)
- [Agent Management](#agent-management)
- [Admin](#admin)

## Authentication

The Agent Framework supports multiple authentication methods:

### Authentication Methods

1. **Basic Authentication**: Username and password
2. **Bearer Token (API Key)**: API key in Authorization header
3. **X-API-Key Header**: API key in custom header

### Configuration

Authentication is controlled by environment variables:

- `REQUIRE_AUTH`: Set to `"true"` to enable authentication (default: `"false"`)
- `BASIC_AUTH_USERNAME`: Username for basic auth (default: `"admin"`)
- `BASIC_AUTH_PASSWORD`: Password for basic auth (default: `"password"`)
- `API_KEYS`: Comma-separated list of valid API keys

### Example Requests

**Basic Authentication:**
```bash
curl -u admin:password http://localhost:8000/metadata
```

**Bearer Token:**
```bash
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/metadata
```

**X-API-Key Header:**
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/metadata
```

## Session Management

### POST /init

Initialize a new session with configuration and optional data.

**Request Body:**
```json
{
  "user_id": "user123",
  "correlation_id": "optional-correlation-id",
  "session_id": "optional-session-id",
  "data": {
    "key": "value"
  },
  "configuration": {
    "system_prompt": "You are a helpful assistant for {{data.key}}",
    "model_name": "gpt-4o-mini",
    "temperature": 0.7,
    "enable_rich_content": true
  }
}
```

**Response:**
```json
{
  "user_id": "user123",
  "correlation_id": "optional-correlation-id",
  "session_id": "generated-or-provided-session-id",
  "data": {"key": "value"},
  "configuration": {
    "system_prompt": "You are a helpful assistant for value",
    "model_name": "gpt-4o-mini",
    "temperature": 0.7
  },
  "agent_id": "agent-unique-id",
  "agent_type": "AgentClassName"
}
```

**Features:**
- Template system prompts with data using `{{data.key}}` or `{{key}}` syntax
- Supports nested data access: `{{data.key.subkey}}`
- Auto-generates session_id if not provided
- Tracks agent identity for multi-agent scenarios

### POST /end

End a session by marking it as closed.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Request Body:**
```json
{
  "session_id": "session-id-to-close"
}
```

**Response:**
```json
{
  "message": "Session session-id-to-close has been successfully closed",
  "session_id": "session-id-to-close"
}
```

### GET /sessions

List all active session IDs for a user, filtered by current agent.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Response:**
```json
["session-id-1", "session-id-2", "session-id-3"]
```

### GET /sessions/info

List all sessions with detailed information including labels and metadata.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")
- `agent_id`: Filter by specific agent ID (optional)
- `agent_type`: Filter by specific agent type (optional)

**Response:**
```json
[
  {
    "session_id": "session-id-1",
    "session_label": "Customer Support Chat",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:30:00Z",
    "correlation_id": "correlation-123",
    "metadata": {},
    "agent_id": "agent-unique-id",
    "agent_type": "AgentClassName",
    "session_configuration": {},
    "agent_lifecycle": []
  }
]
```

### GET /sessions/{session_id}/history

Retrieve message history for a specific session.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Response:**
```json
[
  {
    "role": "user",
    "text_content": "Hello",
    "parts": [],
    "response_text_main": null,
    "timestamp": "2024-01-01T10:00:00Z",
    "interaction_id": "interaction-uuid",
    "processing_time_ms": null,
    "processed_at": null,
    "model_used": null
  },
  {
    "role": "assistant",
    "text_content": null,
    "parts": [{"type": "text", "text": "Hi! How can I help you?"}],
    "response_text_main": "Hi! How can I help you?",
    "timestamp": "2024-01-01T10:00:01Z",
    "interaction_id": "interaction-uuid",
    "processing_time_ms": 1234.5,
    "processed_at": "2024-01-01T10:00:01Z",
    "model_used": "gpt-4o-mini"
  }
]
```

### PUT /session/{session_id}/label

Update the label of a session.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Request Body:**
```json
{
  "session_id": "session-id",
  "label": "My Custom Label"
}
```

**Response:**
Returns updated SessionInfo object.

### GET /session/{session_id}/status

Get the status of a session (active, closed, or not found).

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Response:**
```json
{
  "session_id": "session-id",
  "user_id": "user123",
  "status": "active",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:30:00Z",
  "closed_at": null
}
```

### GET /sessions/by-correlation/{correlation_id}

Retrieve all sessions across users that share a correlation ID.

**Response:**
```json
{
  "message": "Cross-user correlation search not yet implemented",
  "correlation_id": "correlation-123",
  "sessions": []
}
```

### GET /users

List all user IDs who have at least one session.

**Response:**
```json
["user1", "user2", "user3"]
```

## Messaging

### POST /message

Send a message to an agent and receive a response.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")
- `session_id`: Session identifier (optional, can be in body)

**Request Body:**
```json
{
  "query": "What is the weather today?",
  "parts": [
    {
      "type": "text",
      "text": "Additional context"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://example.com/image.jpg"
      }
    },
    {
      "type": "file_data",
      "filename": "document.pdf",
      "mime_type": "application/pdf",
      "content": "base64-encoded-content"
    }
  ],
  "session_id": "optional-session-id",
  "correlation_id": "optional-correlation-id"
}
```

**Response:**
```json
{
  "response_text": "The weather today is sunny with a high of 75°F.",
  "parts": [
    {
      "type": "text",
      "text": "The weather today is sunny with a high of 75°F."
    }
  ],
  "session_id": "session-id",
  "user_id": "user123",
  "correlation_id": "optional-correlation-id",
  "interaction_id": "interaction-uuid",
  "processing_time_ms": 1234.5,
  "model_used": "gpt-4o-mini",
  "agent_id": "agent-unique-id",
  "agent_type": "AgentClassName",
  "agent_metadata": {}
}
```

**Features:**
- Supports multimodal inputs (text, images, files)
- Automatic file processing and markdown conversion
- Creates session if it doesn't exist
- Prevents messaging to closed sessions

### POST /stream

Stream agent responses in real-time using Server-Sent Events (SSE).

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")
- `session_id`: Session identifier (optional, can be in body)

**Request Body:**
Same as `/message` endpoint.

**Response:**
Server-Sent Events stream with JSON data:

```
data: {"response_text": "The", "parts": [...], "session_id": "...", ...}

data: {"response_text": "The weather", "parts": [...], "session_id": "...", ...}

data: {"response_text": "The weather today", "parts": [...], "session_id": "...", ...}

data: {"status": "done", "session_id": "...", "interaction_id": "..."}
```

**Features:**
- Real-time streaming responses
- Same multimodal support as `/message`
- Automatic state persistence
- Final "done" message when complete

### GET /sessions/{session_id}/response-times

Get response times for all agent responses in a session.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Response:**
```json
{
  "session_id": "session-id",
  "user_id": "user123",
  "response_times": [
    {
      "interaction_id": "interaction-uuid",
      "response_time_ms": 1234.5,
      "user_message_timestamp": "2024-01-01T10:00:00Z",
      "agent_response_timestamp": "2024-01-01T10:00:01Z"
    }
  ],
  "total_responses": 1,
  "average_response_time_ms": 1234.5
}
```

**Note:** Only available with MongoDB storage backend.

### GET /interactions/{interaction_id}/response-time

Get response time for a specific interaction.

**Response:**
```json
{
  "interaction_id": "interaction-uuid",
  "response_time_ms": 1234.5,
  "user_message_timestamp": "2024-01-01T10:00:00Z",
  "agent_response_timestamp": "2024-01-01T10:00:01Z"
}
```

**Note:** Only available with MongoDB storage backend.

## File Storage

### POST /files/upload

Upload a file to storage.

**Query Parameters:**
- `user_id`: User identifier (required)
- `session_id`: Session identifier (optional)

**Request:**
Multipart form data with file upload.

**Response:**
```json
{
  "file_id": "generated-file-id",
  "filename": "document.pdf",
  "size_bytes": 12345,
  "mime_type": "application/pdf"
}
```

### GET /files/{file_id}/download

Download a file from storage.

**Response:**
Binary file content with appropriate Content-Type and Content-Disposition headers.

### GET /files/{file_id}/metadata

Get metadata for a file.

**Response:**
```json
{
  "file_id": "file-id",
  "filename": "document.pdf",
  "mime_type": "application/pdf",
  "size_bytes": 12345,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z",
  "user_id": "user123",
  "session_id": "session-id",
  "agent_id": "agent-id",
  "is_generated": false,
  "tags": ["document", "pdf"],
  "storage_backend": "local"
}
```

### GET /files/{file_id}/preview

Preview file content optimized for UI display.

**Response:**
```json
{
  "file_id": "file-id",
  "filename": "document.txt",
  "mime_type": "text/plain",
  "size_bytes": 1234,
  "preview_type": "text",
  "preview_available": true,
  "message": "Preview ready",
  "content": "File content here...",
  "metadata": {
    "created_at": "2024-01-01T10:00:00Z",
    "is_generated": false,
    "tags": [],
    "session_id": "session-id"
  }
}
```

**Preview Types:**
- `text`: Plain text files (includes `content` field)
- `json`: JSON files (includes formatted `content` field)
- `markdown`: Markdown files (includes `content` and `html_preview` fields)
- `image`: Image files (includes `content_base64` field)
- `binary`: Binary files (preview not available)

### GET /files

List files with filtering.

**Query Parameters:**
- `user_id`: User identifier (required)
- `session_id`: Filter by session (optional)
- `is_generated`: Filter by generated status (optional)

**Response:**
```json
[
  {
    "file_id": "file-id",
    "filename": "document.pdf",
    "mime_type": "application/pdf",
    "size_bytes": 12345,
    "created_at": "2024-01-01T10:00:00Z",
    "is_generated": false,
    "session_id": "session-id",
    "tags": []
  }
]
```

### DELETE /files/{file_id}

Delete a file from storage.

**Response:**
```json
{
  "success": true,
  "message": "File file-id deleted successfully"
}
```

### GET /files/stats

Get file storage system statistics.

**Response:**
```json
{
  "backends": {
    "local": {
      "type": "local",
      "enabled": true,
      "path": "/path/to/storage"
    },
    "s3": {
      "type": "s3",
      "enabled": false
    }
  },
  "default_backend": "local"
}
```

## Configuration Management

### GET /config/models

Get model configuration information.

**Response:**
```json
{
  "default_model": "gpt-4o-mini",
  "configuration_status": {
    "openai_configured": true,
    "anthropic_configured": false,
    "gemini_configured": true
  },
  "supported_models": [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gemini-1.5-pro",
    "gemini-1.5-flash"
  ],
  "supported_providers": ["openai", "anthropic", "gemini"],
  "fallback_provider": "openai"
}
```

### GET /config/agents/{agent_id}

Get current effective configuration for an agent.

**Response:**
```json
{
  "agent_id": "agent-id",
  "config": {
    "system_prompt": "You are a helpful assistant",
    "model_name": "gpt-4o-mini",
    "model_config": {
      "temperature": 0.7,
      "max_tokens": 2000
    }
  },
  "version": 1,
  "updated_at": "2024-01-01T10:00:00Z",
  "source": "elasticsearch",
  "agent_type": "AgentClassName",
  "metadata": {},
  "active": true
}
```

**Configuration Sources:**
- `elasticsearch`: From Elasticsearch configuration storage
- `hardcoded`: From agent class implementation
- `default`: Default fallback configuration

### PUT /config/agents/{agent_id}

Update agent configuration in Elasticsearch.

**Request Body:**
```json
{
  "config": {
    "system_prompt": "Updated prompt",
    "model_name": "gpt-4o",
    "model_config": {
      "temperature": 0.8
    }
  },
  "agent_type": "AgentClassName",
  "updated_by": "admin",
  "metadata": {
    "reason": "Performance improvement"
  },
  "active": true
}
```

**Response:**
Returns updated configuration with new version number.

**Features:**
- Creates new version, deactivates old versions
- Invalidates cache automatically
- Returns HTTP 503 if Elasticsearch unavailable

### GET /config/agents/{agent_id}/versions

Get configuration version history for an agent.

**Query Parameters:**
- `limit`: Maximum versions to return (default: 10, max: 100)

**Response:**
```json
[
  {
    "agent_id": "agent-id",
    "agent_type": "AgentClassName",
    "version": 2,
    "updated_at": "2024-01-01T11:00:00Z",
    "updated_by": "admin",
    "config": {...},
    "metadata": {},
    "active": true
  },
  {
    "agent_id": "agent-id",
    "agent_type": "AgentClassName",
    "version": 1,
    "updated_at": "2024-01-01T10:00:00Z",
    "updated_by": "system",
    "config": {...},
    "metadata": {},
    "active": false
  }
]
```

### DELETE /config/agents/{agent_id}

Delete all configurations for an agent.

**Response:**
```json
{
  "success": true,
  "message": "All configurations for agent agent-id have been deleted",
  "agent_id": "agent-id",
  "fallback_behavior": "Agent will now use hardcoded or default configuration"
}
```

**Note:** After deletion, agent falls back to hardcoded or default configuration.

## Feedback

### POST /feedback/message

Submit feedback for a specific message.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Request Body:**
```json
{
  "session_id": "session-id",
  "message_id": "interaction-uuid",
  "feedback": "up"
}
```

**Feedback Values:**
- `up`: Positive feedback
- `down`: Negative feedback

**Response:**
```json
{
  "status": "success",
  "message": "Feedback 'up' recorded for message interaction-uuid",
  "session_id": "session-id",
  "message_id": "interaction-uuid",
  "feedback": "up",
  "previous_feedback": null,
  "feedback_changed": true
}
```

**Features:**
- Validates session exists and is open
- Validates message exists in session
- Tracks feedback changes
- Prevents feedback on closed sessions

### POST /feedback/flag
### PUT /feedback/flag

Submit or update session-level flag.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Request Body:**
```json
{
  "session_id": "session-id",
  "flag_message": "This session needs review"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Session flag created",
  "session_id": "session-id",
  "flag_message": "This session needs review",
  "previous_flag": null,
  "flag_changed": true
}
```

**Features:**
- Editable while session is open
- Tracks flag changes
- Prevents editing on closed sessions

### GET /feedback/session/{session_id}

Retrieve all feedback data for a session.

**Query Parameters:**
- `user_id`: User identifier (default: "default_user")

**Response:**
```json
{
  "session_id": "session-id",
  "user_id": "user123",
  "session_status": "active",
  "flag_message": "Needs review",
  "flag_timestamp": "2024-01-01T10:00:00Z",
  "message_feedback": {
    "interaction-uuid-1": "up",
    "interaction-uuid-1_timestamp": "2024-01-01T10:01:00Z",
    "interaction-uuid-2": "down",
    "interaction-uuid-2_timestamp": "2024-01-01T10:02:00Z"
  }
}
```

### GET /feedback/message/{message_id}

Retrieve feedback for a specific message.

**Query Parameters:**
- `session_id`: Session identifier (required)
- `user_id`: User identifier (default: "default_user")

**Response:**
```json
{
  "message_id": "interaction-uuid",
  "session_id": "session-id",
  "user_id": "user123",
  "feedback": "up",
  "feedback_timestamp": "2024-01-01T10:01:00Z"
}
```

## Agent Management

### GET /metadata

Get agent metadata card.

**Response:**
```json
{
  "name": "Personal Assistant",
  "description": "A helpful AI assistant",
  "version": "1.0.0",
  "capabilities": ["chat", "file_processing"],
  "supported_models": ["gpt-4o", "gpt-4o-mini"]
}
```

### GET /system-prompt

Get agent's default system prompt.

**Response:**
```json
{
  "system_prompt": "You are a helpful AI assistant..."
}
```

**Note:** Returns 404 if no default system prompt is configured.

### GET /agents

List all agent types and their usage statistics.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "agent_type": "AgentClassName",
      "session_count": 42,
      "user_count": 10,
      "last_used": "2024-01-01T10:00:00Z"
    }
  ]
}
```

### GET /agents/{agent_type}/sessions

Get sessions for a specific agent type.

**Query Parameters:**
- `user_id`: Filter by specific user (optional)

**Response:**
```json
{
  "success": true,
  "agent_type": "AgentClassName",
  "user_id": null,
  "session_count": 42,
  "sessions": ["session-id-1", "session-id-2"]
}
```

### GET /agents/{agent_id}/lifecycle

Get lifecycle events for a specific agent instance.

**Response:**
```json
{
  "success": true,
  "agent_id": "agent-unique-id",
  "event_count": 3,
  "events": [
    {
      "lifecycle_id": "lifecycle-uuid",
      "agent_id": "agent-unique-id",
      "agent_type": "AgentClassName",
      "event_type": "created",
      "session_id": "session-id",
      "user_id": "user123",
      "timestamp": "2024-01-01T10:00:00Z",
      "metadata": {}
    }
  ]
}
```

### GET /endpoints

List all available API endpoints.

**Response:**
```json
[
  {
    "path": "/message",
    "methods": ["POST"],
    "summary": "Handle incoming messages",
    "description": "Handles incoming messages using the session storage backend.",
    "parameters": [
      {
        "name": "user_id",
        "in": "query",
        "required": false,
        "type": "str"
      }
    ],
    "request_body": {
      "model": "MessageRequest",
      "required": true
    }
  }
]
```

## Admin

### POST /admin/authenticate

Validate admin password for accessing admin features.

**Request Body:**
```json
{
  "password": "admin-password"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Admin authentication successful"
}
```

**Note:** This is a secondary authentication layer on top of base auth.

## UI Endpoints

### GET /

Root endpoint with welcome message.

**Response:**
```json
{
  "message": "Agent server is running. Visit /docs for API documentation or /ui for a interface human friendly with agent."
}
```

### GET /ui

Serve the modern HTML UI application.

**Response:**
HTML page with modern UI interface.

### GET /testapp

Serve the HTML test application.

**Response:**
HTML page with test application interface.

### GET /docs

OpenAPI documentation (Swagger UI).

### GET /redoc

ReDoc API documentation.

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication required. Use Basic Auth (username/password) or API Key (Bearer token or X-API-Key header)."
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied to this resource"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 409 Conflict
```json
{
  "detail": "Resource already exists"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error: error details"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Service is unavailable (e.g., Elasticsearch down)"
}
```

## Rich Content Module

### agent_framework.core.rich_content_prompt

This module provides centralized rich content instructions that are automatically injected into agent system prompts.

**Constants:**

- `RICH_CONTENT_INSTRUCTIONS` - Complete instructions for generating rich content (Mermaid diagrams, Chart.js charts, forms, options blocks, tables)

**Functions:**

#### combine_prompts(base_prompt, rich_content_prompt)

Combine a base prompt with rich content instructions.

**Parameters:**
- `base_prompt` (str): The agent's custom system prompt
- `rich_content_prompt` (str, optional): Rich content instructions (defaults to RICH_CONTENT_INSTRUCTIONS)

**Returns:**
- `str`: Combined prompt with rich content capabilities

**Example:**
```python
from agent_framework.core.rich_content_prompt import combine_prompts, RICH_CONTENT_INSTRUCTIONS

# Combine custom prompt with rich content
base = "You are a helpful assistant."
combined = combine_prompts(base)

# Or use custom rich content instructions
combined = combine_prompts(base, custom_instructions)
```

### Session Configuration

The `enable_rich_content` configuration option controls automatic rich content injection:

```python
session_config = {
    "user_id": "user123",
    "session_id": "session456",
    "enable_rich_content": True,  # Default: True
    "system_prompt": "Custom prompt..."
}
```

When `enable_rich_content` is `True` (default), the framework automatically appends rich content instructions to the agent's system prompt. Set to `False` to disable this behavior.

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production deployments.

## Versioning

The API does not currently use versioning. Breaking changes will be documented in the CHANGELOG.

## CORS

CORS is enabled for all origins (`*`) by default. Configure CORS middleware for production deployments.
