import os
from pathlib import Path
from typing import List, Optional, Any, Dict
import json
import re

from smolagents import tool

from .exceptions import FileOperationError, wrap_exceptions
from .logging import get_logger

logger = get_logger(__name__)

@wrap_exceptions
def save_content_to_file(content: str, source_directory: str, file_name: str) -> str:
    """
    Saves content to a file, creating parent directories if needed.
    
    Args:
        content: The content to save
        source_directory: The directory where the file will be saved
        file_name: The name of the file
        
    Returns:
        The absolute path to the saved file
        
    Raises:
        FileOperationError: If there's an issue with the file operation
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        logger.debug(f"Content saved to {file_path}")
        return str(path.absolute())
    except Exception as e:
        raise FileOperationError(f"Failed to save content to {file_path}: {str(e)}")

@wrap_exceptions
def read_file_content(file_path: str) -> str:
    """
    Reads content from a file.
    
    Args:
        file_path: The path to the file
        
    Returns:
        The file content as a string
        
    Raises:
        FileOperationError: If there's an issue with the file operation
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise FileOperationError(f"Failed to read content from {file_path}: {str(e)}")

@wrap_exceptions
def delete_folder_or_file(path: str) -> bool:
    """
    Deletes a folder or file.
    
    Args:
        path: The path to the folder or file
        
    Returns:
        True if the deletion was successful, False otherwise
        
    Raises:
        FileOperationError: If there's an issue with the file operation
    """
    try:
        path_obj = Path(path)
        
        if path_obj.is_file():
            path_obj.unlink()
        elif path_obj.is_dir():
            # Import here to avoid circular imports
            import shutil
            shutil.rmtree(path)
        else:
            logger.warning(f"Path {path} does not exist")
            return False
            
        logger.debug(f"Deleted {path}")
        return True
    except Exception as e:
        raise FileOperationError(f"Failed to delete {path}: {str(e)}")

@wrap_exceptions
def extract_code_blocks(markdown_content: str, language: Optional[str] = None) -> List[str]:
    """
    Extracts code blocks from markdown content.
    
    Args:
        markdown_content: The markdown content
        language: Optional language filter
        
    Returns:
        List of extracted code blocks
    """
    if language:
        pattern = r'```(?:' + language + r')?\s*([\s\S]*?)\s*```(?:\n|$)'
    else:
        pattern = r'```(?:\w*)?\s*([\s\S]*?)\s*```(?:\n|$)'
        
    return re.findall(pattern, markdown_content)

@wrap_exceptions
def load_json_file(file_path: str) -> Any:
    """
    Loads a JSON file.
    
    Args:
        file_path: The path to the JSON file
        
    Returns:
        The parsed JSON content
        
    Raises:
        FileOperationError: If there's an issue with the file operation
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise FileOperationError(f"Invalid JSON in {file_path}: {str(e)}")
    except Exception as e:
        raise FileOperationError(f"Failed to read JSON from {file_path}: {str(e)}")

@wrap_exceptions
def save_json_file(content: Dict[str, Any], file_path: str, indent: int = 2) -> str:
    """
    Saves content as a JSON file.
    
    Args:
        content: The content to save
        file_path: The path to the file
        indent: JSON indentation level
        
    Returns:
        The absolute path to the saved file
        
    Raises:
        FileOperationError: If there's an issue with the file operation
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=indent)
            
        logger.debug(f"JSON content saved to {file_path}")
        return str(path.absolute())
    except Exception as e:
        raise FileOperationError(f"Failed to save JSON content to {file_path}: {str(e)}")