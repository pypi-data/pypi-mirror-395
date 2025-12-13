"""Minimal Python SDK for the vLLM API."""

from vllm_sdk.client import AsyncClient, Client
from vllm_sdk.exceptions import VLLMAPIError, VLLMConnectionError, VLLMValidationError
from vllm_sdk.schemas import (
    ChatCompletionChoice,
    ChatCompletionChunk,
    ChatCompletionChunkChoice,
    ChatCompletionDelta,
    ChatCompletionMessage,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionUsage,
    ChatMessage,
    FeatureItem,
    FeatureSearchRequest,
    FeatureSearchResponse,
    InterventionSpec,
    ModelName,
    RoleLiteral,
)
from vllm_sdk.variant import Variant

__version__ = "0.1.0"

__all__ = [
    "Client",
    "AsyncClient",
    "Variant",
    "VLLMAPIError",
    "VLLMConnectionError",
    "VLLMValidationError",
    "ChatMessage",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "ChatCompletionChunk",
    "FeatureSearchRequest",
    "FeatureSearchResponse",
    "FeatureItem",
    "ModelName",
    "RoleLiteral",
    "InterventionSpec",
    "ChatCompletionChoice",
    "ChatCompletionChunkChoice",
    "ChatCompletionDelta",
    "ChatCompletionMessage",
    "ChatCompletionUsage",
]
