"""Filter parsing utilities for VirtualDojo CLI."""

import json
import re
from typing import Any


def parse_filters(filter_string: str) -> str:
    """Parse a filter string into JSON format for the API.

    Supports multiple formats:
    - JSON: '{"field_contains": "value"}'
    - Key-value pairs: 'field_contains=value,status_ne=inactive'
    - Simple equality: 'status=active,tier=enterprise'

    Args:
        filter_string: The filter string to parse

    Returns:
        JSON string for the filters parameter

    Examples:
        >>> parse_filters('name_contains=Acme')
        '{"name_contains": "Acme"}'

        >>> parse_filters('status=active,amount_gte=10000')
        '{"status": "active", "amount_gte": 10000}'

        >>> parse_filters('{"field": "value"}')
        '{"field": "value"}'
    """
    filter_string = filter_string.strip()

    # If it's already JSON, validate and return
    if filter_string.startswith("{"):
        try:
            # Validate JSON
            json.loads(filter_string)
            return filter_string
        except json.JSONDecodeError:
            pass

    # Parse key-value pairs
    filters: dict[str, Any] = {}

    # Split by comma, but respect quoted values
    pairs = _split_filter_pairs(filter_string)

    for pair in pairs:
        if "=" not in pair:
            continue

        key, value = pair.split("=", 1)
        key = key.strip()
        value = value.strip()

        # Remove quotes if present
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]

        # Try to parse value as appropriate type
        parsed_value = _parse_value(value)

        # Handle _in and _not_in operators - convert to list
        if key.endswith('_in') or key.endswith('_not_in'):
            if isinstance(parsed_value, str):
                # Split by comma or pipe and parse each value
                delimiter = '|' if '|' in parsed_value else ','
                values = [_parse_value(v.strip()) for v in parsed_value.split(delimiter)]
                filters[key] = values
            else:
                # Single value - wrap in list
                filters[key] = [parsed_value]
        else:
            filters[key] = parsed_value

    return json.dumps(filters)


def _split_filter_pairs(filter_string: str) -> list[str]:
    """Split filter string by comma, respecting quoted values."""
    pairs = []
    current = ""
    in_quotes = False
    quote_char = None

    for char in filter_string:
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
            current += char
        elif char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
            current += char
        elif char == "," and not in_quotes:
            if current.strip():
                pairs.append(current.strip())
            current = ""
        else:
            current += char

    if current.strip():
        pairs.append(current.strip())

    return pairs


def _parse_value(value: str) -> Any:
    """Parse a string value into the appropriate Python type."""
    # Boolean
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False

    # Null
    if value.lower() in ("null", "none"):
        return None

    # Number
    if re.match(r"^-?\d+$", value):
        return int(value)
    if re.match(r"^-?\d+\.\d+$", value):
        return float(value)

    # String (default)
    return value


def build_filter_help() -> str:
    """Build help text for filter syntax."""
    return """
Filter Syntax:
  Simple: field=value
  Multiple: field1=value1,field2=value2
  Operators:
    field_ne=value       Not equals
    field_gt=100         Greater than
    field_gte=100        Greater than or equal
    field_lt=100         Less than
    field_lte=100        Less than or equal
    field_contains=text  Contains (case-insensitive)
    field_startswith=x   Starts with
    field_endswith=x     Ends with
    field_in=a|b|c       In list (use | delimiter)
    field_in="a,b,c"     In list (use quotes with commas)
    field_isnull=true    Is null

Examples:
  --filter "status=active"
  --filter "amount_gte=10000,stage_ne=closed"
  --filter "name_contains=Acme,tier=enterprise"
  --filter 'name_in=VENDORS|DISTRIBUTORS|RESELLERS'
  --filter 'name_in="VENDORS,DISTRIBUTORS,RESELLERS"'
"""


# Operator definitions for reference
FILTER_OPERATORS = {
    "": "equals",
    "_ne": "not equals",
    "_gt": "greater than",
    "_gte": "greater than or equal",
    "_lt": "less than",
    "_lte": "less than or equal",
    "_contains": "contains",
    "_not_contains": "does not contain",
    "_startswith": "starts with",
    "_endswith": "ends with",
    "_in": "in list",
    "_not_in": "not in list",
    "_isnull": "is null / is not null",
}
