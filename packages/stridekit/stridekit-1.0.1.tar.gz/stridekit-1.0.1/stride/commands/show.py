"""
Implementation of 'stride show' command.
"""

import typer
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from ..core.sprint_manager import SprintManager
from ..constants import (
    FILE_PROPOSAL, FILE_PLAN, FILE_DESIGN, FILE_IMPLEMENTATION, FILE_RETROSPECTIVE,
    MAX_TASK_DISPLAY, MAX_LOG_ENTRIES
)
from ..utils import (
    create_progress_text, format_timestamp_relative, 
    format_checkbox, colorize_status, truncate_text
)

console = Console()

def show(
    sprint_id: str = typer.Argument(..., help="ID of the sprint to show"),
    file: str = typer.Option(None, help="Specific file to display (proposal, plan, design, implementation, retrospective)"),
    tasks: bool = typer.Option(False, "--tasks", help="Focus on task list view"),
    timeline: bool = typer.Option(False, "--timeline", help="Show chronological implementation timeline"),
    acceptance: bool = typer.Option(False, "--acceptance", help="Focus on acceptance criteria tracking"),
    full: bool = typer.Option(False, "--full", help="Show all content including full logs"),
):
    """
    Show details and content of a specific sprint with smart overview.
    """
    manager = SprintManager()
    
    # Load sprint with full details
    sprint = manager.get_sprint_details(sprint_id)

    if not sprint:
        console.print(f"[red]Sprint '{sprint_id}' not found.[/red]")
        raise typer.Exit(code=1)

    sprint_path = Path(sprint.path)
    
    files_map = {
        "proposal": FILE_PROPOSAL,
        "plan": FILE_PLAN,
        "design": FILE_DESIGN,
        "implementation": FILE_IMPLEMENTATION,
        "retrospective": FILE_RETROSPECTIVE
    }

    # If specific file requested, show that file
    if file:
        if file not in files_map:
            console.print(f"[red]Invalid file type. Choose from: {', '.join(files_map.keys())}[/red]")
            raise typer.Exit(code=1)
        
        target_file = sprint_path / files_map[file]
        if target_file.exists():
            content = target_file.read_text(encoding="utf-8")
            console.print(Panel(Markdown(content), title=f"{sprint_id} / {files_map[file]}", border_style="blue"))
        else:
            console.print(f"[yellow]File {files_map[file]} does not exist for this sprint.[/yellow]")
        return
    
    # === SMART DEFAULT VIEW ===
    
    # 1. Header Panel
    _show_header(sprint)
    
    # 2. Focus views
    if acceptance:
        _show_acceptance_criteria(sprint)
    elif tasks:
        _show_tasks_view(sprint)
    elif timeline:
        _show_timeline_view(sprint, full)
    else:
        # Default comprehensive view
        console.print()
        
        if sprint.progress and sprint.progress.acceptance_criteria_total > 0:
            _show_acceptance_criteria(sprint)
            console.print()
        
        if sprint.progress and sprint.progress.strides:
            _show_strides_progress(sprint)
            console.print()
        
        if sprint.recent_logs:
            _show_recent_activity(sprint, full)
            console.print()
        
        _show_files_summary(sprint_path, files_map)


def _show_header(sprint):
    """Display sprint header with metadata."""
    # Create header content
    status_colored = colorize_status(sprint.status.value)
    
    header_lines = [
        f"[bold cyan]Sprint:[/bold cyan] {sprint.id}",
        f"[bold]Title:[/bold] {sprint.title}",
        f"[bold]Status:[/bold] {status_colored}",
    ]
    
    # Add progress if available
    if sprint.progress and sprint.progress.total_tasks > 0:
        progress_text = create_progress_text(
            sprint.progress.completed_tasks,
            sprint.progress.total_tasks,
            show_bar=True,
            bar_width=30
        )
        header_lines.append(f"[bold]Overall Progress:[/bold] {progress_text}")
        header_lines.append(f"[dim]Tasks: {sprint.progress.completed_tasks}/{sprint.progress.total_tasks} | " +
                           f"Acceptance Criteria: {sprint.progress.acceptance_criteria_completed}/{sprint.progress.acceptance_criteria_total}[/dim]")
    
    # Add dates
    header_lines.append(f"[dim]Created: {sprint.created_at.strftime('%Y-%m-%d %H:%M')} | " +
                       f"Updated: {format_timestamp_relative(sprint.updated_at)}[/dim]")
    
    console.print(Panel(
        "\n".join(header_lines),
        border_style="blue",
        title="[bold]Sprint Overview[/bold]"
    ))


