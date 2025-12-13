"""Route matching logic for the SDK.

This module implements the same route matching algorithm as the backend.
See shared/route-matching-tests.json for the canonical test suite.
"""

from typing import List, Optional, Tuple

from orvion.models import RouteConfig


def normalize_path(path: str) -> str:
    """
    Normalize a request path.

    - Strip query parameters
    - Strip trailing slashes (except for root /)
    """
    # Strip query parameters
    if "?" in path:
        path = path.split("?")[0]

    # Strip trailing slashes, but keep root /
    return path.rstrip("/") or "/"


def normalize_pattern(pattern: str) -> str:
    """
    Normalize a route pattern.

    - Strip trailing slashes (except for root / and wildcard patterns)
    """
    # Don't strip trailing slash if pattern ends with /*
    if pattern.endswith("/*"):
        return pattern

    # Strip trailing slashes, but keep root /
    return pattern.rstrip("/") or "/"


def is_wildcard_pattern(pattern: str) -> bool:
    """Check if pattern is a wildcard pattern (ends with /*)"""
    return pattern.endswith("/*")


def get_wildcard_prefix(pattern: str) -> str:
    """Get the prefix of a wildcard pattern."""
    if not is_wildcard_pattern(pattern):
        return pattern
    return pattern[:-1]  # '/api/premium/*' -> '/api/premium/'


def matches_pattern(path: str, pattern: str, original_had_trailing_slash: bool = False) -> bool:
    """
    Check if a path matches a route pattern.
    
    Args:
        path: Normalized path (trailing slashes stripped)
        pattern: Normalized pattern
        original_had_trailing_slash: Whether the original path had a trailing slash
    """
    if is_wildcard_pattern(pattern):
        prefix = get_wildcard_prefix(pattern)  # '/api/premium/*' -> '/api/premium/'
        # Check if path starts with prefix (has content after prefix)
        if path.startswith(prefix):
            return True
        # For wildcard patterns, path must have trailing slash or additional segments
        # Check if normalized path + '/' equals prefix AND original had trailing slash
        if path + "/" == prefix and original_had_trailing_slash:
            return True
        # Path doesn't match - no trailing slash and no additional segments
        return False
    else:
        return path == pattern


def matches_method(request_method: str, route_method: str) -> bool:
    """Check if a request method matches a route method."""
    request_method = request_method.upper()
    route_method = route_method.upper()

    if route_method == "*":
        return True

    return request_method == route_method


def calculate_priority(pattern: str, method: str) -> Tuple[int, int]:
    """
    Calculate the priority of a route for matching.

    Priority order (lower = higher priority):
    1. Exact path + exact method (0, 0)
    2. Exact path + wildcard method (1, 0)
    3. Wildcard path + exact method (2, -prefix_length)
    4. Wildcard path + wildcard method (3, -prefix_length)
    """
    is_wildcard = is_wildcard_pattern(pattern)
    is_method_wildcard = method.upper() == "*"

    if not is_wildcard and not is_method_wildcard:
        return (0, 0)
    elif not is_wildcard and is_method_wildcard:
        return (1, 0)
    elif is_wildcard and not is_method_wildcard:
        prefix_len = len(get_wildcard_prefix(pattern))
        return (2, -prefix_len)
    else:
        prefix_len = len(get_wildcard_prefix(pattern))
        return (3, -prefix_len)


def match_route(path: str, method: str, routes: List[RouteConfig]) -> Optional[RouteConfig]:
    """
    Match a request path and method to the best matching route.

    Args:
        path: The request path (will be normalized)
        method: The HTTP method (will be normalized)
        routes: List of route configurations

    Returns:
        The best matching route, or None if no match
    """
    normalized_path = normalize_path(path)
    normalized_method = method.upper()
    # Track if original path had trailing slash (before normalization)
    original_had_trailing_slash = path != normalized_path and path.endswith("/")

    matches: List[Tuple[Tuple[int, int], RouteConfig]] = []

    for route in routes:
        pattern = normalize_pattern(route.route_pattern)

        if matches_pattern(normalized_path, pattern, original_had_trailing_slash) and matches_method(normalized_method, route.method):
            priority = calculate_priority(pattern, route.method)
            matches.append((priority, route))

    if not matches:
        return None

    matches.sort(key=lambda x: x[0])
    return matches[0][1]

