"""Tag management functionality for the LLM completion library."""

from typing import Dict, List, Any, Optional, Tuple, Set
import logging
from collections import Counter

from .resources.tag_data import (
    get_all_tags,
    get_tags_by_category,
    get_recommended_tags_for_component,
    filter_tags,
    validate_tags,
    TAG_CATEGORIES,
    COMMON_COMPONENT_TAGS
)
from .logger import logger


class TagManager:
    """Manager for landing page component tags."""
    
    def __init__(self) -> None:
        """Initialize the tag manager."""
        try:
            # Validate that tag data is accessible and consistent
            all_tags = get_all_tags()
            categories_tags = []
            for category in TAG_CATEGORIES:
                categories_tags.extend(TAG_CATEGORIES[category])
            
            # Ensure all category tags are in ALL_TAGS
            missing_tags = [tag for tag in categories_tags if tag not in all_tags]
            if missing_tags:
                logger.warning(f"Some tags in categories are missing from ALL_TAGS: {missing_tags}")
            
            # Ensure no duplicates in ALL_TAGS
            duplicates = [item for item, count in Counter(all_tags).items() if count > 1]
            if duplicates:
                logger.warning(f"Duplicate tags found in ALL_TAGS: {duplicates}")
                
            logger.info(f"TagManager initialized with {len(all_tags)} tags across {len(TAG_CATEGORIES)} categories")
            
        except Exception as e:
            logger.error(f"Error initializing TagManager: {str(e)}")
            raise RuntimeError(f"Failed to initialize TagManager: {str(e)}")
    
    def get_recommended_tags(self, component_name: str) -> List[str]:
        """Get recommended tags for a specific component.

        Args:
            component_name: Name of the component to get tags for.

        Returns:
            List of recommended tags.
        """
        try:
            component_tags = get_recommended_tags_for_component(component_name)
            recommended = [component_tags["primary"]] + component_tags["recommended"]
            return recommended
        except ValueError as e:
            logger.warning(f"No predefined tags for component '{component_name}': {str(e)}")
            # Fallback to primary structural tag if possible
            component_name_lower = component_name.lower()
            for tag in TAG_CATEGORIES["primary"]:
                if tag in component_name_lower:
                    logger.info(f"Using partial match for component '{component_name}': {tag}")
                    return [tag]
            # No match found
            logger.info(f"No tag match found for component '{component_name}', returning empty list")
            return []
        except Exception as e:
            logger.error(f"Error getting recommended tags for '{component_name}': {str(e)}")
            return []
    
    def get_component_combinations(self, count: int = 5, focus: Optional[str] = None) -> List[str]:
        """Get recommended component combinations for a landing page.

        Args:
            count: Minimum number of components to return.
            focus: Optional focus area (e.g., 'conversion', 'trust', 'awareness').

        Returns:
            List of recommended component names.
        """
        # Essential components that should be included in any landing page
        essential = ["hero", "features", "cta"]
        
        # Add focus-specific components
        focus_components = {
            "conversion": ["pricing", "testimonials", "faq"],
            "trust": ["testimonials", "partners", "team"],
            "awareness": ["showcase", "stats", "gallery"],
            "engagement": ["newsletter", "contact", "process"]
        }
        
        result = essential.copy()
        
        # Add focus-specific components if requested
        if focus and focus in focus_components:
            for component in focus_components[focus]:
                if component not in result:
                    result.append(component)
        
        # Add more components if needed to reach the count
        all_components = list(COMMON_COMPONENT_TAGS.keys())
        for component in all_components:
            if len(result) >= count:
                break
            if component not in result:
                result.append(component)
        
        return result[:count]
    
    def search_tags(self, query: str) -> List[str]:
        """Search for tags matching a query.

        Args:
            query: Search query.

        Returns:
            List of matching tags.
        """
        query = query.lower()
        
        # Direct match with tag categories
        if query in TAG_CATEGORIES:
            return TAG_CATEGORIES[query]
        
        # Search in all tags
        all_tags = get_all_tags()
        return [tag for tag in all_tags if query in tag.lower()]
    
    def create_tag_set(
        self, 
        primary_tag: str, 
        additional_count: int = 3, 
        exclude_categories: Optional[List[str]] = None
    ) -> List[str]:
        """Create a balanced set of tags for a component.

        Args:
            primary_tag: Primary tag for the component.
            additional_count: Number of additional tags to include.
            exclude_categories: Categories to exclude from additional tags.

        Returns:
            List of tags.
        """
        result = [primary_tag]
        
        try:
            # Try to determine which category the primary tag belongs to
            primary_category = None
            for category, tags in TAG_CATEGORIES.items():
                if primary_tag in tags:
                    primary_category = category
                    break
            
            # Get additional tags from different categories
            categories_to_try = list(TAG_CATEGORIES.keys())
            if primary_category:
                categories_to_try.remove(primary_category)
            
            if exclude_categories:
                categories_to_try = [c for c in categories_to_try if c not in exclude_categories]
            
            # Add one tag from each category until we reach the desired count
            for category in categories_to_try:
                if len(result) >= additional_count + 1:
                    break
                
                category_tags = TAG_CATEGORIES[category]
                if category_tags:
                    # Choose the first tag from this category
                    result.append(category_tags[0])
            
            return result
            
        except Exception as e:
            logger.error(f"Error creating tag set for '{primary_tag}': {str(e)}")
            return [primary_tag]  # Return at least the primary tag
    
    def validate_component_tags(self, component_name: str, tags: List[str]) -> Tuple[bool, List[str]]:
        """Validate tags for a specific component.

        Args:
            component_name: Name of the component.
            tags: List of tags to validate.

        Returns:
            Tuple of (is_valid, validation_messages).
        """
        messages = []
        
        # Check if tags exist
        invalid_tags = [tag for tag in tags if tag not in get_all_tags()]
        if invalid_tags:
            messages.append(f"Invalid tags: {', '.join(invalid_tags)}")
        
        # Check if component has a primary structural tag
        has_primary = any(tag in TAG_CATEGORIES["primary"] for tag in tags)
        if not has_primary:
            messages.append("Missing primary structural tag")
        
        # Check for tag coverage (at least one tag from important categories)
        important_categories = ["function", "content", "technical"]
        for category in important_categories:
            if not any(tag in TAG_CATEGORIES[category] for tag in tags):
                messages.append(f"Missing tag from '{category}' category")
        
        return len(messages) == 0, messages