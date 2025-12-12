"""Input validation utilities."""

from typing import Any, Dict, List, Optional


class Validator:
    """Validation utilities for FlowMind tasks."""
    
    @staticmethod
    def require_fields(config: Dict[str, Any], *fields: str) -> bool:
        """Check if required fields are present.
        
        Args:
            config: Configuration dictionary
            *fields: Required field names
            
        Returns:
            True if all fields present
            
        Raises:
            ValueError: If any field is missing
        """
        missing = [f for f in fields if f not in config]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
        return True
    
    @staticmethod
    def validate_type(value: Any, expected_type: type, name: str = "value") -> bool:
        """Validate value type.
        
        Args:
            value: Value to check
            expected_type: Expected type
            name: Value name for error messages
            
        Returns:
            True if type matches
            
        Raises:
            TypeError: If type doesn't match
        """
        if not isinstance(value, expected_type):
            raise TypeError(
                f"{name} must be {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        return True
    
    @staticmethod
    def validate_choice(value: Any, choices: List[Any], name: str = "value") -> bool:
        """Validate value is in allowed choices.
        
        Args:
            value: Value to check
            choices: List of allowed values
            name: Value name for error messages
            
        Returns:
            True if value in choices
            
        Raises:
            ValueError: If value not in choices
        """
        if value not in choices:
            raise ValueError(
                f"{name} must be one of {choices}, got {value}"
            )
        return True
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is valid
            
        Raises:
            ValueError: If URL is invalid
        """
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL: {url}")
        return True
    
    @staticmethod
    def validate_file_path(path: str) -> bool:
        """Validate file path format.
        
        Args:
            path: Path to validate
            
        Returns:
            True if path is valid
            
        Raises:
            ValueError: If path is invalid
        """
        if not path or not isinstance(path, str):
            raise ValueError(f"Invalid file path: {path}")
        return True
