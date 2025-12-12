"""CLI for component processing operations."""

import argparse
import json
import sys
import os
from typing import Dict, Any

from ..component_processor import ComponentProcessor
from ..implementations.shadcn_to_ts import ShadcnToTypeScriptConverter
from ..implementations.json_generator import JsonSchemaDataGenerator
from ..logger import logger, setup_logger
from ..completion import LiteLLMCompletion


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(description="Component processing tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Process component command
    process_parser = subparsers.add_parser("process", help="Process a shadcn component")
    process_parser.add_argument("--file", required=True, help="Path to the component file")
    process_parser.add_argument("--output", help="Output file for JSON result (default: stdout)")
    
    # Convert component command
    convert_parser = subparsers.add_parser("convert", help="Convert a component to TypeScript")
    convert_parser.add_argument("--file", required=True, help="Path to the component file")
    convert_parser.add_argument("--output-dir", help="Directory to save output files (default: current directory)")
    
    # Generate JSON data command
    generate_parser = subparsers.add_parser("generate", help="Generate JSON data from schema")
    generate_parser.add_argument("--schema", required=True, help="Path to JSON schema file")
    generate_parser.add_argument("--prompt", required=True, help="User prompt for data generation")
    generate_parser.add_argument("--count", type=int, default=1, help="Number of examples to generate")
    generate_parser.add_argument("--output", help="Output file for JSON result (default: stdout)")
    
    return parser.parse_args()


def read_component_file(file_path: str) -> str:
    """Read component file content.

    Args:
        file_path: Path to the component file.

    Returns:
        Component file content.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there's an error reading the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Component file not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading component file {file_path}: {str(e)}")


def read_json_file(file_path: str) -> Dict[str, Any]:
    """Read and parse JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        Parsed JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If there's an error reading the file.
        json.JSONDecodeError: If the file doesn't contain valid JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading JSON file {file_path}: {str(e)}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {str(e)}", e.doc, e.pos)


def write_file(content: str, file_path: str) -> None:
    """Write content to a file.

    Args:
        content: Content to write.
        file_path: Path to the output file.

    Raises:
        IOError: If there's an error writing the file.
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except IOError as e:
        raise IOError(f"Error writing file {file_path}: {str(e)}")


def process_component(args: argparse.Namespace) -> int:
    """Process a shadcn component.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    try:
        component_code = read_component_file(args.file)
        
        # Process the component
        processor = ComponentProcessor()
        result = processor.process_component(component_code, args.file)
        
        # Output the result
        output_json = json.dumps(result, indent=2)
        
        if args.output:
            write_file(output_json, args.output)
            logger.info(f"Component processing result written to {args.output}")
        else:
            print(output_json)
            
        return 0
        
    except Exception as e:
        logger.error(f"Error processing component: {str(e)}")
        return 1


def convert_component(args: argparse.Namespace) -> int:
    """Convert a component to TypeScript.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    try:
        component_code = read_component_file(args.file)
        
        # Convert the component
        converter = ShadcnToTypeScriptConverter()
        ts_component, props_file, metadata = converter.convert(component_code)
        
        # Determine output directory
        output_dir = args.output_dir if args.output_dir else os.path.dirname(args.file)
        
        # Determine file names
        component_name = metadata.get("name", os.path.splitext(os.path.basename(args.file))[0])
        component_file = metadata.get("file_name", f"{component_name}.tsx")
        props_file_name = metadata.get("props_file_name", f"{component_name}.props.ts")
        
        # Write the files
        component_path = os.path.join(output_dir, component_file)
        props_path = os.path.join(output_dir, props_file_name)
        
        write_file(ts_component, component_path)
        write_file(props_file, props_path)
        
        logger.info(f"Component converted successfully:")
        logger.info(f"  - Component: {component_path}")
        logger.info(f"  - Props: {props_path}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error converting component: {str(e)}")
        return 1


def generate_json_data(args: argparse.Namespace) -> int:
    """Generate JSON data from schema.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    try:
        schema = read_json_file(args.schema)
        
        # Generate the data
        generator = JsonSchemaDataGenerator()
        data = generator.generate_data(
            schemas=schema,
            user_prompt=args.prompt,
            num_examples=args.count
        )
        
        # Output the result
        output_json = json.dumps(data, indent=2)
        
        if args.output:
            write_file(output_json, args.output)
            logger.info(f"Generated JSON data written to {args.output}")
        else:
            print(output_json)
            
        return 0
        
    except Exception as e:
        logger.error(f"Error generating JSON data: {str(e)}")
        return 1


def main() -> int:
    """Main entry point for the CLI.
    
    Returns:
        Exit code (0 for success, non-zero for error).
    """
    # Set up logging
    setup_logger(level=20)  # INFO level
    
    try:
        args = parse_arguments()
        
        if args.command == "process":
            return process_component(args)
            
        elif args.command == "convert":
            return convert_component(args)
            
        elif args.command == "generate":
            return generate_json_data(args)
            
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1
            
    except Exception as e:
        logger.error(f"Error executing command: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())