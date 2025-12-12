from smolagents import tool
import os
from tools import save_content_to_file, delete_folder_or_file
from directory_tree import DisplayTree

@tool
def generate_folder_tree(source_directory: str, ignore_directories_containing: list[str]) -> str:
    """
    Generates a folder tree for the given source directory.
    Args:
        source_directory: The source directory to analyze.
        permit_file_extensions: The file extensions to permit in the analysis.
        ignore_directories_containing: The directories to ignore in the analysis.
    Returns:
        str: The folder tree file path.
    Raises:
        ValueError: If the source directory does not exist or is not a directory.
    """
    # Check if the source directory exists
    if not os.path.exists(source_directory):
        raise ValueError(f"Source directory does not exist: {source_directory}")

    # Check if the source directory is a directory
    if not os.path.isdir(source_directory):
        raise ValueError(f"Source path is not a directory: {source_directory}")

    # Generate the folder tree
    tree = DisplayTree(
        dirPath=source_directory,
        stringRep=True,
        ignoreList=ignore_directories_containing if 'ignore_directories_containing' in locals() else None
    )
    folder_tree_str = f"# Folder Structure:\n\n```\n{tree}\n```\n\n## Dependency Graph\n\nFor detailed component and module dependencies, see [dependency_graph.toon](dependency_graph.toon)"

    # Save the folder tree to a file
    file_path = save_content_to_file(
        content=folder_tree_str,
        source_directory=source_directory,
        file_name="brief.md"
    )

    return file_path