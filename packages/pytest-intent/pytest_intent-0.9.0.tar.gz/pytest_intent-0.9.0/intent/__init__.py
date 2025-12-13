"""A pytest plugin for intent-based testing."""

from __future__ import annotations

import json
import logging
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

from intent.autofill import check_and_update_references
from intent.coverage import CoverageTracker, _get_base_nodeid
from intent.requirements import load_doorstop_requirements

if TYPE_CHECKING:
    import pytest

logger = logging.getLogger("pytest_intent")


def _str_to_bool(value: str | None) -> bool:
    """Convert string to boolean."""
    if value is None:
        return True
    return value.lower() in ("true", "1", "yes", "on")


def _normalized_path(value: str | Path) -> Path:
    """Normalize a path."""
    return Path(value).expanduser().resolve()


def _get_coverage_tmpdir() -> Path:
    """Get the temporary directory for storing worker coverage files.

    This directory is used to store JSON files containing coverage data from
    worker processes, which are then merged by the main process. This approach
    is similar to how pytest-cov handles distributed coverage.

    Returns:
        Path to the temporary directory for coverage files.
    """
    tmpdir = Path(tempfile.gettempdir()) / "pytest_intent_coverage"
    tmpdir.mkdir(parents=True, exist_ok=True)
    return tmpdir


def _write_worker_coverage(
    tracker: CoverageTracker,
    worker_id: str,
    tmpdir: Path,
) -> None:
    """Write worker coverage data to a temporary JSON file.

    Args:
        tracker: The coverage tracker with collected data.
        worker_id: The worker ID (e.g., "gw0").
        tmpdir: Temporary directory for coverage files.
    """
    coverage_data: dict[str, list[str]] = {}
    for requirement_id, test_items in tracker.requirement_to_tests.items():
        nodeids = sorted({_get_base_nodeid(item) for item in test_items})
        coverage_data[requirement_id] = nodeids

    # Include test results in the worker coverage file
    worker_data: dict[str, object] = {
        "requirement_coverage": coverage_data,
        "test_results": dict(tracker.test_results),
    }

    if not coverage_data and not tracker.test_results:
        logger.info(
            "No coverage data to write for worker %s (tracker has %d requirements)",
            worker_id,
            len(tracker.requirement_to_tests),
        )
        # Write an empty file to indicate this worker had no coverage
        coverage_file = tmpdir / f"intent_coverage_{worker_id}.json"
        with coverage_file.open("w") as f:
            json.dump({}, f)
        logger.info("Wrote empty coverage file for worker %s", worker_id)
        return

    coverage_file = tmpdir / f"intent_coverage_{worker_id}.json"
    with coverage_file.open("w") as f:
        json.dump(worker_data, f)
    logger.info(
        "Wrote worker coverage to %s: %d requirements, %d test results",
        coverage_file,
        len(coverage_data),
        len(tracker.test_results),
    )


def _write_worker_test_results(
    tracker: CoverageTracker,
    worker_id: str,
    tmpdir: Path,
) -> None:
    """Write worker test results to a temporary JSON file.

    Args:
        tracker: The coverage tracker with test results.
        worker_id: The worker ID (e.g., "gw0").
        tmpdir: Temporary directory for coverage files.
    """
    if not tracker.test_results:
        return

    results_file = tmpdir / f"intent_test_results_{worker_id}.json"
    with results_file.open("w") as f:
        json.dump(tracker.test_results, f)
    logger.debug(
        "Wrote worker test results to %s: %d results",
        results_file,
        len(tracker.test_results),
    )


def _read_worker_test_results_file(results_file: Path) -> dict[str, str] | None:
    """Read test results from a single worker file.

    Args:
        results_file: Path to the test results file.

    Returns:
        Dictionary of test results, or None if reading failed.
    """
    try:
        with results_file.open("r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logger.warning(
            "Failed to read test results file %s: %s",
            results_file,
            e,
        )
        return None


