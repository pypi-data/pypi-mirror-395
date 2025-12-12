"""Component processor for shadcn components."""

from typing import Dict, Any, List, Optional, Tuple
import os
import json
import re

from .completion import LiteLLMCompletion
from .logger import logger
from .utils import extract_code_from_markdown
from .tag_manager import TagManager
from .implementations.shadcn_to_ts import ShadcnToTypeScriptConverter


class ComponentProcessor:
    """Processor for shadcn components with TypeScript conversion and tagging."""

    def __init__(self, completion_provider: Optional[LiteLLMCompletion] = None) -> None:
        """Initialize the component processor.

        Args:
            completion_provider: Optional completion provider to use. If not provided,
                a new instance will be created.
        """
        self.converter = ShadcnToTypeScriptConverter(completion_provider)
        self.tag_manager = TagManager()
        self.completion_provider = completion_provider or LiteLLMCompletion()

    def process_component(self, component_code: str, file_path: str) -> Dict[str, Any]:
        """Process a shadcn component: convert to TypeScript, extract icons, and tag it.

        Args:
            component_code: The React component code to convert.
            file_path: Path of the original component file.

        Returns:
            Dictionary with processed component data including TypeScript code,
            props file, component name, tags, and icons.

        Raises:
            Exception: If processing fails.
        """
        logger.info(f"Processing component from {file_path}")
        
        try:
            # 1. Convert to TypeScript
            ts_component, props_file, metadata = self.converter.convert(component_code)
            
            # 2. Extract component name and props info
            component_name = metadata.get("name", self._extract_component_name(file_path, component_code))
            props_name = metadata.get("props", f"{component_name}Props")
            props_file_name = metadata.get("props_file_name", f"{self._get_base_filename(file_path)}.props.ts")
            
            # 3. Extract icons from component code
            icons = self._extract_icons(component_code, ts_component)
            
            # 4. Get appropriate tags for the component
            component_tags = self._tag_component(component_name, component_code, ts_component)
            
            # 5. Prepare the result
            result = {
                "component": {
                    "name": component_name,
                    "typescript_code": ts_component,
                    "file_name": f"{self._get_base_filename(file_path)}.tsx"
                },
                "props": {
                    "name": props_name,
                    "code": props_file,
                    "file_name": props_file_name
                },
                "icons": icons,
                "tags": component_tags,
                "original_file": file_path
            }
            
            logger.info(f"Successfully processed component {component_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing component: {str(e)}")
            raise

    async def aprocess_component(self, component_code: str, file_path: str) -> Dict[str, Any]:
        """Asynchronously process a shadcn component: convert to TypeScript, extract icons, and tag it.

        Args:
            component_code: The React component code to convert.
            file_path: Path of the original component file.

        Returns:
            Dictionary with processed component data including TypeScript code,
            props file, component name, tags, and icons.

        Raises:
            Exception: If processing fails.
        """
        logger.info(f"Async processing component from {file_path}")
        
        try:
            # 1. Convert to TypeScript
            ts_component, props_file, metadata = await self.converter.aconvert(component_code)
            
            # 2. Extract component name and props info
            component_name = metadata.get("name", self._extract_component_name(file_path, component_code))
            props_name = metadata.get("props", f"{component_name}Props")
            props_file_name = metadata.get("props_file_name", f"{self._get_base_filename(file_path)}.props.ts")
            
            # 3. Extract icons from component code
            icons = await self._aextract_icons(component_code, ts_component)
            
            # 4. Get appropriate tags for the component
            component_tags = await self._atag_component(component_name, component_code, ts_component)
            
            # 5. Prepare the result
            result = {
                "component": {
                    "name": component_name,
                    "typescript_code": ts_component,
                    "file_name": f"{self._get_base_filename(file_path)}.tsx"
                },
                "props": {
                    "name": props_name,
                    "code": props_file,
                    "file_name": props_file_name
                },
                "icons": icons,
                "tags": component_tags,
                "original_file": file_path
            }
            
            logger.info(f"Successfully async processed component {component_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error async processing component: {str(e)}")
            raise

    def _extract_component_name(self, file_path: str, component_code: str) -> str:
        """Extract component name from file path or code.

        Args:
            file_path: Path of the component file.
            component_code: Component code.

        Returns:
            Extracted component name.
        """
        # Try to extract from file path
        base_name = os.path.basename(file_path)
        file_name = os.path.splitext(base_name)[0]
        
        # Convert kebab-case or snake_case to PascalCase
        if "-" in file_name or "_" in file_name:
            parts = re.split(r"[-_]", file_name)
            pascal_name = "".join(part.capitalize() for part in parts)
            return pascal_name
            
        # Try to extract from code using regex
        pattern = r"(?:export\s+)?(?:const|function|class)\s+([A-Z][a-zA-Z0-9]+)"
        match = re.search(pattern, component_code)
        if match:
            return match.group(1)
            
        # Default to capitalized file name
        return file_name.capitalize()

    def _get_base_filename(self, file_path: str) -> str:
        """Get the base filename without extension.

        Args:
            file_path: Path of the file.

        Returns:
            Base filename without extension.
        """
        base_name = os.path.basename(file_path)
        return os.path.splitext(base_name)[0]

    def _extract_icons(self, original_code: str, typescript_code: str) -> List[Dict[str, str]]:
        """Extract icon information from component code.

        Args:
            original_code: Original component code.
            typescript_code: TypeScript converted component code.

        Returns:
            List of dictionaries with icon information.
        """
        # Try to extract information about icons from the code using a separate API call
        prompt = (
            "Identify all icons used in the following React component code. "
            "Return a JSON array of objects with 'package' and 'name' for each icon. "
            "For example, if the component uses FaUser from react-icons/fa, return "
            "{ \"package\": \"react-icons/fa\", \"name\": \"FaUser\" }. "
            "Only include known icons from react-icons packages such as fa, md, io, bi, etc. "
            "If no icons are used, return an empty array.\n\n"
            f"Original code:\n{original_code}\n\n"
            f"TypeScript code:\n{typescript_code}"
        )
        
        system_prompt = "You are an expert at identifying React icons in component code."
        
        try:
            # Define schema for icon result
            schema = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "package": {"type": "string"},
                        "name": {"type": "string"},
                        "usage": {"type": "string"}
                    },
                    "required": ["package", "name"]
                }
            }
            
            # Use JSON completion to directly get structured data
            result = self.completion_provider.complete_with_json(prompt, system_prompt, json_schema=schema)
            
            # Ensure result is a list
            if isinstance(result, list):
                # Validate each item has required fields
                validated_icons = []
                for icon in result:
                    if isinstance(icon, dict) and "package" in icon and "name" in icon:
                        validated_icons.append({
                            "package": icon["package"],
                            "name": icon["name"]
                        })
                return validated_icons
            elif isinstance(result, dict) and "icons" in result and isinstance(result["icons"], list):
                # Sometimes the API returns a wrapper object
                return result["icons"]
            else:
                logger.warning(f"Unexpected icon extraction result format: {type(result)}")
                return []
                
        except Exception as e:
            logger.error(f"Error extracting icons: {str(e)}")
            
            # Fallback to regex pattern matching for common icon patterns
            icon_patterns = [
                r"import\s+{\s*([A-Z][a-zA-Z0-9]*Icon[a-zA-Z0-9]*)\s*}\s*from\s*['\"]([^'\"]+)['\"]",
                r"import\s+{\s*([A-Z][a-zA-Z0-9]*)\s*}\s*from\s*['\"]react-icons/([^'\"]+)['\"]",
                r"<([A-Z][a-zA-Z0-9]*Icon[a-zA-Z0-9]*)\s*",
            ]
            
            icons = []
            for pattern in icon_patterns:
                matches = re.findall(pattern, original_code + "\n" + typescript_code)
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        icons.append({
                            "name": match[0],
                            "package": match[1]
                        })
                    elif isinstance(match, str):
                        # Just the icon name, try to guess the package
                        if match.startswith("Fa"):
                            package = "react-icons/fa"
                        elif match.startswith("Md"):
                            package = "react-icons/md"
                        elif match.startswith("Io"):
                            package = "react-icons/io"
                        elif match.startswith("Bi"):
                            package = "react-icons/bi"
                        else:
                            package = "unknown"
                        
                        icons.append({
                            "name": match,
                            "package": package
                        })
            
            return icons

    async def _aextract_icons(self, original_code: str, typescript_code: str) -> List[Dict[str, str]]:
        """Asynchronously extract icon information from component code.

        Args:
            original_code: Original component code.
            typescript_code: TypeScript converted component code.

        Returns:
            List of dictionaries with icon information.
        """
        # Try to extract information about icons from the code using a separate API call
        prompt = (
            "Identify all icons used in the following React component code. "
            "Return a JSON array of objects with 'package' and 'name' for each icon. "
            "For example, if the component uses FaUser from react-icons/fa, return "
            "{ \"package\": \"react-icons/fa\", \"name\": \"FaUser\" }. "
            "Only include known icons from react-icons packages such as fa, md, io, bi, etc. "
            "If no icons are used, return an empty array.\n\n"
            f"Original code:\n{original_code}\n\n"
            f"TypeScript code:\n{typescript_code}"
        )
        
        system_prompt = "You are an expert at identifying React icons in component code."
        
        try:
            # Define schema for icon result
            schema = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "package": {"type": "string"},
                        "name": {"type": "string"},
                        "usage": {"type": "string"}
                    },
                    "required": ["package", "name"]
                }
            }
            
            # Use async JSON completion to directly get structured data
            result = await self.completion_provider.acomplete_with_json(prompt, system_prompt, json_schema=schema)
            
            # Ensure result is a list
            if isinstance(result, list):
                # Validate each item has required fields
                validated_icons = []
                for icon in result:
                    if isinstance(icon, dict) and "package" in icon and "name" in icon:
                        validated_icons.append({
                            "package": icon["package"],
                            "name": icon["name"]
                        })
                return validated_icons
            elif isinstance(result, dict) and "icons" in result and isinstance(result["icons"], list):
                # Sometimes the API returns a wrapper object
                return result["icons"]
            else:
                logger.warning(f"Unexpected icon extraction result format: {type(result)}")
                return []
                
        except Exception as e:
            logger.error(f"Error async extracting icons: {str(e)}")
            
            # Fallback to regex pattern matching for common icon patterns
            icon_patterns = [
                r"import\s+{\s*([A-Z][a-zA-Z0-9]*Icon[a-zA-Z0-9]*)\s*}\s*from\s*['\"]([^'\"]+)['\"]",
                r"import\s+{\s*([A-Z][a-zA-Z0-9]*)\s*}\s*from\s*['\"]react-icons/([^'\"]+)['\"]",
                r"<([A-Z][a-zA-Z0-9]*Icon[a-zA-Z0-9]*)\s*",
            ]
            
            icons = []
            for pattern in icon_patterns:
                matches = re.findall(pattern, original_code + "\n" + typescript_code)
                for match in matches:
                    if isinstance(match, tuple) and len(match) >= 2:
                        icons.append({
                            "name": match[0],
                            "package": match[1]
                        })
                    elif isinstance(match, str):
                        # Just the icon name, try to guess the package
                        if match.startswith("Fa"):
                            package = "react-icons/fa"
                        elif match.startswith("Md"):
                            package = "react-icons/md"
                        elif match.startswith("Io"):
                            package = "react-icons/io"
                        elif match.startswith("Bi"):
                            package = "react-icons/bi"
                        else:
                            package = "unknown"
                        
                        icons.append({
                            "name": match,
                            "package": package
                        })
            
            return icons

    def _tag_component(self, component_name: str, original_code: str, typescript_code: str) -> Dict[str, Any]:
        """Tag the component based on its name and code.

        Args:
            component_name: Component name.
            original_code: Original component code.
            typescript_code: TypeScript converted component code.

        Returns:
            Dictionary with component tags.
        """
        # Use the tag manager to get appropriate tags
        tag_finder = self.tag_manager
        
        try:
            # First try to get tags based on component name
            component_tags = tag_finder.get_recommended_tags(component_name)
            
            # If no tags were found, analyze the code to infer tags
            if not component_tags:
                # Use a smart approach to infer tags from the code
                code_analysis_prompt = (
                    "Analyze the following React component code and identify the most appropriate "
                    "tags for it. Return a JSON object with 'primary_tag' and 'additional_tags' keys. "
                    "The primary tag should be one of the following structural tags:\n"
                    "hero, header, footer, navigation, cta, testimonials, features, pricing, faq, "
                    "contact, team, stats, newsletter, banner, gallery, partners, showcase, process\n\n"
                    "Additional tags should be selected from the following categories:\n"
                    "- Function: action-trigger, data-display, content-container, form-element, feedback, "
                    "navigation-element, social-proof, disclosure, media-display, state-indicator\n"
                    "- Content: text-heavy, visual-dominant, icon-based, form, interactive-element, "
                    "data-visualization, mixed-media\n"
                    "- Style: minimalist, bold, dark-mode, gradient, glassmorphism, neumorphic, "
                    "skeuomorphic, flat-design, animated, gradient-border, shadow-heavy, rounded\n"
                    "- Technical: responsive-mobile, responsive-desktop, interactive, static, "
                    "dynamic-content, lazy-loaded, fixed-position, sticky-element\n\n"
                    f"Component name: {component_name}\n\n"
                    f"Component code:\n{typescript_code}"
                )
                
                try:
                    # Define schema for code analysis
                    analysis_schema = {
                        "type": "object",
                        "properties": {
                            "primary_tag": {"type": "string"},
                            "additional_tags": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "complexity": {"type": "string", "enum": ["simple", "medium", "complex"]},
                            "features": {
                                "type": "array", 
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["primary_tag"]
                    }
                    
                    code_analysis = self.completion_provider.complete_with_json(code_analysis_prompt, json_schema=analysis_schema)
                    
                    if isinstance(code_analysis, dict):
                        primary_tag = code_analysis.get("primary_tag", "")
                        additional_tags = code_analysis.get("additional_tags", [])
                        
                        if primary_tag:
                            component_tags = [primary_tag] + additional_tags
                    
                except Exception as e:
                    logger.warning(f"Error in code analysis for tagging: {str(e)}")
            
            # Ensure we have at least some tags
            if not component_tags:
                # Create some default tags based on the component name
                primary = component_name.lower()
                component_tags = tag_finder.create_tag_set(primary, 3)
            
            # Format the result
            primary_tag = component_tags[0] if component_tags else component_name.lower()
            additional_tags = component_tags[1:] if len(component_tags) > 1 else []
            
            return {
                "primary": primary_tag,
                "additional": additional_tags,
                "all": component_tags
            }
            
        except Exception as e:
            logger.error(f"Error tagging component: {str(e)}")
            # Return minimal tags based on component name
            return {
                "primary": component_name.lower(),
                "additional": [],
                "all": [component_name.lower()]
            }

    async def _atag_component(self, component_name: str, original_code: str, typescript_code: str) -> Dict[str, Any]:
        """Asynchronously tag the component based on its name and code.

        Args:
            component_name: Component name.
            original_code: Original component code.
            typescript_code: TypeScript converted component code.

        Returns:
            Dictionary with component tags.
        """
        # Use the tag manager to get appropriate tags
        tag_finder = self.tag_manager
        
        try:
            # First try to get tags based on component name
            component_tags = tag_finder.get_recommended_tags(component_name)
            
            # If no tags were found, analyze the code to infer tags
            if not component_tags:
                # Use a smart approach to infer tags from the code
                code_analysis_prompt = (
                    "Analyze the following React component code and identify the most appropriate "
                    "tags for it. Return a JSON object with 'primary_tag' and 'additional_tags' keys. "
                    "The primary tag should be one of the following structural tags:\n"
                    "hero, header, footer, navigation, cta, testimonials, features, pricing, faq, "
                    "contact, team, stats, newsletter, banner, gallery, partners, showcase, process\n\n"
                    "Additional tags should be selected from the following categories:\n"
                    "- Function: action-trigger, data-display, content-container, form-element, feedback, "
                    "navigation-element, social-proof, disclosure, media-display, state-indicator\n"
                    "- Content: text-heavy, visual-dominant, icon-based, form, interactive-element, "
                    "data-visualization, mixed-media\n"
                    "- Style: minimalist, bold, dark-mode, gradient, glassmorphism, neumorphic, "
                    "skeuomorphic, flat-design, animated, gradient-border, shadow-heavy, rounded\n"
                    "- Technical: responsive-mobile, responsive-desktop, interactive, static, "
                    "dynamic-content, lazy-loaded, fixed-position, sticky-element\n\n"
                    f"Component name: {component_name}\n\n"
                    f"Component code:\n{typescript_code}"
                )
                
                try:
                    # Define schema for code analysis
                    analysis_schema = {
                        "type": "object",
                        "properties": {
                            "primary_tag": {"type": "string"},
                            "additional_tags": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "complexity": {"type": "string", "enum": ["simple", "medium", "complex"]},
                            "features": {
                                "type": "array", 
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["primary_tag"]
                    }
                    
                    code_analysis = await self.completion_provider.acomplete_with_json(code_analysis_prompt, json_schema=analysis_schema)
                    
                    if isinstance(code_analysis, dict):
                        primary_tag = code_analysis.get("primary_tag", "")
                        additional_tags = code_analysis.get("additional_tags", [])
                        
                        if primary_tag:
                            component_tags = [primary_tag] + additional_tags
                    
                except Exception as e:
                    logger.warning(f"Error in async code analysis for tagging: {str(e)}")
            
            # Ensure we have at least some tags
            if not component_tags:
                # Create some default tags based on the component name
                primary = component_name.lower()
                component_tags = tag_finder.create_tag_set(primary, 3)
            
            # Format the result
            primary_tag = component_tags[0] if component_tags else component_name.lower()
            additional_tags = component_tags[1:] if len(component_tags) > 1 else []
            
            return {
                "primary": primary_tag,
                "additional": additional_tags,
                "all": component_tags
            }
            
        except Exception as e:
            logger.error(f"Error async tagging component: {str(e)}")
            # Return minimal tags based on component name
            return {
                "primary": component_name.lower(),
                "additional": [],
                "all": [component_name.lower()]
            }