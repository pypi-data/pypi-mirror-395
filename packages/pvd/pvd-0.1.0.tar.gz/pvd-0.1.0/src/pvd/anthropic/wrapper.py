"""
Paved wrapper for Anthropic with policy enforcement.

This module provides a drop-in replacement for the anthropic library
that automatically enforces Paved policies.
"""
import os
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator

try:
    from anthropic import Anthropic as OriginalAnthropic
    from anthropic import AsyncAnthropic as OriginalAsyncAnthropic
    from anthropic import Stream, AsyncStream
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    OriginalAnthropic = object
    OriginalAsyncAnthropic = object

from pvd.sdk import Agent


class PavedMessages:
    """
    Wrapper for Anthropic messages API with policy enforcement.

    Intercepts all message creation calls to enforce Paved policies.
    """

    def __init__(self, original_messages, paved_agent: Agent):
        """
        Initialize messages wrapper.

        Args:
            original_messages: Original Anthropic messages client
            paved_agent: Paved agent for policy enforcement
        """
        self._original = original_messages
        self._paved = paved_agent

    def _extract_user_content(self, messages: List[Dict[str, Any]]) -> str:
        """Extract user message content for policy checks."""
        user_content = []
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                # Handle both string content and structured content blocks
                if isinstance(content, str):
                    user_content.append(content)
                elif isinstance(content, list):
                    # Extract text from content blocks
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            user_content.append(block.get("text", ""))
        return " ".join(user_content) if user_content else ""

    def _build_policy_payload(self, **kwargs) -> Dict[str, Any]:
        """Build policy check payload from message creation parameters."""
        messages = kwargs.get("messages", [])
        return {
            "text": self._extract_user_content(messages),
            "messages": messages,
            "model": kwargs.get("model", "unknown"),
            "max_tokens": kwargs.get("max_tokens"),
            "temperature": kwargs.get("temperature"),
            "top_p": kwargs.get("top_p"),
            "top_k": kwargs.get("top_k"),
            "tools": kwargs.get("tools"),
            "tool_choice": kwargs.get("tool_choice"),
            "system": kwargs.get("system"),
            "framework": "anthropic"
        }

    def create(self, **kwargs) -> Any:
        """
        Create message with policy enforcement.

        Supports all Anthropic message creation parameters including:
        - Standard chat completion
        - Tool/function calling
        - System messages
        - Streaming

        Args:
            **kwargs: Anthropic message creation parameters

        Returns:
            Anthropic Message object

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Build and check policy
        payload = self._build_policy_payload(**kwargs)
        self._paved.check("llm", payload)

        # Call original Anthropic API
        return self._original.create(**kwargs)

    def stream(self, **kwargs) -> Union[Stream, Iterator]:
        """
        Create streaming message with policy enforcement.

        Args:
            **kwargs: Anthropic message creation parameters

        Returns:
            Stream of message deltas

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Check policy before streaming starts
        payload = self._build_policy_payload(**kwargs)
        self._paved.check("llm", payload)

        # Use the messages create method with stream=True
        # The anthropic SDK handles this internally
        return self._original.create(stream=True, **kwargs)


class AsyncPavedMessages:
    """
    Async wrapper for Anthropic messages API with policy enforcement.
    """

    def __init__(self, original_messages, paved_agent: Agent):
        """
        Initialize async messages wrapper.

        Args:
            original_messages: Original async Anthropic messages client
            paved_agent: Paved agent for policy enforcement
        """
        self._original = original_messages
        self._paved = paved_agent

    def _extract_user_content(self, messages: List[Dict[str, Any]]) -> str:
        """Extract user message content for policy checks."""
        user_content = []
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str):
                    user_content.append(content)
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            user_content.append(block.get("text", ""))
        return " ".join(user_content) if user_content else ""

    def _build_policy_payload(self, **kwargs) -> Dict[str, Any]:
        """Build policy check payload from message creation parameters."""
        messages = kwargs.get("messages", [])
        return {
            "text": self._extract_user_content(messages),
            "messages": messages,
            "model": kwargs.get("model", "unknown"),
            "max_tokens": kwargs.get("max_tokens"),
            "temperature": kwargs.get("temperature"),
            "top_p": kwargs.get("top_p"),
            "top_k": kwargs.get("top_k"),
            "tools": kwargs.get("tools"),
            "tool_choice": kwargs.get("tool_choice"),
            "system": kwargs.get("system"),
            "framework": "anthropic"
        }

    async def create(self, **kwargs) -> Any:
        """
        Create message with policy enforcement (async).

        Args:
            **kwargs: Anthropic message creation parameters

        Returns:
            Anthropic Message object

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Build and check policy (sync check for now)
        payload = self._build_policy_payload(**kwargs)
        self._paved.check("llm", payload)

        # Call original async Anthropic API
        return await self._original.create(**kwargs)

    async def stream(self, **kwargs) -> Union[AsyncStream, AsyncIterator]:
        """
        Create streaming message with policy enforcement (async).

        Args:
            **kwargs: Anthropic message creation parameters

        Returns:
            AsyncStream of message deltas

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Check policy before streaming starts
        payload = self._build_policy_payload(**kwargs)
        self._paved.check("llm", payload)

        # Use the messages create method with stream=True
        return await self._original.create(stream=True, **kwargs)


