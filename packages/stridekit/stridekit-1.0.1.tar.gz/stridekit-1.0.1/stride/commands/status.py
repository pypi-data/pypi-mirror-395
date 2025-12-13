"""
Implementation of 'stride status' command.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ..core.sprint_manager import SprintManager
from ..constants import SprintStatus
from ..utils import (
    create_progress_text, format_timestamp_relative, 
    colorize_status, truncate_text, format_checkbox
)

console = Console()

def status(
    sprint_id: str = typer.Argument(None, help="ID of the sprint to check (optional)"),
):
    """
    Show the current status of the project or a specific sprint with detailed progress.
    """
    manager = SprintManager()

    if sprint_id:
        _show_sprint_status(manager, sprint_id)
    else:
        _show_project_status(manager)


def _show_sprint_status(manager: SprintManager, sprint_id: str):
    """Display detailed status for a specific sprint."""
    sprint = manager.get_sprint_details(sprint_id)
    
    if not sprint:
        console.print(f"[red]Sprint '{sprint_id}' not found.[/red]")
        raise typer.Exit(code=1)
    
    # Header
    status_colored = colorize_status(sprint.status.value)
    
    header_text = f"[bold cyan]{sprint.id}[/bold cyan] - {sprint.title}\n"
    header_text += f"[bold]Status:[/bold] {status_colored}\n"
    header_text += f"[dim]Updated {format_timestamp_relative(sprint.updated_at)}[/dim]"
    
    console.print(Panel(header_text, border_style="blue", title="[bold]Sprint Status[/bold]"))
    console.print()
    
    # Progress Overview
    if sprint.progress:
        _show_sprint_progress_summary(sprint)
        console.print()
        
        # Current Stride
        if sprint.progress.current_stride:
            _show_current_stride(sprint.progress.current_stride)
            console.print()
        else:
            console.print("[green]✓[/green] [bold]All strides completed![/bold]\n")
        
        # Next Steps
        _show_next_steps(sprint)
    else:
        console.print("[dim]No progress data available for this sprint.[/dim]\n")
    
    # Recent Activity
    if sprint.recent_logs:
        _show_recent_changes(sprint)


def _show_sprint_progress_summary(sprint):
    """Show overall progress metrics."""
    progress = sprint.progress
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Metric", style="bold")
    table.add_column("Progress")
    table.add_column("Count", justify="right")
    
    # Tasks
    tasks_progress = create_progress_text(
        progress.completed_tasks,
        progress.total_tasks,
        show_bar=True,
        bar_width=20
    )
    table.add_row(
        "Tasks",
        tasks_progress,
        f"{progress.completed_tasks}/{progress.total_tasks}"
    )
    
    # Acceptance Criteria
    ac_progress = create_progress_text(
        progress.acceptance_criteria_completed,
        progress.acceptance_criteria_total,
        show_bar=True,
        bar_width=20
    )
    table.add_row(
        "Acceptance Criteria",
        ac_progress,
        f"{progress.acceptance_criteria_completed}/{progress.acceptance_criteria_total}"
    )
    
    # Strides
    total_strides = len(progress.strides)
    completed_strides = sum(1 for s in progress.strides 
                           if s.completed_tasks == s.total_tasks and s.total_tasks > 0)
    strides_progress = create_progress_text(
        completed_strides,
        total_strides,
        show_bar=True,
        bar_width=20
    )
    table.add_row(
        "Strides",
        strides_progress,
        f"{completed_strides}/{total_strides}"
    )
    
    console.print(Panel(table, border_style="green", title="[bold]Progress Summary[/bold]"))


def _show_current_stride(stride):
    """Show details of the current stride being worked on."""
    header = f"[bold yellow]→ Stride {stride.stride_number}: {stride.stride_name}[/bold yellow]"
    console.print(header)
    
    if stride.purpose:
        console.print(f"[dim]Purpose: {stride.purpose}[/dim]")
    
    console.print()
    
    # Show tasks
    if stride.tasks:
        console.print("[bold]Remaining Tasks:[/bold]")
        for task in stride.tasks:
            if not task.checked:
                console.print(f"  {format_checkbox(False)} {task.text}")
        
        completed_count = sum(1 for t in stride.tasks if t.checked)
        if completed_count > 0:
            console.print(f"\n[dim]Completed: {completed_count}/{len(stride.tasks)} tasks[/dim]")
    else:
        console.print("[dim]No tasks defined for this stride.[/dim]")


def _show_next_steps(sprint):
    """Suggest next steps based on sprint status."""
    console.print("[bold]Next Steps:[/bold]")
    
    if sprint.progress:
        # Find incomplete acceptance criteria
        incomplete_ac = [ac for ac in sprint.acceptance_criteria if not ac.checked]
        
        if incomplete_ac:
            console.print(f"  • Complete remaining acceptance criteria ({len(incomplete_ac)} pending)")
        
        # Check current stride
        if sprint.progress.current_stride:
            incomplete_tasks = [t for t in sprint.progress.current_stride.tasks if not t.checked]
            if incomplete_tasks:
                console.print(f"  • Work on {len(incomplete_tasks)} remaining task(s) in current stride")
        
        # Check if all done
        if (sprint.progress.completed_tasks == sprint.progress.total_tasks and 
            sprint.progress.total_tasks > 0 and
            sprint.status != SprintStatus.COMPLETED):
            console.print("  • [green]All tasks complete! Consider running validation and closing sprint.[/green]")
    else:
        console.print("  • [dim]Define tasks in plan.md to track progress[/dim]")


def _show_recent_changes(sprint):
    """Show recent implementation activity."""
    console.print("\n[bold]Recent Activity:[/bold]")
    
    # Show most recent log entry
    if sprint.recent_logs:
        latest = sprint.recent_logs[0]
        
        console.print(f"  [bold]{latest.timestamp}[/bold] - {latest.stride_name}")
        
        if latest.tasks_addressed:
            console.print(f"  [yellow]Tasks:[/yellow] {', '.join(latest.tasks_addressed[:2])}")
        
        if latest.changes:
            console.print(f"  [green]Changes:[/green] {len(latest.changes)} file(s) modified")
            for change in latest.changes[:3]:
                console.print(f"    • {truncate_text(change, 70)}")
        
        if len(sprint.recent_logs) > 1:
            console.print(f"\n  [dim]... {len(sprint.recent_logs) - 1} earlier log entries[/dim]")


def _show_project_status(manager: SprintManager):
    """Display overall project status."""
    sprints = manager.list_sprints()
    
    if not sprints:
        console.print("[yellow]No sprints found in this project.[/yellow]")
        console.print("[dim]Run 'stride init' to create your first sprint.[/dim]")
        return
    
    # Count by status
    active = [s for s in sprints if s.status == SprintStatus.ACTIVE]
    proposed = [s for s in sprints if s.status == SprintStatus.PROPOSED]
    review = [s for s in sprints if s.status == SprintStatus.REVIEW]
    completed = [s for s in sprints if s.status == SprintStatus.COMPLETED]
    
    # Header
    console.print(Panel(
        f"[bold]Total Sprints:[/bold] {len(sprints)}",
        border_style="blue",
        title="[bold]Project Status[/bold]"
    ))
    console.print()
    
    # Status breakdown
    table = Table(show_header=True, box=None)
    table.add_column("Status", style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Sprint IDs", style="dim")
    
    if proposed:
        ids = ", ".join([s.id for s in proposed[:3]])
        if len(proposed) > 3:
            ids += f" (+{len(proposed) - 3} more)"
        table.add_row(colorize_status("proposed"), str(len(proposed)), ids)
    
    if active:
        ids = ", ".join([s.id for s in active[:3]])
        if len(active) > 3:
            ids += f" (+{len(active) - 3} more)"
        table.add_row(colorize_status("active"), str(len(active)), ids)
    
    if review:
        ids = ", ".join([s.id for s in review[:3]])
        if len(review) > 3:
            ids += f" (+{len(review) - 3} more)"
        table.add_row(colorize_status("review"), str(len(review)), ids)
    
    if completed:
        ids = ", ".join([s.id for s in completed[:3]])
        if len(completed) > 3:
            ids += f" (+{len(completed) - 3} more)"
        table.add_row(colorize_status("completed"), str(len(completed)), ids)
    
    console.print(table)
    console.print()
    
    # Active sprints detail
    if active:
        console.print("[bold]Active Sprint Details:[/bold]\n")
        
        for sprint in active[:3]:  # Show up to 3 active sprints
            detailed = manager.get_sprint_details(sprint.id)
            if detailed and detailed.progress:
                progress_text = create_progress_text(
                    detailed.progress.completed_tasks,
                    detailed.progress.total_tasks,
                    show_bar=True,
                    bar_width=15
                )
                
                current_stride = detailed.progress.current_stride
                stride_info = f"Stride {current_stride.stride_number}" if current_stride else "Complete"
                
                console.print(f"  [cyan]{sprint.id}[/cyan] - {truncate_text(detailed.title, 40)}")
                console.print(f"    Progress: {progress_text}")
                console.print(f"    Current: {stride_info}")
                console.print()
        
        if len(active) > 3:
            console.print(f"  [dim]... and {len(active) - 3} more active sprint(s)[/dim]\n")
    
    # Summary tips
    console.print("[dim]Tip: Use 'stride status <sprint-id>' for detailed sprint status[/dim]")
    console.print("[dim]Tip: Use 'stride list -v' for comprehensive sprint list[/dim]")
