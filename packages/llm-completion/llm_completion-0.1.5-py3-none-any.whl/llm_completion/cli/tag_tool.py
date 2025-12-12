"""CLI for tag management operations."""

import argparse
import json
import sys
from typing import List, Dict, Any, Optional

from ..tag_manager import TagManager
from ..implementations.landing_tags import LandingPageTagFinder
from ..logger import logger, setup_logger


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(description="Landing page tag management tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Search tags command
    search_parser = subparsers.add_parser("search", help="Search for tags")
    search_parser.add_argument("query", help="Search term")
    
    # List components command
    list_parser = subparsers.add_parser("list", help="List recommended components")
    list_parser.add_argument("--count", type=int, default=5, help="Number of components to list")
    list_parser.add_argument("--focus", choices=["conversion", "trust", "awareness", "engagement"], 
                            help="Focus area for the landing page")
    
    # Get component tags command
    tags_parser = subparsers.add_parser("tags", help="Get tags for a component")
    tags_parser.add_argument("component", help="Component name")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export tag data")
    export_parser.add_argument("--format", choices=["json", "text"], default="json", 
                              help="Export format")
    export_parser.add_argument("--output", help="Output file (default: stdout)")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze landing page components")
    analyze_parser.add_argument("--components", required=True, help="JSON file or string with component list")
    
    return parser.parse_args()


def format_output(data: Any, output_format: str = "json") -> str:
    """Format output data according to specified format.
    
    Args:
        data: The data to format.
        output_format: Format to use ('json' or 'text').
        
    Returns:
        Formatted string.
    """
    if output_format == "json":
        return json.dumps(data, indent=2)
    
    # Text format
    if isinstance(data, list):
        return "\n".join(str(item) for item in data)
    elif isinstance(data, dict):
        return "\n".join(f"{k}: {v}" for k, v in data.items())
    else:
        return str(data)


def write_output(content: str, output_file: Optional[str] = None) -> None:
    """Write content to output file or stdout.
    
    Args:
        content: Content to write.
        output_file: Path to output file or None for stdout.
        
    Raises:
        IOError: If unable to write to the output file.
    """
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(content)
        except IOError as e:
            raise IOError(f"Failed to write to {output_file}: {str(e)}")
    else:
        print(content)


def load_components(components_input: str) -> List[Dict[str, Any]]:
    """Load components from file or JSON string.
    
    Args:
        components_input: Path to JSON file or JSON string.
        
    Returns:
        List of component dictionaries.
        
    Raises:
        ValueError: If unable to parse components.
    """
    try:
        # Try to parse as JSON string
        return json.loads(components_input)
    except json.JSONDecodeError:
        # Try to load as file
        try:
            with open(components_input, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load components: {str(e)}")


def main() -> int:
    """Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    # Set up logging
    setup_logger(level=20)  # INFO level
    
    try:
        args = parse_arguments()
        
        # Initialize tag manager
        tag_manager = TagManager()
        
        if args.command == "search":
            results = tag_manager.search_tags(args.query)
            output = format_output(results)
            write_output(output)
            
        elif args.command == "list":
            tag_finder = LandingPageTagFinder(use_api=False)
            components = tag_finder.tag_manager.get_component_combinations(
                count=args.count, 
                focus=args.focus
            )
            output = format_output(components)
            write_output(output)
            
        elif args.command == "tags":
            tag_finder = LandingPageTagFinder(use_api=False)
            tags = tag_finder.get_tags_for_component(args.component)
            output = format_output(tags)
            write_output(output)
            
        elif args.command == "export":
            from ..resources.tag_data import TAG_CATEGORIES, COMMON_COMPONENT_TAGS
            
            export_data = {
                "categories": {k: TAG_CATEGORIES[k] for k in TAG_CATEGORIES},
                "components": COMMON_COMPONENT_TAGS
            }
            
            output = format_output(export_data, args.format)
            write_output(output, args.output)
            
        elif args.command == "analyze":
            tag_finder = LandingPageTagFinder(use_api=False)
            components = load_components(args.components)
            analysis = tag_finder.analyze_component_structure(components)
            output = format_output(analysis)
            write_output(output)
            
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1
            
        return 0
        
    except Exception as e:
        logger.error(f"Error executing command: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())