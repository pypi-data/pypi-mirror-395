"""
Paved OpenAI API Wrapper.

This module provides a drop-in replacement for the openai library
that automatically enforces Paved policies.
"""
import os
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator
from openai import OpenAI as OriginalOpenAI
from openai import AsyncOpenAI as OriginalAsyncOpenAI
from openai import Stream, AsyncStream

from pvd.sdk import Agent

class PavedOpenAIWrapper:
    """Mixin for OpenAI wrappers to add policy enforcement."""

    def __init__(
        self,
        agent_id: str = "openai-agent",
        paved_api_key: str = None,
        paved_url: str = None,
        paved_policies: List[str] = None,
        paved_policy: Dict[str, Any] = None,
        **kwargs
    ):
        # Initialize Paved agent
        self._paved = Agent(
            agent_id=agent_id,
            policies=paved_policies or [],
            policy_config=paved_policy,
            base_url=paved_url or os.getenv("PAVED_URL", "http://localhost:8000"),
            api_key=paved_api_key or os.getenv("PAVED_API_KEY")
        )

class PavedOpenAICompletions:
    """Wrapper for OpenAI completions with policy enforcement."""

    def __init__(self, original_completions, paved_agent):
        self._original = original_completions
        self._paved = paved_agent

    def _extract_user_content(self, messages: List[Dict]) -> str:
        """Extract user message content for policy checks."""
        return "\n".join([
            m.get("content", "") for m in messages
            if isinstance(m, dict) and m.get("role") == "user"
        ])

    def _build_policy_payload(self, **kwargs) -> Dict[str, Any]:
        """Build comprehensive policy payload."""
        messages = kwargs.get("messages", [])
        return {
            "text": self._extract_user_content(messages),
            "messages": messages,
            "model": kwargs.get("model", "unknown"),
            "max_tokens": kwargs.get("max_tokens"),
            "temperature": kwargs.get("temperature"),
            "top_p": kwargs.get("top_p"),
            "frequency_penalty": kwargs.get("frequency_penalty"),
            "presence_penalty": kwargs.get("presence_penalty"),
            "tool_choice": kwargs.get("tool_choice"),
            "tools": kwargs.get("tools"),
            "response_format": kwargs.get("response_format"),
            "stream": kwargs.get("stream", False),
            "framework": "openai"
        }

    def create(self, **kwargs):
        """
        Create chat completion with policy enforcement.

        Supports all OpenAI parameters including streaming, tools, and response formats.
        """
        # Build and check policy
        payload = self._build_policy_payload(**kwargs)
        self._paved.check("llm", payload)

        # Call original OpenAI API
        return self._original.create(**kwargs)

class PavedOpenAIChat:
    """Wrapper for OpenAI chat with policy enforcement."""

    def __init__(self, original_chat, paved_agent):
        self.completions = PavedOpenAICompletions(original_chat.completions, paved_agent)


class PavedOpenAIEmbeddings:
    """Wrapper for OpenAI embeddings with policy enforcement."""

    def __init__(self, original_embeddings, paved_agent):
        self._original = original_embeddings
        self._paved = paved_agent

    def create(self, **kwargs):
        """
        Create embeddings with policy enforcement.

        Args:
            input: Text or list of texts to embed
            model: Embedding model (e.g., "text-embedding-ada-002")
            **kwargs: Additional OpenAI parameters

        Returns:
            OpenAI CreateEmbeddingResponse object
        """
        input_text = kwargs.get("input", "")
        model = kwargs.get("model", "unknown")

        # Handle both string and list inputs
        if isinstance(input_text, list):
            text_content = " ".join(input_text)
        else:
            text_content = input_text

        payload = {
            "text": text_content,
            "input": input_text,
            "model": model,
            "encoding_format": kwargs.get("encoding_format"),
            "framework": "openai",
            "action": "embedding"
        }

        # Policy check
        self._paved.check("embedding", payload)

        # Call original OpenAI API
        return self._original.create(**kwargs)


