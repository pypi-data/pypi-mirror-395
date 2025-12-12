"""Landing page tagging system data module.

This module contains comprehensive tagging data for landing page components,
enabling consistent categorization without requiring API calls.
"""

from typing import Dict, List, Any, Optional, Set
import json

# Primary Structural Tags
PRIMARY_STRUCTURAL_TAGS = [
    "hero",
    "header",
    "footer",
    "navigation",
    "cta",
    "testimonials",
    "features",
    "pricing",
    "faq",
    "contact",
    "team",
    "stats",
    "newsletter",
    "banner",
    "gallery",
    "partners",
    "showcase",
    "process",
]

# Component Function Tags
COMPONENT_FUNCTION_TAGS = [
    "action-trigger",
    "data-display",
    "content-container",
    "form-element",
    "feedback",
    "navigation-element",
    "social-proof",
    "disclosure",
    "media-display",
    "state-indicator",
]

# Content Type Tags
CONTENT_TYPE_TAGS = [
    "text-heavy",
    "visual-dominant",
    "icon-based",
    "form",
    "interactive-element",
    "data-visualization",
    "mixed-media",
]

# Styling & Theme Tags
STYLING_THEME_TAGS = [
    "minimalist",
    "bold",
    "dark-mode",
    "gradient",
    "glassmorphism",
    "neumorphic",
    "skeuomorphic",
    "flat-design",
    "animated",
    "gradient-border",
    "shadow-heavy",
    "rounded",
]

# Technical Behavior Tags
TECHNICAL_BEHAVIOR_TAGS = [
    "responsive-mobile",
    "responsive-desktop",
    "interactive",
    "static",
    "dynamic-content",
    "lazy-loaded",
    "fixed-position",
    "sticky-element",
    "accessibility-optimized",
    "performance-critical",
]

# Placement Context Tags
PLACEMENT_CONTEXT_TAGS = [
    "above-fold",
    "below-fold",
    "full-width",
    "container-bound",
    "floating-element",
    "section-divider",
    "overlay",
]

# Marketing Purpose Tags
MARKETING_PURPOSE_TAGS = [
    "lead-generation",
    "conversion-focused",
    "brand-awareness",
    "product-highlight",
    "trust-building",
    "engagement",
    "scarcity-timer",
]

# Component Complexity Tags
COMPONENT_COMPLEXITY_TAGS = [
    "simple",
    "composite",
    "animated-complex",
    "custom-integration",
    "theme-variant",
]

# Audience Stage Tags
AUDIENCE_STAGE_TAGS = [
    "awareness-stage",
    "consideration-stage",
    "decision-stage",
    "retention-focused",
]

# All tags combined
ALL_TAGS = (
    PRIMARY_STRUCTURAL_TAGS
    + COMPONENT_FUNCTION_TAGS
    + CONTENT_TYPE_TAGS
    + STYLING_THEME_TAGS
    + TECHNICAL_BEHAVIOR_TAGS
    + PLACEMENT_CONTEXT_TAGS
    + MARKETING_PURPOSE_TAGS
    + COMPONENT_COMPLEXITY_TAGS
    + AUDIENCE_STAGE_TAGS
)

# Tag categories mapping for easier access
TAG_CATEGORIES = {
    "primary": PRIMARY_STRUCTURAL_TAGS,
    "function": COMPONENT_FUNCTION_TAGS,
    "content": CONTENT_TYPE_TAGS,
    "style": STYLING_THEME_TAGS,
    "technical": TECHNICAL_BEHAVIOR_TAGS,
    "placement": PLACEMENT_CONTEXT_TAGS,
    "marketing": MARKETING_PURPOSE_TAGS,
    "complexity": COMPONENT_COMPLEXITY_TAGS,
    "audience": AUDIENCE_STAGE_TAGS,
}

