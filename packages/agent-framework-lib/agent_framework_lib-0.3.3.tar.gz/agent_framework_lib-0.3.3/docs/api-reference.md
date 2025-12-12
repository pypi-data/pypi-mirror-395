# API Reference

Complete API reference for the Agent Framework.

## Table of Contents

- [Core Components](#core-components)
  - [AgentInterface](#agentinterface)
  - [BaseAgent](#baseagent)
  - [StateManager](#statemanager)
  - [ModelClientFactory](#modelclientfactory)
- [Implementations](#implementations)
  - [LlamaIndexAgent](#llamaindexagent)
  - [MicrosoftAgent](#microsoftagent)
- [Session Management](#session-management)
  - [SessionStorage](#sessionstorage)
- [Data Models](#data-models)
- [Utilities](#utilities)

## Core Components

### AgentInterface

The abstract interface that all agents must implement.

**Location:** `agent_framework.core.agent_interface`

#### Methods

##### `async handle_message(session_id: str, agent_input: StructuredAgentInput) -> StructuredAgentOutput`

Process a user message and return a complete response.

**Parameters:**
- `session_id` (str): Unique identifier for the session
- `agent_input` (StructuredAgentInput): User input with query and optional parts

**Returns:**
- `StructuredAgentOutput`: Agent response with text and metadata

**Example:**
```python
response = await agent.handle_message(
    session_id="session-123",
    agent_input=StructuredAgentInput(query="Hello!")
)
print(response.response_text)
```

##### `async handle_message_stream(session_id: str, agent_input: StructuredAgentInput) -> AsyncIterator[StructuredAgentOutput]`

Process a user message with streaming response.

**Parameters:**
- `session_id` (str): Unique identifier for the session
- `agent_input` (StructuredAgentInput): User input

**Yields:**
- `StructuredAgentOutput`: Streaming response chunks

**Example:**
```python
async for chunk in agent.handle_message_stream(session_id, agent_input):
    print(chunk.response_text, end='', flush=True)
```

##### `async get_state(session_id: str) -> Dict[str, Any]`

Retrieve the current agent state for persistence.

**Parameters:**
- `session_id` (str): Session identifier

**Returns:**
- `Dict[str, Any]`: Agent state dictionary

**Example:**
```python
state = await agent.get_state("session-123")
# Save state to storage
await storage.save_agent_state("session-123", state)
```

##### `async load_state(state: Dict[str, Any])`

Load previously saved agent state.

**Parameters:**
- `state` (Dict[str, Any]): State dictionary to load

**Example:**
```python
state = await storage.load_agent_state("session-123")
await agent.load_state(state)
```

##### `async configure_session(session_id: str, system_prompt: str = None, model_name: str = None, model_config: dict = None)`

Configure session parameters.

**Parameters:**
- `session_id` (str): Session identifier
- `system_prompt` (str, optional): Custom system prompt
- `model_name` (str, optional): Model to use
- `model_config` (dict, optional): Model configuration parameters

**Example:**
```python
await agent.configure_session(
    session_id="session-123",
    system_prompt="You are a helpful assistant",
    model_name="gpt-4",
    model_config={"temperature": 0.7}
)
```

##### `async get_metadata() -> Dict[str, Any]`

Get agent metadata.

**Returns:**
- `Dict[str, Any]`: Agent metadata including name, version, capabilities

**Example:**
```python
metadata = await agent.get_metadata()
print(f"Agent: {metadata['name']} v{metadata['version']}")
```

---

### BaseAgent

Generic base class providing common agent functionality.

**Location:** `agent_framework.core.base_agent`

**Inherits:** `AgentInterface`

#### Constructor

```python
BaseAgent()
```

Creates a new base agent instance with default configuration.

#### Methods

All methods from `AgentInterface` plus:

##### `def get_system_prompt() -> Optional[str]`

Get the default system prompt for this agent.

**Returns:**
- `Optional[str]`: System prompt or None

**Example:**
```python
class MyAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return "You are a helpful assistant"
```

---

### StateManager

Handles framework-agnostic state management.

**Location:** `agent_framework.core.state_manager`

#### Static Methods

##### `compress_state(state: Dict[str, Any]) -> bytes`

Compress agent state for efficient storage.

**Parameters:**
- `state` (Dict[str, Any]): State dictionary to compress

**Returns:**
- `bytes`: Compressed state data

**Example:**
```python
from agent_framework.core import StateManager

state = {"conversation": [...], "config": {...}}
compressed = StateManager.compress_state(state)
```

##### `decompress_state(compressed: bytes) -> Dict[str, Any]`

Decompress previously compressed state.

**Parameters:**
- `compressed` (bytes): Compressed state data

**Returns:**
- `Dict[str, Any]`: Decompressed state dictionary

**Example:**
```python
state = StateManager.decompress_state(compressed_data)
```

##### `create_agent_identity(agent_instance: Any) -> AgentIdentity`

Create an identity for an agent instance.

**Parameters:**
- `agent_instance` (Any): Agent instance

**Returns:**
- `AgentIdentity`: Agent identity with ID, type, and metadata

**Example:**
```python
identity = StateManager.create_agent_identity(my_agent)
print(f"Agent ID: {identity.agent_id}")
```

##### `validate_state_compatibility(state: Dict[str, Any], identity: AgentIdentity) -> bool`

Validate if state is compatible with agent identity.

**Parameters:**
- `state` (Dict[str, Any]): State to validate
- `identity` (AgentIdentity): Agent identity

**Returns:**
- `bool`: True if compatible, False otherwise

**Example:**
```python
if StateManager.validate_state_compatibility(state, identity):
    await agent.load_state(state)
else:
    print("State incompatible, starting fresh")
```

---

### ModelClientFactory

Factory for creating LLM clients.

**Location:** `agent_framework.core.model_clients`

#### Constructor

```python
ModelClientFactory(config: ModelConfig = None)
```

**Parameters:**
- `config` (ModelConfig, optional): Model configuration

#### Methods

##### `create_openai_client(model_name: str = None, agent_config: dict = None, **override_params) -> AsyncOpenAI`

Create an OpenAI client.

**Parameters:**
- `model_name` (str, optional): Model name
- `agent_config` (dict, optional): Agent configuration
- `**override_params`: Additional parameters to override

**Returns:**
- `AsyncOpenAI`: Configured OpenAI client

**Example:**
```python
from agent_framework.core import ModelClientFactory

factory = ModelClientFactory()
client = factory.create_openai_client(
    model_name="gpt-4",
    temperature=0.7
)
```

##### `create_anthropic_client(model_name: str = None, agent_config: dict = None, **override_params) -> AsyncAnthropic`

Create an Anthropic client.

**Parameters:**
- `model_name` (str, optional): Model name
- `agent_config` (dict, optional): Agent configuration
- `**override_params`: Additional parameters

**Returns:**
- `AsyncAnthropic`: Configured Anthropic client

##### `create_gemini_client(model_name: str = None, agent_config: dict = None, **override_params) -> genai.GenerativeModel`

Create a Google Gemini client.

**Parameters:**
- `model_name` (str, optional): Model name
- `agent_config` (dict, optional): Agent configuration
- `**override_params`: Additional parameters

**Returns:**
- `genai.GenerativeModel`: Configured Gemini client

##### `create_llamaindex_llm(model_name: str = None, agent_config: dict = None, **override_params) -> Any`

Create a LlamaIndex LLM instance.

**Parameters:**
- `model_name` (str, optional): Model name
- `agent_config` (dict, optional): Agent configuration
- `**override_params`: Additional parameters

**Returns:**
- `Any`: LlamaIndex LLM instance (OpenAI, Anthropic, or Gemini)

**Example:**
```python
llm = factory.create_llamaindex_llm(
    model_name="gpt-4",
    temperature=0.8
)
```

---

## Implementations

### LlamaIndexAgent

Base class for LlamaIndex-based agents.

**Location:** `agent_framework.implementations.llamaindex_agent`

**Inherits:** `BaseAgent`

#### Constructor

```python
LlamaIndexAgent()
```

Creates a new LlamaIndex agent instance.

#### Abstract Methods

These methods must be implemented by subclasses:

##### `def get_agent_prompt() -> str`

Return the system prompt for the agent.

**Returns:**
- `str`: System prompt text

**Example:**
```python
def get_agent_prompt(self) -> str:
    return "You are a helpful calculator assistant."
```

##### `def get_agent_tools() -> List[callable]`

Return the list of tools available to the agent.

**Returns:**
- `List[callable]`: List of LlamaIndex FunctionTool instances

**Example:**
```python
from llama_index.core.tools import FunctionTool

def get_agent_tools(self) -> List[callable]:
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    return [FunctionTool.from_defaults(fn=add)]
```

#### Optional Methods

##### `def get_mcp_server_params() -> List[StdioServerParams]`

Configure external MCP tools.

**Returns:**
- `List[StdioServerParams]`: List of MCP server configurations

**Example:**
```python
from autogen_ext.tools.mcp import StdioServerParams

def get_mcp_server_params(self) -> List[StdioServerParams]:
    return [
        StdioServerParams(
            command='npx',
            args=['-y', '@modelcontextprotocol/server-filesystem', '/tmp'],
            read_timeout_seconds=60
        )
    ]
```

##### `def initialize_agent(model_name: str = None, agent_config: dict = None)`

Customize agent initialization.

**Parameters:**
- `model_name` (str, optional): Model to use
- `agent_config` (dict, optional): Configuration parameters

**Example:**
```python
def initialize_agent(self, model_name: str = None, agent_config: dict = None):
    # Custom initialization logic
    super().initialize_agent(model_name, agent_config)
```

---

### MicrosoftAgent

Base class for Microsoft Agent Framework-based agents.

**Location:** `agent_framework.implementations.microsoft_agent`

**Inherits:** `BaseAgent`

#### Constructor

```python
MicrosoftAgent()
```

Creates a new Microsoft agent instance.

#### Methods

Implementation-specific methods for Microsoft Agent Framework integration.

---

## Session Management

### SessionStorage

Interface for session persistence.

**Location:** `agent_framework.session.session_storage`

#### Implementations

##### MemorySessionStorage

In-memory session storage for development.

```python
from agent_framework.session import MemorySessionStorage

storage = MemorySessionStorage()
```

##### MongoDBSessionStorage

MongoDB-based session storage for production.

```python
from agent_framework.session import MongoDBSessionStorage

storage = MongoDBSessionStorage(
    connection_string="mongodb://localhost:27017",
    database_name="agent_sessions",
    collection_name="sessions"
)
```

#### Methods

##### `async save_session(session_data: SessionData) -> bool`

Save session metadata.

**Parameters:**
- `session_data` (SessionData): Session metadata to save

**Returns:**
- `bool`: True if successful

##### `async load_session(session_id: str) -> Optional[SessionData]`

Load session metadata.

**Parameters:**
- `session_id` (str): Session identifier

**Returns:**
- `Optional[SessionData]`: Session data or None if not found

##### `async save_agent_state(session_id: str, agent_state: Dict[str, Any]) -> bool`

Save agent state.

**Parameters:**
- `session_id` (str): Session identifier
- `agent_state` (Dict[str, Any]): Agent state to save

**Returns:**
- `bool`: True if successful

##### `async load_agent_state(session_id: str) -> Optional[Dict[str, Any]]`

Load agent state.

**Parameters:**
- `session_id` (str): Session identifier

**Returns:**
- `Optional[Dict[str, Any]]`: Agent state or None if not found

##### `async list_sessions(user_id: str = None) -> List[str]`

List all sessions, optionally filtered by user.

**Parameters:**
- `user_id` (str, optional): Filter by user ID

**Returns:**
- `List[str]`: List of session IDs

---

## Data Models

### StructuredAgentInput

User input to the agent.

**Fields:**
- `query` (str): User's text query
- `parts` (List[Dict], optional): Multimodal parts (images, etc.)
- `system_prompt` (str, optional): Custom system prompt
- `agent_config` (dict, optional): Agent configuration
- `session_id` (str, optional): Session identifier
- `correlation_id` (str, optional): Correlation identifier

**Example:**
```python
from agent_framework import StructuredAgentInput

agent_input = StructuredAgentInput(
    query="What is 2 + 2?",
    session_id="session-123",
    agent_config={"temperature": 0.7}
)
```

### StructuredAgentOutput

Agent response.

**Fields:**
- `response_text` (str): Main response text
- `parts` (List[Dict], optional): Response parts
- `session_id` (str): Session identifier
- `user_id` (str): User identifier
- `correlation_id` (str, optional): Correlation identifier
- `conversation_id` (str): Conversation identifier
- `metadata` (dict, optional): Additional metadata

**Example:**
```python
output = StructuredAgentOutput(
    response_text="The answer is 4",
    session_id="session-123",
    user_id="user-456"
)
```

### SessionData

Session metadata.

**Fields:**
- `session_id` (str): Unique session identifier
- `user_id` (str): User identifier
- `agent_instance_config` (dict): Agent configuration
- `correlation_id` (str, optional): Correlation identifier
- `created_at` (str, optional): Creation timestamp
- `updated_at` (str, optional): Last update timestamp
- `metadata` (dict, optional): Additional metadata
- `agent_id` (str, optional): Agent identifier
- `agent_type` (str, optional): Agent type
- `session_configuration` (dict, optional): Session configuration
- `session_label` (str, optional): Human-readable label

### AgentIdentity

Agent identity information.

**Fields:**
- `agent_id` (str): Unique agent identifier (UUID)
- `agent_type` (str): Agent class name
- `agent_class` (str): Full class path
- `config_hash` (str): Configuration hash
- `created_at` (datetime): Creation timestamp
- `metadata` (dict): Additional metadata

---

## Utilities

### create_basic_agent_server

Convenience function to start an agent server.

**Location:** `agent_framework`

**Signature:**
```python
def create_basic_agent_server(
    agent_class: Type[AgentInterface],
    port: int = 8000,
    host: str = "0.0.0.0"
) -> None
```

**Parameters:**
- `agent_class` (Type[AgentInterface]): Agent class to serve
- `port` (int, optional): Port number (default: 8000)
- `host` (str, optional): Host address (default: "0.0.0.0")

**Example:**
```python
from agent_framework import LlamaIndexAgent, create_basic_agent_server

class MyAgent(LlamaIndexAgent):
    def get_agent_prompt(self) -> str:
        return "I am a helpful assistant"
    
    def get_agent_tools(self) -> list:
        return []

if __name__ == "__main__":
    create_basic_agent_server(MyAgent, port=8000)
```

---

## HTTP API Endpoints

When using `create_basic_agent_server`, the following endpoints are available:

### POST /message

Send a message to the agent.

**Request Body:**
```json
{
  "query": "string",
  "parts": [],
  "system_prompt": "string",
  "agent_config": {},
  "session_id": "string",
  "correlation_id": "string"
}
```

**Response:**
```json
{
  "response_text": "string",
  "parts": [],
  "session_id": "string",
  "user_id": "string",
  "correlation_id": "string",
  "conversation_id": "string"
}
```

### POST /stream

Send a message with streaming response.

**Request Body:** Same as /message

**Response:** Server-Sent Events (SSE) stream

### POST /init

Initialize a new session.

**Request Body:**
```json
{
  "user_id": "string",
  "correlation_id": "string",
  "configuration": {
    "system_prompt": "string",
    "model_name": "string",
    "model_config": {}
  }
}
```

**Response:**
```json
{
  "session_id": "string",
  "configuration": {}
}
```

### POST /end

End a session.

**Request Body:**
```json
{
  "session_id": "string"
}
```

**Response:**
```json
{
  "success": true
}
```

### GET /sessions

List all sessions.

**Response:**
```json
["session-1", "session-2", ...]
```

### GET /sessions/{session_id}/history

Get session history.

**Response:**
```json
{
  "messages": [...]
}
```

### GET /config/models

Get model configuration.

**Response:**
```json
{
  "default_model": "gpt-4",
  "supported_models": {...},
  "supported_providers": {...}
}
```

### GET /metadata

Get agent metadata.

**Response:**
```json
{
  "name": "string",
  "version": "string",
  "capabilities": {}
}
```

---

## Environment Variables

### API Keys

- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GEMINI_API_KEY`: Google Gemini API key

### Configuration

- `DEFAULT_MODEL`: Default model to use (default: "gpt-4")
- `AGENT_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Authentication

- `REQUIRE_AUTH`: Enable authentication (true/false)
- `BASIC_AUTH_USERNAME`: Basic auth username
- `BASIC_AUTH_PASSWORD`: Basic auth password
- `API_KEYS`: Comma-separated list of valid API keys

### Session Storage

- `SESSION_STORAGE_TYPE`: Storage type ("memory" or "mongodb")
- `MONGODB_CONNECTION_STRING`: MongoDB connection string
- `MONGODB_DATABASE_NAME`: MongoDB database name
- `MONGODB_COLLECTION_NAME`: MongoDB collection name

### File Storage

- `LOCAL_STORAGE_PATH`: Local storage path
- `AWS_S3_BUCKET`: S3 bucket name
- `AWS_REGION`: AWS region
- `MINIO_ENDPOINT`: MinIO endpoint
- `MINIO_ACCESS_KEY`: MinIO access key
- `MINIO_SECRET_KEY`: MinIO secret key

---

## Type Hints

The framework uses Python type hints throughout. Import types from:

```python
from typing import List, Dict, Any, Optional, AsyncIterator
from agent_framework import (
    AgentInterface,
    BaseAgent,
    LlamaIndexAgent,
    StructuredAgentInput,
    StructuredAgentOutput,
    SessionData,
    AgentIdentity
)
```

---

## Error Handling

### Common Exceptions

- `ValueError`: Invalid configuration or parameters
- `ImportError`: Missing dependencies
- `HTTPException`: HTTP-related errors (from FastAPI)
- `ConnectionError`: Database or network connection errors

### Example Error Handling

```python
try:
    response = await agent.handle_message(session_id, agent_input)
except ValueError as e:
    print(f"Invalid input: {e}")
except ConnectionError as e:
    print(f"Connection failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Further Reading

- [Creating Agents Guide](creating-agents.md) - Learn how to build agents
- [Installation Guide](installation.md) - Installation instructions
- [Architecture](../ARCHITECTURE.md) - System architecture
- [Examples](../examples/) - Example implementations

---

**Questions?** Check the [Creating Agents Guide](creating-agents.md) or open an issue on GitHub.
