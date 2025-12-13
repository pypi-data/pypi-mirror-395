"""
universal_agent_nexus.adapters.langgraph.factory

LLM Factory for LangChain chat model instantiation.

Implements provider routing based on connection strings:
- openai://gpt-4o-mini (or just "gpt-4o-mini")
- ollama://llama3
- local://qwen3 (OpenAI-compatible local server like LM Studio, vLLM)
- anthropic://claude-3-sonnet

This is LangChain-specific. For UAA kernel runtime, use ContractRegistry.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

# Import base class that all LangChain chat models inherit from
try:
    from langchain_core.language_models.chat_models import BaseChatModel
except ImportError as exc:
    raise ImportError(
        "Install 'universal-agent-nexus[langgraph]' to use the LLM factory."
    ) from exc

# Provider-specific imports (optional - fail gracefully)
try:
    from langchain_openai import ChatOpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    ChatOpenAI = None
    _OPENAI_AVAILABLE = False

try:
    from langchain_ollama import ChatOllama
    _OLLAMA_AVAILABLE = True
except ImportError:
    ChatOllama = None
    _OLLAMA_AVAILABLE = False

try:
    from langchain_anthropic import ChatAnthropic
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    ChatAnthropic = None
    _ANTHROPIC_AVAILABLE = False

logger = logging.getLogger(__name__)


class LLMFactory:
    """
    Factory for creating LangChain chat models based on provider prefixes.
    
    Supports connection string format: provider://model_name
    
    Examples:
        LLMFactory.create("gpt-4o-mini")           # OpenAI (default)
        LLMFactory.create("openai://gpt-4o")       # OpenAI explicit
        LLMFactory.create("ollama://llama3")       # Ollama
        LLMFactory.create("local://qwen3")         # Local OpenAI-compatible
        LLMFactory.create("anthropic://claude-3-sonnet")  # Anthropic
    
    Config options:
        temperature: float (default 0.2)
        base_url: str (override endpoint)
        api_key: str (override env var)
    """

    # Default local server URL (LM Studio, vLLM, etc.)
    DEFAULT_LOCAL_URL = "http://localhost:1234/v1"
    
    # Default Ollama URL
    DEFAULT_OLLAMA_URL = "http://localhost:11434"

    @staticmethod
    def create(model_str: str, config: Optional[Dict[str, Any]] = None) -> BaseChatModel:
        """
        Create a LangChain chat model from a connection string.
        
        Args:
            model_str: Model identifier, optionally with provider prefix
                       e.g., "gpt-4o-mini", "ollama://llama3"
            config: Optional configuration dict with:
                    - temperature: float
                    - base_url: str
                    - api_key: str
        
        Returns:
            LangChain BaseChatModel instance
        
        Raises:
            ValueError: If provider is not supported
            ImportError: If required provider package is not installed
        """
        config = config or {}
        
        # Parse connection string: provider://model_name
        if "://" in model_str:
            provider, model_name = model_str.split("://", 1)
            provider = provider.lower()
        else:
            # Default to OpenAI if no prefix (backward compatibility)
            provider = "openai"
            model_name = model_str

        logger.debug("Creating LLM: provider=%s, model=%s", provider, model_name)

        # Dispatch to provider-specific factory method
        if provider == "openai":
            return LLMFactory._create_openai(model_name, config)
        
        elif provider == "ollama":
            return LLMFactory._create_ollama(model_name, config)
        
        elif provider == "local":
            # "local://" uses OpenAI-compatible API (LM Studio, vLLM, Ollama OpenAI mode)
            return LLMFactory._create_local(model_name, config)
        
        elif provider == "anthropic":
            return LLMFactory._create_anthropic(model_name, config)
        
        else:
            raise ValueError(
                f"Unsupported LLM provider: '{provider}' in model '{model_str}'. "
                f"Supported: openai, ollama, local, anthropic"
            )

    @staticmethod
    def _create_openai(model: str, config: Dict[str, Any]) -> BaseChatModel:
        """Create OpenAI chat model."""
        if not _OPENAI_AVAILABLE:
            raise ImportError(
                "langchain-openai is not installed. "
                "Install with: pip install langchain-openai"
            )
        
        return ChatOpenAI(
            model=model,
            temperature=config.get("temperature", 0.2),
            api_key=config.get("api_key") or os.environ.get("OPENAI_API_KEY"),
            base_url=config.get("base_url"),  # None uses default OpenAI endpoint
        )

    @staticmethod
    def _create_local(model: str, config: Dict[str, Any]) -> BaseChatModel:
        """
        Create a chat model for local OpenAI-compatible servers.
        
        Works with: LM Studio, vLLM, Ollama (OpenAI mode), LocalAI, etc.
        """
        if not _OPENAI_AVAILABLE:
            raise ImportError(
                "langchain-openai is not installed. "
                "Install with: pip install langchain-openai"
            )
        
        base_url = config.get("base_url", LLMFactory.DEFAULT_LOCAL_URL)
        logger.info("Using local LLM server at %s with model %s", base_url, model)
        
        return ChatOpenAI(
            model=model,
            temperature=config.get("temperature", 0.2),
            api_key=config.get("api_key", "not-needed"),  # Local servers usually ignore
            base_url=base_url,
        )

    @staticmethod
    def _create_ollama(model: str, config: Dict[str, Any]) -> BaseChatModel:
        """Create Ollama chat model using native LangChain Ollama integration."""
        if not _OLLAMA_AVAILABLE:
            raise ImportError(
                "langchain-ollama is not installed. "
                "Install with: pip install langchain-ollama"
            )
        
        base_url = config.get("base_url", LLMFactory.DEFAULT_OLLAMA_URL)
        logger.info("Using Ollama at %s with model %s", base_url, model)
        
        return ChatOllama(
            model=model,
            temperature=config.get("temperature", 0.2),
            base_url=base_url,
        )

    @staticmethod
    def _create_anthropic(model: str, config: Dict[str, Any]) -> BaseChatModel:
        """Create Anthropic chat model."""
        if not _ANTHROPIC_AVAILABLE:
            raise ImportError(
                "langchain-anthropic is not installed. "
                "Install with: pip install langchain-anthropic"
            )
        
        return ChatAnthropic(
            model=model,
            temperature=config.get("temperature", 0.2),
            api_key=config.get("api_key") or os.environ.get("ANTHROPIC_API_KEY"),
        )

    @staticmethod
    def is_provider_available(provider: str) -> bool:
        """Check if a provider's dependencies are installed."""
        availability = {
            "openai": _OPENAI_AVAILABLE,
            "local": _OPENAI_AVAILABLE,  # Uses ChatOpenAI
            "ollama": _OLLAMA_AVAILABLE,
            "anthropic": _ANTHROPIC_AVAILABLE,
        }
        return availability.get(provider.lower(), False)

    @staticmethod
    def list_available_providers() -> list[str]:
        """List all providers with installed dependencies."""
        providers = []
        if _OPENAI_AVAILABLE:
            providers.extend(["openai", "local"])
        if _OLLAMA_AVAILABLE:
            providers.append("ollama")
        if _ANTHROPIC_AVAILABLE:
            providers.append("anthropic")
        return providers

