"""
Markdown templates for sprint documents.

Templates are loaded directly from sprint_files/, agent_commands/, and agents_docs/
directories during init command execution. This module provides the TEMPLATE_DIR
constant for reference.
"""

from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent


def get_template(name: str) -> str:
    """
    Retrieve the content of a template by name.

    Note: Currently unused. Templates are loaded directly via Path.read_text()
    in the init command and SprintManager.

    Args:
        name: Template filename

    Returns:
        Empty string (templates loaded directly in commands)
    """
    return ""
