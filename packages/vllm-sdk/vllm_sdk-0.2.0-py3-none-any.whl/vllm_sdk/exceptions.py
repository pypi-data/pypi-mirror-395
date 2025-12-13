"""Custom exceptions for the vLLM SDK."""

from typing import Optional


class VLLMAPIError(Exception):
    """Base exception for vLLM API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class VLLMConnectionError(VLLMAPIError):
    """Raised when connection to the API fails."""

    pass


class VLLMValidationError(VLLMAPIError):
    """Raised when request or response validation fails."""

    pass


class RateLimitException(VLLMAPIError):
    """Raised when the rate limit is exceeded."""

    pass


class ServerErrorException(VLLMAPIError):
    """Raised when the server returns a 500 error."""

    pass


class RequestFailedException(VLLMAPIError):
    """Raised when the request fails."""

    pass


class UpstreamProviderUnavailableException(VLLMAPIError):
    """Raised when an upstream provider is temporarily unavailable."""

    pass


def check_status_code(status_code: int, response_text: str):
    if "upstream provider" in response_text.lower() or status_code in (502, 503):
        raise UpstreamProviderUnavailableException(
            response_text or "Upstream provider is temporarily unavailable."
        ).with_traceback(None)
    elif status_code == 400:
        raise VLLMValidationError(response_text or "Bad request.").with_traceback(None)
    elif status_code == 401:
        raise VLLMAPIError(response_text or "Invalid API key.").with_traceback(None)
    elif status_code == 404:
        raise VLLMAPIError(response_text or "Not found.").with_traceback(None)
    elif status_code == 429:
        raise RateLimitException(
            response_text
            or "You have hit your rate limit. You can request a higher limit by contacting AE Studio Team."
        ).with_traceback(None)
    elif status_code == 500:
        raise ServerErrorException("Server error").with_traceback(None)
    elif status_code > 400:
        raise RequestFailedException(response_text or "Bad request").with_traceback(
            None
        )
