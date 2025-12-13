"""Helper functions for common API operations."""

from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse


def format_response(
    data: dict[str, Any], *, pretty: bool = False, indent: int = 2
) -> str:
    """Format API response data as a string.

    Args:
        data: The response data dictionary
        pretty: Whether to format with indentation (default: False)
        indent: Number of spaces for indentation if pretty=True (default: 2)

    Returns:
        Formatted string representation of the response

    Example:
        >>> data = {"user": "john", "status": "active"}
        >>> print(format_response(data, pretty=True))
        {
          "user": "john",
          "status": "active"
        }
    """
    import json

    if pretty:
        return json.dumps(data, indent=indent, sort_keys=True)
    return json.dumps(data)


def parse_query_params(url: str) -> dict[str, Any]:
    """Parse query parameters from a URL.

    Args:
        url: The URL string to parse

    Returns:
        Dictionary of query parameters

    Example:
        >>> url = "https://api.example.com/users?page=1&limit=10"
        >>> params = parse_query_params(url)
        >>> print(params)
        {'page': ['1'], 'limit': ['10']}
    """
    parsed = urlparse(url)
    return dict(parse_qs(parsed.query))


def build_query_string(params: dict[str, Any]) -> str:
    """Build a query string from a dictionary of parameters.

    Args:
        params: Dictionary of query parameters

    Returns:
        URL-encoded query string

    Example:
        >>> params = {"page": 1, "limit": 10, "sort": "name"}
        >>> query = build_query_string(params)
        >>> print(query)
        page=1&limit=10&sort=name
    """
    return urlencode(params)


def merge_headers(
    default_headers: dict[str, str] | None = None,
    custom_headers: dict[str, str] | None = None,
) -> dict[str, str]:
    """Merge default and custom headers.

    Custom headers take precedence over default headers.

    Args:
        default_headers: Default headers dictionary
        custom_headers: Custom headers to merge

    Returns:
        Merged headers dictionary

    Example:
        >>> defaults = {"Content-Type": "application/json"}
        >>> custom = {"Authorization": "Bearer token"}
        >>> headers = merge_headers(defaults, custom)
        >>> print(headers)
        {'Content-Type': 'application/json', 'Authorization': 'Bearer token'}
    """
    result = {}
    if default_headers:
        result.update(default_headers)
    if custom_headers:
        result.update(custom_headers)
    return result
