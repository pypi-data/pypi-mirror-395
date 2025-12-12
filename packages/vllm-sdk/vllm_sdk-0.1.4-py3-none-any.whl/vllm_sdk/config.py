"""Configuration for model-to-URL mapping."""

from vllm_sdk.exceptions import VLLMAPIError

# Model-to-base-URL mapping
_MODEL_URLS = {
    # "meta-llama/Llama-3.1-8B-Instruct": "https://goodfire-api-staging.up.railway.app",
    # "meta-llama/Llama-3.3-70B-Instruct": "https://goodfire-api-staging.up.railway.app",
    "meta-llama/Llama-3.1-8B-Instruct": "http://localhost:3000",
    "meta-llama/Llama-3.3-70B-Instruct": "http://localhost:3000",
}


def get_model_url(model_name: str) -> str:
    """Get the base URL for a given model name.

    Args:
        model_name: The model identifier string

    Returns:
        The base URL for the model

    Raises:
        VLLMAPIError: If the model is not found in the mapping
    """
    if model_name not in _MODEL_URLS:
        available_models = ", ".join(_MODEL_URLS.keys())
        raise VLLMAPIError(
            message=(
                f"Model '{model_name}' not found in URL mapping. "
                f"Available models: {available_models}"
            ),
            status_code=None,
        )
    return _MODEL_URLS[model_name]
