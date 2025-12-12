"""
Agent Provider (Manager) and Proxy

This module contains the AgentManager and the _ManagedAgentProxy classes,
which are responsible for managing the lifecycle of agent instances and
transparently handling state persistence.
"""
import logging
from typing import Type, Dict, Any, Optional, AsyncGenerator

from .agent_interface import AgentInterface, StructuredAgentInput, StructuredAgentOutput
from ..session.session_storage import SessionStorageInterface
from .state_manager import (
    AgentIdentity, 
    StateManager
)
from ..session.session_storage import AgentLifecycleData

logger = logging.getLogger(__name__)

class _ManagedAgentProxy(AgentInterface):
    """
    A proxy that wraps a real agent instance. It implements the AgentInterface
    so that it's indistinguishable from a real agent to the server.

    Its primary role is to automatically trigger state persistence after
    an interaction.
    """
    def __init__(self, session_id: str, real_agent: AgentInterface, agent_manager: 'AgentManager'):
        self._session_id = session_id
        self._real_agent = real_agent
        self._agent_manager = agent_manager
    
    def __getattr__(self, name: str):
        """
        Delegate attribute access to the real agent.
        This allows the proxy to expose attributes like agent_id from the real agent.
        """
        return getattr(self._real_agent, name)

    async def get_metadata(self) -> Dict[str, Any]:
        """Passes the call to the real agent."""
        return await self._real_agent.get_metadata()

    async def get_system_prompt(self) -> Optional[str]:
        """Passes the call to the real agent."""
        return await self._real_agent.get_system_prompt()

    async def get_current_model(self, session_id: str) -> Optional[str]:
        """Passes the call to the real agent."""
        return await self._real_agent.get_current_model(session_id)
        
    async def get_state(self) -> Dict[str, Any]:
        """Passes the call to the real agent."""
        return await self._real_agent.get_state()

    async def load_state(self, state: Dict[str, Any]):
        """Passes the call to the real agent."""
        await self._real_agent.load_state(state)

    async def handle_message(self, session_id: str, agent_input: StructuredAgentInput) -> StructuredAgentOutput:
        """
        Handles the message using the real agent and then automatically
        persists the new state.
        """
        # 1. Forward the call to the real agent
        response = await self._real_agent.handle_message(session_id, agent_input)
        
        # 2. Automatically persist the state after the call
        logger.debug(f"Proxy: Auto-saving state for session {self._session_id}")
        await self._agent_manager.save_agent_state(self._session_id, self._real_agent)
        
        return response

    async def handle_message_stream(
        self, session_id: str, agent_input: StructuredAgentInput
    ) -> AsyncGenerator[StructuredAgentOutput, None]:
        """
        Handles the message stream using the real agent and then automatically
        persists the new state at the end of the stream.
        """
        # 1. Forward the call to the real agent's stream
        response_generator = self._real_agent.handle_message_stream(session_id, agent_input)
        
        # 2. Yield all parts from the generator to the caller
        async for response_part in response_generator:
            yield response_part
            
        # 3. After the stream is complete, persist the final state
        logger.debug(f"Proxy: Stream finished. Auto-saving state for session {self._session_id}")
        await self._agent_manager.save_agent_state(self._session_id, self._real_agent)

