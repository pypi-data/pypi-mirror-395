"""
Microsoft Agent Framework-Based Agent Implementation

This implementation provides Microsoft Agent Framework-specific functionality:
- Session/config handling
- State management via Microsoft Agent Framework context (serialize/deserialize)
- Non-streaming and streaming message processing
- Streaming event formatting aligned with modern UI expectations

Reference: https://github.com/microsoft/agent-framework

Note: This implementation constructs a concrete Microsoft Agent Framework agent.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, List, AsyncGenerator, Union
import json
from datetime import datetime
import logging

from ..core.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class MicrosoftAgent(BaseAgent):
    """
    Concrete implementation of BaseAgent for Microsoft Agent Framework.
    
    This agent uses:
    - Microsoft Agent Framework's agent system for orchestration
    - Context management for conversation tracking
    - Streaming support for real-time responses
    """

    def __init__(self):
        # Microsoft Agent Framework-specific runtime
        self._agent_instance: Optional[Any] = None
        self._context_store: Dict[str, Any] = {}
        super().__init__()

    # ----- Required abstract method implementations -----
    
    def get_agent_prompt(self) -> str:
        """Return the default system prompt for the Microsoft agent."""
        return """You are a helpful AI assistant. You have access to various tools to help answer questions.
Use the tools when necessary to provide accurate and helpful responses."""

    def get_agent_tools(self) -> List[callable]:
        """Return the list of tools available to the agent."""
        # Default empty list - subclasses should override to provide actual tools
        return []

    async def initialize_agent(
        self,
        model_name: str,
        system_prompt: str,
        tools: List[callable],
        **kwargs
    ) -> None:
        """
        Initialize the Microsoft Agent Framework agent.
        
        Args:
            model_name: The LLM model to use (e.g., "gpt-4o-mini")
            system_prompt: The system prompt for the agent
            tools: List of tools available to the agent
            **kwargs: Additional configuration options
        """
        try:
            # Import Microsoft Agent Framework components
            # Note: These imports are based on the expected structure from
            # https://github.com/microsoft/agent-framework
            # Actual imports may need adjustment based on the final API
            from azure.ai.agent import Agent, AgentConfig
            from azure.ai.agent.models import ChatCompletionModel
        except ImportError as e:
            raise RuntimeError(
                f"Failed to initialize MicrosoftAgent: {e}. "
                f"Install the required framework with: uv add agent-framework[microsoft]"
            )

        # Create agent configuration
        config = AgentConfig(
            name="microsoft_agent",
            description="Agent powered by Microsoft Agent Framework",
            instructions=system_prompt,
            model=model_name,
            temperature=0.7,
        )

        # Convert tools to Microsoft Agent Framework format
        microsoft_tools = []
        for t in tools:
            # Wrap tools in Microsoft Agent Framework format
            tool_name = getattr(t, '__name__', 'custom_tool')
            tool_desc = getattr(t, '__doc__', 'A custom tool')
            
            # Create tool wrapper
            # Note: Actual tool wrapping depends on Microsoft Agent Framework API
            microsoft_tools.append({
                'name': tool_name,
                'description': tool_desc,
                'function': t,
            })

        # Create the agent instance
        self._agent_instance = Agent(
            config=config,
            tools=microsoft_tools,
        )

        logger.info(f"MicrosoftAgent initialized with model {model_name} and {len(microsoft_tools)} tools")

    def create_fresh_context(self) -> Any:
        """
        Create a new empty context for the Microsoft Agent Framework.
        
        Returns:
            A new context dictionary for conversation tracking
        """
        return {
            "messages": [],
            "metadata": {
                "created_at": str(datetime.now()),
                "framework": "microsoft",
            }
        }

    def serialize_context(self, ctx: Any) -> Dict[str, Any]:
        """
        Serialize Microsoft Agent Framework context to dictionary for persistence.
        
        Args:
            ctx: Context object (dictionary with messages and metadata)
            
        Returns:
            Dictionary with serialized context
        """
        try:
            return {
                "messages": ctx.get("messages", []),
                "metadata": ctx.get("metadata", {}),
                "framework": "microsoft",
                "_agent_identity": {
                    "agent_type": "MicrosoftAgent",
                    "timestamp": str(datetime.now()),
                }
            }
        except Exception as e:
            logger.error(f"Context serialization failed: {e}")
            return {"messages": [], "error": str(e)}

    def deserialize_context(self, state: Dict[str, Any]) -> Any:
        """
        Deserialize dictionary to Microsoft Agent Framework context object.
        
        Args:
            state: Dictionary with serialized context
            
        Returns:
            Restored context object
        """
        try:
            return {
                "messages": state.get("messages", []),
                "metadata": state.get("metadata", {
                    "created_at": str(datetime.now()),
                    "framework": "microsoft",
                }),
            }
        except Exception as e:
            logger.error(f"Context deserialization failed: {e}. Starting fresh.")
            return self.create_fresh_context()

    async def run_agent(
        self,
        query: str,
        ctx: Any,
        stream: bool = False
    ) -> Union[str, AsyncGenerator]:
        """
        Execute the Microsoft Agent Framework agent with a query.
        
        Args:
            query: The user query to process
            ctx: The context object for conversation history
            stream: Whether to return streaming results
            
        Returns:
            If stream=False: Returns the final response as a string
            If stream=True: Returns an AsyncGenerator that yields streaming events
        """
        if not self._agent_instance:
            raise RuntimeError("Agent not initialized. Call initialize_agent first.")
        
        # Add user message to context
        ctx["messages"].append({
            "role": "user",
            "content": query,
            "timestamp": str(datetime.now()),
        })
        
        if stream:
            return self._stream_agent_response(query, ctx)
        else:
            # Non-streaming execution
            try:
                # Execute agent with context
                response = await self._agent_instance.run(
                    message=query,
                    context=ctx.get("messages", []),
                )
                
                # Add assistant response to context
                response_text = str(response)
                ctx["messages"].append({
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": str(datetime.now()),
                })
                
                return response_text
            except Exception as e:
                logger.error(f"Agent execution failed: {e}")
                return f"Error executing agent: {e}"

    async def _stream_agent_response(self, query: str, ctx: Any) -> AsyncGenerator:
        """
        Stream agent response using Microsoft Agent Framework's streaming API.
        
        Args:
            query: The user query
            ctx: Context object with conversation history
            
        Yields:
            Microsoft Agent Framework streaming events
        """
        try:
            # Stream events from Microsoft Agent Framework
            async for event in self._agent_instance.stream(
                message=query,
                context=ctx.get("messages", []),
            ):
                yield event
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            # Yield error event
            yield {
                "type": "error",
                "content": str(e),
                "timestamp": str(datetime.now()),
            }

    async def process_streaming_event(self, event: Any) -> Optional[Dict[str, Any]]:
        """
        Convert Microsoft Agent Framework streaming events to unified format.
        
        Args:
            event: Microsoft Agent Framework streaming event
            
        Returns:
            Dictionary in unified format, or None if event should be skipped.
        """
        try:
            # Handle different event types from Microsoft Agent Framework
            # Note: Event structure based on expected Microsoft Agent Framework API
            
            if isinstance(event, dict):
                event_type = event.get("type", "")
                
                # Handle text chunks
                if event_type == "content_delta" or event_type == "chunk":
                    content = event.get("content", "") or event.get("delta", "")
                    if content:
                        return {
                            "type": "chunk",
                            "content": content,
                            "metadata": {
                                "source": "microsoft_agent",
                                "timestamp": str(datetime.now()),
                            }
                        }
                    return None
                
                # Handle tool calls
                if event_type == "tool_call_start" or event_type == "tool_call":
                    tool_name = event.get("tool_name", "unknown_tool")
                    tool_args = event.get("arguments", {}) or event.get("tool_arguments", {})
                    call_id = event.get("call_id", "") or event.get("id", "unknown")
                    
                    return {
                        "type": "tool_call",
                        "content": "",
                        "metadata": {
                            "source": "microsoft_agent",
                            "tool_name": tool_name,
                            "tool_arguments": tool_args,
                            "call_id": call_id,
                            "timestamp": str(datetime.now()),
                        }
                    }
                
                # Handle tool results
                if event_type == "tool_call_end" or event_type == "tool_result":
                    tool_name = event.get("tool_name", "unknown_tool")
                    tool_output = event.get("output", "") or event.get("result", "")
                    call_id = event.get("call_id", "") or event.get("id", "unknown")
                    is_error = event.get("error", False) or event.get("is_error", False)
                    
                    return {
                        "type": "tool_result",
                        "content": str(tool_output),
                        "metadata": {
                            "source": "microsoft_agent",
                            "tool_name": tool_name,
                            "call_id": call_id,
                            "is_error": is_error,
                            "timestamp": str(datetime.now()),
                        }
                    }
                
                # Handle agent start
                if event_type == "agent_start" or event_type == "run_start":
                    return {
                        "type": "activity",
                        "content": "Agent loop started",
                        "metadata": {
                            "source": "microsoft_agent",
                            "timestamp": str(datetime.now()),
                        }
                    }
                
                # Handle errors
                if event_type == "error":
                    return {
                        "type": "error",
                        "content": event.get("message", "Unknown error"),
                        "metadata": {
                            "source": "microsoft_agent",
                            "timestamp": str(datetime.now()),
                        }
                    }
                
                # Suppress lifecycle events
                if event_type in {"agent_end", "run_end", "step_start", "step_end"}:
                    return None
            
            # Handle string events (simple text chunks)
            elif isinstance(event, str):
                if event:
                    return {
                        "type": "chunk",
                        "content": event,
                        "metadata": {
                            "source": "microsoft_agent",
                            "timestamp": str(datetime.now()),
                        }
                    }
            
            # Log unknown events for debugging
            logger.debug(f"Unknown Microsoft Agent Framework event: {type(event)}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to process streaming event: {e}")
            return {
                "type": "error",
                "content": f"Failed to process event: {e}",
                "metadata": {
                    "timestamp": str(datetime.now()),
                }
            }

    async def get_metadata(self) -> Dict[str, Any]:
        """Return Microsoft Agent Framework-specific agent metadata."""
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
            "name": "Microsoft Agent",
            "description": "Agent powered by Microsoft Agent Framework with streaming and tool support.",
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
            "framework": "Microsoft Agent Framework",
        }
