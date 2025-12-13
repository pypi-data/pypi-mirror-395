import json
from typing import Any, List, Union

def to_bool(value: str) -> bool:
    """Convert a string to a boolean."""
    if str(value).lower() in ("true", "1", "t", "yes", "y", "on"):
        return True
    if str(value).lower() in ("false", "0", "f", "no", "n", "off"):
        return False
    raise ValueError(f"Invalid boolean value: {value}")

def to_list(value: str, delimiter: str = ",") -> List[str]:
    """Convert a comma-separated string to a list."""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter)]

def to_json(value: str) -> Any:
    """Parse a JSON string."""
    try:
        return json.loads(value)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON value: {value}") from e
