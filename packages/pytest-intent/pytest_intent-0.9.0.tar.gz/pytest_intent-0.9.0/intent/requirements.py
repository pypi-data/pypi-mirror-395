"""Module for loading requirements from Doorstop."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import doorstop

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger("pytest_intent")

# Attribute name for excluding requirements from coverage tracking
EXCLUDE_ATTRIBUTE = "intent.requirements.devstrek.com/exclude"


def is_requirement_excluded(item: doorstop.Item) -> bool:
    """Check if a requirement should be excluded from coverage tracking.

    Args:
        item: The Doorstop item to check.

    Returns:
        True if the requirement should be excluded, False otherwise.
    """
    # Access custom attributes through item.data dictionary
    # Doorstop stores all YAML fields in the data dictionary
    exclude_value = item.data.get(EXCLUDE_ATTRIBUTE, False)
    is_excluded = bool(exclude_value)
    if is_excluded:
        logger.debug(
            "Requirement %s is excluded from coverage tracking",
            item.uid,
        )
    return is_excluded


def load_doorstop_requirements(requirements_path: Path) -> set[str]:
    """Load all requirement IDs from a Doorstop requirements directory.

    Args:
        requirements_path: Path to the directory containing Doorstop requirements.

    Returns:
        Set of requirement IDs (e.g., {"SRD-001", "SRD-002"}).

    Raises:
        ValueError: If requirements cannot be loaded.
    """
    logger.debug("Loading Doorstop requirements from %s", requirements_path)

    if not requirements_path.exists():
        msg = f"Requirements path does not exist: {requirements_path}"
        raise ValueError(msg)

    if not requirements_path.is_dir():
        msg = f"Requirements path is not a directory: {requirements_path}"
        raise ValueError(msg)

    # Load the Doorstop document from the requirements directory
    document = doorstop.Document(requirements_path)

    requirement_ids: set[str] = set()
    excluded_count = 0

    # Iterate through all items (requirements) in the document
    for item in document:
        # Skip excluded requirements
        if is_requirement_excluded(item):
            excluded_count += 1
            continue

        requirement_id = str(item.uid)
        requirement_ids.add(requirement_id)
        logger.debug("Found requirement: %s", requirement_id)

    logger.info(
        "Loaded %d requirements from Doorstop%s",
        len(requirement_ids),
        f" (excluded {excluded_count})" if excluded_count > 0 else "",
    )
    return requirement_ids


def get_doorstop_item(requirements_path: Path, requirement_id: str) -> doorstop.Item:
    """Get a specific Doorstop item by ID.

    Args:
        requirements_path: Path to the directory containing Doorstop requirements.
        requirement_id: The requirement ID to retrieve (e.g., "SRD-001").

    Returns:
        The Doorstop item for the given requirement ID.

    Raises:
        ValueError: If the requirements path is invalid or the item is not found.
    """
    logger.debug("Getting Doorstop item %s from %s", requirement_id, requirements_path)

    if not requirements_path.exists():
        msg = f"Requirements path does not exist: {requirements_path}"
        raise ValueError(msg)

    if not requirements_path.is_dir():
        msg = f"Requirements path is not a directory: {requirements_path}"
        raise ValueError(msg)

    # Load the Doorstop document from the requirements directory
    document = doorstop.Document(requirements_path)

    # Find the item with the matching UID
    for item in document:
        if str(item.uid) == requirement_id:
            logger.debug("Found Doorstop item: %s", requirement_id)
            return item

    msg = f"Requirement {requirement_id} not found in {requirements_path}"
    raise ValueError(msg)


def get_item_references(item: doorstop.Item) -> list[str]:
    """Read current references from a Doorstop item.

    Args:
        item: The Doorstop item to read references from.

    Returns:
        List of reference strings (extracted from path field).
        Returns empty list if references field doesn't exist.
    """
    # Doorstop items have a 'references' attribute that is a list of dicts
    # with 'path' and 'type'
    # If it doesn't exist or is None, return empty list
    references = getattr(item, "references", None)
    if references is None:
        return []
    if isinstance(references, list):
        # Extract path from each reference dict
        result = []
        for ref in references:
            if isinstance(ref, dict) and "path" in ref:
                result.append(str(ref["path"]))
            elif isinstance(ref, str):
                # Handle case where it's already a string
                result.append(ref)
        return result
    # If it's not a list, return empty list
    return []


def update_item_references(item: doorstop.Item, references: list[str]) -> None:
    """Update the references field of a Doorstop item.

    Args:
        item: The Doorstop item to update.
        references: List of reference strings (test nodeids) to set.
    """
    logger.debug("Updating references for item %s: %s", item.uid, references)
    # Doorstop expects references as a list of dicts with 'path' and 'type' keys
    # Convert list of strings to list of dicts
    item.references = [{"path": ref, "type": "file"} for ref in references]


def save_doorstop_item(item: doorstop.Item) -> None:
    """Save changes to a Doorstop item.

    Args:
        item: The Doorstop item to save.

    Raises:
        RuntimeError: If the item cannot be saved.
    """
    logger.debug("Saving Doorstop item %s", item.uid)
    try:
        item.save()
        logger.debug("Successfully saved Doorstop item %s", item.uid)
    except Exception as e:
        msg = f"Failed to save Doorstop item {item.uid}: {e}"
        logger.exception(msg)
        raise RuntimeError(msg) from e
