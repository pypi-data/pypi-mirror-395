from smolagents.tools import tool
import os
from pathlib import Path
import shutil

@tool
def delete_folder_or_file(absolute_path: str) -> bool:
    """
    Deletes a folder or file.
    
    Args:
        absolute_path (str): The path to the folder or file to delete.
    Returns:
       bool: True if the deletion was successful, False otherwise.
    """
    path = Path(absolute_path).resolve()

    if path.is_dir():
        shutil.rmtree(path)
    elif path.is_file():
        os.remove(path)
    else:
        return False

    return  True

@tool
def save_content_to_file(content: str, source_directory: str, file_name: str) -> str:
    """
    Saves the given content to a file.
    
    Args:
        content (str): The content to be saved.
        source_directory (str): The directory where the file will be saved.
        file_name (str): The name of the file where the content will be saved.
    Returns:
        str: The full path of the saved file.
    """
    knolwledge_base_dir = f"{source_directory}/knowledge_base/{file_name}"
    file_path_obj = Path(knolwledge_base_dir).resolve()
    file_path_obj.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path_obj, "w") as file:
        file.write(content)

    return str(file_path_obj)

@tool
def read_file_content(absolute_file_path: str) -> str:
    """
    Reads the content of a dependency.
    
    Args:
        absolute_file_path (str): The path to the file to read.
    Returns:
        str: The content of the file.
    """
    file_path = Path(absolute_file_path).resolve()

    return file_path.read_text(encoding="utf-8")