def _read_and_merge_worker_test_results(
    tracker: CoverageTracker,
    tmpdir: Path,
) -> None:
    """Read and merge test results from worker files.

    Args:
        tracker: The main process tracker to merge into.
        tmpdir: Temporary directory containing test result files.
    """
    results_files = sorted(tmpdir.glob("intent_test_results_*.json"))
    for results_file in results_files:
        worker_results = _read_worker_test_results_file(results_file)
        if worker_results:
            tracker.test_results.update(worker_results)
            logger.debug(
                "Merged %d test results from %s",
                len(worker_results),
                results_file.name,
            )


def _read_and_merge_worker_coverage(
    tracker: CoverageTracker,
    tmpdir: Path,
) -> None:
    """Read all worker coverage files and merge into main tracker.

    This function reads JSON files written by worker processes and merges
    the coverage data into the main process tracker. Requirements are marked
    as tested by ensuring they're in the requirement_to_tests dictionary.
    Since we can't recreate the actual test items, we use empty lists to
    mark them as tested.

    Args:
        tracker: The main process tracker to merge into.
        tmpdir: Temporary directory containing coverage files.
    """
    if not tmpdir.exists():
        logger.debug("No coverage tmpdir found at %s", tmpdir)
        return

    coverage_files = sorted(tmpdir.glob("intent_coverage_*.json"))
    if not coverage_files:
        logger.debug("No worker coverage files found in %s", tmpdir)
        return

    logger.debug("Found %d worker coverage files", len(coverage_files))

    all_covered_requirements: set[str] = set()
    for coverage_file in coverage_files:
        try:
            with coverage_file.open("r") as f:
                worker_data = json.load(f)

            # Handle both old format (dict of requirement_id -> nodeids)
            # and new format (dict with "requirement_coverage" and "test_results")
            if "requirement_coverage" in worker_data:
                # New format
                worker_coverage = worker_data["requirement_coverage"]
                worker_test_results = worker_data.get("test_results", {})
            else:
                # Old format (backward compatibility)
                worker_coverage = worker_data
                worker_test_results = {}

            # Merge requirement coverage
            for requirement_id, nodeids in worker_coverage.items():
                all_covered_requirements.add(requirement_id)
                # Mark requirement as tested by ensuring it's in requirement_to_tests
                # We use empty list since we can't recreate the actual items
                if requirement_id not in tracker.requirement_to_tests:
                    tracker.requirement_to_tests[requirement_id] = []
                # Store nodeids as strings so they can be retrieved for serialization
                tracker.requirement_to_nodeids[requirement_id].update(nodeids)
                logger.debug(
                    "Merged coverage for %s: %d tests from %s",
                    requirement_id,
                    len(nodeids),
                    coverage_file.name,
                )

            # Merge test results
            tracker.test_results.update(worker_test_results)
            if worker_test_results:
                logger.debug(
                    "Merged %d test results from %s",
                    len(worker_test_results),
                    coverage_file.name,
                )
        except (OSError, json.JSONDecodeError) as e:  # noqa: PERF203
            logger.warning(
                "Failed to read coverage file %s: %s",
                coverage_file,
                e,
            )

    logger.info(
        "Merged coverage from %d workers: %d requirements covered",
        len(coverage_files),
        len(all_covered_requirements),
    )


