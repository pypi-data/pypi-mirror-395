"""
Multi-Provider Model Configuration Manager

Handles configuration for multiple AI providers (OpenAI, Gemini, etc.)
and automatically selects the correct client based on the model name.

This module provides:
- Automatic model provider detection based on model names
- Environment variable-based configuration
- Default model mappings with override capabilities
- Fallback provider configuration
- Per-provider default parameters

Environment Variables:
- OPENAI_API_KEY: OpenAI API key
- GEMINI_API_KEY: Google Gemini API key
- DEFAULT_MODEL: Default model to use (default: "gpt-4")
- OPENAI_MODELS: Comma-separated list of OpenAI model names
- GEMINI_MODELS: Comma-separated list of Gemini model names
- FALLBACK_PROVIDER: Provider to use when model provider is unknown
- *_DEFAULT_TEMPERATURE: Default temperature for each provider
- *_DEFAULT_TIMEOUT: Default timeout for each provider
- *_DEFAULT_MAX_RETRIES: Default max retries for each provider

Example:
    ```python
    from agent_framework.model_config import model_config
    
    # Get provider for a model
    provider = model_config.get_provider("gpt-4")
    
    # Get API key for a provider
    api_key = model_config.get_api_key(provider)
    ```
"""

import os
import logging
from typing import Dict, List, Optional, Union, Any, Final
from enum import Enum

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file
except ImportError:
    pass  # dotenv not available, skip

logger = logging.getLogger(__name__)

class ModelProvider(Enum):
    """
    Supported model providers.
    
    Attributes:
        OPENAI: OpenAI GPT models
        ANTHROPIC: Anthropic Claude models
        GEMINI: Google Gemini models
        UNKNOWN: Unknown or unsupported provider
    """
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    UNKNOWN = "unknown"

