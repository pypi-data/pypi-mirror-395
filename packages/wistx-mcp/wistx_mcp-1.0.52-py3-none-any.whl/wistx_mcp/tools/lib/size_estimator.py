"""JSON size estimation utility to prevent memory exhaustion."""

from typing import Any


def estimate_json_size(obj: Any, max_depth: int = 10, current_depth: int = 0) -> int:
    """Estimate JSON size without full serialization.
    
    Args:
        obj: Object to estimate size for
        max_depth: Maximum recursion depth
        current_depth: Current recursion depth
    
    Returns:
        Estimated size in bytes
    """
    if current_depth > max_depth:
        return 1000
    
    if isinstance(obj, str):
        return len(obj.encode('utf-8')) + 2
    elif isinstance(obj, (int, float)):
        return 20
    elif isinstance(obj, bool):
        return 5
    elif obj is None:
        return 4
    elif isinstance(obj, dict):
        size = 2
        for k, v in obj.items():
            size += estimate_json_size(k, max_depth, current_depth + 1)
            size += estimate_json_size(v, max_depth, current_depth + 1)
            size += 3
        return size
    elif isinstance(obj, (list, tuple)):
        size = 2
        for item in obj:
            size += estimate_json_size(item, max_depth, current_depth + 1)
            size += 1
        return size
    
    return 100

