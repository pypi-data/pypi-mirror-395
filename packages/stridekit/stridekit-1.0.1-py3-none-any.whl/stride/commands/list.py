"""
Implementation of 'stride list' command.
"""

import typer
from rich.console import Console
from rich.table import Table
from ..constants import (
    SprintStatus, COLOR_PROPOSED, COLOR_ACTIVE, COLOR_COMPLETED, COLOR_REVIEW,
    MAX_TITLE_LENGTH, PROGRESS_BAR_WIDTH, VERBOSE_PROGRESS_BAR_WIDTH
)
from ..core.sprint_manager import SprintManager
from ..utils import create_progress_text, truncate_text, format_timestamp_relative

console = Console()

def list_sprints(
    status: SprintStatus = typer.Option(None, help="Filter by sprint status"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
):
    """
    List all sprints in the project with progress indicators.
    """
    manager = SprintManager()
    sprints = manager.list_sprints()

    if status:
        sprints = [s for s in sprints if s.status == status]

    if not sprints:
        console.print("[yellow]No sprints found.[/yellow]")
        return

    # Load progress data for each sprint
    detailed_sprints = []
    for sprint in sprints:
        detailed = manager.get_sprint(sprint.id, include_progress=True)
        if detailed:
            detailed_sprints.append(detailed)

    status_colors = {
        SprintStatus.PROPOSED: COLOR_PROPOSED,
        SprintStatus.ACTIVE: COLOR_ACTIVE,
        SprintStatus.REVIEW: COLOR_REVIEW,
        SprintStatus.COMPLETED: COLOR_COMPLETED,
    }

    if verbose:
        # Verbose mode with more columns
        table = Table(title="Stride Sprints", show_lines=True)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="bold")
        table.add_column("Status", style="bold", no_wrap=True)
        table.add_column("Progress", justify="left")
        table.add_column("Tasks", justify="center")
        table.add_column("Strides", justify="center")
        table.add_column("Current Stride", style="dim")
        table.add_column("Updated", style="dim", no_wrap=True)

        for sprint in detailed_sprints:
            color = status_colors.get(sprint.status, "white")
            status_text = f"[{color}]{sprint.status.value.upper()}[/{color}]"
            
            # Title (truncated)
            title = truncate_text(sprint.title, MAX_TITLE_LENGTH)
            
            # Progress bar
            if sprint.progress and sprint.progress.total_tasks > 0:
                progress_text = create_progress_text(
                    sprint.progress.completed_tasks,
                    sprint.progress.total_tasks,
                    show_bar=True,
                    bar_width=VERBOSE_PROGRESS_BAR_WIDTH
                )
                tasks_text = f"{sprint.progress.completed_tasks}/{sprint.progress.total_tasks}"
                
                # Strides info
                total_strides = len(sprint.progress.strides)
                completed_strides = sum(1 for s in sprint.progress.strides 
                                       if s.completed_tasks == s.total_tasks and s.total_tasks > 0)
                strides_text = f"{completed_strides}/{total_strides}"
                
                # Current stride
                current = sprint.progress.current_stride
                current_text = truncate_text(current.stride_name, 30) if current else "[dim]None[/dim]"
            else:
                progress_text = "[dim]No tasks[/dim]"
                tasks_text = "0/0"
                strides_text = "0/0"
                current_text = "[dim]N/A[/dim]"
            
            # Last updated
            updated = format_timestamp_relative(sprint.updated_at)
            
            table.add_row(
                sprint.id,
                title,
                status_text,
                progress_text,
                tasks_text,
                strides_text,
                current_text,
                updated
            )
    else:
        # Compact mode
        table = Table(title="Stride Sprints")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="bold")
        table.add_column("Status", style="bold", no_wrap=True)
        table.add_column("Progress", justify="left")
        table.add_column("Tasks", justify="center", no_wrap=True)
        table.add_column("Updated", style="dim", no_wrap=True)

        for sprint in detailed_sprints:
            color = status_colors.get(sprint.status, "white")
            status_text = f"[{color}]{sprint.status.value.upper()}[/{color}]"
            
            # Title (truncated)
            title = truncate_text(sprint.title, MAX_TITLE_LENGTH)
            
            # Progress bar
            if sprint.progress and sprint.progress.total_tasks > 0:
                progress_text = create_progress_text(
                    sprint.progress.completed_tasks,
                    sprint.progress.total_tasks,
                    show_bar=True,
                    bar_width=PROGRESS_BAR_WIDTH
                )
                tasks_text = f"{sprint.progress.completed_tasks}/{sprint.progress.total_tasks}"
            else:
                progress_text = "[dim]No data[/dim]"
                tasks_text = "[dim]0/0[/dim]"
            
            # Last updated
            updated = format_timestamp_relative(sprint.updated_at)
            
            table.add_row(
                sprint.id,
                title,
                status_text,
                progress_text,
                tasks_text,
                updated
            )

    console.print(table)
    
    # Show summary
    total = len(detailed_sprints)
    if verbose and total > 0:
        console.print(f"\n[dim]Total: {total} sprint{'s' if total != 1 else ''}[/dim]")
        console.print(f"[dim]Tip: Use 'stride show <sprint-id>' for detailed view[/dim]")
