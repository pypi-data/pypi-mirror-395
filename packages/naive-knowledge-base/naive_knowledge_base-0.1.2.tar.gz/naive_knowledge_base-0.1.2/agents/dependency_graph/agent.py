from smolagents import tool
from emerge.appear import Emerge
from .model import DependencyGraph
import os
import json
from toon_format import encode
from tools import save_content_to_file, delete_folder_or_file

@tool
def generate_dependency_graph(source_directory: str, permit_file_extensions: list[str], ignore_directories_containing: list[str]) -> str:
    """
    Generates a dependency graph for the given source directory.
    Args:
        source_directory: The source directory to analyze.
        permit_file_extensions: The file extensions to permit in the analysis.
        ignore_directories_containing: The directories to ignore in the analysis.
    Returns:
        str: The dependency graph file path.
    Raises:
        ValueError: If the source directory does not exist or is not a directory.
    """
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        raise ValueError(f"Source directory does not exist: {source_directory}")

    # Check if the source directory is a directory
    if not os.path.isdir(source_directory):
        raise ValueError(f"Source path is not a directory: {source_directory}")
    
    export_directory = os.path.join(source_directory, "export")

    # Create the Emerge configuration YAML file
    yaml_content = _create_emerge_config_yaml(source_directory, export_directory, permit_file_extensions, ignore_directories_containing)
    
    # Write the YAML content to a file
    yaml_file_path = _write_emerge_config_yaml(yaml_content)
    
    # Run Emerge with the generated YAML file
    try:
        _run_emerge(yaml_file_path)
    except Exception as e:
        raise ValueError(f"Failed to generate dependency graph: {e}")
    
    dependency_graph = _transform_graph(source_directory)

    # Delete the Emerge configuration YAML file
    try:
        delete_folder_or_file(yaml_file_path)
        delete_folder_or_file(export_directory)
        print(f"Deleting Emerge configuration file: {yaml_file_path}")
    except Exception as e:
        raise ValueError(f"Failed to delete Emerge configuration file: {e}")
    
    # Transform the dependency graph into a more readable format
    # content = encode(dependency_graph)

    # file_path = save_content_to_file(
    #     content=content,
    #     source_directory=source_directory,
    #     file_name="dependency_graph.toon"
    # )

    file_path = save_content_to_file(
        content=json.dumps(dependency_graph, indent=2),
        source_directory=source_directory,
        file_name="dependency_graph.json"
    )

    return f"Dependency graph saved to {file_path}"
    
def _create_emerge_config_yaml(source_directory: str, export_dir: str, permit_file_extensions: list[str], ignore_directories_containing: list[str]) -> str:
    """
    Generates a sample YAML configuration for Emerge to be used by write_emerge_config_yaml.
    Args:
        source_directory: The source directory to analyze.
        permit_file_extensions: The file extensions to permit in the analysis.
        ignore_directories_containing: The directories to ignore in the analysis.
    Returns:
        str: The YAML configuration as a string.
    """
    export_directory = export_dir
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)
    return f"""
---
project_name: java_project_example
loglevel: info
analyses:
- analysis_name: full typescript check
  source_directory: {source_directory}
  only_permit_file_extensions: {permit_file_extensions}
  ignore_dependencies_containing:
    - java
    - javax
    - org
    - och
    - lambda
    - javafx
    - jakarta
    - io.cloudevents
    - fasterxml
    - lombok
    - dtcloyalty.lib.idempotentconsumer
    - dtcloyalty.lib.outboxpattern
    - feign
    - io
    - lib.programawaredatasource
    - lib.programproperties
    - com.algolia
  ignore_directories_containing: {ignore_directories_containing}
  file_scan:
  - number_of_methods
  - source_lines_of_code
  - dependency_graph
  - fan_in_out
  - louvain_modularity
  - tfidf
  export:
  - directory: {export_directory}
  - graphml
  - json
  - tabular_file
  - tabular_console_overall
  - d3
    """
        
def _write_emerge_config_yaml(yaml_content: str) -> str:
    """
    Creates a YAML configuration file for Emerge to be used by run_emerge.
    Args:
        yaml_content: The content of the YAML configuration.
    Returns:
        str: The path to the generated YAML configuration file.
    """
    yaml_file_path = "/tmp/emerge_config.yaml"
    with open(yaml_file_path, "w") as yaml_file:
        yaml_file.write(yaml_content)
    
    return yaml_file_path

def _run_emerge(yaml_file_path: str) -> None:
    """
    Runs Emerge on the given source path.
    Args:
        yaml_file_path: The yaml path to the YAML configuration file.
    Returns:
        str: The result of the Emerge analysis.
    """
    try:
        emerge = Emerge()
        emerge.load_config(yaml_file_path)
        emerge.start_analyzing()
    except Exception as e:
        raise ValueError(f"Failed to run Emerge: {e}")
    
def _transform_graph(source_directory: str) -> list[DependencyGraph]:
    """
    Transforms the dependency graph into a more readable format.
    Args:
        source_directory: The source directory to transform the emerge-file_result_dependency_graph-data.json file.
    Returns:
        object: The transformed dependency graph.
    """

    emerge_file_path = os.path.join(source_directory, "export", "emerge-file_result_dependency_graph-data.json")
    if not os.path.exists(emerge_file_path):
        raise ValueError(f"Emerge file not found: {emerge_file_path}")
    with open(emerge_file_path, "r") as emerge_file:
        emerge_data = emerge_file.read()
    
    return _process_data(json.loads(emerge_data), source_directory)

def _process_data(json_data, source_directory) -> list[DependencyGraph]:
    # Step 1: Filter nodes with absolute_name
    relevant_nodes = [node for node in json_data['nodes'] if 'absolute_name' in node]
    
    # Step 2: Map dependencies based on links
    dependency_map = {}
    
    for link in json_data['links']:
        if link['source'] not in dependency_map:
            dependency_map[link['source']] = []
        target = os.path.join(source_directory, link['target'])
        dependency_map[link['source']].append(target)
    
    # Step 3: Create the final array
    result = []
    for node in relevant_nodes:
        absolute_name = node['absolute_name']
        file_path = os.path.join(source_directory, absolute_name.split('/', 1)[1])
        
        
        # Get metrics (with proper error handling for missing values)
        fan_in = node.get('metric_fan-in-dependency-graph', 0)
        fan_out = node.get('metric_fan-out-dependency-graph', 0)
        modularity_level = node.get('metric_file_result_dependency_graph_louvain-modularity-in-file', 0)
        number_of_methods = node.get('metric_number-of-methods-in-file', 0)
        source_lines_of_code = node.get('metric_sloc-in-file', 0)
        
        result.append({
            "absolutePath": str(file_path),
            "fanIn": fan_in,
            "fanOut": fan_out,
            "sourceLinesOfCode": source_lines_of_code,
            "numberOfMethods": number_of_methods,
            "louvainModularity": modularity_level,
            "displayName": node.get('display_name', ''),
            "dependencies":dependency_map.get(absolute_name, [])
        })

    return result