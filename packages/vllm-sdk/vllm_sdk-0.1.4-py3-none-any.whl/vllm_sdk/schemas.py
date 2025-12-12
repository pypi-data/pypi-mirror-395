"""Pydantic schemas for vLLM API requests and responses.

All schemas are standalone with no dependencies on vllm_api.
"""

from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


class ModelName(str, Enum):
    """Enumeration of supported model names."""

    META_LLAMA_3_1_8B_INSTRUCT = "meta-llama/Llama-3.1-8B-Instruct"
    META_LLAMA_3_3_70B_INSTRUCT = "meta-llama/Llama-3.3-70B-Instruct"


# Chat schemas
RoleLiteral = Literal["system", "user", "assistant"]


class ChatMessage(BaseModel):
    role: RoleLiteral
    content: str


class InterventionSpec(BaseModel):
    index_in_sae: int
    strength: float
    mode: Optional[Literal["add", "clamp"]] = "add"


class ChatCompletionRequest(BaseModel):
    model: Union[ModelName, str]
    messages: List[ChatMessage]
    temperature: float = 0.6
    max_completion_tokens: int = 256
    repetition_penalty: float = 1.0
    seed: Optional[int] = None
    interventions: Optional[List[InterventionSpec]] = Field(
        default=None, description="List of SAE feature interventions"
    )
    stream: bool = False


class ChatCompletionMessage(BaseModel):
    role: Literal["assistant"]
    content: str


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: Optional[str] = "stop"
    logprobs: Optional[dict] = None


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: Literal["chat.completion"]
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage


class ChatCompletionDelta(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None


class ChatCompletionChunkChoice(BaseModel):
    index: int
    delta: ChatCompletionDelta
    finish_reason: Optional[str] = None


class ChatCompletionChunk(BaseModel):
    id: str
    object: Literal["chat.completion.chunk"]
    created: int
    model: str
    choices: List[ChatCompletionChunkChoice]
    usage: Optional[ChatCompletionUsage] = None


# Feature search schemas
class FeatureItem(BaseModel):
    """Schema for a single feature item in search results."""

    id: str
    label: str
    layer: int
    index_in_sae: int
    dimension: Optional[int] = None


class FeatureSearchRequest(BaseModel):
    """Request schema for feature search."""

    query: str = Field(..., description="Search query string")
    model_name: Union[ModelName, str] = Field(..., description="Model identifier")
    top_k: int = Field(
        default=10, ge=1, le=100, description="Number of top results to return"
    )


class FeatureSearchResponse(BaseModel):
    """Response schema for feature search."""

    object: str = "feature.list"
    data: List[FeatureItem]


class FeatureRerankRequest(BaseModel):
    """Request schema for feature reranking."""

    query: str = Field(..., description="Rerank query string")
    model_name: ModelName = Field(..., description="Model identifier")
    features: List[FeatureItem] = Field(..., description="List of features to rerank")
    top_k: int = Field(
        default=10, ge=1, le=100, description="Number of top results to return"
    )


class FeatureRerankResponse(BaseModel):
    """Response schema for feature reranking."""

    object: str = "feature.rerank"
    data: List[FeatureItem]


class FeatureInspectionRequest(BaseModel):
    model: ModelName = Field(..., description="Model identifier")
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    interventions: Optional[List[InterventionSpec]] = Field(
        default=None, description="List of SAE feature interventions"
    )
    aggregation_method: Optional[Literal["mean", "max", "sum", "frequency"]] = "mean"
    top_k: Optional[int] = Field(
        default=10, ge=1, le=100, description="Number of top results to return"
    )


class FeatureInspectionUsage(BaseModel):
    total_tokens: int


class FeatureInspection(BaseModel):
    feature: FeatureItem
    activation: Union[int, float]


class FeatureInspectionResponse(BaseModel):
    id: str
    object: Literal["feature.inspect"]
    created: int
    model: ModelName
    features: List[FeatureInspection]
    usage: FeatureInspectionUsage

class FeatureAttributeRequest(BaseModel):
    model: ModelName = Field(..., description="Model identifier")
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    interventions: Optional[List[InterventionSpec]] = Field(
        default=None, description="List of SAE feature interventions"
    )
    start_idx: Optional[int] = Field(
        default=0, ge=0, description="Start index of the feature to return"
    )
    end_idx: Optional[int] = Field(
        default=None, ge=0, description="End index of the feature to return"
    )
    top_k: Optional[int] = Field(
        default=10, ge=1, le=20, description="Number of top features to return"
    )
    


class FeatureAttribute(BaseModel):
    feature: FeatureItem
    activation: Union[int, float]


class FeatureAttributeUsage(BaseModel):
    total_tokens: int

class FeatureAttributeResponse(BaseModel):
    id: str
    object: Literal["feature.attribute"]
    created: int
    model: ModelName
    features: List[FeatureAttribute]
    usage: FeatureAttributeUsage


class ActivationsRequest(BaseModel):
    model: ModelName = Field(..., description="Model identifier")
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    interventions: Optional[List[InterventionSpec]] = Field(
        default=None, description="List of SAE feature interventions"
    )
    aggregation_method: Optional[Literal["mean", "max"]] = "mean"


class ActivationsUsage(BaseModel):
    total_tokens: int


class ActivationsResponse(BaseModel):
    id: str
    object: Literal["feature.activations"]
    created: int
    model: ModelName
    activations: list[float]
    usage: ActivationsUsage


class LogitsRequest(BaseModel):
    model: ModelName = Field(..., description="Model identifier")
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    interventions: Optional[List[InterventionSpec]] = Field(
        default=None, description="List of SAE feature interventions"
    )
    top_k: Optional[int] = None
    start_idx: Optional[int] = None
    end_idx: Optional[int] = None


class LogitsUsage(BaseModel):
    total_tokens: int


class LogitsResponse(BaseModel):
    id: str
    object: Literal["feature.logits"]
    created: int
    model: ModelName
    logits: dict[str, float]
    usage: LogitsUsage


class ContrastRequest(BaseModel):
    model: ModelName = Field(..., description="Model identifier")
    dataset_1: List[List[ChatMessage]] = Field(
        ..., description="List of chat messages for dataset 1"
    )
    dataset_2: List[List[ChatMessage]] = Field(
        ..., description="List of chat messages for dataset 2"
    )
    interventions_1: Optional[List[InterventionSpec]] = Field(
        default=None, description="List of SAE feature interventions"
    )
    interventions_2: Optional[List[InterventionSpec]] = Field(
        default=None, description="List of SAE feature interventions"
    )
    k_to_add: Optional[int] = Field(
        default=10, ge=1, le=100, description="Number of top results to add"
    )
    k_to_remove: Optional[int] = Field(
        default=10, ge=1, le=100, description="Number of top results to remove"
    )


class ContrastUsage(BaseModel):
    total_tokens: int


class ContrastResponse(BaseModel):
    id: str
    object: Literal["feature.contrast"]
    created: int
    model: ModelName
    top_to_add: List[FeatureItem]
    top_to_remove: List[FeatureItem]
    usage: ContrastUsage
