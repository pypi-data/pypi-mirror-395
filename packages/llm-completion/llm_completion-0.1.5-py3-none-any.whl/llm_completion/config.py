"""Configuration management for the LLM completion library."""

import os
from typing import Dict, Any

from .exceptions import APIKeyError


class Config:
    """Configuration management for LLM services."""

    def __init__(self) -> None:
        """Initialize configuration with environment variables."""
        # Check required environment variables
        self._check_required_env_vars()

        # Gemini settings
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini/gemini-2.5-flash")
        self.gemini_max_retries = int(os.getenv("GEMINI_MAX_RETRIES", "2"))
        self.gemini_timeout = int(os.getenv("GEMINI_TIMEOUT", "60"))

        # OpenAI settings (fallback)
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.openai_max_retries = int(os.getenv("OPENAI_MAX_RETRIES", "2"))
        self.openai_timeout = int(os.getenv("OPENAI_TIMEOUT", "60"))

        # General settings
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))

    def _check_required_env_vars(self) -> None:
        """Check that required environment variables are set.

        Raises:
            APIKeyError: If required API keys are missing.
        """
        if not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY"):
            raise APIKeyError(
                "Neither GEMINI_API_KEY nor OPENAI_API_KEY environment variables are set. "
                "At least one API key is required."
            )

    def get_litellm_params(self, provider: str = "gemini") -> Dict[str, Any]:
        """Get parameters for litellm based on provider.

        Args:
            provider: The provider to get parameters for ('gemini' or 'openai').

        Returns:
            Dictionary of parameters for litellm.
        """
        if provider == "gemini":
            return {
                "model": self.gemini_model,
                "api_key": self.gemini_api_key,
                "timeout": self.gemini_timeout,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
        elif provider == "openai":
            return {
                "model": self.openai_model,
                "api_key": self.openai_api_key,
                "timeout": self.openai_timeout,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            }
        else:
            raise ValueError(f"Unsupported provider: {provider}")


# Create a default configuration instance
config = Config()