"""Features nested classes for feature search functionality."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Literal, Optional, Union

import httpx

from vllm_sdk.client import AsyncClient, Client
from vllm_sdk.schemas import (
    ActivationsRequest,
    ActivationsResponse,
    ContrastRequest,
    ContrastResponse,
    ChatMessage,
    FeatureItem,
    FeatureAttributeRequest,
    FeatureAttributeResponse,
    FeatureInspectionRequest,
    FeatureInspectionResponse,
    FeatureSearchRequest,
    FeatureSearchResponse,
    FeatureRerankRequest,
    FeatureRerankResponse,
    InterventionSpec,
    LogitsRequest,
    LogitsResponse,
)
from vllm_sdk.utils import AsyncHTTPWrapper, HTTPWrapper

if TYPE_CHECKING:
    from vllm_sdk.variant import Variant


class _BaseFeatures(ABC):
    """Abstract base class for Features functionality."""

    @abstractmethod
    def search(
        self,
        query: str,
        model: Union["Variant", str],
        top_k: int = 10,
    ):
        """Search for SAE features by semantic similarity.

        Args:
            query: Search query string
            model: Variant instance or model name string
            top_k: Number of top results to return

        Returns:
            FeatureSearchResponse with list of matching features
        """
        pass


class Features(_BaseFeatures):
    """Synchronous Features class for feature search."""

    def __init__(self, client: Client, headers: dict, timeout: float):
        """Initialize Features with a synchronous HTTP client.

        Args:
            client: The parent Client instance with sync HTTP client
        """
        self._client = client
        self._headers = headers
        self._timeout = timeout
        self._http_client = HTTPWrapper(inital_backoff_time=1.3, max_retries=5)

    def search(
        self,
        query: str,
        model: Union["Variant", str],
        top_k: int = 10,
    ) -> FeatureSearchResponse:
        """Search for SAE features by semantic similarity (synchronous).

        Args:
            query: Search query string
            model: Variant instance or model name string
            top_k: Number of top results to return

        Returns:
            FeatureSearchResponse with list of matching features
        """
        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Build request
        request = FeatureSearchRequest(
            query=query,
            model_name=model_name,
            top_k=top_k,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = self._http_client.post(
                url=f"{base_url}/v1/features/search",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_feature_search_response(response)

    def rerank(
        self,
        query: str,
        model: Union["Variant", str],
        features: List[FeatureItem],
        top_k: int = 10,
    ) -> FeatureRerankResponse:
        """Rerank features based on a query (synchronous).

        Args:
            query: Search query string
            model: Variant instance or model name string
            features: List of features to rerank
            top_k: Number of top results to return

        Returns:
            FeatureRerankResponse with list of reranked features
        """
        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Build request
        request = FeatureRerankRequest(
            query=query,
            model_name=model_name,
            top_k=top_k,
            features=features,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = self._http_client.post(
                url=f"{base_url}/v1/features/rerank",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_feature_rerank_response(response)

    def inspect(
        self,
        messages: List[ChatMessage],
        model: Union["Variant", str],
        interventions: Optional[List[InterventionSpec]] = None,
        aggregation_method: Optional[
            Literal["mean", "max", "sum", "frequency"]
        ] = "mean",
        top_k: int = 10,
    ) -> FeatureInspectionResponse:
        """Search for SAE features by semantic similarity (synchronous).

        Args:
            messages: List of chat messages
            model: Variant instance or model name string
            interventions: List of SAE feature interventions
            aggregation_method: Aggregation method of feature activations
            top_k: Number of top features to return

        Returns:
            FeatureInspectionResponse with list of matching features
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

        # Build request
        request = FeatureInspectionRequest(
            model=model_name,
            messages=messages,
            interventions=interventions,
            aggregation_method=aggregation_method,
            top_k=top_k,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/inspect",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_feature_inspection_response(response)

    def activations(
        self,
        messages: List[ChatMessage],
        model: Union["Variant", str],
        interventions: Optional[List[InterventionSpec]] = None,
        aggregation_method: Optional[Literal["mean", "max"]] = "mean",
    ) -> ActivationsResponse:
        """Get activations for SAE features (synchronous).

        Args:
            messages: List of chat messages
            model: Variant instance or model name string
            interventions: List of SAE feature interventions
            aggregation_method: Aggregation method of feature activations

        Returns:
            ActivationsResponse with list of raw feature activations
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

        # Build request
        request = ActivationsRequest(
            model=model_name,
            messages=messages,
            interventions=interventions,
            aggregation_method=aggregation_method,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/activations",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_activations_response(response)

    def attribute(
        self,
        messages: List[ChatMessage],
        model: Union["Variant", str],
        interventions: Optional[List[InterventionSpec]] = None,
        start_idx: Optional[int] = 0,
        end_idx: Optional[int] = None,
        top_k: Optional[int] = 10,
    ) -> FeatureAttributeResponse:
        """Get activations for SAE features (synchronous).

        Args:
            messages: List of chat messages
            model: Variant instance or model name string
            interventions: List of SAE feature interventions
            start_idx: Start index of the feature to return
            end_idx: End index of the feature to return
            top_k: Number of top results to return

        Returns:
            FeatureAttributeResponse with list of raw feature activations
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

        # Build request
        request = FeatureAttributeRequest(
            model=model_name,
            messages=messages,
            interventions=interventions,
            start_idx=start_idx,
            end_idx=end_idx,
            top_k=top_k,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/attribute",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_attribute_response(response)

    def logits(
        self,
        messages: List[ChatMessage],
        model: Union["Variant", str],
        interventions: Optional[List[InterventionSpec]] = None,
        top_k: Optional[int] = None,
        start_idx: Optional[int] = None,
        end_idx: Optional[int] = None,
    ) -> LogitsResponse:
        """Get logits from text and feature interventions (synchronous).

        Args:
            messages: List of chat messages
            model: Variant instance or model name string
            interventions: List of SAE feature interventions
            top_k: Number of top logits to return
            start_idx: Start token index of the logits to return
            end_idx: End token index of the logits to return
        Returns:
            LogitsResponse with dictionary of logits
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

        # Build request
        request = LogitsRequest(
            model=model_name,
            messages=messages,
            interventions=interventions,
            top_k=top_k,
            start_idx=start_idx,
            end_idx=end_idx,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/logits",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_logits_response(response)

    def contrast(
        self,
        dataset_1: List[ChatMessage],
        dataset_2: List[ChatMessage],
        model: Union["Variant", str],
        interventions_1: Optional[List[InterventionSpec]] = None,
        interventions_2: Optional[List[InterventionSpec]] = None,
        k_to_add: Optional[int] = 10,
        k_to_remove: Optional[int] = 10,
    ) -> ContrastResponse:
        """Get contrasting features between two datasets (synchronous).

        Args:
            dataset_1: List of chat messages for dataset 1
            dataset_2: List of chat messages for dataset 2
            model: Variant instance or model name string
            interventions_1: List of SAE feature interventions for dataset 1
            interventions_2: List of SAE feature interventions for dataset 2
            k_to_add: Number of top features to add
            k_to_remove: Number of top features to remove
        Returns:
            ContrastResponse with list of top features to add and remove
        """
        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Build request
        request = ContrastRequest(
            model=model_name,
            dataset_1=dataset_1,
            dataset_2=dataset_2,
            interventions_1=interventions_1,
            interventions_2=interventions_2,
            k_to_add=k_to_add,
            k_to_remove=k_to_remove,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/contrast",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_contrast_response(response)


class AsyncFeatures(_BaseFeatures):
    """Asynchronous Features class for feature search."""

    def __init__(self, client: AsyncClient, headers: dict, timeout: float):
        """Initialize AsyncFeatures with an asynchronous HTTP client.

        Args:
            client: The parent AsyncClient instance with async HTTP client
        """
        self._client = client
        self._headers = headers
        self._timeout = timeout
        self._http_client = AsyncHTTPWrapper()

    async def search(
        self,
        query: str,
        model: Union["Variant", str],
        top_k: int = 10,
    ) -> FeatureSearchResponse:
        """Search for SAE features by semantic similarity (asynchronous).

        Args:
            query: Search query string
            model: Variant instance or model name string
            top_k: Number of top results to return

        Returns:
            FeatureSearchResponse with list of matching features
        """
        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Build request
        request = FeatureSearchRequest(
            query=query,
            model_name=model_name,
            top_k=top_k,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = await self._http_client.post(
                url=f"{base_url}/v1/features/search",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_feature_search_response(response)

    async def rerank(
        self,
        query: str,
        features: List[FeatureItem],
        model: Union["Variant", str],
        top_k: int = 10,
    ) -> FeatureRerankResponse:
        """Rerank features based on a query (asynchronous).

        Args:
            query: Search query string
            model: Variant instance or model name string
            features: List of features to rerank
            top_k: Number of top results to return

        Returns:
            FeatureRerankResponse with list of reranked features
        """
        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Build request
        request = FeatureRerankRequest(
            query=query,
            model_name=model_name,
            top_k=top_k,
            features=features,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = await self._http_client.post(
                url=f"{base_url}/v1/features/rerank",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_feature_rerank_response(response)

    async def inspect(
        self,
        messages: List[ChatMessage],
        model: Union["Variant", str],
        interventions: Optional[List[InterventionSpec]] = None,
        aggregation_method: Optional[
            Literal["mean", "max", "sum", "frequency"]
        ] = "mean",
        top_k: int = 10,
    ) -> FeatureInspectionResponse:
        """Search for SAE features by semantic similarity (synchronous).

        Args:
            messages: List of chat messages
            model: Variant instance or model name string
            interventions: List of SAE feature interventions
            aggregation_method: Aggregation method of feature activations
            top_k: Number of top features to return

        Returns:
            FeatureInspectionResponse with list of matching features
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

        # Build request
        request = FeatureInspectionRequest(
            model=model_name,
            messages=messages,
            interventions=interventions,
            aggregation_method=aggregation_method,
            top_k=top_k,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = await self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/inspect",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_feature_inspection_response(response)

    async def attribute(
        self,
        messages: List[ChatMessage],
        model: Union["Variant", str],
        interventions: Optional[List[InterventionSpec]] = None,
        start_idx: Optional[int] = 0,
        end_idx: Optional[int] = None,
        top_k: Optional[int] = 10,
    ) -> FeatureAttributeResponse:
        """Get activations for SAE features (synchronous).

        Args:
            messages: List of chat messages
            model: Variant instance or model name string
            interventions: List of SAE feature interventions
            start_idx: Start index of the feature to return
            end_idx: End index of the feature to return
            top_k: Number of top results to return

        Returns:
            FeatureAttributeResponse with list of raw feature activations
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
        # Build request
        request = FeatureAttributeRequest(
            model=model_name,
            messages=messages,
            interventions=interventions,
            start_idx=start_idx,
            end_idx=end_idx,
            top_k=top_k,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = await self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/attribute",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_feature_attribute_response(response)

    async def activations(
        self,
        messages: List[ChatMessage],
        model: Union["Variant", str],
        interventions: Optional[List[InterventionSpec]] = None,
        aggregation_method: Optional[Literal["mean", "max"]] = "mean",
    ) -> ActivationsResponse:
        """Get activations for SAE features (asynchronous).

        Args:
            messages: List of chat messages
            model: Variant instance or model name string
            interventions: List of SAE feature interventions
            aggregation_method: Aggregation method of feature activations

        Returns:
            ActivationsResponse with list of raw feature activations
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

        # Build request
        request = ActivationsRequest(
            model=model_name,
            messages=messages,
            interventions=interventions,
            aggregation_method=aggregation_method,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = await self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/activations",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_activations_response(response)

    async def logits(
        self,
        messages: List[ChatMessage],
        model: Union["Variant", str],
        interventions: Optional[List[InterventionSpec]] = None,
        top_k: Optional[int] = None,
        start_idx: Optional[int] = None,
        end_idx: Optional[int] = None,
    ) -> LogitsResponse:
        """Get logits from text and feature interventions (asynchronous).

        Args:
            messages: List of chat messages
            model: Variant instance or model name string
            interventions: List of SAE feature interventions
            top_k: Number of top logits to return
            start_idx: Start token index of the logits to return
            end_idx: End token index of the logits to return
        Returns:
            LogitsResponse with dictionary of logits
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

        # Build request
        request = LogitsRequest(
            model=model_name,
            messages=messages,
            interventions=interventions,
            top_k=top_k,
            start_idx=start_idx,
            end_idx=end_idx,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = await self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/logits",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_logits_response(response)

    async def contrast(
        self,
        dataset_1: List[ChatMessage],
        dataset_2: List[ChatMessage],
        model: Union["Variant", str],
        interventions_1: Optional[List[InterventionSpec]] = None,
        interventions_2: Optional[List[InterventionSpec]] = None,
        k_to_add: Optional[int] = 10,
        k_to_remove: Optional[int] = 10,
    ) -> ContrastResponse:
        """Get contrasting features between two datasets (asynchronous).

        Args:
            dataset_1: List of chat messages for dataset 1
            dataset_2: List of chat messages for dataset 2
            model: Variant instance or model name string
            interventions_1: List of SAE feature interventions for dataset 1
            interventions_2: List of SAE feature interventions for dataset 2
            k_to_add: Number of top features to add
            k_to_remove: Number of top features to remove
        Returns:
            ContrastResponse with list of top features to add and remove
        """
        # Extract model name from Variant if needed
        model_name = model.model_name if isinstance(model, Variant) else model

        # Get base URL for the model
        base_url = self._client._get_base_url(model_name)

        # Build request
        request = ContrastRequest(
            model=model_name,
            dataset_1=dataset_1,
            dataset_2=dataset_2,
            interventions_1=interventions_1,
            interventions_2=interventions_2,
            k_to_add=k_to_add,
            k_to_remove=k_to_remove,
        )

        # Make HTTP request
        # Ensure base_url doesn't have trailing slash
        base_url = base_url.rstrip("/")
        try:
            response = await self._http_client.post(
                url=f"{base_url}/v1/chat_attribution/contrast",
                headers=self._headers,
                timeout=self._timeout,
                json=request.model_dump(),
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            self._client._handle_error(e.response)
        except httpx.RequestError as e:
            from vllm_sdk.exceptions import VLLMConnectionError

            raise VLLMConnectionError(
                message=f"Connection error: {str(e)}",
            ) from e

        # Parse and return response
        return self._client._parse_contrast_response(response)


# Import here to avoid circular dependency
from vllm_sdk.variant import Variant  # noqa: E402
