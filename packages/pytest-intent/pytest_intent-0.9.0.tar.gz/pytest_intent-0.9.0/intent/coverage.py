"""Module for tracking requirement coverage and test results."""

from __future__ import annotations

import logging
import re
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest

logger = logging.getLogger("pytest_intent")

# Pattern to match pytest-repeat suffix: [digits] or [digits-digits] at the end
# Used as fallback when originalname is not available
_REPEAT_PATTERN = re.compile(r"\[\d+(-\d+)?\]$")

# Constants for nodeid part counts
_NODEID_PARTS_SIMPLE = 2  # path::function
_NODEID_PARTS_WITH_CLASS = 3  # path::class::function


def _get_base_nodeid(item: pytest.Item) -> str:  # type: ignore[name-defined]
    """Get the base nodeid without pytest-repeat suffix.

    Uses the item's originalname property to construct the base nodeid,
    which is more reliable than parsing the nodeid string. Falls back to
    regex parsing if originalname is not available (e.g., in test mocks).

    Args:
        item: The pytest.Item to get the base nodeid for.

    Returns:
        The base nodeid without repeat suffix (e.g., "tests/test.py::test_function").
    """
    # Try to use originalname if available (preferred method)
    if hasattr(item, "originalname"):
        nodeid_parts = item.nodeid.split("::")
        if len(nodeid_parts) == _NODEID_PARTS_SIMPLE:
            # Simple case: path::function
            return f"{nodeid_parts[0]}::{item.originalname}"
        if len(nodeid_parts) == _NODEID_PARTS_WITH_CLASS:
            # Class method: path::class::function
            return f"{nodeid_parts[0]}::{nodeid_parts[1]}::{item.originalname}"
        # Fallback: use originalname to replace the last part
        return "::".join(nodeid_parts[:-1] + [item.originalname])

    # Fallback to regex parsing if originalname is not available
    return _REPEAT_PATTERN.sub("", item.nodeid)


class CoverageTracker:
    """Tracks requirement coverage and test results."""

    def __init__(self) -> None:
        """Initialize the coverage tracker."""
        self.all_requirements: set[str] = set()
        self.requirement_to_tests: dict[str, list] = defaultdict(list)
        # requirement_id -> set of test nodeids (as strings)
        self.requirement_to_nodeids: dict[str, set[str]] = defaultdict(set)
        # test nodeid -> outcome ("passed"/"failed"/"skipped"/"xfailed"/"xpassed")
        self.test_results: dict[str, str] = {}

    def add_requirement(self, requirement_id: str) -> None:
        """Add a requirement to track."""
        self.all_requirements.add(requirement_id)

    def add_test_coverage(
        self,
        requirement_id: str,
        test_item: pytest.Item,  # type: ignore[name-defined]
    ) -> None:
        """Record that a test covers a requirement."""
        self.requirement_to_tests[requirement_id].append(test_item)
        # Also store the base nodeid as a string for serialization
        base_nodeid = _get_base_nodeid(test_item)
        self.requirement_to_nodeids[requirement_id].add(base_nodeid)

    def record_test_result(self, test_nodeid: str, result: str) -> None:
        """Record the result of a test."""
        self.test_results[test_nodeid] = result

    def get_untested_requirements(self) -> set[str]:
        """Get requirements that have no tests covering them."""
        tested_requirements = set(self.requirement_to_tests.keys())
        return self.all_requirements - tested_requirements

    def get_requirements_with_failures(self) -> dict[str, list]:
        """Get requirements that have failing tests.

        Expected failures (xfailed) are considered passing and excluded.
        """
        failing: dict[str, list] = {}
        for requirement_id, test_items in self.requirement_to_tests.items():
            # Count tests as failing only if they are "failed" or "xpassed"
            # "xfailed" (expected failure) is considered passing
            failing_tests = [
                item
                for item in test_items
                if self.test_results.get(item.nodeid) in ("failed", "xpassed")
            ]
            if failing_tests:
                failing[requirement_id] = failing_tests
        return failing

    def get_requirement_test_nodeids(self, requirement_id: str) -> list[str]:
        """Get sorted list of test nodeids for a requirement.

        Args:
            requirement_id: The requirement ID to get test nodeids for.

        Returns:
            Sorted list of unique base test nodeids (alphabetically sorted for
            deterministic ordering). Repeat suffixes from pytest-repeat are stripped
            to avoid duplicates using the item's originalname property.
        """
        # First, get nodeids from test items if available
        test_items = self.requirement_to_tests.get(requirement_id, [])
        base_nodeids = {_get_base_nodeid(item) for item in test_items}
        # Also include nodeids stored as strings (from worker coverage merging)
        base_nodeids.update(self.requirement_to_nodeids.get(requirement_id, set()))
        return sorted(base_nodeids)

    def merge_from(self, other: CoverageTracker) -> None:
        """Merge data from another CoverageTracker into this one.

        Used to sync data from worker processes to the main process with pytest-xdist.

        Args:
            other: Another CoverageTracker to merge data from.
        """
        # Merge requirements
        self.all_requirements.update(other.all_requirements)

        # Merge test coverage (deduplicate by nodeid)
        for requirement_id, test_items in other.requirement_to_tests.items():
            existing_nodeids = {
                _get_base_nodeid(item)
                for item in self.requirement_to_tests[requirement_id]
            }
            for test_item in test_items:
                base_nodeid = _get_base_nodeid(test_item)
                if base_nodeid not in existing_nodeids:
                    self.requirement_to_tests[requirement_id].append(test_item)
                    existing_nodeids.add(base_nodeid)

        # Merge nodeids stored as strings
        for requirement_id, nodeids in other.requirement_to_nodeids.items():
            self.requirement_to_nodeids[requirement_id].update(nodeids)

        # Merge test results
        self.test_results.update(other.test_results)