class AgentManager:
    """
    Manages the lifecycle of agent instances. This is the single entry point
    for the server to get a fully prepared agent.
    """
    def __init__(self, storage: SessionStorageInterface):
        self._storage = storage
        self._active_agents: Dict[str, AgentInterface] = {} # A cache for active agent instances

    async def get_agent(self, session_id: str, agent_class: Type[AgentInterface], user_id: str = "") -> AgentInterface:
        """
        Gets a fully initialized agent instance for a given session, wrapped in a
        state-managing proxy.
        
        Args:
            session_id: The session identifier
            agent_class: The agent class to instantiate
            user_id: The user ID for session lookup (optional for backward compatibility)
        """
        # For simplicity, we create a new agent instance for each request.
        # A more advanced implementation could cache and reuse agent instances.
        
        logger.debug(f"AgentManager: Getting agent for session {session_id}, user {user_id}")
        
        # 1. Create a fresh instance of the agent
        real_agent = agent_class()
        
        # 1.5. Inject session storage for memory support (if agent supports it)
        if hasattr(real_agent, 'set_session_storage'):
            real_agent.set_session_storage(self._storage)
            logger.debug(f"AgentManager: Injected session storage into agent for memory support")

        # 2. Create agent identity before any other operations
        agent_identity = StateManager.create_agent_identity(real_agent)
        logger.debug(f"AgentManager: Agent identity created - ID: {agent_identity.agent_id}, Type: {agent_identity.agent_type}")

        # Record agent creation lifecycle event
        await self._record_lifecycle_event(agent_identity, "created", session_id, user_id)

        # 3. Load session configuration and apply it to the agent if available
        session_data = await self._storage.load_session(user_id, session_id)
        if session_data and session_data.session_configuration:
            logger.debug(f"AgentManager: Found session configuration for session {session_id}. Applying configuration.")
            # Ensure the configuration includes user_id and session_id
            config_with_session_info = session_data.session_configuration.copy()
            config_with_session_info["user_id"] = user_id
            config_with_session_info["session_id"] = session_id
            
            # If the agent has a configure_session method, call it
            if hasattr(real_agent, 'configure_session'):
                await real_agent.configure_session(config_with_session_info)
            else:
                logger.warning(f"AgentManager: Agent {agent_class.__name__} does not have configure_session method. Configuration not applied.")
        else:
            logger.debug(f"AgentManager: No session configuration found for session {session_id}. Using default configuration with session info.")
            # Even without explicit session configuration, provide basic session info to the agent
            if hasattr(real_agent, 'configure_session'):
                default_config = {
                    "user_id": user_id,
                    "session_id": session_id
                }
                await real_agent.configure_session(default_config)
                logger.debug(f"AgentManager: Applied default session configuration: {default_config}")

        # 4. Update session with agent identity
        await self._update_session_with_agent_identity(user_id, session_id, agent_identity)

        # 5. Load its state from storage with agent identity validation
        agent_state = await self._storage.load_agent_state(session_id)
        if agent_state:
            logger.debug(f"AgentManager: Found existing state for session {session_id}. Loading.")
            # Decompress state if it was compressed
            agent_state = StateManager.decompress_state(agent_state)
            # Validate state compatibility before loading
            if StateManager.validate_state_compatibility(agent_state, agent_identity):
                await real_agent.load_state(agent_state)
                # Record state loaded lifecycle event
                await self._record_lifecycle_event(agent_identity, "state_loaded", session_id, user_id)
            else:
                logger.warning(f"AgentManager: Agent state incompatible for session {session_id}. Starting fresh.")
                await real_agent.load_state({})
        else:
            logger.debug(f"AgentManager: No state found for session {session_id}. Agent will start fresh.")
            # Ensure agent starts with a default empty state if none is found
            await real_agent.load_state({})

        # 6. Record session started lifecycle event
        await self._record_lifecycle_event(agent_identity, "session_started", session_id, user_id)

        # 7. Wrap the real agent in the proxy
        proxy = _ManagedAgentProxy(session_id, real_agent, self)
        
        return proxy
        
    async def save_agent_state(self, session_id: str, agent_instance: AgentInterface):
        """
        Saves the agent's current state to the storage backend with agent identity validation.
        """
        # Create agent identity
        agent_identity = StateManager.create_agent_identity(agent_instance)
        
        # Get new state
        new_state = await agent_instance.get_state()
        
        # Add agent identity metadata to state for validation
        if isinstance(new_state, dict):
            new_state['_agent_identity'] = agent_identity.to_dict()
        
        # Compress state before storage
        compressed_state = StateManager.compress_state(new_state)
        
        await self._storage.save_agent_state(session_id, compressed_state)
        logger.debug(f"AgentManager: Persisted state for session {session_id} with agent identity {agent_identity.agent_id}")
        
        # Record state saved lifecycle event
        await self._record_lifecycle_event(agent_identity, "state_saved", session_id)
    
    async def _update_session_with_agent_identity(self, user_id: str, session_id: str, 
                                                 agent_identity: AgentIdentity) -> None:
        """Updates session metadata with agent identity"""
        try:
            session_data = await self._storage.load_session(user_id, session_id)
            if session_data:
                # Update existing session with agent identity
                session_data.agent_id = agent_identity.agent_id
                session_data.agent_type = agent_identity.agent_type
                
                # Update metadata with full agent identity information
                if not session_data.metadata:
                    session_data.metadata = {}
                session_data.metadata['agent_identity'] = agent_identity.to_dict()
                
                await self._storage.save_session(user_id, session_id, session_data)
                logger.debug(f"AgentManager: Updated session {session_id} with agent identity {agent_identity.agent_id}")
            else:
                logger.warning(f"AgentManager: Could not find session {session_id} to update with agent identity")
        except Exception as e:
            logger.error(f"AgentManager: Error updating session with agent identity: {e}")
    
    async def _validate_agent_state_compatibility(self, agent_identity: AgentIdentity, 
                                                 agent_state: Dict[str, Any]) -> bool:
        """
        Validate that agent state is compatible with current agent identity.
        
        This method is deprecated and kept for backward compatibility.
        Use StateManager.validate_state_compatibility() directly instead.
        """
        return StateManager.validate_state_compatibility(agent_state, agent_identity)
    
    async def _record_lifecycle_event(self, agent_identity: AgentIdentity, event_type: str, 
                                     session_id: Optional[str] = None, user_id: Optional[str] = None,
                                     metadata: Optional[Dict[str, Any]] = None) -> None:
        """Record an agent lifecycle event"""
        try:
            lifecycle_data = AgentLifecycleData(
                lifecycle_id="",  # Will be auto-generated
                agent_id=agent_identity.agent_id,
                agent_type=agent_identity.agent_type,
                event_type=event_type,
                session_id=session_id,
                user_id=user_id,
                metadata=metadata or {}
            )
            
            success = await self._storage.add_agent_lifecycle_event(lifecycle_data)
            if success:
                logger.debug(f"AgentManager: Recorded lifecycle event '{event_type}' for agent {agent_identity.agent_id}")
            else:
                logger.warning(f"AgentManager: Failed to record lifecycle event '{event_type}' for agent {agent_identity.agent_id}")
        except Exception as e:
            logger.error(f"AgentManager: Error recording lifecycle event '{event_type}': {e}") 