"""
CLI command for displaying sprint metrics and analytics.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box
from ..core.analytics import get_metrics, get_cache_info, clear_analytics_cache

console = Console()


def metrics(
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show detailed metrics breakdown"),
    refresh: bool = typer.Option(False, "--refresh", "-r", help="Force refresh (ignore cache)"),
    clear_cache: bool = typer.Option(False, "--clear-cache", help="Clear analytics cache and exit"),
):
    """
    Display sprint metrics and analytics.
    
    Shows comprehensive metrics including:
    - Sprint counts and distribution
    - Duration analysis
    - Task completion rates
    - Process quality metrics
    - Historical trends
    - Health score
    """
    
    # Handle cache clearing
    if clear_cache:
        clear_analytics_cache()
        console.print("[green]✓ Analytics cache cleared.[/green]")
        return
    
    # Show loading message
    with console.status("[cyan]Calculating metrics...[/cyan]"):
        metrics_data = get_metrics(use_cache=not refresh, force_refresh=refresh)
    
    # Check if we have data
    if metrics_data["counts"]["total_sprints"] == 0:
        console.print("\n[yellow]⚠ No sprint data found.[/yellow]")
        console.print("[dim]Run 'stride init' in your AI agent to create your first sprint.[/dim]\n")
        return
    
    # Display metrics
    if detailed:
        display_detailed_metrics(metrics_data)
    else:
        display_summary_metrics(metrics_data)
    
    # Show cache info
    if not refresh:
        cache_info = get_cache_info()
        if cache_info:
            console.print(f"\n[dim]Cached data from {cache_info['cache_age']}. Use --refresh to recalculate.[/dim]")


def display_summary_metrics(data: dict):
    """Display summary metrics view."""
    
    counts = data["counts"]
    duration = data.get("duration", {})
    tasks = data["tasks"]
    quality = data["quality"]
    summary = data["summary"]
    trends = data.get("trends", {})
    
    # Header
    console.print()
    console.print("═" * 60, style="cyan")
    console.print("📊 SPRINT METRICS OVERVIEW", style="bold cyan", justify="center")
    console.print("═" * 60, style="cyan")
    console.print()
    
    # Sprint Overview Panel
    overview_content = f"""[bold]Total Sprints:[/bold] {counts['total_sprints']}
[green]✓ Active:[/green] {counts['active_sprints']}  [cyan]✓ Completed:[/cyan] {counts['completed_sprints']}  [red]✗ Abandoned:[/red] {counts['abandoned_sprints']}

[bold]Success Rate:[/bold] {counts['completion_rate']:.1f}%  |  [bold]Abandonment Rate:[/bold] {counts['abandonment_rate']:.1f}%"""
    
    overview_panel = Panel(
        overview_content,
        title="[bold cyan]Sprint Distribution[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(overview_panel)
    console.print()
    
    # Create two-column layout
    layout = Layout()
    layout.split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    
    # Performance Metrics Table (Left)
    perf_table = Table(title="⚡ Performance", box=box.SIMPLE, show_header=False, padding=(0, 2))
    perf_table.add_column("Metric", style="cyan", no_wrap=True)
    perf_table.add_column("Value", style="bold green")
    
    if duration.get("has_duration_data"):
        perf_table.add_row("Avg Duration", f"{duration['average_duration']:.1f} days")
    perf_table.add_row("Sprint Velocity", f"{tasks['sprint_velocity']:.1f} tasks/sprint")
    perf_table.add_row("Task Completion", f"{tasks['task_completion_rate']:.1f}%")
    
    # Quality Metrics Table (Right)
    quality_table = Table(title="✨ Quality", box=box.SIMPLE, show_header=False, padding=(0, 2))
    quality_table.add_column("Metric", style="cyan", no_wrap=True)
    quality_table.add_column("Value", style="bold green")
    
    quality_table.add_row("Planning Coverage", f"{quality['planning_coverage']:.0f}%")
    quality_table.add_row("Implementation Coverage", f"{quality['implementation_coverage']:.0f}%")
    quality_table.add_row("Retrospective Coverage", f"{quality['retrospective_coverage']:.0f}%")
    quality_table.add_row("Process Adoption", f"{quality['process_adoption_rate']:.0f}%")
    
    layout["left"].update(perf_table)
    layout["right"].update(quality_table)
    console.print(layout)
    console.print()
    
    # Health Score Panel
    health_score = summary["health_score"]
    health_color = _get_health_color(health_score)
    health_bar = _create_progress_bar(health_score, 50)
    
    health_content = f"""[bold]Health Score:[/bold] [{health_color}]{health_score}/100[/{health_color}]

