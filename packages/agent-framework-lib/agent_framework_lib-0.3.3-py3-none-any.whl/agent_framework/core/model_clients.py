"""
Multi-Provider Model Client Factory

Creates appropriate model clients (OpenAI, Anthropic, Gemini, etc.) based on model configuration.
This module is framework-agnostic and uses native client libraries.
"""

import logging
import re
from typing import Any, Dict, Optional, Union, Type
from .model_config import ModelConfigManager, ModelProvider, model_config
from .agent_interface import AgentConfig

logger = logging.getLogger(__name__)

# Try importing OpenAI client
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    logger.warning("[ModelClientFactory] OpenAI client not available. Install with: uv add openai")
    OPENAI_AVAILABLE = False

# Try importing Anthropic client
try:
    from anthropic import AsyncAnthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    logger.warning("[ModelClientFactory] Anthropic client not available. Install with: uv add anthropic")
    ANTHROPIC_AVAILABLE = False

# Try importing Google Gemini client
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    logger.warning("[ModelClientFactory] Google Gemini client not available. Install with: uv add google-generativeai")
    GEMINI_AVAILABLE = False

class ModelClientFactory:
    """
    Factory class for creating appropriate model clients based on model names.
    Framework-agnostic implementation using native client libraries.
    """
    
    def __init__(self, config_manager: ModelConfigManager = None):
        """
        Initialize the client factory.
        
        Args:
            config_manager: Optional ModelConfigManager instance. If None, uses global instance.
        """
        self.config = config_manager or model_config
    
    def create_client(
        self, 
        model_name: str = None, 
        agent_config: AgentConfig = None,
        **override_params
    ) -> Any:
        """
        Create an appropriate model client for the given model.
        
        Args:
            model_name: Name of the model. If None, uses default model.
            agent_config: Optional agent configuration with overrides.
            **override_params: Additional parameters to override defaults.
            
        Returns:
            Configured model client instance (AsyncOpenAI, AsyncAnthropic, or genai client).
        """
        # Use default model if none specified
        if not model_name:
            model_name = self.config.default_model
            logger.debug(f"[ModelClientFactory] No model specified, using default: {model_name}")
        
        # Determine provider and get configuration
        provider = self.config.get_provider_for_model(model_name)
        api_key = self.config.get_api_key_for_provider(provider)
        defaults = self.config.get_defaults_for_provider(provider)
        
        logger.debug(f"[ModelClientFactory] Creating client for model '{model_name}':")
        logger.debug(f"  - Provider: {provider.value}")
        logger.debug(f"  - API key configured: {'✓' if api_key else '✗'}")
        logger.debug(f"  - Provider defaults: {defaults}")
        
        if not api_key:
            raise ValueError(f"No API key configured for provider {provider.value} (model: {model_name})")
        
        # Build parameters with precedence: override_params > agent_config > defaults
        params = defaults.copy()
        params.update(override_params)
        
        # Apply agent config overrides if provided
        if agent_config:
            logger.debug(f"[ModelClientFactory] Applying agent configuration overrides:")
            logger.debug(f"  - Agent config: {agent_config.dict(exclude_unset=True)}")
            
            if agent_config.temperature is not None:
                params["temperature"] = agent_config.temperature
                logger.debug(f"  - Temperature override: {agent_config.temperature}")
            if agent_config.timeout is not None:
                params["timeout"] = agent_config.timeout
                logger.debug(f"  - Timeout override: {agent_config.timeout}")
            if agent_config.max_retries is not None:
                params["max_retries"] = agent_config.max_retries
                logger.debug(f"  - Max retries override: {agent_config.max_retries}")
            if agent_config.model_selection is not None:
                old_model = model_name
                model_name = agent_config.model_selection
                logger.debug(f"  - Model override: {old_model} → {model_name}")
                # Re-determine provider if model was overridden
                provider = self.config.get_provider_for_model(model_name)
                api_key = self.config.get_api_key_for_provider(provider)
                logger.debug(f"  - Provider changed to: {provider.value}")
        
        # Add required parameters
        params.update({
            "model": model_name,
            "api_key": api_key
        })
        
        # Create client based on provider
        if provider == ModelProvider.OPENAI:
            return self._create_openai_client(params, agent_config)
        elif provider == ModelProvider.GEMINI:
            return self._create_gemini_client(params, agent_config)
        elif provider == ModelProvider.ANTHROPIC:
            return self._create_anthropic_client(params, agent_config)
        else:
            logger.warning(f"[ModelClientFactory] Unknown provider {provider}, falling back to OpenAI")
            return self._create_openai_client(params, agent_config)
    
    def _create_openai_client(self, params: Dict[str, Any], agent_config: AgentConfig = None) -> Any:
        """Create an OpenAI client with the given parameters."""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI client not available. Install with: uv add openai")
        
        # Build OpenAI client parameters
        client_params = {
            "api_key": params["api_key"],
        }
        
        # Add optional parameters if present
        if "timeout" in params:
            client_params["timeout"] = params["timeout"]
        if "max_retries" in params:
            client_params["max_retries"] = params["max_retries"]
        
        # Store model configuration for later use
        model_params = {
            "model": params["model"],
            "temperature": params.get("temperature", 0.7),
        }
        
        # Apply agent config overrides for OpenAI-specific parameters
        if agent_config:
            if agent_config.max_tokens is not None:
                model_params["max_tokens"] = agent_config.max_tokens
            if agent_config.top_p is not None:
                model_params["top_p"] = agent_config.top_p
            if agent_config.frequency_penalty is not None:
                model_params["frequency_penalty"] = agent_config.frequency_penalty
            if agent_config.presence_penalty is not None:
                model_params["presence_penalty"] = agent_config.presence_penalty
            if agent_config.stop_sequences is not None:
                model_params["stop"] = agent_config.stop_sequences
        
        logger.info(f"[ModelClientFactory] Creating OpenAI client for model: {model_params['model']}")
        logger.debug(f"[ModelClientFactory] OpenAI client params: {list(client_params.keys())}")
        logger.debug(f"[ModelClientFactory] Model params: {list(model_params.keys())}")
        
        try:
            client = AsyncOpenAI(**client_params)
            # Attach model parameters to client for easy access
            client._model_params = model_params
            return client
        except Exception as e:
            logger.error(f"[ModelClientFactory] Failed to create OpenAI client: {e}")
            raise
    
    def _create_gemini_client(self, params: Dict[str, Any], agent_config: AgentConfig = None) -> Any:
        """Create a Google Gemini client with the given parameters."""
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Gemini client not available. Install with: uv add google-generativeai")
        
        # Configure Gemini API
        genai.configure(api_key=params["api_key"])
        
        # Build generation config
        generation_config = {
            "temperature": params.get("temperature", 0.7),
        }
        
        # Apply agent config overrides for Gemini-specific parameters
        if agent_config:
            if agent_config.max_tokens is not None:
                generation_config["max_output_tokens"] = agent_config.max_tokens
            if agent_config.top_p is not None:
                generation_config["top_p"] = agent_config.top_p
            if agent_config.stop_sequences is not None:
                generation_config["stop_sequences"] = agent_config.stop_sequences
            
            # Log unsupported parameters
            unsupported = []
            if agent_config.frequency_penalty is not None:
                unsupported.append("frequency_penalty")
            if agent_config.presence_penalty is not None:
                unsupported.append("presence_penalty")
            if unsupported:
                logger.warning(f"[ModelClientFactory] Gemini does not support: {unsupported}")
        
        logger.info(f"[ModelClientFactory] Creating Gemini client for model: {params['model']}")
        logger.debug(f"[ModelClientFactory] Gemini generation config: {generation_config}")
        
        try:
            # Create Gemini model instance
            model = genai.GenerativeModel(
                model_name=params["model"],
                generation_config=generation_config
            )
            # Attach model parameters for easy access
            model._model_params = {
                "model": params["model"],
                **generation_config
            }
            return model
        except Exception as e:
            logger.error(f"[ModelClientFactory] Failed to create Gemini client: {e}")
            raise
    
    def _create_anthropic_client(self, params: Dict[str, Any], agent_config: AgentConfig = None) -> Any:
        """Create an Anthropic client with the given parameters."""
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic client not available. Install with: uv add anthropic")
        
        # Build Anthropic client parameters
        client_params = {
            "api_key": params["api_key"],
        }
        
        # Add optional parameters if present
        if "timeout" in params:
            client_params["timeout"] = params["timeout"]
        if "max_retries" in params:
            client_params["max_retries"] = params["max_retries"]
        
        # Store model configuration for later use
        model_params = {
            "model": params["model"],
            "temperature": params.get("temperature", 0.7),
        }
        
        # Apply agent config overrides for Anthropic-specific parameters
        if agent_config:
            if agent_config.max_tokens is not None:
                model_params["max_tokens"] = agent_config.max_tokens
            if agent_config.top_p is not None:
                model_params["top_p"] = agent_config.top_p
            if agent_config.stop_sequences is not None:
                model_params["stop_sequences"] = agent_config.stop_sequences
            
            # Log unsupported parameters
            unsupported = []
            if agent_config.frequency_penalty is not None:
                unsupported.append("frequency_penalty")
            if agent_config.presence_penalty is not None:
                unsupported.append("presence_penalty")
            if unsupported:
                logger.warning(f"[ModelClientFactory] Anthropic does not support: {unsupported}")
        
        logger.info(f"[ModelClientFactory] Creating Anthropic client for model: {model_params['model']}")
        logger.debug(f"[ModelClientFactory] Anthropic client params: {list(client_params.keys())}")
        logger.debug(f"[ModelClientFactory] Model params: {list(model_params.keys())}")
        
        try:
            client = AsyncAnthropic(**client_params)
            # Attach model parameters to client for easy access
            client._model_params = model_params
            return client
        except Exception as e:
            logger.error(f"[ModelClientFactory] Failed to create Anthropic client: {e}")
            raise
    
    def get_supported_providers(self) -> Dict[str, bool]:
        """
        Get information about which providers are available.
        
        Returns:
            Dictionary mapping provider names to availability status.
        """
        return {
            "openai": OPENAI_AVAILABLE,
            "anthropic": ANTHROPIC_AVAILABLE,
            "gemini": GEMINI_AVAILABLE
        }
    
    def validate_model_support(self, model_name: str) -> Dict[str, Any]:
        """
        Validate if a model is supported and properly configured.
        
        Args:
            model_name: The model name to validate.
            
        Returns:
            Dictionary with validation results.
        """
        provider = self.config.get_provider_for_model(model_name)
        api_key = self.config.get_api_key_for_provider(provider)
        
        result = {
            "model": model_name,
            "provider": provider.value,
            "supported": False,
            "api_key_configured": bool(api_key),
            "client_available": False,
            "issues": []
        }
        
        # Check if client is available
        if provider == ModelProvider.OPENAI and OPENAI_AVAILABLE:
            result["client_available"] = True
        elif provider == ModelProvider.ANTHROPIC and ANTHROPIC_AVAILABLE:
            result["client_available"] = True
        elif provider == ModelProvider.GEMINI and GEMINI_AVAILABLE:
            result["client_available"] = True
        else:
            result["issues"].append(f"Client for {provider.value} not available")
        
        # Check API key
        if not api_key:
            result["issues"].append(f"API key for {provider.value} not configured")
        
        # Overall support
        result["supported"] = result["client_available"] and result["api_key_configured"]
        
        return result
    
    def create_llamaindex_llm(
        self, 
        model_name: str = None, 
        agent_config: AgentConfig = None,
        **override_params
    ) -> Any:
        """
        Create a LlamaIndex LLM instance for the given model.
        
        Handles provider-specific imports and parameter compatibility.
        
        Args:
            model_name: Name of the model. If None, uses default model.
            agent_config: Optional agent configuration with overrides.
            **override_params: Additional parameters to override defaults.
            
        Returns:
            Configured LlamaIndex LLM instance (OpenAI, Anthropic, or Gemini).
        """
        # Use default model if none specified
        if not model_name:
            model_name = self.config.default_model
            logger.debug(f"[ModelClientFactory] No model specified, using default: {model_name}")
        
        # Determine provider and get configuration
        provider = self.config.get_provider_for_model(model_name)
        api_key = self.config.get_api_key_for_provider(provider)
        defaults = self.config.get_defaults_for_provider(provider)
        
        logger.debug(f"[ModelClientFactory] Creating LlamaIndex LLM for model '{model_name}':")
        logger.debug(f"  - Provider: {provider.value}")
        logger.debug(f"  - API key configured: {'✓' if api_key else '✗'}")
        
        if not api_key:
            raise ValueError(f"No API key configured for provider {provider.value} (model: {model_name})")
        
        # Build parameters with precedence: override_params > agent_config > defaults
        params = defaults.copy()
        params.update(override_params)
        
        # Apply agent config overrides if provided
        if agent_config:
            logger.debug(f"[ModelClientFactory] Applying agent configuration overrides")
            
            if agent_config.temperature is not None:
                params["temperature"] = agent_config.temperature
            if agent_config.max_tokens is not None:
                params["max_tokens"] = agent_config.max_tokens
            if agent_config.top_p is not None:
                params["top_p"] = agent_config.top_p
            if agent_config.model_selection is not None:
                old_model = model_name
                model_name = agent_config.model_selection
                logger.debug(f"  - Model override: {old_model} → {model_name}")
                # Re-determine provider if model was overridden
                provider = self.config.get_provider_for_model(model_name)
                api_key = self.config.get_api_key_for_provider(provider)
        
        # Add required parameters
        params.update({
            "model": model_name,
            "api_key": api_key
        })
        
        # Create LLM based on provider
        if provider == ModelProvider.OPENAI:
            return self._create_llamaindex_openai(params)
        elif provider == ModelProvider.ANTHROPIC:
            return self._create_llamaindex_anthropic(params)
        elif provider == ModelProvider.GEMINI:
            return self._create_llamaindex_gemini(params)
        else:
            logger.warning(f"[ModelClientFactory] Unknown provider {provider}, falling back to OpenAI")
            return self._create_llamaindex_openai(params)
    
    def _create_llamaindex_openai(self, params: Dict[str, Any]) -> Any:
        """
        Create a LlamaIndex OpenAI LLM with error handling.
        
        Args:
            params: Dictionary of parameters for the LLM.
            
        Returns:
            Configured LlamaIndex OpenAI LLM instance.
        """
        try:
            from llama_index.llms.openai import OpenAI
        except ImportError as e:
            raise ImportError(
                f"LlamaIndex OpenAI LLM not available: {e}\n"
                f"Install with: uv add llama-index-llms-openai"
            )
        
        logger.info(f"[ModelClientFactory] Creating LlamaIndex OpenAI LLM for model: {params['model']}")
        
        # Try with all parameters
        try:
            return OpenAI(**params)
        except TypeError as e:
            # Remove unsupported parameters and retry
            logger.warning(f"[ModelClientFactory] Parameter error: {e}, retrying without problematic params")
            return self._retry_without_unsupported_params(OpenAI, params, e)
    
    def _create_llamaindex_anthropic(self, params: Dict[str, Any]) -> Any:
        """
        Create a LlamaIndex Anthropic LLM with error handling.
        
        Args:
            params: Dictionary of parameters for the LLM.
            
        Returns:
            Configured LlamaIndex Anthropic LLM instance.
        """
        try:
            from llama_index.llms.anthropic import Anthropic
        except ImportError as e:
            raise ImportError(
                f"LlamaIndex Anthropic LLM not available: {e}\n"
                f"Install with: uv add llama-index-llms-anthropic"
            )
        
        logger.info(f"[ModelClientFactory] Creating LlamaIndex Anthropic LLM for model: {params['model']}")
        
        # Try with all parameters
        try:
            return Anthropic(**params)
        except TypeError as e:
            # Remove unsupported parameters and retry
            logger.warning(f"[ModelClientFactory] Parameter error: {e}, retrying without problematic params")
            return self._retry_without_unsupported_params(Anthropic, params, e)
    
    def _create_llamaindex_gemini(self, params: Dict[str, Any]) -> Any:
        """
        Create a LlamaIndex Gemini LLM with error handling.
        
        Args:
            params: Dictionary of parameters for the LLM.
            
        Returns:
            Configured LlamaIndex Gemini LLM instance.
        """
        try:
            from llama_index.llms.gemini import Gemini
        except ImportError as e:
            raise ImportError(
                f"LlamaIndex Gemini LLM not available: {e}\n"
                f"Install with: uv add llama-index-llms-gemini"
            )
        
        logger.info(f"[ModelClientFactory] Creating LlamaIndex Gemini LLM for model: {params['model']}")
        
        # Try with all parameters
        try:
            return Gemini(**params)
        except TypeError as e:
            # Remove unsupported parameters and retry
            logger.warning(f"[ModelClientFactory] Parameter error: {e}, retrying without problematic params")
            return self._retry_without_unsupported_params(Gemini, params, e)
    
    def _retry_without_unsupported_params(
        self, 
        llm_class: Type, 
        params: Dict[str, Any], 
        error: TypeError
    ) -> Any:
        """
        Retry LLM creation by removing unsupported parameters.
        
        Parses the TypeError message to identify problematic parameters
        and removes them before retrying.
        
        Args:
            llm_class: The LLM class to instantiate.
            params: Dictionary of parameters.
            error: The TypeError that was raised.
            
        Returns:
            Configured LLM instance.
            
        Raises:
            TypeError: If the error message cannot be parsed or retry fails.
        """
        # Extract parameter name from error message
        # e.g., "unexpected keyword argument 'temperature'"
        # or "__init__() got an unexpected keyword argument 'temperature'"
        match = re.search(r"(?:unexpected keyword argument|got an unexpected keyword argument)\s+'(\w+)'", str(error))
        
        if match:
            param_to_remove = match.group(1)
            logger.info(f"[ModelClientFactory] Removing unsupported parameter: {param_to_remove}")
            params_copy = params.copy()
            params_copy.pop(param_to_remove, None)
            
            try:
                return llm_class(**params_copy)
            except TypeError as retry_error:
                # If we still get an error, try removing another parameter
                logger.warning(f"[ModelClientFactory] Still getting error after removing {param_to_remove}: {retry_error}")
                return self._retry_without_unsupported_params(llm_class, params_copy, retry_error)
        else:
            # Can't parse error, raise original
            logger.error(f"[ModelClientFactory] Cannot parse TypeError message: {error}")
            raise error

# Global factory instance
client_factory = ModelClientFactory() 