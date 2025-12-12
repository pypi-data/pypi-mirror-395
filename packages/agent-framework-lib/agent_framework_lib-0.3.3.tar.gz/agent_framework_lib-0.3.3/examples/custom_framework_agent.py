"""
Custom Framework Agent Example

This example demonstrates how to create an agent using BaseAgent with a custom AI framework.
This is useful when you want to integrate a framework not natively supported by the library
(e.g., LangChain, Haystack, custom implementations, etc.).

Features demonstrated:
- Direct BaseAgent implementation without framework dependencies
- Custom agent initialization and execution
- Manual context/state management
- Tool integration with custom frameworks
- Streaming support with custom event handling

This example uses a simple custom implementation for demonstration,
but the same pattern works with any AI framework.

Usage:
    python custom_framework_agent.py

The agent will start a web server on http://localhost:8103

Requirements: uv add agent-framework
"""
import asyncio
import os
from typing import List, Any, Dict, AsyncGenerator, Union
import logging

from agent_framework.core.base_agent import BaseAgent
from agent_framework.core.agent_interface import StructuredAgentInput

logger = logging.getLogger(__name__)


class CustomFrameworkAgent(BaseAgent):
    """
    Example agent using BaseAgent with a custom AI framework.
    
    *** COMPLETE INTEGRATION EXAMPLE ***
    
    This demonstrates how to integrate ANY AI framework with the Agent Framework:
    - LangChain
    - Haystack  
    - Microsoft Agent Framework
    - Custom implementations
    - Any other framework
    
    *** FEATURES DEMONSTRATED ***
    
    ✅ Complete tool execution loop with multiple iterations
    ✅ Streaming mode with real-time event updates
    ✅ Non-streaming mode for simple queries
    ✅ Event conversion to unified format
    ✅ Context management and persistence
    ✅ Session configuration
    ✅ Comprehensive comments at every integration point
    
    *** STREAMING VS NON-STREAMING ***
    
    This example demonstrates BOTH modes:
    
    Non-Streaming (_run_non_streaming):
    - Returns complete response as string
    - Simpler implementation
    - Better for batch processing
    - Example: "The answer is 42"
    
    Streaming (_run_streaming):
    - Returns AsyncGenerator yielding events
    - Real-time feedback to user
    - Better UX for long responses
    - Example: Yields chunks as they arrive
    
    The run_agent() method routes to the appropriate mode based on
    the stream parameter.
    
    *** KEY METHODS TO IMPLEMENT ***
    
    Required:
    - get_agent_prompt(): Return system prompt
    - get_agent_tools(): Return list of callable tools
    - initialize_agent(): Set up your framework's agent
    - create_fresh_context(): Create new conversation context
    - serialize_context(): Save context to dict
    - deserialize_context(): Load context from dict
    - run_agent(): Execute agent with query (streaming or non-streaming)
    
    Optional:
    - process_streaming_event(): Convert framework events to unified format
    - configure_session(): Capture session context
    
    *** INTEGRATION POINTS ***
    
    Each method has detailed comments explaining:
    - WHY: Why this method is needed
    - WHAT: What it does
    - HOW: How to implement it
    - EXAMPLES: Examples for different frameworks
    
    Read the comments in each method to understand the integration!
    """
    
    def __init__(self):
        super().__init__()
        # Define unique agent ID (required for session isolation)
        self.agent_id = "custom_framework_agent_v1"
        
        # Your custom framework's agent instance
        self._custom_agent = None
        
        # Store session context
        self.current_user_id = "default_user"
        self.current_session_id = None
    
    async def configure_session(self, session_configuration: Dict[str, Any]) -> None:
        """Capture session context for use in tools."""
        self.current_user_id = session_configuration.get('user_id', 'default_user')
        self.current_session_id = session_configuration.get('session_id')
        await super().configure_session(session_configuration)
    
    # ===== REQUIRED: Agent Configuration =====
    
    def get_agent_prompt(self) -> str:
        """
        Define the agent's system prompt.
        
        *** CRITICAL INTEGRATION POINT ***
        
        WHY: The system prompt defines the agent's behavior, personality,
             and capabilities. It's the foundation of how your agent acts.
        
        WHAT: Returns a string that will be used as the system prompt
              for your agent.
        
        HOW: Return a string describing what the agent should do.
             This is passed to initialize_agent() as system_prompt.
        
        *** TIPS FOR GOOD PROMPTS ***
        
        1. Be specific about the agent's role
        2. List available capabilities
        3. Provide guidelines for behavior
        4. Include examples if helpful
        5. Mention tools if applicable
        
        *** EXAMPLES ***
        
        # Simple assistant:
        return "You are a helpful assistant."
        
        # Specialized agent:
        return '''You are a Python coding expert.
        You help users write clean, efficient Python code.
        Always explain your reasoning and provide examples.'''
        
        # Agent with tools:
        return '''You are a research assistant with web search capabilities.
        Use the search tool to find current information.
        Always cite your sources.'''
        
        *** DYNAMIC PROMPTS ***
        
        You can make this dynamic based on configuration:
        
        def get_agent_prompt(self) -> str:
            base = "You are a helpful assistant."
            if self.config.get("expert_mode"):
                base += " Provide detailed technical explanations."
            return base
        """
        # ===== Define system prompt =====
        # WHY: Tells the LLM what role to play and how to behave
        # WHAT: String describing agent's purpose and capabilities
        # HOW: Return multi-line string with clear instructions
        return """You are a helpful assistant with calculator capabilities.
You can perform basic math operations using the provided tools.
Always use tools when asked to perform calculations."""
    
    def get_agent_tools(self) -> List[callable]:
        """
        Define the tools available to the agent.
        
        *** CRITICAL INTEGRATION POINT ***
        
        WHY: Tools extend your agent's capabilities beyond just text.
             They allow the agent to perform actions, fetch data, etc.
        
        WHAT: Returns a list of Python functions that the agent can call.
              Each function becomes a tool the LLM can use.
        
        HOW: Define functions with clear docstrings and type hints.
             Return them in a list.
        
        *** TOOL REQUIREMENTS ***
        
        Each tool function MUST have:
        1. Clear function name (becomes tool name)
        2. Docstring (becomes tool description for LLM)
        3. Type hints (helps LLM understand parameters)
        4. Return value (sent back to LLM)
        
        *** EXAMPLES ***
        
        # Simple tool:
        def get_weather(city: str) -> str:
            '''Get current weather for a city.'''
            return f"Weather in {city}: Sunny, 72°F"
        
        # Tool with multiple parameters:
        def search_database(query: str, limit: int = 10) -> List[str]:
            '''Search database and return results.'''
            return ["result1", "result2"]
        
        # Tool that calls external API:
        async def fetch_data(url: str) -> dict:
            '''Fetch data from URL.'''
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.json()
        
        *** TOOL BEST PRACTICES ***
        
        1. Keep tools focused (one thing per tool)
        2. Use descriptive names (search_web, not search)
        3. Write clear docstrings (LLM reads these!)
        4. Handle errors gracefully (return error messages)
        5. Use type hints (helps LLM understand parameters)
        6. Return serializable data (str, int, dict, list)
        
        *** ACCESSING SESSION CONTEXT ***
        
        Tools can access session context via self:
        
        def get_user_data() -> dict:
            '''Get current user's data.'''
            user_id = self.current_user_id
            return {"user_id": user_id, "name": "John"}
        
        Returns:
            List of callable functions (tools)
        """
        # ===== Define tool functions =====
        # WHY: Extend agent capabilities beyond text generation
        # WHAT: Python functions the LLM can call
        # HOW: Define functions with docstrings and type hints
        
        def add(a: float, b: float) -> float:
            """
            Add two numbers together.
            
            Args:
                a: First number
                b: Second number
                
            Returns:
                Sum of a and b
            """
            return a + b
        
        def multiply(a: float, b: float) -> float:
            """
            Multiply two numbers together.
            
            Args:
                a: First number
                b: Second number
                
            Returns:
                Product of a and b
            """
            return a * b
        
        def divide(a: float, b: float) -> float:
            """
            Divide first number by second number.
            
            Args:
                a: Numerator
                b: Denominator
                
            Returns:
                Result of a divided by b, or error message if b is zero
            """
            # ===== Handle edge cases =====
            # WHY: Prevent crashes from invalid input
            # WHAT: Check for division by zero
            # HOW: Return error message instead of raising exception
            if b == 0:
                return "Error: Division by zero"
            return a / b
        
        # ===== Return list of tools =====
        # WHY: Framework needs all tools in a list
        # WHAT: List of function objects
        # HOW: Return list containing all tool functions
        return [add, multiply, divide]
    
    # ===== REQUIRED: Agent Initialization =====
    
    async def initialize_agent(
        self,
        model_name: str,
        system_prompt: str,
        tools: List[callable],
        **kwargs
    ) -> None:
        """
        Initialize your custom framework's agent.
        
        *** CRITICAL INTEGRATION POINT ***
        
        WHY: Your framework needs to be set up before it can process queries.
             This is called once when the agent is first created.
        
        WHAT: Sets up your framework's agent instance with the model,
              system prompt, and tools.
        
        HOW: Initialize your framework's agent however it requires.
             Store any necessary state in instance variables.
        
        *** EXAMPLES FOR DIFFERENT FRAMEWORKS ***
        
        # LangChain:
        from langchain.agents import create_openai_functions_agent
        from langchain.chat_models import ChatOpenAI
        from langchain.tools import Tool
        
        llm = ChatOpenAI(model=model_name)
        langchain_tools = [
            Tool(name=t.__name__, func=t, description=t.__doc__)
            for t in tools
        ]
        self._agent = create_openai_functions_agent(
            llm=llm,
            tools=langchain_tools,
            prompt=system_prompt
        )
        
        # Haystack:
        from haystack.agents import Agent
        from haystack.components.generators import OpenAIGenerator
        
        generator = OpenAIGenerator(model=model_name)
        self._agent = Agent(
            generator=generator,
            tools=tools,
            system_prompt=system_prompt
        )
        
        # Microsoft Agent Framework:
        from autogen import AssistantAgent
        
        self._agent = AssistantAgent(
            name="assistant",
            llm_config={"model": model_name},
            system_message=system_prompt
        )
        
        # Custom implementation:
        self._agent = MyCustomAgent(
            model=model_name,
            prompt=system_prompt,
            tools=tools
        )
        
        *** IMPORTANT ***
        
        - This method is async, so you can do async initialization
        - Store your agent instance in self._custom_agent or similar
        - The framework provides a client_factory for OpenAI/Anthropic/Gemini
        - You can access additional config via **kwargs
        
        Args:
            model_name: Name of the LLM model to use (e.g., "gpt-4o-mini")
            system_prompt: System prompt for the agent
            tools: List of callable tools (Python functions)
            **kwargs: Additional configuration options
        """
        logger.info(f"Initializing custom agent with model: {model_name}")
        
        # ===== STEP 1: Get LLM client =====
        # WHY: Need to communicate with LLM provider (OpenAI, Anthropic, etc.)
        # WHAT: Create client using the framework's factory
        # HOW: Use client_factory which handles all providers automatically
        
        # The framework provides a client_factory that automatically
        # handles OpenAI, Anthropic, and Gemini based on the model name.
        # You can use this or create your own client.
        from agent_framework.core.model_clients import client_factory
        
        self._llm_client = client_factory.create_client(model_name=model_name)
        logger.info(f"Created LLM client for model: {model_name}")
        
        # ===== STEP 2: Store configuration =====
        # WHY: Need to access these values in run_agent()
        # WHAT: Save system prompt and tools to instance variables
        # HOW: Store in self._* attributes
        
        self._system_prompt = system_prompt
        
        # Convert tools list to dict for easy lookup by name
        # WHY: When LLM requests a tool by name, we need fast lookup
        # WHAT: Create dict mapping tool name to function
        # HOW: Use dict comprehension with __name__ as key
        self._tools = {tool.__name__: tool for tool in tools}
        
        # Build tool descriptions for the LLM
        # WHY: LLM needs to know what tools are available
        # WHAT: Create formatted string describing each tool
        # HOW: Call helper method to build descriptions
        self._tool_descriptions = self._build_tool_descriptions(tools)
        
        logger.info(f"Custom agent initialized with {len(tools)} tools: {list(self._tools.keys())}")
        
        # ===== STEP 3: Initialize your framework (if needed) =====
        # WHY: Some frameworks need additional setup
        # WHAT: Create your framework's agent instance
        # HOW: Call your framework's initialization code
        
        # For this example, we're using direct LLM calls, so no additional
        # framework initialization is needed. But if you were using LangChain,
        # Haystack, etc., you would initialize their agent here:
        #
        # self._custom_agent = YourFramework.create_agent(
        #     llm=self._llm_client,
        #     tools=tools,
        #     system_prompt=system_prompt
        # )
    
    def _build_tool_descriptions(self, tools: List[callable]) -> str:
        """Build tool descriptions for the LLM."""
        descriptions = []
        for tool in tools:
            name = tool.__name__
            doc = tool.__doc__ or "No description"
            # Get function signature
            import inspect
            sig = inspect.signature(tool)
            descriptions.append(f"- {name}{sig}: {doc}")
        return "\n".join(descriptions)
    
    # ===== REQUIRED: Context Management =====
    
    def create_fresh_context(self) -> Any:
        """
        Create a new conversation context.
        
        *** CRITICAL INTEGRATION POINT ***
        
        WHY: Each conversation needs its own context to track history.
             This is called when starting a new session.
        
        WHAT: Creates and returns a fresh context object for a new conversation.
              The context stores conversation history and any state your
              framework needs between turns.
        
        HOW: Return whatever object your framework uses for context.
             This can be anything - dict, list, custom class, etc.
        
        *** EXAMPLES FOR DIFFERENT FRAMEWORKS ***
        
        # LangChain: List of messages
        return []
        
        # LlamaIndex: ChatMemoryBuffer
        from llama_index.core.memory import ChatMemoryBuffer
        return ChatMemoryBuffer.from_defaults(token_limit=3000)
        
        # Haystack: Custom context dict
        return {
            "conversation_history": [],
            "documents": [],
            "metadata": {}
        }
        
        # Custom: Whatever your framework needs
        return MyCustomContext()
        
        *** IMPORTANT ***
        
        The context object you return here will be:
        1. Passed to run_agent() on each turn
        2. Serialized via serialize_context() when saving
        3. Deserialized via deserialize_context() when loading
        
        Make sure it contains everything needed to continue the conversation!
        """
        # ===== Create context structure =====
        # WHY: Need to track conversation history and metadata
        # WHAT: Create dict with messages list and metadata
        # HOW: Return dict with empty messages list
        return {
            "messages": [],  # Conversation history (user/assistant messages)
            "metadata": {
                "session_id": self.current_session_id,
                "user_id": self.current_user_id,
            }
        }
    
    def serialize_context(self, ctx: Any) -> Dict[str, Any]:
        """
        Serialize context to dictionary for persistence.
        
        *** CRITICAL INTEGRATION POINT ***
        
        WHY: Conversations need to be saved to database/disk so users
             can continue them later. This converts your context to
             a JSON-serializable format.
        
        WHAT: Converts the context object to a dictionary that can be
              saved to MongoDB, JSON file, etc.
        
        HOW: Extract all necessary data from your context object and
             return it as a dict. Must be JSON-serializable (no custom
             objects, functions, etc.).
        
        *** EXAMPLES FOR DIFFERENT FRAMEWORKS ***
        
        # LangChain: Messages list is already serializable
        return {"messages": [msg.dict() for msg in ctx]}
        
        # LlamaIndex: Extract messages from memory
        return {
            "messages": ctx.get_all(),
            "token_count": ctx.token_count
        }
        
        # Custom: Extract relevant data
        return {
            "history": ctx.get_history(),
            "state": ctx.get_state(),
            "metadata": ctx.metadata
        }
        
        *** IMPORTANT ***
        
        The dict you return must be JSON-serializable:
        - ✅ str, int, float, bool, None
        - ✅ list, dict (of serializable types)
        - ❌ Custom objects, functions, lambdas
        - ❌ datetime (convert to ISO string first)
        
        Args:
            ctx: The context object (same type as create_fresh_context returns)
            
        Returns:
            JSON-serializable dictionary
        """
        # ===== Serialize context =====
        # WHY: Need to save context to database
        # WHAT: Convert context to JSON-serializable dict
        # HOW: For this example, context is already a dict, so return as-is
        
        # For this simple example, our context is already a dict with
        # JSON-serializable data, so we can return it directly.
        #
        # If your context contains custom objects, you'd need to convert them:
        # return {
        #     "messages": [msg.to_dict() for msg in ctx.messages],
        #     "metadata": ctx.metadata
        # }
        return ctx
    
    def deserialize_context(self, state: Dict[str, Any]) -> Any:
        """
        Deserialize dictionary to context object.
        
        *** CRITICAL INTEGRATION POINT ***
        
        WHY: When loading a saved conversation, we need to reconstruct
             the context object from the saved dictionary.
        
        WHAT: Converts a dictionary (from serialize_context) back into
              the context object your framework needs.
        
        HOW: Take the dict and reconstruct your context object.
             Must return the same type as create_fresh_context().
        
        *** EXAMPLES FOR DIFFERENT FRAMEWORKS ***
        
        # LangChain: Reconstruct message objects
        from langchain.schema import HumanMessage, AIMessage
        messages = []
        for msg_dict in state["messages"]:
            if msg_dict["type"] == "human":
                messages.append(HumanMessage(content=msg_dict["content"]))
            else:
                messages.append(AIMessage(content=msg_dict["content"]))
        return messages
        
        # LlamaIndex: Reconstruct memory buffer
        from llama_index.core.memory import ChatMemoryBuffer
        memory = ChatMemoryBuffer.from_defaults()
        for msg in state["messages"]:
            memory.put(msg)
        return memory
        
        # Custom: Reconstruct custom object
        ctx = MyCustomContext()
        ctx.load_from_dict(state)
        return ctx
        
        *** IMPORTANT ***
        
        The object you return MUST be the same type as create_fresh_context()
        returns, because it will be passed to run_agent().
        
        Args:
            state: Dictionary from serialize_context()
            
        Returns:
            Context object (same type as create_fresh_context returns)
        """
        # ===== Deserialize context =====
        # WHY: Need to restore context from database
        # WHAT: Convert dict back to context object
        # HOW: For this example, context is a dict, so return as-is
        
        # For this simple example, our context is just a dict, so we
        # can return the state directly.
        #
        # If your context is a custom object, you'd need to reconstruct it:
        # ctx = MyCustomContext()
        # ctx.messages = [Message.from_dict(m) for m in state["messages"]]
        # ctx.metadata = state["metadata"]
        # return ctx
        return state
    
    # ===== REQUIRED: Agent Execution =====
    
    async def run_agent(
        self,
        query: str,
        ctx: Any,
        stream: bool = False
    ) -> Union[str, AsyncGenerator]:
        """
        Execute the agent with a query.
        
        *** CRITICAL INTEGRATION POINT ***
        
        This is the MAIN method that executes your framework's agent.
        BaseAgent calls this method to run your agent logic.
        
        WHY: This is where your framework-specific agent execution happens.
             It's the bridge between BaseAgent and your custom framework.
        
        WHAT: Executes the agent and returns results in one of two modes:
              - Non-streaming: Returns complete response as string
              - Streaming: Returns AsyncGenerator yielding events
        
        HOW: Delegates to _run_non_streaming or _run_streaming based on mode.
        
        *** STREAMING VS NON-STREAMING ***
        
        Non-Streaming (stream=False):
        - MUST return: str (the complete final response)
        - WHEN: Batch processing, simple queries, when latency is acceptable
        - EXAMPLE: "The answer is 42"
        
        Streaming (stream=True):
        - MUST return: AsyncGenerator that yields events
        - WHEN: Long responses, better UX, real-time feedback needed
        - EXAMPLE: Yields {"type": "chunk", "content": "The", ...}
                   Yields {"type": "chunk", "content": " answer", ...}
                   Yields {"type": "chunk", "content": " is 42", ...}
        
        *** IMPORTANT: YIELD RAW FRAMEWORK EVENTS ***
        
        When streaming, yield events in YOUR framework's format.
        DO NOT convert to unified format here - that's done in
        process_streaming_event().
        
        Event Flow:
        1. run_agent(stream=True) yields RAW events
        2. BaseAgent.handle_message_stream() receives them
        3. Calls process_streaming_event() to convert each one
        4. Sends unified format to client
        
        Args:
            query: The user query to process
            ctx: The context object (from create_fresh_context)
            stream: Whether to return streaming results
            
        Returns:
            If stream=False: Returns the final response as a string
            If stream=True: Returns an AsyncGenerator that yields events
        """
        # ===== Route to appropriate execution mode =====
        # WHY: Different modes have different return types and logic
        # WHAT: Call streaming or non-streaming implementation
        # HOW: Check stream flag and delegate
        if stream:
            # Streaming mode: return AsyncGenerator
            return self._run_streaming(query, ctx)
        else:
            # Non-streaming mode: return string
            return await self._run_non_streaming(query, ctx)
    
    async def _run_non_streaming(self, query: str, ctx: Dict) -> str:
        """
        Execute agent in non-streaming mode.
        
        This demonstrates the complete tool execution loop:
        1. Send query to LLM
        2. Check if LLM wants to call tools
        3. Execute tools and send results back
        4. Repeat until LLM returns final answer
        
        WHY: Non-streaming mode is simpler and better for batch processing
        WHAT: Returns the complete final response as a string
        HOW: Iterates through tool calls until completion
        """
        # ===== STEP 1: Add user query to conversation history =====
        # WHY: We need to maintain conversation context across turns
        # WHAT: Append the user's message to the context
        ctx["messages"].append({"role": "user", "content": query})
        
        # ===== STEP 2: Build message list for LLM =====
        # WHY: LLMs need system prompt + conversation history
        # WHAT: Combine system prompt with all messages
        # HOW: System message first, then all conversation messages
        messages = [
            {"role": "system", "content": self._system_prompt},
            *ctx["messages"]
        ]
        
        # ===== STEP 3: Tool execution loop =====
        # WHY: LLM might need multiple tool calls to answer the query
        # WHAT: Iterate until LLM returns final answer (no more tool calls)
        # HOW: Call LLM → Check for tool calls → Execute tools → Repeat
        max_iterations = 5  # Prevent infinite loops
        
        for iteration in range(max_iterations):
            logger.info(f"Tool execution iteration {iteration + 1}/{max_iterations}")
            
            # ===== STEP 3a: Call LLM =====
            # WHY: Get LLM's response (either tool calls or final answer)
            # WHAT: Send messages + tool schemas to LLM
            # HOW: Use the client factory's create method
            response = await self._llm_client.create(
                messages=messages,
                tools=self._get_tool_schemas() if self._tools else None
            )
            
            # ===== STEP 3b: Extract LLM's response =====
            # WHY: Need to check if LLM wants to call tools or return answer
            # WHAT: Get the message from the response
            message = response.choices[0].message
            
            # ===== STEP 3c: Check for tool calls =====
            # WHY: LLM might need to call tools to answer the query
            # WHAT: Check if message contains tool_calls
            # HOW: Look for tool_calls attribute on message
            if hasattr(message, 'tool_calls') and message.tool_calls:
                logger.info(f"LLM requested {len(message.tool_calls)} tool call(s)")
                
                # ===== STEP 3d: Execute each tool call =====
                # WHY: LLM needs tool results to continue reasoning
                # WHAT: Execute each requested tool and collect results
                # HOW: Loop through tool_calls, execute, and add results to messages
                
                # First, add the assistant's message with tool calls
                # WHY: OpenAI API requires this format for tool calling
                messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })
                
                # Now execute each tool and add results
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    
                    # ===== Parse tool arguments =====
                    # WHY: Arguments come as JSON string, need to parse
                    # WHAT: Convert JSON string to Python dict
                    # HOW: Use json.loads (safer than eval)
                    import json
                    try:
                        tool_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        tool_args = {}
                        logger.error(f"Failed to parse tool arguments: {tool_call.function.arguments}")
                    
                    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                    
                    # ===== Execute the tool =====
                    # WHY: Get the actual result the LLM needs
                    # WHAT: Call the Python function with parsed arguments
                    # HOW: Look up tool by name and call it
                    if tool_name in self._tools:
                        try:
                            result = self._tools[tool_name](**tool_args)
                            logger.info(f"Tool {tool_name} returned: {result}")
                        except Exception as e:
                            result = f"Error executing tool: {str(e)}"
                            logger.error(f"Tool execution error: {e}")
                    else:
                        result = f"Error: Tool '{tool_name}' not found"
                        logger.error(f"Unknown tool requested: {tool_name}")
                    
                    # ===== Add tool result to messages =====
                    # WHY: LLM needs to see tool results to continue
                    # WHAT: Add a "tool" role message with the result
                    # HOW: Use OpenAI's tool message format
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
                
                # ===== Continue loop to get LLM's next response =====
                # WHY: LLM needs to process tool results and decide next step
                # WHAT: Loop continues, will call LLM again with tool results
                continue
            
            # ===== STEP 4: No tool calls - return final answer =====
            # WHY: LLM has finished reasoning and has final answer
            # WHAT: Extract content and save to context
            # HOW: Get message.content and append to conversation history
            final_response = message.content
            logger.info(f"LLM returned final response: {final_response[:100]}...")
            
            # Save assistant's response to context for next turn
            ctx["messages"].append({"role": "assistant", "content": final_response})
            
            return final_response
        
        # ===== STEP 5: Max iterations reached =====
        # WHY: Prevent infinite loops if LLM keeps calling tools
        # WHAT: Return error message
        logger.warning("Max tool execution iterations reached")
        return "I apologize, but I reached the maximum number of reasoning steps. Please try rephrasing your question."
    
    async def _run_streaming(self, query: str, ctx: Dict) -> AsyncGenerator:
        """
        Execute agent in streaming mode with tool support.
        
        This demonstrates streaming with the complete tool execution loop:
        1. Stream LLM response chunks in real-time
        2. Detect when LLM wants to call tools
        3. Execute tools and stream tool results
        4. Continue streaming until final answer
        
        WHY: Streaming provides better UX with real-time feedback
        WHAT: Yields events as they happen (chunks, tool calls, tool results)
        HOW: AsyncGenerator that yields framework-specific events
        
        IMPORTANT: This method yields RAW framework events.
        The BaseAgent.handle_message_stream() will call process_streaming_event()
        to convert these to unified format.
        """
        # ===== STEP 1: Add user query to conversation history =====
        # WHY: Maintain conversation context
        # WHAT: Append user message to context
        ctx["messages"].append({"role": "user", "content": query})
        
        # ===== STEP 2: Build message list for LLM =====
        # WHY: LLM needs system prompt + conversation history
        # WHAT: Combine system prompt with all messages
        messages = [
            {"role": "system", "content": self._system_prompt},
            *ctx["messages"]
        ]
        
        # ===== STEP 3: Tool execution loop (streaming version) =====
        # WHY: LLM might need multiple tool calls, but we stream each step
        # WHAT: Iterate until LLM returns final answer
        # HOW: Stream LLM response → Execute tools → Stream again
        max_iterations = 5
        
        for iteration in range(max_iterations):
            logger.info(f"Streaming iteration {iteration + 1}/{max_iterations}")
            
            # ===== STEP 3a: Start streaming from LLM =====
            # WHY: Get real-time response chunks for better UX
            # WHAT: Create streaming response from LLM
            # HOW: Pass stream=True to client
            stream = await self._llm_client.create(
                messages=messages,
                tools=self._get_tool_schemas() if self._tools else None,
                stream=True
            )
            
            # ===== STEP 3b: Process streaming chunks =====
            # WHY: Need to yield chunks AND detect tool calls
            # WHAT: Accumulate response while streaming chunks
            # HOW: Track content and tool calls as chunks arrive
            
            accumulated_content = ""
            accumulated_tool_calls = []
            
            # ===== STEP 3c: Yield chunks as they arrive =====
            # WHY: Provide real-time feedback to user
            # WHAT: Yield each content chunk immediately
            # HOW: Check each delta for content or tool_calls
            async for chunk in stream:
                delta = chunk.choices[0].delta
                
                # ===== Handle content chunks =====
                # WHY: Stream text response to user in real-time
                # WHAT: Yield content chunks as "chunk" events
                # HOW: Check if delta has content, yield immediately
                if hasattr(delta, 'content') and delta.content:
                    accumulated_content += delta.content
                    
                    # IMPORTANT: Yield RAW framework event
                    # BaseAgent will convert via process_streaming_event()
                    yield {
                        "type": "chunk",
                        "content": delta.content,
                        "metadata": {
                            "iteration": iteration,
                            "source": "llm_stream"
                        }
                    }
                
                # ===== Handle tool call chunks =====
                # WHY: LLM might request tool calls (streamed incrementally)
                # WHAT: Accumulate tool call information
                # HOW: OpenAI streams tool calls in chunks, need to accumulate
                if hasattr(delta, 'tool_calls') and delta.tool_calls:
                    for tc_chunk in delta.tool_calls:
                        # Ensure we have enough space in accumulated list
                        while len(accumulated_tool_calls) <= tc_chunk.index:
                            accumulated_tool_calls.append({
                                "id": None,
                                "type": "function",
                                "function": {"name": "", "arguments": ""}
                            })
                        
                        # Accumulate tool call data
                        if tc_chunk.id:
                            accumulated_tool_calls[tc_chunk.index]["id"] = tc_chunk.id
                        if tc_chunk.function.name:
                            accumulated_tool_calls[tc_chunk.index]["function"]["name"] = tc_chunk.function.name
                        if tc_chunk.function.arguments:
                            accumulated_tool_calls[tc_chunk.index]["function"]["arguments"] += tc_chunk.function.arguments
            
            # ===== STEP 3d: Check if we have tool calls =====
            # WHY: Need to execute tools if LLM requested them
            # WHAT: Check accumulated_tool_calls list
            # HOW: If not empty, execute tools and continue loop
            if accumulated_tool_calls:
                logger.info(f"Detected {len(accumulated_tool_calls)} tool call(s) in stream")
                
                # ===== Yield tool call events =====
                # WHY: Inform user that tools are being called
                # WHAT: Yield "tool_call" event for each tool
                # HOW: Create event with tool name and arguments
                for tool_call in accumulated_tool_calls:
                    tool_name = tool_call["function"]["name"]
                    tool_args = tool_call["function"]["arguments"]
                    
                    yield {
                        "type": "tool_call",
                        "content": f"Calling tool: {tool_name}",
                        "metadata": {
                            "tool_name": tool_name,
                            "tool_arguments": tool_args,
                            "call_id": tool_call["id"]
                        }
                    }
                
                # ===== Add assistant message with tool calls =====
                # WHY: OpenAI API requires this format
                # WHAT: Add message showing LLM's tool call request
                messages.append({
                    "role": "assistant",
                    "content": accumulated_content or None,
                    "tool_calls": accumulated_tool_calls
                })
                
                # ===== Execute each tool =====
                # WHY: Get results LLM needs to continue
                # WHAT: Execute tools and add results to messages
                # HOW: Loop through tool calls, execute, yield results
                for tool_call in accumulated_tool_calls:
                    tool_name = tool_call["function"]["name"]
                    
                    # Parse arguments
                    import json
                    try:
                        tool_args = json.loads(tool_call["function"]["arguments"])
                    except json.JSONDecodeError:
                        tool_args = {}
                        logger.error(f"Failed to parse tool arguments: {tool_call['function']['arguments']}")
                    
                    logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                    
                    # Execute tool
                    if tool_name in self._tools:
                        try:
                            result = self._tools[tool_name](**tool_args)
                            logger.info(f"Tool {tool_name} returned: {result}")
                        except Exception as e:
                            result = f"Error executing tool: {str(e)}"
                            logger.error(f"Tool execution error: {e}")
                    else:
                        result = f"Error: Tool '{tool_name}' not found"
                        logger.error(f"Unknown tool requested: {tool_name}")
                    
                    # ===== Yield tool result event =====
                    # WHY: Show user the tool execution result
                    # WHAT: Yield "tool_result" event with result
                    # HOW: Create event with tool name and result
                    yield {
                        "type": "tool_result",
                        "content": f"Tool {tool_name} result: {result}",
                        "metadata": {
                            "tool_name": tool_name,
                            "result": str(result),
                            "call_id": tool_call["id"]
                        }
                    }
                    
                    # ===== Add tool result to messages =====
                    # WHY: LLM needs to see results to continue
                    # WHAT: Add "tool" role message
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": str(result)
                    })
                
                # ===== Continue loop to get LLM's next response =====
                # WHY: LLM needs to process tool results
                # WHAT: Loop continues, will stream LLM's next response
                continue
            
            # ===== STEP 4: No tool calls - save final response =====
            # WHY: Conversation is complete, save to context
            # WHAT: Add assistant's response to context
            # HOW: Append to messages list
            if accumulated_content:
                ctx["messages"].append({"role": "assistant", "content": accumulated_content})
                logger.info(f"Streaming complete. Final response: {accumulated_content[:100]}...")
            
            # Exit loop - we're done
            return
        
        # ===== STEP 5: Max iterations reached =====
        # WHY: Prevent infinite loops
        # WHAT: Yield error event
        logger.warning("Max streaming iterations reached")
        yield {
            "type": "error",
            "content": "Maximum reasoning steps reached. Please try rephrasing your question.",
            "metadata": {"reason": "max_iterations"}
        }
    
    def _get_tool_schemas(self) -> List[Dict]:
        """Convert tools to OpenAI function calling format."""
        schemas = []
        for name, tool in self._tools.items():
            import inspect
            sig = inspect.signature(tool)
            parameters = {
                "type": "object",
                "properties": {},
                "required": []
            }
            for param_name, param in sig.parameters.items():
                param_type = "string"
                if param.annotation == float or param.annotation == int:
                    param_type = "number"
                parameters["properties"][param_name] = {"type": param_type}
                parameters["required"].append(param_name)
            
            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.__doc__ or "",
                    "parameters": parameters
                }
            })
        return schemas
    
    # ===== OPTIONAL: Streaming Event Processing =====
    
    async def process_streaming_event(self, event: Any) -> Dict[str, Any]:
        """
        Convert framework-specific streaming events to unified format.
        
        *** CRITICAL INTEGRATION POINT ***
        
        This method is called by BaseAgent.handle_message_stream() for EVERY
        event yielded by run_agent() in streaming mode.
        
        WHY: Different frameworks emit events in different formats.
             This method normalizes them to a standard format.
        
        WHAT: Converts framework-specific events to unified format that
              the web UI and clients can understand.
        
        HOW: Examine the event structure and map it to unified format.
             Return None to skip events you don't want to send to client.
        
        *** EVENT FLOW ***
        
        1. run_agent(stream=True) yields RAW framework events
        2. BaseAgent.handle_message_stream() receives each event
        3. Calls THIS method (process_streaming_event) to convert
        4. Converts to StructuredAgentOutput
        5. Sends to client
        
        *** UNIFIED FORMAT ***
        
        All events must have this structure:
        {
            "type": "chunk" | "tool_call" | "tool_result" | "activity" | "error",
            "content": str,  # Human-readable content
            "metadata": {...}  # Additional data (optional)
        }
        
        Event Types:
        - "chunk": Text content being streamed (e.g., LLM response)
        - "tool_call": Agent is calling a tool
        - "tool_result": Tool execution completed with result
        - "activity": Status update (e.g., "Thinking...", "Searching...")
        - "error": Error occurred during execution
        
        Args:
            event: Raw event from your framework (whatever run_agent yields)
            
        Returns:
            Dict in unified format, or None to skip this event
        
        *** EXAMPLES FOR DIFFERENT FRAMEWORKS ***
        
        # Example 1: LlamaIndex AgentStream
        if isinstance(event, AgentStream):
            if event.type == "text":
                return {
                    "type": "chunk",
                    "content": event.text,
                    "metadata": {"source": "llamaindex"}
                }
            elif event.type == "tool_call":
                return {
                    "type": "tool_call",
                    "content": f"Calling {event.tool_name}",
                    "metadata": {"tool_name": event.tool_name}
                }
        
        # Example 2: LangChain streaming
        if isinstance(event, dict) and "type" in event:
            if event["type"] == "llm_new_token":
                return {
                    "type": "chunk",
                    "content": event["token"],
                    "metadata": {"source": "langchain"}
                }
        
        # Example 3: Custom framework (this example)
        # Our events are already in unified format, so just return them
        """
        # ===== STEP 1: Validate event structure =====
        # WHY: Ensure event is in expected format
        # WHAT: Check if event is a dict with required fields
        # HOW: Use isinstance and key checks
        if not isinstance(event, dict):
            logger.warning(f"Unexpected event type: {type(event)}")
            return None
        
        # ===== STEP 2: Check event type =====
        # WHY: Different event types need different handling
        # WHAT: Validate event has "type" field
        # HOW: Check for "type" key
        if "type" not in event:
            logger.warning(f"Event missing 'type' field: {event}")
            return None
        
        # ===== STEP 3: Validate event type value =====
        # WHY: Only certain event types are supported
        # WHAT: Check if type is one of the allowed values
        # HOW: Check against list of valid types
        valid_types = ["chunk", "tool_call", "tool_result", "activity", "error"]
        if event["type"] not in valid_types:
            logger.warning(f"Invalid event type: {event['type']}")
            return None
        
        # ===== STEP 4: Ensure content field exists =====
        # WHY: All events must have content
        # WHAT: Add empty content if missing
        # HOW: Use .get() with default value
        if "content" not in event:
            event["content"] = ""
        
        # ===== STEP 5: Ensure metadata field exists =====
        # WHY: Metadata is optional but should always be present
        # WHAT: Add empty metadata if missing
        # HOW: Use .get() with default value
        if "metadata" not in event:
            event["metadata"] = {}
        
        # ===== STEP 6: Return unified format event =====
        # WHY: Event is now in correct format
        # WHAT: Return the validated/normalized event
        # HOW: Return as-is (our events are already in unified format)
        
        # For this example, our _run_streaming() already yields events
        # in unified format, so we just validate and return them.
        # 
        # In a real integration with a different framework, you would
        # transform the framework's event structure here.
        
        logger.debug(f"Processing event: type={event['type']}, content_length={len(event['content'])}")
        return event


def main():
    """Start the custom framework agent server with UI."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY=your-key-here")
        return
    
    # Import server function
    from agent_framework import create_basic_agent_server
    
    # Get port from environment or use default
    port = int(os.getenv("AGENT_PORT", "8103"))
    
    print("=" * 60)
    print("🚀 Starting Custom Framework Agent Server")
    print("=" * 60)
    print(f"📊 Model: {os.getenv('DEFAULT_MODEL', 'gpt-4o-mini')}")
    print(f"🔧 Tools: add, multiply, divide")
    print(f"🎯 Framework: Custom (BaseAgent)")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"🎨 UI: http://localhost:{port}/testapp")
    print("=" * 60)
    print("\nThis example shows how to integrate ANY AI framework:")
    print("  - LangChain")
    print("  - Haystack")
    print("  - Custom implementations")
    print("  - Any other framework")
    print("\nTry asking:")
    print("  - What is 15 + 27?")
    print("  - Multiply 8 by 9")
    print("  - Divide 100 by 4")
    print("=" * 60)
    
    # Start the server
    create_basic_agent_server(
        agent_class=CustomFrameworkAgent,
        host="0.0.0.0",
        port=port,
        reload=False
    )


if __name__ == "__main__":
    main()
