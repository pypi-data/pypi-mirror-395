"""
Configuration management for Stride.
Handles reading/writing .stride/config.yaml and environment variables.

Note: Currently returns empty config. Configuration is managed through
.stride directory structure and agent-specific files.
"""

from typing import Any, Dict


def get_config() -> Dict[str, Any]:
    """
    Retrieve current configuration.

    Returns:
        Empty dict (configuration managed via .stride directory)
    """
    return {}
