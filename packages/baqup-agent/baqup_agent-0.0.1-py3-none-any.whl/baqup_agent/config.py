"""
Configuration loading for baqup agents.

This module wraps baqup-schema for convenient agent configuration loading.
"""

from typing import Any

_PLACEHOLDER_MESSAGE = (
    "baqup-agent is currently a placeholder package. "
    "Full implementation coming soon. "
    "See https://github.com/baqupio/baqup for updates."
)


def load_config(schema_path: str) -> dict[str, Any]:
    """
    Load agent configuration from environment variables.

    Uses baqup-schema to validate against the provided schema.

    Args:
        schema_path: Path to the agent's JSON Schema file

    Returns:
        Validated configuration dict

    Raises:
        NotImplementedError: This is a placeholder package
    """
    raise NotImplementedError(_PLACEHOLDER_MESSAGE)
