"""CLI interface for pytest-intent."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import rich_click as click

from intent.merge import merge_coverage_artifacts

__version__ = "0.6.0"


def _load_artifact_file(file_path: Path) -> dict | None:
    """Load a single artifact file.

    Args:
        file_path: Path to the JSON file to load.

    Returns:
        Artifact dictionary, or None if loading failed.
    """
    try:
        with file_path.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        click.echo(
            f"Error: Failed to read {file_path}: {e}",
            err=True,
        )
        return None


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """pytest-intent: A pytest plugin for intent-based testing."""


@main.group()
def requirements() -> None:
    """Commands for managing requirements."""


@requirements.group()
def coverage() -> None:
    """Commands for managing requirements coverage."""


@coverage.command()
@click.option(
    "--input",
    "-i",
    "input_pattern",
    required=True,
    help="Glob pattern for input JSON files to merge",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    required=True,
    type=click.Path(path_type=Path),
    help="Output file path for merged artifact",
)
@click.argument(
    "path",
    default=Path.cwd(),
    type=click.Path(path_type=Path),
    help="Path to the directory containing the JSON files to merge",
)
def merge(path: Path, input_pattern: str, output_path: Path) -> None:
    """Merge multiple requirements coverage artifacts into a single artifact.

    This command merges multiple JSON artifacts produced by different pytest
    invocations (e.g., different CI jobs) into a single merged artifact.

    Example:
        pytest-intent requirements coverage merge -i "artifacts/*.json" -o merged.json
    """
    # Find all files matching the glob pattern
    path = path.resolve()
    matching_files = sorted(path.glob(pattern=input_pattern))

    if not matching_files:
        click.echo(
            f"Error: No files found matching pattern '{input_pattern}'",
            err=True,
        )
        sys.exit(1)

    click.echo(f"Found {len(matching_files)} file(s) to merge")

    # Load all artifacts
    artifacts: list[dict] = []
    for file_path_str in matching_files:
        file_path = Path(file_path_str)
        artifact = _load_artifact_file(file_path)
        if artifact is None:
            sys.exit(1)
        artifacts.append(artifact)
        click.echo(f"  Loaded: {file_path}")

    # Merge artifacts
    try:
        merged = merge_coverage_artifacts(artifacts)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    # Write merged artifact
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w") as f:
            json.dump(merged, f, indent=2)
        click.echo(f"Successfully merged {len(artifacts)} artifact(s) to {output_path}")
        click.echo(
            f"  Requirements: {len(merged['all_requirements'])} total, "
            f"{len(merged['requirement_coverage'])} covered, "
            f"{len(merged['untested_requirements'])} untested",
        )
    except OSError as e:
        click.echo(f"Error: Failed to write output file: {e}", err=True)
        sys.exit(1)
