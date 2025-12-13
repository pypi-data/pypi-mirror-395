"""Tests for route matching logic using the shared test suite.

This test file loads the canonical test suite from shared/route-matching-tests.json
to ensure the Python SDK matches routes identically to the backend and Node.js SDK.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import pytest

from orvion.matcher import match_route, normalize_path, normalize_pattern
from orvion.models import RouteConfig


def load_test_suite() -> Dict[str, Any]:
    """Load the shared route matching test suite."""
    # Find the shared test suite relative to this file
    sdk_dir = Path(__file__).parent.parent
    repo_root = sdk_dir.parent.parent
    test_suite_path = repo_root / "shared" / "route-matching-tests.json"

    if not test_suite_path.exists():
        pytest.skip(f"Shared test suite not found at {test_suite_path}")

    with open(test_suite_path, "r") as f:
        return json.load(f)


def routes_from_test(test_routes: List[Dict[str, Any]]) -> List[RouteConfig]:
    """Convert test route definitions to RouteConfig objects."""
    configs = []
    for r in test_routes:
        # Skip paused routes (SDK should filter them)
        if r.get("status") == "paused":
            continue

        configs.append(
            RouteConfig(
                id=r["id"],
                route_pattern=r["pattern"],
                method=r["method"],
                amount="0.10",  # Default for tests
                currency="USD",
                allow_anonymous=True,
            )
        )
    return configs


class TestNormalization:
    """Test path and pattern normalization."""

    def test_normalize_path_basic(self):
        assert normalize_path("/api/data") == "/api/data"

    def test_normalize_path_trailing_slash(self):
        assert normalize_path("/api/data/") == "/api/data"

    def test_normalize_path_multiple_trailing_slashes(self):
        assert normalize_path("/api/data//") == "/api/data"

    def test_normalize_path_root(self):
        assert normalize_path("/") == "/"

    def test_normalize_path_query_params(self):
        assert normalize_path("/api/data?foo=bar") == "/api/data"

    def test_normalize_pattern_basic(self):
        assert normalize_pattern("/api/data") == "/api/data"

    def test_normalize_pattern_trailing_slash(self):
        assert normalize_pattern("/api/data/") == "/api/data"

    def test_normalize_pattern_wildcard_preserved(self):
        # Wildcard patterns should keep their trailing /*
        assert normalize_pattern("/api/premium/*") == "/api/premium/*"


class TestSharedTestSuite:
    """Run all tests from the shared test suite."""

    @pytest.fixture
    def test_suite(self) -> Dict[str, Any]:
        return load_test_suite()

    def test_all_cases(self, test_suite):
        """Run all test cases from the shared suite."""
        tests = test_suite.get("tests", [])
        assert len(tests) > 0, "No tests found in test suite"

        for test in tests:
            test_name = test["name"]
            routes = routes_from_test(test.get("routes", []))
            requests = test.get("requests", [])

            for req in requests:
                path = req["path"]
                method = req["method"]
                expected_id = req["expected_route_id"]

                result = match_route(path, method, routes)
                actual_id = result.id if result else None

                assert actual_id == expected_id, (
                    f"Test '{test_name}' failed for {method} {path}: "
                    f"expected route_id={expected_id}, got {actual_id}"
                )


class TestEdgeCases:
    """Additional edge case tests."""

    def test_empty_routes_returns_none(self):
        result = match_route("/api/data", "GET", [])
        assert result is None

    def test_method_case_insensitive(self):
        routes = [
            RouteConfig(
                id="route-1",
                route_pattern="/api/data",
                method="GET",
                amount="0.10",
                currency="USD",
                allow_anonymous=True,
            )
        ]

        # All these should match
        assert match_route("/api/data", "GET", routes) is not None
        assert match_route("/api/data", "get", routes) is not None
        assert match_route("/api/data", "Get", routes) is not None

    def test_priority_exact_over_wildcard(self):
        routes = [
            RouteConfig(
                id="wildcard",
                route_pattern="/api/*",
                method="GET",
                amount="0.10",
                currency="USD",
                allow_anonymous=True,
            ),
            RouteConfig(
                id="exact",
                route_pattern="/api/data",
                method="GET",
                amount="0.20",
                currency="USD",
                allow_anonymous=True,
            ),
        ]

        result = match_route("/api/data", "GET", routes)
        assert result is not None
        assert result.id == "exact"

    def test_longer_wildcard_prefix_wins(self):
        routes = [
            RouteConfig(
                id="short",
                route_pattern="/api/*",
                method="GET",
                amount="0.10",
                currency="USD",
                allow_anonymous=True,
            ),
            RouteConfig(
                id="long",
                route_pattern="/api/premium/*",
                method="GET",
                amount="0.20",
                currency="USD",
                allow_anonymous=True,
            ),
        ]

        result = match_route("/api/premium/data", "GET", routes)
        assert result is not None
        assert result.id == "long"

        result = match_route("/api/other/data", "GET", routes)
        assert result is not None
        assert result.id == "short"

