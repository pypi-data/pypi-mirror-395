"""
Agent Provider (Manager) and Proxy

This module contains the AgentManager and the _ManagedAgentProxy classes,
which are responsible for managing the lifecycle of agent instances and
transparently handling state persistence.
"""
import logging
from datetime import datetime, timezone
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

        # 3. Get dynamic configuration from Elasticsearch (transparent)
        # Priority: Elasticsearch > Hardcoded > Defaults
        from agent_framework.core.model_config import model_config
        
        dynamic_config = await model_config.get_agent_configuration(agent_identity.agent_id)
        config_source = dynamic_config.get('_source', 'unknown')
        logger.debug(
            f"AgentManager: Retrieved dynamic config for agent_id={agent_identity.agent_id} "
            f"from source={config_source}"
        )
        
        # 4. Load session configuration and merge with dynamic config
        session_data = await self._storage.load_session(user_id, session_id)
        
        # Check if session has a stored config_doc_id (from Elasticsearch)
        if session_data and session_data.session_configuration:
            stored_config = session_data.session_configuration
            
            # If session was created with an ES config, load that specific version
            if stored_config.get("config_source") == "elasticsearch" and stored_config.get("config_doc_id"):
                config_doc_id = stored_config["config_doc_id"]
                
                # CRITICAL: Verify config_doc_id is not None
                if config_doc_id is None:
                    logger.error(
                        f"AgentManager: CRITICAL BUG - Loaded config_doc_id is None from session! "
                        f"session_id={session_id}, user_id={user_id}. "
                        f"This violates session isolation. Falling back to current active config."
                    )
                    effective_config = dynamic_config.copy()
                else:
                    logger.info(
                        f"AgentManager: ✓ Session has stored ES config reference - "
                        f"doc_id={config_doc_id}, version={stored_config.get('config_version')}. "
                        f"Loading session-specific config to maintain isolation."
                    )
                    
                    try:
                        # Load the specific config version from Elasticsearch
                        session_specific_config = await model_config.get_agent_configuration(
                            agent_identity.agent_id,
                            doc_id=config_doc_id
                        )
                        effective_config = session_specific_config.copy()
                        config_source = f"elasticsearch (session version {stored_config.get('config_version')})"
                        logger.info(
                            f"AgentManager: ✓ Loaded session-specific ES config - "
                            f"doc_id={config_doc_id}, model={effective_config.get('model_name')}. "
                            f"Session isolation maintained."
                        )
                        
                        # Apply session overrides on top of ES config (overrides take precedence)
                        session_overrides = stored_config.get("session_overrides")
                        if session_overrides:
                            for key, value in session_overrides.items():
                                if value is not None:
                                    effective_config[key] = value
                            logger.info(
                                f"AgentManager: ✓ Applied session overrides on top of ES config: "
                                f"{list(session_overrides.keys())}. "
                                f"Override values take precedence over ES config."
                            )
                    except Exception as e:
                        logger.warning(
                            f"AgentManager: Failed to load session-specific ES config (doc_id={config_doc_id}): {e}. "
                            "Falling back to current active config."
                        )
                        effective_config = dynamic_config.copy()
            else:
                # Session has stored config but not from ES, merge it
                logger.debug(f"AgentManager: Found existing session configuration, merging with dynamic config")
                effective_config = dynamic_config.copy()
                effective_config = self._merge_session_configs(effective_config, stored_config)
        else:
            # No existing session config, use dynamic config
            effective_config = dynamic_config.copy()
        
        # Add session info
        effective_config["user_id"] = user_id
        effective_config["session_id"] = session_id
        
        # Apply configuration to agent
        if hasattr(real_agent, 'configure_session'):
            await real_agent.configure_session(effective_config)
            logger.info(
                f"AgentManager: Applied configuration to agent - "
                f"model={effective_config.get('model_name', 'unknown')}, "
                f"source={config_source}"
            )
        else:
            logger.warning(f"AgentManager: Agent {agent_class.__name__} does not have configure_session method. Configuration not applied.")
        
        # Update session with configuration reference (not full config)
        # Ensure session_data exists before storing config reference
        if not session_data:
            from ..session.session_storage import SessionData
            session_data = SessionData(
                session_id=session_id,
                user_id=user_id,
                agent_instance_config={},
                created_at=datetime.now(timezone.utc).isoformat(),
                updated_at=datetime.now(timezone.utc).isoformat()
            )
            logger.debug(f"AgentManager: Created new session_data for session {session_id}")
        
        # Store reference to ES config document instead of full config
        if config_source == "elasticsearch" and await model_config._ensure_es_provider_initialized():
            try:
                # Get the active config version to store its doc_id
                versions = await model_config._es_config_provider.get_config_versions(agent_identity.agent_id, limit=1)
                if versions:
                    latest = versions[0]
                    config_doc_id = latest.get("_id")
                    
                    # CRITICAL: Verify config_doc_id is not None
                    if config_doc_id is None:
                        logger.error(
                            f"AgentManager: CRITICAL BUG - config_doc_id is None! "
                            f"agent_id={agent_identity.agent_id}, version={latest.get('version')}. "
                            f"This violates session isolation. Falling back to full config."
                        )
                        session_data.session_configuration = effective_config
                    else:
                        # Extract session overrides before storing ES reference
                        # Only extract if current config is NOT already an ES reference
                        session_overrides = {}
                        if session_data and session_data.session_configuration:
                            existing_config = session_data.session_configuration
                            # Only extract if not already an ES reference (no config_source)
                            if existing_config.get("config_source") != "elasticsearch":
                                override_keys = ["system_prompt", "model_name", "model_config", "enable_rich_content"]
                                for key in override_keys:
                                    if key in existing_config:
                                        session_overrides[key] = existing_config[key]
                                if session_overrides:
                                    logger.info(
                                        f"AgentManager: Extracted session overrides before ES reference storage: "
                                        f"{list(session_overrides.keys())}"
                                    )
                        
                        # Store config reference instead of full config
                        session_data.session_configuration = {
                            "config_source": "elasticsearch",
                            "config_doc_id": config_doc_id,  # ES document ID
                            "config_version": latest.get("version"),
                            "agent_id": agent_identity.agent_id,
                            "config_captured_at": latest.get("updated_at"),
                            # Keep essential session-specific overrides
                            "user_id": user_id,
                            "session_id": session_id,
                            # NEW: Preserve session overrides (only if there are any)
                            "session_overrides": session_overrides if session_overrides else None
                        }
                        if session_overrides:
                            logger.info(
                                f"AgentManager: ✓ Stored ES config reference with preserved session overrides - "
                                f"doc_id={config_doc_id}, version={latest.get('version')}, "
                                f"overrides={list(session_overrides.keys())}. "
                                f"Session isolation guaranteed."
                            )
                        else:
                            logger.info(
                                f"AgentManager: ✓ Stored ES config reference - "
                                f"doc_id={config_doc_id}, version={latest.get('version')}. "
                                f"Session isolation guaranteed."
                            )
                else:
                    # Fallback: store full config if we can't get version info
                    session_data.session_configuration = effective_config
                    logger.warning(f"AgentManager: Could not get ES config version, storing full config")
            except Exception as e:
                logger.warning(f"AgentManager: Error getting ES config version: {e}, storing full config")
                session_data.session_configuration = effective_config
        else:
            # For non-ES configs, store the full config as before
            session_data.session_configuration = effective_config
        
        await self._storage.save_session(user_id, session_id, session_data)

        # 5. Update session with agent identity
        await self._update_session_with_agent_identity(user_id, session_id, agent_identity)

        # 6. Load its state from storage with agent identity validation
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

        # 7. Record session started lifecycle event
        await self._record_lifecycle_event(agent_identity, "session_started", session_id, user_id)

        # 7. Wrap the real agent in the proxy
        proxy = _ManagedAgentProxy(session_id, real_agent, self)
        
        return proxy
        
    def _merge_session_configs(self, base_config: Dict[str, Any], session_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge session configuration with base configuration.
        
        Session config takes precedence for fields that exist in both.
        Missing fields in session config are filled from base config.
        
        Args:
            base_config: Base configuration (from Elasticsearch/hardcoded/defaults)
            session_config: Session-specific configuration
            
        Returns:
            Merged configuration dictionary
        """
        merged = base_config.copy()
        
        for key, value in session_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # Deep merge for nested dicts
                merged[key] = self._merge_session_configs(merged[key], value)
            else:
                # Session value takes precedence
                merged[key] = value
        
        return merged
    
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