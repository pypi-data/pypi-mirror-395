"""Implementation of LiteLLM-based completion provider."""

import json
import time
import logging
from typing import Dict, Any, Optional, List
import traceback

import litellm
from litellm import acompletion
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    AsyncRetrying,
)

from .base import CompletionProvider
from .config import config
from .logger import logger
from .exceptions import (
    CompletionError,
    APIKeyError,
    RateLimitError,
    ModelNotAvailableError,
    InvalidRequestError,
    LLMTimeoutError,
)


class LiteLLMCompletion(CompletionProvider):
    """LiteLLM-based completion provider with Gemini and OpenAI support."""

    def __init__(self) -> None:
        """Initialize the completion provider."""

        self.providers = []
        
        # Add Gemini if API key is available
        if config.gemini_api_key:
            self.providers.append("gemini")
        
        # Add OpenAI if API key is available
        if config.openai_api_key:
            self.providers.append("openai")
        
        if not self.providers:
            raise APIKeyError("No API keys available for any provider")
        
        logger.info(f"Initialized LiteLLMCompletion with providers: {self.providers}")

    @retry(
        retry=retry_if_exception_type((RateLimitError, LLMTimeoutError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        before_sleep=before_sleep_log(logger, logging.INFO)  # Fixed parameter
    )
    def complete(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> str:
        """Generate text completion using LiteLLM with fallback support.

        Args:
            prompt: The user prompt to generate completion for.
            system_prompt: Optional system instructions.
            **kwargs: Additional parameters to pass to LiteLLM.

        Returns:
            The generated text completion.

        Raises:
            CompletionError: If all providers fail.
        """
        errors = []

        for provider in self.providers:
            try:
                logger.info(f"Attempting completion with {provider}")
                
                start_time = time.time()
                messages = self._create_messages(prompt, system_prompt)
                
                provider_params = config.get_litellm_params(provider)
                provider_params.update(kwargs)

                print("messages:", messages)
                print("provider_params:", provider_params)
                response = litellm.completion(
                    messages=messages,
                    drop_params=True,
                    **provider_params
                )
                
                completion_text = response.choices[0].message.content
                
                duration = time.time() - start_time
                logger.info(f"Completion with {provider} successful ({duration:.2f}s)")
                
                return completion_text
                
            except litellm.exceptions.RateLimitError as e:
                logger.warning(f"Rate limit exceeded with {provider}: {str(e)}")
                errors.append(f"{provider} rate limit: {str(e)}")
                raise RateLimitError(f"Rate limit exceeded with {provider}: {str(e)}")
                
            except litellm.exceptions.Timeout as e:
                logger.warning(f"Timeout with {provider}: {str(e)}")
                errors.append(f"{provider} timeout: {str(e)}")
                raise LLMTimeoutError(f"Request to {provider} timed out: {str(e)}")
                
            except litellm.exceptions.ServiceUnavailableError as e:
                logger.warning(f"Service unavailable with {provider}: {str(e)}")
                errors.append(f"{provider} unavailable: {str(e)}")
                
            except litellm.exceptions.BadRequestError as e:
                logger.error(f"Bad request with {provider}: {str(e)}")
                errors.append(f"{provider} bad request: {str(e)}")
                raise InvalidRequestError(f"Bad request to {provider}: {str(e)}")
                
            except litellm.exceptions.AuthenticationError as e:
                logger.error(f"Authentication error with {provider}: {str(e)}")
                errors.append(f"{provider} auth error: {str(e)}")
                raise APIKeyError(f"Authentication error with {provider}: {str(e)}")
                
            except Exception as e:
                logger.error(f"Unexpected error with {provider}: {str(e)}")
                logger.error(traceback.format_exc())
                errors.append(f"{provider} error: {str(e)}")
        
        # If we get here, all providers failed
        error_msg = f"All providers failed: {'; '.join(errors)}"
        logger.error(error_msg)
        raise CompletionError(error_msg)

    async def acomplete(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> str:
        """Asynchronously generate text completion using LiteLLM with fallback support.

        Args:
            prompt: The user prompt to generate completion for.
            system_prompt: Optional system instructions.
            **kwargs: Additional parameters to pass to LiteLLM.

        Returns:
            The generated text completion.

        Raises:
            CompletionError: If all providers fail.
        """
        errors = []

        for provider in self.providers:
            try:
                async for attempt in AsyncRetrying(
                    retry=retry_if_exception_type((RateLimitError, LLMTimeoutError)),
                    stop=stop_after_attempt(3),
                    wait=wait_exponential(multiplier=1, min=2, max=10),
                    before_sleep=before_sleep_log(logger, logging.INFO)
                ):
                    with attempt:
                        logger.info(f"Attempting async completion with {provider}")
                        
                        start_time = time.time()
                        messages = self._create_messages(prompt, system_prompt)
                        
                        provider_params = config.get_litellm_params(provider)
                        provider_params.update(kwargs)

                        response = await acompletion(
                            messages=messages,
                            drop_params=True,
                            **provider_params
                        )
                        
                        completion_text = response.choices[0].message.content
                        
                        duration = time.time() - start_time
                        logger.info(f"Async completion with {provider} successful ({duration:.2f}s)")
                        
                        return completion_text
                
            except litellm.exceptions.RateLimitError as e:
                logger.warning(f"Rate limit exceeded with {provider}: {str(e)}")
                errors.append(f"{provider} rate limit: {str(e)}")
                raise RateLimitError(f"Rate limit exceeded with {provider}: {str(e)}")
                
            except litellm.exceptions.Timeout as e:
                logger.warning(f"Timeout with {provider}: {str(e)}")
                errors.append(f"{provider} timeout: {str(e)}")
                raise LLMTimeoutError(f"Request to {provider} timed out: {str(e)}")
                
            except litellm.exceptions.ServiceUnavailableError as e:
                logger.warning(f"Service unavailable with {provider}: {str(e)}")
                errors.append(f"{provider} unavailable: {str(e)}")
                
            except litellm.exceptions.BadRequestError as e:
                logger.error(f"Bad request with {provider}: {str(e)}")
                errors.append(f"{provider} bad request: {str(e)}")
                raise InvalidRequestError(f"Bad request to {provider}: {str(e)}")
                
            except litellm.exceptions.AuthenticationError as e:
                logger.error(f"Authentication error with {provider}: {str(e)}")
                errors.append(f"{provider} auth error: {str(e)}")
                raise APIKeyError(f"Authentication error with {provider}: {str(e)}")
                
            except Exception as e:
                logger.error(f"Unexpected error with {provider}: {str(e)}")
                logger.error(traceback.format_exc())
                errors.append(f"{provider} error: {str(e)}")
        
        # If we get here, all providers failed
        error_msg = f"All providers failed: {'; '.join(errors)}"
        logger.error(error_msg)
        raise CompletionError(error_msg)

    def complete_with_json(
        self, prompt: str, system_prompt: Optional[str] = None, json_schema: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Generate JSON completion using LiteLLM with fallback support.

        Args:
            prompt: The user prompt to generate completion for.
            system_prompt: Optional system instructions.
            json_schema: Optional JSON schema to validate the response format.
            **kwargs: Additional parameters to pass to LiteLLM.

        Returns:
            The generated completion as a JSON object.

        Raises:
            CompletionError: If all providers fail or if the response is not valid JSON.
        """
        # Add JSON instruction to system prompt
        json_system_prompt = (
            "You must respond with valid JSON only, no other text. "
            "Ensure the response can be parsed as JSON."
        )
        
        if system_prompt:
            json_system_prompt = f"{system_prompt}\n\n{json_system_prompt}"
            
        # Set up response format for JSON schema if provided
        if json_schema:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "json_data_generation",
                    "schema": json_schema,
                    "strict": False
                },
            }

        # Get completion with enhanced JSON instruction
        try:
            print("json_system_prompt:", json_system_prompt)
            print("prompt:", prompt)
            print("kwargs:", kwargs)
            result = self.complete(prompt, json_system_prompt, **kwargs)
            print("result:", result)

            # Try to extract JSON from the response if it contains markdown code block
            if "```json" in result:
                try:
                    # Extract content from json code block
                    json_content = result.split("```json")[1].split("```")[0].strip()
                    return json.loads(json_content)
                except (IndexError, json.JSONDecodeError):
                    pass
                    
            # Direct parsing if no code block or extraction failed
            try:
                return json.loads(result)
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse response as JSON: {str(e)}\nResponse: {result}"
                logger.error(error_msg)
                raise CompletionError(error_msg)
                
        except Exception as e:
            if isinstance(e, CompletionError):
                raise
            error_msg = f"Error getting JSON completion: {str(e)}"
            logger.error(error_msg)
            raise CompletionError(error_msg)

    async def acomplete_with_json(
        self, prompt: str, system_prompt: Optional[str] = None, json_schema: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Asynchronously generate JSON completion using LiteLLM with fallback support.

        Args:
            prompt: The user prompt to generate completion for.
            system_prompt: Optional system instructions.
            json_schema: Optional JSON schema to validate the response format.
            **kwargs: Additional parameters to pass to LiteLLM.

        Returns:
            The generated completion as a JSON object.

        Raises:
            CompletionError: If all providers fail or if the response is not valid JSON.
        """
        # Add JSON instruction to system prompt
        json_system_prompt = (
            "You must respond with valid JSON only, no other text. "
            "Ensure the response can be parsed as JSON."
        )
        
        if system_prompt:
            json_system_prompt = f"{system_prompt}\n\n{json_system_prompt}"
            
        # Set up response format for JSON schema if provided
        if json_schema:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "json_data_generation",
                    "schema": json_schema,
                    "strict": False
                },
            }

        # Get completion with enhanced JSON instruction
        try:
            result = await self.acomplete(prompt, json_system_prompt, **kwargs)

            # Try to extract JSON from the response if it contains markdown code block
            if "```json" in result:
                try:
                    # Extract content from json code block
                    json_content = result.split("```json")[1].split("```")[0].strip()
                    return json.loads(json_content)
                except (IndexError, json.JSONDecodeError):
                    pass
                    
            # Direct parsing if no code block or extraction failed
            try:
                return json.loads(result)
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse response as JSON: {str(e)}\nResponse: {result}"
                logger.error(error_msg)
                raise CompletionError(error_msg)
                
        except Exception as e:
            if isinstance(e, CompletionError):
                raise
            error_msg = f"Error getting async JSON completion: {str(e)}"
            logger.error(error_msg)
            raise CompletionError(error_msg)

    def _create_messages(
        self, prompt: str, system_prompt: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Create the messages array for the LLM API.

        Args:
            prompt: The user prompt.
            system_prompt: Optional system instructions.

        Returns:
            List of message dictionaries.
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        messages.append({"role": "user", "content": prompt})
        
        return messages