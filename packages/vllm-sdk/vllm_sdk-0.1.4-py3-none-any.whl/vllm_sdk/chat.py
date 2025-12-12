"""Chat completions nested classes for chat functionality."""

import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, AsyncIterator, List, Optional, Union

import httpx
from pydantic import ValidationError

from vllm_sdk.client import AsyncClient, Client
from vllm_sdk.exceptions import VLLMConnectionError, VLLMValidationError
from vllm_sdk.schemas import (
    ChatCompletionChunk,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    InterventionSpec,
)
from vllm_sdk.utils import AsyncHTTPWrapper, HTTPWrapper

if TYPE_CHECKING:
    from vllm_sdk.variant import Variant


class _BaseChatCompletions(ABC):
    """Abstract base class for ChatCompletions functionality."""

    @abstractmethod
    def create(
        self,
        model: Union["Variant", str],
        messages: Union[List[ChatMessage], List[dict]],
        max_completion_tokens: int,
        temperature: float = 0.6,
        seed: Optional[int] = None,
        interventions: Optional[List[InterventionSpec]] = None,
        repetition_penalty: float = 1.0,
        stream: bool = False,
    ):
        """Create a chat completion.

        Args:
            model: Variant instance or model name string
            messages: List of chat messages (ChatMessage objects or dicts)
            max_completion_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            seed: Random seed
            interventions: List of SAE feature interventions
            repetition_penalty: Repetition penalty
            stream: Whether to stream the response
            is_feature_decode: Return features instead of text
            return_activations: Return activation data
            get_activations_layer: Layers to get activations from

        Returns:
            ChatCompletionResponse object
        """
        pass