def _show_acceptance_criteria(sprint):
    """Display acceptance criteria with completion status."""
    if not sprint.acceptance_criteria:
        console.print("[dim]No acceptance criteria defined.[/dim]")
        return
    
    from ..core.markdown_parser import MarkdownParser
    
    # Try to read proposal and group by category
    sprint_path = Path(sprint.path)
    proposal_path = sprint_path / FILE_PROPOSAL
    
    if proposal_path.exists():
        content = proposal_path.read_text(encoding='utf-8')
        section = MarkdownParser.extract_section(content, "Acceptance Criteria", level=2)
        grouped = MarkdownParser.group_checkboxes_by_category(section)
        
        if grouped:
            table = Table(title="Acceptance Criteria", show_header=False, box=None)
            table.add_column("Status", width=3)
            table.add_column("Criteria")
            
            for category, items in grouped.items():
                if items:
                    # Category header
                    table.add_row("", f"[bold yellow]{category}[/bold yellow]")
                    
                    # Items
                    for item in items:
                        checkbox = format_checkbox(item.checked)
                        table.add_row(checkbox, item.text)
                    
                    # Spacer
                    table.add_row("", "")
            
            console.print(Panel(table, border_style="yellow", title="[bold]Acceptance Criteria[/bold]"))
            
            # Summary
            completed, total, percentage = MarkdownParser.calculate_completion(sprint.acceptance_criteria)
            console.print(f"[dim]Completion: {completed}/{total} ({percentage:.0f}%)[/dim]")
        else:
            _show_simple_acceptance_criteria(sprint)
    else:
        _show_simple_acceptance_criteria(sprint)


def _show_simple_acceptance_criteria(sprint):
    """Simple acceptance criteria view without categories."""
    table = Table(title="Acceptance Criteria", show_header=False, box=None)
    table.add_column("Status", width=3)
    table.add_column("Criteria")
    
    for item in sprint.acceptance_criteria[:MAX_TASK_DISPLAY]:
        checkbox = format_checkbox(item.checked)
        table.add_row(checkbox, item.text)
    
    remaining = len(sprint.acceptance_criteria) - MAX_TASK_DISPLAY
    if remaining > 0:
        table.add_row("", f"[dim]... and {remaining} more[/dim]")
    
    console.print(Panel(table, border_style="yellow"))


def _show_strides_progress(sprint):
    """Display strides with task progress."""
    if not sprint.progress or not sprint.progress.strides:
        console.print("[dim]No strides defined.[/dim]")
        return
    
    table = Table(title="Strides Progress", show_lines=True)
    table.add_column("Stride", style="cyan", no_wrap=True)
    table.add_column("Progress", justify="left")
    table.add_column("Tasks", style="bold")
    table.add_column("Purpose", style="dim")
    
    for stride in sprint.progress.strides:
        stride_name = f"Stride {stride.stride_number}"
        
        # Check if this is the current stride
        if sprint.progress.current_stride and stride.stride_number == sprint.progress.current_stride.stride_number:
            stride_name = f"[bold yellow]→ {stride_name}[/bold yellow]"
        
        # Progress bar
        if stride.total_tasks > 0:
            progress_text = create_progress_text(
                stride.completed_tasks,
                stride.total_tasks,
                show_bar=True,
                bar_width=20
            )
            tasks_text = f"{stride.completed_tasks}/{stride.total_tasks}"
        else:
            progress_text = "[dim]No tasks[/dim]"
            tasks_text = "0/0"
        
        # Truncate purpose
        purpose = truncate_text(stride.purpose, 60) if stride.purpose else "[dim]N/A[/dim]"
        
        table.add_row(stride_name, progress_text, tasks_text, purpose)
    
    console.print(Panel(table, border_style="blue", title="[bold]Strides[/bold]"))


