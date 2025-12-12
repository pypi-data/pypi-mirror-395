"""Implementation for converting Shadcn components to TypeScript."""

from typing import Dict, Any, Optional, Tuple
import json
import re

from ..completion import LiteLLMCompletion
from ..logger import logger
from ..utils import extract_code_from_markdown


class ShadcnToTypeScriptConverter:
    """Converter for Shadcn React components to TypeScript."""

    def __init__(self, completion_provider: Optional[LiteLLMCompletion] = None) -> None:
        """Initialize the converter.

        Args:
            completion_provider: Optional completion provider to use. If not provided,
                a new instance will be created.
        """
        self.completion_provider = completion_provider or LiteLLMCompletion()
        self.system_prompt = (
            "You are a TypeScript expert specializing in React component conversion."
            """
Use following guidelines while converting shadcn components to typescript. Need to replace Icon, Image and Link components (and their variants) with proper usage as per guidelines below,

For Icon Components :
    1. Following interface should be used:
        interface Icon {
        package: 'lucide';
        name: string; // known lucide react icon-name only
        type: 'icon';
        }
    2. Following will be the usage example:
    
        import DynamicIcon from "@/components/DynamicIcon";

        <DynamicIcon name="Home" className="<retain className of original component>" />

For Image Components:
    1. Following interface should be used:
        interface ImageProps {
            src: string;
            alt: string;
            width?: number;
            height?: number;
            priority?: boolean;
            quality?: number;
            sizes?: string;
            fill?: boolean;
            placeholder?: 'blur' | 'empty';
            blurDataURL?: string;
            style?: React.CSSProperties;
            className?: string;
            type?: 'background' | 'profile' | 'logo' | 'banner' | 'gallery' | 'thumbnail' | 'icon' | 'other';
        }
    2. Following will be the usage example:
    
        import Image from "@/components/Image";

        <Image
            src="/path/to/image.jpg"
            alt="Description of image"
            width={500}
            height={300}
            className="<retain className of original component>"
        />

For Link Components:
    1. Following interface should be used:
        interface LinkProps {
            href: string;
            target?: '_blank' | '_self';
            rel?: string;
        }
    2. Every Anchor tag should use the following structure:
        import Link from "@/components/Link";
        <Link href="your-link-here" className="<retain className of original component>" target="_blank" rel="noopener noreferrer">
        </Link>
"""
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

    def convert(self, component_code: str, demo_code: str = None) -> Dict[str, Any]:
        """Convert a Shadcn component to TypeScript.

        Args:
            component_code: The React component code to convert.
            demo_code: Optional demo code for the component.

        Returns:
            Tuple containing (typescript_component, props_file_content, metadata)

        Raises:
            Exception: If the conversion fails.
        """
        logger.info("Converting Shadcn component to TypeScript")
        
        prompt = (
            "Convert following react component code to typescript compatible code with proper props types and export statement.\n"
            "- Convert any button to button embedded Link component using asChild of shadcn button prop. For e.g.\n\n"
            """<Button asChild>
      <Link href="/login">Login</Link>
    </Button>\n\n"""
            "- Ensure that the component is compatible with TypeScript and follows best practices for type definitions.\n"
            "- Create Props in same file.\n"
            "- Extract the user visible things like Text, Button, URL, Image, etc as props. \n"
            "- Extract any hardcoded user visible values (including href, alt, src, etc), default values, demo data, mockups, etc with appropriate props types.\n"
            "- Ensure all colors are from tailwind config only. If not, convert them to tailwind config colors.\n"
            "- Remove any Background Image and Background Color from existing components from top level as we are adding it ourself. Don't remove effects from background.\n"
            ".\n"
            f"```\n\n{component_code}\n\n```"
            + ("Given following concrete variation of above component. Create a typescript variation code for it that will follow same guidelines as above and use above component as base with proper imports." if demo_code else "")
            + (f"\n```\n{demo_code}\n\n```" if demo_code else "")
            + "Give only json for component ts code, variation ts code (if applicable otherwise empty string) component name, props_file_name, component props name, category and tags in following format,\n\n"
            "{\n"
            '"name": "<component name>",\n'
            '"component_ts_code": "<component ts code>",\n'
            '"variation_ts_code": "<variation ts code>",\n'
            '"props": "<component props name>",\n'
            '"category": "<component category>",\n'
            '"tags": [<component tags>]\n'
            "}\n"
        )

        try:
            # Define schema for TypeScript interface response
            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "component_ts_code": {"type": "string"},
                    "variation_ts_code": {"type": "string"},
                    "props": {"type": "string"},
                    "category": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["name", "component_ts_code", "props", "category", "tags"]
            }
            
            
            result = self.completion_provider.complete_with_json(prompt, self.system_prompt, json_schema=schema)
            
            logger.info("Successfully converted component to TypeScript")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to convert component to TypeScript: {str(e)}")
            raise

    async def aconvert(self, component_code: str, demo_code: str = None) -> Dict[str, Any]:
        """Asynchronously convert a Shadcn component to TypeScript.

        Args:
            component_code: The React component code to convert.
            demo_code: Optional demo code for the component.

        Returns:
            Tuple containing (typescript_component, props_file_content, metadata)

        Raises:
            Exception: If the conversion fails.
        """
        logger.info("Async converting Shadcn component to TypeScript")
        
        prompt = (
            "Convert following react component code to typescript compatible code with proper props types and export statement.\n"
            "- Convert any button to button embedded Link component using asChild of shadcn button prop. For e.g.\n\n"
            """<Button asChild>
      <Link href="/login">Login</Link>
    </Button>\n\n"""
            "- Ensure that the component is compatible with TypeScript and follows best practices for type definitions.\n"
            "- Create Props in same file.\n"
            "- Extract the user visible things like Text, Button, URL, Image, etc as props. \n"
            "- Extract any hardcoded user visible values (including href, alt, src, etc), default values, demo data, mockups, etc with appropriate props types.\n"
            "- Ensure all colors are from tailwind config only. If not, convert them to tailwind config colors.\n"
            "- Remove any Background Image and Background Color from existing components from top level as we are adding it ourself. Don't remove effects from background.\n"
            ".\n"
            f"```\n\n{component_code}\n\n```"
            + ("Given following concrete variation of above component. Create a typescript variation code for it that will follow same guidelines as above and use above component as base with proper imports." if demo_code else "")
            + (f"\n```\n{demo_code}\n\n```" if demo_code else "")
            + "Give only json for component ts code, variation ts code (if applicable otherwise empty string) component name, props_file_name, component props name, category and tags in following format,\n\n"
            "{\n"
            '"name": "<component name>",\n'
            '"component_ts_code": "<component ts code>",\n'
            '"variation_ts_code": "<variation ts code>",\n'
            '"props": "<component props name>",\n'
            '"category": "<component category>",\n'
            '"tags": [<component tags>]\n'
            "}\n"
        )

        try:
            # Define schema for TypeScript interface response
            schema = {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "component_ts_code": {"type": "string"},
                    "variation_ts_code": {"type": "string"},
                    "props": {"type": "string"},
                    "category": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["name", "component_ts_code", "props", "category", "tags"]
            }
            
            
            result = await self.completion_provider.acomplete_with_json(prompt, self.system_prompt, json_schema=schema)
            
            logger.info("Successfully async converted component to TypeScript")
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to async convert component to TypeScript: {str(e)}")
            raise