class ChatCompletions(_BaseChatCompletions):
    """Synchronous ChatCompletions class."""

    def __init__(self, client: Client, headers: dict, timeout: float):
        """Initialize ChatCompletions with a synchronous HTTP client.

        Args:
            client: The parent Client instance with sync HTTP client
        """
        self._client = client
        self._headers = headers
        self._timeout = timeout
        self._http_client = HTTPWrapper(inital_backoff_time=1.3, max_retries=5)

    def create(
        self,
        model: Union["Variant", str],
        messages: Union[List[ChatMessage], List[dict]],
        max_completion_tokens: int,
        temperature: float = 0.6,
        seed: Optional[int] = None,
        interventions: Optional[List[InterventionSpec]] = None,
        repetition_penalty: float = 1.0,
        stream: bool = False,
    ) -> ChatCompletionResponse:
        """Create a chat completion (synchronous).

        Args:
            model: Variant instance or model name string
            messages: List of chat messages (ChatMessage objects or dicts)
            max_completion_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            seed: Random seed
            interventions: List of SAE feature interventions
            repetition_penalty: Repetition penalty
            stream: Whether to stream the response (not supported in sync)
            is_feature_decode: Return features instead of text
            return_activations: Return activation data
            get_activations_layer: Layers to get activations from

        Returns:
            ChatCompletionResponse object
        """
        if stream:
            raise ValueError(
                "Streaming is not supported in synchronous client. Use AsyncClient instead."
            )

        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Extract interventions from Variant if not explicitly provided
        if interventions is None and isinstance(model, Variant) and model.interventions:
            from vllm_sdk.schemas import InterventionSpec as SchemaInterventionSpec

            interventions = [
                SchemaInterventionSpec(
                    index_in_sae=iv.index_in_sae,
                    strength=iv.strength,
                    mode=iv.mode,
                )
                for iv in model.interventions
            ]

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Convert dict messages to ChatMessage objects if needed
        chat_messages = self._client._normalize_messages(messages)

        # Build request
        request = ChatCompletionRequest(
            model=model_name,
            messages=chat_messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
            repetition_penalty=repetition_penalty,
            seed=seed,
            interventions=interventions,
            stream=False,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = self._http_client.post(
                url=f"{base_url}/v1/chat/completions",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_chat_completion_response(response)


class AsyncChatCompletions(_BaseChatCompletions):
    """Asynchronous ChatCompletions class."""

    def __init__(self, client: AsyncClient, headers: dict, timeout: float):
        """Initialize AsyncChatCompletions with an asynchronous HTTP client.

        Args:
            client: The parent AsyncClient instance with async HTTP client
        """
        self._client = client
        self._headers = headers
        self._timeout = timeout
        self._http_client = AsyncHTTPWrapper(inital_backoff_time=2, max_retries=5)

    async def create(
        self,
        model: Union["Variant", str],
        messages: Union[List[ChatMessage], List[dict]],
        max_completion_tokens: int,
        temperature: float = 0.6,
        seed: Optional[int] = None,
        interventions: Optional[List[InterventionSpec]] = None,
        repetition_penalty: float = 1.0,
        stream: bool = False,
    ) -> ChatCompletionResponse:
        """Create a chat completion (asynchronous).

        Args:
            model: Variant instance or model name string
            messages: List of chat messages (ChatMessage objects or dicts)
            max_completion_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            seed: Random seed
            interventions: List of SAE feature interventions
            repetition_penalty: Repetition penalty
            stream: Whether to stream the response (use create_stream for streaming)
            is_feature_decode: Return features instead of text
            return_activations: Return activation data
            get_activations_layer: Layers to get activations from

        Returns:
            ChatCompletionResponse object
        """
        if stream:
            raise ValueError("Use create_stream() method for streaming responses")

        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Extract interventions from Variant if not explicitly provided
        if interventions is None and isinstance(model, Variant) and model.interventions:
            from vllm_sdk.schemas import InterventionSpec as SchemaInterventionSpec

            interventions = [
                SchemaInterventionSpec(
                    index_in_sae=iv.index_in_sae,
                    strength=iv.strength,
                    mode=iv.mode,
                )
                for iv in model.interventions
            ]

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Convert dict messages to ChatMessage objects if needed
        chat_messages = self._client._normalize_messages(messages)

        # Build request
        request = ChatCompletionRequest(
            model=model_name,
            messages=chat_messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
            repetition_penalty=repetition_penalty,
            seed=seed,
            interventions=interventions,
            stream=False,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = await self._http_client.post(
                url=f"{base_url}/v1/chat/completions",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_chat_completion_response(response)

    async def create_stream(
        self,
        model: Union["Variant", str],
        messages: Union[List[ChatMessage], List[dict]],
        max_completion_tokens: int,
        temperature: float = 0.6,
        seed: Optional[int] = None,
        interventions: Optional[List[InterventionSpec]] = None,
        repetition_penalty: float = 1.0,
    ) -> AsyncIterator[ChatCompletionChunk]:
        """Stream chat completions (asynchronous).

        Yields:
            ChatCompletionChunk objects
        """
        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Extract interventions from Variant if not explicitly provided
        if interventions is None and isinstance(model, Variant) and model.interventions:
            from vllm_sdk.schemas import InterventionSpec as SchemaInterventionSpec

            interventions = [
                SchemaInterventionSpec(
                    index_in_sae=iv.index_in_sae,
                    strength=iv.strength,
                    mode=iv.mode,
                )
                for iv in model.interventions
            ]

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Convert dict messages to ChatMessage objects if needed
        chat_messages = self._client._normalize_messages(messages)

        # Build request
        request = ChatCompletionRequest(
            model=model_name,
            messages=chat_messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
            repetition_penalty=repetition_penalty,
            seed=seed,
            interventions=interventions,
            stream=True,
        )

        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            byte_stream = await self._http_client.stream(
                method="POST",
                url=f"{base_url}/v1/chat/completions",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )

            buffer = ""
            async for chunk in byte_stream:
                # Decode bytes to text and accumulate into buffer
                buffer += chunk.decode("utf-8", errors="ignore")

                # Process complete lines
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            return
                        try:
                            chunk_data = json.loads(data)
                            yield ChatCompletionChunk(**chunk_data)
                        except (
                            json.JSONDecodeError,
                            ValidationError,
                            TypeError,
                            KeyError,
                        ):
                            # Skip invalid chunks
                            continue

        except Exception as e:
            raise VLLMConnectionError(
                message=f"Streaming error: {str(e)}",
            ) from e


# Import here to avoid circular dependency
from vllm_sdk.variant import Variant  # noqa: E402


class Chat:
    """Synchronous Chat wrapper class following OpenAI SDK structure."""

    def __init__(self, client: Client, headers: dict, timeout: float):
        """Initialize Chat with a synchronous HTTP client.

        Args:
            client: The parent Client instance with sync HTTP client
        """
        self.completions = ChatCompletions(
            client=client, headers=headers, timeout=timeout
        )


class AsyncChat:
    """Asynchronous Chat wrapper class following OpenAI SDK structure."""

    def __init__(self, client: AsyncClient, headers: dict, timeout: float):
        """Initialize AsyncChat with an asynchronous HTTP client.

        Args:
            client: The parent AsyncClient instance with async HTTP client
        """
        self.completions = AsyncChatCompletions(
            client=client, headers=headers, timeout=timeout
        )
