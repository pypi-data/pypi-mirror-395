# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught

import json
import datetime
from enum import Enum
from typing import Any, Dict, List, Union, Optional

def datetime_to_str(obj: Any) -> str:
    """Convert datetime to ISO format string."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, datetime.time):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not serializable")

def make_json_serializable(data: Any) -> Any:
    """
    Recursively convert a Python object to a JSON-serializable form.
    
    Args:
        data: Any Python object to make JSON-serializable
        
    Returns:
        A JSON-serializable version of the input data
    """
    if data is None:
        return None
    elif isinstance(data, (str, int, float, bool)):
        return data
    elif isinstance(data, (datetime.datetime, datetime.date, datetime.time)):
        return datetime_to_str(data)
    elif isinstance(data, dict):
        return {k: make_json_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [make_json_serializable(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(make_json_serializable(item) for item in data)
    elif isinstance(data, set):
        return list(make_json_serializable(item) for item in data)
    elif hasattr(data, "__dict__"):
        # Handle custom objects by converting to dict
        return make_json_serializable(data.__dict__)
    else:
        # For any other types, convert to string
        return str(data)

def process_data_for_bigquery(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Process data to ensure it's in the format expected by BigQuery's load_table_from_json.
    
    Args:
        data: A dict or list of dicts with data to load
        
    Returns:
        A list of dicts with all values JSON-serializable
    """
    # Ensure data is a list
    if isinstance(data, dict):
        data = [data]
    
    # Make each item in the list JSON-serializable
    return [make_json_serializable(item) for item in data]

def to_json_string(data: Any) -> str:
    """
    Convert any Python object to a JSON string with proper handling of datetimes.
    
    Args:
        data: Any Python object
        
    Returns:
        JSON string representation
    """
    serializable_data = make_json_serializable(data)
    return json.dumps(serializable_data)

def pydantic_to_bigquery_dict(
    model_instance,
    fields_to_keep_as_dict: Optional[List[str]] = None,
    fields_to_keep_as_list: Optional[List[str]] = None,
    keep_datetime_as_datetime: bool = True,
    list_to_comma_separated_string: bool = False,
) -> Dict[str, Any]:
    """
    Convert a Pydantic model instance to a BigQuery-compatible dictionary.
    
    This function is specifically designed for BigQuery Python client's requirements
    when using insert_rows_json() or load_table_from_json().
    
    BigQuery Python client native type mappings:
    - datetime → TIMESTAMP (keep as datetime object - client handles conversion)
    - Enum → STRING (convert to str() - Pydantic keeps as enum object)
    - Pydantic models → STRING (JSON serialize for nested objects)
    - list → STRING (JSON serialize - typically used for array fields stored as STRING)
    - dict → STRING (JSON serialize - typically used for JSON fields stored as STRING)
    
    Why not use make_json_serializable()?
    - It converts datetime to ISO string, but BigQuery Python client needs native datetime objects
    - BigQuery Python client's insert_rows_json() expects datetime objects for TIMESTAMP columns
    - The client then converts them to BigQuery's native TIMESTAMP type
    
    Why not just use model_dump()?
    - Pydantic keeps enums as enum objects, BigQuery needs strings for STRING columns
    - Nested Pydantic models need JSON serialization for STRING columns (per DDL schema)
    - Lists and dicts need JSON serialization when DDL defines them as STRING fields
    
    Args:
        model_instance: A Pydantic model instance to convert
        fields_to_keep_as_dict: Fields that should remain as dict (not JSON-stringified)
        fields_to_keep_as_list: Fields that should remain as list (not JSON-stringified)
        keep_datetime_as_datetime: If True, keep datetimes as datetime objects (for TIMESTAMP columns). 
                                    If False, convert to ISO strings (for NDJSON files)
        list_to_comma_separated_string: If True, convert lists to comma-separated strings instead of JSON arrays
        
    Returns:
        Dictionary with BigQuery-compatible types
        
    Example:
        >>> from pydantic import BaseModel
        >>> from datetime import datetime, timezone
        >>> from enum import Enum
        >>> 
        >>> class Status(str, Enum):
        ...     ACTIVE = "active"
        >>> 
        >>> class MyModel(BaseModel):
        ...     name: str
        ...     status: Status
        ...     created_at: datetime
        ...     tags: List[str]
        >>> 
        >>> model = MyModel(
        ...     name="Test",
        ...     status=Status.ACTIVE,
        ...     created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
        ...     tags=["tag1", "tag2"]
        ... )
        >>> result = pydantic_to_bigquery_dict(model)
        >>> # result['created_at'] is datetime object (not string)
        >>> # result['status'] is "active" (not enum object)
        >>> # result['tags'] is '["tag1", "tag2"]' (JSON string)
    """
    fields_to_keep_as_dict = fields_to_keep_as_dict or []
    fields_to_keep_as_list = fields_to_keep_as_list or []

    # Use Pydantic's serialization (mode='python' keeps datetime as datetime objects and enums as enum objects)
    data = model_instance.model_dump(mode='python')

    for key, value in list(data.items()):
        if value is None:
            continue

        # Handle datetime objects
        if isinstance(value, datetime.datetime):
            if keep_datetime_as_datetime:
                # Keep as datetime object (for BigQuery Python client)
                continue
            else:
                # Convert to ISO string (for NDJSON files)
                data[key] = value.isoformat()
                continue

        # Enums -> string
        if isinstance(value, Enum):
            data[key] = str(value)
            continue

        # Lists handling
        if isinstance(value, list):
            # If user requested this field to remain a list, keep as list (but convert enums inside)
            if key in fields_to_keep_as_list:
                data[key] = [str(item) if isinstance(item, Enum) else item for item in value]
                continue

            # Optionally convert to comma-separated string
            if list_to_comma_separated_string and all(isinstance(item, (str, int, float)) for item in value):
                data[key] = ','.join([str(item) for item in value])
                continue

            # Default: JSON-stringify the list (convert enums inside first)
            serialized_list = [str(item) if isinstance(item, Enum) else item for item in value]
            data[key] = json.dumps(make_json_serializable(serialized_list))
            continue

        # Dicts and custom objects
        if isinstance(value, dict) or hasattr(value, '__dict__'):
            # If user wants to keep as dict (for JSON columns), leave as dict but make it JSON-serializable
            if key in fields_to_keep_as_dict:
                data[key] = make_json_serializable(value)
                continue

            # Otherwise, JSON-stringify the dict
            data[key] = json.dumps(make_json_serializable(value))
            continue

        # Fallback: ensure JSON-serializable primitive types
        if isinstance(value, (str, int, float, bool)):
            continue

        # Any other types -> convert to string
        data[key] = str(value)

    return data