def _show_tasks_view(sprint):
    """Show detailed task view for all strides."""
    if not sprint.progress or not sprint.progress.strides:
        console.print("[dim]No tasks found.[/dim]")
        return
    
    console.print(Panel("[bold]Task Details[/bold]", border_style="cyan"))
    
    for stride in sprint.progress.strides:
        console.print(f"\n[bold cyan]Stride {stride.stride_number}: {stride.stride_name}[/bold cyan]")
        
        if stride.tasks:
            for task in stride.tasks:
                checkbox = format_checkbox(task.checked)
                console.print(f"  {checkbox} {task.text}")
        else:
            console.print("  [dim]No tasks defined[/dim]")


def _show_recent_activity(sprint, show_full: bool = False):
    """Display recent implementation log entries."""
    if not sprint.recent_logs:
        console.print("[dim]No implementation activity yet.[/dim]")
        return
    
    logs_to_show = sprint.recent_logs if show_full else sprint.recent_logs[:3]
    
    for log in logs_to_show:
        # Entry header
        console.print(f"[bold]Timestamp:[/bold] {log.timestamp} | [bold]Stride:[/bold] {log.stride_name}")
        
        # Tasks addressed
        if log.tasks_addressed:
            console.print("  [yellow]Tasks:[/yellow]")
            for task in log.tasks_addressed[:3]:
                console.print(f"    • {task}")
        
        # Key decisions
        if log.decisions:
            console.print("  [cyan]Decisions:[/cyan]")
            for decision in log.decisions[:2]:
                console.print(f"    • {truncate_text(decision, 80)}")
        
        # Changes
        if log.changes:
            console.print("  [green]Changes:[/green]")
            for change in log.changes[:3]:
                console.print(f"    • {truncate_text(change, 80)}")
        
        console.print()
    
    if not show_full and len(sprint.recent_logs) > 3:
        console.print(f"[dim]... {len(sprint.recent_logs) - 3} more entries (use --full to see all)[/dim]")


def _show_timeline_view(sprint, show_full: bool = False):
    """Show chronological timeline of all implementation activity."""
    if not sprint.recent_logs:
        console.print("[dim]No implementation activity yet.[/dim]")
        return
    
    console.print(Panel("[bold]Implementation Timeline[/bold]", border_style="green"))
    
    logs = sprint.recent_logs if show_full else sprint.recent_logs[:MAX_LOG_ENTRIES]
    
    for i, log in enumerate(logs):
        marker = "●" if i == 0 else "○"
        console.print(f"\n[bold]{marker}[/bold] [bold]{log.timestamp}[/bold] - {log.stride_name}")
        
        if log.tasks_addressed:
            console.print(f"   [dim]Tasks: {', '.join(log.tasks_addressed[:2])}{' ...' if len(log.tasks_addressed) > 2 else ''}[/dim]")
        
        if log.changes:
            console.print(f"   [dim]Files: {len(log.changes)} changed[/dim]")
    
    if not show_full and len(sprint.recent_logs) > MAX_LOG_ENTRIES:
        console.print(f"\n[dim]... {len(sprint.recent_logs) - MAX_LOG_ENTRIES} earlier entries (use --full to see all)[/dim]")


def _show_files_summary(sprint_path: Path, files_map: dict):
    """Show which sprint files exist."""
    table = Table(title="Sprint Files", show_header=False, box=None)
    table.add_column("Status", width=3)
    table.add_column("File")
    table.add_column("Size", justify="right", style="dim")
    
    for name, filename in files_map.items():
        path = sprint_path / filename
        if path.exists():
            status = "[green]✓[/green]"
            size = path.stat().st_size
            size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
        else:
            status = "[dim]○[/dim]"
            size_str = "[dim]missing[/dim]"
        
        table.add_row(status, filename, size_str)
    
    console.print(Panel(table, border_style="dim", title="[bold]Files[/bold]"))
    console.print(f"\n[dim]Tip: Use 'stride show {sprint_path.name} --file <name>' to view a specific file[/dim]")