class Anthropic(OriginalAnthropic):
    """
    Paved wrapper for Anthropic SDK.

    Drop-in replacement for the Anthropic client that enforces Paved policies
    while maintaining full API compatibility.

    Usage:
        from pvd.anthropic import Anthropic

        client = Anthropic(
            api_key="sk-ant-...",
            agent_id="my-app",
            paved_policies=["pii_strict", "cost_limit"]
        )

        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Hello, Claude!"}
            ]
        )

    Supports all Anthropic features:
    - All Claude models (opus, sonnet, haiku)
    - Tool/function calling
    - System messages
    - Streaming responses
    - Vision (image inputs)
    """

    def __init__(
        self,
        agent_id: str = "anthropic-agent",
        paved_policies: Optional[List[str]] = None,
        paved_policy: Optional[Dict[str, Any]] = None,
        paved_api_key: Optional[str] = None,
        paved_url: Optional[str] = None,
        _paved: Optional[Agent] = None,
        **kwargs
    ):
        """
        Initialize Anthropic client with Paved policy enforcement.

        Args:
            agent_id: Unique identifier for this agent
            paved_policies: Policies (e.g., ["pii_strict", "cost_limit"])
            paved_policy: Dynamic policy configuration
            paved_api_key: Paved API key (or set PAVED_API_KEY env var)
            paved_url: Paved API URL (or set PAVED_URL env var)
            _paved: Internal parameter for testing (inject mock agent)
            **kwargs: Standard Anthropic client arguments (api_key, timeout, etc.)
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "anthropic package is required. Install with: pip install anthropic"
            )

        # Initialize original Anthropic client
        super().__init__(**kwargs)

        # Initialize Paved agent (or use injected one for testing)
        if _paved:
            self._paved = _paved
        else:
            self._paved = Agent(
                agent_id=agent_id,
                policies=paved_policies or [],
                policy_config=paved_policy,
                api_key=paved_api_key,
                base_url=paved_url or os.getenv("PAVED_URL", "http://localhost:8000")
            )

        # Wrap messages API with policy enforcement
        self.messages = PavedMessages(super().messages, self._paved)


class AsyncAnthropic(OriginalAsyncAnthropic):
    """
    Paved wrapper for async Anthropic SDK.

    Async version of the Anthropic wrapper with full policy enforcement.

    Usage:
        from pvd.anthropic import AsyncAnthropic

        client = AsyncAnthropic(
            api_key="sk-ant-...",
            agent_id="my-app",
            paved_policies=["pii_strict"]
        )

        response = await client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": "Hello!"}
            ]
        )
    """

    def __init__(
        self,
        agent_id: str = "anthropic-agent",
        paved_policies: Optional[List[str]] = None,
        paved_policy: Optional[Dict[str, Any]] = None,
        paved_api_key: Optional[str] = None,
        paved_url: Optional[str] = None,
        _paved: Optional[Agent] = None,
        **kwargs
    ):
        """
        Initialize async Anthropic client with Paved policy enforcement.

        Args:
            agent_id: Unique identifier for this agent
            paved_policies: Policies
            paved_policy: Dynamic policy configuration
            paved_api_key: Paved API key
            paved_url: Paved API URL
            _paved: Internal parameter for testing
            **kwargs: Standard Anthropic client arguments
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "anthropic package is required. Install with: pip install anthropic"
            )

        # Initialize original async Anthropic client
        super().__init__(**kwargs)

        # Initialize Paved agent
        if _paved:
            self._paved = _paved
        else:
            self._paved = Agent(
                agent_id=agent_id,
                policies=paved_policies or [],
                policy_config=paved_policy,
                api_key=paved_api_key,
                base_url=paved_url or os.getenv("PAVED_URL", "http://localhost:8000")
            )

        # Wrap messages API with policy enforcement
        self.messages = AsyncPavedMessages(super().messages, self._paved)
