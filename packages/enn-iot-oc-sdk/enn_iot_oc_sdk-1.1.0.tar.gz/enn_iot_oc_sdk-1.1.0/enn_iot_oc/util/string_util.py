"""
Mock string utility functions for IoC Data SDK
"""

from typing import Any, List, Optional, Type, TypeVar
import json

T = TypeVar('T')

def parse_object(value: Any, target_type: Type[T]) -> T:
    """
    Mock function to parse object values
    In real implementation, this would handle complex type conversion
    """
    if value is None:
        # Return default value based on type
        if target_type == str:
            return ""  # type: ignore
        elif target_type == int:
            return 0  # type: ignore
        elif target_type == float:
            return 0.0  # type: ignore
        elif target_type == bool:
            return False  # type: ignore
        elif hasattr(target_type, '__origin__') and target_type.__origin__ is list:
            return []  # type: ignore
        else:
            return None  # type: ignore

    try:
        # Direct conversion if types match
        if isinstance(value, target_type):
            return value  # type: ignore

        # Handle common conversions
        if target_type == str:
            return str(value)  # type: ignore
        elif target_type == int:
            return int(value)  # type: ignore
        elif target_type == float:
            return float(value)  # type: ignore
        elif target_type == bool:
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')  # type: ignore
            return bool(value)  # type: ignore
        else:
            # For complex types, try JSON parsing or return as is
            if isinstance(value, str):
                try:
                    return json.loads(value)  # type: ignore
                except:
                    pass
            return value  # type: ignore

    except (ValueError, TypeError) as e:
        print(f"[MOCK] parse_object warning: Cannot convert {value} to {target_type}, using default: {e}")
        # Return default value on conversion error
        if target_type == str:
            return ""  # type: ignore
        elif target_type == int:
            return 0  # type: ignore
        elif target_type == float:
            return 0.0  # type: ignore
        elif target_type == bool:
            return False  # type: ignore
        else:
            return None  # type: ignore

def parse_array(value: Any, target_type: Type[T]) -> List[T]:
    """
    Mock function to parse array values
    In real implementation, this would handle list conversion with type checking
    """
    if value is None:
        return []

    if isinstance(value, list):
        # Parse each item in the list
        return [parse_object(item, target_type) for item in value]
    elif isinstance(value, str):
        try:
            # Try to parse as JSON array
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [parse_object(item, target_type) for item in parsed]
        except:
            pass

        # If single string, treat as single item array
        return [parse_object(value, target_type)]
    else:
        # Wrap single item in array
        return [parse_object(value, target_type)]