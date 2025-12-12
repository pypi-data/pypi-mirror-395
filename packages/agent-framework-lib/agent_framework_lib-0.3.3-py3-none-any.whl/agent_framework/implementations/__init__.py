"""
Framework-specific agent implementations.

This module contains concrete implementations of the BaseAgent class
for different AI agent frameworks (LlamaIndex, Microsoft Agent Framework, etc.).
"""

from .llamaindex_agent import LlamaIndexAgent
from .microsoft_agent import MicrosoftAgent

__all__ = ["LlamaIndexAgent", "MicrosoftAgent"]
