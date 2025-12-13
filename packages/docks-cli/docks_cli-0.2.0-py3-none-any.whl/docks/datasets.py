"""Dataset aliases and utilities for the Docks CLI.

This module provides friendly aliases for GCS dataset URIs,
so users don't need to remember full gs:// paths.

Convention:
- Any name like "calcom" resolves to gs://izumi-harbor-datasets/calcom
- Explicit aliases below provide additional shortcuts (swebench → swebench-lite, etc.)
- Users never need to know gs:// URIs
"""

import subprocess
import logging

logger = logging.getLogger(__name__)

# Default GCS bucket for datasets
DEFAULT_BUCKET = "gs://izumi-harbor-datasets"

# Explicit aliases mapping friendly names to canonical dataset names
# These are ONLY for shortcuts where the alias differs from folder name
# Any folder name in the bucket works automatically via dynamic resolution
DATASET_ALIASES = {
    # SWE-bench shortcut (swe-bench → swebench-lite folder)
    "swe-bench": "swebench-lite",

    # Go benchmark aliases
    "go-gin": "bench-go-gin",
    "gin": "bench-go-gin",

    # Dev-docks aliases (maps short form to folder name)
    "calcom": "dev-docks-calcom",
    "cal.com": "dev-docks-calcom",
}


def resolve_dataset_uri(dataset: str) -> str:
    """Resolve a dataset name or alias to its full GCS URI.

    Args:
        dataset: Dataset alias (e.g., "swebench") or full GCS URI

    Returns:
        Full GCS URI (gs://bucket/path)

    Examples:
        >>> resolve_dataset_uri("swebench")
        'gs://izumi-harbor-datasets/swebench'

        >>> resolve_dataset_uri("gs://custom/path")
        'gs://custom/path'
    """
    # If it's already a GCS URI, return as-is
    if dataset.startswith("gs://"):
        return dataset

    # Normalize to lowercase for matching
    normalized = dataset.lower().strip()

    # Check explicit aliases first
    if normalized in DATASET_ALIASES:
        folder_name = DATASET_ALIASES[normalized]
        return f"{DEFAULT_BUCKET}/{folder_name}"

    # Convention: any name resolves to gs://izumi-harbor-datasets/<name>
    # This allows users to use just "calcom" without knowing the bucket
    return f"{DEFAULT_BUCKET}/{normalized}"


def discover_datasets_from_bucket() -> list[str]:
    """Discover available datasets from GCS bucket.

    Returns:
        List of dataset folder names in the bucket
    """
    try:
        result = subprocess.run(
            ["gsutil", "ls", f"{DEFAULT_BUCKET}/"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            logger.warning(f"Failed to list GCS bucket: {result.stderr}")
            return []

        # Parse folder names from gsutil output
        # Format: gs://bucket/folder/
        datasets = []
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if line and line.startswith(DEFAULT_BUCKET):
                # Extract folder name from gs://bucket/folder/
                folder = line.replace(f"{DEFAULT_BUCKET}/", "").rstrip("/")
                if folder:
                    datasets.append(folder)
        return sorted(datasets)
    except subprocess.TimeoutExpired:
        logger.warning("Timeout listing GCS bucket")
        return []
    except FileNotFoundError:
        logger.warning("gsutil not found - cannot discover datasets")
        return []
    except Exception as e:
        logger.warning(f"Error discovering datasets: {e}")
        return []


def list_available_datasets(include_discovered: bool = True) -> dict[str, str]:
    """Return all available datasets with their URIs.

    Args:
        include_discovered: If True, also query GCS bucket for available datasets

    Returns:
        Dict mapping dataset names to their full GCS URIs
    """
    # Start with explicit aliases
    result = {}
    for alias, folder in DATASET_ALIASES.items():
        result[alias] = f"{DEFAULT_BUCKET}/{folder}"

    # Optionally discover datasets from bucket
    if include_discovered:
        discovered = discover_datasets_from_bucket()
        for folder in discovered:
            # Add if not already covered by an alias
            if folder not in result:
                result[folder] = f"{DEFAULT_BUCKET}/{folder}"

    return result
