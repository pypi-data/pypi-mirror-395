"""Command-line interface for naive_knowledge_base."""

import sys
import argparse
from pathlib import Path
import os
import dotenv

# Define version locally
__version__ = "0.1.0"

# Add current directory to path to allow local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import dependencies
try:
    from smolagents import CodeAgent, ToolCallingAgent
    from agents.dependency_graph import generate_dependency_graph
    from api_models import FlowApiModel
    from tools import (
        save_content_to_file,
        read_file_content,
        delete_folder_or_file,
        generate_folder_tree,
    )
except ImportError as e:
    print(f"Error importing dependencies: {e}", file=sys.stderr)
    print("Please install dependencies: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)


def run_analysis(source_directory: str, file_extensions: str = "java", 
                 ignore_dirs: str = "target,.git,test,node_modules,Pods") -> str:
    """
    Run dependency graph analysis on a source directory.
    
    Args:
        source_directory: Path to the source code directory to analyze
        file_extensions: File extensions to analyze (default: "java")
        ignore_dirs: Comma-separated list of directories to ignore
        
    Returns:
        str: Analysis results
    """
    dotenv.load_dotenv()
    
    dependency_graph_agent = ToolCallingAgent(
        tools=[generate_dependency_graph],
        planning_interval=1,
        final_answer_checks=[],
        model=FlowApiModel(
            model_id="gpt-4.1",
            temperature=0.4,
        ),
        max_steps=7,
        name="dependency_graph_agent",
        description="Generates a dependency graph for the given source directory.",
    )
    
    manager_agent = CodeAgent(
        managed_agents=[dependency_graph_agent],
        model=FlowApiModel(model_id="gpt-4.1"),
        tools=[
            read_file_content,
            save_content_to_file,
            delete_folder_or_file,
            generate_folder_tree
        ],
        additional_authorized_imports=[
            "os",
            "json",
            "pandas",
            "numpy",
            "pathlib",
            "ast",
            "re",
            "networkx",
            "collections",
        ],
        planning_interval=3,
        max_steps=30,
        name="tech_lead_agent",
        description="This agent is responsible for building and analyzing dependency graphs from source code.",
    )
    
    result = manager_agent.run(
        f"Generate the tree and dependency graph of the {file_extensions} files in the source: "
        f"{source_directory}. Make sure to ignore the {ignore_dirs} directories."
    )
    
    return result


def create_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="naive-kb",
        description="Analyze code dependencies and generate dependency graphs using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a Java project
  naive-kb /path/to/project

  # Analyze with specific file extensions
  naive-kb /path/to/project --extensions python

  # Ignore specific directories
  naive-kb /path/to/project --ignore "target,build,.git,node_modules"

  # Full example
  naive-kb /path/to/project --extensions java --ignore "target,.git,test"
        """
    )
    
    parser.add_argument(
        "source_directory",
        type=str,
        help="Path to the source code directory to analyze"
    )
    
    parser.add_argument(
        "-e", "--extensions",
        type=str,
        default="java",
        help="File extensions to analyze (default: java)"
    )
    
    parser.add_argument(
        "-i", "--ignore",
        type=str,
        default="target,.git,test,node_modules,Pods",
        help="Comma-separated list of directories to ignore (default: target,.git,test,node_modules,Pods)"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "--env-file",
        type=str,
        help="Path to .env file (default: .env in current directory)"
    )
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Load environment variables
    if args.env_file:
        dotenv.load_dotenv(args.env_file)
    else:
        dotenv.load_dotenv()
    
    # Validate source directory
    source_path = Path(args.source_directory)
    if not source_path.exists():
        print(f"Error: Source directory '{args.source_directory}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if not source_path.is_dir():
        print(f"Error: '{args.source_directory}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    print(f"Analyzing source directory: {args.source_directory}")
    print(f"File extensions: {args.extensions}")
    print(f"Ignoring directories: {args.ignore}")
    print("\nRunning analysis...")
    
    try:
        result = run_analysis(
            source_directory=args.source_directory,
            file_extensions=args.extensions,
            ignore_dirs=args.ignore
        )
        
        print("\n" + "=" * 80)
        print("Analysis Complete!")
        print("=" * 80)
        print(result)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user.", file=sys.stderr)
        return 130
        
    except Exception as e:
        print(f"\nError running analysis: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
