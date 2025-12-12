"""Base abstract class for LLM completion providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class CompletionProvider(ABC):
    """Abstract base class for LLM completion providers."""

    @abstractmethod
    def complete(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> str:
        """Generate a text completion for the given prompt.

        Args:
            prompt: The user prompt to generate completion for.
            system_prompt: Optional system instructions.
            **kwargs: Additional parameters to pass to the completion provider.

        Returns:
            The generated text completion.

        Raises:
            CompletionError: If there's an error during completion.
        """
        pass

    @abstractmethod
    async def acomplete(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> str:
        """Asynchronously generate a text completion for the given prompt.

        Args:
            prompt: The user prompt to generate completion for.
            system_prompt: Optional system instructions.
            **kwargs: Additional parameters to pass to the completion provider.

        Returns:
            The generated text completion.

        Raises:
            CompletionError: If there's an error during completion.
        """
        pass

    @abstractmethod
    def complete_with_json(
        self, prompt: str, system_prompt: Optional[str] = None, json_schema: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Generate a JSON completion for the given prompt.

        Args:
            prompt: The user prompt to generate completion for.
            system_prompt: Optional system instructions.
            json_schema: Optional JSON schema to validate the response format.
            **kwargs: Additional parameters to pass to the completion provider.

        Returns:
            The generated completion as a JSON object.

        Raises:
            CompletionError: If there's an error during completion.
        """
        pass

    @abstractmethod
    async def acomplete_with_json(
        self, prompt: str, system_prompt: Optional[str] = None, json_schema: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Asynchronously generate a JSON completion for the given prompt.

        Args:
            prompt: The user prompt to generate completion for.
            system_prompt: Optional system instructions.
            json_schema: Optional JSON schema to validate the response format.
            **kwargs: Additional parameters to pass to the completion provider.

        Returns:
            The generated completion as a JSON object.

        Raises:
            CompletionError: If there's an error during completion.
        """
        pass