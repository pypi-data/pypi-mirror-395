"""
Implementation of 'stride validate' command.
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ..core.sprint_manager import SprintManager
from ..core.validator import Validator

console = Console()

def validate(
    sprint_id: str = typer.Argument(None, help="ID of the sprint to validate (optional)"),
    all: bool = typer.Option(False, "--all", help="Validate all sprints"),
    strict: bool = typer.Option(False, "--strict", help="Treat warnings as errors"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
):
    """
    Validate the structure and content of sprint documents against templates.
    
    This command checks:
    - Required files exist based on sprint status
    - All required sections are present in each file
    - Template structure compliance
    - Cross-file consistency
    - Content completeness (tasks, acceptance criteria, etc.)
    """
    manager = SprintManager()
    validator = Validator()
    
    sprints_to_validate = []

    if sprint_id:
        sprint = manager.get_sprint(sprint_id)
        if not sprint:
            console.print(f"[red]Sprint '{sprint_id}' not found.[/red]")
            raise typer.Exit(code=1)
        sprints_to_validate.append(sprint)
    elif all:
        sprints_to_validate = manager.list_sprints()
        if not sprints_to_validate:
            console.print("[yellow]No sprints found to validate.[/yellow]")
            return
    else:
        console.print("[yellow]Please provide a sprint ID or use --all[/yellow]")
        console.print("[dim]Example: stride validate SPRINT-ABC12[/dim]")
        console.print("[dim]Example: stride validate --all[/dim]")
        return

    # Summary counters
    total_sprints = len(sprints_to_validate)
    total_errors = 0
    total_warnings = 0
    total_info = 0
    sprints_with_errors = 0
    sprints_with_warnings = 0

    # Validate each sprint
    for sprint in sprints_to_validate:
        console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
        console.print(f"[bold]Validating:[/bold] {sprint.id}")
        console.print(f"[dim]Status: {sprint.status.value.upper()} | Path: {sprint.path}[/dim]")
        console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")
        
        results = validator.validate_sprint(sprint)
        
        errors = results.get("errors", [])
        warnings = results.get("warnings", [])
        info = results.get("info", [])
        
        # Update counters
        total_errors += len(errors)
        total_warnings += len(warnings)
        total_info += len(info)
        
        if errors:
            sprints_with_errors += 1
        if warnings:
            sprints_with_warnings += 1
        
        # Display results
        if not errors and not warnings and not info:
            console.print(Panel(
                "[green]✓[/green] Sprint validation passed with no issues!",
                border_style="green",
                title="[bold green]✓ VALID[/bold green]"
            ))
        else:
            # Show errors
            if errors:
                console.print("[bold red]ERRORS:[/bold red]")
                for i, err in enumerate(errors, 1):
                    console.print(f"  [red]{i}. {err}[/red]")
                console.print()
            
            # Show warnings
            if warnings:
                console.print("[bold yellow]WARNINGS:[/bold yellow]")
                for i, warn in enumerate(warnings, 1):
                    console.print(f"  [yellow]{i}. {warn}[/yellow]")
                console.print()
            
            # Show info (only in verbose mode)
            if verbose and info:
                console.print("[bold cyan]INFO:[/bold cyan]")
                for i, inf in enumerate(info, 1):
                    console.print(f"  [cyan]{i}. {inf}[/cyan]")
                console.print()
            
            # Summary for this sprint
            status_icon = "[red]✗[/red]" if errors else "[yellow]⚠[/yellow]"
            status_text = "FAILED" if errors else "PASSED WITH WARNINGS"
            status_color = "red" if errors else "yellow"
            
            summary = f"{status_icon} {len(errors)} error(s), {len(warnings)} warning(s)"
            if verbose:
                summary += f", {len(info)} info message(s)"
            
            console.print(Panel(
                summary,
                border_style=status_color,
                title=f"[bold {status_color}]{status_text}[/bold {status_color}]"
            ))

    # Overall summary
    if total_sprints > 1:
        console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
        console.print("[bold]VALIDATION SUMMARY[/bold]")
        console.print(f"[bold cyan]{'='*60}[/bold cyan]\n")
        
        table = Table(show_header=True, box=None)
        table.add_column("Metric", style="bold")
        table.add_column("Count", justify="right")
        
        table.add_row("Total Sprints Validated", str(total_sprints))
        table.add_row("Sprints with Errors", f"[red]{sprints_with_errors}[/red]" if sprints_with_errors > 0 else "0")
        table.add_row("Sprints with Warnings", f"[yellow]{sprints_with_warnings}[/yellow]" if sprints_with_warnings > 0 else "0")
        table.add_row("Total Errors", f"[red]{total_errors}[/red]" if total_errors > 0 else "0")
        table.add_row("Total Warnings", f"[yellow]{total_warnings}[/yellow]" if total_warnings > 0 else "0")
        
        if verbose:
            table.add_row("Total Info Messages", f"[cyan]{total_info}[/cyan]" if total_info > 0 else "0")
        
        console.print(table)
        console.print()
        
        # Final status
        if sprints_with_errors > 0:
            console.print(f"[red]✗ {sprints_with_errors} sprint(s) failed validation[/red]")
        else:
            console.print(f"[green]✓ All sprints passed validation[/green]")
            if sprints_with_warnings > 0:
                console.print(f"[yellow]⚠ {sprints_with_warnings} sprint(s) have warnings[/yellow]")

    # Exit with error if there are validation failures
    has_failures = total_errors > 0 or (strict and total_warnings > 0)
    
    if has_failures:
        if strict and total_warnings > 0:
            console.print("\n[red]Validation failed (strict mode: warnings treated as errors)[/red]")
        raise typer.Exit(code=1)
    
    if not verbose and total_info > 0:
        console.print("\n[dim]Tip: Use --verbose to see additional information messages[/dim]")
