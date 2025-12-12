"""Command-line entry point for the LLM completion library."""

import sys
import argparse

from .cli.tag_tool import main as tag_tool_main
from .cli.component_tool import main as component_tool_main
from .logger import setup_logger


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(description="LLM Completion Library CLI")
    
    subparsers = parser.add_subparsers(dest="tool", help="Tool to use")
    
    # Tag tool
    tag_parser = subparsers.add_parser("tags", help="Tag management tool")
    tag_parser.add_argument("command", nargs="?", default="help", 
                           help="Command to execute (search, list, tags, export, analyze)")
    tag_parser.add_argument("args", nargs="*", help="Command arguments")
    
    # Component tool
    component_parser = subparsers.add_parser("component", help="Component processing tool")
    component_parser.add_argument("command", nargs="?", default="help",
                                 help="Command to execute (process, convert, generate)")
    component_parser.add_argument("args", nargs="*", help="Command arguments")
    
    return parser.parse_args()


def main() -> int:
    """Main CLI entry point.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    setup_logger()
    
    args = parse_args()
    
    if args.tool == "tags":
        # Reconstruct sys.argv for the tag tool
        sys.argv = [sys.argv[0]] + [args.command] + args.args
        return tag_tool_main()
        
    elif args.tool == "component":
        # Reconstruct sys.argv for the component tool
        sys.argv = [sys.argv[0]] + [args.command] + args.args
        return component_tool_main()
        
    else:
        print("Available tools:")
        print("  tags - Tag management tool")
        print("  component - Component processing tool")
        return 0


if __name__ == "__main__":
    sys.exit(main())