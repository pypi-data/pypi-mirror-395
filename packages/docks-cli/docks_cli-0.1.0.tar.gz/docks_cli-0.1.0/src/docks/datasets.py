"""Dataset aliases and utilities for the Docks CLI.

This module provides friendly aliases for GCS dataset URIs,
so users don't need to remember full gs:// paths.
"""

# Dataset aliases mapping friendly names to GCS URIs
# Users can use either the alias or the full URI

DATASET_ALIASES = {
    # SWE-bench datasets
    "swebench": "gs://izumi-harbor-datasets/swebench",
    "swe-bench": "gs://izumi-harbor-datasets/swebench",
    "swebench-lite": "gs://izumi-harbor-datasets/swebench",

    # Go benchmarks
    "go-gin": "gs://izumi-harbor-datasets/bench-go-gin",
    "gin": "gs://izumi-harbor-datasets/bench-go-gin",

    # Future datasets can be added here:
    # "terminal-bench": "gs://izumi-harbor-datasets/terminal-bench",
    # "enterprise-swe": "gs://izumi-harbor-datasets/enterprise-swe",
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

    if normalized in DATASET_ALIASES:
        return DATASET_ALIASES[normalized]

    # If not found, assume it might be a short form for our default bucket
    # This allows users to use just "swebench" without knowing the bucket
    return f"gs://izumi-harbor-datasets/{normalized}"


def list_available_datasets() -> dict[str, str]:
    """Return all available dataset aliases and their URIs."""
    return DATASET_ALIASES.copy()
