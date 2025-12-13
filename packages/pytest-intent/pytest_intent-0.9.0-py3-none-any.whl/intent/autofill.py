"""Module for autofilling Doorstop requirement references."""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING, Literal

from intent.requirements import (
    get_doorstop_item,
    get_item_references,
    save_doorstop_item,
    update_item_references,
)

if TYPE_CHECKING:
    from pathlib import Path

    from intent.coverage import CoverageTracker

logger = logging.getLogger("pytest_intent")

OutdatedBehavior = Literal["fail", "warn", "ignore"]


def check_and_update_references(
    tracker: CoverageTracker,
    requirements_path: Path,
    *,
    autofill_enabled: bool,
    outdated_behavior: OutdatedBehavior,
    requirements_format: str,
) -> None:
    """Check and update Doorstop requirement references based on test coverage.

    Args:
        tracker: Coverage tracker instance.
        requirements_path: Path to the Doorstop requirements directory.
        autofill_enabled: Whether to automatically update references.
        outdated_behavior: Behavior when references are outdated ("fail", "warn",
            or "ignore").
        requirements_format: Format of requirements (currently only "doorstop"
            supported).

    Raises:
        SystemExit: If references are outdated and behavior is set to "fail".
    """
    # If both features are disabled, skip
    if not autofill_enabled and outdated_behavior == "ignore":
        return

    if requirements_format != "doorstop":  # pragma: no cover
        # Only support doorstop format for now
        return

    outdated_requirements: list[str] = []

    def _process_requirement(requirement_id: str) -> bool:
        """Process a single requirement and return True if it's outdated.

        Args:
            requirement_id: The requirement ID to process.

        Returns:
            True if the requirement has outdated references, False otherwise.
        """
        try:
            # Get the Doorstop item
            item = get_doorstop_item(requirements_path, requirement_id)

            # Get current references from the item
            current_references = get_item_references(item)

            # Get expected references (sorted test nodeids)
            expected_references = tracker.get_requirement_test_nodeids(requirement_id)

            if current_references == expected_references:
                return False

            # Compare current vs expected (order-sensitive comparison)
            # Log the difference
            logger.debug(
                "Requirement %s has outdated references. Current: %s, Expected: %s",
                requirement_id,
                current_references,
                expected_references,
            )

            # Update references if autofill is enabled
            update_item_references(item, expected_references)
            save_doorstop_item(item)
            logger.info(
                "Updated references for requirement %s: %s",
                requirement_id,
                expected_references,
            )
        except (ValueError, RuntimeError) as e:  # pragma: no cover
            logger.warning(
                "Failed to check/update references for requirement %s: %s",
                requirement_id,
                e,
            )
            return False
        return True

    # Iterate through all requirements that have test coverage
    outdated_requirements = [
        requirement_id
        for requirement_id in tracker.requirement_to_tests
        if _process_requirement(requirement_id)
    ]

    # Handle outdated behavior
    if outdated_requirements and outdated_behavior != "ignore":
        error_message = (
            f"\nDoorstop requirements with outdated references "
            f"({len(outdated_requirements)}):\n"
            + "\n".join(f"  - {req_id}" for req_id in sorted(outdated_requirements))
        )

        if outdated_behavior == "fail":
            error_message += (
                "\n\nRun with --intent-references-autofill-enabled to automatically "
                "update references."
            )
            logger.error(error_message)
            print(error_message, file=sys.stderr)  # noqa: T201
            # Raise SystemExit to fail early before tests run
            raise SystemExit(1)
        if outdated_behavior == "warn":
            logger.warning(error_message)
