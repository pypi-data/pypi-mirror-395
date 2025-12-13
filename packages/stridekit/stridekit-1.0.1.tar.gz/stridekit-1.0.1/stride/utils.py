"""
Helper utilities for Stride CLI.
"""

import uuid
from datetime import datetime
from typing import List
from rich.text import Text


def generate_sprint_id() -> str:
    """
    Generate a unique sprint ID.

    Returns:
        Sprint ID in format: SPRINT-XXXXX (5 uppercase hex chars)
    """
    return f"SPRINT-{uuid.uuid4().hex[:5].upper()}"


def get_timestamp() -> str:
    """Get current timestamp formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def render_progress_bar(percentage: float, width: int = 20, show_percentage: bool = True) -> str:
    """
    Render a text-based progress bar.
    
    Args:
        percentage: Completion percentage (0-100)
        width: Width of the bar in characters
        show_percentage: Whether to show percentage text
        
    Returns:
        Formatted progress bar string
    """
    filled = int(width * percentage / 100)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    
    if show_percentage:
        return f"{bar} {percentage:.0f}%"
    return bar


def create_progress_text(completed: int, total: int, show_bar: bool = True, bar_width: int = 15) -> Text:
    """
    Create a Rich Text object with progress information.
    
    Args:
        completed: Number of completed items
        total: Total number of items
        show_bar: Whether to include a progress bar
        bar_width: Width of the progress bar
        
    Returns:
        Rich Text object
    """
    if total == 0:
        percentage = 0.0
    else:
        percentage = (completed / total) * 100
    
    text = Text()
    
    if show_bar:
        filled = int(bar_width * percentage / 100)
        empty = bar_width - filled
        
        # Color the bar based on completion
        if percentage == 100:
            bar_color = "green"
        elif percentage >= 50:
            bar_color = "yellow"
        else:
            bar_color = "red"
        
        text.append("█" * filled, style=bar_color)
        text.append("░" * empty, style="dim")
        text.append(" ")
    
    text.append(f"{completed}/{total}", style="bold")
    
    return text


def format_timestamp_relative(dt: datetime) -> str:
    """
    Format a datetime as a relative time string (e.g., '2 hours ago').
    
    Args:
        dt: Datetime to format
        
    Returns:
        Relative time string
    """
    now = datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return dt.strftime("%Y-%m-%d")


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_checkbox(checked: bool) -> str:
    """
    Format a checkbox as a visual indicator.
    
    Args:
        checked: Whether the checkbox is checked
        
    Returns:
        Formatted checkbox string
    """
    return "[green]✓[/green]" if checked else "[dim]○[/dim]"


def format_task_list(tasks: List, max_display: int = 5) -> List[str]:
    """
    Format a list of tasks for display.
    
    Args:
        tasks: List of task items with 'text' and 'checked' attributes
        max_display: Maximum number of tasks to display
        
    Returns:
        List of formatted task strings
    """
    formatted = []
    
    for i, task in enumerate(tasks[:max_display]):
        checkbox = format_checkbox(task.checked)
        formatted.append(f"{checkbox} {task.text}")
    
    remaining = len(tasks) - max_display
    if remaining > 0:
        formatted.append(f"[dim]... and {remaining} more[/dim]")
    
    return formatted


def colorize_status(status: str) -> str:
    """
    Add color formatting to a status string.
    
    Args:
        status: Status value
        
    Returns:
        Colored status string
    """
    from .constants import SprintStatus, COLOR_PROPOSED, COLOR_ACTIVE, COLOR_REVIEW, COLOR_COMPLETED
    
    status_lower = status.lower()
    
    if status_lower == SprintStatus.PROPOSED.value:
        return f"[{COLOR_PROPOSED}]{status.upper()}[/{COLOR_PROPOSED}]"
    elif status_lower == SprintStatus.ACTIVE.value:
        return f"[{COLOR_ACTIVE}]{status.upper()}[/{COLOR_ACTIVE}]"
    elif status_lower == SprintStatus.REVIEW.value:
        return f"[{COLOR_REVIEW}]{status.upper()}[/{COLOR_REVIEW}]"
    elif status_lower == SprintStatus.COMPLETED.value:
        return f"[{COLOR_COMPLETED}]{status.upper()}[/{COLOR_COMPLETED}]"
    else:
        return status.upper()
