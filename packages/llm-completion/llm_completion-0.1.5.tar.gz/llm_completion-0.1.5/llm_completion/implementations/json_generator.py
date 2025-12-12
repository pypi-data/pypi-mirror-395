"""Implementation for generating data in JSON format based on schemas."""

from typing import Dict, List, Any, Optional, Union
import json

from ..completion import LiteLLMCompletion
from ..logger import logger

def merge_schemas(schemas: dict) -> dict:
    """
    Combines a list of JSON schemas into a single schema using the 'allOf' keyword.

    This is the most robust and recommended method for combining schemas, as it
    preserves the validation rules of each individual schema.

    Args:
        schemas: A list of dictionaries, where each dictionary is a JSON schema.

    Returns:
        A new dictionary representing the combined JSON schema.
    """
    merged_schema = {
        "type": "object",
        "properties": schemas,
        "additionalProperties": False
    }
    
    return merged_schema

class JsonSchemaDataGenerator:
    """Generator for JSON data based on schemas."""

    def __init__(self, completion_provider: Optional[LiteLLMCompletion] = None) -> None:
        """Initialize the JSON generator.

        Args:
            completion_provider: Optional completion provider to use. If not provided,
                a new instance will be created.
        """
        self.completion_provider = completion_provider or LiteLLMCompletion()
        self.system_prompt = (
            "You are an expert Website Copywriter specializing in creating realistic"
            " JSON data that conforms to specific schemas for the Website. Don't repeat things."
        )

    def generate_data(
        self, 
        schemas: Dict[str, Any], 
        user_prompt: str,
        num_examples: int = 1
    ) -> Dict[str, Any]:
        """Generate JSON data based on provided schemas.

        Args:
            schemas: JSON schema or list of schemas.
            user_prompt: Additional instructions for data generation.
            num_examples: Number of examples to generate.

        Returns:
            A single JSON data object with predefined keys from the schema.

        Raises:
            Exception: If data generation fails.
        """
        logger.info(f"Generating data for {len(schemas.keys())} schemas")

        # icons = {
        #     "type": "array",
        #     "items": {
        #         "type": "string"
        #     }
        # }

        # schemas["icons"] = icons

        # merged_schema = merge_schemas(schemas)
        # print("merged_schema:", merged_schema)

        
        prompt = (
            f"Generate {num_examples} examples of JSON data"
            f"Additional requirements: \n{user_prompt}\n\n"
            "We are generating data for Landing pages so repeat minimally only if required.\n"
            "Fill image assets with Unsplash/Pexels/Pixabay stock images you know exist.\n"
            "Only use known icons from `lucide-react`.\n\n"
            # "icons will contain all the icons used in the JSON data."
            "Return ONLY valid JSON data that matches the schema(s) provided."
        )

        try:
            # Define JSON schema for the response
            print("prompt:", prompt)

            result = self.completion_provider.complete_with_json(prompt, self.system_prompt, json_schema=schemas)
            print("Generated JSON data:", result)
            
            # Process the data to ensure all image and icon fields are properly formatted
            processed_result = self._process_generated_data(result)
            
            logger.info("Successfully generated data")

            return processed_result

        except Exception as e:
            logger.error(f"Failed to generate JSON data: {str(e)}")
            raise

    async def agenerate_data(
        self, 
        schemas: Dict[str, Any], 
        user_prompt: str,
        num_examples: int = 1
    ) -> Dict[str, Any]:
        """Asynchronously generate JSON data based on provided schemas.

        Args:
            schemas: JSON schema or list of schemas.
            user_prompt: Additional instructions for data generation.
            num_examples: Number of examples to generate.

        Returns:
            A single JSON data object with predefined keys from the schema.

        Raises:
            Exception: If data generation fails.
        """
        logger.info(f"Async generating data for {len(schemas.keys())} schemas")
        
        prompt = (
            f"Generate {num_examples} examples of JSON data"
            f"Additional requirements: \n{user_prompt}\n\n"
            "We are generating data for Landing pages so repeat minimally only if required.\n"
            "Fill image assets with Unsplash/Pexels/Pixabay stock images you know exist.\n"
            "Only use known icons from `lucide-react`.\n\n"
            "Return ONLY valid JSON data that matches the schema(s) provided."
        )

        try:
            result = await self.completion_provider.acomplete_with_json(prompt, self.system_prompt, json_schema=schemas)
            
            # Process the data to ensure all image and icon fields are properly formatted
            processed_result = self._process_generated_data(result)
            
            logger.info("Successfully async generated data")

            return processed_result

        except Exception as e:
            logger.error(f"Failed to async generate JSON data: {str(e)}")
            raise
            
    def _process_generated_data(self, data: Any) -> Any:
        """Process the generated data to format icons and other fields correctly.
        
        Args:
            data: The generated data structure
            
        Returns:
            Processed data structure
        """
        # Process data and transform icon names
        self._process_data_recursive(data)
        return data
    
    def _process_data_recursive(self, data):
        """
        Recursively process data structure to find and update icon names.
        
        Args:
            data: Any data structure (dict, list, etc.) to process
        """
        if isinstance(data, dict):
            # Check if this dict matches the Icon interface
            if (data.get('package') == 'lucide' and 
                data.get('type') == 'icon' and 
                'name' in data and 
                isinstance(data['name'], str)):
                # Transform hyphenated icon names to title case (e.g., "check-circle" -> "CheckCircle")
                icon_name = data['name']
                data['name'] = ''.join(x.title() for x in icon_name.split('-'))
            
            # Process all values
            for value in data.values():
                self._process_data_recursive(value)
                
        elif isinstance(data, list):
            # Process all list items
            for item in data:
                self._process_data_recursive(item)
    