"""
LiteLLM wrapper for Paved with policy enforcement.

Provides policy-enforced access to 100+ LLM providers through LiteLLM's unified API.
"""
import os
from typing import Any, Dict, List, Optional, Union, Iterator, AsyncIterator

try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    litellm = None

from pvd.sdk import Agent


class LiteLLM:
    """
    Paved wrapper for LiteLLM with policy enforcement.

    Provides policy-enforced access to 100+ LLM providers including:
    - OpenAI (gpt-4, gpt-3.5-turbo, etc.)
    - Anthropic (claude-3-opus, claude-3-sonnet, etc.)
    - Google (gemini-pro, palm-2, etc.)
    - AWS Bedrock (bedrock/anthropic.claude-v2, etc.)
    - Azure OpenAI
    - Cohere, Replicate, Hugging Face, and 90+ more

    Usage:
        from pvd.litellm import LiteLLM

        client = LiteLLM(
            agent_id="my-app",
            paved_policies=["pii_strict", "cost_limit"]
        )

        # Works with any LiteLLM-supported model
        response = client.completion(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello!"}]
        )

        # Or with Anthropic
        response = client.completion(
            model="claude-3-opus-20240229",
            messages=[{"role": "user", "content": "Hello!"}]
        )

        # Or with Bedrock
        response = client.completion(
            model="bedrock/anthropic.claude-v2",
            messages=[{"role": "user", "content": "Hello!"}]
        )
    """

    def __init__(
        self,
        agent_id: str = "litellm-agent",
        paved_policies: Optional[List[str]] = None,
        paved_policy: Optional[Dict[str, Any]] = None,
        paved_api_key: Optional[str] = None,
        paved_url: Optional[str] = None,
        _paved: Optional[Agent] = None,
    ):
        """
        Initialize LiteLLM wrapper with Paved policy enforcement.

        Args:
            agent_id: Unique identifier for this agent
            paved_policies: Policies (e.g., ["pii_strict", "cost_limit"])
            paved_policy: Dynamic policy configuration
            paved_api_key: Paved API key (or set PAVED_API_KEY env var)
            paved_url: Paved API URL (or set PAVED_URL env var)
            _paved: Internal parameter for testing (inject mock agent)
        """
        if not LITELLM_AVAILABLE:
            raise ImportError(
                "litellm package is required. Install with: pip install litellm"
            )

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

    def _extract_user_content(self, messages: List[Dict[str, str]]) -> str:
        """Extract user message content for policy checks."""
        user_messages = [
            m.get("content", "")
            for m in messages
            if isinstance(m, dict) and m.get("role") == "user"
        ]
        return " ".join(user_messages) if user_messages else ""

    def _build_policy_payload(
        self,
        messages: List[Dict[str, str]],
        model: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Build policy check payload from call parameters."""
        return {
            "text": self._extract_user_content(messages),
            "messages": messages,
            "model": model,
            "max_tokens": kwargs.get("max_tokens"),
            "temperature": kwargs.get("temperature"),
            "top_p": kwargs.get("top_p"),
            "frequency_penalty": kwargs.get("frequency_penalty"),
            "presence_penalty": kwargs.get("presence_penalty"),
            "tools": kwargs.get("tools"),
            "tool_choice": kwargs.get("tool_choice"),
            "response_format": kwargs.get("response_format"),
            "framework": "litellm"
        }

    def completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Any:
        """
        Call LiteLLM completion with Paved policy enforcement.

        Supports all LiteLLM parameters and 100+ model providers.

        Args:
            model: Model identifier (e.g., "gpt-4", "claude-3-opus-20240229",
                   "bedrock/anthropic.claude-v2")
            messages: Chat messages in OpenAI format
            **kwargs: Additional LiteLLM arguments (temperature, max_tokens, etc.)

        Returns:
            LiteLLM ModelResponse object

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Build and check policy
        payload = self._build_policy_payload(messages, model, **kwargs)
        self._paved.check("llm", payload)

        # Call LiteLLM
        return litellm.completion(model=model, messages=messages, **kwargs)

    async def acompletion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Any:
        """
        Async version of completion with policy enforcement.

        Args:
            model: Model identifier
            messages: Chat messages
            **kwargs: Additional LiteLLM arguments

        Returns:
            LiteLLM ModelResponse object

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Build and check policy (sync for now)
        payload = self._build_policy_payload(messages, model, **kwargs)
        self._paved.check("llm", payload)

        # Call async LiteLLM
        return await litellm.acompletion(model=model, messages=messages, **kwargs)

    def completion_with_streaming(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = True,
        **kwargs
    ) -> Union[Any, Iterator]:
        """
        Completion with streaming support and policy enforcement.

        Args:
            model: Model identifier
            messages: Chat messages
            stream: Whether to stream the response
            **kwargs: Additional LiteLLM arguments

        Returns:
            Iterator of response chunks if stream=True, else ModelResponse

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Policy check before streaming starts
        payload = self._build_policy_payload(messages, model, **kwargs)
        self._paved.check("llm", payload)

        # Call LiteLLM with streaming
        return litellm.completion(
            model=model,
            messages=messages,
            stream=stream,
            **kwargs
        )

    async def acompletion_with_streaming(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = True,
        **kwargs
    ) -> Union[Any, AsyncIterator]:
        """
        Async completion with streaming support and policy enforcement.

        Args:
            model: Model identifier
            messages: Chat messages
            stream: Whether to stream the response
            **kwargs: Additional LiteLLM arguments

        Returns:
            AsyncIterator of response chunks if stream=True, else ModelResponse

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Policy check before streaming starts
        payload = self._build_policy_payload(messages, model, **kwargs)
        self._paved.check("llm", payload)

        # Call async LiteLLM with streaming
        return await litellm.acompletion(
            model=model,
            messages=messages,
            stream=stream,
            **kwargs
        )

    def embedding(
        self,
        model: str,
        input: Union[str, List[str]],
        **kwargs
    ) -> Any:
        """
        Create embeddings with policy enforcement.

        Args:
            model: Embedding model identifier (e.g., "text-embedding-ada-002")
            input: Text or list of texts to embed
            **kwargs: Additional LiteLLM arguments

        Returns:
            LiteLLM EmbeddingResponse object

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Build policy payload for embeddings
        text = input if isinstance(input, str) else " ".join(input)
        payload = {
            "text": text,
            "model": model,
            "input": input,
            "framework": "litellm",
            "action": "embedding"
        }

        self._paved.check("embedding", payload)

        # Call LiteLLM embedding
        return litellm.embedding(model=model, input=input, **kwargs)

    async def aembedding(
        self,
        model: str,
        input: Union[str, List[str]],
        **kwargs
    ) -> Any:
        """
        Async version of embedding with policy enforcement.

        Args:
            model: Embedding model identifier
            input: Text or list of texts to embed
            **kwargs: Additional LiteLLM arguments

        Returns:
            LiteLLM EmbeddingResponse object

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        # Build policy payload
        text = input if isinstance(input, str) else " ".join(input)
        payload = {
            "text": text,
            "model": model,
            "input": input,
            "framework": "litellm",
            "action": "embedding"
        }

        self._paved.check("embedding", payload)

        # Call async LiteLLM embedding
        return await litellm.aembedding(model=model, input=input, **kwargs)

    def image_generation(
        self,
        prompt: str,
        model: str = "dall-e-3",
        **kwargs
    ) -> Any:
        """
        Generate images with policy enforcement.

        Args:
            prompt: Image generation prompt
            model: Image model identifier (e.g., "dall-e-3", "stable-diffusion")
            **kwargs: Additional LiteLLM arguments (size, quality, etc.)

        Returns:
            LiteLLM ImageResponse object

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        payload = {
            "text": prompt,
            "model": model,
            "size": kwargs.get("size"),
            "quality": kwargs.get("quality"),
            "framework": "litellm",
            "action": "image_generation"
        }

        self._paved.check("image_generation", payload)

        # Call LiteLLM image generation
        return litellm.image_generation(prompt=prompt, model=model, **kwargs)

    async def aimage_generation(
        self,
        prompt: str,
        model: str = "dall-e-3",
        **kwargs
    ) -> Any:
        """
        Async version of image generation with policy enforcement.

        Args:
            prompt: Image generation prompt
            model: Image model identifier
            **kwargs: Additional LiteLLM arguments

        Returns:
            LiteLLM ImageResponse object

        Raises:
            PolicyDeniedError: If the policy check fails
        """
        payload = {
            "text": prompt,
            "model": model,
            "size": kwargs.get("size"),
            "quality": kwargs.get("quality"),
            "framework": "litellm",
            "action": "image_generation"
        }

        self._paved.check("image_generation", payload)

        # Call async LiteLLM image generation
        return await litellm.aimage_generation(prompt=prompt, model=model, **kwargs)