def _serialize_coverage_to_json(tracker: CoverageTracker) -> dict[str, object]:
    """Serialize coverage tracker data to a JSON-serializable dictionary.

    Args:
        tracker: The coverage tracker with collected data.

    Returns:
        Dictionary containing coverage data in JSON-serializable format.
    """
    # Build requirement coverage mapping
    requirement_coverage: dict[str, list[str]] = {}
    for requirement_id in tracker.all_requirements:
        nodeids = tracker.get_requirement_test_nodeids(requirement_id)
        if nodeids:
            requirement_coverage[requirement_id] = nodeids

    # Get untested requirements
    untested_requirements = sorted(tracker.get_untested_requirements())

    # Build all requirements list (sorted for consistency)
    all_requirements = sorted(tracker.all_requirements)

    # Build test results dictionary
    test_results: dict[str, str] = dict(tracker.test_results)

    return {
        "version": "1.0",
        "all_requirements": all_requirements,
        "requirement_coverage": requirement_coverage,
        "test_results": test_results,
        "untested_requirements": untested_requirements,
    }


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add command line options for the plugin."""
    parser.addoption(
        "--intent-enabled",
        action="store",
        nargs="?",
        const="true",
        type=_str_to_bool,
        default=True,
        help=(
            "Enable the pytest-intent plugin (default: true, "
            "use --intent-enabled or --intent-enabled=true to enable, "
            "--intent-enabled=false to disable)"
        ),
    )

    parser.addoption(
        "--intent-requirements-format",
        choices=["doorstop"],
        default="doorstop",
        help="The format of the project's requirements (default: doorstop)",
    )

    parser.addoption(
        "--intent-requirements-path",
        default="requirements",
        type=_normalized_path,
        help="The path to the directory containing the project's requirements (default: requirements)",  # noqa: E501
    )

    parser.addoption(
        "--intent-references-autofill-enabled",
        action="store",
        nargs="?",
        const="true",
        type=_str_to_bool,
        default=True,
        help=(
            "Enable autofilling Doorstop requirements references field with test "
            "nodeids (default: false, use --intent-references-autofill-enabled or "
            "--intent-references-autofill-enabled=true to enable, "
            "--intent-references-autofill-enabled=false to disable)"
        ),
    )

    parser.addoption(
        "--intent-references-outdated-behavior",
        choices=["fail", "warn", "ignore"],
        default="ignore",
        help=(
            "Behavior when Doorstop requirements references are outdated "
            "(default: ignore, choices: fail, warn, ignore)"
        ),
    )

    parser.addoption(
        "--intent-requirements-untested-behavior",
        choices=["fail", "warn", "ignore"],
        default="fail",
        help=(
            "Behavior when requirements are untested "
            "(default: fail, choices: fail, warn, ignore)"
        ),
    )

    parser.addoption(
        "--intent-coverage-report",
        default=None,
        type=_normalized_path,
        help="Path to write a JSON artifact containing requirements coverage data",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Register the plugin with pytest."""
    if not config.getoption("--intent-enabled"):
        logger.info("Intent plugin is disabled")
        return

    # Register our custom intention marker.
    config.addinivalue_line(
        "markers",
        "intent(requirement): mark test as associated with a requirement",
    )

    # Initialize coverage tracker if intent is enabled
    tracker = CoverageTracker()
    config.pluginmanager.register(tracker, "intent_coverage_tracker")


def pytest_sessionstart(session: pytest.Session) -> None:
    """Load requirements when test session starts."""
    config = session.config
    if not config.getoption("--intent-enabled"):
        return

    # Skip loading requirements on worker processes when using pytest-xdist
    # Requirements should only be loaded on the main process
    try:
        # pytest-xdist sets workerinput to a dict on worker processes
        if isinstance(config.workerinput, dict):
            logger.debug("Skipping requirement loading on worker process")
            return
    except AttributeError:
        # workerinput doesn't exist, we're on the main process
        pass

    tracker = _get_tracker(config)
    if not tracker:
        return

    # Load requirements from Doorstop
    requirements_path_raw = config.getoption("--intent-requirements-path")
    # Ensure it's a Path object (type conversion in addoption may not always work)
    requirements_path = _normalized_path(requirements_path_raw)
    requirements_format = config.getoption("--intent-requirements-format")

    if requirements_format == "doorstop":
        try:
            requirement_ids = load_doorstop_requirements(requirements_path)
            for req_id in requirement_ids:
                tracker.add_requirement(req_id)
            logger.info(
                "Loaded %d requirements for coverage tracking",
                len(requirement_ids),
            )
        except (ImportError, ValueError):
            logger.exception("Failed to load requirements")
            # Don't fail here, let validation catch it


def _get_tracker(config: pytest.Config) -> CoverageTracker | None:
    """Get the coverage tracker from the plugin manager."""
    if not config.getoption("--intent-enabled"):
        return None
    return config.pluginmanager.get_plugin("intent_coverage_tracker")


