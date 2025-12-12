"""LLM Completion library using LiteLLM."""

from .base import CompletionProvider
from .completion import LiteLLMCompletion
from .exceptions import (
    CompletionError,
    APIKeyError,
    RateLimitError,
    ModelNotAvailableError,
    InvalidRequestError,
    LLMTimeoutError,
)
from .tag_manager import TagManager

__all__ = [
    "CompletionProvider",
    "LiteLLMCompletion",
    "CompletionError",
    "APIKeyError",
    "RateLimitError",
    "ModelNotAvailableError",
    "InvalidRequestError",
    "LLMTimeoutError",
    "TagManager",
]