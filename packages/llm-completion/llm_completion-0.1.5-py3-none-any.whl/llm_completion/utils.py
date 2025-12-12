"""Utility functions for the LLM completion library."""

import json
from typing import Dict, Any


def format_prompt(template: str, **kwargs: Any) -> str:
    """Format a prompt template with the provided variables.

    Args:
        template: The prompt template with placeholders.
        **kwargs: Variables to fill in the template.

    Returns:
        The formatted prompt.
    """
    return template.format(**kwargs)


def validate_json_response(response: str) -> Dict[str, Any]:
    """Validate and parse JSON from a response string.

    Args:
        response: The response string that should contain JSON.

    Returns:
        Parsed JSON data.

    Raises:
        ValueError: If the response doesn't contain valid JSON.
    """
    # Try to extract JSON from markdown code blocks if present
    if "```json" in response:
        try:
            json_content = response.split("```json")[1].split("```")[0].strip()
            return json.loads(json_content)
        except (IndexError, json.JSONDecodeError):
            pass

    # Try direct JSON parsing
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Response does not contain valid JSON")


def extract_code_from_markdown(markdown: str, language: str = "") -> str:
    """Extract code blocks from markdown content.

    Args:
        markdown: The markdown content containing code blocks.
        language: Optional language identifier to extract specific language blocks.

    Returns:
        Extracted code or empty string if no matching code block found.
    """
    language = language.strip()
    marker = f"```{language}" if language else "```"
    
    if marker not in markdown:
        return ""
    
    parts = markdown.split(marker)
    if len(parts) < 2:
        return ""
    
    # Get the content after the first marker and before the next closing marker
    code_block = parts[1].split("```")[0]
    
    return code_block.strip()