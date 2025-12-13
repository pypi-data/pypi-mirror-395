# Configuration Guide

## Table of Contents

- [Overview](#overview)
- [API Keys](#api-keys)
- [Model Configuration](#model-configuration)
- [Session Storage](#session-storage)
- [File Storage](#file-storage)
- [Authentication](#authentication)
- [Elasticsearch Integration](#elasticsearch-integration)
- [Advanced Options](#advanced-options)
- [Deployment Scenarios](#deployment-scenarios)

## Overview

The Agent Framework is configured through environment variables, typically set in a `.env` file. Copy `.env.example` to `.env` and configure the values for your deployment.

### Configuration Priority

1. Environment variables (highest priority)
2. `.env` file
3. Default values (lowest priority)

### Quick Start

Minimal configuration for development:

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
DEFAULT_MODEL=gpt-5-mini
SESSION_STORAGE_TYPE=memory
REQUIRE_AUTH=false
```

## API Keys

### OPENAI_API_KEY

- **Type**: string
- **Required**: Conditional (required if using OpenAI models)
- **Default**: None
- **Description**: API key for OpenAI services. Get your key from https://platform.openai.com/api-keys

**Example:**
```bash
OPENAI_API_KEY=sk-proj-abc123...
```

### ANTHROPIC_API_KEY

- **Type**: string
- **Required**: Conditional (required if using Anthropic models)
- **Default**: None
- **Description**: API key for Anthropic Claude models. Get your key from https://console.anthropic.com/

**Example:**
```bash
ANTHROPIC_API_KEY=sk-ant-api03-abc123...
```

### GEMINI_API_KEY

- **Type**: string
- **Required**: Conditional (required if using Google Gemini models)
- **Default**: None
- **Description**: API key for Google Gemini models. Get your key from https://makersuite.google.com/app/apikey

**Example:**
```bash
GEMINI_API_KEY=AIzaSyAbc123...
```

## Model Configuration

### DEFAULT_MODEL

- **Type**: string
- **Required**: No
- **Default**: `gpt-5-mini`
- **Description**: Default model to use when no model is specified in agent configuration. The framework automatically detects the provider from the model name.

**Supported Models:**

**OpenAI:**
- `gpt-5` - GPT-5
- `gpt-5-mini` - Smaller, fast
- `o1` - O1

**Anthropic (Claude 4 Family - Latest):**
- `claude-opus-4-5-20251124` - Claude Opus 4.5 (most powerful, released November 2024)
- `claude-opus-4-1-20250514` - Claude Opus 4.1 (incremental update to Opus 4)
- `claude-opus-4-20250522` - Claude Opus 4 (world's best coding model)
- `claude-sonnet-4-5-20250929` - Claude Sonnet 4.5 (smartest model, efficient for everyday use)
- `claude-sonnet-4-20250522` - Claude Sonnet 4 (significant upgrade, superior coding and reasoning)
- `claude-haiku-4-5-20251001` - Claude Haiku 4.5 (fastest, most cost-efficient)

**Anthropic (Claude 3 Family - Previous Generation):**
- `claude-3-7-sonnet-20250219` - Claude 3.7 Sonnet
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `claude-3-5-haiku-20241022` - Claude 3.5 Haiku

**Google Gemini (Gemini 3 Family - Latest):**
- `gemini-3-pro` - Gemini 3 Pro (most intelligent, state-of-the-art reasoning)
- `gemini-3-deep-think` - Gemini 3 Deep Think (advanced reasoning mode)

**Google Gemini (Gemini 2.5 Family):**
- `gemini-2.5-pro` - Gemini 2.5 Pro (powerful with adaptive thinking)
- `gemini-2.5-flash` - Gemini 2.5 Flash (fast, well-rounded capabilities)
- `gemini-2.5-flash-lite` - Gemini 2.5 Flash-Lite (optimized for cost-efficiency)

**Google Gemini (Gemini 2.0 Family):**
- `gemini-2.0-flash` - Gemini 2.0 Flash (1M token context window)
- `gemini-2.0-flash-thinking` - Gemini 2.0 Flash Thinking (shows reasoning process)

**Example:**
```bash
DEFAULT_MODEL=gpt-5-mini
# or
DEFAULT_MODEL=claude-sonnet-4-5-20250929
# or
DEFAULT_MODEL=gemini-3-pro
```

### FALLBACK_PROVIDER

- **Type**: string (enum: `openai`, `anthropic`, `gemini`)
- **Required**: No
- **Default**: `openai`
- **Description**: Provider to use when the model name doesn't clearly indicate a provider. Used as a fallback when automatic detection fails.

**Example:**
```bash
FALLBACK_PROVIDER=openai
```

### Provider-Specific Settings

#### OpenAI Settings

**OPENAI_DEFAULT_TEMPERATURE**
- **Type**: float (0.0 to 2.0)
- **Default**: `0.7`
- **Description**: Default temperature for OpenAI models. Higher values make output more random.

**OPENAI_DEFAULT_TIMEOUT**
- **Type**: integer (seconds)
- **Default**: `120`
- **Description**: Timeout for OpenAI API requests.

**OPENAI_API_MODEL**
- **Type**: string
- **Default**: Value of `DEFAULT_MODEL`
- **Description**: Override model for OpenAI requests.

**Example:**
```bash
OPENAI_DEFAULT_TEMPERATURE=0.7
OPENAI_DEFAULT_TIMEOUT=120
OPENAI_API_MODEL=gpt-5
```

#### Anthropic Settings

**ANTHROPIC_DEFAULT_TEMPERATURE**
- **Type**: float (0.0 to 1.0)
- **Default**: `0.7`
- **Description**: Default temperature for Anthropic models.

**ANTHROPIC_DEFAULT_TIMEOUT**
- **Type**: integer (seconds)
- **Default**: `120`
- **Description**: Timeout for Anthropic API requests.

**Example:**
```bash
ANTHROPIC_DEFAULT_TEMPERATURE=0.7
ANTHROPIC_DEFAULT_TIMEOUT=120
```

#### Gemini Settings

**GEMINI_DEFAULT_TEMPERATURE**
- **Type**: float (0.0 to 2.0)
- **Default**: `0.7`
- **Description**: Default temperature for Gemini models.

**GEMINI_DEFAULT_TIMEOUT**
- **Type**: integer (seconds)
- **Default**: `120`
- **Description**: Timeout for Gemini API requests.

**Example:**
```bash
GEMINI_DEFAULT_TEMPERATURE=0.7
GEMINI_DEFAULT_TIMEOUT=120
```

### Model Selection Behavior

The framework uses the following logic to select a model:

1. **Agent Configuration**: If the agent specifies a model in its configuration, use that model
2. **Session Configuration**: If the session was initialized with a model, use that model
3. **DEFAULT_MODEL**: Use the default model from environment variables
4. **Provider Detection**: Automatically detect provider from model name:
   - Models starting with `gpt-` or `o1` → OpenAI
   - Models starting with `claude-` → Anthropic
   - Models starting with `gemini-` → Google Gemini
5. **Fallback**: If provider cannot be determined, use `FALLBACK_PROVIDER`

### Runtime Model Switching

Models can be changed at runtime through:

1. **Session Initialization**: Specify model in session configuration
2. **Agent Configuration API**: Update agent configuration via `/config/agents/{agent_id}`
3. **Elasticsearch Configuration**: Store and version agent configurations

## Session Storage

### SESSION_STORAGE_TYPE

- **Type**: string (enum: `memory`, `mongodb`, `elasticsearch`)
- **Required**: No
- **Default**: `memory`
- **Description**: Backend for session persistence.

**Options:**
- `memory`: In-memory storage (development only, data lost on restart)
- `mongodb`: MongoDB persistent storage (recommended for production)
- `elasticsearch`: Elasticsearch storage (advanced features, observability)

**Example:**
```bash
SESSION_STORAGE_TYPE=mongodb
```

### MongoDB Configuration

Used when `SESSION_STORAGE_TYPE=mongodb`.

#### MONGODB_CONNECTION_STRING

- **Type**: string (MongoDB connection URI)
- **Required**: Yes (when using MongoDB)
- **Default**: `mongodb://localhost:27017`
- **Description**: MongoDB connection string.

**Examples:**
```bash
# Local MongoDB
MONGODB_CONNECTION_STRING=mongodb://localhost:27017

# MongoDB with authentication
MONGODB_CONNECTION_STRING=mongodb://username:password@localhost:27017

# MongoDB Atlas
MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/database

# MongoDB replica set
MONGODB_CONNECTION_STRING=mongodb://host1:27017,host2:27017,host3:27017/?replicaSet=myReplicaSet
```

#### MONGODB_DATABASE_NAME

- **Type**: string
- **Required**: No
- **Default**: `agent_sessions`
- **Description**: Database name for session storage.

**Example:**
```bash
MONGODB_DATABASE_NAME=agent_sessions
```

#### MONGODB_COLLECTION_NAME

- **Type**: string
- **Required**: No
- **Default**: `sessions`
- **Description**: Collection name for session documents.

**Example:**
```bash
MONGODB_COLLECTION_NAME=sessions
```

### Elasticsearch Configuration

Used when `SESSION_STORAGE_TYPE=elasticsearch`.

#### ELASTICSEARCH_ENABLED

- **Type**: boolean
- **Required**: No
- **Default**: `false`
- **Description**: Enable Elasticsearch integration for advanced features.

**Example:**
```bash
ELASTICSEARCH_ENABLED=true
```

#### ELASTICSEARCH_URL

- **Type**: string (URL)
- **Required**: Yes (when Elasticsearch enabled)
- **Default**: `http://localhost:9200`
- **Description**: Elasticsearch cluster URL.

**Examples:**
```bash
# Local Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200

# Elasticsearch Cloud
ELASTICSEARCH_URL=https://my-deployment.es.us-central1.gcp.cloud.es.io:9243
```

#### ELASTICSEARCH_USERNAME

- **Type**: string
- **Required**: Conditional (required for authenticated Elasticsearch)
- **Default**: None
- **Description**: Username for Elasticsearch authentication.

**Example:**
```bash
ELASTICSEARCH_USERNAME=elastic
```

#### ELASTICSEARCH_PASSWORD

- **Type**: string
- **Required**: Conditional (required for authenticated Elasticsearch)
- **Default**: None
- **Description**: Password for Elasticsearch authentication.

**Example:**
```bash
ELASTICSEARCH_PASSWORD=your-password-here
```

#### ELASTICSEARCH_API_KEY

- **Type**: string
- **Required**: Conditional (alternative to username/password)
- **Default**: None
- **Description**: API key for Elasticsearch authentication.

**Example:**
```bash
ELASTICSEARCH_API_KEY=your-api-key-here
```

#### ELASTICSEARCH_VERIFY_CERTS

- **Type**: boolean
- **Required**: No
- **Default**: `true`
- **Description**: Verify SSL certificates for Elasticsearch connections.

**Example:**
```bash
ELASTICSEARCH_VERIFY_CERTS=true
```

#### ELASTICSEARCH_CA_CERTS

- **Type**: string (file path)
- **Required**: No
- **Default**: None
- **Description**: Path to CA certificate file for SSL verification.

**Example:**
```bash
ELASTICSEARCH_CA_CERTS=/path/to/ca.crt
```

## File Storage

### LOCAL_STORAGE_PATH

- **Type**: string (directory path)
- **Required**: No
- **Default**: `./file_storage`
- **Description**: Directory path for local file storage.

**Example:**
```bash
LOCAL_STORAGE_PATH=./file_storage
# or absolute path
LOCAL_STORAGE_PATH=/var/lib/agent-framework/files
```

### S3 Configuration

#### AWS_S3_BUCKET

- **Type**: string
- **Required**: Conditional (required for S3 storage)
- **Default**: None
- **Description**: S3 bucket name for file storage.

**Example:**
```bash
AWS_S3_BUCKET=my-agent-files
```

#### AWS_REGION

- **Type**: string
- **Required**: Conditional (required for S3 storage)
- **Default**: None
- **Description**: AWS region for S3 bucket.

**Example:**
```bash
AWS_REGION=us-east-1
```

#### AWS_ACCESS_KEY_ID

- **Type**: string
- **Required**: Conditional (required for S3 with explicit credentials)
- **Default**: None (uses AWS credential chain)
- **Description**: AWS access key ID. If not provided, uses default AWS credential chain.

**Example:**
```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
```

#### AWS_SECRET_ACCESS_KEY

- **Type**: string
- **Required**: Conditional (required for S3 with explicit credentials)
- **Default**: None (uses AWS credential chain)
- **Description**: AWS secret access key.

**Example:**
```bash
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### MinIO Configuration

#### MINIO_ENDPOINT

- **Type**: string (URL)
- **Required**: Conditional (required for MinIO storage)
- **Default**: None
- **Description**: MinIO server endpoint.

**Example:**
```bash
MINIO_ENDPOINT=localhost:9000
# or with protocol
MINIO_ENDPOINT=https://minio.example.com
```

#### MINIO_ACCESS_KEY

- **Type**: string
- **Required**: Conditional (required for MinIO storage)
- **Default**: None
- **Description**: MinIO access key.

**Example:**
```bash
MINIO_ACCESS_KEY=minioadmin
```

#### MINIO_SECRET_KEY

- **Type**: string
- **Required**: Conditional (required for MinIO storage)
- **Default**: None
- **Description**: MinIO secret key.

**Example:**
```bash
MINIO_SECRET_KEY=minioadmin
```

#### MINIO_BUCKET

- **Type**: string
- **Required**: Conditional (required for MinIO storage)
- **Default**: None
- **Description**: MinIO bucket name for file storage.

**Example:**
```bash
MINIO_BUCKET=agent-files
```

#### MINIO_SECURE

- **Type**: boolean
- **Required**: No
- **Default**: `false`
- **Description**: Use HTTPS for MinIO connections.

**Example:**
```bash
MINIO_SECURE=true
```

### S3_AS_DEFAULT

- **Type**: boolean
- **Required**: No
- **Default**: `false`
- **Description**: Use S3 as the default file storage backend instead of local storage.

**Example:**
```bash
S3_AS_DEFAULT=true
```

### File Storage Backend Selection

The framework supports multiple file storage backends simultaneously:

1. **Local Storage**: Always available, used as fallback
2. **S3 Storage**: Enabled when `AWS_S3_BUCKET` is configured
3. **MinIO Storage**: Enabled when `MINIO_ENDPOINT` is configured

**Backend Priority:**
- If `S3_AS_DEFAULT=true` and S3 is configured → Use S3
- If MinIO is configured → Use MinIO
- Otherwise → Use Local storage

## Authentication

### REQUIRE_AUTH

- **Type**: boolean
- **Required**: No
- **Default**: `false`
- **Description**: Enable authentication for all API endpoints. When `false`, all endpoints are publicly accessible.

**Example:**
```bash
REQUIRE_AUTH=true
```

### Basic Authentication

#### BASIC_AUTH_USERNAME

- **Type**: string
- **Required**: Conditional (required when `REQUIRE_AUTH=true`)
- **Default**: `admin`
- **Description**: Username for HTTP Basic Authentication.

**Example:**
```bash
BASIC_AUTH_USERNAME=admin
```

#### BASIC_AUTH_PASSWORD

- **Type**: string
- **Required**: Conditional (required when `REQUIRE_AUTH=true`)
- **Default**: `password`
- **Description**: Password for HTTP Basic Authentication.

**Security Best Practice:** Use a strong, randomly generated password in production.

**Example:**
```bash
BASIC_AUTH_PASSWORD=your-secure-password-here
```

### API Key Authentication

#### API_KEYS

- **Type**: string (comma-separated list)
- **Required**: No
- **Default**: Empty
- **Description**: Comma-separated list of valid API keys for Bearer token or X-API-Key header authentication.

**Security Best Practices:**
- Generate cryptographically secure random keys
- Use different keys for different clients/applications
- Rotate keys periodically
- Never commit keys to version control

**Example:**
```bash
API_KEYS=sk-abc123def456,sk-xyz789uvw012
```

**Usage:**
```bash
# Bearer token
curl -H "Authorization: Bearer sk-abc123def456" http://localhost:8000/metadata

# X-API-Key header
curl -H "X-API-Key: sk-abc123def456" http://localhost:8000/metadata
```

### Admin Password

#### ADMIN_PASSWORD

- **Type**: string
- **Required**: No
- **Default**: `admin123`
- **Description**: Password for admin-only endpoints (secondary authentication layer).

**Example:**
```bash
ADMIN_PASSWORD=your-admin-password-here
```

### Authentication Methods

The framework supports three authentication methods (when `REQUIRE_AUTH=true`):

1. **Basic Authentication**: Username and password
   ```bash
   curl -u admin:password http://localhost:8000/metadata
   ```

2. **Bearer Token**: API key in Authorization header
   ```bash
   curl -H "Authorization: Bearer your-api-key" http://localhost:8000/metadata
   ```

3. **X-API-Key Header**: API key in custom header
   ```bash
   curl -H "X-API-Key: your-api-key" http://localhost:8000/metadata
   ```

### Security Best Practices

1. **Always enable authentication in production**: Set `REQUIRE_AUTH=true`
2. **Use strong passwords**: Generate random passwords with sufficient entropy
3. **Use HTTPS**: Always use HTTPS in production to protect credentials
4. **Rotate credentials**: Periodically rotate passwords and API keys
5. **Limit API key scope**: Use different keys for different applications
6. **Monitor access**: Log and monitor authentication attempts
7. **Rate limiting**: Implement rate limiting to prevent brute force attacks

## Elasticsearch Integration

Elasticsearch provides advanced features for the Agent Framework:

### Features

1. **Configuration Management**: Store and version agent configurations
2. **Observability**: Log agent interactions and performance metrics
3. **Circuit Breaker**: Automatic failover when Elasticsearch is unavailable
4. **Performance Monitoring**: Track response times and resource usage

### Configuration

See [Elasticsearch Configuration](#elasticsearch-configuration) section above.

### Circuit Breaker

The framework includes a circuit breaker for Elasticsearch:

- **Closed**: Normal operation, requests go to Elasticsearch
- **Open**: Elasticsearch unavailable, requests fail fast
- **Half-Open**: Testing if Elasticsearch recovered

**Configuration:**
- Failure threshold: 5 consecutive failures
- Recovery timeout: 60 seconds
- Success threshold: 2 consecutive successes

### Observability Features

When Elasticsearch is enabled:

1. **Agent Lifecycle Tracking**: Track agent creation, updates, and deletion
2. **Performance Metrics**: Response times, token usage, error rates
3. **Configuration Versioning**: Track configuration changes over time
4. **Session Analytics**: Analyze session patterns and user behavior

## Advanced Options

### AGENT_TYPE

- **Type**: string
- **Required**: No
- **Default**: Agent class name
- **Description**: Identifier for the agent type in sessions and messages.

**Example:**
```bash
AGENT_TYPE=CustomerSupportAgent
```

### AGENT_PORT

- **Type**: integer
- **Required**: No
- **Default**: `8000`
- **Description**: Port for the FastAPI server.

**Example:**
```bash
AGENT_PORT=8000
```

### AGENT_HOST

- **Type**: string
- **Required**: No
- **Default**: `0.0.0.0`
- **Description**: Host address for the FastAPI server.

**Example:**
```bash
AGENT_HOST=0.0.0.0
```

### AGENT_RELOAD

- **Type**: boolean
- **Required**: No
- **Default**: `true`
- **Description**: Enable auto-reload for development.

**Example:**
```bash
AGENT_RELOAD=false
```

### LOG_LEVEL

- **Type**: string (enum: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- **Required**: No
- **Default**: `INFO`
- **Description**: Logging level for the application.

**Example:**
```bash
LOG_LEVEL=DEBUG
```

### AGENT_CLASS_PATH

- **Type**: string (format: `module:ClassName`)
- **Required**: Conditional (required when running server directly)
- **Default**: None
- **Description**: Python module path and class name for the agent.

**Example:**
```bash
AGENT_CLASS_PATH=examples.simple_agent:CalculatorAgent
```

## Deployment Scenarios

### Development Setup

Minimal configuration for local development:

```bash
# .env
OPENAI_API_KEY=sk-your-key-here
DEFAULT_MODEL=gpt-5-mini
SESSION_STORAGE_TYPE=memory
REQUIRE_AUTH=false
LOG_LEVEL=DEBUG
```

### Production with MongoDB

Recommended configuration for production:

```bash
# .env
# API Keys
OPENAI_API_KEY=sk-your-production-key
ANTHROPIC_API_KEY=sk-ant-your-key
GEMINI_API_KEY=your-gemini-key

# Model Configuration
DEFAULT_MODEL=claude-sonnet-4-5-20250929
FALLBACK_PROVIDER=anthropic

# Session Storage
SESSION_STORAGE_TYPE=mongodb
MONGODB_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/db
MONGODB_DATABASE_NAME=agent_sessions

# File Storage
S3_AS_DEFAULT=true
AWS_S3_BUCKET=my-production-bucket
AWS_REGION=us-east-1

# Authentication
REQUIRE_AUTH=true
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=your-secure-password
API_KEYS=sk-key1,sk-key2,sk-key3
ADMIN_PASSWORD=your-admin-password

# Server
AGENT_PORT=8000
AGENT_HOST=0.0.0.0
AGENT_RELOAD=false
LOG_LEVEL=INFO
```

### Production with Elasticsearch

Advanced configuration with Elasticsearch:

```bash
# .env
# API Keys
OPENAI_API_KEY=sk-your-production-key
ANTHROPIC_API_KEY=sk-ant-your-key
GEMINI_API_KEY=your-gemini-key

# Model Configuration
DEFAULT_MODEL=gemini-3-pro

# Session Storage
SESSION_STORAGE_TYPE=elasticsearch
ELASTICSEARCH_ENABLED=true
ELASTICSEARCH_URL=https://my-deployment.es.cloud.es.io:9243
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=your-es-password
ELASTICSEARCH_VERIFY_CERTS=true

# File Storage
S3_AS_DEFAULT=true
AWS_S3_BUCKET=my-production-bucket
AWS_REGION=us-east-1

# Authentication
REQUIRE_AUTH=true
API_KEYS=sk-key1,sk-key2
ADMIN_PASSWORD=your-admin-password

# Server
AGENT_PORT=8000
LOG_LEVEL=INFO
```

### Multi-Agent Deployment

Configuration for multiple agent types:

```bash
# .env
# API Keys (all providers for flexibility)
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key
GEMINI_API_KEY=your-gemini-key

# Model Configuration
DEFAULT_MODEL=claude-sonnet-4-5-20250929
FALLBACK_PROVIDER=anthropic

# Session Storage (MongoDB for multi-agent tracking)
SESSION_STORAGE_TYPE=mongodb
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE_NAME=multi_agent_sessions

# File Storage (shared across agents)
LOCAL_STORAGE_PATH=/shared/file_storage

# Authentication
REQUIRE_AUTH=true
API_KEYS=sk-agent1-key,sk-agent2-key,sk-agent3-key

# Server
AGENT_PORT=8000
LOG_LEVEL=INFO
```

## Troubleshooting

### Common Configuration Errors

#### "No API key configured"
**Cause:** Missing or invalid API key for the selected model provider.
**Solution:** Set the appropriate API key environment variable (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY`).

#### "Session storage not available"
**Cause:** Session storage backend failed to initialize.
**Solution:** 
- For MongoDB: Verify `MONGODB_CONNECTION_STRING` is correct and MongoDB is running
- For Elasticsearch: Verify `ELASTICSEARCH_URL` and credentials are correct

#### "Authentication required"
**Cause:** `REQUIRE_AUTH=true` but no valid credentials provided.
**Solution:** Provide credentials using Basic Auth, Bearer token, or X-API-Key header.

#### "Elasticsearch service is unavailable"
**Cause:** Elasticsearch is down or unreachable.
**Solution:** 
- Check Elasticsearch is running
- Verify `ELASTICSEARCH_URL` is correct
- Check network connectivity
- Circuit breaker will automatically fail over to default configuration

### Storage Backend Issues

#### MongoDB Connection Failures
- Verify connection string format
- Check MongoDB is running and accessible
- Verify authentication credentials
- Check network firewall rules

#### S3 Upload Failures
- Verify AWS credentials are correct
- Check S3 bucket exists and is accessible
- Verify IAM permissions for bucket operations
- Check AWS region is correct

#### MinIO Connection Issues
- Verify MinIO endpoint is correct
- Check MinIO is running and accessible
- Verify access key and secret key
- Check bucket exists

### Authentication Problems

#### "Invalid credentials"
- Verify username/password are correct
- Check API key is in the `API_KEYS` list
- Ensure no extra whitespace in credentials

#### "Access denied"
- Verify user has permission for the resource
- Check session belongs to the requesting user
- Verify admin password for admin endpoints

## Migration Guide

### Upgrading from Old Configurations

#### From v0.1.x to v0.2.x

**Changes:**
- Added `FALLBACK_PROVIDER` configuration
- Added Elasticsearch support
- Added multi-backend file storage
- Added agent identity tracking
- Updated to latest Claude 4 and Gemini 3 models

**Migration Steps:**
1. Add `FALLBACK_PROVIDER=openai` to your `.env`
2. Update `SESSION_STORAGE_TYPE` if using new backends
3. Configure file storage backends if needed
4. Update model names to latest versions (e.g., `claude-sonnet-4-5-20250929`, `gemini-3-pro`)
5. No breaking changes to existing configurations

### Migrating Between Storage Backends

#### From Memory to MongoDB

1. Set up MongoDB instance
2. Update configuration:
   ```bash
   SESSION_STORAGE_TYPE=mongodb
   MONGODB_CONNECTION_STRING=mongodb://localhost:27017
   ```
3. Restart server
4. Note: Existing in-memory sessions will be lost

#### From MongoDB to Elasticsearch

1. Set up Elasticsearch cluster
2. Update configuration:
   ```bash
   SESSION_STORAGE_TYPE=elasticsearch
   ELASTICSEARCH_ENABLED=true
   ELASTICSEARCH_URL=http://localhost:9200
   ```
3. Restart server
4. Note: Existing MongoDB sessions will remain in MongoDB but new sessions use Elasticsearch

#### From Local to S3 File Storage

1. Create S3 bucket
2. Configure AWS credentials
3. Update configuration:
   ```bash
   S3_AS_DEFAULT=true
   AWS_S3_BUCKET=my-bucket
   AWS_REGION=us-east-1
   ```
4. Restart server
5. Note: Existing local files remain local, new files go to S3
6. Optional: Manually migrate existing files to S3

## Environment Variables Reference

Quick reference table of all environment variables:

| Variable | Type | Default | Required | Description |
|----------|------|---------|----------|-------------|
| `OPENAI_API_KEY` | string | None | Conditional | OpenAI API key |
| `ANTHROPIC_API_KEY` | string | None | Conditional | Anthropic API key |
| `GEMINI_API_KEY` | string | None | Conditional | Google Gemini API key |
| `DEFAULT_MODEL` | string | `gpt-5-mini` | No | Default model to use |
| `FALLBACK_PROVIDER` | string | `openai` | No | Fallback provider |
| `SESSION_STORAGE_TYPE` | string | `memory` | No | Session storage backend |
| `MONGODB_CONNECTION_STRING` | string | `mongodb://localhost:27017` | Conditional | MongoDB connection URI |
| `MONGODB_DATABASE_NAME` | string | `agent_sessions` | No | MongoDB database name |
| `MONGODB_COLLECTION_NAME` | string | `sessions` | No | MongoDB collection name |
| `ELASTICSEARCH_ENABLED` | boolean | `false` | No | Enable Elasticsearch |
| `ELASTICSEARCH_URL` | string | `http://localhost:9200` | Conditional | Elasticsearch URL |
| `ELASTICSEARCH_USERNAME` | string | None | Conditional | Elasticsearch username |
| `ELASTICSEARCH_PASSWORD` | string | None | Conditional | Elasticsearch password |
| `LOCAL_STORAGE_PATH` | string | `./file_storage` | No | Local file storage path |
| `AWS_S3_BUCKET` | string | None | Conditional | S3 bucket name |
| `AWS_REGION` | string | None | Conditional | AWS region |
| `MINIO_ENDPOINT` | string | None | Conditional | MinIO endpoint |
| `MINIO_ACCESS_KEY` | string | None | Conditional | MinIO access key |
| `MINIO_SECRET_KEY` | string | None | Conditional | MinIO secret key |
| `S3_AS_DEFAULT` | boolean | `false` | No | Use S3 as default storage |
| `REQUIRE_AUTH` | boolean | `false` | No | Enable authentication |
| `BASIC_AUTH_USERNAME` | string | `admin` | Conditional | Basic auth username |
| `BASIC_AUTH_PASSWORD` | string | `password` | Conditional | Basic auth password |
| `API_KEYS` | string | Empty | No | Comma-separated API keys |
| `ADMIN_PASSWORD` | string | `admin123` | No | Admin password |
| `AGENT_TYPE` | string | Class name | No | Agent type identifier |
| `AGENT_PORT` | integer | `8000` | No | Server port |
| `AGENT_HOST` | string | `0.0.0.0` | No | Server host |
| `LOG_LEVEL` | string | `INFO` | No | Logging level |