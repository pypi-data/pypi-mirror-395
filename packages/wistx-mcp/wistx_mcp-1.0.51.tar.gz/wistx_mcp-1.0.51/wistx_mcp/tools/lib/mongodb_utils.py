"""MongoDB utility functions for safe query construction."""

import re
from typing import Any


def escape_regex_for_mongodb(text: str) -> str:
    """Escape special regex characters for MongoDB queries.
    
    Args:
        text: User-provided search text
    
    Returns:
        Escaped text safe for MongoDB $regex queries
    
    Raises:
        TypeError: If text is not a string
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string")
    
    return re.escape(text)


def build_safe_mongodb_regex_query(
    query: str,
    fields: list[str],
    case_insensitive: bool = True,
) -> dict[str, Any]:
    """Build safe MongoDB regex query with escaped user input.
    
    Args:
        query: User-provided search query
        fields: List of fields to search
        case_insensitive: Whether to use case-insensitive matching
    
    Returns:
        MongoDB query dictionary
    
    Raises:
        TypeError: If query is not a string or fields is not a list
        ValueError: If fields list is empty
    """
    if not isinstance(query, str):
        raise TypeError("Query must be a string")
    
    if not isinstance(fields, list) or len(fields) == 0:
        raise ValueError("Fields must be a non-empty list")
    
    escaped_query = escape_regex_for_mongodb(query)
    
    options = "i" if case_insensitive else ""
    
    if len(fields) == 1:
        return {fields[0]: {"$regex": escaped_query, "$options": options}}
    else:
        return {
            "$or": [
                {field: {"$regex": escaped_query, "$options": options}}
                for field in fields
            ]
        }