{health_bar}

[bold]Productivity:[/bold] {summary['productivity_level'].capitalize()}  |  [bold]Process Maturity:[/bold] {summary['process_maturity'].capitalize()}
[bold]Overall Status:[/bold] [{health_color}]{summary['overall_status'].replace('_', ' ').title()}[/{health_color}]"""
    
    health_panel = Panel(
        health_content,
        title="[bold cyan]Project Health[/bold cyan]",
        border_style=health_color,
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(health_panel)
    
    # Trends (if available)
    if trends.get("has_trend_data"):
        console.print()
        trend_text = f"""[bold]Recent Activity:[/bold]
  Last 7 days: {trends['sprints_last_7_days']} sprints
  Last 30 days: {trends['sprints_last_30_days']} sprints
  
[bold]Velocity Trend:[/bold] {_format_trend(trends['velocity_trend'])}
[bold]Completion Trend:[/bold] {_format_trend(trends['completion_rate_trend'])}"""
        
        trend_panel = Panel(
            trend_text,
            title="[bold cyan]Trends[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        console.print(trend_panel)
    
    console.print()
    console.print("[dim]💡 Tip: Use --detailed for comprehensive metrics breakdown[/dim]")
    console.print()


def display_detailed_metrics(data: dict):
    """Display detailed metrics view."""
    
    counts = data["counts"]
    duration = data.get("duration", {})
    tasks = data["tasks"]
    quality = data["quality"]
    summary = data["summary"]
    trends = data.get("trends", {})
    
    # Header
    console.print()
    console.print("═" * 80, style="cyan")
    console.print("📊 DETAILED SPRINT ANALYTICS", style="bold cyan", justify="center")
    console.print("═" * 80, style="cyan")
    console.print()
    
    # Sprint Counts Table
    counts_table = Table(title="📈 Sprint Distribution", box=box.ROUNDED, show_header=True)
    counts_table.add_column("Status", style="cyan bold")
    counts_table.add_column("Count", justify="right", style="bold")
    counts_table.add_column("Percentage", justify="right")
    
    total = counts["total_sprints"]
    counts_table.add_row("Active", str(counts["active_sprints"]), f"{counts['active_ratio']:.1f}%")
    counts_table.add_row("Completed", str(counts["completed_sprints"]), f"{counts['completion_rate']:.1f}%")
    counts_table.add_row("Abandoned", str(counts["abandoned_sprints"]), f"{counts['abandonment_rate']:.1f}%")
    counts_table.add_row("Paused", str(counts["paused_sprints"]), f"{counts['paused_sprints']/total*100 if total > 0 else 0:.1f}%")
    counts_table.add_row("[bold]Total", f"[bold]{total}", "[bold]100%")
    
    console.print(counts_table)
    console.print()
    
    # Duration Analysis
    if duration.get("has_duration_data"):
        duration_table = Table(title="⏱️  Duration Analysis", box=box.ROUNDED)
        duration_table.add_column("Metric", style="cyan")
        duration_table.add_column("Value", justify="right", style="bold")
        
        duration_table.add_row("Average Duration", f"{duration['average_duration']:.2f} days")
        duration_table.add_row("Median Duration", f"{duration['median_duration']:.2f} days")
        duration_table.add_row("Shortest Sprint", f"{duration['min_duration']:.2f} days ({duration['fastest_sprint']})")
        duration_table.add_row("Longest Sprint", f"{duration['max_duration']:.2f} days ({duration['slowest_sprint']})")
        duration_table.add_row("Standard Deviation", f"{duration['std_dev']:.2f} days")
        duration_table.add_row("", "")
        duration_table.add_row("Under 3 days", f"{duration['durations_under_3_days']} sprints")
        duration_table.add_row("3-7 days", f"{duration['durations_3_to_7_days']} sprints")
        duration_table.add_row("Over 7 days", f"{duration['durations_over_7_days']} sprints")
        
        console.print(duration_table)
        console.print()
    
    # Task Metrics
    tasks_table = Table(title="✅ Task Metrics", box=box.ROUNDED)
    tasks_table.add_column("Metric", style="cyan")
    tasks_table.add_column("Value", justify="right", style="bold")
    
    tasks_table.add_row("Total Tasks", str(tasks["total_tasks"]))
    tasks_table.add_row("Completed Tasks", f"[green]{tasks['completed_tasks']}[/green]")
    tasks_table.add_row("Pending Tasks", f"[yellow]{tasks['pending_tasks']}[/yellow]")
    tasks_table.add_row("Completion Rate", f"{tasks['task_completion_rate']:.1f}%")
    tasks_table.add_row("", "")
    tasks_table.add_row("Avg Tasks per Sprint", f"{tasks['average_tasks_per_sprint']:.1f}")
    tasks_table.add_row("Sprint Velocity", f"{tasks['sprint_velocity']:.1f} tasks/sprint")
    
    console.print(tasks_table)
    console.print()
    
    # Quality Metrics
    quality_table = Table(title="⭐ Process Quality", box=box.ROUNDED)
    quality_table.add_column("Metric", style="cyan")
    quality_table.add_column("Coverage", justify="right", style="bold")
    
    quality_table.add_row("Planning Documents", f"{quality['sprints_with_planning']}/{total} ({quality['planning_coverage']:.0f}%)")
    quality_table.add_row("Implementation Tracking", f"{quality['sprints_with_implementation']}/{total} ({quality['implementation_coverage']:.0f}%)")
    quality_table.add_row("Retrospectives", f"{quality['sprints_with_retrospective']}/{total} ({quality['retrospective_coverage']:.0f}%)")
    quality_table.add_row("Design Documents", f"{quality['sprints_with_design']}/{total}")
    quality_table.add_row("Proposals", f"{quality['sprints_with_proposal']}/{total}")
    quality_table.add_row("", "")
    quality_table.add_row("[bold]Process Adoption", f"[bold]{quality['process_adoption_rate']:.0f}%")
    
    if quality['average_retrospective_length'] > 0:
        quality_table.add_row("Avg Retrospective Length", f"{quality['average_retrospective_length']:.0f} words")
        quality_table.add_row("Avg Learnings per Retro", f"{quality['average_learnings_count']:.1f}")
    
    console.print(quality_table)
    console.print()
    
    # Health Summary
    health_score = summary["health_score"]
    health_color = _get_health_color(health_score)
    
    summary_panel = Panel(
        f"""[bold]Health Score:[/bold] [{health_color}]{health_score}/100[/{health_color}]
