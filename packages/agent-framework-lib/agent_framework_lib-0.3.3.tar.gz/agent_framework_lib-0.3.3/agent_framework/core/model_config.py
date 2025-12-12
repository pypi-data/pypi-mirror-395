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
        
        self._load_configuration()
    
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

# Global instance
model_config = ModelConfigManager() 