class ModelConfigManager:
    """
    Manages configuration for multiple AI model providers.
    
    This class automatically determines the correct provider and API key based on model name,
    loads configuration from environment variables, and provides default parameters for each provider.
    
    Attributes:
        openai_api_key: OpenAI API key from environment
        gemini_api_key: Google Gemini API key from environment
        default_model: Default model name to use
        openai_models: List of recognized OpenAI model names
        gemini_models: List of recognized Gemini model names
        fallback_provider: Provider to use when model provider is unknown
        openai_defaults: Default parameters for OpenAI models
        gemini_defaults: Default parameters for Gemini models
    """
    
    # Default model mappings (can be overridden by environment variables)
    DEFAULT_OPENAI_MODELS: Final[List[str]] = [
        "gpt-5.1","gpt-5", "gpt-5-mini","gpt-5-nano",
        "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini",
        "gpt-3.5-turbo", "gpt-3.5-turbo-16k",
        "o1-preview", "o1-mini"
    ]
    
    DEFAULT_ANTHROPIC_MODELS: Final[List[str]] = [
        "claude-haiku-4-5-20251001", "claude-sonnet-4-5-20250929", "claude-opus-4-1-20250805",
        "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307",
        "claude-3-5-sonnet-20240620", "claude-3-5-sonnet-20241022",
        "claude-2.1", "claude-2.0", "claude-instant-1.2"
    ]
    
    DEFAULT_GEMINI_MODELS: Final[List[str]] = [
        
        "gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp",
        "gemini-2.5-flash-preview-04-17", "gemini-pro", "gemini-pro-vision"
    ]
    
    def __init__(self) -> None:
        """
        Initialize the configuration manager.
        
        Loads configuration from environment variables and sets up default parameters.
        Automatically initializes Elasticsearch support if ELASTICSEARCH_ENABLED=true.
        """
        self.openai_api_key: str = ""
        self.anthropic_api_key: str = ""
        self.gemini_api_key: str = ""
        self.default_model: str = ""
        self.openai_models: List[str] = []
        self.anthropic_models: List[str] = []
        self.gemini_models: List[str] = []
        self.fallback_provider: ModelProvider = ModelProvider.OPENAI
        self.openai_defaults: Dict[str, Union[float, int]] = {}
        self.anthropic_defaults: Dict[str, Union[float, int]] = {}
        self.gemini_defaults: Dict[str, Union[float, int]] = {}
        
        # Elasticsearch support (transparent)
        self._es_config_provider: Optional[Any] = None
        self._hardcoded_configs: Dict[str, Dict[str, Any]] = {}
        self._es_enabled: bool = False
        
        self._load_configuration()
        self._auto_init_elasticsearch()
    
    def _load_configuration(self) -> None:
        """
        Load configuration from environment variables.
        
        Reads API keys, model mappings, default parameters, and fallback settings
        from environment variables with sensible defaults.
        """
        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
        # Default model
        self.default_model = os.getenv("DEFAULT_MODEL", "gpt-4")
        
        # Model mappings from environment (with fallbacks to defaults)
        openai_models_str = os.getenv("OPENAI_MODELS", "")
        anthropic_models_str = os.getenv("ANTHROPIC_MODELS", "")
        gemini_models_str = os.getenv("GEMINI_MODELS", "")
        
        self.openai_models = (
            [m.strip() for m in openai_models_str.split(",") if m.strip()]
            if openai_models_str else self.DEFAULT_OPENAI_MODELS
        )
        
        self.anthropic_models = (
            [m.strip() for m in anthropic_models_str.split(",") if m.strip()]
            if anthropic_models_str else self.DEFAULT_ANTHROPIC_MODELS
        )
        
        self.gemini_models = (
            [m.strip() for m in gemini_models_str.split(",") if m.strip()]
            if gemini_models_str else self.DEFAULT_GEMINI_MODELS
        )
        
        # Fallback provider
        fallback_str = os.getenv("FALLBACK_PROVIDER", "openai").lower()
        self.fallback_provider = ModelProvider.OPENAI if fallback_str == "openai" else ModelProvider.GEMINI
        
        # Default parameters
        self.openai_defaults = {
            "temperature": float(os.getenv("OPENAI_DEFAULT_TEMPERATURE", "0.7")),
            "timeout": int(os.getenv("OPENAI_DEFAULT_TIMEOUT", "120")),
            "max_retries": int(os.getenv("OPENAI_DEFAULT_MAX_RETRIES", "3"))
        }
        
        self.anthropic_defaults = {
            "temperature": float(os.getenv("ANTHROPIC_DEFAULT_TEMPERATURE", "0.7")),
            "timeout": int(os.getenv("ANTHROPIC_DEFAULT_TIMEOUT", "120")),
            "max_retries": int(os.getenv("ANTHROPIC_DEFAULT_MAX_RETRIES", "3"))
        }
        
        self.gemini_defaults = {
            "temperature": float(os.getenv("GEMINI_DEFAULT_TEMPERATURE", "0.7")),
            "timeout": int(os.getenv("GEMINI_DEFAULT_TIMEOUT", "120")),
            "max_retries": int(os.getenv("GEMINI_DEFAULT_MAX_RETRIES", "3"))
        }
        
        logger.info(f"[ModelConfigManager] Loaded configuration:")
        logger.info(f"  - Default model: {self.default_model}")
        logger.info(f"  - OpenAI models: {len(self.openai_models)} configured")
        logger.info(f"  - Anthropic models: {len(self.anthropic_models)} configured")
        logger.info(f"  - Gemini models: {len(self.gemini_models)} configured") 
        logger.info(f"  - Fallback provider: {self.fallback_provider.value}")
        
        # DEBUG logging for detailed configuration
        logger.debug(f"[ModelConfigManager] Detailed configuration:")
        logger.debug(f"  - OpenAI API key configured: {'✓' if self.openai_api_key else '✗'}")
        logger.debug(f"  - Anthropic API key configured: {'✓' if self.anthropic_api_key else '✗'}")
        logger.debug(f"  - Gemini API key configured: {'✓' if self.gemini_api_key else '✗'}")
        logger.debug(f"  - OpenAI models: {self.openai_models}")
        logger.debug(f"  - Anthropic models: {self.anthropic_models}")
        logger.debug(f"  - Gemini models: {self.gemini_models}")
        logger.debug(f"  - OpenAI defaults: {self.openai_defaults}")
        logger.debug(f"  - Anthropic defaults: {self.anthropic_defaults}")
        logger.debug(f"  - Gemini defaults: {self.gemini_defaults}")
    
    def get_provider_for_model(self, model_name: str) -> ModelProvider:
        """
        Determine the provider for a given model name.
        
        Args:
            model_name: The name of the model
            
        Returns:
            ModelProvider enum indicating the provider
        """
        if not model_name:
            logger.debug(f"[ModelConfigManager] Empty model name, using fallback provider: {self.fallback_provider.value}")
            return self.fallback_provider
        
        model_lower = model_name.lower()
        
        # Check OpenAI models
        for openai_model in self.openai_models:
            if model_lower == openai_model.lower():
                logger.debug(f"[ModelConfigManager] Model '{model_name}' matched OpenAI model '{openai_model}'")
                return ModelProvider.OPENAI
        
        # Check Anthropic models
        for anthropic_model in self.anthropic_models:
            if model_lower == anthropic_model.lower():
                logger.debug(f"[ModelConfigManager] Model '{model_name}' matched Anthropic model '{anthropic_model}'")
                return ModelProvider.ANTHROPIC
        
        # Check Gemini models  
        for gemini_model in self.gemini_models:
            if model_lower == gemini_model.lower():
                logger.debug(f"[ModelConfigManager] Model '{model_name}' matched Gemini model '{gemini_model}'")
                return ModelProvider.GEMINI
        
        # Pattern-based detection as fallback
        if any(pattern in model_lower for pattern in ["gpt", "o1"]):
            logger.debug(f"[ModelConfigManager] Model '{model_name}' matched OpenAI pattern")
            return ModelProvider.OPENAI
        elif any(pattern in model_lower for pattern in ["claude"]):
            logger.debug(f"[ModelConfigManager] Model '{model_name}' matched Anthropic pattern")
            return ModelProvider.ANTHROPIC
        elif any(pattern in model_lower for pattern in ["gemini", "bison", "gecko"]):
            logger.debug(f"[ModelConfigManager] Model '{model_name}' matched Gemini pattern")
            return ModelProvider.GEMINI
        
        logger.warning(f"[ModelConfigManager] Unknown model '{model_name}', using fallback provider: {self.fallback_provider.value}")
        return self.fallback_provider
    
    def get_api_key_for_provider(self, provider: ModelProvider) -> str:
        """
        Get the API key for a specific provider.
        
        Args:
            provider: The provider to get the API key for
            
        Returns:
            The API key string
        """
        if provider == ModelProvider.OPENAI:
            return self.openai_api_key
        elif provider == ModelProvider.ANTHROPIC:
            return self.anthropic_api_key
        elif provider == ModelProvider.GEMINI:
            return self.gemini_api_key
        else:
            logger.warning(f"[ModelConfigManager] Unknown provider: {provider}")
            return ""
    
    def get_api_key_for_model(self, model_name: str) -> str:
        """
        Get the appropriate API key for a given model.
        
        Args:
            model_name: The name of the model
            
        Returns:
            The appropriate API key
        """
        provider = self.get_provider_for_model(model_name)
        return self.get_api_key_for_provider(provider)
    
    def get_defaults_for_provider(self, provider: ModelProvider) -> Dict[str, Any]:
        """
        Get default parameters for a specific provider.
        
        Args:
            provider: The provider to get defaults for
            
        Returns:
            Dictionary of default parameters
        """
        if provider == ModelProvider.OPENAI:
            return self.openai_defaults.copy()
        elif provider == ModelProvider.ANTHROPIC:
            return self.anthropic_defaults.copy()
        elif provider == ModelProvider.GEMINI:
            return self.gemini_defaults.copy()
        else:
            return self.openai_defaults.copy()  # Fallback to OpenAI defaults
    
    def get_defaults_for_model(self, model_name: str) -> Dict[str, Any]:
        """
        Get default parameters for a given model.
        
        Args:
            model_name: The name of the model
            
        Returns:
            Dictionary of default parameters
        """
        provider = self.get_provider_for_model(model_name)
        return self.get_defaults_for_provider(provider)
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate the current configuration and return status.
        
        Returns:
            Dictionary with validation results
        """
        status = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "providers": {}
        }
        
        # Check API keys
        if not self.openai_api_key:
            status["warnings"].append("OpenAI API key not configured")
        else:
            status["providers"]["openai"] = "configured"
        
        if not self.anthropic_api_key:
            status["warnings"].append("Anthropic API key not configured")
        else:
            status["providers"]["anthropic"] = "configured"
        
        if not self.gemini_api_key:
            status["warnings"].append("Gemini API key not configured") 
        else:
            status["providers"]["gemini"] = "configured"
        
        if not self.openai_api_key and not self.anthropic_api_key and not self.gemini_api_key:
            status["valid"] = False
            status["errors"].append("No API keys configured")
        
        # Check default model
        default_provider = self.get_provider_for_model(self.default_model)
        default_key = self.get_api_key_for_provider(default_provider)
        if not default_key:
            status["valid"] = False
            status["errors"].append(f"Default model '{self.default_model}' requires {default_provider.value} API key which is not configured")
        
        return status
    
    def get_model_list(self) -> Dict[str, List[str]]:
        """
        Get all configured models by provider.
        
        Returns:
            Dictionary mapping provider names to model lists
        """
        return {
            "openai": self.openai_models.copy(),
            "anthropic": self.anthropic_models.copy(),
            "gemini": self.gemini_models.copy()
        }
    
    def _auto_init_elasticsearch(self) -> None:
        """
        Automatically initialize Elasticsearch support if enabled via environment variable.
        
        This is called during __init__ and is transparent to the user.
        """
        es_enabled_raw = os.getenv("ELASTICSEARCH_ENABLED", "NOT_SET")
        logger.debug(f"[ModelConfigManager] ELASTICSEARCH_ENABLED raw value = '{es_enabled_raw}'")
        
        self._es_enabled = es_enabled_raw.lower() == "true"
        logger.debug(f"[ModelConfigManager] _es_enabled = {self._es_enabled}")
        
        if not self._es_enabled:
            logger.debug("[ModelConfigManager] Elasticsearch support disabled (ELASTICSEARCH_ENABLED not set to true)")
            return
        
        logger.info("[ModelConfigManager] Elasticsearch support enabled, initializing config provider...")
        
        # Note: Actual initialization happens async in _ensure_es_provider_initialized()
        # This just sets the flag
    
    async def _ensure_es_provider_initialized(self) -> bool:
        """
        Ensure Elasticsearch config provider is initialized (lazy initialization).
        
        Returns:
            True if provider is available, False otherwise
        """
        if not self._es_enabled:
            return False
        
        if self._es_config_provider is not None:
            return True
        
        try:
            from agent_framework.core.elasticsearch_config_provider import ElasticsearchConfigProvider
            
            self._es_config_provider = ElasticsearchConfigProvider(
                index_name=os.getenv("ELASTICSEARCH_CONFIG_INDEX", "agent-configs"),
                cache_ttl=int(os.getenv("ELASTICSEARCH_CONFIG_CACHE_TTL", "300")),
                cache_max_size=int(os.getenv("ELASTICSEARCH_CONFIG_CACHE_MAX_SIZE", "100"))
            )
            
            await self._es_config_provider.initialize()
            
            logger.info("[ModelConfigManager] Elasticsearch config provider initialized successfully")
            return True
        
        except Exception as e:
            logger.warning(
                f"[ModelConfigManager] Failed to initialize Elasticsearch config provider: {e}. "
                "Will use fallback configurations."
            )
            self._es_enabled = False  # Disable to avoid repeated attempts
            return False
    
    def register_agent_config(self, agent_id: str, config: Dict[str, Any]) -> None:
        """
        Register a hardcoded configuration for an agent.
        
        This provides a fallback when Elasticsearch is unavailable or doesn't have
        a configuration for the agent.
        
        Args:
            agent_id: Agent identifier
            config: Configuration dictionary with keys like system_prompt, model_name, model_config
        
        Example:
            ```python
            model_config.register_agent_config("my-agent", {
                "system_prompt": "You are a helpful assistant.",
                "model_name": "gpt-4o",
                "model_config": {"temperature": 0.7, "max_tokens": 2000}
            })
            ```
        """
        self._hardcoded_configs[agent_id] = config
        logger.debug(f"[ModelConfigManager] Registered hardcoded config for agent_id={agent_id}")
    
    def _get_hardcoded_agent_config(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get hardcoded configuration for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Hardcoded configuration if available, None otherwise
        """
        return self._hardcoded_configs.get(agent_id)
    
    def _get_default_agent_config(self) -> Dict[str, Any]:
        """
        Get default framework configuration for an agent.
        
        Returns:
            Default configuration dictionary
        """
        return {
            "system_prompt": "You are a helpful AI assistant.",
            "model_name": self.default_model,
            "model_config": {
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
    
    def _merge_configs(self, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two configurations, with override_config taking precedence.
        
        Performs deep merge for nested dictionaries like model_config.
        Missing fields in override_config are filled from base_config.
        
        Args:
            base_config: Base configuration (lower priority)
            override_config: Override configuration (higher priority)
            
        Returns:
            Merged configuration dictionary
        """
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # Deep merge for nested dicts
                merged[key] = self._merge_configs(merged[key], value)
            else:
                # Override value
                merged[key] = value
        
        return merged
    
    async def get_agent_configuration(self, agent_id: str, doc_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get effective configuration for an agent with priority resolution and config merging.
        
        Priority order (highest to lowest):
        1. Elasticsearch (if available and active=true, or specific doc_id provided)
        2. Hardcoded configuration (registered via register_agent_config)
        3. Framework defaults
        
        Configurations are merged, so missing fields in higher priority configs
        are automatically filled from lower priority configs.
        
        This is transparent - Elasticsearch support is automatic if ELASTICSEARCH_ENABLED=true.
        
        Args:
            agent_id: Agent identifier
            doc_id: Optional Elasticsearch document ID for retrieving a specific config version
            
        Returns:
            Effective configuration dictionary with all required fields
            
        Example:
            ```python
            # Automatically uses ES if available, otherwise fallback
            config = await model_config.get_agent_configuration("my-agent")
            print(config["model_name"])  # Always present
            print(config["system_prompt"])  # Always present
            
            # Get specific version by doc_id
            config = await model_config.get_agent_configuration("my-agent", doc_id="abc123")
            ```
        """
        # Start with default config as base
        default_config = self._get_default_agent_config()
        effective_config = default_config.copy()
        config_source = "default"
        
        # Try hardcoded configuration (Priority 2)
        hardcoded_config = self._get_hardcoded_agent_config(agent_id)
        
        if hardcoded_config is not None:
            # Merge hardcoded over defaults
            effective_config = self._merge_configs(effective_config, hardcoded_config)
            config_source = "hardcoded"
            logger.debug(f"[ModelConfigManager] Merged hardcoded config for agent_id={agent_id}")
        
        # Try Elasticsearch (Priority 1)
        if await self._ensure_es_provider_initialized():
            try:
                es_config = None
                
                # If doc_id is provided, retrieve specific document
                if doc_id:
                    try:
                        # Get document by ID directly from Elasticsearch
                        result = await self._es_config_provider.client.get(
                            index=self._es_config_provider.index_name,
                            id=doc_id
                        )
                        if result and result.get("found"):
                            es_config = result["_source"].get("config")
                            logger.info(
                                f"[ModelConfigManager] Retrieved config by doc_id={doc_id} "
                                f"(version={result['_source'].get('version', 'unknown')})"
                            )
                    except Exception as e:
                        logger.warning(
                            f"[ModelConfigManager] Failed to get config by doc_id={doc_id}: {e}. "
                            "Falling back to active config."
                        )
                
                # If no doc_id or doc_id retrieval failed, get active config
                if es_config is None:
                    es_config = await self._es_config_provider.get_agent_config(agent_id)
                
                if es_config is not None:
                    # Merge ES config over hardcoded/defaults
                    effective_config = self._merge_configs(effective_config, es_config)
                    config_source = "elasticsearch"
                    logger.info(
                        f"[ModelConfigManager] Using Elasticsearch config for agent_id={agent_id} "
                        "(merged with fallback configs)"
                    )
                else:
                    logger.debug(
                        f"[ModelConfigManager] No active Elasticsearch config for agent_id={agent_id}, "
                        f"using {config_source} config"
                    )
            
            except Exception as e:
                logger.warning(
                    f"[ModelConfigManager] Failed to get Elasticsearch config for agent_id={agent_id}: {e}. "
                    f"Using {config_source} configuration."
                )
        
        # Add source metadata for debugging
        effective_config["_source"] = config_source
        
        logger.info(
            f"[ModelConfigManager] Final config for agent_id={agent_id}: "
            f"source={config_source}, model={effective_config.get('model_name', 'unknown')}"
        )
        
        return effective_config

# Global instance
model_config = ModelConfigManager() 