class OpenAI(OriginalOpenAI, PavedOpenAIWrapper):
    def __init__(
        self,
        agent_id: str = "openai-agent",
        paved_api_key: str = None,
        paved_url: str = None,
        paved_policies: List[str] = None,
        paved_policy: Dict[str, Any] = None,
        _paved: Optional[Agent] = None,
        **kwargs
    ):
        # Remove internal args from kwargs if they somehow got there (though explicit args handle most)
        # _paved is used for testing injection
        
        super().__init__(**kwargs)
        PavedOpenAIWrapper.__init__(
            self, 
            agent_id=agent_id, 
            paved_api_key=paved_api_key, 
            paved_url=paved_url,
            paved_policies=paved_policies,
            paved_policy=paved_policy
        )
        # If injected agent is provided (for testing), use it
        if _paved:
            self._paved = _paved

        # Wrap chat and embeddings APIs
        self.chat = PavedOpenAIChat(super().chat, self._paved)
        self.embeddings = PavedOpenAIEmbeddings(super().embeddings, self._paved)

class AsyncPavedOpenAICompletions:
    """Async wrapper for OpenAI completions with policy enforcement."""

    def __init__(self, original_completions, paved_agent):
        self._original = original_completions   
        self._paved = paved_agent

    def _extract_user_content(self, messages: List[Dict]) -> str:
        """Extract user message content for policy checks."""
        return "\n".join([
            m.get("content", "") for m in messages
            if isinstance(m, dict) and m.get("role") == "user"
        ])

    def _build_policy_payload(self, **kwargs) -> Dict[str, Any]:
        """Build comprehensive policy payload."""
        messages = kwargs.get("messages", [])
        return {
            "text": self._extract_user_content(messages),
            "messages": messages,
            "model": kwargs.get("model", "unknown"),
            "max_tokens": kwargs.get("max_tokens"),
            "temperature": kwargs.get("temperature"),
            "top_p": kwargs.get("top_p"),
            "frequency_penalty": kwargs.get("frequency_penalty"),
            "presence_penalty": kwargs.get("presence_penalty"),
            "tool_choice": kwargs.get("tool_choice"),
            "tools": kwargs.get("tools"),
            "response_format": kwargs.get("response_format"),
            "stream": kwargs.get("stream", False),
            "framework": "openai"
        }

    async def create(self, **kwargs):
        """Async create chat completion with policy enforcement."""
        # Build and check policy (sync for now)
        payload = self._build_policy_payload(**kwargs)
        self._paved.check("llm", payload)

        # Call async OpenAI API
        return await self._original.create(**kwargs)


class AsyncPavedOpenAIChat:
    """Async wrapper for OpenAI chat with policy enforcement."""

    def __init__(self, original_chat, paved_agent):
        self.completions = AsyncPavedOpenAICompletions(original_chat.completions, paved_agent)


class AsyncPavedOpenAIEmbeddings:
    """Async wrapper for OpenAI embeddings with policy enforcement."""

    def __init__(self, original_embeddings, paved_agent):
        self._original = original_embeddings
        self._paved = paved_agent

    async def create(self, **kwargs):
        """Async create embeddings with policy enforcement."""
        input_text = kwargs.get("input", "")
        model = kwargs.get("model", "unknown")

        # Handle both string and list inputs
        if isinstance(input_text, list):
            text_content = " ".join(input_text)
        else:
            text_content = input_text

        payload = {
            "text": text_content,
            "input": input_text,
            "model": model,
            "encoding_format": kwargs.get("encoding_format"),
            "framework": "openai",
            "action": "embedding"
        }

        # Policy check (sync for now)
        self._paved.check("embedding", payload)

        # Call async OpenAI API
        return await self._original.create(**kwargs)

class AsyncOpenAI(OriginalAsyncOpenAI, PavedOpenAIWrapper):
    def __init__(
        self,
        agent_id: str = "openai-agent",
        paved_api_key: str = None,
        paved_url: str = None,
        paved_policies: List[str] = None,
        paved_policy: Dict[str, Any] = None,
        _paved: Optional[Agent] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        PavedOpenAIWrapper.__init__(
            self, 
            agent_id=agent_id, 
            paved_api_key=paved_api_key, 
            paved_url=paved_url,
            paved_policies=paved_policies,
            paved_policy=paved_policy
        )
        if _paved:
            self._paved = _paved

        # Wrap chat and embeddings APIs
        self.chat = AsyncPavedOpenAIChat(super().chat, self._paved)
        self.embeddings = AsyncPavedOpenAIEmbeddings(super().embeddings, self._paved)
