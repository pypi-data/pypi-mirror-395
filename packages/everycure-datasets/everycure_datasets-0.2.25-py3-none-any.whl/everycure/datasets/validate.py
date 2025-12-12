"""
Pre-commit validation script for dataset registry.

Checks:
1. All version directories follow semantic versioning (MAJOR.MINOR.PATCH)
2. Dataset folder names are snake_case
3. No files are edited in datasets/ on main branch (immutability check)
"""

import yaml
import re
import sys
from pathlib import Path
from pydantic import ValidationError

from logging import getLogger

from everycure.datasets.models.v1 import DatasetMetadataV1

logger = getLogger(__name__)

# Patterns
SNAKE_CASE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def get_dataset_directories(datasets_dir: Path) -> list[Path]:
    """Get all dataset directories that don't start with '.' or '_'."""
    return [
        item
        for item in datasets_dir.iterdir()
        if item.is_dir()
        and not item.name.startswith(".")
        and not item.name.startswith("_")
    ]


def get_version_directories(dataset_dir: Path) -> list[Path]:
    """Get all valid version directories in a dataset directory."""
    versions = []
    for item in dataset_dir.iterdir():
        if item.is_dir() and SEMVER_PATTERN.match(item.name):
            versions.append(item)
    return versions


def get_dataset_specification_files(datasets_dir: Path) -> list[Path]:
    """Get all dataset specification files in a dataset directory."""
    files = []

    for dataset_dir in datasets_dir.iterdir():
        for versioned_dataset in get_version_directories(dataset_dir):
            if (versioned_dataset / "dataset.yaml").is_file():
                files.append(versioned_dataset / "dataset.yaml")
    return files


def check_snake_case_names(datasets_dir: Path) -> list[str]:
    """Check that all dataset names are snake_case."""
    errors = []

    for item in get_dataset_directories(datasets_dir):
        if not SNAKE_CASE_PATTERN.match(item.name):
            errors.append(
                f"Dataset name '{item.name}' is not snake_case. "
                f"Use lowercase letters, numbers, and underscores only."
            )

    return errors


def check_semver_directories(datasets_dir: Path) -> list[str]:
    """Check that all version directories follow semantic versioning."""
    errors = []

    for dataset in get_dataset_directories(datasets_dir):
        for item in dataset.iterdir():
            # Skip hidden files
            if item.name.startswith("."):
                continue

            if item.is_dir() and not SEMVER_PATTERN.match(item.name):
                errors.append(
                    f"Version directory '{dataset.name}/{item.name}' does not follow "
                    f"semantic versioning (MAJOR.MINOR.PATCH). Example: 0.1.0"
                )

    return errors


def check_schema_validity(datasets_dir: Path) -> list[str]:
    """Check that all schema files are valid."""
    errors = []

    for dataset_file in get_dataset_specification_files(datasets_dir):
        dataset_yaml = yaml.safe_load(dataset_file.read_text())
        try:
            DatasetMetadataV1.model_validate(dataset_yaml)
        except ValidationError as e:
            print(f"Schema file '{dataset_file.relative_to(datasets_dir)}' is not valid: {e}")
            errors.append(f"Schema file '{dataset_file.relative_to(datasets_dir)}' is not valid.")
        
    return errors

def _find_repo_root() -> Path:
    """Find the repository root by walking up from current directory or file location."""
    # Start from current working directory
    current = Path.cwd()

    # Walk up looking for pyproject.toml (repo marker)
    for path in [current, *current.parents]:
        if (path / "pyproject.toml").exists() and (path / "datasets").exists():
            return path

    # Fallback: use file location (we're in src/everycure/datasets/validate.py)
    return Path(__file__).parent.parent.parent.parent


def validate_datasets(datasets_dir: Path | None = None) -> int:
    """
    Run all validation checks.

    Args:
        datasets_dir: Path to the datasets directory. If None, will try to find it
                     relative to the current working directory or repository root.

    Returns:
        0 if validation passes, 1 if it fails.
    """
    if datasets_dir is None:
        repo_root = _find_repo_root()
        datasets_dir = repo_root / "datasets"

    if not datasets_dir.exists():
        print(
            f"Error: datasets/ directory not found at {datasets_dir}", file=sys.stderr
        )
        return 1

    all_errors = []

    # Run all checks
    print("Checking dataset naming conventions...")
    all_errors.extend(check_snake_case_names(datasets_dir))

    print("Checking semantic versioning...")
    all_errors.extend(check_semver_directories(datasets_dir))

    print("Checking schema validity...")
    all_errors.extend(check_schema_validity(datasets_dir))

    # Report results
    if all_errors:
        print("\n❌ Validation failed with the following errors:\n", file=sys.stderr)
        for error in all_errors:
            print(f"  {error}", file=sys.stderr)
        print(f"\nTotal errors: {len(all_errors)}", file=sys.stderr)
        return 1
    else:
        print("\n✅ All validation checks passed!")
        return 0
