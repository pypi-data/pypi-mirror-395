"""
Implementation of 'stride init' command with beautiful animated UI.
"""

import typer
import questionary
import shutil
import os
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TaskProgressColumn
from rich.layout import Layout
from rich.text import Text
from rich import box
import pyfiglet
from stride import __version__
from ..core.agent_registry import AgentRegistry, AGENT_CATEGORIES, AGENT_ROOT_FILES
from ..core.template_converter import TemplateConverter

console = Console()

def init(
    name: str = typer.Option(None, help="Name of the project (optional)"),
    force: bool = typer.Option(False, "--force", "-f", help="Force re-initialization even if already initialized"),
):
    """
    Initialize a new Stride project in the current directory.
    """
    cwd = Path.cwd()
    stride_dir = cwd / ".stride"
    
    # Check if already initialized
    if stride_dir.exists() and not force:
        console.print("\n[yellow]⚠ Stride project is already initialized in this directory.[/yellow]")
        console.print(f"[dim]Location: {stride_dir}[/dim]\n")
        
        reinit = questionary.confirm(
            "Do you want to add/update agent configurations?",
            default=True
        ).ask()
        
        if not reinit:
            console.print("[dim]Initialization cancelled.[/dim]")
            return
        
        console.print("[cyan]Proceeding with agent configuration...[/cyan]\n")
    
    # 1. Show Banner
    f = pyfiglet.Figlet(font='slant')
    title_text = f.renderText('Stride')
    panel = Panel(
        Align.center(
            f"[bold red]{title_text}[/bold red]\n"
            f"[dim]v{__version__}[/dim]\n"
            f"[white]Agent-First Framework for Sprint-Powered, Spec-Driven Development[/white]"
        ),
        border_style="yellow",
        padding=(1, 2),
        title="[bold yellow]Welcome[/bold yellow]",
    )
    console.print(panel)

    # 2. Interactive Selection
    agent_names = AgentRegistry.get_agent_names()
    # Sort by name, remove Custom (no longer exists)
    sorted_names = sorted([name for name in agent_names.values()])
    
    tools = questionary.checkbox(
        "Select AI Tools to configure:",
        choices=sorted_names,
        style=questionary.Style([
            ('checkbox-selected', 'fg:#00ff00 bold'),
            ('checkbox', 'fg:#858585'),
            ('selected', 'noinherit'),
            ('pointer', 'fg:#00d7ff bold'),
            ('highlighted', 'noinherit'),
        ])
    ).ask()

    if not tools:
        console.print("[yellow]No tools selected. Proceeding with basic setup...[/yellow]")
        tools = []

    # 3. Base Scaffold
    sprints_dir = stride_dir / "sprints"
    templates_dir = stride_dir / "templates"
    
    # Create directories
    stride_dir.mkdir(exist_ok=True)
    sprints_dir.mkdir(exist_ok=True)
    
    # Copy Templates
    pkg_templates_dir = Path(__file__).parent.parent / "templates" / "sprint_files"
    if pkg_templates_dir.exists():
        if templates_dir.exists():
            shutil.rmtree(templates_dir)
        shutil.copytree(pkg_templates_dir, templates_dir)
    
    # Note: project.md is NOT created during init
    # It should be created by the agent via /stride-init command

    # Create AGENTS.md files
    agents_docs_dir = Path(__file__).parent.parent / "templates" / "agents_docs"
    
    internal_agents_md = stride_dir / "AGENTS.md"
    if not internal_agents_md.exists() and (agents_docs_dir / "internal.md").exists():
        shutil.copy(agents_docs_dir / "internal.md", internal_agents_md)
        
    root_agents_md = cwd / "AGENTS.md"
    if not root_agents_md.exists() and (agents_docs_dir / "root.md").exists():
        shutil.copy(agents_docs_dir / "root.md", root_agents_md)

    console.print("[green]✓ Base project structure created[/green]")

    # 4. Tool-Specific Setup with Animation
    if tools:
        console.print("\n[bold cyan]🤖 Configuring AI Agents...[/bold cyan]\n")
        
        agent_commands_dir = Path(__file__).parent.parent / "templates" / "agent_commands"
        
        # Command files to copy
        command_files = [
            "init", "derive", "lite", "status", "plan",
            "present", "implement", "feedback", "review", "complete",
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            for tool_name in tools:
                try:
                    # Get agent config
                    agent_config = AgentRegistry.get_agent_by_name(tool_name)
                    
                    # Create task
                    task = progress.add_task(f"[cyan]Setting up {agent_config.name}...", total=None)
                    
                    # Determine target directory
                    if "global-install" in agent_config.special_handling:
                        agent_dir = _get_global_install_path(agent_config)
                    else:
                        agent_dir = cwd / agent_config.directory
                    
                    # Create agent directory
                    agent_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Copy and convert command files
                    for cmd_file in command_files:
                        src_path = agent_commands_dir / f"{cmd_file}.md"
                        
                        if not src_path.exists():
                            continue
                        
                        # Read template content
                        content = src_path.read_text(encoding="utf-8")
                        
                        # Convert to agent-specific format
                        converted_content = TemplateConverter.convert(
                            content=content,
                            format_type=agent_config.format_type,
                            command_name=cmd_file,
                            agent_key=agent_config.key
                        )
                        
                        # Determine destination filename using pattern
                        dest_name = agent_config.filename_pattern.format(command=cmd_file) + agent_config.extension
                        
                        dest_path = agent_dir / dest_name
                        dest_path.write_text(converted_content, encoding="utf-8")
                    
                    # Special handling for archive rewrite (OpenCode)
                    if "archive-rewrite" in agent_config.special_handling:
                        _handle_archive_rewrite(agent_dir, agent_config, agent_commands_dir)
                    
                    # Special handling for specific agents that need root-level .md files
                    if agent_config.key in AGENT_ROOT_FILES:
                        root_filename = AGENT_ROOT_FILES[agent_config.key]
                        root_file = cwd / root_filename
                        agents_md = cwd / "AGENTS.md"
                        
                        if not root_file.exists() and agents_md.exists():
                            shutil.copy(agents_md, root_file)
                    
                    # Update task as complete
                    progress.update(task, description=f"[green]✓ {agent_config.name} configured[/green]")
                    time.sleep(0.15)  # Brief pause for visual effect
                    
                except KeyError as e:
                    progress.update(task, description=f"[red]✗ {tool_name} failed: {e}[/red]")
                except Exception as e:
                    progress.update(task, description=f"[red]✗ {tool_name} failed: {str(e)}[/red]")

    console.print(f"\n[bold green]✨ Stride project initialized successfully![/bold green]")
    
    if tools:
        console.print("\n[bold cyan]📖 How Stride Works:[/bold cyan]")
        console.print("  Stride uses sprints to organize your development. Each sprint has specs,")
        console.print("  plans, and implementation tracking.\n")
        
        console.print("[bold]Agent Commands[/bold] (use inside your AI agent):")
        console.print("  [cyan]init[/cyan]       - Create project spec and start first sprint")
        console.print("  [cyan]plan[/cyan]       - Define sprint goals and break down tasks")
        console.print("  [cyan]implement[/cyan]  - Build features with implementation tracking")
        console.print("  [cyan]status[/cyan]     - Check current sprint progress")
        console.print("  [cyan]review[/cyan]     - Validate work and gather feedback")
        console.print("  [cyan]complete[/cyan]   - Archive sprint and document learnings")
        console.print("  [cyan]present[/cyan]    - Generate sprint presentations")
        console.print("  [cyan]derive[/cyan]     - Create new sprints from existing ones")
        console.print("  [cyan]lite[/cyan]       - Quick reference to all commands")
        console.print("  [cyan]feedback[/cyan]   - Collect and organize feedback\n")
        
        console.print("[bold]CLI Commands[/bold] (run in your terminal):")
        console.print("  [green]stride list[/green]     - View all sprints")
        console.print("  [green]stride show[/green]     - Display sprint details")
        console.print("  [green]stride status[/green]   - Check project status")
        console.print("  [green]stride validate[/green] - Verify project structure")
        console.print("  [green]stride metrics[/green]  - Sprint analytics and statistics\n")
        
        console.print("[bold cyan]🚀 Ready to Start?[/bold cyan]")
        console.print("  Open your AI agent and run the [bold cyan]init[/bold cyan] command to begin!\n")
        console.print("[dim]Tip: See AGENTS.md for agent-specific command syntax[/dim]")

def _get_global_install_path(agent_config: AgentRegistry) -> Path:
    """
    Get global installation path for agents like Codex.
    Checks $CODEX_HOME environment variable first, falls back to ~/.codex
    
    Args:
        agent_config: Agent configuration
        
    Returns:
        Path to global installation directory
    """
    if agent_config.key == "codex":
        # Check for CODEX_HOME environment variable
        codex_home = os.environ.get("CODEX_HOME")
        if codex_home:
            return Path(codex_home) / "prompts"
        else:
            # Default to ~/.codex/prompts
            return Path.home() / ".codex" / "prompts"
    
    # Default fallback
    return Path(agent_config.directory.replace("~/", str(Path.home()) + "/"))


def _handle_archive_rewrite(agent_dir: Path, agent_config: AgentRegistry, templates_dir: Path):
    """
    Special handler for OpenCode archive command rewrite.
    Completely rewrites the archive file to ensure proper formatting.
    
    Args:
        agent_dir: Agent directory path
        agent_config: Agent configuration
        templates_dir: Templates directory
    """
    archive_template = templates_dir / "complete.md"
    if not archive_template.exists():
        return
    
    # Read and convert archive template
    content = archive_template.read_text(encoding="utf-8")
    converted = TemplateConverter.convert(
        content=content,
        format_type=agent_config.format_type,
        command_name="complete",
        agent_key=agent_config.key
    )
    
    # Write complete file using filename_pattern (overwrites any existing version)
    dest_name = agent_config.filename_pattern.format(command="complete") + agent_config.extension
    archive_file = agent_dir / dest_name
    archive_file.write_text(converted, encoding="utf-8")