# Common tag combinations for specific components
COMMON_COMPONENT_TAGS = {
    "hero": {
        "primary": "hero",
        "recommended": [
            "visual-dominant", 
            "action-trigger", 
            "above-fold", 
            "brand-awareness", 
            "awareness-stage"
        ]
    },
    "pricing": {
        "primary": "pricing",
        "recommended": [
            "content-container", 
            "data-display", 
            "interactive", 
            "conversion-focused", 
            "decision-stage"
        ]
    },
    "testimonials": {
        "primary": "testimonials",
        "recommended": [
            "social-proof", 
            "trust-building", 
            "consideration-stage", 
            "text-heavy", 
            "media-display"
        ]
    },
    "features": {
        "primary": "features",
        "recommended": [
            "content-container", 
            "icon-based", 
            "product-highlight", 
            "consideration-stage"
        ]
    },
    "cta": {
        "primary": "cta",
        "recommended": [
            "action-trigger", 
            "conversion-focused", 
            "simple", 
            "decision-stage"
        ]
    },
    "footer": {
        "primary": "footer",
        "recommended": [
            "navigation-element", 
            "below-fold", 
            "text-heavy", 
            "full-width"
        ]
    },
    "header": {
        "primary": "header",
        "recommended": [
            "navigation-element", 
            "above-fold", 
            "fixed-position", 
            "responsive-mobile"
        ]
    },
    "faq": {
        "primary": "faq",
        "recommended": [
            "disclosure", 
            "text-heavy", 
            "consideration-stage", 
            "trust-building"
        ]
    },
    "contact": {
        "primary": "contact",
        "recommended": [
            "form-element", 
            "lead-generation", 
            "decision-stage"
        ]
    }
}


def get_all_tags() -> List[str]:
    """Get all available tags.

    Returns:
        List of all tags across all categories.
    """
    return ALL_TAGS


def get_tags_by_category(category: str) -> List[str]:
    """Get tags for a specific category.

    Args:
        category: The category to get tags for.

    Returns:
        List of tags in the specified category.

    Raises:
        ValueError: If the category doesn't exist.
    """
    if category not in TAG_CATEGORIES:
        raise ValueError(
            f"Unknown tag category: {category}. Available categories: {list(TAG_CATEGORIES.keys())}"
        )
    
    return TAG_CATEGORIES[category]


def get_recommended_tags_for_component(component_name: str) -> Dict[str, Any]:
    """Get recommended tags for a specific component.

    Args:
        component_name: Name of the component to get tags for.

    Returns:
        Dictionary with primary and recommended tags.

    Raises:
        ValueError: If the component doesn't have predefined tags.
    """
    component_name = component_name.lower()
    
    # Try exact match
    if component_name in COMMON_COMPONENT_TAGS:
        return COMMON_COMPONENT_TAGS[component_name]
    
    # Try partial match
    for key in COMMON_COMPONENT_TAGS:
        if key in component_name or component_name in key:
            return COMMON_COMPONENT_TAGS[key]
    
    raise ValueError(
        f"No predefined tags for component: {component_name}. "
        f"Available components: {list(COMMON_COMPONENT_TAGS.keys())}"
    )


def filter_tags(
    categories: Optional[List[str]] = None,
    exclude_categories: Optional[List[str]] = None,
    search_term: Optional[str] = None
) -> List[str]:
    """Filter tags based on categories and search term.

    Args:
        categories: List of categories to include.
        exclude_categories: List of categories to exclude.
        search_term: Term to search for in tag names.

    Returns:
        List of filtered tags.
    """
    result = set()
    
    # If no categories specified, use all
    if not categories:
        categories = list(TAG_CATEGORIES.keys())
    
    # If exclude_categories specified, remove them
    if exclude_categories:
        categories = [c for c in categories if c not in exclude_categories]
    
    # Collect tags from specified categories
    for category in categories:
        if category in TAG_CATEGORIES:
            result.update(TAG_CATEGORIES[category])
    
    # Filter by search term if provided
    if search_term:
        search_term = search_term.lower()
        result = {tag for tag in result if search_term in tag.lower()}
    
    return sorted(list(result))


def validate_tags(tags: List[str]) -> List[str]:
    """Validate a list of tags against known tags.

    Args:
        tags: List of tags to validate.

    Returns:
        List of valid tags.
    """
    valid_tags = set(ALL_TAGS)
    return [tag for tag in tags if tag in valid_tags]


def export_tags_to_json(filepath: str) -> None:
    """Export all tag data to a JSON file.

    Args:
        filepath: Path to save the JSON file.
    
    Raises:
        IOError: If the file cannot be written.
    """
    data = {
        "categories": TAG_CATEGORIES,
        "common_component_tags": COMMON_COMPONENT_TAGS,
        "all_tags": ALL_TAGS
    }
    
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        raise IOError(f"Failed to write tags to {filepath}: {str(e)}")