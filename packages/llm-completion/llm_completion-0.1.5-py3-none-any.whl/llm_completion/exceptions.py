"""Exception classes for the LLM completion library."""


class CompletionError(Exception):
    """Base exception class for all completion-related errors."""

    pass


class APIKeyError(CompletionError):
    """Raised when there's an issue with the API key."""

    pass


class RateLimitError(CompletionError):
    """Raised when the rate limit for an API is exceeded."""

    pass


class ModelNotAvailableError(CompletionError):
    """Raised when the requested model is not available."""

    pass


class InvalidRequestError(CompletionError):
    """Raised when the request to the LLM provider is invalid."""

    pass


class LLMTimeoutError(CompletionError):
    """Raised when the LLM request times out."""

    pass