[bold]Productivity Level:[/bold] {summary['productivity_level'].capitalize()}
[bold]Process Maturity:[/bold] {summary['process_maturity'].capitalize()}
[bold]Overall Status:[/bold] [{health_color}]{summary['overall_status'].replace('_', ' ').title()}[/{health_color}]""",
        title="[bold cyan]Overall Health[/bold cyan]",
        border_style=health_color,
        box=box.ROUNDED
    )
    console.print(summary_panel)
    console.print()


def _get_health_color(score: int) -> str:
    """Get color based on health score."""
    if score >= 80:
        return "green"
    elif score >= 60:
        return "cyan"
    elif score >= 40:
        return "yellow"
    else:
        return "red"


def _create_progress_bar(value: int, width: int = 50) -> str:
    """Create a visual progress bar."""
    filled = int((value / 100) * width)
    empty = width - filled
    color = _get_health_color(value)
    return f"[{color}]{'█' * filled}{'░' * empty}[/{color}] {value}%"


def _format_trend(trend: str) -> str:
    """Format trend with appropriate icon and color."""
    if trend == "improving":
        return "[green]↗ Improving[/green]"
    elif trend == "declining":
        return "[red]↘ Declining[/red]"
    elif trend == "stable":
        return "[cyan]→ Stable[/cyan]"
    else:
        return "[dim]? Insufficient data[/dim]"
