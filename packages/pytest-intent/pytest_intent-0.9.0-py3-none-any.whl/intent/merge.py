"""Module for merging requirements coverage artifacts."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

logger = logging.getLogger("pytest_intent")

# Error message constants
_ERR_EMPTY_ARTIFACTS = "Cannot merge empty list of artifacts"
_ERR_MISSING_VERSION = "All artifacts must have a 'version' field"
_ERR_INVALID_ALL_REQUIREMENTS = (
    "Invalid artifact structure: 'all_requirements' must be a list"
)
_ERR_INVALID_REQUIREMENT_COVERAGE = (
    "Invalid artifact structure: 'requirement_coverage' must be a dict"
)
_ERR_INVALID_TEST_RESULTS = "Invalid artifact structure: 'test_results' must be a dict"


def _validate_artifact_versions(artifacts: list[dict[str, Any]]) -> str:
    """Validate that all artifacts have the same version.

    Args:
        artifacts: List of artifact dictionaries.

    Returns:
        The version string.

    Raises:
        ValueError: If artifacts have different versions or missing version.
    """
    versions = {artifact.get("version") for artifact in artifacts}
    if len(versions) > 1:
        versions_str = ", ".join(sorted(str(v) for v in versions))
        msg = f"Cannot merge artifacts with different versions: {versions_str}"
        raise ValueError(msg)
    if not versions or None in versions:
        raise ValueError(_ERR_MISSING_VERSION)
    return versions.pop()


def _merge_all_requirements(artifacts: list[dict[str, Any]]) -> set[str]:
    """Merge all_requirements from all artifacts.

    Args:
        artifacts: List of artifact dictionaries.

    Returns:
        Set of all requirement IDs.

    Raises:
        TypeError: If artifact structure is invalid.
    """
    all_requirements: set[str] = set()
    for artifact in artifacts:
        reqs = artifact.get("all_requirements", [])
        if not isinstance(reqs, list):
            raise TypeError(_ERR_INVALID_ALL_REQUIREMENTS)
        all_requirements.update(reqs)
    return all_requirements


def _merge_requirement_coverage(artifacts: list[dict[str, Any]]) -> dict[str, set[str]]:
    """Merge requirement_coverage from all artifacts.

    Args:
        artifacts: List of artifact dictionaries.

    Returns:
        Dictionary mapping requirement IDs to sets of test nodeids.

    Raises:
        TypeError: If artifact structure is invalid.
    """
    requirement_coverage: dict[str, set[str]] = {}
    for artifact in artifacts:
        coverage = artifact.get("requirement_coverage", {})
        if not isinstance(coverage, dict):
            raise TypeError(_ERR_INVALID_REQUIREMENT_COVERAGE)
        for req_id, nodeids in coverage.items():
            if not isinstance(nodeids, list):
                msg = (
                    f"Invalid artifact structure: coverage for {req_id} must be a list"
                )
                raise TypeError(msg)
            if req_id not in requirement_coverage:
                requirement_coverage[req_id] = set()
            requirement_coverage[req_id].update(nodeids)
    return requirement_coverage


def _merge_test_results(artifacts: list[dict[str, Any]]) -> dict[str, str]:
    """Merge test_results from all artifacts.

    Args:
        artifacts: List of artifact dictionaries.

    Returns:
        Dictionary mapping test nodeids to outcomes.

    Raises:
        TypeError: If artifact structure is invalid.
    """
    test_results: dict[str, str] = {}
    for artifact in artifacts:
        results = artifact.get("test_results", {})
        if not isinstance(results, dict):
            raise TypeError(_ERR_INVALID_TEST_RESULTS)
        test_results.update(results)
    return test_results


def merge_coverage_artifacts(artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge multiple coverage artifacts into a single artifact.

    Uses union behavior to combine all data:
    - All requirements are combined (union of sets)
    - Requirement coverage merges test nodeids (union, deduplicated)
    - Test results are combined (union, keeping all results)
    - Untested requirements are recalculated from merged data

    Args:
        artifacts: List of artifact dictionaries to merge.

    Returns:
        Merged artifact dictionary with the same structure as input artifacts.

    Raises:
        ValueError: If artifacts have different versions or invalid structure.
        TypeError: If artifact structure has invalid types.
    """
    if not artifacts:
        raise ValueError(_ERR_EMPTY_ARTIFACTS)

    # Validate all artifacts have the same version
    version = _validate_artifact_versions(artifacts)

    # Merge all_requirements (union of all requirement sets)
    all_requirements = _merge_all_requirements(artifacts)

    # Merge requirement_coverage (union of test nodeids per requirement)
    requirement_coverage = _merge_requirement_coverage(artifacts)

    # Merge test_results (union of all test results)
    test_results = _merge_test_results(artifacts)

    # Recalculate untested_requirements from merged data
    tested_requirements = set(requirement_coverage.keys())
    untested_requirements = sorted(all_requirements - tested_requirements)

    # Build final merged artifact with sorted data for consistency
    merged = {
        "version": version,
        "all_requirements": sorted(all_requirements),
        "requirement_coverage": {
            req_id: sorted(nodeids) for req_id, nodeids in requirement_coverage.items()
        },
        "test_results": dict(sorted(test_results.items())),
        "untested_requirements": untested_requirements,
    }

    logger.debug(
        "Merged %d artifacts: %d requirements, %d covered, %d untested, %d results",
        len(artifacts),
        len(all_requirements),
        len(requirement_coverage),
        len(untested_requirements),
        len(test_results),
    )

    return merged
