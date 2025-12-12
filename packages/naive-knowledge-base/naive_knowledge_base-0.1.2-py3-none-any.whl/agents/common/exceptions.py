from typing import Dict, Any, Optional

class CodeRefactorError(Exception):
    """Base exception for all code refactor errors."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class ConfigurationError(CodeRefactorError):
    """Raised when there's an issue with configuration."""
    pass

class DependencyGraphError(CodeRefactorError):
    """Raised when there's an issue with dependency graph generation or processing."""
    pass

class SonarQubeError(CodeRefactorError):
    """Raised when there's an issue with SonarQube integration."""
    pass

class RefactoringError(CodeRefactorError):
    """Raised when there's an issue with the refactoring process."""
    pass

class FileOperationError(CodeRefactorError):
    """Raised when there's an issue with file operations."""
    pass

class MissingDependencyError(CodeRefactorError):
    """Raised when a required dependency is missing."""
    pass

class TestingError(CodeRefactorError):
    """Raised when there's an issue with the testing process."""
    pass

def wrap_exceptions(func):
    """
    Decorator to wrap exceptions with our custom exception types.
    Example usage:
    
    @wrap_exceptions
    def function_that_might_fail():
        # function body
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise FileOperationError(f"File not found: {str(e)}", {"path": str(e)})
        except PermissionError as e:
            raise FileOperationError(f"Permission denied: {str(e)}", {"path": str(e)})
        except ImportError as e:
            raise MissingDependencyError(f"Missing dependency: {str(e)}")
        except Exception as e:
            # If it's already one of our exceptions, re-raise it
            if isinstance(e, CodeRefactorError):
                raise
            # Otherwise wrap it
            raise CodeRefactorError(f"Unexpected error: {str(e)}", {"original_error": str(e)})
    return wrapper