def _is_worker_process(config: pytest.Config) -> bool:
    """Check if we're running on a pytest-xdist worker process.

    Args:
        config: The pytest config object.

    Returns:
        True if running on a worker process, False otherwise.
    """
    try:
        # pytest-xdist sets workerinput to a dict on worker processes
        return isinstance(config.workerinput, dict)
    except AttributeError:
        # workerinput doesn't exist, we're on the main process
        return False


def _should_skip_validation(
    config: pytest.Config,  # noqa: ARG001
    tracker: CoverageTracker,
) -> bool:
    """Check if requirement coverage validation should be skipped.

    Args:
        config: The pytest config object (unused, kept for API compatibility).
        tracker: The coverage tracker.

    Returns:
        True if validation should be skipped, False otherwise.
    """
    # If there are no requirements, there's nothing to validate
    if not tracker.all_requirements:
        logger.debug("Skipping requirement coverage validation: no requirements loaded")
        return True

    # With pytest-xdist, we sync data from workers via file-based approach,
    # so we should validate if we have requirements. The coverage data will
    # be merged before validation runs.
    return False


def _validate_untested_requirements(
    tracker: CoverageTracker,
    untested_behavior: str,
) -> list[str]:
    """Validate untested requirements based on behavior setting.

    Args:
        tracker: The coverage tracker.
        untested_behavior: Behavior setting ("fail", "warn", or "ignore").

    Returns:
        List of error messages (empty if no errors or behavior is warn/ignore).
    """
    errors: list[str] = []
    untested = tracker.get_untested_requirements()
    if untested:
        untested_sorted = sorted(untested)
        untested_message = (
            f"Untested requirements ({len(untested_sorted)}): "
            f"{', '.join(untested_sorted)}"
        )

        if untested_behavior == "fail":
            errors.append(untested_message)
        elif untested_behavior == "warn":
            logger.warning(untested_message)
        # If behavior is "ignore", do nothing

    return errors


def _validate_failing_requirements(tracker: CoverageTracker) -> list[str]:
    """Validate requirements with failing tests.

    Args:
        tracker: The coverage tracker.

    Returns:
        List of error messages (empty if no failing requirements).
    """
    errors: list[str] = []
    failing = tracker.get_requirements_with_failures()
    if failing:
        failing_list = []
        for req_id, test_items in failing.items():
            test_names = [item.nodeid for item in test_items]
            failing_list.append(
                f"{req_id} (failing tests: {', '.join(test_names)})",
            )
        errors.append(
            f"Requirements with failing tests ({len(failing)}): "
            f"{', '.join(failing_list)}",
        )
    return errors


def _report_validation_results(session: pytest.Session, errors: list[str]) -> None:
    """Report validation results and set exit status if needed.

    Args:
        session: The pytest session object.
        errors: List of error messages from validation.
    """
    if not errors:
        logger.info("All requirements are covered by passing tests")
        return

    error_message = "\nRequirement coverage validation failed:\n" + "\n".join(
        f"  - {error}" for error in errors
    )
    logger.error(error_message)
    # Fail the test run by setting exitstatus to non-zero
    session.exitstatus = 1
    # Also print to stderr so it's visible
    print(error_message, file=sys.stderr)  # noqa: T201


