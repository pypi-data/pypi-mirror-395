from typing import Callable, Dict, Any, TypeVar, Protocol, Optional, List, Union
from functools import wraps
import inspect
from smolagents import tool as smolagents_tool
from pydantic import create_model, BaseModel, Field

from logging import get_logger
from exceptions import CodeRefactorError

logger = get_logger(__name__)

T = TypeVar('T')

class Tool(Protocol):
    """Protocol for tool functions."""
    
    @property
    def name(self) -> str:
        """Get the tool name."""
        ...
    
    @property
    def description(self) -> str:
        """Get the tool description."""
        ...
    
    def __call__(self, *args, **kwargs) -> Any:
        """Call the tool."""
        ...

def tool(func: Callable) -> Tool:
    """
    Decorator for tool functions.
    
    This decorator wraps a function to provide standardized error handling and logging.
    It also validates that the function has proper type hints and docstrings.
    
    Args:
        func: The function to wrap
        
    Returns:
        The wrapped function
    """
    # Get function signature
    sig = inspect.signature(func)
    
    # Extract parameter types from type hints
    param_types = {}
    for name, param in sig.parameters.items():
        if param.annotation is inspect.Parameter.empty:
            logger.warning(f"Parameter {name} in {func.__name__} missing type hint")
            continue
        param_types[name] = param.annotation
    
    # Create pydantic model for parameters
    fields = {}
    for name, type_ in param_types.items():
        # Extract description from docstring if available
        param_desc = ""
        if func.__doc__:
            for line in func.__doc__.split('\n'):
                if f"{name}:" in line or f"{name} (" in line:
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        param_desc = parts[1].strip()
                        break
        
        fields[name] = (type_, Field(..., description=param_desc))
    
    # Create model class
    model_name = f"{func.__name__.title()}Model"
    model = create_model(model_name, **fields)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Validate parameters
            params = model(**kwargs)
            
            # Execute function
            logger.debug(f"Executing tool {func.__name__}")
            result = func(*args, **{k: v for k, v in params.dict().items() if k in kwargs})
            
            # Log success
            logger.debug(f"Tool {func.__name__} executed successfully")
            
            return result
        except Exception as e:
            # Log error
            logger.error(f"Error executing tool {func.__name__}: {str(e)}")
            
            # Wrap exception
            if not isinstance(e, CodeRefactorError):
                e = CodeRefactorError(f"Tool {func.__name__} failed: {str(e)}")
            
            raise e
    
    # Add tool name and description
    wrapper.name = func.__name__
    wrapper.description = func.__doc__ or ""
    
    # Decorate with smolagents tool decorator
    decorated_func = smolagents_tool(func)
    
    # Copy attributes from smolagents_tool
    for attr in dir(decorated_func):
        if not attr.startswith('__'):
            setattr(wrapper, attr, getattr(decorated_func, attr))
    
    return wrapper

def create_tool_registry():
    """
    Create a registry for tools.
    
    Returns:
        A dictionary for registering tools
    """
    return {'tools': {}}

def register_tool(registry: Dict[str, Dict[str, Tool]], tool_func: Tool) -> Tool:
    """
    Register a tool function in the registry.
    
    Args:
        registry: The tool registry
        tool_func: The tool function to register
        
    Returns:
        The registered tool function
    """
    registry['tools'][tool_func.name] = tool_func
    return tool_func

def get_tool(registry: Dict[str, Dict[str, Tool]], name: str) -> Optional[Tool]:
    """
    Get a tool from the registry by name.
    
    Args:
        registry: The tool registry
        name: The name of the tool
        
    Returns:
        The tool function or None if not found
    """
    return registry['tools'].get(name)

def get_all_tools(registry: Dict[str, Dict[str, Tool]]) -> List[Tool]:
    """
    Get all tools from the registry.
    
    Args:
        registry: The tool registry
        
    Returns:
        List of all tool functions
    """
    return list(registry['tools'].values())

# Create global tool registry
tool_registry = create_tool_registry()

def register(func: Callable) -> Tool:
    """
    Register a tool function in the global registry.
    
    Args:
        func: The function to register
        
    Returns:
        The registered tool function
    """
    tool_func = tool(func)
    return register_tool(tool_registry, tool_func)

def get(name: str) -> Optional[Tool]:
    """
    Get a tool from the global registry by name.
    
    Args:
        name: The name of the tool
        
    Returns:
        The tool function or None if not found
    """
    return get_tool(tool_registry, name)

def get_all() -> List[Tool]:
    """
    Get all tools from the global registry.
    
    Returns:
        List of all tool functions
    """
    return get_all_tools(tool_registry)