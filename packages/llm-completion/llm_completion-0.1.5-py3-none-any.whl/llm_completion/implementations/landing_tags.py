"""Implementation for finding tags for landing pages."""

from typing import List, Optional, Dict, Any
import json

from ..completion import LiteLLMCompletion
from ..logger import logger
from ..tag_manager import TagManager


class LandingPageTagFinder:
    """Component tag finder for landing pages."""

    def __init__(
        self, 
        completion_provider: Optional[LiteLLMCompletion] = None,
    ) -> None:
        """Initialize the tag finder.

        Args:
            completion_provider: Optional completion provider to use when API is needed.
                If not provided and use_api is True, a new instance will be created.
            use_api: Whether to use the API for tag finding or use built-in tag data.
        """
        self.completion_provider = completion_provider or LiteLLMCompletion()
        
        # Initialize the tag manager for local tag operations
        # self.tag_manager = TagManager()
        
        self.system_prompt = (
            "You are a UI/UX expert specializing in landing page design."
                        """
            Here's a comprehensive tagging system for shadcn components in a landing page context, designed for scalability, searchability, and maintainability:

### **1. Primary Structural Tags (Mandatory)**
The main section identifier:
- `hero`  
- `header`  
- `footer`  
- `cta` (Call-to-Action)  
- `testimonials`  
- `features`  
- `pricing`  
- `faq`  
- `contact`  
- `team`  
- `stats` (Metrics/KPIs)  
- `newsletter`  
- `banner`  
- `gallery`  
- `partners` (Logo cloud)  
- `showcase` (Product demo)  
- `process` (How it works)  

---

### **2. Component Function Tags**
Describes the component's purpose:
- `action-trigger` (Buttons, links)  
- `data-display` (Stats, progress bars)  
- `content-container` (Cards, modals)  
- `form-element` (Inputs, selectors)  
- `feedback` (Alerts, toasts)  
- `navigation-element` (Breadcrumbs, pagination)  
- `social-proof` (Testimonials, trust badges)  
- `disclosure` (Accordions, tooltips)  
- `media-display` (Image/video players)  
- `state-indicator` (Loaders, status badges)  

---

### **3. Content Type Tags**
Content the component holds:
- `text-heavy`  
- `visual-dominant` (Images/video focus)  
- `icon-based`  
- `form`  
- `interactive-element`  
- `data-visualization`  
- `mixed-media`  

---

### **4. Styling & Theme Tags**
Visual characteristics:
- `minimalist`  
- `bold`  
- `dark-mode`  
- `gradient`  
- `glassmorphism`  
- `neumorphic`  
- `skeuomorphic`  
- `flat-design`  
- `animated`  
- `gradient-border`  
- `shadow-heavy`  
- `rounded`  

---

### **5. Technical Behavior Tags**
Functional attributes:
- `responsive-mobile`  
- `responsive-desktop`  
- `interactive` (Hover/click effects)  
- `static`  
- `dynamic-content` (API-driven)  
- `lazy-loaded`  
- `fixed-position`  
- `sticky-element`  
- `accessibility-optimized`  
- `performance-critical`  

---

### **6. Placement Context Tags**
Where it appears:
- `above-fold`  
- `below-fold`  
- `full-width`  
- `container-bound`  
- `floating-element`  
- `section-divider`  
- `overlay`  

---

### **7. Marketing Purpose Tags**
Business objectives:
- `lead-generation`  
- `conversion-focused`  
- `brand-awareness`  
- `product-highlight`  
- `trust-building`  
- `engagement`  
- `scarcity-timer`  

---

### **8. Component Complexity Tags**
Development effort:
- `simple`  
- `composite` (Multiple sub-components)  
- `animated-complex`  
- `custom-integration` (3rd party libs)  
- `theme-variant`  

---

### **9. Audience Stage Tags**
User journey alignment:
- `awareness-stage`  
- `consideration-stage`  
- `decision-stage`  
- `retention-focused`  

---

### **Example Tagging in Practice**
**Hero Section Component:**  
`hero` | `action-trigger` | `visual-dominant` | `animated` | `above-fold` | `conversion-focused` | `awareness-stage`

**Pricing Card Component:**  
`pricing` | `content-container` | `text-heavy` | `neumorphic` | `interactive` | `decision-stage` | `conversion-focused`

**Testimonial Slider:**  
`testimonials` | `social-proof` | `mixed-media` | `responsive-mobile` | `trust-building` | `consideration-stage`

---

### **Implementation Tips**
1. **Consistency:** Use a controlled vocabulary (tag dictionary)  
2. **Priority:** Assign 1 primary tag + 2-5 secondary tags  
3. **Automation:** Generate tags from component props (e.g. `<Button animated responsive cta />`)  
4. **Filtering:** Enable multi-axis filtering (e.g. `function=cta` + `style=glassmorphism`)  
5. **Visual Indicators:** Color-code tag categories in your design system  

This structure supports:  
- Design consistency audits  
- A/B test component selection  
- Responsive behavior filtering  
- Personalization workflows  
- Component discovery for developers  
- Marketing goal tracking  

Always include a primary tag (called category), Marketing Purpose Tag, and 2-5 secondary tags for each component. This ensures clarity while allowing flexibility in categorization.
"""
        )

    def get_category_tags_map(
        self,
        user_input: str,
        count: int = 9,
        focus: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        Return a dictionary mapping categories to their relevant tags for landing page components.

        Args:
            components: List of available component names.
            count: Minimum number of components to select.
            focus: Optional focus area (e.g., 'conversion', 'trust').

        Returns:
            Dictionary mapping categories to their relevant tags.
        """
        logger.info(f"Finding landing page category tags from user input: {user_input}")

        try:
            prompt = (
                f"As a UI/UX expert, select at least {count} components in sequence for a landing page from the following list.\n"
                "Choose components that work well together for a modern, effective landing page.\n"
                "Format your response as a JSON array.\n\n"
                f"User Input: {user_input}\n\n"
                "Remember to:\n"
                f"1. Select at least {count} components\n"
                "2. Choose components that logically work together\n"
                "3. Return only a valid JSON array of categories & tags\n\n"
                "4. It should return category_tags_map: List of dict mapping category and tags e.g.\n"
                "[{category: category1, tags: [tag1, tag2]}, {category: category2, tags: [tag3, tag4]}, ...]\n"
            )
            
            # Define schema for the response
            schema = {
                "type": "object",
                "properties": {
                    "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                        "category": { "type": "string" },
                        "tags": {
                            "type": "array",
                            "items": { "type": "string" }
                        }
                        },
                        "required": ["category", "tags"]
                    }
                    }
                },
                "required": ["data"]
                }

            
            result = self.completion_provider.complete_with_json(prompt, self.system_prompt, json_schema=schema)

        except Exception as e:
            logger.error(f"API approach failed for finding landing page tags: {str(e)}")
            raise

        return result['data'] if 'data' in result else result