def pytest_collection_modifyitems(  # noqa: C901
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Modify collected test items to track requirement coverage."""
    tracker = _get_tracker(config)
    if not tracker:
        return

    # Check if we're on a worker process
    is_worker = _is_worker_process(config)

    logger.debug(
        "Processing %d test items for requirement coverage (%s)",
        len(items),
        "worker" if is_worker else "main",
    )

    for item in items:
        intent_marker = item.get_closest_marker("intent")
        if not intent_marker:
            continue

        # Extract requirement ID from marker
        # Marker can be: @pytest.mark.intent("SRD-001")
        # or @pytest.mark.intent(requirement="SRD-001")
        requirement_id = None
        if intent_marker.args:
            requirement_id = str(intent_marker.args[0])
        elif "requirement" in intent_marker.kwargs:
            requirement_id = str(intent_marker.kwargs["requirement"])

        if not requirement_id:
            continue

        tracker.add_test_coverage(requirement_id, item)
        logger.debug(
            "Test %s covers requirement %s (%s)",
            item.nodeid,
            requirement_id,
            "worker" if is_worker else "main",
        )

    # With pytest-xdist, write worker coverage data to files for merging
    # This is similar to how pytest-cov handles distributed coverage
    if is_worker and config.pluginmanager.hasplugin("xdist"):
        try:
            worker_id = config.workerinput.get("workerid", "unknown")  # type: ignore[attr-defined]
            tmpdir = _get_coverage_tmpdir()
            _write_worker_coverage(tracker, worker_id, tmpdir)
            logger.debug(
                "Worker %s: Wrote coverage to file for merging",
                worker_id,
            )
        except Exception:
            logger.exception("Failed to write worker coverage file")

    # After collecting all test coverage, check and update references
    # Only do this on the main process (not on workers) to avoid conflicts
    if not _is_worker_process(config) and config.getoption("--intent-enabled"):
        requirements_path_raw = config.getoption("--intent-requirements-path")
        requirements_path = _normalized_path(requirements_path_raw)

        # Extract domain-specific values from config
        autofill_enabled = config.getoption("--intent-references-autofill-enabled")
        outdated_behavior = config.getoption("--intent-references-outdated-behavior")
        requirements_format = config.getoption("--intent-requirements-format")

        try:
            check_and_update_references(
                tracker,
                requirements_path,
                autofill_enabled=autofill_enabled,
                outdated_behavior=outdated_behavior,
                requirements_format=requirements_format,
            )
        except SystemExit:
            # Re-raise to fail early before tests run
            raise
        except Exception:
            # Log other errors but don't fail the test run
            logger.exception("Error checking/updating references")


def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo,
) -> pytest.TestReport | None:
    """Track test results and collect coverage for requirement coverage validation."""
    config = item.config
    tracker = _get_tracker(config)
    if not tracker:
        return

    # With pytest-xdist, also collect test coverage on the main process
    # (pytest_collection_modifyitems runs on workers, but we also need coverage
    # on the main process for validation)
    is_worker = _is_worker_process(config)
    if config.pluginmanager.hasplugin("xdist") and not is_worker:
        intent_marker = item.get_closest_marker("intent")
        if intent_marker:
            # Extract requirement ID from marker
            requirement_id = None
            if intent_marker.args:
                requirement_id = str(intent_marker.args[0])
            elif "requirement" in intent_marker.kwargs:
                requirement_id = str(intent_marker.kwargs["requirement"])

            if requirement_id:
                # Check if we already have this coverage to avoid duplicates
                existing_nodeids = {
                    _get_base_nodeid(test_item)
                    for test_item in tracker.requirement_to_tests.get(
                        requirement_id,
                        [],
                    )
                }
                base_nodeid = _get_base_nodeid(item)
                if base_nodeid not in existing_nodeids:
                    tracker.add_test_coverage(requirement_id, item)
                    logger.debug(
                        "Added test coverage in makereport (main): %s covers %s",
                        item.nodeid,
                        requirement_id,
                    )

    # Only record results when the test is actually called
    # (not during setup/teardown)
    if call.when != "call":
        return

    # Determine outcome, accounting for xfail markers
    has_xfail = item.get_closest_marker("xfail") is not None
    test_failed = call.excinfo is not None

    if has_xfail:
        # Expected failure: if it failed, it's "xfailed" (passing)
        # If it passed, it's "xpassed" (unexpected pass, considered failing)
        outcome = "xfailed" if test_failed else "xpassed"
    else:
        # Normal test: passed or failed
        outcome = "passed" if not test_failed else "failed"

    tracker.record_test_result(item.nodeid, outcome)
    logger.debug("Test %s result: %s", item.nodeid, outcome)


def _handle_xdist_worker_finish(
    config: pytest.Config,
    tracker: CoverageTracker,
) -> bool:
    """Handle pytest-xdist worker process finish.

    Args:
        config: The pytest config object.
        tracker: The coverage tracker.

    Returns:
        True if this is a worker process (and we should return early), False otherwise.
    """
    if not config.pluginmanager.hasplugin("xdist"):
        return False

    tmpdir = _get_coverage_tmpdir()
    # If we're on a worker, write test results before finishing
    if _is_worker_process(config):
        try:
            worker_id = config.workerinput.get("workerid", "unknown")  # type: ignore[attr-defined]
            _write_worker_test_results(tracker, worker_id, tmpdir)
        except Exception:
            logger.exception("Failed to write worker test results")
        logger.debug("Skipping requirement coverage validation on worker process")
        return True

    # On main process, read and merge worker coverage and test results
    _read_and_merge_worker_coverage(tracker, tmpdir)
    _read_and_merge_worker_test_results(tracker, tmpdir)
    return False


def _update_references_after_merge(
    config: pytest.Config,
    tracker: CoverageTracker,
) -> None:
    """Update references after merging worker coverage.

    This ensures references are updated with complete coverage data
    when using pytest-xdist.

    Args:
        config: The pytest config object.
        tracker: The coverage tracker.
    """
    if not config.getoption("--intent-enabled"):
        return

    requirements_path_raw = config.getoption("--intent-requirements-path")
    if not requirements_path_raw:
        return

    requirements_path = _normalized_path(requirements_path_raw)
    autofill_enabled = config.getoption("--intent-references-autofill-enabled")
    requirements_format = config.getoption("--intent-requirements-format")

    # Only update if autofill is enabled (don't fail here, that should happen
    # during collection if needed)
    if autofill_enabled:
        try:
            check_and_update_references(
                tracker,
                requirements_path,
                autofill_enabled=autofill_enabled,
                outdated_behavior="ignore",  # Don't fail after tests run
                requirements_format=requirements_format,
            )
        except Exception:
            # Log errors but don't fail the test run
            logger.exception("Error updating references after test run")


def _write_coverage_report_artifact(
    config: pytest.Config,
    tracker: CoverageTracker,
) -> None:
    """Write coverage report artifact if requested.

    Args:
        config: The pytest config object.
        tracker: The coverage tracker.
    """
    coverage_report_path = config.getoption("--intent-coverage-report")
    if not coverage_report_path:
        return

    try:
        # Ensure parent directory exists
        coverage_report_path.parent.mkdir(parents=True, exist_ok=True)

        # Serialize coverage data to JSON
        coverage_data = _serialize_coverage_to_json(tracker)

        # Write JSON file with indentation for readability
        with coverage_report_path.open("w") as f:
            json.dump(coverage_data, f, indent=2)

        logger.info(
            "Wrote requirements coverage report to %s",
            coverage_report_path,
        )
    except (OSError, json.JSONEncodeError):
        logger.exception(
            "Failed to write coverage report to %s",
            coverage_report_path,
        )


def pytest_sessionfinish(
    session: pytest.Session,
    exitstatus: int,  # noqa: ARG001
) -> None:
    """Validate requirement coverage and fail if requirements are untested."""
    config = session.config

    tracker = _get_tracker(config)
    if not tracker:
        return

    # With pytest-xdist, write test results from workers and merge coverage
    if _handle_xdist_worker_finish(config, tracker):
        return

    # Check if validation should be skipped (e.g., pytest-xdist with no coverage)
    if _should_skip_validation(config, tracker):
        return

    logger.info("Validating requirement coverage...")

    # Get untested behavior from config
    untested_behavior = config.getoption("--intent-requirements-untested-behavior")

    # Collect validation errors
    errors: list[str] = []
    errors.extend(_validate_untested_requirements(tracker, untested_behavior))
    errors.extend(_validate_failing_requirements(tracker))

    # Report results
    _report_validation_results(session, errors)

    # Update references after merging worker coverage
    _update_references_after_merge(config, tracker)

    # Write coverage report artifact if requested
    _write_coverage_report_artifact(config, tracker)
