from typing import Dict, Any, List, Optional, Union, Callable
import json
from pydantic import BaseModel

class SchemaConverter:
    """
    Converts between different schema formats for tool functions.
    
    This class handles conversion of parameters and return types between
    different schema formats used by different libraries.
    """
    
    @staticmethod
    def convert_pydantic_to_dict(model_instance: BaseModel) -> Dict[str, Any]:
        """
        Convert a Pydantic model instance to a dictionary.
        
        Args:
            model_instance: The Pydantic model instance to convert
            
        Returns:
            The model as a dictionary
        """
        return model_instance.dict()
    
    @staticmethod
    def convert_dict_to_pydantic(data: Dict[str, Any], model_class: type) -> BaseModel:
        """
        Convert a dictionary to a Pydantic model instance.
        
        Args:
            data: The dictionary data to convert
            model_class: The Pydantic model class to convert to
            
        Returns:
            An instance of the specified Pydantic model
        """
        return model_class(**data)
    
    @staticmethod
    def convert_json_to_pydantic(json_str: str, model_class: type) -> BaseModel:
        """
        Convert a JSON string to a Pydantic model instance.
        
        Args:
            json_str: The JSON string to convert
            model_class: The Pydantic model class to convert to
            
        Returns:
            An instance of the specified Pydantic model
        """
        data = json.loads(json_str)
        return SchemaConverter.convert_dict_to_pydantic(data, model_class)
    
    @staticmethod
    def wrap_function_for_schema_conversion(
        func: Callable,
        input_conversions: Dict[str, type] = None,
        output_conversion: Optional[type] = None
    ) -> Callable:
        """
        Wraps a function to handle schema conversions automatically.
        
        Args:
            func: The function to wrap
            input_conversions: Mapping of parameter names to Pydantic model classes for conversion
            output_conversion: Pydantic model class for converting the function output
            
        Returns:
            A wrapped function that handles schema conversions
        """
        input_conversions = input_conversions or {}
        
        def wrapper(*args, **kwargs):
            # Convert input parameters based on specified conversions
            converted_kwargs = kwargs.copy()
            
            for param_name, model_class in input_conversions.items():
                if param_name in kwargs:
                    # Special case for JSON strings
                    if isinstance(kwargs[param_name], str) and kwargs[param_name].startswith('{'):
                        try:
                            converted_kwargs[param_name] = SchemaConverter.convert_json_to_pydantic(
                                kwargs[param_name], model_class
                            )
                        except (json.JSONDecodeError, ValueError):
                            # Not a valid JSON string, keep original
                            pass
                    # Dict to model conversion
                    elif isinstance(kwargs[param_name], dict):
                        converted_kwargs[param_name] = SchemaConverter.convert_dict_to_pydantic(
                            kwargs[param_name], model_class
                        )
            
            # Call the original function with converted parameters
            result = func(*args, **converted_kwargs)
            
            # Convert output if needed
            if output_conversion and isinstance(result, BaseModel):
                return SchemaConverter.convert_pydantic_to_dict(result)
            elif output_conversion and isinstance(result, dict):
                # Create a model instance and then convert back to dict to ensure schema compliance
                model_instance = SchemaConverter.convert_dict_to_pydantic(result, output_conversion)
                return SchemaConverter.convert_pydantic_to_dict(model_instance)
            
            return result
        
        # Preserve the original function's metadata
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        
        return wrapper