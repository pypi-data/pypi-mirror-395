"""Resource queue names for Workflow Node specification which specify different resource needs."""

from enum import StrEnum


class ResourceQueue(StrEnum):
    """Supported queue names."""

    DEFAULT: str = "default"
    HIGH_MEMORY: str = "high_memory"
