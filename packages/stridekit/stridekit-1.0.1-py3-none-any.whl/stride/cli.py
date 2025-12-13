"""
Main Typer application and command registration.
"""

import typer
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from stride import __version__
from stride.commands import init, list, status, show, validate, metrics

# Initialize Typer app
app = typer.Typer(
    name="stride",
    help="Agent-First Framework for Sprint-Powered, Spec-Driven Development",
    add_completion=True,
)

# Initialize Rich console
console = Console()

# Register commands
app.command(name="init")(init.init)
app.command(name="list")(list.list_sprints)
app.command(name="status")(status.status)
app.command(name="show")(show.show)
app.command(name="validate")(validate.validate)
app.command(name="metrics")(metrics.metrics)

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Stride CLI entry point.
    """
    if ctx.invoked_subcommand is None:
        # Generate ASCII art
        f = pyfiglet.Figlet(font='slant')
        title_text = f.renderText('Stride')
        
        # Create and print banner
        panel = Panel(
            Align.center(
                f"[bold red]{title_text}[/bold red]\n"
                f"[dim]v{__version__}[/dim]\n"
                f"[white]Agent-First Framework for Sprint-Powered, Spec-Driven Development[/white]"
            ),
            border_style="yellow",
            padding=(1, 2),
            title="[bold yellow]Welcome[/bold yellow]",
            subtitle="[dim]Run 'stride --help' for commands[/dim]"
        )
        console.print(panel)

    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
