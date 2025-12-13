"""
Framework-Agnostic Base Agent Class

This base class provides a generic foundation for AI agents across different frameworks
(LlamaIndex, Microsoft Agent Framework, etc.):
- Session/config handling
- State management via subclass-provided context (serialize/deserialize)
- Non-streaming and streaming message processing
- Streaming event formatting aligned with modern UI expectations
- Special output parsing (charts, forms, structured data)

Note: This base does NOT construct any concrete agent.
Subclasses must implement all abstract methods to provide framework-specific functionality.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, List, AsyncGenerator, Union
from abc import abstractmethod
import json
from datetime import datetime
import logging
import os

from .agent_interface import (
    AgentInterface,
    StructuredAgentInput,
    StructuredAgentOutput,
    TextOutputPart,
    TextOutputStreamPart,
    TextInputPart,
)
from .model_config import model_config
from ..utils.special_blocks import parse_special_blocks_from_text

logger = logging.getLogger(__name__)


class BaseAgent(AgentInterface):
    """
    Abstract base class for framework-agnostic agents.
    
    Automatically injects rich content capabilities (Mermaid diagrams, Chart.js charts,
    forms, options blocks, tables) into the system prompt unless disabled via configuration.
    
    For a complete guide on creating agents with BaseAgent, see:
    - docs/CREATING_AGENTS.md - Comprehensive agent creation guide
    - examples/custom_framework_agent.py - Complete working example
    - docs/TOOLS_AND_MCP_GUIDE.md - Adding tools and MCP servers
    
    STREAMING ARCHITECTURE
    ======================
    
    This class implements a clear separation of concerns for streaming:
    
    ┌─────────────────────────────────────────────────────────────┐
    │  Custom Framework Agent (Your Implementation)               │
    │                                                             │
    │  run_agent(stream=True)                                     │
    │    └─> Yields RAW framework-specific events                │
    │         (e.g., LlamaIndex events, custom events, etc.)     │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │  BaseAgent.handle_message_stream() [FINAL - DO NOT OVERRIDE]│
    │                                                             │
    │  Orchestrates the streaming flow:                           │
    │    1. Calls run_agent(stream=True)                          │
    │    2. For each event, calls process_streaming_event()       │
    │    3. Converts to StructuredAgentOutput                     │
    └─────────────────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │  Custom Framework Agent (Your Implementation)               │
    │                                                             │
    │  process_streaming_event(event)                             │
    │    └─> Converts framework event to unified format          │
    │         Returns: {"type": "chunk", "content": "...", ...}   │
    └─────────────────────────────────────────────────────────────┘
    
    KEY PRINCIPLE: 
    - run_agent() = Framework-specific logic, yields RAW events
    - process_streaming_event() = Conversion layer, framework-specific
    - handle_message_stream() = Orchestration, framework-agnostic (DO NOT OVERRIDE)
    
    REQUIRED METHODS (must implement in subclass):
    - get_agent_prompt() -> str
    - get_agent_tools() -> List[callable]
    - async initialize_agent(model_name: str, system_prompt: str, tools: List[callable], **kwargs) -> None
    - create_fresh_context() -> Any
    - serialize_context(ctx: Any) -> Dict[str, Any]
    - deserialize_context(state: Dict[str, Any]) -> Any
    - async run_agent(query: str, ctx: Any, stream: bool = False) -> Union[str, AsyncGenerator]
    
    OPTIONAL METHODS (can be overridden):
    - get_mcp_server_params() -> Optional[Dict[str, Any]]
    - async process_streaming_event(event: Any) -> Optional[Dict[str, Any]]
    - get_model_config() -> Dict[str, Any]
    
    EXAMPLES AND GUIDES:
    - See examples/custom_framework_agent.py for a complete implementation
    - See docs/CREATING_AGENTS.md for step-by-step guide
    - See docs/TOOLS_AND_MCP_GUIDE.md for tool integration patterns
    """

    def __init__(self):
        # Session-configurable settings
        self._session_system_prompt: str = self.get_agent_prompt()
        self._session_model_config: Dict[str, Any] = {}
        self._session_model_name: Optional[str] = None

        # Rich content configuration (enabled by default)
        self._enable_rich_content: bool = True

        # Subclass-managed runtime
        self._agent_built: bool = False
        self._state_ctx: Optional[Any] = None

        # Build the agent via subclass hook
        self._ensure_agent_built()

    # ----- Abstract hooks to implement in subclass -----
    @abstractmethod
    def get_agent_prompt(self) -> str:
        """Return the default system prompt for the agent."""
        raise NotImplementedError

    @abstractmethod
    def get_agent_tools(self) -> List[callable]:
        """Return the list of tools available to the agent."""
        raise NotImplementedError

    @abstractmethod
    async def initialize_agent(
        self,
        model_name: str,
        system_prompt: str,
        tools: List[callable],
        **kwargs
    ) -> None:
        """Initialize the agent with the underlying framework."""
        raise NotImplementedError

    @abstractmethod
    def create_fresh_context(self) -> Any:
        """Create a new empty context for the agent."""
        raise NotImplementedError

    @abstractmethod
    def serialize_context(self, ctx: Any) -> Dict[str, Any]:
        """Serialize context to dictionary for persistence."""
        raise NotImplementedError

    @abstractmethod
    def deserialize_context(self, state: Dict[str, Any]) -> Any:
        """Deserialize dictionary to context object."""
        raise NotImplementedError

    @abstractmethod
    async def run_agent(
        self,
        query: str,
        ctx: Any,
        stream: bool = False
    ) -> Union[str, AsyncGenerator]:
        """
        Execute the agent with a query.
        
        IMPORTANT: This method should yield RAW framework-specific events when streaming.
        The events will be converted to unified format via process_streaming_event().
        
        Args:
            query: The user query to process
            ctx: The context object for conversation history
            stream: Whether to return streaming results
            
        Returns:
            If stream=False:
                - MUST return the final response as a string
                - Example: return "The answer is 42"
                
            If stream=True:
                - MUST return an AsyncGenerator that yields RAW framework events
                - DO NOT convert events to unified format here
                - Events will be converted via process_streaming_event()
                
        Examples:
            # Non-streaming mode
            async def run_agent(self, query, ctx, stream=False):
                if not stream:
                    response = await my_framework.chat(query, ctx)
                    return response.text
                    
            # Streaming mode - yield RAW framework events
            async def run_agent(self, query, ctx, stream=False):
                if stream:
                    async def event_generator():
                        async for event in my_framework.stream_chat(query, ctx):
                            # Yield the RAW event from your framework
                            # DO NOT convert it here - that happens in process_streaming_event()
                            yield event
                    return event_generator()
                    
        Note:
            - The framework events you yield can be in ANY format your framework uses
            - They will be converted to unified format by process_streaming_event()
            - This separation keeps framework-specific logic isolated
        """
        raise NotImplementedError

    # ----- Optional hooks (can be overridden) -----
    def get_mcp_server_params(self) -> Optional[Dict[str, Any]]:
        """
        Return MCP server configuration if MCP tools are needed.
        
        Returns:
            Dictionary with MCP server parameters, or None if MCP is not used.
        """
        return None

    async def process_streaming_event(self, event: Any) -> Optional[Dict[str, Any]]:
        """
        Convert framework-specific streaming events to unified format.
        
        This method is called by handle_message_stream() for each event yielded
        by run_agent(stream=True). It converts your framework's event format
        into the standard unified format used by the framework.
        
        Args:
            event: RAW framework-specific streaming event (any type your framework uses)
            
        Returns:
            Dictionary in unified format, or None to skip this event.
            
            Unified format structure:
            {
                "type": "chunk" | "tool_call" | "tool_result" | "activity" | "error",
                "content": str,
                "metadata": {...}  # Optional additional data
            }
            
        Event Types:
            - "chunk": Text content being streamed to the user
            - "tool_call": Agent is calling a tool
            - "tool_result": Result from a tool execution
            - "activity": General activity message (e.g., "thinking", "processing")
            - "error": Error occurred during processing
            
        Examples:
            # Example 1: LlamaIndex text chunk
            async def process_streaming_event(self, event):
                if hasattr(event, 'delta') and event.delta:
                    return {
                        "type": "chunk",
                        "content": event.delta,
                        "metadata": {"source": "llamaindex"}
                    }
                return None
                
            # Example 2: Custom framework tool call
            async def process_streaming_event(self, event):
                if event.type == "tool_request":
                    return {
                        "type": "tool_call",
                        "content": "",
                        "metadata": {
                            "tool_name": event.tool_name,
                            "tool_arguments": event.arguments,
                            "call_id": event.id
                        }
                    }
                return None
                
            # Example 3: OpenAI-style streaming chunk
            async def process_streaming_event(self, event):
                if event.choices and event.choices[0].delta.content:
                    return {
                        "type": "chunk",
                        "content": event.choices[0].delta.content,
                        "metadata": {"model": event.model}
                    }
                return None
                
            # Example 4: Tool result
            async def process_streaming_event(self, event):
                if event.type == "tool_response":
                    return {
                        "type": "tool_result",
                        "content": str(event.result),
                        "metadata": {
                            "tool_name": event.tool_name,
                            "call_id": event.call_id,
                            "is_error": event.is_error
                        }
                    }
                return None
                
            # Example 5: Multiple event types
            async def process_streaming_event(self, event):
                # Handle different event types from your framework
                if isinstance(event, MyFrameworkTextChunk):
                    return {
                        "type": "chunk",
                        "content": event.text,
                        "metadata": {}
                    }
                elif isinstance(event, MyFrameworkToolCall):
                    return {
                        "type": "tool_call",
                        "content": "",
                        "metadata": {
                            "tool_name": event.name,
                            "tool_arguments": event.args,
                            "call_id": event.id
                        }
                    }
                # Skip unknown events
                return None
                
        Note:
            - Return None to skip events you don't want to process
            - The default implementation returns None (skips all events)
            - Override this method to handle your framework's specific event types
            - This method is called automatically by handle_message_stream()
        """
        return None

    def get_model_config(self) -> Dict[str, Any]:
        """
        Return default model configuration.
        
        Returns:
            Dictionary with model configuration parameters (temperature, max_tokens, etc.)
        """
        return {}

    # ----- Internal helpers -----
    def _resolve_model_name(self) -> str:
        """Resolve the model name from session config, environment, or default."""
        # Priority: session model > OPENAI_API_MODEL env var > DEFAULT_MODEL from config
        candidate = self._session_model_name or os.getenv("OPENAI_API_MODEL") or model_config.default_model
        if not candidate:
            # Final fallback if nothing is configured
            return "gpt-4o-mini"
        return candidate

    def _ensure_agent_built(self):
        """Ensure agent is built (synchronous check)."""
        if not self._agent_built:
            # Synchronous wrapper calling async build in a lazy fashion is not ideal;
            # but AgentManager invokes configure_session before first use. We'll rely on build being awaited there.
            # For safety, we expose an async ensure in configure_session.
            pass

    async def _async_ensure_agent_built(self):
        """Ensure agent is built (asynchronous)."""
        if not self._agent_built:
            tools = self.get_agent_tools()
            # Get the combined system prompt (with rich content if enabled)
            system_prompt = await self.get_system_prompt()
            await self.initialize_agent(
                self._resolve_model_name(),
                system_prompt,
                tools
            )
            self._agent_built = True

    # ----- AgentInterface -----
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """Configure the agent with session-level settings."""
        logger.info(f"BaseAgent: Configuring session: {session_configuration}")
        
        # Handle rich content configuration
        if "enable_rich_content" in session_configuration:
            value = session_configuration["enable_rich_content"]
            if not isinstance(value, bool):
                logger.warning(f"Invalid enable_rich_content value: {value}, defaulting to True")
                self._enable_rich_content = True
            else:
                self._enable_rich_content = value
            logger.info(f"Rich content capabilities: {'enabled' if self._enable_rich_content else 'disabled'}")
        
        if "system_prompt" in session_configuration:
            self._session_system_prompt = session_configuration["system_prompt"]
        if "model_config" in session_configuration:
            self._session_model_config = session_configuration["model_config"]
        if "model_name" in session_configuration:
            self._session_model_name = session_configuration["model_name"]

        # Rebuild agent with new params
        self._agent_built = False
        await self._async_ensure_agent_built()

    async def get_system_prompt(self) -> Optional[str]:
        """
        Return the current system prompt with rich content capabilities.
        
        If rich content is enabled (default), automatically combines the agent's
        custom prompt with rich content instructions for Mermaid, Chart.js, forms, etc.
        
        Returns:
            Combined system prompt with rich content capabilities, or base prompt if disabled
        """
        base_prompt = self._session_system_prompt or ""
        
        if not base_prompt:
            logger.warning("Agent has no base prompt defined")
            if self._enable_rich_content:
                # Import here to avoid circular dependencies
                try:
                    from .rich_content_prompt import RICH_CONTENT_INSTRUCTIONS
                    return RICH_CONTENT_INSTRUCTIONS
                except ImportError as e:
                    logger.error(f"Failed to import rich_content_prompt: {e}")
                    logger.warning("Rich content capabilities unavailable, using empty prompt")
                    return ""
            return ""
        
        if not self._enable_rich_content:
            logger.debug("Rich content disabled, returning base prompt only")
            return base_prompt
        
        # Import here to avoid circular dependencies
        try:
            from .rich_content_prompt import combine_prompts
            combined = combine_prompts(base_prompt)
            logger.debug(f"Combined prompt length: {len(combined)} chars (base: {len(base_prompt)}, rich: {len(combined) - len(base_prompt)})")
            return combined
        except ImportError as e:
            logger.error(f"Failed to import rich_content_prompt: {e}")
            logger.warning("Rich content capabilities unavailable, using base prompt only")
            return base_prompt

    async def get_current_model(self, session_id: str) -> Optional[str]:
        """Return the current model name."""
        return self._resolve_model_name()

    async def get_metadata(self) -> Dict[str, Any]:
        """Return agent metadata."""
        tools = self.get_agent_tools()
        tool_list = [
            {
                "name": getattr(t, "__name__", str(t)),
                "description": getattr(t, "__doc__", "Agent tool"),
                "type": "static",
            }
            for t in tools
        ]
        return {
            "name": "Base Agent",
            "description": "Framework-agnostic agent with streaming and tool support.",
            "capabilities": {
                "streaming": True,
                "tool_use": True,
                "reasoning": True,
                "multimodal": False,
            },
            "defaultInputModes": ["text"],
            "defaultOutputModes": ["text", "structured"],
            "tools": tool_list,
            "tool_summary": {
                "total_tools": len(tools),
                "static_tools": len(tools),
            },
            "framework": "Generic",
        }

    def _build_full_query(self, agent_input: StructuredAgentInput) -> str:
        """Build full query with clear separation between user query and file content."""
        parts_text = []
        
        # Add text from all TextInputPart (file content)
        for part in agent_input.parts:
            if isinstance(part, TextInputPart):
                parts_text.append(part.text)
        
        # Debug logging
        logger.info(f"[_build_full_query] Found {len(parts_text)} TextInputPart(s) in agent_input with {len(agent_input.parts)} total parts")
        if parts_text:
            for i, text in enumerate(parts_text):
                logger.info(f"[_build_full_query] Part {i+1} length: {len(text)} chars, preview: {text[:200]}...")
        
        # Build message with clear structure
        if parts_text:
            # User query first, then file content clearly separated
            full_message = f"User Query: {agent_input.query}\n\n"
            full_message += "Attached Files Content:\n"
            full_message += "\n\n".join(parts_text)
            logger.info(f"[_build_full_query] Final message length: {len(full_message)} chars")
            return full_message
        
        return agent_input.query

    async def handle_message(self, session_id: str, agent_input: StructuredAgentInput) -> StructuredAgentOutput:
        """Handle a user message in non-streaming mode."""
        if not agent_input.query:
            return StructuredAgentOutput(response_text="Input query cannot be empty.", parts=[])

        await self._async_ensure_agent_built()

        # Context reuse
        ctx = self._state_ctx or self.create_fresh_context()

        # Build full query including file content from parts
        full_query = self._build_full_query(agent_input)

        # Use run_agent in non-streaming mode
        final_response = await self.run_agent(full_query, ctx, stream=False)
        response_text = str(final_response)

        # Save context for future
        self._state_ctx = ctx

        cleaned, parts = parse_special_blocks_from_text(response_text)
        return StructuredAgentOutput(response_text=cleaned, parts=[TextOutputPart(text=cleaned), *parts])

    async def handle_message_stream(
        self, session_id: str, agent_input: StructuredAgentInput
    ) -> AsyncGenerator[StructuredAgentOutput, None]:
        """
        Handle a user message in streaming mode.
        
        ⚠️  FINAL METHOD - DO NOT OVERRIDE IN SUBCLASSES ⚠️
        
        This method orchestrates the streaming flow and should NOT be overridden.
        Instead, implement run_agent() and process_streaming_event() in your subclass.
        
        ORCHESTRATION FLOW:
        ===================
        
        1. Calls run_agent(stream=True) to get framework-specific events
        2. For each event from run_agent():
           - Calls process_streaming_event() to convert to unified format
           - Converts unified format to StructuredAgentOutput
           - Yields the output to the client
        3. Handles final response assembly and special block parsing
        
        EVENT FLOW DIAGRAM:
        
        Your Framework          BaseAgent (This Method)         Client
        ───────────────         ───────────────────────         ──────
              │                          │                         │
              │  run_agent(stream=True)  │                         │
              │◄─────────────────────────│                         │
              │                          │                         │
              │  yield raw_event_1       │                         │
              ├─────────────────────────►│                         │
              │                          │                         │
              │                          │ process_streaming_event()│
              │                          │ (converts to unified)   │
              │                          │                         │
              │                          │  StructuredAgentOutput  │
              │                          ├────────────────────────►│
              │                          │                         │
              │  yield raw_event_2       │                         │
              ├─────────────────────────►│                         │
              │                          │                         │
              │                          │ process_streaming_event()│
              │                          │                         │
              │                          │  StructuredAgentOutput  │
              │                          ├────────────────────────►│
              │                          │                         │
              
        WHY THIS IS FINAL:
        ==================
        
        This method contains framework-agnostic orchestration logic that:
        - Manages the streaming lifecycle
        - Handles event conversion consistently
        - Ensures proper output formatting
        - Manages context state
        - Parses special blocks (charts, forms, etc.)
        
        By keeping this final, we ensure:
        - Consistent behavior across all agent implementations
        - Separation of concerns (framework logic vs orchestration)
        - Easier maintenance and debugging
        - Clear extension points (run_agent and process_streaming_event)
        
        WHAT TO IMPLEMENT INSTEAD:
        ===========================
        
        1. run_agent(stream=True) - Yield RAW framework events
           Example:
           async def run_agent(self, query, ctx, stream=True):
               async for event in my_framework.stream(query):
                   yield event  # Yield RAW events
                   
        2. process_streaming_event() - Convert events to unified format
           Example:
           async def process_streaming_event(self, event):
               if event.type == "text":
                   return {"type": "chunk", "content": event.text, "metadata": {}}
               return None
               
        Args:
            session_id: The session identifier
            agent_input: Structured input containing query and optional file content
            
        Yields:
            StructuredAgentOutput: Streaming outputs with text chunks, activities, and final response
            
        Note:
            This method is marked as FINAL to maintain consistent streaming behavior.
            Do not override this method. Implement run_agent() and process_streaming_event() instead.
        """
        if not agent_input.query:
            yield StructuredAgentOutput(response_text="Input query cannot be empty.", parts=[])
            return

        await self._async_ensure_agent_built()

        ctx = self._state_ctx or self.create_fresh_context()
        
        # Build full query including file content from parts
        full_query = self._build_full_query(agent_input)
        
        # Use run_agent in streaming mode
        stream_generator = await self.run_agent(full_query, ctx, stream=True)

        agent_loop_started_emitted = False
        final_text_parts = []

        async for event in stream_generator:
            # Process event through subclass-specific handler
            processed_event = await self.process_streaming_event(event)
            
            if processed_event is None:
                continue
                
            event_type = processed_event.get("type")
            
            # Handle different event types
            if event_type == "chunk":
                chunk = processed_event.get("content", "")
                if chunk:
                    final_text_parts.append(chunk)
                    yield StructuredAgentOutput(
                        response_text="",
                        parts=[TextOutputStreamPart(text=f"__STREAM_CHUNK__{chunk}")],
                    )
                    
            elif event_type == "tool_call":
                tool_request = {
                    "type": "tool_request",
                    "source": processed_event.get("metadata", {}).get("source", "agent"),
                    "tools": [
                        {
                            "name": processed_event.get("metadata", {}).get("tool_name", "unknown"),
                            "arguments": processed_event.get("metadata", {}).get("tool_arguments", {}),
                            "id": processed_event.get("metadata", {}).get("call_id", "unknown"),
                        }
                    ],
                    "timestamp": str(datetime.now()),
                }
                yield StructuredAgentOutput(
                    response_text="",
                    parts=[TextOutputStreamPart(text=f"__STREAM_ACTIVITY__{json.dumps(tool_request)}")],
                )
                agent_loop_started_emitted = False
                
            elif event_type == "tool_result":
                tool_result = {
                    "type": "tool_result",
                    "source": processed_event.get("metadata", {}).get("source", "agent"),
                    "results": [
                        {
                            "name": processed_event.get("metadata", {}).get("tool_name", "unknown"),
                            "content": processed_event.get("content", ""),
                            "is_error": processed_event.get("metadata", {}).get("is_error", False),
                            "call_id": processed_event.get("metadata", {}).get("call_id", "unknown"),
                        }
                    ],
                    "timestamp": str(datetime.now()),
                }
                yield StructuredAgentOutput(
                    response_text="",
                    parts=[TextOutputStreamPart(text=f"__STREAM_ACTIVITY__{json.dumps(tool_result)}")],
                )
                
            elif event_type == "activity":
                if not agent_loop_started_emitted:
                    loop_activity = {
                        "type": "message",
                        "source": "agent",
                        "content": processed_event.get("content", "Agent loop started"),
                        "timestamp": str(datetime.now()),
                    }
                    yield StructuredAgentOutput(
                        response_text="",
                        parts=[TextOutputStreamPart(text=f"__STREAM_ACTIVITY__{json.dumps(loop_activity)}")],
                    )
                    agent_loop_started_emitted = True
                    
            elif event_type == "error":
                error_activity = {
                    "type": "error",
                    "content": processed_event.get("content", "Unknown error"),
                    "timestamp": str(datetime.now()),
                }
                yield StructuredAgentOutput(
                    response_text="",
                    parts=[TextOutputStreamPart(text=f"__STREAM_ACTIVITY__{json.dumps(error_activity)}")],
                )

        # Final result
        self._state_ctx = ctx
        final_text = "".join(final_text_parts)
        cleaned, parts = parse_special_blocks_from_text(final_text)
        yield StructuredAgentOutput(
            response_text=cleaned,
            parts=[TextOutputPart(text=cleaned), *parts],
        )

    async def get_state(self) -> Dict[str, Any]:
        """Get the current agent state."""
        if self._state_ctx is None:
            return {}
        try:
            return self.serialize_context(self._state_ctx)
        finally:
            # One-time retrieval pattern to keep consistent with existing examples
            self._state_ctx = None

    async def load_state(self, state: Dict[str, Any]):
        """Load agent state from a dictionary."""
        # Ensure the concrete agent exists before creating or deserializing context
        await self._async_ensure_agent_built()
        if state:
            try:
                self._state_ctx = self.deserialize_context(state)
            except Exception as e:
                logger.error(f"Failed to load context state: {e}. Starting fresh.")
                self._state_ctx = self.create_fresh_context()
        else:
            self._state_ctx = self.create_fresh_context()
